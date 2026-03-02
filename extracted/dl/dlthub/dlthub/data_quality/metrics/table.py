from dlt.common.libs.ibis import ibis, ir

from dlthub.data_quality.metrics import _base


class row_count(_base.TableMetricDefinition):
    """Row count in table"""

    def expr(self, table: ir.Table) -> ir.IntegerScalar:
        return table.count()


class null_row_count(_base.TableMetricDefinition):
    """Number of nulls in table"""

    def expr(self, table: ir.Table) -> ir.IntegerScalar:
        return table.filter(ibis.and_(table[col].isnull() for col in table.columns)).count()


class unique_count(_base.TableMetricDefinition):
    """Number of unique values in table"""

    def expr(self, table: ir.Table) -> ir.IntegerScalar:
        return table.nunique()
