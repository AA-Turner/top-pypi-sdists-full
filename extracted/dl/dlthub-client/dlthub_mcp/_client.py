"""The workspace the tools read, resolved once from the run environment."""

from __future__ import annotations

# Python internals
import importlib
import os
import threading
from contextlib import suppress
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar, cast

if TYPE_CHECKING:
    # Current package
    from dlthub_sdk import Runtime, Sync, Workspace

F = TypeVar("F", bound=Callable[..., Any])

_lock = threading.Lock()
_runtime: Optional["Runtime[Sync]"] = None
_workspace: Optional["Workspace[Sync]"] = None
#: Whether the held credential is the login the CLI stores, which it can renew.
#: An API key and a runner-injected token cannot be renewed from here.
_stored_login = False
#: Whether that credential was refused, so the next connect re-reads the config
#: rather than trusting what this process resolved before the refusal.
_refused = False


def tool_error(message: str) -> Exception:
    """Build the error type the MCP host masks nothing of.

    fastmcp belongs to whoever runs the server, so it is looked up rather than
    imported.

    Args:
        message: What the agent should be told.

    Returns:
        A ``ToolError``, or a plain ``RuntimeError`` when fastmcp is absent.
    """
    try:
        module = importlib.import_module("fastmcp.exceptions")
    except ImportError:
        return RuntimeError(message)
    return cast(Exception, module.ToolError(message))


def setting(attr: str, env: str) -> Optional[str]:
    """Read one platform setting, preferring dlt's resolved runtime config.

    Args:
        attr: Field on the workspace runtime config.
        env: Environment variable holding the same value.

    Returns:
        The value, or ``None`` when neither source has it.
    """
    # Other libraries
    from dlt.common.runtime.run_context import active

    value = getattr(active().runtime_config, attr, None)
    return str(value) if value else os.environ.get(env)


def reread_config() -> None:
    """Re-resolve dlt's config, so a login refreshed on disk becomes visible.

    A run context resolves its config once and holds it for the whole process,
    so a JWT some other CLI command wrote stays unseen until this is called.
    """
    # Other libraries
    from dlt.common.configuration.container import Container
    from dlt.common.configuration.specs.pluggable_run_context import PluggableRunContext

    # Best effort: a failure here costs a stale read, and the caller is already
    # reporting something else.
    with suppress(Exception):
        Container()[PluggableRunContext].reload_providers()


def workspace() -> "Workspace[Sync]":
    """Return the workspace this process serves, connecting on first use.

    Credentials come from what the runner injects into a job —
    ``RUNTIME__API_KEY`` (or ``RUNTIME__AUTH_TOKEN``), ``RUNTIME__WORKSPACE_ID``
    and ``RUNTIME__API_BASE_URL`` — or, on a developer machine, from the
    connected workspace's own config, which dlt resolves under the same names.
    An ambient key outranks a token, so a developer machine reaches the
    workspace its key is scoped to.

    Returns:
        The workspace, cached for the process along with its connections.

    Raises:
        Exception: A ``ToolError`` naming whichever of the credential and the
            workspace is missing.
    """
    global _runtime, _workspace, _stored_login, _refused
    with _lock:
        if _workspace is None:
            if _refused:
                # A CLI command may have refreshed the login on disk since the
                # refusal, and a run context resolves its config only once.
                reread_config()
                _refused = False
            # Current package
            import dlthub_sdk

            key = setting("api_key", "RUNTIME__API_KEY")
            token = key or setting("auth_token", "RUNTIME__AUTH_TOKEN")
            workspace_id = setting("workspace_id", "RUNTIME__WORKSPACE_ID")
            if not token or not workspace_id:
                # Named separately: "no credential" and "no workspace" have
                # different fixes, and reporting both reads as "not logged in".
                missing = (
                    "no platform credential (RUNTIME__API_KEY or RUNTIME__AUTH_TOKEN)"
                    if not token
                    else "no workspace (RUNTIME__WORKSPACE_ID)"
                )
                raise tool_error(
                    f"This environment has {missing}. A platform run carries "
                    "both; on a developer machine, connect a workspace with "
                    "`dlthub workspace connect`."
                )
            # Omitted rather than defaulted here: `connect` owns the default.
            base_url = setting("api_base_url", "RUNTIME__API_BASE_URL")
            runtime = (
                dlthub_sdk.connect(token=token, base_url=base_url)
                if base_url
                else dlthub_sdk.connect(token=token)
            )
            # Read off the environment, not off which source dlt's config drew
            # from: its provider chain feeds the environment in as well.
            _stored_login = not key and not os.environ.get("RUNTIME__AUTH_TOKEN")
            _runtime = runtime
            _workspace = runtime.workspaces.get(id=workspace_id)
        return _workspace


def runtime() -> "Runtime[Sync]":
    """Return the connection the workspace was reached through.

    Returns:
        The runtime, for the few reads that are not workspace scoped.
    """
    workspace()
    assert _runtime is not None
    return _runtime


def reset(refused: bool = False) -> None:
    """Drop the cached workspace so the next call re-reads the environment.

    Args:
        refused: Whether the credential was refused, in which case the next
            connect also re-reads dlt's config, where a refreshed login lands.
    """
    global _runtime, _workspace, _stored_login, _refused
    with _lock:
        _runtime = None
        _workspace = None
        _stored_login = False
        _refused = refused


def rejected(detail: str) -> str:
    """Drop the refused credential and name what would replace it.

    Args:
        detail: What the platform said about the credential.

    Returns:
        The detail, followed by the fix for the credential this process holds.
    """
    stored = _stored_login
    # The re-read is deferred to the next connect: the login is refreshed after
    # this message is read, not before.
    reset(refused=stored)
    if not stored:
        return (
            f"{detail} This environment's credential (RUNTIME__API_KEY or "
            "RUNTIME__AUTH_TOKEN) was refused and nothing here can renew it."
        )
    return (
        f"{detail} This is the login stored on this machine. Running any "
        "dlthub CLI command refreshes it — `dlthub workspace list` will do, "
        "and it says to run `dlthub login` if the refresh token is gone too. "
        "Retrying this tool afterwards picks the new login up, so the MCP "
        "server does not need reconnecting."
    )


def tool(fn: F) -> F:
    """Translate SDK errors into what the agent can act on.

    An MCP host masks the detail of anything that is not a ``ToolError``, so an
    untranslated error tells the agent nothing.

    Args:
        fn: The tool function.

    Returns:
        The same function, with platform errors translated.
    """
    # Current package
    from dlthub_sdk.errors import DlthubError, NotAuthenticated

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return fn(*args, **kwargs)
        except NotAuthenticated as e:
            raise tool_error(rejected(str(e))) from e
        except (DlthubError, ValueError) as e:
            raise tool_error(str(e)) from e

    return cast(F, wrapper)


__all__ = [
    "rejected",
    "reread_config",
    "reset",
    "runtime",
    "setting",
    "tool",
    "tool_error",
    "workspace",
]
