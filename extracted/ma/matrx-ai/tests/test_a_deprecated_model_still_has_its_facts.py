"""A deprecated, un-aliased model still answers for its window and inputs (CGU-10 IMG7 #9, 2026-11-11).

Live: gpt-5.5's chat request recorded no ``context_window`` in ``input_fit`` while the nano rows recorded
both. The row (read 2026-11-11): ``name="gpt-5.5" context_window=1050000 is_deprecated=true``, no alias.
A deprecated row gives up its NAME slot in the routing map, so the memory-only fact readers
(``context_window``, ``reads_images``, ``wire_format_for``, ``model_maker``) found no state and answered
``None`` — the pre-flight never measured a gpt-5.5 prompt against its window, the picture estimate did
not know its inputs or its wire. Facts now read the row by its own name after routing misses; an alias
still wins (routing first). Proven red by reverting ``_model_facts`` to the routing lookup.
"""

from __future__ import annotations

from matrx_ai.catalog.manager import AiCatalogManager

GPT_55 = "ec8cf459-93d1-418a-beb2-b893fd116bf9"  # the live row
CANON = "11111111-2222-4333-8444-555555555555"


def _catalog(aliases: list[dict] | None = None) -> AiCatalogManager:
    manager = AiCatalogManager()
    manager.load_from_rows(
        endpoints=[],
        apis=[],
        offerings=[],
        settings=[],
        providers={},
        models=[
            {"id": GPT_55, "name": "gpt-5.5", "common_name": "GPT-5.5", "is_deprecated": True,
             "context_window": 1_050_000, "capabilities": {"input": ["text", "image"]}},
            {"id": CANON, "name": "gpt-5.5-canonical", "common_name": "GPT-5.5", "is_deprecated": False,
             "context_window": 400_000, "capabilities": {"input": ["text"]}},
        ],
        aliases=aliases or [],
    )
    return manager


def test_a_deprecated_unaliased_model_reads_its_own_window_and_inputs() -> None:
    catalog = _catalog()
    assert catalog.context_window("gpt-5.5") == 1_050_000
    assert catalog.reads_images("gpt-5.5") is True
    assert catalog.context_window(GPT_55) == 1_050_000


def test_an_alias_still_wins_over_the_deprecated_name() -> None:
    catalog = _catalog([{"id": "a1", "alias": "gpt-5.5", "model_id": CANON}])
    assert catalog.context_window("gpt-5.5") == 400_000
    assert catalog.reads_images("gpt-5.5") is False


def test_an_unknown_name_is_still_unknown() -> None:
    assert _catalog().context_window("gpt-9-imaginary") is None


# ── CGU-10 IMG8 #9: one name, several rows — the same row every load, never dict order ─────────────
def _rows(*rows: dict) -> AiCatalogManager:
    manager = AiCatalogManager()
    manager.load_from_rows(
        endpoints=[], apis=[], offerings=[], settings=[], providers={}, models=list(rows), aliases=[]
    )
    return manager


_OLD = {"id": "b-old", "name": "gpt-x", "is_deprecated": True, "context_window": 100}
_OLDER = {"id": "a-older", "name": "gpt-x", "is_deprecated": True, "context_window": 50}
_LIVE = {"id": "z-live", "name": "gpt-x", "is_deprecated": False, "context_window": 900}


def test_two_deprecated_rows_with_one_name_pick_the_same_row_in_any_order() -> None:
    assert _rows(_OLD, _OLDER).context_window("gpt-x") == _rows(_OLDER, _OLD).context_window("gpt-x") == 50


def test_a_live_row_wins_over_a_deprecated_one_in_any_order() -> None:
    assert _rows(_OLD, _LIVE).context_window("gpt-x") == 900
    assert _rows(_LIVE, _OLD).context_window("gpt-x") == 900


def test_two_live_rows_with_one_name_route_to_the_same_row_in_any_order() -> None:
    other = dict(_LIVE, id="c-live", context_window=700)
    assert _rows(_LIVE, other).context_window("gpt-x") == _rows(other, _LIVE).context_window("gpt-x") == 700


# ── CGU-10 IMG9 #8: an alias naming a LIVE row's name is announced, and the live row keeps it ──────
def test_an_alias_colliding_with_a_live_name_is_announced_and_the_live_row_keeps_it(capsys) -> None:
    from matrx_ai.catalog import manager as manager_mod

    manager_mod._alias_collisions_announced.clear()
    other = {"id": "o-1", "name": "gpt-y", "is_deprecated": False, "context_window": 10}
    catalog = AiCatalogManager()
    catalog.load_from_rows(
        endpoints=[], apis=[], offerings=[], settings=[], providers={},
        models=[_LIVE, other], aliases=[{"id": "al", "alias": "gpt-x", "model_id": "o-1"}],
    )
    assert catalog.context_window("gpt-x") == 900, "an alias rerouted a live model's name"
    out = capsys.readouterr()
    assert "ALIAS COLLISION" in out.out + out.err and "gpt-x" in out.out + out.err, "the collision was silent"
    # Once per distinct collision, not every reload.
    catalog.load_from_rows(
        endpoints=[], apis=[], offerings=[], settings=[], providers={},
        models=[_LIVE, other], aliases=[{"id": "al", "alias": "gpt-x", "model_id": "o-1"}],
    )
    again = capsys.readouterr()
    assert "ALIAS COLLISION" not in again.out + again.err


def test_an_alias_over_a_deprecated_name_is_not_a_collision(capsys) -> None:
    from matrx_ai.catalog import manager as manager_mod

    manager_mod._alias_collisions_announced.clear()
    _catalog([{"id": "a1", "alias": "gpt-5.5", "model_id": CANON}])
    out = capsys.readouterr()
    assert "ALIAS COLLISION" not in out.out + out.err
