"""Nothing outside ``src/routers/webui/`` may reach into it.

**The webui package is throwaway, and a dependency on it points the wrong way.**
The browser pages are leaving Python; when they go, every module under
``src/routers/webui/`` goes with them. Anything else importing from there turns
that deletion into a migration -- the retirement has to find a new home for the
imported symbol *and* keep whatever depends on it working, which is exactly the
work the retirement was supposed to be free of.

This is not hypothetical. ``src/routers/identities.py`` imported
``unmapped_handles`` from ``src.routers.webui.data`` -- the single
router-to-webui edge in the tree -- so ``GET .../identities?unmapped=true``, a
live API endpoint with a CLI in front of it, depended on the UI it was written to
replace. #598 moved the function to ``src/services/summary_service.py``. Nothing
enforced the boundary at the time, so nothing would have caught the next one;
that is what this file is.

**Direction matters, and only one direction is wrong.** webui importing from
``src/services/``, ``src/domain/`` or anywhere else is ordinary and expected --
a UI reading the app's own layers. The rule here is one-way: the UI may depend
on the app, the app may not depend on the UI.

**What is forbidden is a *submodule*, not the package.** ``src/api/app.py``
imports ``webui`` to ``include_router(webui.router)``, and that edge is the
mount point -- the one place the pages have to be plugged in, and a line the
retirement *deletes* rather than untangles. The package's ``__init__`` exports
exactly one name for it. Reaching past that to ``webui.data``, ``webui.render``
or ``webui.session`` is the thing that makes deletion expensive, so the check is
keyed on the real filenames in the package (``SUBMODULES``) rather than on the
prefix alone: ``from src.routers.webui import router`` is a mount,
``from src.routers.webui import data`` is a violation, and only one of them can
be told from the other by looking at what is on disk.

**Deliberately no allowlist.** The count today is zero, and a gate whose baseline
is zero has nothing to work off; an entry here would be a decision to make the
retirement harder, which belongs in review rather than in a set literal. If a
future caller genuinely needs something webui has, the answer is the same one
#598 took: move the shared thing into ``src/services/`` and import it from
there.

Both statement forms are covered, including relative imports (``from .webui
import data`` inside ``src/routers/``, which names the same module by a
different spelling) and function-level imports -- ``src/`` has 95 of the latter,
so a scan that only read the top of each file would miss the shape most likely
to be written by someone working around this rule.
"""

import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
WEBUI = SRC / "routers" / "webui"

#: The package that may not be reached into.
FORBIDDEN = "src.routers.webui"

#: Its modules, read off disk rather than listed here -- a hand-maintained list
#: would silently stop covering a module added after this landed, which is the
#: same "gate over nothing" failure the second test guards against.
SUBMODULES = frozenset(
    p.stem for p in WEBUI.glob("*.py") if p.stem != "__init__"
) | frozenset(p.name for p in WEBUI.iterdir() if p.is_dir() and p.name != "__pycache__")


def _python_files():
    """Every module under ``src/`` that is not itself part of webui."""
    for path in sorted(SRC.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        if WEBUI in path.parents:
            continue
        yield path


def _module_name(path: Path) -> str:
    """``src.routers.identities`` for ``src/routers/identities.py``.

    Needed to resolve a relative import: ``level`` counts packages up from the
    importing module, so the same target can be written ``from
    src.routers.webui import data`` or ``from .webui import data`` and only one
    of those contains the forbidden string.
    """
    rel = path.relative_to(SRC.parent).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _imported_modules(path: Path):
    """Every absolute module name this file imports, relative forms resolved.

    ``from X import Y`` yields ``X`` and ``X.Y``: whether ``Y`` is a submodule or
    an ordinary symbol is not knowable from the syntax, so both spellings are
    emitted and the caller decides using ``SUBMODULES``.
    """
    tree = ast.parse(path.read_text())
    package = _module_name(path).rsplit(".", 1)[0]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                # `from . import x` inside src/routers/foo.py is src.routers.
                anchor = package.split(".")
                anchor = anchor[: len(anchor) - (node.level - 1)] or [""]
                base = ".".join([*anchor, base]) if base else ".".join(anchor)
            yield base
            for alias in node.names:
                yield f"{base}.{alias.name}" if base else alias.name


def _violations_in(path: Path):
    """The webui *modules* this file imports. Empty for a package-only import."""
    found = set()
    for name in _imported_modules(path):
        if not name.startswith(f"{FORBIDDEN}."):
            continue
        if name[len(FORBIDDEN) + 1 :].split(".")[0] in SUBMODULES:
            found.add(name)
    return found


def test_the_webui_package_has_no_importers_outside_itself():
    """The gate. Zero, with no allowlist -- see the module docstring."""
    offenders = {
        str(path.relative_to(SRC.parent)): sorted(found)
        for path in _python_files()
        if (found := _violations_in(path))
    }
    assert offenders == {}, (
        "src/routers/webui/ is throwaway -- the browser pages are leaving Python, "
        "and these modules would have to be untangled before they can go. Move "
        "the shared code into src/services/ and import it from there:\n"
        + "\n".join(
            f"  {path}: {', '.join(names)}" for path, names in offenders.items()
        )
    )


def test_the_scan_reaches_the_files_it_claims_to():
    """A gate over an empty file list passes for the wrong reason.

    The failure mode the assertion above cannot show is finding nothing because
    it looked nowhere -- a renamed package, an `rglob` that stopped matching, a
    `parents` check that excluded everything, a `SUBMODULES` set that came back
    empty and made every reach-in invisible. This pins the facts that make the
    zero mean something.
    """
    scanned = {str(p.relative_to(SRC.parent)) for p in _python_files()}

    assert "src/routers/identities.py" in scanned, "the router that held the edge"
    assert "src/api/app.py" in scanned, "the mount point is checked, not skipped"
    assert "src/routers/webui/data.py" not in scanned, "webui may import webui"
    assert "src/routers/webui/routes.py" not in scanned
    assert len(scanned) > 100, f"only {len(scanned)} files scanned"
    assert {"data", "routes", "render", "session"} <= SUBMODULES, SUBMODULES


def test_mounting_the_package_is_not_a_reach_into_it():
    """The one exempt edge, pinned so the exemption stays that narrow.

    `app.py` must import the package to `include_router` it, and that import is
    deleted -- not migrated -- when the pages go. If this ever stops describing
    `app.py`, the mount has been rewritten to reach past `__init__` and the gate
    above should be the thing that says so.
    """
    app = SRC / "api" / "app.py"
    imported = set(_imported_modules(app))

    assert FORBIDDEN in imported, "app.py still mounts the pages"
    assert _violations_in(app) == set(), "and does it without naming a submodule"
