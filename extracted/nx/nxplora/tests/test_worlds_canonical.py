"""The CANONICAL-WORLDS anti-drift proofs — one source of truth for worlds, CLI pinned to the manifest.

worlds.canonical.json is the single source of truth (adopted from the web WorldId union). This test makes
nx_routing.WORLD_CONFIG match it — every canonical world present at the manifest's tier, every legacy name a
coherent alias, no orphan keys. Same discipline as the pinned palette + routing; fatal in the ship gate so a
world can't be added to one product and silently drift from the other.

Run: python3 nx/cli/tests/test_worlds_canonical.py   (or via the nx verify gate)
"""
import sys, os, json

_HERE = os.path.dirname(os.path.abspath(__file__))
_CLI = os.path.dirname(_HERE)
sys.path.insert(0, _CLI)

import nx_routing as R

with open(os.path.join(_CLI, "worlds.canonical.json"), encoding="utf-8") as _f:
    _MANIFEST = json.load(_f)
CANON = _MANIFEST["canonical"]
ALIASES = _MANIFEST["aliases"]


# ── one source of truth: every canonical world is wired at the manifest's tier ────────────────────────────
def test_every_canonical_world_is_in_world_config_at_the_manifest_tier():
    for world, spec in CANON.items():
        assert world in R.WORLD_CONFIG, "canonical world %r missing from WORLD_CONFIG" % world
        got = R.WORLD_CONFIG[world]["tier"]
        assert got == spec["tier"], "%s tier drifted: manifest=%s WORLD_CONFIG=%s" % (world, spec["tier"], got)


def test_canonical_count_is_32():
    # 30 web WorldId union + code + capital. If this changes, the manifest and the web union must change together.
    assert len(CANON) == 32, "expected 32 canonical worlds, got %d" % len(CANON)


def test_world_config_is_32_canonical_plus_9_aliases_equals_41():
    # The banner says "41 worlds". Pin EXACTLY what 41 is, so the anti-drift test pins a real number, not drift:
    #   41 = 32 canonical (runnable domains) + 9 legacy aliases (ops/lead/leads/strategy/customers/crm/people/
    #   nx-1/nx-code, each resolving to a canonical). len(WORLD_CONFIG) is the banner's source.
    assert len(CANON) == 32
    assert len(ALIASES) == 9
    assert len(R.WORLD_CONFIG) == 41, "WORLD_CONFIG (the banner's 41) must be 32 canonical + 9 aliases, got %d" % len(R.WORLD_CONFIG)
    assert set(R.WORLD_CONFIG) == set(CANON) | set(ALIASES), "WORLD_CONFIG keys must be exactly canonical ∪ aliases"


# ── aliases resolve, and route COHERENTLY (an alias must route exactly like its canonical target) ─────────
def test_every_alias_targets_a_canonical_world_and_routes_like_it():
    for alias, target in ALIASES.items():
        assert target in CANON, "alias %r targets non-canonical %r" % (alias, target)
        assert alias in R.WORLD_CONFIG, "alias %r missing from WORLD_CONFIG" % alias
        # coherence: the legacy name must resolve to the SAME tier as its canonical target — no split routing.
        assert R.route(alias, "x").tier == R.route(target, "x").tier, (
            "alias %r routes to a different tier than its canonical %r" % (alias, target))


# ── no orphan drift: every WORLD_CONFIG key is either canonical or a declared alias ───────────────────────
def test_no_orphan_worlds_in_world_config():
    known = set(CANON) | set(ALIASES)
    orphans = [w for w in R.WORLD_CONFIG if w not in known]
    assert not orphans, "WORLD_CONFIG has worlds absent from the manifest (drift): %s" % orphans


# ── behavior preservation: the reconcile is additive; core lanes are unchanged ────────────────────────────
def test_core_worlds_unchanged():
    # code/devops are input-sensitive (nx_routing.py:938 — a casual turn on a code world drops to flash;
    # only ACTUAL coding stays on the code tier), so probe those two with a coding phrase like test_routing does.
    for world, probe, tier in (("cowork", "x", "flash"), ("sales", "x", "flash"), ("finance", "x", "frontier"),
                        ("code", "fix the bug", "code"), ("devops", "fix the bug", "code"), ("agents", "x", "agentic"),
                        ("research", "x", "frontier"), ("legal", "x", "frontier")):
        assert R.route(world, probe).tier == tier, world


if __name__ == "__main__":
    for n, f in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        f(); print("  ✓ %s" % n)
    print("ALL CANONICAL-WORLDS ANTI-DRIFT PROOFS PASS")
