import ast
from typing import Any, List

class SymbolicSignature:
    """Simple structural signature extracted from an AST node."""

    def __init__(self, name: str, vector: List[float]):
        self.name = name
        self.vector = vector

    def magnitude(self) -> float:
        return sum(self.vector)

def node_complexity(node: ast.AST) -> int:
    """Return complexity score based on AST walk."""
    return sum(1 for _ in ast.walk(node))

def extract_signature(node: ast.AST, name: str) -> SymbolicSignature:
    complexity = node_complexity(node)
    branches = len(
        [
            n
            for n in ast.walk(node)
            if isinstance(n, (ast.If, ast.For, ast.While))
        ]
    )
    loops = len(
        [n for n in ast.walk(node) if isinstance(n, (ast.For, ast.While))]
    )
    vector = [complexity, branches, loops]
    return SymbolicSignature(name=name, vector=vector)

def _walk_js(obj: Any):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            if isinstance(v, (dict, list)):
                yield from _walk_js(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from _walk_js(item)


def extract_signature_from_source(
    source: str, name: str, language: str = "python"
) -> SymbolicSignature:
    """Return signature from source code for ``language``."""
    if language == "python":
        tree = ast.parse(source)
        return extract_signature(tree, name)
    if language == "javascript":
        import esprima

        tree = esprima.parseScript(source).toDict()
        nodes = list(_walk_js(tree))
        complexity = len(nodes)
        branches = len(
            [n for n in nodes if n.get("type") in {"IfStatement", "SwitchStatement"}]
        )
        loops = len(
            [
                n
                for n in nodes
                if n.get("type") in {"ForStatement", "WhileStatement", "DoWhileStatement"}
            ]
        )
        vector = [complexity, branches, loops]
        return SymbolicSignature(name=name, vector=vector)
    raise ValueError(f"Unsupported language: {language}")


__all__ = [
    "SymbolicSignature",
    "node_complexity",
    "extract_signature",
    "extract_signature_from_source",
]

