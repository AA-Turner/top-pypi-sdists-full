from agentic_devtools.ai_providers.availability import _render_markdown_table_cell


def test__render_markdown_table_cell_plain_value_is_unchanged() -> None:
    assert _render_markdown_table_cell("claude-opus-5") == "claude-opus-5"


def test__render_markdown_table_cell_escapes_pipe() -> None:
    assert _render_markdown_table_cell("model|variant") == r"model\|variant"


def test__render_markdown_table_cell_escapes_backslash() -> None:
    assert _render_markdown_table_cell("model\\preview") == "model\\\\preview"


def test__render_markdown_table_cell_collapses_newlines_to_space() -> None:
    assert _render_markdown_table_cell("line1\nline2") == "line1 line2"


def test__render_markdown_table_cell_escapes_pipe_and_backslash_together() -> None:
    assert _render_markdown_table_cell("a\\b|c") == r"a\\b\|c"


def test__render_markdown_table_cell_collapses_newline_then_escapes_pipe() -> None:
    assert _render_markdown_table_cell("a\nb|c") == r"a b\|c"
