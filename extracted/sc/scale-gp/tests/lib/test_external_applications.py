from __future__ import annotations

import os
import logging
from typing import Any, Dict

import httpx
import pytest
from respx import MockRouter

from scale_gp import SGPClient
from tests.utils import assert_matches_type
from scale_gp.lib.external_applications import ExternalApplication, ExternalApplicationOutputCompletion
from scale_gp.types.evaluation_datasets.test_case import TestCase

logger = logging.getLogger(__name__)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


@pytest.fixture
def mock_client(respx_mock: MockRouter) -> SGPClient:
    # Set up default mocks for all tests
    # http://127.0.0.1:4010/v4/application-variants/application_variant_id
    respx_mock.get("/v4/application-variants/application_variant_id").mock(
        return_value=httpx.Response(
            200, json={"id": "application_variant_id", "version": "OFFLINE", "account_id": "test_account"}
        )
    )

    respx_mock.get("/v4/evaluation-datasets/evaluation_dataset_id/test-cases/history/1").mock(
        return_value=httpx.Response(
            200, json={"items": [{"id": "test_case_1", "test_case_data": {"input": "prompt"}, "type": "generation"}]}
        )
    )

    # flexible
    respx_mock.get("/v4/evaluation-datasets/evaluation_dataset_id_2/test-cases/history/1").mock(
        return_value=httpx.Response(
            200,
            json={
                "items": [{"id": "test_case_1", "test_case_data": {"input": {"prompt": "anish"}}, "type": "generation"}]
            },
        )
    )
    respx_mock.post("/v4/application-test-case-outputs/batch").mock(return_value=httpx.Response(200, json={}))

    # Create a client that uses the mocked base URL
    client = SGPClient(base_url=base_url, api_key="test_key")
    return client


class TestExternalApplicationsLibrary:
    @pytest.mark.parametrize("client_type", ["loose", "strict"])
    def test_initialize(self, mock_client: SGPClient, client_type: str) -> None:
        logger.debug(f"Starting test_initialize with client_type: {client_type}")

        try:
            external_app = ExternalApplication(mock_client).initialize(
                application_variant_id="application_variant_id",
                application=lambda prompt: ExternalApplicationOutputCompletion(generation_output=prompt),
            )
            logger.debug("ExternalApplication initialized successfully")
            assert external_app._initialized
        except Exception as e:
            logger.error(f"Error during initialization: {str(e)}")
            raise

    def test_generate_application_with_prompt(self, mock_client: SGPClient) -> None:
        def application(prompt: str) -> ExternalApplicationOutputCompletion:
            assert_matches_type(str, prompt, path=["application", "prompt"])
            return ExternalApplicationOutputCompletion(generation_output=prompt)

        external_application = ExternalApplication(mock_client).initialize(
            application_variant_id="application_variant_id",
            application=application,
        )
        external_application.generate_outputs(
            evaluation_dataset_id="evaluation_dataset_id",
            evaluation_dataset_version=1,
        )

    def test_generate_application_with_prompt_and_test_case(self, mock_client: SGPClient) -> None:
        def application(prompt: str, test_case: TestCase) -> ExternalApplicationOutputCompletion:
            assert_matches_type(str, prompt, path=["application", "prompt"])
            # assert_matches_type(TestCase, test_case, path=["application", "test_case"])
            logger.debug(f"complete test case: {test_case}")  # for linting
            return ExternalApplicationOutputCompletion(generation_output=prompt)

        external_application = ExternalApplication(mock_client).initialize(
            application_variant_id="application_variant_id",
            application=application,
        )
        external_application.generate_outputs(
            evaluation_dataset_id="evaluation_dataset_id",
            evaluation_dataset_version=1,
        )

    def test_generate_application_with_flexible_prompt_and_test_case(self, mock_client: SGPClient) -> None:
        def application(prompt: Dict[str, Any], test_case: TestCase) -> ExternalApplicationOutputCompletion:
            assert_matches_type(Dict[str, str], prompt, path=["application", "prompt"])
            # assert_matches_type(TestCase, test_case, path=["application", "test_case"])
            logger.debug(f"complete test case: {test_case}")  # for linting
            return ExternalApplicationOutputCompletion(generation_output="output")

        external_application = ExternalApplication(mock_client).initialize(
            application_variant_id="application_variant_id",
            application=application,
        )
        external_application.generate_outputs(
            evaluation_dataset_id="evaluation_dataset_id_2",
            evaluation_dataset_version=1,
        )
