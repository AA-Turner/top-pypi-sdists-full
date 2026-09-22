"""A model a person is TOLD about has a name, whatever its routing status.

## The screen this closes (cold walk 17, defect C — 2026-09-21)

Run the Bench named its three arms:

    The judge: Claude Opus 5 · The best model money can buy, three ways:
    Claude Opus 5 · The cheap one: claude-sonnet-4-5

Two display names and one routing ref, at a residential electrician.

Cold walk 16's fix (``model_display_name``, 0cd0508085) was not bypassed by the
Bench — it was defeated by the catalog. ``model_display_name`` resolved through
:meth:`resolve_model_ref`, the ROUTING map, and the loader deliberately
surrenders a **deprecated** model's NAME slot there so an ``ai.model_alias``
row can redirect its traffic to the canonical model. The live row (read
2026-09-21) is:

    name="claude-sonnet-4-5"  common_name="Claude Sonnet 4.5"
    is_deprecated=true        retired_at=null

Deprecated, un-retired, un-aliased — and still exactly what the Bench's cheap
arm runs on. So routing returned the ref unchanged, no state row matched, the
server sent ``cheap_model_name: null``, and the screen's ``??`` fallback
printed the plumbing.

**Naming is not routing.** Display names are now collected for every row, by id
and by name, deprecated included; and :meth:`model_name_for_person` never
returns None and never returns a ref, so no surface has to invent a fallback.

Proven red by reverting each half.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.catalog.manager import AiCatalogManager

#: The live ids, so the fixture is this row and not a convenient one.
SONNET_45 = "4c4c1f0c-d2d8-4ca1-9f5a-033093614ae5"
OPUS_5 = "1a6229af-cb0c-488a-8fef-d669b37c908a"


def _models() -> list[dict[str, Any]]:
    """`ai.model_definition` as the loader receives it, live values."""
    return [
        {
            "id": OPUS_5,
            "name": "claude-opus-5",
            "common_name": "Claude Opus 5",
            "is_deprecated": False,
        },
        {
            "id": SONNET_45,
            "name": "claude-sonnet-4-5",
            "common_name": "Claude Sonnet 4.5",
            # 🚨 THE WHOLE DEFECT, IN ONE BOOLEAN.
            "is_deprecated": True,
        },
        # A row that genuinely has no name to give.
        {
            "id": "nameless-1",
            "name": "claude-future-1",
            "common_name": "",
            "is_deprecated": False,
        },
    ]


def _catalog(aliases: list[dict[str, Any]] | None = None) -> AiCatalogManager:
    manager = AiCatalogManager()
    manager.load_from_rows(
        endpoints=[],
        apis=[],
        offerings=[],
        settings=[],
        providers={},
        models=_models(),
        aliases=aliases or [],
        voices=[],
    )
    return manager


def test_a_deprecated_model_is_still_named_for_a_person() -> None:
    """THE HEADLINE. RED before the fix: this returned None."""
    c = _catalog()
    assert c.model_display_name("claude-sonnet-4-5") == "Claude Sonnet 4.5"
    assert c.model_display_name(SONNET_45) == "Claude Sonnet 4.5"


def test_deprecation_still_surrenders_the_ROUTING_name_slot() -> None:
    """The fix must not quietly re-route a deprecated name.

    That slot is surrendered on purpose, so a ``kind='deprecated'`` alias can
    redirect traffic to the canonical model. Naming reads its own map; routing
    is untouched.
    """
    c = _catalog(aliases=[{"id": "a1", "alias": "claude-sonnet-4-5", "model_id": OPUS_5}])
    assert c.resolve_model_ref("claude-sonnet-4-5") == OPUS_5


def test_every_bench_arm_gets_a_name() -> None:
    """The three refs the Bench actually names (`bench/service.py`)."""
    c = _catalog()
    names = [
        c.model_name_for_person("claude-opus-5"),
        c.model_name_for_person("claude-opus-5"),
        c.model_name_for_person("claude-sonnet-4-5"),
    ]
    assert names == ["Claude Opus 5", "Claude Opus 5", "Claude Sonnet 4.5"]
    assert not [n for n in names if n.startswith("claude-")]


def test_an_id_with_no_catalog_row_gets_a_plain_description() -> None:
    """Never the raw ref — that is the thing an Expert learns nothing from."""
    c = _catalog()
    for ref in ("no-such-model-anywhere", "claude-future-1", None, ""):
        said = c.model_name_for_person(ref)
        assert said == AiCatalogManager.UNNAMED_MODEL
        assert "claude" not in said
        assert said[0].islower()  # a description, not a name


def test_the_honest_lookup_still_answers_none() -> None:
    """`model_display_name` remains the one that can say "I do not know"."""
    c = _catalog()
    assert c.model_display_name("no-such-model-anywhere") is None
    assert c.model_display_name("claude-future-1") is None


def test_an_alias_is_a_name_a_person_can_be_shown() -> None:
    c = _catalog(aliases=[{"id": "a1", "alias": "opus", "model_id": OPUS_5}])
    assert c.model_display_name("opus") == "Claude Opus 5"


def test_an_unloaded_catalog_describes_rather_than_dies() -> None:
    """A screen naming a model must never die because nothing loaded yet."""
    # A singleton, so the empty state is asserted by clearing every map it
    # reads — exactly as `test_model_display_name.py` does.
    manager = AiCatalogManager()
    manager._model_state = {}
    manager._model_ids = frozenset()
    manager._model_names = {}
    manager._aliases = {}
    manager._display_names = {}
    assert manager.model_display_name("claude-opus-5") is None
    assert manager.model_name_for_person("claude-opus-5") == AiCatalogManager.UNNAMED_MODEL
