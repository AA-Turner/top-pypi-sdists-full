"""Refuse a matrx-ai wheel whose instance_create write loses AI provenance.

The production server normally consumes the workspace source, but other hosts consume the
published wheel.  Checking only the checkout let an older wheel look healthy while it wrote
unconfirmed Content IR records with the database's ``code`` fallback.  This guard reads the
actual wheel payload that PyPI will receive and proves the durable create call is nested under
the exact actor declaration.
"""

from __future__ import annotations

import argparse
import ast
import sys
import zipfile
from pathlib import Path

MEMBER = "matrx_ai/tools/implementations/kind_instance.py"
EXPECTED_TIER = "ai"
EXPECTED_SYSTEM = "tool:instance_create"


def _is_expected_declaration(node: ast.AsyncWith) -> bool:
    for item in node.items:
        expr = item.context_expr
        if not (
            isinstance(expr, ast.Call)
            and isinstance(expr.func, ast.Name)
            and expr.func.id == "declared_actor"
            and len(expr.args) == 2
            and all(isinstance(arg, ast.Constant) for arg in expr.args)
        ):
            continue
        if expr.args[0].value == EXPECTED_TIER and expr.args[1].value == EXPECTED_SYSTEM:
            return True
    return False


def verify_wheel(path: Path) -> None:
    with zipfile.ZipFile(path) as wheel:
        try:
            source = wheel.read(MEMBER).decode("utf-8")
        except KeyError as exc:
            raise AssertionError(f"wheel is missing {MEMBER}") from exc

    tree = ast.parse(source, filename=f"{path}!/{MEMBER}")
    parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    creates = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "create_item"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "KindInstance"
    ]
    if len(creates) != 1:
        raise AssertionError(f"expected one KindInstance.create_item call, found {len(creates)}")

    node: ast.AST | None = creates[0]
    while node is not None:
        if isinstance(node, ast.AsyncWith) and _is_expected_declaration(node):
            return
        node = parents.get(node)
    raise AssertionError(
        "instance_create's durable KindInstance.create_item is outside "
        "declared_actor('ai', 'tool:instance_create')"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", type=Path)
    args = parser.parse_args()
    verify_wheel(args.wheel)
    print(f"PASS {args.wheel}: instance_create actor declaration is packaged")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
