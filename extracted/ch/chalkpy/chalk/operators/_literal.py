from typing import Any, Optional

import pyarrow as pa

from chalk.operators import StaticExpression


class LiteralExpression(StaticExpression):
    _chalk__expression_name = StaticExpression._chalk__expression_prefix + "literal"

    def __init__(self, value: Any, dtype: pa.DataType, name: Optional[str] = None) -> None:
        super().__init__(pa_value=pa.scalar(value, dtype), literal_name=name)
        self.value = value
        self.dtype = dtype
        self.name = name

    def alias(self, name: str) -> StaticExpression:
        return LiteralExpression(self.value, self.dtype, name)
