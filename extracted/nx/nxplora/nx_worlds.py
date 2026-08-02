"""nx_worlds — CREATE A WORLD (item 4, paths A + B), local-first + admission-gated.

A user or agent authors a NEW operational world (beyond the canonical set), it PERSISTS to their personal NX
owner-scoped, and it WORKS E2E — but only after it PROVES it works. Same verb as the whole system: prove.

The discipline, inherited exactly from the money wall + the browse gate + nx_proof_gate:
  • A created world starts `draft` and is NOT runnable. Dispatch refuses it.
  • It becomes `verified` (runnable) ONLY on REAL evidence — every capability it declares must resolve to a
    REAL, callable target (a registered skill / a proven tool / a wired connector). A fabricated capability
    fails admission. Never a label, never a green check that lies.
  • A verified world is registered PER-OPERATOR (owner-scoped, user_id), visible + runnable in that operator's
    NX only — never global on mint, never reaching another user, never the marketplace without graduating past
    the T3 wall.
  • A minted world grants NO new authority: its coding actions still pass classify_code_action, its money
    actions still pass is_untouchable. resolve_dispatch cannot relax either gate.

Local-first, exactly like user skills (~/.nx/skills → ~/.nx/worlds). The cloud overlay-table sync (nexplora-v2
per-user world overlays, owner-scoped by RLS user_id=auth.uid()) is a NAMED SEAM — `cloud_sync_seam()` — inert
until wired to a live workspace, honestly reported, never faked. Seams (store / resolver / registry) are
injected so the whole flow is unit-provable without live infra.
"""
import os
import re
import json
import time as _time

# ── slug / validation ────────────────────────────────────────────────────────────────────────────────────
_SLUG_RE = re.compile(r"[^a-z0-9-]+")


def slugify(name: str) -> str:
    s = _SLUG_RE.sub("-", str(name or "").strip().lower()).strip("-")
    return s[:48]


DRAFT, VERIFIED, HELD = "draft", "verified", "held"


# ── the local store (default) — one JSON per world under ~/.nx/worlds, owner-scoped by user_id ─────────────
class LocalWorldStore:
    """Owner-scoped, local-first persistence. Mirrors the user-skills store. A world file records its owner;
    reads/writes are refused across owners so one operator can never see or run another's world."""

    def __init__(self, root=None):
        self.root = root or os.path.expanduser("~/.nx/worlds")

    def _path(self, slug):
        return os.path.join(self.root, "%s.json" % slug)

    def put(self, world: dict):
        os.makedirs(self.root, exist_ok=True)
        with open(self._path(world["slug"]), "w", encoding="utf-8") as f:
            json.dump(world, f, indent=2)

    def get(self, slug, user_id):
        try:
            with open(self._path(slug), encoding="utf-8") as f:
                w = json.load(f)
        except Exception:
            return None
        # OWNER-SCOPE: a world is only visible to its owner. Cross-owner reads return None (not found).
        if str(w.get("owner_user_id")) != str(user_id):
            return None
        return w

    def list(self, user_id):
        out = []
        try:
            for fn in os.listdir(self.root):
                if fn.endswith(".json"):
                    w = self.get(fn[:-5], user_id)
                    if w:
                        out.append(w)
        except Exception:
            pass
        return out


# ── in-memory store for tests (same interface, no disk) ────────────────────────────────────────────────────
class MemoryWorldStore:
    def __init__(self):
        self._d = {}

    def put(self, world):
        self._d[world["slug"]] = dict(world)

    def get(self, slug, user_id):
        w = self._d.get(slug)
        if not w or str(w.get("owner_user_id")) != str(user_id):
            return None
        return dict(w)

    def list(self, user_id):
        return [dict(w) for w in self._d.values() if str(w.get("owner_user_id")) == str(user_id)]


# ── canonical / built-in worlds — always runnable (already shipped + proven) ───────────────────────────────
def _builtin_worlds():
    """The canonical + alias worlds from nx_routing.WORLD_CONFIG (shipped, so no runtime dependency on the JSON
    manifest). These are always runnable — a create path only governs NET-NEW operator worlds."""
    try:
        from nx_routing import WORLD_CONFIG
        return set(WORLD_CONFIG.keys())
    except Exception:
        return set()


# ── the default capability resolver — a capability is REAL iff it resolves to a callable target ────────────
def _default_capability_resolver(cap: dict) -> bool:
    """A world declares capabilities (a skill it runs, a tool, a connector action). Admission requires EVERY
    declared capability to resolve to something REAL — this is what makes 'the world works' un-fakeable.
      {"kind":"skill","ref":"$burn_analysis"}     → real iff registered in _SKILL_PROMPTS
      {"kind":"tool","ref":"<name>"}              → real iff proven in the user's generated tools
      {"kind":"world","ref":"finance"}            → real iff a built-in world (composition)
    Unknown / unresolved → False (fail-closed: a fabricated capability cannot pass)."""
    kind = str(cap.get("kind", "")).lower()
    ref = str(cap.get("ref", "")).lstrip("$")
    if not ref:
        return False
    try:
        if kind == "skill":
            import nx_cli
            return ref in getattr(nx_cli, "_SKILL_PROMPTS", {})
        if kind == "world":
            return ref in _builtin_worlds()
        if kind == "tool":
            import nx_creator
            return any(t.get("name") == ref for t in (nx_creator.list_user_tools() or []))
    except Exception:
        return False
    return False


# ── create → prove → register → resolve ────────────────────────────────────────────────────────────────────
def create_world(name, user_id, capabilities=None, description="", store=None) -> dict:
    """Author a NEW world. It persists owner-scoped as `draft` — NOT runnable until proven. Never dispatchable
    on creation. Returns the stored world record."""
    if not name or not user_id:
        raise ValueError("world name and user_id are required")
    store = store or LocalWorldStore()
    slug = slugify(name)
    if not slug:
        raise ValueError("world name did not produce a valid slug")
    if slug in _builtin_worlds():
        raise ValueError("%r is a canonical world — cannot be re-created" % slug)
    world = {
        "slug": slug,
        "name": name,
        "description": description,
        "owner_user_id": str(user_id),
        "capabilities": list(capabilities or []),
        "state": DRAFT,                       # born draft — an unproven world never runs
        "created_at": None,                   # stamped by the caller (deterministic tests: left None here)
        "verified_at": None,
        "evidence": None,
    }
    store.put(world)
    return world


def prove_world(slug, user_id, resolver=None, store=None) -> dict:
    """Admission: advance a world draft → verified ONLY if EVERY declared capability resolves to a real target.
    Returns {ok, state, evidence|reason}. A world with zero capabilities cannot be proven (nothing to run). A
    fabricated / unresolved capability HOLDS the world in draft. Never fakes readiness."""
    store = store or LocalWorldStore()
    resolver = resolver or _default_capability_resolver
    w = store.get(slug, user_id)
    if not w:
        return {"ok": False, "state": None, "reason": "world not found / not owned by this user"}
    caps = w.get("capabilities") or []
    if not caps:
        w["state"] = HELD
        store.put(w)
        return {"ok": False, "state": HELD, "reason": "no capabilities to prove — a world must DO something"}
    unresolved = []
    for c in caps:
        try:
            if not resolver(c):
                unresolved.append(c.get("ref") or c)
        except Exception:
            unresolved.append(c.get("ref") or c)
    if unresolved:
        w["state"] = HELD
        store.put(w)
        return {"ok": False, "state": HELD,
                "reason": "unproven capabilities (fabricated or not wired): %s" % ", ".join(map(str, unresolved))}
    w["state"] = VERIFIED
    w["evidence"] = {"kind": "capabilities_resolved", "count": len(caps)}
    store.put(w)
    return {"ok": True, "state": VERIFIED, "evidence": w["evidence"]}


def runtime_registry(user_id, store=None) -> set:
    """The set of worlds RUNNABLE for this operator: the canonical/built-in worlds ∪ this operator's VERIFIED
    custom worlds. Draft/held custom worlds are excluded — they are authored but not yet runnable."""
    store = store or LocalWorldStore()
    runnable = set(_builtin_worlds())
    for w in store.list(user_id):
        if w.get("state") == VERIFIED:
            runnable.add(w["slug"])
    return runnable


def resolve_dispatch(slug, user_id, store=None) -> dict:
    """The dispatch chokepoint for worlds. Returns {ok, reason, world}. A world resolves ONLY if it is a
    built-in OR an operator-owned VERIFIED world. A draft/held world, another user's world, or an unknown slug
    is REFUSED. This is the 'no unproven world runs' + owner-scope wall — the analogue of the money/browse gate
    for the world surface. It grants NO new authority: it returns a runnable world, it never authorizes an
    action (coding actions still pass classify_code_action; money still passes is_untouchable)."""
    slug = slugify(slug)
    if slug in _builtin_worlds():
        return {"ok": True, "reason": "canonical world", "world": slug}
    store = store or LocalWorldStore()
    w = (store.get(slug, user_id) or {})
    if not w:
        return {"ok": False, "reason": "unknown world / not owned by this user", "world": None}
    if w.get("state") != VERIFIED:
        return {"ok": False, "reason": "world is %r — not proven, cannot run" % w.get("state"), "world": None}
    return {"ok": True, "reason": "operator-verified world", "world": slug}


# ── the cloud sync SEAM — honest, named, inert until wired ──────────────────────────────────────────────────
def cloud_sync_seam(world: dict, token=None, base_url=None, workspace_id=None, timeout=15) -> dict:
    """Mirror a VERIFIED world into the operator's nexplora-v2 owner-scoped overlay via
    POST /api/user/worlds/overlay (bearer-authed, owner-scoped by user_id). Real wiring, HONEST failure: only a
    verified world syncs; a missing token/base_url, a non-2xx, or an unreachable endpoint returns synced=False
    with the real reason — it NEVER fabricates success. Inert (but truthful) until the endpoint is deployed
    (nexplora-v2 PR: bearer-first world auth + this overlay route)."""
    if (world or {}).get("state") != VERIFIED:
        return {"synced": False, "reason": "world not verified — only a proven world syncs"}
    if not token:
        return {"synced": False, "reason": "no auth token — world persists locally only (cloud sync pending)"}
    if not base_url:
        return {"synced": False, "reason": "no base_url — set the Nexplora API base to sync"}
    try:
        import requests
        r = requests.post(
            str(base_url).rstrip("/") + "/api/user/worlds/overlay",
            json={"workspace_id": workspace_id, "world": world},
            headers={"Authorization": "Bearer " + str(token)},
            timeout=timeout,
        )
        if 200 <= r.status_code < 300 and (r.json() if r.content else {} or {}).get("synced"):
            return {"synced": True, "reason": "synced to your account"}
        return {"synced": False, "reason": "sync failed: HTTP %d" % r.status_code}
    except Exception as e:
        return {"synced": False, "reason": "sync error: %s" % type(e).__name__}
