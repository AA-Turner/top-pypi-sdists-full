import os
import re

AZURE_CONFIG_DIR_ENV = "AZURE_CONFIG_DIR"

LOCALSTACK_HOST_ENV = "LOCALSTACK_HOST"
DEFAULT_LOCALSTACK_HOST = "https://azure.localhost.localstack.cloud:4566"

# `urlsplit` parses `localhost:4566` as scheme `localhost`, so detect the scheme by its separator
_SCHEME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")


def get_localstack_host() -> str:
    """
    The endpoint of the LocalStack Emulator, configurable through the `LOCALSTACK_HOST` env var.

    The env var accepts both a full URL and the schemeless `<hostname>:<port>` form used by
    LocalStack itself, which is normalised to `https://`.

    Resolved on every call, so that the environment can still be changed after import time.
    """
    host = os.environ.get(LOCALSTACK_HOST_ENV, "").strip()
    if not host:
        return DEFAULT_LOCALSTACK_HOST
    if not _SCHEME_PATTERN.match(host):
        host = f"https://{host}"
    return host.rstrip("/")
