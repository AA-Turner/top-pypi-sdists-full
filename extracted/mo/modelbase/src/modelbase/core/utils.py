from __future__ import annotations

__all__ = [
    "ascii_to_character",
    "check_function_arity",
    "convert_id_to_sbml",
    "convert_sbml_id",
    "escape_non_alphanumeric",
    "functionify_lambda",
    "get_formatted_function_source_code",
    "get_function_source_code",
    "patch_lambda_function_name",
    "warning_on_one_line",
    "MissingDependencies",
    "CircularDependency",
]


import inspect
import re
import subprocess
import warnings
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

RE_LAMBDA_FUNC = re.compile(r".*(lambda)(.+?):(.*?)")
RE_LAMBDA_RATE_FUNC = re.compile(r".*(lambda)(.+?):(.*?),")
RE_LAMBDA_ALGEBRAIC_MODULE_FUNC = re.compile(r".*(lambda)(.+?):(.*[\(\[].+[\)\]]),")
RE_TO_SBML = re.compile(r"([^0-9_a-zA-Z])")
RE_FROM_SBML = re.compile(r"__(\d+)__")
SBML_DOT = "__SBML_DOT__"


def warning_on_one_line(
    message: Warning | str,
    category: type[Warning],
    _filename: str,
    _lineno: int,
    _line: int | None = None,
) -> str:  # type: ignore
    """Format warnings to only show the message."""
    return f"{category.__name__}: {message}\n"


warnings.formatwarning = warning_on_one_line  # type: ignore


##########################################################################
# Source code functions
##########################################################################


def check_function_arity(function: Callable, arity: int) -> bool:
    """Check if the amount of arguments given fits the argument count of the function"""
    argspec = inspect.getfullargspec(function)
    # Give up on *args functions
    if argspec.varargs is not None:
        return True

    # The sane case
    if len(argspec.args) == arity:
        return True

    # It might be that the user has set some args to default values,
    # in which case they are also ok (might be kwonly as well)
    defaults = argspec.defaults
    if defaults is not None and len(argspec.args) + len(defaults) == arity:
        return True
    kwonly = argspec.kwonlyargs
    if defaults is not None and len(argspec.args) + len(kwonly) == arity:
        return True
    return False


def get_function_source_code(function: Callable) -> str | None:
    """Get source code of a function."""
    try:
        return inspect.getsource(function)[:-1]  # Remove line break
    except OSError:
        pass
    try:
        # for functions parsed and dynamically executed with modelbase/sbml/parser
        source: str = function.__source__  # type: ignore
        return source
    except AttributeError:
        return None


def patch_lambda_function_name(function: Callable, name: str) -> None:
    """Add a name to a lambda function."""
    if function.__name__ == "<lambda>":
        function.__name__ = name


def functionify_lambda(
    lambda_function_code: str, function_name: str, pattern: re.Pattern[str]
) -> str:
    """Convert lambda function to a proper function."""
    match = re.match(pattern=pattern, string=lambda_function_code)
    if match is None:
        msg = "Could not find pattern"
        raise ValueError(msg)
    _, args, code = match.groups()
    return f"def {function_name}({args.strip()}):\n    return {code.strip()}"


def get_formatted_function_source_code(
    function_name: str, function: Callable, function_type: str
) -> str:
    """Get source code of a function and format it using black."""
    source = get_function_source_code(function=function)

    if source is None:
        msg = "Cannot find function source"
        raise ValueError(msg)

    if "lambda" in source:
        if function_type == "rate":
            source = functionify_lambda(
                lambda_function_code=source,
                function_name=function_name,
                pattern=RE_LAMBDA_RATE_FUNC,
            )
        elif function_type == "module":
            source = functionify_lambda(
                lambda_function_code=source,
                function_name=function_name,
                pattern=RE_LAMBDA_ALGEBRAIC_MODULE_FUNC,
            )
        elif function_type == "function":
            source = functionify_lambda(
                lambda_function_code=source,
                function_name=function_name,
                pattern=RE_LAMBDA_FUNC,
            )
        else:
            msg = "Can only handle rate or module functions"
            raise ValueError(msg)
    blacked_string = subprocess.run(
        ["black", "--fast", "--code", source], stdout=subprocess.PIPE, check=True
    )
    return blacked_string.stdout.decode("utf-8").strip()  # Removing new lines


##########################################################################
# SBML functions
##########################################################################


def escape_non_alphanumeric(re_sub: Any) -> str:
    """Convert a non-alphanumeric charactor to a string representation of its ascii number."""
    return f"__{ord(re_sub.group(0))}__"


def ascii_to_character(re_sub: Any) -> str:
    """Convert an escaped non-alphanumeric character."""
    return chr(int(re_sub.group(1)))


def convert_id_to_sbml(id_: str, prefix: str) -> str:
    """Add prefix if id startswith number."""
    new_id = RE_TO_SBML.sub(escape_non_alphanumeric, id_).replace(".", SBML_DOT)
    if not new_id[0].isalpha():
        return f"{prefix}_{new_id}"
    return new_id


def convert_sbml_id(sbml_id: str, prefix: str) -> str:
    """Convert an model object id to sbml-compatible string.

    Adds a prefix if the id starts with a number.
    """
    new_id = sbml_id.replace(SBML_DOT, ".")
    new_id = RE_FROM_SBML.sub(ascii_to_character, new_id)
    return new_id.lstrip(f"{prefix}_")


##########################################################################
# Sorting dependencies
##########################################################################


class MissingDependencies(Exception):
    """Raised when dependencies cannot be sorted topologically.

    This typically indicates circular dependencies in model components.
    """

    def __init__(self, not_solvable: dict[str, list[str]]) -> None:
        """Initialise exception."""

        missing_by_module = "\n".join(f"\t{k}: {v}" for k, v in not_solvable.items())
        msg = (
            f"Dependencies cannot be solved. "
            "Missing dependencies:\n"
            f"{missing_by_module}"
        )
        super().__init__(msg)


class CircularDependency(Exception):
    """Raised when dependencies cannot be sorted topologically.

    This typically indicates circular dependencies in model components.
    """

    def __init__(
        self,
        missing: dict[str, set[str]],
    ) -> None:
        missing_by_module = "\n".join(f"\t{k}: {v}" for k, v in missing.items())

        """Initialise exception."""
        msg = (
            f"Exceeded max iterations on sorting dependencies.\n"
            "Check if there are circular references. "
            "Missing dependencies:\n"
            f"{missing_by_module}"
        )
        super().__init__(msg)


def _check_if_is_sortable_single(
    available: set[str],
    elements: list[tuple[str, set[str]]],
) -> None:
    all_available = available.copy()
    for name, _ in elements:
        all_available.add(name)

    # Check if it can be sorted in the first place
    not_solvable = {}
    for name, args in elements:
        if not args.issubset(all_available):
            not_solvable[name] = sorted(args.difference(all_available))

    if not_solvable:
        raise MissingDependencies(not_solvable=not_solvable)


def _check_if_is_sortable_multiple(
    available: set[str],
    elements: list[tuple[str, list[str], set[str]]],
) -> None:
    all_available = available.copy()
    for _, der, _ in elements:
        all_available.update(der)

    # Check if it can be sorted in the first place
    not_solvable = {}
    for name, _, args in elements:
        if not args.issubset(all_available):
            not_solvable[name] = sorted(args.difference(all_available))

    if not_solvable:
        raise MissingDependencies(not_solvable=not_solvable)


def _sort_dependencies(
    available: set[str], elements: list[tuple[str, set[str]]]
) -> list[str]:
    """Sort model elements topologically based on their dependencies.

    Args:
        available: Set of available component names
        elements: List of (name, dependencies) tuples to sort

    Returns:
        List of element names in dependency order

    Raises:
        SortError: If circular dependencies are detected

    """
    from queue import Empty, SimpleQueue

    _check_if_is_sortable_single(available, elements)

    order = []
    # FIXME: what is the worst case here?
    max_iterations = len(elements) ** 2
    queue: SimpleQueue[tuple[str, set[str]]] = SimpleQueue()
    for k, v in elements:
        queue.put((k, v))

    last_name = None
    i = 0
    while True:
        try:
            new, args = queue.get_nowait()
        except Empty:
            break
        if args.issubset(available):
            available.add(new)
            order.append(new)
        else:
            if last_name == new:
                order.append(new)
                break
            queue.put((new, args))
            last_name = new
        i += 1

        # Failure case
        if i > max_iterations:
            unsorted: list[str] = []
            while True:
                try:
                    unsorted.append(queue.get_nowait()[0])
                except Empty:  # noqa: PERF203
                    break

            mod_to_args: dict[str, set[str]] = dict(elements)
            missing = {k: mod_to_args[k].difference(available) for k in unsorted}
            raise CircularDependency(missing=missing)
    return order


def _sort_dependencies_multiple(
    available: set[str], elements: list[tuple[str, list[str], set[str]]]
) -> list[str]:
    """Sort model elements topologically based on their dependencies.

    Args:
        available: Set of available component names
        elements: List of (name, dependencies) tuples to sort

    Returns:
        List of element names in dependency order

    Raises:
        SortError: If circular dependencies are detected

    """
    from queue import Empty, SimpleQueue

    _check_if_is_sortable_multiple(available, elements)

    order = []
    # FIXME: what is the worst case here?
    max_iterations = len(elements) ** 2
    queue: SimpleQueue[tuple[str, list[str], set[str]]] = SimpleQueue()
    for k, derived, args in elements:
        queue.put((k, derived, args))

    last_name = None
    i = 0
    while True:
        try:
            k, derived, args = queue.get_nowait()
        except Empty:
            break
        if args.issubset(available):
            order.append(k)
            for cpd in derived:
                available.add(cpd)
        else:
            if last_name == k:
                order.append(k)
                break
            queue.put((k, derived, args))
            last_name = k
        i += 1

        # Failure case
        if i > max_iterations:
            unsorted = []
            while True:
                try:
                    unsorted.append(queue.get_nowait()[0])
                except Empty:  # noqa: PERF203
                    break

            mod_to_args = {k: args for k, _, args in elements}
            missing = {k: mod_to_args[k].difference(available) for k in unsorted}

            raise CircularDependency(missing=missing)
    return order
