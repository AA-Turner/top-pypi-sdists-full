from unittest.mock import patch
from uuid import UUID

import httpx
from typer.testing import CliRunner

from runlayer_cli.config import Config, HostConfig
from runlayer_cli.main import app


runner = CliRunner()


class FakeResponse:
    def raise_for_status(self):
        return None


class FakeClient:
    def __init__(self, response=None):
        self.posts = []
        self._response = response or FakeResponse()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def post(self, url, json=None):
        self.posts.append((url, json))
        return self._response


def _error_client(status_code, payload):
    """A client whose POST raises HTTPStatusError the way httpx would."""
    response = httpx.Response(
        status_code,
        json=payload,
        request=httpx.Request("POST", "https://ecs.prod.runlayer.com"),
    )

    class ErroringClient(FakeClient):
        def post(self, url, json=None):
            self.posts.append((url, json))
            raise httpx.HTTPStatusError(
                "boom", request=response.request, response=response
            )

    return ErroringClient(response)


def _run_with(fake_client, request_id, flag="--approve"):
    host = "https://ecs.prod.runlayer.com"
    config = Config(
        default_host=host,
        hosts={"ecs.prod.runlayer.com": HostConfig(url=host, secret="rl_user_secret")},
    )
    with (
        patch("runlayer_cli.commands.decide_approval.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=None),
        patch(
            "runlayer_cli.commands.decide_approval.http_client",
            return_value=fake_client,
        ),
    ):
        return runner.invoke(
            app,
            [
                "__decide-approval",
                "--approval-request-id",
                str(request_id),
                flag,
            ],
        )


def test_decide_approval_surfaces_policy_rejection_reason():
    """The tray echoes stderr, so the server's reason has to reach it."""
    result = _run_with(
        _error_client(
            403, {"detail": "This approval must be decided in the dashboard"}
        ),
        UUID("dddddddd-dddd-dddd-dddd-dddddddddddd"),
    )

    assert result.exit_code == 1
    assert "This approval must be decided in the dashboard" in result.output


def test_decide_approval_surfaces_already_decided_conflict():
    result = _run_with(
        _error_client(
            409,
            {
                "detail": {
                    "message": "Approval request already decided",
                    "status": "approved",
                }
            },
        ),
        UUID("eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"),
    )

    assert result.exit_code == 1
    assert "Approval request already decided" in result.output
    assert "approved" in result.output


def test_decide_approval_falls_back_to_status_for_unparsable_errors():
    response = httpx.Response(
        500,
        text="<html>nope</html>",
        request=httpx.Request("POST", "https://ecs.prod.runlayer.com"),
    )

    class ErroringClient(FakeClient):
        def post(self, url, json=None):
            raise httpx.HTTPStatusError(
                "boom", request=response.request, response=response
            )

    result = _run_with(
        ErroringClient(response), UUID("ffffffff-ffff-ffff-ffff-ffffffffffff")
    )

    assert result.exit_code == 1
    assert "HTTP 500" in result.output


def test_decide_approval_posts_approve_decision():
    host = "https://ecs.prod.runlayer.com"
    request_id = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
    fake_client = FakeClient()
    config = Config(
        default_host=host,
        hosts={"ecs.prod.runlayer.com": HostConfig(url=host, secret="rl_user_secret")},
    )

    with (
        patch("runlayer_cli.commands.decide_approval.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=None),
        patch(
            "runlayer_cli.commands.decide_approval.http_client",
            return_value=fake_client,
        ),
    ):
        result = runner.invoke(
            app,
            [
                "__decide-approval",
                "--approval-request-id",
                str(request_id),
                "--approve",
            ],
        )

    assert result.exit_code == 0, result.output
    assert fake_client.posts == [
        (
            f"{host}/api/v1/approvals/{request_id}/decision",
            {"approve": True},
        )
    ]


def test_decide_approval_posts_prevent_decision():
    host = "https://ecs.prod.runlayer.com"
    request_id = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
    fake_client = FakeClient()
    config = Config(
        default_host=host,
        hosts={"ecs.prod.runlayer.com": HostConfig(url=host, secret="rl_user_secret")},
    )

    with (
        patch("runlayer_cli.commands.decide_approval.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=None),
        patch(
            "runlayer_cli.commands.decide_approval.http_client",
            return_value=fake_client,
        ),
    ):
        result = runner.invoke(
            app,
            [
                "__decide-approval",
                "--approval-request-id",
                str(request_id),
                "--prevent",
            ],
        )

    assert result.exit_code == 0, result.output
    assert fake_client.posts == [
        (
            f"{host}/api/v1/approvals/{request_id}/decision",
            {"approve": False},
        )
    ]


def test_decide_approval_requires_exactly_one_decision():
    request_id = UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")

    result = runner.invoke(
        app,
        ["__decide-approval", "--approval-request-id", str(request_id)],
    )

    assert result.exit_code == 1
    assert "Choose exactly one" in result.output
