from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Mapping

from chalk.sql._internal.incremental import IncrementalSettings

if TYPE_CHECKING:
    from chalk.sql.finalized_query import Finalizer


@dataclass
class SQLResolverSettings:
    finalizer: Finalizer
    incremental_settings: IncrementalSettings | None
    fields_root_fqn: Mapping[str, str]  # column name -> root fqn of output feature
    params_to_root_fqn: Mapping[str, str]  # escaped param name -> root fqn of input feature
    field_types: Mapping[str, str] = field(default_factory=dict)  # column name -> SQL type string (e.g., "uuid")
    use_native_sql: bool | None = None  # Native SQL override where possible. None defers to environment/planner opts.
    is_chalk_sql_source: bool = False
    """Set by `-- source: chalksql`. The query targets no external datasource: the engine compiles it
    into a logical plan with its own SQL compiler."""
