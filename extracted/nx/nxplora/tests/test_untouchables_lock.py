"""Grail phase #1 — the structural T3 UNTOUCHABLES lock (money movement / signing = founder-only, never
autonomous). Proves the guard at the REAL enforcement chokepoint (_guarded_mcp_call) with the wire instrumented.

Run: python3 nx/cli/tests/test_untouchables_lock.py   (or via pytest)
"""
import sys, os, builtins

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))   # nx/cli on the path

import nx_cli
import nx_mcp_tools

_wired = []


def _instrument():
    nx_mcp_tools.call = lambda s, t, a: (_wired.append(f"{s}.{t}"),
                                         {"ok": True, "connected": True, "result": "(wire)"})[1]


def _tty(v):
    nx_cli.sys = type("S", (), {
        "stdin":  type("x", (), {"isatty": staticmethod(lambda: v)})(),
        "stdout": type("x", (), {"isatty": staticmethod(lambda: v)})(),
    })()


def test_a_t3_never_autonomous_any_config():
    """(a) A T3 op cannot fire in ANY autonomous/headless/--approve/lane/flight/tier context."""
    _instrument()
    t3 = [("stripe", "create_charge"), ("mercury", "send_wire"), ("docusign", "create_envelope"),
          ("gusto", "run_payroll"), ("wise", "create_transfer"), ("hellosign", "create_signature_request")]
    _wired.clear()
    for s, t in t3:
        for approve in (True, False):
            for nonint in (True, False):
                for tty in (True, False):
                    _tty(tty)
                    cfg = {"_approve_ok": approve, "_noninteractive": nonint, "_session_approve_all": True,
                           "_approve_all_scopes": {"run_command": 9e18, "destructive_mcp": 9e18},
                           "_flight": True, "_lane": "*", "_tier": "T1"}
                    r = nx_cli._guarded_mcp_call(s, t, "{}", cfg)
                    assert r.get("untouchable") and r.get("blocked"), (s, t, approve, nonint, tty, r)
    assert not _wired, _wired


def test_b_unknown_money_fails_safe_to_t3():
    """(b) A NEW/unknown money-ish tool resolves T3 (fail-safe), not a lower tier — the STRUCTURAL guarantee."""
    _instrument(); _tty(True); _wired.clear()
    unknown = [("stripe", "zorp_v9"), ("newbank", "book_transfer"), ("acmebank", "frobnicate_transfer"),
               ("mercury", "flush"), ("paypal", "execute_batch")]
    for s, t in unknown:
        assert nx_cli._guarded_mcp_call(s, t, "{}", {"_approve_ok": True}).get("untouchable"), (s, t)
    assert not _wired, _wired


def test_c_founder_only_path():
    """(c) T3 = 'never AUTONOMOUS, not never': a live founder CAN do it via the separate path with explicit confirm."""
    _instrument(); _tty(True)
    builtins.input = lambda *a, **k: "CONFIRM create_charge"; _wired.clear()
    assert nx_cli._founder_execute_untouchable("stripe", "create_charge", "{}", {}).get("ok")
    assert "stripe.create_charge" in _wired
    builtins.input = lambda *a, **k: "nope"; _wired.clear()
    assert not nx_cli._founder_execute_untouchable("stripe", "create_charge", "{}", {}).get("ok")
    assert not _wired
    _tty(False)
    assert not nx_cli._founder_execute_untouchable("stripe", "create_charge", "{}", {}).get("ok")   # headless refused
    _tty(True)
    assert not nx_cli._founder_execute_untouchable("stripe", "create_charge", "{}", {"_noninteractive": True}).get("ok")  # agent refused


def test_d_no_regression_t1_t2():
    """(d) SAFE still runs free; T1/T2 DESTRUCTIVE still headless-fail-closed + TTY-per-op-approvable."""
    _instrument(); nx_cli.approve_gate = lambda **k: (True, "")
    _tty(False); _wired.clear()
    assert nx_cli._guarded_mcp_call("clickup", "get_task", "{}", {"_noninteractive": True}).get("ok")
    assert "clickup.get_task" in _wired                                            # SAFE fires free
    _wired.clear()
    r = nx_cli._guarded_mcp_call("clickup", "delete_task", "{}", {"_noninteractive": True, "_approve_ok": True})
    assert r.get("blocked") and not r.get("untouchable") and not _wired            # DESTRUCTIVE headless-blocked (not T3)
    _tty(True); _wired.clear()
    assert nx_cli._guarded_mcp_call("clickup", "delete_task", "{}", {"_noninteractive": True, "_approve_ok": True}).get("ok")
    assert "clickup.delete_task" in _wired                                         # per-op still fires at a TTY
    _wired.clear()
    assert nx_cli._guarded_mcp_call("gmail", "send_email", "{}", {"_noninteractive": True, "_approve_ok": True}).get("ok")


def test_e_subagent_cannot_reach_t3():
    """(e) A sub-agent (leaders-only + structural T3) still cannot reach T3 or DESTRUCTIVE."""
    _instrument(); _tty(True); _wired.clear()
    sub = {"_noninteractive": True, "_approve_ok": False, "_swarm_depth": 1}
    assert nx_cli._guarded_mcp_call("stripe", "create_charge", "{}", sub).get("untouchable")
    assert nx_cli._guarded_mcp_call("clickup", "delete_task", "{}", sub).get("blocked")
    assert not _wired


if __name__ == "__main__":
    for name, fn in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        fn(); print(f"  ✓ {name}")
    print("ALL T3 UNTOUCHABLES-LOCK PROOFS PASS")
