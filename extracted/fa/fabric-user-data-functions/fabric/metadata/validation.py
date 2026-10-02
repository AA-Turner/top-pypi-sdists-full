import logging

# flake8: noqa: I900
from fabric.metadata.metadata_generator import (
    ERROR_CODE, SUCCESS, _collect_function_metadata, _get_app_functions)


def validate():
    try:
        functions = _get_app_functions()
        if(functions is None):
            return ERROR_CODE
        
        metadata = _collect_function_metadata(functions)
        if(metadata is None):
            return ERROR_CODE
        
        return SUCCESS
    except Exception as e:
        logging.error(f'Got errors when generating metadata. Details:{e}')
        return ERROR_CODE


if __name__ == '__main__':
    validate()
