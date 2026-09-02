"""Which files a file depends on, by reading its import statements.

Declarations -- Pydantic models, an enum, a module of constants -- run once
while their module is imported, before any test starts. Coverage credits them to
no test at all, so following imports is the only way to tell which tests depend
on them.

An import is a dependency of whichever test ran a line referencing the imported
name, so edges are keyed by that line and coverage says who ran it. A name
referenced only where its module is imported -- a module-level statement, a class
body, a decorator, a default argument -- runs before any test starts, so no test
is credited with the line and the edge never applies. The same goes for a name
bound and never referenced, such as a re-export, and for the names a star import
brings in, which cannot be read off the import statement at all. Supporting
those is a follow up.

import_deps works out what each file is importable as. Which name an import
binds, and where that name is then referenced, is read here: an import graph
alone cannot say whether a name is used on a line a test ran.
"""

import ast
from collections import defaultdict

from import_deps import ModuleSet


def import_edges(paths):
    """{path: {line: the paths it depends on if that line ran}}."""
    modules = ModuleSet(sorted(path for path in paths if path.endswith(".py")))
    edges = {}

    for path, module in modules.by_path.items():
        tree = _parse(path)
        if tree is None:
            continue

        lines_of = _referenced_lines(tree)
        by_line = defaultdict(set)
        for name, names in _bindings(tree, module.fqn):
            targets = {
                target
                for target in (_resolve(modules, n) for n in names)
                if target is not None
            }
            if not targets:
                continue
            for line in lines_of.get(name, ()):
                by_line[line] |= targets

        if by_line:
            edges[path] = dict(by_line)

    return edges


def reachable_from(starts, executed):
    """`starts` and everything they reach, following imports transitively.

    `executed[path]` are the edges out of `path` whose line one test ran, so this
    is called once per test file rather than once for the whole run.
    """
    seen = set(starts)
    stack = list(starts)
    while stack:
        for target in executed.get(stack.pop(), ()):
            if target not in seen:
                seen.add(target)
                stack.append(target)
    return seen


def _resolve(modules, name):
    """The file a module name imports, if it is one of ours.

    import_deps keys a package by its __init__, so "pkg" has to be looked up as
    "pkg.__init__".
    """
    module = modules.by_name.get(name)
    if module is None and name in modules.pkgs:
        module = modules.by_name.get(f"{name}.__init__")
    # PyModule.path is a pathlib.Path; every path here is a string.
    return str(module.path) if module else None


def _parse(path):
    try:
        with open(path, "rb") as f:
            return ast.parse(f.read(), filename=path)
    except Exception:
        return None  # Anything unreadable contributes no imports.


def _referenced_lines(tree):
    """{name: the lines referencing it}."""
    lines_of = defaultdict(set)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            lines_of[node.id].add(node.lineno)
    return lines_of


def _bindings(tree, fqn):
    """Yields (name an import binds, {module names it implies}).

    Read off the tree already parsed rather than import_deps.ast_imports, which
    opens the file as text: a module declaring a legacy encoding parses here and
    raises there. `fqn` is the importing file's own dotted name, which a relative
    import is resolved against.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                bound = alias.asname or alias.name.split(".")[0]
                yield bound, _with_ancestors(alias.name)
        elif isinstance(node, ast.ImportFrom):
            # fqn[:-level] is the package a relative import resolves against.
            package = fqn[: -node.level] if node.level else []
            base = ".".join(package + ([node.module] if node.module else []))
            if not base:
                continue
            for alias in node.names:
                # "from pkg import mod" may name a module, not a value, and the
                # ancestors cover pkg itself.
                yield alias.asname or alias.name, _with_ancestors(
                    f"{base}.{alias.name}"
                )


def _with_ancestors(name):
    """{"a", "a.b", "a.b.c"} for "a.b.c".

    Importing a.b.c also executes a/__init__.py and a/b/__init__.py, so a
    change to either affects whoever imported it.
    """
    parts = name.split(".")
    return {".".join(parts[: i + 1]) for i in range(len(parts))}
