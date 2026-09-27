"""Structural pins for the one rule that makes this a package: it must work
installed ALONE, with no aidream repo, no aidream process, and no aidream env.

These are the guards for the failure class the workspace policy calls
*Failure A* (`common-docs/policies/package-vs-implementation.md`) — the package
quietly hardwired to our own implementation. They are AST/structural scans, not
behaviour tests, because that is the only way to catch the next one *before* a
consumer hits it at runtime.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

# Scan the INSTALLED package, not the checkout beside these tests: the
# independence gate copies only `tests/` into a bare venv with an empty cwd, and
# the artifact that ships is the only one whose imports matter.
import matrx_scraper  # noqa: E402

PACKAGE_ROOT = Path(matrx_scraper.__file__).resolve().parent


def _shipped_modules() -> list[Path]:
    return sorted(p for p in PACKAGE_ROOT.rglob("*.py") if "__pycache__" not in p.parts)


def test_no_module_escapes_its_own_install_directory() -> None:
    """No shipped module may resolve a path by walking UP from ``__file__``.

    ``Path(__file__).resolve().parents[3]`` meant "the aidream repo root" — true
    only in this monorepo checkout. In a pip install it points at a random
    ancestor of site-packages, and in any other consumer's tree it points at
    someone else's files. ``gsc_bootstrap.py`` read aidream's ``.env`` that way
    until 2026-08-09. Anything a CLI needs from the project it is *run in* comes
    from the working directory, never from where the wheel happens to live.
    """

    offenders: list[str] = []
    for path in _shipped_modules():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            # Path(__file__)...parents[N]  /  os.path.dirname(os.path.dirname(__file__))
            if not isinstance(node, ast.Subscript):
                continue
            value = node.value
            if not (isinstance(value, ast.Attribute) and value.attr == "parents"):
                continue
            source = ast.unparse(node)
            if "__file__" in source:
                offenders.append(f"{path.relative_to(PACKAGE_ROOT)}:{node.lineno} {source}")

    assert not offenders, (
        "A shipped module resolves a path outside its own install directory:\n  "
        + "\n  ".join(offenders)
        + "\nResolve project paths from the working directory instead."
    )


# Modules a no-DB consumer imports (matrx-local's local execution lane is the
# live example). None of them may reach an OPTIONAL extra at module scope.
_CORE_MODULES = [
    "matrx_scraper.cache",
    "matrx_scraper.domain_config",
    "matrx_scraper.orchestrator",
    "matrx_scraper.scrape_options",
    "matrx_scraper.scraper",
    "matrx_scraper.parser.core",
    "matrx_scraper.utils.url",
    "matrx_scraper.search",
]

# Every distribution behind an optional extra. Reaching one from a core module
# means the extra is not optional at all.
_EXTRA_ONLY_IMPORTS = {
    "matrx_scraper.db": "[db] (matrx-orm)",
    "matrx_orm": "[db] (matrx-orm)",
    "matrx_connect": "[connect]",
    "matrx_runtime": "[durable]",
    "matrx_graph": "[graph]",
}


def _module_scope_nodes(tree: ast.Module) -> list[ast.stmt]:
    """Statements that execute AT IMPORT — descending through if/try/with, but
    never into a function or class body (an import in there is the fix)."""

    out: list[ast.stmt] = []
    stack: list[ast.stmt] = list(tree.body)
    while stack:
        node = stack.pop()
        out.append(node)
        if isinstance(node, ast.If | ast.Try | ast.With | ast.For | ast.While):
            for field in ("body", "orelse", "finalbody"):
                stack.extend(getattr(node, field, []) or [])
            for handler in getattr(node, "handlers", []) or []:
                stack.extend(handler.body)
    return out


def _module_path(dotted: str) -> Path:
    rel = dotted.removeprefix("matrx_scraper.").replace(".", "/")
    direct = PACKAGE_ROOT / f"{rel}.py"
    return direct if direct.exists() else PACKAGE_ROOT / rel / "__init__.py"


@pytest.mark.parametrize("dotted", _CORE_MODULES)
def test_core_module_does_not_import_an_optional_extra(dotted: str) -> None:
    """A core import must never drag in an extra the consumer did not install.

    ``cache.py`` imported ``matrx_scraper.db.models_scraper`` at module scope
    purely so ``TwoTierCache`` could reach its L2 table — so
    ``from matrx_scraper.cache import MemoryCache``, the FIRST line of
    matrx-local's no-DB desktop lane, loaded matrx-orm and died with
    ``ImportError: cannot import name 'PLATFORM_DB_ENV_PREFIX'``. The optional
    dependency belongs inside the class that needs it, never at module scope.
    """

    path = _module_path(dotted)
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    offenders: list[str] = []
    for node in _module_scope_nodes(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names = [node.module]
        else:
            continue
        for name in names:
            for banned, extra in _EXTRA_ONLY_IMPORTS.items():
                if name == banned or name.startswith(f"{banned}."):
                    offenders.append(f"{path.name}:{node.lineno} imports {name} — {extra}")

    assert not offenders, (
        f"{dotted} is a CORE import path and must work without any optional extra:\n  "
        + "\n  ".join(offenders)
        + "\nMove the import into the function/class that actually needs it."
    )


def test_module_scope_import_scan_would_catch_the_regression() -> None:
    """The scan above is only a guard if it FAILS on the shape it forbids."""

    tree = ast.parse("from matrx_scraper.db.models_scraper import ScrapeParsedPage\n")
    node = tree.body[0]
    assert isinstance(node, ast.ImportFrom)
    assert node.module is not None and node.module.startswith("matrx_scraper.db")


#: The only modules that may READ an ``AIDREAM_*`` variable, each with why.
AIDREAM_ENV_READERS: dict[str, str] = {
    "web_crawl/gsc_sync.py": "the documented GSC credential bridge of the standalone deployment.",
    "server/config.py": (
        "the standalone scraper SERVICE's own settings — the deployment is the host here; it hands "
        "the values to make_http_landing_hook(aidream_url=..., service_token=...) as arguments, so "
        "the landing hook itself reads no environment."
    ),
}


def _reads_env(text: str, env_var: str) -> bool:
    """A real read (``os.environ[...]``, ``os.environ.get(...)``, ``os.getenv(...)``) — never a
    docstring or an error sentence that merely names the variable."""
    import re

    return bool(
        re.search(
            rf"""os\.(?:environ\s*(?:\[|\.get\s*\()|getenv\s*\()\s*["']{env_var}["']""",
            text,
        )
    )


@pytest.mark.parametrize(
    "env_var",
    ["AIDREAM_URL", "AIDREAM_SERVICE_TOKEN"],
)
def test_aidream_env_is_read_only_by_the_declared_bridges(env_var: str) -> None:
    """The Matrx-microservice bridge is allowed to exist; it may not spread.

    Every OTHER host — aidream in-process, matrx-local, a customer — goes through
    ``configure_ext(...)``. A module outside ``AIDREAM_ENV_READERS`` READING an ``AIDREAM_*``
    variable means someone skipped the seam and re-hardwired the package to us. Naming the
    variable in a message or docstring (the landing hook's remedy sentence does) is not a read.
    """

    readers = {
        str(path.relative_to(PACKAGE_ROOT))
        for path in _shipped_modules()
        if _reads_env(path.read_text(encoding="utf-8"), env_var)
    }
    assert readers <= set(AIDREAM_ENV_READERS), (
        f"{env_var} is read outside the declared bridges: {sorted(readers - set(AIDREAM_ENV_READERS))}. "
        "Inject a host object through configure_ext(...) instead."
    )
    assert "web_crawl/gsc_sync.py" in readers, "the GSC bridge stopped reading its variable — update the list"


def test_the_env_scan_tells_a_read_from_a_mention() -> None:
    assert _reads_env('base = os.environ.get("AIDREAM_URL", "")', "AIDREAM_URL")
    assert _reads_env("t = os.getenv('AIDREAM_SERVICE_TOKEN')", "AIDREAM_SERVICE_TOKEN")
    assert _reads_env('x = os.environ["AIDREAM_URL"]', "AIDREAM_URL")
    assert not _reads_env('"set AIDREAM_URL on this deployment."', "AIDREAM_URL")
