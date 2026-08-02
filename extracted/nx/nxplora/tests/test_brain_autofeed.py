"""Grail phase #2 STEP 5 — the CLI auto-feed 'important' filter (_brain_autofeed_agent_run).
Fires ONE brain node only on a real-work leader run. Run: python3 nx/cli/tests/test_brain_autofeed.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_cli

_calls = []
nx_cli._brain_write_async = lambda kind, cfg, user_id, content, label, world, metadata=None: _calls.append(
    {"kind": kind, "user_id": user_id, "content": content, "label": label, "world": world, "meta": metadata})

CFG = {"user_id": "u1"}
OKW = [{"server": "clickup", "tool": "create_task", "ok": True}, {"server": "clickup", "tool": "get", "ok": False}]
LONG = "Landed 3 deals into the sales pipeline; created NIC-9. Runway looks healthy for now."


def test_fires_on_real_work_leader_run():
    _calls.clear()
    nx_cli._brain_autofeed_agent_run(CFG, "Vinny", "sales", "map my deals into the pipeline", LONG, OKW, 0)
    assert len(_calls) == 1
    c = _calls[0]
    assert c["kind"] == "agent" and c["user_id"] == "u1" and c["world"] == "sales"
    assert c["meta"]["kind"] == "agent-run" and c["meta"]["agent"] == "Vinny"
    assert "clickup·create_task" in c["meta"]["ops"]           # successful op recorded; failed op omitted
    assert c["content"].startswith("Landed 3 deals")


def test_does_not_fire():
    # sub-agent (depth>0) → leader captures the tree, sub-agents don't feed
    _calls.clear(); nx_cli._brain_autofeed_agent_run(CFG, "Scout", "sales", "x", LONG, OKW, 1); assert not _calls
    # short/insubstantial answer
    _calls.clear(); nx_cli._brain_autofeed_agent_run(CFG, "Vinny", "sales", "x", "too short", OKW, 0); assert not _calls
    # no successful op (idle chit-chat / all failed) → not brain-worthy
    _calls.clear(); nx_cli._brain_autofeed_agent_run(CFG, "Vinny", "sales", "x", LONG, [{"server":"a","tool":"b","ok":False}], 0); assert not _calls
    _calls.clear(); nx_cli._brain_autofeed_agent_run(CFG, "Vinny", "sales", "x", LONG, [], 0); assert not _calls
    # not signed in (no user_id resolvable)
    _calls.clear(); nx_cli._brain_autofeed_agent_run({}, "Vinny", "sales", "x", LONG, OKW, 0); assert not _calls


if __name__ == "__main__":
    for n, f in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        f(); print(f"  ✓ {n}")
    print("ALL CLI AUTO-FEED PROOFS PASS")
