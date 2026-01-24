# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from collections.abc import Mapping
from typing import Callable

from contrast_fireball import OtelAttributes, SpanType

from contrast.agent.policy.handlers import EventDict


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


def starlette_authn_span_attrs_builder(
    event_dict: EventDict,
) -> tuple[SpanType, Callable[[Mapping[str, object], object], OtelAttributes], None]:
    def observe_span_attrs(args: Mapping[str, object], result: object):
        # Starlette authentication requires the app developer to implement their own
        # AuthenticationBackend, so we have no way of knowing the mechanism used.
        # Still, this will signal that authentication was attempted.
        return {}

    return SpanType.AuthenticationRequest, observe_span_attrs, None
