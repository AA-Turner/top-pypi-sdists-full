"""Native typed decision execution.

Decision calls are deliberately separate from chat configuration and loops.

``kinds`` (the contracts) must stay importable from the message-part layer
without dragging in the catalog/provider stack, so the runner exports are
resolved lazily: importing ``matrx_ai.decisions.kinds`` costs pydantic and
``matrx_graph`` and nothing else.
"""

from typing import TYPE_CHECKING, Any

from .kinds import DecisionAnswer, DecisionAnswers, DecisionQuestion, DecisionQuestions

if TYPE_CHECKING:
    from .runner import DecisionExecutionResult, DecisionRequest, execute_decision

_LAZY = {
    "DecisionExecutionResult": "runner",
    "DecisionRequest": "runner",
    "execute_decision": "runner",
}


def __getattr__(name: str) -> Any:
    module_name = _LAZY.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    import importlib

    module = importlib.import_module(f".{module_name}", __name__)
    value = getattr(module, name)
    globals()[name] = value
    return value


__all__ = [
    "DecisionAnswer",
    "DecisionAnswers",
    "DecisionExecutionResult",
    "DecisionQuestion",
    "DecisionQuestions",
    "DecisionRequest",
    "execute_decision",
]
