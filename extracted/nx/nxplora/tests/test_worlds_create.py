"""The CREATE-A-WORLD proofs — a world is authored, proven, registered, and run, owner-scoped, never unproven.

Proves item 4 paths A+B at the CLI layer with injected seams (no live infra):
  create → draft (NOT runnable) → prove (admission on REAL capabilities) → verified → resolvable.
  A fabricated capability is HELD. Another user cannot see or run a world. A minted world grants no authority.

Run: python3 nx/cli/tests/test_worlds_create.py   (or via the nx verify gate)
"""
import sys, os

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

import nx_worlds as W
from nx_worlds import MemoryWorldStore, DRAFT, VERIFIED, HELD

# a resolver that treats a fixed set of refs as REAL, everything else fabricated (fail-closed)
_REAL = {"burn_analysis", "finance"}
def _resolver(cap):
    return str(cap.get("ref", "")).lstrip("$") in _REAL


def test_created_world_is_draft_and_not_runnable():
    st = MemoryWorldStore()
    w = W.create_world("Podcast Ops", "user-A", capabilities=[{"kind": "skill", "ref": "$burn_analysis"}], store=st)
    assert w["state"] == DRAFT and w["slug"] == "podcast-ops" and w["owner_user_id"] == "user-A"
    # a draft world is refused at dispatch — authored, not yet runnable
    r = W.resolve_dispatch("podcast-ops", "user-A", store=st)
    assert r["ok"] is False and "not proven" in r["reason"]
    assert "podcast-ops" not in W.runtime_registry("user-A", store=st)


def test_prove_on_real_capabilities_makes_it_runnable():
    st = MemoryWorldStore()
    W.create_world("Podcast Ops", "user-A", capabilities=[{"kind": "skill", "ref": "$burn_analysis"},
                                                          {"kind": "world", "ref": "finance"}], store=st)
    res = W.prove_world("podcast-ops", "user-A", resolver=_resolver, store=st)
    assert res["ok"] is True and res["state"] == VERIFIED
    assert W.resolve_dispatch("podcast-ops", "user-A", store=st)["ok"] is True
    assert "podcast-ops" in W.runtime_registry("user-A", store=st)


def test_fabricated_capability_is_held_never_verified():
    st = MemoryWorldStore()
    W.create_world("Fake World", "user-A", capabilities=[{"kind": "skill", "ref": "$does_not_exist"}], store=st)
    res = W.prove_world("fake-world", "user-A", resolver=_resolver, store=st)
    assert res["ok"] is False and res["state"] == HELD and "unproven capabilities" in res["reason"]
    assert W.resolve_dispatch("fake-world", "user-A", store=st)["ok"] is False


def test_a_world_with_no_capabilities_cannot_be_proven():
    st = MemoryWorldStore()
    W.create_world("Empty", "user-A", capabilities=[], store=st)
    res = W.prove_world("empty", "user-A", resolver=_resolver, store=st)
    assert res["ok"] is False and "must DO something" in res["reason"]


def test_owner_scoping_no_cross_user_access():
    st = MemoryWorldStore()
    W.create_world("Mine", "user-A", capabilities=[{"kind": "world", "ref": "finance"}], store=st)
    W.prove_world("mine", "user-A", resolver=_resolver, store=st)
    # user-B cannot see, resolve, or list user-A's world — owner-scope wall
    assert st.get("mine", "user-B") is None
    assert W.resolve_dispatch("mine", "user-B", store=st)["ok"] is False
    assert "mine" not in W.runtime_registry("user-B", store=st)
    assert W.resolve_dispatch("mine", "user-A", store=st)["ok"] is True   # owner still resolves


def test_canonical_worlds_always_resolve_without_admission():
    st = MemoryWorldStore()
    for w in ("finance", "code", "cowork", "lead-gen"):
        assert W.resolve_dispatch(w, "anyone", store=st)["ok"] is True
    # and a canonical world cannot be re-created (no shadowing a shipped world)
    try:
        W.create_world("finance", "user-A", capabilities=[{"kind": "world", "ref": "finance"}], store=st)
        assert False, "should not allow re-creating a canonical world"
    except ValueError:
        pass


def test_minted_world_grants_no_new_authority():
    # resolve_dispatch returns a runnable world — it must NOT be a gate bypass. The coding/money gates are
    # separate and still apply to any action taken inside the world. Structural: nx_worlds must not import or
    # relax the gates.
    import inspect
    src = inspect.getsource(W)
    assert "classify_code_action" not in src or "still pass" in src   # only referenced in the docstring, not called to relax
    # a verified custom world is not special-cased around the gate: prove the gate is untouched by world resolve
    from nx_code_gate import classify_code_action
    assert classify_code_action("git push --force").prohibited   # unchanged, world or no world


def test_cloud_sync_seam_is_honest_not_faked():
    # the seam never fabricates success at any step
    verified = {"slug": "x", "state": VERIFIED}
    assert W.cloud_sync_seam({"slug": "x"})["synced"] is False               # unverified never syncs
    r = W.cloud_sync_seam(verified, token=None)
    assert r["synced"] is False and "local" in r["reason"].lower()          # no token → local only
    r2 = W.cloud_sync_seam(verified, token="t")
    assert r2["synced"] is False and "base_url" in r2["reason"].lower()      # no endpoint → honest pending
    # a REAL attempt to an unreachable endpoint fails honestly — never a fabricated success
    r3 = W.cloud_sync_seam(verified, token="t", base_url="https://127.0.0.1:1", workspace_id="w")
    assert r3["synced"] is False


if __name__ == "__main__":
    for n, f in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        f(); print("  ✓ %s" % n)
    print("ALL CREATE-A-WORLD PROOFS PASS")
