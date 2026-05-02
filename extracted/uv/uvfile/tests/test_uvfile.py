import os
import pytest
import textwrap
from testcontainers.core.container import DockerContainer

IMAGE = "ghcr.io/astral-sh/uv:latest"


@pytest.fixture(scope="module")
def uv_container():
    """
    Spin up a Docker container with the uv binary preinstalled.
    We'll mount the local source code, install it via pip, and return the container handle.
    """
    # Resolve the absolute path to the project root (where the user likely runs pytest)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    container = DockerContainer(IMAGE)
    # Mount the local project into /app inside the container
    container.with_volume_mapping(project_root, "/app")
    container.start()
    from testcontainers.core.waiting_utils import wait_for_logs
    while True:

        print(container.get_logs())
    delay = wait_for_logs(container, "uv")
    print(delay)
    # Install uvfile from local source code
    exit_code, output = container.exec(["uv", "tool", "install", "."])
    assert exit_code == 0, f"Installation failed: {output}"

    yield container
    container.stop()


def test_uvfile_init(uv_container):
    """
    Tests that `uvfile init` creates a UVFile in the container.
    Ensures the generated file has the expected header and content.
    """
    # Remove any existing UVFile just to ensure a clean slate
    uv_container.exec(["rm", "-f", "UVFile"])

    # Run `uvfile init` with force
    init_result = uv_container.exec(["uvfile", "init", "--force"])
    assert init_result.exit_code == 0, f"uvfile init failed: {init_result.output}"

    # Check that UVFile now exists
    ls_result = uv_container.exec(["ls", "UVFile"])
    assert ls_result.exit_code == 0, f"UVFile not created: {ls_result.output}"

    # Optionally, inspect the file
    cat_result = uv_container.exec(["cat", "UVFile"])
    assert "UVFile: Auto-generated file to track installed uv tools" in cat_result.output, (
        f"UVFile does not contain expected header:\n{cat_result.output}"
    )


def test_uvfile_sync_basic(uv_container):
    """
    Tests syncing a UVFile with a simple single tool requirement.
    Then verifies that tool is installed via `uv tool list`.
    """
    # Create a minimal UVFile that requires ruff (for example)
    uvfile_contents = textwrap.dedent(
        """
        ruff>=0.2.0
        """
    )
    uv_container.exec(["sh", "-c", f'echo "{uvfile_contents}" > UVFile'])

    # Run `uvfile sync`
    sync_result = uv_container.exec(["uvfile", "sync"])
    assert sync_result.exit_code == 0, f"uvfile sync failed: {sync_result.output}"

    # Check that ruff is installed in uv tool list
    tool_list_result = uv_container.exec(["uv", "tool", "list"])
    # We expect 'ruff' to appear in the tool list output
    assert "ruff" in tool_list_result.output, (
        f"Expected 'ruff' in uv tool list:\n{tool_list_result.output}"
    )


def test_uvfile_env(uv_container):
    """Tests that `uvfile env` returns a shell wrapper script without error."""
    env_result = uv_container.exec(["uvfile", "env"])
    assert env_result.exit_code == 0, f"uvfile env command failed: {env_result.output}"
    assert "uv () {" in env_result.output, "Expected uv wrapper script not found in output."