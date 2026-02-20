from typing import Any, Union

from chalk.features import Feature, Features
from chalk.features._encoding.inputs import features_to_columnar
from chalk.features.dataframe._impl import DataFrame
from chalk.features.feature_wrapper import FeatureWrapper
from chalk.utils.missing_dependency import MissingDependencyException, missing_dependency_exception


def assert_frame_equal(
    left: DataFrame,
    right: DataFrame,
    check_column_order: bool = True,
    check_row_order: bool = True,
):
    """Given two `DataFrame`s, `left` and `right`, check if `left == right`,
    and raise otherwise.

    Parameters
    ----------
    left
        The `DataFrame` to compare.
    right
        The `DataFrame` to compare with.
    check_column_order
        If `False`, allows the assert/test to succeed if the required columns are present,
        irrespective of the order in which they appear.
    check_row_order
        If `False`, allows the assert/test to succeed if the required rows are present,
        irrespective of the order in which they appear; as this requires
        sorting, you cannot set on frames that contain un-sortable columns.

    Raises
    ------
    AssertionError
        If `left` does not equal `right`
    MissingDependencyException
        If `chalkpy[runtime]` is not installed.
    """
    try:
        import polars.testing
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    return polars.testing.assert_frame_equal(
        left.to_polars().collect(),
        right.to_polars().collect(),
        check_row_order=check_row_order,
        check_column_order=check_column_order,
    )


def check_expression(
    feature: Union[Feature, FeatureWrapper, Any],
    assertions: list[Features],
    show_table: bool = False,
    float_rel_tolerance: float = 1e-6,
    float_abs_tolerance: float = 1e-12,
):
    """Check that an underscore expression produces the expected values.

    Parameters
    ----------
    feature
        The feature with an underscore expression to check.
    assertions
        A list of feature instances containing the input values and expected output values.
    show_table
        If `True`, always display a table showing the comparison results.
        If `False` (default), only display the table when there are mismatches.
    float_rel_tolerance
        Relative tolerance for float comparisons. Two floats are considered equal if
        `abs(a - b) <= float_rel_tolerance * max(abs(a), abs(b))`. Default is 1e-6.
    float_abs_tolerance
        Absolute tolerance for float comparisons. Two floats are considered equal if
        `abs(a - b) <= float_abs_tolerance`. Default is 1e-12.
        If both tolerances are specified, values are considered equal if either tolerance is met.

    Raises
    ------
    ValueError
        If the feature does not have an associated underscore expression.
    AssertionError
        If any computed values don't match the expected values.
    MissingDependencyException
        If chalkdf is not installed.
    """
    from rich.console import Console
    from rich.table import Table

    from chalk.client._internal_models.check import Color

    underlying: Any = feature._chalk_underlying  # pyright: ignore[reportAttributeAccessIssue, reportPrivateUsage]
    if underlying.underscore_expression is None:
        raise ValueError(
            f"Feature '{underlying.fqn}' does not have an associated expression. "
            + "Only features defined with underscore expressions (e.g., `_.foo + _.bar`) can be checked."
        )

    import os

    # Suppress libchalk info logs during import
    old_log_level = os.environ.get("LIBCHALK_LOG_LEVEL")
    os.environ["LIBCHALK_LOG_LEVEL"] = "error"

    try:
        from chalkdf import DataFrame as DF  # pyright: ignore[reportMissingImports]
    except ImportError:
        raise MissingDependencyException(
            "chalkdf is needed to run `check_expression`. "
            + "Please install it as dev dependency via `pip install chalkdf`."
        )
    finally:
        # Restore original log level
        if old_log_level is None:
            os.environ.pop("LIBCHALK_LOG_LEVEL", None)
        else:
            os.environ["LIBCHALK_LOG_LEVEL"] = old_log_level

    import pyarrow as pa

    columnar = features_to_columnar(assertions)
    feature_name = underlying.name

    if feature_name not in columnar:
        raise ValueError(
            f"Feature '{underlying.fqn}' not found in inputs. "
            + "Make sure to include the expected value in your input instances."
        )

    expected_values = columnar[feature_name]
    df = DF(columnar)

    # Compute the expression result
    expression_result = df.with_columns(underlying.underscore_expression.alias("__computed__")).run()

    # Convert to arrow to access the computed column
    if hasattr(expression_result, "to_arrow"):
        result_arrow = expression_result.to_arrow()
    elif isinstance(expression_result, pa.Table):
        result_arrow = expression_result
    else:
        raise TypeError(
            f"Unexpected result type from chalkdf run(): {type(expression_result)}. "
            + "Expected a pyarrow Table or an object with to_arrow() method."
        )

    computed_values = result_arrow.column("__computed__").to_pylist()

    # Build input values for display (exclude the feature being checked)
    input_columns = {k: v for k, v in columnar.items() if k != feature_name}

    def format_inputs(row_idx: int) -> str:
        parts = []
        for col_name, values in input_columns.items():
            parts.append(f"{col_name}={values[row_idx]!r}")
        return ", ".join(parts)

    def _values_match(expected: Any, computed: Any) -> bool:
        """Check if two values match, with tolerance for floats."""
        from chalk.utils.comparison import floats_are_close

        # Exact match short circuit
        if expected == computed:
            return True
        # Float tolerance comparison
        if isinstance(expected, (float, int)) and isinstance(computed, (float, int)):
            return floats_are_close(expected, computed, float_rel_tolerance, float_abs_tolerance)
        return False

    # Build comparison results
    mismatches = []
    for i, (expected, computed) in enumerate(zip(expected_values, computed_values)):
        is_match = _values_match(expected, computed)
        if not is_match:
            mismatches.append(i)

    # Show table if requested or if there are mismatches
    if show_table or mismatches:
        console = Console()
        expression_str = str(underlying.underscore_expression)
        result_table = Table(title=f"Expression Check: {underlying.fqn} = {expression_str}", title_justify="left")
        result_table.add_column("Inputs", overflow="fold", max_width=60)
        result_table.add_column("Expected", max_width=30)
        result_table.add_column("Computed", max_width=30)
        result_table.add_column("Status", max_width=10)

        for i, (expected, computed) in enumerate(zip(expected_values, computed_values)):
            is_match = _values_match(expected, computed)
            status = Color.render("Match", Color.G) if is_match else Color.render("Mismatch", Color.R)
            result_table.add_row(
                format_inputs(i),
                str(expected),
                str(computed),
                status,
            )

        print()
        console.print(result_table)

    if mismatches:
        # Use pytest.fail with pytrace=False to suppress stack trace
        fail_msg = (
            f"Expression check failed for '{underlying.fqn}': "
            + f"{len(mismatches)} of {len(expected_values)} rows had mismatches (rows: {mismatches})"
        )
        try:
            import pytest

            pytest.fail(fail_msg, pytrace=False)
        except ImportError:
            raise AssertionError(fail_msg)


__all__ = ["assert_frame_equal", "check_expression"]
