import re


class TranscriptionError(Exception):
    pass


# ── 1. ASR noise & artifacts ─────────────────────────────────────────────────
# Whisper hallucination tags: [BLANK_AUDIO], [MUSIC], (inaudible), etc.
_ARTIFACT_PATTERN = re.compile(r'\[.*?\]|\(.*?\)', re.UNICODE)

# ── 2. Arabic character normalization ────────────────────────────────────────
# Arabic diacritics (tashkeel): U+064B–U+065F and U+0670
_DIACRITICS_PATTERN = re.compile(r'[ً-ٰٟ]')

# Alef variants → plain alef ا
_ALEF_VARIANTS = str.maketrans({'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ٱ': 'ا'})

# Arabic punctuation → ASCII equivalents
_ARABIC_PUNCT = str.maketrans({'،': ',', '؟': '?', '؛': ';'})

# Arabic-Indic numerals → ASCII digits (e.g. ١٢٣ → 123)
_ARABIC_INDIC = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')

# ── 3. Tunisian dialect variations ───────────────────────────────────────────
# Cap character elongation at 2 repetitions (e.g. "برررشا" → "بررشا")
_ELONGATION = re.compile(r'(.)\1{2,}', re.UNICODE)

# Common Tunisian dialect words → MSA equivalents, applied before the LLM.
# Key case: نحب means "I love" in MSA but "I want" in Tunisian — must disambiguate.
_DIALECT_MAP = [
    (re.compile(r'\bهاذا\b'),              'هذا'),
    (re.compile(r'\bهاذي\b'),              'هذه'),
    (re.compile(r'\bهاذو\b'),              'هؤلاء'),
    (re.compile(r'\bكيفاش\b'),             'كيف'),
    (re.compile(r'\bوقتاش\b'),             'متى'),
    (re.compile(r'\bعلاش\b'),              'لماذا'),
    (re.compile(r'\bقدّاش\b|\bقداش\b'),    'كم'),
    (re.compile(r'\bشكون\b'),              'من'),
    (re.compile(r'\bوين\b'),               'أين'),
    (re.compile(r'\bنحب\b'),               'أريد'),   # "I love" (MSA) → "I want" (Tunisian)
    (re.compile(r'\bبرشا\b'),              'كثير'),
    (re.compile(r'\bتوا\b'),               'الآن'),
    (re.compile(r'\bباش\b'),               'لكي'),
    (re.compile(r'\bلازم\b'),              'يجب'),
    (re.compile(r'\bفما\b'),               'يوجد'),
    (re.compile(r'\bورّيني\b|\bوريني\b'),  'أرني'),
    (re.compile(r'\bعطيني\b|\bأعطيني\b'),  'أعطني'),
    (re.compile(r'\bالكل\b'),              'الجميع'),
]

# ── 4. Code-switching detection ──────────────────────────────────────────────
_RE_ARABIC = re.compile(r'[؀-ۿ]')
_RE_LATIN  = re.compile(r'[a-zA-Z]')


def detect_script(text: str) -> str:
    """Returns 'arabic', 'latin', or 'mixed'."""
    has_arabic = bool(_RE_ARABIC.search(text))
    has_latin  = bool(_RE_LATIN.search(text))
    if has_arabic and has_latin:
        return 'mixed'
    return 'arabic' if has_arabic else 'latin'


def preprocess_transcription(text: str) -> str:
    if not text or not text.strip():
        raise TranscriptionError("Empty transcription — no speech detected.")

    # 1. Remove Whisper artifact tags
    text = _ARTIFACT_PATTERN.sub('', text)

    # 2. Arabic character normalization
    text = text.translate(_ALEF_VARIANTS)
    text = _DIACRITICS_PATTERN.sub('', text)
    text = text.translate(_ARABIC_PUNCT)
    text = text.translate(_ARABIC_INDIC)

    # 3. Tunisian dialect normalization (Latin/French tokens are untouched)
    text = _ELONGATION.sub(r'\1\1', text)
    for pattern, replacement in _DIALECT_MAP:
        text = pattern.sub(replacement, text)

    # 4. Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    if len(text) < 3:
        raise TranscriptionError(f"Transcription too short to process: '{text}'")

    return text
