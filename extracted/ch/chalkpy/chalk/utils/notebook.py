import enum
import functools
import inspect
from typing import TYPE_CHECKING, Any, List, Optional

from chalk.parsed.duplicate_input_gql import FailedImport
from chalk.utils.environment_parsing import env_var_bool

if TYPE_CHECKING:
    from chalk.sql._internal.sql_file_resolver import SQLStringResult


class IPythonEvents(enum.Enum):
    SHELL_INITIALIZED = "shell_initialized"
    PRE_EXECUTE = "pre_execute"
    PRE_RUN_CELL = "pre_run_cell"
    POST_EXECUTE = "post_execute"
    POST_RUN_CELL = "post_run_cell"


@functools.lru_cache(maxsize=None)
def get_ipython_string() -> Optional[str]:
    """
    :return: "ZMQInteractiveShell" for jupyter notebook, "TerminalInteractiveShell" for ipython in terminal, None otherwise.
    """
    try:
        # I know this has a redline under it... we'll catch the NameError as a Falsy condition below
        # noinspection PyUnresolvedReferences
        shell = get_ipython().__class__.__name__  # type: ignore
        return shell
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
    shell = get_ipython_string()
    return shell == "ZMQInteractiveShell"


def is_notebook() -> bool:
    # Delegate so it's easier to monkeypatch
    return _is_notebook()


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


def register_resolver_from_cell_magic(sql_string_result: "SQLStringResult") -> List[FailedImport]:
    """Registers a resolver from the %%resolver cell magic.

    Parameters
    ----------
    sql_string_result

    Returns
    -------
    list[FailedImport]
        A list of errors that occurred during registration.
    """
    from chalk.sql._internal.sql_file_resolver import get_sql_file_resolver
    from chalk.sql._internal.sql_source import BaseSQLSource

    if sql_string_result.path == "":
        return [
            FailedImport(
                traceback="Resolver name is required, but none found. Please add a name to the first line of the cell, like %%resolver my_resolver",
                filename="",
                module="",
            )
        ]

    result = get_sql_file_resolver(
        sources=BaseSQLSource.registry,
        sql_string_result=sql_string_result,
    )

    if result.resolver is not None:

        result.resolver.is_cell_magic = True
        result.resolver.add_to_registry(override=True)

    return [
        FailedImport(
            traceback=error.display,
            filename=error.path,
            module=error.path,
        )
        for error in result.errors
    ]
