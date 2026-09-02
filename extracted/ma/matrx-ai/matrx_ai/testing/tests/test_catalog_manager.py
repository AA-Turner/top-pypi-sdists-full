"""Unit tests for AiCatalogManager compile/validate/quarantine — fixture rows, no DB."""

from __future__ import annotations

import pytest

from matrx_ai.catalog.manager import (
    QUARANTINED_ROWS,
    WIRE_FORMATS,
    AiCatalogManager,
)
from matrx_ai.catalog.resolve import client_attr_for_wire_format

SETTINGS = [
    {
        "key": "reasoning_effort",
        "value_type": "enum",
        "canonical_values": [
            "auto", "none", "minimal", "low", "medium", "high", "xhigh", "max"
        ],
    },
    {
        "key": "temperature",
        "value_type": "number",
        "canonical_min": 0,
        "canonical_max": 2,
    },
    {"key": "max_output_tokens", "value_type": "integer", "canonical_min": 1},
]


def _endpoint(**overrides) -> dict:
    base = {
        "id": "ep-1",
        "vendor": "openai",
        "internal_name": "openai_direct",
        "display_name": "OpenAI (direct)",
    }
    base.update(overrides)
    return base


def _api(params: dict | None = None, **overrides) -> dict:
    base = {
        "id": "api-1",
        "name": "openai_chat",
        "display_name": "OpenAI Chat Completions",
        "translator_key": "openai_chat",
        "rules": {"params": params or {}, "constraints": []},
    }
    base.update(overrides)
    return base


def _offering(override_params: dict | None = None, **overrides) -> dict:
    base = {
        "id": "off-1",
        "model_id": "model-1",
        "endpoint_id": "ep-1",
        "api_id": "api-1",
        "provider_model_id": "gpt-5.2",
        "override": {"params": override_params or {}, "constraints": []},
    }
    base.update(overrides)
    return base


def _load(manager, **kwargs) -> None:
    kwargs.setdefault("endpoints", [_endpoint()])
    kwargs.setdefault("apis", [_api()])
    kwargs.setdefault("offerings", [_offering()])
    kwargs.setdefault("settings", SETTINGS)
    manager.load_from_rows(**kwargs)


@pytest.fixture
def manager() -> AiCatalogManager:
    return AiCatalogManager()  # singleton — load_from_rows resets state per test


class TestHappyPath:
    def test_load_and_read(self, manager):
        _load(
            manager,
            apis=[
                _api(
                    params={
                        "reasoning_effort": {
                            "provider_key": "reasoning.effort",
                            "value_map": {"xhigh": "high", "high": "high"},
                        }
                    }
                )
            ],
            offerings=[
                _offering(
                    override_params={
                        "reasoning_effort": {"value_map": {"xhigh": "xhigh", "high": "high"}}
                    }
                )
            ],
            providers={"prov-1": "OpenAI"},
        )
        assert QUARANTINED_ROWS == []
        offerings = manager.offerings_for("model-1")
        assert [o.id for o in offerings] == ["off-1"]
        assert manager.provider_name("prov-1") == "OpenAI"

        compiled = manager.compiled_controls("api-1", "off-1")
        # offering value_map wins per-field; api provider_key survives.
        out, adj = compiled.outbound({"reasoning_effort": "xhigh"})
        assert out == {"reasoning": {"effort": "xhigh"}}
        assert adj == []

    def test_priority_ordering_and_availability(self, manager):
        _load(
            manager,
            endpoints=[_endpoint(id="ep-1"), _endpoint(id="ep-2", vendor="generic_openai")],
            offerings=[
                _offering(id="off-low", endpoint_id="ep-2", priority=200),
                _offering(id="off-high", endpoint_id="ep-1", priority=10),
                _offering(id="off-off", endpoint_id="ep-1", priority=1, is_available=False),
            ],
        )
        assert [o.id for o in manager.offerings_for("model-1")] == ["off-high", "off-low"]

    def test_inactive_endpoint_hides_offerings(self, manager):
        _load(manager, endpoints=[_endpoint(is_active=False)])
        assert manager.offerings_for("model-1") == []


class TestQuarantine:
    def test_unknown_rule_field_quarantines_api_and_its_offerings(self, manager):
        _load(manager, apis=[_api(params={"reasoning_effort": {"typo_field": True}})])
        kinds = {(r.kind, r.row_id) for r in QUARANTINED_ROWS}
        assert ("api", "api-1") in kinds
        assert ("offering", "off-1") in kinds  # its api is gone
        assert manager.offerings_for("model-1") == []
        assert manager.api("api-1") is None

    def test_unknown_envelope_key_quarantines(self, manager):
        # The envelope itself is extra="forbid" — {"params", "constraints"} only.
        _load(manager, apis=[_api(rules={"params": {}, "constraints": [], "bogus": 1})])
        assert any(r.kind == "api" and r.row_id == "api-1" for r in QUARANTINED_ROWS)

    def test_missing_endpoint_quarantines_offering(self, manager):
        _load(manager, offerings=[_offering(endpoint_id="ep-missing")])
        assert any(
            r.kind == "offering" and "endpoint 'ep-missing'" in " ".join(r.errors)
            for r in QUARANTINED_ROWS
        )
        assert manager.offerings_for("model-1") == []

    def test_unknown_setting_key_quarantines(self, manager):
        _load(manager, apis=[_api(params={"not_a_setting": {"supported": False}})])
        assert any(
            r.kind == "api" and "not_a_setting" in " ".join(r.errors) for r in QUARANTINED_ROWS
        )

    def test_enum_value_map_key_outside_canonical_values(self, manager):
        _load(
            manager,
            offerings=[
                _offering(override_params={"reasoning_effort": {"value_map": {"bogus": "high"}}})
            ],
        )
        assert any(r.kind == "offering" and r.row_id == "off-1" for r in QUARANTINED_ROWS)
        assert manager.offerings_for("model-1") == []

    def test_clamp_outside_canonical_range(self, manager):
        _load(manager, apis=[_api(params={"temperature": {"clamp": {"min": 0, "max": 3}}})])
        assert any(
            r.kind == "api" and "canonical_max" in " ".join(r.errors) for r in QUARANTINED_ROWS
        )

    def test_unknown_translator_key_quarantines(self, manager):
        _load(manager, apis=[_api(translator_key="carrier_pigeon")])
        assert any(
            r.kind == "api" and "translator_key" in " ".join(r.errors) for r in QUARANTINED_ROWS
        )

    def test_bad_row_never_crashes_and_good_rows_still_serve(self, manager):
        _load(
            manager,
            apis=[
                _api(id="api-bad", params={"reasoning_effort": {"nope": 1}}),
                _api(id="api-good", name="openai_chat_good"),
            ],
            offerings=[
                _offering(id="off-bad", api_id="api-bad"),
                _offering(id="off-good", api_id="api-good"),
            ],
        )
        assert [o.id for o in manager.offerings_for("model-1")] == ["off-good"]

    def test_bad_setting_row_quarantined(self, manager):
        _load(manager, settings=[{"key": "weird", "value_type": "quantum"}], offerings=[])
        assert any(r.kind == "setting" and r.row_id == "weird" for r in QUARANTINED_ROWS)


class TestWireFormats:
    def test_specials_are_known(self):
        assert "extraction_gliner" in WIRE_FORMATS
        assert "openai_embeddings" in WIRE_FORMATS
        assert "openai_realtime" in WIRE_FORMATS
        assert "xai_realtime" in WIRE_FORMATS

    def test_endpoint_attrs_are_known(self):
        for wf in ("openai_chat", "google_image", "anthropic_chat", "xai_video"):
            assert wf in WIRE_FORMATS

    def test_client_attr_identity_and_specials(self):
        assert client_attr_for_wire_format("openai_chat") == "openai_chat"
        assert client_attr_for_wire_format("extraction_gliner") == "extraction"
        assert client_attr_for_wire_format("openai_embeddings") == "embedding"
        assert client_attr_for_wire_format("openai_realtime") == "realtime"
        assert client_attr_for_wire_format("xai_realtime") == "realtime"

    @pytest.mark.parametrize(
        ("translator_key", "provider_model_id"),
        [
            ("openai_embeddings", "text-embedding-3-large"),
            ("openai_realtime", "gpt-realtime-2.1"),
            ("openai_realtime", "gpt-realtime-2.1-mini"),
        ],
    )
    def test_live_openai_specialized_routes_compile(
        self, manager, translator_key, provider_model_id
    ):
        _load(
            manager,
            apis=[
                _api(
                    name=translator_key,
                    translator_key=translator_key,
                    transport="websocket" if translator_key == "openai_realtime" else "sdk",
                )
            ],
            offerings=[_offering(provider_model_id=provider_model_id)],
        )
        assert QUARANTINED_ROWS == []
        assert [o.provider_model_id for o in manager.offerings_for("model-1")] == [
            provider_model_id
        ]


class TestVendorIsARecordedFact:
    """ai.endpoint.vendor is a COLUMN, never a slice of a translator_key.

    The deleted ``_vendor_from_wire_format`` chopped a ``_chat``/``_image``/``_video``
    suffix off the route token. It silently returned "" for the two shapeless routes,
    bucketing extraction + voice cost under an empty vendor. These tests pin the fact
    that killed it: the vendor is whatever the row SAYS, and two endpoints that share
    an api (wire shape) may carry different vendors.
    """

    def test_shapeless_routes_carry_a_real_vendor(self, manager):
        # Exactly what the string-slicing got wrong: no "_chat"/"_image"/"_video"
        # suffix to strip, so the old code returned "" for both.
        _load(
            manager,
            endpoints=[
                _endpoint(id="ep-gliner", vendor="fastino", internal_name="fastino_gliner"),
                _endpoint(id="ep-realtime", vendor="xai", internal_name="xai_realtime"),
            ],
            apis=[
                _api(id="api-gliner", name="gliner", translator_key="extraction_gliner"),
                _api(id="api-realtime", name="realtime", translator_key="xai_realtime"),
            ],
            offerings=[],
        )
        assert manager.endpoint("ep-gliner").vendor == "fastino"
        assert manager.endpoint("ep-realtime").vendor == "xai"

    def test_same_api_may_carry_different_vendors(self, manager):
        # An OpenAI-compatible route is the whole point of the split: the wire SHAPE
        # (ai.api) says nothing about who is billed (ai.endpoint). Slicing "openai"
        # out of "openai_chat" here would mis-attribute every dollar to OpenAI.
        _load(
            manager,
            endpoints=[
                _endpoint(id="ep-oai", vendor="openai", internal_name="openai_direct"),
                _endpoint(id="ep-azure", vendor="generic_openai", internal_name="azure_openai"),
            ],
            offerings=[
                _offering(id="off-oai", endpoint_id="ep-oai"),
                _offering(id="off-azure", endpoint_id="ep-azure"),
            ],
        )
        oai = manager.offerings_for("model-1")
        assert {manager.endpoint(o.endpoint_id).vendor for o in oai} == {
            "openai",
            "generic_openai",
        }
        assert {manager.api(o.api_id).translator_key for o in oai} == {"openai_chat"}

    def test_missing_vendor_quarantines_the_row(self, manager):
        raw = _endpoint()
        del raw["vendor"]
        _load(manager, endpoints=[raw], offerings=[])
        assert manager.endpoint("ep-1") is None
        assert any(r.kind == "endpoint" and r.row_id == "ep-1" for r in QUARANTINED_ROWS)

    def test_empty_vendor_quarantines_the_row(self, manager):
        # NOT NULL does not stop ''. An empty vendor is the exact bug being retired.
        _load(manager, endpoints=[_endpoint(vendor="   ")], offerings=[])
        assert manager.endpoint("ep-1") is None
        assert any(r.kind == "endpoint" and r.row_id == "ep-1" for r in QUARANTINED_ROWS)


class TestModelRefRouting:
    """resolve_model_ref — the ONE instant name-routing map (id -> name -> alias)."""

    def test_id_name_and_alias_all_resolve_to_the_model_id(self, manager):
        _load(
            manager,
            models=[{"id": "model-1", "name": "gpt-5.2"}],
            aliases=[
                {"id": "al-1", "alias": "gpt-5.2-latest", "model_id": "model-1", "kind": "latest"},
                {"id": "al-2", "alias": "gpt-5", "model_id": "model-1", "kind": "deprecated"},
                {"id": "al-3", "alias": "best-chat", "model_id": "model-1", "kind": "alias"},
            ],
        )
        assert manager.resolve_model_ref("model-1") == "model-1"  # id
        assert manager.resolve_model_ref("gpt-5.2") == "model-1"  # name
        # every alias kind resolves identically at lookup:
        assert manager.resolve_model_ref("gpt-5.2-latest") == "model-1"
        assert manager.resolve_model_ref("gpt-5") == "model-1"
        assert manager.resolve_model_ref("best-chat") == "model-1"

    def test_unknown_ref_passes_through_unchanged(self, manager):
        _load(manager)
        assert manager.resolve_model_ref("no-such-model") == "no-such-model"

    def test_deprecated_model_name_surrenders_to_alias(self, manager):
        _load(
            manager,
            models=[
                {"id": "old-model", "name": "qwen-3-235b-a22b-instruct-2507", "is_deprecated": True},
                {"id": "new-model", "name": "openai/gpt-oss-120b", "is_deprecated": False},
            ],
            aliases=[
                {
                    "id": "al-qwen",
                    "alias": "qwen-3-235b-a22b-instruct-2507",
                    "model_id": "new-model",
                    "kind": "deprecated",
                }
            ],
        )

        assert manager.resolve_model_ref("qwen-3-235b-a22b-instruct-2507") == "new-model"
        assert manager.resolve_model_ref("old-model") == "old-model"

    def test_bad_alias_row_quarantines(self, manager):
        _load(manager, aliases=[{"id": "al-bad", "alias": "", "model_id": "model-1"}])
        assert any(r.kind == "alias" and r.row_id == "al-bad" for r in QUARANTINED_ROWS)
