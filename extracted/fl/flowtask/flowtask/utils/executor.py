"""
Function Executor.
"""
import logging
import traceback
import importlib
from typing import Any
import builtins
from collections.abc import Callable
from querysource.types.validators import Entity
import querysource.utils.functions as qsfunctions
from . import functions as ffunctions


def getFunction(fname: str) -> callable:
    """
    Get any function using name.
    """
    try:
        return getattr(qsfunctions, fname)
    except (TypeError, AttributeError):
        pass
    try:
        return getattr(ffunctions, fname)
    except (TypeError, AttributeError):
        pass
    try:
        func = globals().get(fname)
        if func:
            return func
    except AttributeError:
        pass
    try:
        return getattr(builtins, fname)
    except AttributeError:
        pass
    # If the function name contains dots, try to import the module and get the attribute
    if '.' in fname:
        components = fname.split('.')
        module_name = '.'.join(components[:-1])
        attr_name = components[-1]

        try:
            module = importlib.import_module(module_name)
            func = getattr(module, attr_name)
            return func
        except (ImportError, AttributeError) as e:
            # Function doesn't exists:
            print(f'Cannot find Module {e}')
    logging.warning(
        f"Function {fname} not found in any known modules."
    )
    return None


def fnExecutor(
    value: Any, env: Callable = None, escape: bool = False, quoting: bool = False
) -> Any:
    if isinstance(value, list):
        try:
            fname, args = (value + [{}])[:2]  # Safely unpack with default args
            func = getFunction(fname)
            if not func:
                logging.warning(
                    f"Function {fname} doesn't exist in Builtins or Flowtask."
                )
                return None
            if isinstance(args, list):
                try:
                    return func(*args)
                except Exception as e:
                    print("FN > ", e)
                    traceback.print_exc()
                    return ""
            if isinstance(args, dict):
                if env is not None:
                    args["env"] = env
                try:
                    try:
                        return func(**args)
                    except TypeError:
                        if "env" in args:
                            del args["env"]
                        return func(**args)
                    except Exception as e:
                        print("FN > ", e)
                except (TypeError, ValueError) as err:
                    logging.exception(
                        str(err),
                        exc_info=True,
                        stack_info=True
                    )
                    traceback.print_exc()
                    return ""
            else:
                try:
                    return func()
                except (TypeError, ValueError):
                    return ""
        except (NameError, KeyError) as err:
            logging.exception(str(err), exc_info=True, stack_info=True)
            traceback.print_exc()
            return ""
    else:
        if isinstance(value, str):
            if escape is True:
                return f"'{str(value)}'"
            elif quoting is True:
                return Entity.quoteString(value)
            else:
                return f"{str(value)}"
        return value
