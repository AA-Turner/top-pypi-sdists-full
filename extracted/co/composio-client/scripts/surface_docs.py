"""Extract class and attribute docstrings from importable Python types."""

from __future__ import annotations

import ast
import inspect
import textwrap
from collections.abc import Mapping
from typing import Any


def class_docs(value: type[Any]) -> tuple[str | None, dict[str, str]]:
    """Return a class docstring and its PEP 258 attribute docstrings."""

    try:
        tree = ast.parse(textwrap.dedent(inspect.getsource(value)))
    except (OSError, TypeError):
        return None, {}
    class_nodes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    if len(class_nodes) != 1:
        return None, {}
    class_node = class_nodes[0]
    fields: dict[str, str] = {}
    for declaration, following in zip(class_node.body, class_node.body[1:], strict=False):
        if (
            isinstance(declaration, ast.AnnAssign)
            and isinstance(declaration.target, ast.Name)
            and isinstance(following, ast.Expr)
            and isinstance(following.value, ast.Constant)
            and isinstance(following.value.value, str)
        ):
            fields[declaration.target.id] = inspect.cleandoc(following.value.value)
    return ast.get_docstring(class_node, clean=True), fields


def doc_entry(description: str | None) -> dict[str, str]:
    """The ``description`` entry for a captured symbol, absent when undocumented."""

    return {} if description is None else {"description": description}


def field_docs_entry(field_descriptions: Mapping[str, str]) -> dict[str, dict[str, str]]:
    """The ``descriptions`` entry for a captured symbol, absent when nothing is documented."""

    return {"descriptions": dict(field_descriptions)} if field_descriptions else {}
