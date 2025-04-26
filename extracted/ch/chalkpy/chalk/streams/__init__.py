import inspect
from typing import Any, Callable, Dict, Literal, Optional, TypeVar, Union

from typing_extensions import TYPE_CHECKING, ParamSpec

from chalk._lsp.error_builder import get_resolver_error_builder
from chalk.features.tag import Environments
from chalk.state import KeyedState
from chalk.streams._kafka_source import KafkaSource
from chalk.streams._kinesis_source import KinesisSource
from chalk.streams._pubsub_source import PubSubSource
from chalk.streams._windows import (
    MaterializationWindowConfig,
    Windowed,
    get_name_with_duration,
    group_by_windowed,
    windowed,
)
from chalk.streams.base import StreamSource
from chalk.utils import MachineType

if TYPE_CHECKING:
    from chalk.features.resolver import ResolverProtocol, StreamResolver

__all__ = (
    "KafkaSource",
    "KeyedState",
    "KinesisSource",
    "MaterializationWindowConfig",
    "PubSubSource",
    "StreamSource",
    "Windowed",
    "get_name_with_duration",
    "group_by_windowed",
    "stream",
    "windowed",
)

P = ParamSpec("P")
T = TypeVar("T")
V = TypeVar("V")


def stream(
    *,
    source: StreamSource,
    mode: Optional[Literal["continuous", "tumbling"]] = None,
    environment: Optional[Environments] = None,
    machine_type: Optional[MachineType] = None,
    owner: Optional[str] = None,
    parse: Optional[Callable[[T], V]] = None,
    keys: Optional[Dict[str, Any]] = None,
    timestamp: Optional[str] = None,
    updates_materialized_aggregations: bool = True,
) -> Union[Callable[[Callable[P, T]], "ResolverProtocol[P, T]"], "ResolverProtocol[P, T]"]:
    """Decorator to create a stream resolver.

    Parameters
    ----------
    source
        The streaming source, e.g. `KafkaSource(...)` or `KinesisSource(...)` or `PubSubSource(...)`.
    mode
        This parameter is defined when the streaming resolver returns a windowed feature.
        Tumbling windows are fixed-size, contiguous and non-overlapping time intervals. You can think of
        tumbling windows as adjacently arranged bins of equal width.
        Tumbling windows are most often used alongside `max_staleness` to allow the features
        to be sent to the online store and offline store after each window period.

        Continuous windows, unlike tumbling window, are overlapping and exact.
        When you request the value of a continuous window feature, Chalk looks
        at all the messages received in the window and computes the value on-demand.

        See more at https://docs.chalk.ai/docs/windowed-streaming#window-modes
    parse
        A callable that will interpret an input prior to the invocation of the resolver.
        Parse functions can serve many functions, including pre-parsing bytes,
        skipping unrelated messages, or supporting rekeying.

        See more at https://docs.chalk.ai/docs/streams#parsing
    keys
        A mapping from input `BaseModel` attribute to Chalk feature attribute to support continuous streaming re-keying.
        This parameter is required for continuous resolvers.
        Features that are included here do not have to be explicitly returned in the stream resolver:
        the feature will automatically be set to the key value used for aggregation.
    timestamp
        An optional string specifying an input attribute as the timestamp used for windowed aggregations.
    updates_materialized_aggregations
        If set to `False`, the stream resolver will not update materialized aggregations, but is still eligible for ETL.

    Other Parameters
    ----------------
    environment
        Environments are used to trigger behavior in different deployments
        such as staging, production, and local development.

        Environment can take one of three types:
            - `None` (default) - candidate to run in every environment
            - `str` - run only in this environment
            - `list[str]` - run in any of the specified environment and no others

        Read more at https://docs.chalk.ai/docs/resolver-environments
    machine_type
        You can optionally specify that resolvers need to run
        on a machine other than the default. Must be configured
        in your deployment.
    owner
        Individual or team responsible for this resolver.
        The Chalk Dashboard will display this field, and alerts
        can be routed to owners.

    Returns
    -------
    Callable[[Any, ...], Any]
        A callable function! You can unit-test stream resolvers as you would
        unit-test any other code.
    """
    frame = inspect.currentframe()
    assert frame is not None
    caller_frame = frame.f_back
    assert caller_frame is not None
    caller_globals = caller_frame.f_globals
    caller_locals = caller_frame.f_locals
    from chalk.features.resolver import parse_and_register_stream_resolver

    def decorator(fn: Callable[P, T]) -> "StreamResolver[P,T]":
        caller_filename = inspect.getsourcefile(fn) or "unknown_file"
        error_builder = get_resolver_error_builder(fn)
        return parse_and_register_stream_resolver(
            caller_globals=caller_globals,
            caller_locals=caller_locals,
            fn=fn,
            source=source,
            mode=mode,
            caller_filename=caller_filename,
            caller_line=caller_frame.f_lineno,
            error_builder=error_builder,
            environment=environment,
            machine_type=machine_type,
            message=None,
            owner=owner,
            parse=parse,
            keys=keys,
            timestamp=timestamp,
            updates_materialized_aggregations=updates_materialized_aggregations,
        )

    return decorator
