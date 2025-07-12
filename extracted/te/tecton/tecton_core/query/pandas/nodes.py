import inspect
import itertools
import logging
import typing
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pandas
import pyarrow

import tecton_core.tecton_pendulum as pendulum
from tecton_core import conf
from tecton_core import specs
from tecton_core.arrow import arrow_to_pandas_dataframe
from tecton_core.data_types import BoolType
from tecton_core.data_types import Float32Type
from tecton_core.data_types import Float64Type
from tecton_core.data_types import Int32Type
from tecton_core.data_types import Int64Type
from tecton_core.data_types import StringType
from tecton_core.data_types import TimestampType
from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.filter_context import FilterContext
from tecton_core.id_helper import IdHelper
from tecton_core.iterators import batched_iterator
from tecton_core.materialization_context import MaterializationContext
from tecton_core.query.errors import UserCodeError
from tecton_core.query.executor_params import ExecutionContext
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import PartitionSelector
from tecton_core.query.node_interface import SinglePartition
from tecton_core.query.nodes import StagingNode
from tecton_core.query.pandas.node import ArrowExecNode
from tecton_core.query.pandas.node import SqlExecNode
from tecton_core.query.pandas.pandas_rtfv_pipeline import PandasRealtimeFeaturePipeline
from tecton_core.resource_provider_context import ResourceProviderContext
from tecton_core.schema import Schema
from tecton_core.schema_validation import CastError
from tecton_core.schema_validation import DiffResult
from tecton_core.schema_validation import cast
from tecton_core.schema_validation import cast_columns
from tecton_core.schema_validation import tecton_schema_to_arrow_schema
from tecton_core.secret_management import SecretResolver
from tecton_core.skew_config import SkewConfig
from tecton_proto.args.pipeline__client_pb2 import DataSourceNode
from tecton_proto.args.pipeline__client_pb2 import PipelineNode
from tecton_proto.args.pipeline__client_pb2 import TransformationNode
from tecton_proto.args.transformation__client_pb2 import TransformationMode
from tecton_proto.common import secret__client_pb2 as secret_pb2
from tecton_proto.common.data_source_type__client_pb2 import DataSourceType


logger = logging.getLogger(__name__)

# Maps a tecton datatype to the correct pandas datatype which is to be used when an output schema is defined by the user
PRIMITIVE_TECTON_DATA_TYPE_TO_PANDAS_DATA_TYPE = {
    Int32Type(): "int32",
    Int64Type(): "int64",
    Float32Type(): "float32",
    Float64Type(): "float64",
    StringType(): "string",
    BoolType(): "bool",
    TimestampType(): "datetime64[ns]",
}

RESOURCE_CONTEXT_PARAM_NAME = "context"


@attrs.frozen
class PandasDataSourceScanNode(ArrowExecNode):
    ds: specs.DataSourceSpec
    ds_node: Optional[DataSourceNode]
    is_stream: bool = attrs.field()
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    skew_config: Optional[SkewConfig] = None

    def as_str(self):
        return "ArrowExec node for Pandas data source"

    @property
    def output_partitioning(self):
        return SinglePartition()

    def to_arrow_reader(
        self, context: ExecutionContext, partition_selector: Optional["PartitionSelector"] = None
    ) -> pyarrow.RecordBatchReader:
        batch_source = self.ds.batch_source
        assert isinstance(batch_source, specs.PandasBatchSourceSpec)

        df = self._get_ds_from_dsf(batch_source, self.ds.name, context.secret_resolver)

        if self.ds.type == DataSourceType.STREAM_WITH_BATCH:
            schema = self.ds.stream_source.spark_schema
            cols = [field.name for field in schema.fields]
            df = df[cols]
        elif self.ds.type == DataSourceType.PUSH_WITH_BATCH:
            schema = self.ds.schema.tecton_schema
            cols = [field.name for field in schema.columns]
            df = df[cols]

        # ToDo: use cast instead, when data source schema will be available for all data sources
        batch = pyarrow.RecordBatch.from_pandas(df, preserve_index=False)
        return pyarrow.RecordBatchReader.from_batches(batch.schema, [batch])

    def _get_ds_from_dsf(
        self,
        batch_source: specs.PandasBatchSourceSpec,
        data_source_name: str,
        secret_resolver: Optional[SecretResolver],
    ) -> pandas.DataFrame:
        function_args = {}
        if batch_source.supports_time_filtering:
            function_args["filter_context"] = FilterContext(self.start_time, self.end_time)
        if batch_source.secrets:
            if secret_resolver is None:
                msg = "No secret resolver was provided. For Local Development, please set secrets to string literals."
                raise TectonValidationError(msg)
            function_args["secrets"] = secret_resolver.resolve_map(batch_source.secrets)
        try:
            ret = batch_source.function(**function_args)
        except Exception as exc:
            msg = f"Evaluating Pandas data source '{data_source_name}' failed with exception."
            raise UserCodeError(msg) from exc

        if not isinstance(ret, pandas.DataFrame):
            msg = (
                f"The function of Pandas data source '{data_source_name}' is expected to return result "
                f"with Pandas DataFrame type, but returned result with type {type(ret)} instead."
            )
            raise TectonValidationError(msg, can_drop_traceback=True)

        return ret


@attrs.frozen
class PyArrowDataSourceScanNode(ArrowExecNode):
    ds: specs.DataSourceSpec
    ds_node: Optional[DataSourceNode]
    is_stream: bool = attrs.field()
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    skew_config: Optional[SkewConfig] = None

    def as_str(self):
        return "ArrowExec node for PyArrow data source"

    @property
    def output_partitioning(self):
        return SinglePartition()

    def to_arrow_reader(
        self, context: ExecutionContext, partition_selector: Optional["PartitionSelector"] = None
    ) -> pyarrow.RecordBatchReader:
        batch_source = self.ds.batch_source
        assert isinstance(batch_source, specs.PyArrowBatchSourceSpec)

        if self.ds.type == DataSourceType.STREAM_WITH_BATCH:
            schema = self.ds.stream_source.spark_schema
            cols = [field.name for field in schema.fields]
        elif self.ds.type == DataSourceType.PUSH_WITH_BATCH:
            schema = self.ds.schema.tecton_schema
            cols = [field.name for field in schema.columns]
        else:
            cols = None

        table_or_reader = self._get_reader_or_table_from_dsf(batch_source, self.ds.name, context.secret_resolver)
        if isinstance(table_or_reader, pyarrow.Table):
            return self._get_reader_from_table(table_or_reader, cols)
        else:
            assert isinstance(table_or_reader, pyarrow.RecordBatchReader), (
                "Invalid type of table_or_reader. Expected pyarrow.Table or pyarrow.RecordBatchReader"
            )
            return self._get_reader_from_raw_reader(table_or_reader, cols)

    def _get_reader_from_table(self, table: pyarrow.Table, cols: Optional[List[str]]) -> pyarrow.RecordBatchReader:
        if cols is None:
            return table.to_reader()
        return table.select(cols).to_reader()

    def _get_reader_from_raw_reader(
        self, raw_data_reader: pyarrow.RecordBatchReader, cols: Optional[List[str]]
    ) -> pyarrow.RecordBatchReader:
        if cols is None:
            return raw_data_reader
        # Don't iterate through batches if the schemas already match.
        if raw_data_reader.schema.names == cols:
            return raw_data_reader

        filtered_batches = []
        for batch in raw_data_reader:
            filtered_batches.append(batch.select(cols))
        return pyarrow.RecordBatchReader.from_batches(filtered_batches[0].schema, filtered_batches)

    def _get_reader_or_table_from_dsf(
        self,
        batch_source: specs.PyArrowBatchSourceSpec,
        data_source_name: str,
        secret_resolver: Optional[SecretResolver],
    ) -> Union[pyarrow.Table, pyarrow.RecordBatchReader]:
        function_args = {}
        if batch_source.supports_time_filtering:
            function_args["filter_context"] = FilterContext(self.start_time, self.end_time)
        if batch_source.secrets:
            if secret_resolver is None:
                msg = "No secret resolver was provided. For Local Development, please set secrets to string literals."
                raise TectonValidationError(msg)
            function_args["secrets"] = secret_resolver.resolve_map(batch_source.secrets)
        try:
            ret = batch_source.function(**function_args)
        except Exception as exc:
            msg = f"Evaluating PyArrow data source '{data_source_name}' failed with exception."
            raise UserCodeError(msg) from exc

        if not isinstance(ret, pyarrow.Table) and not isinstance(ret, pyarrow.RecordBatchReader):
            msg = (
                f"The function of PyArrow data source '{data_source_name}' is expected to return result "
                f"with PyArrow Table or PyArrow RecordBatchReader type, but returned result with type {type(ret)} instead."
            )
            raise TectonValidationError(msg, can_drop_traceback=True)

        return ret


@attrs.frozen
class PandasFeatureViewPipelineNode(ArrowExecNode):
    inputs_map: Dict[str, NodeRef]
    feature_definition_wrapper: FeatureDefinitionWrapper
    feature_time_limits: Optional[pendulum.Period]

    # `check_view_schema` is not actually used in pandas node. Having it here to keep all QT node can be intialized consistently.
    check_view_schema: bool

    # Mock context with resources and secrets for testing
    mock_context: Optional[MaterializationContext]

    def to_arrow_reader(
        self, context: ExecutionContext, partition_selector: Optional["PartitionSelector"] = None
    ) -> pyarrow.Table:
        table = self._node_to_value(self.feature_definition_wrapper.pipeline.root, context)
        return table

    @property
    def inputs(self) -> typing.Sequence[NodeRef]:
        return list(self.inputs_map.values())

    @property
    def input_names(self) -> Optional[List[str]]:
        return list(self.inputs_map.keys())

    @property
    def output_partitioning(self):
        return next(iter(self.inputs_map.values())).output_partitioning

    def as_str(self):
        s = f"ArrowExec node for feature view pipeline ({self.feature_definition_wrapper.name}) in Pandas mode"
        return s

    def _node_to_value(
        self, pipeline_node: PipelineNode, context: ExecutionContext
    ) -> Union[pyarrow.RecordBatchReader, MaterializationContext]:
        if pipeline_node.HasField("transformation_node"):
            return self._transformation_node_to_dataframe(pipeline_node.transformation_node, context)
        elif pipeline_node.HasField("data_source_node"):
            ds_query_node = self.inputs_map[pipeline_node.data_source_node.input_name].node
            assert isinstance(ds_query_node, (ArrowExecNode, StagingNode)), (
                "A PandasFeatureViewPipelineNode cannot operate on standard DataSourceScanNodes. They must have been replaced by PandasDataNodes."
            )
            return ds_query_node.to_arrow_reader(context)
        elif pipeline_node.HasField("materialization_context_node") or pipeline_node.HasField("context_node"):
            feature_start_time = None
            feature_end_time = None
            if self.feature_time_limits:
                feature_start_time = self.feature_time_limits.start
                feature_end_time = self.feature_time_limits.end

            secrets = self._get_secrets(self.feature_definition_wrapper.fv_spec.secrets, context)

            # Override secrets with mock context if provided
            if self.mock_context and self.mock_context.secrets:
                secrets = {**secrets, **self.mock_context.secrets}

            mock_secrets = self.mock_context.secrets if self.mock_context else None

            resources = (
                self.mock_context.resources
                if self.mock_context and self.mock_context.resources
                else self._get_resources(self.feature_definition_wrapper.resource_providers, context, mock_secrets)
            )

            return MaterializationContext(
                _start_time=feature_start_time,
                _end_time=feature_end_time,
                secrets=secrets,
                resources=resources,
            )
        else:
            msg = f"Pipeline node of kind {pipeline_node.WhichOneof('node_type')} is not supported in Pandas mode"
            raise NotImplementedError(msg)

    @staticmethod
    def _get_secrets(
        secrets: Optional[Mapping[str, secret_pb2.SecretReference]], execution_context: ExecutionContext
    ) -> Dict[str, Any]:
        resolved_secrets = {}
        if secrets:
            if not execution_context.secret_resolver:
                msg = "No secret resolver was provided."
                raise TectonInternalError(msg)
            resolved_secrets = execution_context.secret_resolver.resolve_map(secrets)
        return resolved_secrets

    @staticmethod
    def _get_resources(
        resource_provider_specs: Mapping[str, specs.ResourceProviderSpec],
        execution_context: ExecutionContext,
        mock_secrets: Optional[Mapping[str, str]] = None,
    ) -> Dict[str, Any]:
        resources = {}
        for key, resource_provider_spec in resource_provider_specs.items():
            signature_args = inspect.signature(resource_provider_spec.function).parameters.keys()
            function_args = (
                {RESOURCE_CONTEXT_PARAM_NAME: ResourceProviderContext()}
                if RESOURCE_CONTEXT_PARAM_NAME in signature_args
                else {}
            )

            if resource_provider_spec.secrets:
                if execution_context.secret_resolver:
                    secrets = execution_context.secret_resolver.resolve_spec_map(resource_provider_spec.secrets)
                else:
                    msg = (
                        "No secret resolver was provided. For Local Development, please set secrets to string literals."
                    )
                    raise TectonInternalError(msg)

                function_args[RESOURCE_CONTEXT_PARAM_NAME] = ResourceProviderContext(
                    secrets={**secrets, **(mock_secrets or {})}
                )
            try:
                resources[key] = resource_provider_spec.function(**function_args)
            except Exception as exc:
                msg = f"Invoking Resource Provider: '{resource_provider_spec.name}' failed with exception."
                raise UserCodeError(msg) from exc
        return resources

    def _node_inputs_to_pandas_udf_args(
        self, node: TransformationNode, context: ExecutionContext
    ) -> Tuple[List[Any], Dict[str, Any]]:
        args = []
        kwargs = {}

        for transformation_input in node.inputs:
            node_value = self._node_to_value(transformation_input.node, context)
            if isinstance(node_value, pyarrow.RecordBatchReader):
                use_arrow_types = conf.get_bool("USE_ARROW_TYPES_IN_PANDAS_TRANSFORMATION")
                node_value = arrow_to_pandas_dataframe(node_value, use_arrow_types=use_arrow_types)
            else:
                assert isinstance(node_value, (MaterializationContext,))

            if transformation_input.HasField("arg_index"):
                assert len(args) == transformation_input.arg_index
                args.append(node_value)
            elif transformation_input.HasField("arg_name"):
                kwargs[transformation_input.arg_name] = node_value
            else:
                msg = f"Unknown argument type for Input node: {transformation_input}"
                raise KeyError(msg)

        return args, kwargs

    def _node_inputs_to_python_udf_args(
        self, node: TransformationNode, context: ExecutionContext
    ) -> Iterable[Tuple[List[Any], Dict[str, Any]]]:
        """Returns iterator producing tuples (args, kwargs).
        Each tuple represents individual call of python UDF with a single row from input arrow dataframe.
        """
        args = []
        kwargs = {}
        for transformation_input in node.inputs:
            node_value = self._node_to_value(transformation_input.node, context)
            if isinstance(node_value, pyarrow.RecordBatchReader):

                def row_iterator(reader):
                    while True:
                        try:
                            yield from reader.read_next_batch().to_pylist()
                        except StopIteration:
                            return

                node_value = row_iterator(node_value)
            else:
                assert isinstance(node_value, (MaterializationContext,))
                node_value = itertools.repeat(node_value)

            if transformation_input.HasField("arg_index"):
                assert len(args) == transformation_input.arg_index
                args.append(node_value)
            elif transformation_input.HasField("arg_name"):
                kwargs[transformation_input.arg_name] = node_value
            else:
                msg = f"Unknown argument type for Input node: {transformation_input}"
                raise KeyError(msg)

        assert args or kwargs
        return zip(
            zip(*args) if args else itertools.repeat([]),
            (dict(zip(kwargs.keys(), kwargs_values)) for kwargs_values in zip(*kwargs.values()))
            if kwargs
            else itertools.repeat({}),
        )

    def _transformation_node_to_dataframe(
        self, transformation_node: TransformationNode, context: ExecutionContext
    ) -> pyarrow.RecordBatchReader:
        """Recursively translates inputs to values and then passes them to the transformation."""

        id_to_transformation = {t.id: t for t in self.feature_definition_wrapper.transformations}
        transformation = id_to_transformation[IdHelper.to_string(transformation_node.transformation_id)]
        user_function = transformation.user_function

        if transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PANDAS:
            return self._call_pandas_udf_and_verify_result(
                transformation_node, user_function, self.feature_definition_wrapper.view_schema, context
            )

        if transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PYTHON:
            return self._call_python_udf_and_verify_result(
                transformation_node, user_function, self.feature_definition_wrapper.view_schema, context
            )

        msg = (
            f"Unknown transformation mode {transformation.transformation_mode} "
            f"in feature view {self.feature_definition_wrapper.fv_spec.name}"
        )
        raise TectonValidationError(msg)

    def _call_pandas_udf_and_verify_result(
        self,
        transformation_node: TransformationNode,
        user_function: typing.Callable,
        expected_schema: Schema,
        context: ExecutionContext,
    ) -> pyarrow.RecordBatchReader:
        args, kwargs = self._node_inputs_to_pandas_udf_args(transformation_node, context)
        try:
            ret = user_function(*args, **kwargs)
        except Exception as exc:
            msg = (
                "Pandas pipeline function (feature view "
                f"'{self.feature_definition_wrapper.fv_spec.name}') "
                f"failed with exception"
            )
            raise UserCodeError(msg) from exc
        try:
            if not isinstance(ret, pandas.DataFrame):
                msg = f"Expected a Pandas Dataframe, but returned {type(ret)}"
                raise CastError(msg)
            return cast(ret, schema=expected_schema).to_reader()
        except CastError as exc:
            validation_msg = (
                f"Pipeline function (feature view '{self.feature_definition_wrapper.fv_spec.name}') produced an "
                + "invalid result: "
            )
            raise CastError(validation_msg + str(exc)) from None

    def _call_python_udf_and_verify_result(
        self,
        transformation_node: TransformationNode,
        user_function: typing.Callable,
        expected_schema: Schema,
        context: ExecutionContext,
    ) -> pyarrow.RecordBatchReader:
        input_it = self._node_inputs_to_python_udf_args(transformation_node, context)

        def record_batch_iterator():
            for input_batch in batched_iterator(input_it, batch_size=1_000_000):
                columns = {name: [] for name in expected_schema.column_names()}
                try:
                    for args, kwargs in input_batch:
                        try:
                            ret = user_function(*args, **kwargs)
                            if not isinstance(ret, dict):
                                other_type = type(ret)
                                msg = f"Expected a Python dict, but returned {other_type}"
                                raise CastError(msg)
                        except Exception as exc:
                            msg = (
                                "Python pipeline function (feature view "
                                f"'{self.feature_definition_wrapper.fv_spec.name}') "
                                f"failed with exception"
                            )
                            raise UserCodeError(msg) from exc
                        for name in columns:
                            if name not in ret:
                                raise CastError.for_diff(DiffResult(missing_fields=[name]))
                            columns[name].append(ret[name])

                    def column_array(name: str, dtype: pyarrow.DataType) -> pyarrow.Array:
                        col = columns[name]
                        return pyarrow.array(col, type=dtype, size=len(col))

                    arrow_schema = tecton_schema_to_arrow_schema(expected_schema)
                    arrays = cast_columns(
                        column_getter=column_array, schema=tecton_schema_to_arrow_schema(expected_schema)
                    )
                    yield pyarrow.RecordBatch.from_arrays(arrays, schema=arrow_schema)
                except CastError as e:
                    validation_msg = (
                        f"Pipeline function (feature view '{self.feature_definition_wrapper.fv_spec.name}') produced an "
                        + "invalid result: "
                    )
                    raise CastError(validation_msg + str(e)) from None

        schema = tecton_schema_to_arrow_schema(expected_schema)
        return pyarrow.RecordBatchReader.from_batches(schema, record_batch_iterator())


@attrs.frozen
class ArrowDataNode(ArrowExecNode):
    input_reader: pyarrow.RecordBatchReader

    @property
    def output_partitioning(self):
        return SinglePartition()

    def to_arrow_reader(
        self, context: ExecutionContext, partition_selector: Optional["PartitionSelector"] = None
    ) -> pyarrow.RecordBatchReader:
        return self.input_reader

    def _to_dataframe(self):
        return self.to_arrow_reader(None).read_pandas()

    def as_str(self):
        return "ArrowDataNode"


@attrs.frozen
class PandasMultiOdfvPipelineNode(ArrowExecNode):
    input_node: Union[ArrowExecNode, SqlExecNode]
    feature_definition_namespaces: List[Tuple[FeatureDefinitionWrapper, str]]
    use_namespace_feature_prefix: bool
    events_df_timestamp_field: str

    def _to_dataframe(self):
        # ToDo(Oleksii): this method should be deprecated together with Snowflake & Athena computes

        if isinstance(self.input_node, ArrowExecNode):
            output_df = arrow_to_pandas_dataframe(self.input_node.to_arrow_reader())
        else:
            output_df = self.input_node._to_dataframe()
        # Apply each ODFV sequentially. Note that attempting to apply ODFV
        # udfs in parallel as we traverse data rows does not meaningfully
        # speed up execution on Athena (unlike in Spark).
        for fdw, namespace in self.feature_definition_namespaces:
            odfv_result_df = self._get_odfv_output_df(output_df, fdw, namespace)
            output_df = output_df.merge(odfv_result_df, left_index=True, right_index=True)
        return output_df

    @property
    def input_names(self) -> Optional[List[str]]:
        return ["odfv_input"]

    def as_str(self):
        return f"ArrowExec node for RTFV execution of {', '.join([fdw.name for fdw, _ in self.feature_definition_namespaces])}"

    def to_arrow_reader(
        self, context: ExecutionContext, partition_selector: Optional["PartitionSelector"] = None
    ) -> pyarrow.RecordBatchReader:
        reader = self.input_node.to_arrow_reader(context, partition_selector)

        output_schema = reader.schema
        for fdw, namespace in self.feature_definition_namespaces:
            arrow_schema = tecton_schema_to_arrow_schema(fdw.view_schema)
            for name, type_ in zip(arrow_schema.names, arrow_schema.types):
                if self.use_namespace_feature_prefix:
                    mapped_name = self.column_name_updater(f"{namespace}{fdw.namespace_separator}{name}")
                else:
                    mapped_name = name
                output_schema = output_schema.append(pyarrow.field(mapped_name, type_))

        def batch_iter():
            while True:
                try:
                    batch = reader.read_next_batch()
                except StopIteration:
                    return

                output_columns = batch.columns
                for fdw, namespace in self.feature_definition_namespaces:
                    realtime_pipeline = PandasRealtimeFeaturePipeline.from_feature_definition(
                        fdw,
                        batch,
                        self.column_name_updater,
                        self.events_df_timestamp_field,
                        secret_resolver=context.secret_resolver,
                    )
                    odfv_result_df = realtime_pipeline.get_dataframe()

                    try:
                        odfv_result = cast(odfv_result_df, fdw.view_schema)
                    except CastError as exc:
                        msg = f"ODFV '{fdw.name}' produced unexpected result that doesn't match output schema: "
                        raise CastError(msg + str(exc)) from None

                    for column in odfv_result.columns:
                        output_columns.append(column.combine_chunks())

                yield pyarrow.RecordBatch.from_arrays(output_columns, schema=output_schema)

        return pyarrow.RecordBatchReader.from_batches(output_schema, batch_iter())

    def _get_odfv_output_df(
        self,
        input_df: pandas.DataFrame,
        fdw: FeatureDefinitionWrapper,
        namespace: str,
    ) -> pandas.DataFrame:
        realtime_pipeline = PandasRealtimeFeaturePipeline.from_feature_definition(
            fdw,
            input_df,
            self.column_name_updater,
            self.events_df_timestamp_field,
        )
        odfv_result_df = realtime_pipeline.get_dataframe()
        rename_map = {}
        datatypes = {}
        # Namespace ODFV outputs to this FV to avoid conflicts in output schemas
        # with other FV
        output_schema = fdw.view_schema.column_name_and_data_types()
        for column_name, datatype in output_schema:
            if self.use_namespace_feature_prefix:
                mapped_name = self.column_name_updater(f"{namespace}{fdw.namespace_separator}{column_name}")
            else:
                mapped_name = column_name
            rename_map[column_name] = mapped_name
            if datatype in PRIMITIVE_TECTON_DATA_TYPE_TO_PANDAS_DATA_TYPE:
                datatypes[mapped_name] = PRIMITIVE_TECTON_DATA_TYPE_TO_PANDAS_DATA_TYPE[datatype]
        return odfv_result_df.rename(columns=rename_map)[[*rename_map.values()]].astype(datatypes)


@attrs.frozen
class PandasRenameColsNode(ArrowExecNode):
    input_node: Union[ArrowExecNode, SqlExecNode]
    mapping: Optional[Dict[str, str]]
    drop: Optional[List[str]]
    keep_original_columns_from_mapping: bool = False

    def _to_dataframe(self) -> pandas.DataFrame:
        input_df = self.input_node._to_dataframe()
        output_df = input_df
        if self.drop:
            columns_to_drop = [self.column_name_updater(name) for name in self.drop]
            output_df = input_df.drop(columns=columns_to_drop)
        if self.mapping:
            output_df = input_df.rename(self.mapping)
        return output_df

    def to_arrow_reader(
        self, context: ExecutionContext, partition_selector: Optional["PartitionSelector"] = None
    ) -> pyarrow.RecordBatchReader:
        reader = self.input_node.to_arrow_reader(context, partition_selector)

        input_schema = reader.schema
        output_fields = []
        for name in input_schema.names:
            if self.drop and name in self.drop:
                continue

            field = input_schema.field(name)
            if self.mapping and name in self.mapping:
                if self.keep_original_columns_from_mapping:
                    output_fields.append(field)
                output_fields.append(field.with_name(self.mapping[name]))
            else:
                output_fields.append(field)

        output_schema = pyarrow.schema(output_fields)

        def batch_iter():
            while True:
                try:
                    batch = reader.read_next_batch()
                except StopIteration:
                    return

                output_columns = []
                for name, column in zip(batch.column_names, batch.columns):
                    if self.drop and name in self.drop:
                        continue

                    output_columns.append(column)

                yield pyarrow.RecordBatch.from_arrays(output_columns, schema=output_schema)

        return pyarrow.RecordBatchReader.from_batches(output_schema, batch_iter())

    def as_str(self):
        return "ArrowExec node for RenameCols"
