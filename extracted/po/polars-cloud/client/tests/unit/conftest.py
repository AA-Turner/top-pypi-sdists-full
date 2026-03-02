# mypy: disable-error-code="attr-defined,return-value,no-untyped-def"
from __future__ import annotations

import os

import pytest
from polars_cloud import constants
from polars_cloud.context import cache as context_cache

from tests.unit.utilities import access_token


@pytest.fixture(scope="session")
def monkeypatch_session():
    """Allow session-scoped monkeypatching."""
    with pytest.MonkeyPatch.context() as mp:
        yield mp


@pytest.fixture
def _set_up_access_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(constants.ACCESS_TOKEN, access_token())


@pytest.fixture(autouse=True)
def _reset_access_token_cache():
    """Make sure each test starts with a fresh cache."""
    context_cache.cached_context = None
    os.environ.pop(constants.CLIENT_ID, None)
    os.environ.pop(constants.CLIENT_SECRET, None)


@pytest.fixture(autouse=True)
def _change_access_token_path(tmp_path) -> None:
    """Make sure we don't use the local access token."""
    if not os.environ.get(constants.ACCESS_TOKEN_PATH):
        os.environ[constants.ACCESS_TOKEN_PATH] = str(tmp_path)
