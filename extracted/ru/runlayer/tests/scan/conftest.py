"""Shared fixtures for scan tests."""

import pytest

from runlayer_cli.scan.containers import collect as containers_module


@pytest.fixture(autouse=True)
def _distinct_cli_runtimes_absent(monkeypatch):
    """Default podman/nerdctl to absent so container-scan tests stay hermetic
    on hosts that have them installed; tests opt in by re-patching."""
    monkeypatch.setattr(
        containers_module,
        "_find_container_cli",
        lambda _binary: None,
    )
