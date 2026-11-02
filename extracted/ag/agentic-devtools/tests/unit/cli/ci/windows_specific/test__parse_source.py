"""AST policy extraction rejects all additional expectation-name bindings."""

import pytest

from agentic_devtools.cli.ci.windows_specific import EXPECTED_EXPANSIONS, EXPECTED_SELECTORS, _parse_source

SOURCE = f"EXPECTED_SELECTORS = {EXPECTED_SELECTORS!r}\nEXPECTED_EXPANSIONS = {EXPECTED_EXPANSIONS!r}\n"


def test_matching_literals_and_unrelated_code():
    policy = _parse_source(
        SOURCE + "\nimport os\nfrom pathlib import Path\ndef other(arg):\n    local = arg\n    return local\n"
    )
    assert policy == (EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items()))


@pytest.mark.parametrize("name", ["EXPECTED_SELECTORS", "EXPECTED_EXPANSIONS"])
@pytest.mark.parametrize(
    "extra",
    [
        "{name} = ()",
        "{name}: tuple = ()",
        "{name} += ()",
        "({name} := ())",
        "del {name}",
        "if False:\n    {name} = ()",
        "def unrelated():\n    {name} = ()",
        "other = {name} = ()",
        "{name}, other = (), ()",
        "import os as {name}",
        "import {name}",
        "import {name}.child",
        "from os import path as {name}",
        "from os import {name}",
        "def {name}():\n    pass",
        "async def {name}():\n    pass",
        "class {name}:\n    pass",
        "def unrelated({name}):\n    pass",
        "def unrelated(*{name}):\n    pass",
        "def unrelated(**{name}):\n    pass",
        "try:\n    pass\nexcept Exception as {name}:\n    pass",
        "for {name} in ():\n    pass",
        "with open('never') as {name}:\n    pass",
        "[x for {name} in ()]",
        "match ():\n    case [*{name}]:\n        pass",
        "match ():\n    case {{**{name}}}:\n        pass",
        "match ():\n    case {name}:\n        pass",
        "type other[{name}] = int",
        "type other[*{name}] = int",
        "type other[**{name}] = int",
        "type {name} = int",
        "def unrelated():\n    global {name}",
        "def unrelated():\n    nonlocal {name}",
    ],
)
def test_additional_bindings_are_rejected(name, extra):
    with pytest.raises(ValueError):
        _parse_source(SOURCE + "\n" + extra.format(name=name) + "\n")


@pytest.mark.parametrize(
    "source",
    [
        "",
        "syntax !",
        "EXPECTED_SELECTORS = tuple()\nEXPECTED_EXPANSIONS = {}",
        "EXPECTED_SELECTORS: tuple = ()\nEXPECTED_EXPANSIONS = {}",
        "EXPECTED_SELECTORS = other = ()\nEXPECTED_EXPANSIONS = {}",
        "EXPECTED_SELECTORS = ()\nEXPECTED_EXPANSIONS = {}",
        "EXPECTED_SELECTORS, EXPECTED_EXPANSIONS = (), {}",
        "if True:\n    EXPECTED_SELECTORS = ()\n    EXPECTED_EXPANSIONS = {}",
    ],
)
def test_missing_unsafe_or_drifted_literals(source):
    with pytest.raises(ValueError):
        _parse_source(source)


def test_duplicate_expansion_literal_keys():
    key = EXPECTED_SELECTORS[0]
    source = f"EXPECTED_SELECTORS = {EXPECTED_SELECTORS!r}\nEXPECTED_EXPANSIONS = {{{key!r}: (), {key!r}: ()}}\n"
    with pytest.raises(ValueError, match="Duplicate"):
        _parse_source(source)


def test_nonliteral_expansion():
    with pytest.raises(ValueError):
        _parse_source(f"EXPECTED_SELECTORS = {EXPECTED_SELECTORS!r}\nEXPECTED_EXPANSIONS = dict()\n")


def test_reads_of_expectation_names_are_allowed():
    assert _parse_source(SOURCE + "\nother = EXPECTED_SELECTORS\n").selectors == EXPECTED_SELECTORS
