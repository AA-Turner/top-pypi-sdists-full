import base64
import json
from contextlib import nullcontext
from unittest.mock import patch

import httpx
import pytest
from pydantic import SecretStr

from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.temporal.context_handler_interceptor import define_context
from mistralai.workflows.exceptions import WorkflowError
from mistralai.workflows.models import WorkflowContext
from mistralai.workflows.plugins.mistralai import utils
from mistralai.workflows.plugins.mistralai.connectors.run_as import ConnectorRunAs


class TestAgentClientHonorsOnBehalfOf:
    @pytest.mark.parametrize("on_behalf_of", [True, False, None], ids=["obo", "non-obo", "no-context"])
    @pytest.mark.parametrize("async_call", [True, False], ids=["async", "sync"])
    async def test_default_client_uses_request_identity(self, monkeypatch, on_behalf_of, async_call):
        payload = base64.urlsafe_b64encode(json.dumps({"exp": 4102444800}).encode()).rstrip(b"=").decode()
        executor_jwt = f"header.{payload}.signature"
        requests: list[httpx.Request] = []

        def handle(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            if request.url.path.endswith("/executor-identity-token"):
                assert request.headers["Authorization"] == "Bearer worker-key"
                assert json.loads(request.content)["execution_token"] == "execution-token"
                return httpx.Response(200, json={"token": executor_jwt})
            return httpx.Response(200, json={"data": [], "object": "list"})

        monkeypatch.setattr(config.http, "transport_factory", lambda _: httpx.MockTransport(handle))
        monkeypatch.setattr(config.worker.agent, "mistral_client_api_key", SecretStr("worker-key"))
        monkeypatch.setattr(config.worker.agent, "mistral_client_server_url", "https://api.example")
        client = utils.get_mistral_client()
        assert not requests
        context = (
            None
            if on_behalf_of is None
            else WorkflowContext(
                namespace="ns", execution_id="exec", execution_token="execution-token", on_behalf_of=on_behalf_of
            )
        )
        try:
            with (
                define_context(context),
                pytest.raises(WorkflowError, match="AUTO requires a workflow context")
                if context is None
                else nullcontext() as error,
            ):
                if async_call:
                    await client.models.list_async()
                else:
                    client.models.list()
            if context is None:
                assert error.value.non_retryable
                assert not requests
                return
            expected = executor_jwt if on_behalf_of else "worker-key"
            assert requests[-1].headers["Authorization"] == f"Bearer {expected}"
            assert len(requests) == (2 if on_behalf_of else 1)
        finally:
            await client.sdk_configuration.async_client.aclose()
            client.sdk_configuration.client.close()


class TestAgentClientRunAs:
    @pytest.mark.parametrize("on_behalf_of", [True, False, None])
    @pytest.mark.parametrize("run_as", list(ConnectorRunAs))
    def test_identity_policy_does_not_capture_construction_context(
        self, run_as: ConnectorRunAs, on_behalf_of: bool | None
    ) -> None:
        context = (
            None
            if on_behalf_of is None
            else WorkflowContext(namespace="ns", execution_id="exec", on_behalf_of=on_behalf_of)
        )
        with (
            define_context(context),
            patch("mistralai.workflows.plugins.mistralai.utils._get_mistral_client") as builder,
        ):
            utils.get_mistral_client(run_as)
        assert builder.call_args.kwargs["run_as"] is run_as
