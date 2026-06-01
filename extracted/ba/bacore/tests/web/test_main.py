"""Test cases for BACore documentation with FastHTML."""

import pytest
from bacore.web.main import app
from starlette.testclient import TestClient

client = TestClient(app)


def test_headers():
    headers = client.headers
    assert headers.get("user-agent") == "testclient", headers


def test_home():
    response = client.get("/")
    assert response, f"\nHeaders: {response.headers}\nText:{response.text}"


def test_docs():
    response = client.get("/docs")
    assert response, f"\nHeaders: {response.headers}\nText:{response.text}"


def test_docs_slash():
    response = client.get("/docs/")
    assert response, f"\nHeaders: {response.headers}\nText:{response.text}"


def test_docs_domain():
    """Test case for docs/domain without a slash.

    TODO: Correct so that optional slashes are handled correctly.
    """
    with pytest.raises(ValueError):
        client.get("/docs/domain")


def test_docs_domain_slash():
    response = client.get("/docs/domain/")
    assert response, f"\nHeaders: {response.headers}\nText:{response.text}"


def test_tests():
    """Test case for tests without a slash.

    TODO: Fix this
    """
    with pytest.raises(ValueError):
        client.get("/tests")


def test_tests_slash():
    """Test case for tests without a slash.

    TODO: Correct so that optional slashes are handled correctly.
    """
    with pytest.raises(ValueError):
        client.get("/tests/")
