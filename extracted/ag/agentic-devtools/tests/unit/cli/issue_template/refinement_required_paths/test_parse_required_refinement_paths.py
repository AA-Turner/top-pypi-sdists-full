"""Contract tests for parsing required paths from structured issue sections."""

import pytest

from agentic_devtools.cli.issue_template.refinement_required_paths import parse_required_refinement_paths

_NAME = "Affected Files & Components"
_EMPTY = {
    "code": "empty_required_section",
    "path": None,
    "message": f"Required section '{_NAME}' has no valid entries.",
}
_MALFORMED = {
    "code": "malformed_required_entry",
    "path": None,
    "message": "Required path entry does not match the Markdown or Jira grammar.",
}
_MISSING = {"code": "missing_required_section", "path": None, "message": f"Required section '{_NAME}' is missing."}
_REPEATED = {
    "code": "repeated_required_section",
    "path": None,
    "message": f"Required section '{_NAME}' appears more than once.",
}
_ERRORS = {
    "empty": {"code": "invalid_required_path", "path": None, "message": "Required path token is empty."},
    "control": {
        "code": "invalid_required_path",
        "path": None,
        "message": "Required path token contains a control character.",
    },
    "whitespace": {
        "code": "invalid_required_path",
        "path": None,
        "message": "Required path token contains whitespace.",
    },
    "absolute": {
        "code": "invalid_required_path",
        "path": None,
        "message": "Required path must be repository-relative.",
    },
    "traversal": {
        "code": "invalid_required_path",
        "path": None,
        "message": 'Required path must not contain "." or ".." segments.',
    },
}
_PATHS_4090 = [
    "agentic_devtools/cli/ci/task_identity.py",
    "agentic_devtools/cli/ci/github_provider.py",
    "agentic_devtools/cli/ci/dispatch_state.py",
    "tests/unit/cli/ci/task_identity/__init__.py",
    "tests/unit/cli/ci/task_identity/test__resolve_writer_task_identity.py",
    "tests/unit/cli/ci/github_provider/test__resolve_writer_task_identity_for_dispatch.py",
    "tests/unit/cli/ci/dispatch_state/test_dispatchrecord.py",
    "tests/unit/cli/ci/dispatch_state/test_transition_dispatch.py",
]


@pytest.mark.parametrize(
    ("heading", "entry", "ending"),
    [
        ("## Affected Files & Components", "-\t ` \tsrc\\one.py \t` \t— \t reason \t", "## End"),
        ("h2. Affected Files & Components", "* \t{{ \tsrc\\one.py \t}} \t— \t reason \t", "h1. End"),
    ],
)
def test_parses_valid_entries_and_normalizes_paths(heading: str, entry: str, ending: str) -> None:
    body = "\n".join([heading, entry, entry.replace("one.py", "two.py"), entry, " \t", ending])
    assert parse_required_refinement_paths(body) == {"paths": ["src/one.py", "src/two.py"], "errors": []}


@pytest.mark.parametrize(
    ("body", "error"),
    [
        ("no section", _MISSING),
        ("## Affected Files & Components\n- `one.py` — x\nh2. Affected Files & Components", _REPEATED),
        (f"## {_NAME}\n \t\n## End", _EMPTY),
    ],
)
def test_section_cardinality_and_empty_content(body: str, error: dict[str, str | None]) -> None:
    assert parse_required_refinement_paths(body) == {"paths": [], "errors": [error]}
    assert parse_required_refinement_paths(f"## {_NAME}\n\u00a0") == {"paths": [], "errors": [_EMPTY, _MALFORMED]}


@pytest.mark.parametrize(
    ("entry", "syntax"),
    [
        ("- `one.py` - reason", "markdown"),
        ("* {{one.py}} - reason", "jira"),
        ("-`one.py` — reason", "markdown"),
        ("*{{one.py}} — reason", "jira"),
        ("* {{one.py}} — reason", "markdown"),
        ("- `one.py` — reason", "jira"),
        ("  - `one.py` — reason", "markdown"),
        ("- `one.py` — \t", "markdown"),
        ("- one.py — reason", "markdown"),
        ("* {one.py} — reason", "jira"),
        ("* {{{{one.py}} — reason", "jira"),
        ("* {{a{{b}} — reason", "jira"),
        ("* {{a}b}} — reason", "jira"),
        ("* {{one.py}} extra — reason", "jira"),
        ("- `one`inside.py` — reason", "markdown"),
        ("narrative mentions src/one.py", "markdown"),
        ("* {{one.py}} — reason", "markdown"),
        ("- `one.py` — reason", "jira"),
    ],
)
def test_malformed_entries_are_not_inferred(entry: str, syntax: str) -> None:
    heading = "## Affected Files & Components" if syntax == "markdown" else "h2. Affected Files & Components"
    assert parse_required_refinement_paths(f"{heading}\n{entry}") == {"paths": [], "errors": [_EMPTY, _MALFORMED]}


@pytest.mark.parametrize(
    ("token", "error"),
    [
        ("", _ERRORS["empty"]),
        ("one two.py", _ERRORS["whitespace"]),
        ("one\u001cpy", _ERRORS["control"]),
        ("one\u0085py", _ERRORS["control"]),
        ("one\u00a0py", _ERRORS["whitespace"]),
        ("../one.py", _ERRORS["traversal"]),
        ("/one.py", _ERRORS["absolute"]),
    ],
)
def test_maps_normalizer_errors(token: str, error: dict[str, str | None]) -> None:
    assert parse_required_refinement_paths(f"## {_NAME}\n- `{token}` — reason") == {
        "paths": [],
        "errors": [_EMPTY, error],
    }


def test_preserves_valid_paths_and_duplicate_diagnostics_in_sorted_order() -> None:
    body = f"## {_NAME}\n- `good.py` — x\n- `bad path.py` — x\n- `bad path.py` — x\n- `/abs.py` — x\nunknown\nunknown"
    assert parse_required_refinement_paths(body) == {
        "paths": ["good.py"],
        "errors": [_ERRORS["absolute"], _ERRORS["whitespace"], _ERRORS["whitespace"], _MALFORMED, _MALFORMED],
    }


@pytest.mark.parametrize(
    ("character", "error"),
    [
        ("\v", _ERRORS["control"]),
        ("\f", _ERRORS["control"]),
        ("\x1c", _ERRORS["control"]),
        ("\x1d", _ERRORS["control"]),
        ("\x1e", _ERRORS["control"]),
        ("\x1f", _ERRORS["control"]),
        ("\x1d", _ERRORS["control"]),
        ("\x1e", _ERRORS["control"]),
        ("\x1f", _ERRORS["control"]),
        ("\x85", _ERRORS["control"]),
        ("\u2028", _ERRORS["whitespace"]),
        ("\u2029", _ERRORS["whitespace"]),
    ],
)
def test_unicode_separators_reach_the_path_normalizer(character: str, error: dict[str, str | None]) -> None:
    assert parse_required_refinement_paths(f"## {_NAME}\n- `bad{character}path.py` — x") == {
        "paths": [],
        "errors": [_EMPTY, error],
    }


@pytest.mark.parametrize("ending", ["\n", "\r\n", "\r"])
@pytest.mark.parametrize("markdown_boundary", ["# End", "## End"])
@pytest.mark.parametrize("jira_boundary", ["h1. End", "h2. End"])
def test_physical_line_segments_and_scanner_boundaries(ending: str, markdown_boundary: str, jira_boundary: str) -> None:
    markdown = ending.join([f"## {_NAME}", "- `one.py` — x", "### stays", "- `two.py` — x", markdown_boundary])
    assert parse_required_refinement_paths(markdown + ending + "- `excluded.py` — x") == {
        "paths": ["one.py", "two.py"],
        "errors": [_MALFORMED],
    }
    jira = ending.join([f"h2. {_NAME}", "* {{one.py}} — x", jira_boundary, "* {{excluded.py}} — x"])
    assert parse_required_refinement_paths(jira) == {"paths": ["one.py"], "errors": []}


def test_markdown_fences_are_malformed_but_jira_has_no_fence_exception() -> None:
    body = f"## {_NAME}\n```\n- `hidden.py` — x\n```\n## End"
    assert parse_required_refinement_paths(body) == {
        "paths": [],
        "errors": [_EMPTY, _MALFORMED, _MALFORMED, _MALFORMED],
    }
    body = f"## {_NAME}\n```\n~~~\n- `hidden.py` — x"
    assert parse_required_refinement_paths(body) == {
        "paths": [],
        "errors": [_EMPTY, _MALFORMED, _MALFORMED, _MALFORMED],
    }
    body = f"h2. {_NAME}\n```\n* {{{{visible.py}}}} — x\n```"
    assert parse_required_refinement_paths(body) == {"paths": ["visible.py"], "errors": [_MALFORMED, _MALFORMED]}
    assert parse_required_refinement_paths(f"```\n## {_NAME}\n```") == {"paths": [], "errors": [_MISSING]}


def test_reports_the_issue_4090_vector_and_each_omission() -> None:
    for omitted in [None, *_PATHS_4090]:
        present = [path for path in _PATHS_4090 if path != omitted]
        entries = "\n".join(f"- `{path}` — implementation or test" for path in present)
        assert parse_required_refinement_paths(f"## {_NAME}\n{entries}") == {"paths": present, "errors": []}
    from agentic_devtools.cli.issue_template import refinement_required_paths

    assert [name for name in vars(refinement_required_paths) if not name.startswith("_")] == [
        "parse_required_refinement_paths"
    ]
