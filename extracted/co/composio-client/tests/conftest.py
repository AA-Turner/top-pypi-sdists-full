from __future__ import annotations

import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

from composio_client import AsyncComposio, Composio, ProjectAuth

# `scripts/` is not a package: `parity_driver.py` and `wire_corpus.py` import
# each other flat, because that is how they resolve under the isolated
# interpreter the parity lanes actually run in. Putting the directory on the
# path lets a test import them the same way the driver does, rather than under
# a second module name the driver would never see.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

BASE_URL = "https://api.test"
API_KEY = "ak_test_123"


@pytest.fixture
def client() -> Iterator[Composio]:
    client = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
    yield client
    client.close()


@pytest.fixture
def async_client() -> AsyncComposio:
    return AsyncComposio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
