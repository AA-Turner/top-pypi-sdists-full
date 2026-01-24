# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from collections.abc import Mapping
from typing import Callable

from contrast_fireball import OtelAttributes, SpanType

from contrast.agent.policy.handlers import EventDict


def authz_span_attrs_builder(
    event_dict: EventDict,
) -> tuple[SpanType, Callable[[Mapping[str, object], object], OtelAttributes], None]:
    if dac_perm_param_location := str(event_dict.get("dac_perm", "")):

        def observe_span_attrs(args: Mapping[str, object], result: object):
            attrs = {"contrast.authorization.mechanism": "dac"}
            if perm := str(args.get(dac_perm_param_location, "")):
                # TODO: PYT-3959 - move to list of permissions
                attrs["contrast.authorization.dac.permission"] = perm.lower()
            return attrs
    elif dac_perms_param_location := str(event_dict.get("dac_perms", "")):

        def observe_span_attrs(args: Mapping[str, object], result: object):
            attrs = {"contrast.authorization.mechanism": "dac"}
            if perms := args.get(dac_perms_param_location):
                perms = [str(p).lower() for p in perms]
                attrs["contrast.authorization.dac.permissions"] = perms
            return attrs
    else:
        raise ValueError("Event must specify dac_perm or dac_perms")

    return SpanType.AuthorizationRequest, observe_span_attrs, None
