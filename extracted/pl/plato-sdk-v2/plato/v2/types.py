"""Helper types for Plato SDK v2.

Re-exports generated models and provides ergonomic factory methods.
"""

from __future__ import annotations

from typing import Any

from plato._generated.models import (
    AppSchemasBuildModelsSimConfigCompute as SimConfigCompute,
)
from plato._generated.models import (
    EnvFromArtifact,
    EnvFromResource,
    EnvFromSimulator,
)


class Env:
    """Factory for environment configurations.

    Provides ergonomic builder methods for environment modes:
    1. simulator + tag: Env.simulator("env:tag") - from artifact snapshot
    2. artifact_id: Env.artifact("artifact-123") - from explicit artifact
    3. simulator + sim_config: Env.resource(...) - blank VM with custom resources
    """

    @staticmethod
    def simulator(
        simulator: str,
        *,
        tag: str | None = None,
        version: str | None = None,
        dataset: str | None = None,
        alias: str | None = None,
        restore_memory: bool = True,
    ) -> EnvFromSimulator:
        """Create env from simulator with tag or version lookup.

        Supports string formats:
        - "simname" -> uses 'latest' tag
        - "simname:tag" -> uses specified tag
        - "simname:version@dataset" -> uses version (git_hash) lookup

        Args:
            simulator: Simulator name with optional tag/version format
            tag: Artifact tag. If neither tag nor version provided, defaults to 'latest'.
            version: Artifact version (git_hash). If provided, looks up by version instead of tag.
            dataset: Dataset name (e.g., "base", "blank"). If not specified, uses default.
            alias: Custom name for this environment
            restore_memory: If True (default), resume from memory snapshot.
                           If False, do a fresh boot with disk state only (for disk snapshots).

        Returns:
            EnvFromSimulator

        Examples:
            >>> Env.simulator("espocrm")  # -> uses "latest" tag
            >>> Env.simulator("espocrm:staging")  # -> uses "staging" tag
            >>> Env.simulator("espocrm:v1@base")  # -> uses version "v1", dataset "base"
            >>> Env.simulator("espocrm:v1@base", restore_memory=False)  # disk snapshot
        """
        sim_name = simulator

        # Parse "simname:version@dataset" format (version lookup)
        if "@" in simulator:
            parts = simulator.split("@", 1)
            dataset = dataset or parts[1]
            if ":" in parts[0]:
                sim_name, version = parts[0].split(":", 1)
            else:
                sim_name = parts[0]
        # Parse "simname:tag" format (tag lookup)
        elif ":" in simulator:
            sim_name, tag = simulator.split(":", 1)

        # Build kwargs
        kwargs: dict[str, Any] = {
            "simulator": sim_name,
            "alias": alias,
            "restore_memory": restore_memory,
        }
        if tag is not None:
            kwargs["tag"] = tag
        if version is not None:
            kwargs["version"] = version
        if dataset is not None:
            kwargs["dataset"] = dataset

        return EnvFromSimulator(**kwargs)

    @staticmethod
    def artifact(
        artifact_id: str,
        *,
        alias: str | None = None,
    ) -> EnvFromArtifact:
        """Create env from explicit artifact ID.

        Args:
            artifact_id: Specific artifact/snapshot ID to use
            alias: Custom name for this environment

        Returns:
            EnvFromArtifact

        Example:
            >>> Env.artifact("artifact-123")
        """
        return EnvFromArtifact(
            artifact_id=artifact_id,
            alias=alias,
        )

    @staticmethod
    def resource(
        simulator: str,
        sim_config: SimConfigCompute | None = None,
        *,
        alias: str | None = None,
        docker_image_url: str | None = None,
        upload_rootfs: bool | None = True,
        rootfs_storage_backend: str | None = None,
    ) -> EnvFromResource:
        """Create env from resource specification (blank VM).

        Args:
            simulator: Simulator/service name
            sim_config: Resource configuration (CPUs, memory, disk). If None, uses defaults.
            alias: Custom name for this environment
            docker_image_url: Custom Docker image URL (ECR). If not set, uses default.
            upload_rootfs: Upload rootfs to S3/snapshot-store if not cached. Set False for one-off VMs.
            rootfs_storage_backend: Storage backend ('sparse-s3' or 'snapshot-store'). If not set, uses default.

        Returns:
            EnvFromResource

        Examples:
            >>> Env.resource("redis", SimConfigCompute(cpus=4, memory=8192, disk=20000))
            >>> Env.resource("agent", docker_image_url="123.dkr.ecr.us-west-1.amazonaws.com/my-image:v1")
            >>> Env.resource("world", rootfs_storage_backend="snapshot-store")
        """
        if sim_config is None:
            sim_config = SimConfigCompute()
        return EnvFromResource(
            simulator=simulator,
            sim_config=sim_config,
            alias=alias,
            docker_image_url=docker_image_url,
            upload_rootfs=upload_rootfs,
            rootfs_storage_backend=rootfs_storage_backend,
        )


__all__ = [
    "Env",
    "EnvFromSimulator",
    "EnvFromArtifact",
    "EnvFromResource",
    "SimConfigCompute",
]
