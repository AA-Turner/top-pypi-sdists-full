# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from typing import TYPE_CHECKING

from contrast_fireball import OtelAttributes, SpanType

from contrast.agent import scope

if TYPE_CHECKING:
    from collections.abc import Callable, Generator, Mapping

    from contrast.agent.context import ContrastContext
    from contrast.agent.policy.handlers import EventDict, EventHandler


def django_authn_span_attrs_builder(
    event_dict: EventDict,
) -> tuple[SpanType, Callable[[Mapping[str, object], object], OtelAttributes], None]:
    mechanism_param_locations = event_dict.get("mechanisms", [])
    if not mechanism_param_locations:
        raise ValueError("Event must specify 'mechanisms' parameter location.")

    def observe_span_attrs(args: Mapping[str, object], result: object):
        credentials = args["credentials"]
        mechanism = next(
            (m for m in mechanism_param_locations if credentials.get(m)), None
        )
        return (
            {"contrast.authentication.mechanism": str(mechanism)} if mechanism else {}
        )

    return SpanType.AuthenticationRequest, observe_span_attrs, None


def django_session_authn_span_attrs_builder(
    event_dict: EventDict,
) -> tuple[SpanType, Callable[[Mapping[str, object], object], OtelAttributes], None]:
    mechanism = str(event_dict.get("mechanism", ""))
    if not mechanism:
        raise ValueError("Event must specify 'mechanism'.")

    def observe_span_attrs(args: Mapping[str, object], result: object):
        return {"contrast.authentication.mechanism": mechanism}

    return SpanType.AuthenticationRequest, observe_span_attrs, None


def starlette_authn_observe_handler_builder(event_dict: EventDict) -> EventHandler:
    """
    `AuthenticationMiddleware.__call__` authenticates the request and then awaits the
    rest of the app, so a span around the call would cover the whole request and
    suppress every span nested in it (e.g. authorization). Instead, record the span
    before the call, to signal that authentication was attempted.
    """

    def observe_handler(
        context: ContrastContext | None, args: Mapping[str, object]
    ) -> Generator:
        if (
            context is not None
            and not scope.in_observe_scope()
            and (trace := context.observability_trace) is not None
        ):
            with trace.child_span(SpanType.AuthenticationRequest) as child_span:
                if child_span is not None:
                    # Starlette authentication requires the app developer to implement
                    # their own AuthenticationBackend, so we have no way of knowing the
                    # mechanism used.
                    child_span.update({})
        yield

    return observe_handler
