"""
NX CLI — FRONTIER-HARNESS PRIMITIVES (parity with the Nexplora code agent).

Pure, dependency-free decision logic the interactive agent loop (nx_cli.run_nx_repl + _cli_agent) wires in so a
long NX run behaves like a frontier harness — the same a-z the Nexplora code agent runs:

  1. VERIFY GATE      — detect the USER PROJECT's build/test/lint from the working dir and, before the agent
                        declares done after changing files, run them + repair on failure. (Detection + interpret
                        here; the loop runs the command via the existing run_command tool.)
  2. TRANSIENT RETRY  — only read-only network tools (browse/search/fetch) retry, and only on a TRANSIENT failure
                        (timeout / connection / 5xx / 429). An action (run_command, a write, an MCP call) never
                        auto-retries — re-running a side effect is unsafe.
  3. SELF-CORRECTION  — after the SAME tool fails N times in a row, inject a targeted nudge so the model changes
                        approach instead of banging on the same failing call.
  4. CONTEXT COMPACT  — when the message transcript grows long, fold the OLDEST complete tool-rounds into one
                        compact progress digest (commands run/failed, files touched, findings) so the run stays
                        bounded WITHOUT breaking function-calling pairing (assistant-with-tool_calls always stays
                        matched to its tool responses — only WHOLE rounds are folded).
  5. RUN COST         — format the per-turn token usage (already captured in cfg["_last_usage"]) into an honest
                        one-line cost read.

Everything here is PURE and unit-tested (tests/test_nx_harness.py). The loop owns the counters + the I/O; this
module owns the decisions. Mirrors lib/code/{verify-gate,self-correct,context-compaction,run-cost}.ts in the
Nexplora repo so NX and Nexplora-code do the same a-z regardless of the model underneath.
"""

from __future__ import annotations

import re
from typing import Any, Optional


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# 1. VERIFY GATE — detect the user project's build/test/lint recipe from the working-dir file listing.
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

# Ordered [build, lint, test]-ish checks per detected stack. The loop runs the FIRST that applies per kind,
# short-circuiting on the first failure (a fast broken-build catch never pays for the slow test suite).
def detect_verify_commands(filenames: list[str]) -> list[dict[str, str]]:
    """Given the top-level filenames of the working dir, return an ordered list of verify checks
    [{"kind","command"}]. Empty when the stack isn't recognized (the agent simply proceeds). Pure."""
    names = {(n or "").strip() for n in filenames}
    checks: list[dict[str, str]] = []

    def has(*n: str) -> bool:
        return any(x in names for x in n)

    # Node / JS / TS — read scripts presence heuristically by lockfile + package.json (the loop confirms the
    # script exists at run time; here we pick the conventional command per package manager).
    if "package.json" in names:
        pm = "pnpm" if has("pnpm-lock.yaml") else "yarn" if has("yarn.lock") else "bun" if has("bun.lockb") else "npm"
        run = f"{pm} run" if pm != "npm" else "npm run"
        # build → lint → test, the frontier order. --if-present so a missing script is a skip, not a hard fail.
        if pm == "npm":
            checks.append({"kind": "build", "command": "npm run build --if-present"})
            checks.append({"kind": "lint", "command": "npm run lint --if-present"})
            checks.append({"kind": "test", "command": "npm test --if-present"})
        else:
            checks.append({"kind": "build", "command": f"{run} build"})
            checks.append({"kind": "lint", "command": f"{run} lint"})
            checks.append({"kind": "test", "command": f"{run} test"})
        return checks

    # Python — prefer pytest when configured, else unittest discovery.
    if has("pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", "tox.ini"):
        if has("pyproject.toml", "pytest.ini", "tox.ini") or "conftest.py" in names:
            checks.append({"kind": "test", "command": "python3 -m pytest -q"})
        else:
            checks.append({"kind": "test", "command": "python3 -m unittest discover"})
        return checks

    # Rust / Go — canonical toolchain commands.
    if "Cargo.toml" in names:
        checks.append({"kind": "build", "command": "cargo build"})
        checks.append({"kind": "test", "command": "cargo test"})
        return checks
    if "go.mod" in names:
        checks.append({"kind": "build", "command": "go build ./..."})
        checks.append({"kind": "test", "command": "go test ./..."})
        return checks
    if "Makefile" in names or "makefile" in names:
        checks.append({"kind": "test", "command": "make test"})
        return checks

    return checks


# A test/build run "passed" only on a clean exit. A timeout is NOT a pass (unproven ≠ proven).
def interpret_verify_result(returncode: Optional[int], stdout: str, stderr: str, timed_out: bool = False) -> dict[str, Any]:
    """Interpret a verify command's outcome. Returns {"passed": bool, "summary": str}. Pure."""
    if timed_out:
        return {"passed": False, "summary": "the check timed out — could not prove it passes"}
    if returncode == 0:
        return {"passed": True, "summary": "passed"}
    tail = _last_lines((stderr or "") + ("\n" + stdout if stdout else ""), 6)
    return {"passed": False, "summary": f"exit {returncode}: {tail}" if tail else f"exit {returncode}"}


def verify_repair_nudge(kind: str, command: str, summary: str, attempt: int) -> str:
    """The repair-feedback message pushed into the transcript when a verify check fails, so the next model turn
    fixes the actual break (in the CODE, not the test)."""
    return (
        f"[NX VERIFY] The project's {kind} check failed (attempt {attempt}): `{command}`\n{summary}\n"
        "Fix the underlying cause in the code (not the test), then it will be re-run. Do not declare done while this fails."
    )


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# 2. TRANSIENT RETRY — only read-only network tools retry, and only on a transient failure code.
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

# Read-only network tools that MAY retry (idempotent reads). Names match the NX tool vocabulary.
RETRYABLE_TOOLS: frozenset[str] = frozenset({
    "browse_url", "browse_research", "browse_task", "web_search", "web_fetch", "fetch_url",
})

# Transient failure signals — a re-run might succeed. A deterministic failure (bad url, 404, no provider) never
# retries (re-running just fails again).
_TRANSIENT_RE = re.compile(
    r"(timed?\s*out|timeout|temporar|connection\s*(reset|refused|error|aborted)|"
    r"\b(5\d\d|429)\b|rate.?limit|too many requests|dns|unreachable|network|ECONN|read timed out)",
    re.I,
)


def is_retryable(tool: str, error_text: Optional[str]) -> bool:
    """True only when `tool` is a read-only network tool AND `error_text` signals a TRANSIENT failure. Pure."""
    if not error_text or tool not in RETRYABLE_TOOLS:
        return False
    return bool(_TRANSIENT_RE.search(str(error_text)))


# Backoff schedule (seconds) for the bounded retry — 2 retries after the first attempt.
RETRY_BACKOFFS: tuple[float, ...] = (0.4, 0.9)


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# 3. SELF-CORRECTION — same-tool-N-failures streak → a targeted nudge (once per streak).
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

FAILURE_ESCALATION_THRESHOLD = 3


def escalation_nudge(tool: str, failures: int) -> str:
    """Targeted advice injected after `tool` fails FAILURE_ESCALATION_THRESHOLD times in a row."""
    prefix = f"[NX SYSTEM] {tool} has failed {failures} times in a row."
    advice = {
        "run_command": " Read the error output above carefully. Check the working directory, that prerequisites "
                       "are installed, and the exact syntax. Try a different command or fix the underlying cause "
                       "before re-running.",
        "run_background": " The command keeps failing to start. Check the binary exists and the working directory "
                          "is right before retrying.",
        "read_file": " The path may be wrong. Use a directory listing to find the correct path before reading again.",
    }.get(tool, " This approach isn't working — change strategy: gather more context or try a different tool "
                "before repeating the same call.")
    return prefix + advice


def track_failure(state: dict[str, Any], tool: str, ok: bool) -> dict[str, Any]:
    """Fold one tool ok/failure into a same-tool consecutive-failure counter. Returns
    {"state": {...}, "nudge": str|None}. A success clears the streak; a different tool restarts it; the nudge fires
    ONCE per streak (then the counter resets so the model gets a fresh streak to act on the advice). Pure — the
    loop holds `state` across rounds. Initial state: {"tool": None, "count": 0}."""
    if ok:
        return {"state": {"tool": None, "count": 0}, "nudge": None}
    count = state.get("count", 0) + 1 if state.get("tool") == tool else 1
    if count >= FAILURE_ESCALATION_THRESHOLD:
        return {"state": {"tool": None, "count": 0}, "nudge": escalation_nudge(tool, count)}
    return {"state": {"tool": tool, "count": count}, "nudge": None}


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# 4. CONTEXT COMPACTION — fold the oldest COMPLETE tool-rounds into one digest, preserving pairing.
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

COMPACTION_MESSAGE_THRESHOLD = 28   # begin compacting once the transcript exceeds this many messages
COMPACTION_KEEP_RECENT_ROUNDS = 4   # always keep this many most-recent tool-rounds verbatim
COMPACTION_DIGEST_CAP = 2000


def _is_assistant_with_tools(m: dict[str, Any]) -> bool:
    return m.get("role") == "assistant" and bool(m.get("tool_calls"))


def _group_rounds(messages: list[dict[str, Any]], start: int) -> list[tuple[int, int]]:
    """Partition messages[start:] into (begin, end_exclusive) spans, each either a complete tool-round
    (assistant-with-tool_calls + its following tool messages) or a single standalone message. Preserves pairing."""
    spans: list[tuple[int, int]] = []
    i = start
    n = len(messages)
    while i < n:
        if _is_assistant_with_tools(messages[i]):
            j = i + 1
            while j < n and messages[j].get("role") == "tool":
                j += 1
            spans.append((i, j))
            i = j
        else:
            spans.append((i, i + 1))
            i += 1
    return spans


def should_compact(messages: list[dict[str, Any]]) -> bool:
    """True when the transcript is long enough that folding older rounds is worthwhile AND there is something
    old enough to fold beyond the recent tail. Pure."""
    if len(messages) <= COMPACTION_MESSAGE_THRESHOLD:
        return False
    # keep messages[0] (system) + preserve the first user task; group the rest into rounds.
    start = _preserve_prefix(messages)
    spans = _group_rounds(messages, start)
    return len(spans) > COMPACTION_KEEP_RECENT_ROUNDS + 1


def _preserve_prefix(messages: list[dict[str, Any]]) -> int:
    """Index after the pinned prefix we never fold: messages[0] (system) and an immediately-following first user
    turn (the task). Returns the index where foldable history begins."""
    i = 0
    n = len(messages)
    if i < n and messages[i].get("role") == "system":
        i += 1
    if i < n and messages[i].get("role") == "user":
        i += 1
    return i


def compact_messages(messages: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], bool]:
    """Fold the oldest complete tool-rounds (leaving the most-recent COMPACTION_KEEP_RECENT_ROUNDS untouched) into
    a SINGLE `{"role":"user","content": digest}` message. Returns (new_messages, did_compact). Pairing-safe: only
    whole rounds are folded, and the digest is a plain user turn (no dangling tool_calls). Pure — returns a new
    list. A no-op (returns the input + False) when nothing is old enough to fold."""
    if not should_compact(messages):
        return messages, False
    start = _preserve_prefix(messages)
    spans = _group_rounds(messages, start)
    fold_spans = spans[: len(spans) - COMPACTION_KEEP_RECENT_ROUNDS]
    if not fold_spans:
        return messages, False
    fold_begin = fold_spans[0][0]
    fold_end = fold_spans[-1][1]
    folded = messages[fold_begin:fold_end]
    digest = {"role": "user", "content": _render_digest(folded)}
    new_messages = messages[:fold_begin] + [digest] + messages[fold_end:]
    return new_messages, True


def _render_digest(folded: list[dict[str, Any]]) -> str:
    """Build a compact progress digest from folded messages: commands run/failed, notable failures, and a count of
    the rounds folded. Bounded by COMPACTION_DIGEST_CAP. Preserves the load-bearing facts a coding agent needs."""
    commands: list[str] = []
    failures: list[str] = []
    tool_calls = 0
    assistant_notes: list[str] = []
    for m in folded:
        role = m.get("role")
        if role == "assistant":
            tool_calls += len(m.get("tool_calls") or [])
            txt = (m.get("content") or "").strip()
            if txt:
                assistant_notes.append(_trim(txt, 160))
        elif role == "tool":
            content = str(m.get("content") or "")
            low = content.lower()
            first = _trim(content, 120)
            if re.search(r"\berror\b|traceback|exit\s*[1-9]|failed|non-zero", low):
                failures.append(first)
            else:
                commands.append(first)
    lines = [f"[progress digest] folded {len(folded)} earlier message(s), {tool_calls} tool call(s):"]
    if commands:
        lines.append("- Did: " + " | ".join(commands[-6:]))
    if failures:
        lines.append("- Failures seen: " + " | ".join(failures[-4:]))
    if assistant_notes:
        lines.append("- Notes: " + " | ".join(assistant_notes[-2:]))
    return _cap("\n".join(lines), COMPACTION_DIGEST_CAP)


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# 5. RUN COST — format per-turn token usage into an honest one-line read.
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def accumulate_usage(acc: Optional[dict[str, Any]], latest: Optional[dict[str, Any]]) -> dict[str, Any]:
    """Sum a stream's usage frame ({prompt, cached, completion}) into a per-turn accumulator. Returns a NEW dict.
    `acc` may be None at turn start. A turn makes several model calls (first stream + between-round re-streams); the
    per-turn cost read reflects the WHOLE turn, not just the last call. Pure.

    (Needed because stream_chat POPs cfg["_last_usage"] for the provider cost-tuner right after each stream, so the
    per-turn cost surface can't read that key directly — the loop accumulates here into its own per-turn key.)"""
    acc = acc or {}
    latest = latest or {}
    return {
        "prompt": _int(acc.get("prompt")) + _int(latest.get("prompt")),
        "cached": _int(acc.get("cached")) + _int(latest.get("cached")),
        "completion": _int(acc.get("completion")) + _int(latest.get("completion")),
    }


def format_run_cost(usage: Optional[dict[str, Any]], cost_usd: Optional[float] = None) -> str:
    """Format cfg["_last_usage"] ({prompt, cached, completion}) into a one-line read, e.g.
    'tokens · 1,240 in (300 cached) · 512 out'. Adds '· $0.0031' when a cost estimate is provided. Empty string
    when there's nothing real to show (never fabricates). Pure."""
    if not usage:
        return ""
    prompt = _int(usage.get("prompt"))
    cached = _int(usage.get("cached"))
    completion = _int(usage.get("completion"))
    if prompt <= 0 and completion <= 0:
        return ""
    inpart = f"{prompt:,} in" + (f" ({cached:,} cached)" if cached > 0 else "")
    out = f"tokens · {inpart} · {completion:,} out"
    if cost_usd is not None and cost_usd > 0:
        out += f" · ${cost_usd:.4f}"
    return out


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# LOOP ADAPTER — one call the agent loop makes BETWEEN tool rounds (keeps the monolith edit to a single line).
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def apply_between_rounds(messages: list[dict[str, Any]], round_results: list[dict[str, Any]], streak_state: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Called between native tool rounds. Folds THIS round's outcome into a same-tool failure streak (appending a
    targeted nudge to `messages` when it fires) and compacts the transcript when it's grown long (pairing-safe).
    Returns (messages, streak_state) — the caller reassigns both because compaction returns a NEW list. Pure aside
    from appending to / replacing `messages`. `streak_state` starts as {"tool": None, "count": 0}."""
    if round_results:
        # Result dicts vary by loop: the REPL native loop uses "success", the agent loop's _trace uses "ok".
        any_ok = any(bool(r.get("success")) or bool(r.get("ok")) for r in round_results)
        # Representative tool of the round for the streak — the last result's tool (a single-tool failing round is
        # the common stuck shape; a mixed round with any success clears the streak below).
        tool = str(round_results[-1].get("tool") or round_results[-1].get("name") or "tool")
        res = track_failure(streak_state, tool, ok=any_ok)
        streak_state = res["state"]
        if res["nudge"]:
            messages = messages + [{"role": "user", "content": res["nudge"]}]
    messages, _ = compact_messages(messages)
    return messages, streak_state


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# helpers
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def _int(v: Any) -> int:
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def _trim(s: str, n: int) -> str:
    t = re.sub(r"\s+", " ", str(s or "")).strip()
    return t if len(t) <= n else t[:n] + "…"


def _cap(s: str, n: int) -> str:
    return s if len(s) <= n else s[:n] + f"\n…[+{len(s) - n} chars]"


def _last_lines(s: str, n: int) -> str:
    lines = [ln for ln in str(s or "").splitlines() if ln.strip()]
    return _trim(" / ".join(lines[-n:]), 400)
