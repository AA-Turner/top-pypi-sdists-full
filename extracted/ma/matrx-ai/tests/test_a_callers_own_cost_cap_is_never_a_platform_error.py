"""A PAID CALL REFUSED BY THE CALLER'S OWN COST CAP IS NEVER A PLATFORM ERROR (2026-11-21).

Live: four ``tool_execution_failed`` rows ``seo_domain (over_max_cost): This seo_domain.overview
call is estimated at $0.0362 (724 points), above your max_cost_usd of $0.0001 (2 points); nothing
was spent.`` The cap is the caller's own argument; the spend desk (aidream
``action_requests/spend_ask.py``) refused at zero cost and its sentence names the value to send.
Same for a spend approval id that was not issued to this caller. A spend desk ``configuration``
refusal (a run with no organization) is the platform's wiring and stays filed.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools.executor import _is_expected_domain_failure


@pytest.mark.parametrize("error_type", ["over_max_cost", "spend_approval_not_yours"])
def test_the_callers_own_spend_argument_is_a_refusal(error_type: str) -> None:
    assert _is_expected_domain_failure(
        tool_name="seo_domain",
        error_type=error_type,
        message="This seo_domain.overview call is estimated at $0.0362, above your max_cost_usd of $0.0001; nothing was spent.",
    )


def test_a_spend_desk_wiring_refusal_is_still_filed() -> None:
    assert not _is_expected_domain_failure(
        tool_name="seo_domain",
        error_type="configuration",
        message="A paid call spends an organization's money, and this run carries no organization.",
    )
