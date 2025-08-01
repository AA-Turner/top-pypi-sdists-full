# Copyright © 2025 Contrast Security, Inc.
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

import inspect
from typing import Callable, TypedDict
from collections.abc import Mapping
from collections.abc import Generator


import contrast
from contrast.agent import agent_state, scope
from contrast.agent.request_context import RequestContext
from contrast.utils.patch_utils import add_watermark
from contrast_vendor import wrapt

# Unfortunately, TypedDicts do not currently support arbitrary extra keys in addition to
# required keys, so we cannot use one here.
EventDict = dict
"""
Part of a v2 policy definition that contains any metadata required to build event
handler functions. At minimum, has an event `name` key.
"""


class PolicyDefinition(TypedDict):
    """
    v2 policy definition for a group of functions that share an event type. Used for
    literal contrast-defined policy.

    Try to keep this easily JSON-serializable in case we want to support receiving
    policy definitions from external sources in the future.
    """

    module: str
    method_names: list[str]
    event: EventDict


EventHandler = Callable[..., Generator]
"""
A v2 policy event handler. The resulting generator must yield exactly once, and a
`result` of the original function call will be sent to the generator via this yield.
For example:

```python
def my_event_handler(instance, args, kwargs) -> Generator:
    # do pre-call work here
    result = yield
    # post-call work here
```
"""

EventHandlerBuilder = Callable[[EventDict], EventHandler]
"""
Builder function for a v2 policy event handler.
"""

NO_RESULT: object = object()
"""
Sentinel used by event handlers. Indicates that the original function did not return a
value (most likely, it raised an exception instead).
"""


# builders are all currently prototypes and eventually need to be fully implemented


def assess_cmd_exec_pre(context: RequestContext, args: Mapping[str, object]) -> None:
    pass


def assess_cmd_exec_post(
    context: RequestContext, args: Mapping[str, object], result
) -> None:
    pass


def assess_cmd_exec_builder(event_dict: EventDict) -> EventHandler:
    def assess_cmd_exec_handler(
        context: RequestContext, args: Mapping[str, object]
    ) -> Generator:
        assess_cmd_exec_pre(context, args)
        result = yield
        assess_cmd_exec_post(context, args, result)

    return assess_cmd_exec_handler


def observe_handler_builder(event_dict: EventDict) -> EventHandler:
    """
    Builder function for the observe handler. The event dict must contain an `action` key
    specifying the action span name that envelopes the patched function call. The event
    dict may also contain `static_attributes` and `dynamic_attributes` keys, which are
    dictionaries of attributes to set on the action span. Static attributes are set
    directly, while dynamic attributes are set after the function call. Dynamic
    attributes map attribute names to argument names, so that the value of the argument
    is added as the value of the attribute.
    """
    reporter = agent_state.module.reporting_client
    assert reporter is not None

    action_name = event_dict["action"]
    static_attributes = event_dict.get("static_attributes", {})
    dynamic_attributes = event_dict.get("dynamic_attributes", {})

    if mixed_attributes := set(static_attributes).intersection(dynamic_attributes):
        raise ValueError(
            f"Overlapping static and dynamic attributes provided: {mixed_attributes}"
        )

    def observe_handler(
        context: RequestContext, args: Mapping[str, object]
    ) -> Generator:
        if (trace := context.observability_trace) is None:
            yield
            return
        with trace.child_span(action_name) as child_span:
            if child_span is None:
                yield
                return
            result = yield
            dyn_attrs = {
                key: result if arg_name == "return" else args[arg_name]
                for key, arg_name in dynamic_attributes.items()
            }
            child_span.update(static_attributes | dyn_attrs)

    return observe_handler


def protect_handler_builder(event_dict: EventDict) -> EventHandler:
    def protect_handler(
        context: RequestContext, args: Mapping[str, object]
    ) -> Generator:
        _ = yield

    return protect_handler


EVENT_HANDLER_BUILDERS: dict[str, dict[str, EventHandlerBuilder]] = {
    "cmd-exec": {
        "assess": assess_cmd_exec_builder,
        "observe": observe_handler_builder,
        "protect": protect_handler_builder,
    }
}
"""
event name -> {mode -> builder fn}

Central storage for v2 policy builder functions
"""

_policy_v2: dict[str, EventDict] = {}
"""
full function name -> event dict

Central storage for v2 policy definitions at runtime.
"""


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
        event_builders = EVENT_HANDLER_BUILDERS[event_dict["name"]]
        handlers = []
        if assess:
            handlers.append(event_builders["assess"](event_dict))
        if observe:
            handlers.append(event_builders["observe"](event_dict))
        if protect:
            handlers.append(event_builders["protect"](event_dict))
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
    if (context := contrast.CS__CONTEXT_TRACKER.current()) is None:
        return agent_state.module.event_handlers.get(location_name, []), None
    return context.event_handlers.get(location_name, []), context


def build_generic_contrast_wrapper(original_func):
    location_name = f"{original_func.__module__}.{original_func.__qualname__}"
    bind_args = event_arguments_binder(original_func)

    @wrapt.function_wrapper
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
                gen = handler(context, bound_args.arguments)
                try:
                    next(gen)
                except StopIteration:
                    assert False, "Invalid event handler - did not yield"  # noqa: B011 PT015
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
                    else:
                        assert False, "Invalid event handler - more than one yield"  # noqa: B011 PT015

            assert result is not NO_RESULT
            return result

    return add_watermark(generic_contrast_wrapper(original_func))


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
