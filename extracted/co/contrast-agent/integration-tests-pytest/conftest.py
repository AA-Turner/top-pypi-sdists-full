import base64
from collections.abc import Generator
import json
import os
from pathlib import Path
import platform
import shutil

import pytest
from contrast.version import __version__ as AGENT_VERSION
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension
from testcontainers.core.image import DockerImage
from testcontainers.core.network import Network
from testcontainers.core.waiting_utils import re, wait_for_logs
from testcontainers.generic import ServerContainer


API_TOKEN = os.environ.get("CONTRAST__API__TOKEN", "")
if not API_TOKEN:
    legacy_keys = {
        key_name: os.environ.get(f"CONTRAST__API__{key_name.upper()}")
        for key_name in [
            "api_key",
            "service_key",
            "url",
            "user_name",
        ]
    }
    missing_keys = [key_name for key_name, value in legacy_keys.items() if not value]
    if missing_keys:
        pytest.skip(
            reason="API token is not set and required legacy keys are missing: "
            f"{', '.join(missing_keys)}"
        )
    else:
        API_TOKEN = base64.b64encode(bytes(json.dumps(legacy_keys), "utf-8")).decode()

OBSERVE_APP_NAME = (
    f"observe-django-integration-test-app-{AGENT_VERSION}-{platform.python_version()}"
)
if summary_file_name := os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(summary_file_name, "a") as summary_file:
        summary_file.write(
            f"## Observe Django Integration Test App Name\n\n{OBSERVE_APP_NAME}\n\n"
        )


@pytest.fixture
def snapshot_json(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.use_extension(JSONSnapshotExtension)


@pytest.fixture(scope="module")
def mitmproxy(
    shared_network: Network, clean_log_dir: Path
) -> Generator[ServerContainer, None, None]:
    with DockerImage(local_path("mitmproxy")) as image:
        REQUEST_AUDIT_DIR = "/home/mitmproxy/request_audit_logs"
        proxy_server = (
            ServerContainer(port=6066, image=image)
            .with_env("REQUEST_AUDIT_DIR", REQUEST_AUDIT_DIR)
            .with_volume_mapping(clean_log_dir, REQUEST_AUDIT_DIR, mode="rw")
            .with_volume_mapping("mitmproxy-certs", "/root/.mitmproxy", mode="rw")
            .with_network(shared_network)
            .with_network_aliases("mitmproxy")
        )
        # HACK: ServerContainer is going to try to connect to "/" when
        # it enters the context manager. This is going to fail because
        # mitmproxy forwards this request to localhost at the exposed port,
        # which doesn't have a web server running.
        #
        # We override the _connect method to avoid this.
        proxy_server._connect = lambda: ...
        with proxy_server:
            wait_for_logs(proxy_server, re.escape("proxy listening at"))

            yield proxy_server


@pytest.fixture(scope="module")
def observe_django_app(
    mitmproxy: ServerContainer, shared_network: Network, clean_log_dir: Path
) -> Generator[ServerContainer, None, None]:
    with (
        DockerImage(local_path("apps", "django"), target="instrumented-app") as image,
        ServerContainer(port=8080, image=image)
        .with_envs(
            CONTRAST__API__PROXY__ENABLE="true",
            CONTRAST__API__PROXY__URL="http://mitmproxy:6066",
            CONTRAST__API__CERTIFICATE__CA_FILE="/etc/mitmproxy/mitmproxy-ca.pem",
            CONTRAST__API__TOKEN=API_TOKEN,
            CONTRAST__OBSERVE__ENABLE="true",
            CONTRAST__AGENT__PYTHON__OBSERVE_PREVIEW="true",
            CONTRAST__AGENT__POLLING__APP_ACTIVITY_MS="5000",
            CONTRAST__REPORTING__OBSERVE__PROTOCOL="http_json",
            CONTRAST__APPLICATION__NAME=OBSERVE_APP_NAME,
            CONTRAST__SERVER__NAME="observe-integration-tests",
        )
        .with_volume_mapping("mitmproxy-certs", "/etc/mitmproxy")
        .with_volume_mapping(local_path(".."), "/agent", mode="rw")
        .with_volume_mapping(clean_log_dir, "/tmp/logs", mode="rw")
        .with_network(shared_network) as app_server,
    ):
        wait_for_logs(app_server, re.escape("Quit the server with CONTROL-C."))
        app_server.get_api_url = app_server._create_connection_url

        yield app_server


def local_path(*args: str) -> Path:
    """Returns an absolute path relative to this directory."""
    return Path(__file__, "..", *args).resolve()


@pytest.fixture(scope="module")
def shared_network() -> Generator[Network, None, None]:
    with Network() as network:
        yield network


@pytest.fixture(scope="module")
def clean_log_dir() -> Path:
    """
    Fixture to ensure the log directory is clean before tests run.
    """
    log_dir = local_path("logs")
    shutil.rmtree(local_path("logs"), ignore_errors=True)
    return log_dir
