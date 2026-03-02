"""Data quality module

- A `Check` is a function applied to individual records and returns a boolean (Success/Failure).
- `Checks` are applied to **data**, whereas tests are applied to **code**.
- `Checks` can be applied to a `Source`, a `Resource` or a `Dataset`
- There are 3 `Check outcome`: Success, Failure, Error (the executed code failed)
- An `Action` is a hook that is executed on a failed check; it takes the record and contextual
  metadata as input
- When `Check outcome = Failure`, it triggers an `Alert`, which has 2 levels:
    - `Fail`: data validation exits early; stops `pipeline.run()` if applicable
    - `Warn`: data validation continues and the `Failure` outcome is recorded; this gives the
      opportunity to send telemetry, notification, etc.; user can fix the data downstream
- The `Action` can be configured per `Alert level` instead of per `Check` to make configuration
  more concise
- `Checks` have a configurable `Alert level`;
- `Checks` are implemented using `dlt_plus.transformation`. This allows to define checks using all
  of the supported libraries (SQL, SQLGlot, Ibis, pandas, polars, etc.)
- For SQL-based checks (SQL, SQLGlot, Ibis, Narwhals on Ibis), we can:
    - serialize the check
    - ensure the check is valid (returns boolean, correct cardinality, etc.)
- `Checks` are used following two main patterns:
    1. `incremental`: checks are applied on each load; then all data arriving at destination is
       validated.
    2. `full`: checks are applied on all existing data stored. This is useful when modifying /
       updating data quality checks; you can think of this as "backfilling" the data validation
- `Checks` can be applied at several points during the lifecycle:
    1. Extract: when the `Resource` yields a record
    2. Extract / before Normalization: applied to load packages (i.e., parquet files on disk)
       produced during the Extract phase
    3. Load / after Normalization: applied to load packages after normalization, but before loading
       to destination
    4. Staging destination / after Load: on the staging destination backend
    5. Main destination / after Load: on the main destination backend
    6. On destination; not tied to a specific load: run the check on all data stored on destination
       / in dataset
- `Checks` results need a standardize storage format
- Advanced: `Data quality migration` allow to apply "old checks on old data" and "new checks on new
  data"
    - example: CompanyFoo has 5 divisions in 2024 and they create a check for the field. In 2025,
      they have 1 new division and 1 that was renamed.
    - Can be done with dlt metadata, but probably easier with Iceberg, DuckLake, etc.
- `Checks` should be stored on the `Schema`; This makes them accessible on `Source`, `Resource`,
  `Dataset`, `Pipeline`
    - One issue is that we can't serialize non-SQL `@dlt_plus.transformation`
"""

from __future__ import annotations

from dlthub.data_quality import checks, storage, metrics
from dlthub.data_quality.checks._runner import (
    prepare_checks,
    run_checks,
    CheckSuite,
    data_quality_checks,
)
from dlthub.data_quality.checks._definitions import with_checks
from dlthub.data_quality.checks._reader import read_check
from dlthub.data_quality.metrics._runner import data_quality_metrics, run_metrics
from dlthub.data_quality.metrics._reader import read_metric
from dlthub.data_quality.metrics._definitions import with_metrics


__all__ = (
    "checks",
    "metrics",
    "storage",
    "prepare_checks",
    "run_checks",
    "run_metrics",
    "CheckSuite",
    "read_metric",
    "read_check",
    "data_quality_metrics",
    "with_metrics",
    "data_quality_checks",
    "with_checks",
)
