import ast
from typing import Any
from typing import Generator
from typing import List
from typing import Tuple
from typing import Type

from .version import VERSION


MSG = "ASS001 do not use bare asserts"


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.missing_msgs: List[Tuple[int, int]] = []

    def visit_Assert(self, node: "ast.Assert") -> None:
        if not node.msg:
            self.missing_msgs.append((node.lineno, node.col_offset))
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = VERSION

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col in visitor.missing_msgs:
            yield line, col, MSG, type(self)
