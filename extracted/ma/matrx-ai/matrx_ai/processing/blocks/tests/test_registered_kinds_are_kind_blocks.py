"""DD-131: a fenced JSON body naming a REGISTERED, LIVE kind is a kind block.

Chair ruling, 2026-09-12. Before it, ``BLOCK_KIND_MAP`` — a hardcoded table of 19 PLATFORM
block types — was the only route to a ``metadata.__ir`` envelope, so a user-authored kind (every
kind anyone creates in the product) could never be verified server-side, and Arman's *"every
output gets saved automatically"* was unreachable for the entire class. This is the guard for
the class, exercised on ``wine_tasting``.

WHY THIS IS A GUARD AND NOT A DECORATION. It drives the PRODUCTION ``StreamBlockProcessor``
with a token stream shaped like a model's, over the REAL registry snapshot, and asserts on the
envelope the production assembler stamps. The one thing it injects is the registry snapshot
itself (via ``prime_registered_kinds`` against the live catalog, or an explicit seed when the
catalog is not wired) — because the snapshot IS the seam under test, and a test that faked the
detector or the validator would prove nothing about either.

THE RED IT WAS WRITTEN AGAINST, measured on the pre-change source: a real ``wine_tasting`` fence
produced block types ``[('text', no envelope), ('code', no envelope)]`` — a plain code block.
"""

from __future__ import annotations

import json

import pytest

from matrx_ai.processing.blocks import kind_catalog
from matrx_ai.processing.blocks.block_detector import KIND_BLOCK_TYPE, detect_json_block_type
from matrx_ai.processing.blocks.envelope import IR_ENVELOPE_KEY
from matrx_ai.processing.blocks.stream_processor import StreamBlockProcessor

WINE = "wine_tasting"

# The live wine_tasting schema (content_ir.kind_definition, v8). Held here so the guard runs
# with or without a wired catalog; the live-catalog test below proves this copy still matches.
WINE_SCHEMA: dict = {
    "type": "object",
    "additionalProperties": False,
    "required": ["__kind", "wine_name", "vintage", "region", "rating", "would_buy_again"],
    "properties": {
        "__kind": {"const": WINE},
        "wine_name": {"type": "string"},
        "vintage": {"type": "integer"},
        "region": {"type": "string"},
        "rating": {"type": "integer", "minimum": 1, "maximum": 100},
        "notes": {"type": "string"},
        "would_buy_again": {"type": "boolean"},
    },
}

TASTING = {
    "__kind": WINE,
    "wine_name": "Guard Cabernet",
    "vintage": 2019,
    "region": "Napa Valley, USA",
    "rating": 91,
    "notes": "Driven through the real stream processor.",
    "would_buy_again": True,
}


def _fence(payload: dict) -> str:
    return "Here is your tasting.\n\n```json\n" + json.dumps(payload, indent=2) + "\n```\n"


def _run(text: str) -> list:
    """Drive the production processor with a model-shaped token stream."""
    processor = StreamBlockProcessor()
    for i in range(0, len(text), 13):
        processor.process_token(text[i : i + 13])
    processor.finalize()
    return processor.get_blocks()


@pytest.fixture
def cold_snapshot():
    kind_catalog.invalidate()
    yield
    kind_catalog.invalidate()


@pytest.fixture
def warm_snapshot(cold_snapshot):
    kind_catalog._snapshot[WINE] = (WINE_SCHEMA, 8)
    kind_catalog._known_versions[WINE] = 8
    kind_catalog._listing_seen = True
    yield


# ---------------------------------------------------------------------------
# RED — the behaviour before the ruling, which must survive for UNREGISTERED slugs
# ---------------------------------------------------------------------------


def test_an_unregistered_slug_stays_a_plain_code_block(warm_snapshot):
    """A bogus ``__kind`` must never be typed, or the detector would claim anything."""
    body = json.dumps({**TASTING, "__kind": "not_a_real_kind_at_all"}, indent=2)
    assert detect_json_block_type(body) is None

    blocks = _run(_fence({**TASTING, "__kind": "not_a_real_kind_at_all"}))
    typed = [b for b in blocks if b.type == KIND_BLOCK_TYPE]
    assert not typed, f"an unregistered slug was typed as a kind block: {[b.type for b in blocks]}"
    assert any(b.type == "code" for b in blocks), [b.type for b in blocks]
    assert all(IR_ENVELOPE_KEY not in (b.metadata or {}) for b in blocks)


def test_a_cold_snapshot_declines_rather_than_guessing(cold_snapshot):
    """Cold means "plain code block" — the safe direction, and the pre-ruling behaviour.

    A wrong envelope poisons the frontend's fingerprint-keyed cache for the whole region; a
    missing one degrades to the frontend's own parse. Declining is the cheap failure.
    """
    assert detect_json_block_type(json.dumps(TASTING, indent=2)) is None
    blocks = _run(_fence(TASTING))
    assert all(b.type != KIND_BLOCK_TYPE for b in blocks)
    assert all(IR_ENVELOPE_KEY not in (b.metadata or {}) for b in blocks)


# ---------------------------------------------------------------------------
# GREEN — a registered, live kind IS a kind block, with the same envelope
# ---------------------------------------------------------------------------


def test_a_registered_kind_is_typed_and_gets_a_verified_envelope(warm_snapshot):
    assert detect_json_block_type(json.dumps(TASTING, indent=2)) == KIND_BLOCK_TYPE

    blocks = _run(_fence(TASTING))
    kinds = [b for b in blocks if b.type == KIND_BLOCK_TYPE]
    assert len(kinds) == 1, f"expected one kind block, got {[b.type for b in blocks]}"
    block = kinds[0]

    assert block.data == TASTING, "the body is canonical JSON and must not be 'adapted'"

    envelope = (block.metadata or {}).get(IR_ENVELOPE_KEY)
    assert envelope is not None, (
        "a complete, schema-valid registered-kind block got NO __ir envelope — the whole "
        "point of the ruling"
    )
    root = envelope["root"]
    assert root["kind"] == WINE
    assert root["kindState"] == "resolved"
    assert root["status"] == "complete"
    assert root["value"]["wine_name"] == TASTING["wine_name"]
    assert root["value"]["__kind"] == WINE
    assert root["discriminator"] == {"format": "json", "key": "__kind"}
    assert envelope["fingerprint"], "the envelope must carry the FE's reuse key"


def test_a_registered_kind_whose_value_breaks_its_schema_goes_back_to_being_code(warm_snapshot):
    """Law 2: validate what you emit — and do not keep a claim you could not back.

    A rating of 900 is outside the kind's own range, so no envelope is stamped. The block must
    then stop calling itself a kind block: the client routes a kind block BY ITS ENVELOPE, and
    one with none falls through to the unregistered-type lane, which screams and renders basic
    markdown. Before this feature the same body was a `code` block and rendered as one, so an
    unverified kind block goes back to exactly that rather than regressing the render.
    """
    bad = {**TASTING, "rating": 900}
    blocks = _run(_fence(bad))
    assert not [b for b in blocks if b.type == KIND_BLOCK_TYPE], (
        "a kind block that could not be verified kept claiming to be one"
    )
    code = [b for b in blocks if b.type == "code"]
    assert len(code) == 1, [b.type for b in blocks]
    assert IR_ENVELOPE_KEY not in (code[0].metadata or {})
    assert (code[0].metadata or {}).get("language") == "json"


def test_a_version_bump_drops_the_cached_schema(warm_snapshot):
    """The chair's invalidation requirement, at the level it actually matters.

    A kind edited in the product must not be validated against the shape it used to have.
    """
    assert kind_catalog.registered_kind_schema(WINE) is WINE_SCHEMA
    kind_catalog.invalidate(WINE)
    assert kind_catalog.registered_kind_schema(WINE) is None
    assert not kind_catalog.is_registered_kind(WINE)


def test_a_directive_slug_still_routes_to_matrx_not_to_kind(warm_snapshot):
    """The reserved namespace keeps its own door — this ruling widened it, never moved it."""
    body = json.dumps({"__kind": "directive_v1_action_create_project_with_tasks", "items": []})
    assert detect_json_block_type(body) == "matrx"


# ---------------------------------------------------------------------------
# The live registry — the half a hand-copied schema cannot prove
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_the_live_registry_types_wine_tasting_and_agrees_with_this_guards_schema():
    """Against the real catalog: wine_tasting is registered, and its schema still matches.

    Skips (loudly, never silently passing) when the host has not wired the kind manager —
    that is an infra condition, not a verdict.
    """
    from aidream.package_integration import _configure_matrx_ai, _configure_matrx_runtime

    _configure_matrx_runtime()
    # wire_package_db() lives here: it is what registers content_ir's
    # kind_definition_manager into matrx-graph's DI seam.
    _configure_matrx_ai()
    kind_catalog.invalidate()
    await kind_catalog.prime_registered_kinds()

    if not kind_catalog.snapshot_is_warm():
        pytest.skip("kind catalog unreachable from this process — not a verdict on the code")

    assert kind_catalog.is_registered_kind(WINE), (
        "wine_tasting is not in the live registry snapshot, so the chat stream cannot type it"
    )
    live = kind_catalog.registered_kind_schema(WINE)
    assert live is not None, "wine_tasting is registered with no usable emitted_json_schema"
    assert set(live.get("properties") or {}) == set(WINE_SCHEMA["properties"]), (
        "the live wine_tasting schema no longer matches the copy this guard validates "
        "against — update WINE_SCHEMA and re-read what changed"
    )
    assert detect_json_block_type(json.dumps(TASTING, indent=2)) == KIND_BLOCK_TYPE
