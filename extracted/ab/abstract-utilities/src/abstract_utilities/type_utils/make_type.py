from .imports import *
from .alpha_utils import *
from .num_utils import *
from .is_type import *
def make_list(obj:any) -> list:
    """
    Converts the input object to a list. If the object is already a list, it is returned as is.
    
    Args:
        obj: The object to convert.
        
    Returns:
        list: The object as a list.
    """
    if isinstance(obj,str):
        if ',' in obj:
            obj = obj.split(',')
    if isinstance(obj,set) or isinstance(obj,tuple):
        return list(obj)
    if isinstance(obj, list):
        return obj
    return [obj]
def get_if_None(obj,default):
    return obj if obj != None else default
def dict_check_conversion(obj:any) -> Union[dict,any]:
    """
    Converts the input object to a dictionary if possible.

    Args:
        obj: The object to convert.

    Returns:
        The object converted to a dictionary if possible, otherwise the original object.
    """
    import json

    if is_dict_or_convertable(obj):
        if is_dict(obj):
            return obj
        return json.loads(obj)
    
    return obj

    
def make_list_lower(ls: list) -> list:
    """
    Converts all elements in a list to lowercase. Ignores None values.
    
    Args:
        ls: The list to convert.
        
    Returns:
        list: The list with all strings converted to lowercase.
    """
    return [item.lower() if is_instance(item, str) else item for item in ls]


def make_float(obj:Union[str,float,int]) -> float:
    """
    Converts the input object to a float.
    
    Args:
        x: The object to convert.
        
    Returns:
        float: The float representation of the object.
    """
    try:
        return float(obj)
    except (TypeError, ValueError):
        return 1.0

def make_bool(obj: Union[bool, int, str]) -> Union[bool, str]:
    """
    Converts the input object to a boolean representation if possible.

    The function attempts to convert various objects, including integers and strings, to their boolean equivalents. 
    If the conversion is not possible, the original object is returned.

    Args:
        obj: The object to be converted.

    Returns:
        bool or original type: The boolean representation of the object if conversion is possible. Otherwise, it returns the original object.

    Examples:
        make_bool("true") -> True
        make_bool(1)      -> True
        make_bool("0")    -> False
        make_bool(2)      -> 2
    """
    if is_instance(obj, bool):
        return obj
    if is_instance(obj, int):
        if obj == 0:
            return False
        if obj == 1:
            return True
    if is_instance(obj, str):
        if obj.lower() in ['0', "false"]:
            return False
        if obj.lower() in ['1', "true"]:
            return True
    return obj

def make_str(obj: any) -> str:
    """
    Converts the input object to a string.
    
    Args:
        obj: The object to convert.
        
    Returns:
        str: The string representation of the object.
    """
    return str(obj)
def convert_to_number(value):
    value_str = str(value)
    if is_number(value_str):
        return float(value_str) if '.' in value_str else int(value_str)
    return value_str

def makeInt(obj):
    if is_number(obj):
       return int(obj)
    return obj
