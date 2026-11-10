"""Shared standard-library imports, external dependencies, and helpers."""

from .init_imports import (
    re, shlex, os, json, tempfile, decimal, uuid, textwrap, math, hashlib,
    glob, dataclasses, unicodedata, fnmatch, importlib, shutil, sys, time,
    threading, posixpath, types, logging, string, subprocess, queue,
    functools, pkgutil, inspect, Any, Callable, Literal, Optional, Protocol,
    Tuple, Union, Iterable, Iterator, Mapping, Dict, List, Set, get_args,
    datetime, date, timezone, Path, reduce, lru_cache, MethodType, ModuleType,
    dataclass, field, SequenceMatcher, format_datetime,
)
from .module_imports import (
    FrameLite, light_stack,
    combineList, compare_lists, ensure_nested_list, filter_json_list_values,
    find_original_case, get_actual_number, get_highest_value_obj,
    get_single_from_list, get_sort, get_symetric_difference, list_set,
    make_list, make_list_add, make_list_it, recursive_json_list,
    remove_from_list, safe_list_return, pexpect, ezodf, tiktoken, gpd, PyPDF2,
    pdfplumber, pd, pytesseract, convert_from_path, FileStorage,
)
from .functions import (
    _LazyCallable, _lazy_module, _lazy_type, jsonify, load_dotenv,
    secure_filename,
)

