"""``data.rules`` compiles each rule ONCE per run, not once per item (system_error 8ab188a8).

A long list evaluated every rule through parse + AST walk + compile per item and held the event
loop ~1.7 s. The sandbox now prepares an expression once; the answers must not change.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.nodes import _sandbox
from matrx_graph.nodes.data.rules import RulesConfig, RulesExecutor, RulesInput

from tests._fixtures import make_app_context


def _forget_prepared() -> None:
    prepared = getattr(_sandbox, "_prepared", None)
    if prepared is not None:
        prepared.cache_clear()


def _run(config: dict[str, Any], inputs: dict[str, Any]) -> Any:
    ctx = make_app_context()
    return RulesExecutor()._decide_all(ctx, RulesInput(**inputs), RulesConfig.model_validate(config))  # type: ignore[arg-type]


def test_each_rule_is_validated_once_for_the_whole_list(monkeypatch: Any) -> None:
    _forget_prepared()
    calls: list[str] = []
    real = _sandbox.validate_expression

    def counting(expr: str) -> Any:
        calls.append(expr)
        return real(expr)

    monkeypatch.setattr(_sandbox, "validate_expression", counting)
    config = {
        "items_path": "xs",
        "rules": [
            {"when": "inputs['item'] > 700 + 0", "then": {"label": "big"}},
            {"when": "inputs['item'] % 2 == 0", "then": {"label": "even"}},
        ],
        "default": {"label": "odd"},
    }
    out = _run(config, {"xs": list(range(1000))}).result
    assert out.counts == {"big": 299, "even": 351, "odd": 350}
    assert [i.label for i in out.items[:3]] == ["even", "odd", "even"]
    assert len(calls) == 2  # two rows, not 2 x 1000 items


def test_a_refused_predicate_is_refused_every_time() -> None:
    _forget_prepared()
    for _ in range(2):
        try:
            _sandbox.safe_eval("__import__('os')", {})
        except Exception as e:  # noqa: BLE001
            assert "Disallowed" in str(e)
        else:
            raise AssertionError("a disallowed expression ran")
