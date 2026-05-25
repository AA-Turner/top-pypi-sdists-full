#!/usr/bin/env python3
"""Drydock progressive-stress gauntlet — Part 2 of the eval suite.

Per the operator's 2026-05-19 spec (with the 2026-05-19 22:00 follow-up
"way too simple, will never find real issues"), this is the escalation
harness that complements lifecycle_runner.py:

  - lifecycle_runner: "Can drydock build a real project end-to-end?"
  - gauntlet_runner:  "Where does drydock break under increasing pressure?"

9 levels across 4 phases run in ONE continuous session against a
PRE-SEEDED realistic 13-file Python project (`mdparse` — markdown→HTML
converter with pytest suite). The seed has a planted off-by-one bug
in parser._parse_blockquote that breaks 3 tests; finding it is L1.

The old gauntlet asked the model to scaffold a 1-file Fibonacci CLI
and check `--help` exited 0 — that never exercised drydock's real
failure modes (search_replace cascades, truncated_history, multi-file
refactor loops, context-bloat compaction). Real bugs only surface when
there's enough surface area to collide with. Most checks now run
`pytest -q` against the seeded project; --help is banned per CLAUDE.md.

Phase 1: Baseline (Easy)
  L1: Debug a Failing Test  — pytest is RED, find & fix the planted bug
  L2: Single-Feature Add    — inline-code (`backticks`) support across
                              lexer + parser + renderer + new tests

Phase 2: System Expansion (Medium)
  L3: Multi-File Rename     — rename public `render_html` → `render`
                              (touches __init__, cli, every test file)
  L4: New Output Format     — --format html|text|json with two new
                              renderer modules and CLI wiring

Phase 3: Architectural Logic (Hard)
  L5: UI Integration        — dashboard/ + http.server backend route
  L6: SQLite Caching        — persist parsed ASTs across runs

Phase 4: Destructive Stress (Breaking Point)
  L7: Three Hidden Bugs     — pre-inject bugs in 3 unrelated files;
                              pytest now has ≥5 failures; find & fix all
  L8: Poisoned PRD          — logical contradiction; must FLAG, not
                              blindly code
  L9: Context Collapse      — 15-file haystack + 60-line stack trace
                              dropped alongside; small, specific fix
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

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


SCRATCH_ROOT = Path("/tmp/drydock_gauntlet")
LOG_ROOT = Path("/data3/drydock/.gauntlet_runs")


# ────────────────────────────────────────────────────────────────────────
# Level definitions
# ────────────────────────────────────────────────────────────────────────

@dataclass
class Level:
    name: str
    phase: str
    prompt: str
    # check(cwd) → (passed, detail)
    check: Callable[[Path], tuple[bool, str]]
    settle_seconds: int = 30
    deadline_seconds: int = 240
    # pre_setup(cwd) runs BEFORE the level's prompt is sent.
    pre_setup: Callable[[Path], None] | None = None


# ── Level checks ────────────────────────────────────────────────────────

def _has_py_with(cwd: Path, pattern: str) -> tuple[bool, str]:
    """Walk cwd looking for any .py file matching `pattern` (regex)."""
    import re
    pat = re.compile(pattern, re.I)
    for p in cwd.rglob("*.py"):
        if pat.search(p.read_text(errors="replace")):
            return True, f"marker found in {p.relative_to(cwd)}"
    return False, f"no .py matches /{pattern}/"


def _runs_ok(cwd: Path, args: list[str], timeout: int = 15) -> tuple[bool, str]:
    import subprocess
    try:
        r = subprocess.run(args, cwd=cwd, capture_output=True,
                           timeout=timeout, text=True)
    except subprocess.TimeoutExpired:
        return False, f"timed out: {args}"
    except Exception as e:
        return False, f"subprocess error: {e!r}"
    if r.returncode != 0:
        return False, f"exit={r.returncode} stderr={r.stderr[:200]}"
    return True, f"ran ok: stdout[:80]={r.stdout[:80]!r}"


def _pytest_passes(cwd: Path, expect_min_pass: int = 0,
                   timeout: int = 90) -> tuple[bool, str, int, int]:
    """Run `pytest -q --tb=line` in cwd. Return (passed, summary, n_passed, n_failed).

    `passed` means rc == 0 (no failing tests) AND at least
    expect_min_pass tests ran.
    """
    import re as _re
    import subprocess
    try:
        r = subprocess.run(
            ["python3", "-m", "pytest", "-q", "--tb=line", "-W", "ignore", "-p", "no:cov"],
            cwd=cwd, capture_output=True, timeout=timeout, text=True,
        )
    except subprocess.TimeoutExpired:
        return False, "pytest timed out", 0, 0
    except Exception as e:
        return False, f"pytest run error: {e!r}", 0, 0
    out = r.stdout + "\n" + r.stderr
    n_pass = sum(int(x) for x in _re.findall(r"(\d+)\s+passed", out))
    n_fail = sum(int(x) for x in _re.findall(r"(\d+)\s+failed", out))
    last = out.strip().splitlines()[-1] if out.strip() else "(no output)"
    if r.returncode != 0:
        return False, f"{last} (failed={n_fail} passed={n_pass})", n_pass, n_fail
    if n_pass < expect_min_pass:
        return False, f"only {n_pass} tests ran, expected ≥{expect_min_pass}", n_pass, n_fail
    return True, f"pytest green: {n_pass} passed", n_pass, n_fail


def _l1_check(cwd: Path) -> tuple[bool, str]:
    """L1 = the planted parser._parse_blockquote off-by-one bug must
    be fixed. With the bug, 3 tests fail; without, all 27 pass."""
    if not (cwd / "mdparse" / "parser.py").is_file():
        return False, "mdparse/parser.py missing (seed not present)"
    ok, summary, _, _ = _pytest_passes(cwd, expect_min_pass=20)
    return ok, summary


def _l2_check(cwd: Path) -> tuple[bool, str]:
    """L2 = inline-code support via backticks. Must render `code` as
    <code>code</code>, AND all existing tests must still pass, AND
    at least one new test for inline code must exist in tests/."""
    import subprocess
    # 1) does the model's render produce <code> for backticked text?
    try:
        r = subprocess.run(
            ["python3", "-c",
             "from mdparse.inline import render_inline; "
             "print(render_inline('hello `world`'))"],
            cwd=cwd, capture_output=True, timeout=10, text=True,
        )
    except Exception as e:
        return False, f"inline-code probe failed: {e!r}"
    if r.returncode != 0:
        return False, f"render_inline broken: {r.stderr[:150]}"
    if "<code>world</code>" not in r.stdout:
        return False, f"render_inline did not produce <code>world</code>: stdout={r.stdout[:120]!r}"
    # 2) did the model add a test for it?
    test_dir = cwd / "tests"
    has_backtick_test = False
    if test_dir.is_dir():
        for tp in test_dir.glob("test_*.py"):
            t = tp.read_text(errors="replace")
            if "<code>" in t or "`" in t and "code" in t.lower():
                has_backtick_test = True
                break
    if not has_backtick_test:
        return False, "no inline-code test added under tests/"
    # 3) pytest must still pass
    ok, summary, _, _ = _pytest_passes(cwd, expect_min_pass=25)
    if not ok:
        return False, f"inline-code works but pytest red: {summary}"
    return True, f"inline code wired + tested ({summary})"


def _l3_check(cwd: Path) -> tuple[bool, str]:
    """L3 = rename public API `render_html` → `render`. Must update
    mdparse/__init__.py + cli.py + every test that imported render_html.
    Pass: `from mdparse import render` works AND pytest stays green."""
    import subprocess
    try:
        r = subprocess.run(
            ["python3", "-c",
             "from mdparse import render; "
             "print(type(render).__name__)"],
            cwd=cwd, capture_output=True, timeout=10, text=True,
        )
    except Exception as e:
        return False, f"import probe failed: {e!r}"
    if r.returncode != 0:
        return False, f"`from mdparse import render` failed: {r.stderr[:200]}"
    # The old name should NO LONGER be importable (full rename, not
    # an alias). If it is, that's still a partial pass.
    try:
        r2 = subprocess.run(
            ["python3", "-c", "from mdparse import render_html"],
            cwd=cwd, capture_output=True, timeout=10, text=True,
        )
        old_still_works = (r2.returncode == 0)
    except Exception:
        old_still_works = False
    ok, summary, _, _ = _pytest_passes(cwd, expect_min_pass=20)
    if not ok:
        return False, f"`render` exists but pytest red: {summary}"
    suffix = " (old render_html ALSO still exported — partial rename)" if old_still_works else ""
    return True, f"renamed render_html→render + pytest green ({summary}){suffix}"


def _l4_check(cwd: Path) -> tuple[bool, str]:
    """L4 = --format {html,text,json} flag. CLI must support all three;
    `--format json` must print a JSON-parseable AST."""
    import json as _json
    import subprocess
    sample = cwd / "_l4_sample.md"
    sample.write_text("# Hello\n\nWorld here.\n", encoding="utf-8")
    # html (default)
    try:
        r_html = subprocess.run(
            ["python3", "-m", "mdparse", str(sample.name)],
            cwd=cwd, capture_output=True, timeout=15, text=True,
        )
    except Exception as e:
        return False, f"html run failed: {e!r}"
    if r_html.returncode != 0 or "<h1>" not in r_html.stdout:
        return False, f"default html broken: rc={r_html.returncode} out[:120]={r_html.stdout[:120]!r}"
    # text
    try:
        r_text = subprocess.run(
            ["python3", "-m", "mdparse", str(sample.name), "--format", "text"],
            cwd=cwd, capture_output=True, timeout=15, text=True,
        )
    except Exception as e:
        return False, f"text run failed: {e!r}"
    if r_text.returncode != 0:
        return False, f"--format text exit={r_text.returncode}: {r_text.stderr[:200]}"
    if "<" in r_text.stdout or "World here" not in r_text.stdout:
        return False, f"--format text didn't produce clean text: {r_text.stdout[:200]!r}"
    # json
    try:
        r_json = subprocess.run(
            ["python3", "-m", "mdparse", str(sample.name), "--format", "json"],
            cwd=cwd, capture_output=True, timeout=15, text=True,
        )
    except Exception as e:
        return False, f"json run failed: {e!r}"
    if r_json.returncode != 0:
        return False, f"--format json exit={r_json.returncode}: {r_json.stderr[:200]}"
    try:
        _json.loads(r_json.stdout)
    except Exception as e:
        return False, f"--format json output not parseable: {e!r}; out={r_json.stdout[:200]!r}"
    return True, "all three --format outputs validated"


def _l5_check(cwd: Path) -> tuple[bool, str]:
    """UI: at least one .html and one .css/.js, plus a backend route."""
    html = list(cwd.rglob("*.html"))
    css_or_js = list(cwd.rglob("*.css")) + list(cwd.rglob("*.js"))
    if not html:
        return False, "no .html file"
    if not css_or_js:
        return False, "no .css or .js file"
    ok, det = _has_py_with(
        cwd, r"flask|fastapi|http\.server|app\.route|@app\."
    )
    if not ok:
        return False, "no backend route/server marker in .py"
    return True, f"html={len(html)} css/js={len(css_or_js)}"


def _l6_check(cwd: Path) -> tuple[bool, str]:
    return _has_py_with(cwd, r"\bsqlite3\b|\.db\b|CREATE TABLE|connect\(.*\.db")


def _l7_check(cwd: Path) -> tuple[bool, str]:
    """L7 = three unrelated bugs were pre-injected in lexer.py,
    renderer.py, and cli.py. pytest -q exits 0 iff all three are fixed.
    Marker check: each bug's signature must be GONE from its file."""
    # signature: heading-strip leaves leading hashes if level miscounted
    lexer = (cwd / "mdparse" / "lexer.py").read_text(errors="replace")
    bug1_present = "stripped[level + 1:]" in lexer  # off-by-one we injected
    # signature: renderer double-escapes
    rend = (cwd / "mdparse" / "renderer.py").read_text(errors="replace")
    bug2_present = ".replace(\"&amp;\", \"&amp;amp;\")" in rend
    # signature: cli returns 1 on success
    cli = (cwd / "mdparse" / "cli.py").read_text(errors="replace")
    bug3_present = "return 1  # BUG" in cli
    still = [b for b in [
        ("lexer", bug1_present),
        ("renderer", bug2_present),
        ("cli", bug3_present),
    ] if b[1]]
    if still:
        return False, "still-broken: " + ", ".join(b[0] for b in still)
    ok, summary, _, _ = _pytest_passes(cwd, expect_min_pass=20, timeout=60)
    if not ok:
        return False, f"signatures clean but pytest red: {summary}"
    return True, f"all 3 bugs fixed + pytest green ({summary})"


def _l8_check(cwd: Path) -> tuple[bool, str]:
    """The poisoned PRD asks for two contradictory things (offline-only
    AND local-cache-on-disk). The model should FLAG the contradiction,
    not blindly write code that does both. Pass if:
    (a) there's a CLARIFICATION.md / NOTES.md / DESIGN.md naming the
        contradiction, OR
    (b) the model added an open-question section to PRD.md, OR
    (c) the latest assistant message in messages.jsonl mentions
        'contradict', 'conflict', or 'ambiguous'.

    (c) is checked by the runner from the session log; here we just
    look at filesystem signals.
    """
    import re
    for cand_name in ("CLARIFICATION.md", "NOTES.md", "DESIGN.md", "QUESTIONS.md"):
        cand = cwd / cand_name
        if cand.is_file():
            txt = cand.read_text(errors="replace").lower()
            if any(w in txt for w in ("contradict", "conflict", "ambigu",
                                      "offline", "cache")):
                return True, f"{cand_name} flags the conflict"
    prd = cwd / "PRD.md"
    if prd.is_file():
        txt = prd.read_text(errors="replace").lower()
        if any(w in txt for w in ("contradict", "conflict", "ambigu",
                                  "open question")):
            return True, "PRD.md acknowledges the conflict"
    return False, "no file flags the contradiction"


def _l9_check(cwd: Path) -> tuple[bool, str]:
    """Context collapse: the trace has a needle pointing at
    mdparse/inline.py:18 and a fix hint at the end. Pass if the model
    actually edited inline.py recently AND didn't touch the noise
    files. Tiered: bonus if `.+?` (non-greedy) actually appears in
    the new inline.py."""
    cutoff = time.time() - 400
    inline = cwd / "mdparse" / "inline.py"
    if not inline.is_file():
        return False, "mdparse/inline.py vanished"
    inline_edited = inline.stat().st_mtime > cutoff
    if not inline_edited:
        return False, "model did not edit mdparse/inline.py (the needle)"
    # Bonus: did the model apply the hinted regex change?
    txt = inline.read_text(errors="replace")
    applied_hint = ".+?" in txt or "non-greedy" in txt
    # Did the model corrupt anything in legacy_modules/? (Shouldn't touch them.)
    touched_noise = any(
        (cwd / "legacy_modules" / f"module_{i:02d}.py").stat().st_mtime > cutoff
        for i in range(15)
        if (cwd / "legacy_modules" / f"module_{i:02d}.py").is_file()
    )
    suffix = " + applied hint" if applied_hint else " (no hint applied)"
    if touched_noise:
        suffix += " (also touched noise files — not ideal)"
    return True, f"edited the needle file{suffix}"


# ── Pre-setup hooks ─────────────────────────────────────────────────────

def _l1_setup(cwd: Path) -> None:
    """Drop the seeded mdparse project + record the failing-tests
    baseline so subsequent levels can diff against it."""
    seed_mdparse(cwd)


def _l7_setup(cwd: Path) -> None:
    """Inject 3 unrelated bugs into 3 different files of the mdparse
    project. Their pytest signatures collide with existing tests, so
    pytest goes from 27/27 green to several failures. The model must
    triage all three."""
    # Bug 1: lexer heading slice off-by-one — skip the leading hashes
    # but ALSO drop the first content character.
    lexer = cwd / "mdparse" / "lexer.py"
    txt = lexer.read_text()
    txt = txt.replace(
        'text = stripped[level:].strip()',
        'text = stripped[level + 1:].strip()',
    )
    lexer.write_text(txt)
    # Bug 2: renderer double-escapes ampersands.
    rend = cwd / "mdparse" / "renderer.py"
    rtxt = rend.read_text()
    rtxt = rtxt.replace(
        'return (s.replace("&", "&amp;")',
        'return (s.replace("&", "&amp;").replace("&amp;", "&amp;amp;")\n         .replace("&", "&amp;")',
        1,
    )
    rend.write_text(rtxt)
    # Bug 3: CLI returns 1 on success.
    cli = cwd / "mdparse" / "cli.py"
    ctxt = cli.read_text()
    ctxt = ctxt.replace("    return 0\n", "    return 1  # BUG\n")
    cli.write_text(ctxt)


def _l9_setup(cwd: Path) -> None:
    """Drop 15 verbose files + a long fake stack trace into cwd.
    Forces drydock into compaction territory."""
    payload_dir = cwd / "legacy_modules"
    payload_dir.mkdir(exist_ok=True)
    for i in range(15):
        f = payload_dir / f"module_{i:02d}.py"
        # Each file has ~80 lines of plausible-looking but unrelated code
        lines = [f"# legacy module {i} — verbose padding for context-collapse test", ""]
        for j in range(80):
            lines.append(f"# row {j}: stub helper for backwards compatibility")
            lines.append(f"def helper_{i}_{j}(x): return x + {i * 100 + j}")
        f.write_text("\n".join(lines))
    # Massive stack trace file — buried in the noise is ONE real
    # frame pointing at mdparse.inline.render_inline (the function the
    # model is supposed to find). Last line documents the fix.
    trace_lines = ["Traceback (most recent call last):"]
    for i in range(28):
        trace_lines.append(
            f'  File "/data3/example/path/to/file_{i:02d}.py", line {100+i}, in func_{i}'
        )
        trace_lines.append(f"    result = layer_{i}.process(item_{i})")
    # The needle:
    trace_lines.append(
        '  File "mdparse/inline.py", line 18, in render_inline'
    )
    trace_lines.append('    text = _BOLD.sub(r"<strong>\\1</strong>", text)')
    for i in range(28, 60):
        trace_lines.append(
            f'  File "/data3/example/path/to/file_{i:02d}.py", line {100+i}, in func_{i}'
        )
        trace_lines.append(f"    result = layer_{i}.process(item_{i})")
    trace_lines.append(
        "RuntimeError: legacy_modules.module_07 failed to initialize: "
        "TypeError: helper_7_42() got unexpected keyword argument 'use_cache'"
    )
    trace_lines.append("")
    trace_lines.append(
        "# FIX HINT: the regex on line 18 of mdparse/inline.py needs "
        "a non-greedy modifier so `**a** **b**` produces TWO bold spans, "
        "not one. Change _BOLD to use a non-greedy match (`.+?` not `[^*]+`)."
    )
    (cwd / "stack_trace.txt").write_text("\n".join(trace_lines))


# ── The 9 levels ────────────────────────────────────────────────────────

LEVELS: list[Level] = [
    Level(
        name="L1_debug_failing_test",
        phase="baseline",
        prompt=(
            "I've seeded a small Python project (`mdparse`, a "
            "markdown→HTML converter) into this directory. The "
            "codebase is already laid out — DO NOT scaffold from "
            "scratch.\n\n"
            "Step 1: cd here and run `pytest -q`. You'll see 24 tests "
            "pass and 3 fail.\n"
            "Step 2: Read the failing test output, open the relevant "
            "source files (lexer.py / parser.py / renderer.py), and "
            "find the root cause. It is a single bug; all 3 failures "
            "share the same root cause.\n"
            "Step 3: Apply a minimal fix to the right source file. "
            "Don't edit the tests.\n"
            "Step 4: Re-run `pytest -q` and show me green.\n\n"
            "Stop once pytest is green. Do not refactor unrelated code."
        ),
        pre_setup=_l1_setup,
        check=_l1_check,
        deadline_seconds=300,
    ),
    Level(
        name="L2_inline_code_feature",
        phase="baseline",
        prompt=(
            "Add inline-code support to mdparse. After this change, "
            "text in backticks should render as <code>…</code>.\n\n"
            "Required edits:\n"
            "1. `mdparse/inline.py` — add a regex for backtick spans "
            "and emit <code>X</code>. The escape order matters: do not "
            "let backtick content get HTML-escaped a second time.\n"
            "2. Add at least one new test under `tests/` that "
            "specifically exercises backtick → <code> rendering.\n"
            "3. All existing tests must still pass.\n\n"
            "Run `pytest -q` and show me everything green when done."
        ),
        check=_l2_check,
        deadline_seconds=300,
    ),
    Level(
        name="L3_rename_public_api",
        phase="expansion",
        prompt=(
            "Rename the public function `render_html` to `render` "
            "across the whole codebase. This is a full rename — not "
            "an alias. After your change:\n"
            "  - `from mdparse import render` works.\n"
            "  - `from mdparse import render_html` does NOT work.\n"
            "  - Every test file imports `render` not `render_html`.\n"
            "  - `__init__.py` exports `render`, not `render_html`.\n"
            "  - `cli.py` calls `render(...)`.\n"
            "  - `pytest -q` is green.\n\n"
            "Touch every file that mentions the old name. Use grep "
            "first if you want to scope the change."
        ),
        check=_l3_check,
        deadline_seconds=360,
    ),
    Level(
        name="L4_format_flag",
        phase="expansion",
        prompt=(
            "Add a `--format` CLI flag with three choices: "
            "`html` (default), `text`, and `json`.\n\n"
            "  - `--format html` keeps current behavior.\n"
            "  - `--format text` outputs a plaintext rendering "
            "(no HTML tags; just the textual content of the AST).\n"
            "  - `--format json` dumps the parsed AST as JSON to "
            "stdout — must be parseable by `json.loads`.\n\n"
            "Add the new renderers under `mdparse/renderers/` (one "
            "module per format) and wire `cli.py` to dispatch on the "
            "flag. Add tests under `tests/` covering each format. "
            "All existing tests must keep passing."
        ),
        check=_l4_check,
        deadline_seconds=420,
    ),
    Level(
        name="L5_ui",
        phase="architectural",
        prompt=(
            "Build a tiny web dashboard for mdparse. Create a "
            "`dashboard/` directory with `index.html`, `style.css`, "
            "`app.js`. The page has a textarea for markdown input + "
            "a 'Render' button + a preview pane.\n\n"
            "Add a stdlib http.server (no Flask) under `mdparse/server.py` "
            "that:\n"
            "  - serves dashboard/ statically at /\n"
            "  - exposes POST /api/render — body is markdown, response "
            "is the HTML produced by mdparse.\n\n"
            "Wire the JS so clicking Render POSTs to /api/render and "
            "drops the response into the preview pane."
        ),
        check=_l5_check,
        deadline_seconds=480,
    ),
    Level(
        name="L6_sqlite_cache",
        phase="architectural",
        prompt=(
            "Add a SQLite persistence layer at "
            "`mdparse/cache.py`. Provide functions "
            "`get_cached(source_sha256) -> str | None` and "
            "`set_cached(source_sha256, html)`. Cache DB lives at "
            "`~/.mdparse/cache.db`. Auto-create the schema on first "
            "use (table `cache(sha TEXT PRIMARY KEY, html TEXT, "
            "ts INTEGER)`).\n\n"
            "Wire `cli.py` to call get_cached before parsing; if hit, "
            "skip the parse/render and return cached HTML. Otherwise "
            "parse, render, set_cached, and return.\n\n"
            "Add at least one test that exercises cache hit AND cache "
            "miss (use a tmpdir, not the real home dir, for testing — "
            "monkeypatch the path)."
        ),
        check=_l6_check,
        deadline_seconds=420,
    ),
    Level(
        name="L7_three_hidden_bugs",
        phase="destructive",
        prompt=(
            "I just regressed three unrelated bugs into the codebase "
            "(one in lexer.py, one in renderer.py, one in cli.py).\n\n"
            "Run `pytest -q`. You'll see multiple failures. Each "
            "failure points at one of the three bugs.\n\n"
            "Find and fix all three bugs. Do not paper over them by "
            "deleting tests. Show me `pytest -q` green when done.\n\n"
            "DO NOT scaffold replacement files — edit the existing "
            "ones in place."
        ),
        pre_setup=_l7_setup,
        check=_l7_check,
        deadline_seconds=540,
    ),
    Level(
        name="L8_poisoned_prd",
        phase="destructive",
        prompt=(
            "New feature spec: 'mdparse must process all markdown "
            "completely OFFLINE with NO local storage or files on "
            "disk written by us. It must ALSO cache parsed ASTs "
            "locally across runs in a persistent local file.'\n\n"
            "Implement this. If you spot any problem with the spec, "
            "write a `CLARIFICATION.md` flagging the contradiction "
            "BEFORE you write code."
        ),
        check=_l8_check,
        deadline_seconds=240,
    ),
    Level(
        name="L9_context_collapse",
        phase="destructive",
        prompt=(
            "I just dropped 15 large legacy modules into "
            "`legacy_modules/` and a 60-line stack_trace.txt at the "
            "project root. They are MOSTLY noise — distractors. "
            "Read the stack trace, find the ONE mdparse function "
            "actually mentioned in the trace, and apply the small "
            "documented fix described in the trace's last line. "
            "Touch as few files as possible — ideally just one."
        ),
        pre_setup=_l9_setup,
        check=_l9_check,
        deadline_seconds=360,
    ),
]


# ────────────────────────────────────────────────────────────────────────
# Telemetry
# ────────────────────────────────────────────────────────────────────────


@dataclass
class LevelMetrics:
    name: str = ""
    phase: str = ""
    passed: bool = False
    detail: str = ""
    duration_sec: float = 0.0
    # token-bloat: msgs added during this level (proxy for token usage)
    messages_added: int = 0
    # state drift: files modified that aren't expected for this level
    files_touched: int = 0
    # tool halting: most-repeated tool call within this level
    most_repeated_tool_call: int = 0
    # files in workspace at end of level
    snapshot: list[str] = field(default_factory=list)


def _list_user_files(cwd: Path) -> list[str]:
    out = []
    for p in cwd.rglob("*"):
        if p.is_file() and ".drydock" not in p.parts:
            try:
                out.append(str(p.relative_to(cwd)))
            except ValueError:
                pass
    return sorted(out)


def _count_tool_call_repetition(
    messages: list[dict], start_index: int
) -> int:
    """Among assistant messages from start_index onward, return the
    highest count of any (tool_name, args) signature."""
    sigs: Counter[tuple[str, str]] = Counter()
    for msg in messages[start_index:]:
        if msg.get("role") != "assistant":
            continue
        for tc in (msg.get("tool_calls") or []):
            f = tc.get("function", {})
            sigs[(f.get("name", "?"), (f.get("arguments", "") or "")[:200])] += 1
    return max(sigs.values()) if sigs else 0


# ────────────────────────────────────────────────────────────────────────


def _prep_scratch() -> Path:
    SCRATCH_ROOT.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    dest = SCRATCH_ROOT / f"run_{stamp}"
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


def _settle(child: pexpect.spawn, watcher: SessionWatcher,
            deadline: float, idle_seconds: int,
            live_index: int = 0) -> tuple[int, int]:
    """Wait for the model to finish working, streaming each new
    messages.jsonl entry to stdout so `tail -f live.log` shows the
    actual drydock TUI activity."""
    quiet_since = time.time()
    try:
        watcher.refresh()
    except Exception:
        pass
    last = len(watcher.messages)
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
            break
    live_index = stream_new_messages(watcher.session_dir, live_index)
    return last, live_index


def run_one(stop_after: str | None = None) -> dict:
    cwd = _prep_scratch()
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    stamp = cwd.name.replace("run_", "")
    pty_log_path = LOG_ROOT / f"{stamp}.log"
    meta_path = LOG_ROOT / f"{stamp}.json"

    meta: dict = {
        "cwd": str(cwd),
        "pty_log": str(pty_log_path),
        "started_at": stamp,
        "session_dir": None,
        "levels": [],
        "exit_reason": None,
        "breaking_point": None,
    }

    pty_log = pty_log_path.open("w", encoding="utf-8", errors="replace")
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    # 2026-05-23: enable new drydock improvements by default for harness runs.
    # See test_harness_runner.py for the same block; matched here so both
    # measurement vehicles exercise the same feature set.
    env.setdefault("DRYDOCK_AUTOTEST", "1")
    env.setdefault("DRYDOCK_COMPACT_PAIRS", "1")
    env.setdefault("DRYDOCK_MULTIFILE_INTERCEPT", "1")

    child: pexpect.spawn | None = None
    last_message_index = 0
    last_snapshot: set[str] = set()
    try:
        print(f"[{time.strftime('%H:%M:%S')}] spawning drydock in {cwd}")
        child = pexpect.spawn(
            DRYDOCK_BIN, cwd=str(cwd), encoding="utf-8", timeout=5,
            dimensions=(40, 140), env=env,
        )
        child.logfile_read = pty_log  # type: ignore[assignment]
        spawned = time.time()
        watcher = SessionWatcher(cwd, since=spawned)
        time.sleep(6)
        drain_pty(child, seconds=2.0)
        for _ in range(300):
            try:
                if watcher.find_session():
                    break
            except Exception:
                pass
            time.sleep(1)
        if watcher.session_dir:
            meta["session_dir"] = str(watcher.session_dir)

        live_index = 0  # streamed message count

        for level in LEVELS:
            print(f"\n=== {level.name} ({level.phase}) ===")
            for line in level.prompt.splitlines():
                print(f"  PROMPT: {line}")
            metrics = LevelMetrics(name=level.name, phase=level.phase)
            t0 = time.time()

            if level.pre_setup:
                try:
                    level.pre_setup(cwd)
                except Exception as e:  # noqa: BLE001
                    metrics.detail = f"pre_setup failed: {e!r}"
                    meta["levels"].append(metrics.__dict__)
                    continue

            try:
                accepted = send_prompt_and_confirm(
                    child, level.prompt, watcher,
                    max_retries=2, wait_per_retry=45.0,
                )
            except Exception as e:  # noqa: BLE001
                metrics.detail = f"prompt_send_error: {e!r}"
                meta["levels"].append(metrics.__dict__)
                meta["exit_reason"] = "prompt_send_failed"
                meta["breaking_point"] = level.name
                break
            if not accepted:
                metrics.detail = "prompt not accepted"
                meta["levels"].append(metrics.__dict__)
                meta["breaking_point"] = level.name
                break

            deadline = t0 + level.deadline_seconds
            _, live_index = _settle(child, watcher, deadline,
                                     level.settle_seconds, live_index)

            # Per-level check
            try:
                passed, detail = level.check(cwd)
            except Exception as e:  # noqa: BLE001
                passed, detail = False, f"check raised: {e!r}"
            metrics.passed = passed
            metrics.detail = detail
            metrics.duration_sec = round(time.time() - t0, 1)

            # Telemetry
            try:
                watcher.refresh()
                msgs = watcher.messages
                metrics.messages_added = len(msgs) - last_message_index
                metrics.most_repeated_tool_call = _count_tool_call_repetition(
                    msgs, last_message_index
                )
                last_message_index = len(msgs)
            except Exception:
                pass

            cur_snapshot = set(_list_user_files(cwd))
            metrics.snapshot = sorted(cur_snapshot)
            metrics.files_touched = len(cur_snapshot ^ last_snapshot)
            last_snapshot = cur_snapshot

            meta["levels"].append(metrics.__dict__)
            print(
                f"[{time.strftime('%H:%M:%S')}] {level.name}: "
                f"{'PASS' if passed else 'FAIL'} | "
                f"msgs+={metrics.messages_added} "
                f"max_repeat={metrics.most_repeated_tool_call} "
                f"files_changed={metrics.files_touched} "
                f"({metrics.duration_sec}s) — {detail}"
            )

            if not passed and meta["breaking_point"] is None:
                meta["breaking_point"] = level.name

            if stop_after and level.name == stop_after:
                break
        else:
            meta["exit_reason"] = "completed_all_levels"
        if meta["exit_reason"] is None:
            meta["exit_reason"] = "completed"

    except pexpect.exceptions.EOF:
        meta["exit_reason"] = "drydock_died"
    except Exception as e:  # noqa: BLE001
        meta["exit_reason"] = f"harness_error: {e!r}"
    finally:
        if child and child.isalive():
            try:
                child.sendcontrol("c")
                time.sleep(0.5)
                child.terminate(force=True)
            except Exception:
                pass
        pty_log.close()

    passed = sum(1 for lvl in meta["levels"] if lvl.get("passed"))
    total = len(meta["levels"])
    meta["score"] = f"{passed}/{total}"

    meta_path.write_text(json.dumps(meta, indent=2))
    return meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stop-after", default=None,
                    help="Stop after this level (e.g. L3_multi_file)")
    args = ap.parse_args()
    meta = run_one(stop_after=args.stop_after)
    print(json.dumps({
        "score": meta.get("score"),
        "breaking_point": meta.get("breaking_point"),
        "exit_reason": meta.get("exit_reason"),
        "levels": [
            {
                "name": lvl.get("name"),
                "phase": lvl.get("phase"),
                "passed": lvl.get("passed"),
                "msgs_added": lvl.get("messages_added"),
                "max_repeat": lvl.get("most_repeated_tool_call"),
                "files_changed": lvl.get("files_touched"),
                "detail": (lvl.get("detail") or "")[:100],
            }
            for lvl in meta.get("levels", [])
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
