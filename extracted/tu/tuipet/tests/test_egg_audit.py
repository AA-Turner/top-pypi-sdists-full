"""EGG AUDIT — the pins (2026-07-25).

Probes over the whole egg surface: the bank (eggs.json.gz), the hatch
lifecycle, the unlock table, the three egg screens, the bank-index
migration, and the generational commit.  Three defects, fixed and pinned:

E1 (FIXED) — TOWNS SOLD THE NEVER-OWNABLE EGGS.  _sellable_eggs excluded
only the starters, so the five can_perm-FALSE lineage eggs (Kuramon,
Puttimon, Fufumon, Ryuda, Lalamon) reached town shelves (towns 0/2/5) and
town_egg_buy pushed them into persistence.egg_own -- permanent ownership
of eggs the design says are never ownable.  eggmigrate._sane_owned exists
to strip exactly these "however they snuck in": the shop was selling, for
800 bits, what the repair pass deletes.  The shelf filter and the single
buy path now both refuse.

E2 (FIXED) — AN EGG RE-ROLL PUMPED THE GENERATION.  Options->new egg on an
unhatched egg "hands off without ceremony" -- and _hatch_new treated that
hand-off as a full generational commit: five re-rolls took gen 2 to gen 7,
and the eventual hatch recorded max_gen 7, opening every gen-gated egg
(and the shop's gen-5 egg_of_destiny) with no lives lived.  A generation
is a LIFE -- snapshot_prev_gen has always refused to record an egg; the
commit now agrees: an unhatched re-roll keeps the generation.

E3 (FIXED) — THE RE-ROLL DESTROYED THE INHERITANCE.  The same commit
banked the EGG's own "care grade" (a flat 2) over the dead elder's banked
seed, and the etched Digimemory -- already taken from the bank by the
discarded shell -- died with it.  A re-pick now moves the whole estate to
the new shell: wallet, bag, trophies, DNA bank, the taken seed and the
etched memory, one chip only.
"""
from tuipet import data, eggmigrate, persistence
from tuipet import egg as egg_mod
from tuipet import lines as L
from tuipet import shop
from tuipet.pet import Pet


def _temp_eggs():
    rules = data.load_egg_unlock()
    return [i for i, r in rules.items() if not r["can_perm"]]


# ---- E1: the lineage eggs stay off the shelves --------------------------

def test_town_shelves_never_stock_a_lineage_egg():
    temp = set(_temp_eggs())
    assert temp, "the lineage rows vanished — re-audit this pin"
    for town in range(12):
        stocked = set(shop.town_egg_stock(town))
        assert not (stocked & temp), \
            f"town {town} shelves lineage eggs {sorted(stocked & temp)}"


def test_the_single_buy_path_refuses_a_lineage_egg():
    """Defense at the ONE buy door (single-source law): even a stale or
    poisoned egg index cannot buy its way into permanent ownership."""
    p = Pet(num=1455, stage="Champion")
    p.bits = 99999
    for idx in _temp_eggs():
        msg, sfx = shop.town_egg_buy(p, idx)
        assert sfx == "error", (idx, msg)
    assert p.bits == 99999, "a refused buy still took bits"
    assert not persistence.get_eggs_owned()


def test_ownable_town_eggs_still_sell():
    """The fix narrows the pool, not the market."""
    p = Pet(num=1455, stage="Champion")
    p.bits = 99999
    idx = shop.town_egg_stock(0)[0]
    msg, sfx = shop.town_egg_buy(p, idx)
    assert sfx == "reward", msg
    assert idx in persistence.get_eggs_owned()


# ---- E4: an EARNED egg reads owned everywhere, before it is banked -------
# (bug report 2026-07-27, v0.5.288: "breakdra egg in mountain shop didnt say
# owned when i own it")  auto_owned only STICKS when EggSelectPanel is built,
# so between meeting a permanent condition and next opening the carousel the
# persisted set is stale -- and the shelf, reading it raw, priced an egg the
# player had already earned.

def _earned_but_unbanked():
    """An egg whose permanent condition is met but which nothing has banked:
    Breakdra's row is `MegaKills 3`, so 3 Mega-class kills earn it."""
    rules = data.load_egg_unlock()
    idx = next(i for i, r in rules.items()
               if r["can_perm"] and not r["start"] and r.get("mega"))
    persistence.mega_kills_add(rules[idx]["mega"])
    assert idx not in persistence.get_eggs_owned(), "banked already — bad pin"
    return idx


def test_an_earned_egg_reads_owned_before_the_carousel_banks_it():
    idx = _earned_but_unbanked()
    assert idx in egg_mod.owned_now()
    # ...and the shelf that stocks it agrees
    town = next((t for t in range(30) if idx in shop.town_egg_stock(t)), None)
    assert town is not None, f"egg {idx} is stocked nowhere — re-audit this pin"
    row = next(r for r in shop.town_egg_rows(town) if r["egg_idx"] == idx)
    assert row["owned"], "the shelf priced an egg already earned"


def test_the_buy_door_refuses_an_earned_but_unbanked_egg():
    """The bits half of the same defect: it would have SOLD it."""
    idx = _earned_but_unbanked()
    p = Pet(num=1455, stage="Champion")
    p.bits = 99999
    msg, sfx = shop.town_egg_buy(p, idx)
    assert sfx == "error", msg
    assert p.bits == 99999, "sold an egg the player had already earned"


def test_reading_ownership_never_writes_the_save():
    """owned_now is a READ: a shop row must not bank eggs as a side effect
    (the egg screen is what banks them)."""
    idx = _earned_but_unbanked()
    before = persistence.get_eggs_owned()
    egg_mod.owned_now()
    shop.town_egg_rows(0)
    assert persistence.get_eggs_owned() == before
    assert idx not in persistence.get_eggs_owned()


# ---- E2/E3: the egg re-roll is a re-pick, not a generation ---------------

class _Shim:
    """Just enough app state to run the REAL _hatch_new/_grant_digimemory."""
    def __init__(self, pet):
        self.pet = pet
    def _do(self, m):
        self.msg = m
    def _open_mode(self, panel, cb):
        raise AssertionError("no mode should open on a direct pick")

def _app(pet):
    import tuipet.app as appmod
    shim = _Shim(pet)
    shim._hatch_new = appmod.TuiPetApp._hatch_new.__get__(shim)
    shim._grant_digimemory = appmod.TuiPetApp._grant_digimemory.__get__(shim)
    return shim


def _heir_egg():
    """The real heir path: a dead elder banked its seed and etched its
    memory; the gen-2 egg took both from the bank."""
    elder = Pet(num=1455, stage="Mega", attribute="Virus", generation=1)
    elder.dead = True
    persistence.bank_bonus_seed(9)
    persistence._note_put("digimemory", {"species": 1455})
    persistence.snapshot_prev_gen(elder)
    app = _app(Pet.new_egg(generation=2, egg_type=1))
    app._grant_digimemory(app.pet)
    return app


def test_an_egg_reroll_keeps_the_generation():
    app = _heir_egg()
    for _ in range(5):
        app._hatch_new(1, app.pet.generation + 1)   # action_new's exact call
    assert app.pet.generation == 2, "re-rolls pumped the generation"
    assert app.pet.stage == "Egg"


def test_an_egg_reroll_never_grades_the_egg_over_the_elders_seed():
    app = _heir_egg()
    assert app.pet.evol_bonus == 9                   # the elder's real grade
    app._hatch_new(2, app.pet.generation + 1)
    assert app.pet.evol_bonus == 9, \
        "the re-roll graded the EGG and stomped the elder's seed"


def test_an_egg_reroll_carries_the_etched_digimemory():
    app = _heir_egg()
    assert app.pet.digimemory == {"species": 1455}
    app._hatch_new(2, app.pet.generation + 1)
    assert app.pet.digimemory == {"species": 1455}, \
        "the etched memory died with the discarded shell"
    assert app.pet.inventory.get("digimemory") == 1, "one chip, exactly"


def test_an_egg_reroll_carries_the_wallet_and_bag():
    app = _heir_egg()
    app.pet.bits = 4321
    app.pet.inventory["meat"] = 3
    app._hatch_new(2, app.pet.generation + 1)
    assert app.pet.bits == 4321
    assert app.pet.inventory.get("meat") == 3


def test_a_real_death_still_advances_the_generation():
    """The guard must not blunt the true path: a dead HATCHED pet's
    hand-off is the generational commit it always was."""
    elder = Pet(num=1455, stage="Mega", attribute="Virus", generation=3)
    elder.dead = True
    app = _app(elder)
    app._hatch_new(1, elder.generation + 1)
    assert app.pet.generation == 4
    assert app.pet.stage == "Egg"


def test_a_live_retire_still_banks_the_care_seed():
    elder = Pet(num=1455, stage="Mega", attribute="Virus", generation=1)
    elder.care_mistakes = 0
    app = _app(elder)
    app._hatch_new(1, 2)
    assert app.pet.generation == 2
    assert app.pet.evol_bonus == elder.final_care_grade()


# ---- the bank: every egg hatches a line-bound Fresh ----------------------

def test_every_egg_hatches_a_line_bound_fresh():
    _, by_num = data.load_sprites()
    for i in range(egg_mod.count()):
        for t in egg_mod.hatch_targets(i):
            rec = by_num.get(t)
            assert rec is not None and rec["stage"] == "Fresh", (i, t)
            _croot, lid = L.canonical_root(t)
            assert lid is not None, f"egg {i} target {t} has no line"


def test_the_full_hatch_lifecycle_lands_in_the_line():
    p = Pet.new_egg(generation=1, egg_type=1)
    assert p.stage == "Egg" and not p.hatching
    for _ in range(70):
        p.tick(1.0)
        if p.hatching:
            break
    assert p.hatching, "the egg never started hatching"
    while not p.advance_hatch(0.1):
        pass
    assert p.stage == "Fresh" and p.line_id, (p.stage, p.line_id)


def test_the_egg_stage_is_inert():
    """No needs, no filth, no mistakes accrue inside the shell."""
    p = Pet.new_egg(egg_type=1)
    before = (p.hunger, p.strength, p.poop, p.care_mistakes, p.weight)
    for _ in range(59):
        p.tick(1.0)
    assert (p.hunger, p.strength, p.poop, p.care_mistakes, p.weight) == before


# ---- the unlock table and its screens ------------------------------------

def test_every_egg_has_a_rule_and_sane_progress_text():
    rules = data.load_egg_unlock()
    assert set(rules) == set(range(egg_mod.count()))
    prog = persistence.get_progress()
    for i in range(egg_mod.count()):
        r = egg_mod.unlock_ratio(i, prog)
        assert r is None or 0.0 <= r <= 1.0, (i, r)
        egg_mod.unlock_progress(i, prog)             # must not raise


def test_the_tournament_gate_cups_exist_in_their_seasons():
    """Dokimon gates on Summer Open #147, Hack on Fall Open #188 — the
    cups must exist in the LIVE seasonal pools or the eggs are unwinnable."""
    ts = {t["id"]: t for t in data.load_tournies()}
    rules = data.load_egg_unlock()
    for i, r in rules.items():
        tid = r.get("tourney")
        if tid is not None and tid < 900:            # town cups are separate
            assert tid in ts, f"egg {i} gates on missing cup {tid}"


def test_migration_translates_every_historical_index():
    n = egg_mod.count()
    for table in (eggmigrate._V401_FULL, eggmigrate._V402_FULL,
                  eggmigrate._V403_FULL, eggmigrate._V404_FULL):
        for old in range(len(table)):
            new = eggmigrate._migrate_egg_index(old, table)
            assert new is None or 0 <= new < n, (old, table[old], new)


def test_sane_owned_still_strips_lineage_eggs():
    assert eggmigrate._sane_owned(_temp_eggs()) == []


def test_digitama_announce_seeds_then_speaks_each_earning_once():
    """announce_new() (event-coverage sweep 2026-07-28): a pre-announce
    save seeds silently -- old earnings never flood as 'new'; a fresh
    earning announces EXACTLY once; the ledger is display bookkeeping and
    never writes eggs_owned (the carousel still banks ownership)."""
    assert persistence.eggs_announced() is None      # virgin save
    assert egg_mod.announce_new() == []              # first run: silent seed
    seeded = persistence.eggs_announced()
    assert seeded is not None                        # the ledger now exists
    idx = next(i for i in range(egg_mod.count()) if i not in seeded)
    owned_before = set(persistence.get_eggs_owned())
    persistence.egg_own(idx)                         # the earning
    names = egg_mod.announce_new()
    assert names == [egg_mod.hatch_name(idx)]        # spoken once, by name
    assert egg_mod.announce_new() == []              # never twice
    assert set(persistence.get_eggs_owned()) == owned_before | {idx}
