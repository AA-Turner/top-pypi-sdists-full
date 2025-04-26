from typing import Any

import attrs
import pandas


@attrs.frozen
class SqlExecutor:
    session: Any

    def read_sql(self, sql: str) -> pandas.DataFrame:
        raise NotImplementedError
