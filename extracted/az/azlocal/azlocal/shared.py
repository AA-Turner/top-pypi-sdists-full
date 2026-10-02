import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

import certifi

from .constants import LOCALSTACK_HOST_ENV, get_localstack_host

HOME_DIR = Path.home()
AZURE_DIR = os.path.join(HOME_DIR, ".localstack/azure")
AZURE_CONFIG_DIR = os.path.join(AZURE_DIR, "az_config")
LS_HOST = get_localstack_host()

if not os.path.exists(AZURE_DIR):
    Path(AZURE_DIR).mkdir(parents=True, exist_ok=True)


def get_proxy_endpoint() -> str:
    with urllib.request.urlopen(f"{LS_HOST}/_localstack/proxy") as req:
        proxy_details = json.loads(req.read().decode("utf-8"))
        proxy_port = proxy_details["proxy_port"]
    return f"http://localhost:{proxy_port}"


def get_default_proxy_certificate_location(proxy_endpoint: str) -> str:
    certificate_path = os.path.join(AZURE_DIR, "ca.crt")
    if not os.path.exists(certificate_path):
        certificate_bytes = _get_certificate_bytes(proxy_endpoint)
        Path(certificate_path).write_bytes(certificate_bytes)
    return certificate_path


def get_custom_proxy_certificate_location(proxy_endpoint: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(_get_certificate_bytes(proxy_endpoint))
    return tmp.name


def _get_certificate_bytes(proxy_endpoint: str) -> bytes:
    # Stock CA certificates
    certificate_bytes = Path(certifi.where()).read_bytes()

    # Custom CA certificate
    with urllib.request.urlopen(
        f"{proxy_endpoint}/_localstack/certs/ca/LocalStack_LOCAL_Root_CA.crt"
    ) as cert:
        certificate_bytes += cert.read()
    return certificate_bytes


def check_emulator_is_running() -> None:
    try:
        assert urllib.request.urlopen(f"{LS_HOST}/_localstack/health").status == 200
    except (AssertionError, urllib.error.URLError):
        sys.stderr.write(f"Error: LocalStack Emulator did not respond on {LS_HOST}!\n")
        sys.stderr.write(
            f"Make sure that the LocalStack Emulator is running, or configure the correct endpoint using the {LOCALSTACK_HOST_ENV} environment variable.\n"
        )
        exit(1)


def prepare_environment(proxy_endpoint: str) -> dict[str, str]:
    # prepare env vars
    env_dict = os.environ.copy()
    env_dict.update(get_proxy_env_vars(proxy_endpoint))

    # update environment variables in the current process
    os.environ.update(env_dict)
    return env_dict


def get_proxy_env_vars(proxy_endpoint: str, certificate_path: str | None = None) -> dict[str, str]:
    certificate_path = certificate_path or get_default_proxy_certificate_location(proxy_endpoint)

    return {
        "HTTP_PROXY": proxy_endpoint,
        "HTTPS_PROXY": proxy_endpoint,
        "REQUESTS_CA_BUNDLE": certificate_path,
        "SSL_CERT_FILE": certificate_path,
    }


def run_in_background(command: str) -> None:
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    log_az_output(p)


def log_az_output(p: subprocess.Popen[bytes]) -> None:
    if not p.stdout:
        return
    for _ in p.stdout.readlines():
        # TODO: Log this cleanly
        #  Just not to stdout, as we should only print the output of the actual command that the user runs
        pass
