"""Every third-party module the CLI side imports is one the package declares.

`probe wizard --reinstall --agent codex` imported `tomlkit` (since 2026-10-19)
while `tomlkit` was in no dependency or extra, so it crashed with
ModuleNotFoundError on every real install. The tests never saw it: the dev
environment carries `tomlkit` for another reason. This reads the SOURCE, not
the environment, so what happens to be installed cannot hide a missing
declaration.

An import inside a `try` that catches ImportError (or broader) is optional by
construction and is skipped; so is an import whose caller catches the
ImportError, listed in `_GUARDED_BY_CALLER` with where.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

from probe._compat import tomllib

_AGENT = Path(__file__).resolve().parents[1]
_PACKAGE = _AGENT / "src" / "probe"

#: The packages that run in the CLI's process, each checked against what is
#: installed where it runs: `[all]` (cli + mcp) everywhere; `daemon/` also has
#: `[daemon]` (daemon mode installs it); `mcp/` also has `[mcp-http]` (the
#: hosted service). "" is the package's top-level modules. Pooling every extra
#: for every package would let `import pydantic_ai` in cli/ pass, and crash an
#: `[all]` install the way tomlkit did.
_ALL = ("cli", "mcp")
_CLI_SIDE = {
    "": _ALL,
    "cli": _ALL,
    "core": _ALL,
    "service": _ALL,
    "_shared": _ALL,
    "harness": _ALL,
    "tap_core": _ALL,
    "hw": _ALL,
    "box": _ALL,
    "daemon": (*_ALL, "daemon"),
    "mcp": (*_ALL, "mcp-http"),
}

#: Import name -> the declared distribution that ships it or pulls it in.
_PROVIDED_BY = {
    "pynvml": "nvidia-ml-py",
    "click": "typer",
    "prompt_toolkit": "questionary",
    "pydantic_core": "pydantic",
    "certifi": "httpx",
    "pydantic_ai": "pydantic-ai-slim",
    "openai": "pydantic-ai-slim",
}

#: Optional imports whose ImportError the CALLER handles.
_GUARDED_BY_CALLER = {
    ("daemon/reader.py", "pyarrow"): "_parquet catches the ImportError from _import_parquet",
}

#: Not a distribution: the tap plugin's own package, on sys.path when it runs.
_NOT_DISTRIBUTIONS = {"probe", "__future__", "tap"}

_CATCHES_IMPORT_ERROR = {"ImportError", "ModuleNotFoundError", "Exception", "BaseException"}


def _declared(extras: tuple[str, ...]) -> set[str]:
    project = tomllib.loads((_AGENT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    specs = list(project["dependencies"])
    for extra in extras:
        specs += project["optional-dependencies"][extra]
    return {re.split(r"[\s<>=!~\[;(]", spec, maxsplit=1)[0].lower().replace("_", "-") for spec in specs}


def _guarded(try_node: ast.Try) -> bool:
    for handler in try_node.handlers:
        if handler.type is None:
            return True
        types = handler.type.elts if isinstance(handler.type, ast.Tuple) else [handler.type]
        if any(isinstance(t, ast.Name) and t.id in _CATCHES_IMPORT_ERROR for t in types):
            return True
    return False


def _unguarded_imports(tree: ast.AST):
    def visit(node: ast.AST, inside_guard: bool):
        for child in ast.iter_child_nodes(node):
            guarded = inside_guard or (isinstance(node, ast.Try) and child in node.body and _guarded(node))
            if isinstance(child, ast.Import):
                if not guarded:
                    for alias in child.names:
                        yield alias.name.split(".")[0], child.lineno
            elif isinstance(child, ast.ImportFrom):
                if not guarded and child.level == 0 and child.module:
                    yield child.module.split(".")[0], child.lineno
            yield from visit(child, guarded)

    yield from visit(tree, False)


def test_every_cli_side_third_party_import_is_declared():
    stdlib = set(sys.stdlib_module_names)
    missing = []
    for package, extras in _CLI_SIDE.items():
        declared = _declared(extras)
        files = (_PACKAGE / package).rglob("*.py") if package else _PACKAGE.glob("*.py")
        for path in sorted(files):
            relative = path.relative_to(_PACKAGE).as_posix()
            for module, line in _unguarded_imports(ast.parse(path.read_text(encoding="utf-8"))):
                if module in stdlib or module in _NOT_DISTRIBUTIONS:
                    continue
                if (relative, module) in _GUARDED_BY_CALLER:
                    continue
                if _PROVIDED_BY.get(module, module.lower().replace("_", "-")) not in declared:
                    missing.append(f"{relative}:{line} imports {module} (has: core + {', '.join(extras)})")
    assert not missing, (
        "imported on the CLI side but not declared for where it runs "
        f"(a real install will not have it): {missing}"
    )


def test_the_guard_sees_an_undeclared_import():
    """The check itself: a module no declaration provides is reported, and
    the same import inside a try/except ImportError is not."""
    bare = ast.parse("def f():\n    import not_a_declared_module\n")
    guarded = ast.parse("try:\n    import not_a_declared_module\nexcept ImportError:\n    pass\n")
    assert [m for m, _ in _unguarded_imports(bare)] == ["not_a_declared_module"]
    assert list(_unguarded_imports(guarded)) == []
