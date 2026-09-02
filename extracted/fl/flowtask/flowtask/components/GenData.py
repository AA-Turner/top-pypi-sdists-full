"""GenData Component.

Generate an artificial DataFrame from declarative rules.

Overview:

    GenData reads a list of column rules from YAML configuration,
    evaluates each rule to produce a column (Series), and assembles
    them into a single DataFrame. Multiple rules with different row
    counts are cross-joined.

    | Name      | Required | Summary                              |
    |-----------|----------|--------------------------------------|
    | rules     | Yes      | List of rule configurations          |

    Example:

    ```yaml
      GenData:
        rules:
          - type: date_sequence
            column_name: weekly_date
            firstdate: "{firstdate}"
            lastdate: "{lastdate}"
            interval: 7
            dow: 0
    ```
"""
import asyncio
from collections.abc import Callable
from typing import Any, Optional, Union

import pandas as pd

from ..exceptions import ComponentError
from ..utils import SafeDict
from ..interfaces.flow import FlowComponent
from .gendata import get_rule_handler


class GenData(FlowComponent):
    """Generate an artificial DataFrame from declarative rules.

    Reads a ``rules`` list from YAML config, delegates each rule to the
    appropriate handler, and assembles the results into a single DataFrame.
    Rules with different row counts are cross-joined.

    Attributes:
        rules: List of rule configuration dicts from YAML.

    YAML example::

        GenData:
          rules:
            - type: date_sequence
              column_name: weekly_date
              firstdate: "2024-01-01"
              lastdate: "2026-03-20"
              interval: 7
              dow: 0
    """

    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self._rules_config: list[dict] = []
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    def _resolve_variables_in_value(self, value: Any) -> Any:
        """Resolve pipeline variable placeholders in a value.

        Handles ``{varname}`` placeholders in string values using
        the component's ``_variables`` dict. Non-string values are
        returned unchanged.

        Args:
            value: The value to resolve.

        Returns:
            The resolved value.
        """
        if isinstance(value, str) and "{" in value:
            try:
                resolved = value.format_map(SafeDict(**self._variables))
                return resolved
            except (KeyError, ValueError, IndexError):
                return value
        return value

    def _resolve_variables_in_rules(
        self, rules: list[dict]
    ) -> list[dict]:
        """Resolve pipeline variables in all rule configurations.

        Args:
            rules: List of rule config dicts.

        Returns:
            New list of dicts with variables resolved.
        """
        resolved = []
        for rule in rules:
            resolved_rule = {}
            for key, value in rule.items():
                resolved_rule[key] = self._resolve_variables_in_value(value)
            resolved.append(resolved_rule)
        return resolved

    async def start(self, **kwargs) -> bool:
        """Parse and validate rules from YAML config.

        Reads the ``rules`` attribute set from YAML configuration,
        resolves pipeline variables, and validates each rule type.

        Returns:
            True if initialization succeeded.

        Raises:
            ComponentError: If rules are missing or contain unknown types.
        """
        if not hasattr(self, "rules") or not self.rules:
            raise ComponentError(
                "GenData: 'rules' attribute is required"
            )
        # Resolve pipeline variables in rule values
        self._rules_config = self._resolve_variables_in_rules(self.rules)
        # Validate each rule type
        for rule_config in self._rules_config:
            rule_type = rule_config.get("type")
            if not rule_type:
                raise ComponentError(
                    "GenData: each rule must have a 'type' field"
                )
            handler = get_rule_handler(rule_type)
            if handler is None:
                raise ComponentError(
                    f"GenData: unknown rule type '{rule_type}'"
                )
        self._logger.info(
            "GenData: validated %d rules", len(self._rules_config)
        )
        self.add_metric("RULES_COUNT", len(self._rules_config))
        return True

    @staticmethod
    def _cross_join(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
        """Cross-join two DataFrames.

        Args:
            left: Left DataFrame.
            right: Right DataFrame.

        Returns:
            Cross-joined DataFrame with reset index.
        """
        left = left.copy()
        right = right.copy()
        left["_cj_key"] = 1
        right["_cj_key"] = 1
        result = left.merge(right, on="_cj_key")
        result.drop("_cj_key", axis=1, inplace=True)
        return result.reset_index(drop=True)

    def _assemble_dataframe(
        self, series_list: list[pd.Series]
    ) -> pd.DataFrame:
        """Assemble multiple Series into a DataFrame.

        If all Series have the same length, they are combined directly.
        If lengths differ, a cross-join is performed.

        Args:
            series_list: List of named pd.Series from rule handlers.

        Returns:
            Assembled DataFrame.
        """
        if not series_list:
            return pd.DataFrame()

        if len(series_list) == 1:
            return series_list[0].to_frame()

        # Check if all same length
        lengths = [len(s) for s in series_list]
        if len(set(lengths)) == 1:
            # Same length — simple column concat
            return pd.concat(
                [s.reset_index(drop=True) for s in series_list],
                axis=1,
            )

        # Different lengths — cross-join
        result = series_list[0].to_frame()
        for s in series_list[1:]:
            result = self._cross_join(result, s.to_frame())
        return result

    async def run(self) -> bool:
        """Execute all rules and assemble the output DataFrame.

        Returns:
            True if execution succeeded.
        """
        series_list: list[pd.Series] = []
        for rule_config in self._rules_config:
            rule_type = rule_config["type"]
            handler = get_rule_handler(rule_type)
            series = handler(rule_config)
            series_list.append(series)
            self._logger.debug(
                "GenData: rule '%s' column '%s' produced %d rows",
                rule_type,
                series.name,
                len(series),
            )

        self._result = self._assemble_dataframe(series_list)
        row_count = len(self._result)
        col_count = len(self._result.columns)
        self.add_metric("OUTPUT_ROWS", row_count)
        self.add_metric("OUTPUT_COLUMNS", col_count)
        self._logger.info(
            "GenData: produced DataFrame with %d rows x %d columns",
            row_count,
            col_count,
        )
        return True

    async def close(self):
        """Clean up resources (no-op for GenData)."""
        pass
