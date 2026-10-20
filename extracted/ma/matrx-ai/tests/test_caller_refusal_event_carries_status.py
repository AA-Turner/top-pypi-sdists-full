"""An expected caller refusal (spend ceiling, usage limit) must reach the wire with the status it
answers with, never a bare event a client reads as a 500 crash (live 2026-10-17: a spend-ceiling
refusal was recorded with http_status 500 by the agent test door)."""

from matrx_ai.orchestrator.executor import _caller_refusal_details
from matrx_ai.providers.guardrail_gate import GuardrailStopError


def test_a_guardrail_refusal_event_carries_its_429():
    stop = GuardrailStopError(
        kind="daily_spend", subject_kind="user", subject_id="u", limit=10, observed=19.98,
        message="reached its daily AI spend ceiling",
    )
    details = _caller_refusal_details(stop.error_info)
    assert details["status_code"] == 429
    assert details["guardrail"] == "daily_spend"
