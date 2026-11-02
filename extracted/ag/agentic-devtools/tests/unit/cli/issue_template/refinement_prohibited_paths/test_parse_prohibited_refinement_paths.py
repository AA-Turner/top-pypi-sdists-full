"""Contract tests for fail-closed prohibited refinement entries."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.issue_template.refinement_prohibited_paths import parse_prohibited_refinement_paths

MALFORMED = {
    "code": "malformed_prohibited_entry",
    "path": None,
    "message": "Out of Scope lines must be Path or Note entries in the section syntax.",
}
FORMS = [("## Out of Scope", "- ", "`", "`"), ("h2. Out of Scope", "* ", "{{", "}}")]


@pytest.mark.parametrize(
    "body", ["", "\r\n", "prose", "## Out of scope\n- Path: `a`", "h2. Other", "## Out of Scope", "h2. Out of Scope"]
)
def test_absent_or_empty_section(body: str) -> None:
    assert parse_prohibited_refinement_paths(body) == {"paths": [], "errors": []}


@pytest.mark.parametrize("head,prefix,left,right", FORMS)
@pytest.mark.parametrize("ending", ["\n", "\r\n", "\r"])
@pytest.mark.parametrize("final", ["", "\n", "\r\n", "\r"])
def test_entries_and_physical_lines(head: str, prefix: str, left: str, right: str, ending: str, final: str) -> None:
    tokens = ["z/file.py", "Makefile", "agentic_devtools/cli/ci/agent_assignment.py", r"z\file.py"]
    tokens.append("a`b" if head.startswith("h") else "a{{b}}")
    lines = ["outside prose", head, "", " \t\u2028", *(f"{prefix}Path: {left}{p}{right} \t" for p in tokens)]
    lines += [f"{prefix}Note: task-9", f"{prefix}Note: --flag", f"{prefix}Note: plain text"]
    boundary = "h1. End" if head.startswith("h") else "# End"
    assert parse_prohibited_refinement_paths(ending.join(lines + [boundary, "outside prose"]) + final) == {
        "paths": sorted(set(p.replace("\\", "/") for p in tokens)),
        "errors": [],
    }


@pytest.mark.parametrize("first", ["## Out of Scope", "h2. Out of Scope"])
@pytest.mark.parametrize("second", ["## Out of Scope", "h2. Out of Scope"])
def test_repeated_sections(first: str, second: str) -> None:
    assert parse_prohibited_refinement_paths(f"{first}\nmalformed\n{second}") == {
        "paths": [],
        "errors": [
            {"code": "repeated_prohibited_section", "path": None, "message": "Out of Scope must appear at most once."}
        ],
    }


@pytest.mark.parametrize("head,prefix,left,right", FORMS)
@pytest.mark.parametrize(
    "entry",
    [
        "unmarked",
        "Makefile",
        "task-9",
        "--flag",
        "{code}",
        "{code:python}",
        "{noformat}",
        "{p}path: {l}a{r}",
        "{p}note: text",
        " {p}Note: text",
        "{p}Note: \t",
        "{p}Note: \u2028",
        "{p}Path: {l}{r}",
        "{p}Path: a",
        "{p}Path: {l}a{r} extra",
        "{p}Path: {l}a{r} {l}b{r}",
        "{p}Note: text {l}a{r}",
        "{q}Path: {l}a{r}",
        "{p}Path: {x}a{y}",
        "{p}Path: {l}a{l}b{r}",
        "{p}Path: {l}a{r}b{r}",
        "{p}Note: stray{l}",
        "{p}Note: stray{r}",
    ],
)
def test_malformed_entries(head: str, prefix: str, left: str, right: str, entry: str) -> None:
    _, other_prefix, other_left, other_right = FORMS[head.startswith("#")]
    line = (
        entry.format(p=prefix, l=left, r=right, q=other_prefix, x=other_left, y=other_right)
        if "{p}" in entry or "{q}" in entry
        else entry
    )
    assert parse_prohibited_refinement_paths(f"{head}\n{line}") == {"paths": [], "errors": [MALFORMED]}


@pytest.mark.parametrize("head,prefix,left,right", FORMS)
def test_sorted_diagnostics_preserve_duplicates(head: str, prefix: str, left: str, right: str) -> None:
    invalid = ["z z", "/absolute", r"a\..\b", "z z", "a\x00b", "a\tb", "a\u2028b", "a\u0085b", "a\vb"]
    lines = [head, "bad", "bad", f"{prefix}Path: {left}valid{right}"]
    lines += [f"{prefix}Path: {left}{token}{right}" for token in invalid]
    errors = [
        {
            "code": "invalid_prohibited_path",
            "path": token,
            "message": "Prohibited path is not a valid repository-relative path.",
        }
        for token in sorted(invalid)
    ] + [MALFORMED, MALFORMED]
    assert parse_prohibited_refinement_paths("\n".join(lines)) == {"paths": ["valid"], "errors": errors}


@pytest.mark.parametrize("head,prefix,left,right", FORMS)
@pytest.mark.parametrize(
    "opener,closer",
    [
        ("```python", "```"),
        ("   ```` info", "  ````` \t"),
        ("~~~ `info`", "~~~~"),
        ("   ~~~info", "~~~"),
        ("```", None),
    ],
)
def test_fenced_examples(head: str, prefix: str, left: str, right: str, opener: str, closer: str | None) -> None:
    body = f"{head}\n{opener}\nh2. Out of Scope\n## Out of Scope\nh2. End\nbad\n{prefix}Path: {left}hidden{right}"
    if closer is not None:
        body += f"\n{closer}\n{prefix}Path: {left}visible{right}"
    assert parse_prohibited_refinement_paths(body) == {
        "paths": [] if closer is None else ["visible"],
        "errors": [],
    }


@pytest.mark.parametrize("head,prefix,left,right", FORMS)
@pytest.mark.parametrize("not_closer", ["```", "~~~~", "```` text", "    ````", "\t````"])
def test_only_valid_closer_ends_fence(head: str, prefix: str, left: str, right: str, not_closer: str) -> None:
    body = f"{head}\n````\n{not_closer}\nbad\n````\n{prefix}Path: {left}visible{right}"
    assert parse_prohibited_refinement_paths(body) == {"paths": ["visible"], "errors": []}


@pytest.mark.parametrize("not_opener", ["``", "~~", "    ```", "\t~~~", "``` info`text"])
@pytest.mark.parametrize("head,prefix,left,right", FORMS)
def test_invalid_openers_are_malformed(head: str, prefix: str, left: str, right: str, not_opener: str) -> None:
    assert parse_prohibited_refinement_paths(f"{head}\n{not_opener}\n{prefix}Path: {left}visible{right}") == {
        "paths": ["visible"],
        "errors": [MALFORMED],
    }


@pytest.mark.parametrize(
    "head,entry,token",
    [
        ("## Out of Scope", "- Path: `a{{b}}`", "a{{b}}"),
        ("h2. Out of Scope", "* Path: {{a`b}}", "a`b"),
        ("## Out of Scope", "- Path: `a\u2028b`", "a\u2028b"),
        ("h2. Out of Scope", "* Path: {{a\u2029b}}", "a\u2029b"),
    ],
)
def test_tokens_reach_shared_normalizer_unchanged(head: str, entry: str, token: str) -> None:
    target = "agentic_devtools.cli.issue_template.refinement_prohibited_paths._normalize"
    with patch(target, return_value=(token, None)) as normalize:
        assert parse_prohibited_refinement_paths(f"{head}\r\n{entry}\r\n") == {"paths": [token], "errors": []}
    normalize.assert_called_once_with(token)
