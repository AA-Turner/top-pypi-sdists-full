import logging
import os
import sys
import traceback
import uuid
from typing import Any
from urllib.parse import urljoin

import httpx
import starlette.exceptions
import structlog
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from structlog.contextvars import bind_contextvars, clear_contextvars, get_contextvars

from .codewords_client import (
    AsyncCodewordsClient,
    AsyncCodewordsResponse,
    CodewordsClient,
    CodewordsResponse,
)


def _service_exc_filter(_logger, _method_name, event_dict):
    """Structlog processor to trim exception tracebacks to service code only.

    - If `exc_info` is present, it is converted to a filtered string containing only frames
      whose filenames start with the current working directory (service root) or an
      explicit `CODEWORDS_SERVICE_ROOT` env var, and then stored under "exception".
    - The original `exc_info` is removed so downstream formatters don't re-emit full traces.
    """
    exc_info = event_dict.get("exc_info")
    if not exc_info:
        return event_dict

    if exc_info is True:
        exc_info = sys.exc_info()
    try:
        exc_type, exc_value, exc_tb = exc_info
    except Exception:
        return event_dict

    service_root = os.environ.get("CODEWORDS_SERVICE_ROOT", os.getcwd())

    try:
        tb_frames = traceback.extract_tb(exc_tb)
        filtered_frames = [frame for frame in tb_frames if str(frame.filename).startswith(service_root)]
        if not filtered_frames:
            filtered_frames = tb_frames[-3:]
        formatted_frames = traceback.format_list(filtered_frames)
        exc_type_name = (
            exc_type.__name__
            if exc_type is not None
            else (type(exc_value).__name__ if exc_value is not None else "Exception")
        )
        formatted = "".join(formatted_frames) + f"{exc_type_name}: {exc_value}"
        event_dict["exception"] = formatted
        event_dict["exc_info"] = None
    except Exception:
        # Fallback to default formatting if anything goes wrong during trimming
        event_dict["exc_info"] = exc_info
    return event_dict


def _format_service_only_traceback(exc, max_frames: int = 5, max_chars: int = 2000) -> str:
    """Return a trimmed traceback string limited to service code.

    - Keeps only frames under CODEWORDS_SERVICE_ROOT or CWD
    - Emits only the last `max_frames` frames
    - Truncates the final string to `max_chars`
    """
    service_root = os.environ.get("CODEWORDS_SERVICE_ROOT", os.getcwd())
    tb = getattr(exc, "__traceback__", None)
    if tb is None:
        return f"{exc.__class__.__name__}: {exc}"

    frames = traceback.extract_tb(tb)
    service_frames = [f for f in frames if str(f.filename).startswith(service_root)]
    if not service_frames:
        service_frames = frames[-max_frames:]
    else:
        service_frames = service_frames[-max_frames:]

    normalized_frames = []
    for f in service_frames:
        try:
            rel = os.path.relpath(f.filename, start=service_root)
        except Exception:
            rel = f.filename
        normalized_frames.append(
            traceback.FrameSummary(rel, f.lineno, f.name, line=getattr(f, "line", None))
        )

    formatted = "".join(traceback.format_list(normalized_frames)) + f"{exc.__class__.__name__}: {exc}"
    if len(formatted) > max_chars:
        formatted = formatted[:max_chars] + "…"
    return formatted


def _setup_logging():
    """Configure structlog logging with filtered service-only tracebacks."""
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            _service_exc_filter,
            structlog.processors.JSONRenderer(sort_keys=True),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

class RequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware to handle request IDs and correlation IDs."""
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
        correlation_id = request.headers.get("X-Correlation-Id", request_id)
        caller_id = request.headers.get("Codewords-Caller-Id", "")
        scheduled_request_id = request.headers.get("X-Scheduled-Request-Id")
        extra_context = {"scheduled_request_id": scheduled_request_id} if scheduled_request_id else {}
        bind_contextvars(request_id=request_id, correlation_id=correlation_id, caller_id=caller_id, **extra_context)

        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id
        response.headers["X-Correlation-Id"] = correlation_id
        response.headers["Codewords-Caller-Id"] = caller_id

        clear_contextvars()
        return response

def _setup_exception_handlers(app: FastAPI):
    """Set up standard exception handlers."""
    logger = structlog.get_logger()

    app.exception_handlers.pop(starlette.exceptions.HTTPException, None)

    @app.exception_handler(starlette.exceptions.HTTPException)
    async def http_exception_handler(request: Request, exc: starlette.exceptions.HTTPException):
        """Handles expected client errors (4xx) and re-raises custom HTTPExceptions."""
        logger.exception("HTTP exception caught", path=str(request.url), status_code=exc.status_code, detail=exc.detail)
        headers = dict(exc.headers or {})
        headers.setdefault("Error-Origin", "service")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail}, headers=headers)

    @app.exception_handler(httpx.HTTPStatusError)
    async def http_status_error_handler(request: Request, exc: httpx.HTTPStatusError):
        """Handles upstream httpx HTTPStatusError by mapping to an HTTP response."""
        status_code = getattr(getattr(exc, "response", None), "status_code", 500)
        # Try to extract a useful detail from the upstream response
        detail: Any
        response = getattr(exc, "response", None)
        if response is not None:
            try:
                payload = response.json()
                if isinstance(payload, dict) and "detail" in payload:
                    detail = payload.get("detail")
                else:
                    detail = payload
            except Exception:
                try:
                    detail = response.text
                except Exception:
                    detail = str(exc)
        else:
            detail = str(exc)

        logger.exception(
            "HTTPStatusError caught",
            path=str(request.url),
            upstream_url=str(getattr(getattr(exc, "request", None), "url", "")),
            status_code=status_code,
            detail=str(detail) if not isinstance(detail, (str, int, float, bool, type(None))) else detail,
        )

        headers = {"Error-Origin": "service"}
        return JSONResponse(status_code=status_code, content={"detail": detail}, headers=headers)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handles FastAPI request-validation errors (422)."""
        logger.exception("Request validation failed", path=str(request.url), errors=exc.errors())
        return JSONResponse(status_code=422, content={"detail": jsonable_encoder(exc.errors())}, headers={"Error-Origin": "service"})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Catch-all handler for unhandled errors, returning a 500 response."""
        logger.exception("Unhandled exception", path=str(request.url), error_type=exc.__class__.__name__)
        # Return a trimmed, service-only traceback in the response for debugging
        traceback_str = _format_service_only_traceback(
            exc,
            max_frames=int(os.environ.get("ERROR_TRACE_MAX_FRAMES", 5)),
            max_chars=int(os.environ.get("ERROR_TRACE_MAX_CHARS", 2000)),
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error:\n\n" + traceback_str},
            headers={"Error-Origin": "service"},
        )

if not hasattr(FastAPI, '_codewords_patched'):
    _original_fastapi_init = FastAPI.__init__

    def _enhanced_fastapi_init(self, auto_setup: bool = True, **kwargs: Any) -> None:
        """Enhanced FastAPI constructor that auto-configures CodeWords infrastructure."""
        
        # Call original constructor
        _original_fastapi_init(self, **kwargs)
        
        if auto_setup:
            self.add_middleware(RequestIdMiddleware)
            _setup_exception_handlers(self)

    # Apply the monkey patch
    FastAPI.__init__ = _enhanced_fastapi_init
    FastAPI._codewords_patched = True

def run_service(app: FastAPI, **kwargs):
    """Convenience function to run the service with sensible defaults."""
    import uvicorn
    logger = structlog.get_logger()

    defaults = {'host': '0.0.0.0', 'port': int(os.environ.get("PORT", 8000)), 'loop': 'uvloop'}
    defaults.update(kwargs)

    logger.info("Starting CodeWords service...")
    uvicorn.run(app, **defaults)

# Setup logging when module is imported
_setup_logging()

# Create logger instance for export
logger = structlog.get_logger()

def _patch_firecrawl():
    """Monkey patch FirecrawlApp to auto-inject correlation IDs and CodeWords proxy settings."""
    try:
        from firecrawl import FirecrawlApp as OriginalFirecrawlApp
        if hasattr(OriginalFirecrawlApp, '_codewords_patched'):
            return
        
        _original_init = OriginalFirecrawlApp.__init__
        _original_prepare_headers = OriginalFirecrawlApp._prepare_headers
        
        def _enhanced_init(self, api_key=None, api_url=None, correlation_id=None, **kwargs):
            api_key = api_key or os.environ.get('CODEWORDS_API_KEY')
            api_url = api_url or urljoin(os.environ.get('CODEWORDS_RUNTIME_URI', 'https://runtime.codewords.ai'), "run/firecrawl")
            correlation_id = correlation_id or get_contextvars().get("correlation_id")
            _original_init(self, api_key=api_key, api_url=api_url, **kwargs)
            self.correlation_id = correlation_id
        
        def _enhanced_prepare_headers(self):
            headers = _original_prepare_headers(self)
            if hasattr(self, 'correlation_id') and self.correlation_id:
                headers['X-Correlation-Id'] = self.correlation_id
            return headers
        
        OriginalFirecrawlApp.__init__ = _enhanced_init
        OriginalFirecrawlApp._prepare_headers = _enhanced_prepare_headers
        OriginalFirecrawlApp._codewords_patched = True
        logger.debug("FirecrawlApp successfully patched for CodeWords auto-configuration")
        
    except ImportError:
        pass
    except Exception as e:
        logger.warning("Failed to patch FirecrawlApp", error=str(e))

def _patch_openai():
    """Monkey patch AsyncOpenAI to auto-inject CodeWords proxy settings and correlation IDs."""
    try:
        from openai import AsyncOpenAI
        if hasattr(AsyncOpenAI, '_codewords_patched'):
            return
        
        _original_init = AsyncOpenAI.__init__
        
        def _enhanced_init(self, api_key=None, base_url=None, default_headers=None, **kwargs):
            api_key = api_key or os.environ.get('CODEWORDS_API_KEY')
            base_url = base_url or urljoin(os.environ.get('CODEWORDS_RUNTIME_URI', 'https://runtime.codewords.ai'), "run/openai/v1")
            default_headers = dict(default_headers or {})
            
            if 'X-Correlation-Id' not in default_headers:
                correlation_id = get_contextvars().get("correlation_id")
                if correlation_id:
                    default_headers['X-Correlation-Id'] = correlation_id
            
            _original_init(self, api_key=api_key, base_url=base_url, default_headers=default_headers, **kwargs)
        
        AsyncOpenAI.__init__ = _enhanced_init
        AsyncOpenAI._codewords_patched = True
        logger.debug("AsyncOpenAI successfully patched for CodeWords auto-configuration")
        
    except ImportError:
        pass
    except Exception as e:
        logger.warning("Failed to patch AsyncOpenAI", error=str(e))

def _patch_anthropic():
    """Monkey patch AsyncAnthropic to auto-inject CodeWords proxy settings and correlation IDs."""
    try:
        from anthropic import AsyncAnthropic
        if hasattr(AsyncAnthropic, '_codewords_patched'):
            return

        _original_init = AsyncAnthropic.__init__

        def _enhanced_init(self, api_key=None, base_url=None, default_headers=None, **kwargs):
            api_key = api_key or os.environ.get('CODEWORDS_API_KEY')
            base_url = base_url or urljoin(os.environ.get('CODEWORDS_RUNTIME_URI', 'https://runtime.codewords.ai'), "run/anthropic")
            default_headers = dict(default_headers or {})

            if 'X-Correlation-Id' not in default_headers:
                correlation_id = get_contextvars().get("correlation_id")
                if correlation_id:
                    default_headers['X-Correlation-Id'] = correlation_id

            _original_init(self, api_key=api_key, base_url=base_url, default_headers=default_headers, **kwargs)

        AsyncAnthropic.__init__ = _enhanced_init
        AsyncAnthropic._codewords_patched = True
        logger.debug("AsyncAnthropic successfully patched for CodeWords auto-configuration")

    except ImportError:
        pass
    except Exception as e:
        logger.warning("Failed to patch AsyncAnthropic", error=str(e))

def _patch_perplexity():
    """Monkey patch Perplexity and AsyncPerplexity to auto-inject CodeWords proxy settings and correlation IDs."""
    try:
        from perplexity import Perplexity, AsyncPerplexity

        # Patch sync client
        if not hasattr(Perplexity, '_codewords_patched'):
            _original_sync_init = Perplexity.__init__

            def _enhanced_sync_init(self, api_key=None, base_url=None, default_headers=None, **kwargs):
                api_key = api_key or os.environ.get('CODEWORDS_API_KEY')
                base_url = base_url or urljoin(os.environ.get('CODEWORDS_RUNTIME_URI', 'https://runtime.codewords.ai'), "run/perplexity")
                default_headers = dict(default_headers or {})

                if 'X-Correlation-Id' not in default_headers:
                    correlation_id = get_contextvars().get("correlation_id")
                    if correlation_id:
                        default_headers['X-Correlation-Id'] = correlation_id

                _original_sync_init(self, api_key=api_key, base_url=base_url, default_headers=default_headers, **kwargs)

            Perplexity.__init__ = _enhanced_sync_init
            Perplexity._codewords_patched = True
            logger.debug("Perplexity successfully patched for CodeWords auto-configuration")

        # Patch async client
        if not hasattr(AsyncPerplexity, '_codewords_patched'):
            _original_async_init = AsyncPerplexity.__init__

            def _enhanced_async_init(self, api_key=None, base_url=None, default_headers=None, **kwargs):
                api_key = api_key or os.environ.get('CODEWORDS_API_KEY')
                base_url = base_url or urljoin(os.environ.get('CODEWORDS_RUNTIME_URI', 'https://runtime.codewords.ai'), "run/perplexity")
                default_headers = dict(default_headers or {})

                if 'X-Correlation-Id' not in default_headers:
                    correlation_id = get_contextvars().get("correlation_id")
                    if correlation_id:
                        default_headers['X-Correlation-Id'] = correlation_id

                _original_async_init(self, api_key=api_key, base_url=base_url, default_headers=default_headers, **kwargs)

            AsyncPerplexity.__init__ = _enhanced_async_init
            AsyncPerplexity._codewords_patched = True
            logger.debug("AsyncPerplexity successfully patched for CodeWords auto-configuration")

    except ImportError:
        pass
    except Exception as e:
        logger.warning("Failed to patch Perplexity", error=str(e))

# Import redis_client from separate module (lazy loading)
from .redis import redis_client

# Apply all monkey patches
_patch_firecrawl()
_patch_openai()
_patch_anthropic()
_patch_perplexity()

# Export everything
__all__ = [
    'AsyncCodewordsClient', 
    'CodewordsClient', 
    'AsyncCodewordsResponse', 
    'CodewordsResponse',
    'logger', 
    'run_service', 
    'RequestIdMiddleware',
    'redis_client'
]
