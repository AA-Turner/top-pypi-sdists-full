"""JOEL'S POOP REPORT — the pins (2026-07-25).

Joel: "is th mon supposed to be pooping during sleep? is the poop
supposed to be visible during lights off? are we using the correct poop
sprites? my mons poop has sprite animations im not familiar with."

Three questions, one chain, three fixes.

P1 (FIXED, option b) — THE SPECIES SPREAD WAS NEVER COMPRESSED.  The
v0.5.258 retune tuned `POOP_INTERVAL_BASE` to four piles a game-day and
verified that against the MODAL species — but the interval is
`BASE * (poop_limit/poop_lapse) / REF_POOP_RATIO`, and the roster's lapse
runs 1 / 2 / 8 / 16.  232 species (14.5%) were left at 32-64 piles a
game-day: a pile every 22 game-minutes.  That also defeated the sleep
rule — canon holds the gauge at night and lets only a DESPERATE 2x gauge
go, which at a 22-minute interval falls well inside a 10-hour night, so
those pets went 5-6 times a night.  Joel ruled option b, "keep the
multiplier but compress its range": the canon ordering is kept, the range
squeezed to at most 2x, so the roster now spans 4.0-8.0 piles a day.

P2 (FIXED) — FILTH SHONE THROUGH THE BLACKOUT.  The lights-off branch
blanks the PET rows and passed the overlay straight through, so the piles
(flies and all) sat lit on a field that is meant to be DVPet's
fully-opaque `lightsOff` — the same cover that makes a dark-room fx "show
NOTHING".  The sick skull already reads the switch this way; the Zzz is
deliberately the one mark that survives.  The piles are unlit now, not
gone: flip the lights and they are all still there.

P3 (FIXED) — THE SIZE-4 PILE WAS DISTORTED ART.  `_poop_size()` produces
1-3, and the filth slots are built to Joel's layout law ("4 poops ==
16x16, and the mon NEVER walks over them") for exactly those: 7x7 / 8x7 /
8x8 in an 8-wide slot.  Size 4 is 10 wide.  It was reachable ONLY through
the backlog upgrade, and the renderer's safety then squashed it with
`fit_w` — a real rip distorted into a shape no device ever drew.  The
upgrade stops at 3; the size-4 rip stays in the data, unused, exactly as
arenafx already assumed.

NOT a defect (measured, and the answer to question 3): the poop IS
animated, and it is canon.  `poop_s1..s4` each carry two `animFilth`
frames that swap every 7 ticks awake / 10 asleep, and the moving pixels
are FLIES orbiting the pile.  Unfamiliar only because P1 made the piles
constant.
"""
import pytest

from tuipet import arenafx, data
from tuipet import lines as L
from tuipet.pet import DAY_LENGTH, Pet
from tuipet.petbase import (POOP_INTERVAL_BASE, POOP_SIZE_FITTING_MAX,
                            POOP_SPREAD_CAP)

PXH = arenafx.SCREEN_ROWS * 2


def _rows():
    """One REAL line member per (poop_limit, poop_lapse) row — a bare
    Pet has no bedtime, so a night measurement needs a line pet."""
    reqs = data.load_requirements()
    out = {}
    for lid, line in L.load_lines().items():
        for num in line["members"]:
            r = reqs.get(num) or {}
            key = (r.get("poop_limit", 64), r.get("poop_lapse", 1))
            out.setdefault(key, (num, lid))
    return out


def _pet(num=1455, line_id="ver1", hour=20.9, **kw):
    p = Pet(num=num, stage="Champion", attribute="Vaccine", obedience=500)
    p.line_id = line_id
    p.energy, p.hunger, p.strength = p.max_energy, 4, 4
    p.weight = p._base_weight()
    p.world_seconds = hour * 60.0
    p.evo_blocked = True
    for k, v in kw.items():
        setattr(p, k, v)
    return p


# ---- P1: the compressed spread -----------------------------------------

def test_no_species_poops_more_than_twice_the_modal_rate():
    """The whole roster, not the one species the retune was checked on."""
    reqs = data.load_requirements()
    rates = []
    for num in reqs:
        p = Pet.__new__(Pet)
        p.num = num
        rates.append(1440 / Pet._poop_interval.fget(p))
    modal = 1440 / POOP_INTERVAL_BASE
    assert min(rates) == pytest.approx(modal, abs=0.05)
    assert max(rates) <= modal * POOP_SPREAD_CAP + 0.05, \
        f"a species poops {max(rates):.1f} times a day"


def test_the_species_ordering_survives_the_squeeze():
    """Compressed, not flattened: a faster canon row is still faster."""
    seen = {}
    for (lim, lap), (num, _lid) in _rows().items():
        p = Pet.__new__(Pet)
        p.num = num
        seen[(lim, lap)] = 1440 / Pet._poop_interval.fget(p)
    ranked = sorted(seen, key=lambda k: k[1] / k[0])       # canon rate order
    rates = [seen[k] for k in ranked]
    assert rates == sorted(rates), f"the ordering broke: {seen}"
    assert len(set(round(r, 1) for r in rates)) > 1, "it was flattened"


@pytest.mark.parametrize("row", sorted(_rows()))
def test_no_species_soils_its_bed_all_night(row):
    """The sleep rule, kept for EVERY species: canon lets only a truly
    desperate gauge go at night.  Waking to a pile is authentic; waking
    to five is the bug Joel reported."""
    num, lid = _rows()[row]
    p = _pet(num=num, line_id=lid)
    if L.bedtime_minutes(p) is None:
        pytest.skip("not a bedtime form")
    nights, cur = [], None
    for _ in range(int(DAY_LENGTH * 5)):
        was = p.asleep
        p.tick(1.0)
        p.lights = not p.asleep
        if p.poop and not p.asleep:
            p.clean()
        if p.hunger <= 1 and not p.asleep:
            p.feed_meat()
        if not was and p.asleep:
            cur = 0
        if p.asleep and cur is not None:
            cur = max(cur, p.poop)
        if was and not p.asleep and cur is not None:
            nights.append(cur)
            cur = None
    assert nights, "the fixture never slept"
    assert max(nights) <= 2, f"{row} soiled the bed {max(nights)}x: {nights}"


def test_a_sleeper_still_holds_it_until_desperate():
    """The canon shape is intact: the ordinary interval does NOT fire in
    bed — only the 2x gauge does."""
    p = _pet()
    p.lights = False
    for _ in range(400):
        p.tick(1.0)
        p.lights = False
        if p.asleep:
            break
    assert p.asleep
    p.poop, p.poop_sizes, p._poop_t = 0, [], 0.0
    for _ in range(int(p._poop_interval) + 5):      # one full interval in bed
        p.tick(1.0)
        p.lights = False
    assert p.poop == 0, "a sleeper let go at the ordinary interval"


# ---- P2: the dark room --------------------------------------------------

@pytest.mark.parametrize("lights,asleep,drawn", [
    (True, False, True), (True, True, True),
    (False, False, False), (False, True, False),
])
def test_filth_is_unlit_in_the_dark(lights, asleep, drawn):
    p = _pet(poop=3, poop_sizes=[2, 3, 1], lights=lights, asleep=asleep)
    overlay = {(x, y) for x, y, *_ in
               arenafx._effect_overlay(p, 0, arenafx.SCREEN_COLS, PXH, tick=0)}
    filth = {(x, y) for x, y, *_ in arenafx._filth_pts(p, 0, px_h=PXH)}
    assert bool(overlay & filth) is drawn


def test_the_piles_are_unlit_not_gone():
    """Nothing is lost in the dark — the mess is still there to clean."""
    p = _pet(poop=3, poop_sizes=[2, 3, 1], lights=False, asleep=True)
    assert not arenafx._effect_overlay(p, 0, arenafx.SCREEN_COLS, PXH, tick=0)
    assert p.poop == 3 and p.poop_sizes == [2, 3, 1]
    p.lights = True
    assert arenafx._effect_overlay(p, 0, arenafx.SCREEN_COLS, PXH, tick=0)


def test_the_sleep_zzz_still_survives_the_blackout():
    """The ONE mark the dark room keeps (DVPet sleepLightsOff) — the fix
    must not take it with the filth."""
    p = _pet(poop=0, lights=False, asleep=True, anim="sleep")
    assert arenafx._effect_overlay(p, 0, arenafx.SCREEN_COLS, PXH, tick=0)


# ---- P3: the pile that fits --------------------------------------------

def _heavy():
    """A species whose `_poop_size()` is already 3 — the ONLY kind whose
    backlog upgrade could reach the 10-wide size-4 art.  A light pet
    passes this pin no matter what the code does."""
    for num, line in ((n, lid) for lid, ln in L.load_lines().items()
                      for n in ln["members"]):
        p = _pet(num=num, line_id=line)
        if p._poop_size() == 3:
            return p
    pytest.skip("no heavy line species")


def test_the_backlog_pile_stops_at_the_art_that_fits():
    p = _heavy()
    assert p._poop_size() == 3, "fixture must be a heavy pet or this proves nothing"
    p._do_poop(backlog=True)
    assert p.poop_sizes[-1] <= POOP_SIZE_FITTING_MAX


def test_a_heavy_pet_never_drops_a_pile_the_slot_cannot_hold():
    """The real path over five days.  Sizes are recorded AS THEY LAND —
    reading `poop_sizes` at the end proves nothing, because cleaning
    empties the list and takes the evidence with it."""
    p = _heavy()
    made, backlogs = [], []
    real = type(p)._do_poop

    def spy(self, backlog=False):
        backlogs.append(backlog)
        before = len(self.poop_sizes)
        out = real(self, backlog=backlog)
        if len(self.poop_sizes) > before:
            made.append(self.poop_sizes[-1])
        return out

    type(p)._do_poop = spy
    try:
        for _ in range(int(DAY_LENGTH * 5)):
            p.tick(1.0)
            p.lights = not p.asleep
            if p.poop >= 4 and not p.asleep:
                p.clean()
    finally:
        type(p)._do_poop = real
    assert made, "nothing pooped"
    assert any(backlogs), "no BACKLOG pile landed — this pin proves nothing"
    assert max(made) <= POOP_SIZE_FITTING_MAX, made


def test_every_pile_size_in_play_fits_its_slot_natively():
    """The layout law: 4 poops == 16x16, and no rip is ever squashed."""
    E = data.load_effects()
    for size in range(1, POOP_SIZE_FITTING_MAX + 1):
        for frame in E.get("poop_s%d" % size) or []:
            assert len(frame[0]) <= arenafx.POOP_W, \
                f"size {size} is {len(frame[0])} wide vs {arenafx.POOP_W}"


# ---- question 3: the animation is canon ---------------------------------

def test_the_filth_animation_is_the_real_two_frame_rip():
    """Joel: "sprite animations im not familiar with" — canon animFilth,
    two frames a pile, and the moving pixels are the flies."""
    E = data.load_effects()
    for size in range(1, POOP_SIZE_FITTING_MAX + 1):
        frames = E.get("poop_s%d" % size)
        assert frames and len(frames) == 2, size
        assert frames[0] != frames[1], f"size {size} does not animate"
        # the pile itself (bottom row) is identical; only the flies move
        assert frames[0][-1] == frames[1][-1], f"size {size} pile shifts"


def test_the_filth_frame_swaps_slower_while_asleep():
    """7 ticks awake / 10 asleep — canon, and pinned so a future tidy
    doesn't quietly make a sleeping pet's flies buzz at daytime speed."""
    awake = _pet(poop=1, poop_sizes=[2], asleep=False)
    asleep = _pet(poop=1, poop_sizes=[2], asleep=True)
    flips = {}
    for label, pet in (("awake", awake), ("asleep", asleep)):
        prev, n = None, 0
        for tick in range(40):
            pts = tuple(sorted((x, y) for x, y, *_ in
                               arenafx._filth_pts(pet, tick, px_h=PXH)))
            if prev is not None and pts != prev:
                n += 1
            prev = pts
        flips[label] = n
    assert flips["awake"] > flips["asleep"], flips
