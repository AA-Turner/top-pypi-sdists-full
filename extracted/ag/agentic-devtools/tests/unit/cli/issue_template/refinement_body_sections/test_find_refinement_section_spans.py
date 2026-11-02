"""Contract tests for the syntax-neutral refinement section scanner."""

import pytest

from agentic_devtools.cli.issue_template.refinement_body_sections import find_refinement_section_spans


@pytest.mark.parametrize(
    ("body", "name", "expected"),
    [
        ("", "Scope", []),
        ("\n", "Scope", []),
        ("## Scope", "", []),
        ("h2. Scope", " \t", []),
        ("## Scope\nh2. Scope", "scope", []),
        ("## Other\nh2. Other", "Scope", []),
        ("## Scope\nh2. Scope", " Scope ", []),
        ("##  Scope \t### \t", "Scope", [(0, 1, "markdown")]),
        ("h2. \tScope \t", "Scope", [(0, 1, "jira")]),
        ("h2. \tScope \t", "\tScope", []),
        ("## Scope", "Scope", [(0, 1, "markdown")]),
        ("h2. Scope", "Scope", [(0, 1, "jira")]),
        ("## Scope#\n## Scope ### text", "Scope", []),
        ("## Scope#\n## Scope ### text", "Scope#", [(0, 1, "markdown")]),
        ("h2. Scope ##", "Scope ##", [(0, 1, "jira")]),
        ("## ##\n##", "#", []),
        ("h1. Scope", "Scope", []),
        ("## Scope\n\n", "Scope", [(0, 2, "markdown")]),
        ("h2. Scope\r\n\r\n", "Scope", [(0, 2, "jira")]),
        ("## Scope\v", "Scope", []),
        ("## Scope\v", "Scope\v", [(0, 1, "markdown")]),
        ("h2. \u00a0Scope\u00a0", "Scope", [(0, 1, "jira")]),
    ],
)
def test_exact_titles(body: str, name: str, expected: list[tuple[int, int, str]]) -> None:
    assert find_refinement_section_spans(body, name) == expected


@pytest.mark.parametrize("ending", ["\n", "\r\n", "\r"])
@pytest.mark.parametrize("final_ending", ["", "\n", "\r\n", "\r"])
def test_physical_indexes_and_mixed_repeated_sections(ending: str, final_ending: str) -> None:
    body = ending.join(["intro", "## Scope", "h2. Scope", "## Scope", "h1. End", "## Other", "h2. Scope"])
    assert find_refinement_section_spans(body + final_ending, "Scope") == [
        (1, 3, "markdown"),
        (2, 4, "jira"),
        (3, 5, "markdown"),
        (6, 7, "jira"),
    ]


@pytest.mark.parametrize("heading", ["## Scope", "h2. Scope"])
def test_adjacent_matching_headings(heading: str) -> None:
    syntax = "markdown" if heading.startswith("#") else "jira"
    assert find_refinement_section_spans(f"{heading}\n{heading}", "Scope") == [(0, 1, syntax), (1, 2, syntax)]


@pytest.mark.parametrize("heading", ["## Scope", " ## Scope", "   ##\tScope ##", "h2. Scope"])
@pytest.mark.parametrize("boundary", ["# End", "   ## End ### \t", "#", "##", "h1. End", "h2. End"])
def test_syntax_specific_boundaries(heading: str, boundary: str) -> None:
    syntax = "jira" if heading.startswith("h") else "markdown"
    same_syntax = boundary.startswith("h") == heading.startswith("h")
    assert find_refinement_section_spans(f"{heading}\n{boundary}\ntext", "Scope") == [
        (0, 1 if same_syntax else 3, syntax)
    ]


@pytest.mark.parametrize(
    "non_boundary",
    [
        "### Scope",
        "####### Scope",
        "#Scope",
        "##Scope",
        "    # Scope",
        "    ## Scope",
        "\t## Scope",
        "h3. Scope",
        "h1.Scope",
        "h2.Scope",
        "h1.\tScope",
        "h2.\tScope",
        " h2. Scope",
        "Scope\n---",
        "Scope\n===",
    ],
)
@pytest.mark.parametrize(("heading", "syntax"), [("## Scope", "markdown"), ("h2. Scope", "jira")])
def test_non_headings_are_neither_starts_nor_boundaries(non_boundary: str, heading: str, syntax: str) -> None:
    assert find_refinement_section_spans(non_boundary, "Scope") == []
    body = f"{heading}\n{non_boundary}\ntext"
    assert find_refinement_section_spans(body, "Scope") == [(0, body.count("\n") + 1, syntax)]


@pytest.mark.parametrize("marker", ["```", "~~~~"])
@pytest.mark.parametrize("indent", ["", " ", "   "])
@pytest.mark.parametrize("ending", ["\n", "\r\n", "\r"])
@pytest.mark.parametrize(("heading", "syntax"), [("## Scope", "markdown"), ("h2. Scope", "jira")])
def test_fences_suppress_starts_and_boundaries(
    marker: str, indent: str, ending: str, heading: str, syntax: str
) -> None:
    body = ending.join(
        [
            heading,
            indent + marker + " info",
            "## Scope",
            "h2. Scope",
            "# End",
            "h1. End",
            indent + marker + marker[0] + " \t",
            heading,
        ]
    )
    assert find_refinement_section_spans(body, "Scope") == [(0, 7, syntax), (7, 8, syntax)]


@pytest.mark.parametrize(
    ("opener", "not_closer"),
    [
        ("````", "```"),
        ("~~~~", "~~~"),
        ("```", "~~~"),
        ("~~~", "```"),
        ("```", "``` text"),
        ("~~~", "~~~ text"),
        ("```", "    ```"),
        ("~~~", "\t~~~"),
    ],
)
def test_invalid_closers_leave_both_syntaxes_fenced(opener: str, not_closer: str) -> None:
    body = "\n".join([opener, not_closer, "## Scope", "h2. Scope", opener, "## Scope", "h2. Scope"])
    assert find_refinement_section_spans(body, "Scope") == [(5, 7, "markdown"), (6, 7, "jira")]


@pytest.mark.parametrize("opener", ["```", "   ~~~ info", "~~~ `allowed`"])
def test_unclosed_fences(opener: str) -> None:
    body = f"## Scope\nh2. Scope\n{opener}\n## Scope\nh2. Scope\n# End\nh1. End"
    assert find_refinement_section_spans(body, "Scope") == [(0, 7, "markdown"), (1, 7, "jira")]


@pytest.mark.parametrize("not_opener", ["``", "~~", "    ```", "\t~~~", "``` info`text"])
def test_invalid_openers_do_not_hide_headings(not_opener: str) -> None:
    assert find_refinement_section_spans(f"{not_opener}\n## Scope\nh2. Scope", "Scope") == [
        (1, 3, "markdown"),
        (2, 3, "jira"),
    ]


@pytest.mark.parametrize("macro", ["{code}", "{code:python}", "{noformat}"])
def test_jira_macros_are_ordinary_text(macro: str) -> None:
    assert find_refinement_section_spans(f"{macro}\nh2. Scope\n{macro}\nh2. Scope", "Scope") == [
        (1, 3, "jira"),
        (3, 4, "jira"),
    ]


@pytest.mark.parametrize("separator", ["\v", "\f", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029"])
def test_unicode_separators_are_not_line_breaks(separator: str) -> None:
    body = f"text{separator}## Scope\ntext{separator}h2. Scope\ntext{separator}```\n## Scope"
    assert find_refinement_section_spans(body, "Scope") == [(3, 4, "markdown")]
    body = f"## Scope\nh2. Scope\ntext{separator}# End\ntext{separator}h1. End\ntext{separator}~~~"
    assert find_refinement_section_spans(body, "Scope") == [(0, 5, "markdown"), (1, 5, "jira")]
