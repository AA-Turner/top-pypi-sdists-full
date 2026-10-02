"""The NAMED RIVAL (Joel 2026-07-26: "build the named rival too") — one
recurring tamer per generation.  Pins: the mint is stable and never the
player's own name, the rival's form tracks OUR stage and holds still between
rematches, the cadence is deterministic, the tally lives in record_battle
(local bouts only), the ledger rides the pet save so the feud dies with the
generation, and the PERSON page speaks the score."""
import random

from tuipet import rival
from tuipet.pet import Pet


def _pet(stage="Rookie", battles=0):
    p = Pet(num=100, stage=stage, attribute="Vaccine")
    p.name, p.battles = "Testmon", battles
    p.line_id = ""
    return p


# ---- the mint ----------------------------------------------------------------

def test_the_mint_names_a_tamer_and_a_line():
    p = _pet()
    rival.ensure(p)
    assert p.rival_name in rival.NAMES
    assert p.rival_line
    was = (p.rival_name, p.rival_line)
    rival.ensure(p)                       # a second call never re-rolls
    assert (p.rival_name, p.rival_line) == was


def test_the_rival_is_never_the_player(monkeypatch):
    from tuipet import persistence
    monkeypatch.setattr(persistence, "get_account", lambda: ("Kai", "pw"))
    random.seed(0)
    for _ in range(30):
        p = _pet()
        rival.ensure(p)
        assert p.rival_name != "Kai"


# ---- the form ----------------------------------------------------------------

def test_the_form_tracks_our_stage_and_holds_still():
    p = _pet(stage="Rookie")
    rival.ensure(p)
    from tuipet import data
    by_num = data.load_sprites()[1]
    rk = rival.form_for(p)
    assert by_num[rk]["stage"] == "Rookie"
    assert rival.form_for(p) == rk        # the same face every rematch
    p.stage = "Champion"                  # we evolve -> so do they
    ch = rival.form_for(p)
    assert by_num[ch]["stage"] == "Champion" and ch != rk
    p.stage = "Rookie"                    # and the old face is remembered
    assert rival.form_for(p) == rk


def test_an_odd_stage_borrows_the_rookie_bracket():
    p = _pet(stage="Fresh")               # below the ladder -> Rookie's pick
    rival.ensure(p)
    from tuipet import data
    assert data.load_sprites()[1][rival.form_for(p)]["stage"] == "Rookie"


# ---- the cadence -------------------------------------------------------------

def test_every_third_bout_is_the_rivals():
    assert not rival.challenges(_pet(battles=0))
    assert not rival.challenges(_pet(battles=1))
    assert rival.challenges(_pet(battles=2))
    assert rival.challenges(_pet(battles=5))


def test_the_challenge_card_is_a_rival_card():
    p = _pet(battles=2)
    foe = rival.maybe_challenge(p)
    assert foe and foe["rival"] and foe["tamer"] == p.rival_name
    assert foe["stage"] == "Rookie" and not foe["boss"]
    assert rival.maybe_challenge(_pet(battles=0)) is None


# ---- the tally ---------------------------------------------------------------

def test_record_battle_tallies_the_feud_and_only_the_feud():
    p = _pet()
    p.energy = 20
    p.record_battle(True, enemy={"rival": True, "num": 5})
    p.record_battle(False, enemy={"rival": True, "num": 5})
    assert (p.rival_wins, p.rival_losses) == (1, 1)
    p.record_battle(True, enemy={"num": 5})            # a stranger: no tally
    assert (p.rival_wins, p.rival_losses) == (1, 1)
    p.record_battle(True, enemy={"rival": True}, online=True)   # L17: never
    assert (p.rival_wins, p.rival_losses) == (1, 1)


def test_the_feud_dies_with_the_generation():
    heir = Pet.new_egg(generation=2)
    assert heir.rival_name == "" and heir.rival_wins == 0


def test_the_ledger_rides_the_save():
    from dataclasses import asdict
    p = _pet()
    rival.ensure(p)
    p.rival_wins = 3
    d = asdict(p)
    assert d["rival_name"] == p.rival_name and d["rival_wins"] == 3


# ---- the surfacing -----------------------------------------------------------

def test_the_person_page_speaks_the_score():
    from tuipet import digicore
    p = _pet()
    rival.ensure(p)
    p.rival_wins, p.rival_losses = 3, 2
    pages = dict(digicore.build_pages(p))
    person = dict(pages["PERSON"])
    assert person["Rival"] == f"{p.rival_name} · 3W-2L"
    q = _pet()                                     # unminted: no row yet
    assert "Rival" not in dict(dict(digicore.build_pages(q))["PERSON"])


def test_a_rival_bout_renders_in_the_arena():
    from tuipet.battlescreen import BattlePanel
    p = _pet(battles=2)
    p.energy = 20
    foe = rival.maybe_challenge(p)
    pan = BattlePanel(p, enemy=foe)
    assert pan.arena                               # the visiting tamer's ring
    for _ in range(4):
        pan.anim()
        assert pan.text().plain
