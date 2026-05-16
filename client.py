"""
╔════════════════════════════════════════════════════════════════════╗
║              Tounsi2SQL Python Client Library                      ║
║                                                                    ║
║  Simple SDK for calling the Tounsi2SQL API from any Python app    ║
║  Works with mobile, desktop, web, and server-side applications    ║
╚════════════════════════════════════════════════════════════════════╝

Usage:
    from client import Tounsi2SQLClient

    client = Tounsi2SQLClient(base_url="http://localhost:5001")

    # Full pipeline
    result = client.pipeline(text="List all airlines", language="en")
    print(result['rows'])

    # Or step by step
    sql = client.sql_generate("How many flights today?")
    results = client.execute(sql)
"""

import requests
import json
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path


class Tounsi2SQLClient:
    """Python client for Tounsi2SQL API."""

    def __init__(self, base_url: str = "http://localhost:5001", timeout: int = 30):
        """
        Initialize client.

        Args:
            base_url: API server URL (default: local)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.api_version = "v1"

    def _request(
        self, method: str, endpoint: str, data: Optional[Dict] = None, files=None
    ) -> Dict[str, Any]:
        """Make HTTP request to API."""
        url = f"{self.base_url}/api/{self.api_version}/{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, timeout=self.timeout)
            elif method == "POST":
                if files:
                    response = requests.post(
                        url, files=files, timeout=self.timeout
                    )
                else:
                    response = requests.post(
                        url,
                        json=data,
                        headers={"Content-Type": "application/json"},
                        timeout=self.timeout,
                    )
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": f"Cannot connect to API at {self.base_url}",
            }
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timeout"}
        except requests.exceptions.HTTPError as e:
            try:
                return e.response.json()
            except:
                return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ────────────────────────────────────────────────────────────────
    #    HEALTH & INFO
    # ────────────────────────────────────────────────────────────────

    def health(self) -> Dict[str, Any]:
        """Check API health."""
        return self._request("GET", "health")

    def models(self) -> Dict[str, Any]:
        """Get available models info."""
        return self._request("GET", "models")

    # ────────────────────────────────────────────────────────────────
    #    STEP-BY-STEP API
    # ────────────────────────────────────────────────────────────────

    def transcribe(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe audio file to Arabic text.

        Args:
            audio_path: Path to audio file (.webm, .wav, .mp3, etc.)

        Returns:
            { success, arabic_text, script, timings }
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            return {"success": False, "error": f"File not found: {audio_path}"}

        with open(audio_path, "rb") as f:
            files = {"audio": f}
            return self._request("POST", "transcribe", files=files)

    def rewrite(self, arabic_text: str) -> Dict[str, Any]:
        """
        Rewrite Tunisian Arabic to formal English.

        Args:
            arabic_text: Arabic question

        Returns:
            { success, arabic_text, english_text, timings }
        """
        return self._request("POST", "rewrite", {"arabic_text": arabic_text})

    def sql_generate(self, question: str) -> str:
        """
        Generate SQL from natural language question.

        Args:
            question: Question in English or Arabic

        Returns:
            SQL query string (or error message)
        """
        result = self._request("POST", "sql", {"question": question})

        if result.get("success"):
            return result.get("sql", "")
        else:
            raise Exception(result.get("error", "SQL generation failed"))

    def execute(self, sql: str) -> Tuple[List[str], List[Dict]]:
        """
        Execute SQL query.

        Args:
            sql: SQL query

        Returns:
            (columns, rows) tuple
        """
        result = self._request("POST", "execute", {"sql": sql})

        if result.get("success"):
            return result.get("columns", []), result.get("rows", [])
        else:
            raise Exception(result.get("error", "SQL execution failed"))

    # ────────────────────────────────────────────────────────────────
    #    HIGH-LEVEL API (Full Pipeline)
    # ────────────────────────────────────────────────────────────────

    def pipeline_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Full pipeline: Audio → Text → SQL → Results.

        Args:
            audio_path: Path to audio file

        Returns:
            {
                success: bool,
                steps: { transcription, rewrite, sql_generation, execution },
                rows: list,
                timings: dict,
            }
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            return {"success": False, "error": f"File not found: {audio_path}"}

        with open(audio_path, "rb") as f:
            files = {"audio": f}
            return self._request("POST", "pipeline", files=files)

    def pipeline(
        self, text: str, language: str = "en"
    ) -> Dict[str, Any]:
        """
        Full pipeline: Text → SQL → Results.

        Args:
            text: Question in English or Arabic
            language: "en" (English) or "ar" (Arabic)

        Returns:
            {
                success: bool,
                steps: { input, [rewrite], sql_generation, execution },
                columns: list,
                rows: list,
                row_count: int,
                timings: dict,
            }
        """
        return self._request(
            "POST", "pipeline", {"text": text, "language": language}
        )

    # ────────────────────────────────────────────────────────────────
    #    CONVENIENCE METHODS
    # ────────────────────────────────────────────────────────────────

    def query(self, question: str, language: str = "en") -> Dict[str, Any]:
        """
        Simple query: question → SQL → results.

        Args:
            question: Your question in English or Arabic
            language: "en" or "ar"

        Returns:
            { success, rows, columns, sql }
        """
        result = self.pipeline(text=question, language=language)

        return {
            "success": result.get("success", False),
            "rows": result.get("rows", []),
            "columns": result.get("columns", []),
            "row_count": result.get("row_count", 0),
            "sql": result.get("steps", {}).get("sql_generation", {}).get("sql", ""),
            "error": result.get("error"),
            "timings": result.get("timings", {}),
        }

    def explain(self, question: str) -> str:
        """Just generate SQL without executing."""
        try:
            return self.sql_generate(question)
        except Exception as e:
            return f"Error: {e}"


# ════════════════════════════════════════════════════════════════════
#    EXAMPLE USAGE
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  Tounsi2SQL Python Client - Examples")
    print("=" * 70 + "\n")

    client = Tounsi2SQLClient("http://localhost:5001")

    # Check health
    print("[1] Health Check:")
    health = client.health()
    print(f"    Status: {health.get('status', 'unknown')}")
    print(f"    STT:    {health.get('components', {}).get('stt', 'unknown')}")
    print(f"    LLM:    {health.get('components', {}).get('llm', 'unknown')}\n")

    # Simple query
    print("[2] Simple Query (English):")
    result = client.query("List all airlines")
    print(f"    Success:    {result['success']}")
    print(f"    Rows:       {result['row_count']}")
    print(f"    Time:       {result['timings'].get('total', 0):.2f}s")
    if result['rows']:
        print(f"    First row:  {result['rows'][0]}\n")

    # Get SQL only
    print("[3] SQL Generation Only:")
    sql = client.explain("How many customers from USA?")
    print(f"    SQL: {sql}\n")

    # Execute custom SQL
    print("[4] Execute Custom SQL:")
    try:
        cols, rows = client.execute("SELECT COUNT(*) as count FROM airline;")
        print(f"    Columns: {cols}")
        print(f"    Result:  {rows}\n")
    except Exception as e:
        print(f"    Error: {e}\n")

    print("=" * 70)
    print("  For more examples, see: https://github.com/your-username/tounsi2sql-api")
    print("=" * 70 + "\n")
