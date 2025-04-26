from __future__ import annotations

import ast
from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from sqlglot.expressions import Select, Union

from chalk.parsed.duplicate_input_gql import PositionGQL, RangeGQL


def node_to_range(node: ast.AST) -> RangeGQL | None:
    if (
        getattr(node, "lineno", None) is None
        or getattr(node, "col_offset", None) is None
        or getattr(node, "end_lineno", None) is None
        or getattr(node, "end_col_offset", None) is None
    ):
        return None
    return RangeGQL(
        start=PositionGQL(
            line=getattr(node, "lineno"),
            character=getattr(node, "col_offset"),
        ),
        end=PositionGQL(
            line=getattr(node, "end_lineno"),
            character=getattr(node, "end_col_offset"),
        ),
    )


def get_class_definition_range(cls: ast.ClassDef, filename: str) -> RangeGQL:
    with open(filename) as f:
        lines = f.readlines()

    line_length = len(lines[cls.lineno - 1]) if cls.lineno < len(lines) else len("class ") + len(cls.name)
    return RangeGQL(
        start=PositionGQL(
            line=cls.lineno,
            character=0,
        ),
        end=PositionGQL(
            line=cls.lineno,
            character=max(line_length - 1, 1),
        ),
    )


def get_decorator_kwarg_value_range(cls: ast.ClassDef, kwarg: str) -> ast.AST | None:
    for stmt in cls.decorator_list:
        if isinstance(stmt, ast.Call):
            for keyword in stmt.keywords:
                if keyword.arg == kwarg:
                    return keyword.value
    return None


def get_property_range(cls: ast.ClassDef, name: str) -> ast.AST | None:
    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == name:
            return stmt.target

        elif isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            target = stmt.targets[0]
            if isinstance(target, ast.Name) and target.id == name:
                return target

    return None


def get_property_value_call_range(cls: ast.ClassDef, name: str, kwarg: str) -> ast.AST | None:
    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == name:
            if stmt.value is None:
                return None
            value = stmt.value
            if isinstance(value, ast.Call):
                for k in value.keywords:
                    if k.arg == kwarg:
                        return k.value

        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            target = stmt.targets[0]
            if isinstance(target, ast.Name) and target.id == name:
                value = stmt.value
                if isinstance(value, ast.Call):
                    for k in value.keywords:
                        if k.arg == kwarg:
                            return k.value

    return None


def get_property_value_range(cls: ast.ClassDef, name: str) -> ast.AST | None:
    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == name:
            if stmt.value is None:
                return None

            return stmt.value

        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            target = stmt.targets[0]
            if isinstance(target, ast.Name) and target.id == name:
                return stmt.value

    return None


def get_annotation_range(cls: ast.ClassDef, name: str) -> ast.AST | None:
    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == name:
            return stmt.annotation

    return None


_RESOLVER_DECORATORS = {"online", "offline", "realtime", "batch", "stream", "sink"}


def get_function_decorator_range(node: ast.FunctionDef | ast.AsyncFunctionDef) -> ast.AST | None:
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name):
            decorator_name = decorator.id
        elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
            decorator_name = decorator.func.id
        else:
            return None
        if decorator_name in _RESOLVER_DECORATORS:
            return decorator

    return None


def get_function_decorator_arg_by_name(node: ast.FunctionDef | ast.AsyncFunctionDef, name: str) -> ast.AST | None:
    """gets args to the decorator call.

    Returns range of parameter by name if exists.
    Returns None if no decorator
    Returns decorator range if name doesn't exist or no parameters exist
    """
    decorator = get_function_decorator_range(node)
    if not isinstance(decorator, ast.Call):
        return decorator
    for keyword in decorator.keywords:
        if keyword.arg == name:
            return keyword.value

    return None


def get_function_arg_values(node: ast.FunctionDef | ast.AsyncFunctionDef) -> Dict[str, ast.AST | None]:
    return {stmt.arg: stmt for stmt in node.args.args}


def get_key_from_dict_node(node: ast.Dict, name: str) -> ast.AST | None:
    for key, _ in zip(node.keys, node.values):
        if isinstance(key, ast.Constant) and key.value == name:
            return key
    return None


def get_value_from_dict_node(node: ast.Dict, name: str) -> ast.AST | None:
    for key, value in zip(node.keys, node.values):
        if isinstance(key, ast.Constant) and key.value == name:
            return value
    return None


def get_function_arg_annotations(node: ast.FunctionDef | ast.AsyncFunctionDef) -> Dict[str, ast.AST | None]:
    return {stmt.arg: stmt.annotation for stmt in node.args.args}


class _ChalkFunctionReturnFinder(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.nodes = []

    def visit_Return(self, node: ast.Return) -> None:
        self.nodes.append(node)
        self.generic_visit(node)


def get_function_return_statement(node: ast.FunctionDef | ast.AsyncFunctionDef) -> List[ast.AST | None]:
    returns = []
    return_finder = _ChalkFunctionReturnFinder()
    return_finder.visit(node)
    for return_stmt in return_finder.nodes:
        returns.append(return_stmt)
    return returns


def get_function_return_annotation(node: ast.FunctionDef | ast.AsyncFunctionDef) -> ast.AST | None:
    return node.returns


def get_missing_return_annotation(node: ast.FunctionDef | ast.AsyncFunctionDef, uri: str) -> RangeGQL | None:
    with open(uri, "r") as f:
        content = f.read()

    lines = content.split("\n")
    if node.args.args:
        if node.args.args[-1].end_lineno is None or node.args.args[-1].end_col_offset is None:
            return None
        line_no = node.args.args[-1].end_lineno
        col_offset = node.args.args[-1].end_col_offset + 1
    else:
        if node.lineno is None or node.col_offset is None:  # pyright: ignore[reportUnnecessaryComparison]
            return None
        line_no = node.lineno
        col_offset = node.col_offset

    start_line = line_no - 1
    start_char = max(col_offset - 1, 0)

    for i in range(start_line, len(lines)):
        line = lines[i]
        start_char_in_line = start_char if i == start_line else 0
        for j in range(start_char_in_line, len(line)):
            if line[j] == ":":
                return RangeGQL(
                    start=PositionGQL(
                        line=i + 1,
                        character=j,
                    ),
                    end=PositionGQL(
                        line=i + 1,
                        character=j + 1,
                    ),
                )


def get_function_name(node: ast.FunctionDef | ast.AsyncFunctionDef, uri: str) -> RangeGQL | None:
    with open(uri, "r") as f:
        content = f.read()

    lines = content.split("\n")
    line_no = node.lineno
    col_offset = node.col_offset

    start_line = line_no - 1
    start_char = max(col_offset - 1, 0)

    found_def = False
    def_start_line_no = None
    def_start_col_offset = None
    for i in range(start_line, len(lines)):
        line = lines[i]
        start_char_in_line = start_char if i == start_line else 0
        for j in range(start_char_in_line, len(line)):
            if line[0:j] == "def":
                found_def = True
            if found_def:
                if def_start_line_no is None:
                    if not line[j].isspace():
                        def_start_line_no = i
                        def_start_col_offset = j
                if def_start_line_no is not None and def_start_col_offset is not None:
                    if line[j] == "(":
                        return RangeGQL(
                            start=PositionGQL(
                                line=def_start_line_no + 1,
                                character=def_start_col_offset,
                            ),
                            end=PositionGQL(
                                line=i + 1,
                                character=j,
                            ),
                        )
    return None


def get_comment_range(lines: List[str], name: str) -> RangeGQL | None:
    for i, line in enumerate(lines):
        if line.lstrip().startswith("--"):
            line_without_comment = line.lstrip().lstrip("--").lstrip()
            split = line_without_comment.split(":")
            if len(split) != 2:
                """this is a docstring, not a comment"""
                continue
            if line_without_comment.startswith(name):
                """this is our correct line. We want to return the value after the ':'"""
                colon_index = line.index(":")
                offset_start = colon_index + 1
                value_string = line[offset_start:]
                start_line_index = end_line_index = i
                if value_string == "" or value_string.isspace():
                    """This field is a dict or list rather than a value. Let's return the key"""
                    offset_start = len(line) - len(line_without_comment)
                else:
                    start_line_index = end_line_index = i
                if lines[start_line_index][offset_start:] != lines[start_line_index][offset_start:].lstrip():
                    while lines[start_line_index][offset_start].isspace():
                        offset_start += 1
                offset_end = len(lines[end_line_index])
                if (
                    lines[end_line_index][:offset_end] != lines[end_line_index][:offset_end].rstrip()
                    or lines[end_line_index][offset_end - 1] == ":"
                ):
                    while (
                        lines[end_line_index][offset_end - 1].isspace() or lines[end_line_index][offset_end - 1] == ":"
                    ):
                        offset_end -= 1

                return RangeGQL(
                    start=PositionGQL(
                        line=start_line_index + 1,
                        character=offset_start,
                    ),
                    end=PositionGQL(
                        line=end_line_index + 1,
                        character=offset_end,
                    ),
                )
    return None


def get_variable_range(lines: List[str], name: str) -> RangeGQL | None:
    name = name.lower()
    variable_name = "${" + name + "}"
    for i, line in enumerate(lines):
        if line.lstrip().startswith("--"):
            continue
        line = line.lower()
        if name in line:
            start = line.index(variable_name)
            end = start + len(variable_name)
            return RangeGQL(
                start=PositionGQL(
                    line=i + 1,
                    character=start,
                ),
                end=PositionGQL(
                    line=i + 1,
                    character=end,
                ),
            )
    return None


def get_feature_range(lines: List[str], exp: Select | Union, name: str) -> RangeGQL | None:
    select_string = None
    for select in exp.selects:
        select_str = str(select).lower()
        if name == select_str.split()[-1]:
            select_string = select_str
            break
        select_str = select.alias_or_name.lower()
        if name.lower() == select_str.split()[-1]:
            select_string = select_str
            break
    if select_string is None:
        return None
    value = select_string.split()[-1]
    for i, line in enumerate(lines):
        if line.lstrip().startswith("--"):
            continue
        line = line.lower()
        if value != select_string:
            found = select_string in line
        else:
            found = any(select_string in split for split in line.split())
        if found:
            start_of_substring = line.index(select_string)
            start_of_value_offset = select_string.rfind(value)
            start = start_of_substring + start_of_value_offset
            end = start + len(value)
            return RangeGQL(
                start=PositionGQL(
                    line=i + 1,
                    character=start,
                ),
                end=PositionGQL(
                    line=i + 1,
                    character=end,
                ),
            )


def get_full_range(lines: List[str]) -> RangeGQL:
    return RangeGQL(
        start=PositionGQL(
            line=1,
            character=0,
        ),
        end=PositionGQL(
            line=len(lines),
            character=len(lines[-1]) if len(lines) > 0 else 0,
        ),
    )


def get_full_comment_range(lines: List[str]) -> RangeGQL | None:
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("--"):
            return RangeGQL(
                start=PositionGQL(
                    line=1,
                    character=0,
                ),
                end=PositionGQL(
                    line=i,
                    character=len(lines[i - 1]),
                ),
            )
    return None


def get_sql_range(lines: List[str]) -> RangeGQL | None:
    start = None
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("--"):
            start = i
            break
    if start is None:
        return None
    return RangeGQL(
        start=PositionGQL(
            line=start + 1,
            character=0,
        ),
        end=PositionGQL(
            line=len(lines),
            character=len(lines[-1]),
        ),
    )
