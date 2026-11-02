"""hugpy_core — hugpy central, minimal: live worker registry, model->worker
pick, and the OpenAI /v1 relay to workers (hugpy_worker over fitevict)."""
# the installed dist's version (the vault bumps pyproject on every release; a
# constant here went stale and every box reported 0.1.0)
try:
    from importlib.metadata import version as _version
    __version__ = _version("hugpy-core")
except Exception:  # noqa: BLE001 — running from a source tree with no install
    __version__ = "0+unknown"
