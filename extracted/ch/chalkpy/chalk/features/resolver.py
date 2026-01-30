# pyright: reportPrivateUsage = false

from __future__ import annotations

import abc
import ast
import asyncio
import base64
import builtins
import collections
import collections.abc
import dataclasses
import datetime as datetime_module
import difflib
import hashlib
import importlib
import inspect
import json
import math
import random
import re
import statistics
import types
import typing
from dataclasses import dataclass, is_dataclass
from datetime import datetime
from enum import Enum, IntEnum
from inspect import Parameter, isclass
from types import ModuleType
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    AsyncIterable,
    AsyncIterator,
    Callable,
    Collection,
    Dict,
    Generator,
    Generic,
    Iterable,
    Iterator,
    List,
    Literal,
    Mapping,
    Optional,
    ParamSpec,
    Protocol,
    Sequence,
    Set,
    Type,
    TypeAlias,
    TypeVar,
    Union,
    cast,
    final,
    get_args,
    get_origin,
    overload,
)

import google.protobuf.message
import pyarrow
import pyarrow as pa
import requests
from google.protobuf import message_factory
from google.protobuf.descriptor import Descriptor
from google.protobuf.internal.python_message import GeneratedProtocolMessageType
from pydantic import BaseModel

from chalk._lsp._class_finder import get_function_caller_info
from chalk._lsp.error_builder import FunctionCallErrorBuilder, ResolverErrorBuilder, get_resolver_error_builder
from chalk.df.LazyFramePlaceholder import LazyFramePlaceholder
from chalk.features._encoding.protobuf import (
    convert_proto_message_type_to_pyarrow_type,
    serialize_message_file_descriptor,
)
from chalk.features._encoding.pyarrow import rich_to_pyarrow
from chalk.features.dataframe import DataFrame, DataFrameMeta
from chalk.features.feature_field import Feature
from chalk.features.feature_set import Features, is_feature_set_class
from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature
from chalk.features.filter import Filter, TimeDelta, time_is_frozen
from chalk.features.namespace_context import build_namespaced_name
from chalk.features.pseudofeatures import CHALK_TS_FEATURE, PSEUDONAMESPACE
from chalk.features.tag import Environments, Tags
from chalk.sink import SinkIntegrationProtocol
from chalk.state import StateWrapper
from chalk.streams import KafkaSource, StreamSource, get_name_with_duration
from chalk.streams.types import (
    StreamResolverParam,
    StreamResolverParamKeyedState,
    StreamResolverParamMessage,
    StreamResolverParamMessageWindow,
    StreamResolverSignature,
)
from chalk.utils import AnyDataclass, MachineType, notebook
from chalk.utils.annotation_parsing import ResolverAnnotationParser
from chalk.utils.cached_type_hints import cached_get_type_hints
from chalk.utils.collections import FrozenOrderedSet, ensure_tuple
from chalk.utils.duration import CronTab, Duration, parse_chalk_duration
from chalk.utils.gas import GasLimit, OutOfGasError
from chalk.utils.import_utils import check_if_subpackage
from chalk.utils.log_with_context import get_logger
from chalk.utils.pydanticutil.pydantic_compat import is_pydantic_basemodel
from chalk.utils.source_parsing import should_skip_source_code_parsing

try:
    from types import UnionType
except ImportError:
    UnionType = Union

if TYPE_CHECKING:
    from pydantic import BaseModel

    from chalk.features import Underscore
    from chalk.features.underscore import UnderscoreAttr, UnderscoreCall, UnderscoreCast, UnderscoreFunction
    from chalk.ml.model_version import ModelVersion
    from chalk.sql import BaseSQLSourceProtocol, SQLSourceGroup
    from chalk.sql._internal.sql_settings import SQLResolverSettings
    from chalk.sql._internal.sql_source import BaseSQLSource


T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
P = ParamSpec("P")
V = TypeVar("V")

ResolverHook: TypeAlias = "Callable[[Resolver], None] | None"

ResourceHint: TypeAlias = Literal["cpu", "io", "gpu"]

_logger = get_logger(__name__)


@dataclasses.dataclass(frozen=True)
class ResolverArgErrorHandler:
    default_value: Any


@dataclass
class StateDescriptor(Generic[T]):
    kwarg: str
    pos: int
    initial: T
    typ: Type[T]


class Cron:
    """
    Detailed options for specify the schedule and filtering
    functions for Chalk batch jobs.
    """

    def __init__(
        self,
        schedule: CronTab | Duration,
        filter: Callable[..., bool] | None = None,
        sample: Callable[[], DataFrame] | None = None,
    ):
        """Run an online or offline resolver on a schedule.

        This class lets you add a filter or sample function
        to your cron schedule for a resolver. See the
        overloaded signatures for more information.

        Parameters
        ----------
        schedule
            The period of the cron job. Can be either a crontab (`"0 * * * *"`)
            or a `Duration` (`"2h"`).
        filter
            Optionally, a function to filter down the arguments to consider.

            See https://docs.chalk.ai/docs/resolver-cron#filtering-examples for more information.
        sample
            Explicitly provide the sample function for the cron job.

            See https://docs.chalk.ai/docs/resolver-cron#custom-examples for more information.


        Examples
        --------
        Using a filter

        >>> def only_active_filter(v: User.active):
        ...     return v
        >>> @online(cron=Cron(schedule="1d", filter=only_active_filter))
        ... def score_user(d: User.signup_date) -> User.score:
        ...     return ...

        Using a sample function

        >>> def s() -> DataFrame[User.id]:
        ...     return DataFrame.read_csv(...)
        >>> @offline(cron=Cron(schedule="1d", sample=s))
        ... def fn(balance: User.account.balance) -> ...:
        """
        super().__init__()
        self.schedule = schedule
        self.filter = filter
        self.sample = sample
        self.trigger_downstream = False


def _flatten_features(output: Optional[Type[Features]]) -> Sequence[Feature]:
    if output is None:
        return []
    features = output.features
    if len(features) == 1 and isinstance(features[0], type) and issubclass(features[0], DataFrame):
        return features[0].columns
    return features


RESOLVER_FUNCTION_CAPTURE_LIMIT = 30


@dataclass(frozen=True)
class FunctionCapturedGlobal(abc.ABC):
    """
    A (global) variable captured by a resolver.

    Only some kinds of variables are recorded:
    - Builtins (e.g. `min`/`max`/`sum`)
    - Feature Classes (e.g. `@features class User: ...`)

    These captured values can be used while translating Python resolvers into static symbolic resolvers.
    """

    ...


@dataclasses.dataclass(frozen=True)
class FunctionCapturedGlobalFeatureClass(FunctionCapturedGlobal):
    """
    When a resolver captures a global variable, this class indicates that the global variable
    is the name of a feature class (a user-defined class wrapped with `@features`).

    Example: `MyFeatures` is a `FunctionCapturedGlobalFeatureClass(feature_names="my_features")`:

    ```
    @features
    class MyFeatures: ...

    @online
    def example(id: MyFeatures.id) -> MyFeatures.value:
        return MyFeatures(value = 123)
    ```
    """

    feature_namespace: str


@dataclasses.dataclass(frozen=True)
class FunctionCapturedGlobalBuiltin(FunctionCapturedGlobal):
    """
    When a resolver captures a builtin function, this class identifies the builtin function.

    For example, the functions `min`, `max`, or `len` are builtins. If there is no function,
    variable, or class with the same name in scope when the function is defined, then the
    closure variable will resolve to the builtin function.
    """

    builtin_name: str


@dataclasses.dataclass(frozen=True)
class FunctionCapturedGlobalStruct(FunctionCapturedGlobal):
    module: str
    name: str
    pa_dtype: pa.DataType

    @classmethod
    def from_typ(cls, obj: Type) -> "FunctionCapturedGlobalStruct":
        if is_pydantic_basemodel(obj) or dataclasses.is_dataclass(obj):
            return cls(
                name=obj.__name__,
                module=obj.__module__,
                pa_dtype=rich_to_pyarrow(obj, obj.__name__, False, True),
            )
        raise ValueError(f"Can't create FunctionCapturedGlobalStruct from non-struct object of type {type(obj)}: {obj}")


@dataclasses.dataclass(frozen=True)
class FunctionCapturedGlobalProto(FunctionCapturedGlobal):
    module: str
    name: str
    serialized_fd: bytes
    full_name: str
    pa_dtype: pa.DataType

    @classmethod
    def from_typ(cls, obj: Type[google.protobuf.message.Message]) -> "FunctionCapturedGlobalProto":
        return cls(
            name=obj.__name__,
            module=obj.__module__,
            serialized_fd=serialize_message_file_descriptor(obj.DESCRIPTOR.file),
            full_name=obj.DESCRIPTOR.full_name,
            pa_dtype=convert_proto_message_type_to_pyarrow_type(obj.DESCRIPTOR),
        )


@dataclasses.dataclass(frozen=True)
class FunctionCapturedGlobalEnum(FunctionCapturedGlobal):
    module: str
    name: str
    bases: tuple[pa.DataType, ...]
    member_map: Mapping[str, pa.Scalar] = dataclasses.field(hash=False)


@dataclasses.dataclass(frozen=True)
class FunctionCapturedGlobalModule(FunctionCapturedGlobal):
    name: str


@dataclasses.dataclass(frozen=True)
class FunctionCapturedGlobalProtobufMessageClass(FunctionCapturedGlobal):
    """A protobuf message class for intermediate namespace access"""

    full_qualified_name: str  # e.g., "broadcast_pb2.AllocationBroadcast"
    enum_names: FrozenOrderedSet[str]  # e.g., {"NotificationStatus", "Priority"}


@dataclasses.dataclass(frozen=True)
class FunctionCapturedGlobalProtobufEnum(FunctionCapturedGlobal):
    """A protobuf enum class with full disambiguation path"""

    full_qualified_name: str  # e.g., "broadcast_pb2.AllocationBroadcast.NotificationStatus"
    value_to_name_map: Mapping[int, str]  # e.g., {0: "STATUS_UNKNOWN", 1: "STATUS_PENDING"}


@dataclasses.dataclass(frozen=True)
class FunctionCapturedGlobalCallableProtobufDeserializerInstance(FunctionCapturedGlobal):
    """A callable instance (object with __call__ method) referenced from the global scope"""

    name: str
    module: str | None
    instance_type: str  # e.g., "ProtobufDeserializer"
    call_signature: str  # Function signature identifier for lookup
    descriptor: Descriptor


@dataclasses.dataclass(frozen=True)
class FunctionCapturedGlobalModuleMember(FunctionCapturedGlobal):
    module_name: str
    qualname: str


@dataclasses.dataclass(frozen=True)
class FunctionCapturedGlobalFunction(FunctionCapturedGlobal):
    """
    A globally defined function used in a resolver.
    These helper functions may reference other global variables.
    Attributes assigned to the function are dropped.
    Keyword parameters, variadic parameters, and parameter defaults are not supported in static python execution.
    """

    source: str
    module: str | None
    name: str
    captured_globals: Mapping[str, FunctionCapturedGlobal] | None


@dataclasses.dataclass(frozen=True)
class FunctionCapturedGlobalVariable(FunctionCapturedGlobal):
    """A variable referenced from the global scope"""

    name: str
    module: str | None


class ResolverProtocol(Protocol[P, T_co]):
    """A resolver, returned from the decorators `@offline` and `@online`."""

    @property
    def function_definition(self) -> str | None:
        """The content of the resolver as a string."""
        ...

    @property
    def function_captured_globals(self) -> Mapping[str, FunctionCapturedGlobal] | None:
        """
        A subset of the global variables mentioned inside of the function, which are
        saved here in order to allow the function to be emulated symbolically.
        """
        ...

    owner: str | None
    """ Individual or team responsible for this resolver.
    The Chalk Dashboard will display this field, and alerts
    can be routed to owners.
    """

    environment: tuple[str, ...] | None
    """
    Environments are used to trigger behavior
    in different deployments such as staging, production, and
    local development. For example, you may wish to interact with
        a vendor via an API call in the production environment, and
        opt to return a constant value in a staging environment.

        Environment can take one of three types:
        - `None` (default) - candidate to run in every environment
        - `str` - run only in this environment
        - `list[str]` - run in any of the specified environment and no others

    Read more at https://docs.chalk.ai/docs/resolver-environments
    """

    tags: tuple[str, ...] | None
    """
    Allow you to scope requests within an
    environment. Both tags and environment need to match for a
    resolver to be a candidate to execute.

    You might consider using tags, for example, to change out
    whether you want to use a sandbox environment for a vendor,
    or to bypass the vendor and return constant values in a
    staging environment.

    Read more at https://docs.chalk.ai/docs/resolver-tags
    """

    __doc__: Optional[str]
    """The docstring of the resolver."""

    __name__: str
    """The function name of the resolver."""

    __module__: str
    """The python module where the function is defined"""

    __annotations__: dict[str, Any]
    """The type annotations for the resolver"""

    filename: str
    """The filename in which the resolver is defined."""

    name: str
    """The name of the resolver, either given by the name of the function,
    or by the keyword argument `name` given to `@offline` or `@online`.
    """

    resource_hint: ResourceHint | None
    """Whether this resolver is bound by CPU or I/O"""

    static: bool
    """whether the resolver is static. Static resolvers are "executed" once during planning time to produce a computation graph."""

    fqn: str
    """The fully qualified name for the resolver"""

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T_co:
        """Returns the result of calling the function decorated
        with `@offline` or `@online` with the given arguments.

        Parameters
        ----------
        args
            The arguments to pass to the decorated function.
            If one of the arguments is a `DataFrame` with a
            filter or projection applied, the resolver will
            only be called with the filtered or projected
            data. Read more at
            https://docs.chalk.ai/docs/unit-tests#data-frame-inputs

        Returns
        -------
        T
            The result of calling the decorated function
            with `args`. Useful for unit-testing.

            Read more at https://docs.chalk.ai/docs/unit-tests

        Examples
        --------
        >>> @online
        ... def get_num_bedrooms(
        ...     rooms: Home.rooms[Room.name == 'bedroom']
        ... ) -> Home.num_bedrooms:
        ...     return len(rooms)
        >>> rooms = [
        ...     Room(id=1, name="bedroom"),
        ...     Room(id=2, name="kitchen"),
        ...     Room(id=3, name="bedroom"),
        ... ]
        >>> assert get_num_bedrooms(rooms) == 2
        """
        ...


class ResolverRegistry:
    def __init__(self):
        super().__init__()
        self._online_and_offline_resolvers: set[OnlineResolver | OfflineResolver] = set()
        self._stream_resolvers: set[StreamResolver] = set()
        self._sink_resolvers: set[SinkResolver] = set()
        self._short_name_to_resolver: dict[str, Resolver] = {}
        self._deferred_resolvers: list[tuple[Callable[[], Resolver], bool]] = []
        self.hook: Callable[[Resolver], None] | None = None

    def get_online_and_offline_resolvers(self) -> Collection[OnlineResolver | OfflineResolver]:
        self._load_deferred_resolvers()
        return self._online_and_offline_resolvers

    def get_stream_resolvers(self) -> Collection[StreamResolver]:
        self._load_deferred_resolvers()
        return self._stream_resolvers

    def get_sink_resolvers(self) -> Collection[SinkResolver]:
        self._load_deferred_resolvers()
        return self._sink_resolvers

    def _load_deferred_resolvers(self):
        while len(self._deferred_resolvers) > 0:
            deferred_resolver, override = self._deferred_resolvers.pop()
            # Not overriding because deferred resolvers only exist
            self.add_to_registry(deferred_resolver(), override=override)

    def add_to_deferred_registry(self, deferred_resolver: Callable[[], Resolver], *, override: bool):
        self._deferred_resolvers.append((deferred_resolver, override))

    def get_resolver(self, name: str):
        self._load_deferred_resolvers()
        short_name = name.split(".")[-1]
        return self._short_name_to_resolver.get(short_name)

    def get_all_resolvers(self) -> Collection[Resolver]:
        self._load_deferred_resolvers()
        return self._short_name_to_resolver.values()

    def remove_resolver(self, resolver_name: str):
        if self.hook:
            raise RuntimeError(
                "Cannot remove resolvers if there is a hook defined, as the hook does not provide an interface to unregister a resolver."
            )
        self._load_deferred_resolvers()
        short_name = resolver_name.split(".")[-1]
        existing_resolver = self._short_name_to_resolver.get(short_name)
        if existing_resolver is None:
            # Resolver not in the registry
            return
        del self._short_name_to_resolver[short_name]
        if isinstance(existing_resolver, (OnlineResolver, OfflineResolver)):
            self._online_and_offline_resolvers.discard(existing_resolver)
        if isinstance(existing_resolver, StreamResolver):
            self._stream_resolvers.discard(existing_resolver)
        if isinstance(existing_resolver, SinkResolver):
            self._sink_resolvers.discard(existing_resolver)

    def add_to_registry(self, resolver: Resolver, *, override: bool):
        """
        Adds the given resolver to the registry.
        If in a notebook or if override is True, first removes any existing resolvers
        with the same short-name.
        """
        short_name = resolver.name
        if short_name in self._short_name_to_resolver:
            if not override and not notebook.is_notebook():
                # Same short name was reused
                resolver.lsp_builder.add_diagnostic(
                    message=(
                        f"Another resolver with the same function name '{resolver.name}' in module "
                        f"'{self._short_name_to_resolver[short_name].__module__}' exists. "
                        f"Resolver function names must be unique. Please rename this resolver in module '{resolver.__module__}'."
                    ),
                    label="duplicate resolver shortname",
                    code="71",
                    range=resolver.lsp_builder.function_name(),
                    raise_error=None,
                )
                return
            existing_resolver = self._short_name_to_resolver[short_name]
            # Need to remove the resolver from the typed registry
            # Using discard instead of pop to be graceful if the resolver is not in there for some reason (would likely involve some exception being raised when registering the resolver)
            if isinstance(existing_resolver, (OnlineResolver, OfflineResolver)):
                self._online_and_offline_resolvers.discard(existing_resolver)
            if isinstance(existing_resolver, StreamResolver):
                self._stream_resolvers.discard(existing_resolver)
            if isinstance(existing_resolver, SinkResolver):
                self._sink_resolvers.discard(existing_resolver)
        self._short_name_to_resolver[short_name] = resolver
        if isinstance(resolver, (OnlineResolver, OfflineResolver)):
            self._online_and_offline_resolvers.add(resolver)
        if isinstance(resolver, StreamResolver):
            self._stream_resolvers.add(resolver)
        if isinstance(resolver, SinkResolver):
            self._sink_resolvers.add(resolver)
        if self.hook:
            self.hook(resolver)


RESOLVER_REGISTRY = ResolverRegistry()


# Turn the ResolverRegistry class into a sing
def _prevent_duplicate_construction(*args: Any, **kwargs: Any):
    raise RuntimeError(
        "The ResolverRegistry class is a singleton. Please use chalk.features.resolver.RESOLVER_REGISTRY"
    )


ResolverRegistry.__new__ = _prevent_duplicate_construction


class Resolver(ResolverProtocol[P, T], abc.ABC):
    def __init__(
        self,
        *,
        function_definition: str | None,
        function_captured_globals: Mapping[str, FunctionCapturedGlobal] | None = None,
        fqn: str,
        filename: str,
        doc: str | None,
        inputs: Sequence[Feature | type[DataFrame]] | None,
        output: Type[Features] | None,
        fn: Callable[P, T],
        environment: Sequence[str] | None,
        tags: Sequence[str] | None,
        cron: CronTab | Duration | Cron | None,
        machine_type: MachineType | None,
        when: None = None,
        state: StateDescriptor | None,
        default_args: Sequence[ResolverArgErrorHandler | None] | None,
        owner: str | None,
        timeout: Duration | None,
        is_sql_file_resolver: bool,
        source_line: int | None,
        data_sources: Sequence[BaseSQLSource | SQLSourceGroup] | None,
        lsp_builder: ResolverErrorBuilder,
        parse: Callable[[], ResolverParseResult[P, T]] | ResolverParseResult[P, T] | None,
        resource_hint: ResourceHint | None,
        static: bool,
        total: bool,
        autogenerated: bool,
        unique_on: tuple[Feature, ...] | None,
        partitioned_by: tuple[Feature, ...] | None,
        data_lineage: Dict[str, Dict[str, Dict[str, List[str]]]] | None,
        sql_settings: SQLResolverSettings | None,
        resource_group: str | None = None,
        output_row_order: Literal["one-to-one"] | None = None,
        venv: str | None = None,
        name: None = None,  # deprecated
        postprocessing: Underscore | None = None,
    ):
        self._function_definition = ... if function_definition is None else function_definition
        self._function_captured_globals = ... if function_captured_globals is None else function_captured_globals
        self.fqn = fqn
        self.filename = filename
        self._inputs = inputs
        self._output = output
        self.fn = fn
        self.__name__ = self.fn.__name__
        self.__module__ = fn.__module__
        self.__doc__ = fn.__doc__
        self.__annotations__ = fn.__annotations__
        self.environment = tuple(environment) if environment is not None else None
        self.tags = tuple(tags) if tags is not None else None
        self.max_staleness = None
        self.cron = cron
        self._doc = doc
        self.machine_type = machine_type
        self.when = None
        self._state = state
        self._default_args = default_args
        self.owner = owner
        if isinstance(timeout, str):
            timeout = parse_chalk_duration(timeout)
        self.timeout = timeout
        self.is_sql_file_resolver = is_sql_file_resolver
        self.source_line = source_line
        self.data_sources = data_sources
        self.lsp_builder = lsp_builder
        self.is_cell_magic = False
        self.name = fqn.split(".")[-1]
        self.resource_hint = resource_hint
        self.resource_group = resource_group
        self.venv = venv
        self._parse = parse
        self.static = static
        self.total = total
        self.autogenerated = autogenerated
        self._unique_on = unique_on
        self._partitioned_by = partitioned_by
        self._data_lineage = data_lineage
        self._sql_settings = sql_settings
        self.output_row_order = output_row_order
        self.postprocessing = postprocessing
        super().__init__()

    @property
    def function_definition(self) -> str | None:
        if self._function_definition is ...:
            self._do_parse()
        assert self._function_definition is not ...
        return self._function_definition

    @property
    def function_captured_globals(self) -> Mapping[str, FunctionCapturedGlobal] | None:
        if self._function_captured_globals is ...:
            self._do_parse()
        assert self._function_captured_globals is not ...
        return self._function_captured_globals

    @property
    def doc(self) -> str | None:
        if self._doc is None:
            self._do_parse()
        return self._doc

    @property
    def data_lineage(self) -> Dict[str, Dict[str, Dict[str, List[str]]]] | None:
        if self._data_lineage is None:
            self._do_parse()
        return self._data_lineage

    @property
    def sql_settings(self) -> SQLResolverSettings | None:
        return self._sql_settings

    @property
    def inputs(self) -> Sequence[Feature | type[DataFrame]]:
        if self._inputs is None:
            self._do_parse()
        assert self._inputs is not None
        return self._inputs

    @property
    def output(self) -> Type[Features] | None:
        if self._output is None:
            self._do_parse()
        return self._output

    @property
    def flattened_output(self) -> Sequence[Feature]:
        return _flatten_features(self.output)

    @property
    def state(self) -> StateDescriptor | None:
        if self._state is None:
            self._do_parse()
        return self._state

    @property
    def default_args(self) -> Sequence[ResolverArgErrorHandler | None]:
        if self._default_args is None:
            self._do_parse()
        assert self._default_args is not None
        return self._default_args

    @property
    def unique_on(self) -> tuple[Feature, ...] | None:
        if self._unique_on is None:
            self._do_parse()
        return self._unique_on

    @property
    def partitioned_by(self) -> tuple[Feature, ...] | None:
        if self._partitioned_by is None:
            self._do_parse()
        return self._partitioned_by

    def _do_parse(self):
        if self._parse is None:
            if self._function_definition is ...:
                self._function_definition = None
            if self._function_captured_globals is ...:
                self._function_captured_globals = None
            return
        if isinstance(self._parse, Callable):
            self._parse = self._parse()
        if self._function_definition is ...:
            self._function_definition = self._parse.function_definition
        if self._function_captured_globals is ...:
            self._function_captured_globals = self._parse.function_captured_globals
        if self._doc is None:
            self._doc = self._parse.doc
        if self._inputs is None:
            self._inputs = self._parse.inputs
        if self._output is None:
            self._output = self._parse.output
        if self._state is None:
            self._state = self._parse.state
        if self._default_args is None:
            self._default_args = self._parse.default_args
        if self._unique_on is None:
            self._unique_on = self._parse.unique_on
        if self._partitioned_by is None:
            self._partitioned_by = self._parse.partitioned_by
        if self._data_lineage is None:
            self._data_lineage = self._parse.data_lineage

    def _process_call(self, *args: P.args, **kwargs: P.kwargs) -> T:
        # __call__ is defined to support userland code that invokes a resolver
        # as if it is a normal python function
        # If the user returns a ChalkQuery, then we'll want to automatically execute it
        from chalk.sql import FinalizedChalkQuery
        from chalk.sql._internal.chalk_query import ChalkQuery
        from chalk.sql._internal.string_chalk_query import StringChalkQuery

        result = self.fn(*args, **kwargs)

        if isinstance(result, (ChalkQuery, StringChalkQuery)):
            result = result.all()
        if isinstance(result, FinalizedChalkQuery):
            result = result.execute(_flatten_features(self.output))
        return cast(T, result)

    async def _process_async_call(self, *args: P.args, **kwargs: P.kwargs):
        # __call__ is defined to support userland code that invokes a resolver
        # as if it is a normal python function
        # If the user returns a ChalkQuery, then we'll want to automatically execute it
        from chalk.sql import FinalizedChalkQuery
        from chalk.sql._internal.chalk_query import ChalkQuery
        from chalk.sql._internal.string_chalk_query import StringChalkQuery

        assert asyncio.iscoroutinefunction(self.fn)

        result = await self.fn(*args, **kwargs)

        if isinstance(result, (ChalkQuery, StringChalkQuery)):
            result = result.all()
        if isinstance(result, FinalizedChalkQuery):
            result = await result.async_execute(_flatten_features(self.output))
        return result

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        bound = inspect.signature(self.fn).bind(*args, **kwargs)
        updated_args = []
        inputs = self.inputs
        if self.state is not None:
            inputs = (*self.inputs[: self.state.pos], None, *inputs[self.state.pos :])

        for i, (val, input_) in enumerate(zip(bound.args, inputs)):
            if isinstance(input_, type) and issubclass(
                input_, DataFrame
            ):  # pyright: ignore[reportUnnecessaryIsInstance]
                annotation = input_
            elif input_ is not None and input_.is_has_many:  # pyright: ignore[reportAttributeAccessIssue]
                annotation = input_.typ.as_dataframe()  # pyright: ignore[reportAttributeAccessIssue]
                assert annotation is not None, f"Expected DataFrame, found {annotation}"
            else:
                annotation = None

            if annotation is not None:
                if self.static and type(val).__name__ == "DataFrame" and type(val).__module__ == "chalkdf.dataframe":
                    # No need to wrap this class in DataFrame.
                    pass
                elif self.static and isinstance(val, LazyFramePlaceholder):
                    # No need to wrap this class in DataFrame.
                    pass
                elif not isinstance(val, DataFrame):
                    val = DataFrame(val)

                if time_is_frozen():
                    frozen_filter = Filter(lhs=CHALK_TS_FEATURE, operation="<=", rhs=TimeDelta(hours_ago=0))
                    annotation.filters = (frozen_filter, *annotation.filters)

                if annotation.filters and len(annotation.filters) > 0 and not isinstance(val, LazyFramePlaceholder):
                    try:
                        val = val[annotation.filters]
                        val._materialize()  # pyright: ignore[reportPrivateUsage]
                    except:
                        kwarg_name = list(bound.signature.parameters)[i]
                        _logger.warning(
                            (
                                f"The resolver '{self.fqn}' takes a DataFrame as '{kwarg_name}', but the provided "
                                "input is missing columns on which it filters."
                            )
                        )

                updated_args.append(val)
            else:
                updated_args.append(val)
        if asyncio.iscoroutinefunction(self.fn):
            # Not awaiting this coroutine here -- when the caller awaits it,
            # it will run
            return cast(T, self._process_async_call(*updated_args))  # pyright: ignore[reportCallIssue]
        else:
            return self._process_call(*updated_args)  # pyright: ignore[reportCallIssue]

    def add_to_registry(self, *, override: bool):
        """
        Shorthand for RESOLVER_REGISTRY.add_to_registry()
        """
        RESOLVER_REGISTRY.add_to_registry(self, override=override)


@final
class SinkResolver(Resolver[P, T]):
    def __init__(
        self,
        *,
        function_definition: str | None,
        function_captured_globals: Mapping[str, FunctionCapturedGlobal] | None = None,
        fqn: str,
        filename: str,
        doc: str | None,
        inputs: list[Feature],
        fn: Callable[P, T],
        environment: Optional[list[str]],
        tags: Optional[list[str]],
        machine_type: Optional[MachineType],
        buffer_size: int | None,
        debounce: Duration | None,
        max_delay: Duration | None,
        upsert: bool,
        owner: str | None,
        input_is_df: bool,
        default_args: list[ResolverArgErrorHandler | None],
        integration: Optional[Union[BaseSQLSourceProtocol, SinkIntegrationProtocol]],
        source_line: int | None,
        data_sources: Optional[list[BaseSQLSource | SQLSourceGroup]],
        lsp_builder: ResolverErrorBuilder,
    ):
        super().__init__(
            function_definition=function_definition,
            function_captured_globals=function_captured_globals,
            lsp_builder=lsp_builder,
            filename=filename,
            environment=environment,
            machine_type=machine_type,
            fqn=fqn,
            fn=fn,
            doc=doc,
            inputs=inputs,
            output=None,
            tags=tags,
            cron=None,
            when=None,
            state=None,
            default_args=default_args,
            owner=owner,
            source_line=source_line,
            timeout=None,
            is_sql_file_resolver=False,
            data_sources=data_sources,
            parse=None,
            static=False,
            resource_hint=None,
            total=False,
            autogenerated=False,
            unique_on=None,
            partitioned_by=None,
            data_lineage=None,
            sql_settings=None,
        )
        self.buffer_size = buffer_size
        if isinstance(debounce, str):
            debounce = parse_chalk_duration(debounce)
        self.debounce = debounce
        if isinstance(max_delay, str):
            max_delay = parse_chalk_duration(max_delay)
        self.max_delay = max_delay
        self.upsert = upsert
        self.integration = integration
        self.input_is_df = input_is_df

    def __repr__(self):
        return f"SinkResolver(name={self.fqn})"


class OnlineResolver(Resolver[P, T]):
    def __repr__(self):
        return f"OnlineResolver(name={self.fqn})"


class OfflineResolver(Resolver[P, T]):
    def __repr__(self):
        return f"OfflineResolver(name={self.fqn})"


@dataclasses.dataclass(frozen=True)
class ResolverParseResult(Generic[P, T]):
    fqn: str
    inputs: list[Feature]
    state: Optional[StateDescriptor]
    output: Optional[Type[Features]]
    function: Callable[P, T]
    function_definition: str | None
    function_captured_globals: Mapping[str, FunctionCapturedGlobal] | None
    doc: Optional[str]
    default_args: list[Optional[ResolverArgErrorHandler]]
    unique_on: tuple[Feature, ...] | None
    partitioned_by: tuple[Feature, ...] | None
    data_lineage: Optional[Dict[str, Dict[str, Dict[str, List[str]]]]]


@dataclasses.dataclass(frozen=True)
class SinkResolverParseResult(Generic[P, T]):
    fqn: str
    input_features: list[Feature]
    input_is_df: bool
    function: Callable[P, T]
    function_definition: str | None
    doc: Optional[str]
    input_feature_defaults: list[Optional[ResolverArgErrorHandler]]


def get_resolver_fqn(function: Callable, name: str | None = None):
    name = function.__name__ if name is None else name
    # We need to prepend the namespace onto the short name, since that is what we ensure uniqueness on
    name = build_namespaced_name(name=name)
    if notebook.is_notebook() and not notebook.is_defined_in_module(function):
        return name
    return f"{function.__module__}.{name}"


def get_state_default_value(
    state_typ: type,
    declared_default: Any,
    parameter_name_for_errors: str,
    resolver_fqn_for_errors: str,
    error_builder: ResolverErrorBuilder,
) -> Any:
    if not is_pydantic_basemodel(state_typ) and not dataclasses.is_dataclass(state_typ):
        error_builder.add_diagnostic(
            message=(
                f"State value must be a pydantic model or dataclass, "
                f"but argument '{parameter_name_for_errors}' has type '{type(state_typ).__name__}'"
            ),
            code="117",
            label="invalid state type",
            range=error_builder.function_arg_annotation_by_name(parameter_name_for_errors),
            raise_error=ValueError,
        )

    default = declared_default
    if default is inspect.Signature.empty:
        try:
            default = state_typ()
        except Exception as e:
            cls_name = state_typ.__name__
            error_builder.add_diagnostic(
                message=(
                    "State parameter must have a default value, or be able to be instantiated "
                    f"with no arguments. For resolver '{resolver_fqn_for_errors}', no default found, and default "
                    f"construction failed with '{str(e)}'. Assign a default in the resolver's "
                    f"signature ({parameter_name_for_errors}: {cls_name} = {cls_name}(...)), or assign a default"
                    f" to each of the fields of '{cls_name}'."
                ),
                code="118",
                label="state value must have a default",
                range=error_builder.function_arg_annotation_by_name(parameter_name_for_errors),
                raise_error=ValueError,
            )

    if not isinstance(default, cast(Type, state_typ)):
        error_builder.add_diagnostic(
            message=(
                f"Expected type '{state_typ.__name__}' for '{parameter_name_for_errors}', "
                f"but default '{default}' does not match."
            ),
            code="119",
            label="invalid default state",
            range=error_builder.function_arg_value_by_name(parameter_name_for_errors),
            raise_error=ValueError,
        )

    return default


def _explode_features(ret_val: Type[Features], inputs: list[Feature]) -> Type[Features]:
    new_features = []
    if getattr(ret_val, "__is_exploded__", False):
        # already exploded by Features[]. Take out inputs and return
        return Features[[feature for feature in ret_val.features if feature not in inputs]]
    if is_feature_set_class(ret_val):
        # Is a root namespace feature class. Return only scalars.
        return Features[
            [
                f
                for f in ret_val.features
                if not f.is_autogenerated
                and not f.is_windowed
                and not f.is_has_many
                and not f.is_has_one
                and f not in inputs
            ]
        ]
    flattened_features = []
    for f in _flatten_features(ret_val):
        if isinstance(f, type) and issubclass(f, DataFrame):
            raise TypeError("If a resolver returns a DataFrame, it must be the only feature returned. ")
        if not f.is_autogenerated:
            flattened_features.append(f)
    # These features should be exploded

    is_dataframe = (
        len(ret_val.features) == 1
        and isinstance(ret_val.features[0], type)
        and issubclass(ret_val.features[0], DataFrame)
    )

    for f in flattened_features:
        if f.is_windowed:
            for d in f.window_durations:
                windowed_name = get_name_with_duration(name_or_fqn=f.name, duration=d)
                windowed_feature = getattr(f.features_cls, windowed_name)
                new_features.append(unwrap_feature(windowed_feature))
        elif f.is_has_many and is_dataframe:
            dataframe_typ = f.typ.as_dataframe()
            assert dataframe_typ is not None
            new_features.extend(
                [
                    col
                    for col in dataframe_typ.columns
                    if not col.is_autogenerated and not col.is_windowed and not col.is_has_many and not col.is_has_one
                ]
            )
        elif f.is_has_one:
            if f.joined_class is None:
                raise ValueError(f"Has one feature {f.fqn} has no joined class")
            new_features.extend(
                [
                    f.copy_with_path(x)
                    for x in f.joined_class.features
                    if not x.is_autogenerated and not x.is_windowed and not x.is_has_many and not x.is_has_one
                ]
            )
        elif not f.is_autogenerated:
            new_features.append(f)

    if is_dataframe:
        return Features[DataFrame[new_features]]

    return Features[new_features]


def parse_function(
    fn: Callable[P, T],
    glbs: Optional[Dict[str, Any]],
    lcls: Optional[Dict[str, Any]],
    error_builder: ResolverErrorBuilder,
    ignore_return: bool = False,
    allow_custom_args: bool = False,
    is_streaming_resolver: bool = False,
    validate_output: bool = False,
    name: str | None = None,
    unique_on: Collection[Any] | None = None,
    partitioned_by: Collection[Any] | None = None,
) -> Callable[[], ResolverParseResult[P, T]]:
    def f():
        fqn = get_resolver_fqn(function=fn, name=name)
        short_name = fqn.split(".")[-1]
        sig = inspect.signature(fn)
        function_source = None

        if not should_skip_source_code_parsing():
            try:
                function_source = inspect.getsource(fn)
            except:
                pass

        return_annotation = cached_get_type_hints(fn).get("return")

        annotation_parser = ResolverAnnotationParser(fn, glbs, lcls, error_builder)

        if return_annotation is None and not ignore_return:
            error_builder.add_diagnostic(
                message=f"Resolver '{short_name}' must have a return annotation.",
                code="81",
                label="resolver lacks a return annotation",
                range=error_builder.function_return_annotation(),
                raise_error=TypeError,
                code_href="https://docs.chalk.ai/docs/python-resolvers#outputs",
            )

        ret_val = None

        origin = get_origin(return_annotation)

        if isinstance(origin, type) and issubclass(origin, (Iterable, Iterator, AsyncIterable, AsyncIterator)):
            # If it's iterable, then it might be a generator
            args = get_args(return_annotation)
            if len(args) != 1:
                error_builder.add_diagnostic(
                    message=(
                        f"Resolver '{short_name}' has a return annotation '{return_annotation}' which does not specify any features. "
                        f"Please include features inside the type signature -- for example, `{origin.__name__}[Features[MyFeatureSet.id, MyFeatureSet.feature_2]]`"
                    ),
                    code="100",
                    label="resolver return does not include features",
                    range=error_builder.function_return_annotation(),
                    raise_error=TypeError,
                )

            return_annotation = get_args(return_annotation)[0]
            if not (isinstance(return_annotation, type) and issubclass(return_annotation, DataFrame)):
                # If a function is annotated to return an iterable, treat it as a DF resolver. This is because generators can yield more than one row
                # Treat scalar-returning generator resolvers as DF-returning, as they could yield more than one row
                return_annotation = DataFrame[return_annotation]
            origin = get_origin(return_annotation)

        if isinstance(origin, type) and issubclass(origin, (Generator, AsyncGenerator)):
            args = get_args(return_annotation)
            if len(args) != 3:
                error_builder.add_diagnostic(
                    message=(
                        f"Resolver '{short_name}' has a return annotation '{return_annotation}' which does not specify any features. "
                        f"Please include features inside the type signature -- for example, `{origin.__name__}[Features[MyFeatureSet.id, MyFeatureSet.feature_2], Any, Any]`"
                    ),
                    code="100",
                    label="resolver return does not include features",
                    range=error_builder.function_return_annotation(),
                    raise_error=TypeError,
                )

            return_annotation = get_args(return_annotation)[0]
            if not (isinstance(return_annotation, type) and issubclass(return_annotation, DataFrame)):
                # If a function is annotated to return an generator, treat it as a DF resolver. This is because generators can yield more than one row
                # Treat scalar-returning generator resolvers as DF-returning, as they could yield more than one row
                return_annotation = DataFrame[return_annotation]
            origin = get_origin(return_annotation)

        if (inspect.isgeneratorfunction(fn) or inspect.isasyncgenfunction(fn)) and not (
            isinstance(return_annotation, type) and issubclass(return_annotation, DataFrame)
        ):
            # If a function is a generator, treat it as a DF resolver. This is because generators can yield more than one row
            # Treat scalar-returning generator resolvers as DF-returning, as they could yield more than one row
            return_annotation = DataFrame[return_annotation]
            origin = get_origin(return_annotation)

        if isinstance(return_annotation, FeatureWrapper):
            return_annotation = unwrap_feature(return_annotation)

        if isinstance(return_annotation, Feature):
            # we handle any explosions in _explode_features()
            maybe_dataframe = return_annotation.typ.parsed_annotation
            if return_annotation.is_has_many and issubclass(maybe_dataframe, DataFrame):
                _validate_dataframe(maybe_dataframe, error_builder, fqn=return_annotation.fqn)
            ret_val = Features[return_annotation]

        if ret_val is None and not ignore_return:
            if not isinstance(return_annotation, type):
                error_builder.add_diagnostic(
                    message=(
                        f"Resolver '{short_name}' has a return annotation '{return_annotation}' of type "
                        f"{type(return_annotation)}. "
                        "Resolver return annotations must be a type."
                    ),
                    code="82",
                    label="resolver return annotation is not a type",
                    range=error_builder.function_return_annotation(),
                    raise_error=TypeError,
                )
            if issubclass(return_annotation, Features):
                # function annotated like def get_account_id(user_id: User.id) -> Features[User.account_id]
                # or def get_account_id(user_id: User.id) -> User:
                ret_val = return_annotation
            elif issubclass(return_annotation, DataFrame):
                # function annotated like def get_transactions(account_id: Account.id) -> DataFrame[Transaction]
                _validate_dataframe(return_annotation, error_builder)
                ret_val = Features[return_annotation]

        if ret_val is None and not ignore_return:
            error_builder.add_diagnostic(
                message=(
                    f"Resolver '{short_name}' does not specify a return type. "
                    "Please add an annotation (like `-> User.first_name`) to the resolver."
                ),
                code="83",
                label="resolver lacks a return type",
                range=error_builder.function_return_annotation(),
                raise_error=TypeError,
            )

        inputs = [annotation_parser.parse_annotation(p) for p in sig.parameters.keys()]

        # Unwrap anything that is wrapped with FeatureWrapper
        inputs = [unwrap_feature(p) if isinstance(p, FeatureWrapper) else p for p in inputs]

        if len(inputs) == 0:
            default_arg_count = 0
        elif isinstance(inputs[0], type) and issubclass(inputs[0], DataFrame):
            default_arg_count = len(inputs[0].columns)
        else:
            default_arg_count = len(inputs)

        state = None
        default_args: list[Optional[ResolverArgErrorHandler]] = [None for _ in range(default_arg_count)]

        function_definition = None if function_source is None else simplify_function_definition(function_source)
        """inexpensive heuristic: if errors, the following inspect code is expensive"""
        datetime_now = "datetime.now()"
        if function_definition is not None and datetime_now in function_definition:
            caller_filename = inspect.getsourcefile(fn)
            if caller_filename is not None:
                with open(caller_filename, "r") as f:
                    content = f.read()
                lines = content.split("\n")
                for i, arg_name in enumerate(sig.parameters.keys()):
                    arg_node = error_builder.function_arg_value_by_index(i)
                    if isinstance(arg_node, ast.AST):
                        datetime_now_range = error_builder.string_in_node(
                            node=arg_node, string=datetime_now, text=lines
                        )
                        if datetime_now_range is not None:
                            error_builder.add_diagnostic(
                                message=(
                                    "Do not use 'datetime.now()' in your resolver arguments. "
                                    "If you want the current time for inference or backfills, "
                                    "replace this annotation with chalk.Now."
                                ),
                                code="87",
                                label="replace with chalk.Now",
                                range=datetime_now_range,
                                raise_error=ValueError,
                                code_href="https://docs.chalk.ai/docs/time",
                            )

        for i, (arg_name, parameter) in enumerate(sig.parameters.items()):
            bad_input_message = (
                "Resolver inputs must be Features, DataFrame, or State. "
                f"Resolver '{short_name}' received '{str(inputs[i])}' for argument '{arg_name}'."
            )
            arg = inputs[i]

            if get_origin(arg) in (UnionType, Union):
                args = get_args(arg)
                if len(args) != 2:
                    error_builder.add_diagnostic(
                        message=bad_input_message,
                        code="87",
                        label="invalid input type",
                        range=error_builder.function_arg_annotation_by_name(arg_name),
                        raise_error=ValueError,
                    )
                if type(None) not in args:
                    error_builder.add_diagnostic(
                        message=bad_input_message,
                        code="87",
                        label="invalid input type",
                        range=error_builder.function_arg_annotation_by_name(arg_name),
                        raise_error=ValueError,
                    )
                real_arg = next((a for a in args if a is not type(None)), None)
                if real_arg is None:
                    error_builder.add_diagnostic(
                        message=bad_input_message,
                        code="87",
                        label="invalid input type",
                        range=error_builder.function_arg_annotation_by_name(arg_name),
                        raise_error=ValueError,
                    )
                default_args[i] = ResolverArgErrorHandler(None)
                arg = unwrap_feature(real_arg)
                inputs[i] = arg

            if parameter.empty != parameter.default:
                default_args[i] = ResolverArgErrorHandler(parameter.default)

            if not isinstance(arg, (StateWrapper, Feature)) and not (
                isinstance(arg, type) and issubclass(arg, DataFrame)
            ):
                if allow_custom_args:
                    continue
                if isinstance(arg, datetime) or arg == datetime:
                    error_builder.add_diagnostic(
                        message=f"{bad_input_message} If you want the current time for inference or backfills, replace this annotation with chalk.Now.",
                        code="87",
                        label="replace with chalk.Now",
                        range=error_builder.function_arg_annotation_by_name(arg_name),
                        raise_error=ValueError,
                        code_href="https://docs.chalk.ai/docs/time",
                    )
                else:
                    error_builder.add_diagnostic(
                        message=bad_input_message,
                        code="87",
                        label="invalid input type",
                        range=error_builder.function_arg_annotation_by_name(arg_name),
                        raise_error=ValueError,
                    )

            if isinstance(arg, Feature) and arg.last_for is not None and default_args[i] is None:
                default_args[i] = ResolverArgErrorHandler(None)

            if isinstance(arg, Feature) and arg.is_windowed:
                # Windowed arguments in resolver signatures must specify a window bucket
                available_windows = ", ".join(f"{x}s" for x in arg.window_durations)

                error_builder.add_diagnostic(
                    message=(
                        f"Resolver argument '{arg_name}' to '{short_name}' does not select a window period. "
                        f"Add a selected window, like {arg.name}('{next(iter(arg.window_durations), '')}'). "
                        f"Available windows: {available_windows}."
                    ),
                    code="88",
                    label="missing period",
                    range=error_builder.function_arg_annotation_by_name(arg_name),
                    raise_error=ValueError,
                )

            if isinstance(arg, Feature) and arg.is_has_many:
                maybe_dataframe = arg.typ.parsed_annotation
                if issubclass(maybe_dataframe, DataFrame):
                    _validate_dataframe(maybe_dataframe, error_builder, fqn=arg.fqn, arg_index=i)

            if not isinstance(arg, StateWrapper):
                continue

            if state is not None:
                error_builder.add_diagnostic(
                    message=(
                        f"Only one state argument is allowed. "
                        f"Two provided to '{short_name}': '{state.kwarg}' and '{arg_name}'"
                    ),
                    code="89",
                    label="second state argument",
                    range=error_builder.function_arg_annotations()[arg_name],
                    raise_error=ValueError,
                )

            arg_name = parameter.name

            state = StateDescriptor(
                kwarg=arg_name,
                pos=i,
                initial=get_state_default_value(
                    state_typ=arg.typ,
                    resolver_fqn_for_errors=fqn,
                    parameter_name_for_errors=arg_name,
                    declared_default=parameter.default,
                    error_builder=error_builder,
                ),
                typ=arg.typ,
            )

        if not is_streaming_resolver:
            assert ret_val is not None
            ret_val = _explode_features(ret_val, inputs)

        assert ret_val is None or issubclass(ret_val, Features)
        if (
            not ignore_return
            and ret_val is not None
            and issubclass(ret_val, Features)  # pyright: ignore[reportUnnecessaryIsInstance]
        ):
            # Streaming resolvers are themselves windowed, so the outputs must not specify a window explicitly.
            for f in _flatten_features(ret_val):
                if f.is_windowed_pseudofeature and is_streaming_resolver:
                    feature_name_without_duration = "__".join(
                        f.root_fqn.split("__")[:-1]
                    )  # A bit hacky, but should work
                    error_builder.add_diagnostic(
                        message=(
                            "Stream resolvers should not resolve features of particular window periods in the return type. "
                            f"Resolver '{short_name}' returned feature '{f.root_fqn}'. "
                            f"Instead, return '{feature_name_without_duration}'."
                        ),
                        code="90",
                        label="invalid outputs",
                        range=error_builder.function_return_annotation(),
                        raise_error=ValueError,
                    )

        if not is_streaming_resolver:
            # TODO(rkargon) If inputs are DataFrames, then the output must be a DataFrame as well.
            #   Remove this once we support resolvers of type DF[X] --> Y.y
            #   (e.g. 'population-level' aggregations)
            if any((isinstance(x, type) and issubclass(x, DataFrame)) for x in inputs):
                assert ret_val is not None
                if not (
                    len(ret_val.features) == 1
                    and isinstance(ret_val.features[0], type)
                    and issubclass(cast(type, ret_val.features[0]), DataFrame)
                ):
                    error_builder.add_diagnostic(
                        message=(
                            f"Resolver that has DataFrame inputs cannot have a non-DataFrame output feature. "
                            f"The resolver '{short_name}' returns '{ret_val}', which is not a DataFrame."
                        ),
                        code="91",
                        label="non-DataFrame output",
                        range=error_builder.function_return_annotation(),
                        raise_error=TypeError,
                    )

        state_index = state.pos if state is not None else None

        if validate_output and ret_val is None:
            error_builder.add_diagnostic(
                message=f"Online resolvers must return features; '{fqn}' returns None",
                code="72",
                label="missing output",
                range=error_builder.function_return_annotation(),
                raise_error=TypeError,
            )
        unique_on_parsed = (
            _validate_feature_reference_collection(unique_on, error_builder, fqn, "unique_on", ret_val)
            if unique_on is not None
            else None
        )
        partitioned_by_parsed = (
            _validate_feature_reference_collection(partitioned_by, error_builder, fqn, "partitioned_by", ret_val)
            if partitioned_by is not None
            else None
        )

        gas = GasLimit(remaining_gas=RESOLVER_FUNCTION_CAPTURE_LIMIT, out_of_gas_error=OutOfGasError())
        function_captured_globals = parse_extract_function_object_captured_globals(fn, gas)

        return ResolverParseResult(
            fqn=fqn,
            inputs=[v for i, v in enumerate(inputs) if i != state_index],
            output=ret_val,
            function=cast(Callable[P, T], fn),
            function_definition=function_source,
            function_captured_globals=function_captured_globals,
            doc=fn.__doc__,
            state=state,
            default_args=default_args,
            unique_on=unique_on_parsed,
            partitioned_by=partitioned_by_parsed,
            data_lineage=None,
        )

    return f


def parse_helper_function(
    fn: Callable[..., Any],
    gas: GasLimit,
) -> FunctionCapturedGlobalFunction:
    if should_skip_source_code_parsing():
        raise ValueError("Source code parsing is disabled")
    sig = inspect.signature(fn)
    for param in sig.parameters.values():
        if param.default is not inspect.Parameter.empty:
            raise ValueError("Functions with default arguments are not supported")
        if param.kind == param.KEYWORD_ONLY:
            raise ValueError("Functions with keyword-only arguments are not supported")
        if param.kind == param.VAR_POSITIONAL:
            raise ValueError("Functions with *args are not supported")
        if param.kind == param.VAR_KEYWORD:
            raise ValueError("Functions with **kwargs are not supported")
    module = inspect.getmodule(fn)
    module_name = module.__name__ if module is not None else None
    return FunctionCapturedGlobalFunction(
        source=inspect.getsource(fn),
        module=module_name,
        captured_globals=parse_extract_function_object_captured_globals(fn, gas),
        name=fn.__name__,
    )


def _extract_protobuf_enums_directly(mod: ModuleType, module_name: str) -> Dict[str, FunctionCapturedGlobal]:
    """Extract protobuf enums and create intermediate message class globals with full qualified names"""
    all_globals: Dict[str, FunctionCapturedGlobal] = {}

    try:
        # Iterate through all attributes in the module
        for attr_name in dir(mod):
            attr_value = getattr(mod, attr_name)

            # Check if this is a protobuf message class
            if (
                hasattr(attr_value, "DESCRIPTOR")
                and hasattr(attr_value.DESCRIPTOR, "enum_types")
                and not attr_name.startswith("_")
            ):
                descriptor = attr_value.DESCRIPTOR
                enum_names_for_message: Set[str] = set()

                # Extract enum types directly under this message
                for enum_type in descriptor.enum_types:
                    enum_names_for_message.add(enum_type.name)
                    value_to_name_map: Dict[int, str] = {}
                    for enum_value in enum_type.values:
                        value_to_name_map[enum_value.number] = enum_value.name

                    # Create full qualified name for enum
                    enum_full_name = f"{module_name}.{attr_name}.{enum_type.name}"
                    all_globals[enum_full_name] = FunctionCapturedGlobalProtobufEnum(
                        full_qualified_name=enum_full_name, value_to_name_map=value_to_name_map
                    )

                # Extract enum types from nested types
                for nested_type in descriptor.nested_types:
                    for enum_type in nested_type.enum_types:
                        enum_names_for_message.add(f"{nested_type.name}.{enum_type.name}")
                        value_to_name_map: Dict[int, str] = {}
                        for enum_value in enum_type.values:
                            value_to_name_map[enum_value.number] = enum_value.name

                        # Create full qualified name for nested enum
                        enum_full_name = f"{module_name}.{attr_name}.{nested_type.name}.{enum_type.name}"
                        all_globals[enum_full_name] = FunctionCapturedGlobalProtobufEnum(
                            full_qualified_name=enum_full_name, value_to_name_map=value_to_name_map
                        )

                # Create intermediate message class global if it has enums
                if enum_names_for_message:
                    message_class_name = f"{module_name}.{attr_name}"
                    all_globals[message_class_name] = FunctionCapturedGlobalProtobufMessageClass(
                        full_qualified_name=message_class_name,
                        enum_names=FrozenOrderedSet(sorted(enum_names_for_message)),
                    )
    except Exception:
        return {}

    return all_globals


def parse_common_module(
    mod: ModuleType | Any,
) -> FunctionCapturedGlobalModule:
    module_name = mod.__name__

    if (
        mod is math
        or mod is re
        or mod is datetime_module
        or mod is base64
        or mod is hashlib
        or mod is json
        or mod is random
        or mod is difflib
        or mod is requests
        or mod is collections
        or mod is statistics
    ):
        return FunctionCapturedGlobalModule(name=module_name)

    elif mod.__name__ == "pytz":
        try:
            import pytz

            if mod is pytz:
                return FunctionCapturedGlobalModule(name=module_name)
        except ImportError:
            raise ValueError(f"Unsupported module {module_name}")

    elif mod.__name__.startswith("numpy"):
        if check_if_subpackage("numpy", mod.__name__):
            return FunctionCapturedGlobalModule(name=module_name)
    elif mod.__name__.startswith("pandas"):
        if check_if_subpackage("pandas", mod.__name__):
            return FunctionCapturedGlobalModule(name=module_name)
    elif mod.__name__.startswith("polars"):
        if check_if_subpackage("polars", mod.__name__):
            return FunctionCapturedGlobalModule(name=module_name)
    elif mod.__name__.startswith("chalk"):
        import chalk

        if check_if_subpackage(chalk, mod.__name__):
            return FunctionCapturedGlobalModule(name=module_name)

    # return FunctionCapturedGlobalModule(name=module_name)
    raise ValueError(f"Unsupported module {module_name}")


def capture_global(
    *,
    module_name: str | None,
    global_var: str,
    global_value: Any,
    gas: GasLimit,
) -> FunctionCapturedGlobal | None:
    try:
        return _capture_global(
            module_name=module_name,
            global_var=global_var,
            global_value=global_value,
            gas=gas,
        )
    except Exception as e:
        _logger.error(
            f"Error while attempting to capture global '{global_var}' in module '{module_name}' for Python resolver acceleration: {e}"
        )
        return None


def _capture_global(
    *,
    module_name: str | None,
    global_var: str,
    global_value: Any,
    gas: GasLimit,
) -> FunctionCapturedGlobal | None:
    # Check to see if `global_value` is a feature class.
    # Note that we CANNOT trust that the class's namespace matches the `global_var` name.
    if inspect.isclass(global_value):
        try:
            # All feature classes have the field `__chalk_feature_set__` set on them.
            # If these fields are not present, an `AttributeError` will be raised instead.
            if object.__getattribute__(global_value, "__chalk_feature_set__") is True:
                is_feature_set_namespace = global_value.__chalk_namespace__
                if type(is_feature_set_namespace) is str:
                    return FunctionCapturedGlobalFeatureClass(feature_namespace=is_feature_set_namespace)
        except:
            # If there was any kind of exception trying to extract the feature class info from this value,
            # then it is not a `FeatureClass`.
            pass

        try:
            if is_pydantic_basemodel(global_value) or dataclasses.is_dataclass(global_value):
                return FunctionCapturedGlobalStruct(
                    name=global_value.__name__,
                    module=global_value.__module__,
                    pa_dtype=rich_to_pyarrow(global_value, global_value.__name__, False, True),
                )
        except:
            pass
        try:
            if issubclass(global_value, google.protobuf.message.Message):
                return FunctionCapturedGlobalProto.from_typ(global_value)
        except RecursionError as recursion_error:
            # Either the proto structure is too deep or there is an infinitely recursive definition
            raise recursion_error
        except Exception:
            pass

        try:
            if issubclass(global_value, Enum):
                pa_bases: list[pa.DataType] = []
                for base in global_value.__bases__:
                    if base is not Enum and base is not object:
                        if base is int or base is IntEnum:
                            pa_bases.append(pa.int64())
                        elif base is str:
                            pa_bases.append(pa.string())
                        else:
                            raise ValueError(f"Unsupported base type {base}")
                return FunctionCapturedGlobalEnum(
                    name=global_value.__name__,
                    member_map={k: pa.scalar(v.value) for k, v in global_value.__members__.items()},
                    bases=tuple(pa_bases),
                    module=global_value.__module__,
                )
        except:
            pass

    if isinstance(global_value, ModuleType):
        try:
            return parse_common_module(global_value)
        except:
            pass

    if inspect.isfunction(global_value):
        try:
            return parse_helper_function(global_value, gas)
        except:
            pass

    # If global_value is a global value in its module, capture it as a global.
    if hasattr(global_value, "__name__") and hasattr(global_value, "__module__"):
        global_name = global_value.__name__
        global_module_name = global_value.__module__
        if type(global_name) is str and type(global_module_name) is str:
            mod = importlib.import_module(global_value.__module__)
            if hasattr(mod, global_name) and getattr(mod, global_name) is global_value:
                return FunctionCapturedGlobalModuleMember(
                    module_name=global_module_name,
                    qualname=global_name,
                )

    if isinstance(global_value, KafkaSource):
        return FunctionCapturedGlobalVariable(name=global_var, module=module_name)

    # Check if the global value is a callable instance (like ProtobufDeserializer)
    if (
        callable(global_value)
        and not inspect.isfunction(global_value)
        and not inspect.isclass(global_value)
        and not inspect.isbuiltin(global_value)
    ):
        try:
            instance_type = type(global_value).__name__
            # Generate a call signature identifier for the callable instance
            call_signature = f"{instance_type}.__call__"

            # For known callable instances like ProtobufDeserializer, create a specialized capture
            if instance_type in ("ProtobufDeserializer",) and module_name:
                module = importlib.import_module(module_name)
                deserializer = getattr(module, global_var, None)
                if deserializer is None:
                    return None
                if hasattr(deserializer, "_msg_class"):
                    message_class: GeneratedProtocolMessageType = deserializer._msg_class
                    if hasattr(message_class, "DESCRIPTOR"):
                        return FunctionCapturedGlobalCallableProtobufDeserializerInstance(
                            name=global_var,
                            module=module_name,
                            instance_type=instance_type,
                            call_signature=call_signature,
                            # Pyright issue; not sure why hasattr() check above doesn't solve it
                            descriptor=message_class.DESCRIPTOR,  # pyright: ignore[reportAttributeAccessIssue]
                        )
            return None
        except:
            pass

    if isinstance(global_value, (str, int, float, bool, list, set)):
        return FunctionCapturedGlobalVariable(
            name=global_var,
            module=module_name,
        )

    if inspect.isclass(global_value) or inspect.isbuiltin(global_value):
        try:
            parent_module = inspect.getmodule(global_value)
            parsed_module = parse_common_module(parent_module)
            # We use `__qualname__` to guess what the object is, then verify it is as expected.
            if global_value is getattr(parent_module, global_value.__qualname__):
                return FunctionCapturedGlobalModuleMember(
                    module_name=parsed_module.name,
                    qualname=global_value.__qualname__,
                )
        except:
            pass

    return None


@dataclasses.dataclass
class ClosureCapturedValues:
    globals: "dict[str, object]"
    builtins: "dict[str, object]"


def get_closure_vars_including_comprehensions(fn: Callable[..., Any]):
    """
    Returns globals captured by the function or by any inner functions scopes from list comprehensions.
    """
    closure = inspect.getclosurevars(fn)

    # __globals__["__builtins__"] is either a dict or a module
    builtins_ns = fn.__globals__.get("__builtins__", builtins.__dict__)
    if isinstance(builtins_ns, ModuleType):
        builtins_ns = builtins_ns.__dict__
    captured_globals = dict(closure.globals)
    captured_builtins = dict(closure.builtins)

    _visited: "set[types.CodeType]" = set()

    def _visit_code(code: types.CodeType) -> None:
        if code in _visited:
            return
        _visited.add(code)
        for name in code.co_names:
            if name not in captured_globals and name in fn.__globals__:
                captured_globals[name] = fn.__globals__[name]
            elif name not in captured_builtins and name in builtins_ns:
                captured_builtins[name] = builtins_ns[name]
        for const in code.co_consts:
            if type(const) is types.CodeType:
                _visit_code(const)

    for const in fn.__code__.co_consts:
        if type(const) is types.CodeType:
            _visit_code(const)

    return ClosureCapturedValues(
        globals=captured_globals,
        builtins=captured_builtins,
    )


def parse_extract_function_object_captured_globals(
    fn: Callable[..., Any],
    gas: GasLimit,
) -> Mapping[str, FunctionCapturedGlobal] | None:
    """
    Extracts certain well-known values from the `fn` function's closure variables, to be stored in
    the resolver's metadata:

    - builtin functions (`min`, `max`)
    - feature classes

    For example, given a resolver like `my_resolver` in:

    ```
    @features
    class MyFeatures:
        ...

    @online
    def my_resolver(f: MyFeatures.id) -> MyFeatures.value:
      return MyFeatures(value = 42)
    ```

    the global class `MyFeatures` is captured as a `FunctionCapturedGlobalFeatureClass`.

    Note that captured values are determined when the resolver is parsed by chalkpy - this
    means that values which depend on environment variables or other context that may change
    between processes or machines are not guaranteed to be preserved.

    For this reason, ONLY builtins and feature-classes are currently recorded, since these are
    unlikely to be substituted for alternative values.
    """
    gas.consume_gas()
    function_captured_globals: dict[str, FunctionCapturedGlobal] | None = {}
    fn_closure_vars = get_closure_vars_including_comprehensions(fn)
    function_module = inspect.getmodule(fn)

    module_name = function_module.__name__ if function_module is not None else None
    for builtin_var in fn_closure_vars.builtins:
        function_captured_globals[builtin_var] = FunctionCapturedGlobalBuiltin(builtin_name=builtin_var)

    for global_var, global_value in fn_closure_vars.globals.items():
        # Special handling for protobuf modules - extract enums directly. We need to handle this separartely because there may be multiple globals to capture
        if isinstance(global_value, ModuleType) and global_value.__name__.endswith("_pb2"):
            # First, capture the base module itself
            function_captured_globals[global_var] = FunctionCapturedGlobalModule(name=global_var)

            # Then, extract and capture enum globals
            enum_globals = _extract_protobuf_enums_directly(global_value, global_var)
            function_captured_globals.update(enum_globals)
        else:
            captured = capture_global(
                module_name=module_name,
                global_var=global_var,
                global_value=global_value,
                gas=gas,
            )
            if captured is not None:
                function_captured_globals[global_var] = captured

    if not function_captured_globals:
        function_captured_globals = None

    return function_captured_globals


def _validate_dataframe(
    df: DataFrameMeta, error_builder: ResolverErrorBuilder, fqn: Optional[str] = None, arg_index: Optional[int] = None
):
    if fqn is not None:
        feature = Feature.from_root_fqn(fqn)
        if feature.joined_class is not None:
            namespace = feature.joined_class.namespace
        else:
            namespace = None
    else:
        namespace = None
    input_output_string = "output" if arg_index is None else "input"
    path_string = f"at '{fqn}' " if fqn is not None else ""
    for feature in df.columns:
        if feature.namespace == PSEUDONAMESPACE:
            continue
        if namespace is not None and feature.root_namespace != namespace:
            if fqn is None:
                node_range = (
                    error_builder.function_return_annotation()
                    if arg_index is None
                    else error_builder.function_arg_annotation_by_index(arg_index)
                )
                error_builder.add_diagnostic(
                    message=(
                        f"Resolver has DataFrame {input_output_string}s {path_string}with different namespaces,"
                        f" '{namespace}' and '{feature.namespace}'."
                        f" DataFrames can only have features from the same feature class."
                    ),
                    code="161",
                    label="different namespaces",
                    range=node_range,
                    raise_error=ValueError,
                )
            else:
                node_range = (
                    error_builder.function_return_annotation()
                    if arg_index is None
                    else error_builder.function_arg_annotation_by_index(arg_index)
                )
                error_builder.add_diagnostic(
                    message=(
                        f"Resolver has DataFrame {input_output_string}s {path_string}with columns of the wrong namespace,"
                        f" Columns must be features of feature class '{namespace}', but found feature '{feature.fqn}'."
                    ),
                    code="161",
                    label="wrong namespace",
                    range=node_range,
                    raise_error=ValueError,
                )
            break
        namespace = feature.root_namespace


def _validate_feature_reference_collection(
    features: Collection[Any],
    error_builder: ResolverErrorBuilder,
    fqn: str,
    argument_name: str,
    outputs: Type[Features] | None,
) -> tuple[Feature, ...]:
    output_features = _flatten_features(outputs)
    if not isinstance(features, collections.abc.Collection):  # pyright: ignore[reportUnnecessaryIsInstance]
        features = [features]
    feature_list: list[Feature] = []
    for f in features:
        if isinstance(f, str):
            try:
                f = Feature.from_root_fqn(f)
            except:
                error_builder.add_diagnostic(
                    message=(
                        f"Resolver '{fqn}' refers to {f} in decorator argument '{argument_name}' which is not a feature."
                    ),
                    code="109a",
                    label=f"invalid '{argument_name}' parameter",
                    range=error_builder.function_decorator_arg_by_name(argument_name),
                    raise_error=TypeError,
                )
                continue
        if isinstance(f, FeatureWrapper):
            f = unwrap_feature(f)
        if isinstance(f, Feature):
            if f not in output_features:
                error_builder.add_diagnostic(
                    message=(
                        f"Resolver '{fqn}' refers to {f} in decorator argument '{argument_name}',"
                        f"but the resolver does not return this feature."
                    ),
                    code="109b",
                    label=f"invalid '{argument_name}' parameter",
                    range=error_builder.function_decorator_arg_by_name(argument_name),
                    raise_error=TypeError,
                )
                continue
            if f in feature_list:
                error_builder.add_diagnostic(
                    message=(
                        f"Resolver '{fqn}' refers to the same feature {f} in decorator argument '{argument_name}' "
                        f"multiple times."
                    ),
                    code="109c",
                    label=f"invalid '{argument_name}' parameter",
                    range=error_builder.function_decorator_arg_by_name(argument_name),
                    raise_error=TypeError,
                )
            feature_list.append(f)

    return tuple(feature_list)


def simplify_function_definition(text: str) -> str:
    lines = text.split("\n")
    if lines[0].startswith("@"):
        lines = lines[1:]
    open_parentheses_count = 0
    started = False
    definition_lines: List[str] = []
    for line in lines:
        if "(" in line:
            open_parentheses_count += line.count("(")
            started = True
        if ")" in line:
            open_parentheses_count -= line.count(")")
            started = True
        definition_lines.append(line)
        if started is True and open_parentheses_count == 0:
            return "\n".join(definition_lines)
    return "\n".join(definition_lines)


def parse_sink_function(
    fn: Callable[P, T],
    glbs: Optional[Dict[str, Any]],
    lcls: Optional[Dict[str, Any]],
    error_builder: ResolverErrorBuilder,
    name: str | None,
) -> SinkResolverParseResult[P, T]:
    fqn = get_resolver_fqn(function=fn, name=name)
    sig = inspect.signature(fn)
    annotation_parser = ResolverAnnotationParser(fn, glbs, lcls, error_builder)
    function_definition = None
    if not should_skip_source_code_parsing():
        try:
            function_definition = inspect.getsource(fn)
        except:
            pass
    annotations = [annotation_parser.parse_annotation(p) for p in sig.parameters.keys()]

    if len(annotations) == 1 and isinstance(annotations[0], type) and issubclass(annotations[0], DataFrame):
        # It looks like the user's function wants a DataFrame of features
        df = annotations[0]
        features = df.columns

        return SinkResolverParseResult(
            fqn=fqn,
            input_is_df=True,
            function=fn,
            function_definition=function_definition,
            doc=fn.__doc__,
            input_feature_defaults=[None for _ in range(len(features))],
            input_features=list(features),
        )

    else:
        # It looks like the user's function wants features as individual parameters
        feature_default_values: list[Optional[ResolverArgErrorHandler]] = []
        feature_inputs = []

        for i, (arg_name, parameter) in enumerate(sig.parameters.items()):
            arg = annotations[i]
            default_value = None
            if isinstance(arg, FeatureWrapper):
                # Unwrap anything that is wrapped with FeatureWrapper
                arg = unwrap_feature(arg)

            bad_input_message = (
                f"Sink resolver inputs must be Features. Received {str(arg)} for argument '{arg_name}' for '{fqn}'.\n"
            )

            if get_origin(arg) in (UnionType, Union):  # Optional[] handling
                args = get_args(arg)
                if len(args) != 2:
                    error_builder.add_diagnostic(
                        message=bad_input_message,
                        code="92",
                        label="invalid input",
                        range=error_builder.function_arg_annotation_by_name(arg_name),
                        raise_error=ValueError,
                    )
                if type(None) not in args:
                    error_builder.add_diagnostic(
                        message=bad_input_message,
                        code="92",
                        label="invalid input",
                        range=error_builder.function_arg_annotation_by_name(arg_name),
                        raise_error=ValueError,
                    )
                real_arg = next((a for a in args if a is not type(None)), None)
                if real_arg is None:
                    error_builder.add_diagnostic(
                        message=bad_input_message,
                        code="92",
                        label="invalid input",
                        range=error_builder.function_arg_annotation_by_name(arg_name),
                        raise_error=ValueError,
                    )
                default_value = ResolverArgErrorHandler(None)
                arg = unwrap_feature(real_arg)

            if not isinstance(arg, Feature):
                error_builder.add_diagnostic(
                    message=bad_input_message,
                    code="92",
                    label="invalid input",
                    range=error_builder.function_arg_annotations()[arg_name],
                    raise_error=ValueError,
                )

            if parameter.empty != parameter.default:
                default_value = ResolverArgErrorHandler(parameter.default)

            feature_default_values.append(default_value)
            feature_inputs.append(arg)

        return SinkResolverParseResult(
            fqn=fqn,
            input_features=feature_inputs,
            function=fn,
            function_definition=function_definition,
            doc=fn.__doc__,
            input_is_df=False,
            input_feature_defaults=feature_default_values,
        )


@overload
def online(
    *,
    environment: Optional[Environments] = None,
    tags: Optional[Tags] = None,
    cron: CronTab | Duration | Cron | None = None,
    machine_type: Optional[MachineType] = None,
    owner: Optional[str] = None,
    timeout: Optional[Duration] = None,
    name: str | None = None,
    resource_hint: ResourceHint | None = None,
    static: bool = False,
    total: bool = False,
    unique_on: Collection[Any] | None = None,
    partitioned_by: Collection[Any] | None = None,
    resource_group: str | None = None,
    output_row_order: Literal["one-to-one"] | None = None,
    venv: str | None = None,
) -> Callable[[Callable[P, T]], ResolverProtocol[P, T]]:
    ...


@overload
def online(
    fn: Callable[P, T],
    /,
) -> ResolverProtocol[P, T]:
    ...


def online(
    fn: Callable[P, T] | None = None,
    /,
    *,
    environment: Environments | None = None,
    tags: Tags | None = None,
    cron: CronTab | Duration | Cron | None = None,
    machine_type: MachineType | None = None,
    owner: str | None = None,
    timeout: Duration | None = None,
    name: str | None = None,
    resource_hint: ResourceHint | None = None,
    static: bool = False,
    total: bool = False,
    unique_on: Collection[Any] | None = None,
    partitioned_by: Collection[Any] | None = None,
    resource_group: str | None = None,
    output_row_order: Literal["one-to-one"] | None = None,
    venv: str | None = None,
) -> Union[Callable[[Callable[P, T]], ResolverProtocol[P, T]], ResolverProtocol[P, T]]:
    """Decorator to create an online resolver.

    Parameters
    ----------
    environment
        Environments are used to trigger behavior
        in different deployments such as staging, production, and
        local development. For example, you may wish to interact with
        a vendor via an API call in the production environment, and
        opt to return a constant value in a staging environment.

        Environment can take one of three types:
            - `None` (default) - candidate to run in every environment
            - `str` - run only in this environment
            - `list[str]` - run in any of the specified environment and no others

        Read more at https://docs.chalk.ai/docs/resolver-environments
    owner
        Individual or team responsible for this resolver.
        The Chalk Dashboard will display this field, and alerts
        can be routed to owners.
    tags
        Allow you to scope requests within an
        environment. Both tags and environment need to match for a
        resolver to be a candidate to execute.

        You might consider using tags, for example, to change out
        whether you want to use a sandbox environment for a vendor,
        or to bypass the vendor and return constant values in a
        staging environment.

        Read more at https://docs.chalk.ai/docs/resolver-tags
    cron
        You can schedule resolvers to run on a pre-determined
        schedule via the cron argument to resolver decorators.

        Cron can sample all examples, a subset of all examples,
        or a custom provided set of examples.

        Read more at https://docs.chalk.ai/docs/resolver-cron
    timeout
        You can specify the maximum `Duration` to wait for the
        resolver's result. Once the resolver's runtime exceeds
        the specified duration, a timeout error will be returned
        along with each output feature.

        Read more at https://docs.chalk.ai/docs/timeout.
    resource_hint
        Whether this resolver is bound by CPU, I/O, or GPU. Chalk uses
        the resource hint to optimize resolver execution.
    static
        Whether this resolver should be invoked once during planning time
        to build a static computation graph. If `True`, all inputs will
        either be `StaticOperators` (for has-many and `DataFrame` relationships)
        or `StaticExpressions` (for individual features). The resolver must
        return a `StaticOperator` as output.

    Other Parameters
    ----------------
    fn
        The function that you're decorating as a resolver.
    machine_type
        You can optionally specify that resolvers need to run on a
        machine other than the default. Must be configured in your
        deployment.
    name
        An alternative short name for the resolver, to use instead of the function name.
    total
        Whether this resolver returns all ids of a given namespace.
        To have this annotation, the resolver must take no arguments
        and return a `DataFrame`. Typically, this annotation would
        be used in a SQL-file resolver.
    unique_on
        A list of features that must be unique for each row of the output.
        This enables unique optimizations in the resolver execution.
        Only applicable to resolvers that return a DataFrame.
    partitioned_by
        A list of features that correspond to partition keys in the data source.
        This field indicates that this resolver executes its query against a data storage system that is
        partitioned by a particular set of columns.
        This is most common with data-warehouse sources like Snowflake, BigQuery or Databricks.
    resource_group
        The resource group for the resolver: this is used to isolate execution of
        the resolver onto a separate pod (or set of nodes), allowing model inference
        to be run in a separate environment, such as on a GPU-enabled node.
    output_row_order
        If set to "one-to-one", signals the planner that this resolver is logically equivalent
        to a batched scalar resolver. A resolver marked `output_row_order="one-to-one"` must adhere
        to the following constraints:

            - the resolver must take in one dataframe input and return a dataframe output
            - both the input and the output must have the pkey column
            - the operation must be logically one-to-one - ie all corresponding input rows have a corresponding output row
            - the order of the rows must be preserved

        Here is an example resolver that can be marked one-to-one to batch the account_ids lookup

        >>> @online(output_row_order="one-to-one")
        ... def my_one_to_one_df_resolver(
        ...     input: DataFrame[User.id, User.account_info]
        ... ) -> DataFrame[User.id, User.account_ids]:
        ...     input_as_pydict = input.to_pyarrow().to_pydict()
        ...     info_to_ids_map = get_batch_info_to_ids_map(input_as_pydict)
        ...     return DataFrame({
        ...         User.id: input_as_pydict[str(User.id)],
        ...         User.account_info: [
        ...             info_to_ids_map.get(info, []) for info in input_as_pydict[str(User.account_info)]
        ...         ]
        ...     })
    venv
        A virtual environment to use for the resolver. This is used to isolate the resolver
        from the default requirements, allowing different versions of packages to be used.

    Returns
    -------
    Callable[[Callable[P, T]], ResolverProtocol[P, T]] | ResolverProtocol[P, T]
        A `ResolverProtocol` which can be called as a normal function! You can unit-test
        resolvers as you would unit-test any other code.

        Read more at https://docs.chalk.ai/docs/unit-tests

    Examples
    --------
    >>> @online
    ... def name_match(
    ...     name: User.full_name,
    ...     account_name: User.bank_account.title
    ... ) -> User.account_name_match_score:
    ...     if name.lower() == account_name.lower():
    ...         return 1.
    ...     return 0.
    """
    frame = inspect.currentframe()
    assert frame is not None
    caller_frame = frame.f_back
    assert caller_frame is not None
    caller_globals = caller_frame.f_globals
    caller_locals = caller_frame.f_locals
    del frame

    def decorator(fn: Callable[P, T]):
        caller_filename = inspect.getsourcefile(fn) or "<unknown file>"
        try:
            caller_lines = inspect.getsourcelines(fn) or None
        except:
            caller_lines = None
        error_builder = get_resolver_error_builder(fn)

        parse_fn = parse_function(
            fn=fn,
            glbs=caller_globals,
            lcls=caller_locals,
            error_builder=error_builder,
            name=name,
            validate_output=True,
            unique_on=unique_on,
            partitioned_by=partitioned_by,
        )

        resolver = OnlineResolver(
            filename=caller_filename,
            function_definition=None,
            function_captured_globals=None,
            fqn=get_resolver_fqn(function=fn, name=name),
            doc=None,
            inputs=None,
            output=None,
            fn=fn,
            environment=None if environment is None else list(ensure_tuple(environment)),
            tags=None if tags is None else list(ensure_tuple(tags)),
            cron=cron,
            machine_type=machine_type,
            owner=owner,
            state=None,
            default_args=None,
            timeout=timeout,
            source_line=None if caller_lines is None else caller_lines[1],
            lsp_builder=error_builder,
            data_sources=None,
            is_sql_file_resolver=False,
            parse=parse_fn,
            resource_hint=resource_hint,
            static=static,
            total=total,
            autogenerated=False,
            unique_on=None,  # these two will be parsed correctly when parse_fn is evaluated
            partitioned_by=None,
            data_lineage=None,
            sql_settings=None,
            resource_group=resource_group,
            output_row_order=output_row_order,
            venv=venv,
        )

        resolver.add_to_registry(override=False)
        # Return the decorated resolver, which notably implements __call__() so it acts the same as
        # the underlying function if called directly, e.g. from test code
        return resolver

    return decorator(fn) if fn else decorator


@overload
def offline(
    *,
    environment: Environments | None = None,
    tags: Tags | None = None,
    cron: CronTab | Duration | Cron | None = None,
    machine_type: MachineType | None = None,
    owner: str | None = None,
    name: str | None = None,
    resource_hint: ResourceHint | None = None,
    static: bool = False,
    total: bool = False,
    unique_on: Collection[Any] | None = None,
    partitioned_by: Collection[Any] | None = None,
    output_row_order: Literal["one-to-one"] | None = None,
    venv: str | None = None,
) -> Callable[[Callable[P, T]], ResolverProtocol[P, T]]:
    ...


@overload
def offline(
    fn: Callable[P, T],
    /,
) -> ResolverProtocol[P, T]:
    ...


def offline(
    fn: Optional[Callable[P, T]] = None,
    /,
    *,
    environment: Environments | None = None,
    tags: Tags | None = None,
    cron: CronTab | Duration | Cron | None = None,
    machine_type: MachineType | None = None,
    owner: str | None = None,
    timeout: Duration | None = None,
    name: str | None = None,
    resource_hint: ResourceHint | None = None,
    static: bool = False,
    total: bool = False,
    unique_on: Collection[Any] | None = None,
    partitioned_by: Collection[Any] | None = None,
    output_row_order: Literal["one-to-one"] | None = None,
    venv: str | None = None,
) -> Union[Callable[[Callable[P, T]], Callable[P, T]], ResolverProtocol[P, T]]:
    """Decorator to create an offline resolver.

    Parameters
    ----------
    environment
        Environments are used to trigger behavior
        in different deployments such as staging, production, and
        local development. For example, you may wish to interact with
        a vendor via an API call in the production environment, and
        opt to return a constant value in a staging environment.

        Environment can take one of three types:
            - `None` (default) - candidate to run in every environment
            - `str` - run only in this environment
            - `list[str]` - run in any of the specified environment and no others

        Read more at https://docs.chalk.ai/docs/resolver-environments
    owner
        Allows you to specify an individual or team
        who is responsible for this resolver. The Chalk Dashboard
        will display this field, and alerts can be routed to owners.
    tags
        Allow you to scope requests within an
        environment. Both tags and environment need to match for a
        resolver to be a candidate to execute.

        You might consider using tags, for example, to change out
        whether you want to use a sandbox environment for a vendor,
        or to bypass the vendor and return constant values in a
        staging environment.

        Read more at https://docs.chalk.ai/docs/resolver-tags
    cron
        You can schedule resolvers to run on a pre-determined
        schedule via the cron argument to resolver decorators.

        Cron can sample all examples, a subset of all examples,
        or a custom provided set of examples.

        Read more at https://docs.chalk.ai/docs/resolver-cron
    timeout
        You can specify the maximum `Duration` to wait for the
        resolver's result. Once the resolver's runtime exceeds
        the specified duration, a timeout error will be raised.

        Read more at https://docs.chalk.ai/docs/timeout.
    resource_hint
        Whether this resolver is bound by CPU or I/O. Chalk uses
        the resource hint to optimize resolver execution.
    static
        Whether this resolver should be invoked once during planning time to
        build a static computation graph. If `True`, all inputs will either
        be `StaticOperators` (for has-many and dataframe relationships) or
        `StaticExpressions` (for individual features). The resolver must
        return a `StaticOperator` as output.
    total
        Whether this resolver returns all ids of a given namespace.
        To have this annotation, the resolver must take no arguments
        and return a `DataFrame`. Typically, this annotation would
        be used in a SQL-file resolver.

    Other Parameters
    ----------------
    fn
        The function that you're decorating as a resolver.
    machine_type
        You can optionally specify that resolvers need to run on
        a machine other than the default. Must be configured in
        your deployment.
    name
        An alternative short name for the resolver, to use instead of the function name.
    unique_on
        A list of features that must be unique for each row of the output.
        This enables unique optimizations in the resolver execution.
        Only applicable to resolvers that return a DataFrame.
    partitioned_by
        A list of features that correspond to partition keys in the data source.
        This field indicates that this resolver executes its query against a data storage system that is
        partitioned by a particular set of columns.
        This is most common with data-warehouse sources like Snowflake, BigQuery or Databricks.
    output_row_order
        If set to "one-to-one", signals the planner that this resolver is logically equivalent
        to a batched scalar resolver. A resolver marked `output_row_order="one-to-one"` must adhere
        to the following constraints:

            - the resolver must take in one dataframe input and return a dataframe output
            - both the input and the output must have the pkey column
            - the operation must be logically one-to-one - ie all corresponding input rows have a corresponding output row
            - the order of the rows must be preserved

        Here is an example resolver that can be marked one-to-one to batch the account_ids lookup

        >>> @offline(output_row_order="one-to-one")
        ... def my_one_to_one_df_resolver(
        ...     input: DataFrame[User.id, User.account_info]
        ... ) -> DataFrame[User.id, User.account_ids]:
        ...     input_as_pydict = input.to_pyarrow().to_pydict()
        ...     info_to_ids_map = get_batch_info_to_ids_map(input_as_pydict)
        ...     return DataFrame({
        ...         User.id: input_as_pydict[str(User.id)],
        ...         User.account_info: [
        ...             info_to_ids_map.get(info, []) for info in input_as_pydict[str(User.account_info)]
        ...         ]
        ...     })
    venv
        A virtual environment to use for the resolver. This is used to isolate the resolver
        from the default requirements, allowing different versions of packages to be used.

    Returns
    -------
    Union[Callable[[Callable[P, T]], ResolverProtocol[P, T]], ResolverProtocol[P, T]]
        A `ResolverProtocol` which can be called as a normal function! You can unit-test
        resolvers as you would unit-test any other code.

        Read more at https://docs.chalk.ai/docs/unit-tests

    Examples
    --------
    >>> @offline(cron="1h")
    ... def get_fraud_score(
    ...     email: User.email,
    ...     name: User.name,
    ... ) -> User.fraud_score:
    ...     return socure.get_sigma_score(email, name)
    """
    frame = inspect.currentframe()
    assert frame is not None
    caller_frame = frame.f_back
    assert caller_frame is not None
    caller_globals = caller_frame.f_globals
    caller_locals = caller_frame.f_locals
    caller_line = caller_frame.f_lineno
    del frame

    def decorator(fn: Callable[P, T]):
        caller_filename = inspect.getsourcefile(fn) or "<unknown file>"
        error_builder = get_resolver_error_builder(fn)
        parse_fn = parse_function(
            fn=fn,
            glbs=caller_globals,
            lcls=caller_locals,
            error_builder=error_builder,
            validate_output=True,
            unique_on=unique_on,
            partitioned_by=partitioned_by,
        )
        resolver = OfflineResolver(
            filename=caller_filename,
            function_definition=None,
            function_captured_globals=None,
            fqn=get_resolver_fqn(function=fn, name=name),
            doc=None,
            inputs=None,
            output=None,
            fn=fn,
            environment=None if environment is None else list(ensure_tuple(environment)),
            tags=None if tags is None else list(ensure_tuple(tags)),
            cron=cron,
            machine_type=machine_type,
            state=None,
            owner=owner,
            default_args=None,
            timeout=timeout,
            source_line=caller_line,
            lsp_builder=error_builder,
            is_sql_file_resolver=False,
            data_sources=None,
            parse=parse_fn,
            resource_hint=resource_hint,
            static=static,
            total=total,
            autogenerated=False,
            unique_on=None,  # these two will be parsed correctly when parse_fn is evaluated
            partitioned_by=None,
            data_lineage=None,
            sql_settings=None,
            output_row_order=output_row_order,
            venv=venv,
        )
        resolver.add_to_registry(override=False)
        return resolver

    return decorator(fn) if fn else decorator


@overload
def sink(
    *,
    environment: Environments | None = None,
    tags: Tags | None = None,
    machine_type: MachineType | None = None,
    buffer_size: int | None = None,
    debounce: Duration | None = None,
    max_delay: Duration | None = None,
    upsert: bool = False,
    integration: BaseSQLSourceProtocol | SinkIntegrationProtocol | None = None,
    owner: str | None = None,
) -> Callable[[Callable[P, T]], ResolverProtocol[P, T]]:
    ...


@overload
def sink(
    fn: Callable[P, T],
    /,
) -> ResolverProtocol[P, T]:
    ...


def sink(
    fn: Callable[P, T] | None = None,
    /,
    *,
    environment: Environments | None = None,
    tags: Tags | None = None,
    machine_type: MachineType | None = None,
    buffer_size: int | None = None,
    debounce: Duration | None = None,
    max_delay: Duration | None = None,
    upsert: bool = False,
    integration: BaseSQLSourceProtocol | SinkIntegrationProtocol | None = None,
    owner: str | None = None,
    name: str | None = None,
) -> Union[Callable[[Callable[P, T]], ResolverProtocol[P, T]], ResolverProtocol[P, T]]:
    """Decorator to create a sink.
    Read more at https://docs.chalk.ai/docs/sinks

    Parameters
    ----------
    environment
        Environments are used to trigger behavior
        in different deployments such as staging, production, and
        local development. For example, you may wish to interact with
        a vendor via an API call in the production environment, and
        opt to return a constant value in a staging environment.

        Environment can take one of three types:
            - `None` (default) - candidate to run in every environment
            - `str` - run only in this environment
            - `list[str]` - run in any of the specified environment and no others

        Read more at https://docs.chalk.ai/docs/resolver-environments
    tags
        Allow you to scope requests within an
        environment. Both tags and environment need to match for a
        resolver to be a candidate to execute.

        You might consider using tags, for example, to change out
        whether you want to use a sandbox environment for a vendor,
        or to bypass the vendor and return constant values in a
        staging environment.

        Read more at https://docs.chalk.ai/docs/resolver-tags
    buffer_size
        Count of updates to buffer.
    owner
        The individual or team responsible for this resolver.
        The Chalk Dashboard will display this field, and alerts
        can be routed to owners.

    Other Parameters
    ----------------
    fn
        The function that you're decorating as a resolver.
    machine_type
        You can optionally specify that resolvers need to run on a
        machine other than the default. Must be configured in your
        deployment.
    name
        An alternative short name for the resolver, to use instead of the function name.
    debounce
    max_delay
    upsert
    integration

    Examples
    --------
    >>> @sink
    ... def process_updates(
    ...     uid: User.id,
    ...     email: User.email,
    ...     phone: User.phone,
    ... ):
    ...     user_service.update(
    ...         uid=uid,
    ...         email=email,
    ...         phone=phone
    ...     )
    >>> process_updates(123, "sam@chalk.ai", "555-555-5555")

    Returns
    -------
    Callable[[Any, ...], Any]
        A callable function! You can unit-test sinks as you
        would unit test any other code.
        Read more at https://docs.chalk.ai/docs/unit-tests
    """
    frame = inspect.currentframe()
    assert frame is not None
    caller_frame = frame.f_back
    assert caller_frame is not None
    caller_globals = caller_frame.f_globals
    caller_locals = caller_frame.f_locals
    caller_line = caller_frame.f_lineno

    def decorator(fn: Callable[P, T]):
        caller_filename = inspect.getsourcefile(fn) or "unknown_file"
        error_builder = get_resolver_error_builder(fn)
        parsed = parse_sink_function(fn, caller_globals, caller_locals, error_builder, name=name)
        # TODO: lazily parse
        resolver = SinkResolver(
            filename=caller_filename,
            function_definition=parsed.function_definition,
            function_captured_globals=None,
            fqn=parsed.fqn,
            doc=parsed.doc,
            inputs=parsed.input_features,
            fn=fn,
            environment=None if environment is None else list(ensure_tuple(environment)),
            tags=None if tags is None else list(ensure_tuple(tags)),
            machine_type=machine_type,
            buffer_size=buffer_size,
            debounce=debounce,
            max_delay=max_delay,
            upsert=upsert,
            integration=integration,
            owner=owner,
            default_args=parsed.input_feature_defaults,
            input_is_df=parsed.input_is_df,
            source_line=caller_line,
            lsp_builder=error_builder,
            data_sources=None,
        )
        resolver.add_to_registry(override=False)
        return resolver

    return decorator(fn) if fn else decorator


class StreamResolver(Resolver[P, T]):
    def __init__(
        self,
        *,
        function_definition: str | None,
        function_captured_globals: Mapping[str, FunctionCapturedGlobal] | None = None,
        fqn: str,
        filename: str,
        source: StreamSource,
        fn: Callable[P, T],
        environment: list[str] | None,
        doc: str | None,
        mode: Literal["continuous", "tumbling"] | None,
        machine_type: str | None,
        message: Type[Any] | None,
        output: Type[Features],
        signature: StreamResolverSignature,
        state: StateDescriptor | None,
        sql_query: str | None,
        owner: str | None,
        parse: ParseInfo | None,
        keys: dict[str, Any] | None,
        timestamp: str | None,
        source_line: int | None,
        tags: list[str] | None,
        lsp_builder: ResolverErrorBuilder,
        autogenerated: bool,
        updates_materialized_aggregations: bool,
        sql_settings: SQLResolverSettings | None,
        feature_expressions: dict[Feature, Underscore] | None,
        message_producer_parsed: StreamResolverMessageProducerParsed | None,
        skip_online: bool = False,
        skip_offline: bool = False,
    ):
        super().__init__(
            function_definition=function_definition,
            function_captured_globals=function_captured_globals,
            lsp_builder=lsp_builder,
            filename=filename,
            environment=environment,
            machine_type=machine_type,
            fqn=fqn,
            fn=fn,
            doc=doc,
            inputs=[],
            output=output,
            tags=tags,
            cron=None,
            when=None,
            state=state,
            default_args=[],
            owner=owner,
            source_line=source_line,
            timeout=None,
            is_sql_file_resolver=False,
            data_sources=None,
            parse=None,
            resource_hint=None,
            static=False,
            total=False,
            autogenerated=autogenerated,
            unique_on=None,
            partitioned_by=None,
            data_lineage=None,
            sql_settings=sql_settings,
        )
        self.source = source
        self.message = message
        self.mode = mode
        self.signature = signature
        self.sql_query = sql_query
        self.parse = parse
        self.keys = keys
        self.timestamp = timestamp
        self.updates_materialized_aggregations = updates_materialized_aggregations
        fqn_to_windows = {o.fqn: o.window_durations for o in _flatten_features(self.output) if o.is_windowed}
        if len(set(tuple(v) for v in fqn_to_windows.values())) > 1:
            fqn_to_declared_windows = {
                o.fqn: sorted(o.window_durations) for o in _flatten_features(self.output) if o.is_windowed
            }
            periods = [f"{fqn}[{', '.join(f'{window}s')}]" for fqn, window in fqn_to_declared_windows.items()]
            raise ValueError(f"All features must have the same window periods. Found {', '.join(periods)}")
        self.window_periods_seconds = next(iter(fqn_to_windows.values()), ())
        # Mapping of window (in secs) to mapping of (original feature, windowed pseudofeature)
        self.windowed_pseudofeatures: Dict[int, Dict[Feature, Feature]] = {}
        self.window_index = None
        for i, w in enumerate(signature.params):
            if isinstance(w, StreamResolverParamMessageWindow):
                self.window_index = i
                break

        for window_period in self.window_periods_seconds:
            self.windowed_pseudofeatures[window_period] = {}
            for o in _flatten_features(self.output):
                if o.is_windowed:
                    windowed_fqn = get_name_with_duration(o.root_fqn, window_period)
                    windowed_feature = Feature.from_root_fqn(windowed_fqn)
                    self.windowed_pseudofeatures[window_period][o] = windowed_feature

        self.feature_expressions: dict[Feature, Underscore] | None = feature_expressions
        self.message_producer_parsed: StreamResolverMessageProducerParsed | None = message_producer_parsed
        self.skip_online = skip_online
        self.skip_offline = skip_offline

    @property
    def output_features(self) -> Sequence[Feature]:
        return _flatten_features(self.output)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        from chalk._autosql.autosql import query_as_feature_formatted

        raw_result = self.fn(*args, **kwargs)
        if self.window_index is not None and isinstance(raw_result, str) and str(args[self.window_index]) in raw_result:
            raw_result = DataFrame(
                query_as_feature_formatted(
                    formatted_query=raw_result,
                    fqn_to_name={s.root_fqn: s.name for s in self.output_features},
                    table=args[self.window_index],
                )
            )

        return cast(T, raw_result)

    def __repr__(self):
        return f"StreamResolver(name={self.fqn})"


def _is_stream_resolver_body_type(annotation: Type):
    origin = get_origin(annotation)
    if origin is not None:
        return False
    return (
        isinstance(annotation, type)  # pyright: ignore[reportUnnecessaryIsInstance]
        and (issubclass(annotation, (str, bytes)) or is_pydantic_basemodel(annotation))
    ) or dataclasses.is_dataclass(annotation)


def _parse_stream_resolver_param(
    param: Parameter,
    annotation_parser: ResolverAnnotationParser,
    resolver_fqn_for_errors: str,
    is_windowed_resolver: bool,
    error_builder: ResolverErrorBuilder,
) -> StreamResolverParam:
    if param.kind not in {Parameter.KEYWORD_ONLY, Parameter.POSITIONAL_OR_KEYWORD}:
        error_builder.add_diagnostic(
            message=(
                f"Stream resolver '{resolver_fqn_for_errors}' includes unsupported keyword or variadic arg '{param.name}'"
            ),
            code="120",
            label="invalid stream resolver parameter",
            range=error_builder.function_arg_annotation_by_name(param.name),
            raise_error=ValueError,
        )

    annotation = annotation_parser.parse_annotation(param.name)
    if isinstance(annotation, StateWrapper):
        if is_windowed_resolver:
            error_builder.add_diagnostic(
                message=(
                    f"Windowed stream resolvers cannot have state, but '{resolver_fqn_for_errors}' requires state."
                ),
                code="121",
                label="invalid state parameter",
                range=error_builder.function_arg_annotation_by_name(param.name),
                raise_error=ValueError,
            )
        default_value = get_state_default_value(
            state_typ=annotation.typ,
            declared_default=param.default,
            resolver_fqn_for_errors=resolver_fqn_for_errors,
            parameter_name_for_errors=param.name,
            error_builder=error_builder,
        )
        return StreamResolverParamKeyedState(
            name=param.name,
            typ=annotation.typ,
            default_value=default_value,
        )

    if not is_windowed_resolver and _is_stream_resolver_body_type(annotation):
        return StreamResolverParamMessage(name=param.name, typ=annotation)

    if is_windowed_resolver and get_origin(annotation) in (list, List):
        item_typ = get_args(annotation)[0]
        if _is_stream_resolver_body_type(item_typ):
            return StreamResolverParamMessageWindow(name=param.name, typ=annotation)

    if (
        is_windowed_resolver
        and isclass(annotation)
        and (
            issubclass(annotation, pyarrow.Table)
            or is_pydantic_basemodel(annotation)
            or annotation.__name__ in ("DataFrame", "DataFrameImpl", "SubclassedDataFrame")
        )
    ):
        # Using string comparison as polars may not be installed
        return StreamResolverParamMessageWindow(name=param.name, typ=annotation)
    error_builder.add_diagnostic(
        message=(
            f"Stream resolver parameter '{param.name}' of resolver '{resolver_fqn_for_errors}' is not recognized. "
            "Message payloads must be one of `str`, `bytes`, or pydantic model class. "
            "Keyed state parameters must be chalk.KeyedState[T]. "
            f"Received: {annotation}"
        ),
        code="122",
        label="invalid input",
        range=error_builder.function_arg_annotation_by_name(param.name),
        raise_error=ValueError,
    )


def _parse_stream_resolver_params(
    user_func: Callable,
    error_builder: ResolverErrorBuilder,
    *,
    resolver_fqn_for_errors: str,
    annotation_parser: ResolverAnnotationParser,
    is_windowed_resolver: bool,
) -> Sequence[StreamResolverParam]:
    sig = inspect.signature(user_func)
    params = [
        _parse_stream_resolver_param(p, annotation_parser, resolver_fqn_for_errors, is_windowed_resolver, error_builder)
        for p in sig.parameters.values()
    ]
    num_params = len(params)
    if num_params == 1:
        if not isinstance(params[0], (StreamResolverParamMessage, StreamResolverParamMessageWindow)):
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{resolver_fqn_for_errors}' must take as input "
                    "a Pydantic model, `str`, or `bytes` representing the message body. "
                ),
                code="93",
                label="invalid input",
                range=error_builder.function_arg_annotation_by_name(params[0].name),
                raise_error=ValueError,
            )
    elif num_params == 2:
        if isinstance(params[0], StreamResolverParamKeyedState):
            stream_input_model = params[1]
        elif isinstance(params[1], StreamResolverParamKeyedState):
            stream_input_model = params[0]
        else:
            error_builder.add_diagnostic(
                message=(
                    f"Streaming resolver '{resolver_fqn_for_errors}' of length '{num_params}' must have "
                    "exactly one non-State input argument. "
                ),
                code="94",
                label="invalid input",
                range=error_builder.function_arg_annotation_by_name(params[1].name),
                raise_error=ValueError,
            )
            raise  # for type-checking, but the above raises
        if isinstance(stream_input_model, StreamResolverParamKeyedState):
            error_builder.add_diagnostic(
                message=f"Stream resolver '{resolver_fqn_for_errors}' includes more than one KeyedState parameter.",
                code="95",
                label="only one KeyedState parameter permitted",
                range=error_builder.function_arg_annotation_by_name(params[1].name),
                raise_error=ValueError,
            )
        if not isinstance(stream_input_model, (StreamResolverParamMessage, StreamResolverParamMessageWindow)):
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{resolver_fqn_for_errors}' must take as input "
                    "a Pydantic model, `str`, or `bytes` representing the message body. "
                ),
                code="96",
                label="invalid input",
                range=error_builder.function_arg_annotation_by_name(params[0].name),
                raise_error=ValueError,
            )
    else:
        error_builder.add_diagnostic(
            message=(
                f"Streaming resolver '{resolver_fqn_for_errors}' of length '{num_params}' must have "
                "exactly one non-State input argument. "
            ),
            code="97",
            label="invalid input",
            range=error_builder.function_arg_annotation_by_name(params[0].name),
            raise_error=ValueError,
        )

    return params


def _parse_stream_resolver_output_features(
    user_func: Callable,
    error_builder: ResolverErrorBuilder,
    *,
    resolver_fqn_for_errors: str,
) -> Type[Features]:
    return_annotation = cached_get_type_hints(user_func).get("return")
    if return_annotation is None:
        error_builder.add_diagnostic(
            message=f"Resolver '{resolver_fqn_for_errors}' must have a return annotation.",
            code="81",
            label="missing return annotation",
            range=error_builder.function_return_annotation(),
            raise_error=TypeError,
            code_href="https://docs.chalk.ai/docs/python-resolvers#outputs",
        )
    if isinstance(return_annotation, FeatureWrapper):
        return_annotation = Features[unwrap_feature(return_annotation)]

    if not isinstance(return_annotation, type):
        error_builder.add_diagnostic(
            message=(
                f"Resolver '{resolver_fqn_for_errors}' has a return annotation {return_annotation} "
                f"of type {type(return_annotation)}. Resolver return annotation values must be a type. "
            ),
            code="82",
            label="not a type",
            range=error_builder.function_return_annotation(),
            raise_error=TypeError,
        )

    if issubclass(return_annotation, DataFrame):
        return Features[return_annotation]

    if not issubclass(return_annotation, Features):
        error_builder.add_diagnostic(
            message=(
                f"Stream resolver '{resolver_fqn_for_errors}' did not have a valid return type: "
                "must be a features class or Features[...]."
            ),
            code="82",
            label="invalid return type",
            range=error_builder.function_return_annotation(),
            raise_error=TypeError,
        )

    found_primary = False
    found_windowed = False
    namespace = None
    for feature in return_annotation.features:
        if feature.is_windowed_pseudofeature:
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{resolver_fqn_for_errors}' did not have a valid return type: "
                    "For stream resolvers, specific durations should not be specified in the return."
                    "For example, 'A.windowed_feature[\"60m\"]' should be rewritten as 'A.windowed_feature'"
                ),
                code="82",
                label="windowed feature does not need a specified duration",
                range=error_builder.function_return_annotation(),
                raise_error=TypeError,
            )
        if feature.primary:
            found_primary = True
        if feature.is_windowed:
            found_windowed = True
        if namespace is None:
            namespace = feature.root_namespace
        elif namespace != feature.root_namespace:
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{resolver_fqn_for_errors}' returned features with different namespaces. "
                    "Stream resolvers must return features with the same namespace."
                ),
                code="82",
                label="different namespaces",
                range=error_builder.function_return_annotation(),
                raise_error=TypeError,
            )
    if not found_primary and not found_windowed:
        # windowed resolvers don't have to return a primary key
        error_builder.add_diagnostic(
            message=(
                f"Stream resolver '{resolver_fqn_for_errors}' did not return a primary key feature. "
                "Stream resolvers must return a primary key feature."
            ),
            code="82",
            label="missing primary key",
            range=error_builder.function_return_annotation(),
            raise_error=TypeError,
        )

    output_features = return_annotation
    return output_features


def _is_valid_stream_message_type(typ: Type) -> bool:
    from chalk.functions.proto import _is_protobuf_message

    if is_pydantic_basemodel(typ):
        return True
    if is_dataclass(typ):
        return True
    if _is_protobuf_message(typ):
        return True
    return False


@dataclass(frozen=True)
class ParseInfo(Generic[T, V]):
    fn: Callable[[T], V]
    input_type: Type[T]
    output_type: Type[V]
    output_is_optional: bool
    parse_function_captured_globals: Mapping[str, FunctionCapturedGlobal] | None
    parse_expression: Underscore | None


def _validate_parse_function(
    stream_fqn: str,
    parse_fn: Callable[[T], Any],
    globals: dict[str, Any] | None,
    locals: dict[str, Any] | None,
    stream_fn_input_type: Type[Any],
    name: str | None,
) -> ParseInfo:
    parse_error_builder = get_resolver_error_builder(parse_fn)
    """We need separate error builders for resolver and parse fn: different AST nodes"""

    parse_fqn = get_resolver_fqn(function=parse_fn, name=name)
    sig = inspect.signature(parse_fn)
    annotation_parser = ResolverAnnotationParser(parse_fn, globals, locals, parse_error_builder)

    output_optional = False
    return_annotation = cached_get_type_hints(parse_fn).get("return")
    if not return_annotation:
        parse_error_builder.add_diagnostic(
            message=f"Parse function '{parse_fqn}' must have a return annotation.",
            code="98",
            label="missing return annotation",
            range=parse_error_builder.function_return_annotation(),
            raise_error=TypeError,
        )
    if get_origin(return_annotation) in (UnionType, Union):
        return_args = get_args(return_annotation)
        parse_output = next((a for a in return_args if a is not type(None)), None)
        if len(return_args) != 2 or type(None) not in return_args or parse_output is None:
            parse_error_builder.add_diagnostic(
                message=(
                    f"Parse function '{parse_fqn}' return annotation must be a singleton or an optional singleton."
                ),
                code="99",
                label="invalid parse function return annotation",
                range=parse_error_builder.function_return_annotation(),
                raise_error=TypeError,
            )
        output_optional = True
    elif get_origin(return_annotation):
        parse_error_builder.add_diagnostic(
            message=(f"Parse function '{parse_fqn}' return annotation must be a singleton or an optional singleton."),
            code="99",
            label="invalid parse function return annotation",
            range=parse_error_builder.function_return_annotation(),
            raise_error=TypeError,
        )
        raise
    else:
        parse_output = return_annotation
    if not _is_valid_stream_message_type(parse_output):
        parse_error_builder.add_diagnostic(
            message=f"Parse function '{parse_fqn}' return annotation must be either a pydantic BaseModel, decorated with @dataclass, or a protobuf Message type",
            code="101",
            label="invalid parse function return annotation",
            range=parse_error_builder.function_return_annotation(),
            raise_error=TypeError,
        )
    if parse_output != stream_fn_input_type:
        parse_error_builder.add_diagnostic(
            message=(
                f"Parse function '{parse_fqn}' return annotation must match input annotation of resolver '{stream_fqn}'"
            ),
            code="102",
            label="invalid parse function return annotation",
            range=parse_error_builder.function_return_annotation(),
            raise_error=TypeError,
        )

    parse_inputs = [annotation_parser.parse_annotation(p) for p in sig.parameters.keys()]
    if len(parse_inputs) != 1:
        parse_error_builder.add_diagnostic(
            message=(
                f"Parse function '{parse_fqn}' has {len(parse_inputs)} inputs. "
                f"Parse functions must have one input argument"
            ),
            code="103",
            label="extraneous argument",
            range=parse_error_builder.function_arg_value_by_index(len(parse_inputs) - 1),
            raise_error=TypeError,
        )
    parse_input = parse_inputs[0]
    parse_input_name = list(sig.parameters.keys())[0]
    if get_origin(parse_input):
        parse_error_builder.add_diagnostic(
            message=f"Parse function '{parse_fqn}' input annotation must be a singleton",
            code="104",
            label="extraneous argument",
            range=parse_error_builder.function_arg_value_by_name(parse_input_name),
            raise_error=TypeError,
        )

    if not is_pydantic_basemodel(parse_input) and parse_input != bytes:
        parse_error_builder.add_diagnostic(
            message=f"Parse function '{parse_fqn}' input annotation must be of type pydantic.BaseModel or bytes",
            code="105",
            label="invalid parse function input annotation",
            range=parse_error_builder.function_arg_value_by_name(parse_input_name),
            raise_error=TypeError,
        )

    gas = GasLimit(remaining_gas=RESOLVER_FUNCTION_CAPTURE_LIMIT, out_of_gas_error=OutOfGasError())
    parse_function_captured_globals = parse_extract_function_object_captured_globals(parse_fn, gas)

    return ParseInfo(
        fn=parse_fn,
        input_type=cast(Any, parse_input),
        output_type=parse_output,
        output_is_optional=output_optional,
        parse_function_captured_globals=parse_function_captured_globals,
        parse_expression=None,
    )


def _get_stream_resolver_input_type(
    param: Union[StreamResolverParamMessage, StreamResolverParamMessageWindow],
    stream_fqn: str,
    error_builder: ResolverErrorBuilder,
) -> "Type[BaseModel]":
    if isinstance(param, StreamResolverParamMessage):
        input_model_type = param.typ
    elif isinstance(param, StreamResolverParamMessageWindow):  # pyright: ignore[reportUnnecessaryIsInstance]
        if get_origin(param.typ) in (List, list):
            input_model_types = get_args(param.typ)
            input_model_type = next((a for a in input_model_types if a is not type(None)), None)
        elif isinstance(param.typ, type) and issubclass(param.typ, DataFrame):
            stream_input_annotation = param.typ
            input_model_type = stream_input_annotation.__pydantic_model__
        else:
            error_builder.add_diagnostic(
                message=f"Stream resolver '{stream_fqn}' input {param.name} must be a list or a DataFrame",
                code="106",
                label="invalid input",
                range=error_builder.function_arg_value_by_name(param.name),
                raise_error=TypeError,
            )
            raise
    else:
        error_builder.add_diagnostic(
            message=f"Unrecognized input argument {param.name} for stream resolver {stream_fqn}",
            code="107",
            label="invalid input",
            range=error_builder.function_arg_value_by_name(param.name),
            raise_error=ValueError,
        )
        raise
    if not (isinstance(input_model_type, type) and is_pydantic_basemodel(input_model_type)):
        error_builder.add_diagnostic(
            message=f"Stream resolver '{stream_fqn}' input {param.name} must take in BaseModel",
            code="108",
            label="invalid input",
            range=error_builder.function_arg_value_by_name(param.name),
            raise_error=ValueError,
        )
        raise
    return input_model_type


def _validate_possibly_nested_key(
    *, stream_fqn: str, input_model_type: "Type[BaseModel]", key_path: str, error_builder: ResolverErrorBuilder
) -> Any:
    """
    Validates that the given key can be used to look up the corresponding `value` in the original model.

    Examples:
    - if `key` is `"user_id"` then `input_model_type` should have a `user_id` field.
    - if `key` is `"user.id"` then `input_model_type` should have a `user` field that has a `id` field

    This functionality is technically unnecessary given the availability of parse functions
    """
    if not isinstance(key_path, str):  # pyright: ignore[reportUnnecessaryIsInstance]
        # The key must be a string.
        error_builder.add_diagnostic(
            message=f"Stream resolver '{stream_fqn}' key '{key_path}' should be type string",
            code="123",
            label="invalid stream resolver key parameter",
            range=error_builder.function_decorator_key_from_dict("keys", key_path),
            raise_error=TypeError,
        )
    if key_path == "":
        error_builder.add_diagnostic(
            message=f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. Key must not be empty.",
            code="124",
            label="invalid stream resolver key parameter",
            range=error_builder.function_decorator_key_from_dict("keys", key_path),
            raise_error=ValueError,
        )
    if "." in key_path:
        if key_path.startswith("."):
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                    f"Key '{key_path}' must not start with a dot '.'"
                ),
                code="125",
                label="invalid stream resolver key parameter",
                range=error_builder.function_decorator_key_from_dict("keys", key_path),
                raise_error=ValueError,
            )
        if key_path.endswith("."):
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                    f"Key '{key_path}' must not start with a dot '.'"
                ),
                code="125",
                label="invalid stream resolver key parameter",
                range=error_builder.function_decorator_key_from_dict("keys", key_path),
                raise_error=ValueError,
            )

        nested_model_type = input_model_type
        # This is a nested key path, which is treated somewhat differently.
        key_path_parts = key_path.split(".")
        for key_path_part_index, key_path_part in enumerate(key_path_parts):
            # If we're not still on the first field in the path, we should explain how we got here to the user:
            explain_current_path = (
                f" (which is the type of '{'.'.join(key_path_parts[:key_path_part_index])}' on input model class '{input_model_type}')"
                if key_path_part_index != 0
                else ""
            )

            if (
                nested_model_type is None
                or nested_model_type is str
                or nested_model_type is bool
                or nested_model_type is int
                or nested_model_type is float
                or nested_model_type is datetime
            ):
                error_builder.add_diagnostic(
                    message=(
                        f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                        f"Key field '{key_path_part}' cannot be looked up in type '{nested_model_type}' because the latter cannot have fields"
                        f"{explain_current_path}"
                    ),
                    code="126",
                    label="invalid stream resolver key parameter",
                    range=error_builder.function_decorator_key_from_dict("keys", key_path),
                    raise_error=ValueError,
                )

            if not is_pydantic_basemodel(nested_model_type):
                # TODO: Alternatively, we can just stop here, and trust that the user knows what they're doing.
                # It won't immediately break anything here, but could cause problems down the line (but so would type-errors in the actual stream).
                error_builder.add_diagnostic(
                    message=(
                        f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                        f"Key field '{key_path_part}' cannot be looked up in type '{nested_model_type}' because the latter is not a Pydantic Model"
                        f"{explain_current_path}"
                    ),
                    code="127",
                    label="invalid stream resolver key parameter",
                    range=error_builder.function_decorator_key_from_dict("keys", key_path),
                    raise_error=ValueError,
                )

            if key_path_part == "":
                error_builder.add_diagnostic(
                    message=(
                        f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                        f"Key '{key_path}' contains an empty key path part"
                    ),
                    code="128",
                    label="invalid stream resolver key parameter",
                    range=error_builder.function_decorator_key_from_dict("keys", key_path),
                    raise_error=ValueError,
                )
            # Otherwise, look it up in the subtype.
            if key_path_part not in nested_model_type.__fields__.keys():
                error_builder.add_diagnostic(
                    message=(
                        f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                        f"Key field '{key_path_part}' is not an attribute in model class '{nested_model_type}'"
                        f"{explain_current_path}"
                    ),
                    code="129",
                    label="invalid stream resolver key parameter",
                    range=error_builder.function_decorator_key_from_dict("keys", key_path),
                    raise_error=ValueError,
                )

            # Now, drill into the nested model type.
            nested_model_field_info = nested_model_type.__fields__[key_path_part]
            if not nested_model_field_info.annotation:
                # We need to have a type annotation to be able to move forward.
                error_builder.add_diagnostic(
                    message=(
                        f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                        f"Key field '{key_path_part}' is not an attribute in model class '{nested_model_type}'"
                        f"{explain_current_path}"
                    ),
                    code="129",
                    label="invalid stream resolver key parameter",
                    range=error_builder.function_decorator_key_from_dict("keys", key_path),
                    raise_error=ValueError,
                )
            nested_model_type = nested_model_field_info.annotation

    # This is not a nested key path, so the key should exist as a field directly on the model.
    elif key_path not in input_model_type.__fields__.keys():
        error_builder.add_diagnostic(
            message=(
                f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                f"Key '{key_path}' is not an attribute in input model class '{input_model_type}'"
            ),
            code="129",
            label="invalid stream resolver key parameter",
            range=error_builder.function_decorator_key_from_dict("keys", key_path),
            raise_error=ValueError,
        )


def _validate_keys(
    stream_fn: Callable[P, Any],
    keys: dict[str, Any],
    params: Sequence[StreamResolverParam],
    error_builder: ResolverErrorBuilder,
    name: str | None,
) -> dict[str, Any]:
    stream_fqn = get_resolver_fqn(function=stream_fn, name=name)

    if not isinstance(keys, dict):  # pyright: ignore[reportUnnecessaryIsInstance]
        error_builder.add_diagnostic(
            message=f"Stream resolver '{stream_fqn}' keys parameter must be of type dict",
            code="109",
            label="invalid stream resolver keys parameter",
            range=error_builder.function_decorator_arg_by_name("keys"),
            raise_error=TypeError,
        )
    input_model_arg = next(
        param for param in params if isinstance(param, (StreamResolverParamMessage, StreamResolverParamMessageWindow))
    )
    input_model_type = _get_stream_resolver_input_type(input_model_arg, stream_fqn, error_builder)

    for key, value in keys.items():
        _validate_possibly_nested_key(
            stream_fqn=stream_fqn, input_model_type=input_model_type, key_path=key, error_builder=error_builder
        )

        if not isinstance(value, FeatureWrapper):
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{stream_fqn}' maps key '{key}' to value '{value}', "
                    f"but '{value}' is not of type Feature"
                ),
                code="110",
                label="invalid stream resolver keys parameter",
                range=error_builder.function_decorator_value_from_dict("keys", key),
                raise_error=TypeError,
            )
        value = unwrap_feature(value)
        if not value.is_scalar:
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{stream_fqn}' maps key '{key}' to value '{value}', "
                    f"but '{value}' is not a scalar feature"
                ),
                code="111",
                label="invalid stream resolver keys parameter",
                range=error_builder.function_decorator_value_from_dict("keys", key),
                raise_error=TypeError,
            )
        if value.is_windowed:
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{stream_fqn}' maps key '{key}' to value '{value}', "
                    f"but '{value}' cannot be a windowed feature"
                ),
                code="112",
                label="invalid stream resolver keys parameter",
                range=error_builder.function_decorator_value_from_dict("keys", key),
                raise_error=TypeError,
            )

    return {key: keys[key] for key in sorted(keys.keys())}


def _validate_timestamp(
    stream_fn: Callable[P, Any],
    timestamp: str,
    params: Sequence[StreamResolverParam],
    error_builder: ResolverErrorBuilder,
    name: str | None,
):
    stream_fqn = get_resolver_fqn(function=stream_fn, name=name)
    input_model_arg = next(
        param for param in params if isinstance(param, (StreamResolverParamMessage, StreamResolverParamMessageWindow))
    )
    input_model_type = _get_stream_resolver_input_type(input_model_arg, stream_fqn, error_builder)

    if timestamp not in input_model_type.__fields__.keys():
        error_builder.add_diagnostic(
            message=(
                f"Stream resolver '{stream_fqn}' specifies an invalid 'timestamp' attribute. "
                f"'{timestamp}' is not an attribute of the input model class '{input_model_type}'"
            ),
            code="113",
            label="invalid stream resolver timestamp parameter",
            range=error_builder.function_decorator_arg_by_name("timestamp"),
            raise_error=ValueError,
        )
    model_field = input_model_type.__fields__[timestamp]

    # handling Optional[datetime] and datetime with get_args
    if model_field.annotation != datetime and datetime not in get_args(model_field.annotation):
        error_builder.add_diagnostic(
            message=(
                f"Stream resolver '{stream_fqn}' specifies an invalid 'timestamp' attribute. "
                f"'{timestamp}' field must be of type datetime.datetime. "
                "Use the parse function to convert your timestamp to a zoned (not naive!) datetime."
            ),
            code="114",
            label="invalid stream resolver timestamp parameter",
            range=error_builder.function_decorator_arg_by_name("timestamp"),
            raise_error=TypeError,
        )


def parse_and_register_stream_resolver(
    *,
    caller_globals: Optional[Dict[str, Any]],
    caller_locals: Optional[Dict[str, Any]],
    fn: Callable[P, T],
    source: StreamSource,
    caller_filename: str,
    error_builder: ResolverErrorBuilder,
    mode: Optional[Literal["continuous", "tumbling"]] = None,
    environment: Optional[Environments] = None,
    machine_type: Optional[MachineType] = None,
    message: Optional[Type[Any]] = None,
    sql_query: Optional[str] = None,
    owner: Optional[str] = None,
    parse: Optional[Callable[[T], Any]] = None,
    keys: Optional[Dict[str, Any]] = None,
    timestamp: Optional[str] = None,
    caller_line: Optional[int] = None,
    name: str | None = None,
    updates_materialized_aggregations: bool = True,
) -> StreamResolver[P, T]:
    fqn = f"{fn.__module__}.{fn.__name__}"
    annotation_parser = ResolverAnnotationParser(fn, caller_globals, caller_locals, error_builder)
    output_features = _parse_stream_resolver_output_features(
        fn,
        error_builder,
        resolver_fqn_for_errors=fqn,
    )
    flattened_output_features = (
        df.columns
        if len(output_features.features) == 1
        and isinstance(output_features.features[0], type)
        and issubclass(df := output_features.features[0], DataFrame)
        else output_features.features
    )
    is_windowed_resolver = any(x.is_windowed for x in flattened_output_features)
    params = _parse_stream_resolver_params(
        fn,
        error_builder,
        resolver_fqn_for_errors=fqn,
        annotation_parser=annotation_parser,
        is_windowed_resolver=is_windowed_resolver,
    )
    parse_info = None
    if parse:
        stream_fqn = get_resolver_fqn(function=fn, name=name)
        stream_fn_input_arg = next(
            param
            for param in params
            if isinstance(param, (StreamResolverParamMessage, StreamResolverParamMessageWindow))
        )
        stream_fn_input_type = _get_stream_resolver_input_type(stream_fn_input_arg, stream_fqn, error_builder)
        parse_info = _validate_parse_function(
            stream_fqn=stream_fqn,
            parse_fn=parse,
            globals=caller_globals,
            locals=caller_locals,
            stream_fn_input_type=stream_fn_input_type,
            name=name,
        )
    if keys is not None:
        keys = _validate_keys(stream_fn=fn, keys=keys, params=params, error_builder=error_builder, name=name)
    elif keys is None and mode == "continuous":
        error_builder.add_diagnostic(
            message=(
                f"Stream resolver '{fqn}' must take a 'keys' argument in the decorator "
                "if mode is continuous. The 'keys' argument should be dict mapping from "
                "the attribute of the incoming message to the Chalk feature"
            ),
            code="115",
            label="continuous resolvers need a keys parameter",
            range=error_builder.function_decorator(),
            raise_error=ValueError,
        )
    output_feature_fqns = set(f.fqn for f in flattened_output_features)

    signature = StreamResolverSignature(
        params=params,
        output_feature_fqns=output_feature_fqns,
    )
    parsed = parse_function(
        fn,
        caller_globals,
        caller_locals,
        error_builder,
        allow_custom_args=True,
        is_streaming_resolver=True,
        name=name,
    )()

    if timestamp:
        _validate_timestamp(stream_fn=fn, timestamp=timestamp, params=params, error_builder=error_builder, name=name)
    for resolver in RESOLVER_REGISTRY.get_stream_resolvers():
        if resolver.source == source:
            if resolver.timestamp != timestamp:
                error_builder.add_diagnostic(
                    message=(
                        f"Stream resolver '{fqn}' specifies 'timestamp' attribute, "
                        f"but stream resolver '{resolver.fqn}' does not or specifies a different attribute. "
                        "Stream resolvers with the same source must all have the same timestamp value"
                    ),
                    code="116",
                    label="Resolver timestamp inconsistency",
                    range=error_builder.function_decorator(),
                    raise_error=ValueError,
                )

    resolver = StreamResolver(
        function_definition=parsed.function_definition,
        function_captured_globals=parsed.function_captured_globals,
        fqn=parsed.fqn,
        filename=caller_filename,
        source=source,
        fn=fn,
        tags=None,
        environment=None if environment is None else list(ensure_tuple(environment)),
        doc=parsed.doc,
        mode=mode,
        machine_type=machine_type,
        message=message,
        output=output_features,
        signature=signature,
        state=parsed.state,
        sql_query=None,
        owner=owner,
        parse=parse_info,
        keys=keys,
        timestamp=timestamp,
        source_line=caller_line,
        lsp_builder=error_builder,
        autogenerated=False,
        updates_materialized_aggregations=updates_materialized_aggregations,
        sql_settings=None,
        feature_expressions=None,
        message_producer_parsed=None,
    )
    resolver.add_to_registry(override=False)
    return resolver


def _validate_message_type(message_type: Type[Any], allow_lists: bool = True) -> str | None:
    if hasattr(message_type, "__origin__"):
        assert hasattr(message_type, "__args__")
        if message_type.__origin__ not in (list, typing.List, typing.Sequence):
            return "The only generic type supported is list|List|Sequence."
        if len(message_type.__args__) != 1:
            return f"Found {len(message_type.__args__)} type parameters for generic type, only one supported."
        if not allow_lists:
            return f"Nested lists (e.g. List[List[MessageType]]) not supported."
        sub_type = message_type.__args__[0]
        sub_res = _validate_message_type(sub_type, allow_lists=False)
        if sub_res is not None:
            sub_res = f"Found type List[T] with invalid T: {sub_res}"
        return sub_res

    if message_type in (str, bytes):
        return None

    if inspect.isclass(message_type):  # pyright: ignore[reportUnnecessaryIsInstance]
        if issubclass(message_type, BaseModel):
            return None
        elif issubclass(message_type, google.protobuf.message.Message):
            return None
        elif is_dataclass(message_type):
            return None
        else:
            return "Unsupported type (expected str/bytes, a struct type, or a list[struct])"
    else:
        return "message type should be a type"


def _is_list_message_type(message_type: Type[Any]):
    return getattr(message_type, "__origin__", None) in (list, typing.List, typing.Sequence)


def make_stream_resolver(
    *,
    name: str,
    source: StreamSource,
    message_type: Type[BaseModel | google.protobuf.message.Message | AnyDataclass | str | bytes],
    output_features: "Mapping[FeatureWrapper, Underscore]",
    parse: Underscore | Callable[[str | bytes], Any] | None = None,
    environment: Optional[Environments] = None,
    machine_type: Optional[MachineType] = None,
    owner: Optional[str] = None,
    doc: str | None = None,
    sink: Sink | None = None,
    additional_output_features: Iterable[FeatureWrapper | str] | None = None,
    skip_online: bool = False,
    skip_offline: bool = False,
) -> StreamResolver:
    """Constructs a streaming resolver that, instead of a Python function,
    defines its output features as column projections on an input message.

    Parameters
    ----------
    name
        The name of the streaming resolver.
    source
        The streaming source, e.g. `KafkaSource(...)` or `KinesisSource(...)` or `PubSubSource(...)`.
    message_type
        The type of message to process.
    output_features
        Mapping of output features to their corresponding expressions.
    parse
        Converts bytes -> message_type. If it returns `None`, message is skipped.
    environment
        Environments are used to trigger behavior in different deployments
        such as staging, production, and local development.
    machine_type
        You can optionally specify that resolvers need to run
        on a machine other than the default. Must be configured
        in your deployment.
    owner
        Individual or team responsible for this resolver.
        The Chalk Dashboard will display this field, and alerts
        can be routed to owners.
    doc
        Documentation string for the resolver.
    sink
        An optional message producer configuration that specifies where to send messages.
        Read more at https://docs.chalk.ai/api-docs#Sink
    additional_output_features
        An optional iterable of additional features to compute and persist to the online store
        without publishing to an auxiliary stream. Mutually exclusive with `sink`.
        Use this when you want to enrich features without setting up stream publishing infrastructure.
    skip_online
        If True, skip online persistence (no writes to Redis/DynamoDB/etc).
        Results will still be processed but not stored in online stores.
        Note: Only applies to native streaming. Default: False
    skip_offline
        If True, skip offline persistence (no result bus publishing for offline storage).
        Results will still be processed but not stored in offline stores (S3/BigQuery/etc).
        Note: Only applies to native streaming. Default: False

    Returns
    -------
    StreamResolver
        A configured stream resolver.
    """
    from chalk.features.underscore import Underscore

    # The function "definition" will be the source code of the invocation, for error reporting / LSP highlighting.
    caller_info = get_function_caller_info(frame_offset=1)
    caller_source = caller_info.caller_source
    caller_filename = caller_info.filename
    caller_lineno = caller_info.lineno
    error_builder = FunctionCallErrorBuilder(caller_info)

    # TODO unify this with the above
    frame = inspect.currentframe()
    assert frame is not None
    caller_frame = frame.f_back
    assert caller_frame is not None
    caller_globals = caller_frame.f_globals
    caller_locals = caller_frame.f_locals
    del frame

    if not isinstance(source, StreamSource):  # pyright: ignore[reportUnnecessaryIsInstance]
        error_builder.add_diagnostic(
            message=(
                f"Invalid source for stream resolver '{name}': expected KafkaSource, KinesisSource, or PubSubSource, got {type(source).__name__}"
            ),
            code="190",
            label="Invalid stream source",
            range=error_builder.function_arg_range_by_name("source"),
        )

    # Validate that sink and additional_output_features are mutually exclusive
    if sink is not None and additional_output_features is not None:
        error_builder.add_diagnostic(
            message=(
                "Cannot specify both 'sink' and 'additional_output_features'. "
                + "If you're using Sink, add all desired features to Sink.output_features instead."
            ),
            code="208",
            label="Use Sink.output_features for all features",
            range=error_builder.function_arg_range_by_name("additional_output_features"),
        )

    # Validate name is a string
    if not isinstance(name, str):  # pyright: ignore[reportUnnecessaryIsInstance]
        error_builder.add_diagnostic(
            message=f"Stream resolver name must be a string, got {type(name).__name__}",
            code="191",
            label="Invalid resolver name type",
            range=error_builder.function_arg_range_by_name("name"),
        )

    # Validate name is a valid FQN (basic validation)
    if isinstance(name, str):  # pyright: ignore[reportUnnecessaryIsInstance]
        # Check for empty name
        if not name.strip():
            error_builder.add_diagnostic(
                message="Stream resolver name cannot be empty",
                code="192",
                label="Empty resolver name",
                range=error_builder.function_arg_range_by_name("name"),
            )
        # Check for dots (not allowed in FQNs)
        elif "." in name:
            error_builder.add_diagnostic(
                message=f"Stream resolver name '{name}' cannot contain dots. Use underscores instead",
                code="193",
                label="Invalid resolver name format",
                range=error_builder.function_arg_range_by_name("name"),
            )

    # Validate message_type is one of the allowed types
    message_type_validation_msg = _validate_message_type(message_type)
    if message_type_validation_msg is not None:
        error_builder.add_diagnostic(
            message=f"Invalid message_type for stream resolver '{name}' ({message_type}): {message_type_validation_msg}. Supported message types includes 'str', 'bytes', some struct type (a pydantic BaseModel or dataclass), or a list[T] where T is a string/bytes/struct)",
            code="195",
            label="Invalid message type",
            range=error_builder.function_arg_range_by_name("message_type"),
        )

    if _is_list_message_type(message_type) and parse is None:
        error_builder.add_diagnostic(
            message=(
                f"Found list message_type without a parse function for stream resolver '{name}' ({message_type}): List message types are only supported if a custom parse function is provided. "
                f"Otherwise, only struct or bytes/string messages are supported."
            ),
            code="196",
            label="List message type without parse function",
            range=error_builder.function_arg_range_by_name("message_type"),
        )

    from chalk import Features

    unwrapped_features: list[Feature] = []
    for f in output_features.keys():
        if not isinstance(f, FeatureWrapper):  # pyright: ignore[reportUnnecessaryIsInstance]
            error_builder.add_diagnostic(
                message=f"Stream resolver output feature '{f}' is not a Feature, got {type(f)} instead",
                code="194",
                label="Invalid output feature",
                range=error_builder.function_arg_range_by_name("output_features"),
            )
        unwrapped_features.append(unwrap_feature(f))
    _validate_output_features(unwrapped_features, error_builder, name)
    validate_message_attributes(
        expressions=output_features.values(), message_type=message_type, error_builder=error_builder, name=name
    )

    output_type = Features[tuple(output_features.keys())]

    def _fn(*args: Any, **kwargs: Any):
        raise ValueError(
            f"Stream resolver '{name}' can't be called directly since it's defined as a set of static expressions."
        )

    def _dummy_parse_fn(*args: Any, **kwargs: Any):
        raise ValueError(
            f"Stream resolver '{name}' has expression-based parse function so it can't be called directly."
        )

    params = [StreamResolverParamMessage(typ=message_type, name="message")]

    parse_info: Optional[ParseInfo] = None
    if isinstance(parse, Underscore):
        parse_info = ParseInfo(
            fn=_dummy_parse_fn,
            input_type=bytes,
            output_type=message_type,
            output_is_optional=True,
            parse_function_captured_globals=None,
            parse_expression=parse,
        )
    elif callable(parse):
        parse_info = _validate_parse_function(
            name,
            parse_fn=parse,
            globals=caller_globals,
            locals=caller_locals,
            stream_fn_input_type=message_type,
            name=name,
        )
        if parse_info.input_type != bytes:
            raise ValueError(
                f"Native streaming resolvers only support python parse functions with input bytes 'bytes'. Function {parse} has input type {parse_info.input_type}"
            )

    # Validate and parse sink or additional_output_features before creating StreamResolver
    message_producer_parsed: StreamResolverMessageProducerParsed | None = None
    if sink is not None:
        message_producer_parsed = parse_message_producer_with_lsp_errors(
            sink, error_builder, "sink", message_type, name
        )
    elif additional_output_features is not None:
        message_producer_parsed = parse_additional_output_features_with_lsp_errors(
            additional_output_features, error_builder, "additional_output_features", message_type, name
        )

    resolver = StreamResolver(
        function_definition=caller_source,
        # No captured globals, the function "definition" is a bunch of static expressions
        function_captured_globals=None,
        fqn=name,
        filename=caller_filename or "<unknown file>",
        source=source,
        fn=_fn,
        tags=None,
        environment=None if environment is None else list(ensure_tuple(environment)),
        doc=doc,
        mode=None,
        machine_type=machine_type,
        message=message_type,
        output=output_type,
        signature=StreamResolverSignature(
            params=params,
            output_feature_fqns={str(x) for x in output_features.keys()},
        ),
        state=None,
        sql_query=None,
        owner=owner,
        parse=parse_info,
        keys=None,
        timestamp=None,
        source_line=caller_lineno,
        lsp_builder=ResolverErrorBuilder(fn=None),
        autogenerated=False,
        updates_materialized_aggregations=True,
        sql_settings=None,
        feature_expressions={unwrap_feature(x): u for x, u in output_features.items()},
        message_producer_parsed=message_producer_parsed,
        skip_online=skip_online,
        skip_offline=skip_offline,
    )
    resolver.add_to_registry(override=False)
    return resolver


@dataclass(kw_only=True)
class Sink:
    """Computes additional output features and sends them to a stream source."""

    send_to: StreamSource
    """The stream source to send results to."""

    output_features: Iterable[FeatureWrapper | str]
    """
    The requested output features. These can include both features returned by the stream resolvers and
    other features retrievable via online query given the stream resolver outputs as inputs.
    The message sent to the stream will have these output features as columns.
    """

    format: Literal["json", "ipc_stream"] = "ipc_stream"
    """Format of messages sent."""

    feature_expressions: Mapping[FeatureWrapper | str, Underscore] | None = None


def parse_message_producer_with_lsp_errors(
    message_producer: Sink,
    error_builder: FunctionCallErrorBuilder,
    param_name: str,
    message_type: Type[BaseModel | google.protobuf.message.Message | AnyDataclass | str | bytes],
    resolver_name: str,
) -> StreamResolverMessageProducerParsed | None:
    """Convert a Sink to StreamResolverMessageProducerParsed with LSP error reporting.

    Args:
        message_producer: The Sink object to parse
        error_builder: Error builder for LSP diagnostics
        param_name: Parameter name for error reporting
        message_type: Message type for validating feature_expressions
        resolver_name: Resolver name for error messages

    Returns:
        StreamResolverMessageProducerParsed if successful, None if validation failed
    """
    # Validate send_to is a StreamSource
    if not isinstance(message_producer.send_to, StreamSource):  # pyright: ignore[reportUnnecessaryIsInstance]
        error_builder.add_diagnostic(
            message="Expected a StreamSource for argument 'send_to' on Sink",
            code="202",
            label="Invalid send_to type",
            range=error_builder.function_arg_range_by_name(param_name),
        )
        return None

    # Validate output_features is iterable
    if not isinstance(
        message_producer.output_features, collections.abc.Iterable
    ):  # pyright: ignore[reportUnnecessaryIsInstance]
        error_builder.add_diagnostic(
            message="Expected an iterable for argument 'output_features' on Sink",
            code="203",
            label="Invalid output_features type",
            range=error_builder.function_arg_range_by_name(param_name),
        )
        return None

    output_features_list = list(message_producer.output_features)
    if len(output_features_list) == 0:
        error_builder.add_diagnostic(
            message="Expected at least one output feature for Sink",
            code="204",
            label="Empty output_features",
            range=error_builder.function_arg_range_by_name(param_name),
        )
        return None

    # Validate output features (primary key, namespaces, etc.)
    unwrapped_features: list[Feature] = []
    for f in output_features_list:
        if isinstance(f, FeatureWrapper):
            unwrapped_features.append(unwrap_feature(f))
        elif isinstance(f, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            try:
                # Try to parse as feature FQN
                feature = Feature.from_root_fqn(f)
                unwrapped_features.append(feature)
            except Exception:
                error_builder.add_diagnostic(
                    message=f"Invalid feature FQN '{f}' in Sink output_features",
                    code="206",
                    label="Invalid feature FQN",
                    range=error_builder.function_arg_range_by_name(param_name),
                )
                return None
        else:
            error_builder.add_diagnostic(
                message=f"Sink output feature '{f}' must be a Feature or string, got {type(f)} instead",
                code="207",
                label="Invalid output feature type",
                range=error_builder.function_arg_range_by_name(param_name),
            )
            return None

    # Run the same validation as stream resolvers (primary key, namespace consistency)
    _validate_output_features(unwrapped_features, error_builder, resolver_name)

    # Validate feature_expressions if present
    if message_producer.feature_expressions is not None:
        if not isinstance(
            message_producer.feature_expressions, collections.abc.Mapping
        ):  # pyright: ignore[reportUnnecessaryIsInstance]
            error_builder.add_diagnostic(
                message="Expected a mapping for argument 'feature_expressions' on Sink",
                code="205",
                label="Invalid feature_expressions type",
                range=error_builder.function_arg_range_by_name(param_name),
            )
            return None
        feature_expressions_dict = {str(k): v for k, v in message_producer.feature_expressions.items()}

        # Validate underscore expressions in feature_expressions
        validate_message_attributes(
            expressions=message_producer.feature_expressions.values(),
            message_type=message_type,
            error_builder=error_builder,
            name=resolver_name,
        )
    else:
        feature_expressions_dict = None

    # Validate format is valid
    if message_producer.format not in ("json", "ipc_stream"):
        error_builder.add_diagnostic(
            message=f"Invalid format '{message_producer.format}' on Sink. Must be 'json' or 'ipc_stream'",
            code="208",
            label="Invalid format",
            range=error_builder.function_arg_range_by_name(param_name),
        )

    # Create and return the parsed version
    return StreamResolverMessageProducerParsed(
        send_to=message_producer.send_to,
        output_features=[str(f) for f in output_features_list],
        feature_expressions=feature_expressions_dict,
        format=message_producer.format,
    )


def parse_additional_output_features_with_lsp_errors(
    output_features_input: Iterable[FeatureWrapper | str],
    error_builder: FunctionCallErrorBuilder,
    param_name: str,
    message_type: Type[BaseModel | google.protobuf.message.Message | AnyDataclass | str | bytes],
    resolver_name: str,
) -> StreamResolverMessageProducerParsed | None:
    """Parse additional_output_features into StreamResolverMessageProducerParsed.

    Similar to parse_message_producer_with_lsp_errors but for additional_output_features
    parameter, which doesn't require a send_to destination.
    """
    # Validate output_features is iterable
    if not isinstance(output_features_input, collections.abc.Iterable):  # pyright: ignore[reportUnnecessaryIsInstance]
        error_builder.add_diagnostic(
            message="Expected an iterable for argument 'additional_output_features'",
            code="209",
            label="Invalid additional_output_features type",
            range=error_builder.function_arg_range_by_name(param_name),
        )
        return None

    output_features_list = list(output_features_input)
    if len(output_features_list) == 0:
        error_builder.add_diagnostic(
            message="Expected at least one feature in 'additional_output_features'",
            code="210",
            label="Empty additional_output_features",
            range=error_builder.function_arg_range_by_name(param_name),
        )
        return None

    # Validate and unwrap features (same logic as parse_message_producer_with_lsp_errors)
    unwrapped_features: list[Feature] = []
    for f in output_features_list:
        if isinstance(f, FeatureWrapper):
            unwrapped_features.append(unwrap_feature(f))
        elif isinstance(f, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            try:
                feature = Feature.from_root_fqn(f)
                unwrapped_features.append(feature)
            except Exception:
                error_builder.add_diagnostic(
                    message=f"Invalid feature FQN '{f}' in additional_output_features",
                    code="211",
                    label="Invalid feature FQN",
                    range=error_builder.function_arg_range_by_name(param_name),
                )
                return None
        else:
            error_builder.add_diagnostic(
                message=f"Feature '{f}' must be a Feature or string, got {type(f)} instead",
                code="212",
                label="Invalid feature type",
                range=error_builder.function_arg_range_by_name(param_name),
            )
            return None

    # Reuse existing validation
    _validate_output_features(unwrapped_features, error_builder, resolver_name)

    # Create StreamResolverMessageProducerParsed with send_to=None
    return StreamResolverMessageProducerParsed(
        output_features=[str(f) for f in output_features_list],
        format="ipc_stream",
        send_to=None,
        feature_expressions=None,
    )


class StreamResolverMessageProducerParsed:
    def __init__(
        self,
        send_to: StreamSource | None,
        output_features: list[str],
        format: Literal["json", "ipc_stream"],
        feature_expressions: Mapping[str, Underscore] | None = None,
    ):
        super().__init__()
        self.send_to = send_to
        self.output_features = output_features
        self.format = format
        self.feature_expressions = feature_expressions


def _validate_output_features(features: Iterable[Feature], error_builder: FunctionCallErrorBuilder, name: str):
    found_primary = False
    namespace = None
    for feature in features:
        if feature.primary:
            found_primary = True
        if namespace is None:
            namespace = feature.root_namespace
        elif namespace != feature.root_namespace:
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{name}' returned features with different namespaces '{namespace}' and '{feature.root_namespace}'. "
                    "Stream resolvers must return features with the same namespace."
                ),
                code="194",
                label="different namespaces",
                range=error_builder.function_arg_range_by_name("output_features"),
                raise_error=TypeError,
            )
    if not found_primary:
        error_builder.add_diagnostic(
            message=(
                f"Stream resolver '{name}' did not return a primary key feature. "
                "Stream resolvers must return a primary key feature."
            ),
            code="194",
            label="missing primary key",
            range=error_builder.function_arg_range_by_name("output_features"),
            raise_error=TypeError,
        )


def is_structured_type(
    message_type: Type[BaseModel | google.protobuf.message.Message | AnyDataclass | str | bytes],
) -> bool:
    """Check if message_type is a structured type (BaseModel/protobuf/dataclass)."""
    if not inspect.isclass(message_type):  # pyright: ignore[reportUnnecessaryIsInstance]
        return False

    if hasattr(message_type, "__origin__"):
        # It's a generic type like List[T]
        return False

    # Check if it's a Pydantic BaseModel
    if issubclass(message_type, BaseModel):
        return True

    # Check if it's a protobuf Message
    if issubclass(message_type, google.protobuf.message.Message):
        return True

    # Check if it's a dataclass
    if is_dataclass(message_type):
        return True

    return False


def get_valid_fields(
    message_type: Type[BaseModel | google.protobuf.message.Message | AnyDataclass | str | bytes],
) -> Set[str]:
    """Get valid field names for a structured type."""
    if not inspect.isclass(message_type):  # pyright: ignore[reportUnnecessaryIsInstance]
        return set()

    # Check if it's a Pydantic BaseModel
    if issubclass(message_type, BaseModel):
        return set(message_type.__fields__.keys())

    # Check if it's a protobuf Message
    if issubclass(message_type, google.protobuf.message.Message):
        return set(field.name for field in message_type.DESCRIPTOR.fields)

    # Check if it's a dataclass
    if is_dataclass(message_type):
        return set(message_type.__dataclass_fields__.keys())

    return set()


def get_field_type(parent_type: Type[Any], field_name: str) -> Optional[Type[Any]]:
    """Get the type of a field from a structured type."""
    if not inspect.isclass(parent_type):  # pyright: ignore[reportUnnecessaryIsInstance]
        return None

    # Check if it's a Pydantic BaseModel
    if issubclass(parent_type, BaseModel):
        from chalk.utils.pydanticutil.pydantic_compat import get_pydantic_field_type

        return get_pydantic_field_type(parent_type, field_name)

    # Check if it's a protobuf Message
    if issubclass(parent_type, google.protobuf.message.Message):
        for field in parent_type.DESCRIPTOR.fields:
            if field.name == field_name:
                if field.message_type:
                    # For nested message fields, get the Python class from the descriptor
                    return message_factory.GetMessageClass(field.message_type)
                else:
                    # For primitive fields, return None since we can't easily convert protobuf field types to Python types
                    # The validation will still work for nested message fields
                    return None

    # Check if it's a dataclass
    if is_dataclass(parent_type):
        if field_name in parent_type.__dataclass_fields__:
            field_type = parent_type.__dataclass_fields__[field_name].type
            # Return the field type if it's a class, otherwise None
            return field_type if inspect.isclass(field_type) else None

    return None


def validate_field_chain(
    underscore_attr: "UnderscoreAttr",
    current_type: Type[BaseModel | google.protobuf.message.Message | AnyDataclass | str | bytes],
    error_builder: FunctionCallErrorBuilder,
    name: str,
) -> Optional[Type[Any]]:
    """Validate a chain of field accesses like _.submessage.id step by step."""
    from chalk.features.underscore import UnderscoreAttr, UnderscoreRoot

    # Base case: if parent is UnderscoreRoot (_), validate field against current_type
    if isinstance(underscore_attr._chalk__parent, UnderscoreRoot):
        if underscore_attr._chalk__attr == "chalk_now":
            return datetime

        # Check if current_type allows field access
        if current_type in (str, bytes):
            error_builder.add_diagnostic(
                message=f"Stream resolver '{name}' with message_type {current_type.__name__} does not support access to fields. Use chalk functions instead.",
                code="197",
                label="Invalid field access on primitive type",
                range=error_builder.function_arg_range_by_name("output_features"),
            )
            return None
        elif is_structured_type(current_type):
            valid_fields = get_valid_fields(current_type)
            if underscore_attr._chalk__attr not in valid_fields:
                error_builder.add_diagnostic(
                    message=f"Stream resolver '{name}' field '{underscore_attr._chalk__attr}' does not exist on message_type {current_type.__name__}. Available fields: {sorted(valid_fields)}",
                    code="198",
                    label="Invalid field name",
                    range=error_builder.function_arg_range_by_name("output_features"),
                )
                return None
            else:
                return get_field_type(current_type, underscore_attr._chalk__attr)

    # Recursive case: get parent's type, then validate current field against it
    elif isinstance(underscore_attr._chalk__parent, UnderscoreAttr):
        parent_type = validate_field_chain(underscore_attr._chalk__parent, current_type, error_builder, name)
        if parent_type is None:
            return None  # Error already reported in parent validation

        # Now validate current field against the parent's field type
        if is_structured_type(parent_type):
            valid_fields = get_valid_fields(parent_type)
            if underscore_attr._chalk__attr not in valid_fields:
                error_builder.add_diagnostic(
                    message=f"Stream resolver '{name}' field '{underscore_attr._chalk__attr}' does not exist on type {parent_type.__name__}. Available fields: {sorted(valid_fields)}",
                    code="198",
                    label="Invalid field name",
                    range=error_builder.function_arg_range_by_name("output_features"),
                )
                return None
            else:
                return get_field_type(parent_type, underscore_attr._chalk__attr)
        else:
            error_builder.add_diagnostic(
                message=f"Stream resolver '{name}' cannot access field '{underscore_attr._chalk__attr}' on non-structured type",
                code="199",
                label="Invalid field access",
                range=error_builder.function_arg_range_by_name("output_features"),
            )
            return None

    return None


def validate_function_args(
    underscore_function: "UnderscoreFunction",
    message_type: Type[BaseModel | google.protobuf.message.Message | AnyDataclass | str | bytes],
    error_builder: FunctionCallErrorBuilder,
    name: str,
) -> None:
    """Recursively validate all arguments in an UnderscoreFunction."""
    from chalk.features.underscore import Underscore

    # Validate all positional arguments
    for arg in underscore_function._chalk__args:
        if isinstance(arg, Underscore):
            validate_underscore_expression(arg, message_type, error_builder, name)

    # Validate all keyword arguments
    for kwarg_value in underscore_function._chalk__kwargs.values():
        if isinstance(kwarg_value, Underscore):
            validate_underscore_expression(kwarg_value, message_type, error_builder, name)


def validate_underscore_call(
    underscore_call: "UnderscoreCall",
    message_type: Type[BaseModel | google.protobuf.message.Message | AnyDataclass | str | bytes],
    error_builder: FunctionCallErrorBuilder,
    name: str,
) -> None:
    """Recursively validate all arguments in an UnderscoreCall (method call like _.field.method())."""
    from chalk.features.underscore import Underscore, UnderscoreAttr

    # For method calls like _.field.method(), we need to validate the field access
    # but not the method name itself (since methods like 'cast' can be called on any field)
    parent = underscore_call._chalk__parent
    if isinstance(parent, UnderscoreAttr):
        # The parent is _.field.method - we want to validate _.field, not _.field.method
        # So we validate the parent's parent instead
        validate_underscore_expression(parent._chalk__parent, message_type, error_builder, name)
    else:
        # For other cases, validate the parent directly
        validate_underscore_expression(parent, message_type, error_builder, name)

    # Validate all positional arguments
    for arg in underscore_call._chalk__args:
        if isinstance(arg, Underscore):
            validate_underscore_expression(arg, message_type, error_builder, name)

    # Validate all keyword arguments
    for kwarg_value in underscore_call._chalk__kwargs.values():
        if isinstance(kwarg_value, Underscore):
            validate_underscore_expression(kwarg_value, message_type, error_builder, name)


def validate_underscore_cast(
    underscore_cast: "UnderscoreCast",
    message_type: Type[BaseModel | google.protobuf.message.Message | AnyDataclass | str | bytes],
    error_builder: FunctionCallErrorBuilder,
    name: str,
) -> None:
    """Validate an UnderscoreCast expression (e.g., cast(_.field, str))."""
    from chalk.features.underscore import Underscore

    # Validate the value being cast
    if isinstance(underscore_cast._chalk__value, Underscore):  # pyright: ignore[reportUnnecessaryIsInstance]
        validate_underscore_expression(underscore_cast._chalk__value, message_type, error_builder, name)

    # Note: We don't need to validate the target type (_chalk__to_type) as it's a PyArrow DataType


def validate_underscore_expression(
    expression: "Underscore",
    message_type: Type[BaseModel | google.protobuf.message.Message | AnyDataclass | str | bytes],
    error_builder: FunctionCallErrorBuilder,
    name: str,
) -> None:
    """Main entry point for validating a single underscore expression."""
    from chalk.features.underscore import Underscore, UnderscoreAttr, UnderscoreCall, UnderscoreCast, UnderscoreFunction

    # First validate it's an underscore
    if not isinstance(expression, Underscore):  # pyright: ignore[reportUnnecessaryIsInstance]
        error_builder.add_diagnostic(
            message=f"Stream resolver '{name}' output feature expression must be an Underscore, got {type(expression).__name__}",
            code="196",
            label="Invalid output expression",
            range=error_builder.function_arg_range_by_name("output_features"),
        )
        return

    # Handle different types of underscore expressions
    if isinstance(expression, UnderscoreAttr):
        validate_field_chain(expression, message_type, error_builder, name)
    elif isinstance(expression, UnderscoreFunction):
        validate_function_args(expression, message_type, error_builder, name)
    elif isinstance(expression, UnderscoreCall):
        validate_underscore_call(expression, message_type, error_builder, name)
    elif isinstance(expression, UnderscoreCast):
        validate_underscore_cast(expression, message_type, error_builder, name)
    else:
        # Catch-all for any other underscore types
        error_builder.add_diagnostic(
            message=f"Stream resolver '{name}' does not support {expression.__name__} expressions",
            code="201",
            label="Unsupported underscore expression",
            range=error_builder.function_arg_range_by_name("output_features"),
        )


def validate_message_attributes(
    expressions: Iterable[Any],
    message_type: Type[BaseModel | google.protobuf.message.Message | AnyDataclass | str | bytes],
    error_builder: FunctionCallErrorBuilder,
    name: str,
) -> None:
    """Validate that all underscore expressions use valid field names for the message_type."""
    if _is_list_message_type(message_type):
        message_type = message_type.__args__[0]  # pyright: ignore[reportAttributeAccessIssue]
    for expression in expressions:
        validate_underscore_expression(expression, message_type, error_builder, name)


def make_model_resolver(
    name: str,
    model: "ModelVersion",
    inputs: Dict[Feature, str] | List[Feature],
    output: Feature | List[Feature] | Dict[Feature, str],
    feature_class: Optional[type[Features]] = None,
    resource_group: Optional[str] = None,
    resource_hint: Optional[ResourceHint] = None,
) -> OnlineResolver:
    """
    Create an online resolver that runs inference on a model.

    This function provides an imperative API for creating model inference resolvers,
    as an alternative to using F.inference in feature definitions. It uses the same
    underlying implementation as F.inference but allows you to create resolvers
    programmatically.

    Parameters
    ----------
    name
        The name of the resolver
    model
        A ModelVersion reference to a deployed model
    inputs
        Either a dict mapping Feature objects to model input names (strings), or a list of
        Feature objects. If a dict, the values represent the model's expected input names
        (for future use). If a list, the features will be passed as a single DataFrame to
        the model.
    output
        The output feature(s) that will contain the predictions.
        Can be a single Feature, a list of Features, or a dict mapping Feature objects to
        model output names (strings) for future use with multi-output models.
    feature_class
        Optional feature class to use. If not provided, will be inferred from the inputs.
    resource_group
        Optional resource group for the resolver
    resource_hint
        Optional resource hint for execution (e.g., CPU/GPU preferences)

    Returns
    -------
    OnlineResolver
        The created resolver

    Examples
    --------
    >>> from chalk.features import features, feature
    >>> from chalk.features.resolver import make_model_resolver
    >>> from chalk.ml import ModelVersion
    >>>
    >>> @features
    ... class User:
    ...     id: str = feature(primary=True)
    ...     age: float
    ...     income: float
    ...     risk_score: float
    ...     credit_score: float
    >>>
    >>> # Create a model version reference
    >>> model = ModelVersion(
    ...     name="risk_model",
    ...     version=1,
    ...     model_type="sklearn",
    ...     model_encoding="pickle",
    ...     filename="model.pkl"
    ... )
    >>>
    >>> # Create resolver with single output
    >>> resolver = make_model_resolver(
    ...     name="risk_model",
    ...     model=model,
    ...     inputs=[User.age, User.income],
    ...     output=User.risk_score,
    ... )
    >>>
    >>> # Create resolver with multiple outputs (list)
    >>> resolver = make_model_resolver(
    ...     name="multi_output_model",
    ...     model=model,
    ...     inputs=[User.age, User.income],
    ...     output=[User.risk_score, User.credit_score],
    ... )
    >>>
    >>> # Create resolver with named inputs and outputs (dict)
    >>> resolver = make_model_resolver(
    ...     name="named_model",
    ...     model=model,
    ...     inputs={User.age: "age_input", User.income: "income_input"},
    ...     output={User.risk_score: "risk_output", User.credit_score: "credit_output"},
    ... )
    """
    from chalk.features.inference import build_inference_function

    if isinstance(inputs, dict):
        input_features_raw = list(inputs.keys())
    else:
        input_features_raw = inputs

    input_features = [unwrap_feature(f) for f in input_features_raw]

    if isinstance(output, dict):
        output_features = [unwrap_feature(f) for f in output.keys()]
    elif isinstance(output, list):
        output_features = [unwrap_feature(f) for f in output]
    else:
        output_features = [unwrap_feature(output)]

    # If feature_class is not provided, try to infer it from the first input feature
    if feature_class is None:
        if not input_features:
            raise ValueError("Cannot infer feature class: no input features provided and feature_class not specified")

        first_input = input_features[0]

        if hasattr(first_input, "features_cls") and first_input.features_cls is not None:
            feature_class = first_input.features_cls
        else:
            raise ValueError(
                "Cannot infer feature class from inputs. Please provide feature_class parameter explicitly."
            )

    pkey = feature_class.__chalk_primary__
    if pkey is None:
        raise ValueError(f"Feature class {feature_class} does not have a primary key defined")

    first_output = output_features[0]

    output_namespace = (
        first_output.namespace
        if hasattr(first_output, "namespace") and first_output.namespace
        else feature_class.__name__.lower()
    )

    # Use the same underlying inference function as F.inference
    # Pass list of outputs if multiple, single if only one
    output_for_inference = output_features if len(output_features) > 1 else output_features[0]
    inference_fn = build_inference_function(model, pkey, output_for_inference)

    if len(output_features) == 1:
        output_names = output_features[0].name
    else:
        output_names = "_".join(f.name for f in output_features)

    resolver = OnlineResolver(
        function_definition="",
        filename="",
        fqn=f"{name}__{output_namespace}_{output_names}",
        doc=None,
        inputs=[DataFrame[[pkey, *ensure_tuple(input_features)]]],
        state=None,
        output=Features[DataFrame[tuple([*output_features, pkey])]],  # type: ignore[misc]
        fn=inference_fn,
        environment=None,
        machine_type=None,
        default_args=[None],
        timeout=None,
        cron=None,
        when=None,
        tags=None,
        owner=None,
        resource_hint=resource_hint or model.resource_hint,
        data_sources=None,
        is_sql_file_resolver=False,
        source_line=None,
        lsp_builder=get_resolver_error_builder(inference_fn),
        parse=None,
        static=False,
        total=False,
        autogenerated=False,
        unique_on=None,
        partitioned_by=None,
        data_lineage=None,
        sql_settings=None,
    )

    # Register the resolver
    RESOLVER_REGISTRY.add_to_registry(resolver, override=False)

    return resolver
