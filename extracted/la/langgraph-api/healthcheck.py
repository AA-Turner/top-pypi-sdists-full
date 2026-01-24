import json
import os
import urllib.request
from ipaddress import IPv6Address, ip_address

from langgraph_api import config


def get_healthcheck_host() -> str:
    server_host = os.environ.get("LANGGRAPH_SERVER_HOST", "0.0.0.0")
    if server_host in (
        "0.0.0.0",  # IPv4 wildcard
        "",  # IPv4/IPv6 dual-stack
    ):
        return "localhost"

    try:
        server_host_ip = ip_address(server_host)
    except ValueError:
        return server_host

    return (
        f"[{server_host_ip.compressed}]"
        if isinstance(server_host_ip, IPv6Address)
        else server_host_ip.compressed
    )


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
