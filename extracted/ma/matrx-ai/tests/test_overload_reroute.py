"""Unit tests for overload-class retry/reroute decision logic
(orchestrator/overload_reroute.py) and the catalog reload counts surface
(catalog/manager.py::AiCatalogManager.counts). Pure fixtures, no DB."""

from __future__ import annotations

from matrx_ai.catalog.manager import QUARANTINED_ROWS, AiCatalogManager
from matrx_ai.orchestrator.overload_reroute import (
    DEFAULT_RETRY_MAX_ATTEMPTS,
    MAX_FALLBACK_HOPS,
    MAX_SIBLING_OFFERING_HOPS,
    OverloadPolicy,
    OverloadRerouteState,
    decide_overload_action,
    is_overload_error,
    is_reroutable_provider_error,
)
from matrx_ai.providers.errors import RetryableError


def _err(
    error_type: str = "provider_overloaded",
    status_code: int | None = 529,
    is_retryable: bool = True,
) -> RetryableError:
    return RetryableError(
        error_type=error_type,
        message=f"test {error_type}",
        status_code=status_code,
        is_retryable=is_retryable,
    )


# ── overload-class membership (explicit enumeration, never a bare except) ────
class TestIsOverloadError:
    def test_rate_limit_429(self):
        assert is_overload_error(_err("rate_limit", 429))

    def test_provider_overloaded_529(self):
        assert is_overload_error(_err("provider_overloaded", 529))

    def test_provider_overloaded_503(self):
        assert is_overload_error(_err("provider_overloaded", 503))

    def test_server_error_503_counts(self):
        assert is_overload_error(_err("server_error", 503))

    def test_server_error_500_does_not(self):
        assert not is_overload_error(_err("server_error", 500))

    def test_non_retryable_server_error_503_does_not(self):
        assert not is_overload_error(_err("server_error", 503, is_retryable=False))

    def test_invalid_request_does_not(self):
        assert not is_overload_error(_err("invalid_request", 400, is_retryable=False))

    def test_billing_error_does_not(self):
        assert not is_overload_error(_err("billing_error", 402, is_retryable=False))

    def test_billing_error_is_provider_reroutable(self):
        assert is_reroutable_provider_error(
            _err("billing_error", 400, is_retryable=False)
        )


# ── the decision function ────────────────────────────────────────────────────
class TestDecideOverloadAction:
    def _decide(self, **overrides):
        kwargs = dict(
            error_info=_err(),
            current_model="model-a",
            attempts_on_model=1,
            policy=OverloadPolicy(retry_max_attempts=2, fallback_ref="model-b"),
            models_tried=[],
            hops=0,
            produced_output=False,
        )
        kwargs.update(overrides)
        return decide_overload_action(**kwargs)

    def test_retry_same_within_budget(self):
        # 1 failed attempt, 2 retries allowed -> retry the SAME model.
        d = self._decide(attempts_on_model=1)
        assert d.action == "retry_same"

    def test_retry_same_at_exact_budget(self):
        # attempts_on_model counts the failure that just happened; with
        # retry_max_attempts=2, the 2nd failure still earns one more same-model try.
        d = self._decide(attempts_on_model=2)
        assert d.action == "retry_same"

    def test_reroute_when_budget_exhausted_and_fallback_set(self):
        d = self._decide(attempts_on_model=3)
        assert d.action == "reroute"
        assert d.to_model == "model-b"
        assert d.note is not None
        assert d.note.kind == "overload_reroute"
        assert d.note.from_model == "model-a"
        assert d.note.to_model == "model-b"
        assert d.note.attempts_on_model == 3
        assert d.note.error_type == "provider_overloaded"
        assert d.note.status_code == 529

    def test_give_up_when_no_fallback(self):
        d = self._decide(
            attempts_on_model=3,
            policy=OverloadPolicy(retry_max_attempts=2, fallback_ref=None),
        )
        assert d.action == "give_up"
        assert "retry_fallback_id" in d.reason

    def test_give_up_when_output_already_streamed(self):
        # A paid call that produced output is never re-run on another model.
        d = self._decide(attempts_on_model=3, produced_output=True)
        assert d.action == "give_up"
        assert "output" in d.reason

    def test_give_up_on_fallback_cycle(self):
        d = self._decide(attempts_on_model=3, models_tried=["model-b"])
        assert d.action == "give_up"
        assert "cycle" in d.reason

    def test_give_up_when_fallback_is_current_model(self):
        d = self._decide(
            attempts_on_model=3,
            policy=OverloadPolicy(retry_max_attempts=2, fallback_ref="model-a"),
        )
        assert d.action == "give_up"

    def test_give_up_at_hop_ceiling(self):
        d = self._decide(attempts_on_model=3, hops=MAX_FALLBACK_HOPS)
        assert d.action == "give_up"
        assert str(MAX_FALLBACK_HOPS) in d.reason

    def test_non_overload_error_gives_up(self):
        d = self._decide(error_info=_err("invalid_request", 400, is_retryable=False))
        assert d.action == "give_up"
        assert "not provider-reroutable" in d.reason

    def test_rate_limit_reroutes_too(self):
        d = self._decide(error_info=_err("rate_limit", 429), attempts_on_model=3)
        assert d.action == "reroute"

    def test_zero_retry_max_reroutes_on_first_failure(self):
        d = self._decide(
            attempts_on_model=1,
            policy=OverloadPolicy(retry_max_attempts=0, fallback_ref="model-b"),
        )
        assert d.action == "reroute"

    def test_billing_error_skips_same_route_retries(self):
        d = self._decide(
            error_info=_err("billing_error", 400, is_retryable=False),
            attempts_on_model=1,
        )
        assert d.action == "reroute"
        assert d.to_model == "model-b"

    def test_billing_error_prefers_sibling_offering_immediately(self):
        d = self._decide(
            error_info=_err("billing_error", 400, is_retryable=False),
            attempts_on_model=1,
            current_offering_id="off-1",
            sibling_offering_ids=["off-2"],
        )
        assert d.action == "reroute_offering"
        assert d.to_offering_id == "off-2"


# ── the sibling-offering rung (pinned → sibling → model-fallback ordering) ───
class TestSiblingOfferingLadder:
    def _decide(self, **overrides):
        kwargs = dict(
            error_info=_err(),
            current_model="model-a",
            attempts_on_model=3,  # same-offering budget exhausted
            policy=OverloadPolicy(retry_max_attempts=2, fallback_ref="model-b"),
            models_tried=[],
            hops=0,
            produced_output=False,
            current_offering_id="off-1",
            sibling_offering_ids=["off-2", "off-3"],
            offering_hops=0,
        )
        kwargs.update(overrides)
        return decide_overload_action(**kwargs)

    def test_retry_same_still_wins_within_budget(self):
        # Rung 1 beats rung 2: within the same-offering retry budget, no hop.
        d = self._decide(attempts_on_model=1)
        assert d.action == "retry_same"

    def test_sibling_offering_before_model_fallback(self):
        d = self._decide()
        assert d.action == "reroute_offering"
        assert d.to_offering_id == "off-2"  # priority order — first sibling
        assert d.to_model == "model-a"  # SAME model
        assert d.note is not None
        assert d.note.scope == "offering"
        assert d.note.from_offering_id == "off-1"
        assert d.note.to_offering_id == "off-2"
        assert d.note.from_model == d.note.to_model == "model-a"

    def test_model_fallback_when_no_siblings_left(self):
        d = self._decide(sibling_offering_ids=[])
        assert d.action == "reroute"
        assert d.to_model == "model-b"
        assert d.note is not None and d.note.scope == "model"

    def test_produced_output_blocks_sibling_hop_too(self):
        d = self._decide(produced_output=True)
        assert d.action == "give_up"
        assert "output" in d.reason

    def test_offering_hop_ceiling_falls_through_to_model_fallback(self):
        d = self._decide(offering_hops=MAX_SIBLING_OFFERING_HOPS)
        assert d.action == "reroute"
        assert d.to_model == "model-b"

    def test_offering_hop_ceiling_with_no_model_fallback_gives_up(self):
        d = self._decide(
            offering_hops=MAX_SIBLING_OFFERING_HOPS,
            policy=OverloadPolicy(retry_max_attempts=2, fallback_ref=None),
        )
        assert d.action == "give_up"

    def test_non_overload_error_never_reaches_the_ladder(self):
        # The owner's rule: a pin deviates ONLY on the predetermined
        # endpoint-specific error classes. Anything else gives up immediately.
        d = self._decide(error_info=_err("invalid_request", 400, is_retryable=False))
        assert d.action == "give_up"
        assert "not provider-reroutable" in d.reason

    def test_state_record_offering_reroute(self):
        state = OverloadRerouteState()
        d = self._decide()
        assert d.action == "reroute_offering" and d.note is not None
        state.record_offering_reroute(
            from_offering_id="off-1", note=d.note, next_base=4
        )
        assert state.offerings_tried == ["off-1"]
        assert state.offering_hops == 1
        assert state.attempt_base == 4
        # The model was NOT abandoned — models_tried stays empty so the later
        # model-level cycle check is not polluted.
        assert state.models_tried == []
        assert state.notes == [d.note]

    def test_full_ladder_exhaustion_then_model_hop(self):
        # off-1 fails -> off-2 -> off-3 -> model-b. Each rung consumes state.
        state = OverloadRerouteState()
        d1 = self._decide(sibling_offering_ids=["off-2", "off-3"])
        assert d1.action == "reroute_offering" and d1.to_offering_id == "off-2"
        state.record_offering_reroute(from_offering_id="off-1", note=d1.note, next_base=4)

        d2 = self._decide(
            current_offering_id="off-2",
            sibling_offering_ids=["off-3"],
            offering_hops=state.offering_hops,
        )
        assert d2.action == "reroute_offering" and d2.to_offering_id == "off-3"
        state.record_offering_reroute(from_offering_id="off-2", note=d2.note, next_base=8)

        d3 = self._decide(
            current_offering_id="off-3",
            sibling_offering_ids=[],
            offering_hops=state.offering_hops,
        )
        assert d3.action == "reroute" and d3.to_model == "model-b"


# ── per-iteration state bookkeeping ──────────────────────────────────────────
class TestOverloadRerouteState:
    def test_record_reroute_advances_base_and_hops(self):
        state = OverloadRerouteState()
        d = decide_overload_action(
            error_info=_err(),
            current_model="model-a",
            attempts_on_model=3,
            policy=OverloadPolicy(retry_max_attempts=2, fallback_ref="model-b"),
            models_tried=state.models_tried,
            hops=state.hops,
            produced_output=False,
        )
        assert d.action == "reroute" and d.note is not None
        state.record_reroute(from_model="model-a", note=d.note, next_base=4)
        assert state.attempt_base == 4
        assert state.hops == 1
        assert state.models_tried == ["model-a"]
        assert state.notes == [d.note]

        # Chain back to model-a is now a cycle.
        d2 = decide_overload_action(
            error_info=_err(),
            current_model="model-b",
            attempts_on_model=3,
            policy=OverloadPolicy(retry_max_attempts=2, fallback_ref="model-a"),
            models_tried=state.models_tried,
            hops=state.hops,
            produced_output=False,
        )
        assert d2.action == "give_up"

    def test_default_policy_matches_column_default(self):
        assert OverloadPolicy().retry_max_attempts == DEFAULT_RETRY_MAX_ATTEMPTS
        assert OverloadPolicy().fallback_ref is None


# ── reload counts (the admin reload endpoint's summary source) ───────────────
class TestCatalogCounts:
    def test_counts_after_load_from_rows(self):
        manager = AiCatalogManager()
        manager.load_from_rows(
            endpoints=[
                {
                    "id": "ep-1",
                    "vendor": "openai",
                    "internal_name": "openai_direct",
                    "display_name": "OpenAI",
                }
            ],
            apis=[
                {
                    "id": "api-1",
                    "name": "openai_chat",
                    "display_name": "OpenAI Chat",
                    "translator_key": "openai_chat",
                    "rules": {"params": {}, "constraints": []},
                }
            ],
            offerings=[
                {
                    "id": "off-1",
                    "model_id": "model-1",
                    "endpoint_id": "ep-1",
                    "api_id": "api-1",
                    "provider_model_id": "gpt-5.2",
                    "override": {"params": {}, "constraints": []},
                }
            ],
            settings=[
                {
                    "key": "temperature",
                    "value_type": "number",
                    "canonical_min": 0,
                    "canonical_max": 2,
                }
            ],
            providers={"prov-1": "OpenAI"},
            models=[
                {"id": "model-1", "name": "gpt-5.2"},
                {"id": "model-2", "name": "claude-fable-5"},
            ],
            aliases=[
                {"id": "al-1", "alias": "best-fast", "model_id": "model-1", "kind": "alias"},
            ],
        )
        counts = manager.counts()
        assert counts.endpoints == 1
        assert counts.apis == 1
        assert counts.offerings == 1
        assert counts.settings == 1
        assert counts.providers == 1
        assert counts.models == 2
        assert counts.aliases == 1
        assert counts.quarantined == len(QUARANTINED_ROWS) == 0

    def test_counts_track_quarantine(self):
        manager = AiCatalogManager()
        manager.load_from_rows(
            endpoints=[
                {
                    # empty vendor -> quarantined endpoint
                    "id": "ep-bad",
                    "vendor": "  ",
                    "internal_name": "broken",
                    "display_name": "Broken",
                }
            ],
            apis=[],
            offerings=[],
            settings=[],
        )
        counts = manager.counts()
        assert counts.endpoints == 0
        assert counts.quarantined == 1
