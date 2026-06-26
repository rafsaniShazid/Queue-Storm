from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
import json
from typing import Any

from pydantic import ValidationError

from .config import Settings, get_settings
from .prompt import build_classification_prompt
from .schemas import SortTicketRequest, SortTicketResponse
from .utils import (
    GeminiAPIError,
    GeminiConfigurationError,
    GeminiRateLimitError,
    GeminiResponseError,
    GeminiTimeoutError,
    ensure_safe_agent_summary,
    parse_gemini_json,
)


class GeminiClient:
    def __init__(self, settings: Settings | None = None, client: Any | None = None) -> None:
        self.settings = settings or get_settings()
        if client is not None:
            self._client = client
            return

        try:
            from google import genai
        except ModuleNotFoundError as exc:  # pragma: no cover - environment dependent
            raise GeminiConfigurationError("Google GenAI SDK is not installed") from exc

        self._client = genai.Client(api_key=self.settings.gemini_api_key or None)

    def classify_ticket(self, ticket: SortTicketRequest) -> SortTicketResponse:
        if not self.settings.gemini_api_key:
            raise GeminiConfigurationError("GEMINI_API_KEY is not configured")

        prompt = build_classification_prompt(ticket)
        raw_text = self._generate_text(prompt)
        try:
            payload = parse_gemini_json(raw_text)
        except json.JSONDecodeError as exc:
            raise GeminiResponseError("Gemini returned invalid JSON") from exc
        payload["ticket_id"] = ticket.ticket_id

        try:
            response = SortTicketResponse.model_validate(payload)
        except ValidationError as exc:
            raise GeminiResponseError("Gemini response failed schema validation") from exc

        ensure_safe_agent_summary(response.agent_summary)
        return response

    def _generate_text(self, prompt: str) -> str:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                self._client.models.generate_content,
                model=self.settings.gemini_model,
                contents=prompt,
            )
            try:
                response = future.result(timeout=self.settings.gemini_timeout_seconds)
            except FuturesTimeoutError as exc:
                raise GeminiTimeoutError("Gemini request timed out") from exc
            except Exception as exc:  # noqa: BLE001
                error_code = getattr(exc, "code", None)
                error_status = str(getattr(exc, "status", "")).upper()
                if error_code == 429 or error_status == "RESOURCE_EXHAUSTED":
                    raise GeminiRateLimitError("Gemini quota exceeded") from exc
                raise GeminiAPIError("Gemini request failed") from exc

        text = getattr(response, "text", None)
        if text is None:
            raise GeminiResponseError("Gemini response did not include text")
        return text
