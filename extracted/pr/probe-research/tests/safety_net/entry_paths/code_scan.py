"""Every process entry the code spells as a string: `-m` targets, `*_MODULE(S)` constants, `-c` imports.

An import codemod rewrites import statements, never these strings, so they are found here and
checked against the pinned lists. Docstrings are skipped; `where` values are for messages only.
"""

from __future__ import annotations

import ast
import re
from collections import defaultdict
from pathlib import Path

import probe

AGENT = Path(__file__).resolve().parents[3]
PACKAGE = Path(probe.__file__).resolve().parent
MODULE = r"probe(?:\.[A-Za-z_]\w*)*"
_DASH_M = re.compile(r"(?:^|[\s\"'>])-m\s+(" + MODULE + r")(?![\w.])")
_LIST_M = re.compile(r"[\"']-m[\"']\s*,\s*[\"'](" + MODULE + r")[\"']")
_FROM = re.compile(r"(?:^|[;\n\s])from\s+(" + MODULE + r")\s+import\s+(\w+(?:\s*,\s*\w+)*)")
_IMPORT = re.compile(r"(?:^|[;\n])\s*import\s+(" + MODULE + r"(?:\s*,\s*" + MODULE + r")*)")
_CONSTANT = re.compile(r"_MODULES?$")
_CANDIDATE = re.compile(r"-m\b|_MODULES?\b|[\"'][^\"'\n]*\b(?:from|import) probe")
_SKIP_DIRS = {"tests", "node_modules", "fixtures", "__pycache__", ".venv"}


def _files(suffixes: tuple[str, ...]) -> list[Path]:
    roots = [PACKAGE, AGENT / "plugins"]
    return sorted(p for root in roots for p in root.rglob("*")
                  if p.suffix in suffixes and p.is_file() and not _SKIP_DIRS & set(p.relative_to(root).parts))


def _where(path: Path, line: int) -> str:
    return f"{path.relative_to(AGENT)}:{line}"


def _docstrings(tree: ast.AST) -> set[int]:
    """Bare string statements (docstrings and their kin): prose, not code."""
    return {id(node.value) for node in ast.walk(tree)
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)}


def _strings(node: ast.AST) -> list[str]:
    return [n.value for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


class Scan:
    """What one pass over the package and the plugins found (each value: where it was seen)."""

    def __init__(self) -> None:
        self.dash_m: dict[str, set[str]] = defaultdict(set)
        self.constants: dict[str, set[str]] = defaultdict(set)
        self.imports: dict[tuple[str, tuple[str, ...]], set[str]] = defaultdict(set)
        texts = {path: path.read_text(encoding="utf-8") for path in _files((".py",))}
        # Parsing all ~500 files costs seconds; only these can hold an entry string.
        trees = {path: ast.parse(text) for path, text in texts.items() if _CANDIDATE.search(text)}
        named = self._named_strings(trees)
        for path, tree in trees.items():
            self._python(path, tree, named)
        for path in _files((".sh",)):
            self._shell(path)
        for path in _files((".ts",)):
            for match in _LIST_M.finditer(text := path.read_text(encoding="utf-8")):
                self.dash_m[match.group(1)].add(_where(path, text.count("\n", 0, match.start()) + 1))

    def _named_strings(self, trees: dict) -> dict[str, set[str]]:
        """NAME -> the probe module strings assigned to it anywhere (to resolve `"-m", CORE_MODULE`)."""
        named: dict[str, set[str]] = defaultdict(set)
        for path, tree in trees.items():
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    targets = node.targets
                elif isinstance(node, ast.AnnAssign) and node.value is not None:
                    targets = [node.target]
                else:
                    continue
                for target in targets:
                    if not isinstance(target, ast.Name) or not target.id.isupper():
                        continue  # only constants: a local `model` is no module
                    values = {v for v in _strings(node.value) if re.fullmatch(MODULE, v)}
                    named[target.id] |= values
                    if values and _CONSTANT.search(target.id):
                        for value in values:
                            self.constants[value].add(f"{target.id} ({_where(path, node.lineno)})")
        return named

    def _python(self, path: Path, tree: ast.AST, named: dict) -> None:
        prose = _docstrings(tree)
        for node in ast.walk(tree):
            if isinstance(node, (ast.List, ast.Tuple)):
                for flag, target in zip(node.elts, node.elts[1:]):
                    if isinstance(flag, ast.Constant) and flag.value == "-m":
                        for value in self._resolve(target, named):
                            self.dash_m[value].add(_where(path, node.lineno))
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in prose:
                self._text(node.value, _where(path, node.lineno))

    @staticmethod
    def _resolve(node: ast.AST, named: dict) -> set[str]:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return {node.value} if re.fullmatch(MODULE, node.value) else set()
        name = node.id if isinstance(node, ast.Name) else node.attr if isinstance(node, ast.Attribute) else ""
        return set(named.get(name, ()))

    def _text(self, text: str, where: str) -> None:
        for module in _DASH_M.findall(text):
            self.dash_m[module].add(where)
        for module, names in _FROM.findall(text):
            self.imports[(module, tuple(sorted(n.strip() for n in names.split(","))))].add(where)
        for modules in _IMPORT.findall(text):
            for module in modules.split(","):
                self.imports[(module.strip(), ())].add(where)

    def _shell(self, path: Path) -> None:
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.lstrip().startswith("#"):
                for module in _DASH_M.findall(line):
                    self.dash_m[module].add(_where(path, number))
