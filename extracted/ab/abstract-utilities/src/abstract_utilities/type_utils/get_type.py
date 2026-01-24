from .imports import *
from .alpha_utils import *
from .num_utils import *
from .is_type import *
from .make_type import *
def get_obj_obj(obj_type: str, obj: any) -> any:
    """
    Returns the object converted according to the given type string.
    
    Args:
        obj_type: The string representing the type to convert to.
        obj: The object to convert.
        
    Returns:
        any: The object converted to the specified type.
    """
    if obj_type == 'str':
        return make_str(obj)
    elif obj_type == 'bool':
        return make_bool(obj)
    elif obj_type == 'float':
        return make_float(obj)
    elif obj_type == 'int':
        try:
            return int(obj)
        except (TypeError, ValueError):
            return obj
    else:
        return obj
def get_len_or_num(obj: any) -> int:
    """
    Returns the length of the object if it can be converted to a string, else the integer representation of the object.
    
    Args:
        obj: The object to process.
        
    Returns:
        int: The length of the object as a string or the integer representation of the object.
    """
    if is_int(obj) or is_float(obj):
        return int(obj)
    else:
        try:
            return len(str(obj))
        except (TypeError, ValueError):
            return 0
def get_types_list()->list:
    return ['list', 'bool', 'str', 'int', 'float', 'set', 'dict', 'frozenset', 'bytearray', 'bytes', 'memoryview', 'range', 'enumerate', 'zip', 'filter', 'map', 'property', 'slice', 'super', 'type', 'Exception', 'NoneType']


def str_lower(obj):
    try:
        obj=str(obj).lower()
    except Exception as e:
        print(f"{e}")
    return obj

def get_bool_response(bool_response,json_data):
    if not is_instance(bool_response,bool):
        try:
            bool_response = json_data.get(bool_response) in [None,'',[],"",{}]
        except:
            pass       
    return bool_response
def get_alphabet_str():
  return 'abcdefghijklmnopqrstuvwxyz'
def get_alphabet_upper_str():
  alphabet_str = get_alphabet_str()
  return alphabet_str.upper()
def get_alphabet_comp_str():
  return get_alphabet_str() + get_alphabet_upper_str()

def get_alphabet():
  alphabet_str = get_alphabet_str()
  return break_string(alphabet_str)
def get_alphabet_upper():
  alphabet_upper_str = get_alphabet_upper_str()
  return break_string(alphabet_upper_str)
def get_alphabet_comp():
  alphabet_comp_str = get_alphabet_comp_str()
  return break_string(alphabet_comp_str)
def get_numbers_str():
  return '0123457890'
def get_numbers_int():
  numbers_str = get_numbers_str()
  return [int(number) for number in numbers_str]
def get_numbers():
  numbers_str = get_numbers_str()
  return break_string(numbers_str)
def get_numbers_comp():
  numbers_str = get_numbers()
  numbers_int = get_numbers_int()
  return numbers_str + numbers_int
def break_string(string):
  string_str = str(string)
  return list(string_str)
def get_alpha_ints(ints=True,alpha=True,lower=True,capitalize=True,string=True,listObj=True):
    objs = [] if listObj else ""
    if ints:
        objs+=getInts(string=string,listObj=listObj)
    if alpha:
        objs+=getAlphas(lower=lower,capitalize=capitalize,listObj=listObj)
    return objs
def if_true_get_string(data, key):
    return key if data.get(key) else None
def find_for_string(string, parts):
    return [part for part in parts if string.lower() in str(part).lower()]


def is_strings_in_string(strings, parts):
    strings = make_list(strings)
    for string in strings:
        parts = find_for_string(string, parts)
        if not parts:
            return []
    return parts
def if_not_bool_default(value,default=None):
    if not isinstance(value,bool):
        value = default
    return value
