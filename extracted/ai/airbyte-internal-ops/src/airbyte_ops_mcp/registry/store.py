# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Registry store types and targets.

This module defines the store *types* and parsed *store targets* used by the
registry tooling to read/write connector metadata and build indexes. The
built-in registry types are:

* **coral** -- the Airbyte Cloud/OSS connector registry stored in GCS.
  Connectors are prefixed `source-` or `destination-`.
* **sonar** -- the Airbyte agent connector registry stored in S3.
  Connectors use bare names (`stripe`, `github`, ...).

A *store target* string combines a store type with an environment and an
optional path prefix. The `local` environment uses a filesystem path after a
second colon:

    "coral:dev"              -> coral dev bucket, no prefix
    "coral:prod"             -> coral prod bucket
    "coral:dev/aj-test100"   -> coral dev bucket, prefix "aj-test100"
    "sonar:prod"             -> sonar prod bucket
    "sonar:dev"              -> sonar dev bucket
    "coral:local:/tmp/output" -> local coral output

Auto-detection
--------------
When the caller omits `--store`, we infer the correct store from:

1. **Connector name** -- `source-*` / `destination-*` -> coral, else -> sonar.
2. **Working directory** -- presence of `integrations/` + `connector-sdk/`
   -> sonar; presence of `airbyte-integrations/connectors/` -> coral.
3. **Environment variable** -- `AIRBYTE_REGISTRY_STORE` (e.g. `coral:dev`).

All applicable detection methods are evaluated and compared; if they disagree
a `ValueError` is raised.
"""

from __future__ import annotations

import logging
import os
import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from airbyte_ops_mcp.registry._constants import (
    DEV_METADATA_SERVICE_BUCKET_NAME,
    PROD_METADATA_SERVICE_BUCKET_NAME,
    SONAR_DEV_BUCKET_NAME,
    SONAR_PROD_BUCKET_NAME,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Store type
# ---------------------------------------------------------------------------


class StoreType(str, Enum):
    """Registry store type identifier."""

    SONAR = "sonar"
    CORAL = "coral"

    # -- Auto-detection class methods ----------------------------------------

    @classmethod
    def get_from_connector_name(cls, name: str) -> StoreType:
        """Infer the store type from a connector's technical name.

        Connectors whose name starts with `source-` or `destination-` belong
        to the **coral** registry.  All other names belong to **sonar**.

        Args:
            name: Connector technical name (e.g. `"source-github"` or `"stripe"`).

        Returns:
            The inferred `StoreType`.
        """
        if name.startswith("source-") or name.startswith("destination-"):
            return cls.CORAL
        return cls.SONAR

    @classmethod
    def detect_from_repo_dir(cls, path: Path | None = None) -> StoreType | None:
        """Infer the store type from a repository working directory.

        Checks for well-known directory markers:

        * **sonar** -- `integrations/` alongside `connector-sdk/`
        * **coral** -- `airbyte-integrations/connectors/`

        Args:
            path: Directory to inspect.  Defaults to `Path.cwd`.

        Returns:
            The inferred `StoreType`, or `None` if the directory does
            not match any known registry repository layout.
        """
        if path is None:
            path = Path.cwd()

        # Sonar markers
        if (path / "integrations").is_dir() and (path / "connector-sdk").is_dir():
            return cls.SONAR

        # Coral markers
        if (path / "airbyte-integrations" / "connectors").is_dir():
            return cls.CORAL

        return None


# Mapping: store_type -> env -> bucket name
BUCKET_MAP: dict[StoreType, dict[str, str]] = {
    StoreType.CORAL: {
        "dev": DEV_METADATA_SERVICE_BUCKET_NAME,
        "prod": PROD_METADATA_SERVICE_BUCKET_NAME,
    },
    StoreType.SONAR: {
        "dev": SONAR_DEV_BUCKET_NAME,
        "prod": SONAR_PROD_BUCKET_NAME,
    },
}


# ---------------------------------------------------------------------------
# RegistryStore -- parsed representation of a --store argument
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class RegistryStore:
    """Parsed store target (type + environment + optional prefix).

    `read_only` is an internal invariant used to ensure a source store
    cannot yield a writable filesystem client.

    Examples::

        RegistryStore.parse("coral:dev")
        # -> RegistryStore(store_type=StoreType.CORAL, env="dev", prefix="")
        RegistryStore.parse("coral:dev/aj-test")
        # -> RegistryStore(store_type=StoreType.CORAL, env="dev", prefix="aj-test")
        RegistryStore.parse("sonar:prod")
        # -> RegistryStore(store_type=StoreType.SONAR, env="prod", prefix="")
    """

    store_type: StoreType
    env: str
    prefix: str = ""
    read_only: bool = False
    local_path: Path | None = None

    def __post_init__(self) -> None:
        """Validate local target fields and allocate omitted paths."""
        if self.env == "local":
            if self.prefix:
                raise ValueError("Local store targets cannot have a prefix.")
            if self.local_path is None:
                object.__setattr__(
                    self,
                    "local_path",
                    Path(tempfile.mkdtemp(prefix="airbyte-registry-")),
                )
        elif self.local_path is not None:
            raise ValueError("Only local store targets may have a local path.")

    # -- Derived helpers -----------------------------------------------------

    @property
    def bucket(self) -> str:
        """Resolve the concrete bucket name for this target."""
        if self.env == "local":
            raise ValueError("Local stores do not have a bucket.")
        env_map = BUCKET_MAP.get(self.store_type)
        if env_map is None:
            raise ValueError(f"Unknown store type: {self.store_type!r}")
        bucket_name = env_map.get(self.env)
        if bucket_name is None:
            raise ValueError(
                f"Unknown environment '{self.env}' for store type '{self.store_type.value}'. "
                f"Expected one of: {', '.join(sorted(env_map))}."
            )
        return bucket_name

    @property
    def bucket_root(self) -> str:
        """Bucket or local root with optional prefix appended."""
        if self.env == "local":
            assert self.local_path is not None
            return str(self.local_path)
        if self.prefix:
            return f"{self.bucket}/{self.prefix}"
        return self.bucket

    # -- Parsing -------------------------------------------------------------

    @classmethod
    def parse(cls, target: str) -> RegistryStore:
        """Parse a store target string.

        Accepted formats:

            "coral:dev"

            "coral:prod"
            "coral:dev/aj-test100"
            "sonar:prod"
            "coral:local:/tmp/registry-output"

        Raises:
            ValueError: If the string cannot be parsed or references an
                unknown store type / environment.
        """
        if ":" not in target:
            raise ValueError(
                f"Invalid store target '{target}'. "
                "Expected format: '<store_type>:<env>[/<prefix>]' "
                "(e.g. 'coral:dev', 'sonar:prod', 'coral:dev/my-test')."
            )

        store_part, env_part = target.split(":", 1)

        # Validate store type
        store_part_lower = store_part.lower()
        valid_types = {t.value: t for t in StoreType}
        if store_part_lower not in valid_types:
            raise ValueError(
                f"Unknown store type '{store_part}'. "
                f"Expected one of: {', '.join(sorted(valid_types))}."
            )
        store_type = valid_types[store_part_lower]

        # Split env and prefix
        if env_part.startswith("local:"):
            local_path_text = env_part.removeprefix("local:")
            return cls(
                store_type=store_type,
                env="local",
                local_path=Path(local_path_text) if local_path_text else None,
            )
        env_key, _, prefix = env_part.partition("/")
        prefix = prefix.strip("/")

        # Validate env
        env_map = BUCKET_MAP.get(store_type, {})
        if env_key not in env_map:
            raise ValueError(
                f"Unknown environment '{env_key}' for store type '{store_type.value}'. "
                f"Expected one of: {', '.join(sorted(env_map))}."
            )

        return cls(store_type=store_type, env=env_key, prefix=prefix)


#: Environment variable that can hold a default store target string.
REGISTRY_STORE_ENV_VAR = "AIRBYTE_REGISTRY_STORE"


def resolve_registry_store(
    store: str | None = None,
    connector_name: str | None = None,
    cwd: Path | None = None,
    default_env: str = "dev",
) -> RegistryStore:
    """Resolve a `RegistryStore` from CLI inputs.

    All applicable detection methods are evaluated.  Explicit sources
    (`--store`, then the `AIRBYTE_REGISTRY_STORE` env var) take priority
    and are returned directly.  When only auto-detected sources remain, they
    are compared and a `ValueError` is raised if they disagree.

    Priority (highest → lowest):

    1. **Explicit** `--store` argument (e.g. `"coral:dev"`).
    2. **Environment variable** -- `AIRBYTE_REGISTRY_STORE`.
    3. **Auto-detected** -- connector name and/or working directory.
       If both are present and disagree, a `ValueError` is raised.

    Args:
        store: Explicit store target string (e.g. `"coral:dev"`).
        connector_name: Optional connector name for auto-detection.
        cwd: Working directory for repo-based detection.
        default_env: Environment to use when auto-detecting (default `"dev"`).

    Returns:
        A fully resolved `RegistryStore`.

    Raises:
        ValueError: If no detection method succeeds, or if auto-detected
            methods produce conflicting store types.
    """
    # -- Collect all detection results ------------------------------------
    # Explicit sources (take priority — no conflict checking needed).
    explicit_target: RegistryStore | None = None
    explicit_source: str | None = None

    if store is not None:
        explicit_target = RegistryStore.parse(store)
        explicit_source = "--store"

    env_store = os.environ.get(REGISTRY_STORE_ENV_VAR)
    if env_store and explicit_target is None:
        explicit_target = RegistryStore.parse(env_store)
        explicit_source = REGISTRY_STORE_ENV_VAR

    # Auto-detected sources (only consulted when no explicit source).
    auto_detections: dict[str, StoreType] = {}

    if connector_name is not None:
        auto_detections["connector_name"] = StoreType.get_from_connector_name(
            connector_name,
        )

    dir_type = StoreType.detect_from_repo_dir(cwd)
    if dir_type is not None:
        auto_detections["working_directory"] = dir_type

    # -- Return explicit source if present --------------------------------
    if explicit_target is not None:
        logger.debug(
            "Using explicit store target from %s: %s:%s",
            explicit_source,
            explicit_target.store_type.value,
            explicit_target.env,
        )
        return explicit_target

    # -- No explicit source: resolve from auto-detections -----------------
    if not auto_detections:
        raise ValueError(
            "Cannot determine registry store. "
            "Provide --store (e.g. 'coral:dev' or 'sonar:prod'), "
            f"set ${REGISTRY_STORE_ENV_VAR}, "
            "or run from a recognized repository directory."
        )

    distinct = set(auto_detections.values())

    if len(distinct) > 1:
        detail = ", ".join(f"{src}={st.value}" for src, st in auto_detections.items())
        raise ValueError(
            f"Conflicting store types detected: {detail}. "
            "Provide an explicit --store to resolve the ambiguity."
        )

    resolved_type = distinct.pop()
    logger.info(
        "Auto-detected store type '%s' (sources: %s)",
        resolved_type.value,
        ", ".join(auto_detections),
    )
    return RegistryStore(store_type=resolved_type, env=default_env)
