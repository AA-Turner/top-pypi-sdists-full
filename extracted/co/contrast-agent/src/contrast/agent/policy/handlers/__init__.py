# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from collections.abc import Generator, Mapping
from collections.abc import Callable

from contrast_fireball import OtelAttributes, SpanType

from contrast.agent import scope
from contrast.agent.request_context import RequestContext
from contrast.policy_v2 import EventDict
from contrast.reporting import fireball
from contrast_vendor import structlog as logging

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

SpanAttrUpdateBuilder = Callable[
    [EventDict],
    tuple[
        SpanType,
        Callable[[Mapping[str, object], object], OtelAttributes],  # attribute builder
        "None | Callable[[Mapping[str, object]], str | None]",  # skip check function
    ],
]


LogRecordEventBuilder = Callable[
    [EventDict],
    Callable[
        [Mapping[str, object], object],
        "fireball.LogRecordEvent | None",
    ],
]

logger = logging.getLogger("contrast")


def observe_span_handler_builder(
    attr_updater: SpanAttrUpdateBuilder,
    event_dict: EventDict,
) -> EventHandler:
    """
    Builds an event handler that creates an observability child span around a function call.

    If the function is called within an existing observe scope, it will not create a new
    span, but will instead yield immediately.

    The builder needs an attribute updater that declares the type of action span to create,
    and how to generate attributes for that span based on the function arguments and result.
    The attribute updater may also return a skip check function that can be used to
    determine whether to skip the observe handler entirely based on the function arguments.
    """
    from contrast.agent import agent_state

    reporter = agent_state.module.reporting_client
    assert reporter is not None

    action_type, get_action_attributes, skip_check = attr_updater(event_dict)

    def observe_handler(
        context: RequestContext | None, args: Mapping[str, object]
    ) -> Generator:
        if context is None or scope.in_observe_scope():
            yield
            return
        with scope.observe_scope():
            if (trace := context.observability_trace) is None:
                yield
                return
            if skip_check and (reason := skip_check(args)):
                logger.debug(
                    "skipping observe handler",
                    reason=reason,
                    action_type=action_type,
                    args=args,
                )
                yield
                return

            with trace.child_span(action_type) as child_span:
                if child_span is None:
                    yield
                    return
                logger.debug(
                    "entered new child span",
                    child_span=child_span,
                    action_type=action_type,
                )
                result = yield
                action_attrs = get_action_attributes(args, result)
                child_span.update(action_attrs)
                logger.debug(
                    "updated child_span attributes",
                    child_span=child_span,
                    action_attrs=action_attrs,
                )

    return observe_handler


def observe_log_handler_builder(
    event_builder: LogRecordEventBuilder,
    event_dict: EventDict,
) -> EventHandler:
    from contrast.agent import agent_state

    reporter = agent_state.module.reporting_client
    assert reporter is not None

    build_event = event_builder(event_dict)

    def observe_log_handler(
        context: RequestContext | None, args: Mapping[str, object]
    ) -> Generator:
        if scope.in_observe_scope():
            yield
            return
        with scope.observe_scope():
            trace = context.observability_trace if context is not None else None

            result = yield

            if event := build_event(args, result):
                reporter.new_log_record_event(event, trace)

    return observe_log_handler
