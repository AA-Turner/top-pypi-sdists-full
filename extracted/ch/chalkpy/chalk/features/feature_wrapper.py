from __future__ import annotations

import copy
import dataclasses
import inspect
from collections.abc import Iterable
from typing import Any, Literal, TypeVar, Union, TYPE_CHECKING, Callable, overload

from chalk._lsp.error_builder import LSPErrorBuilder
from chalk.features._chalkop import op, Aggregation
from chalk.features.filter import Filter
from chalk.serialization.parsed_annotation import ParsedAnnotation
from chalk.utils.collections import ensure_tuple
from chalk.utils.notebook import is_notebook

if TYPE_CHECKING:
    from chalk.features.feature_field import Feature
    from chalk.features.dataframe import DataFrame
    from chalk.features.underscore import Underscore

T = TypeVar("T")

class NearestNeighborException(ValueError):
    ...


class UnresolvedFeature:
    """Fallback for features that can't be resolved in notebook environments.

    This allows notebooks to work even when the feature registry is stale or incomplete.
    The server will validate the feature exists when the query is executed.
    """
    __slots__ = ("fqn",)

    def __init__(self, fqn: str):
        self.fqn = fqn
        super().__init__()

    def __str__(self):
        return self.fqn

    def __repr__(self):
        return f"UnresolvedFeature({self.fqn!r})"

    def __hash__(self):
        return hash(self.fqn)

    def __eq__(self, other: object):
        if isinstance(other, UnresolvedFeature):
            return self.fqn == other.fqn
        return False


class _MarkedUnderlyingFeature:
    __slots__ = ("_fn", "_source", "_debug_info")

    def __init__(self, fn: Callable[[], Feature | Filter | type[DataFrame] | FeatureWrapper | Aggregation | UnresolvedFeature],
                 debug_info: Any = None) -> None:
        super().__init__()
        self._fn = fn
        self._debug_info = debug_info

    def __call__(self, *args: Any, **kwds: Any) -> Feature | Filter | type[DataFrame] | FeatureWrapper | Aggregation | UnresolvedFeature:
        return self._fn()


class FeatureWrapper:
    """
    FeatureWrapper emulates DataFrames and
    nested has-one relationships when used
    as a type annotation or within a filter.
    """

    def __init__(
        self, underlying: (
            _MarkedUnderlyingFeature |
            Feature | Filter | type[DataFrame] | FeatureWrapper | Aggregation
        )
    ):
        super().__init__()
        self._chalk_underlying = underlying

    def _chalk_get_underlying(self) -> Feature | Aggregation | Filter | type[DataFrame] | UnresolvedFeature:
        if isinstance(self._chalk_underlying, _MarkedUnderlyingFeature):
            self._chalk_underlying = self._chalk_underlying()
        if isinstance(self._chalk_underlying, FeatureWrapper):
            self._chalk_underlying = unwrap_feature(self._chalk_underlying)
        return self._chalk_underlying

    @property
    def auxiliary_namespace(self) -> str | None:
        """Namespace of the auxiliary class that contributed this feature, if any."""
        from chalk.features.feature_field import Feature
        underlying = self._chalk_get_underlying()
        return underlying.auxiliary_namespace if isinstance(underlying, Feature) else None

    @property
    def auxiliary_filename(self) -> str | None:
        """Source file of the auxiliary class that contributed this feature, if any."""
        from chalk.features.feature_field import Feature
        underlying = self._chalk_get_underlying()
        return underlying.auxiliary_filename if isinstance(underlying, Feature) else None

    def _chalk_do_add(self, other: object):
        from chalk.features.feature_field import Feature
        f_self = unwrap_feature(self, raise_error=False)

        if isinstance(other, (FeatureWrapper, Feature)):

            f_other = unwrap_feature(other)
            if f_other.is_scalar and f_self.is_scalar:
                if str == f_other.converter.rich_type == f_self.converter.rich_type:
                    return op.concat_str(self, other)
                else:
                    return op.sum(self, other)
            else:
                raise TypeError("Only scalar features can be added together")
        # handle literal numerical add
        return op.sum(f_self, other)

    def __radd__(self, other: object):
        return FeatureWrapper(_MarkedUnderlyingFeature(lambda: self._chalk_do_add(other), ("__radd__", other)))

    def __add__(self, other: object):
        return FeatureWrapper(_MarkedUnderlyingFeature(lambda: self._chalk_do_add(other), ("__add__", other)))

    def __matmul__(self, other: int):
        from chalk.features.feature_field import Feature

        def f():
            underlying = self._chalk_get_underlying()
            if not isinstance(underlying, Feature):
                raise TypeError(f"Only features can be used with version. {underlying} is not a feature")
            return underlying.for_version(other)

        return FeatureWrapper(_MarkedUnderlyingFeature(f, ("__matmul__", other)))

    def __hash__(self):
        frame = inspect.currentframe()
        if frame and frame.f_back and frame.f_back.f_globals["__name__"] in ("typing", "typing_extensions"):
            return 0
        del frame
        return hash(self._chalk_get_underlying())

    def __gt__(self, other: object):
        return Filter(self, ">", other)

    def __ge__(self, other: object):
        return Filter(self, ">=", other)

    def __lt__(self, other: object):
        return Filter(self, "<", other)

    def __le__(self, other: object):
        return Filter(self, "<=", other)

    # len_registry: ClassVar[dict[int, FeatureWrapper]] = {}
    #
    # def __len__(self):
    #     r = randint(0, 100_000_000_000_000)
    #     self.len_registry[r] = self
    #     return r

    def _cmp(self, op: str, other: object):
        from chalk.features.feature_field import Feature

        if other == "interval" and op == "==":
            # Pandas compares everything against interval. If we return a FeatureWrapper in this case,
            # then it will fail
            return NotImplemented

        if isinstance(other, Feature):
            # If comparing against a feature directly, then we know it's not being used in a join condition
            # Since join conditions would be against another FeatureWrapper or a literal value
            is_eq = self._chalk_get_underlying() == other
            # They are the same feature. Short-circuit and return a boolean
            if op == "==" and is_eq:
                return True
            if op == "!=" and not is_eq:
                return False
            return NotImplemented  # GT / LT doesn't really make sense otherwise
        if isinstance(other, type):
            return NotImplemented
        return Filter(self, op, other)

    def __ne__(self, other: object):
        return self._cmp("!=", other)

    def __eq__(self, other: object):
        if hasattr(other, "__module__") and other.__module__ in ("typing", "typing_extensions"):
            return False
        return self._cmp("==", other)

    def __and__(self, other: object):
        return self._cmp("and", other)

    def __or__(self, other: object):
        if other is None:
            other = type(None)
        if isinstance(other, type):
            # The FeatureWrapper appears as a UnionType in a type annotation -- e.g.
            # def my_resolver(name: User.name | None = None, ...)
            return Union[other, self]
        return self._cmp("or", other)

    def __str__(self):
        return str(self._chalk_get_underlying())

    def in_(self, examples: Iterable):
        return self._cmp("in", examples)

    def __call__(self, *args: Any, **kwargs: Any):
        # Using a generic signature since this signature must support all types of features
        # Currently, though, only windowed features are callable
        from chalk.features import Feature

        def f() -> FeatureWrapper:
            underlying = self._chalk_get_underlying()
            if not isinstance(underlying, Feature):
                return underlying(*args, **kwargs)  # pyright: ignore -- we want this to raise
            if underlying.is_windowed:
                return self._chalk_get_windowed_feature(*args, **kwargs)
            raise TypeError(f"Feature {self} is not callable")

        return FeatureWrapper(_MarkedUnderlyingFeature(f, ("__call__", args, kwargs)))

    def _chalk_get_windowed_feature(self, window: Union[str, int]) -> FeatureWrapper:
        if not isinstance(window, (str, int)):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("Window duration must be a string or an int")

        from chalk.features import Feature
        from chalk.features.feature_set import CURRENT_FEATURE_REGISTRY
        from chalk.streams import get_name_with_duration

        underlying_feature = self._chalk_get_underlying()
        if not isinstance(underlying_feature, Feature):
            raise TypeError(f"Cannot get the windowed feature for {underlying_feature}, which is not a feature.")

        registry = CURRENT_FEATURE_REGISTRY.get().get_feature_sets()
        parent = (
            registry[underlying_feature.namespace]
            if len(underlying_feature.path) == 0
            else FeatureWrapper(underlying_feature.path[-1].parent)
        )
        desired_attribute_name = get_name_with_duration(underlying_feature.attribute_name, window)
        if not hasattr(parent, desired_attribute_name):
            formatted_window_durations = [f"'{x}s'" for x in underlying_feature.window_durations]
            raise TypeError(
                (
                    f"Unsupported window duration '{window}' for '{underlying_feature.root_fqn}'. "
                    f"Durations {', '.join(formatted_window_durations)} are supported."
                )
            )
        return getattr(parent, desired_attribute_name)

    def __getitem__(self, item: Any):
        from chalk.df.ast_parser import parse_feature_iter

        if isinstance(item, int):
            if item == 0:
                return FeatureWrapper(parse_feature_iter(self))
            else:
                raise StopIteration(f"Cannot subscript feature '{self}' past 0. Attempting to subscript with '{item}'")

        def f():
            from chalk.features.feature_field import get_distance_feature_name, Feature
            from chalk.features.pseudofeatures import Distance
            from chalk.features.feature_set import CURRENT_FEATURE_REGISTRY
            registry = CURRENT_FEATURE_REGISTRY.get()
            underlying = self._chalk_get_underlying()
            if not isinstance(underlying, Feature):
                return underlying[item]  # pyright: ignore -- we want to pass through if the underlying isn't a feature
            if len(underlying.window_durations) > 0:
                return self._chalk_get_windowed_feature(*ensure_tuple(item))

            dataframe_typ = underlying.typ.as_dataframe()
            if dataframe_typ is not None:
                dataframe_item = list(ensure_tuple(item))
                for i, x in enumerate(dataframe_item):
                    if x is Distance:
                        # If requesting a distance, we need to replace it with the distance pseudofeature
                        filter = underlying.join
                        if filter is None:
                            raise ValueError("The `Distance` feature can only be used with has-many relationship")
                        if not filter.operation.startswith("is_near_"):
                            raise ValueError("The `Distance` feature can only be used with a nearest neighbor join")
                        assert isinstance(filter.lhs, Feature)
                        assert isinstance(filter.rhs, Feature)
                        local_feature = filter.lhs if filter.lhs.namespace == underlying.namespace else filter.rhs
                        foreign_feature = (
                            filter.lhs if filter.lhs.namespace != underlying.namespace else filter.rhs
                        )
                        assert local_feature != foreign_feature, "The local and foreign features must be different"
                        key = get_distance_feature_name(
                            local_namespace=local_feature.namespace,
                            local_name=local_feature.name,
                            local_hm_name=underlying.name,
                            op=filter.operation,
                            foreign_name=foreign_feature.name,
                        )
                        feature_fields = registry.get_feature_sets()[foreign_feature.namespace].features
                        x = next(f for f in feature_fields if f.name == key)
                        dataframe_item[i] = x
                tuple_item = tuple(dataframe_item)

                f_copy_underlying = copy.copy(underlying)
                f_copy_underlying.typ = ParsedAnnotation(underlying=dataframe_typ[tuple_item])
                # `Feature.converter` prefers the cached converter and `underlying` (set when the
                # feature is reached through a has-one path) over the narrowed annotation, so both
                # must be rebuilt for the copy.
                f_copy_underlying._converter = None  # pyright: ignore[reportPrivateUsage]
                if f_copy_underlying.underlying is not None:
                    underlying_copy = copy.copy(f_copy_underlying.underlying)
                    underlying_copy.typ = f_copy_underlying.typ
                    underlying_copy._converter = None  # pyright: ignore[reportPrivateUsage]
                    f_copy_underlying.underlying = underlying_copy
                if len(f_copy_underlying.path) > 0:
                    path_copy = list(f_copy_underlying.path)
                    path_copy[-1] = dataclasses.replace(path_copy[-1], child=f_copy_underlying)
                    f_copy_underlying.path = tuple(path_copy)

                return FeatureWrapper(f_copy_underlying)
            item_features_maybe = []
            if isinstance(item, Iterable):
                for i in item:
                    try:
                        item_features_maybe.append(unwrap_feature(i).fqn)
                    except:
                        break
            raise TypeError(f"Feature '{self}' of type {underlying.typ} does not support subscripting. Attempted to subscript with '{item_features_maybe or item}'")

        return FeatureWrapper(_MarkedUnderlyingFeature(f, ("__getitem__", item)))

    def __getattr__(self, item: str):

        # Passing through __getattr__ on has_one features, as users can use getattr
        # notation in annotations for resolvers
        if item.startswith("__") and not item.startswith("__chalk"):
            # Short-circuiting on the dunders to be compatible with copy.copy
            raise AttributeError(item)
        LSPErrorBuilder.save_node(self, item)
        return self._chalk_get_attribute(item)

    def _chalk_get_attribute(self, item: str) -> FeatureWrapper:
        """The feature `item` of this has-one or has-many's feature class, resolved lazily. The caller records the
        user's source node with `LSPErrorBuilder.save_node`, so that resolution errors point at the user's code."""

        def fn():
            from chalk.features.feature_field import Feature
            underlying = self._chalk_get_underlying()
            if not isinstance(underlying, Feature):
                return getattr(underlying, item)
            joined_class = underlying.joined_class
            if joined_class is None:
                underlying_df = underlying.typ.as_dataframe()
                joined_class = underlying_df.references_feature_set if underlying_df is not None else None

            if joined_class is not None:
                for f in joined_class.features:
                    assert isinstance(f, Feature), f"HasOne feature {f} does not inherit from FeaturesBase"
                    if f.attribute_name == item:
                        return FeatureWrapper(underlying.copy_with_path(f))

                if is_notebook():
                    # Construct FQN by preserving the path from the underlying feature
                    # If underlying has a path, we need to include it in the FQN
                    fqn = f"{underlying.root_fqn}.{item}"
                    return UnresolvedFeature(fqn)

                assert underlying.features_cls is not None
                underlying.features_cls.__chalk_error_builder__.invalid_attribute(
                    root_feature_str=joined_class.namespace,
                    root_is_feature_class=True,
                    item=item,
                    candidates=[f.name for f in joined_class.features],
                    back=1,
                    saved_frame=self
                )
                assert False, "unreachable"

            # If in notebook, fallback to constructing FQN string instead of raising error
            if is_notebook():
                fqn = f"{underlying.fqn}.{item}"
                return UnresolvedFeature(fqn)

            assert underlying.features_cls is not None
            underlying.features_cls.__chalk_error_builder__.invalid_attribute(
                root_feature_str=underlying.fqn,
                root_is_feature_class=False,
                item=item,
                candidates=[],
                back=1,
                saved_frame=self,
            )
            assert False, "unreachable"
        return FeatureWrapper(_MarkedUnderlyingFeature(fn, ("__getattr__", item)))

    @property
    def alias(self) -> _AliasAttribute:
        """Return this feature as a query output column with a different name.

        Supported for scalar features, including scalars reached through has-one
        relationships, in `NamedQuery(output=...)` and in the `output` of online
        queries. The aliased column is an output expression that references the
        feature, so the feature itself is still computed, persisted, and logged
        under its own name.

        Parameters
        ----------
        name
            The column name the query returns this feature under. It may not
            contain a `.`, so it can never be mistaken for a feature name.

        Examples
        --------
        >>> from chalk import NamedQuery
        >>> NamedQuery(
        ...     name="user_txns",
        ...     input=[User.id],
        ...     output=[User.transaction_count["1d"].alias("tc_1d")],
        ... )

        A related feature class's own feature named `alias` stays reachable:
        `User.profile.alias` is that feature wherever a feature is expected.
        """
        # Recorded here, not in `_chalk_get_attribute`, so that `save_node` finds the user's frame.
        LSPErrorBuilder.save_node(self, "alias")
        return _AliasAttribute(self)

    def is_near(self, item: Any, metric: Literal["l2", "cos", "ip"] = "l2") -> Filter:
        if metric not in ("l2", "cos", "ip"):
            raise NearestNeighborException(f"Invalid metric '{metric}'. Must be one of 'l2', 'cos', or 'ip'.")
        from chalk.features import Feature
        other = unwrap_feature(item)
        underlying = self._chalk_get_underlying()
        if not isinstance(underlying, Feature):
            raise NearestNeighborException(f"Feature.is_near() is only supported on features. {underlying} is not a feature.")
        self_vector = underlying.typ.as_vector()
        if self_vector is None:
            raise NearestNeighborException(
                f"Nearest neighbor relationships are only supported for vector features. Feature '{underlying.root_fqn}' is not a vector."
            )
        other_vector = other.typ.as_vector()
        if other_vector is None:
            raise NearestNeighborException(
                f"Nearest neighbor relationships are only supported for vector features. Feature '{other.root_fqn}' is not a vector."
            )
        if underlying.converter.pyarrow_dtype != other.converter.pyarrow_dtype:
            raise NearestNeighborException(
                (
                    f"Nearest neighbor relationships are only supported if both vectors have the same data type and dimensions. "
                    f"Feature '{underlying.root_fqn}' is of type `{underlying.converter.pyarrow_dtype}` "
                    f" while feature '{other.root_fqn}' is `{other.converter.pyarrow_dtype}`."
                )
            )
        return Filter(underlying, f"is_near_{metric}", other)


class _AliasAttribute(FeatureWrapper):
    """`FeatureWrapper.alias`: called with a column name, it aliases the parent feature. Anywhere else, it is the
    parent relationship's feature named `alias`, resolved lazily as `__getattr__` would."""

    def __init__(self, parent: FeatureWrapper):
        super().__init__(parent._chalk_get_attribute("alias"))  # pyright: ignore[reportPrivateUsage]
        self._chalk_alias_parent = parent

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        # Calling a related feature named `alias` (to choose a window) keeps working; this check runs only at call
        # time, after the feature classes exist.
        if _has_related_feature(self._chalk_alias_parent, "alias"):
            return super().__call__(*args, **kwargs)
        return AliasedFeature(self._chalk_alias_parent, *args, **kwargs)


def _has_related_feature(wrapper: FeatureWrapper, attribute_name: str) -> bool:
    """Whether `wrapper` is a has-one or has-many whose feature class has a feature with this attribute name."""
    from chalk.features.feature_field import Feature

    try:
        underlying = wrapper._chalk_get_underlying()  # pyright: ignore[reportPrivateUsage]
        if not isinstance(underlying, Feature):
            return False
        joined_class = underlying.joined_class
        if joined_class is None:
            underlying_df = underlying.typ.as_dataframe()
            joined_class = underlying_df.references_feature_set if underlying_df is not None else None
    except Exception:
        # An unresolvable parent cannot have the feature; `AliasedFeature.resolve` reports the parent's error.
        return False
    return joined_class is not None and any(f.attribute_name == attribute_name for f in joined_class.features)


class AliasedFeature:
    """A feature paired with the column name a query returns it under.

    Created by `FeatureWrapper.alias`. It is deliberately not a `FeatureWrapper`:
    anything other than a query output that receives one fails loudly instead of
    silently dropping the alias.
    """

    __slots__ = ("feature", "name")

    def __init__(self, feature: FeatureWrapper, name: str):
        super().__init__()
        validate_output_column_name(name)
        self.feature = feature
        self.name = name

    def resolve(self) -> Feature:
        """Resolve the aliased feature, which must be returned as exactly one scalar column."""
        f = unwrap_feature(self.feature)
        if not f.is_scalar:
            raise TypeError(f"Cannot alias '{f.root_fqn}': only scalar features can be aliased.")
        if f.is_windowed:
            raise TypeError(
                f"Cannot alias windowed feature '{f.root_fqn}' without choosing a window: it expands to one "
                + f"column per window. Alias a specific window instead, e.g. `<Feature>['1d'].alias({self.name!r})`."
            )
        return f

    def to_underscore(self) -> Underscore:
        """The underscore expression, rooted at the feature's root namespace, that references the feature."""
        from chalk.features.feature_field import parse_versioned_name
        from chalk.features.underscore import UnderscoreAttr, UnderscoreRoot

        f = self.resolve()
        expr: Underscore = UnderscoreRoot()
        # Attribute names are the segments of the feature's root fqn after the namespace. A `name@N`
        # segment is a pinned version, which underscore attributes carry separately.
        for segment in (*(p.parent.name for p in f.path), f.name):
            attr, version = parse_versioned_name(segment)
            expr = UnderscoreAttr(expr, attr, version=version)
        return expr

    def __repr__(self):
        return f"AliasedFeature({self.feature!r}, {self.name!r})"


def validate_output_column_name(name: str) -> None:
    """Validate a column name that a query output expression is returned under."""
    if not isinstance(name, str) or name == "":  # pyright: ignore[reportUnnecessaryIsInstance]
        raise ValueError(f"Output column name must be a non-empty string, got {name!r}")
    if "." in name:
        raise ValueError(f"Output column name {name!r} may not contain '.', which is reserved for feature names")


@overload
def unwrap_feature(maybe_feature_wrapper: Any, raise_error: Literal[True] = ...) -> Feature:
    ...


@overload
def unwrap_feature(maybe_feature_wrapper: Any, raise_error: Literal[False]) -> Any:
    ...


def unwrap_feature(maybe_feature_wrapper: Any, raise_error: bool = True) -> Feature | Any:
    """Unwrap a class-annotated FeatureWrapper instance into the underlying feature.

    For example:

        @features
        class FooBar:
            foo: str
            bar: int

        type(FooBar.foo) is FeatureWrapper
        type(unwrap_feature(FooBar.foo)) is Feature
    """
    from chalk.features.feature_field import Feature

    if isinstance(maybe_feature_wrapper, str):
        return Feature.from_root_fqn(maybe_feature_wrapper)
    if isinstance(maybe_feature_wrapper, FeatureWrapper):
        maybe_feature_wrapper = maybe_feature_wrapper._chalk_get_underlying()  # pyright: ignore[reportPrivateUsage]
    if isinstance(maybe_feature_wrapper, Feature):
        return maybe_feature_wrapper
    if raise_error:
        raise TypeError(
            f"{maybe_feature_wrapper} is of type {type(maybe_feature_wrapper).__name__}, expecting type FeatureWrapper"
        )
    else:
        return maybe_feature_wrapper


def feature_to_query_str(feature: Union[str, Feature, FeatureWrapper, Any]) -> str:
    """Serialize a feature reference the way query inputs/outputs and resolver specs expect.

    Behaves like ``str(feature)`` (the feature's root fqn), except that a *projected* has-many --
    e.g. ``User.transactions[Transaction.id, Transaction.amount]`` -- renders its selected
    sub-features as ``user.transactions[transaction.id,transaction.amount]`` (full sub-fqns,
    comma-separated, no spaces), recursing for has-manys nested inside the projection. A bare
    has-many (``DataFrame[Transaction]``) renders as just its fqn, meaning "all columns".

    ``str(feature)`` itself intentionally stays the plain root fqn: it doubles as a DataFrame column
    key in runtime Python resolvers, so it must not carry the ``[...]`` projection. This helper is
    the query/resolver-spec-facing serialization.
    """
    from chalk.features.feature_field import Feature

    if isinstance(feature, str):
        # A string is already the serialized form and passes through verbatim, matching the
        # pre-projection `str()` behavior: the server is the sole authority on what a string
        # reference means (bracketed projections, `@version` suffixes, namespace outputs,
        # graphs newer than this client), and it validates NamedQuery references loudly at
        # deploy-time preplanning. Resolving here would force chalkpy to replicate the
        # server's resolution rules and reject previously-valid strings whenever they drift.
        return feature
    if isinstance(feature, AliasedFeature):
        raise TypeError(
            f"{feature!r}: feature aliases are only supported as query outputs"
        )
    f = unwrap_feature(feature, raise_error=False)
    if isinstance(f, Feature) and f._typ is not None and f.is_has_many:  # pyright: ignore[reportPrivateUsage]
        df = f.typ.as_dataframe()
        if df is not None and df.__columns__:
            return f"{f.root_fqn}[{','.join(feature_to_query_str(c) for c in df.columns)}]"
    return str(feature)


def ensure_feature(feature: Union[str, Feature, FeatureWrapper, Any]) -> Feature:
    from chalk.features.feature_field import Feature

    if isinstance(feature, str):
        return Feature.from_root_fqn(feature)
    if isinstance(feature, FeatureWrapper):
        return unwrap_feature(feature)
    if isinstance(feature, Feature):
        return feature
    raise TypeError(f"Feature identifier {feature} of type {type(feature).__name__} is not supported.")


__all__ = ["AliasedFeature", "FeatureWrapper", "unwrap_feature", "ensure_feature", "validate_output_column_name"]
