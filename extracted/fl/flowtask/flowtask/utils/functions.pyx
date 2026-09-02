# cython: language_level=3, embedsignature=True, boundscheck=False, wraparound=True, initializedcheck=False
# Copyright (C) 2018-present Jesus Lara
#
"""
Main Functions for DataIntegrator.
"""
import os
import re
import ast
from pandas import DataFrame
from libcpp cimport bool as bool_t
from cpython cimport datetime
from cpython.datetime cimport datetime as dt
from cpython.datetime cimport time as dtime

"""
 Filename Operations.
"""

cpdef str filename(str path):
    return os.path.basename(path)


cpdef str file_extension(str path):
    return os.path.splitext(os.path.basename(path))[1][1:].strip().lower()


"""
 Other Utilities.
"""
cpdef object extract_path(str value, str regex, bool_t to_date = False, bool_t to_datetime = False, str mask = "%m/%d/%Y"):
    p = re.compile(regex)
    if p:
        try:
            found = re.search(regex, value)
            result = found.group(1)
            if to_date:
                result = dt.strptime(result, mask).date()
            if to_datetime:
                result = dt.strptime(result, mask)
            return result
        except Exception as err:
            return None
    else:
        return None

cpdef str extract_string(str value, str exp = r"_((\d+)_(\d+))_", int group = 1, bool_t parsedate = False, list masks = ["%Y-%m-%d %H:%M:%S"]):
    match = re.search(r"{}".format(exp), value)
    if match:
        if not parsedate:
            result = match.group(group)
        else:
            val = match.group(group)
            result = None
            for mask in masks:
                try:
                    result = dt.strptime(val, mask)
                    break
                except ValueError:
                    continue
            if result is None:
                # Fallback to dateutil for non-standard formats
                from dateutil.parser import parse as _dateutil_parse
                result = _dateutil_parse(val)
        return result

cpdef bool_t check_empty(object obj):
    """check_empty.
    Check if a basic object is empty or not.
    """
    if isinstance(obj, DataFrame):
        return True if obj.empty else False
    else:
        return bool(not obj)

is_empty = check_empty

cpdef bool_t as_boolean(object value):
    """as_boolean.
    Converting any value to a boolean.
    """
    if isinstance(value, bool):
        return value
    try:
        return ast.literal_eval(value)
    except ValueError:
        return False


cpdef list get_worker_list(list workers):
    """Convert a list of workers in a tuple of worker:port for Scheduler."""
    wl = []
    for worker in workers:
        w,p = worker.split(':')
        wl.append((w, p))
    return wl

cpdef str snake_case(str s):
    """Convert string to snake-case."""
    s = re.sub(r'[^a-zA-Z0-9]', ' ', s)  # Replace non-alphanumeric characters with spaces
    s = re.sub(r'\s+', '_', s)  # Replace one or more spaces with underscores
    s = re.sub(r'_+', '_', s)  # Replace multiple consecutive underscores with a single underscore
    return s.lower().strip('_')
