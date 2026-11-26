"""Pins Sandbox.create(sidecars=): argument checks before any API call, the
create order (sidecars, wait, sandbox), cleanup on failure, and that
create without sidecars is unchanged."""

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from koyeb.api.models.deployment_status import DeploymentStatus
from koyeb.api.models.mesh_scope import MeshScope
from koyeb.sandbox import AsyncSandbox, Sandbox, Sidecar, SidecarError


def _proxy(name="proxy", ports=(8080,)):
    return Sidecar(name=name, image="mitmproxy/mitmproxy", ports=list(ports))


def _clients(statuses=None):
    """Sync API mock: each created service gets an id; deployments report
    the given statuses in turn (default HEALTHY)."""
    clients = MagicMock()
    clients.apps.create_app.return_value.app.id = "app-id"
    counter = {"n": 0}

    def create_service(service):
        counter["n"] += 1
        reply = MagicMock()
        reply.service.id = f"svc-{counter['n']}"
        return reply

    clients.services.create_service.side_effect = create_service
    clients.services.get_service.return_value.service.latest_deployment_id = "dep"
    seq = list(statuses or [])

    def get_deployment(id):
        reply = MagicMock()
        reply.deployment.status = seq.pop(0) if seq else DeploymentStatus.HEALTHY
        reply.deployment.metadata = None
        reply.deployment.definition = None
        return reply

    clients.deployments.get_deployment.side_effect = get_deployment
    return clients


def _created(clients):
    return [c.kwargs["service"] for c in clients.services.create_service.call_args_list]


class TestCreateWithoutSidecars(unittest.TestCase):
    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_unchanged(self, mock_get_clients):
        for sidecars in (None, []):
            clients = _clients()
            mock_get_clients.return_value = clients
            sb = Sandbox.create(
                name="sb", api_token="tok", wait_ready=False, sidecars=sidecars
            )
            services = _created(clients)
            self.assertEqual(len(services), 1)
            self.assertIsNone(services[0].definition.network_policy)
            self.assertEqual(sb.sidecars, [])


class TestSidecarArgumentChecks(unittest.TestCase):
    """Every conflict fails before any API call."""

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_conflicts(self, mock_get_clients):
        cases = [
            {"app_id": "app"},
            {"snapshot": "snap"},
            {"block_network": True},
            {"outbound_allowlist": ["1.2.3.4"]},
            {"enable_mesh": False},
            {"mesh_scope": "MESH_SCOPE_WORKSPACE"},
        ]
        for kwargs in cases:
            with self.subTest(**kwargs), self.assertRaises(SidecarError):
                Sandbox.create(
                    name="sb", api_token="tok", sidecars=[_proxy()], **kwargs
                )
        mock_get_clients.assert_not_called()

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_name_clashes(self, mock_get_clients):
        with self.assertRaises(SidecarError):
            Sandbox.create(name="sb", api_token="tok", sidecars=[_proxy(), _proxy()])
        with self.assertRaises(SidecarError):
            Sandbox.create(name="proxy", api_token="tok", sidecars=[_proxy()])
        mock_get_clients.assert_not_called()

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_explicit_app_scope_and_mesh_allowed(self, mock_get_clients):
        mock_get_clients.return_value = _clients()
        Sandbox.create(
            name="sb",
            api_token="tok",
            wait_ready=False,
            sidecars=[_proxy()],
            enable_mesh=True,
            mesh_scope=MeshScope.MESH_SCOPE_APP,
        )


class TestCreateWithSidecars(unittest.TestCase):
    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_order_and_definitions(self, mock_get_clients):
        clients = _clients()
        mock_get_clients.return_value = clients
        sb = Sandbox.create(
            name="sb",
            api_token="tok",
            region="fra",
            wait_ready=False,
            delete_after_delay=600,
            sidecars=[_proxy(), _proxy(name="db", ports=(5432,))],
        )
        services = _created(clients)
        self.assertEqual([s.name for s in services], ["proxy", "db", "sb"])
        self.assertEqual(clients.apps.create_app.call_count, 1)
        for s in services:
            self.assertEqual(s.app_id, "app-id")
            self.assertEqual(
                s.definition.network_policy.mesh.scope, MeshScope.MESH_SCOPE_APP
            )
            self.assertEqual(s.definition.mesh.value, "DEPLOYMENT_MESH_ENABLED")
            self.assertEqual(s.definition.regions, ["fra"])
            self.assertEqual(s.life_cycle.delete_after_create, 600)
        self.assertEqual(services[0].definition.type.value, "WEB")
        self.assertEqual(services[2].definition.type.value, "SANDBOX")
        self.assertEqual([i.name for i in sb.sidecars], ["proxy", "db"])
        self.assertEqual(sb.sidecar("db").service_id, "svc-2")
        self.assertEqual(sb.sidecar("proxy").url(), "http://proxy:8080")
        self.assertEqual(sb.sidecar("db").url(scheme="postgres"), "postgres://db:5432")
        with self.assertRaises(SidecarError):
            sb.sidecar("nope")

    @patch("koyeb.sandbox.sandbox.time.sleep")
    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_waits_for_sidecars_before_creating_sandbox(self, mock_get_clients, _sleep):
        clients = _clients(
            [
                DeploymentStatus.STARTING,
                DeploymentStatus.STARTING,
                DeploymentStatus.HEALTHY,
            ]
        )
        mock_get_clients.return_value = clients
        events = []
        clients.services.create_service.side_effect = lambda service: events.append(
            ("create", service.name)
        ) or MagicMock(service=MagicMock(id=f"svc-{service.name}"))
        original = clients.deployments.get_deployment.side_effect
        clients.deployments.get_deployment.side_effect = lambda id: (
            events.append(("poll", None)) or original(id)
        )
        with patch.object(Sandbox, "wait_ready", return_value=True):
            Sandbox.create(name="sb", api_token="tok", sidecars=[_proxy()])
        first_sandbox = events.index(("create", "sb"))
        self.assertEqual(events[0], ("create", "proxy"))
        self.assertEqual(events[1:first_sandbox], [("poll", None)] * 3)

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_failed_sidecar_deletes_app(self, mock_get_clients):
        clients = _clients([DeploymentStatus.ERROR])
        mock_get_clients.return_value = clients
        with self.assertRaises(SidecarError) as ctx:
            Sandbox.create(name="sb", api_token="tok", sidecars=[_proxy()])
        self.assertIn("app was deleted", str(ctx.exception))
        clients.apps.delete_app.assert_called_once_with("app-id")
        self.assertEqual([s.name for s in _created(clients)], ["proxy"])

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_failed_sidecar_keeps_app_without_cleanup(self, mock_get_clients):
        clients = _clients([DeploymentStatus.ERROR])
        mock_get_clients.return_value = clients
        with self.assertRaises(SidecarError) as ctx:
            Sandbox.create(
                name="sb",
                api_token="tok",
                sidecars=[_proxy()],
                cleanup_on_failure=False,
            )
        self.assertIn("kept for inspection", str(ctx.exception))
        clients.apps.delete_app.assert_not_called()

    @patch("koyeb.sandbox.sandbox.time.sleep")
    @patch("koyeb.sandbox.sandbox.time.time")
    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_sidecar_timeout_deletes_app(self, mock_get_clients, mock_time, _sleep):
        clients = _clients([DeploymentStatus.STARTING] * 10)
        mock_get_clients.return_value = clients
        mock_time.side_effect = [0, 0, 0, 100, 100, 100, 100]
        with self.assertRaises(SidecarError) as ctx:
            Sandbox.create(name="sb", api_token="tok", sidecars=[_proxy()], timeout=50)
        self.assertIn("did not become healthy within 50 seconds", str(ctx.exception))
        clients.apps.delete_app.assert_called_once_with("app-id")

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_sidecar_create_api_error_deletes_app(self, mock_get_clients):
        from koyeb.api.exceptions import ApiException

        clients = _clients()
        clients.services.create_service.side_effect = ApiException(
            status=400, reason="bad"
        )
        mock_get_clients.return_value = clients
        with self.assertRaises(SidecarError):
            Sandbox.create(name="sb", api_token="tok", sidecars=[_proxy()])
        clients.apps.delete_app.assert_called_once_with("app-id")

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_no_wait_skips_polling(self, mock_get_clients):
        clients = _clients()
        mock_get_clients.return_value = clients
        Sandbox.create(
            name="sb", api_token="tok", wait_ready=False, sidecars=[_proxy()]
        )
        clients.deployments.get_deployment.assert_not_called()


class TestAsyncCreateWithSidecars(unittest.TestCase):
    def _async_clients(self, status=DeploymentStatus.HEALTHY):
        clients = MagicMock()
        clients.apps.create_app = AsyncMock()
        clients.apps.create_app.return_value.app.id = "app-id"
        clients.apps.delete_app = AsyncMock()
        names = []

        async def create_service(service):
            names.append(service.name)
            return MagicMock(service=MagicMock(id=f"svc-{service.name}"))

        clients.services.create_service = AsyncMock(side_effect=create_service)
        clients.services.get_service = AsyncMock()
        clients.services.get_service.return_value.service.latest_deployment_id = "dep"
        clients.deployments.get_deployment = AsyncMock()
        clients.deployments.get_deployment.return_value.deployment.status = status
        clients.deployments.get_deployment.return_value.deployment.metadata = None
        clients.deployments.get_deployment.return_value.deployment.definition = None
        return clients, names

    @patch("koyeb.sandbox.sandbox.get_async_api_clients")
    def test_creates_sidecars_then_sandbox(self, mock_get_clients):
        clients, names = self._async_clients()
        mock_get_clients.return_value = clients

        async def go():
            with patch.object(AsyncSandbox, "wait_ready", AsyncMock(return_value=True)):
                return await AsyncSandbox.create(
                    name="sb", api_token="tok", sidecars=[_proxy()]
                )

        sb = asyncio.run(go())
        self.assertEqual(names, ["proxy", "sb"])
        self.assertEqual(sb.sidecar("proxy").service_id, "svc-proxy")

    @patch("koyeb.sandbox.sandbox.get_async_api_clients")
    def test_failed_sidecar_deletes_app(self, mock_get_clients):
        clients, names = self._async_clients(DeploymentStatus.ERROR)
        mock_get_clients.return_value = clients
        with self.assertRaises(SidecarError):
            asyncio.run(
                AsyncSandbox.create(name="sb", api_token="tok", sidecars=[_proxy()])
            )
        self.assertEqual(names, ["proxy"])
        clients.apps.delete_app.assert_awaited_once_with("app-id")

    @patch("koyeb.sandbox.sandbox.get_async_api_clients")
    def test_conflict_fails_before_any_api_call(self, mock_get_clients):
        with self.assertRaises(SidecarError):
            asyncio.run(
                AsyncSandbox.create(
                    name="sb", api_token="tok", sidecars=[_proxy()], block_network=True
                )
            )
        mock_get_clients.assert_not_called()


class TestCreateSidecarsReviewFixes(unittest.TestCase):
    """Partial failures, transient errors, timeouts and cancellation."""

    @patch("koyeb.sandbox.sandbox.time.sleep")
    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_transient_poll_error_is_retried(self, mock_get_clients, _sleep):
        from koyeb.api.exceptions import ApiException

        clients = _clients()
        original = clients.deployments.get_deployment.side_effect
        calls = {"n": 0}

        def flaky(id):
            calls["n"] += 1
            if calls["n"] == 1:
                raise ApiException(status=502, reason="bad gateway")
            return original(id)

        clients.deployments.get_deployment.side_effect = flaky
        mock_get_clients.return_value = clients
        with patch.object(Sandbox, "wait_ready", return_value=True):
            sb = Sandbox.create(name="sb", api_token="tok", sidecars=[_proxy()])
        self.assertEqual(sb.sidecar("proxy").service_id, "svc-1")
        clients.apps.delete_app.assert_not_called()

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_failed_cleanup_is_reported(self, mock_get_clients):
        clients = _clients([DeploymentStatus.ERROR])
        clients.apps.delete_app.side_effect = RuntimeError("503")
        mock_get_clients.return_value = clients
        with self.assertRaises(SidecarError) as ctx:
            Sandbox.create(name="sb", api_token="tok", sidecars=[_proxy()])
        msg = str(ctx.exception)
        self.assertIn("could not be deleted", msg)
        self.assertIn("app-id", msg)
        self.assertNotIn("app was deleted", msg)

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_second_sidecar_create_failure_deletes_app(self, mock_get_clients):
        from koyeb.api.exceptions import ApiException

        clients = _clients()
        names = []

        def create_service(service):
            names.append(service.name)
            if service.name == "db":
                raise ApiException(status=400, reason="bad")
            return MagicMock(service=MagicMock(id=f"svc-{service.name}"))

        clients.services.create_service.side_effect = create_service
        mock_get_clients.return_value = clients
        with self.assertRaises(SidecarError) as ctx:
            Sandbox.create(
                name="sb", api_token="tok", sidecars=[_proxy(), _proxy("db", (5432,))]
            )
        self.assertIn("'db'", str(ctx.exception))
        self.assertIn("app was deleted", str(ctx.exception))
        self.assertEqual(names, ["proxy", "db"])
        clients.apps.delete_app.assert_called_once_with("app-id")

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_sandbox_create_failure_after_sidecars_deletes_app(self, mock_get_clients):
        from koyeb.api.exceptions import ApiException
        from koyeb.sandbox import SandboxError

        clients = _clients()

        def create_service(service):
            if service.name == "sb":
                raise ApiException(status=400, reason="quota")
            return MagicMock(service=MagicMock(id=f"svc-{service.name}"))

        clients.services.create_service.side_effect = create_service
        mock_get_clients.return_value = clients
        with self.assertRaises(SandboxError) as ctx:
            Sandbox.create(name="sb", api_token="tok", sidecars=[_proxy()])
        self.assertIn("app was deleted", str(ctx.exception))
        clients.apps.delete_app.assert_called_once_with("app-id")

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_interrupt_while_waiting_deletes_app(self, mock_get_clients):
        clients = _clients()
        clients.deployments.get_deployment.side_effect = KeyboardInterrupt()
        mock_get_clients.return_value = clients
        with self.assertRaises(KeyboardInterrupt):
            Sandbox.create(name="sb", api_token="tok", sidecars=[_proxy()])
        clients.apps.delete_app.assert_called_once_with("app-id")

    @patch("koyeb.sandbox.sandbox.time.sleep")
    @patch("koyeb.sandbox.sandbox.time.time")
    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_timeout_is_a_sandbox_timeout_error(
        self, mock_get_clients, mock_time, _sleep
    ):
        from koyeb.sandbox import SandboxTimeoutError, SidecarTimeoutError

        mock_get_clients.return_value = _clients([DeploymentStatus.STARTING] * 10)
        mock_time.side_effect = [0, 0, 0, 100, 100, 100, 100]
        with self.assertRaises(SandboxTimeoutError) as ctx:
            Sandbox.create(name="sb", api_token="tok", sidecars=[_proxy()], timeout=50)
        self.assertIsInstance(ctx.exception, SidecarTimeoutError)
        self.assertIsInstance(ctx.exception, SidecarError)

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_one_deadline_covers_sidecars_and_sandbox(self, mock_get_clients):
        mock_get_clients.return_value = _clients()
        clock = {"t": 1000.0}

        def wait_sidecars(*args, **kwargs):
            clock["t"] += 40  # sidecars took 40s

        seen = {}

        def wait_ready(self, timeout):
            seen["timeout"] = timeout
            return True

        with (
            patch(
                "koyeb.sandbox.sandbox.time.monotonic", side_effect=lambda: clock["t"]
            ),
            patch("koyeb.sandbox.sandbox._wait_sidecars", side_effect=wait_sidecars),
            patch.object(Sandbox, "wait_ready", wait_ready),
        ):
            Sandbox.create(name="sb", api_token="tok", sidecars=[_proxy()], timeout=60)
        self.assertAlmostEqual(seen["timeout"], 20, delta=0.01)

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_without_sidecars_sandbox_gets_full_timeout(self, mock_get_clients):
        mock_get_clients.return_value = _clients()
        seen = {}

        def wait_ready(self, timeout):
            seen["timeout"] = timeout
            return True

        with patch.object(Sandbox, "wait_ready", wait_ready):
            Sandbox.create(name="sb", api_token="tok", timeout=60)
        self.assertEqual(seen["timeout"], 60)

    def test_mesh_scope_unspecified_allowed(self):
        with patch("koyeb.sandbox.sandbox.get_api_clients") as mock_get_clients:
            mock_get_clients.return_value = _clients()
            Sandbox.create(
                name="sb",
                api_token="tok",
                wait_ready=False,
                sidecars=[_proxy()],
                mesh_scope=MeshScope.MESH_SCOPE_UNSPECIFIED,
            )


class TestUpdateNetworkPolicyWithSidecars(unittest.TestCase):
    def _sb(self, cls=Sandbox):
        from koyeb.sandbox.sidecar import SidecarInfo

        sb = cls(
            sandbox_id="sb",
            app_id="app",
            service_id="sb-id",
            name="sb",
            api_token="tok",
            sandbox_secret="s",
        )
        sb._sidecars = [SidecarInfo("proxy", "svc-proxy", [8080])]
        return sb

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_egress_rejected(self, mock_get_clients):
        for kwargs in ({"block_network": True}, {"outbound_allowlist": ["1.2.3.4"]}):
            with self.subTest(**kwargs), self.assertRaises(SidecarError):
                self._sb().update_network_policy(**kwargs)
        mock_get_clients.assert_not_called()

    @patch("koyeb.sandbox.sandbox.get_async_api_clients")
    def test_async_egress_rejected(self, mock_get_clients):
        with self.assertRaises(SidecarError):
            asyncio.run(
                self._sb(AsyncSandbox).update_network_policy(block_network=True)
            )
        mock_get_clients.assert_not_called()


class TestSidecarInfo(unittest.TestCase):
    def test_ports_immutable_and_url_checks_port(self):
        from koyeb.sandbox.sidecar import SidecarInfo

        info = SidecarInfo("proxy", "svc", [8080, 9090])
        self.assertEqual(info.ports, (8080, 9090))
        self.assertEqual(info.url(9090), "http://proxy:9090")
        with self.assertRaises(SidecarError):
            info.url(8081)
        with self.assertRaises(AttributeError):
            info.ports.append(1)


class TestAsyncCreateSidecarsReviewFixes(unittest.TestCase):
    def _async_clients(self, status=DeploymentStatus.HEALTHY):
        clients = MagicMock()
        clients.apps.create_app = AsyncMock()
        clients.apps.create_app.return_value.app.id = "app-id"
        clients.apps.delete_app = AsyncMock()

        async def create_service(service):
            return MagicMock(service=MagicMock(id=f"svc-{service.name}"))

        clients.services.create_service = AsyncMock(side_effect=create_service)
        clients.services.get_service = AsyncMock()
        clients.services.get_service.return_value.service.latest_deployment_id = "dep"
        clients.deployments.get_deployment = AsyncMock()
        clients.deployments.get_deployment.return_value.deployment.status = status
        clients.deployments.get_deployment.return_value.deployment.metadata = None
        clients.deployments.get_deployment.return_value.deployment.definition = None
        return clients

    @patch("koyeb.sandbox.sandbox.get_async_api_clients")
    def test_cancel_while_waiting_deletes_app(self, mock_get_clients):
        clients = self._async_clients(DeploymentStatus.STARTING)
        mock_get_clients.return_value = clients

        async def go():
            with self.assertRaises(asyncio.TimeoutError):
                await asyncio.wait_for(
                    AsyncSandbox.create(
                        name="sb",
                        api_token="tok",
                        sidecars=[_proxy()],
                        poll_interval=0.05,
                    ),
                    timeout=0.3,
                )

        asyncio.run(go())
        clients.apps.delete_app.assert_awaited_once_with("app-id")

    @patch("koyeb.sandbox.sandbox.get_async_api_clients")
    def test_keep_app_without_cleanup(self, mock_get_clients):
        clients = self._async_clients(DeploymentStatus.ERROR)
        mock_get_clients.return_value = clients
        with self.assertRaises(SidecarError) as ctx:
            asyncio.run(
                AsyncSandbox.create(
                    name="sb",
                    api_token="tok",
                    sidecars=[_proxy()],
                    cleanup_on_failure=False,
                )
            )
        self.assertIn("kept for inspection", str(ctx.exception))
        clients.apps.delete_app.assert_not_awaited()

    @patch("koyeb.sandbox.sandbox.get_async_api_clients")
    def test_transient_poll_error_is_retried(self, mock_get_clients):
        clients = self._async_clients()
        ok = clients.deployments.get_deployment.return_value
        clients.deployments.get_deployment.side_effect = [RuntimeError("reset"), ok, ok]
        mock_get_clients.return_value = clients

        async def go():
            with patch.object(AsyncSandbox, "wait_ready", AsyncMock(return_value=True)):
                return await AsyncSandbox.create(
                    name="sb", api_token="tok", sidecars=[_proxy()], poll_interval=0.01
                )

        sb = asyncio.run(go())
        self.assertEqual(sb.sidecar("proxy").service_id, "svc-proxy")
        clients.apps.delete_app.assert_not_awaited()
