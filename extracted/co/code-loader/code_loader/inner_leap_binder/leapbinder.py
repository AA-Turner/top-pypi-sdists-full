import inspect
from typing import Callable, List, Optional, Dict, Any, Type, Union

import numpy as np
import numpy.typing as npt

from code_loader.contract.datasetclasses import SectionCallableInterface, InputHandler, \
    GroundTruthHandler, MetadataHandler, DatasetIntegrationSetup, VisualizerHandler, PreprocessResponse, \
    PreprocessHandler, VisualizerCallableInterface, CustomLossHandler, CustomCallableInterface, PredictionTypeHandler, \
    MetadataSectionCallableInterface, UnlabeledDataPreprocessHandler, CustomLayerHandler, MetricHandler, \
    CustomCallableInterfaceMultiArgs, ConfusionMatrixCallableInterfaceMultiArgs, LeapData, \
    CustomMultipleReturnCallableInterfaceMultiArgs, DatasetBaseHandler, custom_latent_space_attribute, \
    RawInputsForHeatmap, VisualizerHandlerData, MetricHandlerData, CustomLossHandlerData, SamplePreprocessResponse, \
    ElementInstanceMasksHandler, InstanceCallableInterface
from code_loader.contract.enums import LeapDataType, DataStateEnum, DataStateType, MetricDirection, DatasetMetadataType
from code_loader.contract.mapping import NodeConnection, NodeMapping, NodeMappingType
from code_loader.contract.responsedataclasses import DatasetTestResultPayload
from code_loader.contract.visualizer_classes import map_leap_data_type_to_visualizer_class
from code_loader.default_losses import loss_name_to_function
from code_loader.default_metrics import metrics_names_to_functions_and_direction
from code_loader.utils import to_numpy_return_wrapper, get_shape, to_numpy_return_masks_wrapper
from code_loader.visualizers.default_visualizers import DefaultVisualizer, \
    default_graph_visualizer, \
    default_image_visualizer, default_horizontal_bar_visualizer, default_word_visualizer, \
    default_image_mask_visualizer, default_text_mask_visualizer, default_raw_data_visualizer, default_video_visualizer


mapping_runtime_mode_env_var_mame = '__MAPPING_RUNTIME_MODE__'


class LeapBinder:
    """
    Interface to the Tensorleap platform. Provides methods to set up preprocessing,
    visualization, custom loss functions, metrics, and other essential components for integrating the dataset and model
    with Tensorleap.

    Attributes:
    setup_container (DatasetIntegrationSetup): Container to hold setup configurations.
    cache_container (Dict[str, Any]): Cache container to store intermediate data.
    """

    def __init__(self) -> None:
        self.setup_container = DatasetIntegrationSetup()
        self.cache_container: Dict[str, Any] = {"word_to_index": {}}
        self._visualizer_names: List[str] = list()
        self._encoder_names: List[str] = list()
        self._extend_with_default_visualizers()
        self._extend_with_default_metrics()
        self._extend_with_default_losses()

        self.mapping_connections: List[NodeConnection] = []
        self.integration_test_func: Optional[Callable[[str, PreprocessResponse], Any]] = None

        self.batch_size_to_validate: Optional[int] = None

    def _extend_with_default_visualizers(self) -> None:
        self.set_visualizer(function=default_image_visualizer, name=DefaultVisualizer.Image.value,
                            visualizer_type=LeapDataType.Image)
        self.set_visualizer(function=default_video_visualizer, name=DefaultVisualizer.Video.value,
                            visualizer_type=LeapDataType.Video)
        self.set_visualizer(function=default_graph_visualizer, name=DefaultVisualizer.Graph.value,
                            visualizer_type=LeapDataType.Graph)
        self.set_visualizer(function=default_raw_data_visualizer, name=DefaultVisualizer.RawData.value,
                            visualizer_type=LeapDataType.Text)
        self.set_visualizer(function=default_horizontal_bar_visualizer, name=DefaultVisualizer.HorizontalBar.value,
                            visualizer_type=LeapDataType.HorizontalBar)
        self.set_visualizer(function=default_word_visualizer, name=DefaultVisualizer.Text.value,
                            visualizer_type=LeapDataType.Text)
        self.set_visualizer(function=default_image_mask_visualizer, name=DefaultVisualizer.ImageMask.value,
                            visualizer_type=LeapDataType.ImageMask)
        self.set_visualizer(function=default_text_mask_visualizer, name=DefaultVisualizer.TextMask.value,
                            visualizer_type=LeapDataType.TextMask)

    def _extend_with_default_losses(self) -> None:
        for loss_name, func in loss_name_to_function.items():
            self.add_custom_loss(func, loss_name)

    def _extend_with_default_metrics(self) -> None:
        for metric_name, (func, direction) in metrics_names_to_functions_and_direction.items():
            self.add_custom_metric(func, metric_name, direction)

    def set_visualizer(self, function: VisualizerCallableInterface,
                       name: str,
                       visualizer_type: LeapDataType,
                       heatmap_visualizer: Optional[Callable[..., npt.NDArray[np.float32]]] = None) -> None:
        """
        Set a visualizer for a specific data type.

        Args:
        function (VisualizerCallableInterface): The visualizer function to be used for visualizing the data.
        name (str): The name of the visualizer.
        visualizer_type (LeapDataType): The type of data the visualizer handles (e.g., LeapDataType.Image, LeapDataType.Graph, LeapDataType.Text).
        heatmap_visualizer (Optional[Callable[..., npt.NDArray[np.float32]]]): An optional heatmap visualizer function.
        This is used when a heatmap must be reshaped to overlay correctly on the transformed data within the visualizer
        function i.e., if the visualizer changes the shape or scale of the input data, the heatmap visualizer
        adjusts the heatmap accordingly to ensure it aligns properly with the visualized data.

        Example:
        def image_resize_visualizer(data: np.ndarray) -> LeapImage:
            # Resize the image to a fixed size
            resized_image = resize_image(data, (224, 224))
            return LeapImage(data=resized_image)

        def image_resize_heatmap_visualizer(heatmap: RawInputsForHeatmap) -> np.ndarray:
            # Resize the heatmap to match the resized image
            resized_heatmap = resize_heatmap(heatmap, (224, 224))
            return resized_heatmap

        leap_binder.set_visualizer(
            function=image_resize_visualizer,
            name='image_resize_visualizer',
            visualizer_type=LeapDataType.Image,
            heatmap_visualizer=image_resize_heatmap_visualizer
        )
        """

        regular_arg_names = inspect.getfullargspec(function)[0]
        preprocess_response_arg_name = None
        for arg_name, arg_type in inspect.getfullargspec(function).annotations.items():
            if arg_type == SamplePreprocessResponse:
                if preprocess_response_arg_name is not None:
                    raise Exception("only one argument can be of type SamplePreprocessResponse")
                preprocess_response_arg_name = arg_name
                regular_arg_names.remove(arg_name)

        arg_names = regular_arg_names
        if heatmap_visualizer:
            visualizer_arg_names_set = set(arg_names)
            heatmap_visualizer_inspection = inspect.getfullargspec(heatmap_visualizer)
            heatmap_arg_names_set = set(heatmap_visualizer_inspection[0])
            if visualizer_arg_names_set != heatmap_arg_names_set:
                arg_names_difference = set(inspect.getfullargspec(heatmap_visualizer)[0]).difference(set(arg_names))
                if len(arg_names_difference) != 1 or \
                        heatmap_visualizer_inspection.annotations[list(arg_names_difference)[0]] != RawInputsForHeatmap:
                    raise Exception(
                        f'The argument names of the heatmap visualizer callback must match the visualizer callback '
                        f'{str(arg_names)}')

        if visualizer_type.value not in map_leap_data_type_to_visualizer_class:
            raise Exception(
                f'The visualizer_type is invalid. current visualizer_type: {visualizer_type}, '  # type: ignore[attr-defined]
                f'should be one of : {", ".join([arg.__name__ for arg in LeapData.__args__])}')

        func_annotations = function.__annotations__
        if "return" not in func_annotations:
            print(f"Tensorleap Warning: no return type hint for function {function.__name__}. Please configure the "
                  f"right return type. for more info on python type"
                  f" hints: "
                  f"https://docs.python.org/3/library/typing.html")
        else:
            return_type = func_annotations["return"]
            if return_type not in LeapData.__args__:  # type: ignore[attr-defined]
                raise Exception(
                    f'The return type of function {function.__name__} is invalid. current return type: {return_type}, '  # type: ignore[attr-defined]
                    f'should be one of : {", ".join([arg.__name__ for arg in LeapData.__args__])}')

            expected_return_type = map_leap_data_type_to_visualizer_class[visualizer_type.value]
            if not issubclass(return_type, expected_return_type):
                raise Exception(
                    f'The return type of function {function.__name__} is invalid. current return type: {return_type}, '
                    f'should be {expected_return_type}')

        self.setup_container.visualizers.append(
            VisualizerHandler(VisualizerHandlerData(name, visualizer_type, arg_names), function, heatmap_visualizer))
        self._visualizer_names.append(name)

    def set_preprocess(self, function: Callable[[], List[PreprocessResponse]]) -> None:
        """
        Set the preprocessing function for the dataset. That is the function that returns a list of PreprocessResponse objects for use within the Tensorleap platform.

        Args:
        function (Callable[[], List[PreprocessResponse]]): The preprocessing function.

        Example:
            def preprocess_func() -> List[PreprocessResponse]:
                # Preprocess the dataset
                train_data = {
                'subset': 'train',
                'images': ['path/to/train/image1.jpg', 'path/to/train/image2.jpg'],
                'labels': ['SUV', 'truck'],
                'metadata': [{'id': 1, 'source': 'camera1'}, {'id': 2, 'source': 'camera2'}]}

                val_data = {
                'subset': 'val',
                'images': ['path/to/val/image1.jpg', 'path/to/va;/image2.jpg'],
                'labels': ['truck', 'truck'],
                'metadata': [{'id': 1, 'source': 'camera1'}, {'id': 2, 'source': 'camera2'}]}

                return [PreprocessResponse(length=len(train_data['images']), data=train_data),
                        PreprocessResponse(length=len(val_data['images']), data=val_data)]

            leap_binder.set_preprocess(preprocess_func)
        """
        self.setup_container.preprocess = PreprocessHandler(function)

    def set_unlabeled_data_preprocess(self, function: Callable[[], PreprocessResponse]) -> None:
        """
        Set the preprocessing function for unlabeled dataset. This function returns a PreprocessResponse object for use within the Tensorleap platform for sample data that does not contain labels.

        Args:
        function (Callable[[], PreprocessResponse]): The preprocessing function for unlabeled data.

        Example:
            def unlabeled_preprocess_func() -> List[PreprocessResponse]:

                # Preprocess the dataset
                ul_data = {
                'subset': 'unlabeled',
                'images': ['path/to/train/image1.jpg', 'path/to/train/image2.jpg'],
                'metadata': [{'id': 1, 'source': 'camera1'}, {'id': 2, 'source': 'camera2'}]}

                return [PreprocessResponse(length=len(train_data['images']), data=train_data)]

            leap_binder.set_preprocess(unlabeled_preprocess_func)
        """
        self.setup_container.unlabeled_data_preprocess = UnlabeledDataPreprocessHandler(function)

    def set_input(self, function: SectionCallableInterface, name: str, channel_dim: int = -1) -> None:
        """
        Set the input handler function.

        Args:
        function (SectionCallableInterface): The input handler function.
        name (str): The name of the input section.
        channel_dim (int): The dimension of the channels axis

        Example:
            def input_encoder(subset: PreprocessResponse, index: int) -> np.ndarray:
                # Return the processed input data for the given index and given subset response
                img_path = subset.`data["images"][idx]
                img = read_img(img_path)
                img = normalize(img)
                return img

            leap_binder.set_input(input_encoder, name='input_encoder', channel_dim=-1)
        """
        function = to_numpy_return_wrapper(function)
        self.setup_container.inputs.append(InputHandler(name, function, channel_dim=channel_dim))

        self._encoder_names.append(name)


    def set_instance_masks(self, function: InstanceCallableInterface, name: str) -> None:
        """
        Set the instance mask handler function.

        Args:
        function (SectionCallableInterface): The input handler function.
        name (str): The name of the instance mask section.

        Example:
            leap_binder.set_input(input_encoder, name='input_encoder')
        """
        function = to_numpy_return_masks_wrapper(function)
        self.setup_container.instance_masks.append(ElementInstanceMasksHandler(name, function))


    def add_custom_loss(self, function: CustomCallableInterface, name: str) -> None:
        """
        Add a custom loss function to the setup.

        Args:
        function (CustomCallableInterface): The custom loss function.
            This function receives:
                - y_true: The true labels or values.
                - y_pred: The predicted labels or values.
            This function should return:
                - A numeric value representing the loss.
        name (str): The name of the custom loss function.

        Example:
            def custom_loss_function(y_true, y_pred):
                # Calculate mean squared error as custom loss
                return np.mean(np.square(y_true - y_pred))

            leap_binder.add_custom_loss(custom_loss_function, name='custom_loss')
        """

        regular_arg_names = inspect.getfullargspec(function)[0]
        preprocess_response_arg_name = None
        for arg_name, arg_type in inspect.getfullargspec(function).annotations.items():
            if arg_type == SamplePreprocessResponse:
                if preprocess_response_arg_name is not None:
                    raise Exception("only one argument can be of type SamplePreprocessResponse")
                preprocess_response_arg_name = arg_name
                regular_arg_names.remove(arg_name)

        self.setup_container.custom_loss_handlers.append(
            CustomLossHandler(CustomLossHandlerData(name, regular_arg_names), function))

    def add_custom_metric(self,
                          function: Union[CustomCallableInterfaceMultiArgs,
                          CustomMultipleReturnCallableInterfaceMultiArgs,
                          ConfusionMatrixCallableInterfaceMultiArgs],
                          name: str,
                          direction: Optional[
                              Union[MetricDirection, Dict[str, MetricDirection]]] = MetricDirection.Downward,
                          compute_insights: Optional[Union[bool, Dict[str, bool]]] = None) -> None:
        """
        Add a custom metric to the setup.

        Args:
        function (Union[CustomCallableInterfaceMultiArgs, CustomMultipleReturnCallableInterfaceMultiArgs, ConfusionMatrixCallableInterfaceMultiArgs]): The custom metric function.
        name (str): The name of the custom metric.
        direction (Optional[Union[MetricDirection, Dict[str, MetricDirection]]]): The direction of the metric, either
        MetricDirection.Upward or MetricDirection.Downward, in case custom metric return a dictionary of metrics we can
        supply a dictionary of directions correspondingly.
            - MetricDirection.Upward: Indicates that higher values of the metric are better and should be maximized.
            - MetricDirection.Downward: Indicates that lower values of the metric are better and should be minimized.
        compute_insights (Union[bool, Dict[str, bool]]): Whether to compute insights or not. in case custom metric
        return a dictionary of metrics we can supply a dictionary of values correspondingly



        Example:
            def custom_metric_function(y_true, y_pred):
                return np.mean(np.abs(y_true - y_pred))

            leap_binder.add_custom_metric(custom_metric_function, name='custom_metric', direction=MetricDirection.Downward)
        """

        regular_arg_names = inspect.getfullargspec(function)[0]
        preprocess_response_arg_name = None
        for arg_name, arg_type in inspect.getfullargspec(function).annotations.items():
            if arg_type == SamplePreprocessResponse:
                if preprocess_response_arg_name is not None:
                    raise Exception("only one argument can be of type SamplePreprocessResponse")
                preprocess_response_arg_name = arg_name
                regular_arg_names.remove(arg_name)

        metric_handler_data = MetricHandlerData(name, regular_arg_names, direction, compute_insights)
        self.setup_container.metrics.append(MetricHandler(metric_handler_data, function))

    def add_prediction(self, name: str, labels: List[str], channel_dim: int = -1, prediction_index: Optional[int]=None) -> None:
        """
        Add prediction labels to the setup.

        Args:
        name (str): The name of the prediction.
        labels (List[str]): The list of labels for the prediction.
        channel_dim (int): The axis along which the prediction scores are located, default is -1.

        Must satisfy len(labels) == len(output[channel_dim]).

        Example:
            leap_binder.add_prediction(name='class_labels', labels=['cat', 'dog'])
        """
        self.setup_container.prediction_types.append(PredictionTypeHandler(name, labels, channel_dim))
        if prediction_index is not None:
            node_connection = NodeConnection(NodeMapping(name, NodeMappingType.PredictionLabels),
                                             {'temp': NodeMapping('', NodeMappingType(f'Prediction{prediction_index}'))})

            self.mapping_connections.append(node_connection)

    def set_ground_truth(self, function: SectionCallableInterface, name: str) -> None:
        """
        Set the ground truth handler function.

        Args:
        function: The ground truth handler function.
            This function receives two parameters:
                - subset: A `PreprocessResponse` object that contains the preprocessed data.
                - index: The index of the sample within the subset.
            This function should return:
                - A numpy array representing the ground truth for the given sample.

        name (str): The name of the ground truth section.

        Example:
            def ground_truth_handler(subset, index):
                label = subset.data['labels'][index]
                # Assuming labels are integers starting from 0
                num_classes = 10  # Example number of classes
                one_hot_label = np.zeros(num_classes)
                one_hot_label[label] = 1
                return one_hot_label

            leap_binder.set_ground_truth(ground_truth_handler, name='ground_truth')
        """

        function = to_numpy_return_wrapper(function)
        self.setup_container.ground_truths.append(GroundTruthHandler(name, function))

        self._encoder_names.append(name)

    def set_metadata(self, function: MetadataSectionCallableInterface, name: str,
                     metadata_type: Optional[Union[DatasetMetadataType, Dict[str, DatasetMetadataType]]] = None) -> None:
        """
        Set the metadata handler function. This function is used for measuring and analyzing external variable values per sample, which is recommended for analysis within the Tensorleap platform.

        Args:
        function (MetadataSectionCallableInterface): The metadata handler function.
            This function receives:
                subset (PreprocessResponse): The subset of the data.
                index (int): The index of the sample within the subset.
            This function should return one of the following:
                int: A single integer value.
                Dict[str, int]: A dictionary with string keys and integer values.
                str: A single string value.
                Dict[str, str]: A dictionary with string keys and string values.
                bool: A single boolean value.
                Dict[str, bool]: A dictionary with string keys and boolean values.
                float: A single float value.
                Dict[str, float]: A dictionary with string keys and float values.

        name (str): The name of the metadata section.

        Example:
            def metadata_handler_index(subset: PreprocessResponse, index: int) -> int:
                return subset.data['metadata'][index]


            def metadata_handler_image_mean(subset: PreprocessResponse, index: int) -> float:
                fpath = subset.data['images'][index]
                image = load_image(fpath)
                mean_value = np.mean(image)
                return mean_value

            leap_binder.set_metadata(metadata_handler_index, name='metadata_index')
            leap_binder.set_metadata(metadata_handler_image_mean, name='metadata_image_mean')
        """
        self.setup_container.metadata.append(MetadataHandler(name, function, metadata_type))

    def set_custom_layer(self, custom_layer: Type[Any], name: str, inspect_layer: bool = False,
                         kernel_index: Optional[int] = None, use_custom_latent_space: bool = False) -> None:
        """
        Set a custom layer for the model.

        Args:
        custom_layer (Type[Any]): The custom layer class.
        name (str): The name of the custom layer.
        inspect_layer (bool): Whether to inspect the layer, default is False.
        kernel_index (Optional[int]): The index of the kernel to inspect, if inspect_layer is True.
        use_custom_latent_space (bool): Whether to use a custom latent space, default is False.

        Example:
            class CustomLayer:
                def __init__(self, units: int):
                    self.units = units

                def call(self, inputs):
                    return inputs * self.units

            leap_binder.set_custom_layer(CustomLayer, name='custom_layer', inspect_layer=True, kernel_index=0)
        """
        if inspect_layer and kernel_index is not None:
            custom_layer.kernel_index = kernel_index

        if use_custom_latent_space and not hasattr(custom_layer, custom_latent_space_attribute):
            raise Exception(
                f"{custom_latent_space_attribute} function has not been set for custom layer: {custom_layer.__name__}")

        init_args = inspect.getfullargspec(custom_layer.__init__)[0][1:]
        call_args = inspect.getfullargspec(custom_layer.call)[0][1:]
        self.setup_container.custom_layers[name] = CustomLayerHandler(name, custom_layer, init_args, call_args,
                                                                      use_custom_latent_space=use_custom_latent_space)

    def check_preprocess(self, preprocess_result: Dict[DataStateEnum, PreprocessResponse]) -> None:
        preprocess_handler = self.setup_container.preprocess
        unlabeled_preprocess_handler = self.setup_container.unlabeled_data_preprocess

        if preprocess_handler is None:
            raise Exception('None preprocess_handler')

        for state, preprocess_response in preprocess_result.items():
            if preprocess_response.length is None or preprocess_response.length <= 0:
                raise Exception('Invalid dataset length')
            if unlabeled_preprocess_handler is not None and state == DataStateEnum.unlabeled:
                unlabeled_preprocess_handler.data_length = preprocess_response.length
            else:
                state_type = DataStateType(state.name)
                preprocess_handler.data_length[state_type] = preprocess_response.length

    def get_preprocess_result(self) -> Dict[DataStateEnum, PreprocessResponse]:
        preprocess = self.setup_container.preprocess
        if preprocess is None:
            raise Exception("Please make sure you call the leap_binder.set_preprocess method")
        preprocess_results = preprocess.function()
        preprocess_result_dict = {}
        for i, preprocess_result in enumerate(preprocess_results):
            if preprocess_result.state is None:
                state_enum = DataStateEnum(i)
                preprocess_result.state = DataStateType(state_enum.name)
            else:
                state_enum = DataStateEnum[preprocess_result.state.name]

            if state_enum in preprocess_result_dict:
                raise Exception(f"Duplicate state {state_enum.name} in preprocess results")
            preprocess_result_dict[state_enum] = preprocess_result

        if DataStateEnum.unlabeled not in preprocess_result_dict:
            preprocess_unlabeled_result = self.get_preprocess_unlabeled_result()
            if preprocess_unlabeled_result is not None:
                preprocess_result_dict[DataStateEnum.unlabeled] = preprocess_unlabeled_result

        if DataStateEnum.training not in preprocess_result_dict:
            raise Exception("Training data is required")
        if DataStateEnum.validation not in preprocess_result_dict:
            raise Exception("Validation data is required")

        preprocess_result_dict_in_correct_order = {}
        for state_enum in DataStateEnum:
            if state_enum in preprocess_result_dict:
                preprocess_result_dict_in_correct_order[state_enum] = preprocess_result_dict[state_enum]

        return preprocess_result_dict_in_correct_order

    def get_preprocess_unlabeled_result(self) -> Optional[PreprocessResponse]:
        unlabeled_preprocess = self.setup_container.unlabeled_data_preprocess
        if unlabeled_preprocess is not None:
            return unlabeled_preprocess.function()
        return None

    def _get_all_dataset_base_handlers(self) -> List[Union[DatasetBaseHandler, MetadataHandler]]:
        all_dataset_base_handlers: List[Union[DatasetBaseHandler, MetadataHandler]] = []
        all_dataset_base_handlers.extend(self.setup_container.inputs)
        all_dataset_base_handlers.extend(self.setup_container.ground_truths)
        all_dataset_base_handlers.extend(self.setup_container.metadata)
        return all_dataset_base_handlers

    @staticmethod
    def check_handler(
            preprocess_response: PreprocessResponse, test_result: List[DatasetTestResultPayload],
            dataset_base_handler: Union[DatasetBaseHandler, MetadataHandler], state: DataStateEnum) -> List[DatasetTestResultPayload]:
        assert preprocess_response.sample_ids is not None
        raw_result = dataset_base_handler.function(preprocess_response.sample_ids[0], preprocess_response)
        handler_type = 'metadata' if isinstance(dataset_base_handler, MetadataHandler) else None
        if isinstance(dataset_base_handler, MetadataHandler):
            if isinstance(raw_result, dict):
                metadata_test_result_payloads = [
                    DatasetTestResultPayload(f'{dataset_base_handler.name}_{single_metadata_name}')
                    for single_metadata_name, single_metadata_result in raw_result.items()
                ]
                for i, (single_metadata_name, single_metadata_result) in enumerate(raw_result.items()):
                    metadata_test_result = metadata_test_result_payloads[i]

                    if not isinstance(single_metadata_result, (int, str, bool, float, np.unsignedinteger,
                                                               np.signedinteger, np.bool_, np.floating, type(None))):
                        raise Exception(f"Unsupported return type of metadata {single_metadata_name}."
                                        f"The return type should be one of [int, float, str, bool, None]. Got {type(single_metadata_result)}")

                    metadata_type = None
                    if single_metadata_result is None:
                        if state != DataStateEnum.training and test_result[i].name == f'{dataset_base_handler.name}_{single_metadata_name}':
                            metadata_test_result_payloads[i] = test_result[i]
                            continue

                        if dataset_base_handler.metadata_type is None:
                            raise Exception(f"Metadata {single_metadata_name} is None and no metadata type is provided")
                        elif isinstance(dataset_base_handler.metadata_type, dict):
                            if single_metadata_name not in dataset_base_handler.metadata_type:
                                raise Exception(f"Metadata {single_metadata_name} is None and no metadata type is provided")
                            metadata_type = dataset_base_handler.metadata_type[single_metadata_name]
                        else:
                            raise Exception(f"Metadata {single_metadata_name} is None and metadata type is not a dict")

                    result_shape = get_shape(single_metadata_result)
                    metadata_test_result.shape = result_shape
                    metadata_test_result.raw_result = (
                        single_metadata_result) if single_metadata_result is not None else metadata_type
                    metadata_test_result.handler_type = handler_type
                test_result = metadata_test_result_payloads
            else:
                if raw_result is None:
                    if state != DataStateEnum.training:
                        return test_result

                    if dataset_base_handler.metadata_type is None:
                        raise Exception(f"Metadata {dataset_base_handler.name} is None and no metadata type is provided")
                    elif isinstance(dataset_base_handler.metadata_type, dict):
                        raise Exception(f"Metadata {dataset_base_handler.name} is None and no metadata type is provided")
                    metadata_type = dataset_base_handler.metadata_type

                result_shape = get_shape(raw_result)
                test_result[0].shape = result_shape
                test_result[0].raw_result = raw_result if raw_result is not None else metadata_type
                test_result[0].handler_type = handler_type
        else:
            result_shape = get_shape(raw_result)
            test_result[0].shape = result_shape
            test_result[0].raw_result = raw_result
            test_result[0].handler_type = handler_type

            # setting shape in setup for all encoders
            if isinstance(dataset_base_handler, (InputHandler, GroundTruthHandler)):
                dataset_base_handler.shape = result_shape
        return test_result

    def check_handlers(self, preprocess_result: Dict[DataStateEnum, PreprocessResponse]) -> None:
        dataset_base_handlers: List[Union[DatasetBaseHandler, MetadataHandler]] = self._get_all_dataset_base_handlers()
        for dataset_base_handler in dataset_base_handlers:
            test_result = [DatasetTestResultPayload(dataset_base_handler.name)]
            for state, preprocess_response in preprocess_result.items():
                if state == DataStateEnum.unlabeled and isinstance(dataset_base_handler, GroundTruthHandler):
                    continue
                test_result = self.check_handler(preprocess_response, test_result, dataset_base_handler, state)

    def check(self) -> None:
        preprocess_result = self.get_preprocess_result()
        self.check_preprocess(preprocess_result)
        self.check_handlers(preprocess_result)
        print("Successful!")

    def set_batch_size_to_validate(self, batch_size: int) -> None:
        self.batch_size_to_validate = batch_size
