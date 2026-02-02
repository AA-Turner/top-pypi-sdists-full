import sys
from pathlib import Path
from types import TracebackType
from typing import List, Union, Tuple, Any, Callable, Dict, Optional
import traceback
import numpy as np
import numpy.typing as npt

from code_loader.contract.datasetclasses import SectionCallableInterface, PreprocessResponse, \
    InstanceCallableInterface, ElementInstance
from code_loader.contract.enums import DatasetMetadataType


def to_numpy_return_wrapper(encoder_function: SectionCallableInterface) -> SectionCallableInterface:
    def numpy_encoder_function(idx: Union[int, str], samples: PreprocessResponse) -> npt.NDArray[np.float32]:
        result = encoder_function(idx, samples)
        numpy_result: npt.NDArray[np.float32] = np.array(result)
        return numpy_result

    return numpy_encoder_function

def to_numpy_return_masks_wrapper(encoder_function: InstanceCallableInterface) -> InstanceCallableInterface:
    def numpy_encoder_function(idx: Union[int, str], samples: PreprocessResponse, element_idx: int) -> Union[ElementInstance, None]:
        result = encoder_function(idx, samples, element_idx)
        if result is None:
            return None
        result.mask = np.array(result.mask)
        return result
    return numpy_encoder_function


def get_root_traceback(exc_tb: TracebackType) -> TracebackType:
    return_traceback = exc_tb
    while return_traceback.tb_next is not None:
        return_traceback = return_traceback.tb_next
    return return_traceback


def get_root_exception_file_and_line_number() -> Tuple[int, str, str]:
    traceback_as_string = traceback.format_exc()

    root_exception = sys.exc_info()[1]
    assert root_exception is not None
    if root_exception.__context__ is not None:
        root_exception = root_exception.__context__
    _traceback = root_exception.__traceback__

    root_exception_line_number = -1
    root_exception_file_name = ''
    if _traceback is not None:
        root_traceback = get_root_traceback(_traceback)
        root_exception_line_number = root_traceback.tb_lineno
        root_exception_file_name = Path(root_traceback.tb_frame.f_code.co_filename).name
    return root_exception_line_number, root_exception_file_name, traceback_as_string


def get_shape(result: Any) -> List[int]:
    if not isinstance(result, np.ndarray):
        return [1]
    np_shape = result.shape
    # fix single result shape viewing
    if np_shape == ():
        np_shape = (1,)
    shape = list(np_shape)
    return shape


def rescale_min_max(image: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
    image = image.astype('float32')
    image -= image.min()
    image /= (image.max() - image.min() + 1e-5)

    # rescale the values to range between 0 and 255
    image *= 255
    image = image.astype('uint8')

    return image


def map_dict_to_metadata_types(data: Optional[Dict[str, Union[Optional[str], int, bool, Optional[float]]]]) -> Optional[Dict[str, DatasetMetadataType]]:
    if data is None:
        return None
    return {
        k: get_metadata_type_from_variable(v)
        for k, v in data.items()
    }

def get_metadata_type_from_variable(variable: Union[Optional[str], int, bool, Optional[float]]) -> DatasetMetadataType:
    metadata_type = type(variable)
    if metadata_type == int or isinstance(variable,
                                          (np.unsignedinteger, np.signedinteger)):
        metadata_type = float
    if isinstance(variable, str):
        dataset_metadata_type = DatasetMetadataType.string
    elif metadata_type == bool or isinstance(variable, np.bool_):
        dataset_metadata_type = DatasetMetadataType.boolean
    elif metadata_type == float or isinstance(variable, np.floating):
        dataset_metadata_type = DatasetMetadataType.float
    else:
        raise Exception(f"Unsupported return type of metadata {variable}."
                        f"The return type should be one of [int, float, str, bool]. Got {metadata_type}")
    return dataset_metadata_type

