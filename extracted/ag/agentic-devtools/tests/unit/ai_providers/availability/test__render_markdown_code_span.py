from agentic_devtools.ai_providers.availability import _render_markdown_code_span


def test_render_markdown_code_span_wraps_plain_text() -> None:
    assert _render_markdown_code_span("evidence.json") == "`evidence.json`"


def test_render_markdown_code_span_uses_wider_fence_for_embedded_backticks() -> None:
    assert _render_markdown_code_span("path/with``ticks.json") == "```path/with``ticks.json```"


def test_render_markdown_code_span_pads_when_value_starts_with_backtick() -> None:
    assert _render_markdown_code_span("`leading.json") == "`` `leading.json ``"


def test_render_markdown_code_span_collapses_line_breaks() -> None:
    assert _render_markdown_code_span("path/with\nline-break.json") == "`path/with line-break.json`"
