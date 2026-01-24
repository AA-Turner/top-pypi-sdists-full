# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Core architecture for policy v2.

"Policy" is in-agent data that describes how we want to instrument particular functions.
Policy has undergone several iterations over the years, but "v2" is a major refactor
that is a more fundamental change to the way we define and apply policy-based
instrumentation.

A single patch is applied to each function instrumented with policy v2, regardless of
which agent modes are currently enabled. At call-time, this patch retrieves and calls a
series of handler functions specific to the called function. Handler functions are
generated from policy definitions, and can be regenerated after startup to modify the
agent's behavior - for example, if a mode becomes enabled/disabled, handlers can be
easily added/removed.
"""

from __future__ import annotations

import contextlib
import inspect
from dataclasses import dataclass
from functools import partial
from typing import Callable

import contrast
from contrast.agent import scope
from contrast.agent.policy.handlers import (
    EventDict,
    EventHandler,
    EventHandlerBuilder,
    authn,
    authz,
    cmd_exec,
    file_open,
    graphql_request,
    observe_handler_builder,
    outbound_request,
)
from contrast.agent.request_context import RequestContext
from contrast.policy_v2 import PolicyDefinition
from contrast.utils.decorators import log_and_report_exception
from contrast.utils.patch_utils import add_watermark
from contrast_vendor import wrapt

NO_RESULT: object = object()
"""
Sentinel used by event handlers. Indicates that the original function did not return a
value (most likely, it raised an exception instead).
"""


EVENT_HANDLER_BUILDERS: dict[str, dict[str, EventHandlerBuilder]] = {
    "cmd-exec": {
        "observe": partial(
            observe_handler_builder, cmd_exec.observe_span_attrs_builder
        ),
    },
    "file-open": {
        "observe": partial(
            observe_handler_builder, file_open.observe_span_attrs_builder
        ),
    },
    "django-authn": {
        "observe": partial(
            observe_handler_builder, authn.django_authn_span_attrs_builder
        ),
    },
    "django-session-authn": {
        "observe": partial(
            observe_handler_builder, authn.django_session_authn_span_attrs_builder
        ),
    },
    "starlette-authn": {
        "observe": partial(
            observe_handler_builder, authn.starlette_authn_span_attrs_builder
        ),
    },
    "authz": {
        "observe": partial(observe_handler_builder, authz.authz_span_attrs_builder),
    },
    "outbound-request": {
        "observe": partial(
            observe_handler_builder, outbound_request.observe_span_attrs_builder
        )
    },
    "outbound-request-http.client": {
        "observe": partial(
            observe_handler_builder, outbound_request.http_client_attrs_builder
        )
    },
    "graphql-request": {},  # populated conditionally below
}
"""
event name -> {mode -> builder fn}

Central storage for v2 policy builder functions
"""

with contextlib.suppress(ImportError):
    import graphql  # noqa: F401

    # Ensure that graphql-related policy is registered if the graphql package is
    # available.
    EVENT_HANDLER_BUILDERS["graphql-request"] = {
        # Unlike other observe handlers, we don't make a child span for graphql.
        # Attributes are added directly to the root span.
        "observe": graphql_request.observe_handler_builder,
        "protect": graphql_request.protect_handler_builder,
    }

_policy_v2: dict[str, EventDict] = {}
"""
full function name -> event dict

Central storage for v2 policy definitions at runtime.
"""


@dataclass(frozen=True)
class Location:
    """
    Represents a location of a function in the format 'module.method_name' or
    'module.class_name.method_name'. This is used to uniquely identify a function.
    """

    module: str
    method_name: str
    class_name: str | None = None

    @classmethod
    def from_string(cls, name: str) -> Location:
        parts = name.rsplit(".", maxsplit=2)
        if len(parts) == 2:
            return cls(module=parts[0], method_name=parts[1])
        elif len(parts) == 3:
            # This is a loose check for classname. It assumes we aren't dealing with
            # modules that have names starting with uppercase letters. Our existing policy
            # doesn't have such modules, but we should be careful if we accept policy from
            # users.
            if parts[1][0].isupper():
                return cls(
                    module=parts[0],
                    class_name=parts[1],
                    method_name=parts[2],
                )
            else:
                return cls(
                    module=".".join(parts[:2]), class_name=None, method_name=parts[2]
                )
        else:
            raise ValueError(
                f"Invalid location name '{name}'. Must be in the format 'module.method_name' or 'module.class_name.method_name'."
            )


def register_policy_definitions(definitions: list[PolicyDefinition]) -> None:
    """
    Add the given policy definition to centralized storage for all v2 policy definitions
    """
    new_keys = [
        f"{d['module']}.{method_name}"
        for d in definitions
        for method_name in d["method_names"]
    ]
    internal_duplicates = {k for k in new_keys if new_keys.count(k) > 1}
    if internal_duplicates:
        raise RuntimeError(f"Duplicate policy definitions: {internal_duplicates}")

    new_definitions = {
        f"{d['module']}.{method_name}": d["event"]
        for d in definitions
        for method_name in d["method_names"]
    }
    duplicates = set(_policy_v2.keys()).intersection(new_definitions.keys())
    if duplicates:
        raise RuntimeError(f"Duplicate policy definitions: {duplicates}")

    _policy_v2.update(new_definitions)


def get_policy_locations() -> set[Location]:
    return {Location.from_string(location) for location in _policy_v2}


def generate_policy_event_handlers(
    *,
    assess: bool,
    observe: bool,
    protect: bool,
) -> dict[str, list[EventHandler]]:
    """
    Iterate over all registered policy definitions and (re)generate event handlers.
    """
    # NOTE: we may want to cache builder invocations in the future if performance is bad
    event_handlers = {}
    for location_name, event_dict in _policy_v2.items():
        handler_builders = EVENT_HANDLER_BUILDERS[event_dict["name"]]
        handlers = []
        if observe and (build_observe_handler := handler_builders.get("observe")):
            handlers.append(build_observe_handler(event_dict))
        if assess and (build_assess_handler := handler_builders.get("assess")):
            handlers.append(build_assess_handler(event_dict))
        if protect and (build_protect_handler := handler_builders.get("protect")):
            handlers.append(build_protect_handler(event_dict))
        event_handlers[location_name] = handlers

    return event_handlers


def get_event_handlers(
    location_name: str,
) -> tuple[list[EventHandler], RequestContext | None]:
    """
    Gets all current event handlers for a function. Performs the lookup on the event
    handlers stored on the current request context if one is available, otherwise uses
    agent state.

    To avoid duplicate context lookups in the future, also returns the request context.
    """
    if (context := contrast.REQUEST_CONTEXT.get()) is None:
        from contrast.agent import agent_state

        return agent_state.module.event_handlers.get(location_name, []), None
    return context.event_handlers.get(location_name, []), context


def build_generic_contrast_wrapper(original_func, module_name: str | None = None):
    module_name = module_name or original_func.__module__
    location_name = f"{module_name}.{original_func.__qualname__}"
    assert "contrast" not in location_name, (
        f"Attempting to patch Contrast code: {location_name}"
    )
    bind_args = event_arguments_binder(original_func)

    @wrapt.function_wrapper
    @add_watermark
    def generic_contrast_wrapper(wrapped, instance, args, kwargs):
        """
        Generic wrapper for any function instrumented with v2 policy. This is the top-
        level wrapper that is the single entrypoint for all contrast instrumenation.

        The wrapper looks up relevant event handlers and calls them in order before
        calling the original function. Event handlers are then called again in reverse
        order after the original function call.
        """
        if scope.in_contrast_scope():
            return wrapped(*args, **kwargs)

        with scope.contrast_scope():
            # In the future we need to consider error handling more carefully here.
            # Exceptions raised by our machinery should not affect the original function
            # call. Beware that `@fail_quietly` may not work as expected with generator
            # functions.
            result = NO_RESULT
            bound_args = bind_args(instance, args, kwargs)

            post = []
            event_handlers, context = get_event_handlers(location_name)
            for handler in event_handlers:
                try:
                    gen = handler(context, bound_args.arguments)
                    next(gen)
                except StopIteration:  # noqa: PERF203
                    assert False, "Invalid event handler - did not yield"  # noqa: B011 PT015
                except contrast.SecurityException:
                    raise
                except Exception as e:
                    # If an exception is raised in the event handler, we report it and
                    # continue with the next handler.
                    log_and_report_exception(
                        log_message="Exception in pre event handler",
                        error=e,
                        original_func=original_func,
                        args=args,
                        kwargs=kwargs,
                        log_level="error",
                    )
                else:
                    post.append(gen)

            try:
                with scope.pop_contrast_scope():
                    result = wrapped(*args, **kwargs)
            finally:
                for gen in reversed(post):
                    try:
                        gen.send(result)
                    except StopIteration:  # noqa: PERF203
                        pass
                    except Exception as e:
                        # If an exception is raised in the event handler, we report it and
                        # continue with the next handler.
                        log_and_report_exception(
                            log_message="Exception in post event handler",
                            error=e,
                            original_func=original_func,
                            args=args,
                            kwargs=kwargs,
                            log_level="error",
                        )
                    else:
                        assert False, "Invalid event handler - more than one yield"  # noqa: B011 PT015

            assert result is not NO_RESULT
            return result

    return generic_contrast_wrapper(original_func)


def event_arguments_binder(func: Callable):
    """
    Returns a function that binds the arguments for func.

    This is used to bind the arguments for the event handlers, so that arguments
    can be retrieved by their names regardless of their order or how they are passed
    in the function call.
    """
    sig = inspect.signature(func)
    if inspect.ismethod(func):
        sig = inspect.signature(func.__func__)

    def _bind(instance, args, kwargs) -> inspect.BoundArguments:
        bound_args = (
            sig.bind(instance, *args, **kwargs)
            if instance is not None
            else sig.bind(*args, **kwargs)
        )
        bound_args.apply_defaults()
        return bound_args

    return _bind
