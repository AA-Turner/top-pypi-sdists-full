from __future__ import annotations


def pytest_configure(config):
    # The filter keeps the state: a traced program must not import this
    # module, only `kolo.filters`.
    from .filters.pytest import pytest_configs

    pytest_configs.append(config)


def pytest_unconfigure(config):
    from .filters.pytest import pytest_configs

    if config in pytest_configs:
        pytest_configs.remove(config)


def pytest_runtest_logstart(nodeid, location):
    """Stub start test hook for PytestFilter"""


def pytest_runtest_logfinish(nodeid, location):
    """Stub end test hook for PytestFilter"""
