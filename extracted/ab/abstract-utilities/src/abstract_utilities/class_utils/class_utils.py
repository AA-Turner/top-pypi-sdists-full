"""
Sheet: Class Utilities

Module: class_utils.py
Part of: abstract_utilities module
Author: putkoff
Date: 05/31/2023
Version: 0.1.2

This module contains utility functions tailored for handling classes, objects, and modules. It encapsulates operations like:
1. Fetching and checking object types.
2. Manipulating global variables.
3. Checking object membership in a module.
4. Inspecting function signatures and their arguments within a module.
5. Calling functions with supplied arguments.
6. Converting layout definitions into components.
7. Retrieving attributes and methods of a module.

Function Overview:
------------------
- get_type_list: Get a list of common Python types.
- remove_key: Remove a specified key from a dictionary.
- get_module_obj: Retrieve an object from a given module.
- spec_type_mod: Check if an object has a specific type.
- get_type_mod: Retrieve the type name of a given object.
- is_module_obj: Check if an object is part of a module.
- inspect_signature: Fetch the signature of a specified function.
- get_parameter_defaults: Fetch the default parameter values for a function.
- convert_layout_to_components: Convert a layout definition to its component representation.
- get_dir: List all attributes and methods of a module.
- get_proper_args: Call a function using either positional or keyword arguments.
- get_fun: Parse a dictionary to retrieve a function and call it.
- if_none_change: Replace a None object with a default value.
- call_functions: Call a specified function or method using provided arguments.
- process_args: Evaluate and process nested function calls in arguments.
- has_attribute: Check if a function exists in a module.
- mk_fun: Print a statement indicating the existence of a function in a module.

Dependencies:
-------------
- inspect
- json

Each function is furnished with its own docstring that elaborates on its purpose, expected inputs, and outputs.

"""
from .imports import *


def inspect_signature(instance: any, function: str):
    """
    Inspects the signature of a function.

    Args:
        instance (any): The instance containing the function.
        function (str): The name of the function to inspect.

    Returns:
        inspect.Signature: The signature of the function.
    """
    return inspect.signature(get_module_obj(instance, function))

def get_parameter_defaults(module, function):
    """
    Retrieves the default parameter values of a function.

    Args:
        module: The module instance.
        function (str): The name of the function.

    Returns:
        dict: A dictionary containing the parameter names and their default values.
    """
    signature = inspect_signature(module, function)
    if signature is None:
        return {}
    return json.dumps(remove_key({param_name: param.default if param.default != inspect.Parameter.empty else None for param_name, param in signature.parameters.items()}, 'icon'))

def convert_layout_to_components(instance: any = None, component: str = 'function', js: dict = {}):
    """
    Converts a layout to components.

    Args:
        instance (any, optional): The instance containing the components. Defaults to None.
        component (str, optional): The name of the component. Defaults to 'function'.
        js (dict, optional): The dictionary of component properties. Defaults to an empty dictionary.

    Returns:
        any: The result of the component conversion.
    """
    jsN = json.loads(get_parameter_defaults(instance, component))
    keys = list(js.keys())
    for key in jsN:
        if key in js:
            jsN[key] = js[key]
    return call_functions_hard(instance, component, **jsN)
def get_class_inputs(cls, *args, **kwargs):
    fields = list(cls.__annotations__.keys())
    values = {}
    args = list(args)
    for field in fields:
        if field in kwargs:
            values[field] = kwargs[field]
        elif args:
            values[field] = args.pop(0)
        else:
            values[field] = getattr(cls(), field)
    return cls(**values)

