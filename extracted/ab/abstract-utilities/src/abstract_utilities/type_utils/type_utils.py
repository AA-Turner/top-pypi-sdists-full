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
