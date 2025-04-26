import re
from typing import List

import attrs

from tecton_core import feature_set_config
from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.realtime_context import REQUEST_TIMESTAMP_FIELD_NAME
from tecton_core.schema import Schema
from tecton_proto.args import pipeline__client_pb2 as pipeline_pb2
from tecton_proto.args.pipeline__client_pb2 import PipelineNode


_COLUMN_REFERENCE_NAMESPACE_SEPARATOR = re.compile(r"__|\.")


@attrs.define
class ColumnReferenceResolver:
    """
    A class to resolve column reference strings in features to their internal column name strings in the query tree.
    """

    events_df_timestamp_field: str
    input_node_column_names: List[str]

    def _input_node_has_column(self, column_name: str) -> bool:
        return column_name in self.input_node_column_names

    @staticmethod
    def _get_feature_view_node_internal_column_name(
        source_fv_pipeline_node: PipelineNode, feature_name: str, fdw: FeatureDefinitionWrapper
    ) -> str:
        # the source fv is in the fco_container, and it has no dependents, so there will only be 1 item in the result
        dependent_fv_dac = feature_set_config.find_dependent_feature_set_items(
            fdw.fco_container, source_fv_pipeline_node, {}, fdw.id
        )[0]
        if feature_name not in dependent_fv_dac.features:
            msg = f"Feature {feature_name} not found in source feature view {dependent_fv_dac.name}."
            raise TectonInternalError(msg)
        return f"{dependent_fv_dac.namespace}{dependent_fv_dac.feature_definition.namespace_separator}{feature_name}"

    def _get_realtime_context_internal_column_name(self, feature_name: str) -> str:
        if feature_name == REQUEST_TIMESTAMP_FIELD_NAME:
            if not self._input_node_has_column(self.events_df_timestamp_field):
                msg = f"Timestamp field {self.events_df_timestamp_field} not found in input events df. Missing for use in realtime context request_timestamp."
                raise TectonValidationError(msg)
            return self.events_df_timestamp_field
        msg = f"Context attribute {feature_name} not available in realtime context."
        raise TectonInternalError(msg)

    @staticmethod
    def _get_request_data_source_internal_column_name(pipeline_node: PipelineNode, feature_name: str) -> str:
        request_context_schema = pipeline_node.request_data_source_node.request_context.tecton_schema
        schema = Schema(request_context_schema)
        if feature_name in schema.column_names():
            return feature_name
        msg = f"Feature name {feature_name} not found in request data source {pipeline_node.request_data_source_node.input_name}"
        raise TectonValidationError(msg)

    @staticmethod
    def _get_supported_pipeline_node_name(pipeline_node: PipelineNode) -> str:
        if pipeline_node.HasField("feature_view_node"):
            return pipeline_node.feature_view_node.input_name
        elif pipeline_node.HasField("context_node"):
            return pipeline_node.context_node.input_name
        elif pipeline_node.HasField("request_data_source_node"):
            return pipeline_node.request_data_source_node.input_name
        else:
            node_type = pipeline_node.WhichOneof("node_type")
            msg = f"Pipeline node type {node_type} not supported."
            raise TectonInternalError(msg)

    @staticmethod
    def _split_column_reference(column_reference: str) -> List[str]:
        splits = _COLUMN_REFERENCE_NAMESPACE_SEPARATOR.split(column_reference)
        if len(splits) != 2:
            msg = f"Expected column_reference to contain exactly one '__' or '.', but got '{column_reference}' instead."
            raise ValueError(msg)
        return splits

    def get_internal_column_name(self, column_reference: str, fdw: FeatureDefinitionWrapper) -> str:
        """Resolves a column reference string in an attribute or calculation to its corresponding internal column name.

        Attribute and Calculation features can reference columns from their sources like `my_batch_fv__transaction_amt`,
        or `my_request_source__client_app_version`. In the intermediate nodes of the query tree, these data
        columns have internal names like `_udf_internal_my_batch_fv_ab353c4597780f6c7ff33f1a3655a4ca__transaction_amt`.

        This method takes an input column reference, validates it by confirming the column reference refers to a column
        in the feature's sources, and then resolves the column reference string to the internal column name,
        so it can be used in the composed duck db or spark sql query.

        Examples:
             - `my_batch_fv__transaction_amt` -> `_udf_internal_my_batch_fv_ab353c4597780f6c7ff33f1a3655a4ca__transaction_amt`
             - `context__request_timestamp` -> `TIMESTAMP` (timestamp_key in the events df)
        """
        source_name, feature_name = self._split_column_reference(column_reference)
        pipeline_node = fdw.pipeline.root
        if not pipeline_node.HasField("join_inputs_node"):
            msg = "Pipeline root node is not join_inputs_node type. Cannot resolve internal columns from other node types."
            raise TectonInternalError(msg)
        join_inputs_node = pipeline_node.join_inputs_node

        source_pipeline_nodes = [
            input_node
            for input_node in join_inputs_node.nodes
            if self._get_supported_pipeline_node_name(input_node) == source_name
        ]
        if len(source_pipeline_nodes) != 1:
            msg = f"Found {len(source_pipeline_nodes)} input pipeline nodes for the source {source_name} for column reference {column_reference}. Source must match 1 input pipeline node."
            raise TectonInternalError(msg)
        source_pipeline_node = source_pipeline_nodes[0]

        internal_column_name = None
        if source_pipeline_node.HasField("feature_view_node"):
            internal_column_name = self._get_feature_view_node_internal_column_name(
                source_pipeline_node, feature_name, fdw
            )
        elif (
            source_pipeline_node.HasField("context_node")
            and source_pipeline_node.context_node.context_type == pipeline_pb2.CONTEXT_TYPE_REALTIME
        ):
            internal_column_name = self._get_realtime_context_internal_column_name(feature_name)
        elif source_pipeline_node.HasField("request_data_source_node"):
            internal_column_name = self._get_request_data_source_internal_column_name(
                source_pipeline_node, feature_name
            )
        else:
            node_type = source_pipeline_node.WhichOneof("node_type")
            msg = f"Failed to extract Features. Pipeline node type {node_type} not supported."
            raise TectonInternalError(msg)

        # check if the internal_column is in the input columns
        # Could extend this to check membership in input query or input dataframe for spark and sql, respectively
        if not internal_column_name or not self._input_node_has_column(internal_column_name):
            msg = f"Internal column {internal_column_name} for column_reference {column_reference} not found in input to Feature Extraction."
            raise TectonInternalError(msg)

        return internal_column_name
