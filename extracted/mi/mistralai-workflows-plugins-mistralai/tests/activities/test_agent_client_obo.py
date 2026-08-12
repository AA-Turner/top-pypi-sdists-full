from unittest.mock import patch

import pytest

from mistralai.workflows.models import WorkflowContext
from mistralai.workflows.plugins.mistralai import utils
from mistralai.workflows.plugins.mistralai.connectors.run_as import ConnectorRunAs

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


class TestAgentClientRunAs:
    @pytest.mark.parametrize(
        ("run_as", "on_behalf_of", "expected"),
        [
            pytest.param(ConnectorRunAs.DEPLOYMENT, True, False, id="deployment-overrides-obo"),
            pytest.param(ConnectorRunAs.AUTO, True, True, id="auto-follows-obo"),
            pytest.param(ConnectorRunAs.AUTO, False, False, id="auto-no-obo"),
            pytest.param(ConnectorRunAs.DEPLOYMENT, None, False, id="deployment-no-context"),
        ],
    )
    def test_run_as_resolves_executor_credentials(
        self, run_as: ConnectorRunAs, on_behalf_of: bool | None, expected: bool
    ) -> None:
        ctx = (
            None
            if on_behalf_of is None
            else WorkflowContext(namespace="ns", execution_id="e", on_behalf_of=on_behalf_of)
        )
        with patch(_PATCH_CTX, return_value=ctx), patch(_PATCH_BUILDER) as builder:
            utils.get_mistral_client(run_as)
        assert builder.call_args.kwargs["use_executor_credentials"] is expected
