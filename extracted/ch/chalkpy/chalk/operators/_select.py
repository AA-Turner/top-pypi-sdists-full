from __future__ import annotations

from typing_extensions import final

from chalk.operators import StaticExpression, StaticOperator
from chalk.operators._column import ColumnExpression
from chalk.operators._literal import LiteralExpression


def get_name_for_expression(expr: StaticExpression) -> str:
    if isinstance(expr, LiteralExpression):
        if expr.name is None:
            raise ValueError("Literal expressions must have a name")
        return expr.name
    if isinstance(expr, ColumnExpression):
        return expr.final_name()
    raise ValueError("Expected a StaticExpression, got {expr}")


@final
class SelectOperator(StaticOperator):
    _chalk__operator_name = StaticOperator._chalk__operator_prefix + "select"

    def __init__(self, parent: StaticOperator, expressions: tuple[StaticExpression, ...]):
        self.column_names = tuple([get_name_for_expression(e) for e in expressions])
        self.expressions = expressions
        self.parent = parent
        super().__init__(parent, *expressions)
