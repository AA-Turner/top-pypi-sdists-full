"""A bot wall inside a "successful" tool result tells the agent to use a browser.

Conversation 577db529 (2026-10-24): shell_python fetched lmarena.ai, got 403 and
Cloudflare's "Just a moment..." page inside a successful result, and nothing
told the agent a plain HTTP client would keep hitting it while a real browser
would not. ``known_outcome_notices`` is the one ladder; the executor appends its
notices to every result.
"""

from __future__ import annotations

from matrx_ai.tools.error_remedy import known_outcome_notices, shell_recovery_hint
from matrx_ai.tools.models import ToolError, ToolResult

# The stdout the agent actually received (trimmed).
_LMARENA_STDOUT = (
    "('https://lmarena.ai/leaderboard', 403, 'text/html; charset=UTF-8', 5442)\n"
    '    <!DOCTYPE html><html lang="en-US"><head><title>Just a moment...</title>'
    '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n'
    "('https://www.vals.ai/benchmarks', 200, 'text/html; charset=utf-8', 282120)\n"
)


def _shell(stdout: str, *, success: bool = True) -> ToolResult:
    return ToolResult(
        success=success,
        output={"__kind": "shell_execution", "stdout": stdout, "stderr": "", "exit_code": 0},
        call_id="c1",
        tool_name="shell_python",
    )


def test_a_cloudflare_wall_in_a_successful_fetch_points_at_the_browser() -> None:
    notices = known_outcome_notices(
        _shell(_LMARENA_STDOUT), active_tools=frozenset({"shell_python", "cloud_browser"})
    )
    assert len(notices) == 1
    assert "'Just a moment...'" in notices[0]
    assert "cloud_browser" in notices[0]
    assert "do not retry the same way" in notices[0]


def test_the_notice_reaches_the_content_the_model_reads() -> None:
    result = _shell(_LMARENA_STDOUT)
    result.model_notices.extend(known_outcome_notices(result, active_tools=None))
    content = result.to_tool_result_content()["content"]
    assert "cloud_browser" in str(content)


def test_the_next_step_names_only_a_browser_the_run_has() -> None:
    lazy = known_outcome_notices(
        _shell(_LMARENA_STDOUT), active_tools=frozenset({"load_browser_tools"})
    )
    none = known_outcome_notices(_shell(_LMARENA_STDOUT), active_tools=frozenset({"web"}))
    assert "Call load_browser_tools" in lazy[0]
    assert "No browser tool is attached" in none[0] and "cloud_browser" not in none[0]


def test_a_wall_in_an_error_message_is_seen_too() -> None:
    result = ToolResult(
        success=False,
        error=ToolError(
            error_type="exit_code",
            message="curl: (22) 403\n<script src='https://challenges.cloudflare.com/turnstile'>",
        ),
        call_id="c2",
        tool_name="shell_execute",
    )
    assert known_outcome_notices(result, active_tools=None)


def test_an_ordinary_page_that_mentions_access_denied_is_not_a_wall() -> None:
    page = (
        "<html><head><title>Fixing 'access denied' errors in S3</title></head>"
        "<body>Our guide to 403s and the request could not be satisfied.</body></html>"
    )
    assert known_outcome_notices(_shell(page), active_tools=None) == []
    assert known_outcome_notices(_shell("ok\n"), active_tools=None) == []


def test_pandas_without_a_parquet_engine_says_install_pyarrow() -> None:
    stderr = "ImportError: Unable to find a usable engine; tried using: 'pyarrow', 'fastparquet'."
    hint = shell_recovery_hint(stderr, "python3 -")
    assert hint and "pip install pyarrow" in hint
