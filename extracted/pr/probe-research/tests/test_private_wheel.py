"""The private compiled wheel's lists stay true to the code (plan task 5, eng review O1).

agent/packaging/private/private.py says which `probe/` files are private and which private
modules ship as plain .py. A module run with `python -m`, loaded or copied by path, or
reading its caller's frame breaks once compiled, so each must be on the keep-as-source list;
these checks read the code and fail on the PR, not at release time on five runners.
"""

from __future__ import annotations

import ast
import functools
import importlib.util
import re
import sys
import tarfile
import zipfile
from pathlib import Path

AGENT = Path(__file__).resolve().parents[1]
REPO = AGENT.parent
PACKAGE = AGENT / "src" / "probe"


def _load_tool(name: str):
    """A module of agent/packaging/private (they import `private` from beside them)."""
    folder = AGENT / "packaging" / "private"
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))
    spec = importlib.util.spec_from_file_location(f"private_wheel_{name}", folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


manifest = _load_tool("private")
PRIVATE_PY = [rel for rel in manifest.load_private_files(PACKAGE) if rel.endswith(".py")]
COMPILED = manifest.load_compiled_modules(PACKAGE)

#: Where `python -m probe.<x>` is written: the package, its plugins, hooks, the npm
#: launcher, the Makefile, the server image and its helm chart. Tests are not entry paths.
_LAUNCH_SOURCES = [AGENT / "src", AGENT / "plugins", AGENT / "npm", AGENT / "Makefile", REPO / "Dockerfile",
                   REPO / "charts", REPO / "app", REPO / "scripts"]
_LAUNCH_SUFFIXES = {".py", ".sh", ".ts", ".js", ".mjs", ".yaml", ".yml", ".tpl", ".toml", ".json", ""}
_LAUNCHES = [
    re.compile(r"""["']-m["'],\s*["'](probe(?:\.\w+)*)["']"""),   # ["-m", "probe.x"]
    re.compile(r"""-m\s+(probe(?:\.\w+)*)\b"""),                     # python -m probe.x
    re.compile(r"""_MODULE\s*=\s*["'](probe(?:\.\w+)+)["']"""),      # WORKER_MODULE = "probe.x"
]
#: Calls whose result depends on Python frames or on reading source: never compiled.
_FRAME_CALLS = {("sys", "_getframe"), ("inspect", "currentframe"), ("inspect", "stack"),
                ("inspect", "getsource"), ("inspect", "getsourcelines"), ("inspect", "getsourcefile")}
#: Calls that load a file by path: allowed compiled only when audited (PATH_READERS).
_PATH_CALLS = {("util", "spec_from_file_location"), ("runpy", "run_path"), ("runpy", "run_module")}


def _find_launched_modules() -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for root in _LAUNCH_SOURCES:
        files = [root] if root.is_file() else [path for path in root.rglob("*") if path.is_file()]
        for path in files:
            if path.suffix not in _LAUNCH_SUFFIXES or "node_modules" in path.parts or "tests" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for pattern in _LAUNCHES:
                for name in pattern.findall(text):
                    found.setdefault(name, set()).add(path.relative_to(REPO).as_posix())
    return found


def _to_module_file(name: str) -> str | None:
    """`probe.service.client` -> `service/client.py`; a package runs its `__main__.py`."""
    path = name.removeprefix("probe").lstrip(".").replace(".", "/")
    if not path:
        return None
    if (PACKAGE / path).is_dir():
        return f"{path}/__main__.py"
    return f"{path}.py"


def _get_call_name(node: ast.Call) -> tuple[str, str] | None:
    func = node.func
    if isinstance(func, ast.Attribute):
        base = func.value
        name = base.id if isinstance(base, ast.Name) else base.attr if isinstance(base, ast.Attribute) else ""
        return name, func.attr
    return None


@functools.cache
def _parse_module(rel: str) -> ast.Module:
    return ast.parse((PACKAGE / rel).read_text(encoding="utf-8"), filename=rel)


def test_every_file_of_the_package_is_public_or_private_never_both():
    for path in sorted(PACKAGE.rglob("*")):
        rel = path.relative_to(PACKAGE).as_posix()
        if not path.is_file() or "__pycache__" in rel:
            continue
        assert manifest.is_private(rel) != manifest.is_public(rel), (
            f"{rel}: add its folder or root module to PRIVATE_* or PUBLIC_* in agent/packaging/private/private.py")


def test_keep_as_source_names_real_private_modules_with_a_reason():
    for rel, why in {**manifest.KEEP_AS_SOURCE, **manifest.PATH_READERS}.items():
        assert rel in PRIVATE_PY, f"{rel}: not a private module (moved? update private.py)"
        assert why.strip(), rel


def test_every_module_run_with_python_dash_m_ships_as_source():
    launched = _find_launched_modules()
    assert {"probe.service.client", "probe.core.run", "probe.service.keeper"} <= set(launched), (
        "the scan found none of the known entry paths: its patterns are broken")
    missing = {}
    for name, where in sorted(launched.items()):
        rel = _to_module_file(name)
        if rel in PRIVATE_PY and rel not in manifest.RUN_AS_MAIN:
            missing[rel] = sorted(where)[:3]
    assert not missing, (
        "runpy cannot run a compiled module, so these must be in RUN_AS_MAIN "
        f"(agent/packaging/private/private.py; the smoke test runs them): {missing}")


def test_no_compiled_module_reads_frames_or_its_own_source():
    found = []
    for rel in COMPILED:
        for node in ast.walk(_parse_module(rel)):
            if isinstance(node, ast.Call) and _get_call_name(node) in _FRAME_CALLS:
                found.append(f"{rel}:{node.lineno} {'.'.join(_get_call_name(node))}")
    assert not found, ("compiled functions push no Python frames and carry no source: keep these "
                       f"modules as source (KEEP_AS_SOURCE) or drop the call: {found}")


def test_compiled_modules_that_read_paths_are_audited():
    """`__file__` of a compiled module is its .so/.pyd: fine for finding data beside it,
    wrong for copying or running it. Each reader is checked once and listed."""
    readers = {}
    for rel in COMPILED:
        for node in ast.walk(_parse_module(rel)):
            reads_file = ((isinstance(node, ast.Name) and node.id == "__file__")  # its own, or a
                         or (isinstance(node, ast.Attribute) and node.attr == "__file__"))  # module's
            loads_path = isinstance(node, ast.Call) and _get_call_name(node) in _PATH_CALLS
            if reads_file or loads_path:
                readers.setdefault(rel, node.lineno)
    unaudited = {rel: line for rel, line in readers.items() if rel not in manifest.PATH_READERS}
    assert not unaudited, ("these compiled modules read `__file__` or load by path: check each is safe "
                           f"compiled and add it to PATH_READERS, else to KEEP_AS_SOURCE: {unaudited}")
    stale = sorted(set(manifest.PATH_READERS) - set(readers))
    assert not stale, f"PATH_READERS entries that no longer read a path (remove them): {stale}"


def test_a_private_module_named_in_a_string_ships_as_source():
    """`with_name("backfill_plan_tool.py")`, `HANDOFF_NAME = "handoff.py"`: a module used
    by its file name is read or run as a file, which a compiled module is not."""
    names = {Path(rel).name: rel for rel in PRIVATE_PY if not rel.endswith("__init__.py")}
    found = {}
    for rel in PRIVATE_PY:
        for node in ast.walk(_parse_module(rel)):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in names:
                found.setdefault(node.value, set()).add(rel)
    named = {name: sorted(where) for name, where in found.items()
             if names[name] not in manifest.KEEP_AS_SOURCE and name not in manifest.SAME_NAME_ELSEWHERE}
    assert not named, (f"private modules used by file name: keep them as source, or list the name in "
                       f"SAME_NAME_ELSEWHERE if it is another file: {named}")


def test_compiled_modules_avoid_syntax_cython_rejects():
    """Cython 3.2.9 refuses two valid forms ("starred expression is not allowed here"):
    `max([a, *b])` / `min(...)` and `except (A, *B)`. Spell them `max([a] + list(b))` and a
    module-level tuple, or the private build fails on every runner."""
    found = []
    for rel in COMPILED:
        for node in ast.walk(_parse_module(rel)):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("max", "min")
                    and len(node.args) == 1 and isinstance(node.args[0], (ast.List, ast.Tuple))
                    and any(isinstance(item, ast.Starred) for item in node.args[0].elts)):
                found.append(f"{rel}:{node.lineno} {node.func.id}([..., *x])")
            if (isinstance(node, ast.ExceptHandler) and isinstance(node.type, ast.Tuple)
                    and any(isinstance(item, ast.Starred) for item in node.type.elts)):
                found.append(f"{rel}:{node.lineno} except (..., *x)")
    assert not found, found


def test_every_private_file_vendored_into_a_plugin_ships_as_source():
    """A file the public mirror publishes gains nothing from compiling (PUBLISHED_IN_PLUGINS).
    The copies are data in plugins/VENDORED.json, expanded by tools/vendor.py."""
    spec = importlib.util.spec_from_file_location("private_wheel_vendor", AGENT / "tools" / "vendor.py")
    vendor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vendor)
    ops = [op for group in vendor.load()["groups"] for op in vendor.plan(group)]
    published = {source for op in ops if op.dest.startswith("plugins/") for source in op.sources}
    # A private copy of a published file (tap_core/harness_registry.py) is published too.
    published |= {op.dest for op in ops if op.dest.startswith("src/probe/") and set(op.sources) & published}
    published = {path.removeprefix("src/probe/") for path in published if path.startswith("src/probe/")}
    published &= set(PRIVATE_PY)
    assert {"tap_core/transcript.py", "foundation/service_api/procid.py", "shared/updates/version_policy.py"} <= published, "the scan broke"
    assert published == set(manifest.PUBLISHED_IN_PLUGINS)


def _write_wheel(path: Path, names: list[str]) -> Path:
    with zipfile.ZipFile(path, "w") as archive:
        for name in names:
            archive.writestr(name, "")
    return path


def test_the_wheel_check_refuses_public_modules_compiled_source_and_generated_c(tmp_path):
    check_wheel = _load_tool("check_wheel")
    wheel = _write_wheel(tmp_path / "probe_research_cli-0-cp310-abi3-linux_x86_64.whl",
                         ["probe/sdk/client/client.py", "probe/cli/cli.py", "probe/cli/cli.c", "probe/doctrine.abi3.so"])
    problems = "\n".join(check_wheel.check_private(wheel, PACKAGE)[0])
    assert "probe/sdk/client/client.py: not private" in problems
    assert "probe/cli/cli.py: source of a module that must ship compiled" in problems
    assert "probe/cli/cli.c: generated or source file" in problems
    assert "probe/doctrine.abi3.so" not in problems  # a private root module, compiled: fine
    assert "probe/service/server/server.py: no compiled extension" in problems
    assert "no METADATA" in problems


def test_the_public_check_refuses_private_files_in_a_wheel_or_an_sdist(tmp_path):
    check_wheel = _load_tool("check_wheel")
    wheel = _write_wheel(tmp_path / "probe_research-0-py3-none-any.whl",
                         ["probe/sdk/client/client.py", "probe/cli/main.py", "probe/doctrine.abi3.so", "probe/feedback.pyd"])
    assert sorted(check_wheel.check_public(wheel)) == [
        "probe/cli/main.py: private file in the public wheel",
        "probe/doctrine.abi3.so: private file in the public wheel",
        "probe/feedback.pyd: private file in the public wheel",
    ]
    sdist = tmp_path / "probe_research-0.tar.gz"
    with tarfile.open(sdist, "w:gz") as archive:
        for name in ("probe_research-0/src/probe/sdk/client.py", "probe_research-0/src/probe/daemon/worker.py"):
            source = tmp_path / "empty"
            source.write_text("")
            archive.add(source, arcname=name)
    assert check_wheel.check_public(sdist) == ["src/probe/daemon/worker.py: private file in the public sdist"]


def test_the_cli_spec_fingerprint_counts_compiled_cli_modules(tmp_path, monkeypatch):
    """Else a compiled release whose kept .py files did not change would reuse the spec
    cached for the last release (daemon/cli_spec.py `source_sha`)."""
    from importlib.machinery import EXTENSION_SUFFIXES

    from probe.shared.command_rules import cli_spec

    package = tmp_path / "probe"
    (package / "cli").mkdir(parents=True)
    (package / "cli" / "__main__.py").write_text("")
    for name in cli_spec.VOCABULARY:
        (package / name).parent.mkdir(parents=True, exist_ok=True)
        (package / name).write_text("")
    extension = package / "cli" / f"main{EXTENSION_SUFFIXES[0]}"
    extension.write_bytes(b"release 1")
    monkeypatch.setattr(cli_spec, "__file__", str(package / "shared" / "command_rules" / "cli_spec.py"))
    before = cli_spec.source_sha()
    extension.write_bytes(b"release 2")
    assert cli_spec.source_sha() != before
