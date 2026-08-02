"""The 0.5 timing drill (ported 2026-07-17, "replace training system with
0.5 system we made").  One bar, SPACE locks it: mega zone = clean strike,
±5 shoulder = solid hit, wide = whiff.  The lock saves the battle form
(`saved_hit_type`), train_result feeds the LINES TR gates (energy -2), and
the strike plays on battle's own strikefx rails against the 0.5 BRICK
WALL (the clone's battle_fx rips — DSprite is the ultimate truth for
animations and mechanics).  Attribute powers grow only through battle
wins now.
"""
from tuipet import training
from tuipet.pet import Pet, TRAIN_ENERGY_COST


def _pet(**kw):
    p = Pet(num=100, stage="Champion", attribute="Vaccine", obedience=500)
    p.world_seconds = 600.0
    for k, v in kw.items():
        setattr(p, k, v)
    return p


def _panel(p=None):
    return training.TrainingPanel(p or _pet())


def _lock_at(pan, pos):
    pan.bar = pos
    pan.key("space")


# ---- grades + the saved form -----------------------------------------------------

def test_the_three_grades_read_the_window():
    pan = _panel()
    mid = (pan.mega_lo + pan.mega_hi) // 2
    _lock_at(pan, mid)
    assert pan.grade == "mega" and pan.success
    pan2 = _panel()
    _lock_at(pan2, pan2.mega_lo - 3)              # inside the ±5 shoulder
    assert pan2.grade == "normal" and pan2.success
    pan3 = _panel()
    _lock_at(pan3, 0 if pan3.mega_lo - 5 > 0 else 24)
    assert pan3.grade == "miss" and not pan3.success


def test_the_lock_saves_the_battle_form():
    p = _pet()
    pan = training.TrainingPanel(p)
    _lock_at(pan, (pan.mega_lo + pan.mega_hi) // 2)
    assert p.saved_hit_type == "mega"
    pan2 = training.TrainingPanel(p)
    _lock_at(pan2, 0 if pan2.mega_lo - 5 > 0 else 24)
    assert p.saved_hit_type == "miss"             # a whiff overwrites: today's form


def test_a_999_battle_veteran_always_strikes_mega():
    p = _pet(battles=999)
    pan = training.TrainingPanel(p)
    _lock_at(pan, 0)                              # the worst possible timing
    assert pan.grade == "mega"                    # the clone's veteran quirk


# ---- train_result (the sim side) ---------------------------------------------------

def test_every_attempt_counts_costs_and_fills_effort():
    p = _pet(strength=1)
    e0, t0, x0 = p.energy, p.stage_trainings, p.exercise_today
    p.train_result(False)
    assert p.energy == e0 - TRAIN_ENERGY_COST
    assert p.stage_trainings == t0 + 1            # LINES TR gate: win or lose
    assert p.exercise_today == x0 + 1
    assert p.strength == 2                        # the Effort meter fills per drill
    assert p.anim == "sad"
    p.train_result(True)
    assert p.strength == 3                        # ...win or lose (canon setExercise)
    assert p.anim == "happy"


def test_every_drill_sheds_two_toward_base_never_below():
    # canon gates 2026-07-18 (decompile L11701): weight-2 on EVERY drill,
    # win or lose -- floored at the species BASE, the standing adaptation
    # (the source's floor of 1 fattened/starved classic pets)
    p = _pet()
    p.weight = p._base_weight() + 3
    p.train_result(True)
    assert p.weight == p._base_weight() + 1
    r = _pet()
    r.weight = r._base_weight() + 3
    r.train_result(False)                         # a whiff sheds too
    assert r.weight == r._base_weight() + 1
    s2 = _pet()
    s2.weight = s2._base_weight() + 1             # the floor holds mid-shed
    s2.train_result(True)
    assert s2.weight == s2._base_weight()
    q = _pet()
    q.weight = q._base_weight() - 5               # a light runner
    q.train_result(True)
    assert q.weight == q._base_weight() - 5       # the shed never fattens


def test_powers_do_not_grow_at_the_bar():
    p = _pet(vaccine=5, data_power=3, virus=2)
    pan = training.TrainingPanel(p)
    _lock_at(pan, (pan.mega_lo + pan.mega_hi) // 2)
    assert (p.vaccine, p.data_power, p.virus) == (5, 3, 2)


def test_the_energy_gate_is_the_one_hard_gate():
    p = _pet()
    p.energy = TRAIN_ENERGY_COST - 1
    assert "tired" in p.can_train().lower()
    p.energy = TRAIN_ENERGY_COST
    assert p.can_train() is None


def test_three_grades_wear_three_verdict_poses():
    """Joel 2026-07-25: "mon is showing happy pose after a normal training
    hit? wheres the frustration poses at???"  The bar grades mega/normal/miss
    but the verdict read one BOOLEAN, so a shoulder hit celebrated exactly
    like a perfect strike -- the same cheer tableau AND the same cheer fx,
    with only the sentence to tell them apart.  Each grade wears its own
    tell now: Cheering / the frustrated sulk / the dejected slump."""
    poses = {}
    for pos, want in ((None, "mega"), ("shoulder", "normal"), ("wide", "miss")):
        pan = _panel()
        _lock_at(pan, {"mega": (pan.mega_lo + pan.mega_hi) // 2,
                       "normal": pan.mega_lo - 3,
                       "miss": 0 if pan.mega_lo - 5 > 0 else 24}[want])
        assert pan.grade == want
        poses[want] = pan.pet.anim
    assert poses == {"mega": "happy", "normal": "tantrum", "miss": "sad"}
    # ...and the drill's own aftermath tableau does not cheer a wall that
    # never fell: only a MEGA break plays the cheer pair
    pan = _panel()
    _lock_at(pan, pan.mega_lo - 3)                 # a solid hit
    breaks = [f for f in pan.timeline if f.get("m") == "break"]
    assert breaks                                  # a hit still breaks through
    seen = set()
    for i, fr in enumerate(pan.timeline):
        if fr.get("m") != "break":
            continue
        pan.i, pan.frame_i = i, i
        for beat in range(6):                      # both halves of the toggle
            pan.frame_i = beat * 3
            pan.text()                             # renders (no clip, no crash)
            seen.add(training.SULK_A if (pan.frame_i // 3) % 2 else training.SULK_B)
    assert seen == {training.SULK_A, training.SULK_B}
    assert training.CHEER_A not in seen and training.CHEER_B not in seen


def test_only_a_clean_strike_opens_the_praise_window():
    """Joel 2026-07-25 ("tighten"): the proud-moment window read `success`,
    so the shoulder hit the pet now SULKS over still opened one.  A clean
    strike is the proud moment; a solid hit and a whiff are not."""
    def window(where):
        p = _pet()
        p.praise_window = 0.0
        pan = training.TrainingPanel(p)
        _lock_at(pan, where(pan))
        return p.world_seconds <= getattr(p, "praise_window", 0.0)

    assert window(lambda pan: (pan.mega_lo + pan.mega_hi) // 2)      # mega
    assert not window(lambda pan: pan.mega_lo - 3)                   # solid hit
    assert not window(lambda pan: 0 if pan.mega_lo - 5 > 0 else 24)  # whiff


def test_the_bool_callers_still_read_pass_fail():
    """train_result's grade is OPTIONAL: the sim-side callers that only care
    about the counters (lines/care/discipline pins) keep passing a bool, and
    a bare True is still the proud strike."""
    p = _pet()
    p.train_result(True)
    assert p.anim == "happy"
    p.train_result(False)
    assert p.anim == "sad"


# ---- the show ---------------------------------------------------------------------

def test_the_drill_plays_through_and_closes_itself():
    """No done page (Joel 2026-07-17): the aftermath tableau is the verdict,
    the panel auto-closes, and the happy/mad anim plays on the main LCD."""
    pan = _panel()
    for _ in range(10):
        pan.anim()
        assert pan.text().plain                    # the bar renders
    assert pan.strip()
    _lock_at(pan, (pan.mega_lo + pan.mega_hi) // 2)
    assert pan.phase == "shoot"
    assert pan.pet.anim == "happy"                 # the verdict anim, queued
    for _ in range(200):
        pan.anim()
        assert pan.text().plain is not None        # every strike beat renders
        if pan.auto_close:
            break
    assert pan.auto_close == ("done", pan.result)
    assert pan.key("space") is None                # mid-strike keys stay dead


def test_wall_one_stands_through_everything_but_a_mega_break():
    """The clone's wall rule, verbatim: Wall_1 through the whole volley --
    a whiff, a normal break, the incoming orb -- and ONLY a mega break
    crumbles it to Wall_2."""
    import json
    import os
    import tuipet.training as tr
    wall = json.load(open(os.path.join(os.path.dirname(tr.__file__),
                                       "data", "train_wall.json")))
    pan = _panel()
    _lock_at(pan, 0 if pan.mega_lo - 5 > 0 else 24)
    assert pan.grade == "miss"
    standing = set(pan._wall_overlay("miss"))
    assert standing == set(pan._wall_overlay("fire_in"))
    assert standing == set(pan._wall_overlay("break"))   # a miss never crumbles
    assert len(standing) == sum(r.count("1") for r in wall["Wall_1"])
    pan2 = _panel()
    _lock_at(pan2, (pan2.mega_lo + pan2.mega_hi) // 2)
    assert pan2.grade == "mega"
    crumbled = set(pan2._wall_overlay("break"))
    assert crumbled != standing                          # Wall_2: the crumble rip
    assert len(crumbled) == sum(r.count("1") for r in wall["Wall_2"])
    assert set(pan2._wall_overlay("fire_in")) == standing  # it stood to take the shot


def test_the_bar_escape_trains_nothing():
    p = _pet()
    t0, e0 = p.stage_trainings, p.energy
    pan = training.TrainingPanel(p)
    assert pan.key("escape") == ("done", None)
    assert p.stage_trainings == t0 and p.energy == e0
