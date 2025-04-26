import inspect
import math
from datetime import datetime
from datetime import timezone
from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import NamedTuple
from typing import Optional
from typing import Union

import pandas

from tecton_core import conf
from tecton_core import specs
from tecton_core.errors import UDF_ERROR
from tecton_core.errors import UDF_TYPE_ERROR
from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonValidationError
from tecton_core.id_helper import IdHelper
from tecton_core.pipeline.feature_pipeline import FeaturePipeline
from tecton_core.pipeline.feature_pipeline import NodeValueType
from tecton_core.pipeline.pipeline_common import CONSTANT_TYPE
from tecton_core.pipeline.pipeline_common import constant_node_to_value
from tecton_core.query.errors import UserCodeError
from tecton_core.realtime_context import REQUEST_TIMESTAMP_FIELD_NAME
from tecton_core.realtime_context import RealtimeContext
from tecton_core.resource_provider_context import ResourceProviderContext
from tecton_core.secret_management import SecretResolver
from tecton_proto.args.pipeline__client_pb2 import JoinInputsNode
from tecton_proto.args.pipeline__client_pb2 import Pipeline
from tecton_proto.args.pipeline__client_pb2 import PipelineNode
from tecton_proto.args.pipeline__client_pb2 import TransformationNode
from tecton_proto.args.transformation__client_pb2 import TransformationMode
from tecton_proto.common import secret__client_pb2 as secret_pb2
from tecton_proto.common.id__client_pb2 import Id as TectonId


NAMESPACE_SEPARATOR = "__"


class RealtimeFeaturePipeline(FeaturePipeline):
    def __init__(
        self,
        name: str,
        pipeline: Pipeline,
        transformations: List[specs.TransformationSpec],
        context_parameter_name: Optional[str] = None,
        events_df_timestamp_field: Optional[str] = None,
        pipeline_inputs: Optional[Dict[str, Union[Dict[str, Any], pandas.DataFrame, RealtimeContext]]] = None,
        secret_resolver: Optional[SecretResolver] = None,
        secret_references: Optional[Mapping[str, secret_pb2.SecretReference]] = None,
        resource_providers: Optional[Mapping[str, specs.ResourceProviderSpec]] = None,
    ) -> None:
        self._pipeline = pipeline
        self._name = name
        self._id_to_transformation = {t.id: t for t in transformations}
        self._events_df_timestamp_field = events_df_timestamp_field

        if self._pipeline.root.HasField("transformation_node"):
            root_transformation = self.get_transformation_by_id(
                self._pipeline.root.transformation_node.transformation_id
            )
            assert root_transformation.transformation_mode in (
                TransformationMode.TRANSFORMATION_MODE_PYTHON,
                TransformationMode.TRANSFORMATION_MODE_PANDAS,
            )
            # In Spark, the UDF cannot reference a proto enum, so instead save mode as a string
            self.mode = (
                "python"
                if root_transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PYTHON
                else "pandas"
            )
        elif self._pipeline.root.HasField("join_inputs_node"):
            self.mode = "no_transformation"
        else:
            msg = f"Unsupported pipeline root {self._pipeline.root}"
            raise ValueError(msg)

        # Access this conf value outside of the UDF to avoid doing it many times and avoiding any worker/driver state issues.
        self._should_check_output_schema = conf.get_bool("TECTON_PYTHON_ODFV_OUTPUT_SCHEMA_CHECK_ENABLED")
        if context_parameter_name and context_parameter_name in pipeline_inputs:
            # There is a validation that context must be provided, if it is in transformation body
            provided_context = pipeline_inputs[context_parameter_name]
            # Resolve Secrets
            if secret_references:
                provided_secrets = provided_context.secrets or {}

                invalid_provided_secrets = sorted(set(provided_secrets.keys()) - set(secret_references.keys()))
                if invalid_provided_secrets:
                    msg = f"Secrets: {invalid_provided_secrets} have been provided but are not declared in feature view definition."
                    raise TectonValidationError(msg)

                secrets_to_resolve = sorted(set(secret_references.keys()) - set(provided_secrets.keys()))

                if secrets_to_resolve is not None and secret_resolver is None:
                    msg = "Missing a secret resolver."
                    raise TectonInternalError(msg)
                resolved_secrets = secret_resolver.resolve_spec_map(
                    {k: v for k, v in secret_references.items() if k in secrets_to_resolve}
                )
                provided_context._secrets = {**provided_secrets, **resolved_secrets}

            # Resolve Resource Providers
            if resource_providers:
                provided_resources = provided_context.resources or {}
                required_resources = resource_providers or {}

                invalid_provided_resources = sorted(set(provided_resources.keys()) - set(required_resources.keys()))
                if invalid_provided_resources:
                    msg = f"Resource Providers: {invalid_provided_resources} have been provided but are not declared in feature view definition."
                    raise TectonValidationError(msg)

                def resolve_resource(resource_provider_spec):
                    if resource_provider_spec.secrets and secret_resolver is None:
                        msg = "Missing a secret resolver."
                        raise TectonInternalError(msg)
                    # TODO: Dedupe secrets resolving across resource providers.
                    signature_args = inspect.signature(resource_provider_spec.function).parameters.keys()
                    function_args = (
                        {
                            "context": ResourceProviderContext(
                                secrets=secret_resolver.resolve_spec_map(resource_provider_spec.secrets or {})
                            )
                        }
                        if "context" in signature_args
                        else {}
                    )
                    try:
                        return resource_provider_spec.function(**function_args)
                    except Exception as exc:
                        msg = f"Invoking Resource Provider: '{resource_provider_spec.name}' failed with exception."
                        raise UserCodeError(msg) from exc

                resources_to_resolve = sorted(set(required_resources.keys()) - set(provided_resources.keys()))
                resolved_resources = {
                    resource_key: resolve_resource(resource_provider_spec)
                    for resource_key, resource_provider_spec in resource_providers.items()
                    if resource_key in resources_to_resolve
                }
                provided_context._resources = {**provided_resources, **resolved_resources}

        self._pipeline_inputs = pipeline_inputs
        self._secret_resolver = secret_resolver
        self._secret_references = secret_references
        self._resource_providers = resource_providers

    def get_transformation_by_id(self, id: TectonId) -> specs.TransformationSpec:
        return self._id_to_transformation[IdHelper.to_string(id)]

    @property
    def is_pandas_mode(self):
        return self.mode == "pandas"

    @property
    def is_python_mode(self):
        return self.mode == "python"

    @property
    def is_no_transformation_mode(self):
        return self.mode == "no_transformation"

    @property
    def transformation_mode(self) -> TransformationMode:
        if self.mode == "python":
            return TransformationMode.TRANSFORMATION_MODE_PYTHON
        elif self.mode == "pandas":
            return TransformationMode.TRANSFORMATION_MODE_PANDAS
        elif self.mode == "no_transformation":
            return TransformationMode.TRANSFORMATION_MODE_NO_TRANSFORMATION
        else:
            msg = f"Unsupported mode in RealtimeFeaturePipeline, unable to determine transformation_mode. Mode: {self.mode}"
            raise ValueError(msg)

    def _context_node_to_value(self, pipeline_node: PipelineNode) -> Optional[Union[pandas.DataFrame, RealtimeContext]]:
        assert self._pipeline_inputs is not None
        return self._pipeline_inputs[pipeline_node.context_node.input_name]

    def _request_data_node_to_value(self, pipeline_node: PipelineNode) -> Union[Dict[str, Any], pandas.DataFrame]:
        assert self._pipeline_inputs is not None
        return self._pipeline_inputs[pipeline_node.request_data_source_node.input_name]

    def _feature_view_node_to_value(self, pipeline_node: PipelineNode) -> Union[Dict[str, Any], pandas.DataFrame]:
        assert self._pipeline_inputs is not None
        return self._pipeline_inputs[pipeline_node.feature_view_node.input_name]

    def _node_to_value(self, pipeline_node: PipelineNode) -> NodeValueType:
        if pipeline_node.HasField("constant_node"):
            return self._constant_node_to_value(pipeline_node.constant_node)
        elif pipeline_node.HasField("feature_view_node"):
            return self._feature_view_node_to_value(pipeline_node)
        elif pipeline_node.HasField("request_data_source_node"):
            return self._request_data_node_to_value(pipeline_node)
        elif pipeline_node.HasField("transformation_node"):
            return self._transformation_node_to_value(pipeline_node.transformation_node)
        elif pipeline_node.HasField("context_node"):
            return self._context_node_to_value(pipeline_node)
        elif pipeline_node.HasField("join_inputs_node"):
            return self._join_inputs_node_to_value(pipeline_node.join_inputs_node)
        elif pipeline_node.HasField("materialization_context_node"):
            msg = f"MaterializationContext is unsupported for {self._fco_name}s."
            raise ValueError(msg)
        else:
            msg = f"This is not yet implemented {pipeline_node}"
            raise NotImplementedError(msg)

    def _constant_node_to_value(self, pipeline_node: PipelineNode) -> CONSTANT_TYPE:
        return constant_node_to_value(pipeline_node)

    @staticmethod
    def _format_values_for_pandas_mode(input_df: pandas.DataFrame) -> pandas.DataFrame:
        for col in input_df.select_dtypes(include=["datetime64"]).columns:
            input_df[col] = pandas.to_datetime(input_df[col], utc=True)
        return input_df

    @staticmethod
    def _format_values_for_python_mode(input_value: Union[NamedTuple, Dict[str, Any]]) -> Dict[str, Any]:
        input_dict = input_value._asdict() if not isinstance(input_value, dict) else input_value
        for key, value in input_dict.items():
            if isinstance(value, datetime):
                input_dict[key] = value.replace(tzinfo=timezone.utc)
            if value is pandas.NaT:
                input_dict[key] = None
            if isinstance(value, float) and math.isnan(value):
                input_dict[key] = None
        return input_dict

    def _join_inputs_node_to_value(self, join_inputs_node: JoinInputsNode) -> Union[Dict[str, Any], pandas.DataFrame]:
        output = {}
        for input_node in join_inputs_node.nodes:
            prefix = _get_namespace_for_rtfv_source_node(input_node)
            node_value = self._node_to_value(input_node)
            if isinstance(node_value, RealtimeContext):
                output[f"{prefix}{REQUEST_TIMESTAMP_FIELD_NAME}"] = node_value.request_timestamp
                continue

            for key, value in node_value.items():
                output[f"{prefix}{key}"] = value
        return output

    def _transformation_node_to_value(
        self, transformation_node: TransformationNode
    ) -> Union[Dict[str, Any], pandas.DataFrame]:
        """Recursively translates inputs to values and then passes them to the transformation."""
        args: List[Union[str, int, float, bool]] = []
        kwargs = {}
        for transformation_input in transformation_node.inputs:
            input_node = transformation_input.node
            node_value = self._node_to_value(input_node)

            if transformation_input.HasField("arg_index"):
                assert len(args) == transformation_input.arg_index
                args.append(node_value)
            elif transformation_input.HasField("arg_name"):
                kwargs[transformation_input.arg_name] = node_value
            else:
                msg = f"Unknown argument type for Input node: {transformation_input}"
                raise KeyError(msg)

        return self._apply_transformation_function(transformation_node, args, kwargs)

    def _apply_transformation_function(
        self, transformation_node: TransformationNode, args: List[Any], kwargs: Dict[str, Any]
    ) -> Union[Dict[str, Any], pandas.DataFrame]:
        """For the given transformation node, returns the corresponding DataFrame transformation.

        If needed, resulted function is wrapped with a function that translates mode-specific input/output types to DataFrames.
        """
        transformation = self.get_transformation_by_id(transformation_node.transformation_id)
        mode = transformation.transformation_mode
        user_function = transformation.user_function

        if (
            mode != TransformationMode.TRANSFORMATION_MODE_PANDAS
            and mode != TransformationMode.TRANSFORMATION_MODE_PYTHON
        ):
            msg = f"Unsupported transformation mode({transformation.transformation_mode}) for {self._fco_name}s."
            raise KeyError(msg)

        try:
            resp = user_function(*args, **kwargs)
            return resp
        except TypeError as e:
            raise UDF_TYPE_ERROR(e)
        except Exception as e:
            raise UDF_ERROR(e, transformation.metadata.name)

    @property
    def _fco_name(self):
        return "Realtime Feature View"

    def run_with_inputs(
        self, inputs: Union[Dict[str, pandas.DataFrame], Dict[str, Any]]
    ) -> Union[CONSTANT_TYPE, Dict[str, Any], pandas.DataFrame, pandas.Series]:
        self._pipeline_inputs = inputs
        return self.get_dataframe()


def _get_namespace_for_rtfv_source_node(node: PipelineNode) -> str:
    if node.HasField("request_data_source_node"):
        return f"{node.request_data_source_node.input_name}{NAMESPACE_SEPARATOR}"
    elif node.HasField("feature_view_node"):
        return f"{node.feature_view_node.feature_reference.namespace}{NAMESPACE_SEPARATOR}"
    elif node.HasField("context_node"):
        return f"{node.context_node.input_name}{NAMESPACE_SEPARATOR}"
    return ""
