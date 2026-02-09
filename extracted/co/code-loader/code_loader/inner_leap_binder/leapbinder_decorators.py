# mypy: ignore-errors
import os
import warnings
import logging
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Optional, Union, Callable, List, Dict, Set, Any
from typing import Optional, Union, Callable, List, Dict, get_args, get_origin, DefaultDict

import numpy as np
import numpy.typing as npt

from code_loader.utils import get_metadata_type_from_variable, map_dict_to_metadata_types

logger = logging.getLogger(__name__)

from code_loader.contract.datasetclasses import CustomCallableInterfaceMultiArgs, \
    CustomMultipleReturnCallableInterfaceMultiArgs, ConfusionMatrixCallableInterfaceMultiArgs, CustomCallableInterface, \
    VisualizerCallableInterface, MetadataSectionCallableInterface, PreprocessResponse, SectionCallableInterface, \
    ConfusionMatrixElement, SamplePreprocessResponse, PredictionTypeHandler, InstanceCallableInterface, ElementInstance, \
    InstanceLengthCallableInterface
from code_loader.contract.enums import MetricDirection, LeapDataType, DatasetMetadataType, DataStateType
from code_loader import leap_binder, LeapLoader
from code_loader.contract.mapping import NodeMapping, NodeMappingType, NodeConnection
from code_loader.contract.visualizer_classes import LeapImage, LeapImageMask, LeapTextMask, LeapText, LeapGraph, \
    LeapHorizontalBar, LeapImageWithBBox, LeapImageWithHeatmap
from code_loader.inner_leap_binder.leapbinder import mapping_runtime_mode_env_var_mame
from code_loader.mixpanel_tracker import clear_integration_events, AnalyticsEvent, emit_integration_event_once

import inspect
import functools
from pathlib import Path

_called_from_inside_tl_decorator = 0
_called_from_inside_tl_integration_test_decorator = False
_call_from_tl_platform = os.environ.get('IS_TENSORLEAP_PLATFORM') == 'true'

# ---- warnings store (module-level) ----
_UNSET = object()
_STORED_WARNINGS: List[Dict[str, Any]] = []
_STORED_WARNING_KEYS: Set[tuple] = set()
# param_name -> set(user_func_name)
_PARAM_DEFAULT_FUNCS: DefaultDict[str, Set[str]] = defaultdict(set)
# param_name -> default_value used (repr-able)
_PARAM_DEFAULT_VALUE: Dict[str, Any] = {}
_PARAM_DEFAULT_DOCS: Dict[str, str] = {}


def get_entry_script_path() -> str:
    import sys
    argv0 = sys.argv[0] if sys.argv else ""
    if argv0:
        return str(Path(argv0).resolve())
    import __main__
    main_file = getattr(__main__, "__file__", "") or ""
    return str(Path(main_file).resolve()) if main_file else ""

def started_from(filename: str) -> bool:
    entry = get_entry_script_path()
    return bool(entry) and Path(entry).name == filename


def store_warning_by_param(
        *,
        param_name: str,
        user_func_name: str,
        default_value: Any,
        link_to_docs: str = None,
) -> None:
    _PARAM_DEFAULT_FUNCS[param_name].add(user_func_name)

    if param_name not in _PARAM_DEFAULT_VALUE:
        _PARAM_DEFAULT_VALUE[param_name] = default_value

    if link_to_docs and param_name not in _PARAM_DEFAULT_DOCS:
        _PARAM_DEFAULT_DOCS[param_name] = link_to_docs


def _get_param_default_warnings() -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for p, funcs in _PARAM_DEFAULT_FUNCS.items():
        out[p] = {
            "default_value": _PARAM_DEFAULT_VALUE.get(p, None),
            "funcs": set(funcs),
            "link_to_docs": _PARAM_DEFAULT_DOCS.get(p),
        }
    return out


def _get_stored_warnings() -> List[Dict[str, Any]]:
    return list(_STORED_WARNINGS)


def validate_args_structure(*args, types_order, func_name, expected_names, **kwargs):
    def _type_to_str(t):
        origin = get_origin(t)
        if origin is Union:
            return " | ".join(tt.__name__ for tt in get_args(t))
        elif hasattr(t, "__name__"):
            return t.__name__
        else:
            return str(t)

    def _format_types(types, names=None):
        return ", ".join(
            f"{(names[i] + ': ') if names else f'arg{i}: '}{_type_to_str(ty)}"
            for i, ty in enumerate(types)
        )

    if expected_names:
        normalized_args = []
        for i, name in enumerate(expected_names):
            if i < len(args):
                normalized_args.append(args[i])
            elif name in kwargs:
                normalized_args.append(kwargs[name])
            else:
                raise AssertionError(
                    f"{func_name} validation failed: "
                    f"Missing required argument '{name}'. "
                    f"Expected arguments: {expected_names}."
                )
    else:
        normalized_args = list(args)
    if len(normalized_args) != len(types_order):
        expected = _format_types(types_order, expected_names)
        got_types = ", ".join(type(arg).__name__ for arg in normalized_args)
        raise AssertionError(
            f"{func_name} validation failed: "
            f"Expected exactly {len(types_order)} arguments ({expected}), "
            f"but got {len(normalized_args)} argument(s) of type(s): ({got_types}). "
            f"Correct usage example: {func_name}({expected})"
        )

    for i, (arg, expected_type) in enumerate(zip(normalized_args, types_order)):
        origin = get_origin(expected_type)
        if origin is Union:
            allowed_types = get_args(expected_type)
        else:
            allowed_types = (expected_type,)

        if not isinstance(arg, allowed_types):
            allowed_str = " | ".join(t.__name__ for t in allowed_types)
            raise AssertionError(
                f"{func_name} validation failed: "
                f"Argument '{expected_names[i] if expected_names else f'arg{i}'}' "
                f"expected type {allowed_str}, but got {type(arg).__name__}. "
                f"Correct usage example: {func_name}({_format_types(types_order, expected_names)})"
            )


def validate_output_structure(result, func_name: str, expected_type_name="np.ndarray", gt_flag=False):
    if result is None or (isinstance(result, float) and np.isnan(result)):
        if gt_flag:
            raise AssertionError(
                f"{func_name} validation failed: "
                f"The function returned {result!r}. "
                f"If you are working with an unlabeled dataset and no ground truth is available, "
                f"use 'return np.array([], dtype=np.float32)' instead. "
                f"Otherwise, {func_name} expected a single {expected_type_name} object. "
                f"Make sure the function ends with 'return <{expected_type_name}>'."
            )

        raise AssertionError(
            f"{func_name} validation failed: "
            f"The function returned None. "
            f"Expected a single {expected_type_name} object. "
            f"Make sure the function ends with 'return <{expected_type_name}>'."
        )
    if isinstance(result, tuple):
        element_descriptions = [
            f"[{i}] type: {type(r).__name__}"
            for i, r in enumerate(result)
        ]
        element_summary = "\n    ".join(element_descriptions)

        raise AssertionError(
            f"{func_name} validation failed: "
            f"The function returned multiple outputs ({len(result)} values), "
            f"but only a single {expected_type_name} is allowed.\n\n"
            f"Returned elements:\n"
            f"    {element_summary}\n\n"
            f"Correct usage example:\n"
            f"    def {func_name}(...):\n"
            f"        return <{expected_type_name}>\n\n"
            f"If you intended to return multiple values, combine them into a single "
            f"{expected_type_name} (e.g., by concatenation or stacking)."
        )


def batch_warning(result, func_name):
    if len(result.shape) > 0 and result.shape[0] == 1:
        warnings.warn(
            f"{func_name} warning: Tensorleap will add a batch dimension at axis 0 to the output of {func_name}, "
            f"although the detected size of axis 0 is already 1. "
            f"This may lead to an extra batch dimension (e.g., shape (1, 1, ...)). "
            f"Please ensure that the output of '{func_name}' is not already batched "
            f"to avoid computation errors."
        )


def _add_mapping_connection(user_unique_name, connection_destinations, arg_names, name, node_mapping_type):
    connection_destinations = [connection_destination for connection_destination in connection_destinations
                               if not isinstance(connection_destination, SamplePreprocessResponse)]

    main_node_mapping = NodeMapping(name, node_mapping_type, user_unique_name, arg_names=arg_names)

    node_inputs = {}
    for arg_name, destination in zip(arg_names, connection_destinations):
        node_inputs[arg_name] = destination.node_mapping

    leap_binder.mapping_connections.append(NodeConnection(main_node_mapping, node_inputs))


def _add_mapping_connections(connects_to, arg_names, node_mapping_type, name):
    for user_unique_name, connection_destinations in connects_to.items():
        _add_mapping_connection(user_unique_name, connection_destinations, arg_names, name, node_mapping_type)


def tensorleap_integration_test():
    def decorating_function(integration_test_function: Callable):
        leap_binder.integration_test_func = integration_test_function

        def _validate_input_args(*args, **kwargs):
            sample_id, preprocess_response = args
            assert type(sample_id) == preprocess_response.sample_id_type, (
                f"tensorleap_integration_test validation failed: "
                f"sample_id type ({type(sample_id).__name__}) does not match the expected "
                f"type ({preprocess_response.sample_id_type}) from the PreprocessResponse."
            )

        def inner(*args, **kwargs):
            if not _call_from_tl_platform:
                set_current('tensorleap_integration_test')
            validate_args_structure(*args, types_order=[Union[int, str], PreprocessResponse],
                                    func_name='integration_test', expected_names=["idx", "preprocess"], **kwargs)
            _validate_input_args(*args, **kwargs)

            global _called_from_inside_tl_integration_test_decorator
            # Clear integration test events for new test
            try:
                clear_integration_events()
            except Exception as e:
                logger.debug(f"Failed to clear integration events: {e}")
            try:
                _called_from_inside_tl_integration_test_decorator = True
                if not _call_from_tl_platform:
                    update_env_params_func("tensorleap_integration_test",
                                           "v")  # put here because otherwise it will become  v only if it finishes all the script
                ret = integration_test_function(*args, **kwargs)

                try:
                    os.environ[mapping_runtime_mode_env_var_mame] = 'True'
                    integration_test_function(None, PreprocessResponse(state=DataStateType.training, length=0))
                except Exception as e:
                    import traceback
                    first_tb = traceback.extract_tb(e.__traceback__)[-1]
                    file_name = Path(first_tb.filename).name
                    line_number = first_tb.lineno
                    if isinstance(e, TypeError) and 'is not subscriptable' in str(e):
                        update_env_params_func("code_mapping", "x")
                        raise (f'Invalid integration code. File {file_name}, line {line_number}: '
                               f"indexing is supported only on the model's predictions inside the integration test. Please remove this indexing operation usage from the integration test code.")
                    else:
                        update_env_params_func("code_mapping", "x")

                        raise (f'Invalid integration code. File {file_name}, line {line_number}: '
                               f'Integration test is only allowed to call Tensorleap decorators. '
                               f'Ensure any arithmetics, external library use, Python logic is placed within Tensorleap decoders')
                finally:
                    if mapping_runtime_mode_env_var_mame in os.environ:
                        del os.environ[mapping_runtime_mode_env_var_mame]
            finally:
                _called_from_inside_tl_integration_test_decorator = False

            leap_binder.check()

        return inner

    return decorating_function


def _safe_get_item(key):
    try:
        return NodeMappingType[f'Input{str(key)}']
    except ValueError:
        raise Exception(f'Tensorleap currently supports models with no more then 10 inputs')


def tensorleap_load_model(prediction_types: Optional[List[PredictionTypeHandler]] = _UNSET):
    prediction_types_was_provided = prediction_types is not _UNSET

    if not prediction_types_was_provided:
        prediction_types = []
        if not _call_from_tl_platform:
            store_warning_by_param(
                param_name="prediction_types",
                user_func_name="tensorleap_load_model",
                default_value=prediction_types,
                link_to_docs="https://docs.tensorleap.ai/tensorleap-integration/integration-test#tensorleap_load_model"
            )
    assert isinstance(prediction_types, list), (
        f"tensorleap_load_model validation failed: "
        f" prediction_types is an optional argument of type List[PredictionTypeHandler]] but got {type(prediction_types).__name__}."
    )
    for i, prediction_type in enumerate(prediction_types):
        assert isinstance(prediction_type, PredictionTypeHandler), (f"tensorleap_load_model validation failed: "
                                                                    f" prediction_types at position {i} must be of type PredictionTypeHandler but got {type(prediction_types[i]).__name__}.")
        prediction_type_channel_dim_was_provided = prediction_type.channel_dim != "tl_default_value"
        if not prediction_type_channel_dim_was_provided:
            prediction_types[i].channel_dim = -1
            if not _call_from_tl_platform:
                store_warning_by_param(
                    param_name=f"prediction_types[{i}].channel_dim",
                    user_func_name="tensorleap_load_model",
                    default_value=prediction_types[i].channel_dim,
                    link_to_docs="https://docs.tensorleap.ai/tensorleap-integration/integration-test#tensorleap_load_model"
                )
        leap_binder.add_prediction(prediction_type.name, prediction_type.labels, prediction_type.channel_dim, i)

    def _validate_result(result) -> None:
        valid_types = ["onnxruntime", "keras"]
        err_message = f"tensorleap_load_model validation failed:\nSupported models are Keras and onnxruntime only and non of them was returned."
        validate_output_structure(result, func_name="tensorleap_load_model",
                                  expected_type_name=[" | ".join(t for t in valid_types)][0])
        try:
            import keras
        except ImportError:
            keras = None
        try:
            import tensorflow as tf
        except ImportError:
            tf = None
        try:
            import onnxruntime
        except ImportError:
            onnxruntime = None

        if not keras and not onnxruntime:
            raise AssertionError(err_message)

        is_keras_model = (
                bool(keras and isinstance(result, getattr(keras, "Model", tuple())))
                or bool(tf and isinstance(result, getattr(tf.keras, "Model", tuple())))
        )
        is_onnx_model = bool(onnxruntime and isinstance(result, onnxruntime.InferenceSession))

        if not any([is_keras_model, is_onnx_model]):
            raise AssertionError(err_message)

    def decorating_function(load_model_func, prediction_types=prediction_types):
        class TempMapping:
            pass

        @lru_cache()
        def inner(*args, **kwargs):
            if not _call_from_tl_platform:
                set_current('tensorleap_load_model')
            validate_args_structure(*args, types_order=[],
                                    func_name='tensorleap_load_model', expected_names=[], **kwargs)

            class ModelPlaceholder:
                def __init__(self, prediction_types):
                    self.model = load_model_func()  # TODO- check why this fails on onnx model
                    self.prediction_types = prediction_types
                    _validate_result(self.model)

                # keras interface
                def __call__(self, arg):
                    ret = self.model(arg)
                    self.validate_declared_prediction_types(ret)
                    if isinstance(ret, list):
                        return [r.numpy() for r in ret]
                    return ret.numpy()

                def validate_declared_prediction_types(self, ret):
                    if not (len(self.prediction_types) == len(ret) if isinstance(ret, list) else 1) and len(
                            self.prediction_types) != 0:
                        if not _call_from_tl_platform:
                            update_env_params_func("tensorleap_load_model", "x")
                        raise Exception(
                            f"tensorleap_load_model validation failed: number of declared prediction types({len(prediction_types)}) != number of model outputs({len(ret) if isinstance(ret, list) else 1})")

                def _convert_onnx_inputs_to_correct_type(
                        self, float_arrays_inputs: Dict[str, np.ndarray]
                ) -> Dict[str, np.ndarray]:
                    ONNX_TYPE_TO_NP = {
                        "tensor(float)": np.float32,
                        "tensor(double)": np.float64,
                        "tensor(int64)": np.int64,
                        "tensor(int32)": np.int32,
                        "tensor(int16)": np.int16,
                        "tensor(int8)": np.int8,
                        "tensor(uint64)": np.uint64,
                        "tensor(uint32)": np.uint32,
                        "tensor(uint16)": np.uint16,
                        "tensor(uint8)": np.uint8,
                        "tensor(bool)": np.bool_,
                    }

                    """
                    Cast user-provided NumPy inputs to match the dtypes/shapes
                    expected by an ONNX Runtime InferenceSession.
                    """
                    coerced = {}
                    meta = {i.name: i for i in self.model.get_inputs()}

                    for name, arr in float_arrays_inputs.items():
                        if name not in meta:
                            # Keep as-is unless extra inputs are disallowed
                            coerced[name] = arr
                            continue

                        info = meta[name]
                        onnx_type = info.type
                        want_dtype = ONNX_TYPE_TO_NP.get(onnx_type)

                        if want_dtype is None:
                            raise TypeError(f"Unsupported ONNX input type: {onnx_type}")

                        # Cast dtype if needed
                        if arr.dtype != want_dtype:
                            arr = arr.astype(want_dtype, copy=False)

                        coerced[name] = arr

                    # Verify required inputs are present
                    missing = [n for n in meta if n not in coerced]
                    if missing:
                        raise KeyError(f"Missing required input(s): {sorted(missing)}")

                    return coerced

                # onnx runtime interface
                def run(self, output_names, input_dict):
                    corrected_type_inputs = self._convert_onnx_inputs_to_correct_type(input_dict)
                    ret = self.model.run(output_names, corrected_type_inputs)
                    self.validate_declared_prediction_types(ret)
                    return ret

                def get_inputs(self):
                    return self.model.get_inputs()

            model_placeholder = ModelPlaceholder(prediction_types)
            if not _call_from_tl_platform:
                update_env_params_func("tensorleap_load_model", "v")
            return model_placeholder

        def mapping_inner():
            class ModelOutputPlaceholder:
                def __init__(self):
                    self.node_mapping = NodeMapping('', NodeMappingType.Prediction0)

                def __getitem__(self, key):
                    assert isinstance(key, int), \
                        f'Expected key to be an int, got {type(key)} instead.'

                    ret = TempMapping()
                    try:
                        ret.node_mapping = NodeMapping('', NodeMappingType(f'Prediction{str(key)}'))
                    except ValueError as e:
                        raise Exception(f'Tensorleap currently supports models with no more then 10 active predictions,'
                                        f' {key} not supported.')
                    return ret

            class ModelPlaceholder:

                # keras interface
                def __call__(self, arg):
                    if isinstance(arg, list):
                        for i, elem in enumerate(arg):
                            elem.node_mapping.type = _safe_get_item(i)
                    else:
                        arg.node_mapping.type = NodeMappingType.Input0

                    return ModelOutputPlaceholder()

                # onnx runtime interface
                def run(self, output_names, input_dict):
                    assert output_names is None
                    assert isinstance(input_dict, dict), \
                        f'Expected input_dict to be a dict, got {type(input_dict)} instead.'
                    for i, (input_key, elem) in enumerate(input_dict.items()):
                        if isinstance(input_key, NodeMappingType):
                            elem.node_mapping.type = input_key
                        else:
                            elem.node_mapping.type = _safe_get_item(i)

                    return ModelOutputPlaceholder()

                def get_inputs(self):
                    class FollowIndex:
                        def __init__(self, index):
                            self.name = _safe_get_item(index)

                    class FollowInputIndex:
                        def __init__(self):
                            pass

                        def __getitem__(self, index):
                            assert isinstance(index, int), \
                                f'Expected key to be an int, got {type(index)} instead.'

                            return FollowIndex(index)

                    return FollowInputIndex()

            return ModelPlaceholder()

        def final_inner(*args, **kwargs):
            if os.environ.get(mapping_runtime_mode_env_var_mame):
                return mapping_inner()
            else:
                return inner(*args, **kwargs)

        return final_inner

    return decorating_function


def tensorleap_custom_metric(name: str,
                             direction: Union[MetricDirection, Dict[str, MetricDirection]] = _UNSET,
                             compute_insights: Optional[Union[bool, Dict[str, bool]]] = None,
                             connects_to=None):
    name_to_unique_name = defaultdict(set)

    def decorating_function(
            user_function: Union[CustomCallableInterfaceMultiArgs, CustomMultipleReturnCallableInterfaceMultiArgs,
            ConfusionMatrixCallableInterfaceMultiArgs]):
        nonlocal direction

        direction_was_provided = direction is not _UNSET

        if not direction_was_provided:
            direction = MetricDirection.Downward
            if not _call_from_tl_platform:
                store_warning_by_param(
                    param_name="direction",
                    user_func_name=user_function.__name__,
                    default_value=direction,
                    link_to_docs="https://docs.tensorleap.ai/tensorleap-integration/writing-integration-code/custom-metrics"

                )

        def _validate_decorators_signature():
            err_message = f"{user_function.__name__} validation failed.\n"
            if not isinstance(name, str):
                raise TypeError(err_message + f"`name` must be a string, got type {type(name).__name__}.")
            valid_directions = {MetricDirection.Upward, MetricDirection.Downward}
            if isinstance(direction, MetricDirection):
                if direction not in valid_directions:
                    raise ValueError(
                        err_message +
                        f"Invalid MetricDirection: {direction}. Must be one of {valid_directions}, "
                        f"got type {type(direction).__name__}."
                    )
            elif isinstance(direction, dict):
                if not all(isinstance(k, str) for k in direction.keys()):
                    invalid_keys = {k: type(k).__name__ for k in direction.keys() if not isinstance(k, str)}
                    raise TypeError(
                        err_message +
                        f"All keys in `direction` must be strings, got invalid key types: {invalid_keys}."
                    )
                for k, v in direction.items():
                    if v not in valid_directions:
                        raise ValueError(
                            err_message +
                            f"Invalid direction for key '{k}': {v}. Must be one of {valid_directions}, "
                            f"got type {type(v).__name__}."
                        )
            else:
                raise TypeError(
                    err_message +
                    f"`direction` must be a MetricDirection or a Dict[str, MetricDirection], "
                    f"got type {type(direction).__name__}."
                )
            if compute_insights is not None:
                if not isinstance(compute_insights, (bool, dict)):
                    raise TypeError(
                        err_message +
                        f"`compute_insights` must be a bool or a Dict[str, bool], "
                        f"got type {type(compute_insights).__name__}."
                    )
                if isinstance(compute_insights, dict):
                    if not all(isinstance(k, str) for k in compute_insights.keys()):
                        invalid_keys = {k: type(k).__name__ for k in compute_insights.keys() if not isinstance(k, str)}
                        raise TypeError(
                            err_message +
                            f"All keys in `compute_insights` must be strings, got invalid key types: {invalid_keys}."
                        )
                    for k, v in compute_insights.items():
                        if not isinstance(v, bool):
                            raise TypeError(
                                err_message +
                                f"Invalid type for compute_insights['{k}']: expected bool, got type {type(v).__name__}."
                            )
            if connects_to is not None:
                valid_types = (str, list, tuple, set)
                if not isinstance(connects_to, valid_types):
                    raise TypeError(
                        err_message +
                        f"`connects_to` must be one of {valid_types}, got type {type(connects_to).__name__}."
                    )
                if isinstance(connects_to, (list, tuple, set)):
                    invalid_elems = [f"{type(e).__name__}" for e in connects_to if not isinstance(e, str)]
                    if invalid_elems:
                        raise TypeError(
                            err_message +
                            f"All elements in `connects_to` must be strings, "
                            f"but found element types: {invalid_elems}."
                        )

        _validate_decorators_signature()

        for metric_handler in leap_binder.setup_container.metrics:
            if metric_handler.metric_handler_data.name == name:
                raise Exception(f'Metric with name {name} already exists. '
                                f'Please choose another')

        def _validate_input_args(*args, **kwargs) -> None:
            assert len(args) + len(kwargs) > 0, (
                f"{user_function.__name__}() validation failed: "
                f"Expected at least one positional|key-word argument of type np.ndarray, "
                f"but received none. "
                f"Correct usage example: tensorleap_custom_metric(input_array: np.ndarray, ...)"
            )
            for i, arg in enumerate(args):
                assert isinstance(arg, (np.ndarray, SamplePreprocessResponse)), (
                    f'{user_function.__name__}() validation failed: '
                    f'Argument #{i} should be a numpy array. Got {type(arg)}.')
                if leap_binder.batch_size_to_validate and isinstance(arg, np.ndarray):
                    assert arg.shape[0] == leap_binder.batch_size_to_validate, \
                        (f'{user_function.__name__}() validation failed: Argument #{i} '
                         f'first dim should be as the batch size. Got {arg.shape[0]} '
                         f'instead of {leap_binder.batch_size_to_validate}')

            for _arg_name, arg in kwargs.items():
                assert isinstance(arg, (np.ndarray, SamplePreprocessResponse)), (
                    f'{user_function.__name__}() validation failed: '
                    f'Argument {_arg_name} should be a numpy array. Got {type(arg)}.')
                if leap_binder.batch_size_to_validate and isinstance(arg, np.ndarray):
                    assert arg.shape[0] == leap_binder.batch_size_to_validate, \
                        (f'{user_function.__name__}() validation failed: Argument {_arg_name} '
                         f'first dim should be as the batch size. Got {arg.shape[0]} '
                         f'instead of {leap_binder.batch_size_to_validate}')

        def _validate_result(result) -> None:
            validate_output_structure(result, func_name=user_function.__name__,
                                      expected_type_name="List[float | int | None | List[ConfusionMatrixElement] ]  | NDArray[np.float32]  or dictonary with one of these types as its values types")
            supported_types_message = (f'{user_function.__name__}() validation failed: '
                                       f'{user_function.__name__}() has returned unsupported type.\nSupported types are List[float|int|None], '
                                       f'List[List[ConfusionMatrixElement]], NDArray[np.float32] or dictonary with one of these types as its values types. ')

            def _validate_single_metric(single_metric_result, key=None):
                if isinstance(single_metric_result, list):
                    if isinstance(single_metric_result[0], list):
                        assert all(isinstance(cm, ConfusionMatrixElement) for cm in single_metric_result[0]), (
                            f"{supported_types_message} "
                            f"Got {'a dict where the value of ' + str(key) + ' is of type ' if key is not None else ''}"
                            f"List[List[{', '.join(type(cm).__name__ for cm in single_metric_result[0])}]]."
                        )

                    else:
                        assert all(isinstance(v, (float, int, type(None), np.float32)) for v in single_metric_result), (
                            f"{supported_types_message}\n"
                            f"Got {'a dict where the value of ' + str(key) + ' is of type ' if key is not None else ''}"
                            f"List[{', '.join(type(v).__name__ for v in single_metric_result)}]."
                        )
                else:
                    assert isinstance(single_metric_result,
                                      np.ndarray), f'{supported_types_message}\nGot {type(single_metric_result)}.'
                    assert len(single_metric_result.shape) == 1, (f'{user_function.__name__}() validation failed: '
                                                                  f'The return shape should be 1D. Got {len(single_metric_result.shape)}D.')

                if leap_binder.batch_size_to_validate:
                    assert len(single_metric_result) == leap_binder.batch_size_to_validate, \
                        f'{user_function.__name__}() validation failed: The return len {f"of srt{key} value" if key is not None else ""} should be as the batch size.'

            if isinstance(result, dict):
                for key, value in result.items():
                    _validate_single_metric(value, key)

                    assert isinstance(key, str), \
                        (f'{user_function.__name__}() validation failed: '
                         f'Keys in the return dict should be of type str. Got {type(key)}.')
                    _validate_single_metric(value)

                if isinstance(direction, dict):
                    for direction_key in direction:
                        assert direction_key in result, \
                            (f'{user_function.__name__}() validation failed: '
                             f'Keys in the direction mapping should be part of result keys. Got key {direction_key}.')

                if compute_insights is not None:
                    assert isinstance(compute_insights, dict), \
                        (f'{user_function.__name__}() validation failed: '
                         f'compute_insights should be dict if using the dict results. Got {type(compute_insights)}.')

                    for ci_key in compute_insights:
                        assert ci_key in result, \
                            (f'{user_function.__name__}() validation failed: '
                             f'Keys in the compute_insights mapping should be part of result keys. Got key {ci_key}.')

            else:
                _validate_single_metric(result)

                if compute_insights is not None:
                    assert isinstance(compute_insights, bool), \
                        (f'{user_function.__name__}() validation failed: '
                         f'compute_insights should be boolean. Got {type(compute_insights)}.')

        @functools.wraps(user_function)
        def inner_without_validate(*args, **kwargs):
            global _called_from_inside_tl_decorator
            _called_from_inside_tl_decorator += 1

            try:
                result = user_function(*args, **kwargs)
            finally:
                _called_from_inside_tl_decorator -= 1

            return result

        try:
            inner_without_validate.__signature__ = inspect.signature(user_function)
        except (TypeError, ValueError):
            pass

        leap_binder.add_custom_metric(inner_without_validate, name, direction, compute_insights)

        if connects_to is not None:
            arg_names = leap_binder.setup_container.metrics[-1].metric_handler_data.arg_names
            _add_mapping_connections(connects_to, arg_names, NodeMappingType.Metric, name)

        def inner(*args, **kwargs):
            if not _call_from_tl_platform:
                set_current('tensorleap_custom_metric')
            _validate_input_args(*args, **kwargs)

            result = inner_without_validate(*args, **kwargs)

            _validate_result(result)
            if not _call_from_tl_platform:
                update_env_params_func("tensorleap_custom_metric", "v")
            return result

        def mapping_inner(*args, **kwargs):
            user_unique_name = mapping_inner.name
            if 'user_unique_name' in kwargs:
                user_unique_name = kwargs['user_unique_name']

            ordered_connections = [kwargs[n] for n in mapping_inner.arg_names if n in kwargs]
            ordered_connections = list(args) + ordered_connections

            if user_unique_name in name_to_unique_name[mapping_inner.name]:
                user_unique_name = f'{user_unique_name}_{len(name_to_unique_name[mapping_inner.name])}'
            name_to_unique_name[mapping_inner.name].add(user_unique_name)

            _add_mapping_connection(user_unique_name, ordered_connections, mapping_inner.arg_names,
                                    mapping_inner.name, NodeMappingType.Metric)

            return None

        mapping_inner.arg_names = leap_binder.setup_container.metrics[-1].metric_handler_data.arg_names
        mapping_inner.name = name

        def final_inner(*args, **kwargs):
            if os.environ.get(mapping_runtime_mode_env_var_mame):
                return mapping_inner(*args, **kwargs)
            else:
                return inner(*args, **kwargs)

        return final_inner

    return decorating_function


def tensorleap_custom_visualizer(name: str, visualizer_type: LeapDataType,
                                 heatmap_function: Optional[Callable[..., npt.NDArray[np.float32]]] = None,
                                 connects_to=None):
    name_to_unique_name = defaultdict(set)

    def decorating_function(user_function: VisualizerCallableInterface):
        assert isinstance(visualizer_type, LeapDataType), (f"{user_function.__name__} validation failed: "
                                                           f"visualizer_type should be of type {LeapDataType.__name__} but got {type(visualizer_type)}"
                                                           )
        for viz_handler in leap_binder.setup_container.visualizers:
            if viz_handler.visualizer_handler_data.name == name:
                raise Exception(f'Visualizer with name {name} already exists. '
                                f'Please choose another')

        def _validate_input_args(*args, **kwargs):
            assert len(args) + len(kwargs) > 0, (
                f"{user_function.__name__}() validation failed: "
                f"Expected at least one positional|key-word argument of type np.ndarray, "
                f"but received none. "
                f"Correct usage example: {user_function.__name__}(input_array: np.ndarray, ...)"
            )
            for i, arg in enumerate(args):
                assert isinstance(arg, (np.ndarray, SamplePreprocessResponse)), (
                    f'{user_function.__name__}() validation failed: '
                    f'Argument #{i} should be a numpy array. Got {type(arg)}.')
                if leap_binder.batch_size_to_validate and isinstance(arg, np.ndarray):
                    assert arg.shape[0] != leap_binder.batch_size_to_validate, \
                        (f'{user_function.__name__}() validation failed: '
                         f'Argument #{i} should be without batch dimension. ')

            for _arg_name, arg in kwargs.items():
                assert isinstance(arg, (np.ndarray, SamplePreprocessResponse)), (
                    f'{user_function.__name__}() validation failed: '
                    f'Argument {_arg_name} should be a numpy array. Got {type(arg)}.')
                if leap_binder.batch_size_to_validate and isinstance(arg, np.ndarray):
                    assert arg.shape[0] != leap_binder.batch_size_to_validate, \
                        (f'{user_function.__name__}() validation failed: Argument {_arg_name} '
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
            validate_output_structure(result, func_name=user_function.__name__,
                                      expected_type_name=result_type_map[visualizer_type])

            assert isinstance(result, result_type_map[visualizer_type]), \
                (f'{user_function.__name__}() validation failed: '
                 f'The return type should be {result_type_map[visualizer_type]}. Got {type(result)}.')

        @functools.wraps(user_function)
        def inner_without_validate(*args, **kwargs):
            global _called_from_inside_tl_decorator
            _called_from_inside_tl_decorator += 1

            try:
                result = user_function(*args, **kwargs)
            finally:
                _called_from_inside_tl_decorator -= 1

            return result

        try:
            inner_without_validate.__signature__ = inspect.signature(user_function)
        except (TypeError, ValueError):
            pass

        leap_binder.set_visualizer(inner_without_validate, name, visualizer_type, heatmap_function)

        if connects_to is not None:
            arg_names = leap_binder.setup_container.visualizers[-1].visualizer_handler_data.arg_names
            _add_mapping_connections(connects_to, arg_names, NodeMappingType.Visualizer, name)

        def inner(*args, **kwargs):
            if not _call_from_tl_platform:
                set_current('tensorleap_custom_visualizer')
            _validate_input_args(*args, **kwargs)

            result = inner_without_validate(*args, **kwargs)

            _validate_result(result)
            if not _call_from_tl_platform:
                update_env_params_func("tensorleap_custom_visualizer", "v")
            return result

        def mapping_inner(*args, **kwargs):
            user_unique_name = mapping_inner.name
            if 'user_unique_name' in kwargs:
                user_unique_name = kwargs['user_unique_name']

            if user_unique_name in name_to_unique_name[mapping_inner.name]:
                user_unique_name = f'{user_unique_name}_{len(name_to_unique_name[mapping_inner.name])}'
            name_to_unique_name[mapping_inner.name].add(user_unique_name)

            ordered_connections = [kwargs[n] for n in mapping_inner.arg_names if n in kwargs]
            ordered_connections = list(args) + ordered_connections
            _add_mapping_connection(user_unique_name, ordered_connections, mapping_inner.arg_names,
                                    mapping_inner.name, NodeMappingType.Visualizer)

            return None

        mapping_inner.arg_names = leap_binder.setup_container.visualizers[-1].visualizer_handler_data.arg_names
        mapping_inner.name = name

        def final_inner(*args, **kwargs):
            if os.environ.get(mapping_runtime_mode_env_var_mame):
                return mapping_inner(*args, **kwargs)
            else:
                return inner(*args, **kwargs)

        return final_inner

    return decorating_function


def tensorleap_metadata(
        name: str, metadata_type: Optional[Union[DatasetMetadataType, Dict[str, DatasetMetadataType]]] = None):
    def decorating_function(user_function: MetadataSectionCallableInterface):
        for metadata_handler in leap_binder.setup_container.metadata:
            if metadata_handler.name == name:
                raise Exception(f'Metadata with name {name} already exists. '
                                f'Please choose another')

        def _validate_input_args(sample_id: Union[int, str], preprocess_response: PreprocessResponse):
            assert type(sample_id) == preprocess_response.sample_id_type, \
                (f'{user_function.__name__}() validation failed: '
                 f'Argument sample_id should be as the same type as defined in the preprocess response '
                 f'{preprocess_response.sample_id_type}. Got {type(sample_id)}.')

        def _validate_result(result):
            supported_result_types = (type(None), int, str, bool, float, dict, np.floating,
                                      np.bool_, np.unsignedinteger, np.signedinteger, np.integer)
            validate_output_structure(result, func_name=user_function.__name__,
                                      expected_type_name=supported_result_types)
            assert isinstance(result, supported_result_types), \
                (f'{user_function.__name__}() validation failed: '
                 f'Unsupported return type. Got {type(result)}. should be any of {str(supported_result_types)}')
            if isinstance(result, dict):
                for key, value in result.items():
                    assert isinstance(key, str), \
                        (f'{user_function.__name__}() validation failed: '
                         f'Keys in the return dict should be of type str. Got {type(key)}.')
                    assert isinstance(value, supported_result_types), \
                        (f'{user_function.__name__}() validation failed: '
                         f'Values in the return dict should be of type {str(supported_result_types)}. Got {type(value)}.')

        def inner_without_validate(sample_id, preprocess_response):

            global _called_from_inside_tl_decorator
            _called_from_inside_tl_decorator += 1

            try:
                result = user_function(sample_id, preprocess_response)
            finally:
                _called_from_inside_tl_decorator -= 1

            return result

        leap_binder.set_metadata(inner_without_validate, name, metadata_type)

        def inner(*args, **kwargs):
            if not _call_from_tl_platform:
                set_current('tensorleap_metadata')
            if os.environ.get(mapping_runtime_mode_env_var_mame):
                return None
            validate_args_structure(*args, types_order=[Union[int, str], PreprocessResponse],
                                    func_name=user_function.__name__, expected_names=["idx", "preprocess"], **kwargs)
            sample_id, preprocess_response = args if len(args) != 0 else kwargs.values()
            _validate_input_args(sample_id, preprocess_response)

            result = inner_without_validate(sample_id, preprocess_response)

            _validate_result(result)
            if not _call_from_tl_platform:
                update_env_params_func("tensorleap_metadata", "v")
            return result

        return inner

    return decorating_function


def tensorleap_custom_latent_space():
    def decorating_function(user_function: SectionCallableInterface):
        def _validate_input_args(sample_id: Union[int, str], preprocess_response: PreprocessResponse):
            assert isinstance(sample_id, (int, str)), \
                (f'tensorleap_custom_latent_space validation failed: '
                 f'Argument sample_id should be either int or str. Got {type(sample_id)}.')
            assert isinstance(preprocess_response, PreprocessResponse), \
                (f'tensorleap_custom_latent_space validation failed: '
                 f'Argument preprocess_response should be a PreprocessResponse. Got {type(preprocess_response)}.')
            assert type(sample_id) == preprocess_response.sample_id_type, \
                (f'tensorleap_custom_latent_space validation failed: '
                 f'Argument sample_id should be as the same type as defined in the preprocess response '
                 f'{preprocess_response.sample_id_type}. Got {type(sample_id)}.')

        def _validate_result(result):
            assert isinstance(result, np.ndarray), \
                (f'tensorleap_custom_loss validation failed: '
                 f'The return type should be a numpy array. Got {type(result)}.')

        def inner_without_validate(sample_id, preprocess_response):
            global _called_from_inside_tl_decorator
            _called_from_inside_tl_decorator += 1

            try:
                result = user_function(sample_id, preprocess_response)
            finally:
                _called_from_inside_tl_decorator -= 1

            return result

        leap_binder.set_custom_latent_space(inner_without_validate)

        def inner(sample_id, preprocess_response):
            if os.environ.get(mapping_runtime_mode_env_var_mame):
                return None

            _validate_input_args(sample_id, preprocess_response)

            result = inner_without_validate(sample_id, preprocess_response)

            _validate_result(result)
            return result

        return inner

    return decorating_function


def tensorleap_preprocess():
    def decorating_function(user_function: Callable[[], List[PreprocessResponse]]):
        leap_binder.set_preprocess(user_function)

        def _validate_input_args(*args, **kwargs):
            assert len(args) + len(kwargs) == 0, \
                (f'{user_function.__name__}() validation failed: '
                 f'The function should not take any arguments. Got {args} and {kwargs}.')

        def _validate_result(result):
            assert isinstance(result, list), (
                f"{user_function.__name__}() validation failed: expected return type list[{PreprocessResponse.__name__}]"
                f"(e.g., [PreprocessResponse1, PreprocessResponse2, ...]), but returned type is {type(result).__name__}."
                if not isinstance(result, tuple)
                else f"{user_function.__name__}() validation failed: expected to return a single list[{PreprocessResponse.__name__}] object, "
                     f"but returned {len(result)} objects instead."
            )
            for i, response in enumerate(result):
                assert isinstance(response, PreprocessResponse), \
                    (f'{user_function.__name__}() validation failed: '
                     f'Element #{i} in the return list should be a PreprocessResponse. Got {type(response)}.')
            assert len(set(result)) == len(result), \
                (f'{user_function.__name__}() validation failed: '
                 f'The return list should not contain duplicate PreprocessResponse objects.')

        def inner(*args, **kwargs):
            if not _call_from_tl_platform:
                set_current('tensorleap_metadata')
            if os.environ.get(mapping_runtime_mode_env_var_mame):
                return [None, None, None, None]

            _validate_input_args(*args, **kwargs)
            result = user_function()
            _validate_result(result)

            # Emit integration test event once per test
            try:
                emit_integration_event_once(AnalyticsEvent.PREPROCESS_INTEGRATION_TEST, {
                    'preprocess_responses_count': len(result)
                })
            except Exception as e:
                logger.debug(f"Failed to emit preprocess integration test event: {e}")
            if not _call_from_tl_platform:
                update_env_params_func("tensorleap_preprocess", "v")
            return result

        return inner

    return decorating_function


def tensorleap_element_instance_preprocess(
        instance_length_encoder: InstanceLengthCallableInterface, instance_mask_encoder: InstanceCallableInterface):
    def decorating_function(user_function: Callable[[], List[PreprocessResponse]]):
        def user_function_instance() -> List[PreprocessResponse]:
            result = user_function()
            found_instance_metadata = False
            for preprocess_response in result:
                sample_ids_to_instance_mappings = {}
                instance_to_sample_ids_mappings = {}
                all_sample_ids = preprocess_response.sample_ids.copy()
                for sample_id in preprocess_response.sample_ids:
                    instances_length = instance_length_encoder(sample_id, preprocess_response)
                    instances_ids = [f'{sample_id}_{instance_id}' for instance_id in range(instances_length)]
                    sample_ids_to_instance_mappings[sample_id] = instances_ids
                    instance_to_sample_ids_mappings[sample_id] = sample_id
                    for idx, instance_id in enumerate(instances_ids):
                        if not found_instance_metadata:
                            element_instance = instance_mask_encoder(sample_id, preprocess_response, idx)
                            element_instance_metadata = element_instance.instance_metadata
                            if element_instance_metadata is not None:
                                element_instance_metadata_types = map_dict_to_metadata_types(element_instance_metadata)
                                def builtin_instance_extra_metadata(idx: str, preprocess: PreprocessResponse) -> Dict[str, str]:
                                    for k, v in element_instance_metadata.items():
                                        element_instance_metadata[k] = None
                                    return element_instance_metadata
                                leap_binder.set_metadata(builtin_instance_extra_metadata,"builtin_instance_extra_metadata", element_instance_metadata_types)
                            found_instance_metadata = True

                        instance_to_sample_ids_mappings[instance_id] = sample_id
                    all_sample_ids.extend(instances_ids)
                preprocess_response.length = len(all_sample_ids)
                preprocess_response.sample_ids_to_instance_mappings = sample_ids_to_instance_mappings
                preprocess_response.instance_to_sample_ids_mappings = instance_to_sample_ids_mappings
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
            if os.environ.get(mapping_runtime_mode_env_var_mame):
                return [None, None, None, None]

            _validate_input_args(*args, **kwargs)

            result = user_function_instance()
            _validate_result(result)
            if not _call_from_tl_platform:
                update_env_params_func("tensorleap_preprocess", "v")
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
        def _validate_input_args(sample_id: str, preprocess_response: PreprocessResponse, instance_id: int):
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
            assert isinstance(instance_id, int), \
                (f'tensorleap_instances_masks_encoder validation failed: '
                 f'Argument instance_id should be int. Got {type(instance_id)}.')

        def _validate_result(result):
            assert isinstance(result, ElementInstance) or (result is None), \
                (f'tensorleap_instances_masks_encoder validation failed: '
                 f'Unsupported return type. Should be a ElementInstance or None. Got {type(result)}.')

        def inner_without_validate(sample_id, preprocess_response, instance_id):
            global _called_from_inside_tl_decorator
            _called_from_inside_tl_decorator += 1

            try:
                result = user_function(sample_id, preprocess_response, instance_id)
            finally:
                _called_from_inside_tl_decorator -= 1

            return result

        leap_binder.set_instance_masks(inner_without_validate, name)

        def inner(sample_id, preprocess_response, instance_id):
            if os.environ.get(mapping_runtime_mode_env_var_mame):
                return None

            _validate_input_args(sample_id, preprocess_response, instance_id)

            result = inner_without_validate(sample_id, preprocess_response, instance_id)

            _validate_result(result)
            return result

        return inner

    return decorating_function


def tensorleap_instances_length_encoder(name: str):
    def decorating_function(user_function: InstanceLengthCallableInterface):
        def _validate_input_args(sample_id: str, preprocess_response: PreprocessResponse):
            assert isinstance(sample_id, (str, int)), \
                (f'tensorleap_instances_length_encoder validation failed: '
                 f'Argument sample_id should be str. Got {type(sample_id)}.')
            assert isinstance(preprocess_response, PreprocessResponse), \
                (f'tensorleap_instances_length_encoder validation failed: '
                 f'Argument preprocess_response should be a PreprocessResponse. Got {type(preprocess_response)}.')
            assert type(sample_id) == preprocess_response.sample_id_type, \
                (f'tensorleap_instances_length_encoder validation failed: '
                 f'Argument sample_id should be as the same type as defined in the preprocess response '
                 f'{preprocess_response.sample_id_type}. Got {type(sample_id)}.')

        def _validate_result(result):
            assert isinstance(result, int), \
                (f'tensorleap_instances_length_encoder validation failed: '
                 f'Unsupported return type. Should be a int. Got {type(result)}.')

        def inner_without_validate(sample_id, preprocess_response):
            global _called_from_inside_tl_decorator
            _called_from_inside_tl_decorator += 1

            try:
                result = user_function(sample_id, preprocess_response)
            finally:
                _called_from_inside_tl_decorator -= 1

            return result

        def inner(sample_id, preprocess_response):
            if os.environ.get(mapping_runtime_mode_env_var_mame):
                return None

            _validate_input_args(sample_id, preprocess_response)

            result = inner_without_validate(sample_id, preprocess_response)

            _validate_result(result)
            return result

        return inner

    return decorating_function


def tensorleap_input_encoder(name: str, channel_dim=_UNSET, model_input_index=None):
    def decorating_function(user_function: SectionCallableInterface):
        for input_handler in leap_binder.setup_container.inputs:
            if input_handler.name == name:
                raise Exception(f'Input with name {name} already exists. '
                                f'Please choose another')
        nonlocal channel_dim

        channel_dim_was_provided = channel_dim is not _UNSET

        if not channel_dim_was_provided:
            channel_dim = -1
            if not _call_from_tl_platform:
                store_warning_by_param(
                    param_name="channel_dim",
                    user_func_name=user_function.__name__,
                    default_value=channel_dim,
                    link_to_docs="https://docs.tensorleap.ai/tensorleap-integration/writing-integration-code/input-encoder"

                )

        if channel_dim <= 0 and channel_dim != -1:
            raise Exception(f"Channel dim for input {name} is expected to be either -1 or positive")

        def _validate_input_args(sample_id: Union[int, str], preprocess_response: PreprocessResponse):
            assert type(sample_id) == preprocess_response.sample_id_type, \
                (f'{user_function.__name__}() validation failed: '
                 f'Argument sample_id should be as the same type as defined in the preprocess response '
                 f'{preprocess_response.sample_id_type}. Got {type(sample_id)}.')

        def _validate_result(result):
            validate_output_structure(result, func_name=user_function.__name__, expected_type_name="np.ndarray")
            assert isinstance(result, np.ndarray), \
                (f'{user_function.__name__}() validation failed: '
                 f'Unsupported return type. Should be a numpy array. Got {type(result)}.')
            assert result.dtype == np.float32, \
                (f'{user_function.__name__}() validation failed: '
                 f'The return type should be a numpy array of type float32. Got {result.dtype}.')
            assert channel_dim - 1 <= len(result.shape), (f'{user_function.__name__}() validation failed: '
                                                          f'The channel_dim ({channel_dim}) should be <= to the rank of the resulting input rank ({len(result.shape)}).')

        def inner_without_validate(sample_id, preprocess_response):
            global _called_from_inside_tl_decorator
            _called_from_inside_tl_decorator += 1

            try:
                result = user_function(sample_id, preprocess_response)
            finally:
                _called_from_inside_tl_decorator -= 1

            return result

        leap_binder.set_input(inner_without_validate, name, channel_dim=channel_dim)

        def inner(*args, **kwargs):
            if not _call_from_tl_platform:
                set_current("tensorleap_input_encoder")
            validate_args_structure(*args, types_order=[Union[int, str], PreprocessResponse],
                                    func_name=user_function.__name__, expected_names=["idx", "preprocess"], **kwargs)
            sample_id, preprocess_response = args if len(args) != 0 else kwargs.values()
            _validate_input_args(sample_id, preprocess_response)

            result = inner_without_validate(sample_id, preprocess_response)

            _validate_result(result)

            if _called_from_inside_tl_decorator == 0 and _called_from_inside_tl_integration_test_decorator:
                batch_warning(result, user_function.__name__)
                result = np.expand_dims(result, axis=0)
                # Emit integration test event once per test
                try:
                    emit_integration_event_once(AnalyticsEvent.INPUT_ENCODER_INTEGRATION_TEST, {
                        'encoder_name': name,
                        'channel_dim': channel_dim,
                        'model_input_index': model_input_index
                    })
                except Exception as e:
                    logger.debug(f"Failed to emit input_encoder integration test event: {e}")
            if not _call_from_tl_platform:
                update_env_params_func("tensorleap_input_encoder", "v")

            return result

        node_mapping_type = NodeMappingType.Input
        if model_input_index is not None:
            node_mapping_type = NodeMappingType(f'Input{str(model_input_index)}')
        inner.node_mapping = NodeMapping(name, node_mapping_type)

        def mapping_inner(*args, **kwargs):
            class TempMapping:
                pass

            ret = TempMapping()
            ret.node_mapping = mapping_inner.node_mapping

            leap_binder.mapping_connections.append(NodeConnection(mapping_inner.node_mapping, None))
            return ret

        mapping_inner.node_mapping = NodeMapping(name, node_mapping_type)

        def final_inner(*args, **kwargs):
            if os.environ.get(mapping_runtime_mode_env_var_mame):
                return mapping_inner(*args, **kwargs)
            else:
                return inner(*args, **kwargs)

        final_inner.node_mapping = NodeMapping(name, node_mapping_type)

        return final_inner

    return decorating_function


def tensorleap_gt_encoder(name: str):
    def decorating_function(user_function: SectionCallableInterface):
        for gt_handler in leap_binder.setup_container.ground_truths:
            if gt_handler.name == name:
                raise Exception(f'GT with name {name} already exists. '
                                f'Please choose another')

        def _validate_input_args(sample_id: Union[int, str], preprocess_response: PreprocessResponse):
            assert type(sample_id) == preprocess_response.sample_id_type, \
                (f'{user_function.__name__}() validation failed: '
                 f'Argument sample_id should be as the same type as defined in the preprocess response '
                 f'{preprocess_response.sample_id_type}. Got {type(sample_id)}.')

        def _validate_result(result):
            validate_output_structure(result, func_name=user_function.__name__, expected_type_name="np.ndarray",
                                      gt_flag=True)
            assert isinstance(result, np.ndarray), \
                (f'{user_function.__name__}() validation failed: '
                 f'Unsupported return type. Should be a numpy array. Got {type(result)}.')
            assert result.dtype == np.float32, \
                (f'{user_function.__name__}() validation failed: '
                 f'The return type should be a numpy array of type float32. Got {result.dtype}.')

        def inner_without_validate(sample_id, preprocess_response):
            global _called_from_inside_tl_decorator
            _called_from_inside_tl_decorator += 1

            try:
                result = user_function(sample_id, preprocess_response)
            finally:
                _called_from_inside_tl_decorator -= 1

            return result

        leap_binder.set_ground_truth(inner_without_validate, name)

        def inner(*args, **kwargs):
            if not _call_from_tl_platform:
                set_current("tensorleap_gt_encoder")
            validate_args_structure(*args, types_order=[Union[int, str], PreprocessResponse],
                                    func_name=user_function.__name__, expected_names=["idx", "preprocess"], **kwargs)
            sample_id, preprocess_response = args
            _validate_input_args(sample_id, preprocess_response)

            result = inner_without_validate(sample_id, preprocess_response)

            _validate_result(result)

            if _called_from_inside_tl_decorator == 0 and _called_from_inside_tl_integration_test_decorator:
                batch_warning(result, user_function.__name__)
                result = np.expand_dims(result, axis=0)
                # Emit integration test event once per test
                try:
                    emit_integration_event_once(AnalyticsEvent.GT_ENCODER_INTEGRATION_TEST, {
                        'encoder_name': name
                    })
                except Exception as e:
                    logger.debug(f"Failed to emit gt_encoder integration test event: {e}")
            if not _call_from_tl_platform:
                update_env_params_func("tensorleap_gt_encoder", "v")
            return result

        inner.node_mapping = NodeMapping(name, NodeMappingType.GroundTruth)

        def mapping_inner(*args, **kwargs):
            class TempMapping:
                pass

            ret = TempMapping()
            ret.node_mapping = mapping_inner.node_mapping

            return ret

        mapping_inner.node_mapping = NodeMapping(name, NodeMappingType.GroundTruth)

        def final_inner(*args, **kwargs):
            if os.environ.get(mapping_runtime_mode_env_var_mame):
                return mapping_inner(*args, **kwargs)
            else:
                return inner(*args, **kwargs)

        final_inner.node_mapping = NodeMapping(name, NodeMappingType.GroundTruth)

        return final_inner

    return decorating_function


def tensorleap_custom_loss(name: str, connects_to=None):
    name_to_unique_name = defaultdict(set)

    def decorating_function(user_function: CustomCallableInterface):
        for loss_handler in leap_binder.setup_container.custom_loss_handlers:
            if loss_handler.custom_loss_handler_data.name == name:
                raise Exception(f'Custom loss with name {name} already exists. '
                                f'Please choose another')

        valid_types = (np.ndarray, SamplePreprocessResponse)

        def _validate_input_args(*args, **kwargs):
            assert len(args) + len(kwargs) > 0, (
                f"{user_function.__name__}() validation failed: "
                f"Expected at least one positional|key-word argument of the allowed types (np.ndarray|SamplePreprocessResponse|). "
                f"but received none. "
                f"Correct usage example: {user_function.__name__}(input_array: np.ndarray, ...)"
            )
            for i, arg in enumerate(args):
                assert isinstance(arg, valid_types), (f'{user_function.__name__}() validation failed: '
                                                      f'Argument #{i} should be a numpy array. Got {type(arg)}.')
            for _arg_name, arg in kwargs.items():
                assert isinstance(arg, valid_types), (f'{user_function.__name__}() validation failed: '
                                                      f'Argument #{_arg_name} should be a numpy array. Got {type(arg)}.')

        def _validate_result(result):
            validate_output_structure(result, func_name=user_function.__name__,
                                      expected_type_name="np.ndarray")
            assert isinstance(result, np.ndarray), \
                (f'{user_function.__name__} validation failed: '
                 f'The return type should be a numpy array. Got {type(result)}.')
            assert result.ndim < 2, (f'{user_function.__name__}  validation failed: '
                                     f'The return type should be a 1Dim numpy array but got {result.ndim}Dim.')

        @functools.wraps(user_function)
        def inner_without_validate(*args, **kwargs):
            global _called_from_inside_tl_decorator
            _called_from_inside_tl_decorator += 1

            try:
                result = user_function(*args, **kwargs)
            finally:
                _called_from_inside_tl_decorator -= 1

            return result

        try:
            inner_without_validate.__signature__ = inspect.signature(user_function)
        except (TypeError, ValueError):
            pass

        leap_binder.add_custom_loss(inner_without_validate, name)

        if connects_to is not None:
            arg_names = leap_binder.setup_container.custom_loss_handlers[-1].custom_loss_handler_data.arg_names
            _add_mapping_connections(connects_to, arg_names, NodeMappingType.CustomLoss, name)

        def inner(*args, **kwargs):
            if not _call_from_tl_platform:
                set_current("tensorleap_custom_loss")
            _validate_input_args(*args, **kwargs)

            result = inner_without_validate(*args, **kwargs)

            _validate_result(result)
            if not _call_from_tl_platform:
                update_env_params_func("tensorleap_custom_loss", "v")

            return result

        def mapping_inner(*args, **kwargs):
            user_unique_name = mapping_inner.name
            if 'user_unique_name' in kwargs:
                user_unique_name = kwargs['user_unique_name']

            if user_unique_name in name_to_unique_name[mapping_inner.name]:
                user_unique_name = f'{user_unique_name}_{len(name_to_unique_name[mapping_inner.name])}'
            name_to_unique_name[mapping_inner.name].add(user_unique_name)

            ordered_connections = [kwargs[n] for n in mapping_inner.arg_names if n in kwargs]
            ordered_connections = list(args) + ordered_connections
            _add_mapping_connection(user_unique_name, ordered_connections, mapping_inner.arg_names,
                                    mapping_inner.name, NodeMappingType.CustomLoss)

            return None

        mapping_inner.arg_names = leap_binder.setup_container.custom_loss_handlers[
            -1].custom_loss_handler_data.arg_names
        mapping_inner.name = name

        def final_inner(*args, **kwargs):
            if os.environ.get(mapping_runtime_mode_env_var_mame):
                return mapping_inner(*args, **kwargs)
            else:
                return inner(*args, **kwargs)

        final_inner.arg_names = leap_binder.setup_container.custom_loss_handlers[-1].custom_loss_handler_data.arg_names
        final_inner.name = name

        return final_inner

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


def tensorleap_status_table():
    import atexit
    import sys
    import traceback
    from typing import Any

    CHECK = "✅"
    CROSS = "❌"
    UNKNOWN = "❔"

    code_mapping_failure = [0]

    table = [
        {"name": "tensorleap_preprocess", "Added to integration": UNKNOWN},
        {"name": "tensorleap_integration_test", "Added to integration": UNKNOWN},
        {"name": "tensorleap_input_encoder", "Added to integration": UNKNOWN},
        {"name": "tensorleap_gt_encoder", "Added to integration": UNKNOWN},
        {"name": "tensorleap_load_model", "Added to integration": UNKNOWN},
        {"name": "tensorleap_custom_loss", "Added to integration": UNKNOWN},
        {"name": "tensorleap_custom_metric (optional)", "Added to integration": UNKNOWN},
        {"name": "tensorleap_metadata (optional)", "Added to integration": UNKNOWN},
        {"name": "tensorleap_custom_visualizer (optional)", "Added to integration": UNKNOWN},
    ]

    _finalizer_called = {"done": False}
    _crashed = {"value": False}
    _current_func = {"name": None}

    def _link(url: str) -> str:
        return f"\033{url}\033"

    def _remove_suffix(s: str, suffix: str) -> str:
        if suffix and s.endswith(suffix):
            return s[:-len(suffix)]
        return s

    def _find_row(name: str):
        for row in table:
            if _remove_suffix(row["name"], " (optional)") == name:
                return row
        return None

    def _set_status(name: str, status_symbol: str):
        row = _find_row(name)
        if not row:
            return

        cur = row["Added to integration"]
        if status_symbol == UNKNOWN:
            return
        # If any interface of this type already failed (CROSS), keep it as failed
        if cur == CROSS:
            return

        row["Added to integration"] = status_symbol

    def _mark_unknowns_as_cross():
        for row in table:
            if row["Added to integration"] == UNKNOWN:
                row["Added to integration"] = CROSS

    def _format_default_value(v: Any) -> str:
        if hasattr(v, "name"):
            return str(v.name)
        if isinstance(v, str):
            return v
        s = repr(v)
        return s if len(s) <= 120 else s[:120] + "..."

    def _print_param_default_warnings():
        data = _get_param_default_warnings()
        if not data:
            return

        print("\nWarnings (Default use. It is recommended to set values explicitly):")
        for param_name in sorted(data.keys()):
            default_value = data[param_name]["default_value"]
            funcs = ", ".join(sorted(data[param_name]["funcs"]))
            dv = _format_default_value(default_value)

            docs_link = data[param_name].get("link_to_docs")
            docs_part = f" {_link(docs_link)}" if docs_link else ""
            print(
                f" ⚠️ Parameter '{param_name}' defaults to {dv} in the following functions: [{funcs}]. "
                f"For more information, check {docs_part}")
        print("\nIf this isn’t the intended behaviour, set them explicitly.")

    def _print_table():
        _print_param_default_warnings()

        if not started_from("leap_integration.py"):
            return

        ready_mess = "\nAll parts have been successfully set. If no errors accured, you can now push the project to the Tensorleap system."
        not_ready_mess = "\nSome mandatory components have not yet been added to the Integration test. Recommended next interface to add is: "
        mandatory_ready_mess = "\nAll mandatory parts have been successfully set. If no errors accured, you can now push the project to the Tensorleap system or continue to the next optional reccomeded interface,adding: "
        code_mapping_failure_mes = "Tensorleap_integration_test code flow failed, check raised exception."

        name_width = max(len(row["name"]) for row in table)
        status_width = max(len(row["Added to integration"]) for row in table)

        header = f"{'Decorator Name'.ljust(name_width)} | {'Added to integration'.ljust(status_width)}"
        sep = "-" * len(header)

        print("\n" + header)
        print(sep)

        ready = True
        next_step = None

        for row in table:
            print(f"{row['name'].ljust(name_width)} | {row['Added to integration'].ljust(status_width)}")
            if not _crashed["value"] and ready:
                if row["Added to integration"] != CHECK:
                    ready = False
                    next_step = row["name"]

        if _crashed["value"]:
            print(f"\nScript crashed before completing all steps. crashed at function '{_current_func['name']}'.")
            return

        if code_mapping_failure[0]:
            print(f"\n{CROSS + code_mapping_failure_mes}.")
            return

        print(ready_mess) if ready else print(
            mandatory_ready_mess + next_step
        ) if (next_step and "optional" in next_step) else print(not_ready_mess + (next_step or ""))

    def set_current(name: str):
        _current_func["name"] = name

    def update_env_params(name: str, status: str = "v"):
        if name == "code_mapping":
            code_mapping_failure[0] = 1
        if status == "v":
            _set_status(name, CHECK)
        else:
            _set_status(name, CROSS)

    def run_on_exit():
        if _finalizer_called["done"]:
            return
        _finalizer_called["done"] = True
        if not _crashed["value"]:
            _mark_unknowns_as_cross()

        _print_table()

    def handle_exception(exc_type, exc_value, exc_traceback):
        _crashed["value"] = True
        crashed_name = _current_func["name"]
        if crashed_name:
            row = _find_row(crashed_name)
            if row:
                row["Added to integration"] = CROSS

        traceback.print_exception(exc_type, exc_value, exc_traceback)
        run_on_exit()

    atexit.register(run_on_exit)
    sys.excepthook = handle_exception

    return set_current, update_env_params


if not _call_from_tl_platform:
    set_current, update_env_params_func = tensorleap_status_table()








