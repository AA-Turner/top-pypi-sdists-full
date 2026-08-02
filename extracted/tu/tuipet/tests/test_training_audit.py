"""THE TRAINING AUDIT — the pins (2026-07-25).

Joel: "lets do a full blown training audit next."

The drill itself came through clean: it fits the box, it cannot be frozen
by mashing, its ledger is exactly what it advertises, and its timing bar
widens with care.  What the audit found was on the drill's DOOR -- and the
same root reached two more surfaces:

**THE SECOND AILMENT WAS WIRED INTO SOME DOORS AND NOT ITS SIBLINGS.**
Injury came back 2026-07-23 and was taught to `battle_condition` (a
wounded pet cannot fight).  Three places never learned it:

  1. `can_train` -- so a pet refused every bout was sent to do timed
     strike drills instead;
  2. `needs_care()` -- the trigger for the '!' icon, the alarm and the HUD
     call.  The restoration wired injury into `_alarm_urgency`, which only
     decides how LOUD an already-triggered alarm rings, so a pet that was
     ONLY hurt rang nothing and never reached the line written to name its
     cure: the alert existed and could not fire;
  3. that line itself, which sent a panicked tamer to the BAG for a
     Bandage the items refactor had moved to the free F menu two days
     later -- the identical bug v0.5.178 fixed for the pill, one line
     above it.
"""
import random

import pytest

from tuipet import grid, statusbox, strikefx
from tuipet.battlescreen import mega_window
from tuipet.pet import Pet
from tuipet.training import BAR_MAX, TrainingPanel

R, C = grid.ROWS, grid.COLS


def _pet(**kw):
    p = Pet(num=100, stage="Champion", attribute="Vaccine", obedience=500)
    p.energy, p.hunger, p.strength = p.max_energy, 4, 4
    p.weight = p._base_weight() + 6
    p.world_seconds = 600.0
    p.poop = 0
    for k, v in kw.items():
        setattr(p, k, v)
    return p


# ---- the ailment that only half the doors knew about -------------------

def test_a_hurt_pet_cannot_be_sent_to_drill_instead():
    """`battle_condition` refuses a wounded pet; this door has to agree, or
    'too hurt to fight' just means 'go train instead'."""
    p = _pet(injured=True)
    assert "Too hurt" in (p.can_train() or "")
    assert "Too hurt" in (p.battle_condition() or "")
    p.injured = False
    assert p.can_train() is None


def test_being_hurt_CALLS_for_you():
    """The trigger, not just the volume: an injury-only pet must raise the
    care call, or the alarm never rings and the HUD line never fires."""
    p = _pet(injured=True)
    assert p.needs_care() is True
    assert p.status_word() == "injured"
    p.heal_bandage()                       # the H key's cure (2026-07-26)
    assert p.needs_care() is False


def test_every_ailment_is_lethal_adjacent_and_rings_at_full_urgency():
    from tuipet.app import TuiPetApp
    for state in ("sick", "injured"):
        p = _pet(**{state: True})
        assert p.needs_care()
        assert TuiPetApp._alarm_urgency(None, p) == 3


def test_the_hurt_call_names_the_key_that_actually_cures_it():
    """v0.5.178's lesson, final application: the injury cure is the H
    hotkey (2026-07-26), so the call names H -- never the F menu (meat
    and pill only) and never the bag (no item exists)."""
    from tuipet.app import TuiPetApp
    from tuipet import shop
    from tuipet.feedscreen import ROWS_MENU
    assert "bandage" not in shop.CATALOG            # not an item at all
    assert all(k != "bandage" for k, _label in ROWS_MENU)   # not an F row
    msg = TuiPetApp._need_message(None, _pet(injured=True))
    assert "[b]H[/]" in msg and "[b]F[/]" not in msg and "bag" not in msg


# ---- the drill itself, measured ----------------------------------------

def _drive(press_every, seed=5, cap=3000):
    random.seed(seed)
    p = _pet()
    pan = TrainingPanel(p)
    for i in range(cap):
        pan.anim()
        if getattr(pan, "auto_close", None):
            return i + 1, pan
        if press_every and i % press_every == 0:
            pan.key("space")
    return cap, pan


@pytest.mark.parametrize("every", [10, 3, 1])
def test_a_mashed_drill_still_finishes(every):
    """The battle-freeze class, checked on the sibling screen: a phone tap
    must never stall the beat."""
    frames, pan = _drive(every)
    assert frames < 3000 and pan.auto_close is not None


def test_the_drill_states_fit_the_LCD():
    random.seed(3)
    p = _pet()
    pan = TrainingPanel(p)
    seen = set()
    for i in range(300):
        pan.anim()
        phase = getattr(pan, "phase", "?")
        if phase not in seen:
            seen.add(phase)
            plain = pan.text().plain.rstrip("\n")
            rows = plain.split("\n")
            assert len(rows) <= R, f"{phase}: {len(rows)} rows"
            assert max(len(r) for r in rows) <= C, f"{phase}: too wide"
            pan.strip()
        if phase == "bar" and i > 10:
            pan.key("space")
    assert {"bar", "shoot"} <= seen


def test_one_drill_costs_and_pays_exactly_what_it_advertises():
    p = _pet(strength=2)
    p.weight = p._base_weight() + 6
    e0, w0 = p.energy, p.weight
    p.train_result(True)
    assert p.energy == e0 - 2                    # the swing costs energy
    assert p.weight == w0 - 2                    # ...and sheds a little
    assert p.strength == 3                       # effort fills per drill
    assert p.stage_trainings == 1 and p.total_trainings == 1   # both clocks
    p2 = _pet(strength=2)
    p2.train_result(False)                       # a MISS still trains
    assert p2.stage_trainings == 1 and p2.strength == 3


def test_the_weight_shed_floors_at_the_species_base():
    p = _pet()
    p.weight = p._base_weight()
    for _ in range(20):
        p.train_result(True)
    assert p.weight == p._base_weight()


def test_care_widens_the_timing_window_and_the_bar_stays_winnable():
    """The mega zone is 3px at worst -- 300ms at the marker's step, the
    honest human minimum (timing rework 2026-07-23) -- and care widens it."""
    poor = _pet(hunger=1, strength=1, energy=2, battles=10, wins=1)
    rich = _pet(hunger=4, strength=4, battles=20, wins=18,
                age_seconds=6 * 86400)
    plo, phi = mega_window(poor)
    rlo, rhi = mega_window(rich)
    assert (phi - plo + 1) >= 3
    assert (rhi - rlo + 1) > (phi - plo + 1)
    # and every position on the bar grades to something sane
    for bar in range(BAR_MAX + 1):
        assert strikefx.grade_lock([bar], rlo, rhi) in ("mega", "normal",
                                                        "miss")


def test_the_drill_and_the_bout_share_one_grading_rule():
    """One source (strikefx.grade_lock + battlescreen.mega_window), so a
    tamer's practised timing means the same thing in a real fight."""
    import inspect
    from tuipet import training
    src = inspect.getsource(training)
    assert "strikefx.grade_lock" in src and "mega_window" in src


def test_the_card_paints_for_the_drill():
    p = _pet()
    pan = TrainingPanel(p)

    class _S:
        text = ""
        border_subtitle = ""

        def update(self, t):
            _S.text = t

    class _A:
        pet, mode, stats_w = p, pan, _S()

    fn = statusbox.painter_for(pan)
    assert fn is not None
    fn(_A())
    assert _A.stats_w.text
