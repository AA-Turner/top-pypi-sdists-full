# mypy: ignore-errors

from abc import abstractmethod

from typing import Dict, List, Union, Type, Optional, Tuple

import numpy as np
import numpy.typing as npt

from code_loader.contract.datasetclasses import DatasetSample, LeapData, \
    PredictionTypeHandler, CustomLayerHandler, VisualizerHandlerData, MetricHandlerData, MetricCallableReturnType, \
    CustomLossHandlerData
from code_loader.contract.enums import DataStateEnum, DataStateType
from code_loader.contract.responsedataclasses import DatasetIntegParseResult, DatasetTestResultPayload, \
    DatasetSetup, ModelSetup


class LeapLoaderBase:
    def __init__(self, code_path: str, code_entry_name: str):
        self.code_entry_name = code_entry_name
        self.code_path = code_path

        self.current_working_sample_ids: Optional[np.array] = None
        self.current_working_state: Optional[DataStateEnum] = None

    def set_current_working_sample_ids(self, sample_ids: np.array):
        if type(sample_ids[0]) is bytes:
            sample_ids = np.array([sample_id.decode('utf-8') for sample_id in sample_ids])
        self.current_working_sample_ids = sample_ids

    def set_current_working_state(self, state: Union[DataStateEnum, DataStateType, str, int, bytes]):
        if type(state) is bytes:
            state = DataStateEnum[state.decode('utf-8')]
        elif type(state) is str:
            state = DataStateEnum[state]
        elif type(state) is int:
            state = DataStateEnum(state)
        elif type(state) is DataStateType:
            state = DataStateEnum[state.name]

        self.current_working_state = state

    @abstractmethod
    def metric_by_name(self) -> Dict[str, MetricHandlerData]:
        pass

    @abstractmethod
    def visualizer_by_name(self) -> Dict[str, VisualizerHandlerData]:
        pass

    @abstractmethod
    def custom_loss_by_name(self) -> Dict[str, CustomLossHandlerData]:
        pass

    @abstractmethod
    def custom_layers(self) -> Dict[str, CustomLayerHandler]:
        pass

    @abstractmethod
    def prediction_type_by_name(self) -> Dict[str, PredictionTypeHandler]:
        pass

    @abstractmethod
    def get_sample(self, state: DataStateEnum, sample_id: Union[int, str], instance_id: int = None) -> DatasetSample:
        pass

    @abstractmethod
    def get_instances_data(self, state: DataStateEnum) -> Tuple[Dict[str, List[str]], Dict[str, str]]:
        pass

    def get_metadata_multiple_samples(self, state: DataStateEnum, sample_ids: Union[List[int], List[str]],
                                      requested_metadata_names: Optional[List[str]] = None
                                      ) -> Tuple[Dict[str, Union[List[str], List[int], List[bool],
    List[float]]], Dict[str, List[bool]]]:
        aggregated_results: Dict[str, List[Union[str, int, bool, float]]] = {}
        aggregated_is_none: Dict[str, List[bool]] = {}
        sample_id_type = self.get_sample_id_type()
        for sample_id in sample_ids:
            sample_id = sample_id_type(sample_id)
            metadata_result, is_none_result = self.get_metadata(state, sample_id, requested_metadata_names)
            for metadata_name, metadata_value in metadata_result.items():
                if metadata_name not in aggregated_results:
                    aggregated_results[metadata_name] = []
                    aggregated_is_none[metadata_name] = []
                aggregated_results[metadata_name].append(metadata_value)
                aggregated_is_none[metadata_name].append(is_none_result[metadata_name])
        return aggregated_results, aggregated_is_none

    @abstractmethod
    def check_dataset(self) -> DatasetIntegParseResult:
        pass

    @abstractmethod
    def run_visualizer(self, visualizer_name: str, sample_ids: np.array, state: DataStateEnum,
                       input_tensors_by_arg_name: Dict[str, npt.NDArray[np.float32]]) -> LeapData:
        pass

    @abstractmethod
    def run_metric(self, metric_name: str, sample_ids: np.array, state: DataStateEnum,
                   input_tensors_by_arg_name: Dict[str, npt.NDArray[np.float32]]) -> MetricCallableReturnType:
        pass

    @abstractmethod
    def run_custom_loss(self, custom_loss_name: str, sample_ids: np.array, state: DataStateEnum,
                        input_tensors_by_arg_name: Dict[str, npt.NDArray[np.float32]]):
        pass

    @abstractmethod
    def get_metadata(
            self, state: DataStateEnum, sample_id: Union[int, str],
            requested_metadata_names: Optional[List[str]] = None
    ) -> Tuple[Dict[str, Union[str, int, bool, float]], Dict[str, bool]]:
        pass

    @abstractmethod
    def run_heatmap_visualizer(self, visualizer_name: str, sample_ids: np.array, state: DataStateEnum,
                               input_tensors_by_arg_name: Dict[str, npt.NDArray[np.float32]]
                               ) -> Optional[npt.NDArray[np.float32]]:
        pass

    @abstractmethod
    def get_dataset_setup_response(self, handlers_test_payloads: List[DatasetTestResultPayload]) -> DatasetSetup:
        pass

    @abstractmethod
    def get_model_setup_response(self) -> ModelSetup:
        pass

    @abstractmethod
    def get_preprocess_sample_ids(
            self, update_unlabeled_preprocess=False) -> Dict[DataStateEnum, Union[List[int], List[str]]]:
        pass

    @abstractmethod
    def get_sample_id_type(self) -> Type:
        pass

    @abstractmethod
    def has_custom_latent_space_decorator(self) -> bool:
        pass

    @abstractmethod
    def get_heatmap_visualizer_raw_vis_input_arg_name(self, visualizer_name: str) -> Optional[str]:
        pass

    def is_custom_latent_space(self) -> bool:
        if not self.code_entry_name or not self.code_path:
            return False
        custom_layers = self.custom_layers()
        return any(layer.use_custom_latent_space for layer in custom_layers.values())
