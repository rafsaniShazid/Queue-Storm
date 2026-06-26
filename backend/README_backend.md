# QueueStorm Backend

FastAPI backend for ticket classification using the official Google GenAI Python SDK.

## Setup

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`.

## Run

```bash
uvicorn app.main:app --reload
```

Open:
- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `GET /health`
- Ticket classification: `POST /sort-ticket`

## Example Request

```json
{
  "ticket_id": "T-001",
  "channel": "app",
  "locale": "en",
  "message": "I sent 5000 taka to a wrong number this morning."
}
```

## Testing

```bash
pytest
```

## Notes

- Request and response bodies are validated with Pydantic.
- Gemini output is parsed as strict JSON and rejected if it is malformed.
- The API never hardcodes secrets; it reads the Gemini key from environment variables.
