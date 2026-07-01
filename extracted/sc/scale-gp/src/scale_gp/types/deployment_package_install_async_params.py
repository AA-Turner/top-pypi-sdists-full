# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "DeploymentPackageInstallAsyncParams",
    "VersionConstraint",
    "VersionConstraintSemVerMinVersion",
    "VersionConstraintTimestampMinVersion",
    "VersionConstraintExactVersion",
]


class DeploymentPackageInstallAsyncParams(TypedDict, total=False):
    deployment_package_id: str

    deployment_package_name: str

    deployment_package_type: Literal[
        "EGP_CONFIGURATION",
        "BLOB_STORAGE_FILE",
        "DOCKER_IMAGE",
        "EGP_ENTITY",
        "EGP_USER",
        "INTERNAL_MODEL_INFO",
        "EVALUATION_DATASET",
        "MODEL",
        "KNOWLEDGE_BASE",
        "AGENTS_CONFIG",
    ]

    version_constraint: VersionConstraint


class VersionConstraintSemVerMinVersion(TypedDict, total=False):
    minimum_version: Required[str]

    version_constraint_type: Literal["SEMVER_MIN"]


class VersionConstraintTimestampMinVersion(TypedDict, total=False):
    minimum_timestamp: Required[str]

    version_constraint_type: Literal["TIMESTAMP_MIN"]


class VersionConstraintExactVersion(TypedDict, total=False):
    package_version_id: Required[str]

    version_constraint_type: Literal["EXACT_VERSION"]


VersionConstraint: TypeAlias = Union[
    VersionConstraintSemVerMinVersion, VersionConstraintTimestampMinVersion, VersionConstraintExactVersion
]
