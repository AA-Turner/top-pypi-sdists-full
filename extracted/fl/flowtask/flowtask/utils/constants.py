import builtins
import logging
import re
from collections.abc import Callable
import querysource.utils.functions as qsfunctions  # pylint: disable=W0401,C0411
from . import functions as ffunctions  # pylint: disable=W0614,W0401
from querysource.utils.functions import *

### Constants Utilities for Flowtask
DI_CONSTANTS = [
    "CURRENT_DATE",
    "CURRENT_TIMESTAMP",
    "CURRENT_YEAR",
    "CURRENT_MONTH",
    "CURRENT_MIDNIGHT",
    "YESTERDAY_TIMESTAMP",
    "YESTERDAY_MIDNIGHT",
    "TODAY",
    "YESTERDAY",
    "FDOM",
    "LDOM",
]

excel_based = (
    "application/vnd.ms-excel.sheet.binary.macroEnabled.12",  # XLSB
    "application/vnd.ms-excel.sheet.macroEnabled.12",  # XLSM
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # XLSX
    "application/vnd.ms-excel",  # XLS
    "text/xml",  # XML
)


it_func = re.compile(r"^(\w+)\((.*)\)")


def is_constant(value):
    return value in DI_CONSTANTS


def is_function(value):
    if "(" in str(value):
        fn, _ = it_func.match(value).groups()
        # also, I need to know if exists on global values
        func = globals()[fn]
        if not func:
            try:
                func = getattr(ffunctions, value)
            except AttributeError:
                try:
                    func = getattr(qsfunctions, value)
                except AttributeError:
                    func = None
        if not func:
            return False
        else:
            return True
    else:
        return False


def get_func_value(value):
    result = None
    f, args = it_func.match(value).groups()
    args = args.split(",")
    logging.debug(
        f'Conditions: Calling function {value}, {f}'
    )
    try:
        try:
            func = getattr(ffunctions, f)
        except AttributeError:
            try:
                func = getattr(qsfunctions, f)
            except AttributeError:
                func = globals()[f]
        if not func:
            try:
                func = getattr(builtins, f)
            except AttributeError:
                return None
        if callable(func):
            result = func(*args)
    except Exception as err:
        logging.exception(err)
    finally:
        return result


def get_constant(value: str, *args, **kwargs) -> Callable:
    fn = None
    try:
        f = value.lower()
        print(
            f':::: Conditions: Calling function {value}, {f}'
        )
        if value in DI_CONSTANTS:
            fn = globals()[f](*args, **kwargs)
        else:
            try:
                func = getattr(ffunctions, f)
            except AttributeError:
                try:
                    func = getattr(qsfunctions, f)
                except AttributeError:
                    func = globals()[f]
            if not func:
                try:
                    func = getattr(builtins, f)
                except AttributeError:
                    return None
            if func and callable(func):
                try:
                    fn = func(*args, **kwargs)
                except Exception as err:
                    raise Exception(err) from err
    finally:
        return fn
