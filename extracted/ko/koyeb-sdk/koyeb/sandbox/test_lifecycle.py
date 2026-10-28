import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from koyeb.api.models.deployment_definition import DeploymentDefinition
from koyeb.api_async.models.deployment_definition import (
    DeploymentDefinition as AsyncDeploymentDefinition,
)
from koyeb.sandbox.sandbox import AsyncSandbox, Sandbox


def _make_clients():
    clients = MagicMock()
    clients.services.get_service.return_value.service.life_cycle = None
    clients.deployments.get_deployment.return_value.deployment.definition = (
        DeploymentDefinition(name="sb")
    )
    return clients


def _make_sandbox(cls=Sandbox):
    return cls(
        sandbox_id="sb",
        app_id="app-id",
        service_id="svc-id",
        name="sb",
        api_token="tok",
        sandbox_secret="secret",
    )


class TestUpdateLifecycle(unittest.TestCase):
    """update_lifecycle pins the replacement deployment its update creates,
    mirroring update_network_policy: a later wait_ready() polls the new
    deployment, and cached connection state is dropped."""

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_pins_new_deployment_and_resets_cached_state(self, mock_get_clients):
        clients = _make_clients()
        clients.services.update_service.return_value.service.latest_deployment_id = (
            "new-dep"
        )
        mock_get_clients.return_value = clients

        sandbox = _make_sandbox()
        stale_client = MagicMock()
        sandbox._deployment_id = "old-dep"
        sandbox._sandbox_url = ("https://old/koyeb-sandbox", "old-key")
        sandbox._url = "https://old"
        sandbox._domain = "old"
        sandbox._client = stale_client

        sandbox.update_lifecycle(delete_after_delay=600)

        self.assertEqual(sandbox._deployment_id, "new-dep")
        self.assertIsNone(sandbox._sandbox_url)
        self.assertIsNone(sandbox._url)
        self.assertIsNone(sandbox._domain)
        self.assertIsNone(sandbox._client)
        stale_client.close.assert_called_once()

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_falls_back_to_get_service_when_reply_lacks_deployment_id(
        self, mock_get_clients
    ):
        clients = _make_clients()
        clients.services.update_service.return_value.service.latest_deployment_id = None
        clients.services.get_service.return_value.service.latest_deployment_id = (
            "new-dep"
        )
        mock_get_clients.return_value = clients

        sandbox = _make_sandbox()
        sandbox.update_lifecycle()

        self.assertEqual(sandbox._deployment_id, "new-dep")

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_failed_id_lookup_does_not_fail_the_update(self, mock_get_clients):
        from types import SimpleNamespace

        clients = _make_clients()
        clients.services.update_service.return_value.service.latest_deployment_id = None
        # The first get_service (definition read) succeeds; only the fallback
        # id lookup fails.
        clients.services.get_service.side_effect = [
            SimpleNamespace(
                service=SimpleNamespace(latest_deployment_id="dep-1", life_cycle=None)
            ),
            RuntimeError("lookup blew up"),
        ]
        mock_get_clients.return_value = clients

        sandbox = _make_sandbox()
        sandbox.update_lifecycle(delete_after_delay=600)

        self.assertIsNone(sandbox._deployment_id)


class TestAsyncUpdateLifecycle(unittest.TestCase):
    """The async twin pins the replacement deployment too."""

    @patch("koyeb.sandbox.clients.get_async_api_clients")
    def test_pins_new_deployment_and_resets_cached_state(self, mock_get_clients):
        clients = MagicMock()
        clients.services.get_service = AsyncMock()
        clients.deployments.get_deployment = AsyncMock()
        clients.deployments.get_deployment.return_value.deployment.definition = (
            AsyncDeploymentDefinition(name="sb")
        )
        clients.services.get_service.return_value.service.life_cycle = None
        clients.services.update_service = AsyncMock()
        clients.services.update_service.return_value.service.latest_deployment_id = (
            "new-dep"
        )
        mock_get_clients.return_value = clients

        async def run():
            sandbox = _make_sandbox(AsyncSandbox)
            sandbox._deployment_id = "old-dep"
            sandbox._sandbox_url = ("https://old/koyeb-sandbox", "old-key")
            await sandbox.update_lifecycle(delete_after_delay=600)

            self.assertEqual(sandbox._deployment_id, "new-dep")
            self.assertIsNone(sandbox._sandbox_url)

        asyncio.run(run())
