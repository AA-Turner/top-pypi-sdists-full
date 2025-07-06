# ----------------------------------------------------------------------------
# Description    : Docstring helper functions
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2023)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------
import re
from functools import partial
from inspect import signature
from typing import Callable, Optional, Union

# -- decorator ---------------------------------------------------------------


def copy_docstr(
    src_func: Callable, params_to_add: Union[dict[str, tuple[str, str]], None] = None
) -> Callable:
    """
    Decorator that copies the docstring from the provided function to the
    decorated function.

    Parameters
    ----------
    src_func
        Function from which to copy the docstring.
    params_to_add : dict[str, tuple[str, str]]
        Dictionary of parameters to add to the parameters in the docstring.
        The keys must be the parameter names, and the values must be a
        two element tuple containing the parameter type and description.
    """
    if params_to_add is None:
        params_to_add = {}

    def actual_copy_docstr(func) -> Callable:
        doc = src_func.__doc__
        for param_name, p in params_to_add.items():
            param_type, param_description = p
            doc = add_parameters_to_doc(
                lines=doc,
                param_name=param_name,
                param_type=param_type,
                param_description=param_description,
            )
        func.__doc__ = doc
        return func

    return actual_copy_docstr


# ------------------------------------------------------------------------


def get_indent(line: str) -> int:
    """
    Gets the indent (amount of spaces before a non-space character) for a line.
    """
    for i, s in enumerate(line):
        if not s.isspace():
            return i
    return len(line)


# ------------------------------------------------------------------------


def get_min_indent(lines: list[str]) -> int:
    """
    Gets the minimum indent for a list of lines.
    """
    min_indent = None
    for line in lines:
        if line:
            cur_indent = get_indent(line)
            if min_indent is None or cur_indent < min_indent:
                min_indent = cur_indent
    return min_indent or 0


# ------------------------------------------------------------------------


def get_initial_indent(lines: list[str]) -> int:
    """
    Gets the indent of the first line with content
    """
    for line in lines:
        if line:
            return get_indent(line)


# ------------------------------------------------------------------------


def add_indent(lines: list[str], spaces: int = 4) -> list[str]:
    """
    Adds an n-space indent to every line in a list of lines.
    """
    return [(" " * spaces) + line for line in lines if line]


# ------------------------------------------------------------------------


def remove_parameter_from_doc(
    lines: str, param_name: str, initial_indent: Union[int, None] = 0
) -> str:
    """
    Removes the named parameter from the documentation string.

    Parameters
    ----------
    lines: str
        The documentation string
    param_name: str
        Name of the parameter to be removed
    initial_indent: int
        The initial indent of the documentation string provided. Default 0

    Returns
    ----------
    str
        The documentation string with the parameter removed.
    """
    if initial_indent is None:
        initial_indent = get_initial_indent(lines.splitlines())
    try:
        params_start = next(re.finditer("Parameters\n[ -]*?\n", lines)).span()[1]
    except StopIteration:  # No parameters section was found, return as-is
        return lines

    try:  # Parameters might be the last section of the docstring
        params_end = next(re.finditer("\n *-+?\n", lines[params_start:])).span()[0]
    except StopIteration:  # Take until the end if we can't find another separator
        params_end = len(lines)

    params = lines[params_start:][:params_end]
    param_start = next(
        re.finditer(f" {{{initial_indent}}}?" + re.escape(param_name), params)
    ).span()[0]

    try:  # Parameters might be the last section of the docstring
        param_end = next(
            re.finditer(f"\n {{{initial_indent}}}?" + r"\S", params[param_start + initial_indent :])
        ).span()[0]
    except StopIteration:  # Take until the end if we can't find another separator
        param_end = len(lines)

    return (
        lines[: params_start + param_start]
        + lines[params_start + param_start :][param_end + initial_indent :]
    )


# ------------------------------------------------------------------------


def add_parameters_to_doc(
    lines: str,
    param_name: str,
    param_description: str = "",
    param_type: Optional[str] = None,
    indent: int = 4,
    initial_indent: Union[int, None] = None,
) -> str:
    """
    Adds the named parameter from the documentation string.

    Parameters
    ----------
    lines: str
        The documentation string
    param_name: str
        Name of the parameter to be removed
    param_description: str
        Description of parameter
    param_type: str
        String representation of parameter type
    indent: int
        The indent of the documentation string provided. Default 4
    initial_indent: int
        The initial indent of the documentation string provided.

    Returns
    ----------
    str
        The documentation string with the parameter added.
    """
    if initial_indent is None:
        initial_indent = get_initial_indent(lines.splitlines())

    params_start = next(re.finditer("Parameters\n[ -]*?\n", lines)).span()[1]
    param_add_str = " " * initial_indent + param_name
    if param_type:
        param_add_str += " : " + param_type
    param_add_str += (
        "\n"
        + " " * initial_indent
        + " " * indent
        + param_description
        + "\n"
        + " " * initial_indent
        + "\n"
    )
    return lines[:params_start] + param_add_str + lines[params_start:]


# ------------------------------------------------------------------------


def get_parameters_from_doc(lines: str) -> dict[str, str]:
    """
    Gets all parameters, types and description from the documentation string.

    Parameters
    ----------
    lines: str
        The documentation string

    Returns
    ----------
    dict[str, str]
        Dictionary of parameters with the name as key, and a tuple with param type and description.
    """
    all_parameters_regex = re.compile(
        r'[\s\S]*Parameters[\s]*[=\-`:\'"~^_*+#<>]{2,}[\s]*'
        + r'(?P<all_p>[\s\S]+?)(?=\n\n.*\n[\s]*[=\-`:\'"~^_*+#<>]{2,})'
    )
    param_and_type_regex = re.compile(r"^\s*([0-9A-Za-z_]{1}[A-Za-z_]*)\s*:?\s*([A-Za-z,\[\]]*)$")
    result = all_parameters_regex.match(lines)
    parameters_dict = {}
    if result:
        all_parameters = result.groups()[0].splitlines()
        for p in range(len(all_parameters) // 2):
            p_result = param_and_type_regex.match(all_parameters[2 * p])
            param_name, param_type = p_result.groups()
            description = all_parameters[2 * p + 1].lstrip()
            parameters_dict[param_name] = (param_type, description)
    return parameters_dict


# ------------------------------------------------------------------------


def partial_with_numpy_doc(func, /, *args, end_with="", **kwargs) -> Callable:
    """
    Same as functools.partial, but removes the relevant parameter from docstring.

    Parameters
    ----------
    func : Callable
        The method to make a partial method of.
    *args
        Arguments passed to partial
    end_with : str
        String to add to end of documentation.
        It will be indented to match the previous documentation.
    **kwargs
        Keyword arguments passed to partial

    Returns
    ----------
    Callable
        Partial function.
    """
    partial_func = partial(func, *args, **kwargs)

    parent_doc = func.__doc__
    initial_indent = get_initial_indent(parent_doc.splitlines())

    parent_args = list(signature(func).parameters.keys())
    for idx in range(len(args)):
        # remove the relevant arg from doc
        parent_doc = remove_parameter_from_doc(
            lines=parent_doc,
            param_name=parent_args[idx],
            initial_indent=initial_indent,
        )

    end_with = add_indent(end_with.splitlines(), initial_indent)
    end_with = "\n".join(end_with)

    new_doc = parent_doc.rstrip() + "\n" + end_with + "\n" + " " * initial_indent
    partial_func.__doc__ = new_doc

    return partial_func
