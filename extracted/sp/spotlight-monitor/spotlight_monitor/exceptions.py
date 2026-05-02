"""
Spotlight Exception Tracking

Sentry-style exception capture with:
- Full stack traces with local variables
- Error fingerprinting/grouping
- Request context
- Breadcrumbs
- Environment tagging
"""

import hashlib
import linecache
import os
import sys
import threading
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
from contextvars import ContextVar

# Context var for breadcrumbs (thread-safe)
_breadcrumbs: ContextVar[List[Dict]] = ContextVar("breadcrumbs", default=[])
_request_context: ContextVar[Dict] = ContextVar("request_context", default={})


@dataclass
class Frame:
    """Single stack frame"""
    filename: str
    function: str
    lineno: int
    code_context: List[str] = field(default_factory=list)
    local_vars: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "filename": self.filename,
            "function": self.function,
            "lineno": self.lineno,
            "code_context": self.code_context,
            "local_vars": self.local_vars,
        }


@dataclass
class ExceptionInfo:
    """Full exception information"""
    exception_type: str
    message: str
    fingerprint: str
    frames: List[Frame]
    timestamp: datetime
    breadcrumbs: List[Dict]
    request_context: Dict
    environment: str
    release: Optional[str]
    tags: Dict[str, str]
    extra: Dict[str, Any]

    def to_dict(self) -> Dict:
        return {
            "exception_type": self.exception_type,
            "message": self.message,
            "fingerprint": self.fingerprint,
            "frames": [f.to_dict() for f in self.frames],
            "timestamp": self.timestamp.isoformat(),
            "breadcrumbs": self.breadcrumbs,
            "request_context": self.request_context,
            "environment": self.environment,
            "release": self.release,
            "tags": self.tags,
            "extra": self.extra,
        }


def _safe_repr(obj: Any, max_len: int = 200) -> str:
    """Safely convert object to string representation"""
    try:
        r = repr(obj)
        if len(r) > max_len:
            return r[:max_len] + "..."
        return r
    except Exception:
        return "<unrepresentable>"


def _extract_local_vars(frame) -> Dict[str, str]:
    """Extract local variables from frame, filtering sensitive data"""
    sensitive_keys = {
        "password", "secret", "token", "api_key", "apikey",
        "auth", "credential", "private", "key"
    }

    local_vars = {}
    try:
        for key, value in frame.f_locals.items():
            # Skip internal/private vars
            if key.startswith("_"):
                continue
            # Mask sensitive values
            key_lower = key.lower()
            if any(s in key_lower for s in sensitive_keys):
                local_vars[key] = "<sensitive>"
            else:
                local_vars[key] = _safe_repr(value)
    except Exception:
        pass

    return local_vars


def _get_code_context(filename: str, lineno: int, context_lines: int = 5) -> List[str]:
    """Get source code context around the error line"""
    lines = []
    try:
        start = max(1, lineno - context_lines)
        end = lineno + context_lines + 1
        for i in range(start, end):
            line = linecache.getline(filename, i)
            if line:
                prefix = ">>> " if i == lineno else "    "
                lines.append(f"{prefix}{i}: {line.rstrip()}")
    except Exception:
        pass
    return lines


def _generate_fingerprint(exception_type: str, frames: List[Frame]) -> str:
    """
    Generate a fingerprint for error grouping.
    Same error in same location = same fingerprint.
    """
    # Use exception type + top 3 frames for fingerprint
    parts = [exception_type]
    for frame in frames[:3]:
        # Only use app code, not library code
        if "site-packages" not in frame.filename and "lib/python" not in frame.filename:
            parts.append(f"{frame.filename}:{frame.function}:{frame.lineno}")

    fingerprint_str = "|".join(parts)
    return hashlib.sha256(fingerprint_str.encode()).hexdigest()[:16]


def extract_exception_info(
    exc: BaseException,
    environment: str = "production",
    release: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> ExceptionInfo:
    """
    Extract full exception information from an exception.
    """
    exc_type = type(exc).__name__
    exc_message = str(exc)

    # Extract stack frames
    frames = []
    tb = exc.__traceback__
    while tb is not None:
        frame = tb.tb_frame
        lineno = tb.tb_lineno
        filename = frame.f_code.co_filename
        function = frame.f_code.co_name

        frames.append(Frame(
            filename=filename,
            function=function,
            lineno=lineno,
            code_context=_get_code_context(filename, lineno),
            local_vars=_extract_local_vars(frame),
        ))
        tb = tb.tb_next

    # Reverse so most recent is first
    frames.reverse()

    # Get breadcrumbs and request context from context vars
    breadcrumbs = _breadcrumbs.get([])
    request_context = _request_context.get({})

    fingerprint = _generate_fingerprint(exc_type, frames)

    return ExceptionInfo(
        exception_type=exc_type,
        message=exc_message,
        fingerprint=fingerprint,
        frames=frames,
        timestamp=datetime.utcnow(),
        breadcrumbs=list(breadcrumbs),  # Copy to avoid mutation
        request_context=dict(request_context),
        environment=environment,
        release=release,
        tags=tags or {},
        extra=extra or {},
    )


class Breadcrumb:
    """Utility for adding breadcrumbs (events leading up to error)"""

    @staticmethod
    def add(
        message: str,
        category: str = "default",
        level: str = "info",
        data: Optional[Dict] = None,
    ):
        """Add a breadcrumb to the current context"""
        crumbs = _breadcrumbs.get([])
        crumbs.append({
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "category": category,
            "level": level,
            "data": data or {},
        })
        # Keep last 100 breadcrumbs
        if len(crumbs) > 100:
            crumbs = crumbs[-100:]
        _breadcrumbs.set(crumbs)

    @staticmethod
    def clear():
        """Clear breadcrumbs for current context"""
        _breadcrumbs.set([])


class RequestContext:
    """Utility for setting request context"""

    @staticmethod
    def set(
        method: Optional[str] = None,
        url: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[str] = None,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        **kwargs,
    ):
        """Set request context for current request"""
        # Filter sensitive headers
        safe_headers = {}
        if headers:
            sensitive = {"authorization", "cookie", "x-api-key"}
            for k, v in headers.items():
                if k.lower() in sensitive:
                    safe_headers[k] = "<redacted>"
                else:
                    safe_headers[k] = v

        context = {
            "method": method,
            "url": url,
            "headers": safe_headers,
            "body": body[:1000] if body and len(body) > 1000 else body,
            "user_id": user_id,
            "ip_address": ip_address,
            **kwargs,
        }
        # Remove None values
        context = {k: v for k, v in context.items() if v is not None}
        _request_context.set(context)

    @staticmethod
    def clear():
        """Clear request context"""
        _request_context.set({})


def capture_exception(
    exc: Optional[BaseException] = None,
    environment: str = "production",
    release: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Optional[ExceptionInfo]:
    """
    Capture an exception. If no exception is passed, captures the current exception.

    Usage:
        try:
            risky_operation()
        except Exception as e:
            capture_exception(e)
            raise

    Or in an except block:
        except Exception:
            capture_exception()  # Captures current exception
            raise
    """
    if exc is None:
        exc = sys.exc_info()[1]

    if exc is None:
        return None

    return extract_exception_info(
        exc,
        environment=environment,
        release=release,
        tags=tags,
        extra=extra,
    )
