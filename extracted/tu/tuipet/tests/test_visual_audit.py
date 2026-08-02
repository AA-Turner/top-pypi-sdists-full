"""VISUAL AUDIT — the pins (2026-07-25).

The soak battery: every fx kind x state matrix through the REAL
advance_fx + _paint_fx + render_screen, every itemfx script, every assist
act, the full role closure (1548 species x 24 roles), the hatch crack
beat-by-beat, and the main-screen paint over every anim role x
sick/geriatric/filth/dark x (real | unknown | EMPTY-cell) pets.

One defect found, fixed, pinned:

V1 (FIXED) — THE CRASH-LOOP DEFENSE CRASHED.  `record_for` exists so a
save carrying a num this build doesn't know (data refresh, downgrade,
lobby peer on a newer roster) "wears the placeholder" instead of dying in
a relaunch loop (the .bak holds the same num — audit 2026-07-13).  But the
stand-in sheet was ONE frame (copymon), and data.ROLES indexes up to 10 —
so `_pose_rows`, the one role fetch with no index guard (paint() and
bob_frame both guard), raised IndexError on nearly every pose: the first
care fx, the sleep pose, even idle's phase 1.  The defense held for
exactly one frame.  Fixed at both levels: the placeholder sheet pads to 11
slots (same rip, every index answers), and _pose_rows falls back like its
siblings.
"""
import itertools

import pytest

from tuipet import data, itemfx, placeholder
from tuipet.anim import Roamer
from tuipet.app import SCREEN_COLS, SPRITE_W, Screen
from tuipet.pet import Pet

UNKNOWN_NUM = 99999                     # no roster record -> wears the stand-in


def _screen():
    s = type("_S", (), {})()
    for name in dir(Screen):
        if name.startswith(("paint", "_paint", "_pose", "_background",
                            "_crossfade", "_idle", "_sick", "_fx", "start_fx",
                            "advance_fx", "_food", "_fxk_")) or name in ("BG_FADE",):
            attr = getattr(Screen, name)
            setattr(s, name, attr.__get__(s) if callable(attr) else attr)
    s.fx = None
    s.frame_i = 0
    s._idle_expr = None
    s.roamer = Roamer(8.0, SCREEN_COLS, SPRITE_W)
    s.rendered = []
    s.update = lambda t, _s=s: _s.rendered.append(t)
    return s


def _pet(num=29, **kw):
    p = Pet.new_egg(egg_type=1)
    p._hatch_into_fresh()
    p.num = num
    p.anim = "idle"
    for k, v in kw.items():
        setattr(p, k, v)
    return p


# ---- V1: the stand-in answers every pose --------------------------------

def test_the_placeholder_sheet_answers_every_role_index():
    need = max(max(v) for v in data.ROLES.values())
    assert len(placeholder.FRAMES) > need, \
        f"stand-in has {len(placeholder.FRAMES)} slots, roles index up to {need}"


def test_pose_rows_survives_an_unknown_num():
    """The crash-loop scenario itself: a cross-version save's num asks for
    every pose the game can ask for."""
    s = _screen()
    p = Pet.__new__(Pet)
    p.num = UNKNOWN_NUM
    for role, phase in itertools.product(data.ROLES, (0, 1, 2)):
        rows = s._pose_rows(p, role, phase)
        assert rows, (role, phase)


def test_pose_rows_guards_a_short_sheet_even_without_the_pad(monkeypatch):
    """Defense in depth: even if a future stand-in shrinks again, the fetch
    falls back like paint() and bob_frame do instead of IndexError."""
    one = {"frames": [["1111111111111111"] ], "w": 16, "h": 1}
    monkeypatch.setattr(data, "record_for", lambda n: one)
    s = _screen()
    p = Pet.__new__(Pet)
    p.num = 1
    for role in data.ROLES:
        assert s._pose_rows(p, role, 1)


def test_role_closure_over_the_whole_roster():
    """Every species x every role x both phases resolves to renderable rows
    within the 16x16 cell -- the sweep that found V1."""
    _, by_num = data.load_sprites()
    s = _screen()
    p = Pet.__new__(Pet)
    for num in by_num:
        p.num = num
        for role in data.ROLES:
            for phase in (0, 1):
                rows = s._pose_rows(p, role, phase)
                assert rows and len(rows) <= 16, (num, role)
                assert max(len(r) for r in rows) <= 16, (num, role)


# ---- the fx soak: every kind completes and renders ----------------------

_FX = {
    "eat": dict(icon="f:1"), "cheer": {}, "jeer": {}, "clean": {},
    "spit": {}, "evolve": dict(old_num=29), "dying": {}, "dna_charge": {},
    "play": {}, "poop": dict(poop=2), "poopdance": {}, "yawn": {},
    "losing": {}, "gift": dict(icon="meat"), "inherit": {},
}


@pytest.mark.parametrize("kind", sorted(_FX))
@pytest.mark.parametrize("dark", [False, True])
def test_every_fx_kind_completes_and_renders(kind, dark):
    s = _screen()
    p = _pet(poop=3, poop_sizes=[1, 2, 3], lights=not dark)
    s.start_fx(kind, pet=p, **_FX[kind])
    guard = 0
    while s.fx is not None and guard < 400:
        s._paint_fx(p)
        s.advance_fx()
        guard += 1
    assert guard < 400, f"{kind} never ended"
    assert s.rendered, f"{kind} rendered nothing"


@pytest.mark.parametrize("script", sorted(itemfx.SCRIPTS))
def test_every_item_script_completes(script):
    s = _screen()
    p = _pet()
    s.start_fx("item", pet=p, icon="i:1", script=script)
    guard = 0
    while s.fx is not None and guard < 400:
        s._paint_fx(p)
        s.advance_fx()
        guard += 1
    assert guard < 400 and s.rendered, script


@pytest.mark.parametrize("act", ["clean", "feed", "strength", "lights"])
def test_every_assist_visit_completes(act):
    s = _screen()
    p = _pet(poop=2, poop_sizes=[2, 2], lights=True)
    s.start_fx("assist", pet=p, poop=2,
               icon="f:44" if act == "feed" else None)
    s.fx.update(act=act, sizes=[2, 2], helper=29)
    if act in ("feed", "strength"):
        s.fx.update(steps=12, chain_eat="f:44", pet_ref=p)
    guard = 0
    while s.fx is not None and guard < 400:
        s._paint_fx(p)
        s.advance_fx()
        guard += 1
    assert guard < 400 and s.rendered, act


# ---- the hatch crack and the paint soak ---------------------------------

def test_the_hatch_crack_renders_every_beat():
    s = _screen()
    egg = Pet.new_egg(egg_type=3)
    for _ in range(70):
        egg.tick(1.0)
        if egg.hatching:
            break
    assert egg.hatching
    beats = 0
    while egg.hatching:
        s.paint(egg)
        beats += 1
        if egg.advance_hatch(0.1):
            break
    s.paint(egg)                       # the first Fresh frame
    assert beats >= 28 and egg.stage == "Fresh"


@pytest.mark.parametrize("num", [29, UNKNOWN_NUM])
def test_paint_soaks_every_anim_state(num):
    """Every anim role x the body states, 24 ticks each -- including the
    stand-in-wearing pet the crash-loop defense exists for."""
    states = [dict(), dict(sick=True), dict(poop=4, poop_sizes=[1, 2, 3, 2]),
              dict(lights=False), dict(asleep=True, anim="sleep"),
              dict(age_seconds=99 * 86400.0)]
    for role, st in itertools.product(list(data.ROLES), states):
        s = _screen()
        p = _pet(num, **st)
        if "anim" not in st:
            p.anim = role
        for _ in range(24):
            s.frame_i += 1
            s.paint(p)
