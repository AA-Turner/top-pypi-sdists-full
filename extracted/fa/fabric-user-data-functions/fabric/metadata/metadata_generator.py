import importlib
import json
import logging
import os
from pathlib import Path
import sys
import subprocess
# flake8: noqa: I900
import azure.functions as azure_func

# return code:
# 0 - no error
# 1 - error

PYTHON_VERSION_REQUIRED = (3, 11)
SCRIPT_FILE_NAME = 'function_app.py'
METADATA_FILE_NAME = 'functions.metadata'
FABRIC_UDF_LIB_NAME = 'fabric_user_data_functions'
NEEDED_BINDING_TYPES = {'httpTrigger', 'UdfProperty', 'FabricItem', 'UserDataFunctionContext'}
SUPPORTED_UDF_PARAMETER_TYPES = ["str", "int", "float", "bool", "datetime", "list", "dict", "set", "tuple"]
SUPPORTED_UDF_RETURN_TYPES = list(SUPPORTED_UDF_PARAMETER_TYPES) + ["None"]
ERROR_CODE = 1
SUCCESS = 0

def _get_app_functions(file_name: str = SCRIPT_FILE_NAME):
    module_path = os.getcwd()
    func_file = os.path.join(module_path, file_name)

    if not os.path.exists(func_file):
        logging.error(f'Cannot find source code {file_name}')
        return None
    
    sys.path.append(str(module_path))
    module_name = Path(func_file).stem
    imported_module = importlib.import_module(module_name)

    app = None
    for i in imported_module.__dir__():
        if isinstance(getattr(imported_module, i, None), azure_func.FunctionRegister):
            if not app:
                app = getattr(imported_module, i, None)
            else:
                logging.error("More than 1 app found in the source code")
                return None

    if not app:
        logging.error("No app found in the source code")
        return None
    
    functions = app.get_functions()
    if not functions:
        logging.error("No function found in the source code")
        return None
    
    return functions

def _collect_function_metadata(functions):
    metadata=[]
    warnings = []
    errors = []
    for func in functions:
        # log the function bindings
        logging.info(f'Getting metadata from Function {func._name}')

        single_func_meta = {}
        single_func_meta['name'] = func._name
        single_func_meta['scriptFile'] = func.function_script_file
        single_func_meta['bindings'] = []

        udf_worker_version = _get_fabric_lib_version()
        if udf_worker_version is not None and len(udf_worker_version) > 0:
            single_func_meta['fabricWorkerVersion'] = udf_worker_version

        for binding in func._bindings:
            if binding.type not in NEEDED_BINDING_TYPES:
                continue
            logging.info(f' Binding name: {binding.name}')
            logging.info(f' Binding type: {binding.type}')
            logging.info(f' Binding direction: {binding._direction.name}')

            b = {}
            b['name'] = binding.name
            b['direction'] = ''.join([binding._direction.name[0], binding._direction.name[1:].lower()])
            b['type'] = binding.type

            additional_props = {}
            if binding.type == 'httpTrigger':
                additional_props = _get_http_binding_properties(binding)

            if binding.type == 'UdfProperty':
                additional_props = _get_udf_binding_properties(binding)
            
            if binding.type == 'FabricItem':
                additional_props = _get_fabricItem_binding_properties(binding)

            if binding.type == 'UserDataFunctionContext':
                additional_props = _get_userDataFunctionContext_binding_properties(binding)

            for key, value in additional_props.items():
                b[key] = value

            single_func_meta['bindings'].append(b)

        udf_properties, udfproperty_errors = _get_udf_properties_from_function(single_func_meta, func)
        if (len(udfproperty_errors) > 0):
            errors.extend(udfproperty_errors)

        single_func_meta['fabricProperties'] = udf_properties

        # remove UdfProperties from bindings
        single_func_meta['bindings'] = [b for b in single_func_meta['bindings'] if b['type'] != 'UdfProperty']

        metadata.append(single_func_meta)
    
    warning = _generate_metadata_warnings(metadata)
    if(warning is not None and len(metadata) > 0):
        warnings.append(warning)
    
    # put all warnings/errors in the first function because metadata is an array of functions, and the vscode extension knows to look here for them

    if len(warnings) > 0:
        metadata[0]['warnings'] = warnings
    
    if len(errors) > 0:
        metadata[0]['errors'] = errors
    
    return metadata


def _get_fabric_lib_version():
    try:
        output = subprocess.check_output([sys.executable, '-m', 'pip', 'show', FABRIC_UDF_LIB_NAME], text=True)
        version_line = next((line for line in output.splitlines() if line.startswith('Version:')), None)
        if version_line:
            return version_line.split(':')[1].strip()
    except subprocess.CalledProcessError:
        logging.error(f'Cannot find the version of {FABRIC_UDF_LIB_NAME}')
        return None

def _get_http_binding_properties(binding):
    props = {}
    methods = getattr(binding, 'methods', None)
    if not methods:
        methods = [azure_func.HttpMethod.POST]
    
    props['methods'] = []
    for m in methods:
        if m == azure_func.HttpMethod.PUT:
            logging.error("Fabric Function currently does not support PUT HTTP actions.")
            return None
        props['methods'].append(m.value.lower())

    props['route'] = getattr(binding, 'route', None)
    auth = getattr(binding, 'auth_level', None)
    if auth:
        props['authLevel'] = ''.join([auth.value[0].upper(), auth.value[1:].lower()])

    return props

def _get_fabricItem_binding_properties(binding):
    props = {}
    
    props['alias'] = getattr(binding, 'alias', None)

    return props

def _get_userDataFunctionContext_binding_properties(binding):
    props = {}
    
    props['parameterName'] = getattr(binding, 'parameterName', None)

    return props

def _get_udf_binding_properties(binding):
    props = {}
    
    props['parameterName'] = getattr(binding, 'parameterName', None)
    typeName = getattr(binding, 'typeName', 'any')
    if (typeName == 'UdfString'):
        typeName = 'str'
    props['typeName'] = typeName

    return props

   
def _ensure_return_type_is_supported(return_type_name: str, func_name: str, errors: list):
    if return_type_name not in SUPPORTED_UDF_RETURN_TYPES:
        errors.append(f"The function '{func_name}' has a return type '{return_type_name}' that is not supported. Supported types are: {SUPPORTED_UDF_RETURN_TYPES}")

def _ensure_parameter_type_is_supported(parameter_name: str, parameter_type_name: str, func_name: str, errors: list):
     # If the parameter has a fabricitem binding, this function won't check its argument type, but the error message should probably contain that those are available as data types to avoid user confusion.
    if parameter_type_name not in SUPPORTED_UDF_PARAMETER_TYPES:
        errors.append(f"The function '{func_name}' has a parameter '{parameter_name}' with a data type '{parameter_type_name}' that is not supported. Supported types are: {SUPPORTED_UDF_PARAMETER_TYPES}")

def _get_udf_properties_from_function(func_meta, func):
    errors = []
    props = {}

    if 'old_return' not in func._func.__annotations__:
        errors.append(f"Function '{func_meta['name']}': return type must be annotated.")
    else:
        return_type = getattr(func._func.__annotations__['old_return'], "__name__", "None")
        _ensure_return_type_is_supported(return_type, func_meta['name'], errors)
        props['fabricFunctionReturnType'] = return_type
    
    props['fabricFunctionParameters'] = []

    for binding in func_meta['bindings']:
        if binding['type'] == 'UdfProperty':
            p = {}
            p['name'] = binding['parameterName']
            p['dataType'] = binding['typeName']
            _ensure_parameter_type_is_supported(p['name'], p['dataType'], func_meta['name'], errors)
            props['fabricFunctionParameters'].append(p)

    return props, errors

def _get_metadata_file_path(file_name=METADATA_FILE_NAME):
    base_directory = os.getcwd()
    return os.path.join(base_directory, "fabric_lib", file_name)

def _write_metadata_file(metadata, file_name=METADATA_FILE_NAME):
    metadata_json = json.dumps(metadata)
    output = _get_metadata_file_path(file_name)
    with open(output, 'w') as meta_file:
        meta_file.write(metadata_json)

def _delete_metadata_file_if_exist(file_name=METADATA_FILE_NAME):
    metadata_file = _get_metadata_file_path(file_name)
    if os.path.exists(metadata_file):
        os.remove(metadata_file)

def _get_sys_version():
    return sys.version_info

def _generate_metadata_warnings(metadata):
    current_version = _get_sys_version()
    if current_version[0] != PYTHON_VERSION_REQUIRED[0] or current_version[1] != PYTHON_VERSION_REQUIRED[1]:
        return f'Python version {current_version[0]}.{current_version[1]} is not equal to the required version {PYTHON_VERSION_REQUIRED[0]}.{PYTHON_VERSION_REQUIRED[1]}'

def generate_function_metadata():
    try:
        # remove metadata first since VSCode extension uses existence of the file as the success of the script run
        _delete_metadata_file_if_exist()

        functions = _get_app_functions()

        if(functions is None):
            return ERROR_CODE
        
        metadata = _collect_function_metadata(functions)
        if(metadata is None):
            return ERROR_CODE

        _write_metadata_file(metadata)
        # prettify the json metadata and log it
        logging.info(json.dumps(metadata, indent=2, sort_keys=True))
        logging.info(f'Function metadata generated successfully for {len(functions)} functions.')
        return SUCCESS
    except Exception as e:
        logging.error(f'Got errors when generating metadata. Details:{e}')
        return ERROR_CODE
