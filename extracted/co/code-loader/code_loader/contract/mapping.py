# mypy: ignore-errors


from enum import Enum

from typing import Optional, Dict, Any, List
from dataclasses import dataclass



class NodeMappingType(Enum):
    Visualizer = 'Visualizer'
    Metric = 'Metric'
    GroundTruth = 'GroundTruth'
    Input = 'Input'
    Layer = 'Layer'
    Loss = 'Loss'
    CustomLoss = 'CustomLoss'
    Optimizer = 'Optimizer'
    Prediction0 = 'Prediction0'
    Prediction1 = 'Prediction1'
    Prediction2 = 'Prediction2'
    Prediction3 = 'Prediction3'
    Prediction4 = 'Prediction4'
    Prediction5 = 'Prediction5'
    Prediction6 = 'Prediction6'
    Prediction7 = 'Prediction7'
    Prediction8 = 'Prediction8'
    Prediction9 = 'Prediction9'
    Input0 = 'Input0'
    Input1 = 'Input1'
    Input2 = 'Input2'
    Input3 = 'Input3'
    Input4 = 'Input4'
    Input5 = 'Input5'
    Input6 = 'Input6'
    Input7 = 'Input7'
    Input8 = 'Input8'
    Input9 = 'Input9'
    PredictionLabels = 'PredictionLabels'


@dataclass
class NodeMapping:
    name: str
    type: NodeMappingType
    user_unique_name: Optional[str] = None
    sub_type: Optional[str] = None
    arg_names: Optional[List[str]] = None



@dataclass
class NodeConnection:
    node: NodeMapping
    node_inputs: Optional[Dict[str, NodeMapping]]


def leap_output(idx):
    def dummy():
        return None

    node_mapping_type = NodeMappingType(f'Prediction{str(idx)}')
    dummy.node_mapping = NodeMapping('', node_mapping_type)

    return dummy

