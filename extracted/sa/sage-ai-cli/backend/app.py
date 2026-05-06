"""Backend API for SAGE AI Platform.

This module provides the FastAPI backend with proper architectural patterns:
- App state instead of globals (P2-86)
- Isolated instance creation (P2-87)
- Lifecycle hooks (P2-88)
- Runtime locking (P2-89, P2-90)
- Structured error events for SSE (P2-91)
- Rate limiting with eviction (P2-95, P2-98)
- Request IDs and correlation (P2-100)
- Audit logging (P2-101)
- Proper error taxonomy (P2-102)
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import secrets
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from threading import Lock, RLock
from collections.abc import AsyncIterator, Callable

import httpx
import uvicorn
from fastapi import Depends, FastAPI, File, Header, HTTPException, Request, Response, UploadFile, WebSocket, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from .terminal_ws import (
    terminal_websocket_handler,
    get_cli_update_info,
    apply_cli_update,
)

from .auto_updater import AutoUpdater
from .billing import (
    ADMIN_EMAILS, PAYPAL_CLIENT_ID, PAYPAL_PLAN_IDS,
    check_access, ensure_user_record, get_usage,
    increment_usage, activate_subscription, cancel_subscription,
    delete_account, handle_webhook, get_user_record,
)
from .config import runtime_defaults, settings
from .conversations import ConversationStore
from .hardware import detect_hardware_summary
from .model_catalog import (
    filter_by_ram,
    get_recommended_models,
)
from sage.models.catalog import (
    get_recommended_ollama_models,
    get_full_catalog,
    CatalogModel,
)
from sage.models.gcs_manager import (
    GCSModelManager,
    OllamaClient,
)
from .model_registry import ModelRegistry
from .runtime_manager import RuntimeManager
from .schemas import (
    AddSourceReq,
    ChatMessage,
    ChatReq,
    CreateConversationReq,
    DownloadModelReq,
    FileAttachment,
    LargeTextContent,
    LoadModelReq,
    validate_safe_id,
    SAFE_MODEL_ID_PATTERN,
    SAFE_CONVERSATION_ID_PATTERN,
    LARGE_TEXT_THRESHOLD,
)
from .file_store import file_store, MAX_FILE_SIZE
from .conversation_logger import conversation_logger

settings.ensure_dirs()
logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
logger = logging.getLogger("ai-platform")


# ── Firebase token verification ───────────────────────────────────────────────
#
# Uses the Identity Toolkit REST API (accounts:lookup) — no Admin SDK setup needed.
# Falls back to Firebase Admin SDK if the REST call fails.

_FIREBASE_API_KEY = os.environ.get("VITE_FIREBASE_API_KEY", "")
_token_cache: dict = {}  # {token_prefix: {uid, email, expires_at}}


def _verify_firebase_token(token: str) -> dict:
    """Verify a Firebase ID token and return {uid, email}. Raises HTTPException on failure."""
    import time
    cache_key = token[:32]
    cached = _token_cache.get(cache_key)
    if cached and cached["expires_at"] > time.time():
        return {"uid": cached["uid"], "email": cached["email"]}

    # Primary: Firebase Identity Toolkit REST API — no Admin SDK needed
    if _FIREBASE_API_KEY:
        try:
            r = httpx.post(
                f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={_FIREBASE_API_KEY}",
                json={"idToken": token},
                timeout=8,
            )
            if r.is_success:
                users = r.json().get("users", [])
                if users:
                    u = users[0]
                    result = {"uid": u["localId"], "email": u.get("email", "")}
                    _token_cache[cache_key] = {**result, "expires_at": time.time() + 300}
                    return result
        except Exception:
            pass  # fall through to Admin SDK

    # Fallback: Firebase Admin SDK (requires GOOGLE_APPLICATION_CREDENTIALS or ADC)
    try:
        import firebase_admin
        from firebase_admin import auth as fb_auth
        if not firebase_admin._apps:
            firebase_admin.initialize_app(options={"projectId": "sage-ai-d1c22"})
        decoded = fb_auth.verify_id_token(token)
        result = {"uid": decoded["uid"], "email": decoded.get("email", "")}
        _token_cache[cache_key] = {**result, "expires_at": time.time() + 300}
        return result
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"Invalid or expired auth token: {exc}")


def _get_caller_identity(request: Request) -> dict | None:
    """Extract and verify Firebase token from Authorization header. Returns None if absent."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header.removeprefix("Bearer ").strip()
    if not token:
        return None
    return _verify_firebase_token(token)


def _require_auth(request: Request) -> dict:
    """Dependency: require a valid Firebase token. Returns {uid, email}."""
    identity = _get_caller_identity(request)
    if identity is None:
        raise HTTPException(status_code=401, detail="Authentication required. Please log in.")
    ensure_user_record(identity["uid"], identity["email"])
    return identity


# ═══════════════════════════════════════════════════════════════════════════════
# P2-95/98: Enhanced Rate Limiter with Eviction
# ═══════════════════════════════════════════════════════════════════════════════

class RateLimiter:
    """Thread-safe rate limiter with sliding window and automatic eviction.

    Improvements over the original:
    - Automatic eviction of stale entries to prevent memory leaks (P2-98)
    - Support for proxy-aware client identification (P2-99)
    - Per-endpoint rate limiting support
    """

    MAX_CLIENTS = 10000  # Maximum tracked clients before forced cleanup

    def __init__(
        self,
        requests_per_minute: int = 60,
        burst_limit: int = 10,
        eviction_interval: int = 300,  # 5 minutes
    ):
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit
        self.window_size = 60  # 1 minute
        self.eviction_interval = eviction_interval
        self._requests: dict[str, list[float]] = defaultdict(list)
        self._lock = Lock()
        self._last_eviction = time.time()

    def _evict_stale(self, now: float) -> None:
        """Remove stale entries to prevent memory growth."""
        if now - self._last_eviction < self.eviction_interval:
            return

        self._last_eviction = now
        window_start = now - self.window_size

        # Remove clients with no recent requests
        stale_clients = [
            client_id
            for client_id, timestamps in self._requests.items()
            if not timestamps or max(timestamps) < window_start
        ]

        for client_id in stale_clients:
            del self._requests[client_id]

        # Force cleanup if too many clients
        if len(self._requests) > self.MAX_CLIENTS:
            # Sort by last request time and remove oldest half
            sorted_clients = sorted(
                self._requests.items(),
                key=lambda x: max(x[1]) if x[1] else 0,
            )
            for client_id, _ in sorted_clients[: len(sorted_clients) // 2]:
                del self._requests[client_id]

    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed for this client."""
        now = time.time()
        window_start = now - self.window_size

        with self._lock:
            # Periodic eviction
            self._evict_stale(now)

            # Clean old requests for this client
            self._requests[client_id] = [
                t for t in self._requests[client_id] if t > window_start
            ]

            # Check burst limit (requests in last 1 second)
            recent = [t for t in self._requests[client_id] if t > now - 1]
            if len(recent) >= self.burst_limit:
                return False

            # Check rate limit
            if len(self._requests[client_id]) >= self.requests_per_minute:
                return False

            # Allow request
            self._requests[client_id].append(now)
            return True

    # P1-13: Known trusted proxy IPs that can set X-Forwarded-For
    TRUSTED_PROXIES = frozenset([
        "127.0.0.1",
        "::1",
        "localhost",
        # Add your load balancer/reverse proxy IPs here
    ])

    def get_client_id(self, request: Request) -> str:
        """Get client identifier with proxy awareness (P2-99).

        P1-13: Only trust X-Forwarded-For from known proxies.
        """
        direct_client = request.client.host if request.client else "unknown"

        # P1-13: Only trust forwarded headers if request came from a trusted proxy
        if direct_client in self.TRUSTED_PROXIES:
            # Check X-Forwarded-For header for proxied requests
            forwarded = request.headers.get("X-Forwarded-For")
            if forwarded:
                # Take the first (original) IP
                return forwarded.split(",")[0].strip()

            # Check X-Real-IP header
            real_ip = request.headers.get("X-Real-IP")
            if real_ip:
                return real_ip

        # Fall back to direct client (or if not from trusted proxy)
        return direct_client


# ═══════════════════════════════════════════════════════════════════════════════
# P2-86/87: App State (replacing globals)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class AppState:
    """Application state container (P2-86).

    This replaces global variables with proper app state management,
    enabling better isolation, testing, and concurrency control.
    """

    registry: ModelRegistry
    runtime_manager: RuntimeManager
    conversation_store: ConversationStore
    updater: AutoUpdater
    rate_limiter: RateLimiter

    # P1-12: Separate rate limiters for expensive endpoints
    download_rate_limiter: RateLimiter = field(
        default_factory=lambda: RateLimiter(requests_per_minute=10, burst_limit=2)
    )
    gcs_rate_limiter: RateLimiter = field(
        default_factory=lambda: RateLimiter(requests_per_minute=20, burst_limit=5)
    )
    terminal_rate_limiter: RateLimiter = field(
        default_factory=lambda: RateLimiter(requests_per_minute=5, burst_limit=2)
    )

    # P2-89/90: Runtime operation lock
    runtime_lock: RLock = field(default_factory=RLock)

    # GCS model manager for pull-upload-delete cycle
    gcs_manager: GCSModelManager | None = None

    # P2-101: Audit log
    audit_log: list[dict] = field(default_factory=list)
    max_audit_entries: int = 1000

    def log_audit(
        self,
        action: str,
        request_id: str,
        client_id: str,
        details: dict | None = None,
    ) -> None:
        """Log an audit event (P2-101)."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "request_id": request_id,
            "client_id": client_id,
            "details": details or {},
        }

        self.audit_log.append(entry)

        # Trim old entries
        if len(self.audit_log) > self.max_audit_entries:
            self.audit_log = self.audit_log[-self.max_audit_entries:]

        # Also log to standard logger
        logger.info(f"AUDIT: {action} | request={request_id} | client={client_id}")


def create_app_state() -> AppState:
    """Create isolated app state (P2-87)."""
    registry = ModelRegistry()

    # Initialize GCS manager for model pull-upload-delete cycle
    gcs_creds = settings.gcs_credentials_path if hasattr(settings, "gcs_credentials_path") else None
    try:
        gcs_manager = GCSModelManager(
            bucket_name="sage-ai-models",
            credentials_path=gcs_creds,
        )
    except Exception as e:
        logger.warning(f"Failed to initialize GCS manager: {e}")
        gcs_manager = None

    return AppState(
        registry=registry,
        runtime_manager=RuntimeManager(),
        conversation_store=ConversationStore(),
        updater=AutoUpdater(registry),
        rate_limiter=RateLimiter(requests_per_minute=120, burst_limit=20),
        gcs_manager=gcs_manager,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# P2-100: Request ID Middleware
# ═══════════════════════════════════════════════════════════════════════════════

async def add_request_id(request: Request, call_next: Callable) -> Response:
    """Add request ID to all requests (P2-100)."""
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())[:8]
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response


# ═══════════════════════════════════════════════════════════════════════════════
# P2-102: Error Classes
# ═══════════════════════════════════════════════════════════════════════════════

class APIError(HTTPException):
    """Base API error with proper taxonomy (P2-102)."""

    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: dict | None = None,
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error": error_code,
                "message": message,
                "details": details or {},
            },
        )


class NotFoundError(APIError):
    """Resource not found (404)."""

    def __init__(self, resource: str, identifier: str):
        super().__init__(
            status_code=404,
            error_code="NOT_FOUND",
            message=f"{resource} not found: {identifier}",
            details={"resource": resource, "identifier": identifier},
        )


class ValidationError(APIError):
    """Validation error (400)."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(
            status_code=400,
            error_code="VALIDATION_ERROR",
            message=message,
            details=details,
        )


class ModelRuntimeError(APIError):
    """Runtime/model error (500). Named to avoid shadowing built-in RuntimeError."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(
            status_code=500,
            error_code="RUNTIME_ERROR",
            message=message,
            details=details,
        )


class RateLimitError(APIError):
    """Rate limit exceeded (429)."""

    def __init__(self, retry_after: int = 60):
        super().__init__(
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED",
            message="Rate limit exceeded. Please try again later.",
            details={"retry_after_seconds": retry_after},
        )


# Global app state (will be set by create_app)
_app_state: AppState | None = None


def get_app_state() -> AppState:
    """Get the current app state."""
    global _app_state
    if _app_state is None:
        _app_state = create_app_state()
    return _app_state


# Legacy compatibility
rate_limiter = None  # Will be set by create_app

def _extract_bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    return token


def _require_admin_token_strict(
    request: Request,
    authorization: str | None = Header(default=None),
    x_admin_token: str | None = Header(default=None),
) -> None:
    """Require admin token for protected endpoints - FAILS CLOSED.

    CRITICAL SECURITY: This function fails closed if admin_token is not configured.
    Use this for all admin endpoints to prevent fail-open security bypass.
    """
    expected = settings.admin_token.strip()

    # CRITICAL: Fail closed if admin token is not configured
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin authentication not configured - cannot authorize request",
        )

    provided = x_admin_token or _extract_bearer_token(authorization)
    if not provided or not secrets.compare_digest(provided, expected):
        # Log failed auth attempt (P2-101)
        state = get_app_state()
        state.log_audit(
            action="AUTH_FAILED",
            request_id=getattr(request.state, "request_id", "unknown"),
            client_id=state.rate_limiter.get_client_id(request),
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin token",
        )


def require_admin_token(
    request: Request,
    authorization: str | None = Header(default=None),
    x_admin_token: str | None = Header(default=None),
) -> None:
    """Require admin token for protected endpoints (legacy - fails open).

    DEPRECATED: Use _require_admin_token_strict instead for security.
    This version fails open if token is not configured - use only for backward compatibility.
    """
    expected = settings.admin_token.strip()
    if not expected:
        return
    provided = x_admin_token or _extract_bearer_token(authorization)
    if not provided or not secrets.compare_digest(provided, expected):
        # Log failed auth attempt (P2-101)
        state = get_app_state()
        state.log_audit(
            action="AUTH_FAILED",
            request_id=getattr(request.state, "request_id", "unknown"),
            client_id=state.rate_limiter.get_client_id(request),
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin token required",
        )


def check_rate_limit(request: Request) -> None:
    """Rate limit dependency with proxy awareness (P2-99)."""
    state = get_app_state()
    client_id = state.rate_limiter.get_client_id(request)

    if not state.rate_limiter.is_allowed(client_id):
        raise RateLimitError(retry_after=60)


# P1-12: Rate limit checkers for expensive endpoints
def check_download_rate_limit(request: Request) -> None:
    """Stricter rate limit for download endpoints (P1-12)."""
    state = get_app_state()
    client_id = state.download_rate_limiter.get_client_id(request)

    if not state.download_rate_limiter.is_allowed(client_id):
        raise RateLimitError(retry_after=300)  # 5 minute retry for downloads


def check_gcs_rate_limit(request: Request) -> None:
    """Rate limit for GCS operations (P1-12)."""
    state = get_app_state()
    client_id = state.gcs_rate_limiter.get_client_id(request)

    if not state.gcs_rate_limiter.is_allowed(client_id):
        raise RateLimitError(retry_after=120)  # 2 minute retry for GCS


def check_terminal_rate_limit(request: Request) -> None:
    """Rate limit for terminal WebSocket connections (P1-12)."""
    state = get_app_state()
    client_id = state.terminal_rate_limiter.get_client_id(request)

    if not state.terminal_rate_limiter.is_allowed(client_id):
        raise RateLimitError(retry_after=60)


# ═══════════════════════════════════════════════════════════════════════════════
# Path Parameter Validation (TDD Cycle)
# ═══════════════════════════════════════════════════════════════════════════════

import re


def validate_model_id_path(model_id: str) -> str:
    """Validate model_id path parameter against safe pattern."""
    try:
        validate_safe_id(model_id, "model_id")
    except ValueError as e:
        raise ValidationError(str(e))

    if not re.match(SAFE_MODEL_ID_PATTERN, model_id):
        raise ValidationError(f"Invalid model_id format: {model_id}")

    return model_id


def validate_conversation_id_path(conversation_id: str) -> str:
    """Validate conversation_id path parameter against safe pattern."""
    try:
        validate_safe_id(conversation_id, "conversation_id")
    except ValueError as e:
        raise ValidationError(str(e))

    if not re.match(SAFE_CONVERSATION_ID_PATTERN, conversation_id):
        raise ValidationError(f"Invalid conversation_id format: {conversation_id}")

    return conversation_id


def validate_model_name_path(model_name: str) -> str:
    """Validate model_name path parameter (for Ollama/GCS)."""
    if not model_name or not model_name.strip():
        raise ValidationError("model_name cannot be empty")

    # Check for path traversal
    if ".." in model_name or "/" in model_name or "\\" in model_name:
        raise ValidationError("model_name contains invalid characters")

    # Check for null bytes
    if "\x00" in model_name:
        raise ValidationError("model_name contains null byte")

    return model_name


# ═══════════════════════════════════════════════════════════════════════════════
# Bundled model auto-registration
# ═══════════════════════════════════════════════════════════════════════════════

_BUNDLED_MODELS = [
    {
        "model_id": "llama3.2-1b",
        "file_path": "/app/models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
        "size_gb": 0.8,
        "runtime": "llama_cpp",
        "version_tag": "q4_k_m",
        "source_url": "https://storage.googleapis.com/sage-ai-models/gguf/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
    },
]


def _register_bundled_models(state) -> None:
    """Register GGUF models baked into the Docker image so /models sees them on startup."""
    import datetime as _dt
    for m in _BUNDLED_MODELS:
        model_id = m["model_id"]
        fpath = Path(m["file_path"])
        if not fpath.exists():
            continue  # model not bundled in this build
        try:
            raw = state.registry._load_raw()
            if model_id in raw:
                continue  # already registered
            raw[model_id] = {
                "model_id": model_id,
                "runtime": m["runtime"],
                "license": "",
                "format": "gguf",
                "source_repo": "gcs",
                "active_version": 1,
                "versions": [{
                    "version": 1,
                    "version_tag": m["version_tag"],
                    "file_path": str(fpath),
                    "source_url": m["source_url"],
                    "sha256": "",
                    "size_gb": m["size_gb"],
                    "created_at": _dt.datetime.utcnow().isoformat() + "Z",
                }],
            }
            state.registry._save_raw(raw)
            logger.info("Auto-registered bundled model: %s → %s", model_id, fpath)
        except Exception as exc:
            logger.warning("Failed to auto-register %s: %s", model_id, exc)


# ═══════════════════════════════════════════════════════════════════════════════
# P2-88: Lifecycle Hooks
# ═══════════════════════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager (P2-88)."""
    global _app_state

    # Startup
    logger.info("Starting AI Platform API...")
    _app_state = create_app_state()

    # Register any bundled GGUF models present on disk but not yet in registry.
    # This handles the Docker case where the model is baked into the image.
    _register_bundled_models(_app_state)

    # Log startup
    _app_state.log_audit(
        action="APP_STARTUP",
        request_id="system",
        client_id="system",
        details={"version": "3.0.0"},
    )

    logger.info("App state initialized")

    # Start the central SMS bridge email poller (non-fatal if not configured)
    from .sms_poller import run_imap_poller, BRIDGE_EMAIL
    sms_task = None
    if BRIDGE_EMAIL:
        sms_task = asyncio.create_task(run_imap_poller())
        logger.info("SMS bridge poller started for %s", BRIDGE_EMAIL)
    else:
        logger.info(
            "SMS bridge disabled — set SAGE_BRIDGE_EMAIL and "
            "SAGE_BRIDGE_APP_PASSWORD in Cloud Run env vars to enable"
        )

    yield

    # Cancel SMS poller
    if sms_task and not sms_task.done():
        sms_task.cancel()
        try:
            await sms_task
        except (asyncio.CancelledError, Exception):
            pass

    # Shutdown
    logger.info("Shutting down AI Platform API...")

    if _app_state:
        # Unload any loaded model
        if _app_state.runtime_manager.runtime is not None:
            try:
                _app_state.runtime_manager.unload()
            except Exception as e:
                logger.warning(f"Error unloading model during shutdown: {e}")

        # Log shutdown
        _app_state.log_audit(
            action="APP_SHUTDOWN",
            request_id="system",
            client_id="system",
        )

    logger.info("Shutdown complete")


def create_app() -> FastAPI:
    """Create FastAPI app with proper configuration (P2-87)."""
    fastapi_app = FastAPI(
        title="Local AI Platform",
        version="3.0.0",
        lifespan=lifespan,
    )

    # CORS middleware
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request ID middleware (P2-100)
    @fastapi_app.middleware("http")
    async def request_id_middleware(request: Request, call_next):
        return await add_request_id(request, call_next)

    # HTML no-cache middleware — prevents browsers from caching index.html
    # so users always get the latest bundle references after a deployment.
    # Stale HTML referencing an old JS bundle causes Firebase auth failures.
    @fastapi_app.middleware("http")
    async def html_no_cache_middleware(request: Request, call_next):
        response = await call_next(request)
        ct = response.headers.get("content-type", "")
        if "text/html" in ct:
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response

    # ── Security & Cross-Origin Isolation headers ────────────────────────────

    @fastapi_app.middleware("http")
    async def security_headers_middleware(request: Request, call_next):
        response = await call_next(request)

        # Cross-origin isolation — required for SharedArrayBuffer / WebLLM.
        # COOP must be exactly "same-origin" (not "same-origin-allow-popups")
        # for the browser to set crossOriginIsolated = true.
        # Firebase signInWithPopup still works because the auth callback
        # (__/auth/handler) is served from the same origin, so window.opener
        # is accessible from the same-origin redirect page inside the popup.
        response.headers["Cross-Origin-Opener-Policy"]   = "same-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "credentialless"

        # Clickjacking protection
        response.headers["X-Frame-Options"] = "SAMEORIGIN"

        # MIME-type sniffing protection
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Referrer — send origin only for cross-origin requests
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions — restrict access to sensitive browser APIs
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=(), "
            "usb=(), magnetometer=(), gyroscope=(), accelerometer=()"
        )

        # HSTS — enforce HTTPS for 1 year (only meaningful over TLS)
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )

        # Content-Security-Policy
        # - default-src 'self': all resources default to same origin
        # - script-src: allow self, CDN scripts (onnxruntime), PayPal, inline modules
        # - connect-src: allow Firebase, GCS, PayPal APIs, HuggingFace CDN (all tiers)
        # - frame-src: allow PayPal checkout frames
        # - img-src: allow any HTTPS image (models + user avatars)
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
                "https://cdn.jsdelivr.net "
                "https://www.paypal.com https://www.paypalobjects.com; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' "
                # Firebase / Google APIs
                "https://*.googleapis.com "
                "https://identitytoolkit.googleapis.com "
                "https://securetoken.googleapis.com "
                "https://storage.googleapis.com "
                # PayPal
                "https://api-m.paypal.com "
                "https://www.paypal.com "
                # Static CDN
                "https://cdn.jsdelivr.net "
                # HuggingFace — model files can arrive from several CDN tiers:
                #   huggingface.co          — hub API & small files
                #   *.huggingface.co        — hub subdomains (e.g. cdn-lfs.huggingface.co)
                #   hf.co                   — short domain
                #   *.hf.co                 — first-level subdomains (xethub.hf.co, etc.)
                #   *.xethub.hf.co          — XetHub CAS bridge (cas-bridge.xethub.hf.co)
                #   raw.githubusercontent.com — WASM/metadata from GitHub releases
                "https://huggingface.co "
                "https://*.huggingface.co "
                "https://hf.co "
                "https://*.hf.co "
                "https://*.xethub.hf.co "
                "https://raw.githubusercontent.com "
                "https://github.com "
                "https://*.github.com "
                # SAGE WebSocket terminal
                "wss://sageworksai.com; "
            "frame-src https://www.paypal.com https://www.sandbox.paypal.com "
                "https://sageworksai.com; "
            "worker-src 'self' blob:; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self' https://www.paypal.com; "
            "upgrade-insecure-requests"
        )
        response.headers["Content-Security-Policy"] = csp

        return response

    return fastapi_app


app = create_app()


@app.get("/health")
def health():
    state = get_app_state()
    return {
        "ok": True,
        "version": "3.0.0",
        "loaded_model_id": state.runtime_manager.loaded_model_id,
        "loaded_runtime": state.runtime_manager.loaded_runtime,
    }


@app.get("/hardware")
def hardware():
    return detect_hardware_summary()


@app.get("/models")
def list_models():
    state = get_app_state()
    return {"ok": True, "models": [m.model_dump() for m in state.registry.list_models()]}


@app.get("/models/names")
def model_names():
    state = get_app_state()
    names = {m.model_id for m in state.registry.list_models()}
    for source in state.updater.list_sources():
        names.add(source.model_id)
    return {"ok": True, "names": sorted(names)}


@app.get("/models/{model_id}")
def get_model(model_id: str):
    # Validate path parameter (TDD Cycle)
    model_id = validate_model_id_path(model_id)
    state = get_app_state()
    try:
        record = state.registry.get_model(model_id)
    except KeyError:
        raise NotFoundError("Model", model_id)
    return {"ok": True, "model": record.model_dump()}


@app.post("/models/download")
def download_model(
    request: Request,
    req: DownloadModelReq,
    _admin: None = Depends(_require_admin_token_strict),
    _rate_limit: None = Depends(check_download_rate_limit),  # P1-12
):
    state = get_app_state()
    request_id = getattr(request.state, "request_id", "unknown")
    client_id = state.rate_limiter.get_client_id(request)

    # Audit log (P2-101)
    state.log_audit(
        action="MODEL_DOWNLOAD",
        request_id=request_id,
        client_id=client_id,
        details={"model_id": req.model_id if hasattr(req, "model_id") else "unknown"},
    )

    try:
        record = state.registry.download_and_register(req)
    except ValueError as exc:
        detail = str(exc)
        if "GitHub" in detail or "allowed" in detail:
            raise ValidationError(f"source not allowed: {detail}")
        raise ValidationError(detail)
    except Exception as exc:
        raise ModelRuntimeError(f"Download failed: {exc}")
    return {"ok": True, "model": record.model_dump()}


@app.post("/models/load")
def load_model(
    request: Request,
    req: LoadModelReq,
    _admin: None = Depends(_require_admin_token_strict),
):
    state = get_app_state()
    request_id = getattr(request.state, "request_id", "unknown")
    client_id = state.rate_limiter.get_client_id(request)

    model_id = req.model_id

    # Audit log (P2-101)
    state.log_audit(
        action="MODEL_LOAD",
        request_id=request_id,
        client_id=client_id,
        details={"model_id": model_id},
    )

    # Use lock to prevent concurrent load operations (P2-89, P2-90)
    with state.runtime_lock:
        # Ollama models (local inference only)
        if model_id.startswith("ollama:"):
            ollama_name = model_id.removeprefix("ollama:")
            try:
                state.runtime_manager.load("ollama", model_id, ollama_name, threads=None)
            except Exception as exc:
                raise ModelRuntimeError(f"Failed to load Ollama model: {exc}") from exc
            return {
                "ok": True,
                "loaded_model_id": state.runtime_manager.loaded_model_id,
                "loaded_runtime": "ollama",
                "threads": 0,
            }

        if model_id.startswith("cloud:"):
            raise ModelRuntimeError(
                "cloud:* model aliases are no longer supported. "
                "Use ollama:<name> or register a local GGUF model."
            )

        # Standard GGUF/local model
        try:
            record = state.registry.get_model(model_id)
        except KeyError:
            raise NotFoundError("Model", model_id)

        try:
            active = record.active()
            threads = (
                req.threads
                or runtime_defaults.default_threads
                or detect_hardware_summary().get("cpu_threads", 1)
            )
            state.runtime_manager.load(
                record.runtime, model_id, active.file_path, threads=threads
            )
        except Exception as exc:
            raise ModelRuntimeError(f"Failed to load model: {exc}")

        return {
            "ok": True,
            "loaded_model_id": state.runtime_manager.loaded_model_id,
            "loaded_runtime": state.runtime_manager.loaded_runtime,
            "threads": threads,
        }


@app.post("/chat")
def chat(request: Request, req: ChatReq, _rate_limit: None = Depends(check_rate_limit)):
    """Chat endpoint with proper SSE error handling (P2-91)."""
    state = get_app_state()
    request_id = getattr(request.state, "request_id", "unknown")

    # ── Billing access check ───────────────────────────────────────────────
    # browser: models are free; server/CLI models require a paid plan.
    is_browser = req.model_id.startswith("browser:")
    is_cli = request.headers.get("X-CLI", "").lower() == "true"
    message_type = "browser" if is_browser else ("cli" if is_cli else "server")

    identity = _get_caller_identity(request)
    _billing_uid: str | None = None
    _billing_mtype: str = message_type

    if identity is None:
        if not is_browser:
            raise HTTPException(status_code=401, detail="Login required to use server models.")
    else:
        uid = identity["uid"]
        email = identity["email"]
        ensure_user_record(uid, email)
        allowed, reason = check_access(uid, email, message_type)
        if not allowed:
            # Include upgrade URL in 402 response so frontend/CLI can redirect
            detail = {
                "error": reason,
                "upgrade_url": "https://sageworksai.com",
                "billing_tab": True,
            }
            raise HTTPException(status_code=402, detail=detail)
        _billing_uid = uid
        # Token usage is incremented AFTER we know the response length (done via SSE done event)

    # Auto-load model if not loaded or different model requested
    if state.runtime_manager.runtime is None or state.runtime_manager.loaded_model_id != req.model_id:
        model_id = req.model_id

        # Use lock for model loading (P2-89)
        with state.runtime_lock:
            try:
                if model_id.startswith("ollama:"):
                    # Check Ollama is reachable before trying to load
                    import httpx as _httpx
                    try:
                        with _httpx.Client(timeout=2) as _c:
                            _c.get("http://localhost:11434/api/tags").raise_for_status()
                    except Exception:
                        raise ModelRuntimeError(
                            "Ollama is not running on this server. "
                            "To use local AI models, run Ollama on your own machine and "
                            "host the sage-ai platform locally, or install the sage CLI: "
                            "pip install sage-ai-cli && sage pull " + model_id.removeprefix("ollama:")
                        )
                    state.runtime_manager.load(
                        "ollama", model_id, model_id.removeprefix("ollama:"), threads=None
                    )
                elif model_id.startswith("cloud:"):
                    raise ModelRuntimeError(
                        "cloud:* model aliases are no longer supported. "
                        "Use ollama:<name> or register a local GGUF model."
                    )
                else:
                    # Try loading as registered GGUF model.
                    # If not registered but present in the GCS catalog, auto-download it
                    # from the public GCS bucket so the user never has to use the CLI.
                    try:
                        record = state.registry.get_model(model_id)
                    except KeyError:
                        record = None

                    if record is None:
                        # Check GCS catalog for this model_id
                        from sage.models.catalog import get_full_catalog
                        catalog_entry = next(
                            (m for m in get_full_catalog()
                             if m.backend == "gguf" and m.name == model_id and m.url),
                            None
                        )
                        if catalog_entry is None:
                            raise ModelRuntimeError(
                                f"Model '{model_id}' is not available. "
                                "Browse the Downloads tab to see available models."
                            )
                        # Auto-download from GCS (this is the first use)
                        import httpx as _httpx
                        from pathlib import Path as _Path
                        dest = _Path(f"/app/models/{catalog_entry.filename}")
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        if not dest.exists() or dest.stat().st_size < 1_000_000:
                            logger.info(f"Auto-downloading {model_id} ({catalog_entry.size_gb:.1f} GB) from GCS...")
                            with _httpx.Client(follow_redirects=True, timeout=600) as dl_client:
                                with dl_client.stream("GET", catalog_entry.url) as dl_resp:
                                    dl_resp.raise_for_status()
                                    with dest.open("wb") as fout:
                                        for chunk in dl_resp.iter_bytes(chunk_size=1024 * 1024):
                                            fout.write(chunk)
                            logger.info(f"Downloaded {model_id} to {dest}")
                        # Register in registry
                        import datetime as _dt
                        state.registry._save_raw({
                            **state.registry._load_raw(),
                            model_id: {
                                "model_id": model_id,
                                "runtime": "llama_cpp",
                                "license": "",
                                "format": "gguf",
                                "source_repo": "gcs",
                                "active_version": 1,
                                "versions": [{
                                    "version": 1,
                                    "version_tag": "gcs",
                                    "file_path": str(dest),
                                    "source_url": catalog_entry.url,
                                    "sha256": "",
                                    "size_gb": catalog_entry.size_gb,
                                    "created_at": _dt.datetime.utcnow().isoformat() + "Z",
                                }],
                            }
                        })
                        record = state.registry.get_model(model_id)

                    try:
                        active = record.active()
                        threads = detect_hardware_summary().get("cpu_threads", 1)
                        state.runtime_manager.load(record.runtime, model_id, active.file_path, threads=threads)
                    except Exception as exc:
                        raise ModelRuntimeError(f"Failed to load model: {exc}")
            except (NotFoundError, ValidationError, ModelRuntimeError):
                raise
            except Exception as exc:
                raise ModelRuntimeError(f"Failed to load model: {exc}")

    conv_id = req.conversation_id

    # Process messages with file attachments
    processed_messages = []
    for msg in req.messages:
        content = msg.content

        # If message has attachments, expand file content into context
        if hasattr(msg, 'attachments') and msg.attachments:
            attachment_contents = []
            for att in msg.attachments:
                try:
                    file_content = file_store.get_content_for_chat(att.file_id)
                    attachment_contents.append(file_content)
                except KeyError:
                    logger.warning(f"File not found for attachment: {att.file_id}")

            if attachment_contents:
                content = content + "\n\n" + "\n\n".join(attachment_contents)

        processed_messages.append(ChatMessage(role=msg.role, content=content))

        # Log user input
        if conv_id and msg.role == "user":
            attachments_data = None
            if hasattr(msg, 'attachments') and msg.attachments:
                attachments_data = [
                    {"file_id": a.file_id, "filename": a.filename}
                    for a in msg.attachments
                ]
            conversation_logger.log_input(
                conversation_id=conv_id,
                content=msg.content,
                attachments=attachments_data
            )

    if conv_id:
        for msg in req.messages:
            state.conversation_store.append_message(conv_id, msg.role, msg.content)

    messages = processed_messages

    def stream_with_error_handling():
        """SSE stream generator with structured error events (P2-91)."""
        chunks = []
        error_occurred = False

        try:
            # Send initial step indicator
            yield f"data: {json.dumps({'step': 'thinking', 'message': 'Processing your message...'})}\n\n"
            yield f"data: {json.dumps({'step': 'generating', 'message': 'Generating response...'})}\n\n"

            for token in state.runtime_manager.runtime.stream_chat(
                messages,
                temperature=req.temperature,
                max_tokens=req.max_tokens,
            ):
                chunks.append(token)
                yield f"data: {json.dumps({'token': token})}\n\n"

            final = "".join(chunks).strip()
            if conv_id:
                state.conversation_store.append_message(conv_id, "assistant", final)
                conversation_logger.log_output(
                    conversation_id=conv_id,
                    content=final,
                    model_id=req.model_id
                )

            # Track token usage after we know the full response length
            if _billing_uid:
                try:
                    from .billing import tokens_from_text
                    _response_tokens = tokens_from_text(final)
                    increment_usage(_billing_uid, _billing_mtype, tokens=_response_tokens)
                except Exception:
                    pass

            yield f"data: {json.dumps({'step': 'complete', 'message': 'Done'})}\n\n"
            yield f"data: {json.dumps({'done': True, 'conversation_id': conv_id})}\n\n"

        except Exception as exc:
            # P2-91: Structured error event for SSE failures
            error_occurred = True
            error_event = {
                "error": True,
                "error_code": "STREAM_ERROR",
                "message": str(exc),
                "request_id": request_id,
                "partial_response": "".join(chunks) if chunks else None,
            }
            yield f"data: {json.dumps(error_event)}\n\n"

            # Log the error
            logger.error(f"Stream error in request {request_id}: {exc}")

        finally:
            if not error_occurred:
                # Log successful completion
                state.log_audit(
                    action="CHAT_COMPLETE",
                    request_id=request_id,
                    client_id=state.rate_limiter.get_client_id(request),
                    details={"model_id": req.model_id, "tokens": len(chunks)},
                )

    if req.stream:
        return StreamingResponse(stream_with_error_handling(), media_type="text/event-stream")

    # Non-streaming response
    try:
        text = state.runtime_manager.runtime.chat(
            messages,
            temperature=req.temperature,
            max_tokens=req.max_tokens,
        )
        if conv_id:
            state.conversation_store.append_message(conv_id, "assistant", text)
            # Log AI output
            conversation_logger.log_output(
                conversation_id=conv_id,
                content=text,
                model_id=req.model_id
            )
        return {"ok": True, "output": text, "conversation_id": conv_id}
    except Exception as exc:
        raise ModelRuntimeError(f"Chat failed: {exc}")


@app.post("/conversations")
def create_conversation(req: CreateConversationReq):
    state = get_app_state()
    conversation = state.conversation_store.create(req.title)
    return {"ok": True, "conversation": conversation}


@app.get("/conversations")
def list_conversations():
    state = get_app_state()
    return {"ok": True, "conversations": state.conversation_store.list_all()}


@app.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str):
    # Validate path parameter (TDD Cycle)
    conversation_id = validate_conversation_id_path(conversation_id)
    state = get_app_state()
    try:
        conversation = state.conversation_store.get(conversation_id)
    except KeyError:
        raise NotFoundError("Conversation", conversation_id)
    return {"ok": True, "conversation": conversation}


@app.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: str):
    # Validate path parameter (TDD Cycle)
    conversation_id = validate_conversation_id_path(conversation_id)
    state = get_app_state()
    state.conversation_store.delete(conversation_id)
    # Also delete conversation logs
    conversation_logger.delete(conversation_id)
    return {"ok": True}


@app.get("/conversations/{conversation_id}/logs")
def get_conversation_logs(conversation_id: str):
    """Get input/output logs for a conversation."""
    conversation_id = validate_conversation_id_path(conversation_id)
    return {
        "ok": True,
        "inputs": conversation_logger.get_inputs(conversation_id),
        "outputs": conversation_logger.get_outputs(conversation_id),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# File Upload/Download Endpoints
# ═══════════════════════════════════════════════════════════════════════════════


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file for use in chat."""
    # Read file content
    content = await file.read()

    # Validate file size
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="File cannot be empty")

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds maximum size of {MAX_FILE_SIZE // (1024*1024)}MB"
        )

    # Determine MIME type
    mime_type = file.content_type or "application/octet-stream"

    try:
        file_id = file_store.save(
            content=content,
            filename=file.filename or "unnamed",
            mime_type=mime_type,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    metadata = file_store.get_metadata(file_id)

    return {
        "ok": True,
        "file_id": file_id,
        "filename": metadata["filename"],
        "mime_type": metadata["mime_type"],
        "size_bytes": metadata["size_bytes"],
        "content_preview": metadata.get("content_preview"),
    }


@app.get("/files/{file_id}")
def download_file(file_id: str):
    """Download a file by ID."""
    # Validate file_id
    try:
        validate_safe_id(file_id, "file_id")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid file ID")

    try:
        file_data = file_store.get(file_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="File not found")

    return Response(
        content=file_data["content"],
        media_type=file_data["mime_type"],
        headers={
            "Content-Disposition": f'attachment; filename="{file_data["filename"]}"'
        },
    )


@app.get("/files")
def list_files():
    """List all uploaded files."""
    return {"ok": True, "files": file_store.list_all()}


@app.delete("/files/{file_id}")
def delete_file(file_id: str):
    """Delete a file by ID."""
    try:
        validate_safe_id(file_id, "file_id")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid file ID")

    file_store.delete(file_id)
    return {"ok": True}


@app.post("/paste")
def submit_large_text(req: LargeTextContent):
    """Submit large text content to be treated as a file."""
    content_bytes = req.content.encode("utf-8")

    # Check if small enough to handle inline
    if len(content_bytes) < LARGE_TEXT_THRESHOLD:
        return {
            "ok": True,
            "inline": True,
            "content": req.content,
            "size_bytes": len(content_bytes),
            "language": req.language,
        }

    # Save as file
    mime_type = "text/plain"
    if req.language:
        # Map language to MIME type
        lang_mime_map = {
            "python": "text/x-python",
            "py": "text/x-python",
            "javascript": "text/javascript",
            "js": "text/javascript",
            "typescript": "text/typescript",
            "ts": "text/typescript",
            "java": "text/x-java",
            "c": "text/x-c",
            "cpp": "text/x-c++",
            "go": "text/x-go",
            "rust": "text/x-rust",
            "json": "application/json",
            "yaml": "application/x-yaml",
            "yml": "application/x-yaml",
            "html": "text/html",
            "css": "text/css",
            "markdown": "text/markdown",
            "md": "text/markdown",
            "sh": "application/x-sh",
            "bash": "application/x-sh",
        }
        mime_type = lang_mime_map.get(req.language.lower(), "text/plain")

    try:
        file_id = file_store.save(
            content=content_bytes,
            filename=req.filename,
            mime_type=mime_type,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    metadata = file_store.get_metadata(file_id)

    return {
        "ok": True,
        "inline": False,
        "file_id": file_id,
        "filename": metadata["filename"],
        "size_bytes": metadata["size_bytes"],
        "language": req.language,
    }


@app.get("/sources")
def list_sources():
    state = get_app_state()
    return {"ok": True, "sources": [s.__dict__ for s in state.updater.list_sources()]}


@app.post("/sources/add")
def add_source(
    request: Request,
    req: AddSourceReq,
    _admin: None = Depends(_require_admin_token_strict),
):
    state = get_app_state()

    # Audit log
    state.log_audit(
        action="SOURCE_ADD",
        request_id=getattr(request.state, "request_id", "unknown"),
        client_id=state.rate_limiter.get_client_id(request),
        details={"model_id": req.model_id, "repo_url": req.repo_url},
    )

    try:
        source = state.updater.add_source(
            repo_url=req.repo_url,
            model_id=req.model_id,
            runtime=req.runtime,
            asset_pattern=req.asset_pattern,
            license=req.license,
        )
    except ValueError as exc:
        raise ValidationError(str(exc))
    return {"ok": True, "source": source.__dict__}


@app.delete("/sources/{model_id}")
def remove_source(
    request: Request,
    model_id: str,
    _admin: None = Depends(_require_admin_token_strict),
):
    state = get_app_state()

    # Audit log
    state.log_audit(
        action="SOURCE_REMOVE",
        request_id=getattr(request.state, "request_id", "unknown"),
        client_id=state.rate_limiter.get_client_id(request),
        details={"model_id": model_id},
    )

    state.updater.remove_source(model_id)
    return {"ok": True}


def _catalog_with_gcs() -> list[CatalogModel]:
    """Return the full catalog merged with any GGUF files live in GCS.

    catalog.json is updated periodically by sync_catalog.py, but models
    uploaded via /gcs/pull or the CLI sync never appear in the hardcoded
    catalog. This function adds them dynamically so the Downloads tab
    always reflects actual bucket contents.
    """
    models = list(get_full_catalog())
    state = get_app_state()
    if not state.gcs_manager:
        return models
    try:
        known = {m.name for m in models}
        for gm in state.gcs_manager.list_gcs_models():
            if gm.name in known:
                continue
            # Model is in GCS but not in the catalog — add it as a plain GGUF entry.
            display = (gm.display_name or gm.name).replace("-", " ").replace("_", " ").title()
            models.append(CatalogModel(
                name=gm.name,
                display_name=display,
                filename=gm.filename,
                url=gm.url,
                size_gb=gm.size_gb or 0.0,
                params=gm.params or "",
                family=gm.family or "",
                description=gm.description or "Custom model stored in GCS",
                backend="gguf",
                category=gm.category or "general",
                default=False,
            ))
            known.add(gm.name)
    except Exception:
        pass  # Never fail the catalog endpoint due to a GCS connectivity issue
    return models


@app.get("/catalog")
def catalog(backend: str | None = None):
    """List models from the Sage catalog.

    Args:
        backend: Filter by backend type (gguf, ollama, or all). Defaults to "gguf".

    Tries the remote GCS catalog first for auto-updated models,
    falls back to the hardcoded catalog.
    """
    all_models = _catalog_with_gcs()

    # Filter by backend if specified
    if backend and backend != "all":
        filtered_models = [m for m in all_models if m.backend == backend]
    elif backend == "all":
        filtered_models = all_models
    else:
        # Default to GGUF for backwards compatibility
        filtered_models = [m for m in all_models if m.backend == "gguf"]

    return {
        "ok": True,
        "models": [
            {
                "model_id": m.name,
                "name": m.display_name,
                "description": m.description,
                "params": m.params,
                "size_gb": m.size_gb,
                "family": m.family,
                "filename": m.filename,
                "url": m.url,
                "default": m.default,
                "backend": m.backend,
                "category": m.category,
                "tags": list(m.tags) if m.tags else [],
            }
            for m in filtered_models
        ],
        "total": len(filtered_models),
    }


@app.get("/catalog/all")
def catalog_all(category: str | None = None, search: str | None = None):
    """List ALL models from the Sage catalog (GGUF + Ollama + Cloud).

    Args:
        category: Filter by category (coding, reasoning, general, vision, small, embedding)
        search: Search models by name or description
    """
    all_models = _catalog_with_gcs()

    if search:
        q = search.lower()
        results = [
            m for m in all_models
            if q in m.name.lower() or q in m.display_name.lower()
            or q in m.description.lower() or q in m.category.lower()
        ]
    elif category:
        results = [m for m in all_models if m.category == category]
    else:
        results = all_models

    return {
        "ok": True,
        "models": [
            {
                "model_id": m.name,
                "name": m.display_name,
                "description": m.description,
                "params": m.params,
                "size_gb": m.size_gb,
                "family": m.family,
                "filename": m.filename,
                "url": m.url,
                "default": m.default,
                "backend": m.backend,
                "category": m.category,
                "tags": list(m.tags) if m.tags else [],
            }
            for m in results
        ],
        "total": len(results),
    }


@app.get("/catalog/recommended")
def catalog_recommended():
    return {"ok": True, "models": get_recommended_models()}


@app.get("/catalog/fits-ram")
def catalog_fits_ram(max_gb: float):
    return {"ok": True, "models": filter_by_ram(max_gb)}


@app.get("/ollama/catalog")
def ollama_catalog(category: str | None = None, search: str | None = None):
    """List all Ollama models available to pull.

    Uses remote GCS catalog for auto-updated model list.
    """
    all_models = _catalog_with_gcs()
    ollama_models = [m for m in all_models if m.backend == "ollama"]

    if search:
        q = search.lower()
        results = [
            m for m in ollama_models
            if q in m.name.lower() or q in m.display_name.lower()
            or q in m.description.lower() or q in m.category.lower()
        ]
    elif category:
        results = [m for m in ollama_models if m.category == category]
    else:
        results = ollama_models
    return {
        "ok": True,
        "models": [
            {
                "name": m.name,
                "display_name": m.display_name,
                "sizes": m.params,
                "tags": list(m.tags),
                "description": m.description,
                "pulls": "",
                "category": m.category,
            }
            for m in results
        ],
    }


@app.get("/ollama/status")
def ollama_status():
    """Check if Ollama is running and list pulled models."""
    import httpx
    try:
        with httpx.Client(timeout=3) as client:
            resp = client.get("http://localhost:11434/api/tags")
            resp.raise_for_status()
            data = resp.json()
            models = [
                {"name": m["name"], "size": m.get("size", 0), "modified": m.get("modified_at", "")}
                for m in data.get("models", [])
            ]
            return {"ok": True, "running": True, "models": models}
    except Exception:
        return {"ok": True, "running": False, "models": []}


@app.get("/free-models")
def free_models():
    """Deprecated endpoint — Pollinations cloud models have been removed.

    Use ``GET /ollama/recommended`` or install models locally (``sage pull`` / ``ollama pull``).
    """
    return {
        "ok": True,
        "models": [],
        "message": "Pollinations-backed cloud models are no longer exposed. Use local Ollama or GGUF models.",
    }


@app.get("/ollama/recommended")
def ollama_recommended():
    """Return recommended Ollama models for Sage."""
    results = get_recommended_ollama_models()
    return {
        "ok": True,
        "models": [
            {
                "name": m.name,
                "display_name": m.display_name,
                "sizes": m.params,
                "tags": list(m.tags),
                "description": m.description,
                "category": m.category,
            }
            for m in results
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# GCS Model Management - Pull/Upload/Delete Cycle
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/gcs/status")
def gcs_status():
    """Check GCS manager status and Ollama availability."""
    state = get_app_state()

    gcs_available = state.gcs_manager is not None
    ollama_running = False

    if gcs_available:
        ollama_running = state.gcs_manager.ollama.is_running()

    return {
        "ok": True,
        "gcs_available": gcs_available,
        "ollama_running": ollama_running,
    }


@app.get("/gcs/models")
def gcs_list_models():
    """List all models available in GCS."""
    state = get_app_state()

    if not state.gcs_manager:
        raise ModelRuntimeError("GCS manager not initialized")

    try:
        models = state.gcs_manager.list_gcs_models()
        return {
            "ok": True,
            "models": [
                {
                    "name": m.name,
                    "display_name": m.display_name,
                    "filename": m.filename,
                    "url": m.url,
                    "size_gb": m.size_gb,
                    "params": m.params,
                    "family": m.family,
                    "description": m.description,
                    "category": m.category,
                    "tags": m.tags,
                    "checksum": m.checksum,
                    "uploaded_at": m.uploaded_at,
                    "source": m.source,
                }
                for m in models
            ],
        }
    except Exception as exc:
        raise ModelRuntimeError(f"Failed to list GCS models: {exc}")


@app.get("/gcs/models/{model_name}")
def gcs_get_model(model_name: str):
    """Get info about a specific model in GCS."""
    # Validate path parameter (TDD Cycle)
    model_name = validate_model_name_path(model_name)
    state = get_app_state()

    if not state.gcs_manager:
        raise ModelRuntimeError("GCS manager not initialized")

    model = state.gcs_manager.get_model_info(model_name)
    if not model:
        raise NotFoundError("Model", model_name)

    return {
        "ok": True,
        "model": {
            "name": model.name,
            "display_name": model.display_name,
            "filename": model.filename,
            "url": model.url,
            "size_gb": model.size_gb,
            "params": model.params,
            "family": model.family,
            "description": model.description,
            "category": model.category,
            "tags": model.tags,
            "checksum": model.checksum,
            "uploaded_at": model.uploaded_at,
            "source": model.source,
        },
    }


@app.post("/gcs/pull")
def gcs_pull_upload(
    request: Request,
    ollama_model: str,
    display_name: str | None = None,
    description: str | None = None,
    family: str | None = None,
    category: str = "general",
    delete_after_upload: bool = False,
    _admin: None = Depends(_require_admin_token_strict),
    _rate_limit: None = Depends(check_gcs_rate_limit),  # P1-12
):
    """Pull a model from Ollama, convert to GGUF, and upload to GCS.

    This is the main endpoint for the pull-upload-delete cycle.

    Args:
        ollama_model: Ollama model name (e.g., "qwen2.5:7b")
        display_name: Human-readable name (optional)
        description: Model description (optional)
        family: Model family (optional)
        category: Category (coding, reasoning, general, etc.)
        delete_after_upload: Whether to delete from Ollama after upload
    """
    state = get_app_state()
    request_id = getattr(request.state, "request_id", "unknown")
    client_id = state.rate_limiter.get_client_id(request)

    if not state.gcs_manager:
        raise ModelRuntimeError("GCS manager not initialized")

    # Audit log
    state.log_audit(
        action="GCS_PULL_UPLOAD",
        request_id=request_id,
        client_id=client_id,
        details={
            "ollama_model": ollama_model,
            "delete_after_upload": delete_after_upload,
        },
    )

    try:
        success, message = state.gcs_manager.pull_convert_upload(
            ollama_model=ollama_model,
            display_name=display_name,
            description=description,
            family=family,
            category=category,
            delete_after_upload=delete_after_upload,
        )

        return {
            "ok": success,
            "message": message,
        }
    except Exception as exc:
        raise ModelRuntimeError(f"Pull-upload failed: {exc}")


@app.post("/gcs/download/{model_name}")
def gcs_download(
    request: Request,
    model_name: str,
    _admin: None = Depends(_require_admin_token_strict),
    _rate_limit: None = Depends(check_gcs_rate_limit),  # P1-12
):
    """Download a model from GCS to local storage."""
    state = get_app_state()
    request_id = getattr(request.state, "request_id", "unknown")
    client_id = state.rate_limiter.get_client_id(request)

    if not state.gcs_manager:
        raise ModelRuntimeError("GCS manager not initialized")

    # Audit log
    state.log_audit(
        action="GCS_DOWNLOAD",
        request_id=request_id,
        client_id=client_id,
        details={"model_name": model_name},
    )

    try:
        path = state.gcs_manager.download_from_gcs(model_name)
        if path:
            return {
                "ok": True,
                "path": str(path),
                "message": f"Downloaded {model_name} to {path}",
            }
        else:
            raise NotFoundError("Model", model_name)
    except NotFoundError:
        raise
    except Exception as exc:
        raise ModelRuntimeError(f"Download failed: {exc}")


@app.delete("/gcs/models/{model_name}")
def gcs_delete(
    request: Request,
    model_name: str,
    _admin: None = Depends(_require_admin_token_strict),
):
    """Delete a model from GCS."""
    # Validate path parameter (TDD Cycle)
    model_name = validate_model_name_path(model_name)
    state = get_app_state()
    request_id = getattr(request.state, "request_id", "unknown")
    client_id = state.rate_limiter.get_client_id(request)

    if not state.gcs_manager:
        raise ModelRuntimeError("GCS manager not initialized")

    # Get filename from model info first
    model = state.gcs_manager.get_model_info(model_name)
    if not model:
        raise NotFoundError("Model", model_name)

    # Audit log
    state.log_audit(
        action="GCS_DELETE",
        request_id=request_id,
        client_id=client_id,
        details={"model_name": model_name, "filename": model.filename},
    )

    try:
        success = state.gcs_manager.delete_from_gcs(model.filename)
        return {
            "ok": success,
            "message": f"Deleted {model_name}" if success else f"Failed to delete {model_name}",
        }
    except Exception as exc:
        raise ModelRuntimeError(f"Delete failed: {exc}")


@app.post("/gcs/sync")
def gcs_sync(
    request: Request,
    delete_after_upload: bool = False,
    _admin: None = Depends(_require_admin_token_strict),
):
    """Sync all pulled Ollama models to GCS.

    This pulls all currently pulled Ollama models and uploads them to GCS.
    """
    state = get_app_state()
    request_id = getattr(request.state, "request_id", "unknown")
    client_id = state.rate_limiter.get_client_id(request)

    if not state.gcs_manager:
        raise ModelRuntimeError("GCS manager not initialized")

    # Audit log
    state.log_audit(
        action="GCS_SYNC",
        request_id=request_id,
        client_id=client_id,
        details={"delete_after_upload": delete_after_upload},
    )

    try:
        results = state.gcs_manager.sync_ollama_to_gcs(
            models=None,  # All pulled models
            delete_after_upload=delete_after_upload,
        )

        return {
            "ok": True,
            "results": {
                model: {"success": success, "message": message}
                for model, (success, message) in results.items()
            },
        }
    except Exception as exc:
        raise ModelRuntimeError(f"Sync failed: {exc}")


@app.get("/ollama/pulled")
def ollama_pulled():
    """List all models currently pulled in Ollama."""
    state = get_app_state()

    if not state.gcs_manager:
        # Fall back to direct Ollama API call
        client = OllamaClient()
        if not client.is_running():
            return {"ok": True, "running": False, "models": []}

        models = client.list_models()
        client.close()
    else:
        if not state.gcs_manager.ollama.is_running():
            return {"ok": True, "running": False, "models": []}

        models = state.gcs_manager.ollama.list_models()

    return {
        "ok": True,
        "running": True,
        "models": [
            {
                "name": m.get("name", ""),
                "size": m.get("size", 0),
                "size_gb": m.get("size", 0) / 1e9,
                "modified": m.get("modified_at", ""),
            }
            for m in models
        ],
    }


@app.delete("/ollama/models/{model_name}")
def ollama_delete(
    request: Request,
    model_name: str,
    _admin: None = Depends(_require_admin_token_strict),
):
    """Delete a model from Ollama."""
    # Validate path parameter (TDD Cycle)
    model_name = validate_model_name_path(model_name)
    state = get_app_state()
    request_id = getattr(request.state, "request_id", "unknown")
    client_id = state.rate_limiter.get_client_id(request)

    # Audit log
    state.log_audit(
        action="OLLAMA_DELETE",
        request_id=request_id,
        client_id=client_id,
        details={"model_name": model_name},
    )

    if state.gcs_manager:
        success = state.gcs_manager.delete_from_ollama(model_name)
    else:
        client = OllamaClient()
        success = client.delete_model(model_name)
        client.close()

    return {
        "ok": success,
        "message": f"Deleted {model_name} from Ollama" if success else f"Failed to delete {model_name}",
    }


# ═══════════════════════════════════════════════════════════════════════════════
# WebSocket Terminal Endpoint (WebGL-accelerated xterm.js)
# ═══════════════════════════════════════════════════════════════════════════════


@app.websocket("/ws/terminal")
async def websocket_terminal(websocket: WebSocket):
    """WebSocket endpoint for WebGL terminal running sage-ai-cli."""
    await terminal_websocket_handler(websocket)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI Auto-Update Endpoints
# ═══════════════════════════════════════════════════════════════════════════════


@app.get("/api/cli/check-update")
def check_cli_update():
    """Check if a sage-ai-cli update is available."""
    return get_cli_update_info()


@app.post("/api/cli/apply-update")
def apply_update_endpoint(_admin: None = Depends(_require_admin_token_strict)):
    """Apply sage-ai-cli update (requires admin token)."""
    return apply_cli_update()


# ═══════════════════════════════════════════════════════════════════════════════
# Billing endpoints
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/billing/track")
async def billing_track(request: Request):
    """Track AI usage for the current user (fire-and-forget).

    Body: { "type": "server"|"cli"|"browser", "tokens": int, "text": str }
    - Called by the frontend after each browser model response
    - Called by the CLI after each local inference
    - tokens: actual output token count (or estimated from text length)
    """
    identity = _get_caller_identity(request)
    if identity is None:
        return {"ok": False, "reason": "not authenticated"}
    body = {}
    try:
        body = await request.json()
    except Exception:
        pass
    message_type = body.get("type", "server")
    if message_type not in ("server", "cli", "browser"):
        message_type = "server"
    uid, email = identity["uid"], identity["email"]
    if email not in ADMIN_EMAILS:
        try:
            from .billing import tokens_from_text
            # Accept explicit token count, estimate from text, or default to 500
            tokens = body.get("tokens") or tokens_from_text(body.get("text", "")) or 500
            increment_usage(uid, message_type, tokens=int(tokens))
        except Exception:
            pass
    return {"ok": True}


@app.get("/billing/me")
def billing_me(request: Request):
    """Get the current user's billing record + usage for the current month."""
    identity = _require_auth(request)
    uid, email = identity["uid"], identity["email"]
    record = get_user_record(uid)
    usage = get_usage(uid)
    from .billing import TIERS, ADMIN_EMAILS, _month_key
    tier = "admin" if email in ADMIN_EMAILS else record.get("tier", "free")
    tier_info = TIERS.get(tier, TIERS["free"])
    tokens_used = usage.get("tokens_used", 0)
    token_limit = tier_info.get("token_limit", 0)
    tokens_remaining = max(0, token_limit - tokens_used) if token_limit > 0 else None
    return {
        "ok": True,
        "uid": uid,
        "email": email,
        "tier": tier,
        "tier_info": tier_info,
        "subscription_status": record.get("subscription_status"),
        "usage": usage,
        "tokens_used": tokens_used,
        "token_limit": token_limit,
        "tokens_remaining": tokens_remaining,
        "billing_month": _month_key(),
        "upgrade_url": "https://sageworksai.com",
        "paypal_client_id": PAYPAL_CLIENT_ID,
        "paypal_plans": PAYPAL_PLAN_IDS,
    }


@app.post("/billing/subscribe")
def billing_subscribe(request: Request):
    """Activate a PayPal subscription after user approves it."""
    import json as _json
    body = request.state.__dict__.get("body") or {}
    try:
        raw = request._body if hasattr(request, "_body") else b""
        if not raw:
            import asyncio
            raw = asyncio.run(request.body()) if not asyncio.get_event_loop().is_running() else b""
        body = _json.loads(raw or b"{}") if raw else {}
    except Exception:
        body = {}

    identity = _require_auth(request)
    subscription_id = body.get("subscription_id", "")
    if not subscription_id:
        raise HTTPException(status_code=400, detail="subscription_id required")

    try:
        tier = activate_subscription(identity["uid"], subscription_id)
        return {"ok": True, "tier": tier, "subscription_id": subscription_id}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/billing/subscribe-body")
async def billing_subscribe_body(request: Request):
    """Activate a PayPal subscription — async version to properly read body."""
    identity = _require_auth(request)
    body = await request.json()
    subscription_id = body.get("subscription_id", "")
    if not subscription_id:
        raise HTTPException(status_code=400, detail="subscription_id required")
    try:
        tier = activate_subscription(identity["uid"], subscription_id)
        return {"ok": True, "tier": tier, "subscription_id": subscription_id}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.delete("/billing/subscription")
def billing_cancel(request: Request):
    """Cancel the current user's subscription and downgrade to free."""
    identity = _require_auth(request)
    cancel_subscription(identity["uid"])
    return {"ok": True, "message": "Subscription cancelled. You will retain access until the end of the billing period."}


@app.get("/account/providers")
def account_get_providers(request: Request):
    """Return the OAuth providers linked to this account (Google, Apple, etc.)."""
    from firebase_admin import auth as fb_auth
    identity = _require_auth(request)
    try:
        record = fb_auth.get_user(identity["uid"])
        providers = [
            {
                "provider_id":   p.provider_id,
                "email":         p.email or "",
                "display_name":  p.display_name or "",
                "photo_url":     p.photo_url or "",
            }
            for p in record.provider_data
        ]
    except Exception as exc:
        logger.warning("get_providers failed: %s", exc)
        providers = []
    return {"ok": True, "providers": providers}


@app.post("/account/sync-contacts")
def account_sync_contacts(request: Request):
    """Auto-register linked Google/Apple emails as authorized SMS contacts."""
    from firebase_admin import auth as fb_auth
    from .sms_manager import add_contact
    identity = _require_auth(request)
    try:
        record = fb_auth.get_user(identity["uid"])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    added = []
    for p in record.provider_data:
        if p.email and p.provider_id in ("google.com", "apple.com"):
            name = "Google" if p.provider_id == "google.com" else "Apple"
            add_contact(identity["uid"], p.email, f"{name} — {p.email}")
            added.append({"email": p.email, "provider": name})
    return {"ok": True, "added": added}


@app.delete("/account")
def account_delete(request: Request):
    """Delete the user's account and all data."""
    identity = _require_auth(request)
    delete_account(identity["uid"])
    return {"ok": True, "message": "Account and all data deleted."}


@app.post("/billing/webhook")
async def billing_webhook(request: Request):
    """PayPal webhook — verifies signature and processes subscription events."""
    import hmac, hashlib
    body = await request.body()
    event = {}
    try:
        import json as _json
        event = _json.loads(body)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    event_type = event.get("event_type", "")
    resource = event.get("resource", {})
    try:
        handle_webhook(event_type, resource)
    except Exception as exc:
        logger.warning("Webhook handling error: %s", exc)

    return {"ok": True}


@app.get("/billing/usage")
def billing_usage(request: Request):
    """Return usage stats for the current month."""
    identity = _require_auth(request)
    usage = get_usage(identity["uid"])
    return {"ok": True, "usage": usage}


# ── CLI auth endpoint ──────────────────────────────────────────────────────────

@app.post("/auth/verify")
async def auth_verify(request: Request):
    """Verify a Firebase ID token and return user billing info. Used by CLI."""
    body = await request.json()
    token = body.get("token", "")
    if not token:
        raise HTTPException(status_code=400, detail="token required")
    identity = _verify_firebase_token(token)
    uid, email = identity["uid"], identity["email"]
    ensure_user_record(uid, email)
    record = get_user_record(uid)
    from .billing import ADMIN_EMAILS
    tier = "admin" if email in ADMIN_EMAILS else record.get("tier", "free")
    return {"ok": True, "uid": uid, "email": email, "tier": tier}


# ── SMS Device & Contact Registry ─────────────────────────────────────────────
# Each user manages their own computers and authorized phone contacts.
# All endpoints require a valid SAGE Firebase auth token.

@app.websocket("/ws/sms")
async def sms_cli_websocket(websocket: WebSocket):
    """
    Persistent WebSocket for sage sms start.

    Protocol:
      CLI  → {"type":"auth","token":"<firebase>","computer_name":"macbook"}
      SAGE → {"type":"ready","bridge_email":"message@sageworksai.com","display_email":"..."}
      SAGE → {"type":"task","task_id":"uuid","task":"...","from":"user@icloud.com"}
      CLI  → {"type":"result","task_id":"uuid","output":"..."}
      CLI  → {"type":"heartbeat"}  (every 30s, keeps connection alive)
    """
    from .sms_poller import (
        register_cli_session, unregister_cli_session,
        resolve_task_result, BRIDGE_EMAIL, DISPLAY_EMAIL,
    )
    from .sms_manager import register_computer

    await websocket.accept()
    uid = None
    computer_name = None

    try:
        # First message must be auth
        auth_msg = await asyncio.wait_for(websocket.receive_json(), timeout=15)
        if auth_msg.get("type") != "auth":
            await websocket.close(code=4001, reason="First message must be auth")
            return

        token = auth_msg.get("token", "")
        computer_name = auth_msg.get("computer_name", "").strip()
        if not token or not computer_name:
            await websocket.close(code=4002, reason="token and computer_name required")
            return

        try:
            identity = _verify_firebase_token(token)
        except Exception:
            await websocket.close(code=4003, reason="Invalid auth token")
            return

        uid = identity["uid"]
        ensure_user_record(uid, identity["email"])

        # Register computer in Firestore (idempotent)
        register_computer(uid, computer_name, BRIDGE_EMAIL or "")

        # Register active WebSocket session for task dispatch
        register_cli_session(uid, computer_name, websocket)

        await websocket.send_json({
            "type": "ready",
            "bridge_email": BRIDGE_EMAIL,
            "display_email": DISPLAY_EMAIL or BRIDGE_EMAIL,
            "computer_name": computer_name,
        })

        # Message loop
        while True:
            msg = await websocket.receive_json()
            msg_type = msg.get("type", "")

            if msg_type == "result":
                resolve_task_result(msg.get("task_id", ""), msg.get("output", ""))

            elif msg_type == "heartbeat":
                await websocket.send_json({"type": "pong"})

    except Exception as exc:
        logger.debug("SMS WS closed: %s", exc)
    finally:
        if uid and computer_name:
            unregister_cli_session(uid, computer_name)


@app.post("/sms/computers/register")
async def sms_register_computer(request: Request):
    """Register (or refresh) a computer for the authenticated user's SMS bridge."""
    from .sms_manager import register_computer
    identity = _require_auth(request)
    body = await request.json()
    computer_name = body.get("computer_name", "").strip()
    if not computer_name:
        raise HTTPException(status_code=400, detail="computer_name required")
    # bridge_email is optional now — SAGE owns the bridge email
    bridge_email = body.get("bridge_email", "").strip()
    result = register_computer(identity["uid"], computer_name, bridge_email)
    return {"ok": True, "computer": result}


@app.post("/sms/computers/heartbeat")
async def sms_computer_heartbeat(request: Request):
    """Update last_seen for a running computer. Called every poll cycle by the bridge."""
    from .sms_manager import heartbeat_computer
    identity = _require_auth(request)
    body = await request.json()
    computer_name = body.get("computer_name", "").strip()
    if not computer_name:
        raise HTTPException(status_code=400, detail="computer_name required")
    heartbeat_computer(identity["uid"], computer_name)
    return {"ok": True}


@app.get("/sms/computers")
def sms_list_computers(request: Request):
    """List all registered computers for the authenticated user."""
    from .sms_manager import list_computers
    identity = _require_auth(request)
    computers = list_computers(identity["uid"])
    return {"ok": True, "computers": computers}


@app.delete("/sms/computers/{computer_id}")
def sms_remove_computer(computer_id: str, request: Request):
    """Remove a registered computer from the user's account."""
    from .sms_manager import remove_computer
    identity = _require_auth(request)
    ok = remove_computer(identity["uid"], computer_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Computer not found")
    return {"ok": True}


@app.post("/sms/contacts")
async def sms_add_contact(request: Request):
    """Add an authorized contact — accepts an email address or a phone number."""
    from .sms_manager import add_contact, _normalize_phone
    identity = _require_auth(request)
    body = await request.json()
    raw   = body.get("email", "").strip()
    label = body.get("label", "").strip()
    if not raw:
        raise HTTPException(status_code=400, detail="email or phone number required")
    # Accept phone numbers (digits only) or valid email addresses
    phone = _normalize_phone(raw)
    if not phone and "@" not in raw:
        raise HTTPException(status_code=400, detail="Provide a valid email or 10-digit phone number")
    result = add_contact(identity["uid"], raw, label)
    return {"ok": True, "contact": result}


@app.get("/sms/contacts")
def sms_list_contacts(request: Request):
    """List all authorized phone contacts for the authenticated user."""
    from .sms_manager import list_contacts
    identity = _require_auth(request)
    contacts = list_contacts(identity["uid"])
    return {"ok": True, "contacts": contacts}


@app.delete("/sms/contacts/{email}")
def sms_remove_contact(email: str, request: Request):
    """Remove an authorized contact email."""
    from .sms_manager import remove_contact
    from urllib.parse import unquote
    identity = _require_auth(request)
    decoded_email = unquote(email)
    ok = remove_contact(identity["uid"], decoded_email)
    if not ok:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"ok": True}


@app.post("/sms/announce")
async def sms_announce_online(request: Request):
    """
    Send an 'I'm online' message from the bridge computer to all registered contacts.
    Called once by the CLI immediately after a successful WebSocket connection.
    """
    import asyncio
    from .sms_manager import get_contact_emails
    from .sms_poller import send_reply
    identity = _require_auth(request)
    body = await request.json()
    computer_name = body.get("computer_name", "SAGE").strip() or "SAGE"
    emails = get_contact_emails(identity["uid"])
    if not emails:
        return {"ok": True, "notified": 0}
    msg = (
        f"✅ [{computer_name}] SAGE is online and ready.\n"
        f"Send me any task and I'll run it on your computer.\n"
        f"Reply @help to see available commands."
    )
    loop = asyncio.get_event_loop()
    for email in emails:
        await loop.run_in_executor(None, send_reply, email, msg, computer_name)
    return {"ok": True, "notified": len(emails)}


@app.api_route("/__/auth/{path:path}", methods=["GET", "POST", "OPTIONS"])
async def firebase_auth_proxy(path: str, request: Request):
    """
    Proxy Firebase's OAuth handler to the same origin so signInWithPopup works
    with COOP: same-origin (required for crossOriginIsolated / WebLLM).

    Without this, the popup opens at sage-ai-d1c22.firebaseapp.com/__/auth/handler
    (a different origin). With COOP: same-origin, cross-origin popups cannot
    access window.opener, so Firebase can't deliver the OAuth token back.

    With this proxy the popup URL is sageworksai.com/__/auth/handler — same origin —
    so window.opener works and both WebLLM and Google/Apple sign-in work together.
    """
    from fastapi.responses import Response as _Resp
    firebase_project = os.environ.get("VITE_FIREBASE_PROJECT_ID", "sage-ai-d1c22")
    target = f"https://{firebase_project}.firebaseapp.com/__/auth/{path}"
    if request.query_params:
        target += "?" + str(request.query_params)
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            proxy_resp = await client.request(
                method=request.method,
                url=target,
                headers={
                    k: v for k, v in request.headers.items()
                    if k.lower() not in ("host", "content-length", "transfer-encoding")
                },
                content=await request.body(),
            )
        # Strip hop-by-hop headers that can't be forwarded
        skip = {"transfer-encoding", "content-encoding", "connection", "keep-alive"}
        headers = {k: v for k, v in proxy_resp.headers.items() if k.lower() not in skip}
        return _Resp(
            content=proxy_resp.content,
            status_code=proxy_resp.status_code,
            headers=headers,
        )
    except Exception as exc:
        logger.warning("Firebase auth proxy error for %s: %s", path, exc)
        raise HTTPException(status_code=502, detail="Auth proxy unavailable")


@app.get("/pricing")
def pricing_page():
    """Redirect /pricing to the landing page pricing section."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/#pricing", status_code=301)


@app.get("/sitemap.xml")
def sitemap():
    """Serve sitemap for SEO crawlers."""
    from fastapi.responses import Response
    _dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
    f = _dist / "sitemap.xml"
    if f.exists():
        return Response(content=f.read_text(), media_type="application/xml")
    return Response(content="", status_code=404)


@app.get("/robots.txt")
def robots():
    """Serve robots.txt."""
    from fastapi.responses import PlainTextResponse
    _dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
    f = _dist / "robots.txt"
    content = f.read_text() if f.exists() else "User-agent: *\nAllow: /"
    return PlainTextResponse(content)


_frontend_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if _frontend_dist.is_dir():
    app.mount("/", StaticFiles(directory=str(_frontend_dist), html=True), name="frontend")


def main():
    # P1-14: Use settings for host/port instead of hardcoded values
    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
