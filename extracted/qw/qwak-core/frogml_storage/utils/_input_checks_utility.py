import os
import re
from typing import List, Optional, Union

from frogml_storage.logging import logger
from frogml_storage.constants import FROG_ML_MAX_CHARS_FOR_NAME
from frogml_storage.exceptions.validation_error import FrogMLValidationError

valid_characters_pattern = re.compile(r"^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*$")


def user_input_validation(
    entity_name: Optional[str],
    namespace: Optional[str],
    version: Optional[str],
    properties: Optional[dict[str, str]] = None,
) -> bool:
    for arg_name, arg_value in {
        "entity_name": entity_name,
        "namespace": namespace,
        "version": version,
    }.items():
        if arg_value is not None:
            __input_validation(arg_value, arg_name)

    if properties is not None:
        __user_input_dict_validation(properties)

    return True


def __user_input_dict_validation(properties: dict[str, str]) -> bool:
    if properties is not None:
        for key, value in properties.items():
            __input_validation(key, "properties")
            __input_validation(value, "properties")
    return True


def is_not_none(arg_name: str, arg_value: Optional[object]) -> bool:
    if arg_value is None:
        raise FrogMLValidationError("{} can't be 'None'.".format(arg_name))
    return True


def __input_validation(field_value: str, field_name: str) -> bool:
    if len(str(field_value)) > FROG_ML_MAX_CHARS_FOR_NAME:
        raise FrogMLValidationError(
            "Max length for {} is 60 characters.".format(field_name.capitalize())
        )

    if not field_value or not re.match(valid_characters_pattern, str(field_value)):
        raise FrogMLValidationError(
            "Invalid characters detected at {}: {}".format(
                field_name.capitalize(), field_value
            )
        )

    return True


def is_valid_thread_number(thread_count: str) -> bool:
    try:
        int_thread_count = int(thread_count)
        cpu_count = os.cpu_count()
        if int_thread_count <= 0 or (
            cpu_count is not None and int_thread_count >= cpu_count
        ):
            raise ValueError(
                "Invalid thread count: {}. The default value will be used.".format(
                    thread_count
                )
            )
        return True
    except ValueError as e:
        logger.warning("Thread count {}: {}".format(thread_count, e))
        return False
    except TypeError:
        logger.debug("Thread count not configured. The default value will be used.")
        return False


def validate_not_folder_paths(paths: Union[Optional[List[str]], Optional[str]]) -> bool:
    if paths is not None:
        if isinstance(paths, List):
            for path in paths:
                __validate_not_folder_path(path)
        else:
            __validate_not_folder_path(paths)
    return True


def __validate_not_folder_path(path: str) -> bool:
    if os.path.isdir(path):
        raise FrogMLValidationError(
            "file '{}' must be a file, but is a directory.".format(path)
        )
    return True


def validate_path_exists(path: str) -> bool:
    if not os.path.exists(path):
        raise ValueError(f"Provided path does not exists : '{path}'")
    return True
