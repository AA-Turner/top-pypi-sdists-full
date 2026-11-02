"""Jira SDK client factory — lazy wrapper around atlassian-python-api."""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import TYPE_CHECKING, Any

from agentic_devtools.cli.jira.config import get_jira_auth_header, get_jira_base_url
from agentic_devtools.cli.jira.helpers import _get_ssl_verify

if TYPE_CHECKING:
    from agentic_devtools.tools.jira import JiraConfig

__all__ = ["build_jira_client", "is_cloud"]

_SDK_TIMEOUT_SECONDS = 30


def build_jira_client(config: JiraConfig | None = None):  # type: ignore[return]
    """Build a configured atlassian.Jira client from repo helpers.

    The ``atlassian-python-api`` package is imported lazily so that importing
    this module does not require it to be installed.

    Args:
        config: Optional :class:`JiraConfig` instance. When provided, the
            client uses ``config.base_url``, ``config.ssl_verify``, and
            ``config.headers['Authorization']`` directly, bypassing repo
            helper resolution. Only the ``Authorization`` header from
            ``config.headers`` is applied; other headers are not forwarded.
            When *None* (the default), URL, SSL, and auth are resolved from
            environment/state via the existing helper functions.

    Raises:
        ImportError: If ``atlassian-python-api`` is not installed.
        ValueError: If the Jira base URL is not configured — raised directly
            when ``config.base_url`` is empty, or propagated from
            ``get_jira_base_url()`` when ``config`` is *None*.
        OSError: If Jira credentials are missing — raised when
            ``config.headers['Authorization']`` is empty/missing, or
            propagated from ``get_jira_auth_header()`` when ``config`` is *None*.
        RuntimeError: If the installed SDK version is incompatible (missing
            ``_session`` or non-MutableMapping headers).
    """
    try:
        from atlassian import Jira
    except ModuleNotFoundError as exc:
        if exc.name != "atlassian":
            raise
        raise ImportError(
            "atlassian-python-api is required for Jira SDK client support. "
            'Install it with: pip install "atlassian-python-api>=4.0,<5"'
        ) from exc

    if config is not None:
        url = config.base_url
        if not url or not url.strip():
            raise ValueError(
                "JiraConfig.base_url must be a non-empty string when using "
                "build_jira_client(config=...). Set the Jira base URL in configuration."
            )
        ssl = config.ssl_verify
        auth_header = config.headers.get("Authorization")
        if not isinstance(auth_header, str) or not auth_header.strip():
            raise OSError(
                "JiraConfig.headers['Authorization'] must be a non-empty "
                "string when using build_jira_client(config=...)."
            )
    else:
        url = get_jira_base_url()
        ssl = _get_ssl_verify()
        auth_header = get_jira_auth_header()  # may raise OSError

    client = Jira(url=url, verify_ssl=ssl)

    # Verify SDK compatibility before header injection
    session = getattr(client, "_session", None)
    if session is None:
        version = _get_atlassian_version()
        raise RuntimeError(f"atlassian-python-api {version} is incompatible: expected client._session to exist")

    headers = getattr(session, "headers", None)
    if not isinstance(headers, MutableMapping):
        version = _get_atlassian_version()
        raise RuntimeError(
            f"atlassian-python-api {version} is incompatible: expected client._session.headers to be a MutableMapping"
        )

    headers["Authorization"] = auth_header

    # Configure timeout for all SDK-backed HTTP requests (NFR-001).
    # Keep session.timeout for introspection; wrap session.request so that
    # requests actually enforces the timeout (requests ignores session.timeout
    # unless the per-call timeout= kwarg is also set).
    session.timeout = _SDK_TIMEOUT_SECONDS
    _original_request = session.request

    def _request_with_timeout(*args: Any, **kwargs: Any) -> Any:
        if kwargs.get("timeout") is None:
            kwargs["timeout"] = _SDK_TIMEOUT_SECONDS
        return _original_request(*args, **kwargs)

    session.request = _request_with_timeout

    return client


def is_cloud(metadata: dict[str, Any]) -> bool:
    """Return True if metadata indicates a Jira Cloud deployment.

    Checks ``metadata.get("deploymentType") == "Cloud"`` (exact,
    case-sensitive match mirroring the Jira REST ``serverInfo`` response).
    """
    return metadata.get("deploymentType") == "Cloud"


def _get_atlassian_version() -> str:
    """Best-effort version detection for error messages."""
    try:
        from importlib.metadata import version

        return version("atlassian-python-api")
    except Exception:
        return "unknown"
