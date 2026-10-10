"""TE-20322 (auteur #6461) + json_path carry (auteur #6161): materialized
conditions arrive as a sub_check LIST — {description, extracted_value:
'{{evidence}}', expected_value, operator, transforms, json_path} plus a
composite_operator — and the legacy leaf beneath them is hollow. Before this
port selenium-python never evaluated sub_checks, so a materialized if/else
took the wrong branch and a materialized while ran zero or unbounded laps.

Evaluation semantics are ported from playwright-python's
testmu_helper/evaluation module so both bindings reach identical verdicts.
"""
from __future__ import annotations

import json

import pytest

from testmu_selenium.condition import Assertion


def _gv(store):
    def get_variable_value(template, variables=None, *args, **kwargs):
        return store.get(template, template)
    return get_variable_value


def _tree(sub_checks, composite="and", claim="materialized claim"):
    # The shape the materializer exports: hollow leaf + the sub_check contract.
    return {
        "operator": "equals",
        "left_operand": "",
        "right_operand": "",
        "sub_checks": sub_checks,
        "composite_operator": composite,
        "claim": claim,
    }


def _sc(extracted, expected, operator="equals", transforms=None, json_path=None):
    return {
        "description": "",
        "store_key": "ev",
        "extracted_value": extracted,
        "expected_value": expected,
        "operator": operator,
        "transforms": transforms or [],
        "json_path": json_path,
    }


def test_sub_checks_verdict_beats_the_hollow_leaf():
    # The hollow leaf ("" equals "") evaluates True; the sub_check is False —
    # the materialized contract must win, or the branch goes the wrong way.
    tree = _tree([_sc("{{ev1}}", "6")])
    node = Assertion.from_json(tree)
    passed, used = node.evaluate({}, _gv({"{{ev1}}": "5"}))
    assert passed is False
    assert used["{{ev1}}"] == "5"  # evidence resolution is tracked


def test_sub_checks_pass_and_record_sub_results():
    node = Assertion.from_json(_tree([_sc("{{ev1}}", "5")]))
    passed, _ = node.evaluate({}, _gv({"{{ev1}}": "5"}))
    assert passed is True
    assert node.sub_results and node.sub_results[0]["passed"] is True


def test_composite_or_and():
    checks = [_sc("{{a}}", "1"), _sc("{{b}}", "2")]
    store = {"{{a}}": "1", "{{b}}": "999"}
    assert Assertion.from_json(_tree(checks, "or")).evaluate({}, _gv(store))[0] is True
    assert Assertion.from_json(_tree(checks, "and")).evaluate({}, _gv(store))[0] is False


def test_json_path_derivation_is_not_a_whole_value_compare():
    # auteur #6161: without json_path carried AND applied, this compares the
    # whole JSON string against "7" and fails.
    payload = json.dumps({"a": {"b": 7}})
    check = _sc("{{ev}}", "7", transforms=["json_path"], json_path="a.b")
    node = Assertion.from_json(_tree([check]))
    assert node.evaluate({}, _gv({"{{ev}}": payload}))[0] is True


def test_string_to_float_transform_handles_currency():
    check = _sc("{{ev}}", "1200.5", transforms=["string_to_float"])
    node = Assertion.from_json(_tree([check]))
    assert node.evaluate({}, _gv({"{{ev}}": "$1,200.50"}))[0] is True


def test_ordering_operator_is_numeric_not_lexical():
    check = _sc("{{ev}}", "9", operator="gt")
    node = Assertion.from_json(_tree([check]))
    assert node.evaluate({}, _gv({"{{ev}}": "10"}))[0] is True  # lexically "10" < "9"


def test_absent_operator_defaults_to_equals():
    check = {"extracted_value": "{{ev}}", "expected_value": "x", "transforms": []}
    node = Assertion.from_json(_tree([check]))
    assert node.evaluate({}, _gv({"{{ev}}": "x"}))[0] is True


def test_trees_without_sub_checks_are_untouched():
    tree = {"operator": "equals", "left_operand": "{{x}}", "right_operand": "5"}
    node = Assertion.from_json(tree)
    assert node.evaluate({}, _gv({"{{x}}": 5}))[0] is True
