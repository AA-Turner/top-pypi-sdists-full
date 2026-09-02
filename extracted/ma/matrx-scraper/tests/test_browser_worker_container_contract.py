from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def test_fargate_volume_bootstrap_drops_privileges_before_worker_start() -> None:
    dockerfile = (PACKAGE_ROOT / "Dockerfile").read_text()
    entrypoint = (
        PACKAGE_ROOT / "docker" / "browser-worker-entrypoint.sh"
    ).read_text()

    assert "USER root" in dockerfile
    assert "command -v runuser >/dev/null" in dockerfile
    assert 'if [[ "$(id -u)" == "0" ]]' in entrypoint
    assert "install -d -m 1777 -o root -g root /tmp" in entrypoint
    assert "install -d -m 1777 -o root -g root /tmp/.X11-unix" in entrypoint
    assert (
        "install -d -m 0750 -o browser-worker -g browser-worker "
        "/home/browser-worker"
    ) in entrypoint
    assert "exec runuser --user browser-worker --preserve-environment" in entrypoint

    privilege_drop = entrypoint.index("exec runuser --user browser-worker")
    xvfb_start = entrypoint.index('Xvfb "${worker_display}"')
    server_start = entrypoint.index("uv run --no-sync uvicorn")
    assert privilege_drop < xvfb_start < server_start


def test_volume_bootstrap_never_recursively_changes_profile_custody() -> None:
    entrypoint = (
        PACKAGE_ROOT / "docker" / "browser-worker-entrypoint.sh"
    ).read_text()

    assert "chown -R" not in entrypoint
    assert "install -d" not in "\n".join(
        line for line in entrypoint.splitlines() if "/profiles" in line
    )


def test_browser_worker_entrypoint_forwards_ecs_termination_to_uvicorn() -> None:
    entrypoint = (
        PACKAGE_ROOT / "docker" / "browser-worker-entrypoint.sh"
    ).read_text()

    assert "trap terminate_server TERM INT" in entrypoint
    assert 'kill -TERM "${server_pid}"' in entrypoint
    assert 'wait "${server_pid}"' in entrypoint
