from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SortTicketRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_id: str = Field(min_length=1, max_length=64)
    channel: str = Field(min_length=1, max_length=64)
    locale: str = Field(min_length=1, max_length=32)
    message: str = Field(min_length=1, max_length=5000)


class SortTicketResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_id: str = Field(min_length=1, max_length=64)
    case_type: str = Field(min_length=1, max_length=64)
    severity: str = Field(min_length=1, max_length=32)
    department: str = Field(min_length=1, max_length=64)
    agent_summary: str = Field(min_length=1, max_length=500)
    human_review_required: bool
    confidence: float = Field(ge=0.0, le=1.0)
