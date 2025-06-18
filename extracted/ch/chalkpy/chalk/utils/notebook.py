import enum
import functools
import inspect
import sys
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Optional

from chalk.utils.environment_parsing import env_var_bool

if TYPE_CHECKING:
    from chalk.sql._internal.sql_file_resolver import SQLStringResult


def print_user_error(message: str, exception: Optional[Exception] = None, suggested_action: Optional[str] = None):
    print(f"\033[91mERROR: {message}\033[0m", file=sys.stderr)

    if exception is not None:
        print(f"\033[93mDetails: {str(exception)}\033[0m", file=sys.stderr)

    if suggested_action is not None:
        print(f"\033[94mSuggested action: {suggested_action}.\033[0m", file=sys.stderr)


class IPythonEvents(enum.Enum):
    SHELL_INITIALIZED = "shell_initialized"
    PRE_EXECUTE = "pre_execute"
    PRE_RUN_CELL = "pre_run_cell"
    POST_EXECUTE = "post_execute"
    POST_RUN_CELL = "post_run_cell"


def get_ipython_or_none() -> Optional[object]:
    """
    Returns the global IPython shell object, if this code is running in an ipython environment.
    :return: An `IPython.core.interactiveshell.InteractiveShell`, or None if we're not running in a notebook/ipython repl
    """
    try:
        # This method only exists if we're running inside an ipython env
        return get_ipython()  # type: ignore
    except NameError:
        return None  # Probably standard Python interpreter


_is_notebook_override: bool = env_var_bool("CHALK_IS_NOTEBOOK_OVERRIDE")

"""
For testing, this variable can be set to simulate running inside a notebook. If None, ignored. If true/false, that value is returned by is_notebook().
Note that `is_notebook()` caches its results to must be called _after_ setting this value.
"""


@functools.lru_cache(maxsize=None)
def _is_notebook() -> bool:
    """:return: true if run inside a Jupyter notebook"""
    if _is_notebook_override:
        return True
    shell = get_ipython_or_none()
    if shell is None:
        return False
    # Check MRO since some envs (e.g. DataBricks) subclass the kernel
    for c in shell.__class__.__mro__:
        cname: str = c.__name__
        if cname == "ZMQInteractiveShell":
            return True
        if cname == "TerminalInteractiveShell":
            return False  # ipython running in terminal
    return False


def is_notebook() -> bool:
    # Delegate so it's easier to monkeypatch
    return _is_notebook()


notebook_features_loaded: ContextVar[bool] = ContextVar("notebook_features_loaded", default=False)


def check_in_notebook(msg: Optional[str] = None):
    if not is_notebook():
        if msg is None:
            msg = "Not running inside a Jupyter kernel."
        raise RuntimeError(msg)


def is_defined_in_module(obj: Any) -> bool:
    """
    Whether the given object was defined in a module that was imported, or if it's defined at the top level of a shell/script.
    :return: True if object was defined inside a module.
    """
    m = inspect.getmodule(obj)
    if m is None:
        return False
    return m.__name__ != "__main__"


def is_defined_in_cell_magic(obj: Any) -> bool:
    from chalk.features import Resolver

    if isinstance(obj, Resolver):
        return obj.is_cell_magic
    return False


def register_resolver_from_cell_magic(sql_string_result: "SQLStringResult"):
    """Registers a resolver from the %%sql_resolver cell magic.
    Parameters
    ----------
    sql_string_result
    """
    from chalk.sql._internal.sql_file_resolver import NOTEBOOK_DEFINED_SQL_RESOLVERS, get_sql_file_resolver
    from chalk.sql._internal.sql_source import BaseSQLSource

    if sql_string_result.path == "":
        print_user_error(
            "Resolver name is required, but none found. Please add a name to the first line of the cell, like %%resolver my_resolver.",
        )
        return

    resolver_result = get_sql_file_resolver(
        sources=BaseSQLSource.registry, sql_string_result=sql_string_result, has_import_errors=False
    )
    if resolver_result.errors:
        errs = [e.display for e in resolver_result.errors]
        err_message = "\n".join(errs)

        print_user_error(
            f"Failed to parse notebook-defined SQL resolver '{sql_string_result.path}'. Found the following errors:\n{err_message}",
        )
        return

    NOTEBOOK_DEFINED_SQL_RESOLVERS[sql_string_result.path] = resolver_result
