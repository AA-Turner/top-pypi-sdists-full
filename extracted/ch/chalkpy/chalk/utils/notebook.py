import ast
import enum
import functools
import inspect
import sys
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Callable, Optional, Union

from chalk.utils._ast_extract import is_module_level_definition
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
For testing, this variable can be set to simulate running inside a notebook. If `None`, ignored. If `True`/`False`, that value is returned by is_notebook().
Note that `is_notebook()` caches its results to must be called _after_ setting this value.
"""


@functools.lru_cache(maxsize=None)
def _is_notebook() -> bool:
    """:return: `True` if running inside a Jupyter notebook"""
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


def _strip_ipython_magics(cell_source: str) -> str:
    """Replace IPython line magics (`%foo`), cell magics (`%%foo` and the rest of
    the cell), and shell escapes (`!cmd`, `?obj`) with blank lines, preserving
    overall line numbers so ast line/column offsets continue to align with the
    original cell text used by ast.get_source_segment."""
    out_lines: list[str] = []
    in_cell_magic = False
    for line in cell_source.splitlines(keepends=True):
        stripped = line.lstrip()
        ending = "\n" if line.endswith("\n") else ""
        if in_cell_magic:
            out_lines.append(ending)
            continue
        if stripped.startswith("%%"):
            in_cell_magic = True
            out_lines.append(ending)
            continue
        if stripped.startswith("%") or stripped.startswith("!") or stripped.startswith("?"):
            out_lines.append(ending)
            continue
        out_lines.append(line)
    return "".join(out_lines)


def _source_with_decorators(cell_source: str, node: Union["ast.FunctionDef", "ast.ClassDef"]) -> Optional[str]:
    """Like ast.get_source_segment, but for decorated FunctionDef/ClassDef nodes
    prepend the decorator lines that ast.get_source_segment otherwise drops
    (CPython sets `node.lineno` to the `def`/`class` keyword, not the first `@`)."""
    base = ast.get_source_segment(cell_source, node)
    if base is None:
        return None
    decorators = node.decorator_list
    if not decorators:
        return base
    lines = cell_source.splitlines(keepends=True)
    first_decorator_lineno = min(d.lineno for d in decorators)  # 1-indexed
    def_lineno = node.lineno  # 1-indexed; points at `def`/`class`
    prefix = "".join(lines[first_decorator_lineno - 1 : def_lineno - 1])
    return prefix + base


def _names_from_target(target: ast.AST) -> list[str]:
    """Extract all bound names from an assignment target, recursing into Tuple/List/Starred."""
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, (ast.Tuple, ast.List)):
        names: list[str] = []
        for elt in target.elts:
            names.extend(_names_from_target(elt))
        return names
    if isinstance(target, ast.Starred):
        return _names_from_target(target.value)
    return []  # Subscript / Attribute — not a new global binding


def _parse_notebook_cells(cells: list[tuple[int, int, str]]):
    """Parse notebook cells and extract definitions of functions, classes, globals, and imports."""
    import ast

    latest_function_def: dict[str, tuple[str, ast.AST]] = {}  # name -> (source, ast_node)
    latest_global_assign: dict[str, str] = {}  # name -> source
    latest_class_def: dict[str, tuple[str, ast.AST]] = {}  # name -> (source, ast_node)
    all_imports: dict[str, tuple[list[str], ast.AST]] = {}  # import_text -> (names_imported, ast_node)

    for _, _, cell_source in cells:
        if not cell_source.strip():
            continue

        # Strip IPython magics/shell escapes before parsing, but keep line
        # numbers aligned so ast.get_source_segment still works on the sanitized
        # source.
        sanitized = _strip_ipython_magics(cell_source)

        try:
            cell_tree = ast.parse(sanitized)
        except SyntaxError:
            continue

        for node in cell_tree.body:
            # Definition-shaped nodes only; side-effect statements (top-level
            # calls, control flow) are dropped. Per-kind branches below route
            # each into its own name-keyed dict.
            if not is_module_level_definition(node):
                continue
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                import_source = ast.get_source_segment(sanitized, node)
                if import_source is None:
                    continue
                imported_names = _get_import_names(node, sanitized, import_source)
                all_imports[import_source] = (list(imported_names), node)

            elif isinstance(node, ast.FunctionDef):
                func_source = _source_with_decorators(sanitized, node)
                if func_source is not None:
                    latest_function_def[node.name] = (func_source, node)

            elif isinstance(node, ast.ClassDef):
                class_source = _source_with_decorators(sanitized, node)
                if class_source is not None:
                    latest_class_def[node.name] = (class_source, node)

            elif isinstance(node, ast.Assign):
                assign_source = ast.get_source_segment(sanitized, node)
                if assign_source is None:
                    continue
                for target in node.targets:
                    for name in _names_from_target(target):
                        latest_global_assign[name] = assign_source

            elif isinstance(node, ast.AnnAssign):
                if node.value is None or not isinstance(node.target, ast.Name):
                    # Bare annotations (`x: int`) carry no value to ship; skip.
                    continue
                assign_source = ast.get_source_segment(sanitized, node)
                if assign_source is not None:
                    latest_global_assign[node.target.id] = assign_source

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
    """Recursively collect dependencies needed by the function and emit them in
    topological (post-order) order, so that base classes appear before subclasses
    and globals appear before the helpers that use them."""
    needed_functions: dict[str, str] = {}
    needed_classes: dict[str, str] = {}
    needed_globals: dict[str, str] = {}
    needed_names: set[str] = set()
    visiting: set[str] = set()

    def visit(name: str) -> None:
        if name in visiting:
            return
        if name in needed_classes or name in needed_functions or name in needed_globals:
            return
        visiting.add(name)
        if name in latest_class_def:
            class_source, _ = latest_class_def[name]
            for ref in _get_referenced_names(class_source) - builtin_names - {fn_name, name}:
                needed_names.add(ref)
                visit(ref)
            needed_classes[name] = class_source
        elif name in latest_function_def:
            func_source, _ = latest_function_def[name]
            for ref in _get_referenced_names(func_source) - builtin_names - {fn_name, name}:
                needed_names.add(ref)
                visit(ref)
            needed_functions[name] = func_source
        elif name in latest_global_assign:
            needed_globals[name] = latest_global_assign[name]

    for ref in _get_referenced_names(fn_source) - builtin_names - {fn_name}:
        needed_names.add(ref)
        visit(ref)

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


def assemble_module_for_class(cls: type) -> str:
    """Reconstruct a self-contained Python module that defines ``cls``, pulling
    only the dependency closure of helpers/imports/constants from Jupyter cell
    history.

    Must be called from inside a Jupyter notebook. Walks the IPython history,
    parses cells with ``_parse_notebook_cells``, then reuses the same
    ``_collect_dependencies`` / ``_filter_imports`` / ``_build_script``
    pipeline that ``parse_notebook_into_script`` uses for training functions.
    The output therefore contains only the imports, globals, and helper
    classes/functions actually referenced by ``cls`` (transitively), with the
    target class appended last so siblings/bases resolve first.

    Caveat: name resolution is purely textual — references introduced via
    ``getattr(module, "name")`` or string-keyed config lookups will not be
    detected. If a user hits this they should pass the missing dependency
    through ``register_model_version(dependencies=[...])`` or refactor.

    Raises
    ------
    RuntimeError
        Not running inside a notebook, or IPython history isn't accessible.
    ValueError
        ``cls.__name__`` was never defined at the top level of any cell.
    """
    import builtins as _builtins

    if not is_notebook():
        raise RuntimeError("assemble_module_for_class should only be called from a notebook environment.")

    shell = get_ipython_or_none()
    if shell is None:
        raise RuntimeError("Could not access IPython shell")
    if getattr(shell, "history_manager", None) is None:
        raise RuntimeError("Could not access IPython history manager")

    history_manager = shell.history_manager
    session_number = history_manager.get_last_session_id()
    cells = list(history_manager.get_range(session=session_number, start=1))

    latest_function_def, latest_class_def, latest_global_assign, all_imports = _parse_notebook_cells(cells)

    if cls.__name__ not in latest_class_def:
        raise ValueError(
            f"@model_handler class {cls.__name__!r} was not found in the notebook's cell history. Make sure the class is defined at the top level of a cell (not inside a function or `if` block) and that the cell has been executed."
        )

    target_src, _target_node = latest_class_def[cls.__name__]
    builtin_names = set(dir(_builtins))

    needed_functions, needed_classes, needed_globals, needed_names = _collect_dependencies(
        target_src,
        cls.__name__,
        latest_function_def,
        latest_class_def,
        latest_global_assign,
        builtin_names,
    )
    needed_imports = _filter_imports(all_imports, needed_names)

    script = _build_script(
        target_src,
        cls.__name__,
        needed_imports,
        needed_globals,
        needed_classes,
        needed_functions,
    )

    if not is_valid_python_code(script):
        raise RuntimeError(f"Error generating valid module source for class {cls.__name__!r} from notebook")
    return script


def validate_train_script(script: str, function_name: str, takes_argument: bool) -> None:
    """Validate that ``script`` is a syntactically valid Python module that
    defines a top-level ``def {function_name}`` with the expected arity
    (0 if ``takes_argument`` is False, 1 if True).

    Raises:
        RuntimeError: if ``script`` is not valid Python.
        ValueError: if the named function is missing or has the wrong arity.
    """
    if not is_valid_python_code(script):
        raise RuntimeError("Provided train script is not valid Python.")
    tree = ast.parse(script)
    matching = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == function_name]
    if not matching:
        raise ValueError(f"Function '{function_name}' not found at the top level of the training script.")
    fn_node = matching[-1]  # last definition wins, matching Python semantics
    nargs = len(fn_node.args.args)
    expected = int(takes_argument)
    if nargs != expected:
        raise ValueError(
            f"Function '{function_name}' must take {expected} inputs, but has parameters: "
            + f"{[a.arg for a in fn_node.args.args]}"
        )


def resolve_train_script(
    train_fn: Callable[..., Any],
    train_script: Optional[str],
    takes_argument: bool,
) -> str:
    """Produce the Python source string to ship for ``train_fn``.

    Resolution order:
      1. If ``train_script`` is provided, validate and return it as-is.
      2. If running inside a Jupyter notebook, reconstruct via ``parse_notebook_into_script``.
      3. Otherwise, read the entire ``.py`` file ``train_fn`` is defined in.
    """
    if train_script is not None:
        validate_train_script(train_script, train_fn.__name__, takes_argument)
        return train_script

    if is_notebook():
        return parse_notebook_into_script(train_fn, takes_argument)

    try:
        source_path = inspect.getfile(train_fn)
    except TypeError as e:
        raise RuntimeError(
            f"Could not locate the source file for `{train_fn.__name__}`. "
            + "When calling `client.train_model` outside a Jupyter notebook, either "
            + "define `train_fn` in a regular `.py` file or pass `train_script=` explicitly."
        ) from e

    try:
        with open(source_path, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError as e:
        raise RuntimeError(
            f"Could not read source file `{source_path}` for `{train_fn.__name__}`: {e}. "
            + "Pass `train_script=` explicitly to bypass file lookup."
        ) from e

    validate_train_script(source, train_fn.__name__, takes_argument)
    return source


def resolve_script_entrypoint(script: str, entrypoint: Optional[str] = None) -> str:
    """Determine the entry-point function name for a self-contained training script.

    If ``entrypoint`` is provided, it is returned as-is (existence and arity are
    verified later by :func:`validate_train_script`). Otherwise the script must
    define exactly one top-level function, whose name is returned.
    """
    if entrypoint is not None:
        return entrypoint
    if not is_valid_python_code(script):
        raise RuntimeError("Provided train script is not valid Python.")
    tree = ast.parse(script)
    top_level_fns = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    if not top_level_fns:
        raise ValueError("train_script must define at least one top-level function.")
    if len(top_level_fns) > 1:
        raise ValueError(
            f"train_script defines multiple top-level functions: {top_level_fns}. Specify an entrypoint function name with the 'entrypoint' parameter."
        )
    return top_level_fns[0]
