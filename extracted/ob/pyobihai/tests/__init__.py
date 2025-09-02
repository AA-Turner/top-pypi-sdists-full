"""PyObihai Tests."""

from unittest.mock import MagicMock


class MockResponse(MagicMock):
    """Mock HTTP Response Object"""

    def __init__(self, text: str, status_code: int):
        super().__init__()
        self.text = text
        self.status_code = status_code
