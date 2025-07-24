"""
type_utils.py

This module provides a collection of utility functions for type checking and conversion.
It includes functions to determine the type of an object, check if an object is a specific type,
and perform type conversions. These functions help simplify the process of handling different
types of data and ensure consistent behavior across different data types.

Usage:
    import abstract_utilities.type_utils as type_utils

Functions:
- is_iterable(obj: any) -> bool
- is_number(obj: any) -> bool
- is_str(obj: any) -> bool
- is_int(obj: any) -> bool
- is_float(obj: any) -> bool
- is_bool(obj: any) -> bool
- is_list(obj: any) -> bool
- is_tuple(obj: any) -> bool
- is_set(obj: any) -> bool
- is_dict(obj: any) -> bool
- is_frozenset(obj: any) -> bool
- is_bytearray(obj: any) -> bool
- is_bytes(obj: any) -> bool
- is_memoryview(obj: any) -> bool
- is_range(obj: any) -> bool
- is_enumerate(obj: any) -> bool
- is_zip(obj: any) -> bool
- is_filter(obj: any) -> bool
- is_map(obj: any) -> bool
- is_property(obj: any) -> bool
- is_slice(obj: any) -> bool
- is_super(obj: any) -> bool
- is_type(obj: any) -> bool
- is_Exception(obj: any) -> bool
- is_none(obj: any) -> bool
- is_str_convertible_dict(obj: any) -> bool
- is_dict_or_convertable(obj: any) -> bool
- dict_check_conversion(obj: any) -> Union[dict, any]
- make_list(obj: any) -> list
- make_list_lower(ls: list) -> list
- make_float(obj: Union[str, float, int]) -> float
- make_bool(obj: Union[bool, int, str]) -> Union[bool, str]
- make_str(obj: any) -> str
- get_obj_obj(obj_type: str, obj: any) -> any
- get_len_or_num(obj: any) -> int
- get_types_list() -> list
- det_bool_F(obj: (tuple or list or bool) = False) -> bool
- det_bool_T(obj: (tuple or list or bool) = False) -> bool
- T_or_F_obj_eq(event: any = '', obj: any = '') -> bool

This module is part of the `abstract_utilities` package.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""
import os
from pathlib import Path
from typing import Union
from .path_utils import get_all_item_paths,get_files
from .list_utils import make_list
# A big, but by no means exhaustive, map of extensions to mime‐types by category:
MIME_TYPES = {
    'image': {
        '.jpg':   'image/jpeg',
        '.jpeg':  'image/jpeg',
        '.png':   'image/png',
        '.gif':   'image/gif',
        '.bmp':   'image/bmp',
        '.tiff':  'image/tiff',
        '.webp':  'image/webp',
        '.svg':   'image/svg+xml',
        '.ico':   'image/vnd.microsoft.icon',
        '.heic':  'image/heic',
        '.psd':   'image/vnd.adobe.photoshop',
        '.raw':   'image/x-raw',
    },
    'video': {
        '.mp4':   'video/mp4',
        '.webm':  'video/webm',
        '.ogg':   'video/ogg',
        '.mov':   'video/quicktime',
        '.avi':   'video/x-msvideo',
        '.mkv':   'video/x-matroska',
        '.flv':   'video/x-flv',
        '.wmv':   'video/x-ms-wmv',
        '.3gp':   'video/3gpp',
        '.ts':    'video/mp2t',
    },
    'audio': {
        '.mp3':   'audio/mpeg',
        '.wav':   'audio/wav',
        '.flac':  'audio/flac',
        '.aac':   'audio/aac',
        '.ogg':   'audio/ogg',
        '.m4a':   'audio/mp4',
        '.opus':  'audio/opus',
    },
    'document': {
        '.pdf':   'application/pdf',
        '.doc':   'application/msword',
        '.docx':  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.odt':   'application/vnd.oasis.opendocument.text',
        '.txt':   'text/plain',
        '.rtf':   'application/rtf',
        '.md':    'text/markdown',
        '.markdown': 'text/markdown',
        '.tex':   'application/x-tex',
        '.log':   'text/plain',
        '.json':  'application/json',
        '.xml':   'application/xml',
        '.yaml':  'application/x-yaml',
        '.yml':   'application/x-yaml',
        '.ini':   'text/plain',
        '.cfg':   'text/plain',
        '.toml':  'application/toml',
        '.csv':   'text/csv',
        '.tsv':   'text/tab-separated-values'
    },
    'presentation': {
        '.ppt':   'application/vnd.ms-powerpoint',
        '.pptx':  'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.odp':   'application/vnd.oasis.opendocument.presentation',
    },
    'spreadsheet': {
        '.xls':   'application/vnd.ms-excel',
        '.xlsx':  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.ods':   'application/vnd.oasis.opendocument.spreadsheet',
        '.csv':   'text/csv',
        '.tsv':   'text/tab-separated-values'
    },
    'code': {
        '.py':    'text/x-python',
        '.java':  'text/x-java-source',
        '.c':     'text/x-c',
        '.cpp':   'text/x-c++',
        '.h':     'text/x-c',
        '.hpp':   'text/x-c++',
        '.js':    'application/javascript',
        '.cjs':   'application/javascript',
        '.mjs':   'application/javascript',
        '.jsx':   'application/javascript',
        '.ts':    'application/typescript',
        '.tsx':   'application/typescript',
        '.rb':    'text/x-ruby',
        '.php':   'application/x-php',
        '.go':    'text/x-go',
        '.rs':    'text/rust',
        '.swift': 'text/x-swift',
        '.kt':    'text/x-kotlin',
        '.sh':    'application/x-shellscript',
        '.bash':  'application/x-shellscript',
        '.ps1':   'application/x-powershell',
        '.sql':   'application/sql',
        '.yml':   'application/x-yaml',
        '.coffee':'text/coffeescript',
        '.lua':   'text/x-lua',
    },
    'archive': {
        '.zip':   'application/zip',
        '.tar':   'application/x-tar',
        '.gz':    'application/gzip',
        '.tgz':   'application/gzip',
        '.bz2':   'application/x-bzip2',
        '.xz':    'application/x-xz',
        '.rar':   'application/vnd.rar',
        '.7z':    'application/x-7z-compressed',
        '.iso':   'application/x-iso9660-image',
        '.dmg':   'application/x-apple-diskimage',
        '.jar':   'application/java-archive',
        '.war':   'application/java-archive',
        '.whl':   'application/python-wheel',
        '.egg':   'application/python-egg',
    },
    'font': {
        '.ttf':   'font/ttf',
        '.otf':   'font/otf',
        '.woff':  'font/woff',
        '.woff2': 'font/woff2',
        '.eot':   'application/vnd.ms-fontobject'
    },
    'executable': {
        '.exe':   'application/vnd.microsoft.portable-executable',
        '.dll':   'application/vnd.microsoft.portable-executable',
        '.bin':   'application/octet-stream',
        '.deb':   'application/vnd.debian.binary-package',
        '.rpm':   'application/x-rpm'
    }
}

# And just the sets, if you only need to test ext‐membership:
MEDIA_TYPES = {
    category: set(mapping.keys())
    for category, mapping in MIME_TYPES.items()
}


def get_media_map(categories=None):
    """
    Return a sub‐dict of MEDIA_TYPES for the given categories.
    If categories is None or empty, return the whole MEDIA_TYPES.
    """
    if not categories:
        return MEDIA_TYPES
    cats = {str(c) for c in categories}
    return {c: MEDIA_TYPES[c] for c in cats if c in MEDIA_TYPES}


def get_media_exts(categories=None):
    """
    Return a flat, sorted list of all extensions for the given categories.
    """
    media_map = get_media_map(categories)
    return sorted({ext for exts in media_map.values() for ext in exts})


def confirm_type(path_or_ext, categories=None,**kwargs):
    """
    Given a file‐path or extension, return its media category (e.g. "image"), or None.
    """
    categories = categories or kwargs.get('media_types')
    ext = Path(path_or_ext).suffix.lower()
    media_map = get_media_map(categories)
    for category, exts in media_map.items():
        if ext in exts:
            return category
    return None


def is_media_type(path_or_ext, categories=None,**kwargs):
    """
    True if the given file‐path or extension belongs to one of the categories.
    """
    categories = categories or kwargs.get('media_types')
    return confirm_type(path_or_ext, categories) is not None


def get_mime_type(path_or_ext):
    """
    Look up the MIME type by extension in MIME_TYPES; fall back to octet‐stream.
    """
    ext = Path(path_or_ext).suffix.lower()
    for mapping in MIME_TYPES.values():
        if ext in mapping:
            return mapping[ext]
    return 'application/octet-stream'


def get_all_file_types(categories=None, directory=None,**kwargs):
    """
    Recursively glob for files under `directory` whose extension belongs to `categories`.
    Returns a list of full paths.
    """
    categories = categories or kwargs.get('media_types')
    base = Path(directory)
    if not base.is_dir():
        return []
    wanted = get_media_map(categories)
    return [
        str(p)
        for p in base.rglob('*')
        if p.is_file() and Path(p).suffix.lower() in {e for exts in wanted.values() for e in exts}
    ]

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


            
def convert_to_number(value):
    value_str = str(value)
    if is_number(value_str):
        return float(value_str) if '.' in value_str else int(value_str)
    return value_str

def makeInt(obj):
    if is_number(obj):
       return int(obj)
    return obj

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
def is_any_instance(value):
    for each in [dict, list, int, float]:
        if is_instance(value, each):
            return True

# Function: is_number
# Function: is_str
# Function: is_int
# Function: get_type
# Function: is_float
# Function: is_object
# Function: is_bool
# Function: is_list
# Function: is_tuple
# Function: is_set
# Function: is_dict
# Function: is_frozenset
# Function: is_bytearray
# Function: is_bytes
# Function: is_memoryview
# Function: is_range
# Function: is_enumerate
# Function: is_zip
# Function: is_filter
# Function: is_map
# Function: is_property
# Function: is_slice
# Function: is_super
# Function: is_type
# Function: is_Exception
# Function: is_none
# Function: is_str_convertible_dict
# Function: is_dict_or_convertable
# Function: dict_check_conversion
# Function: make_list
# Function: make_list_lower
# Function: make_float
# Function: make_bool
# Function: make_str
# Function: get_obj_obj
# Function: get_len_or_num
# Function: get_types_list
