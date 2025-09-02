"""Define test fixtures for Obihai."""

from collections.abc import Generator
from typing import Type
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_response() -> Generator[Type[MagicMock], None, None]:
    """Override _get_response."""
    with patch("pyobihai.requests.Response", new=MagicMock) as mocked_response:
        yield mocked_response
