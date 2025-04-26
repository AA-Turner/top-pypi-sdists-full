from __future__ import annotations

import ast
import builtins
import inspect
from types import FrameType
from typing import Any, Callable, Dict, Optional, Type, Union

from executing import Source

from chalk.features._chalkop import op
from chalk.features.feature_field import Feature
from chalk.features.feature_wrapper import FeatureWrapper
from chalk.features.filter import Filter
from chalk.utils.collections import get_unique_item


class ExecutingException(Exception):
    pass


class RetrievingError(ExecutingException):
    pass


def _get_node_by_frame(frame: FrameType, raise_exc: bool = True) -> Optional[ast.AST]:
    """Get the node by frame, raise errors if possible"""
    exect = Source.executing(frame)

    if exect.node:
        # attach the frame for better exception message
        # (i.e. where ImproperUseError happens)
        exect.node.__frame__ = frame  # type: ignore
        return exect.node

    assert isinstance(exect.source, Source)
    if exect.source.text and exect.source.tree and raise_exc:
        raise RetrievingError(
            (
                "Couldn't retrieve the call node. "
                "This may happen if you're using some other AST magic at the "
                "same time, such as pytest, ipython, macropy, or birdseye."
            )
        )

    return None


def _get_func_frame_and_nodes(condition: Callable[[Optional[ast.AST]], bool]):
    frame = inspect.currentframe()
    assert frame is not None
    # We want to go back 3 frames -- get out of this function, out of parse_feature_iter, and out
    # of df __getitem__
    frame = frame.f_back
    assert frame is not None
    frame = frame.f_back
    assert frame is not None
    frame = frame.f_back
    while frame is not None:
        func_node = _get_node_by_frame(frame)
        if condition(func_node):
            # This is the correct getitem frame.
            # It is important that the "slice" isn't an ast.Name,
            # as otherwise it would be impossible to parse the expression
            # ast.Name would imply something like this:
            # def __getitem__(self, item):
            #    return self.df[item]  # <--- item is of type ast.name. We need to go one frame higher!
            return frame, func_node
        frame = frame.f_back
    raise RuntimeError("Condition not found in stack")


def parse_feature_iter(f: Feature | FeatureWrapper | Any):
    _, func_node = _get_func_frame_and_nodes(lambda node: isinstance(node, ast.Call))
    if not isinstance(func_node, ast.Call):
        raise RuntimeError("Could not evaluate function")
    if not isinstance(func_node.func, ast.Name):
        raise RuntimeError("Could not evaluate function")
    func_name = func_node.func.id
    if func_name == "sum":
        return op.sum(f)
    elif func_name == "max":
        return op.max(f)
    elif func_name == "min":
        return op.min(f)

    raise RuntimeError(f"Could not evaluate function {func_name}")


def parse_dataframe_getitem():
    func_frame, func_node = _get_func_frame_and_nodes(
        lambda node: isinstance(node, ast.Subscript) and not isinstance(node.slice, ast.Name)
    )
    assert isinstance(func_node, ast.Subscript)
    slc = func_node.slice
    if isinstance(slc, ast.Index):
        slc = slc.value  # type: ignore
        assert isinstance(slc, ast.expr)
    converted_slice = convert_slice(slc)
    return eval_converted_expr(converted_slice, glbs=func_frame.f_globals, lcls=func_frame.f_locals)


def parse_inline_setattr_annotation(key: str) -> Optional[Type[Any]]:
    """Parses the type annotation for inline feature definitions."""
    # Get the frame when the attribute is set
    frame = inspect.currentframe()
    for _ in range(2):
        assert frame is not None
        frame = frame.f_back
    assert frame is not None

    try:
        source = Source.executing(frame)
        node = source.node
        parent_node = node.parent

        if isinstance(parent_node, ast.AnnAssign) and isinstance(node, ast.Attribute):
            attribute_name = node.attr
            if attribute_name == key:
                if isinstance(parent_node.annotation, ast.Name):
                    type_name = parent_node.annotation.id

                    if hasattr(builtins, type_name):
                        return getattr(builtins, type_name)
                    elif type_name in frame.f_globals:
                        return frame.f_globals[type_name]
    except:
        raise TypeError(f"Failed to parse type annotation for feature {key}.")
    return None


def parse_when() -> Optional[Filter]:
    func_frame, func_node = _get_func_frame_and_nodes(lambda node: isinstance(node, ast.Call))
    assert isinstance(func_node, ast.Call)
    when = next((k for k in func_node.keywords if k.arg == "when"), None)
    when_filter = convert_slice(when.value) if when else None
    assert isinstance(when_filter, ast.expr)
    return (
        eval_converted_expr(when_filter, glbs=func_frame.f_globals, lcls=func_frame.f_locals) if when_filter else None
    )


def _convert_maybe_tuple(slc: ast.expr):
    if isinstance(slc, ast.Tuple):
        return ast.Tuple(
            elts=[_convert_ops(x) for x in slc.elts],
            ctx=slc.ctx,
        )
    else:
        assert isinstance(slc, ast.expr)
        return _convert_ops(slc)


def convert_slice(slc: Union[ast.expr, ast.Index]):
    if isinstance(slc, ast.Index):
        # Index is deprecated in Python 3.9+
        slc = slc.value  # type: ignore
        assert isinstance(slc, ast.expr)
        slc = _convert_maybe_tuple(slc)
        return ast.Index(value=slc)  # pyright: ignore[reportCallIssue]
    return _convert_maybe_tuple(slc)


def eval_converted_expr(expr: ast.AST, glbs: Optional[Dict[str, Any]] = None, lcls: Optional[Dict[str, Any]] = None):
    expr.lineno = 1  # pyright: ignore[reportAttributeAccessIssue]
    expr.col_offset = 0  # pyright: ignore[reportAttributeAccessIssue]
    expr.end_lineno = 1  # pyright: ignore[reportAttributeAccessIssue]
    expr.end_col_offset = 0  # pyright: ignore[reportAttributeAccessIssue]
    expression = ast.Expression(body=expr)  # pyright: ignore[reportArgumentType]
    ast.fix_missing_locations(expression)
    glbs = dict(glbs or {})  # shallow copy
    # Inject the __CHALK_FILTER__ so the converted "in" and "not in" expressions can be parsed
    glbs["__CHALK_FILTER__"] = Filter
    return eval(compile(expression, filename="<string>", mode="eval"), glbs, lcls)  # nosemgrep: eval-detected


def _convert_ops(stmt: ast.expr):
    """Recursively convert operations so that they can be parsed by the filters"""
    if isinstance(stmt, ast.BoolOp):
        assert len(stmt.values) >= 2, "bool ops need at least two values"
        op: ast.operator
        if isinstance(stmt.op, ast.And):
            op = ast.BitAnd()
        elif isinstance(stmt.op, ast.Or):
            op = ast.BitOr()
        else:
            raise ValueError(f"Invalid op: {stmt.op}")
        values = list(stmt.values)
        ans = _convert_ops(values.pop())
        while len(values) > 0:
            left = values.pop()
            ans = ast.BinOp(
                left=_convert_ops(left),
                op=op,
                right=ans,
            )
        return ans
    if isinstance(stmt, ast.UnaryOp):
        if isinstance(stmt.op, ast.Not):
            return ast.UnaryOp(
                op=ast.Invert(),
                operand=_convert_ops(stmt.operand),
            )
        return stmt
    if isinstance(stmt, ast.Compare):
        if len(stmt.ops) == 1:
            lhs = stmt.left
            rhs = get_unique_item(stmt.comparators)
            compare_op: ast.cmpop = get_unique_item(stmt.ops)
            # Replace is with == and isnot with !=
            # It doesn't make sense to have identity checks in a dataframe filter

            if isinstance(compare_op, ast.Is):
                return ast.Compare(left=lhs, ops=[ast.Eq()], comparators=[rhs])
            if isinstance(compare_op, ast.IsNot):
                return ast.Compare(left=lhs, ops=[ast.NotEq()], comparators=[rhs])

            if isinstance(compare_op, (ast.In, ast.NotIn)):
                filter_op = "in" if isinstance(compare_op, ast.In) else "not in"
                return ast.Call(
                    func=ast.Name(id="__CHALK_FILTER__", ctx=ast.Load()),
                    args=[
                        stmt.left,
                        ast.Constant(value=filter_op),
                        rhs,
                    ],
                    keywords=[],
                )
        return stmt
    return stmt
