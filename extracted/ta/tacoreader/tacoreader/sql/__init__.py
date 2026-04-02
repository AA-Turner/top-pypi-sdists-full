"""SQL branch — free SQL queries returning native DataFrames.

Two main branches in tacoreader:
    sql/   → ds.sql(query) → DataFrame  (this package)
    nav/   → ds.filter_*() → TacoDataset
"""

from tacoreader.sql.executor import execute_sql
from tacoreader.sql.flatten import execute_flatten

__all__ = ["execute_sql", "execute_flatten"]