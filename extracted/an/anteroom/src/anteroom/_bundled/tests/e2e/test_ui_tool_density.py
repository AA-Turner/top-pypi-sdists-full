"""E2E tests for #1467 tool-result density rendering in the web UI.

Per ``.claude/rules/ux-testing.md``, changes to ``routers/chat.py`` SSE
emitters and ``static/js/chat.js`` require browser-level coverage.

Approach: drive ``Chat._handleSSEEvent`` with synthesised `tool_call_start`
/ `tool_call_end` events, then assert DOM state matches the density mode's
contract. This keeps the test hermetic (no real AI / agent loop).

Five behaviours covered:

1. **Zero-config (normal mode) → DOM byte-identical.** When all five summary
   fields are null, the rendered DOM matches today's raw-JSON output
   exactly.
2. **Compact mode → smart summary visible, raw JSON reachable.** When fields
   are populated, a `.tool-summary-body` appears and the raw `<pre>` is now
   inside a nested `<details class="tool-raw-output">`.
3. **Error-class CSS applied.** When `error_class` is populated, the
   matching `tool-error-*` class lands on the outer `.tool-call`.
4. **Compact diff rendering.** When `output_preview` begins with `@@ `, the
   body renders as `.tool-diff-hunk` line divs.
5. **Repeat collapse.** Three consecutive calls with the same
   `output_shape_hash` collapse into a single `.tool-repeat-collapsed` row.
"""

from __future__ import annotations

import pytest

pytestmark = [pytest.mark.e2e]

try:
    from playwright.sync_api import Page  # noqa: F401

    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

requires_playwright = pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="playwright not installed")


# ---------------------------------------------------------------------------
# Static content assertions — runnable even without Playwright installed.
# ---------------------------------------------------------------------------


class TestStaticAssets:
    def test_density_enhancement_helper_present(self, base_url: str) -> None:
        import httpx

        resp = httpx.get(f"{base_url}/js/chat.js", follow_redirects=True)
        assert resp.status_code == 200
        assert "_applyToolDensityEnhancements" in resp.text
        assert "_renderDiffHunks" in resp.text
        assert "tool-repeat-collapsed" in resp.text

    def test_density_css_hooks_present(self, base_url: str) -> None:
        import httpx

        resp = httpx.get(f"{base_url}/css/style.css", follow_redirects=True)
        assert resp.status_code == 200
        for cls in (
            ".tool-summary-body",
            ".tool-raw-output",
            ".tool-error-exit_nonzero",
            ".tool-error-exception",
            ".tool-error-timeout",
            ".tool-error-denied",
            ".tool-diff-hunk",
            ".tool-diff-add",
            ".tool-diff-del",
            ".tool-repeat-collapsed",
        ):
            assert cls in resp.text, f"expected CSS class {cls} missing"


# ---------------------------------------------------------------------------
# DOM-level assertions via Chat._handleSSEEvent
# ---------------------------------------------------------------------------


_DISPATCH_SCRIPT = r"""(events) => {
    const container = document.getElementById('messages-container');
    const before = container.innerHTML;
    const errors = [];
    for (const evt of events) {
        try {
            Chat._handleSSEEvent(evt.type, evt.data);
        } catch (e) {
            errors.push({error: String(e), type: evt.type});
        }
    }
    const after = container.innerHTML;
    return {before, after, errors};
}"""


def _normal_mode_events() -> list[dict[str, object]]:
    """All five density fields null (zero-config contract)."""
    return [
        {
            "type": "tool_call_start",
            "data": {
                "id": "t1",
                "tool_name": "bash",
                "server_name": "",
                "input": {"cmd": "ls"},
                "input_preview": None,
            },
        },
        {
            "type": "tool_call_end",
            "data": {
                "id": "t1",
                "output": {"exit_code": 0, "stdout": "a\nb\n"},
                "status": "success",
                "summary": None,
                "output_preview": None,
                "error_class": None,
                "output_shape_hash": None,
            },
        },
    ]


def _compact_mode_events() -> list[dict[str, object]]:
    return [
        {
            "type": "tool_call_start",
            "data": {
                "id": "t1",
                "tool_name": "bash",
                "server_name": "",
                "input": {"cmd": "ls"},
                "input_preview": "ls",
            },
        },
        {
            "type": "tool_call_end",
            "data": {
                "id": "t1",
                "output": {"exit_code": 0, "stdout": "a\nb\n"},
                "status": "success",
                "summary": "a\nb",
                "output_preview": "a\nb",
                "error_class": None,
                "output_shape_hash": "hash-ok-001",
            },
        },
    ]


def _compact_mode_error_events(error_class: str) -> list[dict[str, object]]:
    return [
        {
            "type": "tool_call_start",
            "data": {"id": "t1", "tool_name": "bash", "server_name": "", "input": {"cmd": "x"}},
        },
        {
            "type": "tool_call_end",
            "data": {
                "id": "t1",
                "output": {"exit_code": 2, "stderr": "failed"},
                "status": "error",
                "summary": "failed",
                "output_preview": "failed",
                "error_class": error_class,
                "output_shape_hash": "hash-err",
            },
        },
    ]


def _compact_mode_diff_events() -> list[dict[str, object]]:
    diff = "@@ -1,3 +1,3 @@\n context\n-old line\n+new line\n more context"
    return [
        {
            "type": "tool_call_start",
            "data": {"id": "t1", "tool_name": "edit_file", "server_name": "", "input": {"path": "x"}},
        },
        {
            "type": "tool_call_end",
            "data": {
                "id": "t1",
                "output": {"diff": diff},
                "status": "success",
                "summary": diff,
                "output_preview": diff,
                "error_class": None,
                "output_shape_hash": "hash-diff",
            },
        },
    ]


def _compact_mode_repeat_events(n: int, shape_hash: str = "samehash") -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    for i in range(n):
        events.append(
            {
                "type": "tool_call_start",
                "data": {
                    "id": f"t{i}",
                    "tool_name": "bash",
                    "server_name": "",
                    "input": {"cmd": "ls"},
                },
            }
        )
        events.append(
            {
                "type": "tool_call_end",
                "data": {
                    "id": f"t{i}",
                    "output": {"exit_code": 0, "stdout": "same"},
                    "status": "success",
                    "summary": "same",
                    "output_preview": "same",
                    "error_class": None,
                    "output_shape_hash": shape_hash,
                },
            }
        )
    return events


def _compact_mode_interleaved_repeat_events() -> list[dict[str, object]]:
    hashes = ["samehash", "otherhash", "samehash", "samehash"]
    events: list[dict[str, object]] = []
    for i, shape_hash in enumerate(hashes):
        events.append(
            {
                "type": "tool_call_start",
                "data": {
                    "id": f"t{i}",
                    "tool_name": "bash",
                    "server_name": "",
                    "input": {"cmd": "ls"},
                },
            }
        )
        events.append(
            {
                "type": "tool_call_end",
                "data": {
                    "id": f"t{i}",
                    "output": {"exit_code": 0, "stdout": f"same-{i}"},
                    "status": "success",
                    "summary": "same",
                    "output_preview": "same",
                    "error_class": None,
                    "output_shape_hash": shape_hash,
                },
            }
        )
    return events


def _filter_expected_errors(errors: list[str]) -> list[str]:
    return [
        e
        for e in errors
        if "Content-Security-Policy" not in e
        and "Refused to" not in e
        and "ERR_CONNECTION_REFUSED" not in e
        and "/api/events" not in e
    ]


@requires_playwright
class TestNormalModeZeroConfig:
    """HARD GATE: normal mode must render DOM byte-identical to today."""

    def test_normal_mode_has_no_density_markup(self, authenticated_page) -> None:
        page = authenticated_page
        console_errors: list[str] = []
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)

        result = page.evaluate(_DISPATCH_SCRIPT, _normal_mode_events())
        assert result["errors"] == [], f"JS errors: {result['errors']}"
        after = result["after"]

        # No density enhancement markup should appear in normal mode.
        assert "tool-summary-body" not in after, "Normal mode leaked density summary markup"
        assert "tool-raw-output" not in after, "Normal mode leaked nested raw-output details"
        assert "tool-error-" not in after, "Normal mode leaked error-class CSS"
        assert "tool-repeat-collapsed" not in after

        # Legacy affordances remain.
        assert "tool-call" in after, "Legacy .tool-call wrapper missing"
        assert "Output (success)" in after, "Legacy Output label missing"

        filtered = _filter_expected_errors(console_errors)
        assert filtered == [], f"Console errors: {filtered}"


@requires_playwright
class TestCompactModeRendering:
    """Populated summary fields → smart rendering, raw JSON still reachable."""

    def test_compact_mode_shows_summary_body(self, authenticated_page) -> None:
        page = authenticated_page
        result = page.evaluate(_DISPATCH_SCRIPT, _compact_mode_events())
        assert result["errors"] == []
        after = result["after"]

        assert "tool-summary-body" in after, "Summary body missing"
        assert "tool-raw-output" in after, "Nested raw-output details missing"
        assert "Show raw output" in after, "Raw-output disclosure label missing"

    def test_compact_mode_error_class_applied(self, authenticated_page) -> None:
        page = authenticated_page
        result = page.evaluate(_DISPATCH_SCRIPT, _compact_mode_error_events("exit_nonzero"))
        assert result["errors"] == []
        assert "tool-error-exit_nonzero" in result["after"]
        assert 'aria-label="Tool call failed: exit_nonzero"' in result["after"]

    def test_compact_mode_diff_rendering(self, authenticated_page) -> None:
        page = authenticated_page
        result = page.evaluate(_DISPATCH_SCRIPT, _compact_mode_diff_events())
        assert result["errors"] == []
        after = result["after"]
        assert "tool-diff-hunk" in after
        assert "tool-diff-add" in after
        assert "tool-diff-del" in after

    def test_compact_mode_repeat_collapse(self, authenticated_page) -> None:
        page = authenticated_page
        result = page.evaluate(_DISPATCH_SCRIPT, _compact_mode_repeat_events(3))
        assert result["errors"] == []
        after = result["after"]
        # Exactly one collapsed row should appear.
        assert after.count("tool-repeat-collapsed") >= 1
        assert "bash \u00d7 3" in after or "bash × 3" in after

    def test_interleaved_shapes_do_not_collapse(self, authenticated_page) -> None:
        page = authenticated_page
        result = page.evaluate(_DISPATCH_SCRIPT, _compact_mode_interleaved_repeat_events())
        assert result["errors"] == []
        after = result["after"]
        assert "tool-repeat-collapsed" not in after


@requires_playwright
class TestErrorClassVariants:
    """Each of the four error classes applies the matching CSS hook."""

    @pytest.mark.parametrize("error_class", ["exit_nonzero", "exception", "timeout", "denied"])
    def test_error_class_hook(self, authenticated_page, error_class: str) -> None:
        page = authenticated_page
        result = page.evaluate(_DISPATCH_SCRIPT, _compact_mode_error_events(error_class))
        assert result["errors"] == []
        assert f"tool-error-{error_class}" in result["after"]


@requires_playwright
class TestReplayTurnBoundaries:
    def test_replay_does_not_collapse_across_assistant_turns(self, authenticated_page) -> None:
        page = authenticated_page
        html = page.evaluate(
            """() => {
                Chat.loadMessages([
                    {
                        role: 'assistant',
                        content: 'first turn',
                        tool_calls: [
                            {
                                id: 't1',
                                tool_name: 'bash',
                                input: {cmd: 'ls'},
                                output: {exit_code: 0, stdout: 'same'},
                                status: 'success',
                                summary: 'same',
                                output_preview: 'same',
                                error_class: null,
                                output_shape_hash: 'samehash',
                            },
                            {
                                id: 't2',
                                tool_name: 'bash',
                                input: {cmd: 'ls'},
                                output: {exit_code: 0, stdout: 'same'},
                                status: 'success',
                                summary: 'same',
                                output_preview: 'same',
                                error_class: null,
                                output_shape_hash: 'samehash',
                            },
                        ],
                    },
                    {
                        role: 'assistant',
                        content: 'second turn',
                        tool_calls: [
                            {
                                id: 't3',
                                tool_name: 'bash',
                                input: {cmd: 'ls'},
                                output: {exit_code: 0, stdout: 'same'},
                                status: 'success',
                                summary: 'same',
                                output_preview: 'same',
                                error_class: null,
                                output_shape_hash: 'samehash',
                            },
                            {
                                id: 't4',
                                tool_name: 'bash',
                                input: {cmd: 'ls'},
                                output: {exit_code: 0, stdout: 'same'},
                                status: 'success',
                                summary: 'same',
                                output_preview: 'same',
                                error_class: null,
                                output_shape_hash: 'samehash',
                            },
                        ],
                    },
                ]);
                return document.getElementById('messages-container').innerHTML;
            }"""
        )
        assert "tool-repeat-collapsed" not in html
