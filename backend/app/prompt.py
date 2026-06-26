from __future__ import annotations

import json

from .schemas import SortTicketRequest


def build_classification_prompt(ticket: SortTicketRequest) -> str:
    ticket_payload = json.dumps(ticket.model_dump(), ensure_ascii=False)

    return (
        "You are a customer support ticket classifier for a banking workflow.\n"
        "Return ONLY valid JSON. No markdown. No code fences. No explanation.\n"
        "The JSON object must include exactly these keys: ticket_id, case_type, severity, department, agent_summary, human_review_required, confidence.\n"
        "Rules:\n"
        "- ticket_id must match the input ticket_id.\n"
        "- confidence must be a number between 0 and 1 inclusive.\n"
        "- agent_summary must be a short neutral summary.\n"
        "- agent_summary must never ask for OTP, PIN, password, card number, or any secret.\n"
        "- Choose the best classification for the ticket content.\n"
        "- Use concise, production-ready labels.\n"
        "Input ticket JSON:\n"
        f"{ticket_payload}"
    )
