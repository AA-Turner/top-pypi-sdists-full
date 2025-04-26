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

if TYPE_CHECKING:
    from chalk.features.feature_field import Feature
    from chalk.features.dataframe import DataFrame

T = TypeVar("T")


class _MarkedUnderlyingFeature:
    __slots__ = ("_fn", "_source", "_debug_info")

    def __init__(self, fn: Callable[[], Feature | Filter | type[DataFrame] | FeatureWrapper | Aggregation],
                 debug_info: Any = None) -> None:
        super().__init__()
        self._fn = fn
        self._debug_info = debug_info

    def __call__(self, *args: Any, **kwds: Any) -> Feature | Filter | type[DataFrame] | FeatureWrapper | Aggregation:
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

    def _chalk_get_underlying(self) -> Feature | Aggregation | Filter | type[DataFrame]:
        if isinstance(self._chalk_underlying, _MarkedUnderlyingFeature):
            self._chalk_underlying = self._chalk_underlying()
        if isinstance(self._chalk_underlying, FeatureWrapper):
            self._chalk_underlying = unwrap_feature(self._chalk_underlying)
        return self._chalk_underlying

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

        from chalk.features import FeatureSetBase, Feature
        from chalk.streams import get_name_with_duration

        underlying_feature = self._chalk_get_underlying()
        if not isinstance(underlying_feature, Feature):
            raise TypeError(f"Cannot get the windowed feature for {underlying_feature}, which is not a feature.")

        parent = (
            FeatureSetBase.registry[underlying_feature.namespace]
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
            from chalk.features.feature_set import FeatureSetBase

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
                        x = next(
                            f for f in FeatureSetBase.registry[foreign_feature.namespace].features if f.name == key)
                        dataframe_item[i] = x
                tuple_item = tuple(dataframe_item)

                f_copy_underlying = copy.copy(underlying)
                f_copy_underlying.typ = ParsedAnnotation(underlying=dataframe_typ[tuple_item])
                if len(f_copy_underlying.path) > 0:
                    path_copy = list(f_copy_underlying.path)
                    path_copy[-1] = dataclasses.replace(path_copy[-1], child=f_copy_underlying)
                    f_copy_underlying.path = tuple(path_copy)

                return FeatureWrapper(f_copy_underlying)
            raise TypeError(f"Feature '{self}' does not support subscripting. Attempted to subscript with '{item}'")

        return FeatureWrapper(_MarkedUnderlyingFeature(f, ("__getitem__", item)))

    def __getattr__(self, item: str):

        # Passing through __getattr__ on has_one features, as users can use getattr
        # notation in annotations for resolvers
        if item.startswith("__") and not item.startswith("__chalk"):
            # Short-circuiting on the dunders to be compatible with copy.copy
            raise AttributeError(item)

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
        LSPErrorBuilder.save_node(self, item)
        return FeatureWrapper(_MarkedUnderlyingFeature(fn, ("__getattr__", item)))

    def is_near(self, item: Any, metric: Literal["l2", "cos", "ip"] = "l2") -> Filter:
        from chalk.features import Feature
        other = unwrap_feature(item)
        underlying = self._chalk_get_underlying()
        if not isinstance(underlying, Feature):
            raise TypeError(f"Feature.is_near() is only supported on features. {underlying} is not a feature.")
        self_vector = underlying.typ.as_vector()
        if self_vector is None:
            raise TypeError(
                f"Nearest neighbor relationships are only supported for vector features. Feature '{underlying.root_fqn}' is not a vector."
            )
        other_vector = other.typ.as_vector()
        if other_vector is None:
            raise TypeError(
                f"Nearest neighbor relationships are only supported for vector features. Feature '{other.root_fqn}' is not a vector."
            )
        if underlying.converter.pyarrow_dtype != other.converter.pyarrow_dtype:
            raise TypeError(
                (
                    f"Nearest neighbor relationships are only supported if both vectors have the same data type and dimensions. "
                    f"Feature '{underlying.root_fqn}' is of type `{underlying.converter.pyarrow_dtype}` "
                    f" while feature '{other.root_fqn}' is `{other.converter.pyarrow_dtype}`."
                )
            )
        return Filter(underlying, f"is_near_{metric}", other)


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


def ensure_feature(feature: Union[str, Feature, FeatureWrapper, Any]) -> Feature:
    from chalk.features.feature_field import Feature

    if isinstance(feature, str):
        return Feature.from_root_fqn(feature)
    if isinstance(feature, FeatureWrapper):
        return unwrap_feature(feature)
    if isinstance(feature, Feature):
        return feature
    raise TypeError(f"Feature identifier {feature} of type {type(feature).__name__} is not supported.")


__all__ = ["FeatureWrapper", "unwrap_feature", "ensure_feature"]
