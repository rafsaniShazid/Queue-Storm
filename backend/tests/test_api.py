from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from app.gemini_client import GeminiClient
from app.config import Settings
from app.main import app
from app.routes import get_gemini_client
from app.schemas import SortTicketRequest
from app.utils import GeminiAPIError, GeminiResponseError, GeminiTimeoutError

client = TestClient(app)


VALID_REQUEST = {
    "ticket_id": "T-001",
    "channel": "app",
    "locale": "en",
    "message": "I sent 5000 taka to a wrong number this morning.",
}

VALID_RESPONSE = {
    "ticket_id": "T-001",
    "case_type": "wrong_transfer",
    "severity": "high",
    "department": "dispute_resolution",
    "agent_summary": "Customer reports sending money to the wrong recipient and requests assistance.",
    "human_review_required": True,
    "confidence": 0.95,
}


class StubGeminiClient:
    def __init__(self, response: dict[str, object] | None = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error

    def classify_ticket(self, ticket: SortTicketRequest):
        if self.error is not None:
            raise self.error
        payload = dict(self.response or VALID_RESPONSE)
        payload["ticket_id"] = ticket.ticket_id
        return payload


class RaisingClient:
    def __init__(self, error: Exception) -> None:
        self.error = error

    def classify_ticket(self, ticket: SortTicketRequest):
        raise self.error


class FakeResponse:
    def __init__(self, text: str | None) -> None:
        self.text = text


class FakeSDKClient:
    def __init__(self, text: str | None, error: Exception | None = None) -> None:
        self.text = text
        self.error = error
        self.models = self

    def generate_content(self, *, model: str, contents: str):
        if self.error is not None:
            raise self.error
        return FakeResponse(self.text)


@pytest.fixture(autouse=True)
def clear_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def override_gemini_client():
    def _override(fake_client):
        app.dependency_overrides[get_gemini_client] = lambda: fake_client

    return _override


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_sort_ticket_success(override_gemini_client) -> None:
    override_gemini_client(StubGeminiClient())
    response = client.post("/sort-ticket", json=VALID_REQUEST)

    assert response.status_code == 200
    assert response.json() == VALID_RESPONSE


def test_sort_ticket_invalid_json() -> None:
    response = client.post(
        "/sort-ticket",
        data="{",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422


def test_sort_ticket_missing_fields() -> None:
    response = client.post("/sort-ticket", json={"ticket_id": "T-001", "channel": "app"})

    assert response.status_code == 422


def test_sort_ticket_gemini_timeout(override_gemini_client) -> None:
    override_gemini_client(RaisingClient(GeminiTimeoutError("Gemini request timed out")))
    response = client.post("/sort-ticket", json=VALID_REQUEST)

    assert response.status_code == 504


def test_sort_ticket_gemini_failure(override_gemini_client) -> None:
    override_gemini_client(RaisingClient(GeminiAPIError("Gemini request failed")))
    response = client.post("/sort-ticket", json=VALID_REQUEST)

    assert response.status_code == 502


def test_sort_ticket_invalid_gemini_json() -> None:
    client_under_test = GeminiClient(settings=Settings(gemini_api_key="test-key"), client=FakeSDKClient("not-json"))

    with pytest.raises(GeminiResponseError):
        client_under_test.classify_ticket(SortTicketRequest.model_validate(VALID_REQUEST))


def test_sort_ticket_invalid_gemini_summary() -> None:
    bad_response = dict(VALID_RESPONSE)
    bad_response["agent_summary"] = "Please provide your OTP and card number to continue."

    client_under_test = GeminiClient(
        settings=Settings(gemini_api_key="test-key"),
        client=FakeSDKClient(json.dumps(bad_response)),
    )

    with pytest.raises(GeminiResponseError):
        client_under_test.classify_ticket(SortTicketRequest.model_validate(VALID_REQUEST))
