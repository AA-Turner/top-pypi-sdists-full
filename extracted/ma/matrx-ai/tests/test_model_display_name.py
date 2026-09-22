"""A MODEL IS NAMED TO A PERSON THE WAY IT IS SOLD, NOT THE WAY IT IS ROUTED.

Sixteenth cold walk of the Masterwork pipeline (2026-09-21, defect D). The
"Run the Bench" screen — the one place in the product where a non-technical
Expert decides to spend real money — printed:

    Judge: claude-opus-5 · Frontier arms: claude-opus-5 · Cheap arm:
    claude-sonnet-4-5

Three provider routing refs, because the only thing the server had to hand was
the ref it routes on. ``ai.model_definition.common_name`` has held the readable
name the whole time ("Claude Opus 5", "Claude Sonnet 4.5" — read live from the
database on 2026-09-21), and the catalog is the one place that knows it.

So the lookup belongs to the CATALOG, not to the Bench: every surface that
names a model to a person calls ``model_display_name`` and nobody keeps a
second table of names. The one thing it must never do is invent one — an
unknown ref comes back None and the caller shows the raw ref, which is
technical but true, instead of a prettier string nobody can check.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.catalog.manager import AiCatalogManager

OPUS = "e8f3a1c2-0000-4000-8000-00000000opus"
SONNET = "e8f3a1c2-0000-4000-8000-0000000sonnet"
NAMELESS = "e8f3a1c2-0000-4000-8000-00000nameless"


@pytest.fixture(autouse=True)
def _restore_catalog():
    """🚨 `AiCatalogManager()` IS A SINGLETON — it returns the one process-wide
    instance, so a test that fills its maps has changed the catalog every other
    test in the run reads. Put back exactly what was there."""
    manager = AiCatalogManager()
    before = (
        manager._model_state,
        manager._model_ids,
        manager._model_names,
        manager._aliases,
    )
    yield
    (
        manager._model_state,
        manager._model_ids,
        manager._model_names,
        manager._aliases,
    ) = before


def catalog() -> AiCatalogManager:
    """The manager, holding the rows the Bench actually asks about, in the
    shape ``_load`` fills them with from ``ai.model_definition``."""
    manager = AiCatalogManager()
    state: dict[str, dict[str, Any]] = {
        OPUS: {"id": OPUS, "name": "claude-opus-5", "common_name": "Claude Opus 5"},
        SONNET: {
            "id": SONNET,
            "name": "claude-sonnet-4-5",
            "common_name": "Claude Sonnet 4.5",
        },
        # A real shape: a row whose common_name was never filled in.
        NAMELESS: {"id": NAMELESS, "name": "claude-future-1", "common_name": ""},
    }
    manager._model_state = state
    manager._model_ids = frozenset(state)
    manager._model_names = {row["name"]: key for key, row in state.items()}
    manager._aliases = {"opus": OPUS}
    return manager


def test_the_routing_ref_becomes_the_name_it_is_sold_under():
    """FAILS before this method existed — the Bench had nothing to call."""
    c = catalog()
    assert c.model_display_name("claude-opus-5") == "Claude Opus 5"
    assert c.model_display_name("claude-sonnet-4-5") == "Claude Sonnet 4.5"


def test_an_id_and_an_alias_resolve_the_same_way_a_name_does():
    """One routing map, one name lookup on top of it — never three."""
    c = catalog()
    assert c.model_display_name(OPUS) == "Claude Opus 5"
    assert c.model_display_name("opus") == "Claude Opus 5"


def test_it_never_invents_a_name():
    """The caller shows the raw ref for these. Technical and true beats
    readable and made up — a display name nobody can check against anything is
    the worse of the two lies."""
    c = catalog()
    assert c.model_display_name("no-such-model") is None
    assert c.model_display_name("claude-future-1") is None
    assert c.model_display_name(None) is None
    assert c.model_display_name("") is None


def test_an_unloaded_catalog_answers_none_rather_than_raising():
    """A screen that names a model must never die because the catalog has not
    loaded yet; it shows the ref and carries on."""
    manager = AiCatalogManager()
    manager._model_state = {}
    manager._model_ids = frozenset()
    manager._model_names = {}
    manager._aliases = {}
    # Naming has its own map (cold walk 17, defect C) and an unloaded catalog
    # has nothing in it either. `AiCatalogManager` is a singleton, so a test
    # that asserts the empty state clears every map it reads.
    manager._display_names = {}
    assert manager.model_display_name("claude-opus-5") is None
