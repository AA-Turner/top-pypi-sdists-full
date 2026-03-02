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
    build_cmd = calls[0]
    assert build_cmd[:2] == ["docker", "build"]
    assert "--provenance=false" in build_cmd
    assert build_cmd[-1] == str(tmp_path)


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
    build_cmd = calls[0]
    assert "--provenance=false" in build_cmd
    assert "--target" in build_cmd
    assert build_cmd[build_cmd.index("--target") + 1] == "prod"
    assert "--build-arg" in build_cmd
    assert build_cmd[build_cmd.index("--build-arg") + 1] == "FOO=bar"
