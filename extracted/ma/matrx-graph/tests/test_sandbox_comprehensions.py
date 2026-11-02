"""List expressions in the workflow sandbox: comprehensions and join().

Design: common-docs/systems/workflows/projects/generic-only/PRIMITIVES-LIST-EXPRESSIONS.md.
What a comprehension may compute, and every way it must still be refused.
"""

from __future__ import annotations

import pytest

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._sandbox import safe_eval, uses_bare_inputs, validate_expression

RESULTS = {
    "results": [
        {"keyword": "a", "counts": {"read": 3, "good": 2}, "pages": [{"url": "u1", "good": True}, {"url": "u2", "good": False}]},
        {"keyword": "b", "counts": {"read": 4, "good": 1}, "pages": [{"url": "u3", "good": True}]},
    ],
    "goals": {"a": "why a", "b": "why b"},
}


def test_list_comprehension_projects_and_filters() -> None:
    assert safe_eval("[r['keyword'] for r in inputs['results'] if r['counts']['good'] > 1]", RESULTS) == ["a"]


def test_two_for_clauses_flatten() -> None:
    expr = "[p['url'] for r in inputs['results'] for p in r['pages'] if p['good']]"
    assert safe_eval(expr, RESULTS) == ["u1", "u3"]


def test_generator_inside_a_helper_sums() -> None:
    assert safe_eval("sum(r['counts']['read'] for r in inputs['results'])", RESULTS) == 7


def test_dict_comprehension_and_tuple_target() -> None:
    assert safe_eval("{k: v for k, v in inputs['pairs']}", {"pairs": [["x", 1], ["y", 2]]}) == {"x": 1, "y": 2}


def test_dict_keys_iterate() -> None:
    expr = "[{'keyword': k, 'goal': inputs['goals'][k]} for k in sorted(inputs['goals'])]"
    assert safe_eval(expr, RESULTS) == [{"keyword": "a", "goal": "why a"}, {"keyword": "b", "goal": "why b"}]


def test_nested_comprehension_two_levels() -> None:
    expr = "[[p['url'] for p in r['pages']] for r in inputs['results']]"
    assert safe_eval(expr, RESULTS) == [["u1", "u2"], ["u3"]]


def test_helpers_and_inputs_are_visible_inside_the_loop() -> None:
    expr = "[lower(r['keyword']) + str(len(inputs['results'])) for r in inputs['results']]"
    assert safe_eval(expr, RESULTS) == ["a2", "b2"]


def test_join_texts_skips_none() -> None:
    assert safe_eval("join(', ', ['a', None, 'b'])", {}) == "a, b"
    assert safe_eval("join('\\n', [r['keyword'] for r in inputs['results']])", RESULTS) == "a\nb"


def test_join_refuses_a_non_text_item() -> None:
    with pytest.raises(ExecutionError, match=r"join\(\).*item 1"):
        safe_eval("join(', ', ['a', 2])", {})


def test_loop_variable_is_not_bare_inputs() -> None:
    assert not uses_bare_inputs("[x for x in inputs['a']]")


@pytest.mark.parametrize(
    ("expr", "why"),
    [
        ("[x.__class__ for x in inputs['a']]", "Attribute"),
        ("[inputs for inputs in inputs['a']]", "shadow"),
        ("[len for len in inputs['a']]", "shadow"),
        ("[_x for _x in inputs['a']]", "underscore"),
        ("[x for x in inputs['a'] for y in inputs['a'] for z in inputs['a']]", "two 'for'"),
        ("[[[z for z in y] for y in x] for x in inputs['a']]", "two levels"),
        ("(x for x in inputs['a'])", "generator"),
        ("[x for x.y in inputs['a']]", "Attribute"),
        ("[x for x in inputs['a'] if (y := x)]", "NamedExpr"),
        ("[x for x in inputs['f'](1)]", "call"),
    ],
)
def test_still_refused(expr: str, why: str) -> None:  # noqa: ARG001 - `why` names the case
    with pytest.raises(ExecutionError):
        validate_expression(expr)


def test_a_loop_variable_outside_its_loop_is_refused() -> None:
    with pytest.raises(ExecutionError, match="Disallowed name 'x'"):
        validate_expression("[x for x in inputs['a']] + [x]")


def test_iterating_text_is_refused() -> None:
    with pytest.raises(ExecutionError, match="loop over a list"):
        safe_eval("[c for c in inputs['s']]", {"s": "abc"})


def test_the_loop_budget_stops_a_runaway_product() -> None:
    big = {"a": list(range(1000))}
    with pytest.raises(ExecutionError, match="more than"):
        safe_eval("[x for x in inputs['a'] for y in inputs['a']]", big)


def test_a_generator_sees_inputs_and_helpers() -> None:
    # A generator is its own scope: it must read `inputs` and helpers from the one globals dict.
    data = {"pages": [{"url": "ab"}, {"url": "cde"}], "min": 2}
    assert safe_eval("sum(len(p['url']) for p in inputs['pages'] if len(p['url']) > inputs['min'] - 1)", data) == 5
    assert safe_eval("any(p['url'] == 'ab' for p in inputs['pages'])", data) is True


def test_enumerate_and_zip_pair_by_position() -> None:
    data = {"a": ["x", "y"], "b": [10, 20, 30]}
    assert safe_eval("[[i, v] for i, v in enumerate(inputs['a'])]", data) == [[0, "x"], [1, "y"]]
    assert safe_eval("[{'name': n, 'score': s} for n, s in zip(inputs['a'], inputs['b'])]", data) == [
        {"name": "x", "score": 10},
        {"name": "y", "score": 20},
    ]


@pytest.mark.parametrize(
    "expr",
    [
        "[1 for inputs['a'] in [5]]",
        "[1 for *x in inputs['a']]",
        "str(x for x in inputs['a'])",
        "[(x for x in inputs['a'])]",
        "len(x for x in inputs['a'])",
    ],
)
def test_targets_and_generators_are_structural(expr: str) -> None:
    with pytest.raises(ExecutionError):
        validate_expression(expr)


def test_the_payload_is_never_written() -> None:
    data = {"a": [1, 2]}
    safe_eval("[x for x in inputs['a']]", data)
    assert data == {"a": [1, 2]}


def test_constants_count_against_the_budget() -> None:
    with pytest.raises(ExecutionError, match="more than"):
        safe_eval("sum(1 for a in [0] * 1000 for b in [0] * 1000)", {})
