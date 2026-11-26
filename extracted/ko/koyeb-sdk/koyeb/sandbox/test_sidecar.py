"""Pins the Sidecar model: validation before any API call, and the service
definition each sidecar is created with."""

import unittest

from koyeb.api.models.deployment_definition_type import DeploymentDefinitionType
from koyeb.api.models.deployment_mesh import DeploymentMesh
from koyeb.api.models.egress_policy_mode import EgressPolicyMode
from koyeb.api.models.mesh_scope import MeshScope
from koyeb.api.models.secret import Secret
from koyeb.sandbox import Sidecar, SidecarError
from koyeb.sandbox.errors import SandboxError
from koyeb.sandbox.sidecar import validate_sidecars


def _sidecar(**kwargs):
    kwargs.setdefault("name", "proxy")
    kwargs.setdefault("image", "mitmproxy/mitmproxy")
    kwargs.setdefault("ports", [8080])
    return Sidecar(**kwargs)


class TestSidecarValidation(unittest.TestCase):
    def test_valid(self):
        s = _sidecar(ports=[8080, 9000])
        self.assertEqual(s.ports, [8080, 9000])
        self.assertEqual(s.instance_type, "nano")

    def test_error_is_a_sandbox_error_and_value_error(self):
        with self.assertRaises(SandboxError):
            _sidecar(name="Bad")
        with self.assertRaises(ValueError):
            _sidecar(name="Bad")

    def test_invalid_names(self):
        for name in [
            "",
            "a",
            "Proxy",
            "-proxy",
            "proxy-",
            "my_proxy",
            "a.b",
            "x" * 64,
            None,
            3,
        ]:
            with self.subTest(name=name), self.assertRaises(SidecarError):
                _sidecar(name=name)

    def test_valid_names(self):
        for name in ["db", "proxy-1", "x" * 63, "1a"]:
            with self.subTest(name=name):
                self.assertEqual(_sidecar(name=name).name, name)

    def test_image_required(self):
        with self.assertRaises(SidecarError):
            _sidecar(image="")

    def test_invalid_ports(self):
        for ports in [
            [],
            [0],
            [65000],
            [8080] * 2,
            [1, 2, 3, 4, 5, 6],
            ["80"],
            [True],
            "8080",
            None,
            8080,
        ]:
            with self.subTest(ports=ports), self.assertRaises(SidecarError):
                _sidecar(ports=ports)

    def test_tuple_ports_accepted(self):
        self.assertEqual(_sidecar(ports=(80, 443)).ports, [80, 443])

    def test_conflicting_egress(self):
        with self.assertRaises(SidecarError):
            _sidecar(block_network=True, outbound_allowlist=["1.2.3.4"])

    def test_invalid_allowlist(self):
        with self.assertRaises(SidecarError):
            _sidecar(outbound_allowlist=["not-an-ip"])


class TestValidateSidecars(unittest.TestCase):
    def test_unique_names(self):
        with self.assertRaises(SidecarError):
            validate_sidecars([_sidecar(), _sidecar()], "sb")

    def test_name_differs_from_sandbox(self):
        with self.assertRaises(SidecarError):
            validate_sidecars([_sidecar(name="sb")], "sb")

    def test_rejects_non_sidecar(self):
        with self.assertRaises(SidecarError):
            validate_sidecars([{"name": "proxy"}], "sb")

    def test_returns_list(self):
        sidecars = (_sidecar(name="a1"), _sidecar(name="b1"))
        self.assertEqual(validate_sidecars(sidecars, "sb"), list(sidecars))


class TestSidecarServiceDefinition(unittest.TestCase):
    def _definition(self, **kwargs):
        return _sidecar(**kwargs).service_spec(region="fra").deployment_definition()

    def test_web_service_without_routes(self):
        d = self._definition()
        self.assertEqual(d.type, DeploymentDefinitionType.WEB)
        self.assertEqual(d.routes, [])
        self.assertEqual([(p.port, p.protocol) for p in d.ports], [(8080, "tcp")])

    def test_health_check_on_first_port(self):
        d = self._definition(ports=[9000, 8080])
        self.assertEqual(len(d.health_checks), 1)
        self.assertEqual(d.health_checks[0].tcp.port, 9000)

    def test_mesh_enabled_with_app_scope(self):
        d = self._definition()
        self.assertEqual(d.mesh, DeploymentMesh.DEPLOYMENT_MESH_ENABLED)
        self.assertEqual(d.network_policy.mesh.scope, MeshScope.MESH_SCOPE_APP)
        self.assertIsNone(d.network_policy.egress)

    def test_always_on(self):
        scaling = self._definition().scalings[0]
        self.assertEqual((scaling.min, scaling.max), (1, 1))
        self.assertIsNone(scaling.targets)

    def test_no_sandbox_secret_or_sandbox_ports(self):
        d = self._definition()
        self.assertNotIn("SANDBOX_SECRET", [e.key for e in d.env or []])
        self.assertNotIn(3030, [p.port for p in d.ports])
        self.assertFalse(d.proxy_ports)

    def test_secret_env_is_a_reference(self):
        d = self._definition(env={"API_KEY": Secret(name="my-key"), "MODE": "x"})
        env = {e.key: e.value for e in d.env}
        self.assertEqual(env, {"API_KEY": "{{ secret.my-key }}", "MODE": "x"})

    def test_egress_allowlist_kept_with_mesh(self):
        d = self._definition(outbound_allowlist=["1.2.3.4"])
        self.assertEqual(
            d.network_policy.egress.mode, EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL
        )
        self.assertEqual(d.network_policy.mesh.scope, MeshScope.MESH_SCOPE_APP)

    def test_docker_overrides_and_files(self):
        d = self._definition(
            command="mitmdump",
            args=["--listen-port", "8080"],
            entrypoint=["/bin/sh", "-c"],
            registry_secret="reg",
            config_files={"/etc/x.py": "print(1)"},
            instance_type="small",
        )
        self.assertEqual(d.docker.command, "mitmdump")
        self.assertEqual(d.docker.args, ["--listen-port", "8080"])
        self.assertEqual(d.docker.entrypoint, ["/bin/sh", "-c"])
        self.assertEqual(d.docker.image_registry_secret, "reg")
        self.assertFalse(d.docker.privileged)
        self.assertEqual([f.path for f in d.config_files], ["/etc/x.py"])
        self.assertEqual(d.instance_types[0].type, "small")
        self.assertEqual(d.regions, ["fra"])

    def test_lifecycle_follows_the_sandbox(self):
        # Sidecars never sleep, so only delete_after_create applies.
        spec = _sidecar().service_spec(delete_after_delay=600)
        self.assertEqual(
            spec.service_life_cycle(),
            {"delete_after_create": 600, "delete_after_sleep": 0},
        )

    def test_payload_coerces_into_both_model_flavors(self):
        from koyeb.api.models.create_service import CreateService
        from koyeb.api_async.models.create_service import (
            CreateService as AsyncCreateService,
        )

        payload = _sidecar().service_spec().create_service_payload("app-id")
        self.assertEqual(payload["name"], "proxy")
        for model in (CreateService, AsyncCreateService):
            service = model(**payload)
            self.assertEqual(service.definition.health_checks[0].tcp.port, 8080)


class TestSidecarValidationFromReview(unittest.TestCase):
    def test_names_the_api_rejects(self):
        for name in ["a--b", "ab\n", "a.b", "proxy--1"]:
            with self.subTest(name=name), self.assertRaises(SidecarError):
                _sidecar(name=name)

    def test_overlapping_allowlist_rejected(self):
        with self.assertRaises(SidecarError):
            _sidecar(outbound_allowlist=["10.0.0.0/8", "10.1.0.0/16"])
        with self.assertRaises(SidecarError):
            _sidecar(outbound_allowlist=["1.2.3.4", "1.2.3.4/32"])

    def test_disjoint_allowlist_accepted(self):
        _sidecar(outbound_allowlist=["10.0.0.0/8", "192.168.0.0/16", "2001:db8::/32"])


class TestSidecarVpnOptions(unittest.TestCase):
    """privileged and startup_grace_period, for VPN sidecars."""

    def test_privileged(self):
        self.assertFalse(
            _sidecar().service_spec().deployment_definition().docker.privileged
        )
        d = _sidecar(privileged=True).service_spec().deployment_definition()
        self.assertTrue(d.docker.privileged)

    def test_grace_period(self):
        hc = _sidecar().service_spec().deployment_definition().health_checks[0]
        self.assertIsNone(hc.grace_period)
        hc = (
            _sidecar(startup_grace_period=300)
            .service_spec()
            .deployment_definition()
            .health_checks[0]
        )
        self.assertEqual(hc.grace_period, 300)

    def test_invalid_grace_period(self):
        for value in (4, 901, "60", True, 1.5):
            with self.subTest(value=value), self.assertRaises(SidecarError):
                _sidecar(startup_grace_period=value)
