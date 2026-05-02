"""GenData rule handlers.

Rule registry for the GenData component. Each rule type maps to a handler
function that accepts a rule config dict and returns a pd.Series.
"""
from typing import Optional
from collections.abc import Callable

import pandas as pd

from .date_sequence import DateSequenceRule, generate_date_sequence
from .static_list import StaticListRule, generate_static_list


# Registry mapping rule type strings to handler functions
_RULE_HANDLERS: dict[str, Callable[[dict], pd.Series]] = {
    "date_sequence": generate_date_sequence,
    "static_list": generate_static_list,
}


def get_rule_handler(rule_type: str) -> Optional[Callable[[dict], pd.Series]]:
    """Look up the handler function for a given rule type.

    Args:
        rule_type: The rule type identifier (e.g. 'date_sequence').

    Returns:
        The handler function, or None if not found.
    """
    return _RULE_HANDLERS.get(rule_type)


def register_rule(rule_type: str, handler: Callable[[dict], pd.Series]) -> None:
    """Register a new rule handler.

    Args:
        rule_type: The rule type identifier.
        handler: A callable that accepts a rule config dict and returns a pd.Series.
    """
    _RULE_HANDLERS[rule_type] = handler


__all__ = [
    "get_rule_handler",
    "register_rule",
    "DateSequenceRule",
    "generate_date_sequence",
    "StaticListRule",
    "generate_static_list",
]
