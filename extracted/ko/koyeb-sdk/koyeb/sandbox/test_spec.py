"""Pins the SandboxSpec create vocabulary: one definition of a sandbox,
consumed by every create flow (sync and async, Sandbox and ServicePool)."""

import unittest
from unittest import mock

from koyeb.api.models.deployment_definition_type import DeploymentDefinitionType
from koyeb.api.models.deployment_mesh import DeploymentMesh
from koyeb.api.models.egress_policy_mode import EgressPolicyMode
from koyeb.api.models.mesh_scope import MeshScope

from koyeb.sandbox.snapshot import SnapshotType
from koyeb.sandbox.spec import (
    SandboxSpec,
    create_deployment_definition,
    create_docker_source,
)
from koyeb.sandbox.errors import EgressPolicyError


def _spec(**kwargs):
    kwargs.setdefault("name", "quick-sandbox")
    return SandboxSpec(**kwargs)


class TestSandboxSpecSecret(unittest.TestCase):
    """The SANDBOX_SECRET injection belongs to the spec, not to each flow."""

    def test_given_secret_flows_into_definition_env(self):
        spec = _spec(env={"MY_VAR": "x"})
        secret = spec.apply_sandbox_secret("given-secret")
        self.assertEqual(secret, "given-secret")
        env = {e.key: e.value for e in spec.deployment_definition().env}
        self.assertEqual(env["SANDBOX_SECRET"], "given-secret")
        self.assertEqual(env["MY_VAR"], "x")

    def test_missing_secret_is_generated(self):
        spec = _spec()
        secret = spec.apply_sandbox_secret()
        self.assertTrue(secret)
        env = {e.key: e.value for e in spec.deployment_definition().env}
        self.assertEqual(env["SANDBOX_SECRET"], secret)

    def test_caller_env_dict_is_not_mutated(self):
        env = {"MY_VAR": "x"}
        _spec(env=env).apply_sandbox_secret("s")
        self.assertEqual(env, {"MY_VAR": "x"})


class TestSandboxSpecPayloads(unittest.TestCase):
    """Payload dicts are the wire truth; both model flavors coerce them."""

    def test_definition_defaults(self):
        definition = _spec().deployment_definition()
        self.assertEqual(definition.type, DeploymentDefinitionType.SANDBOX)
        self.assertEqual(definition.mesh, DeploymentMesh.DEPLOYMENT_MESH_AUTO)
        scaling = definition.scalings[0]
        self.assertEqual(scaling.min, 0)
        self.assertEqual(scaling.targets[0].sleep_idle_delay.deep_sleep_value, 300)

    def test_create_service_payload_coerces_into_both_model_flavors(self):
        from koyeb.api.models.create_service import CreateService
        from koyeb.api_async.models.create_service import (
            CreateService as AsyncCreateService,
        )

        payload = _spec(env={"A": "b"}).create_service_payload("app-1")
        service = CreateService(**payload)
        async_service = AsyncCreateService(**payload)
        self.assertEqual(service.app_id, "app-1")
        self.assertEqual(async_service.app_id, "app-1")
        self.assertEqual(service.definition.mesh, DeploymentMesh.DEPLOYMENT_MESH_AUTO)
        self.assertEqual(
            async_service.definition.mesh, DeploymentMesh.DEPLOYMENT_MESH_AUTO
        )

    def test_app_payload_coerces_into_both_model_flavors(self):
        from koyeb.api.models.create_app import CreateApp
        from koyeb.api_async.models.create_app import CreateApp as AsyncCreateApp

        payload = _spec().app_payload()
        self.assertTrue(payload["name"].startswith("sandbox-app-quick-sandbox-"))
        app = CreateApp(**payload)
        async_app = AsyncCreateApp(**payload)
        self.assertTrue(app.life_cycle.delete_when_empty)
        self.assertTrue(async_app.life_cycle.delete_when_empty)

    def test_app_name_differs_for_same_name_creates_in_the_same_second(self):
        # the longest name that fit with the 10-digit seconds suffix
        spec = _spec(name="n" * 41)

        with mock.patch("koyeb.sandbox.spec.time.time", return_value=1_794_916_800.0):
            names = {spec.app_payload()["name"] for _ in range(20)}

        self.assertEqual(len(names), 20)
        for name in names:
            self.assertLessEqual(len(name), 64)
            self.assertRegex(name, r"^[a-z0-9]+([.-][a-z0-9]+)*$")

    def test_full_snapshot_omits_definition(self):
        payload = _spec(
            snapshot_id="snap-1", snapshot_type=SnapshotType.FULL
        ).create_service_payload("app-1")
        self.assertNotIn("definition", payload)
        self.assertEqual(payload["instance_snapshot_id"], "snap-1")

    def test_filesystem_snapshot_pins_definition(self):
        payload = _spec(
            snapshot_id="snap-1", snapshot_type=SnapshotType.FILESYSTEM
        ).create_service_payload("app-1")
        self.assertIn("definition", payload)
        self.assertEqual(payload["instance_snapshot_id"], "snap-1")

    def test_service_life_cycle(self):
        spec = _spec(delete_after_delay=10, delete_after_inactivity_delay=20)
        self.assertEqual(
            spec.service_life_cycle(),
            {"delete_after_create": 10, "delete_after_sleep": 20},
        )


class TestSandboxSpecFailsFast(unittest.TestCase):
    """Invalid input must die at spec construction, before any API call."""

    def test_invalid_egress_rejected_at_construction(self):
        with self.assertRaises(EgressPolicyError):
            _spec(block_network=True, outbound_allowlist=["10.0.0.0/8"])

    def test_invalid_protocol_rejected_at_construction(self):
        with self.assertRaises(ValueError):
            _spec(exposed_port_protocol="ftp")


class TestCreateDockerSource(unittest.TestCase):
    """Tests for create_docker_source entrypoint, command, and args support."""

    def test_default_no_entrypoint_no_command(self):
        ds = create_docker_source("myimage")
        self.assertIsNone(ds.command)
        self.assertIsNone(ds.args)
        self.assertIsNone(ds.entrypoint)

    def test_command_and_args(self):
        ds = create_docker_source("myimage", command="python", args=["-u", "app.py"])
        self.assertEqual(ds.command, "python")
        self.assertEqual(ds.args, ["-u", "app.py"])
        self.assertIsNone(ds.entrypoint)

    def test_command_only(self):
        ds = create_docker_source("myimage", command="python app.py")
        self.assertEqual(ds.command, "python app.py")
        self.assertIsNone(ds.args)
        self.assertIsNone(ds.entrypoint)

    def test_entrypoint_only(self):
        ds = create_docker_source("myimage", entrypoint=["/bin/sh", "-c"])
        self.assertIsNone(ds.command)
        self.assertIsNone(ds.args)
        self.assertEqual(ds.entrypoint, ["/bin/sh", "-c"])

    def test_entrypoint_and_command(self):
        ds = create_docker_source(
            "myimage", entrypoint=["/bin/sh", "-c"], command="python app.py"
        )
        self.assertEqual(ds.command, "python app.py")
        self.assertEqual(ds.entrypoint, ["/bin/sh", "-c"])
        self.assertIsNone(ds.args)

    def test_entrypoint_command_and_args(self):
        ds = create_docker_source(
            "myimage", entrypoint=["/bin/sh", "-c"], command="python", args=["app.py"]
        )
        self.assertEqual(ds.command, "python")
        self.assertEqual(ds.entrypoint, ["/bin/sh", "-c"])
        self.assertEqual(ds.args, ["app.py"])

    def test_privileged_and_registry_secret_still_work(self):
        ds = create_docker_source(
            "myimage",
            privileged=True,
            image_registry_secret="my-secret",
            entrypoint=["/entrypoint.sh"],
            command="serve",
        )
        self.assertTrue(ds.privileged)
        self.assertEqual(ds.image_registry_secret, "my-secret")


class TestDeploymentDefinitionMapping(unittest.TestCase):
    """Pins the enable_mesh and idle_timeout semantics the sync/async
    default alignment depends on."""

    def _definition(self, **kwargs):
        return create_deployment_definition(
            name="svc",
            docker_source=create_docker_source("koyeb/sandbox"),
            env_vars=[],
            instance_type="micro",
            **kwargs,
        )

    def test_enable_mesh_tri_state(self):
        self.assertEqual(
            self._definition(enable_mesh=None).mesh, DeploymentMesh.DEPLOYMENT_MESH_AUTO
        )
        self.assertEqual(
            self._definition(enable_mesh=True).mesh,
            DeploymentMesh.DEPLOYMENT_MESH_ENABLED,
        )
        self.assertEqual(
            self._definition(enable_mesh=False).mesh,
            DeploymentMesh.DEPLOYMENT_MESH_DISABLED,
        )

    def test_default_idle_timeout_scales_to_zero(self):
        scaling = self._definition().scalings[0]
        self.assertEqual(scaling.min, 0)
        self.assertEqual(scaling.targets[0].sleep_idle_delay.deep_sleep_value, 300)

    def test_idle_timeout_zero_is_always_on(self):
        scaling = self._definition(idle_timeout=0).scalings[0]
        self.assertEqual(scaling.min, 1)
        self.assertIsNone(scaling.targets)

    def test_light_sleep_mode(self):
        delay = (
            self._definition(idle_timeout=120, _experimental_enable_light_sleep=True)
            .scalings[0]
            .targets[0]
            .sleep_idle_delay
        )
        self.assertEqual(delay.light_sleep_value, 120)
        self.assertEqual(delay.deep_sleep_value, 3900)

    def test_custom_idle_timeout_deep_sleep_only(self):
        delay = (
            self._definition(idle_timeout=90).scalings[0].targets[0].sleep_idle_delay
        )
        self.assertEqual(delay.deep_sleep_value, 90)
        self.assertIsNone(delay.light_sleep_value)

    def test_light_sleep_deep_sleep_override(self):
        delay = (
            self._definition(
                idle_timeout=90,
                _experimental_enable_light_sleep=True,
                _experimental_deep_sleep_value=600,
            )
            .scalings[0]
            .targets[0]
            .sleep_idle_delay
        )
        self.assertEqual(delay.light_sleep_value, 90)
        self.assertEqual(delay.deep_sleep_value, 600)


if __name__ == "__main__":
    unittest.main()


class TestSandboxSpecMeshScope(unittest.TestCase):
    """mesh_scope lands in network_policy.mesh, next to egress."""

    def test_default_sends_no_mesh(self):
        self.assertIsNone(_spec().deployment_definition().network_policy)

    def test_app_scope(self):
        policy = (
            _spec(mesh_scope=MeshScope.MESH_SCOPE_APP)
            .deployment_definition()
            .network_policy
        )
        self.assertEqual(policy.mesh.scope, MeshScope.MESH_SCOPE_APP)
        self.assertIsNone(policy.egress)

    def test_scope_by_name(self):
        policy = (
            _spec(mesh_scope="MESH_SCOPE_WORKSPACE")
            .deployment_definition()
            .network_policy
        )
        self.assertEqual(policy.mesh.scope, MeshScope.MESH_SCOPE_WORKSPACE)

    def test_unspecified_is_default(self):
        spec = _spec(mesh_scope=MeshScope.MESH_SCOPE_UNSPECIFIED)
        self.assertIsNone(spec.mesh_scope)
        self.assertIsNone(spec.deployment_definition().network_policy)

    def test_scope_combines_with_egress(self):
        policy = (
            _spec(mesh_scope=MeshScope.MESH_SCOPE_APP, outbound_allowlist=["1.2.3.4"])
            .deployment_definition()
            .network_policy
        )
        self.assertEqual(policy.mesh.scope, MeshScope.MESH_SCOPE_APP)
        self.assertEqual(
            policy.egress.mode, EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL
        )
        self.assertEqual([d.cidr for d in policy.egress.allow_list], ["1.2.3.4/32"])

    def test_custom_scope_rejected(self):
        with self.assertRaises(ValueError):
            _spec(mesh_scope=MeshScope.MESH_SCOPE_CUSTOM)

    def test_unknown_scope_rejected(self):
        with self.assertRaises(ValueError):
            _spec(mesh_scope="MESH_SCOPE_GALAXY")

    def test_scope_with_mesh_disabled_rejected(self):
        with self.assertRaises(ValueError):
            _spec(mesh_scope=MeshScope.MESH_SCOPE_APP, enable_mesh=False)

    def test_wire_payload_coerces_into_both_model_flavors(self):
        from koyeb.api_async.models.create_service import (
            CreateService as AsyncCreateService,
        )
        from koyeb.api.models.create_service import CreateService

        payload = _spec(
            mesh_scope=MeshScope.MESH_SCOPE_APP, enable_mesh=True
        ).create_service_payload("app-id")
        self.assertEqual(
            payload["definition"]["network_policy"]["mesh"]["scope"], "MESH_SCOPE_APP"
        )
        for model in (CreateService, AsyncCreateService):
            service = model(**payload)
            self.assertEqual(
                service.definition.network_policy.mesh.scope.value, "MESH_SCOPE_APP"
            )


class TestSandboxSpecMeshScopeRules(unittest.TestCase):
    def test_scope_turns_the_mesh_on(self):
        d = _spec(mesh_scope=MeshScope.MESH_SCOPE_APP).deployment_definition()
        self.assertEqual(d.mesh, DeploymentMesh.DEPLOYMENT_MESH_ENABLED)

    def test_no_scope_keeps_mesh_auto(self):
        self.assertEqual(
            _spec().deployment_definition().mesh, DeploymentMesh.DEPLOYMENT_MESH_AUTO
        )

    def test_free_instance_rejected(self):
        with self.assertRaises(ValueError):
            _spec(mesh_scope=MeshScope.MESH_SCOPE_APP, instance_type="free")

    def test_full_snapshot_rejected(self):
        with self.assertRaises(ValueError):
            _spec(
                mesh_scope=MeshScope.MESH_SCOPE_APP,
                snapshot_id="snap",
                snapshot_type=SnapshotType.FULL,
            )

    def test_filesystem_snapshot_keeps_scope(self):
        spec = _spec(
            mesh_scope=MeshScope.MESH_SCOPE_APP,
            snapshot_id="snap",
            snapshot_type=SnapshotType.FILESYSTEM,
        )
        payload = spec.create_service_payload("app-id")
        self.assertEqual(
            payload["definition"]["network_policy"]["mesh"]["scope"], "MESH_SCOPE_APP"
        )


class TestSandboxSpecHealthChecks(unittest.TestCase):
    def test_default_sends_no_health_checks(self):
        self.assertIsNone(_spec().deployment_definition().health_checks)
