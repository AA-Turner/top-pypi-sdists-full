from __future__ import annotations

from dataclasses import dataclass
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
