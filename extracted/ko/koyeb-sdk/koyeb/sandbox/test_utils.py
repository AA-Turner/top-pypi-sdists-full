import unittest

from koyeb.api.models.egress_policy_mode import EgressPolicyMode
from koyeb.sandbox.utils import (
    EgressPolicyError,
    build_network_policy,
    create_docker_source,
)


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
        self.assertEqual(ds.entrypoint, ["/entrypoint.sh"])
        self.assertEqual(ds.command, "serve")


class TestBuildEgressPolicy(unittest.TestCase):
    """Tests for build_network_policy validation and normalization."""

    def test_both_unset_returns_none(self):
        self.assertIsNone(build_network_policy(False, None))
        self.assertIsNone(build_network_policy())

    def test_both_passed_raises(self):
        with self.assertRaises(EgressPolicyError):
            build_network_policy(True, ["1.2.3.4"])
        with self.assertRaises(EgressPolicyError):
            build_network_policy(True, [])

    def test_block_network_deny_all_without_allowlist(self):
        policy = build_network_policy(True, None)
        self.assertEqual(
            policy.egress.mode, EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL
        )
        self.assertIsNone(policy.egress.allow_list)

    def test_bare_ipv4_normalized_to_slash_32(self):
        policy = build_network_policy(False, ["1.2.3.4"])
        self.assertEqual(
            policy.egress.mode, EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL
        )
        self.assertEqual([d.cidr for d in policy.egress.allow_list], ["1.2.3.4/32"])

    def test_bare_ipv6_normalized_to_slash_128(self):
        policy = build_network_policy(False, ["2001:db8::1"])
        self.assertEqual(
            [d.cidr for d in policy.egress.allow_list], ["2001:db8::1/128"]
        )

    def test_cidr_passthrough(self):
        policy = build_network_policy(False, ["10.0.0.0/8", "2001:db8::/32"])
        self.assertEqual(
            [d.cidr for d in policy.egress.allow_list],
            ["10.0.0.0/8", "2001:db8::/32"],
        )

    def test_cidr_host_bits_normalized(self):
        policy = build_network_policy(False, ["10.0.0.1/8"])
        self.assertEqual([d.cidr for d in policy.egress.allow_list], ["10.0.0.0/8"])

    def test_invalid_entries_raise(self):
        for bad in [
            "example.com",
            "not-an-ip",
            "",
            "  ",
            "10.0.0.0/33",
            "1.2.3",
            "fe80::1%eth0",
        ]:
            with self.assertRaises(EgressPolicyError, msg=f"entry: {bad!r}"):
                build_network_policy(False, [bad])

    def test_empty_allowlist_means_deny_all(self):
        policy = build_network_policy(False, [])
        self.assertEqual(
            policy.egress.mode, EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL
        )
        self.assertEqual(policy.egress.allow_list, [])

    def test_error_is_sandbox_error_and_exported(self):
        import koyeb.sandbox as sandbox_pkg
        from koyeb.sandbox.utils import SandboxError

        self.assertTrue(issubclass(EgressPolicyError, SandboxError))
        self.assertIs(sandbox_pkg.EgressPolicyError, EgressPolicyError)
        self.assertIn("EgressPolicyError", sandbox_pkg.__all__)


if __name__ == "__main__":
    unittest.main()
