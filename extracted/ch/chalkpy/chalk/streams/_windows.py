from __future__ import annotations

from datetime import datetime, timedelta
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Iterable,
    List,
    Literal,
    Mapping,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from typing_extensions import TypedDict

from chalk._validation.feature_validation import FeatureValidation
from chalk._validation.validation import Validation
from chalk.features._encoding.primitive import TPrimitive
from chalk.features.feature_field import WindowConfigResolved
from chalk.features.underscore import Underscore
from chalk.utils.collections import ensure_tuple
from chalk.utils.duration import CHALK_MAX_TIMEDELTA, CronTab, Duration, parse_chalk_duration_s

TPrim = TypeVar("TPrim", bound=TPrimitive)
TRich = TypeVar("TRich")

if TYPE_CHECKING:
    import pyarrow as pa

    from chalk.features._encoding.converter import TDecoder, TEncoder


class WindowedInstance(Generic[TRich]):
    def __init__(self, values: Mapping[str, TRich]):
        super().__init__()
        self.values = values

    def __call__(self, period: str):
        return self.values[period]


class WindowedMeta(type, Generic[TRich]):
    def __getitem__(cls, underlying: Type[Any]) -> Windowed[TRich]:
        return Windowed(
            kind=underlying,
            buckets=[],
            description=None,
            owner=None,
            tags=None,
            name=None,
            default=...,
            max_staleness=None,
            version=None,
            etl_offline_to_online=None,
            encoder=None,
            decoder=None,
            min=None,
            max=None,
            min_length=None,
            max_length=None,
            contains=None,
            strict=False,
            dtype=None,
            validations=None,
            offline_ttl=None,
            expression=None,
            materialization=None,
        )  # noqa


JsonValue = Any


def get_name_with_duration(name_or_fqn: str, duration: Union[str, int, timedelta]) -> str:
    duration_secs = parse_chalk_duration_s(duration)
    if duration_secs >= CHALK_MAX_TIMEDELTA.total_seconds():
        return f"{name_or_fqn}__all__"
    return f"{name_or_fqn}__{duration_secs}__"


if TYPE_CHECKING:
    _WINDOWED_METACLASS = type
else:
    _WINDOWED_METACLASS = WindowedMeta


class Windowed(Generic[TRich], metaclass=_WINDOWED_METACLASS):
    """Declare a windowed feature.

    Examples
    --------
    >>> @features
    ... class User:
    ...     failed_logins: Windowed[int] = windowed("10m", "24h")
    """

    def __getitem__(self, item: Type[Any] | Any):
        # Here for editor support
        super().__getitem__(item)  # pyright: ignore

    @property
    def buckets_seconds(self) -> Set[int]:
        return {parse_chalk_duration_s(bucket) for bucket in self._buckets}

    @property
    def kind(self) -> Type[TRich]:
        if self._kind is None:
            raise RuntimeError("Window type has not yet been parsed")
        return self._kind

    @kind.setter
    def kind(self, kind: Type[TRich]) -> None:
        assert self._kind is None, "Window type cannot be set twice"
        self._kind = kind

    def _to_feature(self, bucket: int | str | None):
        from chalk.features import Feature

        assert self._name is not None

        window_duration = None if bucket is None else parse_chalk_duration_s(bucket)
        if bucket is None:
            name = self._name
        elif window_duration not in self.buckets_seconds:
            raise ValueError(f"Bucket {bucket} is not in the list of specified buckets")
        else:
            name = get_name_with_duration(self._name, duration=window_duration)

        return Feature(
            name=name,
            version=self._version,
            owner=self._owner,
            tags=None if self._tags is None else list(ensure_tuple(self._tags)),
            description=self._description,
            primary=False,
            default=self._default,
            max_staleness=self._max_staleness,
            offline_ttl=self._offline_ttl,
            etl_offline_to_online=self._etl_offline_to_online,
            encoder=self._encoder,
            decoder=self._decoder,
            pyarrow_dtype=self._dtype,
            validations=FeatureValidation(
                min=self._min,
                max=self._max,
                min_length=self._min_length,
                max_length=self._max_length,
                contains=self._contains,
                strict=self._strict,
            ),
            all_validations=(
                None
                if self._validations is None
                else [
                    FeatureValidation(
                        min=v.min,
                        max=v.max,
                        min_length=v.min_length,
                        max_length=v.max_length,
                        contains=None,
                        strict=v.strict,
                    )
                    for v in self._validations
                ]
            ),
            # Only the root feature should have all the durations
            # The pseudo-features, which are bound to a duration, should not have the durations
            # of the other buckets
            window_durations=tuple(self.buckets_seconds) if bucket is None else tuple(),
            window_duration=window_duration,
            underscore_expression=self._expression,
            window_materialization=(
                MaterializationWindowConfig(bucket_duration=timedelta(seconds=window_duration))
                if self._materialization is True and window_duration is not None
                else self._materialization
                if isinstance(self._materialization, dict)
                else None
            ),
        )

    def __init__(
        self,
        buckets: List[str],
        description: str | None,
        owner: str | None,
        tags: Any | None,
        name: str | None,
        default: TRich | ellipsis,
        max_staleness: Duration | ellipsis | None,
        version: int | None,
        etl_offline_to_online: bool | None,
        encoder: TEncoder[TPrim, TRich] | None,
        decoder: TDecoder[TPrim, TRich] | None,
        min: TRich | None,
        max: TRich | None,
        min_length: int | None,
        max_length: int | None,
        contains: TRich | None,
        strict: bool,
        validations: List[Validation] | None,
        dtype: pa.DataType | None,
        kind: Type[TRich] | None,
        offline_ttl: Duration | ellipsis | None,
        expression: Underscore | None,
        materialization: MaterializationWindowConfig | Literal[True] | None,
    ):
        super().__init__()
        self._kind = kind
        self._buckets = buckets
        self._description = description
        self._owner = owner
        self._tags = tags
        self._name = name
        self._default = default
        self._max_staleness = max_staleness
        self._offline_ttl = offline_ttl
        self._description = description
        self._version = version
        self._etl_offline_to_online = etl_offline_to_online
        self._encoder = encoder
        self._decoder = decoder
        self._min = min
        self._max = max
        self._min_length = min_length
        self._max_length = max_length
        self._contains = contains
        self._strict = strict
        self._validations = validations
        self._dtype = dtype
        self._expression = expression
        self._materialization = materialization


class SelectedWindow:
    def __init__(self, kind: Windowed, selected: str):
        super().__init__()
        self.windowed = kind
        self.selected = selected


class MaterializationWindowConfig(TypedDict, total=False):
    """Configuration for window aggregates. At least one of
    `bucket_duration` and `bucket_durations` must be provided.

    If both are provided, `bucket_duration` acts as a default
    for the window materialization, which may be overridden by
    `bucket_duration`.
    """

    bucket_duration: Duration
    """The duration of each bucket in the window, using a
    `chalk.Duration` string, e.g. `"1m"`, `"1h"`, `"1d"`.

    To use different bucket durations for different window
    sizes, see `bucket_durations` below.
    """

    bucket_durations: Mapping[Duration, Sequence[Duration] | Duration]
    """A mapping from the desired bucket duration to the
    window size(s) that should use that bucket duration.

    If `bucket_duration` is also provided, any window
    durations not specified in this mapping will pick up
    the bucket duration from the `bucket_duration` parameter.

    This parameter is useful when you have some very large
    windows and some very small windows. For example, if you
    have a 365-day window and a 10-minute window, you wouldn't
    want to maintain 365 days of 10-minute buckets in the online
    store. However, using a 1-day bucket for the 10-minute
    window would also lead to significantly more events fitting
    into the window than you might want.

    In this case, you could specify:

    ```
    count: Windowed[int] = windowed(
        "1d", "7d", "60d", "365d",
        materialization={
            # 1-day buckets as a default, for the 7d window
            bucket_duration="1d",
            bucket_durations={
                # 10-minute buckets for the 1d window
                "10m": "1d",
                # 5-day buckets for 60d and 365d windows
                "5d": ["60d", "365d"],
            }
        },
        expression=_.events.count(),
    )
    ```
    """

    bucket_start: datetime
    """The lower bound of the first bucket. All buckets will start at some multiple of the bucket duration after this time."""

    bucket_starts: Mapping[datetime, Sequence[Duration] | Duration]
    """Used to specify a different bucket start for each window duration. Same format as `bucket_durations`."""

    backfill_schedule: CronTab | None
    """The schedule on which to automatically backfill the aggregation. For example, `"* * * * *"` or `"1h"`."""

    continuous_buffer_duration: Duration | None
    """The minimum period of time for which to sample data directly via online query, rather than from the backfilled aggregations."""


def group_by_windowed(
    *buckets: str,
    expression: Underscore,
    materialization: MaterializationWindowConfig | Literal[True],
    days: Iterable[int] = (),
    hours: Iterable[int] = (),
    minutes: Iterable[int] = (),
    description: str | None = None,
    owner: str | None = None,
    tags: Any | None = None,
    name: str | None = None,
    default: TRich | ellipsis = ...,
    min: TRich | None = None,
    max: TRich | None = None,
    strict: bool = False,
    validations: List[Validation] | None = None,
    dtype: pa.DataType | None = None,
) -> Any:
    """Create a windowed feature with grouping.

    See more at https://docs.chalk.ai/docs/materialized_aggregations

    Parameters
    ----------
    buckets
        The size of the buckets for the window function.
        Buckets are specified as strings in the format `"1d"`, `"2h"`, `"1h30m"`, etc.
        You may also choose to specify the buckets using the days, hours, and minutes
        parameters instead. The buckets parameter is helpful if you want to use
        multiple units to express the bucket size, like `"1h30m"`.
    days
        Convenience parameter for specifying the buckets in days.
        Using this parameter is equvalent to specifying the buckets parameter
        with a string like `"1d"`.
    hours
        Convenience parameter for specifying the buckets in hours.
        Using this parameter is equvalent to specifying the buckets parameter
        with a string like `"1h"`.
    minutes
        Convenience parameter for specifying the buckets in minutes.
        Using this parameter is equvalent to specifying the buckets parameter
        with a string like `"1m"`.
    default
        The default value of the feature if it otherwise can't be computed.
    materialization
        Configuration for aggregating data. Pass `bucket_duration` with a
        [Duration](/api-docs#Duration) to configure the bucket size for aggregation.

        See more at https://docs.chalk.ai/docs/materialized_aggregations
    dtype
        The backing `pyarrow.DataType` for the feature. This parameter can
        be used to control the storage format of data. For example, if you
        have a lot of data that could be represented as smaller data types,
        you can use this parameter to save space.

        >>> import pyarrow as pa
        >>> from chalk.features import features
        >>> @features
        ... class User:
        ...     id: str
        ...     email_count: Windowed[int] = windowed(
        ...         "10m", "30m",
        ...         dtype=pa.int16(),
        ...     )
    owner
        You may also specify which person or group is responsible for a feature.
        The owner tag will be available in Chalk's web portal.
        Alerts that do not otherwise have an owner will be assigned
        to the owner of the monitored feature.
    tags
        Add metadata to a feature for use in filtering, aggregations,
        and visualizations. For example, you can use tags to assign
        features to a team and find all features for a given team.
    min
        If specified, when this feature is computed, Chalk will check that `x >= min`.
    max
        If specified, when this feature is computed, Chalk will check that `x <= max`.
    strict
        If `True`, if this feature does not meet the validation criteria, Chalk will not persist
        the feature value and will treat it as failed.
    expression
        The expression to compute the feature. This is an underscore expression,
        like `_.transactions[_.amount].sum()`.

    Other Parameters
    ----------------
    name
        The name for the feature. By default, the name of a feature is
        the name of the attribute on the class, prefixed with
        the camel-cased name of the class. Note that if you provide an
        explicit name, the namespace, determined by the feature class,
        will still be prepended. See `features` for more details.
    description
        Descriptions are typically provided as comments preceding
        the feature definition. For example, you can document a
        `emails_by_category` feature with information about the values
        as follows:
        >>> from chalk import _
        >>> @features
        ... class User:
        ...     # Count of emails sent, grouped by category
        ...     emails_by_category: DataFrame = group_by_windowed(
        ...         "10m", "30m",
        ...         description="Count of emails sent, grouped by category",
        ...         expression=_.emails.group_by(_.category).count(),
        ...     )

        You can also specify the description directly with this parameter:
        >>> from chalk import _
        >>> @features
        ... class User:
        ...     emails: DataFrame[Email]
        ...     emails_by_category: DataFrame = group_by_windowed(
        ...         "10m", "30m",
        ...         description="Count of emails sent, grouped by category",
        ...         expression=_.emails.group_by(_.category).count(),
        ...     )
    validations

    Returns
    -------
    GroupByWindowed

    Examples
    --------
    >>> from chalk import group_by_windowed, DataFrame
    >>> from chalk.features import features
    >>> @features
    ... class Email:
    ...     id: int
    ...     user_id: "User.id"
    >>> @features
    ... class User:
    ...     id: int
    ...     emails: DataFrame[Email]
    ...     emails_by_category: DataFrame = group_by_windowed(
    ...         "10m", "30m",
    ...         expression=_.emails.group_by(_.category).count(),
    ...     )
    """
    return GroupByWindowed(
        list(buckets) + [f"{x}m" for x in minutes] + [f"{x}h" for x in hours] + [f"{x}d" for x in days],
        description=description,
        owner=owner,
        tags=tags,
        name=name,
        default=default,
        min=min,
        max=max,
        strict=strict,
        dtype=dtype,
        validations=validations,
        expression=expression,
        materialization=materialization,
    )


class GroupByWindowNarrowed(Generic[TRich]):
    def __init__(
        self,
        kind: GroupByWindowed[TRich],
        filters: Tuple[Any, ...],
        selected_window: int,
    ):
        super().__init__()
        self._kind = kind
        self._filters = filters
        self._selected_window = selected_window

    def __str__(self):
        parent_name = self._kind._name  # pyright: ignore[reportPrivateUsage]
        namespace = self._kind._namespace  # pyright: ignore[reportPrivateUsage]
        return f"{namespace}.{parent_name}_{self._selected_window}"


class GroupByWindowed(Generic[TRich], metaclass=_WINDOWED_METACLASS):
    def __init__(
        self,
        buckets: List[str],
        materialization: MaterializationWindowConfig | Literal[True],
        expression: Underscore,
        description: str | None,
        owner: str | None,
        tags: Any | None,
        name: str | None,
        default: Union[TRich, ellipsis],
        min: TRich | None,
        max: TRich | None,
        strict: bool,
        validations: List[Validation] | None,
        dtype: pa.DataType | None,
    ):
        super().__init__()
        self._buckets = buckets
        self._description = description
        self._owner = owner
        self._tags = tags
        self._name = name
        self._namespace: str | None = None
        self._default = default
        self._description = description
        self._min = min
        self._max = max
        self._strict = strict
        self._validations = validations
        self._dtype = dtype
        self._expression = expression
        self._materialization: MaterializationWindowConfig | Literal[True] = materialization
        self._kind: Type | None = None
        self._window_materialization_parsed: "WindowConfigResolved | None" = None

    def __getitem__(self, item: Type[Any]):
        filters = []
        window_seconds = []
        for x in ensure_tuple(item):
            if isinstance(x, str):
                duration_seconds = parse_chalk_duration_s(x)
                if duration_seconds not in self.buckets_seconds:
                    raise ValueError(f"Bucket {x} is not in the list of specified buckets")
                window_seconds.append(duration_seconds)
            else:
                filters.append(x)

        if len(window_seconds) == 0:
            raise ValueError("No window selected")
        elif len(window_seconds) > 1:
            raise ValueError("Only one window can be selected")

        return GroupByWindowNarrowed(
            kind=self,
            filters=tuple(filters),
            selected_window=window_seconds[0],
        )

    @property
    def buckets_seconds(self) -> Set[int]:
        return {parse_chalk_duration_s(bucket) for bucket in self._buckets}


def windowed(
    *buckets: str,
    days: Iterable[int] = (),
    hours: Iterable[int] = (),
    minutes: Iterable[int] = (),
    description: str | None = None,
    owner: str | None = None,
    tags: Any | None = None,
    name: str | None = None,
    default: TRich | ellipsis = ...,
    max_staleness: Duration | ellipsis | None = ...,
    offline_ttl: Duration | ellipsis | None = ...,
    version: int | None = None,
    etl_offline_to_online: bool | None = None,
    encoder: TEncoder[TPrim, TRich] | None = None,
    decoder: TDecoder[TPrim, TRich] | None = None,
    min: TRich | None = None,
    max: TRich | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    strict: bool = False,
    validations: List[Validation] | None = None,
    dtype: pa.DataType | None = None,
    expression: Underscore | None = None,
    materialization: MaterializationWindowConfig | Literal[True] | None = None,
) -> Windowed[TRich]:
    """Create a windowed feature.

    See more at https://docs.chalk.ai/docs/aggregations

    Parameters
    ----------
    buckets
        The size of the buckets for the window function.
        Buckets are specified as strings in the format `"1d"`, `"2h"`, `"1h30m"`, etc.
        You may also choose to specify the buckets using the days, hours, and minutes
        parameters instead. The buckets parameter is helpful if you want to use
        multiple units to express the bucket size, like `"1h30m"`.
    days
        Convenience parameter for specifying the buckets in days.
        Using this parameter is equvalent to specifying the buckets parameter
        with a string like `"1d"`.
    hours
        Convenience parameter for specifying the buckets in hours.
        Using this parameter is equvalent to specifying the buckets parameter
        with a string like `"1h"`.
    minutes
        Convenience parameter for specifying the buckets in minutes.
        Using this parameter is equvalent to specifying the buckets parameter
        with a string like `"1m"`.
    default
        The default value of the feature if it otherwise can't be computed.
    materialization
        Configuration for aggregating data. Pass `bucket_duration` with a
        [Duration](/api-docs#Duration) to configure the bucket size for aggregation.
        If `True`, each of the windows will use a bucket duration equal to its
        window duration.

        See more at https://docs.chalk.ai/docs/materialized_aggregations
    owner
        You may also specify which person or group is responsible for a feature.
        The owner tag will be available in Chalk's web portal.
        Alerts that do not otherwise have an owner will be assigned
        to the owner of the monitored feature.
    tags
        Add metadata to a feature for use in filtering, aggregations,
        and visualizations. For example, you can use tags to assign
        features to a team and find all features for a given team.
    max_staleness
        When a feature is expensive or slow to compute, you may wish to cache its value.
        Chalk uses the terminology "maximum staleness" to describe how recently a feature
        value needs to have been computed to be returned without re-running a resolver.

        See more at https://docs.chalk.ai/docs/feature-caching
    version
        Feature versions allow you to manage a feature as its
        definition changes over time.

        The `version` keyword argument allows you to specify the
        maximum number of versions available for this feature.

        See more at https://docs.chalk.ai/docs/feature-versions
    etl_offline_to_online
        When `True`, Chalk copies this feature into the online environment
        when it is computed in offline resolvers.

        See more at https://docs.chalk.ai/docs/reverse-etl
    min
        If specified, when this feature is computed, Chalk will check that `x >= min`.
    max
        If specified, when this feature is computed, Chalk will check that `x <= max`.
    min_length
        If specified, when this feature is computed, Chalk will check that `len(x) >= min_length`.
    max_length
        If specified, when this feature is computed, Chalk will check that `len(x) <= max_length`.
    strict
        If `True`, if this feature does not meet the validation criteria, Chalk will not persist
        the feature value and will treat it as failed.
    expression
        The expression to compute the feature. This is an underscore expression, like `_.transactions[_.amount].sum()`.
    validations
        A list of Validations to apply to this feature.

        See more at https://docs.chalk.ai/api-docs#Validation
    offline_ttl
        Sets a maximum age for values eligible to be retrieved from the offline store,
        defined in relation to the query's current point-in-time.

    Other Parameters
    ----------------
    name
        The name for the feature. By default, the name of a feature is
        the name of the attribute on the class, prefixed with
        the camel-cased name of the class. Note that if you provide an
        explicit name, the namespace, determined by the feature class,
        will still be prepended. See `features` for more details.
    description
        Descriptions are typically provided as comments preceding
        the feature definition. For example, you can document a
        `email_count` feature with information about the values
        as follows:
        >>> @features
        ... class User:
        ...     # Count of emails sent
        ...     email_count: Windowed[int] = windowed("10m", "30m")

        You can also specify the description directly with this parameter:
        >>> @features
        ... class User:
        ...     email_count: Windowed[int] = windowed(
        ...         "10m",
        ...         "30m",
        ...         description="Count of emails sent",
        ...     )
    dtype
        The backing `pyarrow.DataType` for the feature. This parameter can
        be used to control the storage format of data. For example, if you
        have a lot of data that could be represented as smaller data types,
        you can use this parameter to save space.

        >>> import pyarrow as pa
        >>> from chalk.features import features
        >>> @features
        ... class User:
        ...     id: str
        ...     email_count: Windowed[int] = windowed(
        ...         "10m", "30m",
        ...         dtype=pa.int16(),
        ...     )
    encoder
    decoder

    Returns
    -------
    Windowed[TPrim, TRich]
        Metadata for the windowed feature, parameterized by
        `TPrim` (the primitive type of the feature) and
        `TRich` (the decoded type of the feature, if `decoder` is provided).

    Examples
    --------
    >>> from chalk import windowed, Windowed
    >>> @features
    ... class User:
    ...     id: int
    ...     email_count: Windowed[int] = windowed(days=range(1, 30))
    ...     logins: Windowed[int] = windowed("10m", "1d", "30d")
    >>> User.email_count["7d"]
    """
    return Windowed(
        list(buckets) + [f"{x}m" for x in minutes] + [f"{x}h" for x in hours] + [f"{x}d" for x in days],
        description=description,
        owner=owner,
        tags=tags,
        name=name,
        default=default,
        max_staleness=max_staleness,
        version=version,
        etl_offline_to_online=etl_offline_to_online,
        encoder=cast("TEncoder", encoder),
        decoder=decoder,
        min=min,
        max=max,
        min_length=min_length,
        max_length=max_length,
        contains=None,
        strict=strict,
        dtype=dtype,
        kind=None,
        validations=validations,
        offline_ttl=offline_ttl,
        expression=expression,
        materialization=materialization,
    )
