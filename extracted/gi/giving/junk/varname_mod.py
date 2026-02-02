import ast
import warnings
from typing import Tuple, Union

from varname.ignore import IgnoreType
from varname.utils import (
    ImproperUseError,
    MultiTargetAssignmentWarning,
    VarnameRetrievingError,
    get_node,
    node_name,
)


def lookfor_immediate_parent_assign(
    node: ast.AST,
) -> Union[ast.Assign, ast.AnnAssign]:
    """Look for an ast.Assign node in the immediate parent"""
    print(node)
    if hasattr(node, "parent"):
        node = node.parent

        if isinstance(node, (ast.AnnAssign, ast.Assign, ast.NamedExpr)):
            return node
    return None


def varname(
    frame: int = 1,
    ignore: IgnoreType = ["give"],
    multi_vars: bool = False,
    raise_exc: bool = True,
) -> Union[str, Tuple[Union[str, Tuple], ...]]:
    """Get the name of the variable(s) that assigned by function call or
    class instantiation.
    To debug and specify the right frame and ignore arguments, you can set
    debug on and see how the frames are ignored or selected:
    >>> from varname import config
    >>> config.debug = True
    Args:
        frame: `N`th frame used to retrieve the variable name. This means
            `N-1` intermediate frames will be skipped. Note that the frames
            match `ignore` will not be counted. See `ignore` for details.
        ignore: Frames to be ignored in order to reach the `N`th frame.
            These frames will not be counted to skip within that `N-1` frames.
            You can specify:
            - A module (or filename of a module). Any calls from it and its
                submodules will be ignored.
            - A function. If it looks like it might be a decorated function,
                a `MaybeDecoratedFunctionWarning` will be shown.
            - Tuple of a function and a number of additional frames that should
                be skipped just before reaching this function in the stack.
                This is typically used for functions that have been decorated
                with a 'classic' decorator that replaces the function with
                a wrapper. In that case each such decorator involved should
                be counted in the number that's the second element of the tuple.
            - Tuple of a module (or filename) and qualified name (qualname).
                You can use Unix shell-style wildcards to match the qualname.
                Otherwise the qualname must appear exactly once in the
                module/file.
            By default, all calls from `varname` package, python standard
            libraries and lambda functions are ignored.
        multi_vars: Whether allow multiple variables on left-hand side (LHS).
            If `True`, this function returns a tuple of the variable names,
            even there is only one variable on LHS.
            If `False`, and multiple variables on LHS, a
            `ImproperUseError` will be raised.
        raise_exc: Whether we should raise an exception if failed
            to retrieve the ast node.
            Note that set this to `False` will not supress the exception when
            the use of `varname` is improper (i.e. multiple variables on
            LHS with `multi_vars` is `False`). See `Raises/ImproperUseError`.
    Returns:
        The variable name, or `None` when `raise_exc` is `False` and
            we failed to retrieve the variable name.
        A tuple or a hierarchy (tuple of tuples) of variable names
            when `multi_vars` is `True`.
    Raises:
        VarnameRetrievingError: When there is invalid variables or
            invalid number of variables used on the LHS; or
            when we are unable to retrieve the variable name and `raise_exc`
            is set to `True`.
        ImproperUseError: When the use of `varname()` is improper. For example:
            - When LHS is not an `ast.Name` or `ast.Attribute` node or not a
                list/tuple of them
            - When there are multiple variables on LHS but `multi_vars` is False
        UserWarning: When there are multiple target
            in the assign node. (e.g: `a = b = func()`, in such a case,
            `b == 'a'`, may not be the case you want)
    """
    # Skip one more frame, as it is supposed to be called
    # inside another function
    node = get_node(frame + 1, ignore, raise_exc=raise_exc)
    if not node:
        if raise_exc:
            raise VarnameRetrievingError("Unable to retrieve the ast node.")
        return None

    node = lookfor_immediate_parent_assign(node)
    if not node:
        if raise_exc:
            raise VarnameRetrievingError("Failed to retrieve the variable name.")
        return None

    if isinstance(node, ast.AnnAssign):
        target = node.target
    else:
        # Need to actually check that there's just one
        # give warnings if: a = b = func()
        if len(node.targets) > 1:
            warnings.warn(
                "Multiple targets in assignment, variable name "
                "on the very left will be used.",
                MultiTargetAssignmentWarning,
            )
        target = node.targets[0]

    names = node_name(target)

    if not isinstance(names, tuple):
        names = (names,)

    if multi_vars:
        return names

    if len(names) > 1:
        raise ImproperUseError(
            f"Expect a single variable on left-hand side, got {len(names)}."
        )

    return names[0]
