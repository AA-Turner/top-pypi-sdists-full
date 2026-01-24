def is_iterable(obj:any):
    try:
        iterator=iter(obj)
    except TypeError:
        return False
    else:
        return True
    return True

def get_type(obj:any) -> any:
    """
    Determines the type of the input object.

    Args:
        obj: The object to determine the type of.

    Returns:
        any: The object with the updated type.
    """
    if is_number(obj):
        obj = int(obj)
    if is_float(obj):
        return float(obj)
    elif obj == 'None':
        obj = None
    elif is_str(obj):
        obj = str(obj)
    return obj

def is_instance(obj:any,typ:any) -> bool:
    """
    Checks whether the input object can be represented as a number.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object can be represented as a number, False otherwise.
    """
    boolIt = False
    try:
        boolIt = isinstance(obj, typ)
        return boolIt
    except:
        return boolIt

def is_number(s):
    try:
        float(s)
        return True
    except:
        return False

def is_object(obj:any) -> bool:
    """
    Checks whether the input object is of type 'object'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'object', False otherwise.
    """
    return is_instance(obj, object)
def is_str(obj:any) -> bool:
    """
    Checks whether the input object is of type 'str'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'str', False otherwise.
    """
    return is_instance(obj, str)
def is_int(obj:any) -> bool:
    """
    Checks whether the input object is of type 'int'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'int', False otherwise.
    """
    return is_instance(obj, int)
def is_float(obj:any) -> bool:
    """
    Checks whether the input object is of type 'float'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'float', False otherwise.
    """
    return is_instance(obj, float)
def is_bool(obj:any) -> bool:
    """
    Checks whether the input object is of type 'bool'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'bool', False otherwise.
    """
    return is_instance(obj, bool)


def is_list(obj:any) -> bool:
    """
    Checks whether the input object is of type 'list'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'list', False otherwise.
    """
    return is_instance(obj, list)
def is_tuple(obj:any) -> bool:
    """
    Checks whether the input object is of type 'tuple'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'tuple', False otherwise.
    """
    return is_instance(obj, tuple)
def is_set(obj:any) -> bool:
    """
    Checks whether the input object is of type 'set'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'set', False otherwise.
    """
    return is_instance(obj, set)
def is_dict(obj:any) -> bool:
    """
    Checks whether the input object is of type 'dict'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'dict', False otherwise.
    """
    return is_instance(obj, dict)
def is_frozenset(obj:any) -> bool:
    """
    Checks whether the input object is of type 'frozenset'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'frozenset', False otherwise.
    """
    return is_instance(obj, frozenset)
def is_bytearray(obj:any) -> bool:
    """
    Checks whether the input object is of type 'bytearray'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'bytearray', False otherwise.
    """
    return is_instance(obj, bytearray)
def is_bytes(obj:any) -> bool:
    """
    Checks whether the input object is of type 'bytes'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'bytes', False otherwise.
    """
    return is_instance(obj, bytes)
def is_memoryview(obj:any) -> bool:
    """
    Checks whether the input object is of type 'memoryview'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'memoryview', False otherwise.
    """
    return is_instance(obj, memoryview)
def is_range(obj:any) -> bool:
    """
    Checks whether the input object is

 of type 'range'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'range', False otherwise.
    """
    return is_instance(obj, range)
def is_enumerate(obj:any) -> bool:
    """
    Checks whether the input object is of type 'enumerate'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'enumerate', False otherwise.
    """
    return is_instance(obj, enumerate)
def is_zip(obj:any) -> bool:
    """
    Checks whether the input object is of type 'zip'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'zip', False otherwise.
    """
    return is_instance(obj, zip)
def is_filter(obj:any) -> bool:
    """
    Checks whether the input object is of type 'filter'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'filter', False otherwise.
    """
    return is_instance(obj, filter)
def is_map(obj:any) -> bool:
    """
    Checks whether the input object is of type 'map'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'map', False otherwise.
    """
    return is_instance(obj, map)
def is_property(obj:any) -> bool:
    """
    Checks whether the input object is of type 'property'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'property', False otherwise.
    """
    return is_instance(obj, property)


def is_slice(obj:any) -> bool:
    """
    Checks whether the input object is of type 'slice'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'slice', False otherwise.
    """
    return is_instance(obj, slice)


def is_super(obj:any) -> bool:
    """
    Checks whether the input object is of type 'super'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'super', False otherwise.
    """
    return is_instance(obj, super)


def is_type(obj:any) -> bool:
    """
    Checks whether the input object is of type 'type'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'type', False otherwise.
    """
    return is_instance(obj, type)


def is_Exception(obj:any) -> bool:
    """
    Checks whether the input object is of type 'Exception'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'Exception', False otherwise.
    """
    return is_instance(obj, Exception)


def is_none(obj:any) -> bool:
    """
    Checks whether the input object is of type 'None'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'None', False otherwise.
    """
    if type(obj) is None:
        return True
    else:
        return False



def is_dict_or_convertable(obj:any) -> bool:
    """
    Checks whether the input object is of type 'dict' or can be converted to a dictionary.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'dict' or can be converted to a dictionary, False otherwise.
    """
    if is_dict(obj):
        return True
    if is_str_convertible_dict(obj):
        return True
    return False
def is_str_convertible_dict(obj:any) -> bool:
    """
    Checks whether the input object is a string that can be converted to a dict.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object can be converted to a dict, False otherwise.
    """
    import json

    if is_instance(obj, str):
        try:
            json.loads(obj)
            return True
        except json.JSONDecodeError:
            return False

    return False
def is_any_instance(value):
    for each in [dict, list, int, float]:
        if is_instance(value, each):
            return True
def det_bool_F(obj: (tuple or list or bool) = False):
    """
    Determines if the given object is a boolean False value.

    Args:
        obj (tuple or list or bool): The object to determine the boolean False value.

    Returns:
        bool: True if the object is a boolean False value, False otherwise.
    """
    if is_instance(obj, bool):
        return obj
    return all(obj)
def det_bool_T(obj: (tuple or list or bool) = False):
    """
    Determines if the given object is a boolean True value.

    Args:
        obj (tuple or list or bool): The object to determine the boolean True value.

    Returns:
        bool: True if the object is a boolean True value, False otherwise.
    """
    if is_instance(obj, bool):
        return obj 
    return any(obj)
def T_or_F_obj_eq(event: any = '', obj: any = ''):
    """
    Compares two objects and returns True if they are equal, False otherwise.

    Args:
        event (any): The first object to compare.
        obj (any): The second object to compare.

    Returns:
        bool: True if the objects are equal, False otherwise.
    """
    return True if event == obj else False
def ensure_integer(page_value:any, default_value:int):
    """
    Ensures the given value is an integer. If not, it tries to extract 
    the numeric part of the value. If still unsuccessful, it defaults 
    to the given default value.

    Parameters:
    - page_value (str|int|any): The value to ensure as integer. 
                                Non-numeric characters are stripped if necessary.
    - default_value (int): The default value to return if conversion 
                           to integer is unsuccessful.

    Returns:
    - int: The ensured integer value.
    """
    # Check if page_value is already a number
    if not is_number(page_value):
        # Convert to string in case it's not already
        page_value = str(page_value)
        
        # Remove non-numeric characters from the beginning
        while len(page_value) > 0 and page_value[0] not in '0123456789'.split(','):
            page_value = page_value[1:]

        # Remove non-numeric characters from the end
        while len(page_value) > 0 and page_value[-1] not in '0123456789'.split(','):
            page_value = page_value[:-1]

    # If page_value is empty or still not a number, use the default value
    if len(page_value) == 0 or not is_number(page_value):
        return default_value

    # Convert page_value to an integer and return
    return int(page_value)
def if_default_return_obj(obj:any,default:any=None,default_compare:any=None):
    if default == default_compare:
        return obj
    return default


            
