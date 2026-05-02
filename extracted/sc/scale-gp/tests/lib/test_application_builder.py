from __future__ import annotations

import pytest

from scale_gp import SGPClient
from scale_gp.lib.application_builder import ApplicationBuilder


class TestApplicationBuilderLibrary:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_create_completion_application(self, client: SGPClient) -> None:
        ApplicationBuilder(client).create_completion_application(
            account_id="account_id",
            application_name="test_application_name",
            completion_model_id="completion_model_id",
        )

    @parametrize
    def test_create_rag_application(self, client: SGPClient) -> None:
        ApplicationBuilder(client).create_rag_application(
            account_id="account_id",
            application_name="test_application_name",
            completion_model_id="completion_model_id",
            knowledge_base_id="knowledge_base_id",
            knowledge_base_top_k=1,
            prompt_engineering_template="prompt_engineering_template",
            reranker_model_id="reranker_model_id",
            reranker_top_k=1,
        )
