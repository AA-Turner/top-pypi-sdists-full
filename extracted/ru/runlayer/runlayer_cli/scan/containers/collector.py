"""Container-runtime collector contract for bounded, read-only discovery."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Callable, Protocol

if TYPE_CHECKING:
    from runlayer_cli.scan.containers.inspect_parse import (
        DiscoveredContainer,
        DockerPSInventory,
    )
    from runlayer_cli.scan.containers.tar_walk import _TarWalkResult


class ContainerRuntimeCollector(Protocol):
    """Read-only runtime operations used by container artifact collection.

    Implementations must honor supplied deadlines and collection caps and must
    never execute code inside a container. The transitive import closure must
    remain compatible with the stdlib-only AI Watch bundle.

    The copy operations receive the inspected ``DiscoveredContainer`` rather
    than a bare id so implementations stay stateless: Docker keys off
    ``container_id`` while the k3s/procfs collector keys off ``pid``. There is
    no inspect-before-copy ordering state held on the collector.
    """

    def discover_container_ids(
        self, *, deadline: float
    ) -> DockerPSInventory | None: ...

    def inspect_containers(
        self,
        *,
        container_ids: list[str],
        deadline: float,
        host_home: Path,
    ) -> list[DiscoveredContainer] | None: ...

    def collect_image_digests(
        self,
        *,
        containers: list[DiscoveredContainer],
        deadline: float,
    ) -> list[DiscoveredContainer]: ...

    def copy_file_archive(
        self,
        *,
        container: DiscoveredContainer,
        path: str,
        deadline: float,
    ) -> bytes | None: ...

    def copy_tree(
        self,
        *,
        container: DiscoveredContainer,
        root_path: str,
        wanted_file: Callable[[str], bool],
        allow_file_in_skipped_directory: Callable[[str], bool] | None = None,
        deadline: float,
        max_stream_bytes: int,
    ) -> _TarWalkResult: ...
