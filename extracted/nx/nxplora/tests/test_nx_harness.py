"""
NX CLI — frontier-harness primitives (nx_harness) unit tests.

Proves the pure decisions the agent loop wires in: project verify detection + result interpretation, transient
retry classification, same-tool self-correction streaks, context compaction (with the load-bearing FUNCTION-CALLING
PAIRING invariant — a fold never orphans a tool message), and per-turn cost formatting.

Run: python3 tests/test_nx_harness.py   (or: python3 -m unittest tests.test_nx_harness)
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nx_harness import (  # noqa: E402
    detect_verify_commands,
    interpret_verify_result,
    verify_repair_nudge,
    is_retryable,
    RETRYABLE_TOOLS,
    track_failure,
    escalation_nudge,
    FAILURE_ESCALATION_THRESHOLD,
    should_compact,
    compact_messages,
    COMPACTION_MESSAGE_THRESHOLD,
    COMPACTION_KEEP_RECENT_ROUNDS,
    format_run_cost,
    accumulate_usage,
    apply_between_rounds,
)


# ── 1. verify gate detection ────────────────────────────────────────────────────────────────────────────────
class TestVerifyDetection(unittest.TestCase):
    def test_node_npm_build_lint_test_order(self):
        cmds = detect_verify_commands(["package.json", "src", "README.md"])
        kinds = [c["kind"] for c in cmds]
        self.assertEqual(kinds, ["build", "lint", "test"])
        self.assertIn("npm run build", cmds[0]["command"])
        self.assertIn("npm test", cmds[2]["command"])

    def test_node_pnpm_lockfile_switches_pm(self):
        cmds = detect_verify_commands(["package.json", "pnpm-lock.yaml"])
        self.assertTrue(all(c["command"].startswith("pnpm run") for c in cmds))

    def test_python_pytest_when_configured(self):
        cmds = detect_verify_commands(["pyproject.toml", "conftest.py"])
        self.assertEqual(len(cmds), 1)
        self.assertIn("pytest", cmds[0]["command"])

    def test_python_unittest_fallback(self):
        cmds = detect_verify_commands(["setup.py", "requirements.txt"])
        self.assertIn("unittest", cmds[0]["command"])

    def test_rust_and_go(self):
        self.assertIn("cargo", detect_verify_commands(["Cargo.toml"])[0]["command"])
        self.assertIn("go build", detect_verify_commands(["go.mod"])[0]["command"])

    def test_unknown_stack_returns_empty(self):
        self.assertEqual(detect_verify_commands(["notes.txt", "photo.png"]), [])


class TestVerifyInterpret(unittest.TestCase):
    def test_exit_zero_passes(self):
        r = interpret_verify_result(0, "ok", "")
        self.assertTrue(r["passed"])

    def test_timeout_is_not_a_pass(self):
        r = interpret_verify_result(0, "", "", timed_out=True)
        self.assertFalse(r["passed"])

    def test_nonzero_fails_with_tail(self):
        r = interpret_verify_result(1, "running", "AssertionError: boom")
        self.assertFalse(r["passed"])
        self.assertIn("exit 1", r["summary"])
        self.assertIn("boom", r["summary"])

    def test_repair_nudge_mentions_kind_and_code_not_test(self):
        n = verify_repair_nudge("test", "npm test", "exit 1: 2 failing", 1)
        self.assertIn("test check failed", n)
        self.assertIn("in the code (not the test)", n)


# ── 2. transient retry ──────────────────────────────────────────────────────────────────────────────────────
class TestRetry(unittest.TestCase):
    def test_readonly_net_tool_retries_on_transient(self):
        self.assertTrue(is_retryable("browse_url", "Read timed out"))
        self.assertTrue(is_retryable("web_search", "Connection reset by peer"))
        self.assertTrue(is_retryable("fetch_url", "HTTP 503 Service Unavailable"))
        self.assertTrue(is_retryable("browse_research", "429 Too Many Requests"))

    def test_deterministic_failure_never_retries(self):
        self.assertFalse(is_retryable("browse_url", "404 Not Found"))
        self.assertFalse(is_retryable("fetch_url", "invalid url"))

    def test_action_tools_never_retry_even_on_transient(self):
        for t in ("run_command", "run_background", "write_file", "mcp"):
            self.assertFalse(is_retryable(t, "timeout"), f"{t} must never auto-retry")

    def test_empty_error_never_retries(self):
        self.assertFalse(is_retryable("browse_url", None))
        self.assertFalse(is_retryable("browse_url", ""))

    def test_retryable_set_is_readonly_net_only(self):
        self.assertIn("browse_url", RETRYABLE_TOOLS)
        self.assertNotIn("run_command", RETRYABLE_TOOLS)


# ── 3. self-correction ──────────────────────────────────────────────────────────────────────────────────────
class TestSelfCorrect(unittest.TestCase):
    def test_streak_fires_nudge_once_at_threshold_then_resets(self):
        state = {"tool": None, "count": 0}
        nudges = []
        for _ in range(FAILURE_ESCALATION_THRESHOLD):
            r = track_failure(state, "run_command", ok=False)
            state = r["state"]
            if r["nudge"]:
                nudges.append(r["nudge"])
        self.assertEqual(len(nudges), 1)
        self.assertIn("run_command has failed", nudges[0])
        self.assertEqual(state, {"tool": None, "count": 0})  # reset after firing

    def test_success_clears_streak(self):
        state = {"tool": "run_command", "count": 2}
        r = track_failure(state, "run_command", ok=True)
        self.assertEqual(r["state"], {"tool": None, "count": 0})
        self.assertIsNone(r["nudge"])

    def test_different_tool_restarts_streak(self):
        state = {"tool": "run_command", "count": 2}
        r = track_failure(state, "read_file", ok=False)
        self.assertEqual(r["state"], {"tool": "read_file", "count": 1})
        self.assertIsNone(r["nudge"])

    def test_nudge_is_tool_specific(self):
        self.assertIn("working directory", escalation_nudge("run_command", 3))
        self.assertIn("change strategy", escalation_nudge("some_other_tool", 3))


# ── 4. context compaction (pairing-safe) ────────────────────────────────────────────────────────────────────
def _round(text, cmd, out, ok=True):
    """A complete tool-round: assistant-with-tool_calls + its tool response."""
    return [
        {"role": "assistant", "content": text, "tool_calls": [{"id": "c", "type": "function", "function": {"name": "run_command", "arguments": "{}"}}]},
        {"role": "tool", "tool_call_id": "c", "content": out if ok else f"error: {out} (exit 1)"},
    ]


def _transcript(n_rounds):
    msgs = [{"role": "system", "content": "sys"}, {"role": "user", "content": "the task"}]
    for i in range(n_rounds):
        msgs += _round(f"step {i}", f"cmd {i}", f"out {i}", ok=(i % 4 != 0))
    return msgs


def _pairing_ok(messages):
    """Every maximal run of tool messages must be immediately preceded by an assistant-with-tool_calls."""
    for i, m in enumerate(messages):
        if m.get("role") == "tool":
            prev = messages[i - 1] if i > 0 else None
            # the tool msg is valid if the previous is an assistant-with-tool_calls OR another tool msg
            if not (prev and (prev.get("role") == "tool" or (prev.get("role") == "assistant" and prev.get("tool_calls")))):
                return False
    return True


class TestCompaction(unittest.TestCase):
    def test_below_threshold_does_not_compact(self):
        msgs = _transcript(2)
        self.assertLessEqual(len(msgs), COMPACTION_MESSAGE_THRESHOLD)
        self.assertFalse(should_compact(msgs))
        out, did = compact_messages(msgs)
        self.assertFalse(did)
        self.assertEqual(out, msgs)

    def test_long_transcript_compacts_and_preserves_pairing(self):
        msgs = _transcript(20)  # 2 + 40 = 42 messages, 20 rounds
        self.assertTrue(should_compact(msgs))
        self.assertTrue(_pairing_ok(msgs), "fixture itself must be paired")
        out, did = compact_messages(msgs)
        self.assertTrue(did)
        self.assertLess(len(out), len(msgs))
        self.assertTrue(_pairing_ok(out), "compaction MUST NOT orphan a tool message")

    def test_preserves_system_and_first_user_and_recent_rounds(self):
        msgs = _transcript(20)
        out, _ = compact_messages(msgs)
        self.assertEqual(out[0]["role"], "system")
        self.assertEqual(out[1]["role"], "user")
        self.assertEqual(out[1]["content"], "the task")
        # the digest is a single user turn right after the preserved prefix
        self.assertEqual(out[2]["role"], "user")
        self.assertIn("progress digest", out[2]["content"])
        # the last KEEP_RECENT_ROUNDS rounds survive verbatim → the final message is the last round's tool result
        self.assertEqual(out[-1]["role"], "tool")
        self.assertIn("out 19", out[-1]["content"])

    def test_digest_captures_failures(self):
        msgs = _transcript(20)  # rounds 0,4,8,12,16 fail (i % 4 == 0)
        out, _ = compact_messages(msgs)
        digest = out[2]["content"]
        self.assertIn("Failures seen", digest)

    def test_idempotent_enough_after_one_fold(self):
        # one fold should bring it under the fold-again bar (recent tail preserved) — no infinite compaction
        msgs = _transcript(20)
        out1, did1 = compact_messages(msgs)
        out2, did2 = compact_messages(out1)
        self.assertTrue(did1)
        self.assertFalse(did2, "a single fold should leave only the recent tail + digest, not re-fold")


# ── 5. run cost ─────────────────────────────────────────────────────────────────────────────────────────────
class TestRunCost(unittest.TestCase):
    def test_formats_tokens_with_cached_and_cost(self):
        s = format_run_cost({"prompt": 1240, "cached": 300, "completion": 512}, cost_usd=0.0031)
        self.assertIn("1,240 in", s)
        self.assertIn("300 cached", s)
        self.assertIn("512 out", s)
        self.assertIn("$0.0031", s)

    def test_omits_cached_and_cost_when_absent(self):
        s = format_run_cost({"prompt": 100, "completion": 50})
        self.assertIn("100 in", s)
        self.assertNotIn("cached", s)
        self.assertNotIn("$", s)

    def test_empty_when_no_real_usage(self):
        self.assertEqual(format_run_cost(None), "")
        self.assertEqual(format_run_cost({"prompt": 0, "completion": 0}), "")

    def test_accumulate_usage_sums_a_turns_streams(self):
        # a turn makes several model calls; the per-turn total is the sum (the fix for the dead-wired cost primitive)
        acc = accumulate_usage(None, {"prompt": 100, "cached": 10, "completion": 40})
        acc = accumulate_usage(acc, {"prompt": 250, "cached": 30, "completion": 80})
        self.assertEqual(acc, {"prompt": 350, "cached": 40, "completion": 120})
        # and it renders through format_run_cost
        self.assertIn("350 in", format_run_cost(acc))
        self.assertIn("120 out", format_run_cost(acc))

    def test_accumulate_usage_tolerates_none_and_missing_keys(self):
        self.assertEqual(accumulate_usage(None, None), {"prompt": 0, "cached": 0, "completion": 0})
        self.assertEqual(accumulate_usage({"prompt": 5}, {"completion": 3}), {"prompt": 5, "cached": 0, "completion": 3})


# ── loop adapter (between rounds) ───────────────────────────────────────────────────────────────────────────
class TestBetweenRounds(unittest.TestCase):
    def test_failing_round_advances_streak_and_eventually_nudges(self):
        msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "t"}]
        streak = {"tool": None, "count": 0}
        fired = False
        for _ in range(FAILURE_ESCALATION_THRESHOLD):
            msgs, streak = apply_between_rounds(msgs, [{"tool": "run_command", "success": False}], streak)
            if any("[NX SYSTEM]" in (m.get("content") or "") for m in msgs):
                fired = True
        self.assertTrue(fired, "a same-tool failure streak must inject a nudge")

    def test_successful_round_clears_streak_no_nudge(self):
        msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "t"}]
        streak = {"tool": "run_command", "count": 2}
        msgs, streak = apply_between_rounds(msgs, [{"tool": "run_command", "success": True}], streak)
        self.assertEqual(streak, {"tool": None, "count": 0})
        self.assertFalse(any("[NX SYSTEM]" in (m.get("content") or "") for m in msgs))

    def test_compacts_a_long_transcript(self):
        msgs = _transcript(20)
        before = len(msgs)
        msgs, _ = apply_between_rounds(msgs, [{"tool": "run_command", "success": True}], {"tool": None, "count": 0})
        self.assertLess(len(msgs), before)
        self.assertTrue(_pairing_ok(msgs))

    def test_no_results_is_a_noop_on_streak(self):
        msgs = [{"role": "system", "content": "s"}]
        streak = {"tool": "x", "count": 1}
        out, st = apply_between_rounds(msgs, [], streak)
        self.assertEqual(st, streak)

    def test_agent_loop_trace_shape_uses_ok_key(self):
        # the _cli_agent loop's _trace entries use "ok"/"tool" (not "success"); a success must clear the streak
        msgs = [{"role": "system", "content": "s"}]
        streak = {"tool": "mcp", "count": 2}
        _, st = apply_between_rounds(msgs, [{"tool": "mcp", "ok": True}], streak)
        self.assertEqual(st, {"tool": None, "count": 0})


if __name__ == "__main__":
    unittest.main()
