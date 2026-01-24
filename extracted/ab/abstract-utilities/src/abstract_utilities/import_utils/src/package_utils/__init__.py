import ast
from pathlib import Path
from importlib.util import find_spec
from typing import Dict, Set
import ast, sys
from pathlib import Path
from importlib.util import find_spec
from typing import Dict, Set
from src.abstract_utilities.import_utils import *
STDLIB_NAMES = set(sys.builtin_module_names)
def parse_imports(file_path: Path):
    """Return list of (module, level) for every import/from-import."""
    try:
        src = file_path.read_text(errors="ignore")
        tree = ast.parse(src, filename=str(file_path))
    except Exception:
        return []
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((alias.name, 0))
        elif isinstance(node, ast.ImportFrom):
            imports.append((node.module, node.level))
    return imports


def resolve_relative_import(base_file: Path, module: str | None, level: int) -> Path | None:
    """Follow a relative import path to its real file if it exists."""
    base = base_file.parent
    for _ in range(level - 1):
        base = base.parent
    if not module:
        target = base
    else:
        target = base / module.replace(".", "/")
    if (target / "__init__.py").exists():
        return target / "__init__.py"
    if target.with_suffix(".py").exists():
        return target.with_suffix(".py")
    return None




def classify_import(mod_name: str, root_pkg: str) -> str:
    """Return 'local', 'internal', or 'external'."""
    if not mod_name:
        return "unknown"
    if mod_name.startswith("."):
        return "local"
    if mod_name.split(".")[0] == root_pkg:
        return "internal"
    if mod_name.split(".")[0] in STDLIB_NAMES:
        return "stdlib"
    return "external"


def follow_imports(entry: Path, root_pkg: str,
                   visited: Dict[Path, Dict[str, Set[str]]] | None = None):
    """
    Recursively follow only internal/local imports.
    Returns {file_path: {'internal': set(), 'external': set()}}
    """
    visited = visited or {}
    if entry in visited:
        return visited

    visited[entry] = {"internal": set(), "external": set()}

    for mod, level in parse_imports(entry):
        if level > 0:
            target = resolve_relative_import(entry, mod, level)
            if target:
                visited[entry]["internal"].add(str(target))
                follow_imports(target, root_pkg, visited)
            continue

        category = classify_import(mod, root_pkg)
        if category == "internal":
            spec = find_spec(mod)
            if spec and spec.origin and spec.origin.endswith(".py"):
                visited[entry]["internal"].add(spec.origin)
                follow_imports(Path(spec.origin), root_pkg, visited)
        elif category == "external":
            visited[entry]["external"].add(mod)
        elif category == "stdlib":
            # stdlib gets treated like external but labeled
            visited[entry]["external"].add(mod + "  # stdlib")

    return visited



def build_master_imports(entry: Path, root_pkg: str, output: Path):
    trace = follow_imports(entry, root_pkg)
    lines = ["# Auto-generated master imports for abstract_utilities\n"]
    all_modules = set()
    external_modules = set()
    imports = get_all_imports(path)
    for _, data in trace.items():
        for dep in data["internal"]:
            path = Path(dep)
            if path.suffix != ".py":
                continue
            try:
                rel_parts = path.with_suffix("").parts
                idx = rel_parts.index(root_pkg)
                dotted = ".".join(rel_parts[idx:])
                all_modules.add(dotted)
            except ValueError:
                continue
        external_modules.update(data["external"])

    for mod in sorted(all_modules):
        short = mod.split(".", 1)[-1]
        lines.append(f"from .{short} import *")

    if external_modules:
        lines.append("\n# External / stdlib imports (not traced, for reference)")
        for ext in sorted(external_modules):
            lines.append(f"# {ext}")
    
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines+str(imports)))
    print(f"✅ wrote master imports hub → {output}")



if __name__ == "__main__":
    entry = Path(
        "/home/flerb/Documents/pythonTools/modules/src/modules/abstract_utilities/src/"
        "abstract_utilities/import_utils/src/import_functions.py"
    )

    
    pkg = "abstract_utilities"
    out = entry.parents[4] / "imports" / "__init__.py"
    build_master_imports(entry, pkg, out)
