from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, List, Literal, Optional, TypedDict, Union

from dateutil.parser import isoparse

from typing_extensions import NotRequired

from novita_sandbox.core.template.logger import LogEntry


class TemplateBuildStatus(str, Enum):
    """
    Status of a template build.
    """

    BUILDING = "building"
    WAITING = "waiting"
    READY = "ready"
    ERROR = "error"


@dataclass
class BuildStatusReason:
    """
    Reason for the current build status (typically for errors).
    """

    message: str
    """Message with the status reason."""

    step: Optional[str] = None
    """Step that failed."""

    log_entries: List[LogEntry] = field(default_factory=list)
    """Log entries related to the status reason."""


@dataclass
class TemplateBuildStatusResponse:
    """
    Response from getting build status.
    """

    build_id: str
    """Build identifier."""

    template_id: str
    """Template identifier."""

    status: TemplateBuildStatus
    """Current status of the build."""

    log_entries: List[LogEntry]
    """Build log entries."""

    logs: List[str]
    """Build logs (raw strings). Deprecated: use log_entries instead."""

    reason: Optional[BuildStatusReason] = None
    """Reason for the current status (typically for errors)."""


@dataclass
class TemplateTagInfo:
    """
    Information about assigned template tags.
    """

    build_id: str
    """Build identifier associated with this tag."""

    tags: List[str]
    """Assigned tags of the template."""


@dataclass
class TemplateTag:
    """
    Detailed information about a single template tag.
    """

    tag: str
    """Name of the tag."""

    build_id: str
    """Build identifier associated with this tag."""

    created_at: datetime
    """When this tag was assigned."""


def _parse_date(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return isoparse(value)
    return datetime.fromtimestamp(0)


@dataclass
class TemplateInfo:
    """Information about a listed template."""

    template_id: str
    build_id: str
    aliases: List[str] = field(default_factory=list)
    names: List[str] = field(default_factory=list)
    template_type: Optional[str] = None
    build_status: Optional[str] = None
    build_count: int = 0
    cpu_count: int = 0
    memory_mb: int = 0
    disk_size_mb: int = 0
    spawn_count: int = 0
    envd_version: str = ""
    public: bool = False
    metadata: Optional[dict[str, str]] = None
    created_at: datetime = field(default_factory=lambda: datetime.fromtimestamp(0))
    updated_at: datetime = field(default_factory=lambda: datetime.fromtimestamp(0))
    last_spawned_at: Optional[datetime] = None
    created_by: Optional[dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any], template_type: Optional[str] = None):
        last_spawned_at = data.get("lastSpawnedAt")
        return cls(
            template_id=data.get("templateID", ""),
            build_id=data.get("buildID", ""),
            aliases=data.get("aliases") or [],
            names=data.get("names") or [],
            template_type=data.get("templateType") or template_type,
            build_status=data.get("buildStatus"),
            build_count=data.get("buildCount") or 0,
            cpu_count=data.get("cpuCount") or 0,
            memory_mb=data.get("memoryMB") or 0,
            disk_size_mb=data.get("diskSizeMB") or 0,
            spawn_count=data.get("spawnCount") or 0,
            envd_version=data.get("envdVersion") or "",
            public=bool(data.get("public", False)),
            metadata=data.get("metadata"),
            created_at=_parse_date(data.get("createdAt")),
            updated_at=_parse_date(data.get("updatedAt")),
            last_spawned_at=_parse_date(last_spawned_at) if last_spawned_at else None,
            created_by=data.get("createdBy"),
        )

    @classmethod
    def from_api_template(cls, template: Any, template_type: Optional[str] = None):
        return cls.from_dict(template.to_dict(), template_type=template_type)

    def to_dict(self) -> dict[str, Any]:
        return {
            "templateID": self.template_id,
            "buildID": self.build_id,
            "aliases": self.aliases,
            "names": self.names,
            "templateType": self.template_type,
            "buildStatus": self.build_status,
            "buildCount": self.build_count,
            "cpuCount": self.cpu_count,
            "memoryMB": self.memory_mb,
            "diskSizeMB": self.disk_size_mb,
            "spawnCount": self.spawn_count,
            "envdVersion": self.envd_version,
            "public": self.public,
            "metadata": self.metadata,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
            "lastSpawnedAt": self.last_spawned_at.isoformat()
            if self.last_spawned_at
            else None,
            "createdBy": self.created_by,
        }


@dataclass
class TemplateList:
    """Paginated template list response."""

    items: List[TemplateInfo]
    total: int
    page: int
    limit: int
    total_pages: int

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index: int):
        return self.items[index]


class InstructionType(str, Enum):
    """
    Types of instructions that can be used in a template.
    """

    COPY = "COPY"
    ENV = "ENV"
    RUN = "RUN"
    WORKDIR = "WORKDIR"
    USER = "USER"


class CopyItem(TypedDict):
    """
    Configuration for a single file/directory copy operation.
    """

    src: Union[Union[str, Path], List[Union[str, Path]]]
    dest: Union[str, Path]
    forceUpload: NotRequired[Optional[Literal[True]]]
    user: NotRequired[Optional[str]]
    mode: NotRequired[Optional[int]]
    resolveSymlinks: NotRequired[Optional[bool]]


class Instruction(TypedDict):
    """
    Represents a single instruction in the template build process.
    """

    type: InstructionType
    args: List[str]
    force: bool
    forceUpload: NotRequired[Optional[Literal[True]]]
    filesHash: NotRequired[Optional[str]]
    resolveSymlinks: NotRequired[Optional[bool]]


class GenericDockerRegistry(TypedDict):
    """
    Configuration for a generic Docker registry with basic authentication.
    """

    type: Literal["registry"]
    username: str
    password: str


class AWSRegistry(TypedDict):
    """
    Configuration for AWS Elastic Container Registry (ECR).
    """

    type: Literal["aws"]
    awsAccessKeyId: str
    awsSecretAccessKey: str
    awsRegion: str


class GCPRegistry(TypedDict):
    """
    Configuration for Google Container Registry (GCR) or Artifact Registry.
    """

    type: Literal["gcp"]
    serviceAccountJson: str


class OCIRegistry(TypedDict):
    """
    Configuration for Oracle Cloud Infrastructure Registry.
    """

    type: Literal["oci"]
    tenancyOcid: str
    userOcid: str
    fingerprint: str
    privateKey: str
    region: str


class HuaweiCloudRegistry(TypedDict):
    """
    Configuration for Huawei Cloud Software Repository for Container.
    """

    type: Literal["huawei"]
    accessKeyId: str
    secretAccessKey: str
    region: str


"""
Union type for all supported container registry configurations.
"""
RegistryConfig = Union[
    GenericDockerRegistry,
    AWSRegistry,
    GCPRegistry,
    OCIRegistry,
    HuaweiCloudRegistry,
]


class TemplateType(TypedDict):
    """
    Internal representation of a template for the Novita AI sandbox build API.
    """

    fromImage: NotRequired[str]
    fromTemplate: NotRequired[str]
    fromImageRegistry: NotRequired[RegistryConfig]
    startCmd: NotRequired[str]
    readyCmd: NotRequired[str]
    patchCmd: NotRequired[str]
    steps: List[Instruction]
    force: bool


@dataclass
class BuildInfo:
    """
    Information about a built template.
    """

    template_id: str
    build_id: str
    name: str
    # Deprecated: use name instead
    alias: str
    tags: List[str] = field(default_factory=list)
