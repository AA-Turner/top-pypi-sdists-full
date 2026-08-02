"""The PACKAGING invariants — the finding of the session, pinned so it can't recur.

TWICE a security module shipped omitted from setup.py py_modules (nx_browse, then nx_code_gate), and both
importers swallowed the ImportError — so the module ran as a SILENT NO-OP while the CLI reported it live. A
security control that fails open on import is a fake-success generator living in the packaging. Two invariants:

  1. Every shipped .py module in nx/cli/ is listed in py_modules (anti-drift, like the pinned palette).
  2. Security-critical imports are FATAL, not swallowed — a missing gate crashes the module load, loud.

Run: python3 nx/cli/tests/test_packaging_invariants.py   (or via the nx verify gate)
"""
import sys, os, re, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
_CLI = os.path.dirname(_HERE)
sys.path.insert(0, _CLI)

# Modules that legitimately DO NOT ship as importable py_modules (build/dev only). Anything else on disk that
# is missing from py_modules is a ship-omission bug — the exact class that hid nx_browse + nx_code_gate.
_SKIP = {"setup"}


def _py_modules():
    src = open(os.path.join(_CLI, "setup.py"), encoding="utf-8").read()
    m = re.search(r"py_modules\s*=\s*\[([^\]]+)\]", src)
    assert m, "could not find py_modules in setup.py"
    return set(re.findall(r'"([^"]+)"', m.group(1)))


def test_every_shipped_module_is_in_py_modules():
    listed = _py_modules()
    on_disk = set()
    for fn in os.listdir(_CLI):
        if fn.endswith(".py") and not fn.endswith(".py.bak"):
            mod = fn[:-3]
            if mod in _SKIP or mod.startswith("__"):
                continue
            on_disk.add(mod)
    missing = on_disk - listed
    assert not missing, (
        "modules on disk but MISSING from setup.py py_modules — they would ship as silent no-ops "
        "(the nx_browse / nx_code_gate class): %s" % sorted(missing))


def test_security_modules_import_cleanly():
    # a missing security module must be a hard import error here, not a silent skip
    for m in ("nx_code_gate", "nx_worlds", "risk_tiers", "autonomy_loop", "nx_proof_gate", "nx_tool_sandbox"):
        __import__(m)


def test_executor_holds_the_gate_at_module_level():
    import nx_executor
    assert hasattr(nx_executor, "classify_code_action"), (
        "nx_executor must import the coding-lane gate at MODULE level (fatal), not swallow it in a function")


def test_missing_gate_crashes_the_executor_loud_not_silent():
    # THE regression guard: with nx_code_gate blocked, importing nx_executor must FAIL — never import
    # successfully with the gate silently absent (which is what shipped twice).
    blocker = (
        "import sys, importlib.abc\n"
        "class B(importlib.abc.MetaPathFinder):\n"
        "    def find_spec(self, name, path, target=None):\n"
        "        if name == 'nx_code_gate':\n"
        "            raise ModuleNotFoundError('blocked for test')\n"
        "        return None\n"
        "sys.meta_path.insert(0, B())\n"
        "import nx_executor\n"
    )
    r = subprocess.run([sys.executable, "-c", blocker], cwd=_CLI, capture_output=True, text=True)
    assert r.returncode != 0, "nx_executor imported WITHOUT the gate present — FAIL-OPEN regression!"
    assert "nx_code_gate" in (r.stderr or "") or "blocked" in (r.stderr or "")


if __name__ == "__main__":
    for n, f in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        f(); print("  ✓ %s" % n)
    print("ALL PACKAGING-INVARIANT PROOFS PASS")
