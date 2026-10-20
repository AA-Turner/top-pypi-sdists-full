"""Multi-column sort keys for the `by=` aggregations.

Public exports live on ``chalk.functions``. Import from there, not from this module.

``F.max_by``, ``F.min_by``, ``F.max_by_n`` and ``F.min_by_n`` take a single comparator. To order
by several columns, ``F.sort_order`` encodes them into one order-preserving value, so raw
byte comparison *is* the intended ordering -- direction and null placement are baked into the
bytes rather than applied by a comparator the aggregation would have to know about.

A single bare column never goes through this encoding: it stays a leaf and keeps its existing
lowering, representation and plan shape, which is what keeps materialized aggregations and
existing feature definitions untouched.
"""

from __future__ import annotations

from typing import Any

from chalk.features.underscore import Underscore, UnderscoreFunction

_SORT_DIRECTIONS = {"asc": "a", "desc": "d"}
_SORT_NULL_ORDERS = {"nulls_first": "f", "nulls_last": "l"}
_SORT_ORDER_FUNCTION = "sort_order"


def _encode_sort_key(key: Underscore | Any) -> "tuple[str, Underscore]":
    """Renders one key of a sort spec, returning its two spec characters and the column.

    A key is a bare column, `(column, direction)`, or `(column, direction, null_order)`. This is
    the convention `sort_by` and `order_by` already use, so the same shapes read the same way.
    """
    if not isinstance(key, (tuple, list)):
        return _SORT_DIRECTIONS["asc"] + _SORT_NULL_ORDERS["nulls_last"], key
    if len(key) not in (2, 3):
        raise ValueError(
            f"A sort key must be a column, `(column, direction)`, or `(column, direction, null_order)`, got {key!r}"
        )
    column, direction = key[0], key[1]
    null_order = key[2] if len(key) == 3 else "nulls_last"
    if direction not in _SORT_DIRECTIONS:
        raise ValueError(f"Sort direction must be one of {sorted(_SORT_DIRECTIONS)}, got {direction!r} in {key!r}")
    if null_order not in _SORT_NULL_ORDERS:
        raise ValueError(f"Null order must be one of {sorted(_SORT_NULL_ORDERS)}, got {null_order!r} in {key!r}")
    return _SORT_DIRECTIONS[direction] + _SORT_NULL_ORDERS[null_order], column


def sort_order(*keys: Underscore | Any):
    """
    Build a sort order over one or more columns, for use as the comparator of
    :func:`max_by`, :func:`min_by`, :func:`max_by_n` or :func:`min_by_n`.

    Each key is a column, `(column, direction)`, or `(column, direction, null_order)`, where
    direction is `"asc"` or `"desc"` and null_order is `"nulls_first"` or `"nulls_last"`.
    Direction defaults to `"asc"` and null order to `"nulls_last"`, which places nulls where they
    lose -- matching how a null sort key behaves without an explicit order.

    Parameters
    ----------
    keys
        The columns to order by, in precedence order. Earlier keys decide the ordering; later
        keys break ties.

    Examples
    --------
    >>> from chalk import DataFrame, _
    >>> from chalk.features import features, has_many
    >>> import chalk.functions as F
    >>> @features
    ... class Transaction:
    ...     id: int
    ...     amount: float
    ...     date: datetime
    ...     user_id: int
    >>> @features
    ... class User:
    ...     id: int
    ...     transactions: DataFrame[Transaction] = has_many(lambda: User.id == Transaction.user_id)
    ...     # The most recent transaction, breaking ties on the smaller amount.
    ...     latest_id: int = F.max_by(
    ...         _.transactions[_.id],
    ...         F.sort_order(_.date, (_.amount, "desc")),
    ...     )
    """
    if not keys:
        raise ValueError("`sort_order` requires at least one key")
    encoded = [_encode_sort_key(key) for key in keys]
    spec = ",".join(chars for chars, _column in encoded)
    columns = [column for _chars, column in encoded]
    names = [f"k{index}" for index in range(len(columns))]
    # The same node `F.struct_pack` builds, constructed here so this module needs no import back
    # into `chalk.functions`, whose own import of this one would then be circular.
    packed = UnderscoreFunction("struct_pack", names, *columns)
    return UnderscoreFunction(_SORT_ORDER_FUNCTION, spec, packed)


def _invert_null_order(spec: str) -> str:
    """Flips each key's null placement.

    `max_by` selects the *greatest* key, so a user asking for `nulls_last` -- nulls deprioritized
    -- needs nulls encoded first, where `max_by` will never reach them. `min_by` selects the least
    and needs no such flip. Keeping the flip here means the encoding stays a faithful
    "nulls sort first/last in ascending order" primitive, and only the aggregation that reverses
    the reading compensates for it.
    """
    flipped = {"f": "l", "l": "f"}
    return ",".join(token[0] + flipped[token[1]] for token in spec.split(","))


def normalize_sort(sort: Underscore | Any, *, selects_greatest: bool):
    """Turns a by-aggregation's `sort=` argument into the value the aggregation should receive.

    A bare column is passed through untouched, so single-column calls keep their exact plan shape.
    A tuple becomes a `sort_order`, and a `sort_order` -- however it was written -- has its null
    placement resolved against `selects_greatest`.

    Parameters
    ----------
    sort
        What the caller passed: a column, a tuple of keys, or a `sort_order`.
    selects_greatest
        Whether the aggregation takes the greatest key (`max_by`) rather than the least
        (`min_by`). Nulls are encoded to lose either way, which takes opposite placements.
    """
    # Resolving placement here, rather than in `sort_order`, is what lets a user build
    # `F.sort_order(...)` without knowing which aggregation will consume it.
    if (
        isinstance(sort, UnderscoreFunction)
        and sort._chalk__function_name == _SORT_ORDER_FUNCTION  # pyright: ignore[reportPrivateUsage]
    ):
        if not selects_greatest:
            return sort
        spec, packed = sort._chalk__args  # pyright: ignore[reportPrivateUsage]
        return UnderscoreFunction(_SORT_ORDER_FUNCTION, _invert_null_order(spec), packed)
    if isinstance(sort, (tuple, list)):
        return normalize_sort(sort_order(*sort), selects_greatest=selects_greatest)
    return sort
