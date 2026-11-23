"""This machine's node key, asked of every metadata server (AWS IMDSv2, GCP, Azure, OCI) at once within one
total budget, else read from what cloud-init recorded (Lambda). It is the key the node daemon gives the same
machine (`agent/tools/probe-node/internal/identity`), so the server can match this process's GPUs to the
node's: AWS `i-0abc`, GCP `<project>/<zone>/<name>`, Azure the lowercased resource id, OCI the instance OCID,
Lambda the API instance id. Never raises."""

from __future__ import annotations

import json
import re
import threading
import time
import urllib.request
from collections.abc import Callable
from pathlib import Path

#: The link-local metadata address every cloud answers on (no DNS lookup to wait for).
METADATA_HOST = "169.254.169.254"
#: The whole ask, every source together: a machine off any cloud pays this once, on a background thread.
BUDGET_SECONDS = 0.2
#: An instance id as a provider's API names it (`i-0abc...`, a GCP or Azure instance name, an OCID).
_INSTANCE_ID = re.compile(r"^[A-Za-z0-9._:()-]{1,128}$")
#: A node key: an instance id, or a path of them (GCP, Azure).
_NODE_KEY = re.compile(r"^[A-Za-z0-9._:/()-]{1,256}$")
#: cloud-init's world-readable instance data, and the dpkg database that marks a Lambda Cloud image.
CLOUD_INIT_DATA = Path("/run/cloud-init/instance-data.json")
DPKG_STATUS = Path("/var/lib/dpkg/status")
_LAMBDA_PACKAGE = "Package: lambda-repository\n"
#: A Lambda Cloud instance id: its API UUID without dashes.
_LAMBDA_ID = re.compile(r"^[0-9a-f]{32}$")

#: (method, url, headers, timeout seconds) -> the body, or None on any failure.
Requester = Callable[[str, str, dict, float], "str | None"]


def request_metadata(method: str, url: str, headers: dict, timeout: float) -> str | None:
    """One metadata request, never through a proxy (the address is link-local)."""
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        metadata_request = urllib.request.Request(url, method=method, headers=headers)
        with opener.open(metadata_request, timeout=timeout) as response:  # noqa: S310 -- a fixed http URL
            if response.status != 200:
                return None
            return response.read(4096).decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001 -- off a cloud, every source fails; that is the normal answer
        return None


def ask_aws(request: Requester, timeout: float) -> str | None:
    """IMDSv2: a session token first, then the instance id under it."""
    token = request("PUT", f"http://{METADATA_HOST}/latest/api/token",
                    {"X-aws-ec2-metadata-token-ttl-seconds": "60"}, timeout)
    if not token:
        return None
    return request("GET", f"http://{METADATA_HOST}/latest/meta-data/instance-id",
                   {"X-aws-ec2-metadata-token": token.strip()}, timeout)


def ask_gcp(request: Requester, timeout: float) -> str | None:
    """`<project-id>/<zone>/<name>`, the shape of GKE's providerID; the numeric id when a part is missing."""
    headers = {"Metadata-Flavor": "Google"}
    base = f"http://{METADATA_HOST}/computeMetadata/v1"
    name = (request("GET", f"{base}/instance/name", headers, timeout) or "").strip()
    zone = (request("GET", f"{base}/instance/zone", headers, timeout) or "").strip().rsplit("/", 1)[-1]
    project = (request("GET", f"{base}/project/project-id", headers, timeout) or "").strip()
    if name and zone and project:
        return f"{project}/{zone}/{name}"
    return request("GET", f"{base}/instance/id", headers, timeout)


def ask_azure(request: Requester, timeout: float) -> str | None:
    """The VM's resource id, lowercased (the providerID's resource-group casing varies); else its vmId."""
    base = f"http://{METADATA_HOST}/metadata/instance/compute"
    headers = {"Metadata": "true"}
    resource_id = (request("GET", f"{base}/resourceId?api-version=2021-02-01&format=text", headers, timeout)
                   or "").strip()
    if resource_id.startswith("/subscriptions/"):
        return resource_id.lower()
    return request("GET", f"{base}/vmId?api-version=2021-02-01&format=text", headers, timeout)


def ask_oci(request: Requester, timeout: float) -> str | None:
    """OCI IMDS v2: the instance OCID."""
    ocid = (request("GET", f"http://{METADATA_HOST}/opc/v2/instance/id",
                    {"Authorization": "Bearer Oracle"}, timeout) or "").strip()
    return ocid if ocid.startswith("ocid1.instance.") else None


#: Every metadata source, in the order a tie is settled (two answering is not expected).
SOURCES: tuple[tuple[str, Callable[[Requester, float], "str | None"]], ...] = (
    ("aws", ask_aws),
    ("gcp", ask_gcp),
    ("azure", ask_azure),
    ("oci", ask_oci),
)


def fetch_node_key(
    budget: float = BUDGET_SECONDS,
    request: Requester = request_metadata,
    cloud_init: Path = CLOUD_INIT_DATA,
    dpkg_status: Path = DPKG_STATUS,
) -> str | None:
    """The first metadata source's node key that answered within ``budget`` seconds in total, else the one
    cloud-init recorded, else None."""
    return _ask_metadata(budget, request) or read_cloud_init_key(cloud_init, dpkg_status)


def _ask_metadata(budget: float, request: Requester) -> str | None:
    deadline = time.monotonic() + budget
    answers: dict[str, str] = {}

    def ask(name: str, source: Callable[[Requester, float], str | None]) -> None:
        try:
            value = clean_node_key(source(request, budget))
        except Exception:  # noqa: BLE001
            value = None
        if value:
            answers[name] = value

    threads = [threading.Thread(target=ask, args=source, name=f"probe-imds-{source[0]}", daemon=True)
               for source in SOURCES]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(max(0.0, deadline - time.monotonic()))
    return next((answers[name] for name, _ in SOURCES if name in answers), None)


def read_cloud_init_key(cloud_init: Path = CLOUD_INIT_DATA, dpkg_status: Path = DPKG_STATUS) -> str | None:
    """For clouds with no metadata service. A Lambda Cloud VM boots from a NoCloud disk whose instance id is
    its API id with dashes (cloud-init calls the cloud "unknown"; the image's apt package names it); any cloud
    cloud-init names gives its own id. A bare NoCloud id (often `iid-local01`) is no identity."""
    try:
        v1 = json.loads(cloud_init.read_text()).get("v1") or {}
    except (OSError, ValueError, AttributeError):
        return None
    instance_id = str(v1.get("instance_id") or "")
    if not instance_id:
        return None
    lambda_id = instance_id.replace("-", "")
    # Lambda Stack brings the same package to people's own servers, and Proxmox boots VMs from NoCloud too:
    # only a Lambda API id (a UUID) makes it Lambda Cloud (the daemon's identity/cloudinit.go agrees).
    if v1.get("platform") == "nocloud" and _LAMBDA_ID.match(lambda_id) and _has_lambda_image(dpkg_status):
        return clean_node_key(lambda_id)
    if str(v1.get("cloud_name") or "").lower() in ("", "unknown", "none", "nocloud"):
        return None
    return clean_node_key(instance_id)


def _has_lambda_image(dpkg_status: Path) -> bool:
    try:
        status = dpkg_status.read_text(errors="replace")
    except OSError:
        return False
    return status.startswith(_LAMBDA_PACKAGE) or f"\n{_LAMBDA_PACKAGE}" in status


def get_instance_id(node_key: str | None) -> str | None:
    """The instance id inside a node key: its last path segment (a GCP or Azure instance name)."""
    return clean_instance_id((node_key or "").rsplit("/", 1)[-1])


def clean_node_key(text: str | None) -> str | None:
    """The key as one token, or None for an empty or odd answer (an HTML error page, a captive portal)."""
    value = (text or "").strip()
    return value if _NODE_KEY.match(value) else None


def clean_instance_id(text: str | None) -> str | None:
    value = (text or "").strip()
    return value if _INSTANCE_ID.match(value) else None
