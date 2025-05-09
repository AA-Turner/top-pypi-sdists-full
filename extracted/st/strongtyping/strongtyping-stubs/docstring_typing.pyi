import typing
from _typeshed import Incomplete
from strongtyping._utils import action as action, remove_subclass as remove_subclass
from strongtyping.cached_set import CachedSet as CachedSet
from strongtyping.strong_typing import TypeMismatch as TypeMisMatch

TYPE_EXTRACTION_PATTERN: str
PATTERN_1: str
EXTRACT_PARAM_NAME_PATTERN: str
TUPLE_PATTERN: str
PATTERN: str
OR_PATTERN: str
COMMA_PATTERN: str
REMOVE_PATTERN: str
FM_PATTERN: str

def separate_param_type(docstring_type_part: str) -> tuple: ...

possible_types: Incomplete

def param_attr(attr: str): ...
def get_container_types(ttype_of: str) -> typing.Union[None, tuple]: ...
def get_or_types(ttype: str) -> list: ...
def is_tuple(arg, type_of: str): ...
def is_list(arg, type_of: str): ...
def is_dict(arg, type_of: str): ...
def is_set(arg, type_of: str): ...
def is_function_or_method_type(arg, type_of): ...

options: Incomplete

def check_doc_str_type(arg, type_of): ...
def is_type_info(docstring_line: str) -> bool: ...
def is_param_info(docstring_line: str) -> bool: ...
def extract_docstring_param_types(func) -> dict: ...
def match_docstring(_func: Incomplete | None = ..., *, excep_raise: Exception = ..., cache_size: int = ..., subclass: bool = ..., severity: str = ..., **kwargs): ...
def match_class_docstring(_cls: Incomplete | None = ..., *, excep_raise: Exception = ..., cache_size: int = ..., severity: str = ..., **kwargs): ...
def getter(func): ...
def setter(func): ...
def getter_setter(func): ...
