"""
Cognitive Version Control (CVC) — Git for the AI Mind.

A state-based middleware system for managing AI agent context using
Merkle DAGs, delta compression, and provider-agnostic caching strategies.
"""

# CRITICAL: Put the vendored CVC runtime on sys.path at the very first
# opportunity. The tools and plugins packages are vendored under
# cvc/agent/_vendor/hermes/, but their internal imports use top-level
# package names (e.g. `import tools.registry`, `import plugins.browser`).
# Without this path injection, EVERY tool fails to load with
# `ModuleNotFoundError: No module named 'tools'`, leaving the agent
# toolless and forcing it to hallucinate answers.
#
# This must run from cvc/__init__.py — not cvc/gateway/__init__.py —
# because the legacy god-file (cvc/gateway_legacy.py) and the
# cvc.daemon subprocesses may import individual cvc submodules
# directly without ever touching cvc.gateway. Putting the path
# injection here guarantees it runs no matter how cvc is loaded.
import sys
from pathlib import Path
_VENDORED_HERMES = Path(__file__).resolve().parent / "agent" / "_vendor" / "hermes"
if str(_VENDORED_HERMES) not in sys.path:
    sys.path.insert(0, str(_VENDORED_HERMES))

from pathlib import Path
import tomllib
from importlib.metadata import version, PackageNotFoundError

def _resolve_version() -> str:
    """Resolve CVC version.

    Priority:
    1) Local source checkout version from pyproject.toml (if present)
    2) Installed package metadata (tm-ai)
    3) Safe fallback
    """
    try:
        root = Path(__file__).resolve().parent.parent
        pyproject = root / "pyproject.toml"
        if pyproject.exists():
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            proj = data.get("project", {})
            ver = proj.get("version")
            if isinstance(ver, str) and ver.strip():
                return ver.strip()
    except Exception:
        pass

    try:
        return version("tm-ai")
    except PackageNotFoundError:
        return "0.0.0"


__version__ = _resolve_version()


# ---------------------------------------------------------------------------
# Backwards-compat alias: `cvc.gateway` (legacy god-file) → `cvc.gateway_legacy`
# ---------------------------------------------------------------------------
# Before the v3.3.0 refactor, CVC had a single 11k-line module at
# `cvc/gateway.py`. Lots of code (including some legacy dashboard
# endpoints under `cvc/dashboard/`) still does `from cvc import gateway`
# or `import cvc.gateway` and then accesses module-level globals
# (e.g. `gateway._workspace_mgr`, `gateway._manager`,
# `gateway.lifespan`, `gateway._SAFE_TOOLS`, `gateway._approval_mode`,
# `gateway._loop_cost_budget_lock`).
#
# After the refactor, `cvc.gateway` is a *package* (containing the new
# `cvc/gateway/app.py` etc.), not a module, so those legacy lookups
# blow up with `AttributeError: module 'cvc.gateway' has no attribute
# '_workspace_mgr'`. This re-export proxy injects the legacy module
# attributes onto the package's namespace so both old and new code
# work in the same process.
#
# This must run AFTER the new package's __init__ has registered any
# of its own names (so we don't clobber them), so we do it at the
# bottom of cvc/__init__.py.
import types as _types

def _install_gateway_legacy_alias() -> None:
    """Backwards-compat shim — real alias lives in cvc/gateway/__init__.py.

    Before the v3.3.0 refactor, CVC had a single 11k-line module at
    ``cvc/gateway.py``. Some legacy code does ``from cvc import gateway
    as gw`` and accesses module-level globals on the result.

    v3.3.6 — The real proxy is now a PEP 562 ``__getattr__`` defined
    inside ``cvc/gateway/__init__.py`` so it lives on the package
    itself and fires for *any* attribute access that doesn't resolve
    on the new package. This shim is a no-op kept for compatibility
    with code that imports ``cvc`` directly without touching
    ``cvc.gateway``.
    """
    return

_install_gateway_legacy_alias()
