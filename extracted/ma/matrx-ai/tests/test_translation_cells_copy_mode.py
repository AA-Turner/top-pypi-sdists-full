"""Settings-translation item C1 — the engine tolerates the cell world before any data moves.

Contracts: common-docs/projects/settings-translation/CONTRACTS.md (K5, K6, K9).

1. A rule row carrying any K6 field (``off``, ``from_number``, ``to_number``,
   ``accepts``, ``{"drop": true, "why"}``) compiles WITHOUT quarantine and
   WITHOUT changing a single wire byte (nothing acts on K6 until item C5).
2. Every Adjustment carries K9 provenance; the foreign-key gate's drops become
   Adjustments (still silent to the client until item C6).
3. Rows shaped exactly like ``ai.offering_rules_compiled`` (K5) compile to the
   most specific cell per key, WHOLE (no field merge), and the cell's
   id/layer/state reach every Adjustment for that key.
"""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import patch

import pytest

from matrx_ai.catalog import manager as manager_mod
from matrx_ai.catalog.controls import (
    ViewRowError,
    compile_controls,
    compile_controls_from_cells,
    select_cells_from_view,
)
from matrx_ai.catalog.manager import QUARANTINED_ROWS, AiCatalogManager
from matrx_ai.catalog.models import ControlRule
from matrx_ai.providers import outbound_params

API_ID = "a7a1c3de-0000-4000-8000-000000000001"
ENDPOINT_ID = "e0e1c3de-0000-4000-8000-000000000001"
OFFERING_ID = "0ff1c3de-0000-4000-8000-000000000001"
OTHER_OFFERING_ID = "0ff1c3de-0000-4000-8000-000000000002"
MODEL_ID = "m0d1c3de-0000-4000-8000-000000000001"
PROFILE_ID = "9f0f11e0-0000-4000-8000-000000000001"

SETTINGS: list[dict[str, Any]] = [
    {
        "key": "reasoning_effort",
        "value_type": "enum",
        "canonical_values": ["auto", "none", "minimal", "low", "medium", "high", "xhigh", "max"],
    },
    {"key": "max_output_tokens", "value_type": "integer", "canonical_min": 1},
    {"key": "temperature", "value_type": "number", "canonical_min": 0, "canonical_max": 2},
    {"key": "thinking_budget", "value_type": "integer", "canonical_min": -1},
]

# A Groq-shaped chat api, as ai.api.rules carries it today.
API_PARAMS: dict[str, dict[str, Any]] = {
    "reasoning_effort": {
        "value_map": {"none": "none", "low": "low", "medium": "medium", "high": "high"},
        "ui_values": ["auto", "none", "low", "medium", "high"],
    },
    "max_output_tokens": {"provider_key": "max_completion_tokens", "default": 4096},
    "temperature": {"clamp": {"min": 0, "max": 2}},
    "thinking_budget": {"supported": False},
}
OFFERING_PARAMS: dict[str, dict[str, Any]] = {
    "temperature": {"clamp": {"min": 0, "max": 1}},
}

# Every K6 field, in the exact shapes CONTRACTS.md K6 freezes.
K6_FIELDS: dict[str, dict[str, Any]] = {
    "off_send": {"off": {"send": "none"}},
    "off_floor": {"off": {"floor": True}},
    "off_omit": {"off": {"omit": True, "why": "the provider has no off; unset is its off"}},
    "from_number": {
        "from_number": [
            {"lte": 1024, "to": None},
            {"lte": 5000, "to": "low"},
            {"lte": 11000, "to": "medium"},
            {"lte": None, "to": "high"},
        ]
    },
    "to_number": {"to_number": {"low": 2048, "medium": 8192, "high": 24576}},
    "accepts": {"accepts": ["none", "low", "medium", "high"]},
    "drop": {"drop": True, "why": "this model has no reasoning control"},
}

ASKS: list[dict[str, Any]] = [
    {},
    {"reasoning_effort": "high", "max_output_tokens": 999_999, "temperature": 1.7},
    {"reasoning_effort": "xhigh"},  # not mapped -> nearest
    {"reasoning_effort": "minimal", "temperature": 0.2},
    {"thinking_budget": 8000},  # supported:false
    {"max_output_tokens": 100, "verbosity": "high"},  # verbosity is foreign
]


def _rows(api_params: dict[str, Any], offering_params: dict[str, Any]) -> dict[str, Any]:
    return {
        "endpoints": [
            {
                "id": ENDPOINT_ID,
                "vendor": "groq",
                "internal_name": "groq",
                "display_name": "Groq",
            }
        ],
        "apis": [
            {
                "id": API_ID,
                "name": "groq_chat",
                "display_name": "Groq chat",
                "translator_key": "groq_chat",
                "rules": {"params": api_params, "constraints": []},
            }
        ],
        "offerings": [
            {
                "id": oid,
                "model_id": MODEL_ID,
                "endpoint_id": ENDPOINT_ID,
                "api_id": API_ID,
                "provider_model_id": f"qwen3.8-27b-{n}",
                "priority": n,
                "override": {"params": offering_params, "constraints": []},
            }
            for n, oid in ((1, OFFERING_ID), (2, OTHER_OFFERING_ID))
        ],
        "settings": SETTINGS,
        "models": [{"id": MODEL_ID, "name": "qwen3.8-27b", "common_name": "Qwen 3.8 27B"}],
    }


def _load(api_params: dict[str, Any], offering_params: dict[str, Any], **extra: Any) -> AiCatalogManager:
    manager = AiCatalogManager()
    manager.load_from_rows(**_rows(api_params, offering_params), **extra)
    return manager


def _wire(manager: AiCatalogManager, offering_id: str = OFFERING_ID) -> list[Any]:
    """Every ask's wire bytes + adjustments (legacy fields only) for one offering."""
    controls = manager.compiled_controls(API_ID, offering_id)
    out: list[Any] = []
    for ask in ASKS:
        canonical = dict(ask)
        outbound_params.drop_foreign_canonical_keys(canonical, controls)
        params, adjustments = controls.outbound(canonical)
        out.append(
            [
                json.dumps(params),  # insertion order too: these are the wire bytes
                sorted(
                    (a.key, a.action, repr(a.canonical_value), repr(a.sent_value), a.expected)
                    for a in adjustments
                ),
            ]
        )
    return out


def _with(params: dict[str, Any], key: str, extra: dict[str, Any]) -> dict[str, Any]:
    return {**params, key: {**params.get(key, {}), **extra}}


@pytest.fixture(autouse=True)
def _restore_singleton_state():
    yield
    AiCatalogManager().load_from_rows(endpoints=[], apis=[], offerings=[], settings=[])


# ── 1. K6 fields: no quarantine, no wire change ─────────────────────────────
# Since item C5 the K6 fields ACT (tests/test_catalog_rule_language_c5.py). On
# these ASKS only two of them have anything to act on: a declared drop removes
# reasoning_effort, and to_number turns the scale into a number. The rest
# (no "none" ask, no numeric effort, accepts' nearest == value_map's nearest)
# must leave the wire byte-identical.
K6_FIELDS_THAT_ACT_ON_ASKS = frozenset({"drop", "to_number"})


@pytest.mark.parametrize("field", sorted(K6_FIELDS))
@pytest.mark.parametrize("layer", ["api", "offering"])
def test_a_rule_carrying_a_k6_field_compiles_and_changes_nothing_on_the_wire(
    field: str, layer: str
) -> None:
    baseline = _wire(_load(API_PARAMS, OFFERING_PARAMS))
    baseline_export = AiCatalogManager().export_model_routing(MODEL_ID)
    assert not QUARANTINED_ROWS

    if layer == "api":
        manager = _load(_with(API_PARAMS, "reasoning_effort", K6_FIELDS[field]), OFFERING_PARAMS)
    else:
        manager = _load(API_PARAMS, _with(OFFERING_PARAMS, "reasoning_effort", K6_FIELDS[field]))

    assert not QUARANTINED_ROWS, [q.errors for q in QUARANTINED_ROWS]
    assert manager.offering(OFFERING_ID) is not None
    rule = manager.compiled_controls(API_ID, OFFERING_ID).rule_for("reasoning_effort")
    # Carried: the field survives compilation.
    for name in K6_FIELDS[field]:
        assert getattr(rule, name) is not None, name
    if field in K6_FIELDS_THAT_ACT_ON_ASKS:
        assert _wire(manager) != baseline
    else:
        assert _wire(manager) == baseline
    # And a client host still receives the same rules for rows without K6
    # fields (the reload above is the baseline catalog plus one field).
    assert set(baseline_export["control_rules"]) == set(
        manager.export_model_routing(MODEL_ID)["control_rules"]
    )


def test_rows_without_k6_fields_export_byte_identical_rules_to_client_hosts() -> None:
    manager = _load(API_PARAMS, OFFERING_PARAMS)
    exported = manager.export_model_routing(MODEL_ID)["control_rules"]
    for key, rule in exported.items():
        assert not {"off", "from_number", "to_number", "accepts", "drop", "why"} & set(rule), key
    assert exported["max_output_tokens"] == {
        "provider_key": "max_completion_tokens",
        "on_unmapped": "nearest",
        "supported": True,
        "default": 4096,
        "send_when_unset": False,
        "processor_config": {},
    }


@pytest.mark.parametrize(
    "bad",
    [
        {"drop": True},  # a declared drop must say why
        {"off": {"omit": True}},  # omit must say why
        {"off": {"send": "none", "floor": True}},  # exactly one form
        {"from_number": [{"lte": 5000, "to": "low"}, {"lte": 1024, "to": None}]},  # descending
        {"from_number": [{"lte": None, "to": "high"}, {"lte": 5000, "to": "low"}]},  # null not last
        {"off": {"sends": "none"}},  # unknown field inside off
    ],
)
def test_a_malformed_k6_field_still_quarantines(bad: dict[str, Any]) -> None:
    """The K6 shapes are validated, not waved through — a typo is a data bug."""
    manager = _load(API_PARAMS, _with(OFFERING_PARAMS, "reasoning_effort", bad))
    assert manager.offering(OFFERING_ID) is None
    assert any(q.row_id == OFFERING_ID for q in QUARANTINED_ROWS)


# ── 2. K9 provenance ────────────────────────────────────────────────────────
def _adjust(controls: Any, ask: dict[str, Any]) -> dict[str, Any]:
    _, adjustments = controls.outbound(dict(ask))
    return {a.key: a for a in adjustments}


def test_provenance_names_who_decided() -> None:
    from matrx_ai.catalog.models import CatalogSetting

    controls = compile_controls(
        {k: ControlRule.model_validate(v) for k, v in API_PARAMS.items()},
        {k: ControlRule.model_validate(v) for k, v in OFFERING_PARAMS.items()},
        settings={s["key"]: CatalogSetting.model_validate(s) for s in SETTINGS},
    ).with_output_maximum(16384)
    clamped = _adjust(controls, {"temperature": 1.7})["temperature"]
    assert (clamped.action, clamped.provenance) == ("clamped", "declared")
    dropped = _adjust(controls, {"thinking_budget": 8000})["thinking_budget"]
    assert (dropped.action, dropped.provenance) == ("dropped", "declared")
    nearest = _adjust(controls, {"reasoning_effort": "xhigh"})["reasoning_effort"]
    assert (nearest.action, nearest.sent_value, nearest.provenance) == ("mapped", "high", "computed")
    ceiling = _adjust(controls, {"max_output_tokens": 32000})["max_output_tokens"]
    assert (ceiling.action, ceiling.provenance) == ("clamped", "computed")
    # Copy mode: no cells, so no cell fields.
    assert (clamped.cell_id, clamped.layer, clamped.cell_state) == (None, None, None)


def test_a_foreign_key_drop_is_an_adjustment_and_still_silent_to_the_client() -> None:
    manager = _load(API_PARAMS, OFFERING_PARAMS)
    controls = manager.compiled_controls(API_ID, OFFERING_ID)
    canonical = {"verbosity": "high", "temperature": 0.5}
    collected: list[Any] = []
    dropped = outbound_params.drop_foreign_canonical_keys(
        canonical, controls, adjustments=collected
    )
    assert dropped == ["verbosity"] and canonical == {"temperature": 0.5}
    (adj,) = collected
    assert (adj.key, adj.action, adj.canonical_value, adj.provenance, adj.expected) == (
        "verbosity",
        "dropped",
        "high",
        "computed",
        True,
    )

    class _Config:
        model = "qwen3.8-27b"

    with (
        patch(
            "matrx_ai.catalog.canonicalize.canonical_settings_from_config",
            return_value={"verbosity": "high", "temperature": 0.5},
        ),
        patch.object(outbound_params, "send_client_warning") as warn,
    ):
        params = outbound_params.resolve_outbound_params(_Config(), controls)
    assert params == {"temperature": 0.5, "max_completion_tokens": 4096}
    warn.assert_not_called()  # C1 adds no user-visible warning; C6 owns that


# ── 3. K5 view rows -> compiled controls ────────────────────────────────────
def _cell(layer: str, owner: str, key: str, rule: dict[str, Any], n: int, offering: str = OFFERING_ID) -> dict[str, Any]:
    """One ai.offering_rules_compiled row, exactly the K5 columns."""
    return {
        "offering_id": offering,
        "setting_key": key,
        "rule": rule,
        "cell_id": f"ce11{n:04d}-0000-4000-8000-{owner[-12:]}",
        "layer": layer,
        "state": "inherited",
        "version": 1,
    }


def _inherited_copy(offering: str) -> list[dict[str, Any]]:
    """What item C3 seeds: today's per-key outcome, as cells (offering wins whole)."""
    rows: list[dict[str, Any]] = []
    merged = compile_controls(
        {k: ControlRule.model_validate(v) for k, v in API_PARAMS.items()},
        {k: ControlRule.model_validate(v) for k, v in OFFERING_PARAMS.items()},
    )
    for n, (key, rule) in enumerate(sorted(merged.rules.items())):
        layer = "offering" if key in OFFERING_PARAMS else "api"
        rows.append(
            _cell(layer, offering if layer == "offering" else API_ID, key,
                  rule.model_dump(exclude_unset=True), n, offering)
        )
    return rows


def test_an_exact_copy_in_the_view_produces_the_same_wire_as_the_columns() -> None:
    legacy = _wire(_load(API_PARAMS, OFFERING_PARAMS))
    manager = _load(API_PARAMS, OFFERING_PARAMS, rule_cells=_inherited_copy(OFFERING_ID))
    assert manager.rules_source == "view"
    assert not QUARANTINED_ROWS
    assert _wire(manager) == legacy
    # The other offering has no rows in the view -> the columns still serve it.
    assert manager.compiled_controls(API_ID, OTHER_OFFERING_ID).cells == {}
    assert _wire(manager, OTHER_OFFERING_ID) == _wire(_load(API_PARAMS, OFFERING_PARAMS), OTHER_OFFERING_ID)


def test_the_most_specific_cell_wins_whole_never_field_merged() -> None:
    rows = [
        _cell("api", API_ID, "max_output_tokens", {"provider_key": "max_completion_tokens", "default": 4096}, 1),
        _cell("profile", PROFILE_ID, "max_output_tokens", {"provider_key": "max_tokens"}, 2),
        _cell("offering", OFFERING_ID, "temperature", {"clamp": {"max": 1}}, 3),
        _cell("api", API_ID, "temperature", {"clamp": {"min": 0, "max": 2}, "provider_key": "temp"}, 4),
    ]
    chosen = select_cells_from_view(rows)[OFFERING_ID]
    controls = compile_controls_from_cells(chosen)
    # Profile beats api WHOLE: no default leaks in from the api cell.
    assert controls.rules["max_output_tokens"].provider_key == "max_tokens"
    assert controls.rules["max_output_tokens"].default is None
    # Offering beats api WHOLE: the api cell's provider_key does not merge in.
    assert controls.rules["temperature"].provider_key is None
    params, adjustments = controls.outbound({"temperature": 1.5})
    assert params == {"temperature": 1}
    (adj,) = adjustments
    assert (adj.cell_id, adj.layer, adj.cell_state, adj.provenance) == (
        rows[2]["cell_id"],
        "offering",
        "inherited",
        "declared",
    )
    assert controls.cells["max_output_tokens"].layer == "profile"


def test_two_cells_at_one_layer_for_one_key_distrust_the_view() -> None:
    rows = _inherited_copy(OFFERING_ID)
    dup = dict(rows[0], cell_id="ce11ffff-0000-4000-8000-000000000000")
    with pytest.raises(ViewRowError):
        select_cells_from_view([*rows, dup])
    manager = _load(API_PARAMS, OFFERING_PARAMS, rule_cells=[*rows, dup])
    assert manager.rules_source == "legacy_columns"
    assert _wire(manager) == _wire(_load(API_PARAMS, OFFERING_PARAMS))


def test_an_invalid_cell_rule_quarantines_its_offering_only() -> None:
    rows = [_cell("offering", OFFERING_ID, "temperature", {"clamp": {"max": 1}, "bogus": 1}, 1)]
    manager = _load(API_PARAMS, OFFERING_PARAMS, rule_cells=rows)
    assert manager.offering(OFFERING_ID) is None
    assert manager.offering(OTHER_OFFERING_ID) is not None


# ── 4. absence: cheap, loud once, never per request ─────────────────────────
@pytest.mark.asyncio
async def test_an_absent_view_is_copy_mode_and_announced_once_per_process() -> None:
    manager_mod._rules_source_announced.clear()
    with (
        patch.object(manager_mod, "get_model", side_effect=manager_mod.DBNotConfiguredError("x")),
        patch.object(manager_mod, "vcprint") as printed,
    ):
        assert await AiCatalogManager._load_rule_cells() is None
        assert await AiCatalogManager._load_rule_cells() is None
    assert printed.call_count == 1
    assert "COPY MODE" in printed.call_args.args[0]


@pytest.mark.asyncio
async def test_registered_view_rows_are_read_in_k5_shape() -> None:
    manager_mod._rules_source_announced.clear()
    row = _cell("api", API_ID, "temperature", {"clamp": {"max": 2}}, 7)

    class _Row:
        def __init__(self, data: dict[str, Any]) -> None:
            self.__dict__.update(data)

    class _Query:
        async def all(self) -> list[Any]:
            return [_Row(row)]

    class _View:
        @staticmethod
        def filter(**_: Any) -> _Query:
            return _Query()

    with (
        patch.object(manager_mod, "get_model", return_value=_View),
        patch.object(manager_mod, "vcprint"),
    ):
        assert await AiCatalogManager._load_rule_cells() == [row]


# ── 5. the rules export client hosts fetch (GET /api/ai-models, item C4a) ────
# aidream's GET /api/ai-models puts ``export_model_routing(model)["control_rules"]``
# on every model (aidream/services/ai_catalog/model_payload.py); matrx-local caches
# it and shapes params with it (host_catalog._catalog_model_controls). It must be
# the K5 cells WHEN the preferred offering has rows, and the column merge otherwise.
def test_client_hosts_receive_each_cell_rule_whole_from_the_view() -> None:
    rows = [
        _cell("api", API_ID, "max_output_tokens", {"provider_key": "max_tokens"}, 1),
        _cell("offering", OFFERING_ID, "temperature", {"clamp": {"max": 1}}, 2),
        _cell("api", API_ID, "thinking_budget", {"drop": True, "why": "no thinking budget here"}, 3),
    ]
    manager = _load(API_PARAMS, OFFERING_PARAMS, rule_cells=rows)
    assert manager.rules_source == "view"
    exported = manager.export_model_routing(MODEL_ID)
    assert exported is not None
    # Each exported rule is its cell's rule, dumped exactly as the export always dumps.
    assert exported["control_rules"] == {
        row["setting_key"]: ControlRule.model_validate(row["rule"]).model_dump(exclude_none=True)
        for row in rows
    }
    assert "default" not in exported["control_rules"]["max_output_tokens"]  # no column default leaks in
    assert exported["control_rules"]["temperature"]["clamp"] == {"max": 1}  # no api clamp min leaks in
    assert exported["control_rules"]["thinking_budget"]["drop"] is True
    # The column-only key reasoning_effort is NOT exported: the cells are the whole truth.
    # What a client host builds from it is a valid ControlRule set (K6 fields included).
    from matrx_ai.catalog.host_catalog import _catalog_model_controls

    class _Model(dict):
        name = "qwen3.8-27b"

    client = _catalog_model_controls(_Model(exported), "groq_chat")
    assert set(client.rules) == set(exported["control_rules"])
    assert client.outbound({"temperature": 1.7, "thinking_budget": 8000})[0] == {"temperature": 1}


def test_an_offering_without_view_rows_exports_the_column_merge() -> None:
    legacy = _load(API_PARAMS, OFFERING_PARAMS).export_model_routing(MODEL_ID)
    # Cells exist, but only for the NON-preferred offering.
    rows = [_cell("offering", OTHER_OFFERING_ID, "temperature", {"clamp": {"max": 1}}, 1, OTHER_OFFERING_ID)]
    manager = _load(API_PARAMS, OFFERING_PARAMS, rule_cells=rows)
    assert manager.rules_source == "view"
    assert manager.export_model_routing(MODEL_ID) == legacy
