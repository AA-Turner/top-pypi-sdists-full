#!/usr/bin/env python3
"""Test-harness runner — drives drydock through cases.json.

The test harness at /data3/drydock/test_harness/ (operator-built,
2026-05-19) defines 52 cases across 6 projects in cases.json. Each case
has a verbatim prompt, an `@seed` variant, machine-checkable
`pass_criteria`, and telemetry expectations.

This runner:
  1. Loads cases.json (the source of truth, generated from CASES.md).
  2. For each case: lay down the seed → send the prompt to a real
     drydock TUI → settle → run the checks → record telemetry.
  3. Honors continuity chains (C1/C2): consecutive same-chain cases
     reuse the workspace so state-retention is tested.
  4. Skips cleanly when a seed variant isn't implemented yet — emits a
     "skip" reason so the operator knows what to wire next.

Only P1 (mdparse) seeds are implemented at v1 (10 cases). P0/P2-P6
will skip until their SEEDS.md specs are realized as actual file trees.

Check DSL supported:
  - "green(N)"                            pytest exits 0 with ≥N passed
  - "green"                               pytest exits 0
  - "<cmd> -> 'X'"                        bash cmd, stdout contains X
  - "<cmd> -> stderr matches /R/"         bash cmd, stderr matches regex R
  - "<path> exists"                       file exists
  - "from <pkg> import <name> works"      import probe → must succeed
  - "from <pkg> import <name> fails"      import probe → must raise
  - "no '<token>' token in any .py"       grep across .py files
  - "artifact(<path>) ..."                file exists; description ignored
  - "<path>.py has X & Y"                 file exists, contains X and Y
  - "<file> edited (mtime advanced)"      file mtime > case start
  - "<file> untouched (readonly)"         file mtime unchanged from pre-prompt
  - anything else                         marked manual_review (advisory)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

import pexpect

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shakedown_interactive import (  # noqa: E402
    DRYDOCK_BIN,
    SessionWatcher,
    drain_pty,
    send_prompt_and_confirm,
)
from _eval_live_printer import stream_new_messages  # noqa: E402
from _gauntlet_seed import seed_mdparse  # noqa: E402
from _test_harness_seeds import (  # noqa: E402
    seed_keystore, seed_loglens, seed_miniapi, seed_pipeflow, seed_taskvault,
)


CASES_JSON = Path("/data3/drydock/test_harness/cases.json")
SCRATCH_ROOT = Path("/tmp/drydock_test_harness")
LOG_ROOT = Path("/data3/drydock/.test_harness_runs")


# ── seed adapters ─────────────────────────────────────────────────────

def _seed_p1_clean(cwd: Path) -> None:
    seed_mdparse(cwd)


def _seed_p1_bug_blockquote(cwd: Path) -> None:
    """P1@clean already has the off-by-one blockquote bug (the
    _gauntlet_seed planted it). So this is just the clean seed."""
    seed_mdparse(cwd)


def _seed_p1_bug_trio(cwd: Path) -> None:
    """P1@bug-trio = clean seed + the 3 unrelated bugs from L7."""
    seed_mdparse(cwd)
    # Fix the blockquote planted bug FIRST so the trio is the only red.
    p = cwd / "mdparse" / "parser.py"
    p.write_text(p.read_text().replace(
        "parts.append(tokens[i].text[1:])",
        "parts.append(tokens[i].text)",
    ))
    # Now inject the 3 bugs.
    lex = cwd / "mdparse" / "lexer.py"
    lex.write_text(lex.read_text().replace(
        "text = stripped[level:].strip()",
        "text = stripped[level + 1:].strip()",
    ))
    rend = cwd / "mdparse" / "renderer.py"
    rend.write_text(rend.read_text().replace(
        'return (s.replace("&", "&amp;")',
        'return (s.replace("&", "&amp;").replace("&amp;", "&amp;amp;")\n         .replace("&", "&amp;")',
        1,
    ))
    cli = cwd / "mdparse" / "cli.py"
    cli.write_text(cli.read_text().replace("    return 0\n", "    return 1  # BUG\n"))


def _seed_p1_clean_plus_l9(cwd: Path) -> None:
    """P1 clean + 15-file noise haystack + 60-line stack trace with a
    needle pointing at mdparse/inline.py."""
    seed_mdparse(cwd)
    # Fix the planted blockquote bug so the haystack is the only signal.
    p = cwd / "mdparse" / "parser.py"
    p.write_text(p.read_text().replace(
        "parts.append(tokens[i].text[1:])",
        "parts.append(tokens[i].text)",
    ))
    payload_dir = cwd / "legacy_modules"
    payload_dir.mkdir(exist_ok=True)
    for i in range(15):
        f = payload_dir / f"module_{i:02d}.py"
        lines = [f"# legacy module {i} — verbose padding", ""]
        for j in range(80):
            lines.append(f"# row {j}: stub helper")
            lines.append(f"def helper_{i}_{j}(x): return x + {i * 100 + j}")
        f.write_text("\n".join(lines))
    trace_lines = ["Traceback (most recent call last):"]
    for i in range(28):
        trace_lines.append(
            f'  File "/data3/example/path/to/file_{i:02d}.py", line {100+i}, in func_{i}'
        )
        trace_lines.append(f"    result = layer_{i}.process(item_{i})")
    trace_lines.append('  File "mdparse/inline.py", line 18, in render_inline')
    trace_lines.append('    text = _BOLD.sub(r"<strong>\\1</strong>", text)')
    for i in range(28, 60):
        trace_lines.append(
            f'  File "/data3/example/path/to/file_{i:02d}.py", line {100+i}, in func_{i}'
        )
        trace_lines.append(f"    result = layer_{i}.process(item_{i})")
    trace_lines.append("RuntimeError: legacy_modules.module_07 failed to initialize")
    trace_lines.append("")
    trace_lines.append(
        "# FIX HINT: the _BOLD regex in mdparse/inline.py needs a "
        "non-greedy modifier so `**a** **b**` produces TWO bold spans, "
        "not one. Change [^*]+ to .+?."
    )
    (cwd / "stack_trace.txt").write_text("\n".join(trace_lines))


def _seed_empty(_cwd: Path) -> None:
    """No-op seed for P0-B1 (model scaffolds the project from scratch)."""
    return None


SEED_ADAPTERS: dict[str, Callable[[Path], None]] = {
    # P0 — model scaffolds from scratch
    "none": _seed_empty,
    # P1 mdparse
    "P1@clean": _seed_p1_clean,
    "P1@bug-blockquote": _seed_p1_bug_blockquote,
    "P1@bug-trio": _seed_p1_bug_trio,
    "P1@bug-trio (C1-continue)": _seed_p1_bug_trio,
    "P1@clean +L9 payload": _seed_p1_clean_plus_l9,
    # P2 taskvault
    "P2@clean": lambda cwd: seed_taskvault(cwd, "clean"),
    "P2@bug-search": lambda cwd: seed_taskvault(cwd, "bug-search"),
    "P2@bug-search (C2-continue)": lambda cwd: seed_taskvault(cwd, "bug-search"),
    "P2@bug-dates": lambda cwd: seed_taskvault(cwd, "bug-dates"),
    "P2@v1 (C1-continue C2)": lambda cwd: seed_taskvault(cwd, "v1"),
    # P3 loglens
    "P3@clean": lambda cwd: seed_loglens(cwd, "clean"),
    "P3@bug-ipv6": lambda cwd: seed_loglens(cwd, "bug-ipv6"),
    "P3@bug-percentile": lambda cwd: seed_loglens(cwd, "bug-percentile"),
    "P3@clean +nginx fixture": lambda cwd: seed_loglens(cwd, "clean"),
    # P4 pipeflow
    "P4@clean": lambda cwd: seed_pipeflow(cwd, "clean"),
    "P4@bug-mean": lambda cwd: seed_pipeflow(cwd, "bug-mean"),
    "P4@bug-dedupe": lambda cwd: seed_pipeflow(cwd, "bug-dedupe"),
    "P4@clean +big.csv": lambda cwd: seed_pipeflow(cwd, "clean"),
    "P3@clean + P4@clean": lambda cwd: (
        seed_loglens(cwd, "clean") or seed_pipeflow(cwd, "clean")
    ),
    # P5 keystore
    "P5@clean": lambda cwd: seed_keystore(cwd, "clean"),
    "P5@bug-lru": lambda cwd: seed_keystore(cwd, "bug-lru"),
    "P5@bug-ttl": lambda cwd: seed_keystore(cwd, "bug-ttl"),
    "P5@bug-compact": lambda cwd: seed_keystore(cwd, "bug-compact"),
    "P5@clean +impossible test": lambda cwd: seed_keystore(cwd, "clean"),
    "P5@clean +noise files": lambda cwd: seed_keystore(cwd, "clean"),
    # P6 miniapi
    "P6@clean": lambda cwd: seed_miniapi(cwd, "clean"),
    "P6@bug-pathparse": lambda cwd: seed_miniapi(cwd, "bug-pathparse"),
    "P6@vuln-sqli": lambda cwd: seed_miniapi(cwd, "vuln-sqli"),
    "P6@clean +50 items": lambda cwd: seed_miniapi(cwd, "clean"),
    # Long-horizon final case: no seed + scratch state
    "none + PRD.md + site/ fixture": _seed_empty,
}
# Chain markers — runner reuses prior workspace, no re-seed.
CHAIN_CONTINUE_SEEDS = {"C1-continue", "C2-continue",
                        "P2@v1 (C1-continue C2)"}


# ── check interpreter ─────────────────────────────────────────────────

@dataclass
class CheckResult:
    spec: str
    passed: bool
    detail: str
    kind: str = "exact"  # exact / partial / manual_review / not_supported


def _run_pytest(cwd: Path, timeout: int = 120) -> tuple[int, str, int, int]:
    try:
        r = subprocess.run(
            ["python3", "-m", "pytest", "-q", "--tb=line", "-W", "ignore"],
            cwd=cwd, capture_output=True, timeout=timeout, text=True,
        )
    except subprocess.TimeoutExpired:
        return -1, "pytest timed out", 0, 0
    except Exception as e:
        return -1, f"pytest error: {e!r}", 0, 0
    out = r.stdout + "\n" + r.stderr
    n_pass = sum(int(x) for x in re.findall(r"(\d+)\s+passed", out))
    n_fail = sum(int(x) for x in re.findall(r"(\d+)\s+failed", out))
    last = out.strip().splitlines()[-1] if out.strip() else "(no output)"
    return r.returncode, last, n_pass, n_fail


def _check_green(spec: str, cwd: Path) -> CheckResult:
    m = re.match(r"^green(?:\((\d+|>=\d+)\))?$", spec.strip())
    expected_n: int | None = None
    allow_failures = False  # `>=N` means "≥N pass, don't care about pre-existing failures"
    if m and m.group(1):
        g = m.group(1)
        allow_failures = g.startswith(">=")
        expected_n = int(g.lstrip(">="))
    rc, last, n_pass, n_fail = _run_pytest(cwd)
    # `green(>=N)` is permissive: pre-existing failures (planted seed bugs
    # reserved for debug cases) are OK as long as we still see ≥N passes.
    # `green(N)` (no `>=`) requires a fully-green suite.
    if rc != 0 and not allow_failures:
        return CheckResult(spec, False, f"pytest rc={rc} {last} (passed={n_pass} failed={n_fail})")
    if expected_n is not None and n_pass < expected_n:
        return CheckResult(spec, False, f"pytest green but only {n_pass}/{expected_n} passed")
    return CheckResult(spec, True, f"pytest green: {n_pass} passed (failed={n_fail})")


def _check_cmd_stdout(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: '<cmd> -> 'X'' / '<cmd> -> \"X\"' / '<cmd> prints 'X''.

    Quoted RHS only; unquoted forms (e.g. "-> 5 data rows") go to
    _check_cmd_assertion below.

    Also handles the "prints" verb (e.g. "count prints 'open: 3  done: 2'")
    by treating 'prints' as equivalent to '->'.
    """
    # First try the "prints" / "yields" form
    m = re.match(r"^(.+?)\s+(?:prints|yields(?:\s+rows\s+with)?)\s+['\"](.+?)['\"]\s*$", spec)
    if m:
        # Synthesize a command from the prefix. e.g. for taskvault:
        #   "count prints 'open: 3 done: 2 total: 5'"
        # the prefix "count" isn't a real command — it's the subcommand.
        # Look for a package dir under cwd and run `python -m <pkg> <prefix>`.
        cmd_prefix, expected = m.group(1).strip(), m.group(2)
        if cmd_prefix and not any(cmd_prefix.startswith(p) for p in
                                  ("python", "python3", "pytest", "curl",
                                   "grep", "ls", "cat", "bash")):
            # Try to find the project package
            pkg_dirs = [p for p in cwd.iterdir() if p.is_dir()
                        and (p / "__main__.py").is_file()
                        and not p.name.startswith(".")] if cwd.is_dir() else []
            if pkg_dirs:
                cmd_prefix = f"python3 -m {pkg_dirs[0].name} {cmd_prefix}"
        try:
            r = subprocess.run(
                ["/bin/bash", "-c", cmd_prefix], cwd=cwd,
                capture_output=True, timeout=30, text=True,
            )
        except Exception as e:
            return CheckResult(spec, False, f"run error: {e!r}")
        haystack = (r.stdout or "") + "\n" + (r.stderr or "")
        if expected in haystack:
            return CheckResult(spec, True, f"output contains {expected!r}")
        return CheckResult(
            spec, False,
            f"output did NOT contain {expected!r}; got: {haystack[:140]!r}",
        )
    m = re.match(r"^(.+?)\s*->\s*['\"](.+?)['\"]\s*$", spec)
    if not m:
        return None
    cmd, expected = m.group(1).strip(), m.group(2)
    if "stderr" in cmd:  # handled by separate check
        return None
    try:
        r = subprocess.run(
            ["/bin/bash", "-c", cmd], cwd=cwd,
            capture_output=True, timeout=30, text=True,
        )
    except Exception as e:
        return CheckResult(spec, False, f"run error: {e!r}")
    if expected in r.stdout:
        return CheckResult(spec, True, f"stdout contains {expected!r}")
    return CheckResult(
        spec, False,
        f"stdout did NOT contain {expected!r}; got: {r.stdout[:140]!r}",
    )


_CMD_HINTS = ("python3 ", "python ", "python3.", "pytest ",
              "curl ", "grep ", "ls ", "cat ")


def _check_cmd_assertion(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: '<cmd> -> <expectation>' with UNQUOTED expectation.

    e.g. 'read sales.csv --limit 5 -> 5 data rows'
         '--limit 0 -> all rows'
         'python -m mdparse to-roman 1994 -> MCMXCIV'

    Heuristics:
    - The form must contain ' -> '.
    - LHS treated as a shell command if it starts with `python`/`pytest`/
      `curl` etc, OR if it includes 'sales.csv'/'--' (CLI args). Otherwise
      it's prose like 'new test present' — not interpretable, fall through.
    - Expectation: any digit-token or quoted-look word from the RHS must
      appear in stdout OR stderr.

    Conservative: when we can't synthesize a real command, fall through
    to the not_supported default so we don't FALSELY PASS.
    """
    if " -> " not in spec:
        return None
    lhs, rhs = spec.split(" -> ", 1)
    lhs, rhs = lhs.strip(), rhs.strip()
    if not rhs:
        return None
    # If RHS contains "stderr matches /R/" it's the regex check, skip
    if "stderr matches" in rhs:
        return None
    # If RHS is a quoted string the other check should have matched
    if rhs.startswith(("'", '"')) and rhs.endswith(("'", '"')):
        return None
    # Build a candidate command. We accept LHS as a CLI invocation
    # only if it looks like one.
    looks_like_cmd = (
        any(lhs.startswith(h) for h in _CMD_HINTS)
        or lhs.startswith("python -m ")
        or lhs.startswith("python3 -m ")
        or "--" in lhs
    )
    if not looks_like_cmd:
        return None
    # A spec like '--limit 0 -> all rows' starts with '--' — it's a bare flag,
    # not a runnable command on its own. Fall through so it gets manual_review.
    if lhs.startswith("-"):
        return None
    # When '--' appears in the LHS but the leading word isn't a known binary,
    # the spec is probably a package subcommand ('read sales.csv --limit 5').
    # Prepend 'python3 -m <pkg>' using the same package detection as the
    # quoted-cmd path, so we don't hit bash builtins like 'read'.
    known_bins = tuple(_CMD_HINTS) + ("python -m ", "python3 -m ")
    if not any(lhs.startswith(b) for b in known_bins) and cwd.is_dir():
        pkg_dirs = [p for p in cwd.iterdir() if p.is_dir()
                    and (p / "__main__.py").is_file()
                    and not p.name.startswith(".")]
        if pkg_dirs:
            lhs = f"python3 -m {pkg_dirs[0].name} {lhs}"
    # Substring match: if RHS has a quoted-ish token (digits / capital
    # word / hyphenated identifier), test for it. Otherwise compare
    # the literal RHS.
    needle_match = re.search(r"['\"]([^'\"]+)['\"]|\b(\d[\w./-]*)\b|\b([A-Z]+[A-Z0-9_-]+)\b", rhs)
    needle = needle_match.group(1) or needle_match.group(2) or needle_match.group(3) if needle_match else rhs
    if not needle:
        needle = rhs
    try:
        r = subprocess.run(
            ["/bin/bash", "-c", lhs], cwd=cwd,
            capture_output=True, timeout=30, text=True,
        )
    except subprocess.TimeoutExpired:
        return CheckResult(spec, False, "command timed out")
    except Exception as e:
        return CheckResult(spec, False, f"run error: {e!r}")
    haystack = (r.stdout or "") + "\n" + (r.stderr or "")
    if needle in haystack:
        return CheckResult(spec, True, f"output contains {needle!r}")
    return CheckResult(
        spec, False,
        f"output did NOT contain {needle!r}; got: {haystack[:160]!r}",
    )


def _check_stderr_regex(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: '<cmd> -> stderr matches /R/' or '<cmd> stderr matches /R/'."""
    m = re.match(r"^(.+?)\s+(?:->\s+)?stderr matches\s+/(.+)/\s*$", spec)
    if not m:
        return None
    cmd, pat = m.group(1), m.group(2)
    # Trim a trailing "-> " if the arrow was included in the cmd group
    cmd = re.sub(r"\s*->\s*$", "", cmd).strip()
    # If cmd is bare flags (no program name), prepend the project package
    if cmd.startswith("-") and cwd.is_dir():
        pkg_dirs = [p for p in cwd.iterdir() if p.is_dir()
                    and (p / "__main__.py").is_file()
                    and not p.name.startswith(".")]
        if pkg_dirs:
            cmd = f"python3 -m {pkg_dirs[0].name} {cmd}"
    try:
        r = subprocess.run(
            ["/bin/bash", "-c", cmd], cwd=cwd,
            capture_output=True, timeout=30, text=True,
        )
    except Exception as e:
        return CheckResult(spec, False, f"run error: {e!r}")
    if re.search(pat, r.stderr):
        return CheckResult(spec, True, f"stderr matched /{pat}/")
    return CheckResult(
        spec, False,
        f"stderr did NOT match /{pat}/; got: {r.stderr[:160]!r}",
    )


def _check_path_exists(spec: str, cwd: Path) -> CheckResult | None:
    m = re.match(r"^(\S+)\s+exists(?:\s|$)", spec)
    if not m:
        return None
    p = cwd / m.group(1)
    return CheckResult(spec, p.exists(),
                       f"{p.relative_to(cwd)} {'exists' if p.exists() else 'missing'}")


def _check_import_probe(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'from <pkg> import <name> works/fails' (+ 'still works')."""
    m = re.match(r"^from\s+(\S+)\s+import\s+(\S+)\s+(?:still\s+)?(works|fails)\s*$", spec)
    if not m:
        return None
    pkg, name, mode = m.group(1), m.group(2), m.group(3)
    try:
        r = subprocess.run(
            ["python3", "-c", f"from {pkg} import {name}"],
            cwd=cwd, capture_output=True, timeout=10, text=True,
        )
        rc = r.returncode
    except Exception as e:
        return CheckResult(spec, False, f"probe error: {e!r}")
    if mode == "works":
        return CheckResult(spec, rc == 0,
                           f"import {pkg}.{name} {'ok' if rc==0 else 'failed'}: {r.stderr[:120]}")
    # fails
    return CheckResult(spec, rc != 0,
                       f"import {pkg}.{name} {'failed as required' if rc!=0 else 'unexpectedly worked'}")


def _check_no_token(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: "no '<token>' token in any .py"."""
    m = re.match(r"^no\s+['\"](.+?)['\"]\s+token\s+in\s+any\s+\.py\s*$", spec)
    if not m:
        return None
    tok = m.group(1)
    bad: list[str] = []
    for p in cwd.rglob("*.py"):
        if "legacy_modules" in p.parts:
            continue
        if tok in p.read_text(errors="replace"):
            bad.append(str(p.relative_to(cwd)))
    if bad:
        return CheckResult(spec, False, f"token {tok!r} still in: {bad[:3]}")
    return CheckResult(spec, True, f"token {tok!r} purged from all .py")


def _check_artifact(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'artifact(<path>) <prose ignored>'."""
    m = re.match(r"^artifact\(([^)]+)\)\s*(.*)$", spec)
    if not m:
        return None
    p = cwd / m.group(1).strip()
    if not p.is_file():
        return CheckResult(spec, False, f"artifact {p.name} missing")
    return CheckResult(spec, True, f"artifact {p.name} exists ({p.stat().st_size}B)",
                       kind="exact")


def _check_file_has_strings(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: '<file>.py has X & Y' / '<file> has X and Y'."""
    m = re.match(r"^(\S+\.\w+)\s+has\s+(.+)$", spec)
    if not m:
        return None
    fp = cwd / m.group(1)
    if not fp.is_file():
        return CheckResult(spec, False, f"{m.group(1)} missing")
    needles_raw = re.split(r"\s*&\s*|\s+and\s+", m.group(2))
    txt = fp.read_text(errors="replace")
    missing = [n.strip() for n in needles_raw if n.strip() and n.strip() not in txt]
    if missing:
        return CheckResult(spec, False, f"{m.group(1)} missing: {missing}")
    return CheckResult(spec, True, f"{m.group(1)} contains all needles")


def _check_fix_is_in(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'fix is in <path>' / 'change is in <path>'.

    Cases sometimes name just the leaf (`parser.py`) when the file
    is actually nested under the project package (`mdparse/parser.py`).
    Look at top-level first, then under each one-level subdir.
    Same nested-search pattern as _check_package_dir.
    """
    m = re.match(r"^(?:fix|change|edit) is in\s+(\S+)", spec)
    if not m:
        return None
    name = m.group(1).strip().rstrip(".,")
    candidates = [cwd / name]
    if cwd.is_dir():
        for sub in cwd.iterdir():
            if sub.is_dir() and not sub.name.startswith(".") and sub.name not in (
                    "tests", "__pycache__", ".drydock"):
                candidates.append(sub / name)
    for p in candidates:
        if p.is_file() or p.is_dir():
            return CheckResult(spec, True, f"{p.relative_to(cwd)} present")
    return CheckResult(spec, False, f"{name} missing under cwd or any subdir")


def _check_file_absent(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'old <file> gone', '<file> removed', 'no top-level <file>'."""
    patterns = [
        r"^old\s+(\S+\.\w+)(?:\s+\S+)*\s+(?:gone|removed|deleted)",  # allow intervening words
        r"^(\S+\.\w+)\s+(?:gone|removed|deleted)\s*$",
        r"^no top-level\s+(\S+)\s+",
    ]
    for pat in patterns:
        m = re.match(pat, spec)
        if m:
            p = cwd / m.group(1).strip().rstrip(",.")
            if not p.exists():
                return CheckResult(spec, True, f"{m.group(1)} is absent")
            return CheckResult(spec, False, f"{m.group(1)} still present")
    return None


def _check_all_py_parse(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'all created .py parse' / 'all .py parse'."""
    if not re.match(r"^all\s+(?:created\s+)?\.py\s+parse\s*$", spec):
        return None
    import ast as _ast
    bad: list[str] = []
    for p in cwd.rglob("*.py"):
        if any(part.startswith(".") for part in p.parts):
            continue
        try:
            _ast.parse(p.read_text(errors="replace"))
        except SyntaxError as e:
            bad.append(f"{p.relative_to(cwd)}:{e.lineno}")
    if bad:
        return CheckResult(spec, False, f"SyntaxError in: {bad[:3]}")
    py_count = sum(1 for p in cwd.rglob("*.py")
                   if not any(pt.startswith(".") for pt in p.parts))
    return CheckResult(spec, True, f"all {py_count} .py files parse")


def _check_package_dir(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'X/ is a package with __init__.py'.

    Some cases use a path relative to the project root (e.g.
    `aggregate/` actually means `loglens/aggregate/` in the P3
    seed). Search at cwd first, then any depth-1 subdir, then full
    rglob — accept the first match.
    """
    m = re.match(r"^(\S+/)\s+is a package\b", spec)
    if not m:
        return None
    name = m.group(1).rstrip("/")
    # Try top-level first
    candidates = [cwd / name]
    # Then nested under a one-level subdir (the project package).
    for sub in cwd.iterdir() if cwd.is_dir() else []:
        if sub.is_dir() and not sub.name.startswith(".") and sub.name not in (
                "tests", "__pycache__", ".drydock"):
            candidates.append(sub / name)
    for pkg_dir in candidates:
        if pkg_dir.is_dir() and (pkg_dir / "__init__.py").is_file():
            return CheckResult(
                spec, True,
                f"{pkg_dir.relative_to(cwd)} is a package",
            )
    return CheckResult(
        spec, False,
        f"no '{name}/__init__.py' under cwd or its subdirs",
    )


def _check_multi_path_exists(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'X & Y exist' / 'X & Y exist with ...'.

    When the second path is just a leaf filename (e.g.
    'taskvault/timeparse/relative.py & iso.py'), inherit the
    first path's parent directory so `iso.py` is checked at
    `cwd/taskvault/timeparse/iso.py` instead of `cwd/iso.py`.
    """
    m = re.match(r"^(\S+)\s+&\s+(\S+)\s+exist", spec)
    if not m:
        return None
    p1_str = m.group(1).strip()
    p2_str = m.group(2).strip()
    p1 = cwd / p1_str
    # If p2 is a bare leaf (no slash), try in p1's parent dir too.
    p2_candidates = [cwd / p2_str]
    if "/" not in p2_str and "/" in p1_str:
        parent = (cwd / p1_str).parent
        p2_candidates.append(parent / p2_str)
    missing = []
    if not p1.exists():
        missing.append(p1_str)
    if not any(p.exists() for p in p2_candidates):
        missing.append(p2_str)
    if missing:
        return CheckResult(spec, False, f"missing: {missing}")
    return CheckResult(spec, True, "both paths exist")


def _check_named_test(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'tests/X.py passes' / 'test_X.py passes'."""
    m = re.match(r"^((?:tests?/)?test\S+\.py)\s+passes\s*$", spec)
    if not m:
        return None
    test_path = cwd / m.group(1)
    if not test_path.is_file():
        return CheckResult(spec, False, f"{m.group(1)} missing")
    try:
        r = subprocess.run(
            ["python3", "-m", "pytest", str(test_path), "-q", "--timeout=30", "--tb=no"],
            cwd=cwd, capture_output=True, text=True, timeout=90,
        )
        if r.returncode == 0:
            return CheckResult(spec, True, f"{m.group(1)} passed")
        return CheckResult(spec, False,
                           f"{m.group(1)} failed: {(r.stdout + r.stderr)[-120:]}")
    except Exception as e:
        return CheckResult(spec, False, f"test run error: {e!r}")


def _check_file_defines(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: '<file>.py defines <ClassName>' / '<file> defines <name>'."""
    m = re.match(r"^(\S+\.\w+)\s+defines?\s+([\w.]+)", spec)
    if not m:
        return None
    fp, name = m.group(1), m.group(2).rstrip(",.")
    p = cwd / fp
    if not p.is_file():
        return CheckResult(spec, False, f"{fp} missing")
    txt = p.read_text(errors="replace")
    if re.search(rf"\b(?:class|def)\s+{re.escape(name)}\b", txt):
        return CheckResult(spec, True, f"{fp} defines {name}")
    return CheckResult(spec, False, f"{fp} does NOT define {name}")


def _check_no_fstring_sql(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'no f-string SQL' — verify no .py uses f-strings with SQL keywords."""
    if not re.match(r"^no\s+f.?string\s+SQL\s*$", spec, re.I):
        return None
    fstring_sql_re = re.compile(
        r'f["\'].*\b(?:SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|CREATE|DROP|ALTER)\b',
        re.IGNORECASE,
    )
    for py_file in cwd.rglob("*.py"):
        try:
            txt = py_file.read_text(errors="replace")
        except OSError:
            continue
        if fstring_sql_re.search(txt):
            return CheckResult(spec, False, f"{py_file.relative_to(cwd)} has f-string SQL")
    return CheckResult(spec, True, "no f-string SQL found in .py files")


def _check_file_has_no(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: '<file>.py has no 'X'' / '<file> has no X'."""
    m = re.match(r"^(\S+\.\w+)\s+has\s+no\s+['\"]?([^'\"]+?)['\"]?\s*$", spec)
    if not m:
        return None
    fp, needle = m.group(1), m.group(2).strip()
    p = cwd / fp
    if not p.is_file():
        return CheckResult(spec, False, f"{fp} missing")
    if needle in p.read_text(errors="replace"):
        return CheckResult(spec, False, f"{fp} still contains {needle!r}")
    return CheckResult(spec, True, f"{fp} no longer contains {needle!r}")


def _check_new_test_references(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'new test references <X>' — grep tests/ for X."""
    m = re.match(r"^new test references?\s+(.+)$", spec, re.I)
    if not m:
        return None
    needle = m.group(1).strip().rstrip(".,")
    test_dir = cwd / "tests"
    if not test_dir.is_dir():
        return CheckResult(spec, False, "no tests/ dir")
    for tp in test_dir.rglob("test_*.py"):
        try:
            if needle in tp.read_text(errors="replace"):
                return CheckResult(spec, True, f"{tp.relative_to(cwd)} references {needle!r}")
        except OSError:
            continue
    return CheckResult(spec, False, f"no test file references {needle!r}")


def _check_pyproject_src_layout(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'pyproject.toml with src layout' — verify TOML has src-layout config."""
    if "pyproject.toml" not in spec or "src layout" not in spec:
        return None
    p = cwd / "pyproject.toml"
    if not p.is_file():
        return CheckResult(spec, False, "pyproject.toml missing")
    txt = p.read_text(errors="replace")
    # Recognized shapes: setuptools find with where=["src"], or package-dir = {"" = "src"}
    if re.search(r'where\s*=\s*\[\s*["\']src["\']\s*\]', txt):
        return CheckResult(spec, True, "pyproject.toml has setuptools find with where=['src']")
    if re.search(r'package[-_]?dir\s*=\s*\{\s*["\']{2}\s*[=:]\s*["\']src["\']', txt):
        return CheckResult(spec, True, "pyproject.toml has package-dir ''='src'")
    # Hatch / pdm / poetry equivalents
    if re.search(r'packages\s*=\s*\[[^\]]*src/', txt):
        return CheckResult(spec, True, "pyproject.toml lists src/ in packages")
    if re.search(r'\bsrc[/\\][\w\-]+', txt):
        # Conservative: src/<pkg> appears somewhere meaningful
        return CheckResult(spec, True, "pyproject.toml references a src/<pkg> path")
    return CheckResult(spec, False, "pyproject.toml does NOT configure src layout")


def _check_v2_schema_iso_dates(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'on-disk file is v2 with ISO dues' — read tasks.json, check version+ISO dates."""
    if "v2 with ISO" not in spec:
        return None
    # Find the candidate store file. Tests typically monkeypatch HOME to a tmpdir,
    # but the harness keeps state in the cwd or HOME. Try both.
    candidates = [
        cwd / "tasks.json",
        Path.home() / ".taskvault" / "tasks.json",
    ]
    # Also scan tmpdirs created by the harness
    for tp in cwd.rglob("tasks.json"):
        if tp.is_file():
            candidates.append(tp)
    for p in candidates:
        if not p.is_file():
            continue
        try:
            import json as _json
            data = _json.loads(p.read_text())
        except Exception:
            continue
        if not isinstance(data, dict) or data.get("version") != 2:
            return CheckResult(spec, False, f"{p}: missing version=2")
        tasks = data.get("tasks", [])
        for t in tasks:
            due = (t or {}).get("due")
            if due and isinstance(due, str):
                # MM/DD/YYYY would be the v1 shape; reject those
                if re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", due):
                    return CheckResult(spec, False, f"{p}: task has MM/DD/YYYY due {due!r}")
                if not re.match(r"^\d{4}-\d{2}-\d{2}", due):
                    return CheckResult(spec, False, f"{p}: due {due!r} not ISO")
        return CheckResult(spec, True, f"{p} is v2 with ISO dates ({len(tasks)} tasks)")
    return CheckResult(spec, False, "no tasks.json found to verify")


def _check_v1_bak_preserved(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'tasks.json.v1.bak == original' — verify .v1.bak exists and is parseable as v1."""
    if "v1.bak" not in spec:
        return None
    # Find candidate .v1.bak files
    candidates = list(cwd.rglob("tasks.json.v1.bak"))
    if not candidates:
        return CheckResult(spec, False, "no tasks.json.v1.bak found")
    for p in candidates:
        try:
            import json as _json
            raw = _json.loads(p.read_text())
        except Exception as e:
            return CheckResult(spec, False, f"{p} not valid JSON: {e}")
        # v1 shape: bare list of tasks
        if not isinstance(raw, list):
            return CheckResult(spec, False, f"{p} is not a bare list (not v1 shape)")
        return CheckResult(spec, True, f"{p} preserved as v1 ({len(raw)} tasks)")
    return CheckResult(spec, False, "no v1.bak verified")


def _check_migration_test_exists(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'migration test exists' — grep tests/ for test_*migration* OR v1->v2."""
    if "migration test" not in spec or "exists" not in spec:
        return None
    test_dir = cwd / "tests"
    if not test_dir.is_dir():
        return CheckResult(spec, False, "no tests/ dir")
    for tp in test_dir.rglob("test_*.py"):
        try:
            txt = tp.read_text(errors="replace")
        except OSError:
            continue
        if re.search(r"def\s+test_\w*migrat", txt) or "v1_to_v2" in txt or "v1.bak" in txt:
            return CheckResult(spec, True, f"{tp.relative_to(cwd)} has migration test")
    return CheckResult(spec, False, "no migration-test function found")


def _check_new_test_present(spec: str, cwd: Path, baselines: dict | None = None) -> CheckResult | None:
    """Recognize: 'new test present' — verify tests/ has at least one test file
    newer than the seed baseline, OR that tests/ has more files than baselines reports.

    Without a baseline, fall back to checking that tests/ has a *_added marker file
    OR that any test file's mtime is fresher than the case start time."""
    if spec.strip().lower() != "new test present":
        return None
    test_dir = cwd / "tests"
    if not test_dir.is_dir():
        return CheckResult(spec, False, "no tests/ dir")
    # Use baseline count if present
    baseline_n = (baselines or {}).get("test_file_count") if baselines else None
    files = list(test_dir.rglob("test_*.py"))
    if baseline_n is not None:
        if len(files) > baseline_n:
            return CheckResult(spec, True, f"tests/ has {len(files)} files (baseline was {baseline_n})")
        return CheckResult(spec, False, f"tests/ has {len(files)} files, same as baseline {baseline_n}")
    # No baseline: detect via mtime — a file modified during the case window
    case_start = (baselines or {}).get("case_start_ts") if baselines else None
    if case_start:
        for tp in files:
            if tp.stat().st_mtime > case_start:
                return CheckResult(spec, True, f"{tp.relative_to(cwd)} modified during case")
        return CheckResult(spec, False, "no test file touched during case")
    # Worst case — accept that we can't tell baseline from current state
    return CheckResult(spec, True, f"tests/ has {len(files)} files (no baseline; advisory)",
                       kind="manual_review")


def _check_includes_file(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'includes <file.ext> <string>' — file contains string."""
    m = re.match(r"^includes?\s+(\S+\.\w+)\s+(.+)$", spec)
    if not m:
        return None
    filename, needle = m.group(1), m.group(2).strip()
    candidates = [cwd / filename]
    if cwd.is_dir():
        for sub in cwd.iterdir():
            if sub.is_dir() and not sub.name.startswith("."):
                candidates.append(sub / filename)
    for p in candidates:
        if p.is_file():
            txt = p.read_text(errors="replace")
            if needle in txt:
                return CheckResult(spec, True, f"{filename} contains {needle!r}")
            return CheckResult(spec, False, f"{filename} missing {needle!r}")
    return CheckResult(spec, False, f"{filename} not found under cwd")


def _check_grep_only_in(spec: str, cwd: Path) -> CheckResult | None:
    """Recognize: 'grep: '<term>' only in <file1> and <file2>' / 'grep: '<term>' only in <file1>'."""
    m = re.match(r"^grep:\s+['\"]([^'\"]+)['\"]\s+only in\s+(.+)$", spec)
    if not m:
        return None
    term = m.group(1)
    raw_files = re.split(r"\s+and\s+|,\s*", m.group(2).strip())
    expected_files = {f.strip() for f in raw_files if f.strip()}
    try:
        r = subprocess.run(
            ["grep", "-rl", term, "."],
            cwd=cwd, capture_output=True, timeout=15, text=True,
        )
    except Exception as e:
        return CheckResult(spec, False, f"grep error: {e!r}")
    found_files = {p.lstrip("./") for p in r.stdout.splitlines() if p.strip()}
    expected_norm = {f.lstrip("./") for f in expected_files}
    extra = found_files - expected_norm
    if extra:
        return CheckResult(spec, False, f"term {term!r} also in: {sorted(extra)}")
    return CheckResult(spec, True, f"term {term!r} only in expected files")


def evaluate_check(
    spec: str, cwd: Path, baselines: dict[str, Any],
) -> CheckResult:
    """Dispatch the spec to whichever sub-checker recognizes it."""
    spec = spec.strip()
    for fn in (
        _check_artifact, _check_no_token, _check_import_probe,
        _check_path_exists, _check_stderr_regex, _check_cmd_stdout,
        _check_cmd_assertion, _check_file_has_strings,
        _check_fix_is_in, _check_file_absent, _check_all_py_parse,
        _check_package_dir, _check_multi_path_exists, _check_named_test,
        _check_file_defines, _check_file_has_no, _check_no_fstring_sql,
        _check_new_test_references, _check_pyproject_src_layout,
        _check_v2_schema_iso_dates, _check_v1_bak_preserved,
        _check_migration_test_exists, _check_includes_file, _check_grep_only_in,
    ):
        r = fn(spec, cwd)
        if r is not None:
            return r
    # 'new test present' wants the baselines dict; dispatch separately.
    r = _check_new_test_present(spec, cwd, baselines)
    if r is not None:
        return r
    if re.match(r"^green(\(.+\))?$", spec):
        return _check_green(spec, cwd)
    # readonly(...) is a telemetry assertion handled in the case loop
    if spec.startswith("readonly("):
        return CheckResult(spec, True, "readonly checked separately", kind="manual_review")
    # partial=... is a soft signal
    if spec.startswith("partial"):
        return CheckResult(spec, True, "partial-credit note", kind="partial")
    if spec.startswith("red->green"):
        # Compared against pre-case baseline elsewhere; manual for now.
        return CheckResult(spec, True, "red→green tracked in baselines",
                           kind="manual_review")
    if "files_touched" in spec:
        return CheckResult(spec, True, "files_touched checked separately",
                           kind="manual_review")
    # "states X" — prose assertions about what a doc/artifact says.
    # Cannot auto-verify; treat as advisory so they don't block pass.
    if spec.startswith("states "):
        return CheckResult(spec, True, "prose assertion — manual review",
                           kind="manual_review")
    # "names X" — code style / naming assertions, advisory only.
    if spec.startswith("names "):
        return CheckResult(spec, True, "naming assertion — manual review",
                           kind="manual_review")
    # "stdout identical to no-flag run" — behavioral assertion that
    # the tested flag adds nothing to stdout (only stderr). Requires
    # knowing the original cmd + args, which aren't passed here.
    # Treat as manual_review so it doesn't permanently block pass.
    if "identical to no-flag run" in spec:
        return CheckResult(spec, True, "stdout-identity assertion — manual review",
                           kind="manual_review")
    # Variable-reference assertions: "X == K2", "Y == K3" — the K-variables
    # resolve from artifact content and can't be verified statically.
    if re.search(r"==\s*K\d+", spec):
        return CheckResult(spec, True, "variable-reference assertion — manual review",
                           kind="manual_review")
    # HTTP-verb specs (with or without ->) that include body.X assertions —
    # require a live server to verify; treat as advisory.
    if re.match(r"^(GET|POST|PUT|DELETE|PATCH)\s+/", spec) and "body." in spec:
        return CheckResult(spec, True, "HTTP+body assertion — manual review",
                           kind="manual_review")
    # HTTP-verb prose specs without a curl invocation (no -> and no curl prefix)
    if re.match(r"^(GET|POST|PUT|DELETE|PATCH)\s+/", spec) and " -> " not in spec:
        return CheckResult(spec, True, "HTTP assertion — manual review",
                           kind="manual_review")
    # issubclass / type-hierarchy assertions require a live Python runtime.
    if re.search(r"\bissubclass\b", spec):
        return CheckResult(spec, True, "type-hierarchy assertion — manual review",
                           kind="manual_review")
    # "X references Y" (class/module references) — structural assertions beyond
    # simple grep that need import analysis; treat as advisory.
    if re.search(r"\breferences\s+\w", spec) and not spec.startswith("new test references"):
        return CheckResult(spec, True, "code-reference assertion — manual review",
                           kind="manual_review")
    # Function-call / return-value assertions — require executing code.
    if re.search(r"\breturns\b", spec) and not re.search(r"\s->\s", spec):
        return CheckResult(spec, True, "function-return assertion — manual review",
                           kind="manual_review")
    # Behavioral assertions: phrases describing expected runtime behavior that
    # can't be auto-verified without executing the feature under test.
    # Patterns observed: "X correct", "X intact", "X guarded", "idempotent",
    # "no hallucinated X", "X matches across case", "each mapped to >=1 test",
    # "flags correct for seed", "lists X/Y with correct tags"
    _BEHAVIORAL_PATTERNS = [
        r".*\bcorrect\b.*",
        r".*\bintact\b.*",
        r".*\bguarded\b.*",
        r".*\bidempotent\b.*",
        r"^no\s+hallucinated\b",
        r".*\bmatches across case\b.*",
        r"^each\s+mapped\s+to\b",
        r"^flags\s+correct\b",
        r"^lists\s+\w.+\bwith\s+correct\b",
    ]
    if not re.search(r"\s->\s", spec) and any(
        re.match(p, spec, re.I) for p in _BEHAVIORAL_PATTERNS
    ):
        return CheckResult(spec, True, "behavioral assertion — manual review",
                           kind="manual_review")
    # 2026-05-20: unrecognized shapes used to default to passed=True/
    # kind=manual_review. That produced FALSE POSITIVE passes when a
    # case's only `kind=exact` check was a `green(N)` against a clean
    # seed (which passes trivially because the model did nothing).
    # P4-B1 PASS'd this way despite the model never responding.
    # Default is now passed=False so unimplemented checks block pass.
    return CheckResult(spec, False, "unrecognized check shape — NOT verified",
                       kind="not_supported")


# ── per-case telemetry ────────────────────────────────────────────────

@dataclass
class CaseMetrics:
    id: str = ""
    phase: str = ""
    difficulty: str = ""
    project: str = ""
    chain: str = "none"
    passed: bool = False
    skipped: bool = False
    skip_reason: str = ""
    duration_sec: float = 0.0
    messages_added: int = 0
    max_repeat: int = 0
    files_touched: int = 0
    forbidden_touched: int = 0
    yielded_cleanly: bool = True
    check_results: list[dict] = field(default_factory=list)
    detail: str = ""


_IGNORE_DIRS = {".drydock", "__pycache__", ".pytest_cache", ".git",
                ".mypy_cache", ".ruff_cache"}


def _list_user_files(cwd: Path) -> set[str]:
    """User-visible workspace files. Excludes drydock + build/cache dirs
    that would otherwise inflate files_touched with .pyc noise generated
    by `pytest` runs the model performs inside the case."""
    out: set[str] = set()
    for p in cwd.rglob("*"):
        if not p.is_file():
            continue
        if any(part in _IGNORE_DIRS for part in p.parts):
            continue
        if p.suffix == ".pyc":
            continue
        try:
            out.add(str(p.relative_to(cwd)))
        except ValueError:
            pass
    return out


def _count_tool_call_repetition(messages: list[dict], start_index: int) -> int:
    from collections import Counter
    sigs: Counter = Counter()
    for msg in messages[start_index:]:
        if msg.get("role") != "assistant":
            continue
        for tc in (msg.get("tool_calls") or []):
            f = tc.get("function", {})
            sigs[(f.get("name", "?"), (f.get("arguments", "") or "")[:200])] += 1
    return max(sigs.values()) if sigs else 0


# ── runner ────────────────────────────────────────────────────────────

def _prep_scratch(reuse: Path | None = None) -> Path:
    SCRATCH_ROOT.mkdir(parents=True, exist_ok=True)
    if reuse:
        return reuse
    stamp = time.strftime("%Y%m%d_%H%M%S")
    dest = SCRATCH_ROOT / f"run_{stamp}_{os.getpid() % 10000}"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    trusted = Path.home() / ".drydock" / "trusted_folders.toml"
    trusted.parent.mkdir(parents=True, exist_ok=True)
    text = trusted.read_text() if trusted.exists() else ""
    line = f'"{dest}" = true'
    if line not in text:
        with trusted.open("a") as f:
            f.write(f"\n{line}\n")
    return dest


def _settle(
    child: pexpect.spawn, watcher: SessionWatcher,
    deadline: float, idle_seconds: int, live_index: int,
) -> tuple[int, int, bool]:
    """Returns (last_msg_count, live_index, yielded_cleanly)."""
    quiet_since = time.time()
    try:
        watcher.refresh()
    except Exception:
        pass
    last = len(watcher.messages)
    yielded = False
    while time.time() < deadline:
        time.sleep(3)
        drain_pty(child, seconds=0.5)
        if watcher.session_dir is None:
            try:
                watcher.find_session()
            except Exception:
                pass
        try:
            watcher.refresh()
            now = len(watcher.messages)
        except Exception:
            now = last
        live_index = stream_new_messages(watcher.session_dir, live_index)
        if now > last:
            last = now
            quiet_since = time.time()
        if time.time() - quiet_since > idle_seconds:
            yielded = True
            break
    live_index = stream_new_messages(watcher.session_dir, live_index)
    return last, live_index, yielded


def run_cases(only_ids: list[str] | None = None,
              max_cases: int | None = None) -> dict:
    cases_data = json.loads(CASES_JSON.read_text())
    all_cases = cases_data["cases"]
    if only_ids:
        all_cases = [c for c in all_cases if c["id"] in only_ids]
    if max_cases:
        all_cases = all_cases[:max_cases]

    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    run_stamp = time.strftime("%Y%m%d_%H%M%S")
    run_meta_path = LOG_ROOT / f"{run_stamp}.json"
    pty_log_path = LOG_ROOT / f"{run_stamp}.log"

    meta: dict[str, Any] = {
        "started_at": run_stamp,
        "n_cases_total": len(cases_data["cases"]),
        "n_cases_attempted": len(all_cases),
        "results": [],
    }

    pty_log = pty_log_path.open("w", encoding="utf-8", errors="replace")
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    # 2026-05-23: enable the new drydock improvements by default in the
    # harness so they get exercised across all 52 cases. Operator can
    # override by exporting these vars in the shell that spawns the harness.
    #   - DRYDOCK_AUTOTEST: auto-run pytest after every file edit + inject
    #     RED/GREEN as a system note (targets the "add flag, break default"
    #     wall cases P1-B1, P4-B1, P6-B1, P2-B1, P0-B1, P2-S1, P6-S1).
    #   - DRYDOCK_COMPACT_PAIRS: pair-delete old (assistant tool_call, tool)
    #     pairs instead of stubbing the JSON arguments (fixes the
    #     "truncated history entry used as template" loop pattern).
    env.setdefault("DRYDOCK_AUTOTEST", "1")
    env.setdefault("DRYDOCK_COMPACT_PAIRS", "1")
    # 2026-05-23 (cont): coerce mech_rename usage by intercepting
    # search_replace calls whose SEARCH text appears in ≥2 .py files of
    # the same package — that's a multi-file rename in disguise.
    env.setdefault("DRYDOCK_MULTIFILE_INTERCEPT", "1")

    chain_workspaces: dict[str, Path] = {}  # chain_id → reused workspace
    child: pexpect.spawn | None = None
    cwd: Path | None = None
    pre_case_snapshot: set[str] = set()
    last_message_index = 0
    live_index = 0
    watcher: SessionWatcher | None = None

    def _flush_meta() -> None:
        """Incremental JSON write — operator wants partial results to
        survive a hard kill, since cases.json takes >1h end-to-end."""
        attempted = [r for r in meta["results"] if not r.get("skipped")]
        passed = [r for r in attempted if r.get("passed")]
        meta["score_running"] = f"{len(passed)}/{len(attempted)}"
        meta["skipped_running"] = sum(1 for r in meta["results"] if r.get("skipped"))
        meta["last_update"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        try:
            run_meta_path.write_text(json.dumps(meta, indent=2))
        except Exception:
            pass

    try:
        for case in all_cases:
            cid = case["id"]
            seed_spec = case.get("seed", "none")
            chain = case.get("chain", "none")
            chain_id = chain.split("[")[0] if chain != "none" else None
            metrics = CaseMetrics(
                id=cid, phase=case["phase"],
                difficulty=case["difficulty"],
                project=case["project"], chain=chain,
            )
            t0 = time.time()

            # 2026-05-25: write the case's `check` list to a per-case
            # JSON file and point DRYDOCK_SPEC_CHECK_FILE at it. The
            # agent_loop spec_check hook (commit 70c5be9) will read
            # this when the model emits a text-only "done" message,
            # run the assertions, and inject the failure list as the
            # next prompt instead of "Continue." — blocking unverified
            # done claims for cases with mechanically-checkable specs.
            # Mutates the shared `env` between cases; the next spawn
            # picks up the new path. Cleanup: file is overwritten next
            # case, no leftover state.
            case_check = case.get("check") or []
            spec_path = SCRATCH_ROOT / "spec_checks" / f"{cid}.json"
            spec_path.parent.mkdir(parents=True, exist_ok=True)
            spec_path.write_text(json.dumps(case_check))
            env["DRYDOCK_SPEC_CHECK_FILE"] = str(spec_path)

            # --- workspace + seed ---
            is_continuation = (
                seed_spec in CHAIN_CONTINUE_SEEDS or
                "C1-continue" in seed_spec or "C2-continue" in seed_spec
            )
            if is_continuation and chain_id and chain_id in chain_workspaces:
                cwd = chain_workspaces[chain_id]
                # The current `child` might be from a non-chain case
                # that ran BETWEEN chain steps (e.g. P6-B1 between
                # P1-B1 and P1-C1). Its cwd is miniapi, not mdparse.
                # We can't `cd` drydock at runtime, so kill+respawn
                # in the chain workspace. State retention semantics
                # weaken slightly (no in-process memory between chain
                # steps), but the WORKSPACE state DOES survive on
                # disk — that's what the chain checks actually verify.
                # Observed 2026-05-22: P1-C1 ran in miniapi workspace
                # 5+ iters in a row because of this.
                print(f"[{time.strftime('%H:%M:%S')}] {cid}: continuing chain {chain_id} in {cwd}")
                if child and child.isalive():
                    try:
                        child.sendcontrol("c")
                        time.sleep(0.5)
                        child.terminate(force=True)
                    except Exception:
                        pass
                child = None
                print(f"  [{time.strftime('%H:%M:%S')}] {cid}: respawning drydock in chain cwd")
                child = pexpect.spawn(
                    DRYDOCK_BIN, cwd=str(cwd), encoding="utf-8",
                    timeout=5, dimensions=(40, 140), env=env,
                )
                child.logfile_read = pty_log  # type: ignore[assignment]
                spawned = time.time()
                watcher = SessionWatcher(cwd, since=spawned)
                time.sleep(6)
                drain_pty(child, seconds=2.0)
                _fs_t0 = time.time()
                _marker = cwd / ".drydock" / "current_session.txt"
                for _ in range(30):
                    try:
                        if _marker.is_file():
                            _target = Path(_marker.read_text().strip())
                            if _target.is_dir():
                                watcher.session_dir = _target
                                break
                    except Exception:
                        pass
                    try:
                        if watcher.find_session():
                            break
                    except Exception:
                        pass
                    time.sleep(1)
                _fs_elapsed = time.time() - _fs_t0
                print(f"  find_session(chain): {'OK' if watcher.session_dir else 'TIMEOUT'} "
                      f"in {_fs_elapsed:.1f}s")
                last_message_index = 0
                live_index = 0
            elif seed_spec in SEED_ADAPTERS:
                # Fresh workspace + drydock
                cwd = _prep_scratch()
                SEED_ADAPTERS[seed_spec](cwd)
                if chain_id:
                    chain_workspaces[chain_id] = cwd
                # Close any prior drydock from a different case
                if child and child.isalive():
                    try:
                        child.sendcontrol("c")
                        time.sleep(0.5)
                        child.terminate(force=True)
                    except Exception:
                        pass
                child = None
                print(f"[{time.strftime('%H:%M:%S')}] {cid}: spawning drydock in {cwd}")
                child = pexpect.spawn(
                    DRYDOCK_BIN, cwd=str(cwd), encoding="utf-8",
                    timeout=5, dimensions=(40, 140), env=env,
                )
                child.logfile_read = pty_log  # type: ignore[assignment]
                spawned = time.time()
                watcher = SessionWatcher(cwd, since=spawned)
                time.sleep(6)
                drain_pty(child, seconds=2.0)
                # Aggressive session detection: drydock publishes
                # cwd/.drydock/current_session.txt within 2s of spawn.
                # Don't wait for find_session's mtime/meta-wd checks
                # (which can race with drydock's session_dir mkdir and
                # produce 30s timeouts even though the marker exists).
                # Just hand-set watcher.session_dir as soon as the
                # marker resolves to an existing dir.
                _fs_t0 = time.time()
                _marker = cwd / ".drydock" / "current_session.txt"
                for _ in range(30):
                    try:
                        if _marker.is_file():
                            _target = Path(_marker.read_text().strip())
                            if _target.is_dir():
                                watcher.session_dir = _target
                                break
                    except Exception:
                        pass
                    # fall-back: also try the proper find_session in case
                    # the marker path doesn't exist for some reason
                    try:
                        if watcher.find_session():
                            break
                    except Exception:
                        pass
                    time.sleep(1)
                _fs_elapsed = time.time() - _fs_t0
                print(f"  find_session: {'OK' if watcher.session_dir else 'TIMEOUT'} "
                      f"in {_fs_elapsed:.1f}s "
                      f"({watcher.session_dir.name if watcher.session_dir else 'no marker'})")
                last_message_index = 0
                live_index = 0
            else:
                metrics.skipped = True
                metrics.skip_reason = f"seed not implemented: {seed_spec}"
                meta["results"].append(asdict(metrics))
                _flush_meta()
                print(f"[{time.strftime('%H:%M:%S')}] {cid}: SKIP — {metrics.skip_reason}")
                continue

            if child is None or watcher is None or cwd is None:
                metrics.skipped = True
                metrics.skip_reason = "drydock did not start"
                meta["results"].append(asdict(metrics))
                _flush_meta()
                continue

            pre_case_snapshot = _list_user_files(cwd)
            pre_case_mtimes = {
                p: (cwd / p).stat().st_mtime
                for p in pre_case_snapshot if (cwd / p).is_file()
            }

            # --- send prompt ---
            prompt = case["prompt"]
            print(f"\n=== {cid} ({case['phase']}/{case['difficulty']}) ===")
            for ln in prompt.splitlines()[:6]:
                print(f"  PROMPT: {ln}")
            if len(prompt.splitlines()) > 6:
                print(f"  PROMPT: ... ({len(prompt)} chars total)")
            try:
                accepted = send_prompt_and_confirm(
                    child, prompt, watcher,
                    max_retries=2, wait_per_retry=45.0,
                )
            except Exception as e:
                metrics.detail = f"prompt_send_error: {e!r}"
                meta["results"].append(asdict(metrics))
                _flush_meta()
                continue
            if not accepted:
                metrics.detail = "prompt not accepted"
                meta["results"].append(asdict(metrics))
                _flush_meta()
                continue

            # --- settle ---
            deadline = t0 + int(case.get("deadline_s", 300))
            _, live_index, yielded = _settle(
                child, watcher, deadline, idle_seconds=30,
                live_index=live_index,
            )
            metrics.yielded_cleanly = yielded

            # --- run checks ---
            baselines: dict[str, Any] = {}
            results: list[CheckResult] = []
            for chk in case.get("check", []):
                try:
                    r = evaluate_check(chk, cwd, baselines)
                except Exception as e:
                    r = CheckResult(chk, False, f"check raised: {e!r}")
                results.append(r)
            # Pass requires:
            # - at least one exact check
            # - every exact check passed
            # - no `not_supported` check (those are real assertions we
            #   couldn't interpret; can't claim PASS while they're unmet).
            exact_results = [r for r in results if r.kind == "exact"]
            not_supported = [r for r in results if r.kind == "not_supported"]
            passed = (
                bool(exact_results)
                and all(r.passed for r in exact_results)
                and not not_supported
            )
            metrics.passed = passed
            metrics.check_results = [asdict(r) for r in results]
            metrics.duration_sec = round(time.time() - t0, 1)

            # --- telemetry ---
            try:
                watcher.refresh()
                msgs = watcher.messages
                metrics.messages_added = len(msgs) - last_message_index
                metrics.max_repeat = _count_tool_call_repetition(
                    msgs, last_message_index
                )
                last_message_index = len(msgs)
            except Exception:
                pass

            post_snapshot = _list_user_files(cwd)
            metrics.files_touched = len(post_snapshot ^ pre_case_snapshot)
            # forbidden_touched: anything in case.readonly that has a new mtime
            ro = case.get("readonly", [])
            ro_paths: list[str] = []
            for entry in ro:
                if entry.startswith("everything except"):
                    # Hard to encode generically; treat as "every file not
                    # explicitly listed should be untouched."
                    allowed = re.findall(r"[\w./]+\.\w+", entry)
                    for p in pre_case_mtimes:
                        if p in allowed:
                            continue
                        if (cwd / p).is_file() and (cwd / p).stat().st_mtime > pre_case_mtimes[p] + 0.5:
                            ro_paths.append(p)
                else:
                    target = cwd / entry
                    if target.is_file() and target.stat().st_mtime > pre_case_mtimes.get(entry, 0) + 0.5:
                        ro_paths.append(entry)
            metrics.forbidden_touched = len(ro_paths)

            metrics.detail = "; ".join(
                f"{r.spec[:30]}={'P' if r.passed else 'F'}{r.kind[0]}"
                for r in results
            )[:300]

            print(
                f"[{time.strftime('%H:%M:%S')}] {cid}: "
                f"{'PASS' if passed else 'FAIL'} | "
                f"msgs+={metrics.messages_added} max_repeat={metrics.max_repeat} "
                f"files_changed={metrics.files_touched} "
                f"forbidden={metrics.forbidden_touched} "
                f"yielded={metrics.yielded_cleanly} ({metrics.duration_sec}s)"
            )
            meta["results"].append(asdict(metrics))
            _flush_meta()

        # --- run-level rollups ---
        attempted = [r for r in meta["results"] if not r.get("skipped")]
        passed = [r for r in attempted if r.get("passed")]
        meta["score"] = f"{len(passed)}/{len(attempted)}"
        meta["skipped"] = sum(1 for r in meta["results"] if r.get("skipped"))
        meta["loop_incidents"] = sum(
            1 for r in attempted if (r.get("max_repeat") or 0) >= 4
        )
        meta["drift_incidents"] = sum(
            1 for r in attempted if (r.get("forbidden_touched") or 0) > 0
        )
        meta["deadline_kills"] = sum(
            1 for r in attempted if not r.get("yielded_cleanly")
        )
    finally:
        if child and child.isalive():
            try:
                child.sendcontrol("c")
                time.sleep(0.5)
                child.terminate(force=True)
            except Exception:
                pass
        pty_log.close()

    run_meta_path.write_text(json.dumps(meta, indent=2))
    return meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", nargs="+", default=None,
                    help="Run only these case IDs (e.g. P1-B1 P1-D1)")
    ap.add_argument("--max", type=int, default=None,
                    help="Cap number of cases (after id filter)")
    ap.add_argument("--p1-only", action="store_true",
                    help="Shortcut: run only the 10 P1 (mdparse) cases")
    args = ap.parse_args()

    only_ids = args.ids
    if args.p1_only:
        cases = json.loads(CASES_JSON.read_text())["cases"]
        only_ids = [c["id"] for c in cases if c["project"] == "mdparse"]

    meta = run_cases(only_ids=only_ids, max_cases=args.max)
    print(json.dumps(
        {
            "score": meta.get("score"),
            "skipped": meta.get("skipped"),
            "loop_incidents": meta.get("loop_incidents"),
            "drift_incidents": meta.get("drift_incidents"),
            "deadline_kills": meta.get("deadline_kills"),
            "results": [
                {
                    "id": r["id"], "passed": r.get("passed"),
                    "skipped": r.get("skipped"),
                    "skip_reason": r.get("skip_reason") or None,
                    "msgs": r.get("messages_added"),
                    "max_repeat": r.get("max_repeat"),
                    "files_touched": r.get("files_touched"),
                    "yielded": r.get("yielded_cleanly"),
                    "detail": (r.get("detail") or "")[:80],
                }
                for r in meta.get("results", [])
            ],
        },
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
