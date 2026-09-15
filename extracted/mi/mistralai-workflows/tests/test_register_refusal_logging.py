import json
import logging
from http import HTTPStatus
from unittest.mock import AsyncMock

import httpx
import pytest

from mistralai.workflows.core.worker import _register_workflow_specs
from mistralai.workflows.exceptions import WorkflowsException
from mistralai.workflows.worker_client.errors import SDKError


def _forbidden(body: dict) -> SDKError:
    # status_code is read off the response, so a real one is cheaper than faking the attribute.
    return SDKError("Forbidden", httpx.Response(HTTPStatus.FORBIDDEN), json.dumps(body))


async def _refuse(body: dict, caplog: pytest.LogCaptureFixture) -> None:
    client = AsyncMock()
    client.register_workflow_definitions_async.side_effect = _forbidden(body)
    with caplog.at_level(logging.ERROR), pytest.raises(WorkflowsException):
        await _register_workflow_specs(client, [], "dep", "worker", None)


@pytest.mark.asyncio
async def test_refusal_relays_the_server_reason(caplog: pytest.LogCaptureFixture) -> None:
    """The server owns this wording, so it can change without shipping an SDK release.

    It also distinguishes a hardened deployment from an unhardened one, which the fixed sentence
    this replaced could not: it always read as a problem with the API key.
    """
    await _refuse(
        {
            "detail": "Deployment 'dep' is hardened and this principal is not authorized to register on it.",
            "admin_panel_url": "https://admin.example/hardened-deployments?deployment_name=dep",
        },
        caplog,
    )

    assert "is hardened" in caplog.text
    assert "https://admin.example/hardened-deployments?deployment_name=dep" in caplog.text


@pytest.mark.asyncio
async def test_refusal_without_a_remediation_url_is_not_logged(caplog: pytest.LogCaptureFixture) -> None:
    """A 403 from anywhere else in the stack carries no link and is not a registration refusal."""
    await _refuse({"detail": "Some other forbidden thing"}, caplog)

    assert "Workflow registration refused" not in caplog.text
