from unittest.mock import patch

from mistralai.workflows.models import WorkflowContext
from mistralai.workflows.plugins.mistralai import utils

_PATCH_CTX = "mistralai.workflows.client.retrieve_context"
_PATCH_BUILDER = "mistralai.workflows.plugins.mistralai.utils._get_mistral_client"


class TestAgentClientHonorsOnBehalfOf:
    def test_uses_executor_credentials_when_obo(self) -> None:
        ctx = WorkflowContext(namespace="ns", execution_id="e", on_behalf_of=True)
        with patch(_PATCH_CTX, return_value=ctx), patch(_PATCH_BUILDER) as builder:
            utils.get_mistral_client()
        assert builder.call_args.kwargs["use_executor_credentials"] is True

    def test_uses_worker_credentials_when_not_obo(self) -> None:
        ctx = WorkflowContext(namespace="ns", execution_id="e", on_behalf_of=False)
        with patch(_PATCH_CTX, return_value=ctx), patch(_PATCH_BUILDER) as builder:
            utils.get_mistral_client()
        assert builder.call_args.kwargs["use_executor_credentials"] is False

    def test_uses_worker_credentials_without_context(self) -> None:
        with patch(_PATCH_CTX, return_value=None), patch(_PATCH_BUILDER) as builder:
            utils.get_mistral_client()
        assert builder.call_args.kwargs["use_executor_credentials"] is False
