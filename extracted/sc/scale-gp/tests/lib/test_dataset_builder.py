from __future__ import annotations

import os

import pytest

from scale_gp import SGPClient
from scale_gp.lib.dataset_builder import DatasetBuilder
from scale_gp.lib.types.multiturn import MultiturnTestCaseSchema
from scale_gp.lib.types.summarization import SummarizationTestCaseSchema
from scale_gp.types.evaluation_datasets import FlexibleTestCaseSchema

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDatasetBuilderLibrary:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_initialize_flexible(self, client: SGPClient) -> None:
        DatasetBuilder(client).initialize(
            account_id="account_id",
            name="dataset-builder",
            test_cases=[
                FlexibleTestCaseSchema(
                    input={"test-string": "string", "array": [1, 2, 3]},
                    expected_output={
                        "test-num": 1,
                        "object": {"foo": 1, "awesome": True},
                    },
                ),
                FlexibleTestCaseSchema(
                    input={"test-string": "string", "array": [1, 2, 3]},
                    expected_output={
                        "test-num": 1,
                        "object": {"foo": 1, "awesome": True},
                    },
                ),
            ],
        )

    @parametrize
    def test_initialize_summarization(self, client: SGPClient) -> None:
        DatasetBuilder(client).initialize(
            account_id="account_id",
            name="dataset-builder",
            test_cases=[
                SummarizationTestCaseSchema(document="test-document", expected_summary="expected-summary"),
                SummarizationTestCaseSchema(document="test-document", expected_summary="expected-summary"),
            ],
        )

    @parametrize
    def test_initialize_multiturn(self, client: SGPClient) -> None:
        DatasetBuilder(client).initialize(
            account_id="account_id",
            name="dataset-builder",
            test_cases=[
                MultiturnTestCaseSchema(
                    messages=[
                        {"role": "user", "content": "What is the capital of France?"},
                        {"role": "assistant", "content": "The capital of France is Paris."},
                        {"role": "user", "content": "Thank you!"},
                    ],
                    expected_messages=[
                        {"role": "user", "content": "What is the capital of France?"},
                        {"role": "assistant", "content": "The capital of France is Paris."},
                        {"role": "user", "content": "Thank you!"},
                    ],
                ),
                MultiturnTestCaseSchema(
                    messages=[
                        {"role": "user", "content": "What is the capital of France?"},
                        {"role": "assistant", "content": "The capital of France is Paris."},
                        {"role": "user", "content": "Thank you!"},
                    ],
                    turns=[1],
                    expected_messages=[
                        {"role": "user", "content": "What is the capital of France?"},
                        {"role": "assistant", "content": "The capital of France is Paris."},
                        {"role": "user", "content": "Thank you!"},
                    ],
                ),
            ],
        )
