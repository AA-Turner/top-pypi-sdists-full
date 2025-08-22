from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Dict, Union, Type
import re
import numpy as np
import numpy.typing as npt

from code_loader.contract.enums import DataStateType, DataStateEnum, LeapDataType, ConfusionMatrixValue, \
    MetricDirection, DatasetMetadataType
from code_loader.contract.visualizer_classes import LeapImage, LeapText, LeapGraph, LeapHorizontalBar, \
    LeapTextMask, LeapImageMask, LeapImageWithBBox, LeapImageWithHeatmap, LeapVideo

custom_latent_space_attribute = "custom_latent_space"


@dataclass
class PreprocessResponse:
    """
    An object that holds the preprocessed data for use within the Tensorleap platform.

    This class is used to encapsulate the results of data preprocessing, including inputs, metadata, labels, and other relevant information.
    It facilitates handling and integration of the processed data within Tensorleap.

    Attributes:
    length (int): The length of the preprocessed data.
    data (Any): The preprocessed data itself. This can be any data type depending on the preprocessing logic.

    Example:
        # Example usage of PreprocessResponse
        preprocessed_data = {
            'images': ['path/to/image1.jpg', 'path/to/image2.jpg'],
            'labels': ['SUV', 'truck'],
            'metadata': [{'id': 1, 'source': 'camera1'}, {'id': 2, 'source': 'camera2'}]
        }
        response = PreprocessResponse(length=len(preprocessed_data), data=preprocessed_data)
    """
    length: Optional[int] = None  # Deprecated. Please use sample_ids instead
    data: Any = None
    sample_ids: Optional[Union[List[str], List[int]]] = None
    state: Optional[DataStateType] = None
    sample_id_type: Optional[Union[Type[str], Type[int]]] = None
    sample_ids_to_instance_mappings: Optional[Dict[str, List[str]]] = None # in use only for element instance
    instance_to_sample_ids_mappings: Optional[Dict[str, str]] = None # in use only for element instance
    instance_ids_to_names: Optional[Dict[str, str]] = None # in use only for element instance

    def __post_init__(self) -> None:
        assert self.sample_ids_to_instance_mappings is None, f"Keep sample_ids_to_instance_mappings None when initializing PreprocessResponse"
        assert self.instance_to_sample_ids_mappings is None, f"Keep instance_to_sample_ids_mappings None when initializing PreprocessResponse"
        assert self.instance_ids_to_names is None, f"Keep instance_ids_to_names None when initializing PreprocessResponse"

        if self.length is not None and self.sample_ids is None:
            self.sample_ids = [i for i in range(self.length)]
            self.sample_id_type = int
        elif self.length is None and self.sample_ids is not None:
            self.length = len(self.sample_ids)
            if self.sample_id_type is None:
                self.sample_id_type = str
            if self.sample_id_type == str:
                for sample_id in self.sample_ids:
                    assert isinstance(sample_id, str), f"Sample id should be of type str. Got: {type(sample_id)}"
        else:
            raise Exception("length is deprecated.")

    def __hash__(self) -> int:
        return id(self)

    def __len__(self) -> int:
        assert self.sample_ids is not None
        return len(self.sample_ids)

@dataclass
class ElementInstance:
    name: str
    mask: npt.NDArray[np.float32]

SectionCallableInterface = Callable[[Union[int, str], PreprocessResponse], npt.NDArray[np.float32]]
InstanceCallableInterface = Callable[[Union[int, str], PreprocessResponse], List[ElementInstance]]

MetadataSectionCallableInterface = Union[
    Callable[[Union[int, str], PreprocessResponse], int],
    Callable[[Union[int, str], PreprocessResponse], Dict[str, int]],
    Callable[[Union[int, str], PreprocessResponse], str],
    Callable[[Union[int, str], PreprocessResponse], Dict[str, str]],
    Callable[[Union[int, str], PreprocessResponse], bool],
    Callable[[Union[int, str], PreprocessResponse], Dict[str, bool]],
    Callable[[Union[int, str], PreprocessResponse], float],
    Callable[[Union[int, str], PreprocessResponse], Dict[str, float]]
]


@dataclass
class PreprocessHandler:
    function: Callable[[], List[PreprocessResponse]]
    data_length: Dict[DataStateType, int] = field(default_factory=dict)


@dataclass
class UnlabeledDataPreprocessHandler:
    function: Callable[[], PreprocessResponse]
    data_length: int = 0


VisualizerCallableInterface = Union[
    Callable[..., LeapImage],
    Callable[..., LeapVideo],
    Callable[..., LeapText],
    Callable[..., LeapGraph],
    Callable[..., LeapHorizontalBar],
    Callable[..., LeapImageMask],
    Callable[..., LeapTextMask],
    Callable[..., LeapImageWithBBox],
    Callable[..., LeapImageWithHeatmap]
]

LeapData = Union[LeapImage, LeapText, LeapGraph, LeapHorizontalBar, LeapImageMask, LeapTextMask, LeapImageWithBBox,
LeapImageWithHeatmap, LeapVideo]

CustomCallableInterface = Callable[..., Any]


@dataclass
class ConfusionMatrixElement:
    label: str
    expected_outcome: ConfusionMatrixValue
    predicted_probability: float
    id: str = ''


ConfusionMatrixCallableInterface = Callable[[Any, Any], List[List[ConfusionMatrixElement]]]

CustomCallableInterfaceMultiArgs = Callable[..., Any]
CustomMultipleReturnCallableInterfaceMultiArgs = Callable[..., Dict[str, Any]]
ConfusionMatrixCallableInterfaceMultiArgs = Callable[..., List[List[ConfusionMatrixElement]]]
MetricCallableReturnType = Union[Any, List[List[ConfusionMatrixElement]]]


@dataclass
class CustomLossHandlerData:
    name: str
    arg_names: List[str]


@dataclass
class CustomLossHandler:
    custom_loss_handler_data: CustomLossHandlerData
    function: CustomCallableInterface


@dataclass
class MetricHandlerData:
    name: str
    arg_names: List[str]
    direction: Union[None, MetricDirection, Dict[str, MetricDirection]] = MetricDirection.Downward
    compute_insights: Optional[Union[bool, Dict[str, bool]]] = None


@dataclass
class MetricHandler:
    metric_handler_data: MetricHandlerData
    function: Union[CustomCallableInterfaceMultiArgs, ConfusionMatrixCallableInterfaceMultiArgs]


@dataclass
class RawInputsForHeatmap:
    raw_input_by_vizualizer_arg_name: Dict[str, npt.NDArray[np.float32]]


@dataclass
class SamplePreprocessResponse:
    sample_ids: Union[npt.NDArray[np.float32], npt.NDArray[np.str_]]
    preprocess_response: PreprocessResponse


@dataclass
class VisualizerHandlerData:
    name: str
    type: LeapDataType
    arg_names: List[str]


@dataclass
class VisualizerHandler:
    visualizer_handler_data: VisualizerHandlerData
    function: VisualizerCallableInterface
    heatmap_function: Optional[Callable[..., npt.NDArray[np.float32]]] = None


@dataclass
class DatasetBaseHandler:
    name: str
    function: SectionCallableInterface


@dataclass
class InputHandler(DatasetBaseHandler):
    shape: Optional[List[int]] = None
    channel_dim: Optional[int] = -1

@dataclass
class ElementInstanceMasksHandler:
    name: str
    function: InstanceCallableInterface

@dataclass
class GroundTruthHandler(DatasetBaseHandler):
    shape: Optional[List[int]] = None


@dataclass
class MetadataHandler:
    name: str
    function: MetadataSectionCallableInterface
    metadata_type: Optional[Union[DatasetMetadataType, Dict[str, DatasetMetadataType]]] = None


@dataclass
class PredictionTypeHandler:
    name: str
    labels: List[str]
    channel_dim: int = -1


@dataclass
class CustomLayerHandler:
    name: str
    layer: Type[Any]
    init_arg_names: List[str]
    call_arg_names: List[str]
    use_custom_latent_space: bool = False


@dataclass
class DatasetIntegrationSetup:
    preprocess: Optional[PreprocessHandler] = None
    unlabeled_data_preprocess: Optional[UnlabeledDataPreprocessHandler] = None
    visualizers: List[VisualizerHandler] = field(default_factory=list)
    inputs: List[InputHandler] = field(default_factory=list)
    instance_masks: List[ElementInstanceMasksHandler] = field(default_factory=list)
    ground_truths: List[GroundTruthHandler] = field(default_factory=list)
    metadata: List[MetadataHandler] = field(default_factory=list)
    prediction_types: List[PredictionTypeHandler] = field(default_factory=list)
    custom_loss_handlers: List[CustomLossHandler] = field(default_factory=list)
    metrics: List[MetricHandler] = field(default_factory=list)
    custom_layers: Dict[str, CustomLayerHandler] = field(default_factory=dict)


@dataclass
class DatasetSample:
    inputs: Dict[str, npt.NDArray[np.float32]]
    gt: Optional[Dict[str, npt.NDArray[np.float32]]]
    metadata: Dict[str, Union[Optional[str], int, bool, Optional[float]]]
    metadata_is_none: Dict[str, bool]
    index: Union[int, str]
    state: DataStateEnum
    instance_masks: Optional[Dict[str, List[ElementInstance]]] = None

