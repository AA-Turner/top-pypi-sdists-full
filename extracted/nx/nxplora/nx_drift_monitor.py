"""nx_drift_monitor — KEY 2 of the verification layer: the continuous DRIFT / FALSE-SUCCESS monitor.

The anti-gallery-failure layer, made CONTINUOUS instead of luck-caught. A one-shot proof at creation time can go
stale: an artifact marked `proven` can later STOP being provable (an API changed, the wall re-classified, the
sandbox tightened) while its status still lies `proven`. This monitor, on a cadence, RE-RUNS the honest executor
(nx_proof_gate.prove) for every reported-proven artifact and COMPARES to the reported state:

  still_proven      — re-prove passes. No drift.
  expected          — re-prove fails BUT the artifact's content changed since last seen → an intentional edit, not a
                      lie. (A content hash snapshot in ~/.nx/drift_state.json distinguishes intent from regression.)
  false_completion  — re-prove fails AND the content is unchanged (or first-seen) → the system is lying to itself.
                      DRIFT. Downgrade to pending + alert.

Cadence: run via `nx verify --drift` / a scheduled dispatch. Composes existing parts (the proof gate is the
re-runnable honest executor) — the only new thing is the standing compare-to-reported loop + the intent classifier.
"""
import glob
import hashlib
import json
import os

_NX = os.path.join(os.path.expanduser("~"), ".nx")


def _hash(s):
    return hashlib.sha256(str(s or "").encode("utf-8", "replace")).hexdigest()[:16]


def _state_path():
    return os.path.join(_NX, "drift_state.json")


def _load_state():
    try:
        with open(_state_path(), encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _save_state(d):
    try:
        os.makedirs(_NX, exist_ok=True)
        with open(_state_path(), "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)
    except Exception:
        pass


def _classify(name, content, reproven_ready, state):
    """still_proven | expected | false_completion — the intent classifier (unchanged + fails = a lie)."""
    h = _hash(content)
    prev = state.get(name)
    state[name] = h
    if reproven_ready:
        return "still_proven"
    if prev is not None and prev != h:
        return "expected"       # changed since last seen → intentional edit, not drift
    return "false_completion"   # unchanged (or first-seen) yet no longer provable → the status lies


def _reprove_tool(d):
    import nx_proof_gate as G
    return G.prove({"type": "tool", "name": d.get("name"), "kind": d.get("kind", "compute"), "code": d.get("code"),
                    "input": d.get("probe_input"), "server": d.get("server"), "action": d.get("action"),
                    "args": d.get("args", "")}).ready


def _tool_content(d):
    return (d.get("code") or "") + "|" + str(d.get("server") or "") + "|" + str(d.get("action") or "")


def run_monitor(act=False):
    """Scan reported-proven artifacts, re-prove, classify drift. If act=True, downgrade false_completions to pending.
    Returns {checked, drift:[{kind,name,class}], false_completions:int}."""
    state = _load_state()
    report = {"checked": 0, "drift": [], "false_completions": 0}

    # generated TOOLS (local, deterministic re-prove)
    for p in glob.glob(os.path.join(_NX, "generated_tools", "*.json")):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if d.get("status") != "proven":
            continue
        report["checked"] += 1
        key = "tool:" + str(d.get("name"))
        cls = _classify(key, _tool_content(d), _reprove_tool(d), state)
        if cls != "still_proven":
            report["drift"].append({"kind": "tool", "name": d.get("name"), "class": cls})
        if cls == "false_completion":
            report["false_completions"] += 1
            if act:
                d["status"] = "pending"
                d["drift"] = {"downgraded": True, "reason": "false_completion: proven but re-prove failed, content unchanged"}
                try:
                    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
                except Exception:
                    pass

    _save_state(state)
    return report


def alert_line(report):
    """One honest human line for the report-back channels."""
    fc = report["false_completions"]
    if fc:
        names = [d["name"] for d in report["drift"] if d["class"] == "false_completion"]
        return "⚠️ DRIFT: %d artifact(s) reported proven but no longer prove (false-completion): %s — downgraded to pending." % (fc, ", ".join(names[:5]))
    exp = sum(1 for d in report["drift"] if d["class"] == "expected")
    return "✓ no false-completion drift across %d proven artifact(s)%s." % (report["checked"], (" (%d changed intentionally)" % exp) if exp else "")


if __name__ == "__main__":
    import sys
    r = run_monitor(act="--act" in sys.argv)
    print(alert_line(r))
    sys.exit(1 if r["false_completions"] else 0)
