import asyncio
from typing import Any, Optional
from collections.abc import Callable

import pandas as pd

from ..exceptions import ComponentError, ConfigError
from .flow import FlowComponent


class tMerge(FlowComponent):
    """tMerge.

    Overview

        Merges two DataFrames using a database-style join.
        Supports 'inner', 'outer', 'left', 'right', 'cross', **'asof'**,
        and **'cross_func'** join types.

        When ``type: asof`` is used, the component performs a ``pd.merge_asof``
        (temporal nearest-match merge).  This is useful for matching time-series
        events (e.g. kiosk emptiness) to the closest subsequent action (e.g. FSO
        restock visit).

        When ``type: cross_func`` is used, the component performs a cross join
        (cartesian product) followed by a vectorized date-range evaluation.
        For each row, it checks whether a date column from DF1 falls within a
        range defined by two columns in DF2 (inclusive on both sides).  If the
        right boundary is ``NaT``/``None``, the range is treated as open-ended
        (returns ``True``).  The boolean result is stored in ``result_column``
        (default ``"active"``).

    Attributes (common):

        | type     | No  | Join type: inner, outer, left, right, cross, **asof**, **cross_func** |
        | pd_args  | No  | Extra kwargs forwarded to ``pd.merge``                                |

    Attributes (asof-only):

        | left_on        | Yes | Left datetime column for temporal matching           |
        | right_on       | Yes | Right datetime column for temporal matching           |
        | by             | No  | Grouping column(s) — match within same group          |
        | direction      | No  | 'forward' (default), 'backward', or 'nearest'        |
        | tolerance      | No  | Max gap as string, e.g. '60 days'                     |
        | filter_column  | No  | Column to pre-filter left DF (keep matching rows)     |
        | filter_value   | No  | Value for filter_column (default True)                |
        | exclude_filter | No  | Dict {col: val} — exclude rows where col == val       |
        | compute_elapsed| No  | Dict with left/right/hours_col/days_col keys          |

    Attributes (cross_func-only):

        | eval_column    | Yes | Column from DF1 to evaluate against the date range    |
        | range_start    | Yes | Column from DF2: left boundary (inclusive)             |
        | range_end      | Yes | Column from DF2: right boundary (inclusive, NaT=open)  |
        | result_column  | No  | Output boolean column name (default: ``"active"``)     |

    Example (cross merge):

        ```yaml
        tMerge:
          depends:
            - QueryToPandas_1
            - QueryToPandas_2
          type: cross
        ```

    Example (asof merge):

        ```yaml
        tMerge:
          depends:
            - TransformRows_2
            - TransformRows_4
          type: asof
          filter_column: became_empty
          filter_value: true
          left_on: kiosk_history_date
          right_on: visit_date
          by: kiosk_id
          direction: forward
          tolerance: "60 days"
          compute_elapsed:
            left: kiosk_history_date
            right: completed_date
            hours_col: lrw_hours
            days_col: lrw_days
        ```

    Example (cross_func merge):

        ```yaml
        tMerge:
          depends:
            - GenData_weekly
            - QueryToPandas_employees
          type: cross_func
          eval_column: weekly_date
          range_start: start_date
          range_end: termination_date
          result_column: active
        ```
    """

    _version = "1.2.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.df1: Any = None
        self.df2: Any = None
        self.type: str = kwargs.pop('type', 'cross')
        # asof-specific parameters
        self._left_on: Optional[str] = kwargs.pop('left_on', None)
        self._right_on: Optional[str] = kwargs.pop('right_on', None)
        self._by = kwargs.pop('by', None)
        self._direction: str = kwargs.pop('direction', 'forward')
        self._tolerance: Optional[str] = kwargs.pop('tolerance', None)
        self._filter_column: Optional[str] = kwargs.pop('filter_column', None)
        self._filter_value: Any = kwargs.pop('filter_value', True)
        self._exclude_filter: Optional[dict] = kwargs.pop('exclude_filter', None)
        self._compute_elapsed: Optional[dict] = kwargs.pop('compute_elapsed', None)
        # cross_func-specific parameters
        self._eval_column: Optional[str] = kwargs.pop('eval_column', None)
        self._range_start: Optional[str] = kwargs.pop('range_start', None)
        self._range_end: Optional[str] = kwargs.pop('range_end', None)
        self._result_column: str = kwargs.pop('result_column', 'active')
        super(tMerge, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found")
        try:
            self.df1 = self.previous[0].output()
        except IndexError as ex:
            name = self.depends[0]
            raise ComponentError(
                f"Missing LEFT Dataframe: {name}"
            ) from ex
        try:
            self.df2 = self.previous[1].output()
        except IndexError as ex:
            name = self.depends[1]
            raise ComponentError(
                "Missing RIGHT Dataframe"
            ) from ex
        return True

    async def close(self):
        pass

    async def run(self):
        if self.type == "asof":
            return await self._run_asof()
        if self.type == "cross_func":
            return await self._run_cross_func()
        return await self._run_merge()

    async def _run_merge(self):
        """Standard pd.merge path."""
        try:
            args = self.pd_args if hasattr(self, "pd_args") else {}
            df = pd.merge(self.df1, self.df2, how=self.type, **args)
            self._result = df
            self.add_metric("NUM_ROWS", self._result.shape[0])
            self.add_metric("NUM_COLUMNS", self._result.shape[1])
            if self._debug:
                self._print_debug(df)
            return self._result
        except (ValueError, KeyError) as err:
            raise ComponentError(f"tMerge Error: {err!s}") from err
        except Exception as err:
            raise ComponentError(f"tMerge error {err!s}") from err

    async def _run_asof(self):
        """pd.merge_asof path for temporal nearest-match merges."""
        if not self._left_on or not self._right_on:
            raise ConfigError(
                "tMerge asof requires 'left_on' and 'right_on' parameters"
            )

        left = self.df1.copy()
        right = self.df2.copy()

        # --- Pre-filter left DF ---
        if self._filter_column:
            col = self._filter_column
            if col not in left.columns:
                raise ConfigError(
                    f"filter_column '{col}' not found in left DataFrame"
                )
            left = left[left[col] == self._filter_value].copy()
            if self._debug:
                print(
                    f"tMerge asof: filtered '{col}' == {self._filter_value}"
                    f" → {len(left)} rows"
                )

        if self._exclude_filter and isinstance(self._exclude_filter, dict):
            for col, val in self._exclude_filter.items():
                if col not in left.columns:
                    raise ConfigError(
                        f"exclude_filter column '{col}' not found in left DataFrame"
                    )
                left = left[left[col] != val].copy()
                if self._debug:
                    print(
                        f"tMerge asof: excluded '{col}' == {val}"
                        f" → {len(left)} rows"
                    )

        if left.empty:
            raise ComponentError(
                "tMerge asof: left DataFrame is empty after filtering"
            )

        # --- Ensure datetime columns ---
        try:
            left[self._left_on] = pd.to_datetime(left[self._left_on])
        except Exception as err:
            raise ComponentError(
                f"Cannot convert left_on '{self._left_on}' to datetime: {err}"
            ) from err
        try:
            right[self._right_on] = pd.to_datetime(right[self._right_on])
        except Exception as err:
            raise ComponentError(
                f"Cannot convert right_on '{self._right_on}' to datetime: {err}"
            ) from err

        # --- Sort by temporal key only (merge_asof needs global sort) ---
        left = left.sort_values(self._left_on).reset_index(drop=True)
        right = right.sort_values(self._right_on).reset_index(drop=True)

        # --- Build merge_asof kwargs ---
        asof_kwargs: dict[str, Any] = {
            "left_on": self._left_on,
            "right_on": self._right_on,
            "direction": self._direction,
            "suffixes": ("_left", "_right"),
        }
        if self._by:
            asof_kwargs["by"] = self._by
        if self._tolerance:
            asof_kwargs["tolerance"] = pd.Timedelta(self._tolerance)

        try:
            df = pd.merge_asof(left, right, **asof_kwargs)
        except (ValueError, KeyError) as err:
            raise ComponentError(
                f"tMerge asof merge error: {err!s}"
            ) from err
        except Exception as err:
            raise ComponentError(
                f"tMerge asof unexpected error: {err!s}"
            ) from err

        # --- Compute elapsed time columns ---
        if self._compute_elapsed and isinstance(self._compute_elapsed, dict):
            elapsed_left = self._compute_elapsed.get("left", self._left_on)
            elapsed_right = self._compute_elapsed.get("right", self._right_on)
            hours_col = self._compute_elapsed.get("hours_col", "elapsed_hours")
            days_col = self._compute_elapsed.get("days_col", "elapsed_days")

            if elapsed_left not in df.columns:
                raise ConfigError(
                    f"compute_elapsed left column '{elapsed_left}' not found"
                )
            if elapsed_right not in df.columns:
                raise ConfigError(
                    f"compute_elapsed right column '{elapsed_right}' not found"
                )

            df[elapsed_left] = pd.to_datetime(df[elapsed_left])
            df[elapsed_right] = pd.to_datetime(df[elapsed_right])
            delta = (df[elapsed_right] - df[elapsed_left]).dt.total_seconds()
            df[hours_col] = delta / 3600
            df[days_col] = delta / 86400

        # --- Metrics and debug ---
        self._result = df
        self.add_metric("NUM_ROWS", self._result.shape[0])
        self.add_metric("NUM_COLUMNS", self._result.shape[1])
        matched = self._result[self._right_on].notna().sum()
        unmatched = self._result[self._right_on].isna().sum()
        self.add_metric("MATCHED_ROWS", int(matched))
        self.add_metric("UNMATCHED_ROWS", int(unmatched))

        if self._debug:
            print(f"tMerge asof: {len(df)} total rows, "
                  f"{matched} matched, {unmatched} unmatched")
            self._print_debug(df)

        return self._result

    async def _run_cross_func(self):
        """Cross join + vectorized date-range evaluation.

        Performs a cartesian product of DF1 and DF2, then checks whether
        ``eval_column`` falls within the ``[range_start, range_end]`` interval.
        If ``range_end`` is NaT/None the range is treated as open-ended.
        The boolean result is stored in ``result_column``.
        """
        if not self._eval_column or not self._range_start or not self._range_end:
            raise ConfigError(
                "tMerge cross_func requires 'eval_column', 'range_start', "
                "and 'range_end' parameters"
            )

        # 1. Cross join
        try:
            df = pd.merge(self.df1, self.df2, how='cross')
        except (ValueError, KeyError) as err:
            raise ComponentError(
                f"tMerge cross_func cross-join error: {err!s}"
            ) from err

        # 2. Validate columns exist in merged DataFrame
        for col in (self._eval_column, self._range_start, self._range_end):
            if col not in df.columns:
                similar = [c for c in df.columns if c.startswith(col)]
                hint = (
                    f" (found {similar} — possible suffix collision "
                    f"from shared column names)"
                    if similar else ""
                )
                raise ComponentError(
                    f"tMerge cross_func: column '{col}' not found "
                    f"after cross join{hint}"
                )

        # 3. Coerce to datetime
        for col in (self._eval_column, self._range_start, self._range_end):
            df[col] = pd.to_datetime(df[col], errors='coerce')

        # 4. Vectorized range check (inclusive, open right if NaT)
        after_start = df[self._eval_column] >= df[self._range_start]
        end_is_open = df[self._range_end].isna()
        before_end = df[self._eval_column] <= df[self._range_end]
        df[self._result_column] = after_start & (end_is_open | before_end)

        # 5. Metrics
        self._result = df
        self.add_metric("NUM_ROWS", df.shape[0])
        self.add_metric("NUM_COLUMNS", df.shape[1])
        active_count = int(df[self._result_column].sum())
        self.add_metric("ACTIVE_COUNT", active_count)
        self.add_metric("INACTIVE_COUNT", df.shape[0] - active_count)

        if self._debug:
            print(
                f"tMerge cross_func: {len(df)} total rows, "
                f"{active_count} active, "
                f"{df.shape[0] - active_count} inactive"
            )
            self._print_debug(df)

        return self._result

    def _print_debug(self, df: pd.DataFrame) -> None:
        """Print column types and first-row values."""
        print("::: Printing Column Information === ")
        if df.empty:
            print("(empty DataFrame)")
            return
        for column, t in df.dtypes.items():
            print(column, "->", t, "->", df[column].iloc[0])
