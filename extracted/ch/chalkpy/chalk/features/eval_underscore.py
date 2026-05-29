"""Evaluate an `Underscore` expression against an input `chalkdf.DataFrame`.

This helper translates feature-aware `Underscore` expressions into the
column-level operations supported by `chalkdf`. The shape/feature semantics
are resolved here; the actual computation is delegated to `chalkdf`.

# Naming convention for feature columns

Within any `struct[...]` column that holds the features of a namespace `ns`,
the subfields are named `"<ns>.<feature>"` — using the *immediate* namespace
name, not a path from the root. Nested `has_one` and the inner struct of
`has_many` follow the same rule recursively.

For example, with a `user` namespace that has a `has_one` `account` (of
namespace `account`) and a `has_many` `transactions` (of namespace
`transaction`):

```
user.account: struct[
    account.balance: float64,
    account.bank:    struct[bank.name: string],   # nested has_one
]

user.transactions: large_list[struct[
    transaction.amount:   float64,
    transaction.merchant: struct[
        merchant.name:     string,
        merchant.category: struct[category.name: string],
    ],
    transaction.tags: large_list[struct[tag.name: string]],
]]
```

# Input DataFrame shape

The caller-supplied input is itself a `_NamespaceRef` (see below) — a
`chalkdf.DataFrame` with exactly two columns:

```
__index__0   : int64           # uniquely identifies each input row
__features__ : struct[
                   user.id            : int64,
                   user.amount        : float64,
                   user.account       : struct[...],         # has_one
                   user.transactions  : large_list[struct[...]],  # has_many
                   __now__            : timestamp,           # optional special fields
                   ...
               ]
```

The caller is responsible for packing their data into this shape (e.g. via
`with_unique_id` plus a `struct_pack`). Special pseudo-features such as
`chalk_now` and `chalk_window` live as subfields of `__features__` with
`__dunder__` names so they cannot collide with user features.

# Intermediate DataFrame format

Every intermediate value produced during evaluation is a materialized
`chalkdf.DataFrame`. There are exactly two kinds of intermediate values,
distinguished by their value-column name so they cannot be accidentally
mixed up.

## `_NamespaceRef` — a position in the namespace hierarchy

Used for `_` itself, `_.has_one_feature`, and the inside of
`_.has_many[...]`. The df schema is:

```
__index__0, __index__1, ..., __index__N, __features__
```

`__features__` always has dtype `struct[<namespace_name>.<feature>: ...]`.
Feature lookup is always `get_struct_subfield(__features__,
f"{namespace_name}.{feature}")` — the subfield prefix is just the
`_NamespaceRef`'s `namespace_name`, so there is no separate "inner prefix"
field to track.

## `_Scalar` — a scalar value

Used for any expression that resolves to a value. The df schema is:

```
__index__0, __index__1, ..., __index__N, __value__
```

`__value__` can be any dtype (including struct or list, for things like
`array_agg`). Importantly, a `_Scalar`'s value column is named `__value__`
(not `__features__`), so the two kinds are never confused.

## Index columns

`__index__0` is supplied by the caller. Each `has_many` traversal adds one
more `__index__N`. `has_one` traversal does not add an index column
(one-to-one). When values from different levels are combined (e.g.
`__.x + _.y` inside a has_many, or `_.x + _.items[_.y].sum()` at the root),
the helper joins them on the shared prefix of their index columns.

# Worked examples

Assume the input shape above with namespaces `user`, `account`,
`transaction`, `merchant`, `category`, `tag` related as described.

| Expression                                              | df columns                                       | index_cols                    | kind                                                |
|---------------------------------------------------------|--------------------------------------------------|-------------------------------|-----------------------------------------------------|
| `_` (the root)                                          | `__index__0, __features__(struct)`               | `(__index__0,)`               | `_NamespaceRef` (namespace_name=`"user"`)           |
| `_.amount`                                              | `__index__0, __value__`                          | `(__index__0,)`               | `_Scalar`                                           |
| `_.account`                                             | `__index__0, __features__(struct)`               | `(__index__0,)`               | `_NamespaceRef` (namespace_name=`"account"`)        |
| `_.account.balance`                                     | `__index__0, __value__`                          | `(__index__0,)`               | `_Scalar`                                           |
| `_.account.bank`                                        | `__index__0, __features__(struct)`               | `(__index__0,)`               | `_NamespaceRef` (namespace_name=`"bank"`)           |
| `_.transactions`                                        | `__index__0, __index__1, __features__(struct)`   | `(__index__0, __index__1)`    | `_NamespaceRef` (namespace_name=`"transaction"`)    |
| `_.transactions[_.amount]`                              | `__index__0, __index__1, __value__`              | `(__index__0, __index__1)`    | `_Scalar`                                           |
| `_.transactions[_.amount].sum()`                        | `__index__0, __value__`                          | `(__index__0,)`               | `_Scalar`                                           |
| `_.transactions[_.tags[_.name == "x"].count()].sum()`   | `__index__0, __value__`                          | `(__index__0,)`               | `_Scalar`                                           |
| `_.chalk_now`                                           | `__index__0, __value__`                          | `(__index__0,)`               | `_Scalar` (reads `__now__` subfield of root)        |

# Transitions between kinds

- `_NamespaceRef` → `_Scalar` (scalar feature lookup): project a new df with
  the same `__index__*` cols and `__value__ = get_struct_subfield(
  __features__, "<ns>.<feature>")`.
- `_NamespaceRef` → `_NamespaceRef` (`has_one` drill-in): project a new df
  with `__features__ = get_struct_subfield(__features__,
  "<ns>.<feature>")`; `namespace_name` updates to the foreign namespace.
- `_NamespaceRef` → `_NamespaceRef` (`has_many` entry via `[...]`): explode
  the list column, add a fresh `__index__N` via `with_unique_id`, and project
  to `[*index_cols, __features__=exploded_struct]`.
- `_Scalar` aggregate → `_Scalar` at parent level: group by the parent's
  `index_cols` (dropping the deepest `__index__N`), apply the aggregate to
  `__value__`, and project the result.
- Combining scalars across levels in a scalar function: `_join_scalars` joins
  each operand's df on the shared prefix of `index_cols`, renames each
  `__value__` to a unique column, and projects the function call as the new
  `__value__`.
"""

# This file accesses many private fields of the `Underscore` classes.
# pyright: reportPrivateUsage=false
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Literal, Optional, Protocol, Union, cast

import pyarrow as pa

if TYPE_CHECKING:
    from chalkdf import DataFrame  # pyright: ignore[reportMissingTypeStubs, reportMissingImports]
else:
    import importlib.util

    CHALKDF_AVAILABLE = importlib.util.find_spec("chalkdf") is not None
    if CHALKDF_AVAILABLE:
        from chalkdf import DataFrame
    else:
        DataFrame = None

from chalk.features.underscore import (
    DoubleUnderscore,
    Underscore,
    UnderscoreAttr,
    UnderscoreCall,
    UnderscoreCast,
    UnderscoreFunction,
    UnderscoreItem,
    UnderscoreRoot,
)
from chalk.utils.duration import parse_chalk_duration_s

__all__ = (
    "eval_underscore",
    "eval_underscore_values",
    "normalize_input",
    "FeatureKind",
    "FeatureKindScalar",
    "FeatureKindHasOne",
    "FeatureKindHasMany",
    "FeatureKindWindowed",
    "FeatureKindWindowedPseudoFeature",
    "InputContext",
    "GlobalRegistryContext",
    "VALUE_COL_NAME",
    "FEATURES_COL_NAME",
    "INDEX_COL_PREFIX",
)

VALUE_COL_NAME = "__value__"
FEATURES_COL_NAME = "__features__"
INDEX_COL_PREFIX = "__index__"

# Subfield names of the root `__features__` struct that carry special
# pseudo-features. Their `__dunder__` names prevent collisions with user
# features.
CHALK_NOW_FIELD = "__now__"

# Dtype used for the `_.chalk_window` literal. `timedelta` has microsecond
# precision, so `duration("us")` is the natural arrow representation.
_CHALK_WINDOW_DTYPE = pa.duration("us")


def _index_col(level: int) -> str:
    """Name of the index column at the given nesting level (0 = root)."""
    return f"{INDEX_COL_PREFIX}{level}"


@dataclass(frozen=True)
class FeatureKindScalar:
    data_type: pa.DataType


@dataclass(frozen=True)
class FeatureKindHasMany:
    foreign_namespace: str


@dataclass(frozen=True)
class FeatureKindHasOne:
    foreign_namespace: str


@dataclass(frozen=True)
class FeatureKindWindowed:
    """A windowed feature: a collection of scalar features, one per time window.

    Represented in the input as a struct-typed subfield whose own subfields
    hold the per-window scalar values. The subfields are named with chalk
    duration strings (e.g. `"30d"`, `"1h30m"`).
    """

    data_type: pa.DataType
    """Arrow dtype of each per-window scalar value."""

    windows: tuple[str, ...]
    """Allowed window strings (chalk duration syntax)."""


@dataclass(frozen=True)
class FeatureKindWindowedPseudoFeature:
    """A single per-bucket pseudo-feature of a windowed feature.

    Chalk stores each window of a windowed feature as its own scalar feature
    with FQN `<windowed_feature>__<duration_seconds>__`. `normalize_input`
    uses this kind to recognize such columns and group them back into the
    windowed parent's `struct[<window>: ...]` shape.
    """

    data_type: pa.DataType
    """Arrow dtype of the per-window value."""

    windowed_feature_name: str
    """Name (within the same namespace) of the windowed parent feature."""

    window_seconds: int
    """The bucket's duration in seconds (e.g. `86400` for `"1d"`)."""


FeatureKind = Union[
    FeatureKindScalar,
    FeatureKindHasMany,
    FeatureKindHasOne,
    FeatureKindWindowed,
    FeatureKindWindowedPseudoFeature,
]


class InputContext(Protocol):
    """Resolves the kind of a feature within a namespace.

    A minimal protocol so callers can swap in a real feature graph, a static
    mapping, or a test fixture.
    """

    def get_feature(
        self,
        *,
        namespace_name: str,
        feature_name: str,
    ) -> Optional[FeatureKind]: ...


class GlobalRegistryContext:
    """An `InputContext` backed by chalkpy's global feature registry.

    Reads each feature via `Feature.from_root_fqn(f"{namespace}.{feature}")`
    and inspects the resulting `Feature` to determine its kind:

    - windowed scalar     → `FeatureKindWindowed(data_type, windows)`
    - `is_scalar`         → `FeatureKindScalar(data_type=feature.pyarrow_dtype)`
    - `is_has_one`        → `FeatureKindHasOne(foreign_namespace=...)`
    - `is_has_many`       → `FeatureKindHasMany(foreign_namespace=...)`

    Windowed features are reported with their `window_durations` converted
    to seconds-suffix strings — `[86400, 604800]` → `("86400s", "604800s")`.
    The caller's packed input must use those same strings as the windowed
    feature's struct subfield names (because `parse_chalk_duration_s` is
    used to match the subscript key, declarations like `"30d"` /
    `"86400s"` / `timedelta(days=1)` are all interchangeable, but they
    must agree with whatever the input struct's field names actually are).

    Unknown / unresolvable features return `None` so the caller can raise the
    standard "no feature named ..." error. This avoids forcing every caller
    to build a static `{(namespace, feature): kind}` map by hand.

    Note that this context relies on `FeatureSetBase.registry`, so any
    `@features` classes you intend to look up must already be imported.
    """

    def get_feature(
        self,
        *,
        namespace_name: str,
        feature_name: str,
    ) -> Optional[FeatureKind]:
        # Late import: avoids dragging the rest of `chalk.features` into the
        # module-level import graph (and the eventual circular import) when
        # callers only need the protocol type.
        from chalk.features.feature_field import Feature

        try:
            f = Feature.from_root_fqn(f"{namespace_name}.{feature_name}")
        except Exception:
            return None

        if f.is_has_one:
            joined = f.joined_class
            if joined is None:
                return None
            return FeatureKindHasOne(foreign_namespace=joined.namespace)

        if f.is_has_many:
            joined = f.joined_class
            if joined is None:
                return None
            return FeatureKindHasMany(foreign_namespace=joined.namespace)

        # Windowed pseudo-features (`<feature>__<seconds>__`) must be
        # detected BEFORE the generic scalar branch: chalk reports them as
        # `is_scalar=True` since they're a single bucket, but we want
        # `normalize_input` to recognize them as part of their windowed
        # parent rather than standalone scalars.
        if f.is_windowed_pseudofeature:
            if f.window_duration is None:
                raise ValueError(
                    f"The feature `{f.fqn}` is marked as a windowed scalar feature, but it does not have a specified window duration"
                )
            return FeatureKindWindowedPseudoFeature(
                data_type=f.converter.pyarrow_dtype,
                windowed_feature_name=f.window_stem,
                window_seconds=f.window_duration,
            )

        # Windowed features take precedence over the plain scalar branch.
        # `is_windowed` implies `is_scalar`, so the order matters.
        if f.is_windowed:
            windows = tuple(f"{d}s" for d in f.window_durations)
            return FeatureKindWindowed(
                data_type=f.converter.pyarrow_dtype,
                windows=windows,
            )

        # `FeatureTime` features (`ts: FeatureTime`) report `is_scalar=False`
        # in chalkpy but they are semantically scalars (a single timestamp
        # value per row) and the rest of the helper treats them as such.
        if f.is_scalar or f.is_feature_time:
            return FeatureKindScalar(data_type=f.converter.pyarrow_dtype)

        return None


# --- Internal representation -------------------------------------------------
#
# See the module docstring for the full schema invariants. Briefly:
#
# - `_NamespaceRef.df` columns: `[*index_cols, __features__]` with
#   `__features__: struct[<namespace_name>.<feature>: ...]`.
# - `_Scalar.df` columns:        `[*index_cols, __value__]` with
#   `__value__` of any type.
#
# Both dataclasses are frozen so a result, once produced, is immutable —
# making intermediate plans easy to introspect.


@dataclass(frozen=True)
class _NamespaceRef:
    """A position in the namespace hierarchy during traversal.

    Produced for `_` itself, `_.has_one_feature`, and the inside of
    `_.has_many[...]`.
    """

    namespace_name: str
    """The chalk namespace whose features are accessible here (e.g. `"user"`,
    `"transaction"`).

    By convention, this is also the prefix used when looking up a feature as
    a struct subfield of `__features__` — feature `f` is the subfield
    `f"{namespace_name}.{f}"` — so there is no separate inner-prefix field."""

    df: "DataFrame"
    """Materialized chalkdf DataFrame with schema
    `[*index_cols, __features__]`."""

    index_cols: tuple[str, ...]
    """The index columns in `df`, outermost first. `index_cols[0]` is always
    `__index__0`; each `has_many` traversal appends another `__index__N`."""


@dataclass(frozen=True)
class _Scalar:
    """A scalar value at a particular namespace level.

    Used as the result of any sub-expression that resolves to a value (scalar
    features, function calls, aggregates, ...). `__value__` may have any
    dtype, including struct or list (e.g. for `array_agg`).
    """

    df: "DataFrame"
    """Materialized chalkdf DataFrame with schema `[*index_cols, __value__]`."""

    index_cols: tuple[str, ...]
    """The index columns in `df`, outermost first."""


@dataclass(frozen=True)
class _Literal:
    """A plain Python value passed as a function operand.

    Used to keep literal operands distinguishable from `_Scalar` values
    without resorting to `Any`. The value flows straight into the chalkdf
    function call.
    """

    value: Any


@dataclass(frozen=True)
class _Windowed:
    """Intermediate windowed-feature reference, produced by `_compute_attr`
    when a `FeatureKindWindowed` is encountered.

    The only valid operation on a `_Windowed` is to be subscripted via
    `UnderscoreItem` with a window key (string, timedelta, int seconds, or
    `_.chalk_window`), which selects the corresponding struct subfield and
    materializes a `_Scalar`.
    """

    df: "DataFrame"
    """`[*index_cols, __value__]` with `__value__` a `struct[<window>: data_type]`."""

    index_cols: tuple[str, ...]
    windows: tuple[str, ...]
    data_type: pa.DataType


_ComputeResult = Union[_Scalar, _NamespaceRef, _Windowed]
_FunctionOperand = Union[_Scalar, _Literal]


@dataclass(frozen=True)
class _EvalState:
    """Immutable per-evaluation state threaded through the recursion.

    `feature_context` is the user-supplied feature lookup. `root` is the
    top-level `_NamespaceRef` — kept around so `_.chalk_now` can be
    resolved against the root's `__features__.__now__` regardless of how
    deep into has_many traversal the expression currently is.
    `chalk_window` is the optional timedelta passed in by the caller for
    `_.chalk_window`.
    """

    feature_context: InputContext
    root: _NamespaceRef
    chalk_window: Optional[timedelta]


# --- Public entry point ------------------------------------------------------


def eval_underscore(
    expr: Any,
    *,
    input_table: Any,
    namespace_name: Optional[str] = None,
    context: Optional[InputContext] = None,
    chalk_window: Optional[timedelta] = None,
) -> "DataFrame":
    """Evaluate `expr` against `input_table`.

    `expr` may be either:

    - an `Underscore` expression, in which case `namespace_name` is required
      and (for `_.chalk_window`) `chalk_window` may be required; or
    - a chalk feature / `FeatureWrapper` (e.g. `User.total_amount`), in which
      case the feature's `.underscore_expression`, `.namespace`, and (for
      windowed pseudo-features) `.window_duration` are read automatically.
      Callers can still override `namespace_name` and `chalk_window`
      explicitly; the explicit value wins.

    `input_table` accepts any of:

    - a `chalkdf.DataFrame` already in the packed shape
      `[__index__0, __features__]` — used directly.
    - a `chalkdf.DataFrame` in the flat caller-friendly shape (dotted-FQN
      columns and/or nested dicts/lists); auto-routed through
      `normalize_input`.
    - a `pyarrow.Table` (treated like the above).
    - a `list[dict]` of records (each dict keyed by feature FQN) — converted
      via `pyarrow.Table.from_pylist` and auto-normalized.
    - a `dict[str, list]` of columnar data — converted via
      `pyarrow.Table.from_pydict` and auto-normalized.

    For non-`chalkdf.DataFrame` inputs the coercion casts top-level scalar
    columns to the declared feature dtype from the context (walking dotted
    column names through the feature graph), so that e.g. an inferred
    `int64` matches a declared `int32`.

    `context` resolves features by `(namespace, name)`. If `None`, defaults
    to a `GlobalRegistryContext` that reads chalkpy's global feature
    registry.

    The output value column is named `__value__` for a bare-Underscore
    `expr`. When `expr` is a chalk feature, the column is renamed to the
    feature's root FQN so the caller's DataFrame already matches the
    feature name.
    """
    underscore_expr, feature_namespace, feature_window, output_column = _interpret_eval_target(expr)

    if namespace_name is None:
        namespace_name = feature_namespace
    if chalk_window is None:
        chalk_window = feature_window
    if namespace_name is None:
        raise ValueError(
            (
                "`namespace_name` is required when `expr` is a bare Underscore "
                "expression (it can only be inferred when `expr` is a chalk feature)"
            )
        )
    if context is None:
        context = GlobalRegistryContext()

    input_table = _coerce_to_dataframe(input_table, namespace_name, context)
    if FEATURES_COL_NAME not in input_table.schema:
        input_table = normalize_input(input_table, context=context)

    if _index_col(0) not in input_table.schema:
        raise ValueError(f"input_table must contain a `{_index_col(0)}` column that uniquely identifies each input row")
    if FEATURES_COL_NAME not in input_table.schema:
        raise ValueError(
            f"input_table must contain a `{FEATURES_COL_NAME}` struct column holding the root namespace's features"
        )
    root = _NamespaceRef(
        namespace_name=namespace_name,
        df=input_table,
        index_cols=(_index_col(0),),
    )
    state = _EvalState(feature_context=context, root=root, chalk_window=chalk_window)

    result = _compute(underscore_expr, root, state)
    if not isinstance(result, _Scalar):
        raise ValueError(
            (
                f"Expected expression `{underscore_expr}` to produce a scalar value, "
                f"got {type(result).__name__} (an incomplete intermediate) instead"
            )
        )

    if output_column is None or output_column == VALUE_COL_NAME:
        return result.df
    # Rename the value column to the feature's FQN. This is the only place
    # in the helper that knows about the feature-supplied output name —
    # the inner computation always uses the canonical `__value__`.
    return result.df.project(
        {
            **{ic: result.df.col(ic) for ic in result.index_cols},
            output_column: result.df.col(VALUE_COL_NAME),
        }
    )


def eval_underscore_values(
    expr: Any,
    *,
    input_table: Any,
    namespace_name: Optional[str] = None,
    context: Optional[InputContext] = None,
    chalk_window: Optional[timedelta] = None,
) -> list:
    """Materialize `eval_underscore(...)` and return the value column as a
    Python list, sorted by `__index__0` so the order matches the original
    input rows.

    Useful for tests and quick interactive exploration. Production callers
    should usually prefer `eval_underscore` directly: that keeps the
    result lazy as a `chalkdf.DataFrame`, retains the `__index__0` column
    for joining the result back to the input, and composes with further
    chalkdf operations.

    Accepts all the same arguments as `eval_underscore`.
    """
    df = eval_underscore(
        expr,
        input_table=input_table,
        namespace_name=namespace_name,
        context=context,
        chalk_window=chalk_window,
    )
    arrow = df.to_arrow().sort_by([(_index_col(0), "ascending")])
    value_columns = [name for name in arrow.schema.names if not name.startswith(INDEX_COL_PREFIX)]
    if len(value_columns) != 1:  # pragma: no cover  -- invariant of eval_underscore
        raise AssertionError(f"eval_underscore_values expected exactly one value column, got {value_columns!r}")
    return arrow.column(value_columns[0]).to_pylist()


# --- Input coercion (raw → chalkdf.DataFrame) -------------------------------


def _coerce_to_dataframe(
    input_table: Any,
    namespace_name: str,
    context: InputContext,
) -> "DataFrame":
    """Convert a caller-supplied input into a `chalkdf.DataFrame`.

    Supported input shapes:

    - `chalkdf.DataFrame` — returned as-is.
    - `pyarrow.Table` — wrapped, with top-level scalar columns cast to the
      declared dtype per the feature context.
    - `list[dict]` — converted via `pa.Table.from_pylist` then cast.
    - `dict[str, list]` — converted via `pa.Table.from_pydict` then cast.

    Casting walks each top-level column's dotted name through the feature
    graph; if it resolves to a scalar (possibly via has_one drill-down)
    whose declared dtype differs from the inferred dtype, the column is
    cast to the declared dtype.
    """
    if DataFrame is None:  # pyright: ignore[reportUnnecessaryComparison]
        raise ValueError(
            "The chalkpy eval_underscore helper requires that the `chalkdf` dependency is installed - consider running `pip install chalkdf`"
        )

    if isinstance(input_table, DataFrame):
        return input_table

    if isinstance(input_table, pa.Table):
        table = input_table
    elif isinstance(input_table, list):
        if not input_table:
            raise ValueError(
                (
                    "input_table is an empty list — cannot infer a schema; "
                    "pass a non-empty list of records or a pre-built DataFrame"
                )
            )
        table = pa.Table.from_pylist(input_table)
    elif isinstance(input_table, dict):
        table = pa.Table.from_pydict(input_table)
    else:
        raise TypeError(
            (
                f"input_table must be a chalkdf.DataFrame, pyarrow.Table, "
                f"list[dict], or dict[str, list]; got {type(input_table).__name__}"
            )
        )

    table = _cast_scalar_columns_to_declared_dtype(table, namespace_name, context)
    return DataFrame.from_arrow(table)


def _cast_scalar_columns_to_declared_dtype(table: "pa.Table", root_namespace: str, context: InputContext) -> "pa.Table":
    """Cast each top-level column to the declared dtype from the context
    when it resolves to a scalar feature (possibly via has_one drill-down).

    Columns that don't resolve to a known scalar (struct / list columns,
    special `__*` columns, unknown columns) are left untouched and pa's
    own inference applies.
    """
    new_fields: list[pa.Field] = []
    needs_cast = False
    for field in table.schema:
        declared = _declared_scalar_dtype(field.name, root_namespace, context)
        if declared is not None and declared != field.type:
            new_fields.append(pa.field(field.name, declared))
            needs_cast = True
        else:
            new_fields.append(field)
    if not needs_cast:
        return table
    return table.cast(pa.schema(new_fields))


def _declared_scalar_dtype(column_name: str, root_namespace: str, context: InputContext) -> Optional["pa.DataType"]:
    """If `column_name` resolves to a scalar feature (possibly nested via
    `has_one` drill-down) per the context, return its declared dtype;
    otherwise `None`.

    `"user.amount"`           → scalar `amount` of `user` → its `data_type`
    `"user.account.balance"`  → walks `user` ⇒ `account` (has_one) ⇒ scalar
                                `balance` → its `data_type`
    `"user.account"`          → resolves to has_one (not scalar) → `None`
    `"user.transactions"`     → resolves to has_many → `None`
    `"__index__0"` etc.       → no namespace prefix match → `None`
    """
    if not column_name.startswith(root_namespace + "."):
        return None

    current_namespace = root_namespace
    segments = column_name[len(root_namespace) + 1 :].split(".")
    while segments:
        feature_name = segments[0]
        rest = segments[1:]
        kind = context.get_feature(namespace_name=current_namespace, feature_name=feature_name)
        if kind is None:
            return None
        if isinstance(kind, FeatureKindScalar):
            return kind.data_type if not rest else None
        if isinstance(kind, FeatureKindHasOne):
            if not rest:
                # The column is the has_one struct itself; don't try to
                # cast the whole struct.
                return None
            current_namespace = kind.foreign_namespace
            segments = rest
            continue
        # has_many / windowed at top level — leave inferred.
        return None
    return None


# --- Caller-friendly input normalization ------------------------------------


# Caller-supplied "now" timestamp column candidates, in priority order. If
# any of these is present on the input, it is renamed to `__now__` so that
# `_.chalk_now` finds it. We complain if more than one shows up at once.
_NOW_COLUMN_ALIASES: tuple[str, ...] = (
    "__chalk__.now",  # chalkpy's `Now` feature FQN
    "__ts__",
    "__now__",
)


def normalize_input(
    df: "DataFrame",
    *,
    context: Optional[InputContext] = None,
) -> "DataFrame":
    """Convert a caller-friendly `chalkdf.DataFrame` into the eval_underscore
    input shape: `[__index__0, __features__]`.

    The input is expected to use the chalk-feature naming convention — flat
    columns named `"<ns>.<feature>"` for scalars, with optional dotted
    drill-down (e.g. `"user.account.balance"`) for `has_one` chains. The
    helper walks the `InputContext` to determine which features are scalars
    vs `has_one` vs `has_many`, and recursively groups the dotted columns
    into the nested `struct[...]` form that `eval_underscore` requires:

    - **Scalars** are projected straight in as struct subfields.
    - **`has_one`** with flat dotted children: synthesized into a struct
      whose subfields use the *foreign* namespace name as prefix (per the
      packed-input convention). If the user already provided a struct
      column (e.g. `"user.account"`), it's passed through as-is.
    - **`has_many`** is expected to already be a `large_list[struct[...]]`
      column and is passed through directly.
    - **Windowed features** are expected to already be a `struct[<window>:
      ...]` column and are passed through directly.

    The root namespace is inferred from the input column names — every
    feature-shaped column (matching `<namespace>.<feature>`) must share a
    common namespace prefix; otherwise the helper raises.

    `__index__0` is added via `with_unique_id` if not already present.

    The "now" timestamp can be supplied via any one of: chalk's `Now`
    feature FQN (`"__chalk__.now"`), a `"__ts__"` column, or a
    pre-named `"__now__"` column. If exactly one is present it is renamed
    to `__now__` and folded in as a special subfield of `__features__`.
    Providing more than one raises a `ValueError`.

    Unknown columns (not matching any feature in the context) are silently
    ignored.
    """
    if context is None:
        context = GlobalRegistryContext()

    df, has_now = _resolve_now_column(df)

    if _index_col(0) not in df.schema:
        df = df.with_unique_id(_index_col(0))

    namespace_name = _infer_namespace_from_columns(df.column_names)

    extra_subfields: dict[str, Underscore] = {}
    if has_now:
        extra_subfields["__now__"] = df.col("__now__")

    features_expr, consumed = _build_features_struct(
        df=df,
        namespace_name=namespace_name,
        column_prefix=namespace_name,
        context=context,
        extra_subfields=extra_subfields,
    )
    if features_expr is None:
        raise ValueError(
            (
                f"normalize_input: no features matching namespace '{namespace_name}' "
                f"were found in the input (columns: {df.column_names})"
            )
        )

    # Strict mode: every feature-shaped column in the input must have been
    # consumed by the packed struct. If anything is left over, it means the
    # caller has columns that don't map to any feature in the context — we
    # surface that as an error rather than silently dropping data.
    feature_shaped_cols = {c for c in df.column_names if not c.startswith("__") and "." in c}
    unaccounted = feature_shaped_cols - consumed
    if unaccounted:
        raise ValueError(
            (
                f"normalize_input: input columns {sorted(unaccounted)!r} don't "
                f"match any feature in namespace '{namespace_name}' (or any "
                f"nested has_one struct under it). Remove them or extend the "
                f"feature context."
            )
        )

    return df.project(
        {
            _index_col(0): df.col(_index_col(0)),
            FEATURES_COL_NAME: features_expr,
        }
    )


def _infer_namespace_from_columns(column_names: list[str]) -> str:
    """Infer the root namespace from the first segment of every
    feature-shaped column in `column_names`.

    A column is "feature-shaped" if it contains a `.` and does not start
    with `__` (which would mark a special column such as `__index__N`,
    `__ts__`, `__now__`, or `__chalk__.now`).

    All feature-shaped columns must share the same first segment; multiple
    candidate prefixes raise. Zero candidate prefixes also raise.
    """
    candidates: set[str] = set()
    for col in column_names:
        if col.startswith("__"):
            continue
        if "." not in col:
            continue
        candidates.add(col.split(".", 1)[0])
    if not candidates:
        raise ValueError(
            (
                "normalize_input: cannot infer namespace — input has no "
                "feature-shaped columns (expected at least one column of the "
                "form `<namespace>.<feature>`)"
            )
        )
    if len(candidates) > 1:
        raise ValueError(
            (
                f"normalize_input: cannot infer namespace — input columns have "
                f"multiple namespace prefixes: {sorted(candidates)!r}"
            )
        )
    return next(iter(candidates))


def _resolve_now_column(df: "DataFrame") -> tuple["DataFrame", bool]:
    """Look for any caller-supplied "now" column under one of the recognized
    aliases. If exactly one is present, rename it to `__now__` and return
    `(df, True)`. If none are present, return `(df, False)`. If more than
    one is present, raise.
    """
    found = [name for name in _NOW_COLUMN_ALIASES if name in df.schema]
    if len(found) > 1:
        raise ValueError(
            (
                f"normalize_input: input has multiple `now` columns {found!r}. "
                f"Provide only one of {list(_NOW_COLUMN_ALIASES)!r}."
            )
        )
    if not found:
        return df, False
    src = found[0]
    if src == "__now__":
        return df, True
    # Rename src → __now__ via project (every other column passes through).
    return (
        df.project(
            {
                **{c: df.col(c) for c in df.column_names if c != src},
                "__now__": df.col(src),
            }
        ),
        True,
    )


def _build_features_struct(
    *,
    df: "DataFrame",
    namespace_name: str,
    column_prefix: str,
    context: InputContext,
    extra_subfields: Optional[dict[str, Underscore]] = None,
) -> tuple[Optional[Underscore], set[str]]:
    """Recursively pack columns under `column_prefix` into the canonical
    `struct[<ns>.<feature>: ...]` form for `namespace_name`.

    Returns `(struct_expr, consumed_columns)`:
    - `struct_expr` is `None` if no features matched (caller decides whether
      that's an error).
    - `consumed_columns` is the set of input column names that were used
      to build the struct (directly or transitively through recursion).
      `normalize_input` uses this to detect "unknown" columns the caller
      provided that don't correspond to any feature in the context.
    """
    available = set(df.column_names)
    prefix_dot = column_prefix + "." if column_prefix else ""

    # Find every unique immediate-child feature name appearing in any column
    # under `column_prefix`. We also pick up an exact match
    # (e.g. `"user.account"` provided as a pre-packed struct).
    #
    # Columns whose first segment resolves to a `FeatureKindWindowedPseudoFeature`
    # (chalk's `<stem>__<seconds>__` per-bucket form) get substituted with
    # the windowed parent's name, so the `FeatureKindWindowed` branch
    # below picks the per-bucket columns up and groups them into the
    # canonical struct shape.
    feature_names: set[str] = set()
    for col in available:
        if not col.startswith(prefix_dot):
            continue
        tail = col[len(prefix_dot) :]
        if not tail:
            continue
        first_segment = tail.split(".", 1)[0]
        kind = context.get_feature(namespace_name=namespace_name, feature_name=first_segment)
        if isinstance(kind, FeatureKindWindowedPseudoFeature):
            feature_names.add(kind.windowed_feature_name)
        else:
            feature_names.add(first_segment)

    subfields: dict[str, Underscore] = {}
    consumed: set[str] = set()

    for feature_name in sorted(feature_names):
        kind = context.get_feature(namespace_name=namespace_name, feature_name=feature_name)
        if kind is None:
            # Not a known feature; leave columns unconsumed so the top-level
            # caller can flag them.
            continue

        subfield_name = f"{namespace_name}.{feature_name}"
        column_for_feature = f"{prefix_dot}{feature_name}"

        if isinstance(kind, FeatureKindScalar):
            if column_for_feature in available:
                subfields[subfield_name] = df.col(column_for_feature)
                consumed.add(column_for_feature)

        elif isinstance(kind, FeatureKindHasOne):
            if column_for_feature in available:
                # Already a struct column — pass through.
                subfields[subfield_name] = df.col(column_for_feature)
                consumed.add(column_for_feature)
            else:
                # Synthesize from deeper dotted columns.
                inner, inner_consumed = _build_features_struct(
                    df=df,
                    namespace_name=kind.foreign_namespace,
                    column_prefix=column_for_feature,
                    context=context,
                )
                consumed |= inner_consumed
                if inner is not None:
                    subfields[subfield_name] = inner

        elif isinstance(kind, FeatureKindHasMany):
            # Must be pre-packed as `large_list[struct[...]]`.
            if column_for_feature in available:
                subfields[subfield_name] = df.col(column_for_feature)
                consumed.add(column_for_feature)

        elif isinstance(kind, FeatureKindWindowed):
            if column_for_feature in available:
                # Pre-packed `struct[<window>: ...]` — pass through.
                subfields[subfield_name] = df.col(column_for_feature)
                consumed.add(column_for_feature)
            else:
                # Try chalk's native pseudo-feature FQN form: one flat
                # column per window suffixed with `__<seconds>__`. Group
                # any present windows into the canonical struct shape.
                window_subfields: dict[str, Underscore] = {}
                for window in kind.windows:
                    seconds = parse_chalk_duration_s(window)
                    pseudo_col = f"{column_for_feature}__{seconds}__"
                    if pseudo_col in available:
                        window_subfields[window] = df.col(pseudo_col)
                        consumed.add(pseudo_col)
                if window_subfields:
                    names = list(window_subfields.keys())
                    values = [window_subfields[k] for k in names]
                    subfields[subfield_name] = UnderscoreFunction("struct_pack", names, *values)

    if extra_subfields:
        subfields.update(extra_subfields)

    if not subfields:
        return None, consumed

    # Build a chalkdf `struct_pack` call. chalkdf infers each subfield's
    # dtype from the corresponding expression at conversion time, so we
    # don't need to compute them upfront here.
    names = list(subfields.keys())
    values = [subfields[k] for k in names]
    return UnderscoreFunction("struct_pack", names, *values), consumed


def _interpret_eval_target(
    expr: Any,
) -> tuple[Underscore, Optional[str], Optional[timedelta], Optional[str]]:
    """Resolve the `expr` argument of `eval_underscore` into a tuple of
    `(underscore_expression, default_namespace, default_chalk_window,
    output_column_name)`.

    - For a raw `Underscore`, the defaults are `None` — the caller must
      supply `namespace_name` (and `chalk_window` if used). The output
      column name is `None`, meaning the result keeps the default
      `__value__` column name.
    - For a chalk feature / `FeatureWrapper`, reads the feature's underscore
      expression and inherits the namespace; for windowed pseudo-features,
      also inherits the bucket's window duration as the default
      `chalk_window`. The output column name is the feature's root FQN so
      the caller's result column matches the feature name directly.
    """
    if isinstance(expr, Underscore):
        return expr, None, None, None

    # Late imports: avoid pulling chalk's wrapper / feature graph in at
    # module load time (eval_underscore.py is also useful as a low-level
    # helper independent of those).
    from chalk.features.feature_field import Feature
    from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature

    if isinstance(expr, FeatureWrapper):
        feature = unwrap_feature(expr)
    elif isinstance(expr, Feature):
        feature = expr
    else:
        raise TypeError(f"`expr` must be an Underscore expression or a chalk feature, got {type(expr).__name__}")

    underscore_expr = feature.underscore_expression
    if underscore_expr is None:
        raise ValueError(f"Feature '{feature.root_fqn}' has no underscore expression to evaluate")

    default_window: Optional[timedelta] = None
    if feature.is_windowed_pseudofeature:
        if feature.window_duration is None:
            raise ValueError(
                f"The feature '{feature.fqn}' is invalid because it is marked as a windowed scalar feature, but it has no specified window_duration"
            )
        # `window_duration` is in seconds.
        default_window = timedelta(seconds=feature.window_duration)

    return underscore_expr, feature.namespace, default_window, feature.root_fqn


# --- Recursive walker --------------------------------------------------------


def _compute(
    expr: Any,
    current: _NamespaceRef,
    state: _EvalState,
) -> _ComputeResult:
    if isinstance(expr, UnderscoreRoot):
        return current

    if isinstance(expr, DoubleUnderscore):
        # `__` refers to the namespace "one level up" — typically used inside
        # a has_many filter (e.g. `_.txns.where(_.user_id == __.id)`). Not
        # yet implemented; the recursion would need to track the namespace
        # stack and join the parent's scalar columns into the current level.
        raise NotImplementedError(
            f"`__` (outer-namespace reference) is not yet supported in eval_underscore (in `{expr}`)"
        )

    if isinstance(expr, UnderscoreAttr):
        return _compute_attr(expr, current, state)

    if isinstance(expr, UnderscoreFunction):
        return _compute_function(expr, current, state)

    if isinstance(expr, UnderscoreItem):
        return _compute_item(expr, current, state)

    if isinstance(expr, UnderscoreCall):
        return _compute_call(expr, current, state)

    if isinstance(expr, UnderscoreCast):
        return _compute_cast(expr, current, state)

    raise ValueError(f"Unsupported underscore expression type `{type(expr).__name__}` in `{expr}`")


def _compute_attr(
    expr: UnderscoreAttr,
    current: _NamespaceRef,
    state: _EvalState,
) -> _ComputeResult:
    attr = expr._chalk__attr

    # Special pseudo-features. Both must be applied directly to `_`, and both
    # resolve to a `_Scalar` at the root level so they can be broadcast into
    # any deeper level via the usual prefix-join in `_join_scalars`.
    if attr in ("chalk_now", "chalk_window"):
        if not isinstance(expr._chalk__parent, UnderscoreRoot):
            raise ValueError(f"The special attribute `_.{attr}` can only be applied directly to `_`, not as `{expr}`")
        if attr == "chalk_now":
            return _compute_chalk_now(state, expr)
        return _compute_chalk_window(state, expr)

    parent = _compute(expr._chalk__parent, current, state)
    if isinstance(parent, _Scalar):
        # Attribute access on a scalar is only valid when the scalar's
        # value happens to be a struct — in that case, `.<field>` is a
        # `get_struct_subfield` projection. This is *not* a feature lookup
        # (there's no namespace), so field names follow the underlying
        # struct schema exactly.
        return _project_scalar_struct_field(parent, attr, expr)
    assert isinstance(parent, _NamespaceRef)

    feature_info = state.feature_context.get_feature(
        namespace_name=parent.namespace_name,
        feature_name=attr,
    )
    if feature_info is None:
        raise ValueError(
            f"No feature named '{attr}' in namespace '{parent.namespace_name}' to compute expression `{expr}`"
        )

    # Feature lookup is always a struct subfield of `__features__`, named with
    # the immediate namespace's prefix (see module docstring).
    subfield_name = f"{parent.namespace_name}.{attr}"
    subfield_dtype = _resolve_features_subfield(parent, subfield_name, expr)

    feature_value_expr = parent.df.col(FEATURES_COL_NAME).get_struct_subfield(subfield_name)
    index_projection = {ic: parent.df.col(ic) for ic in parent.index_cols}

    if isinstance(feature_info, FeatureKindScalar):
        if subfield_dtype != feature_info.data_type:
            raise ValueError(
                (
                    f"Feature '{attr}' on namespace '{parent.namespace_name}' is "
                    f"declared as {feature_info.data_type} in the context, but the "
                    f"input has subfield '{subfield_name}' with dtype "
                    f"{subfield_dtype} while resolving `{expr}`"
                )
            )
        new_df = parent.df.project({**index_projection, VALUE_COL_NAME: feature_value_expr})
        return _Scalar(df=new_df, index_cols=parent.index_cols)

    if isinstance(feature_info, FeatureKindHasOne):
        if not isinstance(subfield_dtype, pa.StructType):
            raise ValueError(
                (
                    f"Expected `has_one` feature '{attr}' on namespace "
                    f"'{parent.namespace_name}' to be represented as a struct in "
                    f"the input, got dtype {subfield_dtype} while resolving `{expr}`"
                )
            )
        new_df = parent.df.project({**index_projection, FEATURES_COL_NAME: feature_value_expr})
        return _NamespaceRef(
            namespace_name=feature_info.foreign_namespace,
            df=new_df,
            index_cols=parent.index_cols,
        )

    if isinstance(feature_info, FeatureKindHasMany):
        return _enter_has_many(
            parent=parent,
            attr=attr,
            info=feature_info,
            subfield_dtype=subfield_dtype,
            feature_value_expr=feature_value_expr,
            expr=expr,
        )

    if isinstance(feature_info, FeatureKindWindowed):
        return _project_windowed_feature(
            parent=parent,
            attr=attr,
            info=feature_info,
            subfield_dtype=subfield_dtype,
            feature_value_expr=feature_value_expr,
            expr=expr,
        )

    raise ValueError(f"Unsupported feature kind {feature_info!r} for expression `{expr}`")


def _project_scalar_struct_field(
    parent: _Scalar,
    attr: str,
    expr: UnderscoreAttr,
) -> _Scalar:
    """Project a struct subfield out of a `_Scalar` whose `__value__` is a
    struct. Errors descriptively if the value isn't a struct or the field
    isn't present.
    """
    value_dtype = parent.df.schema[VALUE_COL_NAME]
    if not isinstance(value_dtype, pa.StructType):
        raise ValueError(
            (
                f"Cannot access attribute `.{attr}` on a scalar value of dtype "
                f"{value_dtype} (in expression `{expr}`); only struct-typed "
                f"scalars support attribute access"
            )
        )
    field_names = [value_dtype.field(i).name for i in range(value_dtype.num_fields)]
    if attr not in field_names:
        raise ValueError(
            (
                f"Struct subfield '{attr}' is not present on the scalar value "
                f"(available subfields: {field_names}) in expression `{expr}`"
            )
        )
    new_df = parent.df.project(
        {
            **{ic: parent.df.col(ic) for ic in parent.index_cols},
            VALUE_COL_NAME: parent.df.col(VALUE_COL_NAME).get_struct_subfield(attr),
        }
    )
    return _Scalar(df=new_df, index_cols=parent.index_cols)


def _compute_cast(
    expr: UnderscoreCast,
    current: _NamespaceRef,
    state: _EvalState,
) -> _Scalar:
    """Evaluate an `UnderscoreCast` — either `F.cast(<underscore>, dtype)`
    (cast an existing scalar) or `lit(<python value>, dtype)` (typed literal).

    For an Underscore inner value, we recursively compute it to a `_Scalar`
    and project a new `_Scalar` with `__value__` cast to the target dtype.
    For a literal inner value, we project against `current.df` so the
    result broadcasts to one value per row at the current level.
    """
    inner = expr._chalk__value
    to_type = expr._chalk__to_type

    if isinstance(inner, Underscore):  # pyright: ignore[reportUnnecessaryIsInstance]
        inner_result = _compute(inner, current, state)
        if not isinstance(inner_result, _Scalar):
            raise ValueError(
                f"Cannot cast a non-scalar value `{inner}` (in `{expr}`); the value being cast must resolve to a scalar"
            )
        # Build a new `UnderscoreCast` rooted at the joined df's `__value__`
        # column, then let chalkdf's project apply the cast.
        cast_expr: Underscore = UnderscoreCast(
            value=UnderscoreAttr(UnderscoreRoot(), VALUE_COL_NAME),
            to_type=to_type,
        )
        new_df = inner_result.df.project(
            {
                **{ic: inner_result.df.col(ic) for ic in inner_result.index_cols},
                VALUE_COL_NAME: cast_expr,
            }
        )
        return _Scalar(df=new_df, index_cols=inner_result.index_cols)

    # Typed literal — broadcast to one value per row at the current level.
    cast_expr = UnderscoreCast(value=inner, to_type=to_type)
    new_df = current.df.project(
        {
            **{ic: current.df.col(ic) for ic in current.index_cols},
            VALUE_COL_NAME: cast_expr,
        }
    )
    return _Scalar(df=new_df, index_cols=current.index_cols)


def _resolve_features_subfield(
    ns: _NamespaceRef,
    subfield_name: str,
    expr: Underscore,
) -> pa.DataType:
    """Verify that the given subfield exists on `ns.df`'s `__features__` struct
    and return its dtype. Raises a descriptive error if missing or malformed.
    """
    features_dtype = ns.df.schema[FEATURES_COL_NAME]
    if not isinstance(features_dtype, pa.StructType):
        # This is an invariant of `_NamespaceRef`; if it's violated, an
        # upstream step produced a malformed result.
        raise ValueError(
            (
                f"Expected `{FEATURES_COL_NAME}` column to be a struct in order "
                f"to resolve `{expr}`, got dtype {features_dtype}"
            )
        )
    field_names = [features_dtype.field(i).name for i in range(features_dtype.num_fields)]
    if subfield_name not in field_names:
        raise ValueError(
            (
                f"The feature subfield '{subfield_name}' isn't present in the "
                f"`{FEATURES_COL_NAME}` struct of the input "
                f"(available subfields: {field_names}) "
                f"while resolving `{expr}`"
            )
        )
    return features_dtype.field(field_names.index(subfield_name)).type


# --- chalk_now / chalk_window ------------------------------------------------


def _compute_chalk_now(state: _EvalState, expr: Underscore) -> _Scalar:
    """`_.chalk_now` always reads the `__now__` subfield of the **root**
    `__features__` struct. The result is a `_Scalar` at the root level, which
    `_join_scalars` will broadcast onto any deeper level on demand.
    """
    root = state.root
    features_dtype = root.df.schema[FEATURES_COL_NAME]
    if not isinstance(features_dtype, pa.StructType):
        raise ValueError(
            (
                f"Expected the root `{FEATURES_COL_NAME}` column to be a struct "
                f"while resolving `{expr}`, got dtype {features_dtype}"
            )
        )
    field_names = [features_dtype.field(i).name for i in range(features_dtype.num_fields)]
    if CHALK_NOW_FIELD not in field_names:
        raise ValueError(
            (
                f"`_.chalk_now` requires a `{CHALK_NOW_FIELD}` subfield on the "
                f"root `{FEATURES_COL_NAME}` struct, but it is not present "
                f"(available subfields: {field_names})"
            )
        )
    now_expr = root.df.col(FEATURES_COL_NAME).get_struct_subfield(CHALK_NOW_FIELD)
    new_df = root.df.project(
        {
            **{ic: root.df.col(ic) for ic in root.index_cols},
            VALUE_COL_NAME: now_expr,
        }
    )
    return _Scalar(df=new_df, index_cols=root.index_cols)


def _compute_chalk_window(state: _EvalState, expr: Underscore) -> _Scalar:
    """`_.chalk_window` resolves to the timedelta constant passed in via the
    `chalk_window=` argument of `eval_underscore`. Broadcast across root rows
    so the result is a `_Scalar` at the root level.
    """
    if state.chalk_window is None:
        raise ValueError(
            (
                f"`_.chalk_window` was used (in `{expr}`) but no `chalk_window` "
                f"argument was passed to `eval_underscore(...)`"
            )
        )
    root = state.root
    window_literal: Underscore = UnderscoreCast(
        value=cast(Underscore, state.chalk_window),
        to_type=_CHALK_WINDOW_DTYPE,
    )
    new_df = root.df.project(
        {
            **{ic: root.df.col(ic) for ic in root.index_cols},
            VALUE_COL_NAME: window_literal,
        }
    )
    return _Scalar(df=new_df, index_cols=root.index_cols)


# --- windowed feature projection ---------------------------------------------


def _project_windowed_feature(
    *,
    parent: _NamespaceRef,
    attr: str,
    info: FeatureKindWindowed,
    subfield_dtype: pa.DataType,
    feature_value_expr: Underscore,
    expr: UnderscoreAttr,
) -> _Windowed:
    """Project a windowed feature out of `parent`. The subfield must be a
    struct whose per-window subfields are declared on `info.windows`.
    Returns a `_Windowed` intermediate that can only be subscripted.
    """
    if not isinstance(subfield_dtype, pa.StructType):
        raise ValueError(
            (
                f"Expected windowed feature '{attr}' on namespace "
                f"'{parent.namespace_name}' to be a struct (one subfield per "
                f"window) in the input, got dtype {subfield_dtype} while "
                f"resolving `{expr}`"
            )
        )
    # Use the windows actually present in the input. The caller may have
    # provided only a subset of the declared windows; we don't error here —
    # the per-subscript window lookup in `_select_window` will surface a
    # clear error if the specific window being requested is missing.
    available_windows = tuple(subfield_dtype.field(i).name for i in range(subfield_dtype.num_fields))
    new_df = parent.df.project(
        {
            **{ic: parent.df.col(ic) for ic in parent.index_cols},
            VALUE_COL_NAME: feature_value_expr,
        }
    )
    return _Windowed(
        df=new_df,
        index_cols=parent.index_cols,
        windows=available_windows,
        data_type=info.data_type,
    )


# --- has_many entry, subscript, and aggregate calls --------------------------


# Kinds of "secondary" positional arguments an aggregate may take after its
# receiver. `"scalar"` is an Underscore expression to be evaluated in the same
# has_many namespace as the value column; `"constant_int"` is a plain Python
# `int` literal (e.g. the `n` in `max_by_n`).
_SecondaryKind = Literal["scalar", "constant_int"]


@dataclass(frozen=True)
class _AggregateSpec:
    """Declarative behavior for an aggregate method like `.sum()` or `.max_by()`.

    Aggregates take the form `<receiver>.<name>(<secondary args...>)`:

    - `name`: the method name (also used to build the chalkdf agg expression
      `_.<primary>.<name>(...)`).
    - `needs_primary`: whether the aggregate semantically requires a primary
      value column. `True` for everything except `count`.
    - `secondary_kinds`: kinds of the positional arguments after the receiver.
      `"scalar"` arguments are Underscore expressions evaluated in the same
      has_many namespace as the value column — aggregates with any scalar
      secondaries can therefore only be called on a subscript receiver
      `_.has_many[value].<name>(...)`. `"constant_int"` arguments are plain
      Python integers.
    - `empty_default`: optional value to coalesce into `__value__` for empty
      groups (parents whose has_many list was empty). If `None`, NULL is left
      as-is. Matched to the value column's dtype via `pa.scalar(...)`.
    """

    name: str
    needs_primary: bool
    secondary_kinds: tuple[_SecondaryKind, ...] = field(default_factory=tuple)
    empty_default: Optional[Any] = None


_AGGREGATES: dict[str, _AggregateSpec] = {
    "sum": _AggregateSpec("sum", needs_primary=True, empty_default=0),
    "count": _AggregateSpec("count", needs_primary=False, empty_default=0),
    "min": _AggregateSpec("min", needs_primary=True),
    "max": _AggregateSpec("max", needs_primary=True),
    "mean": _AggregateSpec("mean", needs_primary=True),
    "array_agg": _AggregateSpec("array_agg", needs_primary=True),
    "max_by": _AggregateSpec("max_by", needs_primary=True, secondary_kinds=("scalar",)),
    "min_by": _AggregateSpec("min_by", needs_primary=True, secondary_kinds=("scalar",)),
    "max_by_n": _AggregateSpec("max_by_n", needs_primary=True, secondary_kinds=("scalar", "constant_int")),
    "min_by_n": _AggregateSpec("min_by_n", needs_primary=True, secondary_kinds=("scalar", "constant_int")),
}


def _enter_has_many(
    *,
    parent: _NamespaceRef,
    attr: str,
    info: FeatureKindHasMany,
    subfield_dtype: pa.DataType,
    feature_value_expr: Underscore,
    expr: Underscore,
) -> _NamespaceRef:
    """Enter a has_many namespace by exploding the list column and adding a
    fresh index column at the new depth."""
    if not isinstance(subfield_dtype, (pa.LargeListType, pa.ListType)):
        raise ValueError(
            (
                f"Expected `has_many` feature '{attr}' on namespace "
                f"'{parent.namespace_name}' to be represented as a large_list "
                f"of structs in the input, got dtype {subfield_dtype} while "
                f"resolving `{expr}`"
            )
        )
    inner_dtype = subfield_dtype.value_type
    if not isinstance(inner_dtype, pa.StructType):
        raise ValueError(
            (
                f"Expected the inner element type of `has_many` feature '{attr}' "
                f"on namespace '{parent.namespace_name}' to be a struct, got "
                f"{inner_dtype} while resolving `{expr}`"
            )
        )

    new_index_col = _index_col(len(parent.index_cols))
    new_index_cols = (*parent.index_cols, new_index_col)
    # Transient column name holding the list (and, after explode, the inner
    # struct). Chosen to not collide with `__features__` or `__value__`.
    list_col = f"__has_many_{new_index_col}__"

    # Step 1: project parent.df to (parent_index_cols, <list_col>) — the
    # __features__ column is dropped here since we only need the list field
    # for the explode.
    list_df = parent.df.project(
        {
            **{ic: parent.df.col(ic) for ic in parent.index_cols},
            list_col: feature_value_expr,
        }
    )
    # Step 2: explode the list. The column type goes from large_list[T] to T.
    exploded = list_df.explode(list_col)
    # Step 3: add the fresh index column at the new depth.
    with_id = exploded.with_unique_id(new_index_col)
    # Step 4: project to the canonical `_NamespaceRef` shape.
    new_df = with_id.project(
        {
            **{ic: with_id.col(ic) for ic in new_index_cols},
            FEATURES_COL_NAME: with_id.col(list_col),
        }
    )
    return _NamespaceRef(
        namespace_name=info.foreign_namespace,
        df=new_df,
        index_cols=new_index_cols,
    )


def _compute_item(
    expr: UnderscoreItem,
    current: _NamespaceRef,
    state: _EvalState,
) -> _Scalar | _NamespaceRef:
    """Evaluate `<receiver>[k1, k2, ...]`.

    The receiver must be a `_NamespaceRef` (typically a has_many namespace
    just entered via `_compute_attr`). Each key is classified syntactically:

    - `F.select(inner)` — `inner` is treated as the value column. Use this
      to force a non-column expression (e.g. arithmetic) to be a value.
    - Any non-`UnderscoreFunction` key (attribute chain, subscript, call) —
      treated as a value column.
    - `UnderscoreFunction` keys (comparisons, boolean ops, ...) — treated
      as row filters; their result must be boolean.

    Exactly one value key is required. All filter keys are evaluated against
    the receiver, ANDed together, and used to filter the receiver's df
    before evaluating the value.
    """
    parent = _compute(expr._chalk__parent, current, state)
    if isinstance(parent, _Windowed):
        return _select_window(parent, expr, state)
    if not isinstance(parent, _NamespaceRef):
        raise ValueError(f"Cannot subscript a scalar value `{expr._chalk__parent}` (in expression `{expr}`)")

    value_keys, filter_keys = _classify_subscript_keys(expr, expr)

    if len(value_keys) >= 2:
        raise ValueError(
            (
                f"`{expr}` must reference exactly one value column, found "
                f"{len(value_keys)}. Non-column expressions are treated as "
                f"filters; wrap a non-column expression in `F.select(...)` to "
                f"use it as the value column."
            )
        )

    filter_scalars = [_evaluate_filter(fk, parent, state, expr) for fk in filter_keys]
    filtered_parent = _apply_filters_to_namespace(parent, filter_scalars, expr)

    if len(value_keys) == 0:
        # We have begun to filter the namespace, but we have not yet selected a scalar value.
        return filtered_parent

    value = _compute(value_keys[0], filtered_parent, state)
    if not isinstance(value, _Scalar):
        raise ValueError(
            f"Subscript value key in `{expr}` must evaluate to a scalar value, got a namespace reference instead"
        )
    return value


def _unwrap_select(key: Underscore) -> Optional[Underscore]:
    """If `key` is `F.select(inner)`, return `inner`; otherwise return `None`.

    `F.select(...)` is the escape hatch to force a non-column expression to
    be treated as a value column inside `_.hm[...]`.
    """
    if not (isinstance(key, UnderscoreFunction) and key._chalk__function_name == "select"):
        return None
    if len(key._chalk__args) != 1 or key._chalk__kwargs:
        raise ValueError(f"`F.select(...)` expects exactly one positional argument (in `{key}`)")
    inner = key._chalk__args[0]
    if not isinstance(inner, Underscore):
        raise ValueError(f"`F.select(...)` requires an Underscore expression argument (in `{key}`)")
    return inner


def _is_column_key(key: Underscore) -> bool:
    """A subscript key is treated as a value column iff it is not an
    `UnderscoreFunction`. Function-call expressions are filters by default.
    """
    return not isinstance(key, UnderscoreFunction)


def _select_window(
    parent: _Windowed,
    expr: UnderscoreItem,
    state: _EvalState,
) -> _Scalar:
    """Select a single window from a `_Windowed` reference.

    Accepts one subscript key, which may be a `str` (chalk duration), a
    `timedelta`, an `int` (seconds), or the underscore expression
    `_.chalk_window`. The key is normalized to seconds and matched against
    the windowed feature's declared `windows`; the corresponding struct
    subfield is projected as the new `__value__`.
    """
    if len(expr._chalk__key) != 1:
        raise ValueError(
            f"Windowed feature selection requires exactly one subscript key, got {len(expr._chalk__key)} (in `{expr}`)"
        )
    window_str = _resolve_window_key(expr._chalk__key[0], parent.windows, state, expr)
    new_df = parent.df.project(
        {
            **{ic: parent.df.col(ic) for ic in parent.index_cols},
            VALUE_COL_NAME: parent.df.col(VALUE_COL_NAME).get_struct_subfield(window_str),
        }
    )
    return _Scalar(df=new_df, index_cols=parent.index_cols)


def _resolve_window_key(
    key: Any,
    allowed_windows: tuple[str, ...],
    state: _EvalState,
    expr: UnderscoreItem,
) -> str:
    """Resolve a subscript key to one of the `allowed_windows` strings.

    Match is by numeric equality on total seconds via `parse_chalk_duration_s`,
    so e.g. `timedelta(days=30)` matches the declared window `"30d"`.
    """
    if (
        isinstance(key, UnderscoreAttr)
        and key._chalk__attr == "chalk_window"
        and isinstance(key._chalk__parent, UnderscoreRoot)
    ):
        if state.chalk_window is None:
            raise ValueError(
                (
                    f"`_.chalk_window` was used as a windowed-feature subscript "
                    f"(in `{expr}`) but no `chalk_window` argument was passed to "
                    f"`eval_underscore(...)`"
                )
            )
        target: Union[str, timedelta, int] = state.chalk_window
    elif isinstance(key, (str, timedelta, int)):
        target = key
    else:
        raise ValueError(
            (
                f"Windowed-feature subscript key must be a string, timedelta, "
                f"int (seconds), or `_.chalk_window`; got {key!r} (in `{expr}`)"
            )
        )

    target_seconds = parse_chalk_duration_s(target)
    matching = [w for w in allowed_windows if parse_chalk_duration_s(w) == target_seconds]
    if not matching:
        raise ValueError(
            (
                f"Subscript window {key!r} ({target_seconds}s) does not match any "
                f"declared window {list(allowed_windows)} (in `{expr}`)"
            )
        )
    return matching[0]


def _evaluate_filter(
    key: Underscore,
    ns: _NamespaceRef,
    state: _EvalState,
    expr: Underscore,
) -> _Scalar:
    """Evaluate a filter key against `ns`, validating that the result is a
    scalar boolean *operation* (not a bare feature reference).

    A bare feature reference like `_.is_paid` is rejected with a hint to
    use `_.is_paid == True` instead — this matches the original parser's
    "add `== True`" message and the convention that filters are always
    explicit comparisons / boolean operations. Syntactically, an operation
    is anything whose top node is an `UnderscoreFunction` (operators, F
    function calls) or an `UnderscoreCall` (method calls like `.is_null()`
    or aggregates).
    """
    if not isinstance(key, (UnderscoreFunction, UnderscoreCall)):
        raise ValueError(
            (
                f"Cannot filter by plain feature expression `{key}` in `{expr}`; "
                f"add `== True` (or another explicit comparison / boolean operation) "
                f"to make it a valid filter."
            )
        )
    result = _compute(key, ns, state)
    if not isinstance(result, _Scalar):
        raise ValueError(
            f"Filter key `{key}` in `{expr}` must evaluate to a scalar boolean, got a namespace reference instead"
        )
    value_dtype = result.df.schema[VALUE_COL_NAME]
    if value_dtype != pa.bool_():
        raise ValueError(
            f"Filter expression `{key}` in `{expr}` must evaluate to a boolean, got dtype {value_dtype}. If you meant to compute this as a column, select it via `F.select({key})`, otherwise it will be interpreted as a filter expression in this context."
        )
    return result


def _apply_filters_to_namespace(
    parent: _NamespaceRef,
    filters: list[_Scalar],
    expr: Underscore,
) -> _NamespaceRef:
    """Return a `_NamespaceRef` whose df is `parent.df` filtered by the AND
    of all filter masks. Each filter must be a `_Scalar` at the same level
    as `parent` with a boolean value column.
    """
    if not filters:
        return parent

    for i, f in enumerate(filters):
        if f.index_cols != parent.index_cols:
            raise ValueError(f"Filter #{i} in `{expr}` has index_cols {f.index_cols!r}, expected {parent.index_cols!r}")

    # Project each filter's value into a distinct column, join into the
    # parent's df. Each filter and parent share `index_cols` so the join is
    # a 1:1 broadcast of the mask onto each row.
    filter_cols = [f"__filter_{i}__" for i in range(len(filters))]
    base_df = parent.df
    for i, f in enumerate(filters):
        renamed = f.df.project(
            {
                **{ic: f.df.col(ic) for ic in f.index_cols},
                filter_cols[i]: f.df.col(VALUE_COL_NAME),
            }
        )
        base_df = base_df.join(renamed, on=list(parent.index_cols), how="left")

    mask = base_df.col(filter_cols[0])
    for col in filter_cols[1:]:
        mask = mask & base_df.col(col)
    filtered = base_df.filter(mask)

    # Drop the transient filter columns by re-projecting to the canonical
    # `_NamespaceRef` shape.
    cleaned = filtered.project(
        {
            **{ic: filtered.col(ic) for ic in parent.index_cols},
            FEATURES_COL_NAME: filtered.col(FEATURES_COL_NAME),
        }
    )
    return _NamespaceRef(
        namespace_name=parent.namespace_name,
        df=cleaned,
        index_cols=parent.index_cols,
    )


def _compute_call(
    expr: UnderscoreCall,
    current: _NamespaceRef,
    state: _EvalState,
) -> _ComputeResult:
    """Evaluate `<receiver>.<method>(...)`. Currently only aggregate methods
    are supported."""
    method_expr = expr._chalk__parent
    if not isinstance(method_expr, UnderscoreAttr):
        raise ValueError(f"Unsupported call form: expected `<receiver>.<method>(...)`, got `{expr}`")
    fn_name = method_expr._chalk__attr
    receiver_expr = method_expr._chalk__parent

    if fn_name == "where":
        return _compute_where(
            expr=expr,
            current=current,
            state=state,
            receiver_expr=receiver_expr,
        )

    if fn_name == "alias":
        # `.alias(name)` only makes sense for naming an aggregate's output
        # column in contexts (like chalkdf `.agg(...)`) that produce
        # arbitrarily-named columns. `eval_underscore` always emits a single
        # `__value__` column, so there is nothing meaningful for the alias
        # to attach to.
        raise ValueError(
            (
                f"`.alias(...)` is not supported in eval_underscore — the result "
                f"is always a `{VALUE_COL_NAME}` column (in `{expr}`)"
            )
        )

    spec = _AGGREGATES.get(fn_name)
    if spec is not None:
        return _compute_aggregate(
            expr=expr,
            current=current,
            state=state,
            spec=spec,
            receiver_expr=receiver_expr,
        )

    # Method chaining via `chalk.functions`: `_.x.fn(args)` rewrites to
    # `F.fn(_.x, args)` when `fn` matches a function in `chalk.functions`.
    # Done lazily here so the bare `eval_underscore` import doesn't pull in
    # the whole `chalk.functions` namespace (which would risk circular
    # imports).
    rewritten = _rewrite_as_chalk_function_call(fn_name=fn_name, receiver_expr=receiver_expr, expr=expr)
    if rewritten is not None:
        return _compute(rewritten, current, state)

    raise NotImplementedError(f"Method `.{fn_name}(...)` is not yet supported in `{expr}`")


def _rewrite_as_chalk_function_call(
    *, fn_name: str, receiver_expr: Underscore, expr: UnderscoreCall
) -> Optional[Underscore]:
    """If `fn_name` matches a function exposed by `chalk.functions`, return
    the rewritten expression `F.<fn_name>(receiver_expr, *args, **kwargs)`.
    Otherwise return `None` so the caller can fall back to its default
    "unknown method" error.

    Calling `chalk.functions.<fn_name>(...)` is what produces the underlying
    `UnderscoreFunction` (or related) node — we then recurse on that node
    via the normal `_compute` dispatch.
    """
    import chalk.functions as F

    if not hasattr(F, fn_name):
        return None
    fn = getattr(F, fn_name)
    if not callable(fn):
        return None

    # A bare `_.fn(...)` call (receiver is `_`) is not a meaningful method
    # chain — match the original parser's "did you mean chalk.functions.fn"
    # error rather than silently rewriting to e.g. `F.lower(_)`.
    if isinstance(receiver_expr, UnderscoreRoot):
        raise ValueError(
            (
                f"Cannot call `_.{fn_name}(...)` directly on `_` — did you mean "
                f"`chalk.functions.{fn_name}(...)` (in `{expr}`)?"
            )
        )

    return cast(Underscore, fn(receiver_expr, *expr._chalk__args, **expr._chalk__kwargs))


def _compute_where(
    *,
    expr: UnderscoreCall,
    current: _NamespaceRef,
    state: _EvalState,
    receiver_expr: Underscore,
) -> _ComputeResult:
    """Evaluate `<receiver>.where(filter1, filter2, ...)`.

    Two receiver shapes are accepted:

    1. **Namespace receiver** — e.g. `_.has_many.where(f).count()`. Filters
       are evaluated against the namespace and combined via AND to restrict
       the rows. Returns a new `_NamespaceRef`.
    2. **Subscript receiver** — e.g. `_.has_many[value].where(f).sum()`.
       Equivalent to pushing the filter into the subscript:
       `_.has_many[value, f].sum()`. The has_many namespace is re-extracted
       from the subscript, the existing subscript filters plus the new
       `.where` filters are applied, and the subscript's value key is
       re-evaluated against the filtered namespace. Returns a `_Scalar`.
    """
    if not expr._chalk__args:
        raise ValueError(f"`.where(...)` requires at least one filter argument (in `{expr}`)")
    if expr._chalk__kwargs:
        raise ValueError(f"`.where(...)` does not accept keyword arguments (in `{expr}`)")

    for raw in expr._chalk__args:
        if not isinstance(raw, Underscore):
            raise ValueError(f"`.where(...)` argument must be an Underscore expression, got {raw!r} (in `{expr}`)")
    new_filter_exprs: list[Underscore] = list(expr._chalk__args)

    if isinstance(receiver_expr, UnderscoreItem):
        return _compute_where_on_subscript(
            expr=expr,
            current=current,
            state=state,
            subscript_expr=receiver_expr,
            new_filter_exprs=new_filter_exprs,
        )

    receiver = _compute(receiver_expr, current, state)
    if not isinstance(receiver, _NamespaceRef):
        raise ValueError(
            (
                f"`.where(...)` can only be applied to a namespace reference or a "
                f"subscript of one, got {type(receiver).__name__} (in `{expr}`)"
            )
        )

    filters = [_evaluate_filter(f, receiver, state, expr) for f in new_filter_exprs]
    return _apply_filters_to_namespace(receiver, filters, expr)


def _compute_where_on_subscript(
    *,
    expr: UnderscoreCall,
    current: _NamespaceRef,
    state: _EvalState,
    subscript_expr: UnderscoreItem,
    new_filter_exprs: list[Underscore],
) -> _Scalar:
    """`<subscript>.where(f1, f2, ...)` — push the new filters into the
    underlying has_many's filter set, re-apply the subscript's value key
    against the filtered namespace, and return the resulting `_Scalar`.
    """
    namespace = _compute(subscript_expr._chalk__parent, current, state)
    if not isinstance(namespace, _NamespaceRef):
        raise ValueError(
            (
                f"`.where(...)` on `{subscript_expr}` requires the subscript receiver "
                f"to be a namespace reference (in `{expr}`)"
            )
        )

    value_keys, existing_filter_keys = _classify_subscript_keys(subscript_expr, expr)
    if len(value_keys) != 1:
        raise ValueError(
            (
                f"`{subscript_expr}` (receiver of `.where`) must reference exactly "
                f"one value column, found {len(value_keys)}"
            )
        )

    all_filter_keys = list(existing_filter_keys) + new_filter_exprs
    filter_scalars = [_evaluate_filter(fk, namespace, state, expr) for fk in all_filter_keys]
    filtered_ns = _apply_filters_to_namespace(namespace, filter_scalars, expr)

    value = _compute(value_keys[0], filtered_ns, state)
    if not isinstance(value, _Scalar):
        raise ValueError(f"Value key in `{subscript_expr}` must evaluate to a scalar (in `{expr}`)")
    return value


def _compute_aggregate(
    *,
    expr: UnderscoreCall,
    current: _NamespaceRef,
    state: _EvalState,
    spec: _AggregateSpec,
    receiver_expr: Underscore,
) -> _Scalar:
    """Evaluate `<receiver>.<spec.name>(...)` driven by `spec`.

    Flow:
    1. Validate / classify the positional secondary args (scalar Underscores
       vs constant ints) per `spec.secondary_kinds`.
    2. Resolve the receiver and any scalar secondaries to a single "level df"
       containing the row set being aggregated plus per-row primary/secondary
       columns.
    3. Group by the parent's index cols and run the chalkdf agg.
    4. Left-join back onto the parent's index cols so empty groups appear,
       then coalesce to `spec.empty_default` if set.
    """
    classified_args = _classify_aggregate_args(spec, expr)
    has_scalar_secondaries = any(kind == "scalar" for kind, _ in classified_args)

    if has_scalar_secondaries:
        scalar_secondary_raws = [arg for kind, arg in classified_args if kind == "scalar"]
        level_df, primary_col, scalar_col_names, level_index_cols = _build_aggregate_inputs_from_subscript(
            receiver_expr=receiver_expr,
            current=current,
            state=state,
            spec=spec,
            scalar_secondary_raws=scalar_secondary_raws,
            expr=expr,
        )
    else:
        level_df, primary_col, level_index_cols = _build_aggregate_inputs_from_receiver(
            receiver_expr=receiver_expr,
            current=current,
            state=state,
            spec=spec,
            expr=expr,
        )
        scalar_col_names: list[str] = []

    if spec.needs_primary and primary_col is None:
        raise ValueError(f"Aggregate `.{spec.name}(...)` requires a primary value column (in `{expr}`)")
    if len(level_index_cols) <= len(current.index_cols):
        raise ValueError(
            (
                f"Aggregate `.{spec.name}(...)` requires the receiver to be inside "
                f"a deeper level than the current scope (in `{expr}`)"
            )
        )
    parent_index_cols = level_index_cols[:-1]

    # Build the chalkdf agg expression. When the aggregate is declared to
    # operate on a primary column (`spec.needs_primary`), it takes the form
    # `_.<primary>.<name>(<sec args>...).alias(__value__)`. Otherwise (e.g.
    # `count`) it uses the bare form `_.<name>(...)`, even if a primary
    # column happens to be present in the level df — chalkdf's `count`
    # rejects a column receiver.
    #
    # Secondary args are emitted in the declared order. Scalar operands are
    # threaded through `scalar_col_names` (also in declared order); constant
    # ints flow straight in.
    scalar_col_iter = iter(scalar_col_names)
    secondary_args: list[Any] = []
    for kind, arg in classified_args:
        if kind == "scalar":
            secondary_args.append(UnderscoreAttr(UnderscoreRoot(), next(scalar_col_iter)))
        else:  # "constant_int"
            secondary_args.append(arg)

    if spec.needs_primary:
        assert primary_col is not None  # validated above
        primary_ref = UnderscoreAttr(UnderscoreRoot(), primary_col)
        agg_call: Underscore = UnderscoreCall(UnderscoreAttr(primary_ref, spec.name), *secondary_args)
    else:
        agg_call = UnderscoreCall(UnderscoreAttr(UnderscoreRoot(), spec.name), *secondary_args)
    aliased = UnderscoreCall(UnderscoreAttr(agg_call, "alias"), VALUE_COL_NAME)

    agg_df = level_df.agg(list(parent_index_cols), aliased)

    # Left-join the agg result onto the parent's index column set so groups
    # that had zero rows (i.e. parents with empty has_many lists) still
    # appear in the output.
    parent_index_df = current.df.project({ic: current.df.col(ic) for ic in parent_index_cols})
    joined = parent_index_df.join(agg_df, on=list(parent_index_cols), how="left")

    if spec.empty_default is not None:
        # Build a typed scalar that matches the joined value column's dtype.
        # chalkdf's coalesce requires both sides to have the same arrow type,
        # so e.g. summing a `float64` requires a `float64` zero rather than a
        # plain Python `int`.
        value_dtype = joined.schema[VALUE_COL_NAME]
        typed_default = pa.scalar(spec.empty_default, type=value_dtype)
        joined = joined.fill_null({VALUE_COL_NAME: typed_default})

    return _Scalar(df=joined, index_cols=parent_index_cols)


def _classify_aggregate_args(spec: _AggregateSpec, expr: UnderscoreCall) -> list[tuple[_SecondaryKind, Any]]:
    """Validate `expr`'s positional args against `spec.secondary_kinds` and
    return them tagged with their kind, preserving declaration order.

    The tuples are `("scalar", Underscore)` or `("constant_int", int)`.
    Returning them in order matters because the agg expression is built by
    iterating through this list — re-merging two split lists would only
    work if scalars always preceded constants.
    """
    if len(expr._chalk__args) != len(spec.secondary_kinds):
        raise ValueError(
            (
                f"`.{spec.name}(...)` expects {len(spec.secondary_kinds)} positional "
                f"argument(s), got {len(expr._chalk__args)} (in `{expr}`)"
            )
        )
    if expr._chalk__kwargs:
        raise ValueError(f"`.{spec.name}(...)` does not accept keyword arguments (in `{expr}`)")

    classified: list[tuple[_SecondaryKind, Any]] = []
    for arg, kind in zip(expr._chalk__args, spec.secondary_kinds):
        if kind == "scalar":
            if not isinstance(arg, Underscore):
                raise ValueError(
                    (
                        f"`.{spec.name}(...)` argument must be an Underscore "
                        f"expression (kind='scalar'), got {arg!r} (in `{expr}`)"
                    )
                )
            classified.append(("scalar", arg))
        elif kind == "constant_int":
            # `bool` is a subclass of `int` in Python — reject it explicitly so
            # e.g. `.max_by_n(_.ts, True)` doesn't sneak through as `n=1`.
            if not isinstance(arg, int) or isinstance(arg, bool):
                raise ValueError(
                    (
                        f"`.{spec.name}(...)` argument must be a constant int "
                        f"(kind='constant_int'), got {arg!r} (in `{expr}`)"
                    )
                )
            classified.append(("constant_int", arg))
        else:  # pragma: no cover  -- exhaustive over _SecondaryKind
            raise AssertionError(f"unknown secondary kind {kind!r}")
    return classified


def _build_aggregate_inputs_from_receiver(
    *,
    receiver_expr: Underscore,
    current: _NamespaceRef,
    state: _EvalState,
    spec: _AggregateSpec,
    expr: UnderscoreCall,
) -> tuple["DataFrame", Optional[str], tuple[str, ...]]:
    """Used when an aggregate has no scalar secondaries.

    The receiver is computed normally; if it's a `_Scalar`, its `__value__`
    is the primary column. If it's a `_NamespaceRef`, we have no primary
    column (only valid when `spec.needs_primary=False`, e.g. `_.hm.count()`).
    """
    receiver = _compute(receiver_expr, current, state)
    if isinstance(receiver, _NamespaceRef):
        return receiver.df, None, receiver.index_cols
    if isinstance(receiver, _Scalar):
        return receiver.df, VALUE_COL_NAME, receiver.index_cols
    raise ValueError(
        f"Aggregate `.{spec.name}(...)` got unsupported receiver kind {type(receiver).__name__} (in `{expr}`)"
    )


def _build_aggregate_inputs_from_subscript(
    *,
    receiver_expr: Underscore,
    current: _NamespaceRef,
    state: _EvalState,
    spec: _AggregateSpec,
    scalar_secondary_raws: list[Underscore],
    expr: UnderscoreCall,
) -> tuple["DataFrame", Optional[str], list[str], tuple[str, ...]]:
    """Used when an aggregate has scalar secondary args (e.g. `.max_by(by)`).

    The receiver must be a subscript on a has_many — that's the only way to
    get a well-defined namespace in which to evaluate the secondary
    expressions. We re-parse the subscript's keys here (using the same
    column-vs-filter classification as `_compute_item`) so the secondaries
    see the same filtered scope as the value column.
    """
    if not isinstance(receiver_expr, UnderscoreItem):
        raise ValueError(
            (
                f"`.{spec.name}(...)` requires a subscript receiver of the form "
                f"`_.has_many[value_col].{spec.name}(...)` so the secondary "
                f"expressions can be evaluated in the same has_many namespace as "
                f"the value (in `{expr}`)"
            )
        )

    namespace = _compute(receiver_expr._chalk__parent, current, state)
    if not isinstance(namespace, _NamespaceRef):
        raise ValueError(f"`.{spec.name}(...)` subscript receiver must resolve to a namespace reference (in `{expr}`)")

    value_keys, filter_keys = _classify_subscript_keys(receiver_expr, expr)
    if spec.needs_primary and len(value_keys) != 1:
        raise ValueError(
            (
                f"`{receiver_expr}` (receiver of `.{spec.name}`) must reference "
                f"exactly one value column, found {len(value_keys)}"
            )
        )

    filter_scalars = [_evaluate_filter(fk, namespace, state, expr) for fk in filter_keys]
    filtered_ns = _apply_filters_to_namespace(namespace, filter_scalars, expr)
    level_index_cols = filtered_ns.index_cols

    primary_scalar: Optional[_Scalar] = None
    if spec.needs_primary:
        result = _compute(value_keys[0], filtered_ns, state)
        if not isinstance(result, _Scalar):
            raise ValueError(
                f"Value key `{value_keys[0]}` in `{receiver_expr}` must evaluate to a scalar (in `{expr}`)"
            )
        primary_scalar = result

    secondary_scalars: list[_Scalar] = []
    for s_raw in scalar_secondary_raws:
        s = _compute(s_raw, filtered_ns, state)
        if not isinstance(s, _Scalar):
            raise ValueError(
                f"`.{spec.name}(...)` secondary expression `{s_raw}` must evaluate to a scalar (in `{expr}`)"
            )
        secondary_scalars.append(s)

    # Project the namespace's index cols as the base of the level df, then
    # join each primary/secondary scalar in under a distinct column name.
    primary_col_name = "__agg_primary__"
    secondary_col_names = [f"__agg_sec_{i}__" for i in range(len(secondary_scalars))]

    level_df = filtered_ns.df.project({ic: filtered_ns.df.col(ic) for ic in level_index_cols})
    if primary_scalar is not None:
        renamed = primary_scalar.df.project(
            {
                **{ic: primary_scalar.df.col(ic) for ic in primary_scalar.index_cols},
                primary_col_name: primary_scalar.df.col(VALUE_COL_NAME),
            }
        )
        level_df = level_df.join(renamed, on=list(level_index_cols), how="left")
    for i, s in enumerate(secondary_scalars):
        renamed = s.df.project(
            {
                **{ic: s.df.col(ic) for ic in s.index_cols},
                secondary_col_names[i]: s.df.col(VALUE_COL_NAME),
            }
        )
        level_df = level_df.join(renamed, on=list(level_index_cols), how="left")

    primary_col = primary_col_name if primary_scalar is not None else None
    return level_df, primary_col, secondary_col_names, level_index_cols


def _classify_subscript_keys(item: UnderscoreItem, expr: Underscore) -> tuple[list[Underscore], list[Underscore]]:
    """Split `item._chalk__key` into (value_keys, filter_keys) using the same
    classification as `_compute_item` (`F.select(...)` and non-`UnderscoreFunction`
    keys are values; `UnderscoreFunction` keys are filters)."""
    value_keys: list[Underscore] = []
    filter_keys: list[Underscore] = []
    for raw_key in item._chalk__key:
        if not isinstance(raw_key, Underscore):
            raise ValueError(
                f"Subscript key in `{item}` must be an Underscore expression, got {raw_key!r} (in `{expr}`)"
            )
        unwrapped = _unwrap_select(raw_key)
        if unwrapped is not None:
            value_keys.append(unwrapped)
        elif _is_column_key(raw_key):
            value_keys.append(raw_key)
        else:
            filter_keys.append(raw_key)
    return value_keys, filter_keys


def _compute_function(
    expr: UnderscoreFunction,
    current: _NamespaceRef,
    state: _EvalState,
) -> _Scalar:
    """Evaluate a scalar function call.

    Each Underscore operand is recursively computed to a `_Scalar`. We then
    join all those `_Scalar` DataFrames on their shared index-col prefix —
    each operand's `__value__` is first projected into a unique `__arg_N__`
    column to avoid collisions — and project the function call as the new
    `__value__` against the joined DataFrame.
    """
    if expr._chalk__function_name in ("lambda", "lambda_parameter"):
        # `F.lambda(...)` / `F.lambda_parameter(...)` are pseudo-functions
        # the parser uses to encode lambda bodies and their parameters
        # (with deferred type inference). Supporting them would require
        # tracking a per-lambda local scope and a separate evaluation
        # context for the lambda body, which we don't yet model.
        raise NotImplementedError(
            f"Lambda forms (`F.{expr._chalk__function_name}(...)`) are not supported in eval_underscore (in `{expr}`)"
        )

    computed_args: list[_FunctionOperand] = [
        _compute_function_operand(
            raw,
            current,
            state,
            label=f"argument #{i}",
            fn_name=expr._chalk__function_name,
        )
        for i, raw in enumerate(expr._chalk__args)
    ]
    computed_kwargs: dict[str, _FunctionOperand] = {
        k: _compute_function_operand(
            v,
            current,
            state,
            label=f"keyword argument `{k}`",
            fn_name=expr._chalk__function_name,
        )
        for k, v in expr._chalk__kwargs.items()
    }

    scalar_operands: list[_Scalar] = [
        op for op in (*computed_args, *computed_kwargs.values()) if isinstance(op, _Scalar)
    ]

    if scalar_operands:
        joined_df, scalar_col_names, joined_index_cols = _join_scalars(scalar_operands)
    else:
        # No Underscore operands — the function value depends only on
        # literals. Evaluate against `current.df` so the result has the
        # level's index shape (literals broadcast to one value per row at
        # this level).
        joined_df = current.df.project({ic: current.df.col(ic) for ic in current.index_cols})
        scalar_col_names: list[str] = []
        joined_index_cols = current.index_cols

    # Map each computed operand back to either a column reference on the
    # joined DataFrame (for scalars) or its literal value. `scalar_col_names`
    # is ordered to match the iteration order over `scalar_operands` above.
    scalar_iter = iter(scalar_col_names)

    def _resolve(op: _FunctionOperand) -> Any:
        if isinstance(op, _Scalar):
            return joined_df.col(next(scalar_iter))
        return op.value

    chalkdf_args = [_resolve(op) for op in computed_args]
    chalkdf_kwargs = {k: _resolve(op) for k, op in computed_kwargs.items()}

    func_expr = UnderscoreFunction(
        expr._chalk__function_name,
        *chalkdf_args,
        **chalkdf_kwargs,
    )
    new_df = joined_df.project(
        {
            **{ic: joined_df.col(ic) for ic in joined_index_cols},
            VALUE_COL_NAME: func_expr,
        }
    )
    return _Scalar(df=new_df, index_cols=joined_index_cols)


def _compute_function_operand(
    raw: Any,
    current: _NamespaceRef,
    state: _EvalState,
    *,
    label: str,
    fn_name: str,
) -> _FunctionOperand:
    """Compute one operand of a scalar function.

    Returns a `_Scalar` for `Underscore` operands and a `_Literal` wrapper
    for plain Python values. Raises if an Underscore operand resolves to a
    `_NamespaceRef` (never a valid scalar argument).
    """
    if not isinstance(raw, Underscore):
        return _Literal(value=raw)
    result = _compute(raw, current, state)
    if not isinstance(result, _Scalar):
        raise ValueError(
            f"{label} of `{fn_name}` (`{raw}`) must evaluate to a scalar value, got a namespace reference instead"
        )
    return result


def _join_scalars(
    scalars: list[_Scalar],
) -> tuple["DataFrame", list[str], tuple[str, ...]]:
    """Join the given `_Scalar` DataFrames on their shared index-col prefix.

    All inputs must have `index_cols` that form a chain — each scalar's
    `index_cols` must be a prefix of (or equal to) the widest scalar's. The
    output `index_cols` matches the widest input.

    Returns `(joined_df, value_col_per_scalar, joined_index_cols)` where:

    - `joined_df` has columns `[*joined_index_cols, __arg_0__, __arg_1__, ...]`
      — one renamed value column per input scalar, in input order.
    - `value_col_per_scalar[i]` is the column name in `joined_df` holding
      `scalars[i]`'s value.
    - `joined_index_cols` equals the widest input's `index_cols`.

    Narrower-index scalars are left-joined onto the widest, so missing
    matches are filled with NULL rather than dropping rows.
    """
    assert len(scalars) > 0, "_join_scalars called with no scalars"

    widest_idx = max(range(len(scalars)), key=lambda i: len(scalars[i].index_cols))
    joined_index_cols = scalars[widest_idx].index_cols

    for i, s in enumerate(scalars):
        if joined_index_cols[: len(s.index_cols)] != s.index_cols:
            raise ValueError(
                (
                    f"Cannot combine scalar operands with incompatible index "
                    f"columns: operand #{i} has {s.index_cols!r}, expected a "
                    f"prefix of {joined_index_cols!r}"
                )
            )

    value_col_per_scalar = [f"__arg_{i}__" for i in range(len(scalars))]

    # Project each scalar's df to rename `__value__` -> `__arg_N__`. Using
    # `project` explicitly (rather than `df.rename`) keeps every intermediate
    # operation a `project` or `join` for easier plan inspection.
    def _rename_value_to_arg(s: _Scalar, new_value_col: str) -> "DataFrame":
        return s.df.project(
            {
                **{ic: s.df.col(ic) for ic in s.index_cols},
                new_value_col: s.df.col(VALUE_COL_NAME),
            }
        )

    joined_df = _rename_value_to_arg(scalars[widest_idx], value_col_per_scalar[widest_idx])
    for i, s in enumerate(scalars):
        if i == widest_idx:
            continue
        right_df = _rename_value_to_arg(s, value_col_per_scalar[i])
        joined_df = joined_df.join(right_df, on=list(s.index_cols), how="left")

    return joined_df, value_col_per_scalar, joined_index_cols
