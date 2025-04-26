import dataclasses
import zlib
from copy import deepcopy
from typing import Any, Callable, List, Literal, Optional, Tuple, TypeVar, Union, overload

from chalk._monitoring.charts_enums_codegen import (
    ChartLinkKind,
    ComparatorKind,
    FilterKind,
    GroupByKind,
    MetricKind,
    WindowFunctionKind,
)
from chalk.features import Feature
from chalk.features.resolver import RESOLVER_REGISTRY, ResolverProtocol


@dataclasses.dataclass
class MetricFilter:
    kind: FilterKind
    comparator: ComparatorKind
    value: List[str]


@dataclasses.dataclass
class ThresholdFunction:
    lhs: "SeriesBase"
    operation: str
    rhs: float


ResolverType = Literal["online", "offline", "stream"]
TSeries = TypeVar("TSeries", bound="SeriesBase")


_WINDOW_FUNCTION_VALUE_DICT = {
    "99%": WindowFunctionKind.PERCENTILE_99,
    "95%": WindowFunctionKind.PERCENTILE_95,
    "75%": WindowFunctionKind.PERCENTILE_75,
    "50%": WindowFunctionKind.PERCENTILE_50,
    "25%": WindowFunctionKind.PERCENTILE_25,
    "5%": WindowFunctionKind.PERCENTILE_5,
    "99": WindowFunctionKind.PERCENTILE_99,
    "95": WindowFunctionKind.PERCENTILE_95,
    "75": WindowFunctionKind.PERCENTILE_75,
    "50": WindowFunctionKind.PERCENTILE_50,
    "25": WindowFunctionKind.PERCENTILE_25,
    "5": WindowFunctionKind.PERCENTILE_5,
    "ALL": WindowFunctionKind.ALL_PERCENTILES,
}


class SeriesBase:
    """
    Base class for Series
    """

    def __init__(
        self,
        name: Optional[str],
        metric: Union[MetricKind, str],
        window_function: Optional[Union[WindowFunctionKind, str]] = None,
        time_shift: Optional[int] = None,
    ):
        self._name = name
        self._metric: Optional[MetricKind] = MetricKind(metric.upper()) if metric else None
        self._filters: List[MetricFilter] = []
        self._window_function: Union[WindowFunctionKind, None] = self._get_window_function_type(window_function)
        self._group_by: List[GroupByKind] = []
        self._time_shift: Optional[int] = time_shift
        self._entity_kind = ChartLinkKind.manual
        self._entity_id = None
        self._validations: List[Callable[[], None]] = []

    @property
    def _default_name(self):
        content = ""
        if self._window_function is not None:
            content += (
                self._window_function.lower().replace("all_percentiles", "pAll").replace("percentile_", "p") + ":"
            )
        if self._metric is not None:
            content += self._metric.lower()
        if len(self._group_by) > 0:
            content += f".{'.'.join(sorted(g.value.lower() for g in self._group_by))})"
        if len(self._filters) > 0:
            f = ",".join(
                sorted(
                    f"{f.kind.value.lower()}{f.comparator.value.replace('EQ', '=').replace('NEQ', '!=').replace('ONE_OF', '∈')}{f.value[0] if len(f.value) == 1 else f.value}"
                    for f in self._filters
                )
            )
            content += f"[{f}]"
        return content

    @property
    def name(self):
        return self._name or self._default_name

    def _get_window_function_type(
        self, key: Optional[Union[str, WindowFunctionKind]]
    ) -> Union[WindowFunctionKind, None]:
        if key is None or isinstance(key, WindowFunctionKind):
            return key

        uk = key.upper()
        if uk in WindowFunctionKind.__members__:
            return WindowFunctionKind(uk)

        if uk in _WINDOW_FUNCTION_VALUE_DICT:
            return _WINDOW_FUNCTION_VALUE_DICT[uk]

        raise ValueError(f"Window function '{key}' is not supported for Series '{self.name}'")

    def _where(
        self: TSeries,
        feature: Optional[Union[List[Any], Any]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        operation_id: Optional[Union[List[str], str]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
        cron_status: Optional[Literal["success", "failure"]] = None,
        migration_status: Optional[Literal["success", "failure"]] = None,
        query_status: Optional[Literal["success", "failure"]] = None,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        cache_hit: Optional[bool] = None,
        is_null: Optional[bool] = None,
        equals: bool = True,
    ) -> TSeries:
        copy = self._copy_with()
        success_dict = {"success": True, "failure": False}
        if feature:
            feature_name = [feature] if not isinstance(feature, list) else feature
            copy = copy._feature_name_filter(*feature_name, equals=equals)
        if resolver:
            resolver_name = [resolver] if not isinstance(resolver, list) else resolver
            copy = copy._resolver_name_filter(*resolver_name, equals=equals)
        if feature_tag:
            feature_tag = [feature_tag] if isinstance(feature_tag, str) else feature_tag
            copy = copy._string_filter(*feature_tag, kind=FilterKind.FEATURE_TAG, equals=equals)
        if resolver_tag:
            resolver_tag = [resolver_tag] if isinstance(resolver_tag, str) else resolver_tag
            copy = copy._string_filter(*resolver_tag, kind=FilterKind.RESOLVER_TAG, equals=equals)
        if operation_id:
            operation_id = [operation_id] if isinstance(operation_id, str) else operation_id
            copy = copy._string_filter(*operation_id, kind=FilterKind.OPERATION_ID, equals=equals)
        if query_name:
            query_name = [query_name] if isinstance(query_name, str) else query_name
            copy = copy._string_filter(*query_name, kind=FilterKind.QUERY_NAME, equals=equals)
        if feature_status:
            copy = copy._status_filter(kind=FilterKind.FEATURE_STATUS, success=success_dict[feature_status] == equals)
        if resolver_status:
            copy = copy._status_filter(kind=FilterKind.RESOLVER_STATUS, success=success_dict[resolver_status] == equals)
        if cron_status:
            copy = copy._status_filter(kind=FilterKind.CRON_STATUS, success=success_dict[cron_status] == equals)
        if migration_status:
            copy = copy._status_filter(
                kind=FilterKind.MIGRATION_STATUS, success=success_dict[migration_status] == equals
            )
        if query_status:
            copy = copy._status_filter(kind=FilterKind.QUERY_STATUS, success=success_dict[query_status] == equals)
        if resolver_type:
            resolver_type = [resolver_type] if not isinstance(resolver_type, list) else resolver_type
            copy = copy._with_resolver_type_filter(*resolver_type, equals=equals)
        if cache_hit is not None:
            copy = copy._true_false_filter(kind=FilterKind.CACHE_HIT, value=cache_hit == equals)
        if is_null is not None:
            copy = copy._true_false_filter(kind=FilterKind.IS_NULL, value=is_null == equals)
        return copy

    def _feature_name_filter(self: TSeries, *features: Tuple[Any], equals: bool) -> TSeries:
        if not features:
            raise ValueError(f"One or more Chalk Features must be supplied to Series '{self.name}'.")
        copy = self._copy_with()
        comparator = ComparatorKind.EQ if equals else ComparatorKind.NEQ
        if len(features) == 1 or not equals:
            for feature in features:
                value = str(feature)
                copy._validate_feature(value)
                metric_filter = MetricFilter(kind=FilterKind.FEATURE_NAME, comparator=comparator, value=[value])
                copy._filters.append(metric_filter)
            if len(features) == 1:
                feature = features[0]
                copy._entity_id = str(feature)
                copy._entity_kind = ChartLinkKind.feature
        else:
            values = [str(feature) for feature in features]
            [copy._validate_feature(value) for value in values]
            metric_filter = MetricFilter(kind=FilterKind.FEATURE_NAME, comparator=ComparatorKind.ONE_OF, value=values)
            copy._filters.append(metric_filter)
        return copy

    def _resolver_name_filter(self: TSeries, *resolvers: Union[ResolverProtocol, str], equals: bool) -> TSeries:
        if not resolvers:
            raise ValueError(f"One or more Chalk Resolvers must be supplied for Series '{self.name}'.")
        copy = self._copy_with()
        comparator = ComparatorKind.EQ if equals else ComparatorKind.NEQ
        if len(resolvers) == 1 or not equals:
            for resolver in resolvers:
                value = resolver if isinstance(resolver, str) else resolver.fqn
                copy._validate_resolver(value)
                metric_filter = MetricFilter(kind=FilterKind.RESOLVER_NAME, comparator=comparator, value=[value])
                copy._filters.append(metric_filter)
            if len(resolvers) == 1:
                resolver = resolvers[0]
                copy._entity_id = resolver if isinstance(resolver, str) else resolver.fqn
                copy._entity_kind = ChartLinkKind.resolver
        else:
            values = [resolver if isinstance(resolver, str) else resolver.fqn for resolver in resolvers]
            [copy._validate_resolver(value) for value in values]
            metric_filter = MetricFilter(kind=FilterKind.RESOLVER_NAME, comparator=ComparatorKind.ONE_OF, value=values)
            copy._filters.append(metric_filter)
        return copy

    def _string_filter(self: TSeries, *strings: str, kind: FilterKind, equals: bool = True) -> TSeries:
        if not strings:
            raise ValueError(f"One or more arguments must be supplied for this filter for Series '{self.name}'.")
        copy = self._copy_with()
        comparator = ComparatorKind.EQ if equals else ComparatorKind.NEQ
        if len(strings) == 1 or not equals:
            for string in strings:
                metric_filter = MetricFilter(kind=kind, comparator=comparator, value=[string])
                copy._filters.append(metric_filter)
            if len(strings) == 1 and kind == FilterKind.QUERY_NAME:
                copy._entity_id = strings[0]
                copy._entity_kind = ChartLinkKind.query
        else:
            metric_filter = MetricFilter(kind=kind, comparator=ComparatorKind.ONE_OF, value=list(strings))
            copy._filters.append(metric_filter)
        return copy

    def _with_resolver_type_filter(
        self: TSeries, *resolver_types: Literal["online", "offline", "stream"], equals: bool = True
    ) -> TSeries:
        if not resolver_types:
            raise ValueError(
                f"One or more resolver types from 'online', 'offline', or 'stream' must be supplied "
                f"for Series '{self.name}'."
            )
        if not set(resolver_types).issubset(["online", "offline", "stream"]):
            raise ValueError(
                f"Resolver types '{resolver_types}' must be one of 'online', 'offline', or 'stream' "
                f"for Series '{self.name}'."
            )
        copy = self._copy_with()
        comparator = ComparatorKind.EQ if equals else ComparatorKind.NEQ
        if len(resolver_types) == 1 or not equals:
            for resolver_type in resolver_types:
                metric_filter = MetricFilter(
                    kind=FilterKind.ONLINE_OFFLINE, comparator=comparator, value=[resolver_type]
                )
                copy._filters.append(metric_filter)
        else:
            metric_filter = MetricFilter(
                kind=FilterKind.ONLINE_OFFLINE, comparator=ComparatorKind.ONE_OF, value=list(resolver_types)
            )
            copy._filters.append(metric_filter)
        return copy

    def _true_false_filter(self: TSeries, kind: FilterKind, value: bool) -> TSeries:
        copy = self._copy_with()
        copy._filters.append(
            MetricFilter(
                kind=kind,
                comparator=ComparatorKind.EQ,
                value=["true" if value else "false"],
            )
        )
        return copy

    def _status_filter(self: TSeries, kind: FilterKind, success: bool) -> TSeries:
        copy = self._copy_with()
        copy._filters.append(
            MetricFilter(
                kind=kind,
                comparator=ComparatorKind.EQ,
                value=["success" if success else "failure"],
            )
        )
        return copy

    def _with_filter(
        self: TSeries,
        kind: Union[FilterKind, str],
        comparator: Union[ComparatorKind, str],
        value: Union[List[str], str],
    ) -> TSeries:
        copy = self._copy_with()
        kind = FilterKind(kind.upper())
        comparator = ComparatorKind(comparator.upper())
        value = [value] if isinstance(value, str) else value
        metric_filter = MetricFilter(kind=kind, comparator=comparator, value=value)
        copy._filters.append(metric_filter)
        return copy

    def with_window_function(self: TSeries, window_function: Union[WindowFunctionKind, str]) -> TSeries:
        copy = self._copy_with()
        copy._window_function = WindowFunctionKind(window_function.upper())
        return copy

    def with_group_by(self: TSeries, group_by: Union[GroupByKind, str]) -> TSeries:
        copy = self._copy_with()
        group_by = GroupByKind(group_by.upper())
        copy._group_by.append(group_by)
        return copy

    def with_time_shift(self: TSeries, time_shift: int) -> TSeries:
        copy = self._copy_with()
        copy._time_shift = time_shift
        return copy

    def _copy_with(self: TSeries) -> TSeries:
        self_copy = deepcopy(self)
        return self_copy

    def _validate_resolver(self, resolver_string: str):
        def _validate_resolver():
            maybe_resolver = RESOLVER_REGISTRY.get_resolver(resolver_string)
            if maybe_resolver is None:
                raise ValueError(f"No resolver found with name or fqn '{resolver_string}' for Series '{self.name}'.")

        self._validations.append(_validate_resolver)

    def _validate_feature(self, feature_string: str):
        def _validate_feature():
            split = feature_string.split(".")
            try:
                assert len(split) == 2
                Feature.from_root_fqn(feature_string)
            except Exception:
                raise ValueError(
                    f"No feature found with name '{feature_string}' for Series '{self._name}'. "
                    f"Feature must be in the format 'user.name'"
                )

        self._validations.append(_validate_feature)

    def __gt__(self, other: Union[float, int]) -> ThresholdFunction:
        return ThresholdFunction(self, ">", other)

    def __lt__(self, other: Union[float, int]) -> ThresholdFunction:
        return ThresholdFunction(self, "<", other)

    def __ge__(self, other: Union[float, int]) -> ThresholdFunction:
        return ThresholdFunction(self, ">=", other)

    def __le__(self, other: Union[float, int]) -> ThresholdFunction:
        return ThresholdFunction(self, "<=", other)

    def __ne__(self, other: Union[float, int]) -> ThresholdFunction:
        return ThresholdFunction(self, "!=", other)

    def __str__(self) -> str:
        return f"Series(name='{self._name}')"

    @overload
    def __eq__(self, other: "SeriesBase") -> bool:
        ...

    @overload
    def __eq__(self, other: Union[float, int]) -> ThresholdFunction:
        ...

    def __eq__(self, other: Union[float, int, "SeriesBase"]) -> Union[bool, ThresholdFunction]:
        if isinstance(other, (int, float)):
            return ThresholdFunction(self, "==", other)
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        name = self._name if self._name else "."
        metric = str(self._metric) if self._metric else "."
        filter_strings = (
            sorted([f"{f.kind}.{f.comparator}.{'.'.join(f.value)}" for f in self._filters]) if self._filters else "."
        )
        window_function = str(self._window_function) if self._window_function else "."
        group_by = sorted([str(group_by) for group_by in self._group_by]) if self._group_by else "."
        time_shift = str(self._time_shift) if self._time_shift else "."

        series_string = (
            f"series.{name}.{metric}.{'.'.join(filter_strings)}.{window_function}.{'.'.join(group_by)}.{time_shift}"
        )

        return zlib.crc32(series_string.encode())
