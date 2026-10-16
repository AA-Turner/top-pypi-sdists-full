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


_DEPLOYMENT_URL = (
    "https://console.example/build/workflows/deployments/dep"
    "?shareContext=%7B%22organizationId%22%3A%2200000000-0000-4000-8000-000000000001%22%2C"
    "%22workspaceId%22%3A%2200000000-0000-4000-8000-000000000002%22%7D&tab=settings"
)
_ADMIN_URL = "https://admin.example/hardened-deployments?deployment_name=dep"


@pytest.mark.asyncio
async def test_refusal_relays_the_server_reason(caplog: pytest.LogCaptureFixture) -> None:
    """The server owns this wording, so it can change without shipping an SDK release.

    It also distinguishes a hardened deployment from an unhardened one, which the fixed sentence
    this replaced could not: it always read as a problem with the API key.
    """
    await _refuse(
        {
            "detail": "Deployment 'dep' is hardened and this principal is not authorized to register on it.",
            "code": "WF_1104",
            "admin_panel_url": _ADMIN_URL,
        },
        caplog,
    )

    assert "is hardened" in caplog.text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("urls", "expected", "absent"),
    [
        pytest.param(
            {"deployment_url": _DEPLOYMENT_URL, "admin_panel_url": _ADMIN_URL},
            _DEPLOYMENT_URL,
            _ADMIN_URL,
            id="prefers_the_deployment_page",
        ),
        pytest.param({"admin_panel_url": _ADMIN_URL}, _ADMIN_URL, None, id="falls_back_to_the_admin_panel"),
    ],
)
async def test_refusal_logs_the_deployment_page_when_the_server_sends_one(
    urls: dict[str, str], expected: str, absent: str | None, caplog: pytest.LogCaptureFixture
) -> None:
    await _refuse({"detail": "Deployment 'dep' is hardened.", "code": "WF_1104", **urls}, caplog)

    assert expected in caplog.text
    if absent is not None:
        assert absent not in caplog.text


@pytest.mark.asyncio
async def test_refusal_without_a_remediation_url_relays_the_server_reason(
    caplog: pytest.LogCaptureFixture,
) -> None:
    reason = "The user associated with this worker credential cannot use Workflows."
    await _refuse({"detail": reason, "code": "WF_1104"}, caplog)

    assert reason in caplog.text


@pytest.mark.asyncio
async def test_unrelated_forbidden_response_is_not_logged(caplog: pytest.LogCaptureFixture) -> None:
    await _refuse({"detail": "Some other forbidden thing"}, caplog)

    assert "Workflow registration refused" not in caplog.text
