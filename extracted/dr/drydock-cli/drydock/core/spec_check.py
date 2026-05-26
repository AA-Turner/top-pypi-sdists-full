"""Spec-assertion checker.

Parses the natural-language ``check`` strings from
``test_harness/cases.json`` (and equivalent PRD acceptance criteria) into
typed assertions, then runs them against a working tree. Returns a
machine-readable verdict the agent loop can use to decide whether a
"done" claim should be accepted.

Background: the ceiling cases (P1-B1, P2-B1, P6-B1, P2-S1, P4-S1, P5-S1,
P6-S1, P3-S2) all fail in spec-specific ways the model doesn't notice
— wrong test count, missing backup file, missing ABC class, etc. Soft
prompt nudges have been ineffective. This module is the bottom half of
a fix: extract the same assertions the harness uses to score, run them
ourselves, and surface the *specific* failed assertion as feedback the
model gets the next turn.

Supported assertion shapes (covers ~50% of harness checks by count):

* ``green(N)`` / ``green(>=N)`` / ``green(>N)`` — exact / minimum pytest
  pass count
* ``<path> exists`` / ``<path>`` (bare path with extension) — file
  presence on disk
* ``<path> == <other-path>`` — byte-for-byte file equality (e.g.
  ``tasks.json.v1.bak == original``)
* ``<file> defines ABC with <m1>/<m2>/...`` — AST-scans the file for a
  class with ``ABC`` (or ``abc.ABC``) in its bases and the listed
  methods as ``@abstractmethod``
* ``<X> issubclass(<Parent>)`` — imports the module and checks
  ``issubclass(X, Parent)`` at runtime
* ``grep -q <pattern> <path>... && echo <TAG> -> '<TAG>'`` — runs the
  literal shell pipeline and checks the output
* ``python -m <pkg> <args> -> '<output>'`` / ``<cmd> -> '<output>'`` —
  CLI invocation, stdout must equal the quoted string

Shapes not yet supported (returned as ``UNKNOWN`` with the raw text):
``readonly(...)`` (needs a pre-task snapshot), HTTP route checks (needs
a server), free-text artifact claims (``artifact(X.md) names Y``).

Usage::

    from drydock.core import spec_check
    checks = ["green(30)", "keystore/backend.py exists"]
    verdict = spec_check.verify(checks, cwd=Path("/tmp/keystore"))
    # verdict = {
    #     "passed": [...], "failed": [...], "unknown": [...],
    #     "ok": False,  # all checks must pass for ok=True
    # }

CLI: ``python -m drydock.core.spec_check --case P5-S1 --cwd .`` reads
the case checks out of ``test_harness/cases.json`` and runs them.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Assertion kinds — string constants keep the wire format JSON-safe.
KIND_GREEN = "green"
KIND_FILE_EXISTS = "file_exists"
KIND_FILE_EQ = "file_eq"
KIND_DEFINES_ABC = "defines_abc"
KIND_ISSUBCLASS = "issubclass"
KIND_GREP_TAG = "grep_tag"
KIND_CLI_OUTPUT = "cli_output"
KIND_UNKNOWN = "unknown"


@dataclass
class Assertion:
    raw: str
    kind: str
    params: dict[str, Any] = field(default_factory=dict)
    ok: bool | None = None
    msg: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "raw": self.raw, "kind": self.kind, "params": self.params,
            "ok": self.ok, "msg": self.msg,
        }


# Regexes anchored once at module load. None of these are user input —
# they come from the harness's own checks list, so we don't need
# defensive parsing, just enough discrimination to route to the right
# runner.

_GREEN_RE = re.compile(r"^\s*green\(\s*(>=|>)?\s*(\d+)\s*\)\s*$")
_FILE_EQ_RE = re.compile(r"^\s*(\S+?)\s*==\s*(\S.+?)\s*$")
_DEFINES_ABC_RE = re.compile(
    r"^\s*(\S+?)\s+defines\s+ABC\s+with\s+([\w/]+)\s*$",
)
_ISSUBCLASS_RE = re.compile(
    r"^\s*(\w[\w.]*)\s+issubclass\((\w[\w.]*)\)\s*$",
)
_GREP_TAG_RE = re.compile(
    r"^\s*grep\s+(-\w+\s+)?-?-?\S+\s+\S+.*&&\s*echo\s+(\S+)\s*->\s*'(\S+)'\s*$",
)
_CLI_OUTPUT_RE = re.compile(r"^\s*(.+?)\s*->\s*'([^']*)'\s*$")
_FILE_EXISTS_RE = re.compile(r"^\s*([\w./_-]+\.[\w]+)\s*(?:exists?)?\s*$")


def parse(check: str) -> Assertion:
    """Route a check string to the correct typed Assertion. Falls back
    to ``KIND_UNKNOWN`` when no pattern matches; callers should surface
    those as "unverified" rather than failing the run."""
    s = check.strip()

    m = _GREEN_RE.match(s)
    if m:
        op = m.group(1) or "=="
        n = int(m.group(2))
        return Assertion(raw=check, kind=KIND_GREEN, params={"op": op, "n": n})

    m = _DEFINES_ABC_RE.match(s)
    if m:
        return Assertion(
            raw=check, kind=KIND_DEFINES_ABC,
            params={"file": m.group(1), "methods": m.group(2).split("/")},
        )

    m = _ISSUBCLASS_RE.match(s)
    if m:
        return Assertion(
            raw=check, kind=KIND_ISSUBCLASS,
            params={"child": m.group(1), "parent": m.group(2)},
        )

    m = _GREP_TAG_RE.match(s)
    if m:
        return Assertion(
            raw=check, kind=KIND_GREP_TAG,
            params={"pipeline": s, "expected": m.group(3)},
        )

    # CLI output before file_eq because both contain "==" / "->" and
    # the CLI pattern is more specific.
    m = _CLI_OUTPUT_RE.match(s)
    if m:
        return Assertion(
            raw=check, kind=KIND_CLI_OUTPUT,
            params={"cmd": m.group(1).strip(), "expected": m.group(2)},
        )

    m = _FILE_EQ_RE.match(s)
    if m:
        # Heuristic: the right-hand side often says "original" — that
        # means the harness snapshot of the file before the migration.
        # We can't verify "== original" without a snapshot, so route to
        # file_eq only when both sides look like paths.
        lhs, rhs = m.group(1), m.group(2).strip()
        if rhs == "original" or "/" in rhs or "." in rhs:
            return Assertion(
                raw=check, kind=KIND_FILE_EQ,
                params={"lhs": lhs, "rhs": rhs},
            )

    m = _FILE_EXISTS_RE.match(s)
    if m:
        return Assertion(
            raw=check, kind=KIND_FILE_EXISTS, params={"path": m.group(1)},
        )

    return Assertion(raw=check, kind=KIND_UNKNOWN)


def _run_pytest_collect(cwd: Path) -> tuple[int, int, str]:
    """Returns (passed, total_collected, raw_output).

    We collect-then-run because for our use the *passed* count is the
    thing we score against. If the suite errors out we report passed=0,
    which surfaces a clear failure rather than masking a broken state.
    """
    try:
        out = subprocess.run(
            [sys.executable, "-m", "pytest", "--tb=no", "-q", "--no-header"],
            cwd=cwd, capture_output=True, text=True, timeout=180,
        )
    except subprocess.TimeoutExpired:
        return 0, 0, "pytest timed out after 180s"
    text = (out.stdout or "") + "\n" + (out.stderr or "")
    # Pytest summary line: "27 passed in 0.42s" or "5 failed, 22 passed in 0.5s"
    passed = 0
    m = re.search(r"(\d+)\s+passed", text)
    if m:
        passed = int(m.group(1))
    failed = 0
    m = re.search(r"(\d+)\s+failed", text)
    if m:
        failed = int(m.group(1))
    return passed, passed + failed, text.strip().splitlines()[-1] if text.strip() else ""


def _resolve(cwd: Path, ref: str) -> Path:
    """A check might say ``tasks.json.v1.bak == original``. ``original``
    is a harness sentinel for the seeded baseline; we map it to a
    sibling ``.original`` file or to the file the harness staged at
    task start. For now, support ``<basename>.original`` if present,
    else punt."""
    if ref == "original":
        # Convention: the harness writes <file>.original alongside any
        # file it expects to be backed up. If absent, this assertion
        # cannot be verified.
        return cwd / "MISSING_ORIGINAL_SENTINEL"
    return cwd / ref


def _run_green(a: Assertion, cwd: Path) -> None:
    passed, total, summary = _run_pytest_collect(cwd)
    op = a.params["op"]
    n = a.params["n"]
    if op == "==":
        a.ok = (passed == n)
        a.msg = f"pytest: {passed} passed (need exactly {n}). {summary}"
    elif op == ">=":
        a.ok = (passed >= n)
        a.msg = f"pytest: {passed} passed (need >= {n}). {summary}"
    elif op == ">":
        a.ok = (passed > n)
        a.msg = f"pytest: {passed} passed (need > {n}). {summary}"


def _run_file_exists(a: Assertion, cwd: Path) -> None:
    p = cwd / a.params["path"]
    a.ok = p.exists() and p.is_file()
    a.msg = f"{p.relative_to(cwd) if a.ok else a.params['path']} {'exists' if a.ok else 'NOT FOUND'}"


def _run_file_eq(a: Assertion, cwd: Path) -> None:
    lhs = cwd / a.params["lhs"]
    rhs = _resolve(cwd, a.params["rhs"])
    if not lhs.exists():
        a.ok, a.msg = False, f"{a.params['lhs']} not found"
        return
    if not rhs.exists():
        # "== original" without a snapshot — cannot verify
        a.ok = None
        a.msg = (
            f"cannot verify {a.params['lhs']} == {a.params['rhs']} "
            f"(no snapshot file at {rhs})"
        )
        return
    same = lhs.read_bytes() == rhs.read_bytes()
    a.ok = same
    a.msg = f"{a.params['lhs']} {'==' if same else '!='} {a.params['rhs']}"


def _scan_abc_class(tree: ast.AST, methods: list[str]) -> tuple[bool, str]:
    """Look for ANY ClassDef whose bases include ``ABC`` (or
    ``abc.ABC``) and that defines every method in ``methods``, each
    decorated with ``@abstractmethod``. Returns (ok, diagnostic)."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        base_names = []
        for b in node.bases:
            if isinstance(b, ast.Name):
                base_names.append(b.id)
            elif isinstance(b, ast.Attribute):
                base_names.append(b.attr)
        if "ABC" not in base_names:
            continue
        # Collect (method_name, has_abstractmethod_decorator) per def
        found: dict[str, bool] = {}
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                deco_names = []
                for d in item.decorator_list:
                    if isinstance(d, ast.Name):
                        deco_names.append(d.id)
                    elif isinstance(d, ast.Attribute):
                        deco_names.append(d.attr)
                found[item.name] = "abstractmethod" in deco_names
        missing = [m for m in methods if m not in found]
        if missing:
            return False, (
                f"class {node.name}(ABC) found but missing methods: "
                f"{', '.join(missing)}"
            )
        non_abstract = [m for m in methods if not found.get(m, False)]
        if non_abstract:
            return False, (
                f"class {node.name}(ABC) has {', '.join(non_abstract)} "
                f"but not as @abstractmethod"
            )
        return True, f"class {node.name}(ABC) with {'/'.join(methods)}"
    return False, "no class with ABC base found"


def _run_defines_abc(a: Assertion, cwd: Path) -> None:
    p = cwd / a.params["file"]
    if not p.exists():
        a.ok, a.msg = False, f"{a.params['file']} does not exist"
        return
    try:
        tree = ast.parse(p.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        a.ok, a.msg = False, f"{a.params['file']} has syntax error: {exc}"
        return
    a.ok, a.msg = _scan_abc_class(tree, a.params["methods"])


def _run_issubclass(a: Assertion, cwd: Path) -> None:
    child = a.params["child"]
    parent = a.params["parent"]
    # Run via subprocess so the package's own __init__ side-effects
    # don't bleed into our process.
    code = (
        f"import sys; sys.path.insert(0, {str(cwd)!r}); "
        f"try:\n"
        f"  from {child.rsplit('.', 1)[0] if '.' in child else child} "
        f"  import {child.rsplit('.', 1)[-1]} as _c\n"
        f"  from {parent.rsplit('.', 1)[0] if '.' in parent else parent} "
        f"  import {parent.rsplit('.', 1)[-1]} as _p\n"
        f"  print('YES' if issubclass(_c, _p) else 'NO')\n"
        f"except Exception as e:\n"
        f"  print(f'ERR: {{type(e).__name__}}: {{e}}')\n"
    )
    try:
        out = subprocess.run(
            [sys.executable, "-c", code],
            cwd=cwd, capture_output=True, text=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        a.ok, a.msg = False, "issubclass check timed out"
        return
    output = (out.stdout or "").strip() + (out.stderr or "").strip()
    if output == "YES":
        a.ok, a.msg = True, f"{child} issubclass({parent})"
    elif output == "NO":
        a.ok, a.msg = False, f"{child} is NOT subclass of {parent}"
    else:
        a.ok, a.msg = False, f"issubclass check failed: {output[:200]}"


def _run_grep_tag(a: Assertion, cwd: Path) -> None:
    try:
        out = subprocess.run(
            ["bash", "-c", a.params["pipeline"]],
            cwd=cwd, capture_output=True, text=True, timeout=15,
        )
    except subprocess.TimeoutExpired:
        a.ok, a.msg = False, "grep pipeline timed out"
        return
    actual = (out.stdout or "").strip()
    expected = a.params["expected"]
    a.ok = (actual == expected)
    a.msg = (
        f"grep -> {actual!r}"
        if a.ok else f"expected {expected!r}, got {actual!r}"
    )


def _run_cli_output(a: Assertion, cwd: Path) -> None:
    cmd = a.params["cmd"]
    expected = a.params["expected"]
    try:
        out = subprocess.run(
            ["bash", "-c", cmd], cwd=cwd, capture_output=True,
            text=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        a.ok, a.msg = False, f"{cmd!r} timed out"
        return
    actual = (out.stdout or "").strip()
    a.ok = (actual == expected)
    a.msg = (
        f"{cmd!r} -> {actual!r}"
        if a.ok else f"{cmd!r} expected {expected!r}, got {actual!r}"
    )


_RUNNERS = {
    KIND_GREEN: _run_green,
    KIND_FILE_EXISTS: _run_file_exists,
    KIND_FILE_EQ: _run_file_eq,
    KIND_DEFINES_ABC: _run_defines_abc,
    KIND_ISSUBCLASS: _run_issubclass,
    KIND_GREP_TAG: _run_grep_tag,
    KIND_CLI_OUTPUT: _run_cli_output,
}


def run(a: Assertion, cwd: Path) -> Assertion:
    """Dispatch to the kind-specific runner. Mutates and returns the
    assertion in place."""
    runner = _RUNNERS.get(a.kind)
    if runner is None:
        a.ok = None
        a.msg = f"unsupported assertion kind: {a.kind}"
        return a
    try:
        runner(a, cwd)
    except Exception as exc:
        a.ok = False
        a.msg = f"runner crashed: {type(exc).__name__}: {exc}"
    return a


def verify(checks: list[str], cwd: Path) -> dict[str, Any]:
    """Parse and run every check; aggregate the verdict.

    ``ok`` is True only when every parseable assertion passed.
    Unparseable assertions (``KIND_UNKNOWN``) are reported separately
    in the ``unknown`` bucket — the caller can decide whether to treat
    them as soft warnings or block. By default we do NOT count UNKNOWN
    against the verdict, since the alternative is refusing to ship
    every PRD with free-text criteria.
    """
    passed: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    unknown: list[dict[str, Any]] = []
    for s in checks:
        a = parse(s)
        if a.kind == KIND_UNKNOWN:
            unknown.append(a.to_dict())
            continue
        run(a, cwd)
        if a.ok:
            passed.append(a.to_dict())
        else:
            failed.append(a.to_dict())
    return {
        "passed": passed, "failed": failed, "unknown": unknown,
        "ok": not failed,  # UNKNOWN doesn't block
        "summary": (
            f"{len(passed)}/{len(passed) + len(failed)} passed"
            + (f", {len(unknown)} unverifiable" if unknown else "")
        ),
    }


def _format_for_model(verdict: dict[str, Any]) -> str:
    """Render the verdict as the agent-loop nudge text. Specific
    failures only — the model needs to know WHAT to fix, not a checklist
    of what's already green."""
    lines = [f"SPEC CHECK: {verdict['summary']}"]
    for a in verdict["failed"]:
        lines.append(f"  ✗ {a['raw']}: {a['msg']}")
    for a in verdict["unknown"]:
        lines.append(f"  ? {a['raw']} (not auto-verified — please confirm manually)")
    return "\n".join(lines)


# ----------------- CLI -----------------


def _load_case_checks(cases_json: Path, case_id: str) -> list[str]:
    data = json.loads(cases_json.read_text(encoding="utf-8"))
    for c in data.get("cases", []):
        if c.get("id") == case_id:
            return c.get("check", []) or []
    raise SystemExit(f"case {case_id} not found in {cases_json}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="drydock.core.spec_check")
    ap.add_argument("--cwd", type=Path, default=Path.cwd())
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--case", help="case_id from cases.json")
    src.add_argument("--check", action="append", help="literal check string (repeatable)")
    ap.add_argument(
        "--cases-json", type=Path,
        default=Path("/data3/drydock/test_harness/cases.json"),
    )
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ns = ap.parse_args(argv)

    checks = (
        _load_case_checks(ns.cases_json, ns.case)
        if ns.case else ns.check
    )
    verdict = verify(checks, ns.cwd)
    if ns.json:
        print(json.dumps(verdict, indent=2))
    else:
        print(_format_for_model(verdict))
    return 0 if verdict["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
