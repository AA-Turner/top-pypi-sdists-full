import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load .env from project root so integration tests have PIPE_API_URL, PIPE_API_KEY etc.
# Use path relative to this file so it works regardless of pytest cwd (e.g. when run via Cursor tasks).
_project_root = Path(__file__).resolve().parent.parent
load_dotenv(_project_root / ".env", override=True)


@pytest.fixture(scope="session")
def mock_api_response():
    """Fixture for mocked API responses in unit tests."""
    return {
        "status": "success",
        "data": {
            "id": "test-id",
            "name": "test-name"
        }
    } 