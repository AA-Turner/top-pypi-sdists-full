"""THE FIX LADDER — what the brain does with a ``missing_dependency`` load failure.

Operator design (2026-10-06, instructions/hugpy/brain/brain-established-2026-10-06):
"every current venv needs to be attempted to run with that model, if one fits
then that venv gets designated for that model, if nothing works, then the
current venv + the new pip install is the choice. if that breaks the venv or
doesn't work, then that new broken install is the one."

So, for one (model, worker):

  1. EXISTING environments — every env profile that is BUILT on that box
     (``ready`` in its /profiles report) whose frozen lock already holds every
     needed package, smallest first. Each is attributed to the model
     (``model_workers.env_profile``) and test-loaded (envprofiles.run_test: one
     minimal real call pinned to the box, an 'env-test' call_log row). The first
     that loads is DESIGNATED; a failure is reverted to the prior attribution.
  2. NEW environment — ``auto-<model>`` = the box's worker base + the packages
     (an overlay profile: the shared venv is never pip-installed into). The box
     builds it on the first load (a background pip, single lane; the load fails
     as ``profile_materializing`` meanwhile), the ladder waits for the build and
     tests again. A test that reveals ANOTHER missing package adds it and
     rebuilds, up to HUGPY_LADDER_ROUNDS (3).
  3. Nothing loads → the new (broken) environment STAYS attributed — "that new
     broken install is the one" — and the ticket stays pending for the operator.

Gate (brain.auto_gate): the ladder starts on its own only when the evaluation is
auto-eligible (Settings brain.auto_fix + the grade threshold); otherwise the
operator's ✓ approve on the Help ticket starts it. Within an auto run, a round
whose new packages a below-threshold brain INFERRED stops as ``needs-approval``.

Record: every test is a call_log row (intent 'env-test', metadata brain_ticket);
the ladder's progress is ``help_tickets.detail.ladder`` (steps, state, profile).
One ladder per worker at a time. While a ladder runs for (worker, model) the
brain's load_error listener stays out of its way.
"""
from __future__ import annotations

import logging
import os
import re
import threading
import time
from typing import Optional

logger = logging.getLogger("hugpy_core.fix_ladder")

ROUNDS = int(os.environ.get("HUGPY_LADDER_ROUNDS", "3"))
BUILD_TIMEOUT_S = float(os.environ.get("HUGPY_LADDER_BUILD_TIMEOUT_S", "1800"))
POLL_S = float(os.environ.get("HUGPY_LADDER_POLL_S", "10"))
# one test load: a model that has not answered in 10 min is a failed test, not a
# reason to hold the ladder (and every approve) for half an hour
TEST_TIMEOUT_S = float(os.environ.get("HUGPY_LADDER_TEST_TIMEOUT_S", "600"))
_NAME_RE = re.compile(r"[^A-Za-z0-9._-]+")

_lock = threading.Lock()
_active: dict = {}           # worker name -> {"ticket", "model_key", "started_at"}


# ── package names ──────────────────────────────────────────────────────────────
def norm_name(spec: str) -> str:
    """The distribution name of a requirement spec or a frozen lock line
    ('Pillow==12.0' → 'pillow', 'opencv_python>=4' → 'opencv-python')."""
    s = str(spec or "").strip()
    s = s.split(" @ ", 1)[0]
    s = re.split(r"[<>=!~;\[\s]", s, maxsplit=1)[0]
    return s.strip().lower().replace("_", "-").replace(".", "-")


def holds_all(lock: list, need) -> bool:
    """Every needed package is in ``lock`` (a frozen lock or a declared manifest;
    pip flags and index URLs in a manifest are not packages)."""
    have = {norm_name(x) for x in (lock or [])
            if isinstance(x, str) and x.strip() and not x.strip().startswith("-") and "://" not in x}
    return all(norm_name(p) in have for p in need)


def candidates(report: dict, need, tried=()) -> list:
    """The box's environments that may already fit, best first: BUILT ones whose
    frozen lock holds every needed package (tier 0, smallest lock first), then
    DECLARED-but-unbuilt ones whose manifest holds them (tier 1 — e.g. a box's
    `vision` profile that pins the right torchvision build; the box builds it on
    the test load). A profile whose build failed is not a candidate."""
    out = []
    for name, r in (report or {}).items():
        if name in tried:
            continue
        st = r.get("state")
        if st == "ready" and holds_all(r.get("lock") or [], need):
            out.append((0, len(r.get("lock") or []), name))
        elif st in ("not built", "materializing") and holds_all(r.get("packages") or [], need):
            out.append((1, len(r.get("packages") or []), name))
    return [name for _t, _n, name in sorted(out)]


def auto_profile_name(model_key: str) -> str:
    """'auto-<model>' — directory-safe (the box's slug rule), ≤ 64 chars."""
    base = _NAME_RE.sub("-", str(model_key or "model")).strip("-.").lower() or "model"
    return ("auto-" + base)[:64].rstrip("-.")


# ── state ──────────────────────────────────────────────────────────────────────
def active_for(worker: Optional[str], key: Optional[str] = None) -> Optional[int]:
    """The ticket id of the ladder running on ``worker`` (for ``key`` when given)."""
    with _lock:
        a = _active.get(worker or "")
    if a and (key is None or a.get("model_key") == key):
        return a.get("ticket")
    return None


RESUME_WAIT_S = float(os.environ.get("HUGPY_LADDER_RESUME_WAIT_S", "300"))


def recover_interrupted() -> int:
    """At core start: a ladder recorded 'running' lost its thread with the process
    that ran it (several sessions restart core). Mark it 'interrupted' and RESUME
    it once its worker has re-registered with an inventory (a box re-registers a
    few seconds after core comes back) — the run was already approved or
    auto-eligible, so it does not wait for another click."""
    from hugpy_core.help import help_store
    with help_store._db() as c:
        rows = c.execute("UPDATE help_tickets SET detail = jsonb_set(jsonb_set(detail, '{ladder,state}',"
                         " '\"interrupted\"'), '{ladder,now}', '\"core restarted — resuming when the worker"
                         " is back\"'), updated = %s WHERE detail->'ladder'->>'state' = 'running'"
                         " RETURNING id, worker_name, model_key, detail", (time.time(),)).fetchall()
    for r in rows:
        lad = (r.get("detail") or {}).get("ladder") or {}
        need = sorted(set(lad.get("need") or []) | set(((r.get("detail") or {}).get("evaluation") or {}).get("packages") or []))
        threading.Thread(target=_resume, args=(int(r["id"]), r.get("worker_name"), r.get("model_key"), need,
                                                str(lad.get("by") or "operator")),
                         name=f"fix-ladder-resume-{r['id']}", daemon=True).start()
    if rows:
        logger.info("fix ladder: interrupted by a restart, resuming: tickets %s", [r["id"] for r in rows])
    return len(rows)


def _resume(ticket_id: int, worker: str, key: str, need: list, by: str) -> None:
    from hugpy_core.registry import registry
    deadline = time.time() + RESUME_WAIT_S
    while time.time() < deadline:
        w = registry.lookup_worker(worker) if worker else None
        if w and registry.is_online(w) and (w.get("models_discovered") or {}):
            break
        time.sleep(5)
    time.sleep(10)                      # let the box finish its re-sync
    res = start(ticket_id, worker=worker, model_key=key, packages=need,
                by=by if by.endswith("(resumed)") else f"{by} (resumed)")
    logger.info("fix ladder ticket %s resume: %s", ticket_id, res)


def _save(ticket_id: int, ladder: dict) -> None:
    from psycopg.types.json import Jsonb
    from hugpy_core.help import help_store
    with help_store._db() as c:
        c.execute("UPDATE help_tickets SET detail = jsonb_set(coalesce(detail, '{}'::jsonb), '{ladder}', %s),"
                  " updated = %s WHERE id = %s", (Jsonb(ladder), time.time(), int(ticket_id)))


def _attribution(wid: str, key: str) -> Optional[str]:
    from hugpy_core.models.modeldb import _conn
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT env_profile FROM model_workers WHERE model_key=%s AND worker_id=%s", (key, wid))
        r = cur.fetchone()
    return (r or {}).get("env_profile")


def _attribute(wid: str, key: str, name: Optional[str]) -> None:
    """model_workers.env_profile for (model, worker) — the box reads it at load
    (fitevict adapters/db.model_env_profile); the row's trigger refreshes its cache."""
    from hugpy_core.models.modeldb import _conn
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO model_workers (model_key, worker_id, env_profile) VALUES (%s,%s,%s)"
                    " ON CONFLICT (model_key, worker_id) DO UPDATE SET env_profile=EXCLUDED.env_profile,"
                    " updated_at=now()", (key, wid, name))
        conn.commit()


def _declare(name: str, base: str, packages: list) -> None:
    from psycopg.types.json import Jsonb
    from hugpy_core.models.modeldb import _conn
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO env_profiles (name, base, packages, updated_at) VALUES (%s,%s,%s,now())"
                    " ON CONFLICT (name) DO UPDATE SET base=EXCLUDED.base, packages=EXCLUDED.packages,"
                    " updated_at=now()", (name, base, Jsonb(list(packages))))
        conn.commit()


def _report(worker: dict) -> dict:
    from hugpy_core.config.envprofiles import _box_report
    return _box_report(worker)


def _wait_built(worker: dict, name: str) -> "tuple[str, Optional[str]]":
    """Until the box reports the profile ready or failed (its /profiles report;
    the box does not publish profile state to the DB, so this is the one read)."""
    deadline = time.time() + BUILD_TIMEOUT_S
    while time.time() < deadline:
        r = _report(worker).get(name) or {}
        if r.get("state") == "ready":
            return "ready", None
        if r.get("state") == "error":
            return "error", r.get("error")
        time.sleep(POLL_S)
    return "timeout", f"the box did not finish building {name!r} within {int(BUILD_TIMEOUT_S)} s"


def _try(worker: dict, key: str, name: str, ticket_id: int, note) -> dict:
    """Attribute → test-load; when the box is still building the profile, wait
    for the build and test again. {ok, error, build}."""
    from hugpy_core.config.envprofiles import run_test
    from hugpy_core.brain.brain import failure_detail
    _attribute(worker["id"], key, name)
    meta = {"brain_ticket": ticket_id, "fix_ladder": True}
    t0 = time.time()
    res = run_test(name, worker, key, extra_metadata=meta, timeout=TEST_TIMEOUT_S)
    err = res.get("error") or ""
    if not res.get("ok") and "profile_materializing" in err:
        note(f"building {name} on {worker.get('name')}")
        state, berr = _wait_built(worker, name)
        if state != "ready":
            return {"ok": False, "error": berr or state, "build": state}
        res = run_test(name, worker, key, extra_metadata=meta, timeout=TEST_TIMEOUT_S)
        err = res.get("error") or ""
    if not res.get("ok") and "profile_error" in err:
        return {"ok": False, "error": err, "build": "error"}
    if not res.get("ok"):
        # the child's own last lines (call_log load_log_tail) — the HTTP error
        # carries only its final line, which rarely names what is missing
        tail = failure_detail(worker.get("name"), key, since=t0 - 1)
        if tail and tail not in err:
            err = err + "\n" + tail
    return {"ok": bool(res.get("ok")), "error": None if res.get("ok") else err, "build": "ready"}


def _more_packages(error: str, need: set) -> "tuple[set, Optional[dict]]":
    """New packages a failed test names (rules first; the brain maps import
    names). Returns (packages not already needed, the evaluation)."""
    from hugpy_core.brain import brain
    if not error:
        return set(), None
    ev = brain.evaluate(error)
    if ev.get("class") != brain.MISSING_DEPENDENCY:
        return set(), ev
    have = {norm_name(p) for p in need}
    return {p for p in ev.get("packages") or [] if norm_name(p) not in have}, ev


def _short(text: Optional[str], n: int = 400) -> Optional[str]:
    return None if not text else str(text)[:n]


# ── the run ────────────────────────────────────────────────────────────────────
def start(ticket_id: int, *, worker: str, model_key: str, packages, by: str) -> dict:
    """Start the ladder for one ticket (background). One ladder per worker."""
    pk = [p for p in (packages or []) if isinstance(p, str) and p.strip()]
    if not (worker and model_key and pk):
        return {"started": False, "why": "need a worker, a model and at least one package"}
    with _lock:
        cur = _active.get(worker)
        if cur:
            return {"started": False, "why": f"a fix ladder is already running on {worker} "
                                             f"(ticket {cur['ticket']}, {cur['model_key']})"}
        _active[worker] = {"ticket": int(ticket_id), "model_key": model_key, "started_at": time.time()}
    threading.Thread(target=_run_safe, args=(int(ticket_id), worker, model_key, pk, by),
                     name=f"fix-ladder-{worker}", daemon=True).start()
    logger.info("fix ladder started: ticket %s, %s on %s, need %s (by %s)", ticket_id, model_key, worker, pk, by)
    return {"started": True, "worker": worker, "model_key": model_key, "packages": pk, "by": by}


def _run_safe(ticket_id: int, worker: str, key: str, packages: list, by: str) -> None:
    try:
        _run(ticket_id, worker, key, packages, by)
    except Exception as exc:  # noqa: BLE001 — a ladder crash is recorded, never raised
        logger.exception("fix ladder crashed (ticket %s)", ticket_id)
        try:
            _save(ticket_id, {"state": "failed", "by": by, "reason": f"ladder crashed: {exc}",
                              "finished_at": time.time()})
        except Exception:  # noqa: BLE001
            pass
    finally:
        with _lock:
            _active.pop(worker, None)


def _run(ticket_id: int, worker_name: str, key: str, packages: list, by: str) -> None:
    from hugpy_core.brain import brain
    from hugpy_core.help import help_store
    from hugpy_core.registry import registry
    w = registry.lookup_worker(worker_name)
    ladder = {"state": "running", "by": by, "need": sorted(packages), "started_at": time.time(),
              "steps": [], "now": None}

    def note(text: str) -> None:
        ladder["now"] = text
        _save(ticket_id, ladder)

    def step(**kw) -> None:
        kw["at"] = time.time()
        ladder["steps"].append(kw)
        ladder["now"] = None
        _save(ticket_id, ladder)

    def finish(state: str, **kw) -> None:
        ladder.update(state=state, finished_at=time.time(), now=None, **kw)
        _save(ticket_id, ladder)
        if state == "done":
            help_store.set_ticket_status(ticket_id, "acted", {"action": "fix-ladder", "by": by,
                                                              "profile": kw.get("profile"),
                                                              "how": kw.get("how")})
        logger.info("fix ladder ticket %s: %s %s", ticket_id, state, kw)

    if not w or not w.get("url"):
        return finish("failed", reason=f"worker {worker_name!r} is not registered (no URL to reach it)")
    prior = _attribution(w["id"], key)
    need = set(packages)
    note("reading the box's environments")

    # 1 — the box's environments that may already fit (recomputed after every
    # failure: a test that reveals another missing package changes the field)
    report = _report(w)
    if not report:
        step(phase="existing", ok=False, error="the box did not answer /profiles; skipping to a new environment")
    tried: list = []
    while report:
        cands = candidates(report, need, tried)
        if not cands:
            step(phase="existing", ok=False, error="no environment on this box holds "
                                                   + ", ".join(sorted(need)))
            break
        name = cands[0]
        tried.append(name)
        note(f"testing {key} in the existing environment {name}")
        res = _try(w, key, name, ticket_id, note)
        step(phase="existing", profile=name, ok=res["ok"], build=res.get("build"), error=_short(res.get("error")))
        if res["ok"]:
            return finish("done", profile=name, how=f"existing environment {name} (holds "
                                                     f"{', '.join(sorted(need))})")
        _attribute(w["id"], key, prior)          # revert: this candidate does not fit
        more, _ev = _more_packages(res.get("error") or "", need)
        if more:
            need |= more
            ladder["need"] = sorted(need)
        report = _report(w) or report

    # 2 — the box's worker base + the new pip install (an overlay profile)
    name = auto_profile_name(key)
    for rnd in range(1, ROUNDS + 1):
        pkgs = sorted(need)
        _declare(name, "worker", pkgs)
        note(f"round {rnd}: {name} = worker base + {', '.join(pkgs)}")
        res = _try(w, key, name, ticket_id, note)
        step(phase="new", round=rnd, profile=name, packages=pkgs, ok=res["ok"],
             build=res.get("build"), error=_short(res.get("error")))
        if res["ok"]:
            return finish("done", profile=name, how=f"new environment: worker base + {', '.join(pkgs)}")
        if res.get("build") in ("error", "timeout"):
            break
        more, ev = _more_packages(res.get("error") or "", need)
        if not more:
            break
        ladder["need"] = sorted(need | more)
        if by.startswith("brain-auto") and ev and ev.get("source") == "brain" and not (ev.get("auto") or {}).get("eligible"):
            # the gate: a below-threshold brain inferred the next package → the operator decides
            return finish("needs-approval", profile=name, pending_packages=sorted(more),
                          reason=(ev.get("auto") or {}).get("why"))
        need |= more

    # 3 — nothing loaded: the new (broken) install stays attributed (operator rule)
    finish("failed", profile=name, how="kept attributed: the new environment did not load",
           reason=_short((ladder["steps"][-1] if ladder["steps"] else {}).get("error")))
