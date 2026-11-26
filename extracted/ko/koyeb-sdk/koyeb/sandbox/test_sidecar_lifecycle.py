"""Pins sidecar lifecycle: the KOYEB_SIDECARS env on the sandbox,
get_from_id finding sidecars again (exact names, never partial),
update_lifecycle keeping sidecars in step, and delete_after_inactivity
being rejected with sidecars."""

import asyncio
import json
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

from koyeb.api.models.deployment_definition import DeploymentDefinition
from koyeb.api.models.create_service import ServiceLifeCycle
from koyeb.api.models.deployment_env import DeploymentEnv
from koyeb.sandbox import AsyncSandbox, Sandbox, Sidecar, SidecarError
from koyeb.sandbox.sidecar import (
    SIDECARS_ENV,
    SidecarInfo,
    aligned_delete_after,
    parse_sidecars_env,
    sidecars_env_value,
)

T0 = datetime(2026, 11, 23, 12, 0, 0, tzinfo=timezone.utc)


def _proxy(name="proxy", ports=(8080,)):
    return Sidecar(name=name, image="mitmproxy/mitmproxy", ports=list(ports))


class TestSidecarsEnv(unittest.TestCase):
    def test_round_trip(self):
        value = sidecars_env_value([_proxy(), _proxy("db", (5432, 5433))])
        self.assertEqual(
            parse_sidecars_env(value),
            [
                {"name": "proxy", "ports": [8080]},
                {"name": "db", "ports": [5432, 5433]},
            ],
        )

    def test_unset(self):
        self.assertEqual(parse_sidecars_env(None), [])
        self.assertEqual(parse_sidecars_env(""), [])

    def test_damaged_values_raise(self):
        for value in (
            "nope",
            "[1]",
            '{"name":"a"}',
            '[{"name":"proxy"}]',
            '[{"name":"proxy","ports":[]}]',
            '[{"name":"proxy","ports":[1e309]}]',
            '[{"name":"proxy","ports":["80"]}]',
            '[{"name":"Bad","ports":[80]}]',
            '[{"name":"proxy","ports":[80]},{"name":"proxy","ports":[81]}]',
        ):
            with self.subTest(value=value), self.assertRaises(SidecarError):
                parse_sidecars_env(value)


class TestAlignedDeleteAfter(unittest.TestCase):
    def test_adds_the_creation_gap(self):
        self.assertEqual(aligned_delete_after(600, T0 + timedelta(seconds=90), T0), 690)

    def test_rounds_up(self):
        self.assertEqual(
            aligned_delete_after(600, T0 + timedelta(seconds=1.2), T0), 602
        )

    def test_zero_and_unknown(self):
        self.assertEqual(aligned_delete_after(0, T0, T0), 0)
        self.assertEqual(aligned_delete_after(600, None, T0), 600)
        self.assertEqual(aligned_delete_after(600, T0, None), 600)
        self.assertEqual(aligned_delete_after(600, T0, T0 + timedelta(seconds=5)), 600)


class TestCreateSetsSidecarsEnv(unittest.TestCase):
    def _create(self, mock_get_clients, **kwargs):
        clients = MagicMock()
        clients.apps.create_app.return_value.app.id = "app-id"
        mock_get_clients.return_value = clients
        Sandbox.create(name="sb", api_token="tok", wait_ready=False, **kwargs)
        return [
            c.kwargs["service"] for c in clients.services.create_service.call_args_list
        ]

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_sandbox_env_lists_sidecars(self, mock_get_clients):
        services = self._create(mock_get_clients, sidecars=[_proxy()], env={"A": "1"})
        env = {e.key: e.value for e in services[-1].definition.env}
        self.assertEqual(
            json.loads(env[SIDECARS_ENV]), [{"name": "proxy", "ports": [8080]}]
        )
        self.assertEqual(env["A"], "1")
        sidecar_env = {e.key for e in services[0].definition.env or []}
        self.assertNotIn(SIDECARS_ENV, sidecar_env)

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_reserved_env_rejected_even_without_sidecars(self, mock_get_clients):
        for sidecars in (None, [], [_proxy()]):
            with self.subTest(sidecars=sidecars), self.assertRaises(SidecarError):
                Sandbox.create(
                    name="sb",
                    api_token="tok",
                    sidecars=sidecars,
                    env={SIDECARS_ENV: "x"},
                )
        mock_get_clients.assert_not_called()

    @patch("koyeb.sandbox.sandbox.get_async_api_clients")
    def test_async_reserved_env_rejected(self, mock_get_clients):
        with self.assertRaises(SidecarError):
            asyncio.run(
                AsyncSandbox.create(name="sb", api_token="tok", env={SIDECARS_ENV: "x"})
            )
        mock_get_clients.assert_not_called()

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_inactivity_delay_rejected_with_sidecars(self, mock_get_clients):
        with self.assertRaises(SidecarError):
            Sandbox.create(
                name="sb",
                api_token="tok",
                sidecars=[_proxy()],
                delete_after_inactivity_delay=300,
            )
        mock_get_clients.assert_not_called()

    @patch("koyeb.sandbox.sandbox.get_async_api_clients")
    def test_async_inactivity_delay_rejected_with_sidecars(self, mock_get_clients):
        with self.assertRaises(SidecarError):
            asyncio.run(
                AsyncSandbox.create(
                    name="sb",
                    api_token="tok",
                    sidecars=[_proxy()],
                    delete_after_inactivity_delay=300,
                )
            )
        mock_get_clients.assert_not_called()


class _FakeApi:
    """Sync API fake: a sandbox service whose deployment carries ``env``,
    WEB services in its app, and list_services filtering names by
    *substring*, like the real API."""

    def __init__(self, env, web_services, life_cycles=None, created=None):
        self.env = env
        self.web = web_services  # name -> service id, in creation order
        self.life_cycles = dict(life_cycles or {})  # service id -> delete_after_create
        self.created = dict(created or {})  # service id -> datetime
        self.updates = []  # (service id, update_mask, delete_after_create)
        self.fail_update_for = set()
        self.fail_list = False
        self.lc_model = None
        self.clients = self._build()

    def use_async_models(self):
        """Async clients need api_async model instances."""
        from koyeb.api_async.models.create_service import (
            ServiceLifeCycle as AsyncServiceLifeCycle,
        )
        from koyeb.api_async.models.deployment_definition import (
            DeploymentDefinition as AsyncDeploymentDefinition,
        )

        self.lc_model = AsyncServiceLifeCycle
        dep = self.clients.deployments.get_deployment.return_value.deployment
        dep.definition = AsyncDeploymentDefinition.from_dict(dep.definition.to_dict())

    def _service(self, sid):
        svc = MagicMock()
        svc.id = sid
        svc.app_id = "app-id"
        svc.name = (
            "sb" if sid == "sb-id" else next(n for n, i in self.web.items() if i == sid)
        )
        svc.active_deployment_id = svc.latest_deployment_id = f"dep-{sid}"
        svc.created_at = self.created.get(sid, T0)
        svc.life_cycle = (self.lc_model or ServiceLifeCycle)(
            delete_after_create=self.life_cycles.get(sid)
        )
        return svc

    def _build(self):
        clients = MagicMock()
        clients.services.get_service.side_effect = lambda id=None, **kw: MagicMock(
            service=self._service(id)
        )
        dep = clients.deployments.get_deployment.return_value.deployment
        dep.id, dep.status, dep.metadata = "dep-sb-id", "HEALTHY", None
        dep.definition = DeploymentDefinition(
            name="sb",
            env=[DeploymentEnv(key=k, value=v) for k, v in self.env.items()],
        )

        def list_services(**kw):
            if self.fail_list:
                raise RuntimeError("503")
            needle = kw.get("name") or ""
            matches = [(n, i) for n, i in self.web.items() if needle in n]
            offset, limit = int(kw.get("offset", 0)), int(kw.get("limit", 100))
            page = matches[offset : offset + limit]
            reply = MagicMock()
            reply.services = []
            for n, i in page:
                s = MagicMock()
                s.id, s.app_id, s.name = i, "app-id", n
                s.active_deployment_id = s.latest_deployment_id = f"dep-{i}"
                reply.services.append(s)
            reply.count = len(matches)
            return reply

        clients.services.list_services.side_effect = list_services

        def update_service(id=None, service=None, update_mask=None, **kw):
            if id in self.fail_update_for:
                raise RuntimeError("boom")
            dac = service.life_cycle.delete_after_create if service.life_cycle else None
            self.updates.append((id, update_mask, dac))
            reply = MagicMock()
            reply.service.latest_deployment_id = f"dep-{id}-2"
            return reply

        clients.services.update_service.side_effect = update_service
        return clients


def _env(*sidecars):
    return {"SANDBOX_SECRET": "s", SIDECARS_ENV: sidecars_env_value(list(sidecars))}


class TestGetFromIdFindsSidecars(unittest.TestCase):
    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_exact_names_despite_substring_matches(self, mock_get_clients):
        # Older services whose names contain the sidecar names come first.
        api = _FakeApi(
            _env(_proxy("db", (5432,)), _proxy()),
            {
                "redis-db": "svc-redis",
                "proxy-admin": "svc-admin",
                "db": "svc-db",
                "proxy": "svc-proxy",
            },
        )
        mock_get_clients.return_value = api.clients
        sb = Sandbox.get_from_id("sb-id", api_token="tok")
        self.assertEqual(
            sb.sidecars,
            [
                SidecarInfo("db", "svc-db", [5432]),
                SidecarInfo("proxy", "svc-proxy", [8080]),
            ],
        )
        for call in api.clients.services.list_services.call_args_list:
            self.assertEqual(call.kwargs["app_id"], "app-id")
            self.assertEqual(call.kwargs["types"], ["WEB"])
            self.assertIsNone(call.kwargs.get("name"))

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_no_lookup_without_sidecars(self, mock_get_clients):
        api = _FakeApi({"SANDBOX_SECRET": "s"}, {})
        mock_get_clients.return_value = api.clients
        sb = Sandbox.get_from_id("sb-id", api_token="tok")
        self.assertEqual(sb.sidecars, [])
        api.clients.services.list_services.assert_not_called()

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_missing_sidecar_raises(self, mock_get_clients):
        api = _FakeApi(_env(_proxy()), {"proxy-admin": "svc-admin"})
        mock_get_clients.return_value = api.clients
        with self.assertRaises(SidecarError):
            Sandbox.get_from_id("sb-id", api_token="tok")

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_lookup_failure_raises(self, mock_get_clients):
        api = _FakeApi(_env(_proxy()), {"proxy": "svc-proxy"})
        api.fail_list = True
        mock_get_clients.return_value = api.clients
        with self.assertRaises(SidecarError):
            Sandbox.get_from_id("sb-id", api_token="tok")

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_damaged_env_raises(self, mock_get_clients):
        api = _FakeApi({"SANDBOX_SECRET": "s", SIDECARS_ENV: "[{}]"}, {})
        mock_get_clients.return_value = api.clients
        with self.assertRaises(SidecarError):
            Sandbox.get_from_id("sb-id", api_token="tok")

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_paginates(self, mock_get_clients):
        web = {f"svc{i:03d}": f"id-{i}" for i in range(150)}
        web["proxy"] = "svc-proxy"
        api = _FakeApi(_env(_proxy()), web)
        mock_get_clients.return_value = api.clients
        sb = Sandbox.get_from_id("sb-id", api_token="tok")
        self.assertEqual(sb.sidecar("proxy").service_id, "svc-proxy")
        self.assertEqual(api.clients.services.list_services.call_count, 2)

    @patch("koyeb.sandbox.sandbox.get_async_api_clients")
    def test_async_exact_names(self, mock_get_clients):
        api = _FakeApi(
            _env(_proxy()), {"proxy-admin": "svc-admin", "proxy": "svc-proxy"}
        )
        api.use_async_models()
        sync = api.clients
        clients = MagicMock()
        clients.services.get_service = AsyncMock(
            side_effect=sync.services.get_service.side_effect
        )
        clients.deployments.get_deployment = AsyncMock(
            return_value=sync.deployments.get_deployment.return_value
        )
        clients.services.list_services = AsyncMock(
            side_effect=sync.services.list_services.side_effect
        )
        clients.apps.get_app = AsyncMock()
        mock_get_clients.return_value = clients
        sb = asyncio.run(AsyncSandbox.get_from_id("sb-id", api_token="tok"))
        self.assertEqual(sb.sidecars, [SidecarInfo("proxy", "svc-proxy", [8080])])


def _handle(cls=Sandbox, sidecars=None):
    sb = cls(
        sandbox_id="sb",
        app_id="app-id",
        service_id="sb-id",
        name="sb",
        api_token="tok",
        sandbox_secret="s",
    )
    sb._sidecars = sidecars or []
    return sb


class TestUpdateLifecycleWithSidecars(unittest.TestCase):
    def _api(self, **kw):
        return _FakeApi(
            _env(_proxy(), _proxy("db", (5432,))),
            {"proxy": "svc-proxy", "db": "svc-db"},
            **kw,
        )

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_sidecars_first_then_sandbox_aligned_and_masked(self, mock_get_clients):
        api = self._api(
            created={
                "svc-proxy": T0,
                "svc-db": T0 + timedelta(seconds=10),
                "sb-id": T0 + timedelta(seconds=90),
            }
        )
        mock_get_clients.return_value = api.clients
        _handle().update_lifecycle(delete_after_delay=900)
        self.assertEqual(
            api.updates,
            [
                ("svc-proxy", "life_cycle.delete_after_create", 990),
                ("svc-db", "life_cycle.delete_after_create", 980),
                ("sb-id", None, 900),
            ],
        )

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_list_handle_without_cached_sidecars_still_updates_them(
        self, mock_get_clients
    ):
        api = self._api()
        mock_get_clients.return_value = api.clients
        sb = _handle()  # like a Sandbox.list() handle: nothing cached
        sb.update_lifecycle(delete_after_delay=900)
        self.assertEqual([u[0] for u in api.updates], ["svc-proxy", "svc-db", "sb-id"])
        self.assertEqual([i.name for i in sb.sidecars], ["proxy", "db"])

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_list_handle_rejects_inactivity(self, mock_get_clients):
        api = self._api()
        mock_get_clients.return_value = api.clients
        with self.assertRaises(SidecarError):
            _handle().update_lifecycle(delete_after_inactivity=300)
        self.assertEqual(api.updates, [])

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_skips_sidecars_already_set(self, mock_get_clients):
        api = self._api(life_cycles={"svc-proxy": 900})
        mock_get_clients.return_value = api.clients
        _handle().update_lifecycle(delete_after_delay=900)
        self.assertEqual([u[0] for u in api.updates], ["svc-db", "sb-id"])

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_sidecar_failure_leaves_sandbox_unchanged(self, mock_get_clients):
        api = self._api()
        api.fail_update_for = {"svc-proxy"}
        mock_get_clients.return_value = api.clients
        with self.assertRaises(SidecarError) as ctx:
            _handle().update_lifecycle(delete_after_delay=900)
        self.assertIn("'proxy'", str(ctx.exception))
        self.assertIn("Nothing was changed on the sandbox", str(ctx.exception))
        self.assertEqual([u[0] for u in api.updates], ["svc-db"])

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_inactivity_rejected_with_cached_sidecars(self, mock_get_clients):
        with self.assertRaises(SidecarError):
            _handle(
                sidecars=[SidecarInfo("proxy", "svc-proxy", [8080])]
            ).update_lifecycle(delete_after_inactivity=300)
        mock_get_clients.assert_not_called()

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_inactivity_zero_allowed(self, mock_get_clients):
        api = self._api()
        mock_get_clients.return_value = api.clients
        _handle().update_lifecycle(delete_after_inactivity=0)
        self.assertEqual([u[0] for u in api.updates], ["sb-id"])

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_without_sidecars_unchanged(self, mock_get_clients):
        api = _FakeApi({"SANDBOX_SECRET": "s"}, {})
        mock_get_clients.return_value = api.clients
        _handle().update_lifecycle(delete_after_delay=900, delete_after_inactivity=300)
        self.assertEqual(api.updates, [("sb-id", None, 900)])
        api.clients.services.list_services.assert_not_called()

    @patch("koyeb.sandbox.clients.get_async_api_clients")
    def test_async_sidecars_first_and_aligned(self, mock_get_clients):
        api = self._api(created={"sb-id": T0 + timedelta(seconds=30)})
        api.use_async_models()
        sync = api.clients
        clients = MagicMock()
        clients.services.get_service = AsyncMock(
            side_effect=sync.services.get_service.side_effect
        )
        clients.deployments.get_deployment = AsyncMock(
            return_value=sync.deployments.get_deployment.return_value
        )
        clients.services.list_services = AsyncMock(
            side_effect=sync.services.list_services.side_effect
        )
        clients.services.update_service = AsyncMock(
            side_effect=sync.services.update_service.side_effect
        )
        mock_get_clients.return_value = clients
        asyncio.run(_handle(AsyncSandbox).update_lifecycle(delete_after_delay=900))
        self.assertEqual(
            api.updates,
            [
                ("svc-proxy", "life_cycle.delete_after_create", 930),
                ("svc-db", "life_cycle.delete_after_create", 930),
                ("sb-id", None, 900),
            ],
        )

    @patch("koyeb.sandbox.clients.get_async_api_clients")
    def test_async_inactivity_rejected_on_list_handle(self, mock_get_clients):
        api = self._api()
        api.use_async_models()
        sync = api.clients
        clients = MagicMock()
        clients.services.get_service = AsyncMock(
            side_effect=sync.services.get_service.side_effect
        )
        clients.deployments.get_deployment = AsyncMock(
            return_value=sync.deployments.get_deployment.return_value
        )
        clients.services.list_services = AsyncMock(
            side_effect=sync.services.list_services.side_effect
        )
        clients.services.update_service = AsyncMock()
        mock_get_clients.return_value = clients
        with self.assertRaises(SidecarError):
            asyncio.run(
                _handle(AsyncSandbox).update_lifecycle(delete_after_inactivity=300)
            )
        clients.services.update_service.assert_not_awaited()


class TestCreateAlignsSidecarExpiry(unittest.TestCase):
    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_create_extends_sidecar_delay_to_the_sandbox(self, mock_get_clients):
        api = _FakeApi(
            {},
            {"proxy": "svc-1"},
            life_cycles={"svc-1": 600},
            created={"svc-1": T0, "svc-2": T0 + timedelta(seconds=45)},
        )
        clients = api.clients
        clients.apps.create_app.return_value.app.id = "app-id"
        ids = iter(["svc-1", "svc-2"])
        clients.services.create_service.side_effect = lambda service: MagicMock(
            service=MagicMock(id=next(ids))
        )
        real_service = api._service

        def service(sid):
            svc = real_service("sb-id" if sid == "svc-2" else sid)
            svc.id = sid
            svc.created_at = api.created.get(sid, T0)
            return svc

        api._service = service
        mock_get_clients.return_value = clients
        Sandbox.create(
            name="sb",
            api_token="tok",
            wait_ready=False,
            delete_after_delay=600,
            sidecars=[_proxy()],
        )
        self.assertEqual(
            api.updates, [("svc-1", "life_cycle.delete_after_create", 645)]
        )

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_alignment_failure_does_not_fail_create(self, mock_get_clients):
        api = _FakeApi({}, {"proxy": "svc-1"})
        clients = api.clients
        clients.apps.create_app.return_value.app.id = "app-id"
        ids = iter(["svc-1", "svc-2"])
        clients.services.create_service.side_effect = lambda service: MagicMock(
            service=MagicMock(id=next(ids))
        )
        clients.services.get_service.side_effect = RuntimeError("503")
        mock_get_clients.return_value = clients
        sb = Sandbox.create(
            name="sb",
            api_token="tok",
            wait_ready=False,
            delete_after_delay=600,
            sidecars=[_proxy()],
        )
        self.assertEqual(sb.sidecar("proxy").service_id, "svc-1")
        clients.apps.delete_app.assert_not_called()

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_no_alignment_without_delay(self, mock_get_clients):
        api = _FakeApi({}, {"proxy": "svc-1"})
        clients = api.clients
        clients.apps.create_app.return_value.app.id = "app-id"
        ids = iter(["svc-1", "svc-2"])
        clients.services.create_service.side_effect = lambda service: MagicMock(
            service=MagicMock(id=next(ids))
        )
        mock_get_clients.return_value = clients
        Sandbox.create(
            name="sb", api_token="tok", wait_ready=False, sidecars=[_proxy()]
        )
        self.assertEqual(api.updates, [])


class TestUpdateNetworkPolicyOnListHandles(unittest.TestCase):
    """A handle that doesn't know its sidecars (list()) must still refuse
    egress settings that would cut the sandbox off from them."""

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_rejected_from_live_deployment(self, mock_get_clients):
        api = _FakeApi(_env(_proxy()), {"proxy": "svc-proxy"})
        mock_get_clients.return_value = api.clients
        for kwargs in ({"block_network": True}, {"outbound_allowlist": ["1.2.3.4"]}):
            with self.subTest(**kwargs), self.assertRaises(SidecarError):
                _handle().update_network_policy(**kwargs)
        api.clients.services.update_service.assert_not_called()

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_reset_to_default_still_allowed(self, mock_get_clients):
        api = _FakeApi(_env(_proxy()), {"proxy": "svc-proxy"})
        mock_get_clients.return_value = api.clients
        _handle().update_network_policy()
        api.clients.services.update_service.assert_called_once()

    @patch("koyeb.sandbox.sandbox.get_api_clients")
    def test_without_sidecars_unchanged(self, mock_get_clients):
        api = _FakeApi({"SANDBOX_SECRET": "s"}, {})
        mock_get_clients.return_value = api.clients
        _handle().update_network_policy(block_network=True)
        api.clients.services.update_service.assert_called_once()

    @patch("koyeb.sandbox.sandbox.get_async_api_clients")
    def test_async_rejected_from_live_deployment(self, mock_get_clients):
        api = _FakeApi(_env(_proxy()), {"proxy": "svc-proxy"})
        api.use_async_models()
        sync = api.clients
        clients = MagicMock()
        clients.services.get_service = AsyncMock(
            side_effect=sync.services.get_service.side_effect
        )
        clients.deployments.get_deployment = AsyncMock(
            return_value=sync.deployments.get_deployment.return_value
        )
        clients.services.update_service = AsyncMock()
        mock_get_clients.return_value = clients
        with self.assertRaises(SidecarError):
            asyncio.run(_handle(AsyncSandbox).update_network_policy(block_network=True))
        clients.services.update_service.assert_not_awaited()
