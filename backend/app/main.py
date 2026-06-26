from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .routes import router
from .utils import GeminiAPIError, GeminiConfigurationError, GeminiError, GeminiRateLimitError, GeminiResponseError, GeminiTimeoutError

app = FastAPI(title="QueueStorm Warmup API", version="1.0.0")
app.include_router(router)


@app.exception_handler(GeminiTimeoutError)
async def gemini_timeout_handler(_: Request, exc: GeminiTimeoutError) -> JSONResponse:
    return JSONResponse(status_code=504, content={"detail": str(exc)})


@app.exception_handler(GeminiConfigurationError)
async def gemini_configuration_handler(_: Request, exc: GeminiConfigurationError) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.exception_handler(GeminiAPIError)
async def gemini_api_handler(_: Request, exc: GeminiAPIError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.exception_handler(GeminiRateLimitError)
async def gemini_rate_limit_handler(_: Request, exc: GeminiRateLimitError) -> JSONResponse:
    return JSONResponse(status_code=429, content={"detail": str(exc)})


@app.exception_handler(GeminiResponseError)
async def gemini_response_handler(_: Request, exc: GeminiResponseError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.exception_handler(GeminiError)
async def gemini_base_handler(_: Request, exc: GeminiError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": str(exc)})
