"""An organization's ``agents.context_trim`` knobs reach the ONE send boundary.

The tiers used to be dataclass constants: an admin turning the knob for an
organization changed nothing. ``prepare_for_send`` now resolves the policy per
organization through the host's resolver (``set_trim_policy_resolver``); with no
host the ruled defaults (12/8000 + 24/2000) still apply, and a resolver that
raises is announced and stamped on the audit — never a silent default.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.config import ToolResultContent, UnifiedMessage
from matrx_ai.config.context_trim import (
    TRIM_POLICY_KNOB_KEYS,
    TrimPolicy,
    set_trim_policy_resolver,
    trim_policy_from_knobs,
)
from matrx_ai.config.send_boundary import STAGE_RESOLVE, prepare_for_send

TIGHT_ORG = "org-tight"
PLAIN_ORG = "org-plain"


def _config() -> SimpleNamespace:
    # 6 results of 3,000 chars. Under the ruled tiers nothing is eligible (tier 1
    # needs >8000 chars, tier 2 needs 24 positions back). TIGHT_ORG sets tier 1
    # to 2 back / 1000 chars, so the first four (2-5 back) become eligible.
    return SimpleNamespace(
        messages=[
            UnifiedMessage(
                role="tool",
                position=None,
                content=[
                    ToolResultContent(
                        tool_use_id=f"call-{i}",
                        name="large_tool",
                        content="x" * 3_000,
                        output_chars=3_000,
                    )
                ],
            )
            for i in range(6)
        ],
        system_instruction=None,
        prompt_cache_key=None,
    )


async def _host_resolver(organization_id: str | None) -> TrimPolicy:
    rows = {
        "tier_1_min_positions_back": 12,
        "tier_1_min_output_chars": 8000,
        "tier_2_min_positions_back": 24,
        "tier_2_min_output_chars": 2000,
    }
    if organization_id == TIGHT_ORG:
        rows.update(tier_1_min_positions_back=2, tier_1_min_output_chars=1000)
    return trim_policy_from_knobs(rows)


@pytest.fixture(autouse=True)
def _unbind():
    set_trim_policy_resolver(None)
    yield
    set_trim_policy_resolver(None)


async def _send(organization_id: str | None):
    return await prepare_for_send(
        _config(), stage=STAGE_RESOLVE, conversation_id=None, organization_id=organization_id
    )


@pytest.mark.asyncio
async def test_an_org_override_changes_the_policy_that_reaches_the_send_boundary() -> None:
    set_trim_policy_resolver(_host_resolver)

    tight = await _send(TIGHT_ORG)
    plain = await _send(PLAIN_ORG)

    assert tight.trim_report is not None and plain.trim_report is not None
    assert tight.trim_report.policy["tier_1_min_positions_back"] == 2
    assert tight.trim_report.policy["source"] == "org_knobs"
    assert tight.trim_report.blocks_rewritten == 4
    assert plain.trim_report.policy["tier_1_min_positions_back"] == 12
    assert plain.trim_report.blocks_rewritten == 0


@pytest.mark.asyncio
async def test_no_host_resolver_means_the_ruled_defaults() -> None:
    prep = await _send(TIGHT_ORG)

    assert prep.trim_report is not None
    snap = prep.trim_report.policy
    assert (snap["tier_1_min_positions_back"], snap["tier_1_min_output_chars"]) == (12, 8000)
    assert (snap["tier_2_min_positions_back"], snap["tier_2_min_output_chars"]) == (24, 2000)
    assert snap["source"] == "package_default"


@pytest.mark.asyncio
async def test_a_failing_resolver_is_stamped_on_the_audit_not_silent() -> None:
    async def _missing_row(_org: str | None) -> TrimPolicy:
        raise LookupError("feature knob agents.context_trim.tier_1_min_positions_back not registered")

    set_trim_policy_resolver(_missing_row)
    prep = await _send(TIGHT_ORG)

    assert prep.trim_report is not None
    assert prep.trim_report.policy["source"] == "package_default:resolver_failed"
    assert prep.trim_report.policy["tier_2_min_positions_back"] == 24


def test_a_missing_knob_value_raises_rather_than_defaulting() -> None:
    with pytest.raises(KeyError):
        trim_policy_from_knobs({k: 1 for k in TRIM_POLICY_KNOB_KEYS[:-1]})
