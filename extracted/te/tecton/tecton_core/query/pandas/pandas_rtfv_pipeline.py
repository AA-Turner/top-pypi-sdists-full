import inspect
from dataclasses import dataclass
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Union

import pandas
import pyarrow

from tecton_core import errors
from tecton_core import feature_set_config
from tecton_core import specs
from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonValidationError
from tecton_core.fco_container import FcoContainer
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.pipeline.feature_pipeline import NodeValueType
from tecton_core.pipeline.rtfv_pipeline import RealtimeFeaturePipeline
from tecton_core.query.errors import UserCodeError
from tecton_core.realtime_context import REQUEST_TIMESTAMP_FIELD_NAME
from tecton_core.realtime_context import RealtimeContext
from tecton_core.resource_provider_context import ResourceProviderContext
from tecton_core.schema import Schema
from tecton_core.schema_validation import CastError
from tecton_core.schema_validation import cast
from tecton_core.secret_management import SecretResolver
from tecton_proto.args.pipeline__client_pb2 import Pipeline
from tecton_proto.args.pipeline__client_pb2 import PipelineNode
from tecton_proto.args.pipeline__client_pb2 import TransformationNode
from tecton_proto.common import secret__client_pb2 as secret_pb2
from tecton_proto.common.schema__client_pb2 import Schema as SchemaProto


RESOURCE_CONTEXT_PARAM_NAME = "context"


class PandasRealtimeFeaturePipeline(RealtimeFeaturePipeline):
    def __init__(
        self,
        name: str,
        pipeline: Pipeline,
        transformations: List[specs.TransformationSpec],
        fco_container: FcoContainer,
        id: str,
        # Input dataframe containing the necessary inputs to the Realtime Feature Pipeline
        data_df: Union[pandas.DataFrame, pyarrow.RecordBatch],
        # Only used by Tecton on Snowflake to uppercase all column names. Should be deprecated
        # with it.
        column_name_updater: Callable,
        events_df_timestamp_field: Optional[str] = None,
        pipeline_inputs: Optional[Dict[str, Union[Dict[str, Any], pandas.DataFrame, RealtimeContext]]] = None,
        secret_resolver: Optional[SecretResolver] = None,
        secret_references: Optional[Mapping[str, secret_pb2.SecretReference]] = None,
        resource_providers: Optional[Mapping[str, specs.ResourceProviderSpec]] = None,
    ) -> None:
        self._data_df = data_df
        self._fco_container = fco_container
        self._fv_id = id
        self._column_name_updater = column_name_updater
        self._context_param_name = None
        self._num_rows = (
            self._data_df.num_rows if isinstance(self._data_df, pyarrow.RecordBatch) else len(self._data_df)
        )

        # For Python Mode we go through each row of inputs in _data_df and run the pipeline for
        # each of them.
        self._current_row_index = 0
        # Cache so we don't run the Spine -> Pandas Input DF logic for every row
        self._input_name_to_df = {}

        # In python, the context is built for every single row. We only resolve secrets and run resource function body once and rest of rows reuse those secrets and resources
        self._resolved_secrets = {}
        self._resources = {}

        super().__init__(
            name=name,
            pipeline=pipeline,
            transformations=transformations,
            events_df_timestamp_field=events_df_timestamp_field,
            pipeline_inputs=pipeline_inputs,
            secret_resolver=secret_resolver,
            secret_references=secret_references,
            resource_providers=resource_providers,
        )

    @classmethod
    def from_feature_definition(
        cls,
        fdw: FeatureDefinitionWrapper,
        data_df: Union[pandas.DataFrame, pyarrow.RecordBatch],
        column_name_updater: Callable,
        events_df_timestamp_field: Optional[str] = None,
        secret_resolver: Optional[SecretResolver] = None,
    ) -> "PandasRealtimeFeaturePipeline":
        return cls(
            fdw.name,
            fdw.pipeline,
            fdw.transformations,
            fdw.fco_container,
            fdw.id,
            data_df,
            column_name_updater,
            events_df_timestamp_field,
            secret_resolver=secret_resolver,
            secret_references=fdw.fv_spec.secrets,
            resource_providers=fdw.resource_providers,
        )

    def get_dataframe(self):
        if not (self.is_pandas_mode or self.is_python_mode):
            msg = "Realtime Feature View pipelines can only run in Pandas or Python Mode."
            raise Exception(msg)

        return self._node_to_value(self._pipeline.root)

    def _node_to_value(self, pipeline_node: PipelineNode) -> NodeValueType:
        value = super()._node_to_value(pipeline_node)

        if self.is_pandas_mode and isinstance(value, pandas.DataFrame):
            value = self._format_values_for_pandas_mode(value)

        return value

    def _request_data_node_to_value(self, pipeline_node: PipelineNode) -> Union[Dict[str, Any], pandas.DataFrame]:
        input_name = pipeline_node.request_data_source_node.input_name

        # Use cache for Python Mode
        if input_name in self._input_name_to_df:
            return self._input_name_to_df[input_name]

        request_context_schema = pipeline_node.request_data_source_node.request_context.tecton_schema

        if isinstance(self._data_df, pandas.DataFrame):
            # TODO(Oleksii): remove this path once Snowflake & Athena are deprecated
            input_df = self._get_request_context_pandas_df(request_context_schema, input_name)
        elif isinstance(self._data_df, pyarrow.RecordBatch):
            try:
                input_df = cast(self._data_df, Schema(request_context_schema)).to_pandas()
            except CastError as exc:
                msg = f"{self._fco_name} {self._name} has a dependency on the Request Data Source named '{input_name}', but it didn't pass schema validation: "
                raise CastError(msg + str(exc)) from None
        else:
            msg = f"Unexpected input dataframe type: {type(self._data_df)}"
            raise RuntimeError(msg)

        self._input_name_to_df[input_name] = input_df
        return input_df

    def _feature_view_node_to_value(self, pipeline_node: PipelineNode) -> Union[Dict[str, Any], pandas.DataFrame]:
        input_name = pipeline_node.feature_view_node.input_name

        # Use cache for Python Mode
        if input_name in self._input_name_to_df:
            return self._input_name_to_df[input_name]

        fv_features = feature_set_config.find_dependent_feature_set_items(
            self._fco_container, pipeline_node, {}, self._fv_id
        )[0]
        # Generate dependent column mappings since dependent FV have
        # internal column names with _udf_internal
        select_columns_and_rename_map = {}
        for f in fv_features.features:
            column_name = self._column_name_updater(f"{fv_features.namespace}__{f}")
            mapped_name = self._column_name_updater(f)
            select_columns_and_rename_map[column_name] = mapped_name
        if isinstance(self._data_df, pandas.DataFrame):
            # TODO(Oleksii): remove this path once Snowflake & Athena are deprecated
            feature_view_input_df = self._rename_pandas_columns(select_columns_and_rename_map, input_name)
        elif isinstance(self._data_df, pyarrow.RecordBatch):
            columns = []
            for f in select_columns_and_rename_map:
                try:
                    columns.append(self._data_df.column(f))
                except KeyError:
                    msg = f"{self._fco_name} {self._name} has a dependency on the Feature View '{input_name}'. Feature {f} of this Feature View is not found in the retrieved historical data. Available columns: {list(self._data_df.column_names)}"
                    raise TectonValidationError(msg)

            feature_view_input_df = pyarrow.RecordBatch.from_arrays(
                columns, names=list(select_columns_and_rename_map.values())
            ).to_pandas()
        else:
            msg = f"Unexpected input dataframe type: {type(self._data_df)}"
            raise RuntimeError(msg)

        self._input_name_to_df[input_name] = feature_view_input_df
        return feature_view_input_df

    def _context_node_to_value(self, pipeline_node: PipelineNode) -> Optional[RealtimeContext]:
        if not isinstance(self._data_df, pyarrow.RecordBatch):
            msg = "Realtime Context is only supported on Rift and Spark Feature Views."
            raise Exception(msg)

        data_df = self._data_df.to_pandas()
        input_name = pipeline_node.context_node.input_name

        if self._events_df_timestamp_field is None or self._events_df_timestamp_field not in data_df:
            timestamp_field = self._events_df_timestamp_field if self._events_df_timestamp_field is not None else ""
            msg = f"Unable to extract timestamp field '{timestamp_field}' from events dataframe."
            raise Exception(msg)

        context_df = data_df[[self._events_df_timestamp_field]].rename(
            columns={self._events_df_timestamp_field: REQUEST_TIMESTAMP_FIELD_NAME}
        )

        self._input_name_to_df[input_name] = context_df

        # Cache resolved secrets for rest of rows in python mode.
        self._resolved_secrets = self._get_secrets()
        self._resources = self._get_resources()

        return RealtimeContext(
            _row_level_data=context_df,
            _mode=self.transformation_mode,
            secrets=self._resolved_secrets,
            resources=self._resources,
        )

    def _apply_transformation_function(
        self, transformation_node: TransformationNode, args: List[Any], kwargs: Dict[str, Any]
    ) -> Union[Dict[str, Any], pandas.DataFrame]:
        """For the given transformation node, returns the corresponding DataFrame transformation.

        If needed, resulted function is wrapped with a function that translates mode-specific input/output types to DataFrames.
        """
        transformation = self.get_transformation_by_id(transformation_node.transformation_id)
        mode = transformation.transformation_mode
        user_function = transformation.user_function

        if not self.is_pandas_mode and not self.is_python_mode:
            msg = f"Unsupported transformation mode({transformation.transformation_mode}) for {self._fco_name}s."
            raise KeyError(msg)

        # RTFV w/o sources
        iterable_args_kwargs = []
        result = []

        if not args and not kwargs:
            resp = user_function()
            result = [resp] * len(self._data_df)
        elif self.is_pandas_mode:
            iterable_args_kwargs = [(args, kwargs)]
        else:
            iterable_args_kwargs = PythonArgsIterator(args, kwargs)

        for args, kwargs in iterable_args_kwargs:
            try:
                resp = user_function(*args, **kwargs)
                result.append(resp)
            except TypeError as e:
                raise errors.UDF_TYPE_ERROR(e)
            except Exception as e:
                raise errors.UDF_ERROR(e, transformation.metadata.name)

        if self.is_pandas_mode:
            return result[0]

        return pandas.DataFrame.from_dict(result)

    def _get_secrets(self) -> Dict[str, Any]:
        if not self._secret_references:
            return {}
        if not self._secret_resolver:
            msg = "Can not find secret resolver."
            raise errors.TectonInternalError(msg)
        return self._secret_resolver.resolve_spec_map(self._secret_references)

    def _get_resources(self) -> Dict[str, Any]:
        resources = {}
        if self._resource_providers:
            for key, resource_provider_spec in self._resource_providers.items():
                signature_args = inspect.signature(resource_provider_spec.function).parameters.keys()
                function_args = (
                    {RESOURCE_CONTEXT_PARAM_NAME: ResourceProviderContext()}
                    if RESOURCE_CONTEXT_PARAM_NAME in signature_args
                    else {}
                )
                if resource_provider_spec.secrets:
                    if not self._secret_resolver:
                        msg = "No secret resolver was provided. For Local Development, please set secrets to string literals."
                        raise TectonInternalError(msg)
                    # TODO: Dedupe secrets resolving across resource providers.
                    function_args[RESOURCE_CONTEXT_PARAM_NAME] = ResourceProviderContext(
                        secrets=self._secret_resolver.resolve_spec_map(resource_provider_spec.secrets)
                    )
                try:
                    resources[key] = resource_provider_spec.function(**function_args)
                except Exception as exc:
                    msg = f"Invoking Resource Provider: '{resource_provider_spec.name}' failed with exception."
                    raise UserCodeError(msg) from exc
        return resources

    # TODO(Oleksii): remove this once Snowflake & Athena are deprecated
    def _rename_pandas_columns(
        self, select_columns_and_rename_map: Dict[str, str], input_name: str
    ) -> pandas.DataFrame:
        for f in select_columns_and_rename_map.keys():
            if f not in self._data_df.columns:
                msg = f"{self._fco_name} {self._name} has a dependency on the Feature View '{input_name}'. Feature {f} of this Feature View is not found in the retrieved historical data. Available columns: {list(self._data_df.columns)}"
                raise TectonValidationError(msg)

        # Select all of the features of the input FV from data_df
        return self._data_df.rename(columns=select_columns_and_rename_map)[[*select_columns_and_rename_map.values()]]

    # TODO(Oleksii): remove this once Snowflake & Athena are deprecated
    def _get_request_context_pandas_df(self, request_context_schema: SchemaProto, input_name: str) -> pandas.DataFrame:
        request_context_fields = [self._column_name_updater(c.name) for c in request_context_schema.columns]
        for f in request_context_fields:
            if f not in self._data_df.columns:
                msg = f"{self._fco_name} {self._name} has a dependency on the Request Data Source named '{input_name}'. Field {f} of this Request Data Source is not found in the spine. Available columns: {list(self._data_df.columns)}"
                raise TectonValidationError(msg)

        return self._data_df[request_context_fields]


@dataclass
class PythonArgument:
    """
    Wrapper class for arguments to be used in PythonArgsIterator

    is_iterator: bool - indicates if the argument is an iterator
    value: Any - the argument itself
    name: Optional[str] - the name of the argument if named
    """

    is_iterator: bool
    value: Any
    name: Optional[str] = None


class PythonArgsIterator:
    """
    Iterator over RTFV arguments (named and positional) for Python mode
    Synchronously iterates over all rows from pandas.Dataframes present in args or kwargs
    """

    def __init__(self, args: List[Any], kwargs: Dict[str, Any]) -> None:
        self._args: List[PythonArgument] = []

        for arg in args:
            if isinstance(arg, pandas.DataFrame):
                self._args.append(
                    PythonArgument(
                        True, map(RealtimeFeaturePipeline._format_values_for_python_mode, arg.itertuples(index=False))
                    )
                )
            elif isinstance(arg, RealtimeContext):
                self._args.append(PythonArgument(True, iter(arg)))
            else:
                self._args.append(PythonArgument(False, arg))

        for key, value in kwargs.items():
            if isinstance(value, pandas.DataFrame):
                self._args.append(
                    PythonArgument(
                        True,
                        map(RealtimeFeaturePipeline._format_values_for_python_mode, value.itertuples(index=False)),
                        key,
                    )
                )
            elif isinstance(value, RealtimeContext):
                self._args.append(PythonArgument(True, iter(value), key))
            else:
                self._args.append(PythonArgument(False, value, key))

    def __iter__(self):
        return self

    def __next__(self):
        try:
            args = []
            kwargs = {}

            for arg in self._args:
                value = next(arg.value) if arg.is_iterator else arg.value
                if arg.name is None:
                    args.append(value)
                else:
                    kwargs[arg.name] = value

            return args, kwargs

        except StopIteration:
            raise StopIteration
