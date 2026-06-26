from __future__ import annotations

from fastapi import APIRouter, Depends

from .gemini_client import GeminiClient
from .schemas import SortTicketRequest, SortTicketResponse

router = APIRouter()


def get_gemini_client() -> GeminiClient:
    return GeminiClient()


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/sort-ticket", response_model=SortTicketResponse)
async def sort_ticket(
    ticket: SortTicketRequest,
    client: GeminiClient = Depends(get_gemini_client),
) -> SortTicketResponse:
    return client.classify_ticket(ticket)
