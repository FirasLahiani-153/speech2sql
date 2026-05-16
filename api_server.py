"""
╔════════════════════════════════════════════════════════════════════╗
║                    Speech2SQL RESTful AI Agent API                 ║
║                                                                    ║
║  Unified REST API for multi-platform access (web, mobile, desktop) ║
║  Converts Speech2SQL orchestrator into a cloud-ready AI service    ║
╚════════════════════════════════════════════════════════════════════╝

Usage:
    python api_server.py              # Start on http://localhost:5001
    curl http://localhost:5001/health # Check status

Endpoints:
    POST /api/v1/transcribe  - Speech to text (audio → Arabic)
    POST /api/v1/rewrite     - Arabic to English (Arabic → English)
    POST /api/v1/sql         - Generate SQL (question → SQL)
    POST /api/v1/execute     - Execute SQL query
    POST /api/v1/pipeline    - Full pipeline (speech/text → SQL → results)
    GET  /api/v1/health      - Health check
    GET  /api/v1/models      - Available models & capabilities
"""

import os
import sys
import json
import traceback
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Tuple

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import numpy as np

# Add Speech2sql to path
Speech2sql_PATH = Path(__file__).parent / "Speech2sql"
sys.path.insert(0, str(Speech2sql_PATH))

print(f"\n[INIT] Adding to path: {Speech2sql_PATH}")

# ════════════════════════════════════════════════════════════════════
#    IMPORT Speech2sql COMPONENTS
# ════════════════════════════════════════════════════════════════════

LINTO_MODEL_ID = "linagora/linto-asr-ar-tn-0.1"
try:
    from Speech2sql.modalities.speech import (
        transcribe,
        load_model as load_stt_model,
        record_audio,
        DEFAULT_DURATION,
        HF_REPO_ID as LINTO_MODEL_ID,
    )
    print("[✓] Speech (STT) components loaded")
except Exception as e:
    print(f"[✗] Speech components failed: {e}")
    load_stt_model = None
    transcribe = None

try:
    from Speech2sql.agent.orchestrator import (
        step2_rewrite,
        step3_generate_sql,
        step4_execute_sql,
        memory,
    )
    print("[✓] Agent (Orchestrator) components loaded")
except Exception as e:
    print(f"[✗] Agent components failed: {e}")
    traceback.print_exc()

try:
    from Speech2sql.modalities.preprocess import (
        preprocess_transcription,
        detect_script,
        TranscriptionError,
    )
    print("[✓] Preprocessing components loaded")
except Exception as e:
    print(f"[✗] Preprocessing components failed: {e}")

# ════════════════════════════════════════════════════════════════════
#    CONFIGURATION
# ════════════════════════════════════════════════════════════════════

API_VERSION = "1.0.0"
API_PORT = int(os.getenv("API_PORT", 5001))
API_HOST = os.getenv("API_HOST", "0.0.0.0")

# Model info
STT_MODEL = None
STT_MODEL_NAME = LINTO_MODEL_ID if LINTO_MODEL_ID else "linagora/linto-asr-ar-tn-0.1"
LLM_MODEL = "anthropic/claude-3-haiku"

# Ensure logs directory exists
LOGS_DIR = Path(__file__).parent / "api_logs"
LOGS_DIR.mkdir(exist_ok=True)

# ════════════════════════════════════════════════════════════════════
#    INITIALIZE MODELS
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("  INITIALIZING Speech2sql API SERVER")
print("=" * 70)

print("\n[1/2] Loading STT Model (LinTO Vosk)...")
if load_stt_model:
    try:
        STT_MODEL = load_stt_model()
        print(f"  [✓] STT Model loaded: {STT_MODEL_NAME}")
    except Exception as e:
        print(f"  [✗] STT Model failed: {e}")
        STT_MODEL = None
else:
    print("  [!] STT not available (speech disabled)")

print("\n[2/2] Verifying LLM & RAG...")
try:
    # Test by importing components
    from Speech2sql.llm.client import llm
    from Speech2sql.rag.retrieve_rag import get_context_for_question
    from Speech2sql.llm.client import retriever

    print(f"  [✓] LLM ready: {LLM_MODEL}")
    print(f"  [✓] RAG ready: FAISS vector store")
except Exception as e:
    print(f"  [✗] LLM/RAG failed: {e}")

print("\n" + "=" * 70)
print(f"  API Server ready on http://{API_HOST}:{API_PORT}")
print("=" * 70 + "\n")

# ════════════════════════════════════════════════════════════════════
#    FLASK APP
# ════════════════════════════════════════════════════════════════════

app = Flask(__name__)
CORS(app)

# ────────────────────────────────────────────────────────────────────
#    HEALTH & INFO ENDPOINTS
# ────────────────────────────────────────────────────────────────────


@app.route("/api/v1/health", methods=["GET"])
def health():
    """Check API and component status."""
    return jsonify(
        {
            "status": "healthy",
            "version": API_VERSION,
            "timestamp": datetime.now().isoformat(),
            "components": {
                "stt": "ready" if STT_MODEL else "disabled",
                "llm": "ready",
                "rag": "ready",
            },
            "models": {
                "stt_model": STT_MODEL_NAME,
                "llm_model": LLM_MODEL,
            },
        }
    )


@app.route("/api/v1/models", methods=["GET"])
def models_info():
    """Get available models and capabilities."""
    return jsonify(
        {
            "api_version": API_VERSION,
            "models": {
                "stt": {
                    "name": STT_MODEL_NAME,
                    "type": "Speech-to-Text (ASR)",
                    "language": "Arabic (Tunisian dialect)",
                    "status": "available" if STT_MODEL else "unavailable",
                },
                "nlp": {
                    "name": LLM_MODEL,
                    "type": "Language Model",
                    "capabilities": ["text-rewriting", "sql-generation"],
                    "status": "available",
                },
                "rag": {
                    "name": "FAISS + all-MiniLM-L6-v2",
                    "type": "Vector Database",
                    "capability": "Contextual SQL generation",
                    "status": "available",
                },
            },
            "endpoints": {
                "transcribe": "POST /api/v1/transcribe",
                "rewrite": "POST /api/v1/rewrite",
                "sql": "POST /api/v1/sql",
                "execute": "POST /api/v1/execute",
                "pipeline": "POST /api/v1/pipeline",
            },
        }
    )


# ────────────────────────────────────────────────────────────────────
#    STEP 1: TRANSCRIBE (Speech → Arabic)
# ────────────────────────────────────────────────────────────────────


@app.route("/api/v1/transcribe", methods=["POST"])
def transcribe_endpoint():
    """
    Transcribe audio to Arabic text.

    Request: FormData with 'audio' file OR JSON with 'audio_path'
    Response: { arabic_text, script, timings }
    """
    try:
        if not STT_MODEL:
            return jsonify({"error": "STT not available"}), 503

        # Get audio input
        audio_input = None

        if "audio" in request.files:
            # Audio file uploaded
            audio_file = request.files["audio"]
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
                audio_file.save(tmp.name)
                audio_input = tmp.name
        elif request.is_json:
            data = request.get_json()
            if "audio_path" in data:
                audio_path = data["audio_path"]
                if not os.path.exists(audio_path):
                    return jsonify({"error": f"Audio file not found: {audio_path}"}), 400
                audio_input = audio_path
            else:
                return jsonify({"error": "No audio provided"}), 400
        else:
            return jsonify({"error": "No audio file or path provided"}), 400

        # Transcribe
        import time

        t0 = time.time()
        arabic_text = transcribe(audio_input, STT_MODEL)
        transcribe_time = time.time() - t0

        # Preprocess
        try:
            arabic_text = preprocess_transcription(arabic_text)
        except TranscriptionError as e:
            return jsonify({"error": f"Transcription failed: {e}"}), 400

        script = detect_script(arabic_text)

        # Clean up temp file
        if "audio" in request.files and audio_input and os.path.exists(audio_input):
            try:
                os.unlink(audio_input)
            except:
                pass

        return jsonify(
            {
                "success": True,
                "arabic_text": arabic_text,
                "script": script,
                "timings": {"transcribe": round(transcribe_time, 2)},
            }
        )

    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500


# ────────────────────────────────────────────────────────────────────
#    STEP 2: REWRITE (Arabic → English)
# ────────────────────────────────────────────────────────────────────


@app.route("/api/v1/rewrite", methods=["POST"])
def rewrite_endpoint():
    """
    Rewrite Tunisian Arabic to formal English.

    Request: { "arabic_text": "..." }
    Response: { english_text, timings }
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        arabic_text = data.get("arabic_text", "").strip()

        if not arabic_text:
            return jsonify({"error": "No arabic_text provided"}), 400

        import time

        t0 = time.time()
        english_text = step2_rewrite(arabic_text)
        rewrite_time = time.time() - t0

        return jsonify(
            {
                "success": True,
                "arabic_text": arabic_text,
                "english_text": english_text,
                "timings": {"rewrite": round(rewrite_time, 2)},
            }
        )

    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500


# ────────────────────────────────────────────────────────────────────
#    STEP 3: GENERATE SQL (Question → SQL)
# ────────────────────────────────────────────────────────────────────


@app.route("/api/v1/sql", methods=["POST"])
def sql_endpoint():
    """
    Generate SQL from natural language question.

    Request: { "question": "...", "language": "en|ar" (optional) }
    Response: { sql, timings }
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "No question provided"}), 400

        import time

        t0 = time.time()
        sql_query = step3_generate_sql(question)
        sql_time = time.time() - t0

        return jsonify(
            {
                "success": True,
                "question": question,
                "sql": sql_query,
                "timings": {"sql_generation": round(sql_time, 2)},
            }
        )

    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500


# ────────────────────────────────────────────────────────────────────
#    STEP 4: EXECUTE SQL (SQL → Results)
# ────────────────────────────────────────────────────────────────────


@app.route("/api/v1/execute", methods=["POST"])
def execute_endpoint():
    """
    Execute SQL query and return results.

    Request: { "sql": "SELECT ...", "limit": 100 (optional) }
    Response: { columns, rows, row_count, timings }
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        sql_query = data.get("sql", "").strip()

        if not sql_query:
            return jsonify({"error": "No SQL provided"}), 400

        import time

        t0 = time.time()
        output = step4_execute_sql(sql_query)
        exec_time = time.time() - t0

        # Parse output
        if isinstance(output, str):
            # Error
            return jsonify(
                {
                    "success": False,
                    "error": output,
                    "sql": sql_query,
                    "timings": {"execution": round(exec_time, 2)},
                }
            )
        else:
            # Success
            columns, rows = output
            # Convert rows (tuples) to dicts for JSON serialization
            row_dicts = []
            for row in rows:
                if isinstance(row, dict):
                    row_dicts.append(row)
                elif isinstance(row, (tuple, list)):
                    # Convert tuple/list to dict using columns as keys
                    row_dicts.append(dict(zip(columns, row)))
                else:
                    row_dicts.append(row)

            return jsonify(
                {
                    "success": True,
                    "sql": sql_query,
                    "columns": columns,
                    "rows": row_dicts,
                    "row_count": len(row_dicts),
                    "timings": {"execution": round(exec_time, 2)},
                }
            )

    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500


# ────────────────────────────────────────────────────────────────────
#    FULL PIPELINE (Speech/Text → SQL → Results)
# ────────────────────────────────────────────────────────────────────


@app.route("/api/v1/pipeline", methods=["POST"])
def pipeline_endpoint():
    """
    Full speech-to-SQL pipeline in one request.

    Request: Either
      { "audio_file": (FormData), language: "ar" } for speech input
      { "text": "...", "language": "en|ar" } for text input

    Response: { question, english_text, sql, columns, rows, row_count, timings, success }
    """
    try:
        import time

        total_start = time.time()
        timings = {}
        result = {
            "success": False,
            "steps": {},
            "timings": {},
        }

        # ── STEP 1: Get question (speech or text) ──
        question = ""
        arabic_text = ""
        english_text = ""

        if "audio" in request.files:
            # Speech input
            if not STT_MODEL:
                return jsonify({"error": "STT not available"}), 503

            audio_file = request.files["audio"]
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
                audio_file.save(tmp.name)
                audio_input = tmp.name

            t0 = time.time()
            arabic_text = transcribe(audio_input, STT_MODEL)
            timings["transcribe"] = round(time.time() - t0, 2)

            try:
                arabic_text = preprocess_transcription(arabic_text)
            except TranscriptionError as e:
                return jsonify({"error": f"Transcription failed: {e}"}), 400

            result["steps"]["transcription"] = {
                "arabic_text": arabic_text,
                "script": detect_script(arabic_text),
            }

            question = arabic_text

            # Step 2: Rewrite to English
            t0 = time.time()
            english_text = step2_rewrite(arabic_text)
            timings["rewrite"] = round(time.time() - t0, 2)
            result["steps"]["rewrite"] = {"english_text": english_text}

            question = english_text

            # Clean up
            try:
                os.unlink(audio_input)
            except:
                pass

        elif request.is_json:
            # Text input
            data = request.get_json()
            text_input = data.get("text", "").strip()
            language = data.get("language", "en").lower()

            if not text_input:
                return jsonify({"error": "No text or audio provided"}), 400

            if language == "ar":
                # Arabic input - rewrite to English
                arabic_text = text_input
                t0 = time.time()
                english_text = step2_rewrite(arabic_text)
                timings["rewrite"] = round(time.time() - t0, 2)
                question = english_text
            else:
                # English input - use directly
                english_text = text_input
                question = text_input

            result["steps"]["input"] = {
                "text": text_input,
                "language": language,
            }
        else:
            return jsonify({"error": "No audio file or text provided"}), 400

        # ── STEP 3: Generate SQL ──
        t0 = time.time()
        sql_query = step3_generate_sql(question)
        timings["sql_generation"] = round(time.time() - t0, 2)
        result["steps"]["sql_generation"] = {"sql": sql_query}

        # ── STEP 4: Execute SQL ──
        t0 = time.time()
        output = step4_execute_sql(sql_query, arabic_text, english_text)
        timings["execution"] = round(time.time() - t0, 2)

        if isinstance(output, str):
            # Error
            result["error"] = output
            result["success"] = False
        else:
            # Success
            columns, rows = output
            # Convert rows (tuples) to dicts for JSON serialization
            row_dicts = []
            for row in rows:
                if isinstance(row, dict):
                    row_dicts.append(row)
                elif isinstance(row, (tuple, list)):
                    # Convert tuple/list to dict using columns as keys
                    row_dicts.append(dict(zip(columns, row)))
                else:
                    row_dicts.append(row)

            result["success"] = True
            result["steps"]["execution"] = {
                "columns": columns,
                "row_count": len(row_dicts),
            }
            result["columns"] = columns
            result["rows"] = row_dicts
            result["row_count"] = len(row_dicts)

        # Add timing info
        total_time = time.time() - total_start
        result["timings"] = timings
        result["timings"]["total"] = round(total_time, 2)

        return jsonify(result)

    except Exception as e:
        return jsonify(
            {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
            }
        ), 500


# ────────────────────────────────────────────────────────────────────
#    ERROR HANDLERS
# ────────────────────────────────────────────────────────────────────


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify(
            {
                "error": "Not found",
                "message": f"Endpoint not found. Check /api/v1/models for available endpoints.",
            }
        ),
        404,
    )


@app.errorhandler(500)
def internal_error(error):
    return (
        jsonify(
            {
                "error": "Internal server error",
                "message": str(error),
            }
        ),
        500,
    )


# ════════════════════════════════════════════════════════════════════
#    START SERVER
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'═' * 70}")
    print(f"  API Server Starting")
    print(f"{'═' * 70}\n")
    print(f"  Base URL:    http://{API_HOST}:{API_PORT}")
    print(f"  Health:      http://{API_HOST}:{API_PORT}/api/v1/health")
    print(f"  Models:      http://{API_HOST}:{API_PORT}/api/v1/models")
    print(f"\n  Try: curl http://localhost:{API_PORT}/api/v1/health\n")

    # Support Render.com's dynamic port assignment
    port = int(os.getenv("PORT", API_PORT))
    app.run(host=API_HOST, port=port, debug=False, threaded=True)
