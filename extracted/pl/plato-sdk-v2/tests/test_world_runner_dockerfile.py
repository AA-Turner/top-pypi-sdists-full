from __future__ import annotations

from pathlib import Path


def test_world_base_dockerfile_uses_glibc_base_and_installs_fuse_runtime():
    dockerfile = Path(__file__).resolve().parents[2] / "worlds" / "world-base.Dockerfile"
    content = dockerfile.read_text()

    assert "plato-ubuntu-22.04" in content
    assert "alpine" not in content.lower()
    assert "fuse3" in content
    assert "plato-fuse" in content
