from .imports import *
def get_module_obj(instance: any, obj: any):
    """
    Retrieves an object from a module.

    Args:
        instance (any): The module instance.
        obj (any): The object to retrieve.

    Returns:
        any: The retrieved object.
    """
    return getattr(instance, obj)

def spec_type_mod(obj: any, st: str) -> bool:
    """
    Checks if an object has a specific type.

    Args:
        obj (any): The object to check.
        st (str): The specific type to check.

    Returns:
        bool: True if the object has the specified type, False otherwise.
    """
    if obj.__class__.__name__ == st:
        return True
    return False

def get_type_mod(obj: any) -> str:
    """
    Retrieves the type of an object.

    Args:
        obj (any): The object to get the type of.

    Returns:
        str: The type of the object.
    """
    type_ls = get_types_list()
    for k in range(len(type_ls)):
        typ = str(type_ls[k])
        if spec_type_mod(obj, typ):
            return typ
    return "NoneType"

def is_module_obj(instance: any, obj: str) -> bool:
    """
    Checks if an object is part of a module.

    Args:
        instance (any): The module instance.
        obj (str): The name of the object to check.

    Returns:
        bool: True if the object is part of the module, False otherwise.
    """
    try:
        if get_type_mod(getattr(instance, obj)) in [None, 'NoneType']:
            return False
        return True
    except:
        return False
