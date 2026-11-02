"""THE BRAIN (operator 2026-10-06, instructions/hugpy/brain/brain-established-2026-10-06):
a brain is established in core — always present, callable, and it AUTO-EVALUATES
failures. hugpy-agent, when installed, adds features and access on top (the
agent-station TUI); without it, this is the brain that evaluates and can be called.

What it does today
------------------
* ``classify(text)`` — the failure CLASS from the loader's own words. The
  taxonomy is LIFTED from legacy hugpy_engine/serve/load_failure.py
  (LOAD_FAILURE_CLASSES) and hugpy_ops/model_audit.classify_load_error; the one
  new class signal is the pip-shaped ``missing_dependency`` ("pip install X",
  "No module named 'x'", transformers' "requires the following packages").
* ``evaluate(...)`` — classify, then INFER the fix. When the class and the
  package are literal in the error, no model is needed (``source: rules``).
  Otherwise the Agent Station keeper's standing conversation answers with a
  JSON verdict. Core still owns validation, tickets, and the auto-fix gate.
* Every evaluation lands as a help ticket (kind 'load-failure'; the console's
  Help panel lists tickets) — deduplicated per (model, worker, error) by
  ``occurrences``.
* A LISTEN thread on hugpy_wrapper 'model_rows' hears a residents row whose
  load_error changed and evaluates it — an event, never a poll.

* WHICH MODEL is the brain: the Hugpy model selected for Agent Station's
  standing keeper conversation. Its grade determines whether an inferred pip
  fix can pass the automatic gate (default coding 3/3 + logic 3/3).
* AUTO-IMPLEMENT GATE (``auto_gate``): Settings brain.auto_fix (a tick box) +
  the threshold. A pip fix read literally off the error needs only the tick; a
  fix a model inferred also needs that model to meet the threshold; otherwise
  it waits for operator approval. Every evaluation carries ``auto``.

Not yet (next step, same ruling): the venv ladder for missing_dependency (try
existing env profiles → new overlay profile → isolated → keep the failed one +
ticket), which is what ``auto`` will gate. The ticket's ``next`` says so plainly.
"""
from __future__ import annotations
from hugpy_core.imports import functions as _F

import json
import logging
import os
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional


logger = logging.getLogger("hugpy_core.brain")


SELF_BASE = _F.self_base()
BRAIN_INTENT = "brain-evaluate"
TICKET_KIND = "load-failure"

# ── taxonomy (lifted: hugpy_engine/serve/load_failure.py LOAD_FAILURE_CLASSES) ──
HARD = "hard_load_failure"
VISION_NEEDS_SLOT = "vision_needs_slot"
MISSING_DEPENDENCY = "missing_dependency"
LOAD_FAILURE_CLASSES = (HARD, "vram_fit", "engine_unavailable", "unreachable",
                        VISION_NEEDS_SLOT, MISSING_DEPENDENCY, "other")
FINAL_LOAD_CLASSES = frozenset((HARD, VISION_NEEDS_SLOT, MISSING_DEPENDENCY))
# fix kinds the brain may answer with — what the next layer acts on
FIX_KINDS = ("pip", "sizing", "repull", "config", "engine", "retry", "pull", "reroute", "unknown")
_CLASS_FIX = {MISSING_DEPENDENCY: "pip", "vram_fit": "sizing", HARD: "repull",
              VISION_NEEDS_SLOT: "engine", "engine_unavailable": "engine",
              "unreachable": "retry", "other": "unknown"}

_PIP_SPEC = r"[A-Za-z0-9][A-Za-z0-9._\-]*(?:\[[A-Za-z0-9_,\-]+\])?(?:[<>=!~]=?[A-Za-z0-9.*+!_\-]+)?"
_RE_PIP = re.compile(r"pip3? install\s+((?:-[-\w]+\s+)*(?:" + _PIP_SPEC + r")(?:\s+" + _PIP_SPEC + r")*)", re.I)
_RE_NOMOD = re.compile(r"No module named ['\"]([A-Za-z0-9_.]+)['\"]")
# importlib.metadata.PackageNotFoundError names the DISTRIBUTION (a pip name) itself,
# e.g. diffusers' quantizer check: "No package metadata was found for bitsandbytes"
_RE_PKG_META = re.compile(r"No package metadata was found for ['\"]?([A-Za-z0-9][A-Za-z0-9_.\-]*)")
_RE_TF_REQ = re.compile(r"requires the following packages that were not found in your environment:\s*([A-Za-z0-9_.\-, ]+)", re.I)
_RE_VER_REQ = re.compile(r"\b([A-Za-z][A-Za-z0-9_.\-]*)\s*(>=|==|~=)\s*([0-9][0-9A-Za-z.]*)\s+is required", re.I)
_RE_NEED = re.compile(r"needs ~?([0-9.]+)\s*GB", re.I)
# transformers' requires_backends wording: "X requires the Torchvision library but
# it was not found in your environment" — the library is named literally; its two
# display names that are not pip names are mapped (transformers' own vocabulary)
_RE_REQ_LIB = re.compile(r"requires the ([A-Za-z0-9][A-Za-z0-9_.\-]*) librar(?:y|ies) but (?:it was|they were) not found", re.I)
_LIB_PIP = {"pytorch": "torch", "pil": "pillow"}


def _packages_from_pip(cmd: str) -> list:
    return [t.strip("`'\".,;") for t in cmd.split() if t and not t.startswith("-")
            and re.fullmatch(_PIP_SPEC, t.strip("`'\".,;"))]


def classify(text: Optional[str]) -> dict:
    """{class, reason, packages (literal pip specs), modules (import names that
    still need a package name), final}. Rules first; never a model call."""
    t = str(text or "")
    low = t.lower()
    out = {"class": "other", "reason": t.strip()[:400], "packages": [], "modules": []}
    # the box's env-profile gate (fitevict _profile_launch): a declared profile that
    # is still building fails the load AS DATA — transient, not a fault; a profile
    # whose pip failed is an environment fault the fix ladder already owns
    if "profile_materializing" in low:
        out.update({"class": "engine_unavailable", "reason": "its environment profile is still building",
                    "transient": True, "final": False, "fix_kind": "retry"})
        return out
    if "profile_error" in low:
        out.update({"class": "engine_unavailable", "reason": "its environment profile failed to build",
                    "final": False, "fix_kind": "config"})
        return out
    # missing_dependency — pip shaped (new signal; the 10-06 pillow case)
    pk, mods = [], []
    for m in _RE_PIP.finditer(t):
        pk += _packages_from_pip(m.group(1))
    for m in _RE_TF_REQ.finditer(t):
        pk += [p.strip() for p in m.group(1).split(",") if p.strip()]
    for m in _RE_VER_REQ.finditer(t):
        pk.append(f"{m.group(1)}{m.group(2)}{m.group(3)}")
    for m in _RE_REQ_LIB.finditer(t):
        lib = m.group(1).lower()
        pk.append(_LIB_PIP.get(lib, lib))
    for m in _RE_PKG_META.finditer(t):
        pk.append(m.group(1))
    for m in _RE_NOMOD.finditer(t):
        mods.append(m.group(1).split(".")[0])
    if pk or mods:
        out.update({"class": MISSING_DEPENDENCY, "packages": sorted(set(pk)), "modules": sorted(set(mods)),
                    "reason": "a package the model's loader imports is not installed in its environment"})
    # lifted legacy rules (load_failure.classify_text + model_audit.classify_load_error)
    elif "hard load failure" in low or HARD in low or "check_tensor_dims" in low or "wrong shape" in low \
            or "bad magic" in low or "invalid magic" in low or "failed to read magic" in low \
            or "gguf_init_from_file" in low or "not within the file bounds" in low:
        out.update({"class": HARD, "reason": "the loader rejected the file itself"})
    elif VISION_NEEDS_SLOT in low:
        out.update({"class": VISION_NEEDS_SLOT, "reason": "a vision GGUF needs a native slot with --mmproj"})
    elif ("vram" in low and ("needs ~" in low or "won't fit" in low or "ceiling" in low)) \
            or "won't fit" in low or "loadrefusal" in low or "out of memory" in low or "cuda out of memory" in low:
        m = _RE_NEED.search(t)
        out.update({"class": "vram_fit", "reason": "does not fit the device memory"})
        if m:
            out["need_bytes"] = int(float(m.group(1)) * 1e9)
    elif "no local inference engine" in low or "localengineunavailable" in low \
            or "local serving disabled" in low or "needs dependency profile" in low \
            or "unknown transformers sub-module" in low:
        out.update({"class": "engine_unavailable", "reason": "no engine on this box can run it as configured"})
    elif "connecterror" in low or "connection refused" in low or "timed out" in low \
            or "unreachable" in low or "readtimeout" in low or "server disconnected" in low:
        out.update({"class": "unreachable", "reason": "the box or its engine did not answer"})
    out["final"] = out["class"] in FINAL_LOAD_CLASSES
    out["fix_kind"] = _CLASS_FIX.get(out["class"], "unknown")
    return out


# ── the failure's own words ───────────────────────────────────────────────────
def failure_detail(worker: Optional[str], key: Optional[str], since: Optional[float] = None) -> str:
    """The child's last log lines for the latest failed load of (worker, model):
    the front door keeps them on call_log.response_meta.load_log_tail (20 lines),
    while residents.load_error carries only the final line — which for a
    transformers ImportError is "Please note that you may need to restart your
    runtime…", not the library it needs."""
    if not worker or not key:
        return ""
    try:
        import psycopg
        from hugpy_core.calllog.calllog_db import dsn
        q = ("SELECT response_meta->'load_log_tail' FROM call_log WHERE model_name=%s AND worker=%s"
             " AND jsonb_typeof(response_meta->'load_log_tail')='array'"
             + (" AND received_at >= to_timestamp(%s)" if since else "") + " ORDER BY id DESC LIMIT 1")
        with psycopg.connect(dsn(), connect_timeout=5) as c:
            r = c.execute(q, (key, worker, since) if since else (key, worker)).fetchone()
        return "\n".join(str(x) for x in ((r or [None])[0] or []))
    except Exception as exc:  # noqa: BLE001
        logger.debug("failure_detail(%s, %s): %s", worker, key, exc)
        return ""


# ── the brain model ────────────────────────────────────────────────────────────
def policy() -> dict:
    """The Settings → Policies 'brain' block (core DB settings_policies)."""
    try:
        from hugpy_core.config.settings import read_policies
        return read_policies().get("brain") or {}
    except Exception:  # noqa: BLE001
        return {}


# ── grade-based qualification (operator 2026-10-06: "the grader should be the
# basis for this automated choice prior to a user selection"; default 3/3 in
# coding and logic). The grader's hugpy-native-v2 suite has 9 categories x 3
# tiers (easy/medium/hard); a category's DEPTH is how many of its tiers the
# model's latest verdicts passed (grader.summary). A model QUALIFIES as a brain
# when its depth meets the threshold in every listed category.
BRAIN_GROUP = "hugpy-brain"
DEFAULT_THRESHOLD = {"coding": 3, "logic": 3}


def threshold() -> dict:
    """{category: tiers that must pass} — Settings brain.threshold, else the default."""
    t = policy().get("threshold")
    return dict(t) if isinstance(t, dict) and t else dict(DEFAULT_THRESHOLD)


def _summaries() -> dict:
    from hugpy_core.grading import grader
    return {s["model_key"]: s for s in grader.summary(None, grader.SUITE)}


def qualification(model_key: Optional[str], summaries: Optional[dict] = None,
                  thr: Optional[dict] = None) -> dict:
    """{meets, depth{cat: passed tiers}, short[...], graded, passed, of} for one model."""
    from hugpy_core.grading import grader
    thr = threshold() if thr is None else thr
    s = (summaries if summaries is not None else _summaries()).get(model_key or "")
    tiers = len(grader.TIER_ORDER)
    if not s:
        return {"meets": False, "depth": {}, "graded": 0, "passed": 0, "of": None,
                "short": [f"ungraded ({c} needs {n}/{tiers})" for c, n in thr.items() if n]}
    depth = s.get("depth") or {}
    short = [f"{c} {int(depth.get(c) or 0)}/{tiers} < {n}" for c, n in thr.items()
             if int(depth.get(c) or 0) < int(n)]
    return {"meets": not short, "depth": depth, "short": short, "graded": s.get("graded"),
            "passed": s.get("passed"), "of": s.get("of")}


def qualified_models(thr: Optional[dict] = None) -> list:
    """Every graded model meeting the threshold, best first (the threshold
    categories' depth, then total passed)."""
    thr = threshold() if thr is None else thr
    sums = _summaries()
    out = [mk for mk in sums if qualification(mk, sums, thr)["meets"]]
    return sorted(out, key=lambda mk: (-sum(int((sums[mk].get("depth") or {}).get(c) or 0) for c in thr),
                                       -int(sums[mk].get("passed") or 0), mk))


def ensure_brain_group() -> dict:
    """The static hugpy-brain group exists; when it is EMPTY it is filled from
    the grades (every model meeting the threshold, best first). An operator's
    member list is never rewritten — only an empty group is filled."""
    from hugpy_core.brain import model_groups as mg
    g = mg.ensure_static(BRAIN_GROUP, name=BRAIN_GROUP, role="brain",
                         note="the models the brain runs on, in priority order")
    if g and not g.get("members"):
        thr = threshold()
        picks = qualified_models(thr)
        if picks:
            g, _errs = mg.put_group(BRAIN_GROUP, name=BRAIN_GROUP, members=picks, enabled=True,
                                    by="hugpy-brain", source="auto",
                                    note="auto-filled " + time.strftime("%Y-%m-%d %H:%M")
                                         + " from grades: " + ", ".join(f"{c} {n}/3" for c, n in thr.items()))
    return g or {}


def _servable(model_key: str) -> bool:
    """Some online worker holds the model (inventory, assignment or discovery)."""
    from hugpy_core.registry import registry
    from hugpy_core.brain.model_groups import keys_match
    for w in registry.all_workers():
        if not registry.is_online(w):
            continue
        held = set(w.get("models_local") or []) | set(w.get("models") or []) \
            | set((w.get("models_discovered") or {}).keys())
        if any(keys_match(model_key, h) for h in held):
            return True
    return False


def resolve_brain() -> dict:
    """The Agent Station keeper is the one brain conversation and model."""
    try:
        keeper = _keeper_role()
        selected = str(keeper.get("model") or "")
        if keeper.get("backend") != "hugpy" or not selected or not keeper.get("live_session_id"):
            raise RuntimeError("keeper has no live Hugpy session and model")
        model = selected.removeprefix("hugpy-fleet:")
        return {"model": model, "why": "Agent Station keeper conversation",
                "qualification": qualification(model)}
    except Exception as exc:
        return {"model": None, "why": f"keeper unavailable: {exc}", "qualification": None}


# ── the brain's conversation: a harness session (2026-10-20) or the legacy keeper ──
# The Core host's `hugpy-agent-sessions.service` (hugpy-agent serve = the
# harness session server, 127.0.0.1:9127) is the brain's home: ONE named session
# "brain", created on first use with the brain directive, answered by the fleet
# through Core's own routing — the hugpy-brain/helper the operator asked for.
# An abstract-serve-core console (the pre-2026-10-20 Agent Station keeper on
# :9125) is still understood when HUGPY_BRAIN_KEEPER_URL names one.
BRAIN_SESSION = "brain"
HARNESS_SERVICES = ("hugpy-fleet", "hugpy-harness", "hugpy-agent")
_KEEPER_DEFAULTS = ("http://127.0.0.1:9127", "http://127.0.0.1:9125")
_keeper_cache: dict = {"base": "", "kind": "", "at": 0.0}


def _state_of(base: str) -> dict:
    try:
        with urllib.request.urlopen(base + "/api/state", timeout=3) as r:
            doc = json.load(r)
        return doc if isinstance(doc, dict) else {}
    except Exception:  # noqa: BLE001 — unreachable is "no keeper here"
        return {}


def _keeper_endpoint() -> "tuple[str, str]":
    """(base, kind): kind 'harness' | 'serve-core' | ''. HUGPY_BRAIN_KEEPER_URL
    pins the base; otherwise the first default that answers /api/state wins
    (the harness session server first). Cached briefly."""
    now = time.monotonic()
    if _keeper_cache["base"] and now - _keeper_cache["at"] < 30:
        return _keeper_cache["base"], _keeper_cache["kind"]
    pinned = os.environ.get("HUGPY_BRAIN_KEEPER_URL", "").rstrip("/")
    for base in ([pinned] if pinned else list(_KEEPER_DEFAULTS)):
        doc = _state_of(base)
        kind = ("harness" if doc.get("service") in HARNESS_SERVICES and "protocol_version" in doc
                else "serve-core" if doc else "")
        if kind or pinned:
            _keeper_cache.update(base=base, kind=kind, at=now)
            return base, kind
    _keeper_cache.update(base=_KEEPER_DEFAULTS[0], kind="", at=now)
    return _KEEPER_DEFAULTS[0], ""


def _keeper_base() -> str:
    return _keeper_endpoint()[0]


def _brain_default_model() -> str:
    """The model a NEW brain session starts on: HUGPY_BRAIN_MODEL, else the
    brain group's first member, else nothing (the operator picks it in the
    console's Station tab)."""
    pinned = os.environ.get("HUGPY_BRAIN_MODEL", "").strip()
    if pinned:
        return pinned
    try:
        members = (ensure_brain_group() or {}).get("members") or []
        return str(members[0]) if members else ""
    except Exception:  # noqa: BLE001
        return ""


def _harness_json(base: str, path: str, body: Optional[dict] = None, timeout: int = 15) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base + path, data=data, method="POST" if data is not None else "GET",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        doc = json.load(r)
    return doc if isinstance(doc, dict) else {}


def _harness_brain_session(base: str) -> dict:
    """The harness session named `brain` on the session server; created with
    the brain directive and the default brain model when absent."""
    rows = _harness_json(base, "/api/sessions").get("sessions") or []
    for row in rows:
        if str(row.get("name") or "").strip().lower() == BRAIN_SESSION:
            return row
    payload = {"name": BRAIN_SESSION, "directive": _SYSTEM}
    model = _brain_default_model()
    if model:
        payload["profile"] = model
    return _harness_json(base, "/api/sessions", payload)


def _keeper_role() -> dict:
    """The brain's conversation as a roster-shaped role: {backend, model,
    live_session_id}. Harness: the `brain` session. Serve-core: the keeper role."""
    base, kind = _keeper_endpoint()
    if kind == "harness":
        row = _harness_brain_session(base)
        return {"role": "keeper", "backend": "hugpy", "model": row.get("model") or "",
                "live_session_id": row.get("id") or "", "kind": "harness"}
    with urllib.request.urlopen(base + "/api/session/roster", timeout=10) as r:
        roster = json.load(r)
    return next((role for role in roster.get("roles", []) if role.get("role") == "keeper"), {})


def _ask_harness(base: str, sid: str, prompt: str) -> str:
    """One turn on the brain session; the reply text. Follows OUR message id
    (`mids`) through the event bus, exactly as the serve-core path follows
    message_ids, so a concurrent operator turn is never mistaken for ours."""
    before = _harness_json(base, "/api/sessions/%s/events?after=%d" % (sid, 1 << 62))
    cursor = int(before.get("cursor") or 0)
    receipt = _harness_json(base, "/api/sessions/%s/messages" % sid, {"text": prompt, "by": "hugpy-core-brain"}, 20)
    mid = str(receipt.get("message_id") or "")
    if not mid:
        raise RuntimeError("brain session accepted no message")
    deadline = time.monotonic() + 240
    while time.monotonic() < deadline:
        view = _harness_json(base, "/api/sessions/%s/events?after=%d" % (sid, cursor))
        for ev in view.get("events") or []:
            cursor = max(cursor, int(ev.get("id") or 0))
            data = ev.get("data") if isinstance(ev.get("data"), dict) else {}
            if ev.get("kind") == "done" and mid in (data.get("mids") or []):
                if data.get("outcome") != "done":
                    raise RuntimeError("brain turn failed: %s" % str(data.get("error") or data.get("outcome"))[:250])
                reply = str(data.get("answer") or "").strip()
                if not reply:
                    raise RuntimeError("brain turn returned an empty reply")
                return reply
        time.sleep(1)
    raise RuntimeError("brain evaluation timed out")


def brain_model() -> Optional[str]:
    return resolve_brain().get("model")


def auto_gate(ev: dict, brain: Optional[dict] = None) -> dict:
    """May this fix be implemented WITHOUT operator approval? Settings
    brain.auto_fix must be ticked, the fix must be a pip fix with packages, and
    when a model inferred it, that model must meet the grade threshold. A fix
    the rules read literally off the error (no model judgement) needs only the
    tick."""
    pol = policy()
    if pol.get("auto_fix") is False:
        return {"eligible": False, "why": "auto-implement fixes is off (Settings → Policies → Brain)"}
    if ev.get("fix_kind") != "pip" or not ev.get("packages"):
        return {"eligible": False, "why": "only pip fixes with named packages are implemented automatically"}
    if ev.get("source") == "rules":
        return {"eligible": True, "why": "the error names the package literally (no model judgement)"}
    q = (brain or {}).get("qualification") or qualification(ev.get("brain_model"))
    if q and q.get("meets"):
        return {"eligible": True, "why": f"brain {ev.get('brain_model')} meets the grade threshold"}
    return {"eligible": False, "why": f"brain {ev.get('brain_model')} is below the grade threshold ("
                                     + "; ".join((q or {}).get("short") or ["ungraded"]) + ") — needs approval"}


_SYSTEM = (
    "You are hugpy-brain. You evaluate ONE model-load failure on a hugpy worker and answer "
    "with ONE JSON object and nothing else:\n"
    '{"class": one of ' + json.dumps(list(LOAD_FAILURE_CLASSES)) + ', '
    '"fix_kind": one of ' + json.dumps(list(FIX_KINDS)) + ', '
    '"packages": [pip requirement specs to install, [] if not a pip fix], '
    '"reason": "one sentence"}\n'
    "Rules: map Python import names to their PyPI distribution names (e.g. an import "
    "name that differs from the package name). Only name packages the error implies. "
    "Never suggest installing into a shared venv; the caller builds an isolated profile. "
    "Do not call tools or ask questions. If the error is ambiguous, choose class other, "
    "fix_kind unknown, packages [], and explain the uncertainty in reason.")


def _ask_brain(model: str, error: str, ctx: dict, rules: dict) -> "tuple[dict, str]":
    user = ("FAILURE\n" + json.dumps({"worker": ctx.get("worker"), "model_key": ctx.get("model_key"),
                                       "engine": ctx.get("engine"), "runner": ctx.get("runner"),
                                       "rules_classification": rules}, indent=1)
            + "\n\nERROR TEXT (verbatim)\n" + error[:6000])
    base = _keeper_base()
    # Check the standing role before sending. A silent keeper model switch must
    # not turn an unqualified model's guess into an automatically approved fix.
    keeper = _keeper_role()
    selected = str(keeper.get("model") or "")
    sid = str(keeper.get("live_session_id") or "")
    if keeper.get("backend") != "hugpy" or selected.removeprefix("hugpy-fleet:") != model or not sid:
        raise RuntimeError(f"keeper model {selected or '(none)'} differs from brain selection {model}")
    prompt = ("[Hugpy Core automatic brain evaluation; intent: " + BRAIN_INTENT + "]\n"
              + _SYSTEM + "\n\n" + user)
    if keeper.get("kind") == "harness":
        reply = _ask_harness(base, sid, prompt)
        m = re.search(r"\{.*\}", reply, re.S)
        if not m:
            raise RuntimeError(f"brain returned no JSON: {reply[:200]!r}")
        return json.loads(m.group(0)), model
    body = {"session_id": sid, "prompt": prompt, "by": "hugpy-core-brain"}
    req = urllib.request.Request(base + "/api/console/chat", data=json.dumps(body).encode(),
                                 method="POST", headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            receipt = json.load(r)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"keeper submit HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:300]}") from exc
    ids = set(receipt.get("message_ids") or [])
    if not ids:
        raise RuntimeError("keeper submit returned no message ID")
    sid = str(receipt.get("session_id") or sid)
    cursor = int(receipt.get("cursor") or 0)
    deadline = time.monotonic() + 240
    reply = ""
    while time.monotonic() < deadline:
        url = base + "/api/console/events?" + urllib.parse.urlencode({"id": sid, "since": cursor})
        with urllib.request.urlopen(url, timeout=15) as r:
            events = json.load(r).get("events") or []
        for event in events:
            cursor = max(cursor, int(event.get("seq") or 0))
            if ids.intersection(event.get("message_ids") or []):
                if event.get("type") == "done":
                    if event.get("rc") not in (None, 0):
                        if 0 < int(event.get("retry") or 0) < 3 and not event.get("held"):
                            continue
                        raise RuntimeError(f"keeper turn failed: {str(event.get('error') or '')[:250]}")
                    reply = str(event.get("result") or "").strip()
                    if not reply:
                        raise RuntimeError("keeper turn returned an empty reply")
                    break
                if event.get("type") == "error":
                    raise RuntimeError(f"keeper turn failed: {str(event.get('error') or event.get('text') or '')[:250]}")
        if reply:
            break
        time.sleep(1)
    if not reply:
        raise RuntimeError("keeper evaluation timed out or returned an empty reply")
    m = re.search(r"\{.*\}", reply, re.S)
    if not m:
        raise RuntimeError(f"brain returned no JSON: {reply[:200]!r}")
    v = json.loads(m.group(0))
    return v, model


def evaluate(error: str, *, worker: Optional[str] = None, model_key: Optional[str] = None,
             engine: Optional[str] = None, runner: Optional[str] = None, use_model: bool = True) -> dict:
    """Classify, then infer the fix. The brain model is asked only when the rules
    leave something unknown (class 'other', or import names with no package)."""
    rules = classify(error)
    ev = {"class": rules["class"], "fix_kind": rules["fix_kind"], "packages": list(rules["packages"]),
          "modules": rules["modules"], "reason": rules["reason"], "final": rules["final"],
          "source": "rules", "literal": bool(rules["packages"]) and not rules["modules"]}
    need_model = rules["class"] == "other" or bool(rules["modules"])
    brain = None
    if need_model and use_model:
        brain = resolve_brain()
        model = brain.get("model")
        if not model:
            ev["brain_error"] = brain.get("why") or "no brain model"
        else:
            try:
                v, answered = _ask_brain(model, error, {"worker": worker, "model_key": model_key,
                                                        "engine": engine, "runner": runner}, rules)
                # the rules' class stands when they determined one; the brain sets
                # the class only for 'other' and otherwise fills in the packages
                if rules["class"] == "other":
                    if v.get("class") in LOAD_FAILURE_CLASSES:
                        ev["class"] = v["class"]
                    if v.get("fix_kind") in FIX_KINDS:
                        ev["fix_kind"] = v["fix_kind"]
                pk = [p for p in (v.get("packages") or []) if isinstance(p, str) and re.fullmatch(_PIP_SPEC, p.strip())]
                ev["packages"] = sorted(set(ev["packages"]) | {p.strip() for p in pk})
                ev["reason"] = str(v.get("reason") or ev["reason"])[:400]
                ev.update({"source": "brain", "brain_model": answered, "literal": False})
                ev["final"] = ev["class"] in FINAL_LOAD_CLASSES
            except Exception as exc:  # noqa: BLE001 — an evaluation never breaks the caller
                ev["brain_error"] = str(exc)[:300]
    if brain is not None:
        ev["brain_why"] = brain.get("why")
    ev["auto"] = auto_gate(ev, brain)
    ev["next"] = ("venv ladder (existing profiles → new overlay → isolated), each candidate test-loaded — "
                  "NOT automated yet; when it is, this fix "
                  + ("applies automatically" if ev["auto"]["eligible"] else "waits for operator approval")
                  + f" ({ev['auto']['why']})") if ev["fix_kind"] == "pip" else None
    return ev


# ── tickets (the filer core lacked; shape 1:1 with legacy help_tickets) ─────────
def file_ticket(ev: dict, *, error: str, model_key: Optional[str], worker_id: Optional[str],
                worker_name: Optional[str]) -> Optional[int]:
    from psycopg.types.json import Jsonb
    from hugpy_core.help import help_store
    title = f"{model_key or '?'} on {worker_name or '?'}: {ev['class']}" + (
        f" → pip {' '.join(ev['packages'])}" if ev.get("packages") else "")
    detail = {"evaluation": ev, "error": error[:20000]}
    now = time.time()
    with help_store._db() as c:
        row = c.execute("SELECT id FROM help_tickets WHERE kind=%s AND status='pending' AND"
                        " model_key IS NOT DISTINCT FROM %s AND worker_name IS NOT DISTINCT FROM %s"
                        " AND detail->>'error' = %s ORDER BY id DESC LIMIT 1",
                        (TICKET_KIND, model_key, worker_name, error[:20000])).fetchone()
        if row:
            # merge, never replace: the fix ladder keeps its progress in detail.ladder
            c.execute("UPDATE help_tickets SET occurrences=occurrences+1, updated=%s,"
                      " detail=coalesce(detail, '{}'::jsonb) || %s, title=%s WHERE id=%s",
                      (now, Jsonb(detail), title, row["id"]))
            return int(row["id"])
        r = c.execute("INSERT INTO help_tickets (kind, status, created, updated, model_key, worker_id,"
                      " worker_name, title, detail) VALUES (%s,'pending',%s,%s,%s,%s,%s,%s,%s) RETURNING id",
                      (TICKET_KIND, now, now, model_key, worker_id, worker_name, title, Jsonb(detail))).fetchone()
        return int(r["id"])


def evaluate_and_file(error: str, *, worker: Optional[str], model_key: Optional[str],
                      engine: Optional[str] = None, runner: Optional[str] = None,
                      log_tail: Optional[str] = None) -> dict:
    if log_tail is None:
        log_tail = failure_detail(worker, model_key)
    ev = evaluate(error + ("\n" + log_tail if log_tail and log_tail not in error else ""),
                  worker=worker, model_key=model_key, engine=engine, runner=runner)
    if log_tail:
        ev["log_tail"] = log_tail[-4000:]
    wid = None
    try:
        from hugpy_core.registry import registry
        wid = (registry.lookup_worker(worker) or {}).get("id") if worker else None
    except Exception:  # noqa: BLE001
        pass
    try:
        ev["ticket_id"] = file_ticket(ev, error=error, model_key=model_key, worker_id=wid, worker_name=worker)
    except Exception as exc:  # noqa: BLE001
        ev["ticket_error"] = str(exc)[:300]
    # THE FIX LADDER starts on its own only when the gate allows it (Settings
    # brain.auto_fix + the grade threshold); otherwise the ticket's ✓ approve
    # starts it. A ticket whose ladder already ran is never re-run automatically.
    if ev.get("ticket_id") and (ev.get("auto") or {}).get("eligible") \
            and ev.get("class") == MISSING_DEPENDENCY and worker and model_key:
        try:
            from hugpy_core.brain import fix_ladder
            from hugpy_core.help import help_store
            prior = ((help_store.get_ticket(ev["ticket_id"]) or {}).get("detail") or {}).get("ladder") or {}
            if prior.get("state") in ("running", "done", "failed", "needs-approval"):
                ev["ladder"] = {"started": False, "why": f"this ticket's fix ladder already ran ({prior.get('state')})"}
            else:
                ev["ladder"] = fix_ladder.start(ev["ticket_id"], worker=worker, model_key=model_key,
                                                packages=ev.get("packages"), by="brain-auto")
        except Exception as exc:  # noqa: BLE001
            ev["ladder"] = {"started": False, "why": f"{type(exc).__name__}: {exc}"}
    logger.info("brain: %s on %s → %s/%s %s (%s) ladder=%s", model_key, worker, ev["class"], ev["fix_kind"],
                ev.get("packages"), ev["source"], ev.get("ladder"))
    return ev


# ── the event: a residents row whose load_error changed ─────────────────────────
_lock = threading.Lock()
_started = [False]
_seen: dict = {}          # (worker, key) -> last evaluated load_error


def _on_resident(worker: str, key: str) -> None:
    import psycopg
    from psycopg.rows import dict_row
    from hugpy_core.calllog.calllog_db import dsn
    with psycopg.connect(dsn(), row_factory=dict_row, connect_timeout=5) as c:
        r = c.execute("SELECT load_error, engine, runner FROM residents WHERE worker=%s AND key=%s",
                      (worker, key)).fetchone()
    err = (r or {}).get("load_error") or ""
    if policy().get("auto") is False:          # Settings → brain auto-evaluate off
        return
    from hugpy_core.brain import fix_ladder
    if fix_ladder.active_for(worker, key) is not None or "profile_materializing" in err:
        return                                 # the ladder's own test loads / a build in progress
    with _lock:
        if not err.strip() or _seen.get((worker, key)) == err:
            return
        _seen[(worker, key)] = err
    evaluate_and_file(err, worker=worker, model_key=key, engine=r.get("engine"), runner=r.get("runner"))


def _loop() -> None:
    import psycopg
    from hugpy_core.calllog.calllog_db import dsn
    from hugpy_core.imports.functions import listen_channel
    while True:
        try:
            with psycopg.connect(dsn(), autocommit=True) as conn:
                chan = listen_channel(conn, "model_rows")
                logger.info("brain listening on '%s' (residents.load_error)", chan)
                for n in conn.notifies():
                    try:
                        p = json.loads(n.payload or "{}") or {}
                    except ValueError:
                        continue
                    if p.get("table") != "residents" or p.get("op") == "DELETE":
                        continue
                    w, k = p.get("worker"), p.get("key")
                    if w and k:
                        threading.Thread(target=_safe, args=(w, k), daemon=True).start()
        except Exception as exc:  # noqa: BLE001
            logger.warning("brain listener reconnect: %s", exc)
            time.sleep(2)


def _safe(w: str, k: str) -> None:
    try:
        _on_resident(w, k)
    except Exception:  # noqa: BLE001
        logger.exception("brain evaluation failed for %s on %s", k, w)


def ensure() -> None:
    if (os.environ.get("HUGPY_BRAIN", "1") or "").strip().lower() in ("0", "false", "off", "no"):
        return
    with _lock:
        if _started[0]:
            return
        _started[0] = True
    try:
        from hugpy_core.brain import fix_ladder
        fix_ladder.recover_interrupted()
    except Exception as exc:  # noqa: BLE001
        logger.warning("fix ladder recovery failed: %s", exc)
    threading.Thread(target=_loop, name="brain-listen", daemon=True).start()
    from hugpy_core.brain import test_fire_review
    test_fire_review.ensure()


# ── callable (route handlers: kwargs in, JSON-able out; brain/routes.py mounts
#    them at /llm/brain and /llm/brain/evaluate) ─────────────────────────────
def brain_evaluate(error=None, worker=None, model_key=None, file=None):
    """{error, worker?, model_key?, file?: bool} → the evaluation (+ ticket_id when filed)."""
    err = str(error or "").strip()
    if not err:
        return {"error": "need error text"}
    if file:
        return evaluate_and_file(err, worker=worker, model_key=model_key)
    return evaluate(err, worker=worker, model_key=model_key)


def brain_status():
    """The resolved brain (and why), policy, grade threshold + grader categories,
    and the hugpy-brain group's members with their qualification."""
    from hugpy_core.grading import grader
    group = {}
    try:
        group = ensure_brain_group()
    except Exception as exc:  # noqa: BLE001
        logger.warning("hugpy-brain group unavailable: %s", exc)
    sums, thr = _summaries(), threshold()
    members = [{"model_key": mk, "servable": _servable(mk), **qualification(mk, sums, thr)}
               for mk in (group.get("members") or [])]
    return {"resolved": resolve_brain(), "policy": policy(), "threshold": thr,
            "default_threshold": DEFAULT_THRESHOLD,
            "categories": list(dict.fromkeys(c for c, _t, _p, _k in grader.curriculum(grader.SUITE))),
            "tiers": len(grader.TIER_ORDER),
            "group": {"id": BRAIN_GROUP, "source": group.get("source"), "note": group.get("note"),
                      "members": members},
            "intent": BRAIN_INTENT, "classes": list(LOAD_FAILURE_CLASSES),
            "fix_kinds": list(FIX_KINDS), "listening": _started[0]}


# ── allocation failures (operator 2026-10-06: "the brain should make a
# determination" — e.g. a benchmark lane refused because the worker does not
# hold the model; core never forces a download) ─────────────────────────────────
ALLOC_TICKET_KIND = "allocation"


def evaluate_constraint(model_key: str, worker: Optional[str], reason: str) -> dict:
    """Where the model actually is, and what would make the lane runnable —
    from the registry and central's catalog (rules; no model call needed):
      held by another online worker → run it there (fix 'reroute')
      in central's catalog            → pull it to this worker (fix 'pull' = ACTIVATE)
      nowhere                         → not available (fix 'unknown')."""
    from hugpy_core.registry import registry
    from hugpy_core.brain.model_groups import keys_match
    holders = []
    for w in registry.all_workers():
        if not registry.is_online(w):
            continue
        held = set(w.get("models_local") or []) | set(w.get("models") or []) \
            | set((w.get("models_discovered") or {}).keys())
        if any(keys_match(model_key, h) for h in held):
            holders.append(w.get("name"))
    central = None
    try:
        from hugpy_core.models.modeldb import _conn
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT model_key, framework, bytes AS size_bytes FROM central_models WHERE model_key=%s AND NOT coalesce(missing, false)",
                        (model_key,))
            central = cur.fetchone()
    except Exception as exc:  # noqa: BLE001
        logger.debug("central_models read failed: %s", exc)
    ev = {"class": "not_on_disk", "worker": worker, "holders": holders, "source": "rules",
          "on_central": bool(central), "central_bytes": (central or {}).get("size_bytes"),
          "constraint": reason, "packages": []}
    if holders and worker not in holders:
        ev.update(fix_kind="reroute", reason=f"{model_key} is on {', '.join(holders)} — run the lane there")
    elif central:
        ev.update(fix_kind="pull", reason=f"{model_key} is in central's catalog "
                                         f"({int(central.get('size_bytes') or 0):,} B) — pull it to {worker}")
    else:
        ev.update(fix_kind="unknown", reason=f"{model_key} is on no online worker and not in central's catalog")
    pol = policy()
    if ev["fix_kind"] != "pull":
        ev["auto"] = {"eligible": False, "why": "only a pull from central is implemented automatically"}
    elif pol.get("auto_fix") is False:
        ev["auto"] = {"eligible": False, "why": "auto-implement fixes is off (Settings → Policies → Brain)"}
    else:
        ev["auto"] = {"eligible": True, "why": "central holds the files (no model judgement)"}
    return ev


def activate(model_key: str, worker: Optional[str]) -> dict:
    """The pull itself: core's ACTIVATE intent on the pair (the box pulls the files
    chunk-verified from central on its next sync)."""
    from hugpy_core.registry import registry
    from hugpy_core.models.modeldb import record_activation
    w = registry.lookup_worker(worker) if worker else None
    if not w:
        return {"ok": False, "why": f"worker {worker!r} is not registered"}
    return {"ok": True, "worker_id": w["id"], "activate": record_activation(model_key, w["id"], "requested")}


def constraint_and_file(model_key: str, worker: Optional[str], reason: str) -> dict:
    """Evaluate one refused allocation, file it (help ticket kind 'allocation',
    de-duplicated), and pull automatically when the gate allows."""
    from psycopg.types.json import Jsonb
    from hugpy_core.help import help_store
    from hugpy_core.registry import registry
    ev = evaluate_constraint(model_key, worker, reason)
    wid = (registry.lookup_worker(worker) or {}).get("id") if worker else None
    title = f"{model_key} on {worker or '?'}: not on disk → {ev['fix_kind']}"
    now = time.time()
    with help_store._db() as c:
        row = c.execute("SELECT id, detail FROM help_tickets WHERE kind=%s AND status='pending' AND"
                        " model_key IS NOT DISTINCT FROM %s AND worker_name IS NOT DISTINCT FROM %s"
                        " ORDER BY id DESC LIMIT 1", (ALLOC_TICKET_KIND, model_key, worker)).fetchone()
        if row:
            tid = int(row["id"])
            c.execute("UPDATE help_tickets SET occurrences=occurrences+1, updated=%s,"
                      " detail=coalesce(detail,'{}'::jsonb) || %s, title=%s WHERE id=%s",
                      (now, Jsonb({"evaluation": ev, "error": reason}), title, tid))
            already = (row.get("detail") or {}).get("pull")
        else:
            tid = int(c.execute("INSERT INTO help_tickets (kind, status, created, updated, model_key, worker_id,"
                                " worker_name, title, detail) VALUES (%s,'pending',%s,%s,%s,%s,%s,%s,%s)"
                                " RETURNING id", (ALLOC_TICKET_KIND, now, now, model_key, wid, worker, title,
                                                  Jsonb({"evaluation": ev, "error": reason}))).fetchone()["id"])
            already = None
    ev["ticket_id"] = tid
    if ev["auto"]["eligible"] and not already:
        res = activate(model_key, worker)
        ev["pull"] = res
        with help_store._db() as c:
            c.execute("UPDATE help_tickets SET detail = coalesce(detail,'{}'::jsonb) || %s WHERE id=%s",
                      (Jsonb({"pull": {**res, "by": "brain-auto", "at": time.time()}}), tid))
    logger.info("brain allocation: %s on %s → %s (%s) ticket %s pull=%s", model_key, worker, ev["fix_kind"],
                ev["reason"], tid, ev.get("pull"))
    return ev
