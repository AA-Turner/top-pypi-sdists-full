#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto

from snowflake import snowpark
from snowflake.snowpark_connect.column_name_handler import (
    ColumnNameMap,
    JoinColumnNameMap,
)
from snowflake.snowpark_connect.config import (
    is_collect_list_window_order_by_direction_enabled,
    is_default_frame_last_includes_peers_enabled,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import (
    SparkException,
    attach_custom_error_code,
)
from snowflake.snowpark_connect.expression.literal import get_literal_field_and_name
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.typed_column import TypedColumn
from snowflake.snowpark_connect.utils.context import temporary_window_expression

# SQL functions that support ROWS BETWEEN but not RANGE BETWEEN.
ROWS_ONLY_FUNCTIONS = frozenset(
    ["first", "first_value", "last", "last_value", "nth_value", "rank", "dense_rank"]
)

SPARK_RANKING_FUNCTIONS = frozenset(
    [
        "row_number",
        "rank",
        "dense_rank",
        "percent_rank",
        "ntile",
        "lag",
        "lead",
    ]
)

RANGE_BASED_WINDOW_FRAME_ONLY_SNOWFLAKE_FUNCTIONS = frozenset(["percent_rank"])

CAPITAL_FUNCTION_NAMES = frozenset(["rank()", "dense_rank()", "percent_rank()"])

# Spark window aggregates whose *result order* depends on the window ORDER BY and
# that map to a Snowflake function supporting the WITHIN GROUP form. For the
# whole-partition frame Snowflake drops the OVER ORDER BY direction, so we rewrite
# these to ARRAY_AGG(x) WITHIN GROUP (ORDER BY ...) OVER (PARTITION BY ...), which
# honors it (see _array_agg_within_group_over and SNOW-3680715).
#
# Keep this gate narrow. WITHIN GROUP is rejected by most window functions
# (SUM/AVG/COUNT/MIN/MAX, ranking, first/last/nth_value), so applying the rewrite
# unconditionally would emit invalid SQL. It is also unnecessary for
# order-insensitive aggregates (their whole-partition result is already correct)
# and for PERCENTILE_* (supports WITHIN GROUP, but its result does not depend on
# ORDER BY direction). collect_set is intentionally excluded: Spark leaves set
# order unspecified and Snowflake's ARRAY_UNIQUE_AGG rejects WITHIN GROUP.
ORDER_SENSITIVE_ARRAY_AGG_FUNCTIONS = frozenset(["collect_list", "array_agg"])


def _gate_running_first_ignore_nulls(
    exp: expressions_proto.Expression,
    proto_func_name: str,
    window_func: TypedColumn,
    partitions: list[snowpark.Column],
    orders: list[snowpark.Column],
    frame: snowpark.window.WindowSpec,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
    *,
    has_order_spec: bool,
    lower: int,
    upper: int,
) -> snowpark.Column | None:
    """Match Spark first(ignorenulls) when the frame starts at the partition.

    Snowflake's ``FIRST_VALUE(x) IGNORE NULLS`` over a frame that begins at
    unbounded preceding still returns the first non-null of the whole partition,
    so rows before that value are not null. Spark's ``First`` aggregate only
    sees rows the frame feeds it. The first non-null in any prefix of the
    partition is null until that value is inside the frame, and is then the
    partition's first non-null. ``COUNT(x)`` over the Spark frame is that
    test. ``FIRST_VALUE(x) IGNORE NULLS`` over the whole partition is the
    value, which Snowflake does honor.

    With no explicit frame, ``first`` is planned as ROWS
    (``ROWS_ONLY_FUNCTIONS``), but Spark's frame is RANGE, so peers count,
    including a null key; the count for that case uses RANGE. Explicit ROWS
    and RANGE frames are counted on that frame.

    The argument is evaluated twice, once in ``COUNT`` and once in
    ``FIRST_VALUE``. A nondeterministic argument such as
    ``when(rand() > 0.5, x)`` gets an independent draw in each, so the gate
    and the value can disagree, and an expensive UDF in the argument runs
    twice per row.

    A frame that does not start at unbounded preceding is a different shape
    and is left unchanged. Returns None when this rewrite does not apply.
    """
    if proto_func_name not in ("first", "first_value"):
        return None
    if not has_order_spec or not orders:
        return None
    if lower != snowpark.Window.UNBOUNDED_PRECEDING:
        return None
    if upper == snowpark.Window.UNBOUNDED_FOLLOWING:
        return None
    from snowflake.snowpark_connect.config import (
        is_first_ignore_nulls_respects_frame_enabled,
    )

    if not is_first_ignore_nulls_respects_frame_enabled():
        return None
    arguments = exp.window.window_function.unresolved_function.arguments
    if len(arguments) < 2 or not _literal_bool(arguments[1]):
        return None
    function = getattr(window_func.col, "_expression", None)
    if getattr(function, "expr", None) is None or not getattr(
        function, "ignore_nulls", False
    ):
        return None

    from snowflake.snowpark.functions import count, first_value, when
    from snowflake.snowpark_connect.expression.map_expression import (
        map_single_column_expression,
    )

    # window_func already wraps the argument in FIRST_VALUE over the original
    # frame, so the bare argument is mapped again from the proto. COUNT and the
    # new FIRST_VALUE share that one mapping, as both windows share the
    # partitions and orders: Snowpark renders a shared node in each window.
    argument = map_single_column_expression(arguments[0], column_mapping, typer)[1].col
    # Unspecified ordered frame: Spark RANGE peers, not the ROWS prefix that
    # first is planned as. Explicit ROWS and RANGE frames keep `frame`.
    if (
        exp.window.frame_spec.frame_type
        == expressions_proto.Expression.Window.WindowFrame.FrameType.FRAME_TYPE_UNDEFINED
    ):
        if partitions:
            count_window = snowpark.Window.partition_by(partitions).order_by(orders)
        else:
            count_window = snowpark.Window.order_by(orders)
        count_window = count_window.range_between(
            snowpark.Window.UNBOUNDED_PRECEDING,
            snowpark.Window.CURRENT_ROW,
        )
    else:
        count_window = frame
    seen = count(argument).over(count_window)
    if partitions:
        whole = snowpark.Window.partition_by(partitions).order_by(orders)
    else:
        whole = snowpark.Window.order_by(orders)
    whole = whole.rows_between(
        snowpark.Window.UNBOUNDED_PRECEDING,
        snowpark.Window.UNBOUNDED_FOLLOWING,
    )
    return when(seen > 0, first_value(argument, True).over(whole))


def try_eval_foldable_boundary_int(
    boundary_exp: expressions_proto.Expression,
) -> int | None:
    """Fold a window frame boundary expression into an integer when possible.

    Args:
        boundary_exp: Spark Connect expression proto for a frame boundary value.

    Returns:
        An ``int`` when the expression can be folded locally from supported
        integral forms, otherwise ``None`` so callers can use the fallback path.

    Supported forms are integral literals, unary ``positive``/``negative`` (and
    ``unary_minus``), and binary ``+``, ``-``, ``*``, and ``/``. Division is
    folded only when it is exact and denominator is non-zero. ``//`` is
    intentionally unsupported because Connect arithmetic expressions use ``/``.
    """
    expr_type = boundary_exp.WhichOneof("expr_type")
    if expr_type == "literal":
        literal_type = boundary_exp.literal.WhichOneof("literal_type")
        if literal_type not in ("byte", "short", "integer", "long"):
            return None
        literal, _ = get_literal_field_and_name(boundary_exp.literal)
        return int(literal)

    if expr_type != "unresolved_function":
        return None

    unresolved_function = boundary_exp.unresolved_function
    function_name = unresolved_function.function_name.lower()
    arguments = unresolved_function.arguments

    if function_name in ("unary_minus", "negative"):
        if len(arguments) != 1:
            return None
        value = try_eval_foldable_boundary_int(arguments[0])
        return None if value is None else -value

    if function_name == "positive":
        if len(arguments) != 1:
            return None
        return try_eval_foldable_boundary_int(arguments[0])

    if function_name in ("+", "-", "*", "/"):
        if len(arguments) != 2:
            return None
        left = try_eval_foldable_boundary_int(arguments[0])
        right = try_eval_foldable_boundary_int(arguments[1])
        if left is None or right is None:
            return None
        if function_name == "+":
            return left + right
        if function_name == "-":
            return left - right
        if function_name == "*":
            return left * right
        if right == 0:
            return None
        if left % right != 0:
            return None
        return left // right

    return None


def _array_agg_within_group_over(
    window_func: TypedColumn,
    orders: list[snowpark.Column],
    partitions: list[snowpark.Column],
) -> snowpark.Column:
    """Build ARRAY_AGG(x) WITHIN GROUP (ORDER BY ...) OVER (PARTITION BY ...).

    Used only for the whole-partition frame, where ARRAY_AGG(x) OVER (... ORDER BY
    ...) ignores the ORDER BY direction but the WITHIN GROUP form honors it.
    ``window_func.col`` is the raw ARRAY_AGG (its ArrayType cast is deferred by
    TypedColumnWithDeferredCast), so re-apply the cast here. ``partitions`` may be
    empty, in which case ``over(None)`` emits ``OVER ()``.
    """
    partition_window = snowpark.Window.partition_by(partitions) if partitions else None
    return (
        window_func.col.within_group(*orders)
        .over(partition_window)
        .cast(window_func.typ)
    )


def _literal_bool(argument: expressions_proto.Expression) -> bool:
    """True only for a boolean literal true (Spark requires a boolean here)."""
    return (
        argument.HasField("literal")
        and argument.literal.HasField("boolean")
        and argument.literal.boolean
    )


def _range_frame_key(order_key: TypedColumn) -> snowpark.Column | None:
    """The key as a type that Snowflake accepts for RANGE CURRENT ROW, if any.

    That frame needs a numeric or date ORDER BY (010054). A timestamp only
    takes interval bounds (010057), so it is ordered by its epoch nanoseconds,
    which are equal exactly when the timestamps are. A float key is folded by
    ``_peer_key``, because the frame tells -0.0 from 0.0.
    """
    from snowflake.snowpark.functions import date_part
    from snowflake.snowpark.types import (
        DateType,
        DoubleType,
        FloatType,
        TimestampType,
        _NumericType,
    )

    data_type = order_key.typ
    if isinstance(data_type, (FloatType, DoubleType)):
        return _peer_key(order_key)
    if isinstance(data_type, (_NumericType, DateType)):
        return order_key.col
    if isinstance(data_type, TimestampType):
        return date_part("epoch_nanosecond", order_key.col)
    return None


def _peer_key(order_key: TypedColumn) -> snowpark.Column:
    """An ORDER BY key as the peer window reads it (range key or PARTITION BY).

    Spark treats -0.0 and 0.0 as peers; adding 0.0 turns -0.0 into 0.0.
    """
    from snowflake.snowpark.functions import lit
    from snowflake.snowpark.types import DoubleType, FloatType

    if isinstance(order_key.typ, (FloatType, DoubleType)):
        return order_key.col + lit(0.0)
    return order_key.col


def _last_including_peers(
    window_func: TypedColumn,
    partitions: list[snowpark.Column],
    orders: list[snowpark.Column],
    order_keys: list[TypedColumn],
    typer: ExpressionTyper | None,
    column_mapping: ColumnNameMap,
    *,
    ignore_nulls: bool,
) -> snowpark.Column:
    """``last()`` over RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.

    Snowflake rejects that cumulative RANGE frame for LAST_VALUE (002303), but
    the frame ends at the current row's last peer, so ``last()`` over it is
    LAST_VALUE over the peer group alone. Every peer gets the same value, and
    it is one of the peers' values. Neither Spark nor Snowflake defines which
    tied row that is.

    The peer group is RANGE BETWEEN CURRENT ROW AND CURRENT ROW on one key,
    with the other keys in PARTITION BY. When no key has a type that frame
    accepts, every key goes into PARTITION BY and the frame is the whole
    partition.
    """
    range_keys = [_range_frame_key(key) for key in order_keys]
    index = next((i for i, key in enumerate(range_keys) if key is not None), None)
    if index is None:
        peer_window = (
            snowpark.Window.partition_by([*partitions, *map(_peer_key, order_keys)])
            .order_by(orders[0])
            .rows_between(
                snowpark.Window.UNBOUNDED_PRECEDING,
                snowpark.Window.UNBOUNDED_FOLLOWING,
            )
        )
    else:
        other_keys = [_peer_key(k) for i, k in enumerate(order_keys) if i != index]
        peer_window = (
            snowpark.Window.partition_by([*partitions, *other_keys])
            .order_by(range_keys[index])
            .range_between(snowpark.Window.CURRENT_ROW, snowpark.Window.CURRENT_ROW)
        )
    last = window_func.over(peer_window)
    if not ignore_nulls:
        return last
    # An all-null peer group carries the value of the nearest earlier group that
    # has one. A second window over the source rows breaks that group's ties in
    # its own order, so the fill reads the peer value itself, from a select
    # under the projection. Without that select (e.g. a window in an aggregate)
    # the carried value is still a peer's, but not always the one its group shows.
    from snowflake.snowpark.functions import coalesce, last_value
    from snowflake.snowpark_connect.utils.expression_transformer import (
        is_child_agg_function_expression,
    )

    rows_before = _rows_before_peers(partitions, orders)
    # A window over an aggregate cannot be computed in a select under a global
    # aggregate projection (000979), so it keeps the second window.
    # LAST_VALUE keeps its argument in ``expr``, not in ``children``.
    func = window_func.col._expression
    over_aggregate = any(
        is_child_agg_function_expression(e)
        for e in (
            getattr(func, "expr", func),
            *(c._expression for c in (*partitions, *orders)),
        )
    )
    # The select under the projection sees only the input columns. A lateral
    # alias from the same projection (Spark rejects it in a window, SCOS lets
    # Snowflake resolve it) is not one of them, so it keeps the second window.
    # A window that reads no column at all, such as last(lit("x"), true) over
    # orderBy(lit(1)) next to count(*), may sit in a global aggregate, where an
    # outer reference to the lifted column is not grouped (000979).
    peer_value = (
        typer.lift_window_input(last)
        if typer is not None
        and typer.lifts_window_inputs
        and not over_aggregate
        and _reads_only_input_columns(
            (window_func.col, *partitions, *orders), column_mapping
        )
        else None
    )
    if peer_value is None:
        return coalesce(last, window_func.over(rows_before))
    return coalesce(peer_value, last_value(peer_value, True).over(rows_before))


def _reads_only_input_columns(
    columns: tuple[snowpark.Column, ...], column_mapping: ColumnNameMap
) -> bool:
    """True when these expressions read at least one column, all in ``column_mapping``."""
    from snowflake.snowpark._internal.analyzer.analyzer_utils import quote_name

    if isinstance(column_mapping, JoinColumnNameMap):
        return False
    available = {
        quote_name(name)
        for name in column_mapping.get_snowpark_columns(with_hidden=True)
    }
    read: set[str] = set()
    for column in columns:
        names = column._expression.dependent_column_names()
        if names is None:
            return False
        read |= names
    return bool(read) and read <= available


def _rows_before_peers(
    partitions: list[snowpark.Column], orders: list[snowpark.Column]
) -> snowpark.WindowSpec:
    """ROWS frame ending at 1 PRECEDING.

    Only used when the current peer group is all null, so the earlier rows of
    that group add nothing and the frame reaches back to earlier keys.
    """
    spec = snowpark.Window.partition_by(partitions) if partitions else snowpark.Window
    return spec.order_by(*orders).rows_between(snowpark.Window.UNBOUNDED_PRECEDING, -1)


def map_window_function(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[str, TypedColumn]:
    from snowflake.snowpark_connect.expression.map_expression import (
        map_single_column_expression,
    )

    with temporary_window_expression():

        def parse_frame_boundary(
            boundary: expressions_proto.Expression.Window.WindowFrame.FrameBoundary,
            is_upper: bool,
        ) -> tuple[str, int]:
            if boundary.HasField("current_row"):
                return "CURRENT ROW", snowpark.Window.CURRENT_ROW
            elif boundary.HasField("unbounded"):
                if is_upper:
                    return "UNBOUNDED FOLLOWING", snowpark.Window.UNBOUNDED_FOLLOWING
                else:
                    return "UNBOUNDED PRECEDING", snowpark.Window.UNBOUNDED_PRECEDING
            elif boundary.HasField("value"):
                # Preserve legacy behavior for literal boundaries and only fold
                # non-literal expressions incrementally.
                if boundary.value.HasField("literal"):
                    literal, _ = get_literal_field_and_name(boundary.value.literal)
                else:
                    # try to eval the boundary first, fallback to send snowflake query if failed.
                    literal = try_eval_foldable_boundary_int(boundary.value)
                if not boundary.value.HasField("literal") and literal is None:
                    expr_proto = boundary.value
                    session = snowpark.Session.get_active_session()
                    m = ColumnNameMap([], [], None)
                    expr = map_single_column_expression(
                        expr_proto, m, ExpressionTyper.dummy_typer(session)
                    )
                    literal = session.range(1).select(expr[1].col).collect()[0][0]

                return f"{literal} FOLLOWING", literal

        function_name, window_func = map_single_column_expression(
            exp.window.window_function, column_mapping, typer
        )
        partitions = []
        partition_col_names = []
        for p in exp.window.partition_spec:
            partition_col_name, typed_col = map_single_column_expression(
                p, column_mapping, typer
            )
            map_single_column_expression(p, column_mapping, typer)[1].col
            partition_col_names.append(partition_col_name)
            partitions.append(typed_col.col)

        orders = []
        order_keys = []
        order_col_names = []
        for order in exp.window.order_spec:
            order_col_name, order_typed = map_single_column_expression(
                order.child, column_mapping, typer
            )
            order_exp = order_typed.col
            order_keys.append(order_typed)

            order_col_name_parts = [order_col_name]
            match order.direction:
                case expressions_proto.Expression.SortOrder.SortDirection.SORT_DIRECTION_ASCENDING:
                    order_col_name_parts.append("ASC")
                    match order.null_ordering:
                        case expressions_proto.Expression.SortOrder.NullOrdering.SORT_NULLS_FIRST:
                            order_col_name_parts.append("NULLS FIRST")
                            orders.append(order_exp.asc_nulls_first())
                        case expressions_proto.Expression.SortOrder.NullOrdering.SORT_NULLS_LAST:
                            order_col_name_parts.append("NULLS LAST")
                            orders.append(order_exp.asc_nulls_last())
                        case _:
                            orders.append(order_exp.asc())
                case expressions_proto.Expression.SortOrder.SortDirection.SORT_DIRECTION_DESCENDING:
                    order_col_name_parts.append("DESC")
                    match order.null_ordering:
                        case expressions_proto.Expression.SortOrder.NullOrdering.SORT_NULLS_FIRST:
                            order_col_name_parts.append("NULLS FIRST")
                            orders.append(order_exp.desc_nulls_first())
                        case expressions_proto.Expression.SortOrder.NullOrdering.SORT_NULLS_LAST:
                            order_col_name_parts.append("NULLS LAST")
                            orders.append(order_exp.desc_nulls_last())
                        case _:
                            orders.append(order_exp.desc())
                case _:
                    # When order direction is not specified, nulls first/last is ignored, because
                    # there is no order_exp.nulls_first() / order_exp.nulls_last()
                    orders.append(order_exp)

            order_col_names.append(" ".join(order_col_name_parts))

        frame_name = []
        default_frame = False
        explicit_cumulative_range = False
        proto_func_name = (
            exp.window.window_function.unresolved_function.function_name.lower()
        )
        match exp.window.frame_spec.frame_type:
            case expressions_proto.Expression.Window.WindowFrame.FrameType.FRAME_TYPE_ROW:
                frame_name.append("ROWS BETWEEN")
                frame_type_func_string = "rows_between"
                if proto_func_name in RANGE_BASED_WINDOW_FRAME_ONLY_SNOWFLAKE_FUNCTIONS:
                    # Seems like Snowflake and Spark have different understanding of some functions. For those,
                    # Spark only allows rows_between while Snowflake only allows range_between. To be compatible
                    # with Spark, we have to use range_between here.
                    frame_type_func_string = "range_between"
                lower_name, lower = parse_frame_boundary(
                    exp.window.frame_spec.lower, is_upper=False
                )
                upper_name, upper = parse_frame_boundary(
                    exp.window.frame_spec.upper, is_upper=True
                )
                if proto_func_name in SPARK_RANKING_FUNCTIONS and (
                    lower != snowpark.Window.UNBOUNDED_PRECEDING
                    or upper != snowpark.Window.CURRENT_ROW
                ):
                    exception = SparkException.invalid_ranking_function_window_frame(
                        window_frame=f"specifiedwindowframe(RowFrame, {lower_name}, {upper_name})"
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception

                is_unbounded = (
                    lower == snowpark.Window.UNBOUNDED_PRECEDING
                    and upper == snowpark.Window.UNBOUNDED_FOLLOWING
                )
                if not orders and is_unbounded:
                    orders = [column_mapping.get_snowpark_columns()[0]]
                frame_name.append(f"{lower_name} AND {upper_name}")
            case expressions_proto.Expression.Window.WindowFrame.FrameType.FRAME_TYPE_RANGE:
                frame_name.append("RANGE BETWEEN")
                frame_type_func_string = "range_between"

                lower_name, lower = parse_frame_boundary(
                    exp.window.frame_spec.lower, is_upper=False
                )
                upper_name, upper = parse_frame_boundary(
                    exp.window.frame_spec.upper, is_upper=True
                )
                explicit_cumulative_range = (
                    lower == snowpark.Window.UNBOUNDED_PRECEDING
                    and upper == snowpark.Window.CURRENT_ROW
                )
                if lower == upper == snowpark.Window.CURRENT_ROW and orders:
                    # only one order is allowed when the frame is between current row and current row. and spark seems
                    # to ignore the non-first order.
                    orders = orders[:1]

                if proto_func_name in SPARK_RANKING_FUNCTIONS:
                    exception = SparkException.invalid_ranking_function_window_frame(
                        window_frame=f"specifiedwindowframe(RangeFrame, {lower_name}, {upper_name})"
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception

                is_unbounded = (
                    lower == snowpark.Window.UNBOUNDED_PRECEDING
                    and upper == snowpark.Window.UNBOUNDED_FOLLOWING
                )
                if not orders and is_unbounded:
                    orders = [column_mapping.get_snowpark_columns()[0]]
                frame_name.append(f"{lower_name} AND {upper_name}")
            case _:
                """
                Spark behavior:

                Default frame specification depends on other aspects of a given window defintion:

                if the ORDER BY clause is specified and the function accepts the frame specification, then the frame specification is defined by RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW,
                otherwise the frame specification is defined by ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING.

                RANKING window functions do not accept FRAMING.
                """
                default_frame = True
                frame_type_func_string = "rows_between"
                frame_type_string = "ROWS"
                if orders:
                    # Work around functions that support ROWS BETWEEN but not RANGE BETWEEN.
                    # ROWS matches RANGE only when no two rows tie on the ORDER BY
                    # keys: RANGE CURRENT ROW also covers the current row's peers.
                    lower_name, lower = (
                        "UNBOUNDED PRECEDING",
                        snowpark.Window.UNBOUNDED_PRECEDING,
                    )
                    upper_name, upper = "CURRENT ROW", snowpark.Window.CURRENT_ROW
                    match proto_func_name:
                        case "nth_value":
                            frame_type_string = "RANGE"
                        case "last" | "last_value" if (
                            is_default_frame_last_includes_peers_enabled()
                        ):
                            # Logical frame is RANGE. LAST_VALUE cannot emit it
                            # (002303); _last_including_peers builds the value.
                            frame_type_string = "RANGE"
                        case "lag" | "lead":
                            frame_type_func_string = "range_between"
                            func_args = (
                                exp.window.window_function.unresolved_function.arguments
                            )
                            sign = -1 if proto_func_name == "lag" else 1
                            offset = (
                                func_args[1].literal.integer
                                if len(func_args) > 1
                                else 1
                            )
                            lower_name = upper_name = f"{sign * offset} FOLLOWING"
                        case _ if proto_func_name not in ROWS_ONLY_FUNCTIONS:
                            frame_type_func_string = "range_between"
                            frame_type_string = (
                                "RANGE"
                                if proto_func_name not in SPARK_RANKING_FUNCTIONS
                                else frame_type_string
                            )
                else:
                    orders = [column_mapping.get_snowpark_columns()[0]]
                    lower_name, lower = (
                        "UNBOUNDED PRECEDING",
                        snowpark.Window.UNBOUNDED_PRECEDING,
                    )
                    upper_name, upper = (
                        "UNBOUNDED FOLLOWING",
                        snowpark.Window.UNBOUNDED_FOLLOWING,
                    )
                frame_name.append(
                    f"{frame_type_string} BETWEEN {lower_name} AND {upper_name}"
                )

        has_order_spec = len(exp.window.order_spec) > 0
        is_whole_partition_frame = (
            lower == snowpark.Window.UNBOUNDED_PRECEDING
            and upper == snowpark.Window.UNBOUNDED_FOLLOWING
        )

        # build window
        window = snowpark.Window
        if len(partitions) > 0:
            window = window.partitionBy(partitions)
        if len(orders) > 0:
            window = window.orderBy(orders)
        window = getattr(window, frame_type_func_string)(lower, upper)

        if function_name in CAPITAL_FUNCTION_NAMES:
            # weird spark behavior
            function_name = function_name.upper()

        window_parts = []
        if partition_col_names:
            window_parts.append(f"PARTITION BY {', '.join(partition_col_names)}")
        if order_col_names:
            window_parts.append(f"ORDER BY {', '.join(order_col_names)}")
        window_parts.extend(frame_name)
        spark_col_name = f"{function_name} OVER ({' '.join(window_parts)})"

        # SNOW-3680715: for the whole-partition frame, ARRAY_AGG(x) OVER (... ORDER
        # BY ...) ignores the ORDER BY direction (returns table scan order) while
        # Spark's collect_list preserves it. The WITHIN GROUP form honors it.
        # Other frames already match Spark and cannot use WITHIN GROUP (it cannot
        # carry a frame, nor coexist with an OVER ORDER BY). Gated by a BCR revert
        # flag (default on); set it false to restore the pre-BCR emission.
        if (
            proto_func_name in ORDER_SENSITIVE_ARRAY_AGG_FUNCTIONS
            and has_order_spec
            and is_whole_partition_frame
            and is_collect_list_window_order_by_direction_enabled()
        ):
            result_exp = _array_agg_within_group_over(window_func, orders, partitions)
        elif (
            proto_func_name in ("last", "last_value")
            and has_order_spec
            and (explicit_cumulative_range or default_frame)
            and is_default_frame_last_includes_peers_enabled()
        ):
            func_args = exp.window.window_function.unresolved_function.arguments
            result_exp = _last_including_peers(
                window_func,
                partitions,
                orders,
                order_keys,
                typer,
                column_mapping,
                ignore_nulls=len(func_args) > 1 and _literal_bool(func_args[1]),
            )
        else:
            result_exp = window_func.over(window)

        gated_first = _gate_running_first_ignore_nulls(
            exp,
            proto_func_name,
            window_func,
            partitions,
            orders,
            window,
            column_mapping,
            typer,
            has_order_spec=has_order_spec,
            lower=lower,
            upper=upper,
        )
        if gated_first is not None:
            result_exp = gated_first

        return spark_col_name, TypedColumn(result_exp, lambda: window_func.field_types)
