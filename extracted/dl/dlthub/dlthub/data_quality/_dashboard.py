"""Data quality dashboard widget functions for marimo notebooks.

This module provides reusable functions for creating data quality widgets
that can be imported into any marimo notebook.
"""

from typing import Any, Optional

import dlt
import marimo as mo
import pyarrow.compute as pc
from dlt.destinations.exceptions import DatabaseUndefinedRelation

from dlthub import data_quality as dq
from dlthub.data_quality.storage import (
    TABLE_NAME_COL,
    QUALIFIED_CHECK_NAME_COL,
    ROW_COUNT_COL,
    CHECK_SUCCESS_COUNT_COL,
    CHECK_SUCCESS_RATE_COL,
)


def create_data_quality_controls(
    pipeline: Optional[dlt.Pipeline] = None,
) -> tuple[
    Optional[mo.ui.checkbox],
    Optional[mo.ui.dropdown],
    Optional[mo.ui.slider],
    Optional[Any],
]:
    """Create filter controls for the data quality widget.

    This function creates UI controls for filtering data quality check results.
    Import and call this function from your marimo notebook to get the controls.

    Args:
        dlt_pipeline: The dlt pipeline instance

    Returns:
        Tuple of (show_only_failed_checkbox, table_dropdown, failure_rate_slider, checks_arrow)
        or (None, None, None, None) if not available

    Example:
        ```python
        from dlthub.data_quality._dashboard import create_data_quality_controls

        checkbox, dropdown, slider, checks_data = create_data_quality_controls(pipeline)
        ```
    """
    if pipeline is None:
        return None, None, None, None

    dataset = pipeline.dataset()
    try:
        checks_table = dq.read_check(dataset).arrow()
    # maybe this is not the best mechanism
    except DatabaseUndefinedRelation:
        return None, None, None, None

    if checks_table.num_rows == 0:
        return None, None, None, checks_table

    table_names = sorted(pc.unique(checks_table.column(TABLE_NAME_COL)).to_pylist())
    show_only_failed_checkbox = mo.ui.checkbox(
        value=False,
        label="<small>Show only failed checks</small>",
    )
    table_dropdown = (
        mo.ui.dropdown(
            options=["All"] + table_names,
            value="All",
            label="<small>Filter by Table</small>",
        )
        if table_names
        else None
    )
    failure_rate_slider = mo.ui.slider(
        start=0,
        stop=100,
        step=1,
        value=0,
        label="<small>Minimum Failure Rate (%)<small>",
    )
    return show_only_failed_checkbox, table_dropdown, failure_rate_slider, checks_table


def _style_failed_cells(row_id: str, column_name: str, value: Any) -> dict[str, Any]:
    """Style Success Rate cells with red background when < 1.0."""
    if column_name == "Success Rate" and value is not None:
        try:
            if float(value) < 1.0:
                return {"backgroundColor": "#ffebee", "color": "#c62828"}
        except (ValueError, TypeError):
            pass
    return {}


def _split_check_name(qualified_name: str) -> tuple[str, str]:
    left, _, right = qualified_name.partition("__")
    if right:
        return left, right  # column, check_name
    return "", left


# TODO many operations operate row-wise, but could be vectorized
# using `pyarrow`, `polars`, or `pandas`. Using `pandas` or `polars`
# instead of `pyarrow` would enable native filtering in the marimo table widget.
# However, this would add a new Python dependency.
def data_quality_widget(
    dlt_pipeline: Optional[dlt.Pipeline] = None,
    failure_rate_slider: Optional[mo.ui.slider] = None,
    failure_rate_filter_value: Optional[float] = None,
    show_only_failed_checkbox: Optional[mo.ui.checkbox] = None,
    show_only_failed_value: Optional[bool] = False,
    table_dropdown: Optional[mo.ui.dropdown] = None,
    table_name_filter_value: Optional[str] = None,
    checks_arrow: Optional[Any] = None,
) -> mo.Html | None:
    """Create a data quality widget displaying check results.

    This function builds a marimo vstack with data quality check results,
    including filtering controls and a styled table.

    Args:
        dlt_pipeline: The dlt pipeline instance to get checks from
        failure_rate_slider: Optional slider control to display
        failure_rate_filter_value: Optional minimum failure rate to filter by
        show_only_failed_checkbox: Optional checkbox control to display
        show_only_failed_value: Boolean to show only failed checks
        table_dropdown: Optional dropdown control to display
        table_name_filter_value: Optional table name to filter by
        checks_arrow: Optional PyArrow table with check results

    Returns:
        mo.vstack with the widget UI, or None if checks are not available

    Example:
        ```python
        from dlthub.data_quality._dashboard import (
            create_data_quality_controls,
            data_quality_widget
        )

        # In cell 1: Create controls
        checkbox, dropdown, slider, checks_data = create_data_quality_controls(pipeline)

        # In cell 2: Display widget (access .value in separate cell for reactivity)
        widget = data_quality_widget(
            dlt_pipeline=pipeline,
            show_only_failed_checkbox=checkbox,
            show_only_failed_value=checkbox.value if checkbox else False,
            table_dropdown=dropdown,
            table_name_filter_value=dropdown.value if dropdown else None,
            failure_rate_slider=slider,
            failure_rate_filter_value=slider.value if slider else None,
            checks_arrow=checks_data,
        )
        widget
        ```
    """
    _result: list[Any] = []

    if not dlt_pipeline:
        _result.append(mo.md("**No pipeline selected.**"))
        return mo.vstack(_result) if _result else None

    try:
        if checks_arrow is None or checks_arrow.num_rows == 0:
            _result.append(
                mo.callout(
                    "**No checks found:** Checks have not been executed yet for this dataset.",
                    kind="info",
                )
            )
            return mo.vstack(_result) if _result else None

        # Convert to list of dictionaries using PyArrow
        records = checks_arrow.to_pylist()

        if not records:
            _result.append(
                mo.callout(
                    "**No check results found:** Checks Table exists but is empty.", kind="info"
                )
            )
            return mo.vstack(_result) if _result else None

        # Process records: add computed columns
        processed_records = []
        for record in records:
            qualified_name = record.get(QUALIFIED_CHECK_NAME_COL, "")
            column, check_name = _split_check_name(qualified_name)

            row_count = record.get(ROW_COUNT_COL, 0)
            success_count = record.get(CHECK_SUCCESS_COUNT_COL, 0)

            # Add computed columns
            new_record = {
                **record,
                "column": column,
                "check_name": check_name,
                "is_failed": row_count > success_count,
                "failure_rate_pct": (
                    round((row_count - success_count) / row_count * 100, 4)
                    if row_count > 0
                    else 0.0
                ),
            }
            processed_records.append(new_record)

        # Apply filters using the provided values
        filtered_records = processed_records.copy()

        if table_name_filter_value and table_name_filter_value != "All":
            filtered_records = [
                r for r in filtered_records if r.get(TABLE_NAME_COL) == table_name_filter_value
            ]

        if failure_rate_filter_value is not None and failure_rate_filter_value > 0:
            filtered_records = [
                r
                for r in filtered_records
                if r.get("failure_rate_pct", 0) >= failure_rate_filter_value
            ]

        # Determine which checks to show based on filter
        failed_records = [r for r in filtered_records if r.get("is_failed", False)]
        total_failed = len(failed_records)
        total_checks = len(filtered_records)

        # Apply "show only failed" filter if enabled
        if show_only_failed_value:
            display_records = failed_records
            if len(display_records) == 0:
                _result.append(mo.md("**No failed checks match the current filters.**"))
                # Still show controls if provided
                controls_empty: list[Any] = []
                if show_only_failed_checkbox is not None:
                    controls_empty.append(show_only_failed_checkbox)
                if table_dropdown is not None:
                    controls_empty.append(table_dropdown)
                if failure_rate_slider is not None:
                    controls_empty.append(failure_rate_slider)
                if controls_empty:
                    _result.append(mo.hstack(controls_empty, justify="start", gap=2))
                return mo.vstack(_result) if _result else None
            else:
                _result.append(
                    mo.md(f"## Failed Checks Only - {total_failed} of {total_checks} failed")
                )
        else:
            # Show all checks by default
            display_records = filtered_records
            if total_failed == 0:
                _result.append(mo.md(f"## All Checks - {total_checks} checks passed"))
            else:
                _result.append(mo.md(f"## All Checks - {total_failed} of {total_checks} failed"))

        # Add filter controls if provided (for display only)
        controls_display: list[Any] = []
        if show_only_failed_checkbox is not None:
            controls_display.append(show_only_failed_checkbox)
        if table_dropdown is not None:
            controls_display.append(table_dropdown)
        if failure_rate_slider is not None:
            controls_display.append(failure_rate_slider)
        if controls_display:
            _result.append(mo.hstack(controls_display, justify="start", gap=2))

        # Prepare display columns with renamed keys
        column_mapping = {
            TABLE_NAME_COL: "Table",
            "column": "Column",
            "check_name": "Check",
            ROW_COUNT_COL: "Row Count",
            CHECK_SUCCESS_COUNT_COL: "Success Count",
            CHECK_SUCCESS_RATE_COL: "Success Rate",
            "failure_rate_pct": "Failure Rate (%)",
        }

        # Select and rename columns for display
        table_records = []
        for record in display_records:
            new_record = {
                column_mapping.get(key, key): record.get(key)
                for key in [
                    TABLE_NAME_COL,
                    "column",
                    "check_name",
                    ROW_COUNT_COL,
                    CHECK_SUCCESS_COUNT_COL,
                    CHECK_SUCCESS_RATE_COL,
                    "failure_rate_pct",
                ]
            }
            table_records.append(new_record)

        _result.append(mo.ui.table(table_records, style_cell=_style_failed_cells))

        # Add summary statistics (using original records, not filtered)
        total_checks_all = len(processed_records)
        total_failed_all = sum(1 for r in processed_records if r.get("is_failed", False))
        if total_checks_all > 0:
            _result.append(
                mo.md(
                    f"<small>**Summary:** {total_failed_all} failed out of "
                    f"{total_checks_all} total checks "
                    f"({total_failed_all / total_checks_all * 100:.1f}% failure rate)</small>"
                )
            )

    except Exception as e:
        _result.append(
            mo.callout(
                mo.md(f"**Error loading checks:** {str(e)}"),
                kind="danger",
            )
        )

    return mo.vstack(_result) if _result else None
