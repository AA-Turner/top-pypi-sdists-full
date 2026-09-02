"""Tests for the container-launcher command classifier (Mode A)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from runlayer_cli.scan.container_command import (
    canonical_image_identity,
    classify_container_command,
    split_image_reference,
)

# Shared cross-service golden fixture. The backend parser
# (backend/app/domains/ai_watch/container_command.py) runs the same cases in
# app/tests/domains/ai_watch/test_container_command.py, so both parsers
# must agree on every case here.
_PARITY_CASES = json.loads(
    (
        Path(__file__).resolve().parents[1]
        / "fixtures"
        / "container_command_cases.json"
    ).read_text()
)


@pytest.mark.parametrize("case", _PARITY_CASES, ids=lambda c: c["id"])
def test_parity_fixture(case):
    launch = classify_container_command(case["command"], case["args"])
    if case["runtime"] == "host":
        assert launch is None
        return
    assert launch is not None
    assert launch.runtime == case["runtime"]
    assert launch.image_ref == case["image_ref"]
    assert launch.image_digest == case["image_digest"]
    assert launch.env_keys == case["env_keys"]
    assert launch.mounts == case["mounts"]


class TestClassifyRun:
    def test_basic_docker_run(self):
        launch = classify_container_command(
            "docker", ["run", "-i", "--rm", "mcp/github"]
        )
        assert launch is not None
        assert launch.runtime == "container"
        assert launch.subcommand == "run"
        assert launch.raw_image == "mcp/github"
        assert launch.image_ref == "oci:mcp/github:latest"
        assert launch.image_digest is None

    def test_podman_run_with_registry_and_tag(self):
        launch = classify_container_command(
            "podman", ["run", "--rm", "docker.io/mcp/github:1.2"]
        )
        assert launch is not None
        assert launch.image_ref == "oci:docker.io/mcp/github:1.2"

    def test_nerdctl_run(self):
        launch = classify_container_command("nerdctl", ["run", "mcp/time"])
        assert launch is not None
        assert launch.image_ref == "oci:mcp/time:latest"

    def test_create_subcommand(self):
        launch = classify_container_command("docker", ["create", "mcp/github"])
        assert launch is not None
        assert launch.subcommand == "create"
        assert launch.image_ref == "oci:mcp/github:latest"

    def test_digest_pin(self):
        digest = "sha256:" + "a" * 64
        launch = classify_container_command("docker", ["run", f"mcp/github@{digest}"])
        assert launch is not None
        assert launch.image_ref == f"oci:mcp/github@{digest}"
        assert launch.image_digest == digest

    def test_tag_and_digest_prefers_digest(self):
        digest = "sha256:" + "b" * 64
        launch = classify_container_command(
            "docker", ["run", f"mcp/github:1.2@{digest}"]
        )
        assert launch is not None
        assert launch.image_ref == f"oci:mcp/github@{digest}"
        assert launch.image_digest == digest

    def test_registry_with_port_is_not_a_tag(self):
        launch = classify_container_command(
            "docker", ["run", "localhost:5000/team/img:v3"]
        )
        assert launch is not None
        assert launch.image_ref == "oci:localhost:5000/team/img:v3"

    def test_registry_no_tag_defaults_latest(self):
        launch = classify_container_command("docker", ["run", "ghcr.io/org/img"])
        assert launch is not None
        assert launch.image_ref == "oci:ghcr.io/org/img:latest"


class TestFlagGrammar:
    def test_value_flags_skipped_before_image(self):
        launch = classify_container_command(
            "docker",
            ["run", "-e", "TOKEN", "-v", "/a:/b", "--name", "x", "mcp/github"],
        )
        assert launch is not None
        assert launch.image_ref == "oci:mcp/github:latest"
        assert launch.env_keys == ["TOKEN"]
        assert launch.mounts == ["/a:/b"]

    def test_entrypoint_value_not_mistaken_for_image(self):
        launch = classify_container_command(
            "docker", ["run", "--entrypoint", "/bin/sh", "mcp/github"]
        )
        assert launch is not None
        assert launch.image_ref == "oci:mcp/github:latest"

    def test_equals_form_flag(self):
        launch = classify_container_command(
            "docker", ["run", "--name=foo", "--network=host", "mcp/github"]
        )
        assert launch is not None
        assert launch.image_ref == "oci:mcp/github:latest"

    def test_short_boolean_cluster(self):
        launch = classify_container_command("docker", ["run", "-it", "mcp/github"])
        assert launch is not None
        assert launch.image_ref == "oci:mcp/github:latest"

    def test_short_cluster_with_trailing_value(self):
        launch = classify_container_command(
            "docker", ["run", "-ite", "FOO=bar", "mcp/github"]
        )
        assert launch is not None
        assert launch.image_ref == "oci:mcp/github:latest"

    def test_short_attached_value(self):
        launch = classify_container_command("docker", ["run", "-eFOO", "mcp/github"])
        assert launch is not None
        assert launch.image_ref == "oci:mcp/github:latest"
        assert launch.env_keys == ["FOO"]

    def test_double_dash_terminates_flags(self):
        launch = classify_container_command(
            "docker", ["run", "--rm", "--", "mcp/github"]
        )
        assert launch is not None
        assert launch.image_ref == "oci:mcp/github:latest"

    def test_env_keys_never_include_values(self):
        launch = classify_container_command(
            "docker", ["run", "-e", "SECRET=super-secret", "mcp/github"]
        )
        assert launch is not None
        assert launch.env_keys == ["SECRET"]

    def test_global_flags_before_subcommand(self):
        launch = classify_container_command(
            "docker", ["--context", "remote", "run", "mcp/github"]
        )
        assert launch is not None
        assert launch.image_ref == "oci:mcp/github:latest"

    def test_run_with_only_flags_has_no_image(self):
        launch = classify_container_command("docker", ["run", "--rm", "-i"])
        assert launch is not None
        assert launch.runtime == "container"
        assert launch.image_ref is None


class TestExecAndCompose:
    def test_exec_has_no_image(self):
        launch = classify_container_command("docker", ["exec", "my-container", "ls"])
        assert launch is not None
        assert launch.runtime == "container"
        assert launch.subcommand == "exec"
        assert launch.image_ref is None

    def test_docker_compose_subcommand(self):
        launch = classify_container_command("docker", ["compose", "run", "svc"])
        assert launch is not None
        assert launch.runtime == "container"
        assert launch.image_ref is None

    def test_docker_compose_exec(self):
        launch = classify_container_command("docker", ["compose", "exec", "svc", "cmd"])
        assert launch is not None
        assert launch.runtime == "container"
        assert launch.subcommand == "compose exec"
        assert launch.image_ref is None

    def test_compose_standalone_binary(self):
        launch = classify_container_command("docker-compose", ["run", "svc"])
        assert launch is not None
        assert launch.runtime == "container"
        assert launch.image_ref is None

    def test_compose_standalone_exec(self):
        launch = classify_container_command("docker-compose", ["exec", "svc", "cmd"])
        assert launch is not None
        assert launch.runtime == "container"
        assert launch.subcommand == "compose exec"
        assert launch.image_ref is None


class TestCommandBasename:
    def test_absolute_posix_path(self):
        launch = classify_container_command("/usr/local/bin/docker", ["run", "mcp/x"])
        assert launch is not None
        assert launch.image_ref == "oci:mcp/x:latest"

    def test_windows_path_with_exe(self):
        launch = classify_container_command(
            "C:\\Program Files\\Docker\\docker.exe", ["run", "mcp/x"]
        )
        assert launch is not None
        assert launch.image_ref == "oci:mcp/x:latest"


class TestNonContainer:
    @pytest.mark.parametrize(
        ("command", "args"),
        [
            ("npx", ["-y", "@modelcontextprotocol/server-github"]),
            ("node", ["server.js"]),
            ("uvx", ["some-mcp"]),
            ("python", ["-m", "server"]),
            (None, ["run", "mcp/x"]),
            ("dockerize", ["run", "mcp/x"]),  # not an exact launcher basename
        ],
    )
    def test_returns_none(self, command, args):
        assert classify_container_command(command, args) is None

    def test_docker_without_subcommand(self):
        assert classify_container_command("docker", ["--version"]) is None


class TestImageHelpers:
    def test_split_plain(self):
        assert split_image_reference("mcp/github") == ("mcp/github", None, None)

    def test_split_tag(self):
        assert split_image_reference("mcp/github:1.2") == ("mcp/github", "1.2", None)

    def test_split_registry_port(self):
        assert split_image_reference("localhost:5000/img") == (
            "localhost:5000/img",
            None,
            None,
        )

    def test_split_digest(self):
        digest = "sha256:" + "c" * 64
        assert split_image_reference(f"mcp/github@{digest}") == (
            "mcp/github",
            None,
            digest,
        )

    def test_canonical_rejects_flag_like_token(self):
        assert canonical_image_identity("--rm") == (None, None)

    def test_canonical_rejects_empty(self):
        assert canonical_image_identity("") == (None, None)
