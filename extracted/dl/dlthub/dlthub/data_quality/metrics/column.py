from dlt.common.libs.ibis import ir
from dlthub.data_quality.metrics import _base


class maximum(_base.ColumnMetricDefinition):
    """Maximum value in {column}"""

    def expr(self, column: ir.Column) -> ir.Scalar:
        return column.max()


class minimum(_base.ColumnMetricDefinition):
    """Minimum value in {column}"""

    def expr(self, column: ir.Column) -> ir.Scalar:
        return column.min()


class null_count(_base.ColumnMetricDefinition):
    """Number of nulls in {column}"""

    def expr(self, column: ir.Column) -> ir.IntegerScalar:
        return column.isnull().sum()


class null_rate(_base.ColumnMetricDefinition):
    """Rate of nulls in {column}"""

    def expr(self, column: ir.Column) -> ir.NumericScalar:
        return column.isnull().sum() / column.count()


class unique_count(_base.ColumnMetricDefinition):
    """Number of unique values in {column}"""

    def expr(self, column: ir.Column) -> ir.IntegerScalar:
        return column.nunique()


class mean(_base.ColumnMetricDefinition):
    """Mean value in {column}"""

    def expr(self, column: ir.Column) -> ir.NumericScalar:
        return column.mean()


class median(_base.ColumnMetricDefinition):
    """Median value in {column}"""

    def expr(self, column: ir.Column) -> ir.Scalar:
        return column.median()


class mode(_base.ColumnMetricDefinition):
    """Median value in {column}"""

    def expr(self, column: ir.Column) -> ir.Scalar:
        return column.mode()


class quantile(_base.ColumnMetricDefinition):
    """Quantile {quantile} value in {column}"""

    def __init__(self, column: str, *, quantile: float) -> None:
        self._column = column
        self._arguments = {"quantile": quantile}

    def expr(self, column: ir.Column) -> ir.Scalar:
        return column.quantile(self._arguments["quantile"])


class standard_deviation(_base.ColumnMetricDefinition):
    """Standard deviation of {column}"""

    def expr(self, column: ir.Column) -> ir.NumericScalar:
        return column.std()


class sum(_base.ColumnMetricDefinition):
    """Sum of {column}"""

    def expr(self, column: ir.Column) -> ir.NumericScalar:
        return column.sum()


class average_length(_base.ColumnMetricDefinition):
    """Average length of {column}"""

    def expr(self, column: ir.Column) -> ir.NumericScalar:
        return column.length().mean()


class minimum_length(_base.ColumnMetricDefinition):
    """Minimum length of {column}"""

    def expr(self, column: ir.Column) -> ir.IntegerScalar:
        return column.length().min()


class maximum_length(_base.ColumnMetricDefinition):
    """Maximum length of {column}"""

    def expr(self, column: ir.Column) -> ir.IntegerScalar:
        return column.length().max()
