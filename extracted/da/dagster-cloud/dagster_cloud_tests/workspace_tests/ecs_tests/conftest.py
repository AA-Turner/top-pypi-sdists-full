import pytest


@pytest.fixture(autouse=True)
def env(monkeypatch):
    # Prevent boto clients from actually connecting to AWS;
    # real connections should only happen in integration tests
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test")
