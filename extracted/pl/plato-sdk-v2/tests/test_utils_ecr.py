"""Tests for Docker publish helpers in plato.utils.ecr."""

from __future__ import annotations

from types import SimpleNamespace

from plato.utils import ecr


def _mock_successful_publish(monkeypatch):
    calls: list[list[str]] = []

    def fake_run(cmd, *args, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(ecr.subprocess, "run", fake_run)
    monkeypatch.setattr(ecr, "ensure_repository", lambda _: True)
    monkeypatch.setattr(ecr, "ecr_login", lambda: True)
    return calls


def _buildx_build_call(calls: list[list[str]]) -> list[str]:
    return next(cmd for cmd in calls if cmd[:3] == ["docker", "buildx", "build"])


def test_publish_docker_image_disables_provenance_by_default(tmp_path, monkeypatch):
    (tmp_path / "Dockerfile").write_text("FROM scratch\n")
    calls = _mock_successful_publish(monkeypatch)

    result = ecr.publish_docker_image(
        name="my-world",
        version="1.2.3",
        build_path=str(tmp_path),
        repo_prefix="vm/rootfs/plato-worlds",
    )

    assert result.success is True
    build_cmd = _buildx_build_call(calls)
    assert build_cmd[:3] == ["docker", "buildx", "build"]
    assert "--provenance=false" in build_cmd
    assert build_cmd[-1] == str(tmp_path)


def test_clean_aws_env_strips_credentials_locally(monkeypatch):
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "FAKE")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "FAKE")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "FAKE")

    env = ecr._clean_aws_env()
    assert "AWS_ACCESS_KEY_ID" not in env
    assert "AWS_SECRET_ACCESS_KEY" not in env
    assert "AWS_SESSION_TOKEN" not in env


def test_clean_aws_env_preserves_credentials_in_ci(monkeypatch):
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "OIDC_ID")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "OIDC_SECRET")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "OIDC_TOKEN")

    env = ecr._clean_aws_env()
    assert env["AWS_ACCESS_KEY_ID"] == "OIDC_ID"
    assert env["AWS_SECRET_ACCESS_KEY"] == "OIDC_SECRET"
    assert env["AWS_SESSION_TOKEN"] == "OIDC_TOKEN"


def test_publish_docker_image_keeps_target_and_build_args(tmp_path, monkeypatch):
    (tmp_path / "Dockerfile").write_text("FROM scratch AS prod\n")
    calls = _mock_successful_publish(monkeypatch)

    result = ecr.publish_docker_image(
        name="my-agent",
        version="9.9.9",
        build_path=str(tmp_path),
        repo_prefix="vm/rootfs/plato-agents",
        build_args={"FOO": "bar"},
    )

    assert result.success is True
    build_cmd = _buildx_build_call(calls)
    assert "--provenance=false" in build_cmd
    assert "--target" in build_cmd
    assert build_cmd[build_cmd.index("--target") + 1] == "prod"
    assert "--build-arg" in build_cmd
    assert "FOO=bar" in build_cmd
