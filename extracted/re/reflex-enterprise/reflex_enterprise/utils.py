"""Utility functions for Reflex Enterprise."""

import asyncio
import dataclasses
import inspect
from collections.abc import Sequence
from typing import Any, Callable, TypedDict

import psutil
import reflex as rx
from packaging import version
from reflex import ImportVar, constants
from reflex.config import get_config
from reflex.event import Event, IndividualEventType, fix_events
from reflex.state import BaseState, StateUpdate
from reflex.utils import console, prerequisites
from reflex.utils.decorator import once
from reflex.utils.prerequisites import get_app
from reflex.vars.base import Var, VarData
from reflex.vars.function import ArgsFunctionOperation, FunctionStringVar

from reflex_enterprise.constants import IS_OFFLINE

from .vars import ArgsFunctionOperationPromise, PromiseVar


def get_user_tier() -> str:
    """Get the current user's subscription tier.

    Returns:
        The user's subscription tier as a string.
    """
    if IS_OFFLINE:
        return "enterprise"
    return prerequisites.get_user_tier() or "anonymous"


def check_config_option_in_tier(
    option_name: str,
    allowed_tiers: list[str],
    fallback_value: Any,
    help_link: str | None = None,
):
    """Check if a config option is allowed for the authenticated user's current tier.

    Args:
        option_name: The name of the option to check.
        allowed_tiers: The tiers that are allowed to use the option.
        fallback_value: The fallback value if the option is not allowed.
        help_link: The help link to show to a user that is authenticated.
    """
    config = get_config()
    current_tier = get_user_tier()

    if allowed_tiers == []:
        the_remedy = "This option is not available in the current context."
    else:
        if current_tier == "anonymous":
            the_remedy = "You are currently logged out. Run `reflex login` to access this option."
        else:
            the_remedy = (
                f"Your current subscription tier is `{current_tier}`. "
                f"Please upgrade to {allowed_tiers} to access this option. "
            )
            if help_link:
                the_remedy += f"See {help_link} for more information."

    value = getattr(config, option_name)

    if value is None:
        setattr(config, option_name, fallback_value)
        return

    if value != fallback_value and current_tier not in allowed_tiers:
        console.warn(f"Config option `{option_name}` is restricted. {the_remedy}")
        setattr(config, option_name, fallback_value)
        config._set_persistent(**{option_name: fallback_value})


def is_deploy_context():
    """Check if the current context is a deploy context.

    Returns:
        True if the current context is a deploy context, False otherwise.
    """
    from reflex.utils.exec import get_compile_context

    return get_compile_context() == constants.CompileContext.DEPLOY  # pyright: ignore [reportPrivateImportUsage]


def get_backend_url(relative_url: str | Var[str]) -> Var[str]:
    """Get the full backend URL for a given relative URL.

    Use with `fetch` to access backend API endpoints.

    Args:
        relative_url: The relative URL to convert.

    Returns:
        A Var representing the full backend URL.
    """
    # Remove when reflex-enterprise drops support for < 0.8.27
    use_compatible_get_backend_url = version.parse(
        rx.constants.Reflex.VERSION
    ) < version.parse("0.8.27")
    if use_compatible_get_backend_url:
        # This is the older, less ideal implementation
        return ArgsFunctionOperation.create(
            args_names=("url",),
            return_expr=Var(
                r"`${getBackendURL(typeof env !== 'undefined' ? env.UPLOAD : env_default.UPLOAD).origin}/${url.replace(/^\/+/, '')}`"
            ),
            _var_data=VarData(
                imports={
                    "$/utils/state": ["getBackendURL"],
                    "$/env.json": ImportVar(tag="env", is_default=True),
                }
            ),
        )(relative_url).to(str)

    # Reflex 0.8.27+ use the newer getBackendURL that doesn't require an argument.
    backend_url = Var(
        "getBackendURL()",
        _var_data=VarData(imports={"$/utils/state": ["getBackendURL"]}),
    )
    return ArgsFunctionOperation.create(
        args_names=("path", "backendUrl"),
        return_expr=Var(
            "(backendUrl.pathname ="
            ' backendUrl.pathname.slice(0, backendUrl.pathname.lastIndexOf("/") + 1)'
            ' + (path[0] === "/" ? path.slice(1) : path),'
            " backendUrl.href)"
        ),
    )(relative_url, backend_url).to(str)


def fetch(
    url: str | Var[str], options: dict[str, Any] | Var[dict[str, Any]] | None = None
) -> PromiseVar:
    """Fetch a URL with the given options.

    Args:
        url: The URL to fetch.
        options: The options to use for the fetch.

    Returns:
        A PromiseVar representing the eventual result of the fetch.
    """
    return ArgsFunctionOperationPromise.create(
        args_names=("url", "options"),
        return_expr=Var(
            "fetch(url, {...options, headers: {...options.headers, 'X-Reflex-Client-Token': getToken()}})"
        ),
        _var_data=VarData(
            imports={
                "$/utils/state": [
                    "getToken",
                ],
            }
        ),
    )(url, options or {})


def encode_uri_component(value: str | Var[str]) -> Var[str]:
    """Encode a URI component.

    Args:
        value: The value to encode.

    Returns:
        A Var representing the encoded URI component.
    """
    return FunctionStringVar.create("encodeURIComponent")(value).to(str)


def arrow_func(py_fn: Callable) -> ArgsFunctionOperation:
    """Convert a Python function to a js arrow function."""
    sig = inspect.signature(py_fn)
    params = [
        Var(
            param.name,
            _var_type=param.annotation,
        ).guess_type()
        for param in sig.parameters.values()
    ]
    return ArgsFunctionOperation.create(
        args_names=tuple(sig.parameters),
        return_expr=py_fn(*params),
    )


@once
def is_new_session() -> bool:
    """Check if this is a new development session vs hot reload restart.

    Returns:
        True if this is a new session, False if it's a hot reload restart.
    """
    # Get current parent PID (this could fail in unusual environments)
    try:
        current_parent_pid = (
            parent.pid if (parent := psutil.Process().parent()) else None
        )
    except Exception:
        return True  # Default to showing message if process detection fails

    if current_parent_pid is None:
        return True

    # Check stored parent PID from previous session
    backend_dir = prerequisites.get_web_dir() / "backend"
    backend_dir.mkdir(parents=True, exist_ok=True)
    session_file = backend_dir / "session_parent_pid"

    if session_file.exists():
        # Read and parse stored PID (this could fail if file is corrupted)
        try:
            stored_parent_pid = int(session_file.read_text().strip())
            is_new = current_parent_pid != stored_parent_pid
        except Exception:
            # File is corrupted, treat as new session
            is_new = True
    else:
        # First time, treat as new session
        is_new = True

    if is_new:
        session_file.write_text(str(current_parent_pid))

    return is_new


class CallEventPayload(TypedDict):
    """Payload for calling an event from a computed var."""

    handler: rx.EventHandler
    state: BaseState
    payload: Any


def _call_event_payload(state: BaseState, fixed_event: Event) -> CallEventPayload:
    substate, handler = state._get_root_state()._get_event_handler(fixed_event)  # pyright: ignore[reportAttributeAccessIssue]

    if handler.is_background or not isinstance(substate, BaseState):
        msg = "Background events cannot be called from computed vars. Use chain_event_out_of_band instead."
        raise RuntimeError(msg)
    return CallEventPayload(
        handler=handler,
        state=substate,
        payload=fixed_event.payload,
    )


async def call_event_from_computed_var(
    state: BaseState, events: IndividualEventType | list[IndividualEventType]
):
    """Chain an event from an async computed var.

    Args:
        state: The state to call the event on.
        events: The events to call.
    """
    if not isinstance(events, Sequence):
        events = [events]
    token = state.router.session.client_token

    app = get_app().app

    # Clean the current dirty vars, since the original ones are saved in the `get_delta` frame.
    state._clean()

    # reflex > 0.9.0 method:
    if (event_processor := getattr(app, "event_processor", None)) is not None:
        for event_future in asyncio.as_completed(
            [
                event_processor.enqueue(token, event)
                for event in Event.from_event_type(events)
            ]
        ):
            await event_future
        return

    # Fallback method.
    event_payloads = [
        _call_event_payload(state, fixed_event)
        for fixed_event in fix_events(
            events=events,  # pyright: ignore[reportArgumentType]
            token=token,
            router_data=state.router_data,
        )
    ]

    for ep in event_payloads:
        async for update in state._process_event(**ep):  # pyright: ignore[reportAttributeAccessIssue]
            # In-bound updates are not final! The delta that triggered the computed
            # var may be final and we don't want to override that.
            update = dataclasses.replace(update, final=None)

            # Send the update to the client.
            await app.event_namespace.emit_update(update=update, token=token)


async def chain_event_out_of_band(
    state: BaseState, events: IndividualEventType | list[IndividualEventType]
):
    """Chain an event out-of-band from the main event loop.

    This allows an event handler to deterministically chain another event
    regardless of whether it is returned/yielded. It is primarily useful for
    allowing helper functions which return data to also trigger events as side
    effects.

    Args:
        state: The state associated with the client to call the event on.
        events: The event to chain.
    """
    if not isinstance(events, Sequence):
        events = [events]
    token = state.router.session.client_token
    try:
        fixed_events = Event.from_event_type(events)
    except AttributeError:
        fixed_events = fix_events(
            events=events,  # pyright: ignore[reportArgumentType]
            token=token,
            router_data=state.router_data,
        )
    app = get_app().app
    # Send the update to the client.
    await app.event_namespace.emit_update(
        update=StateUpdate(
            events=fixed_events,
            final=None,
        ),
        token=token,
    )


def get_hook_deps(hook: str) -> list[str]:
    """Extract var deps from a hook.

    Args:
        hook: The hook line to extract deps from.

    Returns:
        A list of var names created by the hook declaration.
    """
    # Ensure that the hook is a var declaration.
    var_decl = hook.partition("=")[0].strip()
    if not any(var_decl.startswith(kw) for kw in ["const ", "let ", "var "]):
        return []

    # Extract the var name from the declaration.
    _, _, var_name = var_decl.partition(" ")
    var_name = var_name.strip()

    # Break up array and object destructuring if used.
    if var_name.startswith(("[", "{")):
        return [v.strip().replace("...", "") for v in var_name.strip("[]{}").split(",")]
    return [var_name]
