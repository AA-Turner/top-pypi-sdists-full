from collections.abc import Mapping, Sequence
from typing import Any

# Either a dict of named params (for SQLite)
# or an ordered sequence of values (for Postgres)
DBParams = Mapping[str, Any] | Sequence[Any] | None

try:
    from sqlalchemy.sql.expression import Executable

    DBQuery = str | Executable
except ImportError:  # sqlalchemy not installed
    DBQuery = str  # type: ignore[misc]
