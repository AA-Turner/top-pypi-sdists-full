import ast
import enum
import functools
import inspect
import sys
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Callable, Optional, Union

from chalk.utils.environment_parsing import env_var_bool

if TYPE_CHECKING:
    from chalk.sql._internal.sql_file_resolver import SQLStringResult

    try:
        from ipython.core.interactiveshell import InteractiveShell  # type: ignore
    except ImportError:
        InteractiveShell = Any  # type: ignore


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


def get_ipython_or_none() -> Optional[Any]:
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


def is_valid_python_code(code_string: str):
    try:
        compile(code_string, "<string>", "exec")
        return True
    except (SyntaxError, ValueError):
        return False


def _get_import_names(node: Union[ast.Import, ast.ImportFrom], cell_source: str, import_source: str) -> set[str]:
    """Extract the names that an import statement brings into scope."""
    import ast

    imported_names = set()
    if isinstance(node, ast.Import):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            imported_names.add(name)
    else:  # ast.ImportFrom
        for alias in node.names:
            if alias.name == "*":
                # Can't track wildcard imports precisely, so include the import text itself
                imported_names.add(import_source)
            else:
                name = alias.asname if alias.asname else alias.name
                imported_names.add(name)
    return imported_names


def _parse_notebook_cells(cells: list[tuple[int, int, str]]):
    """Parse notebook cells and extract definitions of functions, classes, globals, and imports."""
    import ast

    latest_function_def: dict[str, tuple[str, ast.AST]] = {}  # name -> (source, ast_node)
    latest_global_assign: dict[str, str] = {}  # name -> source
    latest_class_def: dict[str, tuple[str, ast.AST]] = {}  # name -> (source, ast_node)
    all_imports: dict[str, tuple[list[str], ast.AST]] = {}  # import_text -> (names_imported, ast_node)

    for _, _, cell_source in cells:
        cell_source = cell_source.strip()
        if not cell_source:
            continue

        try:
            cell_tree = ast.parse(cell_source)
        except SyntaxError:
            continue

        for node in cell_tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                import_source = ast.get_source_segment(cell_source, node)
                if import_source is None:
                    continue
                imported_names = _get_import_names(node, cell_source, import_source)
                all_imports[import_source] = (list(imported_names), node)

            elif isinstance(node, ast.FunctionDef):
                func_source = ast.get_source_segment(cell_source, node)
                if func_source is not None:
                    latest_function_def[node.name] = (func_source, node)

            elif isinstance(node, ast.ClassDef):
                class_source = ast.get_source_segment(cell_source, node)
                if class_source is not None:
                    latest_class_def[node.name] = (class_source, node)

            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assign_source = ast.get_source_segment(cell_source, node)
                        if assign_source is not None:
                            latest_global_assign[target.id] = assign_source

    return latest_function_def, latest_class_def, latest_global_assign, all_imports


def _get_referenced_names(source_code: str) -> set[str]:
    """Extract all names referenced in source code."""
    import ast

    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return set()

    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            # For module.function, capture the base module
            if isinstance(node.value, ast.Name):
                names.add(node.value.id)
    return names


def _collect_dependencies(
    fn_source: str,
    fn_name: str,
    latest_function_def: dict[str, tuple[str, ast.AST]],
    latest_class_def: dict[str, tuple[str, ast.AST]],
    latest_global_assign: dict[str, str],
    builtin_names: set[str],
):
    """Recursively collect all dependencies needed by the function."""
    # maps name -> source
    needed_functions: dict[str, str] = {}
    needed_classes: dict[str, str] = {}
    needed_globals: dict[str, str] = {}
    needed_names: set[str] = set()

    to_process = [fn_source]
    processed = set()

    while to_process:
        current_source = to_process.pop()
        if current_source in processed:
            continue
        processed.add(current_source)

        referenced = _get_referenced_names(current_source)
        referenced = referenced - builtin_names - {fn_name}
        needed_names.update(referenced)

        for name in referenced:
            # Check if it's a class we defined
            if name in latest_class_def and name not in needed_classes:
                class_source, _ = latest_class_def[name]
                needed_classes[name] = class_source
                to_process.append(class_source)

            # Check if it's a function we defined
            elif name in latest_function_def and name not in needed_functions:
                func_source, _ = latest_function_def[name]
                needed_functions[name] = func_source
                to_process.append(func_source)

        for name in referenced:
            # Check if it's a global variable we defined
            if name in latest_global_assign and name not in needed_globals:
                assign_source = latest_global_assign[name]
                needed_globals[name] = assign_source
                to_process.append(assign_source)

    return needed_functions, needed_classes, needed_globals, needed_names


def _filter_imports(all_imports: dict[str, tuple[list[str], ast.AST]], needed_names: set[str]) -> list[str]:
    """Filter imports to only include those that are actually used."""
    needed_imports: list[str] = []
    for import_text, (imported_names, _) in all_imports.items():
        if any(name in needed_names or name == import_text for name in imported_names):
            needed_imports.append(import_text)
    return needed_imports


def _build_script(
    fn_source: str,
    fn_name: str,
    needed_imports: list[str],
    needed_globals: dict[str, str],
    needed_classes: dict[str, str],
    needed_functions: dict[str, str],
) -> str:
    """Build the final script from collected components."""
    script_parts: list[str] = []

    if needed_imports:
        script_parts.extend(needed_imports)
        script_parts.append("")

    if needed_globals:
        script_parts.extend(needed_globals.values())
        script_parts.append("")

    if needed_classes:
        script_parts.extend(needed_classes.values())
        script_parts.append("")

    if needed_functions:
        script_parts.extend(needed_functions.values())
        script_parts.append("")

    script_parts.append(fn_source)

    return "\n".join(script_parts)


def parse_notebook_into_script(fn: Callable[[], None], takes_argument: bool) -> str:
    """
    Parse a notebook function and its dependencies into a standalone Python script.

    The function must take no inputs and produce no outputs. The output script will
    call fn() in __main__ and include all necessary imports, globals, and helper
    functions that have been executed in the notebook.

    Args:
        fn (Callable[[], None]): A callable with no parameters and no return value.

    Returns:
        str: A Python script as a string.
    """
    import builtins

    if not is_notebook():
        raise RuntimeError("parse_notebook_into_script should only be called from a notebook environment.")

    sig = inspect.signature(fn)
    if len(sig.parameters) != int(takes_argument):
        raise ValueError(
            f"Function {fn.__name__} must take {int(takes_argument)} inputs, but has parameters: {list(sig.parameters.keys())}"
        )

    shell = get_ipython_or_none()
    if shell is None:
        raise RuntimeError("Could not access IPython shell")

    # Get the cell contents of executed cells
    if getattr(shell, "history_manager", None) is None:
        raise RuntimeError("Could not access IPython history manager")

    history_manager = shell.history_manager
    session_number = history_manager.get_last_session_id()
    cells = list(history_manager.get_range(session=session_number, start=1))

    # Parse cells to extract definitions
    latest_function_def, latest_class_def, latest_global_assign, all_imports = _parse_notebook_cells(cells)

    # Get function source and collect dependencies
    fn_source = inspect.getsource(fn)
    builtin_names = set(dir(builtins))

    needed_functions, needed_classes, needed_globals, needed_names = _collect_dependencies(
        fn_source, fn.__name__, latest_function_def, latest_class_def, latest_global_assign, builtin_names
    )

    # Filter imports to only used ones
    needed_imports = _filter_imports(all_imports, needed_names)

    # Build and return the script
    script = _build_script(fn_source, fn.__name__, needed_imports, needed_globals, needed_classes, needed_functions)

    if not is_valid_python_code(script):
        raise RuntimeError("Error generating valid training function from notebook")

    return script
