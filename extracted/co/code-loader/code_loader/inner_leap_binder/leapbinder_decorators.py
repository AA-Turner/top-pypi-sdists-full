# mypy: ignore-errors

from typing import Optional, Union, Callable, List, Dict

import numpy as np
import numpy.typing as npt

from code_loader.contract.datasetclasses import CustomCallableInterfaceMultiArgs, \
    CustomMultipleReturnCallableInterfaceMultiArgs, ConfusionMatrixCallableInterfaceMultiArgs, CustomCallableInterface, \
    VisualizerCallableInterface, MetadataSectionCallableInterface, PreprocessResponse, SectionCallableInterface, \
    ConfusionMatrixElement, SamplePreprocessResponse, InstanceCallableInterface, ElementInstance
from code_loader.contract.enums import MetricDirection, LeapDataType, DatasetMetadataType
from code_loader import leap_binder
from code_loader.contract.mapping import NodeMapping, NodeMappingType, NodeConnection
from code_loader.contract.visualizer_classes import LeapImage, LeapImageMask, LeapTextMask, LeapText, LeapGraph, \
    LeapHorizontalBar, LeapImageWithBBox, LeapImageWithHeatmap


def _add_mapping_connections(connects_to, arg_names, node_mapping_type, name):
    for user_unique_name, connection_destinations in connects_to.items():
        main_node_mapping = NodeMapping(name, node_mapping_type, user_unique_name, arg_names=arg_names)
        node_inputs = {}
        for arg_name, destination in zip(arg_names, connection_destinations):
            node_inputs[arg_name] = destination.node_mapping

        leap_binder.mapping_connections.append(NodeConnection(main_node_mapping, node_inputs))


def tensorleap_custom_metric(name: str,
                             direction: Union[MetricDirection, Dict[str, MetricDirection]] = MetricDirection.Downward,
                             compute_insights: Optional[Union[bool, Dict[str, bool]]] = None,
                             connects_to=None):
    def decorating_function(user_function: Union[CustomCallableInterfaceMultiArgs,
    CustomMultipleReturnCallableInterfaceMultiArgs,
    ConfusionMatrixCallableInterfaceMultiArgs]):
        for metric_handler in leap_binder.setup_container.metrics:
            if metric_handler.metric_handler_data.name == name:
                raise Exception(f'Metric with name {name} already exists. '
                                f'Please choose another')

        leap_binder.add_custom_metric(user_function, name, direction, compute_insights)

        if connects_to is not None:
            arg_names = leap_binder.setup_container.metrics[-1].metric_handler_data.arg_names
            _add_mapping_connections(connects_to, arg_names, NodeMappingType.Metric, name)

        def _validate_input_args(*args, **kwargs) -> None:
            for i, arg in enumerate(args):
                assert isinstance(arg, (np.ndarray, SamplePreprocessResponse)), (
                    f'tensorleap_custom_metric validation failed: '
                    f'Argument #{i} should be a numpy array. Got {type(arg)}.')
                if leap_binder.batch_size_to_validate and isinstance(arg, np.ndarray):
                    assert arg.shape[0] == leap_binder.batch_size_to_validate, \
                        (f'tensorleap_custom_metric validation failed: Argument #{i} '
                         f'first dim should be as the batch size. Got {arg.shape[0]} '
                         f'instead of {leap_binder.batch_size_to_validate}')

            for _arg_name, arg in kwargs.items():
                assert isinstance(arg, (np.ndarray, SamplePreprocessResponse)), (
                    f'tensorleap_custom_metric validation failed: '
                    f'Argument {_arg_name} should be a numpy array. Got {type(arg)}.')
                if leap_binder.batch_size_to_validate and isinstance(arg, np.ndarray):
                    assert arg.shape[0] == leap_binder.batch_size_to_validate, \
                        (f'tensorleap_custom_metric validation failed: Argument {_arg_name} '
                         f'first dim should be as the batch size. Got {arg.shape[0]} '
                         f'instead of {leap_binder.batch_size_to_validate}')

        def _validate_result(result) -> None:
            supported_types_message = (f'tensorleap_custom_metric validation failed: '
                                       f'Metric has returned unsupported type. Supported types are List[float], '
                                       f'List[List[ConfusionMatrixElement]], NDArray[np.float32]. ')

            def _validate_single_metric(single_metric_result):
                if isinstance(single_metric_result, list):
                    if isinstance(single_metric_result[0], list):
                        assert isinstance(single_metric_result[0][0], ConfusionMatrixElement), \
                            f'{supported_types_message}Got List[List[{type(single_metric_result[0][0])}]].'
                    else:
                        assert isinstance(single_metric_result[0], (
                            float, int, type(None))), f'{supported_types_message}Got List[{type(single_metric_result[0])}].'
                else:
                    assert isinstance(single_metric_result,
                                      np.ndarray), f'{supported_types_message}Got {type(single_metric_result)}.'
                    assert len(single_metric_result.shape) == 1, (f'tensorleap_custom_metric validation failed: '
                                                                  f'The return shape should be 1D. Got {len(single_metric_result.shape)}D.')

                if leap_binder.batch_size_to_validate:
                    assert len(single_metric_result) == leap_binder.batch_size_to_validate, \
                        f'tensorleap_custom_metrix validation failed: The return len should be as the batch size.'

            if isinstance(result, dict):
                for key, value in result.items():
                    assert isinstance(key, str), \
                        (f'tensorleap_custom_metric validation failed: '
                         f'Keys in the return dict should be of type str. Got {type(key)}.')
                    _validate_single_metric(value)

                if isinstance(direction, dict):
                    for direction_key in direction:
                        assert direction_key in result, \
                            (f'tensorleap_custom_metric validation failed: '
                             f'Keys in the direction mapping should be part of result keys. Got key {direction_key}.')

                if compute_insights is not None:
                    assert isinstance(compute_insights, dict), \
                        (f'tensorleap_custom_metric validation failed: '
                         f'compute_insights should be dict if using the dict results. Got {type(compute_insights)}.')

                    for ci_key in compute_insights:
                        assert ci_key in result, \
                            (f'tensorleap_custom_metric validation failed: '
                             f'Keys in the compute_insights mapping should be part of result keys. Got key {ci_key}.')

            else:
                _validate_single_metric(result)

                if compute_insights is not None:
                    assert isinstance(compute_insights, bool), \
                        (f'tensorleap_custom_metric validation failed: '
                         f'compute_insights should be boolean. Got {type(compute_insights)}.')


        def inner(*args, **kwargs):
            _validate_input_args(*args, **kwargs)
            result = user_function(*args, **kwargs)
            _validate_result(result)
            return result

        return inner

    return decorating_function


def tensorleap_custom_visualizer(name: str, visualizer_type: LeapDataType,
                                 heatmap_function: Optional[Callable[..., npt.NDArray[np.float32]]] = None,
                                 connects_to=None):
    def decorating_function(user_function: VisualizerCallableInterface):
        for viz_handler in leap_binder.setup_container.visualizers:
            if viz_handler.visualizer_handler_data.name == name:
                raise Exception(f'Visualizer with name {name} already exists. '
                                f'Please choose another')

        leap_binder.set_visualizer(user_function, name, visualizer_type, heatmap_function)

        if connects_to is not None:
            arg_names = leap_binder.setup_container.visualizers[-1].visualizer_handler_data.arg_names
            _add_mapping_connections(connects_to, arg_names, NodeMappingType.Visualizer, name)

        def _validate_input_args(*args, **kwargs):
            for i, arg in enumerate(args):
                assert isinstance(arg, (np.ndarray, SamplePreprocessResponse)), (
                    f'tensorleap_custom_visualizer validation failed: '
                    f'Argument #{i} should be a numpy array. Got {type(arg)}.')
                if leap_binder.batch_size_to_validate and isinstance(arg, np.ndarray):
                    assert arg.shape[0] != leap_binder.batch_size_to_validate, \
                        (f'tensorleap_custom_visualizer validation failed: '
                         f'Argument #{i} should be without batch dimension. ')

            for _arg_name, arg in kwargs.items():
                assert isinstance(arg, (np.ndarray, SamplePreprocessResponse)), (
                    f'tensorleap_custom_visualizer validation failed: '
                    f'Argument {_arg_name} should be a numpy array. Got {type(arg)}.')
                if leap_binder.batch_size_to_validate and isinstance(arg, np.ndarray):
                    assert arg.shape[0] != leap_binder.batch_size_to_validate, \
                        (f'tensorleap_custom_visualizer validation failed: Argument {_arg_name} '
                         f'should be without batch dimension. ')

        def _validate_result(result):
            result_type_map = {
                LeapDataType.Image: LeapImage,
                LeapDataType.ImageMask: LeapImageMask,
                LeapDataType.TextMask: LeapTextMask,
                LeapDataType.Text: LeapText,
                LeapDataType.Graph: LeapGraph,
                LeapDataType.HorizontalBar: LeapHorizontalBar,
                LeapDataType.ImageWithBBox: LeapImageWithBBox,
                LeapDataType.ImageWithHeatmap: LeapImageWithHeatmap
            }
            assert isinstance(result, result_type_map[visualizer_type]), \
                (f'tensorleap_custom_visualizer validation failed: '
                 f'The return type should be {result_type_map[visualizer_type]}. Got {type(result)}.')

        def inner(*args, **kwargs):
            _validate_input_args(*args, **kwargs)
            result = user_function(*args, **kwargs)
            _validate_result(result)
            return result

        return inner

    return decorating_function


def tensorleap_metadata(
        name: str, metadata_type: Optional[Union[DatasetMetadataType, Dict[str, DatasetMetadataType]]] = None):
    def decorating_function(user_function: MetadataSectionCallableInterface):
        for metadata_handler in leap_binder.setup_container.metadata:
            if metadata_handler.name == name:
                raise Exception(f'Metadata with name {name} already exists. '
                                f'Please choose another')

        leap_binder.set_metadata(user_function, name, metadata_type)

        def _validate_input_args(sample_id: Union[int, str], preprocess_response: PreprocessResponse):
            assert isinstance(sample_id, (int, str)), \
                (f'tensorleap_metadata validation failed: '
                 f'Argument sample_id should be either int or str. Got {type(sample_id)}.')
            assert isinstance(preprocess_response, PreprocessResponse), \
                (f'tensorleap_metadata validation failed: '
                 f'Argument preprocess_response should be a PreprocessResponse. Got {type(preprocess_response)}.')
            assert type(sample_id) == preprocess_response.sample_id_type, \
                (f'tensorleap_metadata validation failed: '
                 f'Argument sample_id should be as the same type as defined in the preprocess response '
                 f'{preprocess_response.sample_id_type}. Got {type(sample_id)}.')

        def _validate_result(result):
            supported_result_types = (type(None), int, str, bool, float, dict, np.floating,
                                      np.bool_, np.unsignedinteger, np.signedinteger, np.integer)
            assert isinstance(result, supported_result_types), \
                (f'tensorleap_metadata validation failed: '
                 f'Unsupported return type. Got {type(result)}. should be any of {str(supported_result_types)}')
            if isinstance(result, dict):
                for key, value in result.items():
                    assert isinstance(key, str), \
                        (f'tensorleap_metadata validation failed: '
                         f'Keys in the return dict should be of type str. Got {type(key)}.')
                    assert isinstance(value, supported_result_types), \
                        (f'tensorleap_metadata validation failed: '
                         f'Values in the return dict should be of type {str(supported_result_types)}. Got {type(value)}.')

        def inner(sample_id, preprocess_response):
            _validate_input_args(sample_id, preprocess_response)
            result = user_function(sample_id, preprocess_response)
            _validate_result(result)
            return result

        return inner

    return decorating_function


def tensorleap_preprocess():
    def decorating_function(user_function: Callable[[], List[PreprocessResponse]]):
        leap_binder.set_preprocess(user_function)

        def _validate_input_args(*args, **kwargs):
            assert len(args) == 0 and len(kwargs) == 0, \
                (f'tensorleap_preprocess validation failed: '
                 f'The function should not take any arguments. Got {args} and {kwargs}.')

        def _validate_result(result):
            assert isinstance(result, list), \
                (f'tensorleap_preprocess validation failed: '
                 f'The return type should be a list. Got {type(result)}.')
            for i, response in enumerate(result):
                assert isinstance(response, PreprocessResponse), \
                    (f'tensorleap_preprocess validation failed: '
                     f'Element #{i} in the return list should be a PreprocessResponse. Got {type(response)}.')
            assert len(set(result)) == len(result), \
                (f'tensorleap_preprocess validation failed: '
                 f'The return list should not contain duplicate PreprocessResponse objects.')

        def inner(*args, **kwargs):
            _validate_input_args(*args, **kwargs)
            result = user_function()
            _validate_result(result)
            return result

        return inner

    return decorating_function

def tensorleap_element_instance_preprocess(instance_mask_encoder: Callable[[str, PreprocessResponse], List[ElementInstance]]):
    def decorating_function(user_function: Callable[[], List[PreprocessResponse]]):
        def user_function_instance() -> List[PreprocessResponse]:
            result = user_function()
            for preprocess_response in result:
                sample_ids_to_instance_mappings = {}
                instance_to_sample_ids_mappings = {}
                instance_ids_to_names = {}
                all_sample_ids = preprocess_response.sample_ids.copy()
                for sample_id in preprocess_response.sample_ids:
                    instances_masks = instance_mask_encoder(sample_id, preprocess_response)
                    instances_ids = [f'{sample_id}_{instance_id}' for instance_id in range(len(instances_masks))]
                    sample_ids_to_instance_mappings[sample_id] = instances_ids
                    instance_to_sample_ids_mappings[sample_id] = sample_id
                    instance_names = [instance.name for instance in instances_masks]
                    instance_ids_to_names[sample_id] = 'none'
                    for instance_id, instance_name in zip(instances_ids, instance_names):
                        instance_to_sample_ids_mappings[instance_id] = sample_id
                        instance_ids_to_names[instance_id] = instance_name
                    all_sample_ids.extend(instances_ids)
                preprocess_response.sample_ids_to_instance_mappings = sample_ids_to_instance_mappings
                preprocess_response.instance_to_sample_ids_mappings = instance_to_sample_ids_mappings
                preprocess_response.instance_ids_to_names = instance_ids_to_names
                preprocess_response.sample_ids = all_sample_ids
            return result

        def builtin_instance_metadata(idx: str, preprocess: PreprocessResponse) -> Dict[str, str]:
            return {'is_instance': '0', 'original_sample_id': idx, 'instance_name': 'none'}
        leap_binder.set_preprocess(user_function_instance)
        leap_binder.set_metadata(builtin_instance_metadata, "builtin_instance_metadata")

        def _validate_input_args(*args, **kwargs):
            assert len(args) == 0 and len(kwargs) == 0, \
                (f'tensorleap_element_instance_preprocess validation failed: '
                 f'The function should not take any arguments. Got {args} and {kwargs}.')

        def _validate_result(result):
            assert isinstance(result, list), \
                (f'tensorleap_element_instance_preprocess validation failed: '
                 f'The return type should be a list. Got {type(result)}.')
            for i, response in enumerate(result):
                assert isinstance(response, PreprocessResponse), \
                    (f'tensorleap_element_instance_preprocess validation failed: '
                     f'Element #{i} in the return list should be a PreprocessResponse. Got {type(response)}.')
            assert len(set(result)) == len(result), \
                (f'tensorleap_element_instance_preprocess validation failed: '
                 f'The return list should not contain duplicate PreprocessResponse objects.')

        def inner(*args, **kwargs):
            _validate_input_args(*args, **kwargs)
            result = user_function_instance()
            _validate_result(result)
            return result

        return inner

    return decorating_function


def tensorleap_unlabeled_preprocess():
    def decorating_function(user_function: Callable[[], PreprocessResponse]):
        leap_binder.set_unlabeled_data_preprocess(user_function)

        def _validate_input_args(*args, **kwargs):
            assert len(args) == 0 and len(kwargs) == 0, \
                (f'tensorleap_unlabeled_preprocess validation failed: '
                 f'The function should not take any arguments. Got {args} and {kwargs}.')

        def _validate_result(result):
            assert isinstance(result, PreprocessResponse), \
                (f'tensorleap_unlabeled_preprocess validation failed: '
                 f'The return type should be a PreprocessResponse. Got {type(result)}.')

        def inner(*args, **kwargs):
            _validate_input_args(*args, **kwargs)
            result = user_function()
            _validate_result(result)
            return result

        return inner

    return decorating_function


def tensorleap_instances_masks_encoder(name: str):
    def decorating_function(user_function: InstanceCallableInterface):
        leap_binder.set_instance_masks(user_function, name)

        def _validate_input_args(sample_id: str, preprocess_response: PreprocessResponse):
            assert isinstance(sample_id, str), \
                (f'tensorleap_instances_masks_encoder validation failed: '
                 f'Argument sample_id should be str. Got {type(sample_id)}.')
            assert isinstance(preprocess_response, PreprocessResponse), \
                (f'tensorleap_instances_masks_encoder validation failed: '
                 f'Argument preprocess_response should be a PreprocessResponse. Got {type(preprocess_response)}.')
            assert type(sample_id) == preprocess_response.sample_id_type, \
                (f'tensorleap_instances_masks_encoder validation failed: '
                 f'Argument sample_id should be as the same type as defined in the preprocess response '
                 f'{preprocess_response.sample_id_type}. Got {type(sample_id)}.')

        def _validate_result(result):
            assert isinstance(result, list), \
                (f'tensorleap_instances_masks_encoder validation failed: '
                 f'Unsupported return type. Should be a numpy array. Got {type(result)}.')

        def inner(sample_id, preprocess_response):
            _validate_input_args(sample_id, preprocess_response)
            result = user_function(sample_id, preprocess_response)
            _validate_result(result)
            return result

        return inner

    return decorating_function


def tensorleap_input_encoder(name: str, channel_dim=-1, model_input_index=None):
    def decorating_function(user_function: SectionCallableInterface):
        for input_handler in leap_binder.setup_container.inputs:
            if input_handler.name == name:
                raise Exception(f'Input with name {name} already exists. '
                                f'Please choose another')
        if channel_dim <= 0 and channel_dim != -1:
            raise Exception(f"Channel dim for input {name} is expected to be either -1 or positive")

        leap_binder.set_input(user_function, name, channel_dim=channel_dim)

        def _validate_input_args(sample_id: Union[int, str], preprocess_response: PreprocessResponse):
            assert isinstance(sample_id, (int, str)), \
                (f'tensorleap_input_encoder validation failed: '
                 f'Argument sample_id should be either int or str. Got {type(sample_id)}.')
            assert isinstance(preprocess_response, PreprocessResponse), \
                (f'tensorleap_input_encoder validation failed: '
                 f'Argument preprocess_response should be a PreprocessResponse. Got {type(preprocess_response)}.')
            assert type(sample_id) == preprocess_response.sample_id_type, \
                (f'tensorleap_input_encoder validation failed: '
                 f'Argument sample_id should be as the same type as defined in the preprocess response '
                 f'{preprocess_response.sample_id_type}. Got {type(sample_id)}.')

        def _validate_result(result):
            assert isinstance(result, np.ndarray), \
                (f'tensorleap_input_encoder validation failed: '
                 f'Unsupported return type. Should be a numpy array. Got {type(result)}.')
            assert result.dtype == np.float32, \
                (f'tensorleap_input_encoder validation failed: '
                 f'The return type should be a numpy array of type float32. Got {result.dtype}.')
            assert channel_dim - 1 <= len(result.shape), (f'tensorleap_input_encoder validation failed: '
                                                          f'The channel_dim ({channel_dim}) should be <= to the rank of the resulting input rank ({len(result.shape)}).')

        def inner(sample_id, preprocess_response):
            _validate_input_args(sample_id, preprocess_response)
            result = user_function(sample_id, preprocess_response)
            _validate_result(result)
            return result

        node_mapping_type = NodeMappingType.Input
        if model_input_index is not None:
            node_mapping_type = NodeMappingType(f'Input{str(model_input_index)}')
        inner.node_mapping = NodeMapping(name, node_mapping_type)

        return inner

    return decorating_function


def tensorleap_gt_encoder(name: str):
    def decorating_function(user_function: SectionCallableInterface):
        for gt_handler in leap_binder.setup_container.ground_truths:
            if gt_handler.name == name:
                raise Exception(f'GT with name {name} already exists. '
                                f'Please choose another')

        leap_binder.set_ground_truth(user_function, name)

        def _validate_input_args(sample_id: Union[int, str], preprocess_response: PreprocessResponse):
            assert isinstance(sample_id, (int, str)), \
                (f'tensorleap_gt_encoder validation failed: '
                 f'Argument sample_id should be either int or str. Got {type(sample_id)}.')
            assert isinstance(preprocess_response, PreprocessResponse), \
                (f'tensorleap_gt_encoder validation failed: '
                 f'Argument preprocess_response should be a PreprocessResponse. Got {type(preprocess_response)}.')
            assert type(sample_id) == preprocess_response.sample_id_type, \
                (f'tensorleap_gt_encoder validation failed: '
                 f'Argument sample_id should be as the same type as defined in the preprocess response '
                 f'{preprocess_response.sample_id_type}. Got {type(sample_id)}.')

        def _validate_result(result):
            assert isinstance(result, np.ndarray), \
                (f'tensorleap_gt_encoder validation failed: '
                 f'Unsupported return type. Should be a numpy array. Got {type(result)}.')
            assert result.dtype == np.float32, \
                (f'tensorleap_gt_encoder validation failed: '
                 f'The return type should be a numpy array of type float32. Got {result.dtype}.')

        def inner(sample_id, preprocess_response):
            _validate_input_args(sample_id, preprocess_response)
            result = user_function(sample_id, preprocess_response)
            _validate_result(result)
            return result

        inner.node_mapping = NodeMapping(name, NodeMappingType.GroundTruth)

        return inner



    return decorating_function


def tensorleap_custom_loss(name: str, connects_to=None):
    def decorating_function(user_function: CustomCallableInterface):
        for loss_handler in leap_binder.setup_container.custom_loss_handlers:
            if loss_handler.custom_loss_handler_data.name == name:
                raise Exception(f'Custom loss with name {name} already exists. '
                                f'Please choose another')

        leap_binder.add_custom_loss(user_function, name)

        if connects_to is not None:
            arg_names = leap_binder.setup_container.custom_loss_handlers[-1].custom_loss_handler_data.arg_names
            _add_mapping_connections(connects_to, arg_names, NodeMappingType.CustomLoss, name)


        valid_types = (np.ndarray, SamplePreprocessResponse)
        try:
            import tensorflow as tf
            valid_types = (np.ndarray, SamplePreprocessResponse, tf.Tensor)
        except ImportError:
            pass

        def _validate_input_args(*args, **kwargs):

            for i, arg in enumerate(args):
                if isinstance(arg, list):
                    for y, elem in enumerate(arg):
                        assert isinstance(elem, valid_types), (f'tensorleap_custom_loss validation failed: '
                                                               f'Element #{y} of list should be a numpy array. Got {type(elem)}.')
                else:
                    assert isinstance(arg, valid_types), (f'tensorleap_custom_loss validation failed: '
                                                          f'Argument #{i} should be a numpy array. Got {type(arg)}.')
            for _arg_name, arg in kwargs.items():
                if isinstance(arg, list):
                    for y, elem in enumerate(arg):
                        assert isinstance(elem, valid_types), (f'tensorleap_custom_loss validation failed: '
                                                               f'Element #{y} of list should be a numpy array. Got {type(elem)}.')
                else:
                    assert isinstance(arg, valid_types), (f'tensorleap_custom_loss validation failed: '
                                                          f'Argument #{_arg_name} should be a numpy array. Got {type(arg)}.')

        def _validate_result(result):
            assert isinstance(result, valid_types), \
                (f'tensorleap_custom_loss validation failed: '
                 f'The return type should be a numpy array. Got {type(result)}.')

        def inner(*args, **kwargs):
            _validate_input_args(*args, **kwargs)
            result = user_function(*args, **kwargs)
            _validate_result(result)
            return result

        return inner

    return decorating_function


def tensorleap_custom_layer(name: str):
    def decorating_function(custom_layer):
        for custom_layer_handler in leap_binder.setup_container.custom_layers.values():
            if custom_layer_handler.name == name:
                raise Exception(f'Custom Layer with name {name} already exists. '
                                f'Please choose another')

        try:
            import tensorflow as tf
        except ImportError as e:
            raise Exception('Custom layer should be inherit from tf.keras.layers.Layer') from e

        if not issubclass(custom_layer, tf.keras.layers.Layer):
            raise Exception('Custom layer should be inherit from tf.keras.layers.Layer')

        leap_binder.set_custom_layer(custom_layer, name)

        return custom_layer

    return decorating_function
