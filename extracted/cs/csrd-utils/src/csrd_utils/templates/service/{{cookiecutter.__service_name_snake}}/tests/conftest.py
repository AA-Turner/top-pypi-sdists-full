"""Shared test fixtures for {{ cookiecutter.service_name }}."""

import pytest
from fastapi.testclient import TestClient

from {{ cookiecutter.__service_name_snake }} import build_app


@pytest.fixture
def client():
    app = build_app()
    return TestClient(app)
