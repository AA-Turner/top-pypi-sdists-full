from typing import Optional

from chalk.operators import StaticExpression


class ColumnExpression(StaticExpression):
    _chalk__expression_name = StaticExpression._chalk__expression_prefix + "column"

    def __init__(self, source_column: str, alias: Optional[str] = None) -> None:
        super().__init__(source_column=source_column, aliased_name=alias)
        self.source_column = source_column
        self.aliased_name = alias

    def alias(self, name: str) -> StaticExpression:
        return ColumnExpression(self.source_column, alias=name)

    def final_name(self) -> str:
        return self.aliased_name or self.source_column
