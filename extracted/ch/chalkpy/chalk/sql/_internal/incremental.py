import dataclasses
from datetime import timedelta
from typing import Literal, Optional


@dataclasses.dataclass
class IncrementalSettings:
    """Incremental settings for Chalk SQL queries.

    In `"row"` mode:
    `incremental_column` MUST be set.

    Returns the results represented by this query as a list (like `.all()`), but modifies the query to
    only return "new" results, by adding a clause that looks like:

        ```
        "WHERE <incremental_column> >= <previous_latest_row_timestamp> - <lookback_period>"
        ```

    In `"group"` mode:
    `incremental_column` MUST be set.

    Returns the results represented by this query as a list (like `.all()`), but modifies the query to
    only results from "groups" which have changed since the last run of the query.

    This works by (1) parsing your query, (2) finding the "group keys", (3) selecting only changed groups.
    Concretely:

        ```
        SELECT user_id, sum(amount) as sum_amount
        FROM payments
        GROUP BY user_id
        ```

    would be rewritten like this:

        ```
        SELECT user_id, sum(amount) as sum_amount
        FROM payments
        WHERE user_id in (
            SELECT DISTINCT(user_id)
            FROM payments WHERE created_at >= <previous_latest_row_timestamp> - <lookback_period>
        )
        GROUP BY user_id
        ```

    In "parameter" mode:
    `incremental_column` WILL BE IGNORED.

    This mode is for cases where you want full control of incrementalization. Chalk will not manipulate your query.
    Chalk will include a query parameter named `"chalk_incremental_timestamp"`. Depending on your SQL
    dialect, you can use this value to incrementalize your query with `:chalk_incremental_timestamp` or
    `%(chalk_incremental_timestamp)s`. This will incrementalize your query using the timestamp
    of the latest row that has been ingested.

    Chalk will also include another query parameter named `"chalk_last_execution_timestamp"` that can be used instead.
    This will incrementalize your query using the last time the query was executed.

    incremental_timestamp:

    If incremental_timestamp is "feature_time", we will incrementalize your query using the timestamp
    of the latest row that has been ingested. This is the default.

    If incremental_timestamp is "resolver_execution_time", we will incrementalize your query using the last
    time the query was executed instead.
    """

    mode: Literal["row", "group", "parameter"] = "row"  # "row" or "group" or "parameter"

    lookback_period: Optional[timedelta] = None
    """The amount of overlap to check for late-arriving rows."""

    incremental_column: Optional[str] = None
    """The column on which to incrementalize."""

    incremental_timestamp: Literal["feature_time", "resolver_execution_time"] = "feature_time"
    """The timestamp to set as the lower bound"""
