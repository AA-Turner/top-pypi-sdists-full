import json
import os
import urllib.request

from langgraph_api import config
from langgraph_api.utils.network import get_healthcheck_url_host


def get_healthcheck_host() -> str:
    server_host = os.environ.get("LANGGRAPH_SERVER_HOST", "0.0.0.0")
    return get_healthcheck_url_host(server_host)


def healthcheck():
    host = get_healthcheck_host()

    prefix = ""
    mount_prefix = None
    # Override prefix if it's set in the http config
    if (http := os.environ.get("LANGGRAPH_HTTP")) and (
        mount_prefix := json.loads(http).get("mount_prefix")
    ):
        prefix = mount_prefix
    # Override that
    if config.MOUNT_PREFIX:
        prefix = config.MOUNT_PREFIX

    with urllib.request.urlopen(
        f"http://{host}:{os.environ['PORT']}{prefix}/ok"
    ) as response:
        if response.status != 200:
            raise Exception(f"Healthcheck failed: {response.status}")


if __name__ == "__main__":
    healthcheck()
