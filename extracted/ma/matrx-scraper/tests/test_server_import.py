"""`matrx_scraper.server` must import — it IS the standalone scraper service.

Regression guard for the 2026-08-09 bug: matrx-connect 0.1.8+ imports
``AsyncSingleFlight`` from matrx_utils (first exported in matrx-utils 2.0.1)
while declaring only ``matrx-utils>=1.0.20``. That floor happily resolves
matrx-utils 2.0.0, so ``pip install matrx-scraper[server]`` produced an
environment where importing the server raised::

    ImportError: cannot import name 'AsyncSingleFlight' from 'matrx_utils'

The service was dead on arrival at startup, and nothing in the suite noticed
because no test ever imported the module.

The import test below SKIPS only when an optional ``[server]`` dependency is
genuinely absent from the environment. It deliberately does NOT catch
ImportError from the import itself — a missing *symbol* is the bug this file
exists to catch, and swallowing it is how a broken server ships silently.
"""

from __future__ import annotations

import importlib
import importlib.util
import tomllib
from pathlib import Path

import pytest

# Top-level distributions the `[server]` extra installs. Absent → the extra is
# not installed here and the import test has nothing to prove. Present → the
# server module MUST import.
_SERVER_EXTRA_MODULES = (
    "fastapi",
    "uvicorn",
    "asyncpg",
    "cachetools",
    "matrx_connect",
    "matrx_orm",
    "matrx_runtime",
)

_PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"


def _missing_server_deps() -> list[str]:
    return [m for m in _SERVER_EXTRA_MODULES if importlib.util.find_spec(m) is None]


def test_server_module_imports() -> None:
    """`import matrx_scraper.server` succeeds against the installed deps."""
    missing = _missing_server_deps()
    if missing:
        pytest.skip(f"matrx-scraper[server] extra not installed (missing: {', '.join(missing)})")

    server = importlib.import_module("matrx_scraper.server")

    assert hasattr(server, "create_app")
    assert hasattr(server, "ServerConfig")


def test_auth_middleware_symbols_resolve() -> None:
    """The exact symbols whose absence broke the server are importable.

    matrx_connect.middleware.auth does `from matrx_utils import AsyncSingleFlight,
    get_inflight_registry, vcprint` at module scope. Pinning them here names the
    failure directly, so a future matrx-utils release that drops one produces a
    pointed failure rather than an opaque server-import traceback.
    """
    if importlib.util.find_spec("matrx_utils") is None:  # pragma: no cover
        pytest.skip("matrx_utils not installed")

    matrx_utils = importlib.import_module("matrx_utils")

    for symbol in ("AsyncSingleFlight", "get_inflight_registry", "vcprint"):
        assert hasattr(matrx_utils, symbol), (
            f"matrx_utils no longer exports {symbol!r}, which "
            f"matrx_connect.middleware.auth imports at module scope"
        )


@pytest.mark.parametrize(
    ("extra", "requirement", "minimum"),
    [
        # The `connect` extra and the `server` extra both pull matrx-connect.
        # 0.1.25 is the first release whose own matrx-utils floor (>=2.0.7)
        # excludes the versions that lack AsyncSingleFlight.
        ("connect", "matrx-connect", (0, 1, 25)),
        ("server", "matrx-connect", (0, 1, 25)),
    ],
)
def test_connect_floor_excludes_broken_resolutions(
    extra: str, requirement: str, minimum: tuple[int, ...]
) -> None:
    """Lowering the matrx-connect floor re-opens the broken resolution."""
    pyproject = tomllib.loads(_PYPROJECT.read_text(encoding="utf-8"))
    specs = pyproject["project"]["optional-dependencies"][extra]

    declared = [s for s in specs if s.replace("_", "-").startswith(f"{requirement}>=")]
    assert declared, f"{requirement} floor missing from the [{extra}] extra"

    for spec in declared:
        floor = tuple(int(p) for p in spec.split(">=", 1)[1].strip().split("."))
        assert floor >= minimum, (
            f"[{extra}] declares {spec!r}; anything below "
            f"{'.'.join(str(p) for p in minimum)} can resolve a matrx-connect "
            f"that ImportErrors on matrx_utils.AsyncSingleFlight"
        )
