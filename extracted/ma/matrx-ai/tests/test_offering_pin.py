"""Unit tests for the offering-pin resolution semantics
(catalog/resolve.py::_resolve_pinned_offering) — "we're not listing the model,
we're listing the exact call." Pure fixtures via load_from_rows, no DB.

The async resolve_call_profile funnel needs a host model manager; the pin
selection/validation core is the sync helper, tested exhaustively here. The
funnel-level pin plumbing is exercised by the live e2e (pin → together serves
GPT OSS 120B instead of the preferred cerebras).
"""

from __future__ import annotations

import pytest

from matrx_ai.catalog.manager import AiCatalogManager
from matrx_ai.catalog.resolve import _resolve_pinned_offering


def _loaded_manager() -> AiCatalogManager:
    manager = AiCatalogManager()
    manager.load_from_rows(
        endpoints=[
            {
                "id": "ep-cerebras",
                "vendor": "cerebras",
                "internal_name": "cerebras_direct",
                "display_name": "Matrx Fast",
            },
            {
                "id": "ep-together",
                "vendor": "together",
                "internal_name": "together_direct",
                "display_name": "Matrx Standard",
            },
            {
                "id": "ep-dead",
                "vendor": "groq",
                "internal_name": "groq_direct",
                "display_name": "Inactive",
                "is_active": False,
            },
        ],
        apis=[
            {
                "id": "api-oa",
                "name": "openai_chat",
                "display_name": "OpenAI Chat",
                "translator_key": "openai_chat",
                "rules": {"params": {}, "constraints": []},
            }
        ],
        offerings=[
            {
                "id": "off-cerebras",
                "model_id": "model-1",
                "endpoint_id": "ep-cerebras",
                "api_id": "api-oa",
                "provider_model_id": "gpt-oss-120b",
                "priority": 10,
                "override": {"params": {}, "constraints": []},
            },
            {
                "id": "off-together",
                "model_id": "model-1",
                "endpoint_id": "ep-together",
                "api_id": "api-oa",
                "provider_model_id": "openai/gpt-oss-120b",
                "priority": 20,
                "override": {"params": {}, "constraints": []},
            },
            {
                "id": "off-unavailable",
                "model_id": "model-1",
                "endpoint_id": "ep-together",
                "api_id": "api-oa",
                "provider_model_id": "openai/gpt-oss-120b",
                "priority": 30,
                "is_available": False,
                "override": {"params": {}, "constraints": []},
            },
            {
                "id": "off-dead-endpoint",
                "model_id": "model-1",
                "endpoint_id": "ep-dead",
                "api_id": "api-oa",
                "provider_model_id": "gpt-oss-120b",
                "priority": 40,
                "override": {"params": {}, "constraints": []},
            },
            {
                "id": "off-other-model",
                "model_id": "model-2",
                "endpoint_id": "ep-cerebras",
                "api_id": "api-oa",
                "provider_model_id": "llama-4-70b",
                "priority": 10,
                "override": {"params": {}, "constraints": []},
            },
        ],
        settings=[],
        models=[
            {"id": "model-1", "name": "gpt-oss-120b"},
            {"id": "model-2", "name": "llama-4-70b"},
        ],
    )
    return manager


class TestPinnedOfferingResolution:
    def test_pin_resolves_exactly_that_offering(self):
        manager = _loaded_manager()
        offerings = manager.offerings_for("model-1")
        # Preferred head is the cerebras offering (priority 10)...
        assert offerings[0].id == "off-cerebras"
        # ...but the pin selects the together sibling exactly.
        chosen = _resolve_pinned_offering(
            offerings,
            manager,
            offering_id="off-together",
            model_id="model-1",
            model_name="gpt-oss-120b",
        )
        assert chosen.id == "off-together"
        assert chosen.provider_model_id == "openai/gpt-oss-120b"

    def _expect_raise(self, manager, pin: str, match: str):
        offerings = manager.offerings_for("model-1")
        with pytest.raises(ValueError, match=match):
            _resolve_pinned_offering(
                offerings,
                manager,
                offering_id=pin,
                model_id="model-1",
                model_name="gpt-oss-120b",
            )

    def test_unknown_offering_raises(self):
        self._expect_raise(_loaded_manager(), "off-nope", "does not exist")

    def test_cross_model_pin_raises(self):
        # The pin belongs to model-2 — a model swap must clear the pin, never
        # silently re-route.
        self._expect_raise(_loaded_manager(), "off-other-model", "belongs to model_id")

    def test_unavailable_offering_raises(self):
        self._expect_raise(_loaded_manager(), "off-unavailable", "is_available=false")

    def test_inactive_endpoint_offering_raises(self):
        self._expect_raise(_loaded_manager(), "off-dead-endpoint", "missing or inactive")

    def test_no_silent_fallback_to_preferred(self):
        # The failure mode the pin exists to prevent: an unroutable pin must
        # NEVER return the preferred offering.
        manager = _loaded_manager()
        offerings = manager.offerings_for("model-1")
        try:
            _resolve_pinned_offering(
                offerings,
                manager,
                offering_id="off-unavailable",
                model_id="model-1",
                model_name="gpt-oss-120b",
            )
        except ValueError:
            return
        raise AssertionError("pinned resolution silently fell back to preferred")


class TestResolvedProfileRoute:
    def test_resolution_route_default_is_preferred(self):
        from matrx_ai.catalog.models import ResolvedCallProfile

        assert (
            ResolvedCallProfile.model_fields["resolution_route"].default == "preferred"
        )


class TestOfferingStampPersistence:
    """The per-call record stamp: TokenUsage.offering_id/offering_route (set by
    UnifiedAIClient._stamp_offering_usage) must land in the per-iteration
    cx_request row's metadata via CompletedRequest.to_storage_dict — and the
    user pin must round-trip through the conversation config JSONB while the
    RUNTIME sibling pin must NOT."""

    @pytest.fixture(autouse=True)
    def _ambient_context(self):
        """Own the ambient AppContext for the duration of ONE test.

        ``to_storage_dict`` stamps ``user_id`` from the ambient context, so these
        tests need one — but the ContextVar is process-global, so leaving it set
        pollutes every later test in the session (the repo-root
        ``_no_leaked_app_context`` guard fails the polluting test by name).
        Set here, cleared with the token in teardown.
        """
        from matrx_ai.context.app_context import (
            AppContext,
            clear_app_context,
            set_app_context,
        )

        token = set_app_context(AppContext(emitter=None, user_id="u1"))
        try:
            yield
        finally:
            clear_app_context(token)

    def _completed(self):
        from matrx_ai.config.unified_config import UnifiedConfig
        from matrx_ai.config.usage_config import TokenUsage
        from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

        config = UnifiedConfig(
            model="gpt-oss-120b",
            messages=[{"role": "user", "content": "hi"}],
            offering_id="off-user-pin",
            runtime_offering_id="off-sibling",
        )
        req = AIMatrixRequest(
            conversation_id="c1",
            config=config,
            usage_history=[
                TokenUsage(
                    input_tokens=10,
                    output_tokens=5,
                    matrx_model_name="gpt-oss-120b",
                    api="together",
                    offering_id="off-sibling",
                    offering_route="sibling_fallback",
                    billing_components={"input.text": 10, "output.text": 5},
                    metadata={"cost_reconciliation": "provider_exact"},
                )
            ],
        )
        return CompletedRequest(request=req, iterations=1, final_response=None)

    def test_row_metadata_carries_offering(self):
        storage = self._completed().to_storage_dict()
        row = storage["requests"][0]
        assert row["metadata"] == {
            "offering_id": "off-sibling",
            "offering_route": "sibling_fallback",
            "billing_components": {"input.text": 10, "output.text": 5},
            "cost_reconciliation": "provider_exact",
        }

    def test_provider_reported_cost_is_preserved_with_the_raw_usage_audit_record(self):
        from matrx_ai.config.usage_config import TokenUsage

        completed = self._completed()
        completed.request.usage_history = [
            TokenUsage(
                input_tokens=10,
                output_tokens=5,
                matrx_model_name="gpt-oss-120b",
                api="together",
                offering_id="off-sibling",
                offering_route="sibling_fallback",
                raw_usage={"prompt_tokens": 10, "completion_tokens": 5, "cost": 0.0042},
            )
        ]

        row = completed.to_storage_dict()["requests"][0]

        assert row["raw_usage"]["cost"] == 0.0042
        assert row["metadata"]["provider_charge_available"] is True
        assert row["metadata"]["provider_charge_usd"] == 0.0042
        assert row["metadata"]["provider_charge"]["field_path"] == "usage.cost"

    def test_retry_attempts_are_grouped_without_losing_paid_calls(self):
        from matrx_ai.config.usage_config import TokenUsage

        completed = self._completed()
        completed.request.usage_history = [
            TokenUsage(
                input_tokens=100,
                output_tokens=2,
                matrx_model_name="model-a",
                api="anthropic",
                raw_usage={"input_tokens": 100, "output_tokens": 2},
                metadata={
                    "iteration": 1,
                    "provider_attempt": 1,
                    "attempt_outcome": "failed",
                },
            ),
            TokenUsage(
                input_tokens=100,
                output_tokens=20,
                matrx_model_name="model-b",
                api="anthropic",
                raw_usage={"input_tokens": 100, "output_tokens": 20},
                metadata={
                    "iteration": 1,
                    "provider_attempt": 2,
                    "attempt_outcome": "succeeded",
                },
            ),
        ]

        storage = completed.to_storage_dict()
        row = storage["requests"][0]

        assert len(storage["requests"]) == 1
        assert row["input_tokens"] == 200
        assert row["output_tokens"] == 22
        assert row["raw_usage"]["provider_attempts"] == [
            {"input_tokens": 100, "output_tokens": 2},
            {"input_tokens": 100, "output_tokens": 20},
        ]
        assert [attempt["outcome"] for attempt in row["metadata"]["provider_attempts"]] == [
            "failed",
            "succeeded",
        ]
        assert completed.request.total_usage.total.total_requests == 2
        assert completed.request.total_usage.total.unique_models == 2

    def test_user_pin_persists_but_runtime_pin_does_not(self):
        storage = self._completed().to_storage_dict()
        conv_config = storage["conversation"]["config"]
        assert conv_config["offering_id"] == "off-user-pin"
        assert "runtime_offering_id" not in conv_config

    def test_routing_pin_prefers_runtime_over_user(self):
        from matrx_ai.config.unified_config import UnifiedConfig

        config = UnifiedConfig(
            model="m",
            messages=[],
            offering_id="off-user-pin",
            runtime_offering_id="off-sibling",
        )
        assert config.routing_offering_id == "off-sibling"
        config.runtime_offering_id = None
        assert config.routing_offering_id == "off-user-pin"

    def test_offering_id_round_trips_from_dict(self):
        from matrx_ai.config.unified_config import UnifiedConfig

        config = UnifiedConfig.from_dict(
            {"model": "m", "messages": [], "offering_id": "off-1"}
        )
        assert config.offering_id == "off-1"
        # A settings blob key, not an unrecognized key — no warning path.
        assert "offering_id" not in (config._unrecognized_keys or [])
