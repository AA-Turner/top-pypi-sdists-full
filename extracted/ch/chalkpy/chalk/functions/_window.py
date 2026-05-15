"""Window (analytic) expressions.

Public exports live on ``chalk.functions``. Import from there, not from this module.

Most functions here take an expression as their first positional argument, which
means users can equivalently write the function form ``F.fn(expr, ...)`` or the
method form ``expr.fn(...)`` — chalkdf's conversion layer routes them to the
same node. The two snippets below are equivalent:

>>> import chalk.functions as F
>>> from chalk.features import _
>>> # Cumulative sum of v partitioned by idx, ordered by t
>>> F.over(_.v.sum(), partition_by="idx", order_by="t", frame=F.cumulative()).alias("rs")
>>> _.v.sum().over(partition_by="idx", order_by="t", frame=F.cumulative()).alias("rs")

Ranking functions that don't take an input expression (``F.rank``,
``F.row_number``, ``F.percent_rank``, ``F.cume_dist``, ``F.ntile``) only work in
the function form — there's no expression for them to attach to.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Sequence, Union

from chalk.features.underscore import Underscore, UnderscoreFunction

FrameBoundary = Literal[
    "unbounded_preceding",
    "preceding",
    "current_row",
    "following",
    "unbounded_following",
]

OrderDirection = Literal["asc", "desc"]
OrderItem = Union[str, Underscore, "tuple[Union[str, Underscore], OrderDirection]"]


@dataclass(frozen=True)
class Frame:
    """A window frame: how rows around the current row are included in the window.

    Construct via :func:`trailing`, :func:`cumulative`, :func:`whole_partition`,
    :func:`centered`, or :func:`rows_between` rather than instantiating directly.

    Note: libchalk currently only supports row-based frames (``ROWS BETWEEN``).
    Value-based frames (``RANGE BETWEEN``) are not yet supported.
    """

    start_type: FrameBoundary
    start_offset: int | None
    end_type: FrameBoundary
    end_offset: int | None


@dataclass(frozen=True)
class WindowSpec:
    """A reusable window specification: ``partition_by``, ``order_by``, and an optional default frame."""

    partition_by: tuple[Union[str, Underscore], ...]
    order_by: tuple[OrderItem, ...]
    default_frame: Frame | None = None


########################################################################################################################
# Frame helpers                                                                                                        #
########################################################################################################################


def trailing(n: int) -> Frame:
    """A trailing frame: the ``n`` rows before the current row, plus the current row.

    Equivalent to SQL ``ROWS BETWEEN n PRECEDING AND CURRENT ROW``.
    """
    if n < 0:
        raise ValueError(f"trailing(n) requires n >= 0, got {n}")
    return Frame("preceding", n, "current_row", 0)


def cumulative() -> Frame:
    """A cumulative frame: everything from the start of the partition through the current row.

    Equivalent to SQL ``ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW``.
    """
    return Frame("unbounded_preceding", None, "current_row", 0)


def whole_partition() -> Frame:
    """The entire partition. Equivalent to SQL ``ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING``."""
    return Frame("unbounded_preceding", None, "unbounded_following", None)


def centered(n: int) -> Frame:
    """A symmetric frame of ``n`` rows on either side of the current row.

    For example, ``centered(3)`` is ``ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING``.
    """
    if n < 0:
        raise ValueError(f"centered(n) requires n >= 0, got {n}")
    return Frame("preceding", n, "following", n)


def rows_between(start: int | None, end: int | None) -> Frame:
    """A row-based frame between two offsets relative to the current row.

    Negative integers are preceding offsets, positive integers are following offsets,
    and ``0`` is the current row. ``None`` means unbounded in that direction.
    """
    start_type, start_offset = _bound_from_int(start, unbounded_side="preceding")
    end_type, end_offset = _bound_from_int(end, unbounded_side="following")
    return Frame(start_type, start_offset, end_type, end_offset)


def _bound_from_int(
    v: int | None, *, unbounded_side: Literal["preceding", "following"]
) -> tuple[FrameBoundary, int | None]:
    if v is None:
        return ("unbounded_preceding" if unbounded_side == "preceding" else "unbounded_following", None)
    if v < 0:
        return ("preceding", -v)
    if v == 0:
        return ("current_row", 0)
    return ("following", v)


########################################################################################################################
# Reusable window spec                                                                                                 #
########################################################################################################################


def window(
    partition_by: Union[str, Underscore, Sequence[Union[str, Underscore]]],
    order_by: Union[OrderItem, Sequence[OrderItem], None] = None,
    frame: Frame | None = None,
) -> WindowSpec:
    """Build a reusable :class:`WindowSpec` to share across multiple window expressions.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _
    >>> w = F.window(partition_by="idx", order_by="t")
    >>> F.over(_.v.sum(), spec=w, frame=F.cumulative()).alias("rs")
    >>> F.over(_.v.shift(1), spec=w).alias("prev_v")
    """
    return WindowSpec(
        partition_by=_normalize_partition_by(partition_by),
        order_by=_normalize_order_by(order_by),
        default_frame=frame,
    )


def _normalize_partition_by(
    partition_by: Union[str, Underscore, Sequence[Union[str, Underscore]]],
) -> tuple[Union[str, Underscore], ...]:
    if isinstance(partition_by, (str, Underscore)):
        return (partition_by,)
    return tuple(partition_by)


def _normalize_order_by(
    order_by: Union[OrderItem, Sequence[OrderItem], None],
) -> tuple[OrderItem, ...]:
    if order_by is None:
        return ()
    if isinstance(order_by, (str, Underscore)):
        return (order_by,)
    if isinstance(order_by, tuple) and len(order_by) == 2 and isinstance(order_by[1], str):
        return (order_by,)  # type: ignore[return-value]
    return tuple(order_by)


########################################################################################################################
# over()                                                                                                               #
########################################################################################################################


def over(
    expr: Underscore | Any,
    *,
    partition_by: Union[str, Underscore, Sequence[Union[str, Underscore]], None] = None,
    order_by: Union[OrderItem, Sequence[OrderItem], None] = None,
    frame: Frame | None = None,
    spec: WindowSpec | None = None,
) -> Underscore:
    """Apply ``expr`` over a window partitioned by ``partition_by`` and ordered by ``order_by``.

    Parameters
    ----------
    expr
        The expression to apply over the window. Typically an aggregation
        (``_.v.sum()``, ``_.v.mean()``, ...), a :func:`shift`, or a ranking
        function such as :func:`row_number` or :func:`rank`.
    partition_by
        Partition columns. Mutually exclusive with ``spec``.
    order_by
        Ordering within each partition. Mutually exclusive with ``spec``.
        Required for cumulative aggregations and for ranking functions that
        weren't given a column argument.
    frame
        The frame to apply. If omitted and ``spec`` has a ``default_frame``, that is used.
    spec
        A :class:`WindowSpec` from :func:`window`. Mutually exclusive with
        ``partition_by`` / ``order_by``.

    Examples
    --------
    Both forms below are equivalent — pick whichever reads better:

    >>> import chalk.functions as F
    >>> from chalk.features import _
    >>> # Whole-partition sum, broadcast to each row
    >>> _.v.sum().over(partition_by="idx").alias("partition_sum")
    >>> F.over(_.v.sum(), partition_by="idx").alias("partition_sum")
    >>> # 7-row trailing mean
    >>> _.v.mean().over(partition_by="idx", order_by="t", frame=F.trailing(7)).alias("ma7")
    >>> # Cumulative running sum
    >>> _.v.sum().over(partition_by="idx", order_by="t", frame=F.cumulative()).alias("rs")
    >>> # Lag by 1 within partition
    >>> _.v.shift(1).over(partition_by="idx", order_by="t").alias("prev_v")
    >>> # Rank — column-arg form (Polars-style)
    >>> _.v.rank().over(partition_by="idx").alias("rk")
    >>> # Rank — SQL-form fallback (no column on rank; order_by drives the ranking)
    >>> F.over(F.rank(), partition_by="idx", order_by="v").alias("rk")
    """
    if spec is not None:
        if partition_by is not None or order_by is not None:
            raise ValueError("`over` accepts either `spec=` or `partition_by=`/`order_by=`, not both")
        partition_by_norm = spec.partition_by
        order_by_norm = spec.order_by
        frame_resolved = frame if frame is not None else spec.default_frame
    else:
        if partition_by is None:
            raise ValueError("`over` requires either `spec=` or `partition_by=`")
        partition_by_norm = _normalize_partition_by(partition_by)
        order_by_norm = _normalize_order_by(order_by)
        frame_resolved = frame
    return UnderscoreFunction("over", expr, partition_by_norm, order_by_norm, frame_resolved)


########################################################################################################################
# Window-only functions                                                                                                #
########################################################################################################################


RankMethod = Literal["standard", "dense", "ordinal"]

_RANK_METHOD_TO_FN: dict[str, str] = {
    "standard": "rank",
    "dense": "dense_rank",
    "ordinal": "row_number",
}


def row_number(
    column: Underscore | Any | None = None,
    *,
    descending: bool = False,
) -> Underscore:
    """The 1-based row number within the window's partition.

    Equivalent to ``F.rank(column, method="ordinal")`` and SQL ``ROW_NUMBER()``.
    Must be used inside :func:`over`.

    Parameters
    ----------
    column
        The column whose values determine the ordering. If ``None``, the
        ordering comes from :func:`over`'s ``order_by`` argument (SQL form).
        Method form ``_.t.row_number()`` is equivalent to
        ``F.row_number(_.t)``.
    descending
        Reverse the sort order. Only meaningful when ``column`` is provided.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _
    >>> # Polars-style: column on the function
    >>> _.t.row_number().over(partition_by="idx").alias("rn")
    >>> # SQL-style: ordering from over(order_by=)
    >>> F.over(F.row_number(), partition_by="idx", order_by="t").alias("rn")
    """
    if column is None:
        return UnderscoreFunction("row_number")
    return UnderscoreFunction("row_number", column, descending=descending)


def rank(
    column: Underscore | Any | None = None,
    *,
    method: RankMethod = "standard",
    descending: bool = False,
) -> Underscore:
    """Rank within a partition. Must be used inside :func:`over`.

    Parameters
    ----------
    column
        The column whose values to rank. If ``None``, the ordering comes from
        :func:`over`'s ``order_by`` argument (SQL form). Method form
        ``_.v.rank()`` is equivalent to ``F.rank(_.v)``.
    method
        How to assign ranks:

        - ``"standard"`` (default): tied values get the same rank, and the next rank
          jumps to ``rank + count_of_ties``. Equivalent to SQL ``RANK()``.
          Example: values ``[10, 20, 20, 30]`` → ranks ``[1, 2, 2, 4]``.
        - ``"dense"``: tied values get the same rank, and the next rank is
          ``rank + 1``. Equivalent to SQL ``DENSE_RANK()``.
          Example: values ``[10, 20, 20, 30]`` → ranks ``[1, 2, 2, 3]``.
        - ``"ordinal"``: every row gets a unique rank, with ties broken in
          arrival order. Equivalent to SQL ``ROW_NUMBER()``.
          Example: values ``[10, 20, 20, 30]`` → ranks ``[1, 2, 3, 4]``.
    descending
        Reverse the sort order. Only meaningful when ``column`` is provided.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _
    >>> # Polars-style: column on the function (method form works via dispatch)
    >>> _.v.rank().over(partition_by="idx").alias("rk")
    >>> _.v.rank(method="dense").over(partition_by="idx").alias("rk_dense")
    >>> _.v.rank(descending=True).over(partition_by="idx").alias("rk_desc")
    >>> # SQL-style: column comes from over(order_by=)
    >>> F.over(F.rank(), partition_by="idx", order_by="v").alias("rk")
    """
    if method not in _RANK_METHOD_TO_FN:
        raise ValueError(f"unsupported rank method '{method}'; expected one of {sorted(_RANK_METHOD_TO_FN)}")
    fn_name = _RANK_METHOD_TO_FN[method]
    if column is None:
        return UnderscoreFunction(fn_name)
    return UnderscoreFunction(fn_name, column, descending=descending)


def percent_rank(
    column: Underscore | Any | None = None,
    *,
    descending: bool = False,
) -> Underscore:
    """Relative rank within a partition, in ``[0, 1]``.

    Must be used inside :func:`over`. See :func:`rank` for the meaning of
    ``column`` and ``descending``.
    """
    if column is None:
        return UnderscoreFunction("percent_rank")
    return UnderscoreFunction("percent_rank", column, descending=descending)


def cume_dist(
    column: Underscore | Any | None = None,
    *,
    descending: bool = False,
) -> Underscore:
    """Cumulative distribution within a partition, in ``(0, 1]``.

    Must be used inside :func:`over`. See :func:`rank` for the meaning of
    ``column`` and ``descending``.
    """
    if column is None:
        return UnderscoreFunction("cume_dist")
    return UnderscoreFunction("cume_dist", column, descending=descending)


def ntile(
    column: Underscore | Any | None = None,
    n: int | None = None,
    *,
    descending: bool = False,
) -> Underscore:
    """Divide a partition into ``n`` buckets and return the bucket index for each row.

    Must be used inside :func:`over`.

    Parameters
    ----------
    column
        The column whose values determine the ordering. If ``None``, the
        ordering comes from :func:`over`'s ``order_by`` argument (SQL form).
        Method form ``_.v.ntile(4)`` is equivalent to ``F.ntile(_.v, 4)``.
    n
        Number of buckets. Required.
    descending
        Reverse the sort order. Only meaningful when ``column`` is provided.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _
    >>> # Polars-style
    >>> _.v.ntile(4).over(partition_by="idx").alias("quartile")
    >>> # SQL-style
    >>> F.over(F.ntile(n=4), partition_by="idx", order_by="v").alias("quartile")
    """
    if n is None:
        raise ValueError("ntile requires `n` (number of buckets)")
    if n <= 0:
        raise ValueError(f"ntile requires n > 0, got {n}")
    if column is None:
        return UnderscoreFunction("ntile", n=n)
    return UnderscoreFunction("ntile", column, n=n, descending=descending)


def shift(expr: Underscore | Any, offset: int) -> Underscore:
    """Shift ``expr`` by ``offset`` rows within the window's partition.

    Positive offsets look backwards (lag); negative offsets look forwards (lead).
    Must be used inside :func:`over` with an ``order_by``. Equivalently:
    ``_.v.shift(1)``.
    """
    return UnderscoreFunction("shift", expr, offset)


########################################################################################################################
# Cumulative aggregates                                                                                                #
########################################################################################################################


def cum_sum(expr: Underscore | Any) -> Underscore:
    """Cumulative sum of ``expr``. Sugar for ``F.over(expr.sum(), ..., frame=F.cumulative())``.

    Equivalently: ``_.v.cum_sum()``.
    """
    return UnderscoreFunction("cum_sum", expr)


def cum_mean(expr: Underscore | Any) -> Underscore:
    """Cumulative mean of ``expr``."""
    return UnderscoreFunction("cum_mean", expr)


def cum_min(expr: Underscore | Any) -> Underscore:
    """Cumulative min of ``expr``."""
    return UnderscoreFunction("cum_min", expr)


def cum_max(expr: Underscore | Any) -> Underscore:
    """Cumulative max of ``expr``."""
    return UnderscoreFunction("cum_max", expr)


def cum_count(expr: Underscore | Any) -> Underscore:
    """Cumulative count of non-null ``expr``."""
    return UnderscoreFunction("cum_count", expr)


def cum_prod(expr: Underscore | Any) -> Underscore:
    """Cumulative product of ``expr``."""
    return UnderscoreFunction("cum_prod", expr)
