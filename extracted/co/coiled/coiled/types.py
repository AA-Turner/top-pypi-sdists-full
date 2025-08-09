import re
from enum import Enum
from logging import getLogger
from pathlib import Path
from typing import BinaryIO, Dict, List, Optional, Tuple, Union

from typing_extensions import Literal, TypedDict
from urllib3.util import parse_url

logger = getLogger("coiled.package_sync")


event_type_list = Literal[
    "add_role_to_profile",
    "attach_gateway_to_router",
    "attach_subnet_to_router",
    "create_vm",
    "create_machine_image",
    "create_schedulercreate_worker",
    "delete_machine_image",
    "create_fw_rule",
    "create_fw",
    "create_network_cidr",
    "create_subnet",
    "create_network",
    "create_log_sink",
    "create_router",
    "create_iam_role",
    "create_log_bucket",
    "create_storage_bucket",
    "create_instance_profile",
    "check_log_sink_exists",
    "check_or_attach_cloudwatch_policy",
    "delete_vm",
    "delete_route",
    "get_firewall",
    "get_network",
    "get_subnet",
    "get_policy_arn",
    "get_log_group",
    "gcp_instance_create",
    "net_gateways_get_or_create",
    "scale",
]


class CondaPlaceHolder(dict):
    pass


class PackageInfo(TypedDict):
    name: str
    path: Optional[Path]
    source: Literal["pip", "conda"]
    channel_url: Optional[str]
    channel: Optional[str]
    subdir: Optional[str]
    conda_name: Optional[str]
    version: str
    wheel_target: Optional[str]
    requested: bool


class PackageSchema(TypedDict):
    name: str
    source: Literal["pip", "conda"]
    channel: Optional[str]
    conda_name: Optional[str]
    client_version: Optional[str]
    specifier: str
    include: bool
    file: Optional[int]


class ResolvedPackageInfo(TypedDict):
    name: str
    source: Literal["pip", "conda"]
    channel: Optional[str]
    conda_name: Optional[str]
    client_version: Optional[str]
    specifier: str
    include: bool
    note: Optional[str]
    error: Optional[str]
    sdist: Optional[BinaryIO]
    md5: Optional[str]


class PackageLevelEnum(int, Enum):
    """
    Package mismatch severity level
    Using a high int so we have room to add extra levels as needed

    Ordering is allow comparison like

    if somelevel >= PackageLevelEnum.STRICT_MATCH:
        <some logic for high or critical levels>
    """

    CRITICAL = 100
    STRICT_MATCH = 75
    WARN = 50
    NONE = 0
    LOOSE = -1
    IGNORE = -2
    MATCH_MINOR = -3
    MATCH_MINOR_CEILING = -4
    IGNORE_UNLESS_REQUESTED = -5


KNOWN_PACKAGE_LEVELS = {level.value for level in PackageLevelEnum}


class ApproximatePackageRequest(TypedDict):
    name: str
    priority_override: Optional[PackageLevelEnum]
    python_major_version: str
    python_minor_version: str
    python_patch_version: str
    source: Literal["pip", "conda"]
    channel_url: Optional[str]
    channel: Optional[str]
    subdir: Optional[str]
    conda_name: Optional[str]
    version: str
    wheel_target: Optional[str]
    requested: bool


class ApproximatePackageResult(TypedDict):
    name: str
    conda_name: Optional[str]
    specifier: Optional[str]
    include: bool
    note: Optional[str]
    error: Optional[str]
    channel_url: Optional[str]
    client_version: Optional[str]


class PiplessCondaEnvSchema(TypedDict, total=False):
    name: Optional[str]
    channels: List[str]
    dependencies: List[str]


class CondaEnvSchema(TypedDict, total=False):
    name: Optional[str]
    channels: List[str]
    dependencies: List[Union[str, Dict[str, List[str]]]]


class SoftwareEnvSpec(TypedDict):
    packages: List[PackageSchema]
    raw_pip: Optional[List[str]]
    raw_conda: Optional[CondaEnvSchema]


# KNOWN_SUBDIRS is copied from conda's known subdirs
KNOWN_SUBDIRS = (
    "noarch",
    "emscripten-wasm32",
    "wasi-wasm32",
    "freebsd-64",
    "linux-32",
    "linux-64",
    "linux-aarch64",
    "linux-armv6l",
    "linux-armv7l",
    "linux-ppc64",
    "linux-ppc64le",
    "linux-riscv64",
    "linux-s390x",
    "osx-64",
    "osx-arm64",
    "win-32",
    "win-64",
    "win-arm64",
    "zos-z",
)
KNOWN_SUBDIR_RE = re.compile(r"(?:/|^)(?:" + "|".join(KNOWN_SUBDIRS) + r")(?:/|$)", flags=re.IGNORECASE)


# This function is in this module to prevent circular import issues
def parse_conda_channel(package_name: str, channel: str, subdir: str) -> Tuple[Optional[str], str]:
    """Return a channel and channel_url for a conda package with any extra information removed."""
    # Handle unknown channels
    if channel == "<unknown>":
        logger.warning(f"Channel for {package_name} is unknown, setting to conda-forge")
        channel = "conda-forge"
    # Remove all known subdirs from channel for noarch packages, because
    # some versions of conda set the channel to the platform-specific
    # channel, even if the package is noarch. This is a workaround for
    # https://github.com/conda/conda/issues/14790
    if subdir == "noarch":
        channel = KNOWN_SUBDIR_RE.sub("", channel)
    else:
        # Strip correct subdir from channel (e.g. "linux-64" or "osx-arm64")
        # We are conservative in this case, because theoretically
        # a private channel could have a different subdir in its name
        for subdir_suffix in (
            f"/{subdir}",
            f"/{subdir}/",
            # Sometimes non-noarch packages have noarch suffixes because
            # of that conda bug.
            "/noarch",
            "/noarch/",
        ):
            if channel.endswith(subdir_suffix):
                channel = channel[: -len(subdir_suffix)]

    # Handle channel urls
    if channel.startswith(("http:", "https:")):
        channel_url = channel
        parsed_url = parse_url(channel)
        channel = parsed_url.path or ""
        netloc = parsed_url.netloc or ""
        # Strip token from channel name
        if channel.startswith("/t/"):
            channel = channel.split("/", maxsplit=3)[3]
        if channel:
            channel = channel.strip("/")
        if netloc and "anaconda" not in netloc:
            channel = f"{netloc}/{channel}"
        channel = channel
    # TODO: Actually upload these files to S3
    elif channel.startswith("file:"):
        logger.warning(f"Channel for {package_name} is a local file, which is not currently supported")
        channel_url = channel
        channel = channel
    else:
        if channel.startswith("pkgs/"):
            domain = "repo.anaconda.com"
        elif channel.startswith("repo/"):
            domain = "repo.anaconda.cloud"
        else:
            domain = "conda.anaconda.org"
        channel_url = f"https://{domain}/{channel}"
        channel = channel
    return (channel or None), channel_url


class CondaPackage:
    def __init__(self, meta_json: Dict, prefix: Path):
        self.prefix = prefix
        self.name: str = meta_json["name"]
        self.version: str = meta_json["version"]
        self.subdir: str = meta_json["subdir"]
        self.files: str = meta_json["files"]
        self.depends: List[str] = meta_json.get("depends", [])
        self.constrains: List[str] = meta_json.get("constrains", [])
        self.channel, self.channel_url = parse_conda_channel(self.name, meta_json["channel"], self.subdir)
        self.requested_spec = meta_json.get("requested_spec", "")

    def __repr__(self):
        return (
            f"CondaPackage(meta_json={{'name': {self.name!r}, 'version': "
            f"{self.version!r}, 'subdir': {self.subdir!r}, 'files': {self.files!r}, "
            f"'depends': {self.depends!r}, 'constrains': {self.constrains!r}, "
            f"'channel': {self.channel!r}}}, prefix={self.prefix!r})"
        )

    def __str__(self):
        return f"{self.name} {self.version} from {self.channel_url}"


class PackageLevel(TypedDict):
    name: str
    level: PackageLevelEnum
    source: Literal["pip", "conda"]


class ApiBase(TypedDict):
    id: int
    created: str
    updated: str


class SoftwareEnvironmentBuild(ApiBase):
    state: Literal["built", "building", "error", "queued"]


class SoftwareEnvironmentSpec(ApiBase):
    latest_build: Optional[SoftwareEnvironmentBuild]


class SoftwareEnvironmentAlias(ApiBase):
    name: str
    latest_spec: Optional[SoftwareEnvironmentSpec]


class ArchitectureTypesEnum(str, Enum):
    """
    All currently supported architecture types
    """

    X86_64 = "x86_64"
    ARM64 = "aarch64"

    def __str__(self) -> str:
        return self.value

    @property
    def conda_suffix(self) -> str:
        if self == ArchitectureTypesEnum.X86_64:
            return "64"
        else:
            return self.value

    @property
    def vm_arch(self) -> Literal["x86_64", "arm64"]:
        if self == ArchitectureTypesEnum.ARM64:
            return "arm64"
        else:
            return self.value

    @classmethod
    def from_vm_arch(cls, arch):
        return cls.ARM64 if arch == "arm64" else cls(arch)


class ClusterDetailsState(TypedDict):
    state: str
    reason: str
    updated: str


class ClusterDetailsProcess(TypedDict):
    created: str
    name: str
    current_state: ClusterDetailsState
    instance: dict


class ClusterDetails(TypedDict):
    id: int
    name: str
    workers: List[ClusterDetailsProcess]
    scheduler: Optional[ClusterDetailsProcess]
    current_state: ClusterDetailsState
    created: str


class FirewallOptions(TypedDict):
    """
    A dictionary with the following key/value pairs

    Parameters
    ----------
    ports
        List of ports to open to cidr on the scheduler.
        For example, ``[22, 8786]`` opens port 22 for SSH and 8786 for client to Dask connection.
    cidr
        CIDR block from which to allow access. For example ``0.0.0.0/0`` allows access from any IP address.
    """

    ports: List[int]
    cidr: str


class BackendOptions(TypedDict, total=False):
    """
    A dictionary with the following key/value pairs

    Parameters
    ----------
    region_name
        Region name to launch cluster in. For example: us-east-2
    zone_name
        Zone name to launch cluster in. For example: us-east-2a
    firewall
        Deprecated; use ``ingress`` instead.
    ingress
        Allows you to specify multiple CIDR blocks (and corresponding ports) to open for ingress
        on the scheduler firewall.
    spot
        Whether to request spot instances.
    spot_on_demand_fallback
        If requesting spot, whether to request non-spot instances if we get fewer spot instances
        than desired.
    spot_replacement
        By default we'll attempt to replace interrupted spot instances; set to False to disable.
    multizone
        Tell the cloud provider to pick zone with best availability; all VMs will be in a single zone
        unless you also use ``multizone_allow_cross_zone``.
    multizone_allow_cross_zone:
        By default, "multizone" cluster is still in a single zone (which zone is picked by cloud provider).
        This option allows the cluster to have VMs in distinct zones. There's a cost for cross-zone traffic
        (usually pennies per GB), so this is a bad choice for shuffle-heavy workloads, but can be a good
        choice for large embarrassingly parallel workloads.
    use_dashboard_public_ip
        Public IP is used by default, lets you choose to use private IP for dashboard link.
    use_dashboard_https
        When public IP address is used for dashboard, we'll enable HTTPS + auth by default.
        You may want to disable this if using something that needs to connect directly to
        the scheduler dashboard without authentication, such as jupyter dask-labextension.
    network_volumes
        Very experimental option to allow mounting SMB volume on cluster nodes.
    docker_shm_size
        Non-default value for shm_size.
    """

    region_name: Optional[str]
    zone_name: Optional[str]
    firewall: Optional[FirewallOptions]  # TODO deprecate, use ingress instead
    ingress: Optional[List[FirewallOptions]]
    spot: Optional[bool]
    spot_on_demand_fallback: Optional[bool]
    spot_replacement: Optional[bool]
    multizone: Optional[bool]
    multizone_allow_cross_zone: Optional[bool]
    use_dashboard_public_ip: Optional[bool]
    use_dashboard_https: Optional[bool]
    send_prometheus_metrics: Optional[bool]  # TODO deprecate
    prometheus_write: Optional[dict]  # TODO deprecate
    network_volumes: Optional[List[dict]]
    docker_shm_size: Optional[str]


class AWSOptions(BackendOptions, total=False):
    """
    A dictionary with the following key/value pairs plus any pairs in :py:class:`BackendOptions`

    Parameters
    ----------
    keypair_name
        AWS Keypair to assign worker/scheduler instances. This would need to be an existing keypair in your
            account, and needs to be in the same region as your cluster. Note that Coiled can also manage
            adding a unique, ephemeral keypair for SSH access to your cluster;
            see :doc:`ssh` for more information.
    use_placement_group
        If possible, this will attempt to put workers in the same cluster placement group (in theory this can
        result in better network between workers, since they'd be physically close to each other in datacenter,
        though we haven't seen this to have much benefit in practice).
    """

    keypair_name: Optional[str]
    use_placement_group: Optional[bool]


class GCPOptions(BackendOptions, total=False):
    """
    A dictionary with GCP specific key/value pairs plus any pairs in :py:class:`BackendOptions`
    """

    scheduler_accelerator_count: Optional[int]
    scheduler_accelerator_type: Optional[str]
    worker_accelerator_count: Optional[int]
    worker_accelerator_type: Optional[str]


class AzureOptions(BackendOptions, total=False):
    """
    A dictionary with Azure-specific key/value pairs plus any pairs in :py:class:`BackendOptions`
    """

    scheduler_ephemeral_os_disk: Optional[bool]
    worker_ephemeral_os_disk: Optional[bool]
