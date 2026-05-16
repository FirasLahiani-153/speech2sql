"""
stt_linto.py
------------
Speech-to-Text using the LinTO Vosk model (Tunisian Arabic dialect).
Handles model download, audio recording, and transcription.
"""

import json
import wave
import zipfile
import logging
from pathlib import Path
from typing import Union

import sounddevice as sd
import soundfile as sf
from vosk import Model, KaldiRecognizer
from huggingface_hub import hf_hub_download

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

SAMPLE_RATE: int = 16000
DEFAULT_DURATION: int = 5
CHUNK_SIZE: int = 4000

OUTPUT_FILE = Path(__file__).parent / ".." / "Audio_records" / "recorded_audio.wav"
MODEL_DIR   = Path(__file__).parent / ".." / "models" / "linto-asr-ar-tn-0.1" / "vosk-model"

HF_REPO_ID  = "linagora/linto-asr-ar-tn-0.1"
HF_FILENAME = "vosk-model.zip"

# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def _download_and_extract_model(model_dir: Path) -> None:

    log.info("Downloading LinTO Vosk model from HuggingFace...")
    zip_path = hf_hub_download(repo_id=HF_REPO_ID, filename=HF_FILENAME)

    extract_dir = model_dir.parent
    extract_dir.mkdir(parents=True, exist_ok=True)

    log.info("Extracting model to %s ...", extract_dir)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)
    log.info("Model extracted successfully.")


def load_model(model_dir: Path = MODEL_DIR) -> Model:

    model_dir = Path(model_dir)
    if not model_dir.exists():
        _download_and_extract_model(model_dir)

    log.info("Loading LinTO Vosk model from %s ...", model_dir)
    model = Model(str(model_dir))
    log.info("LinTO Vosk model ready.")
    return model


# ---------------------------------------------------------------------------
# Audio helpers
# ---------------------------------------------------------------------------

def record_audio(
    duration: int = DEFAULT_DURATION,
    output_file: Path = OUTPUT_FILE,
) -> tuple[list, int]:
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    log.info("Recording for %d second(s) — speak now!", duration)
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()

    sf.write(str(output_file), audio, SAMPLE_RATE)
    log.info("Audio saved to %s", output_file)
    return audio.flatten(), SAMPLE_RATE


def load_audio(path: Union[str, Path]) -> tuple[list, int]:

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    audio_array, sr = sf.read(str(path), dtype="float32")
    if audio_array.ndim > 1:
        audio_array = audio_array[:, 0]

    return audio_array, sr


def _validate_wav(wf: wave.Wave_read) -> None:
    if wf.getnchannels() != 1:
        raise ValueError(
            "Audio must be mono (1 channel). "
            "Convert with: ffmpeg -i input.wav -ac 1 output.wav"
        )
    if wf.getframerate() != 16000:
        raise ValueError(
            f"Audio must be 16 000 Hz (got {wf.getframerate()} Hz). "
            "Convert with: ffmpeg -i input.wav -ar 16000 output.wav"
        )


def transcribe(
    audio_input: Union[tuple, str, Path],
    model: Model,
) -> str:
    # Vosk requires a WAV file — save tuple to disk first if needed
    if isinstance(audio_input, tuple):
        array, sr = audio_input
        sf.write(str(OUTPUT_FILE), array, sr)
        audio_path = OUTPUT_FILE
    else:
        audio_path = Path(audio_input)

    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    parts: list[str] = []

    with wave.open(str(audio_path), "rb") as wf:
        _validate_wav(wf)
        rec = KaldiRecognizer(model, wf.getframerate())

        while True:
            data = wf.readframes(CHUNK_SIZE)
            if not data:
                break
            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result()).get("text", "").strip()
                if text:
                    parts.append(text)

        final = json.loads(rec.FinalResult()).get("text", "").strip()
        if final:
            parts.append(final)

    return " ".join(parts)

def record_and_transcribe(
    model: Model,
    duration: int = DEFAULT_DURATION,
    output_file: Path = OUTPUT_FILE,
) -> str:
    audio_tuple = record_audio(duration=duration, output_file=output_file)
    return transcribe(audio_tuple, model)



