# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from dataclasses import dataclass
import sys
import os
import resource
import subprocess

from threading import Thread

from contrast.reporting import Reporter
from contrast.utils.configuration_utils import get_hostname, get_platform
from contrast.reporting.teamserver_messages.server_inventory import ServerInventory
from contrast.utils.decorators import fail_loudly, fail_quietly
from contrast_vendor import structlog as logging


logger = logging.getLogger("contrast")


REPORT_RESOURCE_ID_THREAD_NAME = "ContrastReportServerInventory"


def report_server_runtime(
    reporting_client: Reporter, discover_cloud_resource_enabled: bool = True
) -> None:
    """
    Report runtime environment info to TS in a background thread.
    """
    logger.debug("Starting detect runtime environment background thread")
    Thread(
        name=REPORT_RESOURCE_ID_THREAD_NAME,
        daemon=True,
        target=_report_runtime_environment,
        args=(reporting_client, discover_cloud_resource_enabled),
    ).start()


@fail_loudly("Failed to report operating system runtime environment details.")
def _report_runtime_environment(
    reporting_client: Reporter, discover_cloud_resource_enabled
) -> None:
    provider = None
    resource_id = None

    if discover_cloud_resource_enabled:
        provider, resource_id = _detect_cloud_resource_id()

    memory_metrics = get_memory_metrics()

    reporting_client.add_message(
        ServerInventory(
            operating_system=get_platform(),
            runtime_path=sys.executable,
            runtime_version=sys.version.split(" ")[0],
            hostname=get_hostname(),
            is_kubernetes=_is_kubernetes(),
            is_docker=_is_docker(),
            cloud_provider=provider,
            cloud_resource_id=resource_id,
            process_memory_limit_bytes=memory_metrics.process_memory_limit_bytes,
        )
    )


def _is_kubernetes():
    return "KUBERNETES_SERVICE_HOST" in os.environ


@fail_quietly()
def _is_docker():
    docker_env_file = "/.dockerenv"
    cgroup_file = "/proc/self/cgroup"

    if os.path.isfile(docker_env_file):
        return True

    try:
        with open(cgroup_file) as cgroup:
            return "/docker" in cgroup.read().strip()
    except FileNotFoundError:
        logger.debug("The file %s was not found", cgroup_file)

    return False


def _detect_cloud_resource_id():
    extract_from = {
        "aws": extract_aws_resource_id,
        "azure": extract_azure_resource_id,
        # "gcp": extract_gcp_resource_id, # TODO: PYT-3346
    }

    for provider, extract_id_func in extract_from.items():
        try:
            resource_id = extract_id_func()
        except ResourceIdError as e:
            logger.debug(
                "did not extract resource ID",
                provider=provider,
                exc_info=e,
            )
            continue

        logger.debug(
            "discovered resource ID",
            cloud_provider=provider,
            resource_id=resource_id,
        )
        return provider, resource_id
    return None, None


METADATA_ENDPOINT_ADDRESS = "169.254.169.254"
TOTAL_RETRIES = 5
RETRY_BACKOFF_FACTOR = 1  # wait 0s, 1s, 2s, 4s, 8s, ..., on request retry
NO_PROXIES = {"http": "", "https": ""}
TIMEOUT_SECONDS = 10


class ResourceIdError(Exception):
    pass


def extract_azure_resource_id() -> str:
    """
    Extract the resource ID from the Azure Instance Metadata Service.
    """
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util import Retry
    from urllib3.exceptions import MaxRetryError

    # This endpoint comes from https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service?tabs=linux#route-parameters
    RESOURCE_ID_ENDPOINT = f"http://{METADATA_ENDPOINT_ADDRESS}/metadata/instance/compute/resourceId?api-version=2023-07-01&format=text"

    # https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service?tabs=linux#errors-and-debugging
    AZURE_RETRY_CODES = {410, 429, 500}

    with requests.Session() as session:
        retries = Retry(
            total=TOTAL_RETRIES,
            backoff_factor=RETRY_BACKOFF_FACTOR,
            status_forcelist=Retry.RETRY_AFTER_STATUS_CODES.union(AZURE_RETRY_CODES),
        )
        session.mount("http://", HTTPAdapter(max_retries=retries))

        try:
            response = session.get(
                RESOURCE_ID_ENDPOINT,
                proxies=NO_PROXIES,
                headers={"Metadata": "true"},
                timeout=TIMEOUT_SECONDS,
            )
            response.raise_for_status()
        except (MaxRetryError, requests.RequestException) as e:
            raise ResourceIdError("Failed to get Azure resource ID") from e
        return response.text


def extract_aws_resource_id() -> str:
    """
    Generate an AWS ARN for the EC2 instance using its Identity Document.

    See:
    https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html
    """
    logger.debug("Attempting to extract AWS resource ID")

    import requests
    import requests.adapters
    import urllib3.util
    import urllib3.exceptions

    retry_config = urllib3.util.Retry(
        total=TOTAL_RETRIES,
        backoff_factor=RETRY_BACKOFF_FACTOR,
        # force a retry for status codes supporting Retry-After, even if the header is
        # missing
        status_forcelist=urllib3.util.Retry.RETRY_AFTER_STATUS_CODES,
    )

    with requests.Session() as session:
        session.mount(
            "http://", requests.adapters.HTTPAdapter(max_retries=retry_config)
        )
        token = _get_aws_token(session)
        # a token is required for IMDSv2, but if we can't get one, still try IMDSv1 (no
        # token)
        headers = {"X-aws-ec2-metadata-token": token} if token else {}
        try:
            response = session.get(
                f"http://{METADATA_ENDPOINT_ADDRESS}/latest/dynamic/instance-identity/document",
                headers=headers,
                proxies=NO_PROXIES,
                timeout=TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            identity_doc = response.json()
        except (
            urllib3.exceptions.MaxRetryError,
            requests.RequestException,
        ) as e:
            raise ResourceIdError("Failed to get AWS resource ID") from e

    logger.debug("Retrieved AWS identity document", aws_identity_doc=identity_doc)
    try:
        region = identity_doc["region"]
        account_id = identity_doc["accountId"]
        instance_id = identity_doc["instanceId"]
    except KeyError as e:
        raise ResourceIdError(
            "Failed to get AWS resource ID. "
            "Missing a required field in identity document."
        ) from e

    arn = ":".join(
        [
            "arn",
            "aws",
            "ec2",
            region,
            account_id,
            f"instance/{instance_id}",
        ]
    )
    return arn


def _get_aws_token(session) -> str | None:
    logger.debug("Retrieving AWS token")

    import requests
    import urllib3.exceptions

    try:
        token_response = session.put(
            f"http://{METADATA_ENDPOINT_ADDRESS}/latest/api/token",
            headers={
                "X-aws-ec2-metadata-token-ttl-seconds": "300",
            },
            proxies=NO_PROXIES,
            timeout=TIMEOUT_SECONDS,
        )
        token_response.raise_for_status()
        return token_response.text
    except (
        urllib3.exceptions.MaxRetryError,
        requests.RequestException,
    ) as e:
        logger.debug(
            "Unable to retrieve token for AWS IMDSv2 - proceeding without it",
            error=str(e),
        )
    return None


CGROUP_V1_PATH = "/sys/fs/cgroup/memory/memory.limit_in_bytes"
CGROUP_V2_PATH = "/sys/fs/cgroup/memory.max"


@dataclass
class MemoryMetrics:
    total_memory_limit_bytes: int | None
    """
    The effective total memory of the current machine, excluding swap memory. On bare
    metal, this is usually the amount of physical memory connected to the device (and
    visible to the OS). This can be further limited by cgroups (often in containers).
    """
    process_memory_limit_bytes: int | None
    """
    The maximum amount of memory useable by the current process. Must not exceed the
    total memory limit.
    """


def get_memory_metrics() -> MemoryMetrics:
    """
    Retrieve memory information for the current machine / process.
    """
    virtual_mem = _total_virtual_memory_bytes()
    cgroup_mem = _cgroup_memory_limit_bytes()
    _, process_hard_limit_mem = _process_rlimits_bytes()

    total_mem = virtual_mem
    if virtual_mem is not None and cgroup_mem is not None:
        total_mem = min(virtual_mem, cgroup_mem)

    process_mem = total_mem
    if total_mem is not None and process_hard_limit_mem is not None:
        process_mem = min(total_mem, process_hard_limit_mem)

    return MemoryMetrics(
        total_memory_limit_bytes=total_mem,
        process_memory_limit_bytes=process_mem,
    )


LINUX = sys.platform.startswith("linux")
MACOS = sys.platform.startswith("darwin")


@fail_quietly(return_value=None)
def _total_virtual_memory_bytes() -> int | None:
    """
    Get the total memory available on the machine in bytes. Based on the implementation
    of `virtual_memory` from https://github.com/giampaolo/psutil.
    """
    if LINUX:
        return _linux_virtual_memory()
    if MACOS:
        return _macos_virtual_memory()
    return None


def _linux_virtual_memory() -> int:
    """
    See https://github.com/giampaolo/psutil/blob/e7754af7400c0836a721befaba0f54c402c4ecb4/psutil/_pslinux.py#L351-L369
    """
    mems = {}
    # Buffering prevents several issues. See the larger comment in psutil.
    with open("/proc/meminfo", "rb", buffering=32 * 1024) as f:
        for line in f:
            fields = line.split()
            mems[fields[0]] = int(fields[1]) * 1024

    return mems[b"MemTotal:"]


def _macos_virtual_memory() -> int:
    """
    Get the total memory available on macOS in bytes.
    """
    output = subprocess.check_output(["sysctl", "-n", "hw.memsize"])
    return int(output.strip())


@fail_quietly(return_value=None)
def _cgroup_memory_limit_bytes() -> int | None:
    """
    Get the memory limit in bytes imposed by cgroups (used by Docker), or None if not
    found or unlimited.
    """
    for path in (CGROUP_V2_PATH, CGROUP_V1_PATH):
        if os.path.exists(path):
            with open(path) as f:
                val = f.read().strip()
            if not val.isdigit():
                return None
            limit = int(val)
            if limit < 0:
                return None
            return limit
    return None


@fail_quietly(return_value=(None, None))
def _process_rlimits_bytes() -> tuple[int | None, int | None]:
    """
    Get the current memory limits for this process in bytes, according to getrlimit.
    Values that cannot be found or are unlimited are reported as None.
    """
    soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_AS)
    return (
        soft_limit if soft_limit != resource.RLIM_INFINITY else None,
        hard_limit if hard_limit != resource.RLIM_INFINITY else None,
    )
