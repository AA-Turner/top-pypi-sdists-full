# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from typing import TYPE_CHECKING

from contrast_fireball import AssessEvent, AssessFinding, HttpRequest

import contrast
from contrast.utils.timer import now_ms

if TYPE_CHECKING:
    from contrast.agent.assess.rules.base_rule import BaseRule

CURRENT_FINDING_VERSION = 4


def build_finding(
    rule: BaseRule,
    properties: dict[str, str],
    events: list[AssessEvent] | None = None,
    request: HttpRequest | None = None,
    **kwargs,
) -> AssessFinding:
    """
    Builds a finding for the given rule. Properties are expected when the rule
    is a configuration or response scanning rule. Events are expected for
    dataflow rules. Request is expected for dataflow and response scanning rules.
    These expectations are from TeamServer, not checked in this function.
    """
    assert not rule.disabled, (
        "Rule should be checked for disabled before building finding"
    )
    from contrast.agent import agent_state

    if events:
        kwargs.update(events=events)
    if request:
        kwargs.update(request=request)

    return AssessFinding(
        version=CURRENT_FINDING_VERSION,
        events=events or [],
        properties=properties,
        routes=[],
        rule_id=rule.name,
        tags=agent_state.module.assess_tags,
        request=request,
        evidence=None,
        hash=int(rule.generate_preflight_hash(**kwargs)),
        created=events[-1].time if events else now_ms(),
    )


def send_finding(finding: AssessFinding, context=None) -> None:
    """
    Send a finding by either appending it to the ContrastContext OR sending it immediately.

    If `context` exists, the agent should not send the finding immediately because the
    current route needs to be appended (once it is available at the end of the request).
    """
    if context:
        web_context = contrast.WEB_CONTEXT.get()
        if (
            web_context is not None
            and web_context.input_exclusions_trigger_time
            and web_context.exclusions.evaluate_assess_trigger_time_exclusions(
                web_context, finding
            )
        ):
            return

        context.findings.append(finding)
        return

    from contrast.agent import agent_state

    agent_state.module.fireball_client.new_findings([finding])
