from __future__ import annotations

import dataclasses
from datetime import timedelta
from typing import Any, Literal, Optional


@dataclasses.dataclass
class IncrementalConfig:
    """Incremental settings for online and offline Python resolvers.

    When a resolver is marked as incremental, Chalk will track the last time the resolver
    was executed and pass that information to the resolver so it can return only new data.

    Parameters
    ----------
    mode
        The incrementalization mode. One of:
        - ``"row"`` (default): Chalk tracks the maximum value of ``incremental_column``
          across all previously-returned rows. On each run, the resolver is expected to
          return only rows where ``incremental_column >= max_previous_value - lookback_period``.
        - ``"group"``: Like ``"row"``, but for GROUP BY queries. Chalk re-runs groups that
          have seen new rows since the last execution.
        - ``"parameter"``: Chalk provides the incremental timestamp as a parameter
          (``chalk_incremental_timestamp``) that the resolver can use however it likes.
    lookback_period
        The amount of overlap to check for late-arriving rows. Accepts a chalk duration
        string like ``"60m"`` or a ``timedelta``. For example, ``"1d"`` will cause Chalk
        to re-process rows from the last day on every run.
    incremental_column
        A reference to the feature (or column) used to determine which rows are new.
        For example, ``SomeFeature.updated_at``. Required for ``"row"`` and ``"group"`` modes.
        Can also be a string column name.
    incremental_timestamp
        Determines how the incremental lower-bound timestamp is computed:
        - ``"feature_time"`` (default): use the timestamp of the latest ingested row.
        - ``"resolver_execution_time"``: use the timestamp of the last resolver execution.

    Examples
    --------
    >>> @offline(incremental=IncrementalConfig(
    ...     mode="row",
    ...     lookback_period="60m",
    ...     incremental_column=Transaction.updated_at,
    ... ))
    ... def get_transactions(
    ...     id: Transaction.id,
    ... ) -> DataFrame[Transaction.id, Transaction.amount]:
    ...     ...
    """

    mode: Literal["row", "group", "parameter"] = "row"

    lookback_period: Optional[str | timedelta] = None
    """The amount of overlap to check for late-arriving rows. Accepts a duration string like '60m' or a timedelta."""

    incremental_column: Optional[Any] = None
    """A feature reference (e.g. MyFeature.updated_at) or column name string used to identify new rows."""

    incremental_timestamp: Literal["feature_time", "resolver_execution_time"] = "feature_time"
    """Whether to use the latest ingested row timestamp or the last resolver execution timestamp."""
