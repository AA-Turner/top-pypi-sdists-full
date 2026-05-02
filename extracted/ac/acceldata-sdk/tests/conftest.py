import logging
import os
import sys

import pytest


def pytest_sessionstart(session):
    """
    Matches tests/conftest.py pytest_sessionstart().
    Must be called BEFORE importing acceldata_sdk.
    """

    root = logging.getLogger()

    # remove any existing handlers
    for h in list(root.handlers):
        root.removeHandler(h)

    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler.setFormatter(formatter)
    root.addHandler(handler)


@pytest.fixture(scope="session")
def adoc_client():
    from acceldata_sdk.torch_client import TorchClient

    return TorchClient(
        url=os.environ["TORCH_CATALOG_URL"],
        access_key=os.environ["TORCH_ACCESS_KEY"],
        secret_key=os.environ["TORCH_SECRET_KEY"],
        torch_connection_timeout_ms=int(os.getenv("TORCH_CONNECTION_TIMEOUT_MS", "40000")),
        torch_read_timeout_ms=int(os.getenv("TORCH_READ_TIMEOUT_MS", "40000")),
        do_version_check=os.getenv("DO_VERSION_CHECK", "false").lower() == "true",
    )
