from __future__ import annotations

import collections
import collections.abc
import inspect
import json
from datetime import timedelta
from typing import Any, Callable, ClassVar, Collection, Dict, Mapping, Optional, Sequence, Union, cast

import pyarrow as pa
from google.protobuf import duration_pb2
from typing_extensions import assert_never

from chalk import DataFrame
from chalk._gen.chalk.arrow.v1 import arrow_pb2 as arrow_pb
from chalk._gen.chalk.expression.v1 import expression_pb2 as expr_pb
from chalk._gen.chalk.graph.v1 import graph_pb2 as pb
from chalk._gen.chalk.graph.v1.graph_pb2 import CronFilterWithFeatureArgs
from chalk._gen.chalk.graph.v2 import sources_pb2 as sources_pb
from chalk._validation.feature_validation import FeatureValidation
from chalk.features import (
    CacheStrategy,
    Feature,
    FeatureConverter,
    Features,
    FeatureWrapper,
    Filter,
    TimeDelta,
    TPrimitive,
    Underscore,
    ensure_feature,
    unwrap_feature,
)
from chalk.features._encoding.converter import PrimitiveFeatureConverter
from chalk.features._encoding.rich import TRich
from chalk.features._encoding.serialized_rich_type import SerializedRichType
from chalk.features.pseudofeatures import PSEUDONAMESPACE
from chalk.features.resolver import (
    Cron,
    FunctionCapturedGlobal,
    FunctionCapturedGlobalBuiltin,
    FunctionCapturedGlobalEnum,
    FunctionCapturedGlobalFeatureClass,
    FunctionCapturedGlobalFunction,
    FunctionCapturedGlobalModule,
    FunctionCapturedGlobalModuleMember,
    FunctionCapturedGlobalProto,
    FunctionCapturedGlobalStruct,
    FunctionCapturedGlobalVariable,
    OfflineResolver,
    OnlineResolver,
    ParseInfo,
    Resolver,
    ResolverArgErrorHandler,
    SinkResolver,
    StateDescriptor,
    StreamResolver,
)
from chalk.features.underscore import convert_value_to_proto_expr
from chalk.importer import SQLSourceGroup
from chalk.operators._utils import static_resolver_to_operator
from chalk.parsed._proto.utils import (
    datetime_to_proto_timestamp,
    seconds_int_to_proto_duration,
    seconds_to_proto_duration,
    timedelta_to_proto_duration,
    value_to_proto,
)
from chalk.parsed.expressions import is_valid_operation
from chalk.queries.named_query import NamedQuery
from chalk.sql._internal.sql_settings import SQLResolverSettings
from chalk.sql._internal.sql_source import BaseSQLSource
from chalk.sql.finalized_query import Finalizer, IncrementalSettings
from chalk.streams import StreamSource
from chalk.streams.types import (
    StreamResolverParam,
    StreamResolverParamKeyedState,
    StreamResolverParamMessage,
    StreamResolverParamMessageWindow,
)
from chalk.utils import paths
from chalk.utils.collections import get_unique_item, unwrap_annotated_if_needed
from chalk.utils.duration import CronTab, Duration, parse_chalk_duration
from chalk.utils.json import TJSON
from chalk.utils.log_with_context import get_logger
from chalk.utils.source_parsing import should_skip_source_code_parsing

_logger = get_logger(__name__)

_CHALK_ANON_SQL_SOURCE_PREFIX = "__chalk_anon_sql_source_"
_CHALK_ANON_STREAM_SOURCE_PREFIX = "__chalk_anon_stream_source_"


class ToProtoConverter:
    _mode_to_proto: ClassVar[Mapping[str, pb.WindowMode]] = {
        "tumbling": pb.WINDOW_MODE_TUMBLING,
        "continuous": pb.WINDOW_MODE_CONTINUOUS,
        "cdc": pb.WINDOW_MODE_CDC,
    }
    _cache_strategy_to_proto: ClassVar[Mapping[CacheStrategy, "pb.CacheStrategy"]] = {
        CacheStrategy.ALL: pb.CACHE_STRATEGY_ALL,
        CacheStrategy.NO_NULLS: pb.CACHE_STRATEGY_NO_NULLS,
        CacheStrategy.NO_DEFAULTS: pb.CACHE_STRATEGY_NO_DEFAULTS,
        CacheStrategy.NO_NULLS_OR_DEFAULTS: pb.CACHE_STRATEGY_NO_NULLS_OR_DEFAULTS,
        CacheStrategy.EVICT_NULLS: pb.CACHE_STRATEGY_EVICT_NULLS,
        CacheStrategy.EVICT_DEFAULTS: pb.CACHE_STRATEGY_EVICT_DEFAULTS,
        CacheStrategy.EVICT_NULLS_AND_DEFAULTS: pb.CACHE_STRATEGY_EVICT_NULLS_AND_DEFAULTS,
    }
    _database_source_group_type: ClassVar[str] = "chalk::db_source_group"

    @classmethod
    def convert_underscore(cls, v: Union[Underscore, TPrimitive]) -> expr_pb.LogicalExprNode:
        if isinstance(v, Underscore):
            return v._to_proto()  # pyright: ignore[reportPrivateUsage]
        else:
            return convert_value_to_proto_expr(v)

    @staticmethod
    def _convert_stream_source(source: StreamSource) -> sources_pb.StreamSource:
        options: Dict[str, TJSON] = source.config_to_dict()
        options.pop("name", None)  # Name is stored separately
        options_proto = {k: value_to_proto(v) for k, v in options.items()}
        return sources_pb.StreamSource(source_type=source.streaming_type, name=source.name, options=options_proto)

    @staticmethod
    def _convert_named_query(source: NamedQuery) -> pb.NamedQuery:
        # Ignoring source.errors when converting named queries because structured errors in named queries
        # prevent that specific query from being used at runtime.
        if source.planner_options is not None:
            try:
                parsed_planner_options = {k: str(v) for k, v in source.planner_options.items()}
            except Exception as e:
                raise ValueError(f"Could not parse provided planner options '{source.planner_options}'") from e
        else:
            parsed_planner_options = None

        parsed_duration: dict[str, duration_pb2.Duration] | None = (
            None
            if source.staleness is None
            else {k: timedelta_to_proto_duration(parse_chalk_duration(v)) for (k, v) in source.staleness.items()}
        )

        try:
            return pb.NamedQuery(
                name=source.name,
                query_version=source.version,
                input=source.input,
                output=source.output,
                additional_logged_features=source.additional_logged_features,
                tags=source.tags,
                description=source.description,
                owner=source.owner,
                meta=source.meta,
                staleness=parsed_duration,
                planner_options=parsed_planner_options,
                file_name=source.filename,
                valid_plan_not_required=source.valid_plan_not_required,
            )
        except Exception as e:
            raise ValueError(f"Could not convert named query '{source.name}'") from e

    @staticmethod
    def convert_stream_source(source: StreamSource) -> sources_pb.StreamSource:
        try:
            return ToProtoConverter._convert_stream_source(source)
        except Exception as e:
            raise ValueError(f"Could not convert stream source '{source.name}'") from e

    @staticmethod
    def convert_engine_args(engine_args: Mapping[str, Any]) -> dict[str, arrow_pb.ScalarValue]:
        res: dict[str, arrow_pb.ScalarValue] = {}
        for k, v in engine_args.items():
            try:
                json_val = json.dumps(v)
            except Exception as e:
                raise ValueError(f"Could not convert engine arg '{k}' to JSON") from e
            res[k] = arrow_pb.ScalarValue(large_utf8_value=json_val)
        return res

    @staticmethod
    def convert_source_secrets(source_secrets: Mapping[str, str]) -> sources_pb.SourceSecrets:
        return sources_pb.SourceSecrets(secrets=source_secrets)

    @staticmethod
    def _convert_sql_source(source: BaseSQLSource) -> sources_pb.DatabaseSource:
        return sources_pb.DatabaseSource(source_type=source.kind.value, name=source.name)

    @staticmethod
    def convert_sql_source(source: BaseSQLSource) -> sources_pb.DatabaseSource:
        try:
            return ToProtoConverter._convert_sql_source(source)
        except Exception as e:
            raise ValueError(f"Could not convert SQL source '{source.name}'") from e

    @classmethod
    def _convert_sql_source_group(cls, group: SQLSourceGroup) -> sources_pb.DatabaseSourceGroup:
        return sources_pb.DatabaseSourceGroup(
            name=group.name,
            default_source=cls.create_database_source_reference(group._default),  # pyright: ignore[reportPrivateUsage]
            tagged_sources={
                tag: cls.create_database_source_reference(source)
                for tag, source in group._tagged_sources.items()  # pyright: ignore[reportPrivateUsage]
            },
        )

    @classmethod
    def convert_sql_source_group(cls, group: SQLSourceGroup) -> sources_pb.DatabaseSourceGroup:
        try:
            return cls._convert_sql_source_group(group)
        except Exception as e:
            raise ValueError(f"Could not convert SQL source group '{group.name}'") from e

    @staticmethod
    def convert_cron_filter(cron: Union[CronTab, Duration, Cron]) -> Optional[CronFilterWithFeatureArgs]:
        if isinstance(cron, Cron) and cron.filter is not None:
            sig = inspect.signature(cron.filter)
            features: list[pb.FeatureReference] = []
            for parameter in sig.parameters.values():
                try:
                    feature = ensure_feature(parameter.annotation)
                except Exception as e:
                    raise ValueError("Cron filter arguments must be features") from e
                if not feature.is_feature_time and not feature.is_scalar:
                    raise ValueError("Cron filters must be scalars or feature time features")
                features.append(ToProtoConverter.create_feature_reference(feature))
            return CronFilterWithFeatureArgs(
                filter=ToProtoConverter.create_function_reference(cron.filter),
                args=features,
            )
        return None

    @staticmethod
    def convert_feature_to_filter_node(raw: Feature) -> expr_pb.LogicalExprNode:
        if raw.path:
            path_converted: list[expr_pb.Column] = []
            for p in raw.path:
                path_converted.append(
                    expr_pb.Column(name=p.parent.name, relation=expr_pb.ColumnRelation(relation=p.parent.namespace))
                )
            path_converted.append(
                expr_pb.Column(name=raw.name, relation=expr_pb.ColumnRelation(relation=raw.namespace))
            )

            return expr_pb.LogicalExprNode(
                binary_expr=expr_pb.BinaryExprNode(
                    operands=[expr_pb.LogicalExprNode(column=p) for p in path_converted],
                    op="foreign_feature_access",
                )
            )

        return expr_pb.LogicalExprNode(
            column=expr_pb.Column(name=raw.name, relation=expr_pb.ColumnRelation(relation=raw.namespace)),
        )

    @classmethod
    def convert_filter(cls, f: Filter) -> expr_pb.LogicalExprNode:
        if not is_valid_operation(f.operation):
            raise ValueError(f"Unknown operation '{f.operation}'")

        if f.operation in ("and", "or"):
            if not isinstance(f.lhs, Filter):
                raise ValueError("lhs of and/or must be a Filter")
            if not isinstance(f.rhs, Filter):
                raise ValueError("rhs of and/or must be a Filter")
            return expr_pb.LogicalExprNode(
                binary_expr=expr_pb.BinaryExprNode(
                    operands=[
                        ToProtoConverter.convert_filter(f.lhs),
                        ToProtoConverter.convert_filter(f.rhs),
                    ],
                    op=f.operation,
                ),
            )

        raw_lhs = f.lhs
        raw_rhs = f.rhs

        if isinstance(raw_lhs, FeatureWrapper):
            raw_lhs = unwrap_feature(raw_lhs)
        if isinstance(raw_rhs, FeatureWrapper):
            raw_rhs = unwrap_feature(raw_rhs)

        converted_lhs = raw_lhs
        converted_rhs = raw_rhs

        if isinstance(raw_lhs, Feature):
            if not raw_lhs.is_scalar and not raw_lhs.is_feature_time:
                raise ValueError("lhs of filter is a feature that is not scalar or feature-time")
            converted_lhs = ToProtoConverter.convert_feature_to_filter_node(raw_lhs)

        if isinstance(raw_rhs, Feature):
            if not raw_rhs.is_scalar and not raw_rhs.is_feature_time:
                raise ValueError("rhs of filter is a feature that is not scalar or feature-time")
            converted_rhs = ToProtoConverter.convert_feature_to_filter_node(raw_rhs)

        if isinstance(raw_lhs, Feature) and isinstance(raw_rhs, TimeDelta):
            # This means that the filter was a before() or after()
            duration_converter = PrimitiveFeatureConverter(
                name="helper", is_nullable=False, pyarrow_dtype=pa.duration("us")
            )
            converted_rhs = expr_pb.LogicalExprNode(
                literal=duration_converter.from_primitive_to_protobuf(raw_rhs.to_std())
            )
            if not isinstance(converted_lhs, expr_pb.LogicalExprNode):
                raise ValueError(f"lhs '{converted_lhs}' is of type {type(converted_lhs)}")
            return expr_pb.LogicalExprNode(
                binary_expr=expr_pb.BinaryExprNode(
                    operands=[converted_lhs, converted_rhs],
                    op=f.operation,
                ),
            )

        if not isinstance(raw_lhs, Feature):
            if not isinstance(raw_rhs, Feature):
                raise ValueError("One side must be a feature")
            if isinstance(raw_lhs, Underscore):
                converted_lhs = cls.convert_underscore(raw_lhs)
            else:
                converted_lhs = expr_pb.LogicalExprNode(
                    literal=raw_rhs.converter.from_primitive_to_protobuf(converted_lhs),
                )

        if not isinstance(raw_rhs, Feature):
            if not isinstance(raw_lhs, Feature):
                raise ValueError("One side must be a feature")
            if f.operation in ("in", "not in"):
                if not isinstance(raw_rhs, collections.abc.Iterable):
                    raise ValueError("rhs must be an iterable when operation is 'in'/'not in'")
                prim_values = tuple(raw_lhs.converter.from_rich_to_primitive(x) for x in raw_rhs)
                list_dtype = pa.large_list(raw_lhs.converter.pyarrow_dtype)
                list_converter = PrimitiveFeatureConverter(name="helper", is_nullable=False, pyarrow_dtype=list_dtype)
                converted_rhs = expr_pb.LogicalExprNode(
                    literal=list_converter.from_primitive_to_protobuf(prim_values),
                )
            elif isinstance(raw_rhs, Underscore):
                converted_rhs = cls.convert_underscore(raw_rhs)
            else:
                converted_rhs = expr_pb.LogicalExprNode(literal=raw_lhs.converter.from_rich_to_protobuf(raw_rhs))

        assert isinstance(converted_lhs, expr_pb.LogicalExprNode), f"lhs is {converted_lhs}"
        assert isinstance(converted_rhs, expr_pb.LogicalExprNode), f"rhs is {converted_rhs}"
        return expr_pb.LogicalExprNode(
            binary_expr=expr_pb.BinaryExprNode(
                operands=[converted_lhs, converted_rhs],
                op=f.operation,
            )
        )

    @staticmethod
    def create_database_source_reference(source: BaseSQLSource | SQLSourceGroup) -> sources_pb.DatabaseSourceReference:
        if isinstance(source, SQLSourceGroup):
            return sources_pb.DatabaseSourceReference(
                source_type=ToProtoConverter._database_source_group_type,
                name=source.name,
            )
        return sources_pb.DatabaseSourceReference(source_type=source.kind.value, name=source.name)

    @staticmethod
    def convert_rich_type_to_protobuf(rich_type: type[TRich]) -> arrow_pb.ArrowType:
        converter = FeatureConverter(name="helper", is_nullable=False, rich_type=rich_type)
        return converter.convert_pa_dtype_to_proto_dtype(converter.pyarrow_dtype)

    @staticmethod
    def create_stream_source_reference(source: StreamSource) -> sources_pb.StreamSourceReference:
        return sources_pb.StreamSourceReference(source_type=source.streaming_type, name=source.name)

    @staticmethod
    def create_function_reference(
        fn: Callable,
        *,
        definition: Optional[str] = None,
        filename: Optional[str] = None,
        source_line: Optional[int] = None,
        captured_globals: Optional[Mapping[str, FunctionCapturedGlobal]] = None,
    ) -> pb.FunctionReference:
        module = inspect.getmodule(fn)
        if definition is None and not should_skip_source_code_parsing():
            try:
                definition = inspect.getsource(fn)
            except:
                pass
        return pb.FunctionReference(
            name=fn.__name__,
            module=module.__name__ if module else "",
            file_name=inspect.getfile(fn) if filename is None else filename,
            function_definition=definition,
            source_line=source_line,
            captured_globals=[
                ToProtoConverter.create_captured_global(name, captured) for name, captured in captured_globals.items()
            ]
            if captured_globals
            else None,
        )

    @staticmethod
    def create_captured_global(
        name: str,
        captured_global: FunctionCapturedGlobal,
    ) -> pb.FunctionReferenceCapturedGlobal:
        if isinstance(captured_global, FunctionCapturedGlobalFeatureClass):
            return pb.FunctionReferenceCapturedGlobal(
                global_name=name,
                feature_class=pb.FunctionGlobalCapturedFeatureClass(
                    feature_class_name=captured_global.feature_namespace,
                ),
            )
        elif isinstance(captured_global, FunctionCapturedGlobalBuiltin):
            return pb.FunctionReferenceCapturedGlobal(
                global_name=name,
                builtin=pb.FunctionGlobalCapturedBuiltin(
                    builtin_name=captured_global.builtin_name,
                ),
            )
        elif isinstance(captured_global, FunctionCapturedGlobalModule):
            return pb.FunctionReferenceCapturedGlobal(
                global_name=name,
                module=pb.FunctionGlobalCapturedModule(
                    name=captured_global.name,
                ),
            )
        elif isinstance(captured_global, FunctionCapturedGlobalModuleMember):
            return pb.FunctionReferenceCapturedGlobal(
                global_name=name,
                module_member=pb.FunctionGlobalCapturedModuleMember(
                    module_name=captured_global.module_name,
                    qualname=captured_global.qualname,
                ),
            )
        elif isinstance(captured_global, FunctionCapturedGlobalFunction):
            return pb.FunctionReferenceCapturedGlobal(
                global_name=name,
                function=pb.FunctionGlobalCapturedFunction(
                    source=captured_global.source,
                    module=captured_global.module,
                    captured_globals=[
                        ToProtoConverter.create_captured_global(name, captured)
                        for name, captured in captured_global.captured_globals.items()
                    ]
                    if captured_global.captured_globals
                    else None,
                    name=captured_global.name,
                ),
            )
        elif isinstance(captured_global, FunctionCapturedGlobalVariable):
            return pb.FunctionReferenceCapturedGlobal(
                global_name=name,
                variable=pb.FunctionGlobalCapturedVariable(
                    module=captured_global.module,
                    name=captured_global.name,
                ),
            )
        elif isinstance(captured_global, FunctionCapturedGlobalEnum):

            def _package_scalar(value: Any):
                pa_dtype = pa.scalar(value).type
                converter = PrimitiveFeatureConverter(
                    name="convert_enum",
                    is_nullable=False,
                    pyarrow_dtype=pa_dtype,
                )
                return converter.from_primitive_to_protobuf(value)

            args = {k: _package_scalar(v) for k, v in captured_global.member_map.items()}
            return pb.FunctionReferenceCapturedGlobal(
                global_name=name,
                enum=pb.FunctionGlobalCapturedEnum(
                    module=captured_global.module,
                    name=captured_global.name,
                    member_map=args,
                    bases=[PrimitiveFeatureConverter.convert_pa_dtype_to_proto_dtype(b) for b in captured_global.bases],
                ),
            )

        elif isinstance(captured_global, FunctionCapturedGlobalProto):
            return pb.FunctionReferenceCapturedGlobal(
                global_name=name,
                proto=pb.FunctionGlobalCapturedProto(
                    name=captured_global.name,
                    module=captured_global.module,
                    pa_dtype=PrimitiveFeatureConverter.convert_pa_dtype_to_proto_dtype(captured_global.pa_dtype),
                    serialized_fd=captured_global.serialized_fd,
                    full_name=captured_global.full_name,
                ),
            )

        elif isinstance(captured_global, FunctionCapturedGlobalStruct):  # pyright: ignore[reportUnnecessaryIsInstance]
            return pb.FunctionReferenceCapturedGlobal(
                global_name=captured_global.name,
                struct=pb.FunctionGlobalCapturedStruct(
                    name=captured_global.name,
                    module=captured_global.module,
                    pa_dtype=PrimitiveFeatureConverter.convert_pa_dtype_to_proto_dtype(captured_global.pa_dtype),
                ),
            )

        raise ValueError(
            f"The captured global reference '{captured_global}' (type {type(captured_global)}) cannot be converted into a protobuf message `FunctionReferenceCapturedGlobal`"
        )

    @staticmethod
    def create_feature_reference(feature: Feature) -> pb.FeatureReference:
        df = None
        if feature.is_has_many:
            df = feature.typ.parsed_annotation
            if not isinstance(df, type) or not issubclass(  # pyright: ignore[reportUnnecessaryIsInstance]
                df, DataFrame
            ):
                raise ValueError("has-many feature missing `DataFrame` annotation")

        path: list[pb.FeatureReference] = []
        for path_elem in feature.path:
            converted = ToProtoConverter.create_feature_reference(path_elem.parent)
            if path_elem.parent.is_has_many:
                converted.df.ClearField("optional_columns")
                converted.df.ClearField("required_columns")
                # Selecting only the foreign features to match
                # https://github.com/chalk-ai/chalk-private/blob/a480c8518ee2f4c3a97250741a3513167ab650ae/chalkruntime/chalkruntime/loader/converter.py#L517
                if len(path_elem.parent.foreign_join_keys) == 0:
                    raise ValueError(f"has-many feature '{path_elem.parent.fqn}' missing `foreign_join_key` annotation")
                converted.df.optional_columns.extend(
                    ToProtoConverter.create_feature_reference(foreign_join_key)
                    for foreign_join_key in path_elem.parent.foreign_join_keys
                )
            path.append(converted)

        return pb.FeatureReference(
            name=feature.name,
            namespace=feature.namespace,
            path=path,
            df=ToProtoConverter.convert_dataframe(df) if df else None,
        )

    @staticmethod
    def convert_resolver_inputs(
        resolver_inputs: Sequence[Union[Feature, FeatureWrapper, type[DataFrame]]],
        state: Optional[StateDescriptor],
        default_args: Sequence[object],
    ) -> Sequence[pb.ResolverInput]:
        inputs: list[pb.ResolverInput] = []
        raw_inputs: list[Optional[Union[Feature, FeatureWrapper, type[DataFrame]]]] = list(resolver_inputs)
        if state is not None:
            raw_inputs.insert(state.pos, None)

        is_sole_dataframe_input = (
            len(resolver_inputs) == 1
            and isinstance(resolver_inputs[0], type)
            and issubclass(resolver_inputs[0], DataFrame)  # pyright: ignore[reportUnnecessaryIsInstance]
        )
        if is_sole_dataframe_input:
            # TODO: Enforce check when there is uniformity in how many
            #       default args there are if there is a sole DF input
            # if len(resolver_inputs[0].columns) != len(default_args):
            #     raise ValueError(
            #         f"Length mismatch: found {len(resolver_inputs[0].columns)} DF "
            #         + f"columns and {len(default_args)} default arg"
            #     )
            pass
        else:
            if len(raw_inputs) != len(default_args):
                if (
                    resolver_inputs
                    and isinstance(resolver_inputs[0], type)
                    and issubclass(resolver_inputs[0], DataFrame)  # pyright: ignore[reportUnnecessaryIsInstance]
                ):
                    # TODO: Remove this exception once we fix the incorrect default args count.
                    #       Currently we take the num columns of the first DF as the num default args,
                    #       regardless of whether it is the sole input.
                    pass
                else:
                    raise ValueError(
                        f"Length mismatch: found {len(raw_inputs)} `inputs` and {len(default_args)} `default_args`"
                    )

        for i in range(len(raw_inputs)):
            raw_input = raw_inputs[i]
            if state and i == state.pos:
                converter = FeatureConverter(
                    name="state", is_nullable=False, rich_type=state.typ, rich_default=state.initial
                )
                inputs.append(
                    pb.ResolverInput(
                        state=pb.ResolverState(
                            initial=converter.from_rich_to_protobuf(state.initial),
                            arrow_type=converter.convert_pa_dtype_to_proto_dtype(converter.pyarrow_dtype),
                        )
                    )
                )
            elif isinstance(raw_input, type) and issubclass(
                raw_input, DataFrame
            ):  # pyright: ignore[reportUnnecessaryIsInstance]
                inputs.append(pb.ResolverInput(df=ToProtoConverter.convert_dataframe(raw_input)))
            else:
                inp = ensure_feature(raw_inputs[i])
                default_arg = default_args[i]
                if default_arg is not None and not isinstance(default_arg, ResolverArgErrorHandler):
                    raise ValueError(f"Invalid default arg: {default_arg}")

                inputs.append(
                    pb.ResolverInput(
                        feature=pb.FeatureInput(
                            feature=ToProtoConverter.create_feature_reference(inp),
                            default_value=(
                                inp.converter.from_primitive_to_protobuf(default_arg.default_value)
                                if default_arg is not None
                                else None
                            ),
                        )
                    )
                )

        return inputs

    @staticmethod
    def convert_resolver_outputs(raw_outputs: Sequence[Union[Feature, type[DataFrame]]]) -> Sequence[pb.ResolverOutput]:
        outputs: list[pb.ResolverOutput] = []
        for o in raw_outputs:
            if isinstance(o, type) and issubclass(o, DataFrame):  # pyright: ignore[reportUnnecessaryIsInstance]
                outputs.append(pb.ResolverOutput(df=ToProtoConverter.convert_dataframe(o)))
            elif isinstance(o, Feature):  # pyright: ignore[reportUnnecessaryIsInstance]
                outputs.append(pb.ResolverOutput(feature=ToProtoConverter.create_feature_reference(o)))
            else:
                raise TypeError(f"Unknown output type: {type(o).__name__}")
        return outputs

    @staticmethod
    def convert_validations(validations: Sequence[FeatureValidation] | None) -> Sequence[pb.FeatureValidation] | None:
        if validations is None:
            return None

        res: list[pb.FeatureValidation] = []
        for val in validations:
            # For backwards compat, store both the arrow and non-arrow versions (modern servers will prefer reading the arrow-based field)
            if val.min is not None:
                res.append(pb.FeatureValidation(min=val.min, strict=val.strict))
                proto_scalar = PrimitiveFeatureConverter.from_pyarrow_to_protobuf(pa.scalar(val.min))
                res.append(pb.FeatureValidation(min_arrow=proto_scalar, strict=val.strict))
            if val.max is not None:
                res.append(pb.FeatureValidation(max=val.max, strict=val.strict))
                proto_scalar = PrimitiveFeatureConverter.from_pyarrow_to_protobuf(pa.scalar(val.max))
                res.append(pb.FeatureValidation(max_arrow=proto_scalar, strict=val.strict))
            if val.min_length is not None:
                res.append(pb.FeatureValidation(min_length=val.min_length, strict=val.strict))
                proto_scalar = PrimitiveFeatureConverter.from_pyarrow_to_protobuf(pa.scalar(val.min_length))
                res.append(pb.FeatureValidation(min_length_arrow=proto_scalar, strict=val.strict))
            if val.max_length is not None:
                res.append(pb.FeatureValidation(max_length=val.max_length, strict=val.strict))
                proto_scalar = PrimitiveFeatureConverter.from_pyarrow_to_protobuf(pa.scalar(val.max_length))
                res.append(pb.FeatureValidation(max_length_arrow=proto_scalar, strict=val.strict))
            if val.contains is not None:
                proto_scalar = PrimitiveFeatureConverter.from_pyarrow_to_protobuf(pa.scalar(val.contains))
                res.append(pb.FeatureValidation(contains=proto_scalar, strict=val.strict))

        return res

    @staticmethod
    def convert_has_many(f: Feature) -> pb.FeatureType:
        if not f.is_has_many:
            raise ValueError("Should only be called on has_many features")
        if f.path:
            raise ValueError("Should not be called on features with `path`")
        if f.join is None:
            raise ValueError("Feature missing join")

        max_staleness_duration = timedelta_to_proto_duration(parse_chalk_duration(f.max_staleness))
        if f.joined_class is None:
            raise ValueError(f"has-many feature {f.fqn} must reference a Features cls")
        res = pb.FeatureType(
            has_many=pb.HasManyFeatureType(
                name=f.name,
                namespace=f.namespace,
                is_autogenerated=f.is_autogenerated,
                join=ToProtoConverter.convert_filter(f.join),
                foreign_namespace=f.joined_class.namespace,
                max_staleness_duration=max_staleness_duration,
                online_store_max_items=f.online_store_max_items,
                tags=f.tags,
                owner=f.owner,
                description=f.description,
                attribute_name=f.attribute_name if hasattr(f, "attribute_name") else None,
                unversioned_attribute_name=f.unversioned_attribute_name
                if hasattr(f, "unversioned_attribute_name")
                else None,
            )
        )

        return res

    @staticmethod
    def convert_has_one(f: Feature) -> pb.FeatureType:
        def _validate_has_one_join(join: Filter):
            if isinstance(join.lhs, Filter) and isinstance(join.rhs, Filter) and join.operation == "and":
                _validate_has_one_join(join.lhs)
                _validate_has_one_join(join.rhs)
                return
            if not isinstance(join.lhs, Feature):
                raise ValueError("lhs of join clause must be a Feature")
            if not isinstance(join.rhs, Feature):
                raise ValueError("rhs of join clause must be a Feature")

        if f.path:
            raise ValueError("Should not be called on features with `path`")
        if f.join is None:
            raise ValueError(f"Feature missing join {f.namespace}.{f.name}")
        if f.joined_class is None:
            raise ValueError("has-one relationships must reference a Features cls")
        _validate_has_one_join(f.join)

        res = pb.FeatureType(
            has_one=pb.HasOneFeatureType(
                name=f.name,
                namespace=f.namespace,
                is_nullable=f.typ.is_nullable,
                is_autogenerated=f.is_autogenerated,
                join=ToProtoConverter.convert_filter(f.join),
                foreign_namespace=f.joined_class.namespace,
                tags=f.tags,
                owner=f.owner,
                description=f.description,
                attribute_name=f.attribute_name if hasattr(f, "attribute_name") else None,
                unversioned_attribute_name=f.unversioned_attribute_name
                if hasattr(f, "unversioned_attribute_name")
                else None,
            )
        )
        return res

    @staticmethod
    def convert_feature_time_feature(f: Feature) -> pb.FeatureType:
        if not f.is_feature_time:
            raise ValueError("Should only be called on feature time features")

        return pb.FeatureType(
            feature_time=pb.FeatureTimeFeatureType(
                name=f.name,
                namespace=f.namespace,
                is_autogenerated=f.is_autogenerated,
                tags=f.tags,
                owner=f.owner,
                description=f.description,
                attribute_name=f.attribute_name if hasattr(f, "attribute_name") else None,
            )
        )

    @staticmethod
    def convert_windowed(f: Feature) -> pb.FeatureType:
        if not f.is_windowed:
            raise ValueError("Should only be called on windowed features")
        if f.path:
            raise ValueError("Should not be called on features with `path`")

        return pb.FeatureType(
            windowed=pb.WindowedFeatureType(
                name=f.name,
                namespace=f.namespace,
                is_autogenerated=f.is_autogenerated,
                window_durations=[seconds_to_proto_duration(d) for d in f.window_durations],
                attribute_name=f.attribute_name if hasattr(f, "attribute_name") else None,
                unversioned_attribute_name=f.unversioned_attribute_name
                if hasattr(f, "unversioned_attribute_name")
                else None,
            )
        )

    @staticmethod
    def convert_group_by_feature(f: Feature) -> pb.FeatureType:
        if not f.is_scalar:
            raise ValueError("Should only be called on scalar features")
        if f.path:
            raise ValueError("Should not be called on features with `path`")
        if f.group_by_windowed is None:
            raise ValueError("Feature is missing group_by_windowed")

        mat = f.group_by_windowed._window_materialization_parsed  # pyright: ignore[reportPrivateUsage]
        if mat is None:
            raise ValueError("Feature is missing window materialization")

        res = pb.FeatureType(
            group_by=pb.GroupByFeatureType(
                name=f.name,
                namespace=f.namespace,
                attribute_name=f.attribute_name if hasattr(f, "attribute_name") else None,
                unversioned_attribute_name=f.unversioned_attribute_name
                if hasattr(f, "unversioned_attribute_name")
                else None,
                arrow_type=f.converter.convert_pa_dtype_to_proto_dtype(f.converter.pyarrow_dtype),
                is_nullable=f.typ.is_nullable,
                description=f.description,
                owner=f.owner,
                default_value=f.converter.from_primitive_to_protobuf(f.converter.primitive_default)
                if f.converter.has_default
                else None,
                expression=None,
                # TODO: If we want this underscore expression to exist, we need to extend underscore parsing to handle group_by agg
                # expression=ToProtoConverter.convert_underscore(f.underscore_expression)
                # if f.underscore_expression
                # else None,
                window_durations=[seconds_to_proto_duration(d) for d in f.group_by_windowed.buckets_seconds],
                aggregation=pb.WindowAggregation(
                    namespace=mat.namespace,
                    group_by=[ToProtoConverter.create_feature_reference(feature=g) for g in mat.group_by],
                    bucket_duration=seconds_int_to_proto_duration(mat.bucket_duration_seconds),
                    bucket_start=datetime_to_proto_timestamp(mat.bucket_start),
                    aggregation=mat.aggregation,
                    aggregate_on=ToProtoConverter.create_feature_reference(feature=mat.aggregate_on)
                    if mat.aggregate_on is not None
                    else None,
                    arrow_type=PrimitiveFeatureConverter.convert_pa_dtype_to_proto_dtype(mat.pyarrow_dtype),
                    filters=[ToProtoConverter.convert_filter(f) for f in mat.filters],
                    backfill_lookback_duration=seconds_int_to_proto_duration(mat.backfill_lookback_duration_seconds)
                    if mat.backfill_lookback_duration_seconds is not None
                    else None,
                    continuous_buffer_duration=seconds_int_to_proto_duration(mat.continuous_buffer_duration_seconds)
                    if mat.continuous_buffer_duration_seconds is not None
                    else None,
                    backfill_resolver=mat.backfill_resolver,
                    continuous_resolver=mat.continuous_resolver,
                    backfill_start_time=datetime_to_proto_timestamp(mat.backfill_start_time)
                    if mat.backfill_start_time is not None
                    else None,
                    backfill_schedule=mat.backfill_schedule,
                ),
                tags=f.tags,
                validations=ToProtoConverter.convert_validations(f.all_validations),
            )
        )
        return res

    @staticmethod
    def _serialized_rich_type_to_proto(typ: SerializedRichType) -> pb.RichClassType:
        return pb.RichClassType(
            module_name=typ.module_name,
            qualname=typ.qualname,
            params=tuple(ToProtoConverter._serialized_rich_type_to_proto(p) for p in typ.type_params),
        )

    @classmethod
    def convert_rich_type_info(cls, f: Feature) -> pb.FeatureRichTypeInfo:
        typ = f.converter.rich_type
        typ = unwrap_annotated_if_needed(typ)

        proto_rich_type: pb.FeatureRichType | None = None
        try:
            serialized_rich_type = SerializedRichType.from_typ(typ)
            proto_rich_type = pb.FeatureRichType(
                class_type=ToProtoConverter._serialized_rich_type_to_proto(serialized_rich_type)
            )
        except:
            _logger.warning(f"Failed to convert rich type for feature {f}")
        return pb.FeatureRichTypeInfo(
            rich_type_is_same_as_primitive_type=not f.converter.has_nontrivial_rich_type(),
            encoder=None,  # TODO ENCODER,
            decoder=None,  # TODO DECODER,
            rich_type=proto_rich_type,
            rich_type_name=str(unwrap_annotated_if_needed(typ)),
        )

    @classmethod
    def convert_scalar(cls, f: Feature) -> pb.FeatureType:
        if not f.is_scalar:
            raise ValueError("Should only be called on scalar features")
        if f.path:
            raise ValueError("Should not be called on features with `path`")

        wmp = f.window_materialization_parsed
        rich_type_info = cls.convert_rich_type_info(f)
        res = pb.FeatureType(
            scalar=pb.ScalarFeatureType(
                name=f.name,
                namespace=f.namespace,
                arrow_type=f.converter.convert_pa_dtype_to_proto_dtype(f.converter.pyarrow_dtype),
                is_distance_pseudofeature=f.is_distance_pseudofeature,
                is_nullable=f.typ.is_nullable,
                is_primary=f.primary,
                description=f.description,
                owner=f.owner,
                is_autogenerated=f.is_autogenerated,
                max_staleness_duration=(
                    None
                    if (f.raw_max_staleness is ... or f.raw_max_staleness is None)
                    else timedelta_to_proto_duration(parse_chalk_duration(f.raw_max_staleness))
                ),
                offline_ttl_duration=timedelta_to_proto_duration(parse_chalk_duration(f.offline_ttl)),
                window_info=(
                    pb.WindowInfo(
                        duration=seconds_to_proto_duration(f.window_duration),
                        aggregation=pb.WindowAggregation(
                            namespace=wmp.namespace,
                            group_by=[ToProtoConverter.create_feature_reference(feature=g) for g in wmp.group_by],
                            bucket_duration=seconds_int_to_proto_duration(wmp.bucket_duration_seconds),
                            bucket_start=datetime_to_proto_timestamp(wmp.bucket_start),
                            aggregation=wmp.aggregation,
                            aggregate_on=ToProtoConverter.create_feature_reference(feature=wmp.aggregate_on)
                            if wmp.aggregate_on is not None
                            else None,
                            arrow_type=PrimitiveFeatureConverter.convert_pa_dtype_to_proto_dtype(wmp.pyarrow_dtype),
                            filters=[cls.convert_filter(f) for f in wmp.filters],
                            backfill_lookback_duration=seconds_int_to_proto_duration(
                                wmp.backfill_lookback_duration_seconds
                            )
                            if wmp.backfill_lookback_duration_seconds is not None
                            else None,
                            backfill_schedule=wmp.backfill_schedule,
                            backfill_resolver=wmp.backfill_resolver,
                            backfill_start_time=datetime_to_proto_timestamp(wmp.backfill_start_time)
                            if wmp.backfill_start_time is not None
                            else None,
                            continuous_buffer_duration=seconds_int_to_proto_duration(
                                wmp.continuous_buffer_duration_seconds
                            )
                            if wmp.continuous_buffer_duration_seconds is not None
                            else None,
                            continuous_resolver=wmp.continuous_resolver,
                        )
                        if wmp is not None
                        else None,
                    )
                    if f.window_duration is not None
                    else None
                ),
                # The protos are nullable; the type hint is wrong
                etl_offline_to_online=cast(bool, f.raw_etl_offline_to_online),
                tags=f.tags,
                version=(
                    pb.VersionInfo(
                        default=f.version.default,
                        maximum=f.version.maximum,
                    )
                    if f.version
                    else None
                ),
                last_for=ToProtoConverter.create_feature_reference(f.last_for) if f.last_for else None,
                default_value=(
                    f.converter.from_primitive_to_protobuf(f.converter.primitive_default)
                    if f.converter.has_default
                    else None
                ),
                validations=ToProtoConverter.convert_validations(f.all_validations),
                expression=ToProtoConverter.convert_underscore(f.underscore_expression)
                if f.underscore_expression is not None
                else None,
                no_display=f.no_display,
                attribute_name=f.attribute_name if hasattr(f, "attribute_name") else None,
                unversioned_attribute_name=f.unversioned_attribute_name
                if hasattr(f, "unversioned_attribute_name")
                else None,
                is_deprecated=f.is_deprecated,
                cache_strategy=ToProtoConverter._cache_strategy_to_proto[f.cache_strategy],
                store_online=f.store_online,
                store_offline=f.store_offline,
                rich_type_info=rich_type_info,
            )
        )
        return res

    @staticmethod
    def _convert_feature(o: Feature) -> pb.FeatureType:
        if o.path:
            raise ValueError(f"Features with `path` not supported yet (feature={o})")
        elif o.group_by_windowed is not None:
            return ToProtoConverter.convert_group_by_feature(o)
        elif o.is_scalar:
            if o.is_windowed:  # nesting in o.is_scalar to prevent bugs
                return ToProtoConverter.convert_windowed(o)
            return ToProtoConverter.convert_scalar(o)
        elif o.is_feature_time:
            return ToProtoConverter.convert_feature_time_feature(o)
        elif o.is_has_one:
            return ToProtoConverter.convert_has_one(o)
        elif o.is_has_many:
            return ToProtoConverter.convert_has_many(o)

        raise ValueError(f"Unknown Feature object: {o}")

    @staticmethod
    def convert_feature(o: Feature) -> pb.FeatureType:
        try:
            return ToProtoConverter._convert_feature(o)
        except Exception as e:
            raise RuntimeError(f"Error converting feature '{o.namespace}.{o.name}'") from e

    @staticmethod
    def convert_dataframe(df: type[DataFrame]) -> pb.DataFrameType:
        return pb.DataFrameType(
            root_namespace=get_unique_item(x.root_namespace for x in df.columns if x.root_namespace != PSEUDONAMESPACE),
            optional_columns=()
            if df.__references_feature_set__ is not None
            else [ToProtoConverter.create_feature_reference(ensure_feature(c)) for c in df.columns],
            required_columns=(),
            filter=expr_pb.LogicalExprNode(
                binary_expr=expr_pb.BinaryExprNode(
                    operands=[ToProtoConverter.convert_filter(f) for f in df.filters],
                    op="and",
                )
            )
            if df.filters
            else None,
            limit=df.__limit__ if df.__limit__ is not None else None,
        )

    @classmethod
    def convert_online_or_offline_resolver(cls, r: Union[OnlineResolver, OfflineResolver]) -> pb.Resolver:
        if r.output is None:
            raise ValueError("Resolver missing `output` attribute")

        outputs = ToProtoConverter.convert_resolver_outputs(r.output.features or [])
        schedule = None
        cron_filter = None
        if r.cron is not None:
            if isinstance(r.cron, Cron):
                duration = None
                crontab = None
                if isinstance(r.cron.schedule, str):
                    try:
                        duration_td = parse_chalk_duration(r.cron.schedule)
                    except ValueError:
                        crontab = r.cron.schedule
                    else:
                        duration = timedelta_to_proto_duration(duration_td)
                elif isinstance(r.cron.schedule, timedelta):  # pyright: ignore[reportUnnecessaryIsInstance]
                    duration = timedelta_to_proto_duration(r.cron.schedule)
                else:
                    raise TypeError(f"Unknown cron schedule type: {type(r.cron.schedule).__name__}")

                cron_filter = ToProtoConverter.convert_cron_filter(r.cron) if r.cron.filter else None

                schedule = pb.Schedule(
                    filter=ToProtoConverter.create_function_reference(r.cron.filter)
                    if r.cron.filter is not None
                    else None,
                    sample=ToProtoConverter.create_function_reference(r.cron.sample) if r.cron.sample else None,
                    duration=duration,
                    crontab=crontab,
                )
            elif isinstance(r.cron, str):
                try:
                    duration_td = parse_chalk_duration(r.cron)
                except:
                    schedule = pb.Schedule(crontab=r.cron)
                else:
                    schedule = pb.Schedule(duration=timedelta_to_proto_duration(duration_td))
            elif isinstance(r.cron, timedelta):  # pyright: ignore[reportUnnecessaryIsInstance]
                schedule = pb.Schedule(duration=timedelta_to_proto_duration(r.cron))
            else:
                raise TypeError(f"Unknown cron type: {type(r.cron).__name__}")

        if r.resource_hint is None:
            resource_hint = None
        elif r.resource_hint == "cpu":
            resource_hint = pb.RESOURCE_HINT_CPU
        elif r.resource_hint == "io":
            resource_hint = pb.RESOURCE_HINT_IO
        elif r.resource_hint == "gpu":
            resource_hint = pb.RESOURCE_HINT_GPU
        else:
            raise ValueError(f"Unsupported resource hint: {r.resource_hint}")

        static_operation = None
        if r.static:
            static_operator = static_resolver_to_operator(fqn=r.fqn, fn=r.fn, inputs=r.inputs, output=r.output)
            static_operation = static_operator._to_proto()  # pyright: ignore[reportPrivateUsage]

        function_reference_proto = ToProtoConverter.create_function_reference(
            r.fn,
            definition=r.function_definition,
            captured_globals=r.function_captured_globals,
            filename=r.filename,
            source_line=r.source_line,
        )

        return pb.Resolver(
            fqn=r.fqn,
            kind=(
                pb.ResolverKind.RESOLVER_KIND_ONLINE
                if isinstance(r, OnlineResolver)
                else pb.ResolverKind.RESOLVER_KIND_OFFLINE
            ),
            inputs=ToProtoConverter.convert_resolver_inputs(r.inputs, r.state, r.default_args),
            outputs=outputs,
            is_generator=inspect.isgeneratorfunction(r.fn) or inspect.isasyncgenfunction(r.fn),
            data_sources_v2=[ToProtoConverter.create_database_source_reference(s) for s in (r.data_sources or [])],
            machine_type=r.machine_type,
            tags=r.tags,
            resource_hint=resource_hint,
            is_static=r.static,
            owner=r.owner,
            doc=r.doc,
            environments=r.environment,
            timeout_duration=timedelta_to_proto_duration(r.timeout) if r.timeout is not None else None,
            schedule=schedule,
            when=ToProtoConverter.convert_filter(r.when) if r.when else None,
            cron_filter=cron_filter,
            function=function_reference_proto,
            is_total=r.total,
            unique_on=tuple(x.root_fqn for x in r.unique_on) if r.unique_on is not None else (),
            partitioned_by=(x.root_fqn for x in r.partitioned_by) if r.partitioned_by is not None else (),
            static_operation=static_operation,
            sql_settings=ToProtoConverter.convert_sql_settings(r.sql_settings) if r.sql_settings else None,
        )

    @staticmethod
    def convert_stream_resolver_param(p: StreamResolverParam) -> pb.StreamResolverParam:
        if isinstance(p, StreamResolverParamMessage):
            try:
                maybe_type = ToProtoConverter.convert_rich_type_to_protobuf(p.typ)
            except:
                # TODO: Stream message types are often more expressive than we can
                #       currently serialize. But we don't want to block `chalk apply`
                #       until we absolutely must need the Arrow type to be serialized.
                maybe_type = None

            return pb.StreamResolverParam(
                message=pb.StreamResolverParamMessage(
                    name=p.name,
                    arrow_type=maybe_type,
                )
            )
        elif isinstance(p, StreamResolverParamMessageWindow):
            try:
                maybe_type = ToProtoConverter.convert_rich_type_to_protobuf(p.typ)
            except:
                # TODO: Stream message types are often more expressive than we can
                #       currently serialize. But we don't want to block `chalk apply`
                #       until we absolutely must need the Arrow type to be serialized.
                maybe_type = None
            return pb.StreamResolverParam(
                message_window=pb.StreamResolverParamMessageWindow(
                    name=p.name,
                    arrow_type=maybe_type,
                )
            )
        elif isinstance(p, StreamResolverParamKeyedState):
            converter = FeatureConverter(
                name="helper", is_nullable=False, rich_type=p.typ, rich_default=p.default_value
            )
            arrow_type = None
            if converter:
                try:
                    arrow_type = converter.convert_pa_dtype_to_proto_dtype(converter.pyarrow_dtype)
                except:
                    # TODO: Stream message types are often more expressive than we can
                    #       currently serialize. But we don't want to block `chalk apply`
                    #       until we absolutely must need the Arrow type to be serialized.
                    pass

            initial = None
            if converter:
                try:
                    initial = converter.from_rich_to_protobuf(p.default_value)
                except:
                    # TODO: Stream message types are often more expressive than we can
                    #       currently serialize. But we don't want to block `chalk apply`
                    #       until we absolutely must need the Arrow type to be serialized.
                    pass

            return pb.StreamResolverParam(state=pb.ResolverState(arrow_type=arrow_type, initial=initial))
        else:
            raise TypeError(f"Unknown param type: {type(p).__name__}")

    @classmethod
    def convert_parse_info(cls, info: ParseInfo) -> pb.ParseInfo:
        try:
            maybe_input_type = ToProtoConverter.convert_rich_type_to_protobuf(info.input_type)
        except:
            # TODO: Stream message types are often more expressive than we can
            #       currently serialize. But we don't want to block `chalk apply`
            #       until we absolutely must need the Arrow type to be serialized.
            maybe_input_type = None

        try:
            maybe_output_type = ToProtoConverter.convert_rich_type_to_protobuf(info.output_type)
        except:
            # TODO: Stream message types are often more expressive than we can
            #       currently serialize. But we don't want to block `chalk apply`
            #       until we absolutely must need the Arrow type to be serialized.
            maybe_output_type = None

        return pb.ParseInfo(
            parse_function_input_type=maybe_input_type,
            parse_function_output_type=maybe_output_type,
            parse_function=ToProtoConverter.create_function_reference(info.fn),
            is_parse_function_output_optional=info.output_is_optional,
            parse_function_input_type_name=info.input_type.__name__,
            parse_function_output_type_name=info.output_type.__name__,
        )

    @classmethod
    def convert_stream_resolver(cls, r: StreamResolver) -> pb.StreamResolver:
        mode: pb.WindowMode | None = None
        if r.mode:
            mode = cls._mode_to_proto.get(r.mode)
            if mode is None:
                raise ValueError(f"Unknown window mode: {r.mode}")

        return pb.StreamResolver(
            fqn=r.fqn,
            params=[ToProtoConverter.convert_stream_resolver_param(p) for p in r.signature.params],
            outputs=ToProtoConverter.convert_resolver_outputs(r.output.features)
            if r.output and r.output.features
            else [],
            explicit_schema=(ToProtoConverter.convert_rich_type_to_protobuf(r.message) if r.message else None),
            keys=(
                [
                    pb.StreamKey(key=k, feature=ToProtoConverter.create_feature_reference(ensure_feature(v)))
                    for k, v in r.keys.items()
                ]
                if r.keys is not None
                else None
            ),
            source_v2=ToProtoConverter.create_stream_source_reference(r.source),
            parse_info=ToProtoConverter.convert_parse_info(r.parse) if r.parse else None,
            mode=mode,
            environments=r.environment or [],
            timeout_duration=timedelta_to_proto_duration(r.timeout) if r.timeout is not None else None,
            timestamp_attribute_name=r.timestamp,
            owner=r.owner,
            doc=r.doc,
            machine_type=r.machine_type,
            function=ToProtoConverter.create_function_reference(
                r.fn,
                definition=r.function_definition,
                filename=r.filename,
                source_line=r.source_line,
                captured_globals=r.function_captured_globals,
            ),
        )

    @staticmethod
    def convert_sink_resolver(r: SinkResolver) -> pb.SinkResolver:
        stream_source = None
        database_source = None

        if r.integration:
            if isinstance(r.integration, BaseSQLSource):
                database_source = ToProtoConverter.create_database_source_reference(r.integration)
            elif isinstance(r.integration, StreamSource):
                stream_source = ToProtoConverter.create_stream_source_reference(r.integration)
            else:
                raise TypeError(f"Unsupported integration type: {type(r.integration).__name__}")

        ans = pb.SinkResolver(
            fqn=r.fqn,
            inputs=ToProtoConverter.convert_resolver_inputs(r.inputs, r.state, r.default_args),
            buffer_size=r.buffer_size if r.buffer_size is not None else None,
            debounce_duration=timedelta_to_proto_duration(r.debounce) if r.debounce is not None else None,
            max_delay_duration=timedelta_to_proto_duration(r.max_delay) if r.max_delay is not None else None,
            upsert=r.upsert,
            machine_type=r.machine_type,
            doc=r.doc,
            owner=r.owner,
            environments=r.environment or [],
            timeout_duration=timedelta_to_proto_duration(r.timeout) if r.timeout is not None else None,
            function=ToProtoConverter.create_function_reference(
                r.fn,
                definition=r.function_definition,
                filename=r.filename,
                source_line=r.source_line,
                captured_globals=r.function_captured_globals,
            ),
        )
        if stream_source is not None:
            ans.stream_source_v2 = stream_source
        if database_source is not None:
            ans.database_source_v2 = database_source
        return ans

    @staticmethod
    def _convert_resolver(r: Resolver) -> Union[pb.Resolver, pb.StreamResolver, pb.SinkResolver]:
        if isinstance(r, (OnlineResolver, OfflineResolver)):
            return ToProtoConverter.convert_online_or_offline_resolver(r)
        elif isinstance(r, StreamResolver):
            return ToProtoConverter.convert_stream_resolver(r)
        elif isinstance(r, SinkResolver):
            return ToProtoConverter.convert_sink_resolver(r)
        else:
            raise TypeError(f"Unknown resolver type: {type(r).__name__}")

    @staticmethod
    def convert_resolver(r: Resolver) -> Union[pb.Resolver, pb.StreamResolver, pb.SinkResolver]:
        try:
            return ToProtoConverter._convert_resolver(r)
        except Exception as e:
            raise ValueError(f"Error converting resolver '{r.fqn}'") from e

    @staticmethod
    def convert_graph(
        features_registry: dict[str, type[Features]],
        resolver_registry: Collection[Resolver],
        sql_source_registry: Collection[BaseSQLSource],
        sql_source_group_registry: Collection[SQLSourceGroup],
        stream_source_registry: Collection[StreamSource],
        named_query_registry: dict[tuple[str, Optional[str]], NamedQuery],
    ) -> pb.Graph:
        feature_sets = []
        for feature_set in features_registry.values():
            features = []
            for f in feature_set.features:
                features.append(ToProtoConverter.convert_feature(f))

            feature_sets.append(
                pb.FeatureSet(
                    name=feature_set.namespace,
                    features=features,
                    is_singleton=feature_set.__chalk_is_singleton__,
                    max_staleness_duration=timedelta_to_proto_duration(feature_set.__chalk_max_staleness__),
                    tags=feature_set.__chalk_tags__,
                    owner=feature_set.__chalk_owner__,
                    doc=feature_set.__doc__,
                    etl_offline_to_online=feature_set.__chalk_etl_offline_to_online__,
                    class_path=paths.get_classpath_or_name(feature_set),
                )
            )

        resolvers: list[pb.Resolver] = []
        stream_resolvers: list[pb.StreamResolver] = []
        sink_resolvers: list[pb.SinkResolver] = []
        named_queries: list[pb.NamedQuery] = []

        for resolver in resolver_registry:
            converted = ToProtoConverter.convert_resolver(resolver)
            if isinstance(converted, pb.Resolver):
                resolvers.append(converted)
            elif isinstance(converted, pb.StreamResolver):
                stream_resolvers.append(converted)
            elif isinstance(converted, pb.SinkResolver):  # pyright: ignore[reportUnnecessaryIsInstance]
                sink_resolvers.append(converted)
            else:
                raise TypeError(f"Unsupported resolver type: {converted}")
        for named_query in named_query_registry.values():
            named_queries.append(ToProtoConverter._convert_named_query(named_query))

        return pb.Graph(
            feature_sets=feature_sets,
            resolvers=resolvers,
            stream_resolvers=stream_resolvers,
            sink_resolvers=sink_resolvers,
            database_sources_v2=[ToProtoConverter.convert_sql_source(s) for s in sql_source_registry],
            database_source_groups=[ToProtoConverter.convert_sql_source_group(s) for s in sql_source_group_registry],
            stream_sources_v2=[ToProtoConverter.convert_stream_source(s) for s in stream_source_registry],
            named_queries=named_queries,
        )

    @classmethod
    def convert_sql_settings(cls, source: SQLResolverSettings) -> pb.SQLResolverSettings:
        """
        Inverts `convert_sql_settings`: creates a pb.SQLResolverSettings from a SQLResolverSettings object.
        """
        return pb.SQLResolverSettings(
            finalizer=cls.convert_finalizer(source.finalizer),
            incremental_settings=(
                cls.convert_incremental_settings(source.incremental_settings)
                if source.incremental_settings is not None
                else None
            ),
            fields_root_fqn=source.fields_root_fqn,
            escaped_param_name_to_fqn=source.params_to_root_fqn,
        )

    @classmethod
    def convert_finalizer(cls, source: Finalizer) -> pb.Finalizer:
        """
        Inverts `convert_finalizer`: creates a pb.Finalizer from a Finalizer enum/constant.
        """
        if source == Finalizer.ONE_OR_NONE:
            return pb.Finalizer.FINALIZER_ONE_OR_NONE
        elif source == Finalizer.ONE:
            return pb.Finalizer.FINALIZER_ONE
        elif source == Finalizer.FIRST:
            return pb.Finalizer.FINALIZER_FIRST
        elif source == Finalizer.ALL:
            return pb.Finalizer.FINALIZER_ALL
        else:
            assert_never(source)

    @classmethod
    def convert_incremental_settings(cls, source: IncrementalSettings) -> pb.IncrementalSettings:
        """
        Inverts `convert_incremental_settings`: creates a pb.IncrementalSettings from an IncrementalSettings object.
        """
        if source.mode == "row":
            mode = pb.IncrementalMode.INCREMENTAL_MODE_ROW
        elif source.mode == "group":
            mode = pb.IncrementalMode.INCREMENTAL_MODE_GROUP
        elif source.mode == "parameter":
            mode = pb.IncrementalMode.INCREMENTAL_MODE_PARAMETER
        else:
            assert_never(source.mode)

        if source.incremental_timestamp == "feature_time":
            timestamp_mode = pb.IncrementalTimestampMode.INCREMENTAL_TIMESTAMP_MODE_FEATURE_TIME
        elif source.incremental_timestamp == "resolver_execution_time":
            timestamp_mode = pb.IncrementalTimestampMode.INCREMENTAL_TIMESTAMP_MODE_RESOLVER_EXECUTION_TIME
        else:
            assert_never(source.incremental_timestamp)

        settings = pb.IncrementalSettings(
            mode=mode,
            timestamp_mode=timestamp_mode,
        )
        if source.lookback_period is not None:
            # Convert from Python timedelta to the protobuf Duration field
            settings.lookback_period.FromTimedelta(source.lookback_period)
        if source.incremental_column is not None:
            settings.incremental_column = source.incremental_column

        return settings
