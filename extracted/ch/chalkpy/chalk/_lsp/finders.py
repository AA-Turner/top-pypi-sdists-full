from __future__ import annotations

import ast
from typing import TYPE_CHECKING, List

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
