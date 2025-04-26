from typing import Any
from typing import Dict
from typing import List
from typing import Union

import pandas

from tecton_core import specs
from tecton_core.errors import UDF_ERROR
from tecton_core.id_helper import IdHelper
from tecton_core.pipeline import pipeline_common
from tecton_proto.args.pipeline__client_pb2 import Pipeline
from tecton_proto.args.pipeline__client_pb2 import PipelineNode
from tecton_proto.args.pipeline__client_pb2 import TransformationNode
from tecton_proto.args.transformation__client_pb2 import TransformationMode


class _ODFVPipelineBuilder:
    def __init__(
        self,
        name: str,
        pipeline: Pipeline,
        transformations: List[specs.TransformationSpec],
    ) -> None:
        self._pipeline = pipeline
        self._name = name
        self._id_to_transformation = {t.id: t for t in transformations}
        self.mode = (
            "python"
            if self._id_to_transformation[
                IdHelper.to_string(self._pipeline.root.transformation_node.transformation_id)
            ].transformation_mode
            == TransformationMode.TRANSFORMATION_MODE_PYTHON
            else "pandas"
        )

    def _apply_transformation_function(
        self,
        transformation_node: TransformationNode,
        args: List[Union[pipeline_common.CONSTANT_TYPE, Dict[str, Any], pandas.DataFrame, pandas.Series]],
        kwargs: Dict[str, Any],
    ) -> Union[Dict[str, Any], pandas.DataFrame]:
        """For the given transformation node, returns the corresponding DataFrame transformation."""
        transformation = self._id_to_transformation[IdHelper.to_string(transformation_node.transformation_id)]
        user_function = transformation.user_function
        if transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PANDAS:
            try:
                res = user_function(*args, **kwargs)
            except Exception as e:
                raise UDF_ERROR(e, feature_definition_name=transformation.metadata.name) from e
            pipeline_common.check_transformation_type(transformation.name, res, "pandas", self._possible_modes())
            return res
        elif transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PYTHON:
            try:
                res = user_function(*args, **kwargs)
            except Exception as e:
                raise UDF_ERROR(e, feature_definition_name=transformation.metadata.name) from e
            # Only restrict types on the root node of python-mode transforms
            if transformation_node == self._pipeline.root:
                pipeline_common.check_transformation_type(transformation.name, res, "python", self._possible_modes())
            return res
        else:
            msg = f"Unknown transformation mode: {transformation.transformation_mode}"
            raise KeyError(msg)

    def _transformation_node_to_online_dataframe(
        self, transformation_node: TransformationNode
    ) -> Union[Dict[str, Any], pandas.DataFrame]:
        """Recursively translates inputs to values and then passes them to the transformation."""
        args: List[Union[str, int, float, bool, None, Dict[str, Any], pandas.DataFrame, pandas.Series]] = []
        kwargs = {}
        for transformation_input in transformation_node.inputs:
            node_value = self._udf_node_to_value(transformation_input.node)
            if transformation_input.HasField("arg_index"):
                assert len(args) == transformation_input.arg_index
                args.append(node_value)
            elif transformation_input.HasField("arg_name"):
                kwargs[transformation_input.arg_name] = node_value
            else:
                msg = f"Unknown argument type for Input node: {transformation_input}"
                raise KeyError(msg)

        return self._apply_transformation_function(transformation_node, args, kwargs)

    # evaluate a node in the Pipeline
    def _udf_node_to_value(
        self, pipeline_node: PipelineNode
    ) -> Union[pipeline_common.CONSTANT_TYPE, Dict[str, Any], pandas.DataFrame, pandas.Series]:
        if pipeline_node.HasField("constant_node"):
            return pipeline_common.constant_node_to_value(pipeline_node.constant_node)
        elif pipeline_node.HasField("feature_view_node"):
            if pipeline_node.feature_view_node.input_name not in self._passed_in_inputs:
                msg = f"Expected to find input {pipeline_node.feature_view_node.input_name} in provided ODFV pipeline inputs"
                raise ValueError(msg)

            return self._passed_in_inputs[pipeline_node.feature_view_node.input_name]
        elif pipeline_node.HasField("request_data_source_node"):
            if pipeline_node.request_data_source_node.input_name not in self._passed_in_inputs:
                msg = f"Expected to find input {pipeline_node.request_data_source_node.input_name} in provided ODFV pipeline inputs"
                raise ValueError(msg)

            return self._passed_in_inputs[pipeline_node.request_data_source_node.input_name]
        elif pipeline_node.HasField("transformation_node"):
            return self._transformation_node_to_online_dataframe(pipeline_node.transformation_node)
        elif pipeline_node.HasField("materialization_context_node"):
            msg = "MaterializationContext is unsupported for pandas pipelines"
            raise ValueError(msg)
        else:
            msg = "This is not yet implemented"
            raise NotImplementedError(msg)

    def _possible_modes(self):
        # note that pipeline is included since this is meant to be a user hint, and it's
        # theoretically possible a pipeline wound up deeper than expected
        return ["pandas", "pipeline", "python"]

    def execute_with_inputs(
        self, inputs: Union[Dict[str, pandas.DataFrame], Dict[str, Any]]
    ) -> Union[pipeline_common.CONSTANT_TYPE, Dict[str, Any], pandas.DataFrame, pandas.Series]:
        self._passed_in_inputs = inputs
        return self._udf_node_to_value(self._pipeline.root)


def build_odfv_execution_pipeline(
    pipeline: Pipeline,
    transformations: List[specs.TransformationSpec],
    name: str,
) -> _ODFVPipelineBuilder:
    return _ODFVPipelineBuilder(
        name=name,
        pipeline=pipeline,
        transformations=transformations,
    )
