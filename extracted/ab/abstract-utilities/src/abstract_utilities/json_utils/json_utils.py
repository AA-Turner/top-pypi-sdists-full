#!/usr/bin/env python3
"""
json_utils.py

This script is a utility module providing functions for handling JSON data. It includes functionalities like:
1. Converting JSON strings to dictionaries and vice versa.
2. Merging, adding to, updating, and removing keys from dictionaries.
3. Retrieving keys, values, specific items, and key-value pairs from dictionaries.
4. Recursively displaying values of nested JSON data structures with indentation.
5. Loading from and saving dictionaries to JSON files.
6. Validating and cleaning up JSON strings.
7. Searching and modifying nested JSON structures based on specific keys, values, or paths.
8. Inverting JSON data structures.
9. Creating and reading from JSON files.

Each function is documented with Python docstrings for detailed usage instructions.

This module is part of the `abstract_utilities` package.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""
from .imports import (
    re,
    os,
    json,
    logging,
    datetime,
    date,
    Path,
    get_closest_match_from_list,
    make_list,
    get_keys,
    make_key_map,
    find_keys,
    safe_json_dumps,
    try_json_loads,
    safe_json_loads,
    clean_invalid_newlines,
    read_malformed_json,
    get_value_from_path,
    find_paths_to_key,
    get_any_value,
    flatten_json,
    dump_if_json,
    validate_file_path,
    get_file_path,
    get_only_kwargs,
    get_desired_key_values,
    makeParams,
)
# No logging.basicConfig here: a library configuring the root logger at import
# turned on DEBUG output for every package in the host process. This module logs
# through its own logger; errors still reach stderr via logging's last resort.
logger = logging.getLogger(__name__)
def convert_and_normalize_values(values):
    for value in values:
        if isinstance(value, str):
            yield value.lower()
        elif isinstance(value, (int, float)):
            yield value
        else:
            yield str(value).lower()
def json_key_or_default(json_data,key,default_value):
    json_data = safe_json_loads(json_data)
    if not isinstance(json_data,dict) or (isinstance(json_data,dict) and key not in json_data):
        return default_value
    return json_data[key]



def is_valid_json(json_string: str) -> bool:
    """
    Checks whether a given string is a valid JSON string.

    Args:
        json_string (str): The string to check.

    Returns:
        bool: True if the string is valid JSON, False otherwise.
    """
    try:
        json_obj = json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False
def get_error_msg(error_msg, default_error_msg):
    return error_msg if error_msg else default_error_msg
def write_file(data,file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(data))
def write_json(data,file_path, ensure_ascii=False, indent=4):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=ensure_ascii, indent=indent)
def safe_write_json(data,file_path, ensure_ascii=False, indent=4):
    if isinstance(data, (dict, list, tuple)):
        write_json(data,file_path, ensure_ascii=ensure_ascii, indent=indent)
    else:
        write_file(data,file_path)
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
def output_read_write_error(e,function_name,file_path,valid_file_path=None,data=None,is_read=False):
    error_text = f"Error in {function_name};{e}\nFile path: {file_path} "
  
    if valid_file_path == None:
        error_text+=f"\nValid File path: {valid_file_path} "
    
    if not is_read:
        error_text+=f"\nData: {data} "
    logger.error(error_text)
def safe_dump_to_file(data, file_path=None, ensure_ascii=False, indent=4, *args, **kwargs):
    is_read=False
    file_args = [file_path,data]
    valid_file_path = get_file_path(*file_args,*args,is_read=is_read,**kwargs)
    
    if valid_file_path:
        file_path = valid_file_path
        if file_path == file_args[-1]:
            data = file_args[0]
    if file_path is not None and data is not None:
        try:
            safe_write_json(data,file_path, ensure_ascii=ensure_ascii, indent=indent)
        except Exception as e:
            function_name='safe_dump_to_file'
            output_read_write_error(e,function_name,file_path,valid_file_path,is_read=is_read)
    else:
        logger.error("file_path and data must be provided to safe_dump_to_file")

def safe_read_from_json(file_path,*args,**kwargs):
    is_read=True


    valid_file_path = get_file_path(file_path,*args,is_read=is_read,**kwargs)
    if valid_file_path:
        file_path = valid_file_path
    try:
        return read_json(file_path)
    except Exception as e:
        function_name='safe_read_from_json'
        output_read_write_error(e,function_name,file_path,valid_file_path,is_read=is_read)
        return None

def create_and_read_json(*args, **kwargs) -> dict:
    """
    Create a JSON file if it does not exist, then read from it.
    
    Args:
        file_path (str): The path of the file to create and read from.
        json_data (dict): The content to write to the file if it does not exist.
        
    Returns:
        dict: The contents of the JSON file.
    """
    is_read=True
    valid_file_path = get_file_path(*args,is_read=is_read,**kwargs)
    if not valid_file_path:
        safe_dump_to_file(*args, **kwargs)
    return safe_read_from_json(*args, **kwargs)
def read_from_json(*args, **kwargs):
    return safe_read_from_json(*args, **kwargs)
def safe_load_from_json(*args, **kwargs):
    return safe_read_from_json(*args, **kwargs)
def safe_load_from_file(*args, **kwargs):
    return safe_read_from_json(*args, **kwargs)
def safe_read_from_file(*args, **kwargs):
    return safe_read_from_json(*args, **kwargs)
def safe_json_reads(*args, **kwargs):
    return safe_read_from_json(*args, **kwargs)

def safe_dump_to_json(*args, **kwargs):
    return safe_dump_to_file(*args, **kwargs)
def safe_write_to_json(*args, **kwargs):
    return safe_dump_to_file(*args, **kwargs)
def safe_write_to_file(*args, **kwargs):
    return safe_dump_to_file(*args, **kwargs)



def try_json_dumps_spec(obj, logger=True, level='error', file_path=None, **kwargs):
    """
    Attempts to serialize an object to JSON using json.dumps or json.dump.
    
    Args:
        obj: The Python object to serialize (e.g., dict, list, str, int, etc.).
        logger: Logger object or None to use _default_logger.
        level: Logging level for errors (default: 'error').
        file_path: If provided, writes JSON to this file using json.dump.
        **kwargs: Additional arguments to pass to json.dumps or json.dump (e.g., indent, sort_keys).
    
    Returns:
        str: The JSON-serialized string if file_path is None and serialization succeeds.
        None: If serialization fails or file_path is provided (in which case it writes to the file).
    
    Raises:
        ValueError: If file_path is provided but the file cannot be written.
    """
    
    try:
        if file_path:
            # Use json.dump to write to a file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(obj, f, **kwargs)
            return None
        else:
            # Use json.dumps to return a string
            return json.dumps(obj)
    except (TypeError, OverflowError, ValueError) as e:
        if log_callable:
            print_or_log(f"Exception in json.dumps/dump: {e}")
        return None
def run_it(endpoint,**kwargs):
    response= make_request_link('typicaly',endpoint,data=kwargs)
    return response
def get_logNone(e):
    logger(f"{e}")
    return None
def try_json_load(file):
    try:
        file = json.load(file)
    except Exception as e:
        file = get_logNone(e)
    return file
def try_json_dump(file):
    try:
        file = json.dump(file)
    except Exception as e:
        file = get_logNone(e)
    return file
def try_json_dumps(data):
    try:
        data = json.dumps(data)
    except Exception as e:
        data = get_logNone(e)
    return data
def safe_json_load(file):
    file = try_json_load(file) or file
    return file
def safe_json_dump(file):
    file = try_json_dump(file) or file
    return file
def unified_json_loader(file_path, default_value=None, encoding='utf-8'):
    # Try to load from the file
    with open(file_path, 'r', encoding=encoding) as file:
        content = all_try(data=file, function=try_json_load, error_value=json.JSONDecodeError, error=False)
    
    if isinstance(content, dict):
        return content
    
    # Try to load from the file as a string
    with open(file_path, 'r', encoding=encoding) as file:
        content_str = file.read()
        content = all_try(data=content_str, function=try_json_loads, error_value=json.JSONDecodeError, error=False)
    
    if isinstance(content, dict):
        return content
    
    print(f"Error reading JSON from '{file_path}'.")
    return default_value


def get_key_values_from_path(json_data, path):
    try_path = get_value_from_path(json_data, path[:-1])
    if isinstance(try_path, dict):
        return list(try_path.keys())
    
    current_data = json_data
    for step in path:
        try:
            current_data = current_data[step]
            if isinstance(current_data, str):
                try:
                    current_data = json.loads(current_data)
                except json.JSONDecodeError:
                    pass
        except (TypeError, KeyError, IndexError):
            return None
    
    if isinstance(current_data, dict):
        return list(current_data.keys())
    else:
        return None
def convert_to_json(obj):
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, str):
        return safe_json_loads(obj)
    return None
def get_any_key(data,key):
    path_to_key = find_paths_to_key(safe_json_loads(data),key)
    if path_to_key:
        value = safe_json_loads(data)
        for each in path_to_key[0]:
            value = safe_json_loads(value[each])
        return value
    return path_to_key

def all_try(function=None, data=None, var_data=None, error=False, error_msg=None, error_value=Exception, attach=None, attach_var_data=None):
    try:
        if not function:
            raise ValueError("Function is required")

        if var_data and not data:
            result = function(**var_data)
        elif data and not var_data:
            if attach and attach_var_data:
                result = function(data).attach(**attach_var_data)
            else:
                result = function(data).attach() if attach else function(data)
        elif data and var_data:
            raise ValueError("Both data and var_data cannot be provided simultaneously")
        else:
            result = function()

        return result
    except error_value as e:
        if error:
            raise e
        elif error_msg:
            print_error_msg(error_msg, f': {e}')
        return False
def all_try_json_loads(data, error=False, error_msg=None, error_value=(json.JSONDecodeError, TypeError)):
    return all_try(data=data, function=json.loads, error=error, error_msg=error_msg, error_value=error_value)

def safe_json_loadss(data, default_value=None, error=False, error_msg=None): 
    """ Safely attempts to load a JSON string. Returns the original data or a default value if parsing fails.
    Args:
        data (str): The JSON string to parse.
        default_value (any, optional): The value to return if parsing fails. Defaults to None.
        error (bool, optional): Whether to raise an error if parsing fails. Defaults to False.
        error_msg (str, optional): The error message to display if parsing fails. Defaults to None.
    
    Returns:
        any: The parsed JSON object, or the original data/default value if parsing fails.
    """
    if isinstance(data,dict):
        return data
    try_json = all_try_json_loads(data=data, error=error, error_msg=error_msg)
    if try_json:
        return try_json
    if default_value:
        data = default_value
    return data
def format_json_key_values(json_data, indent=0):
    formatted_string = ""

    # Check if the input is a string and try to parse it as JSON
    if isinstance(json_data, str):
        try:
            json_data = json.loads(json_data)
        except json.JSONDecodeError:
            return "Invalid JSON string"

    # Function to format individual items based on their type
    def format_item(item, indent):
        if isinstance(item, dict):
            return format_json_key_values(item, indent)
        elif isinstance(item, list):
            return format_list(item, indent)
        else:
            return '    ' * indent + str(item) + "\n"

    # Function to format lists
    def format_list(lst, indent):
        lst_str = ""
        for elem in lst:
            lst_str += format_item(elem, indent + 1)
        return lst_str

    # Iterate over each key-value pair
    for key, value in json_data.items():
        # Append the key with appropriate indentation
        formatted_string += '    ' * indent + f"{key}:\n"

        # Recursively format the value based on its type
        formatted_string += format_item(value, indent)

    return formatted_string

def find_matching_dicts(dict_objs:(dict or list)=None,keys:(str or list)=None,values:(str or list)=None):
    values = make_list(values) if values is not None else []
    dict_objs = make_list(dict_objs) if dict_objs is not None else [{}]
    keys = make_list(keys) if keys is not None else []
    bool_list_og = [False for i in range(len(keys))]
    found_dicts = []
    for dict_obj in dict_objs:
        bool_list = bool_list_og
        for i,key in enumerate(keys):
            if key in list(dict_obj.keys()):
                if dict_obj[key] == values[i]:
                    bool_list[i]=True
                    if False not in bool_list:
                        found_dicts.append(dict_obj)
    return found_dicts

def closest_dictionary(dict_objs:dict=None,values:(str or list)=None):
    values = make_list(values) if values is not None else []
    dict_objs = make_list(dict_objs) if dict_objs is not None else [{}]
    total_values = [value for dict_obj in dict_objs for value in dict_obj.values()]
    matched_objs = [get_closest_match_from_list(value, total_values) for value in values]
    bool_list_og = [False for i in range(len(matched_objs))]
    for dict_obj in dict_objs:
        bool_list = bool_list_og
        for key, key_value in dict_obj.items():
            for i,matched_obj in enumerate(matched_objs):
                if key_value.lower() == matched_obj.lower():
                    bool_list[i]=True
                    if False not in bool_list:
                        return dict_obj
    return None

def get_dict_from_string(string, file_path=None):
    bracket_count = 0
    start_index = None
    for i, char in enumerate(string):
        if char == '{':
            bracket_count += 1
            if start_index is None:
                start_index = i
        elif char == '}':
            bracket_count -= 1
            if bracket_count == 0 and start_index is not None:
                json_data = safe_json_loads(string[start_index:i+1])
                if file_path:
                    safe_dump_to_file(file_path=mkdirs(file_path), data=json_data)
                return json_data
    return None
                    
def closest_dictionary(dict_objs=None, values=None):
    values = make_list(values) if values is not None else []
    dict_objs = make_list(dict_objs) if dict_objs is not None else [{}]
    total_values = [value for dict_obj in dict_objs for value in dict_obj.values()]
    matched_objs = [get_closest_match_from_list(value, total_values) for value in values]

    for dict_obj in dict_objs:
        # Using all() with a generator expression for efficiency
        if all(match in convert_and_normalize_values(dict_obj.values()) for match in matched_objs):
            return dict_obj
    return None                  

def get_all_keys(dict_data,keys=[]):
  if isinstance(dict_data,dict):
    for key,value in dict_data.items():
      keys.append(key)
      keys = get_all_keys(value,keys=keys)
  return keys

def update_dict_value(data, paths, new_value):
    """
    Traverses a dictionary to the specified key path and updates its value.
    
    Args:
        data (dict): The dictionary to traverse.
        paths (list): The list of keys leading to the target value.
        new_value (any): The new value to assign to the specified key.

    Returns:
        dict: The updated dictionary.
    """
    d = data
    for key in paths[:-1]:
        # Traverse the dictionary up to the second-to-last key
        d = d[key]
    # Update the value at the final key
    d[paths[-1]] = new_value
    return data
def get_all_key_values(keys=None,dict_obj=None):
    keys = keys or []
    dict_obj = dict_obj or {}
    new_dict_obj = {}
    for key in keys:
        values = dict_obj.get(key)
        if values:
            new_dict_obj[key]=values
    return new_dict_obj

def get_all_values(keys=None,dict_obj=None):
    keys = keys or []
    dict_obj = dict_obj or {}
    values=[]
    for key in keys:
        value = dict_obj.get(key)
        if value:
            values.append(value)
    return values

def safe_update_json_datas(
    json_data: dict,
    update_data: dict,
    valid_keys: list[str] | None = None,
    invalid_keys: list[str] | None = None
) -> dict:
    """
    - If valid_keys is provided (non-empty), only update keys in that list.
    - Else if invalid_keys is provided, update all keys except those in invalid_keys,
      and delete any existing keys that are in invalid_keys.
    - Else update every key.
    In all cases, overwrite values unconditionally.
    """
    valid = set(make_list(valid_keys or []))
    invalid = set(make_list(invalid_keys or []))

    for key, value in update_data.items():
        if valid:
            if key in valid:
                json_data[key] = value
        elif invalid:
            if key in invalid:
                json_data.pop(key, None)
            else:
                json_data[key] = value
        else:
            json_data[key] = value

    return json_data

def get_json_file_path(file_path,data=None):
    data = data or {}
    if not os.path.isfile(file_path):
        safe_dump_to_file(data={},file_path=file_path)
    return file_path

def get_json_file_data(file_path):
    if os.path.isfile(file_path):
        return safe_load_from_json(file_path)

def get_create_json_data(file_path,data=None):
    get_json_file_path(file_path,data=data)
    return get_json_file_data(file_path)

def get_json_data(file_path):
    file_path = get_file_path(file_path)
    data = safe_read_from_json(file_path)
    return data

def save_updated_json_data(data,file_path):
    data = data or {}
    new_data = get_json_data(file_path)
    new_data.update(data)
    safe_dump_to_file(new_data,file_path)
    
def safe_updated_json_data(
    data,
    file_path,
    valid_keys=None,
    invalid_keys=None
):
    update_data = data or {}
    json_data = get_create_json_data(file_path, data={})
    new_data = safe_update_json_datas(
        json_data=json_data,
        update_data=update_data,
        valid_keys=valid_keys,
        invalid_keys=invalid_keys   # ← now correct
    )
    return new_data
def safe_save_updated_json_data(data,
                            file_path,
                            valid_keys=None,
                            invalid_keys=None
                            ):
    new_data = safe_updated_json_data(data=data,
                            file_path=file_path,
                            valid_keys=valid_keys,
                            invalid_keys=invalid_keys
                            )    
    safe_dump_to_file(new_data,file_path)
    return new_data

def get_result_from_data(key,func,**data):
    result_data = func(**data)
    result = result_data.get(key)
    return result

def to_json_safe(obj):
    if obj is None:
        return None

    if isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    if isinstance(obj, Decimal):
        return float(obj)

    if isinstance(obj, Path):
        return str(obj)

    if isinstance(obj, dict):
        return {k: to_json_safe(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple, set)):
        return [to_json_safe(v) for v in obj]

    # Fallback (yt-dlp objects, enums, etc.)
    return str(obj)
