import copy
import dataclasses
import json
import os
from datetime import datetime
from typing import Any, Optional, Union

import pyarrow as pa
import pytest
from rich.console import Console
from rich.table import Table
from rich.text import Text

from chalk import functions as F
from chalk.client._internal_models.check import Color
from chalk.features import Feature, Features, StreamResolver, _
from chalk.features._encoding.inputs import features_to_columnar
from chalk.features.dataframe._impl import DataFrame
from chalk.features.feature_wrapper import FeatureWrapper
from chalk.features.underscore import Underscore, UnderscoreAttr, UnderscoreRoot
from chalk.utils.collections import OrderedSet
from chalk.utils.comparison import floats_are_close
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


def _to_arrow(result: Any) -> Any:
    if hasattr(result, "to_arrow"):
        return result.to_arrow()
    if isinstance(result, pa.Table):
        return result
    raise TypeError(
        f"Unexpected result type from chalkdf run(): {type(result)}. "
        + "Expected a pyarrow Table or an object with to_arrow() method."
    )


def _values_match(expected: Any, computed: Any, float_rel_tolerance: float, float_abs_tolerance: float) -> bool:
    """Check if two values match, with tolerance for floats."""

    # Exact match short circuit
    if expected == computed:
        return True
    # Float tolerance comparison
    if isinstance(expected, (float, int)) and isinstance(computed, (float, int)):
        return floats_are_close(expected, computed, float_rel_tolerance, float_abs_tolerance)
    return False


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
    underlying: Any = feature._chalk_underlying  # pyright: ignore[reportAttributeAccessIssue, reportPrivateUsage]
    if underlying.underscore_expression is None:
        raise ValueError(
            f"Feature '{underlying.fqn}' does not have an associated expression. "
            + "Only features defined with underscore expressions (e.g., `_.foo + _.bar`) can be checked."
        )

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

    result_arrow = _to_arrow(expression_result)

    computed_values = result_arrow.column("__computed__").to_pylist()

    # Build input values for display (exclude the feature being checked)
    input_columns = {k: v for k, v in columnar.items() if k != feature_name}

    def format_inputs(row_idx: int) -> str:
        parts = []
        for col_name, values in input_columns.items():
            parts.append(f"{col_name}={values[row_idx]!r}")
        return ", ".join(parts)

    # Build comparison results
    mismatches = []
    for i, (expected, computed) in enumerate(zip(expected_values, computed_values)):
        is_match = _values_match(expected, computed, float_rel_tolerance, float_abs_tolerance)
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
            is_match = _values_match(expected, computed, float_rel_tolerance, float_abs_tolerance)
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
        pytest.fail(fail_msg, pytrace=False)


@dataclasses.dataclass
class StreamMessage:
    """Contains the raw/expected data for the stream resolver parser."""

    message: bytes
    """The raw message."""

    parsed: Optional[Features]
    """The expected feature output after parsing. Pass a feature class instance, e.g. ``User(id='u1', name='Alice')``."""


def check_stream_parsing(
    resolver: StreamResolver,
    assertions: list[StreamMessage],
    show_table: bool = False,
    float_rel_tolerance: float = 1e-6,
    float_abs_tolerance: float = 1e-12,
):
    """Check that a stream resolver's parser returns the expected results.

    Parameters
    ----------
    resolver
        The stream resolver with parser to be checked.
    assertions
        A list of stream messages containing input message and expected parsed Feature outputs.
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

    Examples
    --------
    >>> from chalk.testing import StreamMessage, check_stream_parsing
    >>> check_stream_parsing(
    ...     my_stream_resolver,
    ...     [
    ...         StreamMessage(
    ...             message=json.dumps({"event_id": 20, "value": 2.5}).encode(),
    ...             parsed=Event(
    ...             event_id=20,
    ...                 value=2.5,
    ...             ),
    ...         ),
    ...     ],
    ... )
    """

    if not resolver.feature_expressions:
        raise ValueError(
            f"Stream resolver '{resolver.fqn}' has no feature expressions. "
            + "check_stream_parsing only works with resolvers created via make_stream_resolver."
        )

    # Suppress libchalk info logs during import
    old_log_level = os.environ.get("LIBCHALK_LOG_LEVEL")
    os.environ["LIBCHALK_LOG_LEVEL"] = "error"

    try:
        from chalkdf import DataFrame as DF  # pyright: ignore[reportMissingImports]
    except ImportError:
        raise MissingDependencyException(
            "chalkdf is needed to run `check_stream_parsing`. "
            + "Please install it as dev dependency via `pip install chalkdf`."
        )
    finally:
        if old_log_level is None:
            os.environ.pop("LIBCHALK_LOG_LEVEL", None)
        else:
            os.environ["LIBCHALK_LOG_LEVEL"] = old_log_level

    def _struct_col_to_table(col: pa.Array) -> pa.Table:
        if isinstance(col.type, pa.StructType):
            return pa.Table.from_arrays(
                [col.field(i) for i in range(col.type.num_fields)],
                names=[col.type.field(i).name for i in range(col.type.num_fields)],
            )
        # JSON extension type: each non-null value is a serialized JSON string.
        rows = [json.loads(v) if v is not None else None for v in col.to_pylist()]
        return pa.Table.from_pylist([r if r is not None else {} for r in rows])

    _replacement = UnderscoreAttr(UnderscoreRoot(), "message")
    _visited: OrderedSet[int] = OrderedSet({id(_replacement)})

    def _rebind_inplace(node: Underscore) -> None:
        """Mutate a deepcopy of the AST in-place, replacing every UnderscoreRoot with _.message.

        Uses a visited set to handle shared references (deepcopy preserves sharing,
        so a node referenced multiple times in the tree must only be mutated once).
        """
        if id(node) in _visited:
            return
        _visited.add(id(node))
        for attr, val in vars(node).items():
            if isinstance(val, UnderscoreRoot):
                setattr(node, attr, _replacement)
            elif isinstance(val, Underscore):
                _rebind_inplace(val)
            elif isinstance(val, (list, tuple)):
                new_seq: list[Any] = []
                for item in val:
                    if isinstance(item, UnderscoreRoot):
                        new_seq.append(_replacement)
                    elif isinstance(item, Underscore):
                        _rebind_inplace(item)
                        new_seq.append(item)
                    else:
                        new_seq.append(item)
                setattr(node, attr, type(val)(new_seq))
            elif isinstance(val, dict):
                for k, v in val.items():
                    if isinstance(v, UnderscoreRoot):
                        val[k] = _replacement
                    elif isinstance(v, Underscore):
                        _rebind_inplace(v)

    if resolver.parse is None:
        message_type = resolver.message
        if message_type is None:
            raise ValueError(f"Stream resolver '{resolver.fqn}' has no parse function and no message type.")
        parse_df = DF({"message": pa.array([a.message for a in assertions], type=pa.large_binary())})
        struct_col = (
            parse_df.with_columns(
                F.json_value(F.bytes_to_string(_.message, "utf-8"), "$").cast(message_type).alias("__parsed__")
            )
            .run()
            .to_arrow()
            .column("__parsed__")
            .combine_chunks()
        )
        flat_table = _struct_col_to_table(struct_col)
    elif resolver.parse.parse_expression is not None:
        parse_df = DF({"message": pa.array([a.message for a in assertions], type=pa.large_binary())})
        rebound_parse = copy.deepcopy(resolver.parse.parse_expression)
        _rebind_inplace(rebound_parse)
        struct_col = (
            parse_df.with_columns({"__parsed__": rebound_parse}).run().to_arrow().column("__parsed__").combine_chunks()
        )
        flat_table = _struct_col_to_table(struct_col)

    def _uses_chalk_now(expr: Any) -> bool:
        """Return True if the underscore expression references _.chalk_now anywhere."""

        if not isinstance(expr, Underscore):
            return False
        if isinstance(expr, UnderscoreAttr) and expr._chalk__attr == "chalk_now":  # pyright: ignore[reportPrivateUsage]
            return True
        for val in vars(expr).values():
            if isinstance(val, Underscore) and _uses_chalk_now(val):
                return True
            if isinstance(val, (list, tuple)):
                for item in val:
                    if isinstance(item, Underscore) and _uses_chalk_now(item):
                        return True
        return False

    feature_order = list(resolver.feature_expressions.keys())
    skipped_features: set[Any] = {
        feat for feat, expr in resolver.feature_expressions.items() if _uses_chalk_now(expr) or feat.is_feature_time
    }
    feature_projections: dict[str, Any] = {
        feat.name: expr for feat, expr in resolver.feature_expressions.items() if feat not in skipped_features
    }
    expression_result = DF(flat_table).project(feature_projections).run()

    result_arrow = _to_arrow(expression_result)

    computed_by_feature: dict[Any, list[Any]] = {
        feat: (result_arrow.column(feat.name).to_pylist() if feat not in skipped_features else [None] * len(assertions))
        for feat in feature_order
    }

    expected_by_feature: dict[Any, list[Any]] = {feat: [] for feat in feature_order}
    for assertion in assertions:
        if assertion.parsed is None:
            for feat in feature_order:
                expected_by_feature[feat].append(None)
        else:
            # features_to_columnar strips the namespace, yielding {field_name: [value]}.
            col = features_to_columnar([assertion.parsed])
            for feat in feature_order:
                expected_by_feature[feat].append(col.get(feat.name, [None])[0])

    row_mismatch_features: list[list[str]] = []
    for i in range(len(assertions)):
        row_issues = [
            feat.name
            for feat in feature_order
            if expected_by_feature[feat][i] is not None
            and not _values_match(
                expected_by_feature[feat][i], computed_by_feature[feat][i], float_rel_tolerance, float_abs_tolerance
            )
        ]
        row_mismatch_features.append(row_issues)

    mismatch_rows = [i for i, issues in enumerate(row_mismatch_features) if issues]

    if show_table or mismatch_rows:
        console = Console()
        result_table = Table(title=f"Stream Parsing Check: {resolver.fqn}", title_justify="left")
        result_table.add_column("Row", max_width=5)
        for feat in feature_order:
            result_table.add_column(f"Expected\n{feat.name}", max_width=30)
            result_table.add_column(f"Computed\n{feat.name}", max_width=30)
        result_table.add_column("Status", max_width=10)

        for i in range(len(assertions)):
            issues = row_mismatch_features[i]
            status = Color.render("Match", Color.G) if not issues else Color.render("Mismatch", Color.R)
            row_data: list[str | Text] = [str(i)]
            for feat in feature_order:
                row_data.append(str(expected_by_feature[feat][i]))
                row_data.append(str(computed_by_feature[feat][i]))
            row_data.append(status)
            result_table.add_row(*row_data)

        print()
        console.print(result_table)

    if mismatch_rows:
        fail_msg = (
            f"Stream parsing check failed for '{resolver.fqn}': "
            + f"{len(mismatch_rows)} of {len(assertions)} messages had mismatches (rows: {mismatch_rows})"
        )
        pytest.fail(fail_msg, pytrace=False)


def _feature_instance_to_dict(instance: Any) -> dict:
    """Recursively convert a feature instance to a full-FQN dict for PyArrow struct arrays."""
    result = {}
    for fqn, value in instance.items():
        if isinstance(value, list) and value and hasattr(value[0], "__chalk_namespace__"):
            result[fqn] = [_feature_instance_to_dict(v) for v in value]
        elif hasattr(value, "__chalk_namespace__"):
            result[fqn] = _feature_instance_to_dict(value)
        else:
            result[fqn] = value
    return result


def check_static_dataframe(
    resolver: Any,
    assertions: list,
    now: Optional[datetime] = None,
    show_table: bool = False,
    float_rel_tolerance: float = 1e-6,
    float_abs_tolerance: float = 1e-12,
) -> None:
    """Check that a ``@online(static=True)`` DataFrame resolver produces the expected values.

    The resolver's return type annotation determines which features are outputs.
    Each assertion instance should contain both input field values and expected
    output field values. The function builds an input-only ``chalkdf.DataFrame``,
    runs the resolver's underlying function against it, then compares each output
    column against the expected values supplied in the assertions.

    Parameters
    ----------
    resolver
        A resolver decorated with ``@online(static=True)`` that accepts a ``DataFrame``
        input and returns a ``DataFrame``.
    assertions
        A list of feature instances containing input values and expected output values.
        Output features are inferred from the resolver's return type annotation.
    now
        If provided, a ``"__chalk__.now"`` column is added to the input DataFrame.
        Required when the resolver's input type annotation includes ``Now``.
    show_table
        If ``True``, always display a comparison table. If ``False`` (default),
        only display the table when there are mismatches.
    float_rel_tolerance
        Relative tolerance for float comparisons. Default is 1e-6.
    float_abs_tolerance
        Absolute tolerance for float comparisons. Default is 1e-12.

    Raises
    ------
    AssertionError
        If any computed output values don't match the expected values.
    MissingDependencyException
        If ``chalkdf`` is not installed.

    Notes
    -----
    Row order in the resolver output is assumed to match the input order. Most
    static resolvers preserve row order via a final left join back to the input
    skeleton, but if yours does not, results may be compared against the wrong
    expected values.

    Examples
    --------
    >>> check_static_dataframe(
    ...     compute_features,
    ...     assertions=[
    ...         Transaction(id="t1", amount=100.0, is_large=True),
    ...         Transaction(id="t2", amount=50.0,  is_large=False),
    ...     ],
    ... )
    """
    try:
        from chalkdf import DataFrame as ChalkDF  # pyright: ignore[reportMissingImports]
    except ImportError:
        raise MissingDependencyException(
            "chalkdf is needed to run `check_static_dataframe`. Please install it via `uv pip install chalkdf`."
        )

    resolver_input_fqns: set = set()
    for inp in resolver.inputs:
        if hasattr(inp, "__columns__"):  # subscripted DataFrame[...] type
            resolver_input_fqns.update(f.fqn for f in inp.__columns__)
        elif hasattr(inp, "fqn"):  # plain Feature
            resolver_input_fqns.add(inp.fqn)

    output_fqns = {f.fqn for f in resolver.flattened_output} - resolver_input_fqns

    columnar = features_to_columnar(assertions, strip_namespace=False)
    input_columnar = {k: v for k, v in columnar.items() if k not in output_fqns}
    expected_columnar = {k: v for k, v in columnar.items() if k in output_fqns}

    arrow_columns: dict = {}
    for col_name, values in input_columnar.items():
        if values and isinstance(values[0], list):
            converted = [
                [_feature_instance_to_dict(item) if hasattr(item, "__chalk_namespace__") else item for item in row]
                for row in values
            ]
            arrow_columns[col_name] = pa.array(converted)
        else:
            arrow_columns[col_name] = pa.array(values)

    if now is not None:
        arrow_columns["__chalk__.now"] = pa.array([now] * len(assertions), type=pa.timestamp("us"))

    chalkdf_input = ChalkDF.from_arrow(pa.table(arrow_columns))
    result_arrow = resolver.fn(chalkdf_input).run().to_arrow()

    all_mismatches: list = []
    computed_by_fqn: dict = {}

    for output_fqn, expected_values in expected_columnar.items():
        try:
            computed_values = result_arrow.column(output_fqn).to_pylist()
        except KeyError:
            raise ValueError(
                f"Output feature '{output_fqn}' not found in resolver result. Available columns: {result_arrow.schema.names}"
            )
        computed_by_fqn[output_fqn] = computed_values
        for i, (expected, computed) in enumerate(zip(expected_values, computed_values)):
            if not _values_match(expected, computed, float_rel_tolerance, float_abs_tolerance):
                all_mismatches.append((output_fqn, i, expected, computed))

    if show_table or all_mismatches:
        console = Console()
        tbl = Table(title="Static DataFrame Resolver Check", title_justify="left")
        tbl.add_column("Feature", overflow="fold")
        tbl.add_column("Row")
        tbl.add_column("Expected", max_width=30)
        tbl.add_column("Computed", max_width=30)
        tbl.add_column("Status", max_width=10)

        for output_fqn, expected_values in expected_columnar.items():
            computed_values = computed_by_fqn.get(output_fqn, [])
            for i, (expected, computed) in enumerate(zip(expected_values, computed_values)):
                is_match = _values_match(expected, computed, float_rel_tolerance, float_abs_tolerance)
                status = Color.render("Match", Color.G) if is_match else Color.render("Mismatch", Color.R)
                tbl.add_row(output_fqn, str(i), str(expected), str(computed), status)

        print()
        console.print(tbl)

    if all_mismatches:
        fail_msg = (
            f"Static DataFrame resolver check failed: "
            f"{len(all_mismatches)} mismatch(es) across "
            f"{len(expected_columnar)} output feature(s)"
        )
        pytest.fail(fail_msg, pytrace=False)


__all__ = ["assert_frame_equal", "check_expression", "check_static_dataframe", "check_stream_parsing", "StreamMessage"]
