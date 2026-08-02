"""Unit tests for scripts/generate_docstrings.py."""

import importlib.util
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "openapi-docs-sample.json"


def _load_generate_docstrings():
    spec = importlib.util.spec_from_file_location(
        "generate_docstrings", REPO_ROOT / "scripts" / "generate_docstrings.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gd = _load_generate_docstrings()
SPEC = json.loads(FIXTURE.read_text(encoding="utf-8"))
INDEX = gd._index_spec(SPEC)


def _operation(verb: str, normalized_path: str):
    return INDEX[(verb, normalized_path)]


def test_index_spec_keys_by_verb_and_normalized_path():
    assert ("GET", "widgets/{}") in INDEX
    assert ("POST", "widgets") in INDEX
    assert ("POST", "widgets/{}/_merge") in INDEX
    raw_path, operation = INDEX[("GET", "widgets/{}")]
    assert raw_path == "/api/v2/widgets/{widgetId}"
    assert operation["summary"] == "Get widget"


def test_build_api_block_parameters_only():
    raw_path, operation = _operation("GET", "widgets/{}")
    lines = gd.build_api_block("GET", raw_path, operation, SPEC)
    text = "\n".join(lines)
    assert lines[0] == "**GET** ``/api/v2/widgets/{widgetId}``"
    assert "Fetch a single widget by id." in text
    assert "API parameters:" in text
    # Path params precede query params.
    assert "    * ``widgetId`` (path) -- Id of the widget to fetch." in lines
    assert "    * ``verbose`` (query) -- If true, include extra detail." in lines
    widget_index = lines.index("    * ``widgetId`` (path) -- Id of the widget to fetch.")
    verbose_index = lines.index("    * ``verbose`` (query) -- If true, include extra detail.")
    assert widget_index < verbose_index
    # No request body section for a GET.
    assert "API request body:" not in text


def test_build_api_block_resolves_ref_body_and_marks_required():
    raw_path, operation = _operation("POST", "widgets")
    lines = gd.build_api_block("POST", raw_path, operation, SPEC)
    assert "API request body:" in lines
    # Required field has no "(optional)" suffix; optional field does.
    assert "    * ``name`` -- Human-readable widget name." in lines
    assert "    * ``color`` (optional) -- Optional widget colour." in lines


def test_body_fields_handles_inline_object_schema():
    _raw_path, operation = _operation("POST", "widgets/{}/_merge")
    fields = gd._body_fields(operation, SPEC)
    names = [name for name, _description, _required in fields]
    assert names == ["file", "mode"]
    required = {name: req for name, _description, req in fields}
    assert required["file"] is True
    assert required["mode"] is False


def test_summary_and_description_both_rendered_when_distinct():
    raw_path, operation = _operation("GET", "widgets/{}")
    lines = gd.build_api_block("GET", raw_path, operation, SPEC)
    assert "Get widget" in lines
    assert "Fetch a single widget by id." in lines


# --- Marker injection -------------------------------------------------------

INDENT = " " * 8
CONTENT = ["**GET** ``/widgets/{}``", "", "Fetch a widget."]


def test_rebuild_multiline_docstring_injects_block_and_preserves_body():
    literal = [
        '        """Summary line.',
        "",
        "        Args:",
        "            value: A thing.",
        '        """',
    ]
    rebuilt = gd._rebuild_docstring(literal, INDENT, CONTENT)
    text = "\n".join(rebuilt)
    # Hand-written content preserved.
    assert "        Args:" in rebuilt
    assert "            value: A thing." in rebuilt
    # Markers and content injected.
    assert INDENT + gd.START_MARKER in rebuilt
    assert INDENT + gd.END_MARKER in rebuilt
    assert INDENT + "**GET** ``/widgets/{}``" in rebuilt
    # Closing quotes remain last.
    assert rebuilt[-1].strip() == '"""'
    # Block sits after the body and before the closing quotes.
    assert text.index("Args:") < text.index(gd.START_MARKER) < text.index('"""', text.index(gd.START_MARKER))


def test_rebuild_is_idempotent_and_replaces_between_markers():
    literal = [
        '        """Summary line.',
        "",
        "        Args:",
        "            value: A thing.",
        '        """',
    ]
    once = gd._rebuild_docstring(literal, INDENT, CONTENT)
    twice = gd._rebuild_docstring(once, INDENT, CONTENT)
    assert once == twice
    # Only one marker block exists after re-running.
    assert once.count(INDENT + gd.START_MARKER) == 1


def test_rebuild_replaces_stale_block_with_new_content():
    literal = [
        '        """Summary line.',
        "",
        "        Args:",
        "            value: A thing.",
        '        """',
    ]
    once = gd._rebuild_docstring(literal, INDENT, ["**GET** ``/old``", "", "Old text."])
    updated = gd._rebuild_docstring(once, INDENT, ["**GET** ``/new``", "", "New text."])
    text = "\n".join(updated)
    assert "/new" in text
    assert "/old" not in text
    assert updated.count(INDENT + gd.START_MARKER) == 1


def test_rebuild_expands_single_line_docstring():
    literal = ['        """Short summary."""']
    rebuilt = gd._rebuild_docstring(literal, INDENT, CONTENT)
    assert rebuilt[0] == '        """Short summary.'
    assert INDENT + gd.START_MARKER in rebuilt
    assert rebuilt[-1] == '        """'


def test_choose_endpoint_single_multiple_and_override():
    warnings = []
    # Single resolved endpoint is used directly.
    single = gd._choose_endpoint("Foo", "bar", {("GET", "foo")}, warnings, "foo.py")
    assert single == ("GET", "foo")
    assert warnings == []

    # Multiple endpoints without an override -> skipped with a warning.
    multiple = gd._choose_endpoint(
        "Foo", "baz", {("GET", "foo"), ("POST", "foo/_search")}, warnings, "foo.py"
    )
    assert multiple is None
    assert len(warnings) == 1

    # Override wins even when multiple endpoints resolve.
    key = next(iter(gd.METHOD_ENDPOINT_OVERRIDES))
    expected = gd.METHOD_ENDPOINT_OVERRIDES[key]
    chosen = gd._choose_endpoint(key[0], key[1], {("GET", "whatever")}, warnings, "x.py")
    assert chosen == expected
