from __future__ import annotations

import json
import re
from typing import Any


SENSITIVE_PATTERNS = (
    re.compile(r"\botp\b", re.IGNORECASE),
    re.compile(r"\bpin\b", re.IGNORECASE),
    re.compile(r"\bpassword\b", re.IGNORECASE),
    re.compile(r"\bcard\s*number\b", re.IGNORECASE),
    re.compile(r"\bcvv\b", re.IGNORECASE),
)


class GeminiError(Exception):
    """Base exception for Gemini failures."""


class GeminiConfigurationError(GeminiError):
    """Raised when Gemini is not configured correctly."""


class GeminiTimeoutError(GeminiError):
    """Raised when Gemini takes too long to respond."""


class GeminiAPIError(GeminiError):
    """Raised when Gemini returns an unexpected API failure."""


class GeminiRateLimitError(GeminiError):
    """Raised when Gemini rejects requests due to quota or rate limiting."""


class GeminiResponseError(GeminiError):
    """Raised when Gemini returns invalid or unsafe content."""


def parse_gemini_json(raw_text: str) -> dict[str, Any]:
    text = raw_text.strip()
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise GeminiResponseError("Gemini response must be a JSON object")
    return parsed


def ensure_safe_agent_summary(summary: str) -> None:
    lowered_summary = summary.lower()
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(lowered_summary):
            raise GeminiResponseError("agent_summary contains sensitive credential request language")
