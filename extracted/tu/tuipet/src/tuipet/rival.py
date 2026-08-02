"""The NAMED RIVAL — one recurring tamer per generation (Joel 2026-07-26:
"build the named rival too").

Home battles were matched but anonymous: every opponent a stranger, every win
a stat.  Now each generation has ONE named rival — a tamer with a pet of its
own line whose form always matches YOUR stage (it grows alongside you), who
answers every CADENCE'th home bout, and whose head-to-head record persists
until the generation ends.  Beating a stranger is a stat; beating THEM is a
story.

The rival's identity rides the pet save (pet.rival_name / rival_line), so the
feud dies with the pet and the heir meets a fresh face.  Its bout runs the
ordinary Battle engine on an ordinary species card — same stage bracket as
pick_enemy, ideal condition, no purse — so nothing about balance changes;
only the NAME on the fight does.  Rival bouts wear the arena backdrop (a
visiting tamer brings the ring with them)."""
from __future__ import annotations
import random

from . import data
from . import lines

# the tamer pool: small-world names (kai and mika already tamer names in the
# lobby's world — the rival walks the same streets).  Text only, no art.
NAMES = ["Kai", "Mika", "Rei", "Jun", "Nao", "Hiro",
         "Yuna", "Sora", "Ren", "Emi", "Taro", "Aya"]

CADENCE = 3                     # every 3rd home bout is the rival's challenge
LADDER = ["InTraining", "Rookie", "Champion", "Ultimate", "Mega"]


def _spans(line):
    """A line that can walk the ladder with us (rookie AND champion forms)."""
    stages = {r["stage"] for r in line["members"].values()}
    return "Rookie" in stages and "Champion" in stages


def ensure(pet):
    """First challenge mints the rival: a tamer name (never the player's
    own account name) and a line that is not the pet's own."""
    if pet.rival_name and pet.rival_line:
        return
    from . import persistence
    me, _pw = persistence.get_account()
    pool = [n for n in NAMES if n.lower() != (me or "").lower()] or NAMES
    pet.rival_name = random.choice(pool)
    all_lines = lines.load_lines()
    lids = sorted(lid for lid, ln in all_lines.items()
                  if lid != getattr(pet, "line_id", "") and _spans(ln))
    pet.rival_line = random.choice(lids or sorted(all_lines))


def form_for(pet):
    """The rival's pet at OUR stage — it grows alongside.  Stable per
    (line, stage): the same face every rematch, evolving when we do.  A
    line missing our bracket borrows a stage-mate, seeded so the borrowed
    face holds still too."""
    st = pet.stage if pet.stage in LADDER else "Rookie"
    ln = lines.load_lines().get(pet.rival_line) or {"members": {}}
    cands = sorted(r["num"] for r in ln["members"].values()
                   if r["stage"] == st)
    if not cands:
        cands = sorted(r["num"] for r in data.load_sprites()[0]
                       if r["stage"] == st)
    return random.Random(f"{pet.rival_line}:{st}").choice(cands)


def challenges(pet):
    """Every CADENCE'th home bout is the rival's — deterministic, no roll."""
    return pet.battles % CADENCE == CADENCE - 1


def maybe_challenge(pet):
    """The home battle's door: the rival's enemy card on its bout, else
    None (and the ordinary pick_enemy stranger answers)."""
    ensure(pet)
    if not challenges(pet):
        return None
    num = form_for(pet)
    rec = data.record_for(num)
    return {"num": num, "name": rec.get("name", "?"),
            "stage": rec.get("stage", ""),
            "attribute": rec.get("attribute", "Free"),
            "boss": False, "rival": True, "tamer": pet.rival_name}


def record_line(pet):
    """The head-to-head, one line: 'Kai · 3W-2L'."""
    return f"{pet.rival_name} · {pet.rival_wins}W-{pet.rival_losses}L"
