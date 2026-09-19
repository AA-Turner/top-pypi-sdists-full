"""Best-effort artifact discovery inside running Docker and k3s containers.

The scanner uses the Docker CLI when available, then the local Engine API Unix
socket on Linux. On root Linux scans it also discovers k3s containers through
crictl and reads their files through ``/proc/<pid>/root``. It never executes code
in a container; known artifacts are read-only and parsed in memory.
"""

from runlayer_cli.scan.containers.collect import scan_running_containers
from runlayer_cli.scan.containers.inspect_parse import (
    CONTAINER_SCAN_INCOMPLETE_REASON,
    CONTAINER_SCAN_UNAVAILABLE_REASON,
    CONTAINER_SCAN_UNEXPECTED_REASON,
    ContainerMount,
    ContainerScanResult,
    DiscoveredContainer,
    DiscoveredContainerImage,
    parse_container_inspect,
    parse_image_digests,
    path_is_shared_with_host_home,
    sanitize_container_scan_error,
)
from runlayer_cli.scan.file_collector import (
    MAX_SINGLE_FILE_BYTES as MAX_SINGLE_FILE_BYTES,
)

__all__ = [
    "CONTAINER_SCAN_INCOMPLETE_REASON",
    "CONTAINER_SCAN_UNAVAILABLE_REASON",
    "CONTAINER_SCAN_UNEXPECTED_REASON",
    "MAX_SINGLE_FILE_BYTES",
    "ContainerMount",
    "ContainerScanResult",
    "DiscoveredContainer",
    "DiscoveredContainerImage",
    "parse_container_inspect",
    "parse_image_digests",
    "path_is_shared_with_host_home",
    "sanitize_container_scan_error",
    "scan_running_containers",
]
