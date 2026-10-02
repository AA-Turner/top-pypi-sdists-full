from __future__ import annotations

from typing import Any

import pytest
from langchain_tests.conftest import (
    CustomPersister,
    CustomSerializer,
    base_vcr_config,
)
from vcr import VCR  # type: ignore[import-untyped]


def _remove_response_headers(response: dict[str, Any]) -> dict[str, Any]:
    response["headers"] = {}
    return response


@pytest.fixture(scope="session")
def vcr_config() -> dict[str, Any]:
    config = base_vcr_config()
    config["serializer"] = "yaml.gz"
    config["path_transformer"] = VCR.ensure_suffix(".yaml.gz")
    config["before_record_response"] = _remove_response_headers
    return config


def pytest_recording_configure(config: dict[str, Any], vcr: VCR) -> None:
    del config
    vcr.register_persister(CustomPersister())
    vcr.register_serializer("yaml.gz", CustomSerializer())
