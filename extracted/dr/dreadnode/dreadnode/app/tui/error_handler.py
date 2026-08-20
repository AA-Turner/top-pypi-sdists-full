import re
import typing as t
from dataclasses import dataclass

from dreadnode.core.tls import format_tls_error

ERROR_PREFIX_PATTERN = re.compile(
    r"^(?:litellm\.)?(?P<error_type>[A-Za-z_][\w]*)\s*:\s*(?P<message>.+)$"
)
PROXY_UNREACHABLE_MESSAGE = (
    "Cannot reach Dreadnode model proxy. Check your connection or switch to a BYOK model."
)
DN_LOGIN_MESSAGE = "Sign in to use dn/ models — run /login"
DN_KEY_EXPIRED_MESSAGE = "Dreadnode model key expired — re-authenticating..."
INSUFFICIENT_CREDITS_MESSAGE = "Insufficient credits — top up your org or switch to a BYOK model."
MODEL_NOT_FOUND_PATTERN = re.compile(r"model\s+.+\s+not\s+found|model_not_found", re.IGNORECASE)
PROXY_UNREACHABLE_SNIPPETS = (
    "connection error",
    "connecterror",
    "connection timeout",
    "connect timeout",
    "timed out",
    "name or service not known",
    "temporary failure in name resolution",
    "getaddrinfo failed",
    "nodename nor servname",
    "failed to establish a new connection",
    "max retries exceeded",
)


@dataclass(slots=True)
class ErrorClassification:
    error_text: str | None
    error_type: str | None
    is_authentication_error: bool


@dataclass(slots=True)
class ErrorResolution:
    override: str | None = None
    flash_message: str | None = None
    reauthenticate_proxy: bool = False


class ProxyModelView(t.Protocol):
    def current_model(self) -> str: ...

    def platform_model_ids(self) -> list[str]: ...


class WarningSink(t.Protocol):
    def flash_warning(self, message: str) -> None: ...


class ProxyAuthActions(t.Protocol):
    def reauthenticate_proxy(self) -> None: ...


def enrich_error_body(
    body: str,
    error_type: str | None,
    status_code: int | None = None,
) -> str:
    """Append error type or HTTP status to the error body for user context."""
    if status_code is not None:
        return f"{body} (HTTP {status_code})"
    if error_type:
        return f"{body} ({error_type})"
    return body


def classify_error_message(
    error_text: str | None,
    error_type: str | None,
) -> ErrorClassification:
    if not error_text:
        return ErrorClassification(None, error_type, False)
    match = ERROR_PREFIX_PATTERN.match(error_text)
    inferred_type = None
    cleaned = error_text
    if match:
        inferred_type = match.group("error_type")
        cleaned = match.group("message")
    resolved_type = error_type or inferred_type
    return ErrorClassification(
        error_text=cleaned,
        error_type=resolved_type,
        is_authentication_error=resolved_type == "AuthenticationError",
    )


def split_missing_api_key_message(error_text: str) -> tuple[str, str] | None:
    parts = error_text.split(" — ", 1)
    if len(parts) != 2:
        return None
    title = parts[0].strip()
    if title.lower() != "missing api key":
        return None
    return (title, parts[1].strip())


def is_missing_proxy_config_error(error_text: str) -> bool:
    return error_text.strip().lower().startswith("missing proxy configuration")


def is_insufficient_credits_error(error_text: str) -> bool:
    return "insufficient credits" in error_text.lower()


def is_proxy_unreachable_error(error_text: str, error_type: str | None = None) -> bool:
    lowered = error_text.lower()
    if error_type in {"APIConnectionError", "ConnectionError", "ConnectError", "TimeoutError"}:
        return True
    return any(snippet in lowered for snippet in PROXY_UNREACHABLE_SNIPPETS)


def is_key_expired_error(error_text: str, error_type: str | None = None) -> bool:
    lowered = error_text.lower()
    if error_type and error_type != "AuthenticationError":
        return False
    if "401" in error_text or "403" in error_text:
        return True
    return any(token in lowered for token in ("expired", "invalid api key", "key expired"))


def is_model_not_found_error(error_text: str, error_type: str | None = None) -> bool:
    if error_type and error_type not in {"NotFoundError", "ModelNotFoundError"}:
        return False
    return bool(MODEL_NOT_FOUND_PATTERN.search(error_text))


class ErrorHandler:
    """Owns TUI error classification and dn/proxy-specific override policy."""

    def __init__(
        self,
        *,
        model_view: ProxyModelView,
        warnings: WarningSink,
        proxy_auth: ProxyAuthActions,
    ) -> None:
        self._model_view = model_view
        self._warnings = warnings
        self._proxy_auth = proxy_auth

    def resolve_proxy_error(
        self,
        error_text: str | None,
        error_type: str | None,
    ) -> ErrorResolution:
        if not error_text:
            return ErrorResolution()
        if not self._model_view.current_model().startswith("dn/"):
            return ErrorResolution()
        # Credits must win over the missing-proxy-config / login fallback:
        # a zero-balance org's provisioning failure surfaces downstream as
        # missing env vars, and the login prompt is misleading there.
        if is_insufficient_credits_error(error_text):
            return ErrorResolution(override=INSUFFICIENT_CREDITS_MESSAGE)
        if is_missing_proxy_config_error(error_text):
            return ErrorResolution(override=DN_LOGIN_MESSAGE)
        if is_model_not_found_error(error_text, error_type):
            available = sorted(self._model_view.platform_model_ids())
            if available:
                message = "Model not available on proxy. Available models: " + ", ".join(available)
            else:
                message = "Model not available on proxy."
            return ErrorResolution(override=message)
        if tls_message := format_tls_error(error_text, error_type):
            return ErrorResolution(override=tls_message, flash_message=tls_message)
        if is_proxy_unreachable_error(error_text, error_type):
            return ErrorResolution(
                override=PROXY_UNREACHABLE_MESSAGE,
                flash_message=PROXY_UNREACHABLE_MESSAGE,
            )
        if is_key_expired_error(error_text, error_type):
            return ErrorResolution(
                override=DN_KEY_EXPIRED_MESSAGE,
                flash_message=DN_KEY_EXPIRED_MESSAGE,
                reauthenticate_proxy=True,
            )
        return ErrorResolution()

    def apply_resolution(self, resolution: ErrorResolution) -> None:
        if resolution.flash_message:
            self._warnings.flash_warning(resolution.flash_message)
        if resolution.reauthenticate_proxy:
            self._proxy_auth.reauthenticate_proxy()
