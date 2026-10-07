"""Layer the hand-written code in custom/ onto the freshly generated package.

- copies custom/supermemory/* into src/supermemory/
- applies custom/patches/*.patch (small additions to generated core files)
- adds the 3.x per-call options (extra_headers, extra_query, extra_body,
  timeout) to every generated method signature, next to request_options, so
  type checkers accept them; the client wrapper in _compat.py translates them
- removes every name that custom/supermemory/_compat.py exports from the
  generated __init__.py lazy-import tables, then appends custom/__init__.tail.py,
  so `supermemory.Supermemory`, `supermemory.NotFoundError`, … resolve to the
  compatible versions for both the runtime and type checkers.
"""

import ast
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "src" / "supermemory"
CUSTOM = ROOT / "custom"


def compat_exports() -> set[str]:
    tree = ast.parse((CUSTOM / "supermemory" / "_compat.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            return set(ast.literal_eval(node.value))
    raise SystemExit("custom/supermemory/_compat.py has no __all__")


PER_CALL_OPTIONS = (
    ", extra_headers: typing.Optional[typing.Mapping[str, str]] = None"
    ", extra_query: typing.Optional[typing.Mapping[str, typing.Any]] = None"
    ", extra_body: typing.Optional[typing.Mapping[str, typing.Any]] = None"
    ", timeout: typing.Union[float, httpx.Timeout, None, NotGiven] = NOT_GIVEN"
)
PER_CALL_NAMES = {"extra_headers", "extra_query", "extra_body", "timeout"}


def add_per_call_options(path: Path) -> None:
    source = path.read_text()
    lines = source.splitlines(keepends=True)
    inserts: list[tuple[int, int]] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        names = [a.arg for a in node.args.kwonlyargs]
        if "request_options" not in names:
            continue
        clash = PER_CALL_NAMES.intersection(names)
        if clash:
            raise SystemExit(f"{path}:{node.lineno} {node.name}() already has {clash}; rename it in fern/overlay.yaml")
        default = node.args.kw_defaults[names.index("request_options")]
        assert default is not None and default.end_lineno is not None and default.end_col_offset is not None
        inserts.append((default.end_lineno - 1, default.end_col_offset))
    if not inserts:
        return
    for line, col in sorted(inserts, reverse=True):
        text = lines[line]
        # col is a UTF-8 byte offset
        raw = text.encode()
        lines[line] = (raw[:col] + PER_CALL_OPTIONS.encode() + raw[col:]).decode()
    source = "".join(lines)
    if not re.search(r"^import httpx$", source, re.M):
        source = re.sub(r"^import typing$", "import typing\n\nimport httpx", source, count=1, flags=re.M)
    source = re.sub(
        r"^import httpx$",
        "import httpx\n\nfrom supermemory._types import NOT_GIVEN, NotGiven",
        source,
        count=1,
        flags=re.M,
    )
    path.write_text(source)


def main() -> None:
    shutil.copytree(CUSTOM / "supermemory", PACKAGE, dirs_exist_ok=True)
    for patch in sorted((CUSTOM / "patches").glob("*.patch")):
        subprocess.run(["patch", "-p1", "--forward", "--no-backup-if-mismatch", "-i", str(patch)], cwd=ROOT, check=True)
    for path in sorted(PACKAGE.rglob("*client.py")):
        if "core" not in path.relative_to(PACKAGE).parts:
            add_per_call_options(path)

    names = compat_exports()
    init = PACKAGE / "__init__.py"
    lines = []
    for line in init.read_text().splitlines():
        stripped = line.strip()
        # `    NotFoundError,` inside a TYPE_CHECKING `from .x import (...)` block
        if stripped.rstrip(",") in names and stripped.endswith(","):
            continue
        # `"NotFoundError": ".errors",` in the lazy-import mapping
        match = re.fullmatch(r'"(\w+)": "\.[\w.]+",', stripped)
        if match and match.group(1) in names:
            continue
        # `from .client import AsyncSupermemory, Supermemory`
        match = re.fullmatch(r"(\s*from \.[\w.]+ import )([\w, ]+)", line)
        if match:
            kept = [n.strip() for n in match.group(2).split(",") if n.strip() not in names]
            if not kept:
                continue
            line = match.group(1) + ", ".join(kept)
        lines.append(line)
    init.write_text("\n".join(lines) + "\n" + (CUSTOM / "__init__.tail.py").read_text())


if __name__ == "__main__":
    main()
