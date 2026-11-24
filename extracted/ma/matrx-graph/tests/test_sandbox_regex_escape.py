"""regex_escape: a person's word inside a pattern matches only itself.

Live 2026-11-14 (system_error workflow_run_failed, run fd74e511): "Find a person's accounts" built
``'(?<![a-z0-9])' + surname + '(?![a-z0-9])'`` from a typed name ending "(Netscape)"; the surname
"netscape)" broke the pattern and the whole run failed with "unbalanced parenthesis". Expressions had no
way to escape text, so every workflow building a pattern from input carried the same crash.
"""

from __future__ import annotations

import pytest

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._sandbox import safe_eval

LOOK = "'(?<![a-z0-9])' + {word} + '(?![a-z0-9])'"


def test_the_unescaped_word_still_fails_the_step() -> None:
    expr = f"matches('marc andreessen netscape)', {LOOK.format(word=repr('netscape)'))})"
    with pytest.raises(ExecutionError, match="unbalanced parenthesis"):
        safe_eval(expr, {})


def test_an_escaped_word_matches_only_itself() -> None:
    word = "inputs['surname']"
    expr = f"matches(inputs['title'], {LOOK.format(word=f'regex_escape({word})')})"
    assert safe_eval(expr, {"title": "marc andreessen netscape)", "surname": "netscape)"}) is True
    assert safe_eval(expr, {"title": "marc andreessen netscape", "surname": "netscape)"}) is False
    assert safe_eval(expr, {"title": "o'brien md", "surname": "o'brien"}) is True


def test_lists_and_none() -> None:
    assert safe_eval("regex_escape(['a.b', 'c+'])", {}) == ["a\\.b", "c\\+"]
    assert safe_eval("regex_escape(None)", {}) is None
