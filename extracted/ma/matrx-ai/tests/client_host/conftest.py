"""Fixtures for the client-host seam tests.

These tests run inside the shared pytest process (which conftest-configures
stub DB models for the whole suite), so every seam a test injects into the
GLOBAL ``_ext`` registry / runtime-model registry must be rolled back — a
leaked ``conversation_store`` or ``model_catalog`` would silently re-route
every later test in the session.
"""

from __future__ import annotations

import pytest


@pytest.fixture
def client_host_sandbox():
    """Snapshot + restore the global seam registries around a test."""
    from matrx_ai import _ext
    from matrx_ai.catalog import host_catalog

    saved_registry = dict(_ext._registry)
    saved_configured = _ext._configured
    saved_runtime = dict(host_catalog._runtime_models)
    try:
        yield
    finally:
        _ext._registry.clear()
        _ext._registry.update(saved_registry)
        _ext._configured = saved_configured
        host_catalog._runtime_models.clear()
        host_catalog._runtime_models.update(saved_runtime)
