import json
import os
import sys
import tempfile
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest
import uvicorn
import yaml
from dagster._core.test_utils import environ
from dagster_cloud.auth.constants import get_hardcoded_test_agent_token
from dagster_cloud_cli.entrypoint import app
from dagster_shared.utils import find_free_port
from typer.testing import CliRunner

runner = CliRunner()


@contextmanager
def _run_dagit_server(host_unscoped_instance):
    """Run the dagit server on a real port for subprocess access."""
    from dagster_cloud_backend.workspace import CloudDagitProcessContext
    from dagster_cloud_dagit.server.cloud_dagit import CloudDagitWebserver

    port = find_free_port()

    with environ({"SESSION_SECRET_KEY": "fake"}):
        context = CloudDagitProcessContext(host_unscoped_instance, version="test")
        app = CloudDagitWebserver(context).create_asgi_app(debug=True)

        config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
        server = uvicorn.Server(config)

        thread = threading.Thread(target=server.run, daemon=True)
        thread.start()

        # Wait for server to start
        import time

        for _ in range(50):  # Wait up to 5 seconds
            try:
                import httpx

                httpx.get(f"http://127.0.0.1:{port}/server_info", timeout=0.1)
                break
            except Exception:
                time.sleep(0.1)

        try:
            yield f"http://127.0.0.1:{port}"
        finally:
            server.should_exit = True
            thread.join(timeout=5)


@pytest.fixture
def dagit_server_url(host_unscoped_instance):
    """Fixture that provides a real HTTP server URL for the dagit app."""
    with _run_dagit_server(host_unscoped_instance) as url:
        yield url


def _setup_project(project_dir: Path):
    """Adds a dagster_cloud.yaml file and a state-backed component to the project."""
    import shutil

    component_dir = project_dir / "src/foo_bar/defs/the_component"
    component_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(
        Path(__file__).parent / "state_backed_components" / "sample_state_backed_component.py",
        component_dir / "local.py",
    )
    # Create the defs.yaml file
    with (component_dir / "defs.yaml").open("w") as f:
        yaml.dump(
            {"type": ".local.SampleStateBackedComponent"},
            f,
        )

    # Create the dagster_cloud.yaml file
    with open(project_dir.joinpath("dagster_cloud.yaml"), "w") as f:
        dagster_cloud_config = {
            "locations": [
                {
                    "location_name": "test-location",
                    "image": "test-image:latest",
                    "code_source": {"python_file": "test_file.py"},
                }
            ]
        }

        yaml.dump(dagster_cloud_config, f)


def _update_location_state_url(state_dir: Path, new_url: str):
    """Update the URL in all location state files to point to the test server."""
    for state_file in state_dir.glob("location-*.json"):
        with open(state_file) as f:
            state = json.load(f)
        state["url"] = new_url
        with open(state_file, "w") as f:
            json.dump(state, f)


def test_refresh_defs_state(
    monkeypatch: pytest.MonkeyPatch,
    dagit_server_url: str,
) -> None:
    from dagster_test.dg_utils.utils import ProxyRunner, isolated_example_project_foo_bar

    organization_name = "acme"

    with (
        ProxyRunner.test() as dg_runner,
        isolated_example_project_foo_bar(dg_runner, uv_sync=True) as project_dir,
        tempfile.TemporaryDirectory() as tmp_dir,
    ):
        _setup_project(project_dir)

        sys.path.append(os.fspath(project_dir))

        dagster_cloud_state_dir = Path(tmp_dir) / "build"
        dagster_cloud_state_dir.mkdir()

        monkeypatch.setenv("DAGSTER_CLOUD_ORGANIZATION", organization_name)
        monkeypatch.setenv(
            "DAGSTER_CLOUD_API_TOKEN", get_hardcoded_test_agent_token(organization_name)
        )
        monkeypatch.setenv("DAGSTER_BUILD_STATEDIR", os.fspath(dagster_cloud_state_dir))

        # prod ci run
        monkeypatch.setenv("DAGSTER_CLOUD_DEPLOYMENT", "prod")

        # use dagster-cloud ci init
        result = runner.invoke(
            app,
            [
                "ci",
                "init",
                "--statedir",
                os.fspath(dagster_cloud_state_dir),
                "--project-dir",
                os.fspath(project_dir),
            ],
        )
        assert result.exit_code == 0, result.output

        # Update the location state URL to point to our test server instead of https://acme.dagster.cloud
        # This is needed because the subprocess will make real HTTP requests
        # The URL needs to include the organization prefix since dagit routes are /{org}/graphql
        _update_location_state_url(
            dagster_cloud_state_dir, f"{dagit_server_url}/{organization_name}"
        )

        # now refresh the defs state
        result = dg_runner.invoke(
            "plus",
            "deploy",
            "refresh-defs-state",
        )

        assert result.exit_code == 0, result.output
        assert "Updated defs_state_info for all 1 locations" in result.output, result.output

        sys.path.remove(os.fspath(project_dir))
