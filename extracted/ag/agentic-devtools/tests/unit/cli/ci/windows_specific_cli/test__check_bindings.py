"""Direct tests for AST binding validation."""

import ast

import pytest

from agentic_devtools.cli.ci.windows_specific import _EXPECTATION_NAMES
from agentic_devtools.cli.ci.windows_specific_cli import _check_bindings


def test_approved_targets_and_unrelated_bindings():
    tree = ast.parse(
        "EXPECTED_SELECTORS = ()\nEXPECTED_EXPANSIONS = {}\nother = 1\n"
        "import unrelated_module\nfrom unrelated_module import explicit_name\n"
        "def unrelated_function():\n    raise RuntimeError('must not execute')\n"
    )
    targets = {id(statement.targets[0]) for statement in tree.body[:2]}
    _check_bindings(tree, targets, _EXPECTATION_NAMES)


@pytest.mark.parametrize("before_literals", [True, False])
def test_wildcard_import_rejected_before_or_after_literals(before_literals):
    literals = "EXPECTED_SELECTORS = ()\nEXPECTED_EXPANSIONS = {}\n"
    wildcard = "from nonexistent_untrusted_policy_module import *\n"
    tree = ast.parse(wildcard + literals if before_literals else literals + wildcard)
    targets = {id(statement.targets[0]) for statement in tree.body if isinstance(statement, ast.Assign)}
    with pytest.raises(ValueError, match="Wildcard imports"):
        _check_bindings(tree, targets, _EXPECTATION_NAMES)


@pytest.mark.parametrize(
    "source",
    [
        "EXPECTED_SELECTORS = ()",
        "del EXPECTED_EXPANSIONS",
        "import os as EXPECTED_SELECTORS",
        "def unrelated(EXPECTED_SELECTORS):\n    pass",
        "def unrelated():\n    global EXPECTED_SELECTORS",
        "class EXPECTED_EXPANSIONS:\n    pass",
        "match ():\n    case {**EXPECTED_EXPANSIONS}:\n        pass",
    ],
)
def test_unapproved_binding(source):
    with pytest.raises(ValueError):
        _check_bindings(ast.parse(source), set(), _EXPECTATION_NAMES)
