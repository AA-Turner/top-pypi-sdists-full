import sys
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Union


if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import pandas

from tecton_core import specs
from tecton_core.id_helper import IdHelper
from tecton_proto.args.pipeline__client_pb2 import PipelineNode
from tecton_proto.common.id__client_pb2 import Id as TectonId


NodeValueType = Union[str, int, float, bool, datetime, None, Dict[str, Any], pandas.DataFrame, pandas.Series]


class FeaturePipeline(Protocol):
    def _node_to_value(self, pipeline_node: PipelineNode) -> NodeValueType:
        """Evaluates a node of this Feature Pipeline to a value"""
        ...

    def _transformation_node_to_value(self, pipeline_node: PipelineNode) -> Union[Dict[str, Any], pandas.DataFrame]:
        """Evaluates the TransformationNode of this Feature Pipeline to a value"""
        ...

    def __init__(self):
        self._id_to_transformation = {}
        self._pipeline = None

    def get_dataframe(self):
        """Run this Feature Pipeline to generate a result DataFrame"""
        return self._node_to_value(self._pipeline.root)

    def to_dataframe(self):
        return self.get_dataframe()

    def get_transformation_by_id(self, id: TectonId) -> specs.TransformationSpec:
        return self._id_to_transformation[IdHelper.to_string(id)]
