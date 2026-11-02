import contextlib
from datetime import datetime
from enum import StrEnum, auto
from os import PathLike
from pathlib import Path
from typing import Any, Self
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    model_validator,
)

from edison_client.clients.exceptions import DataStorageValidationError


class DataStorageEntryStatus(StrEnum):
    PENDING = auto()
    ACTIVE = auto()
    FAILED = auto()
    DISABLED = auto()


class ShareStatus(StrEnum):
    PRIVATE = auto()
    PUBLIC = auto()
    SHARED = auto()


class DataStorageEntry(BaseModel):
    """Model representing a data storage entry."""

    id: UUID = Field(description="Unique identifier for the data storage entry")
    name: str = Field(description="Name of the data storage entry")
    description: str | None = Field(
        default=None, description="Description of the data storage entry"
    )
    content: str | None = Field(
        default=None, description="Content of the data storage entry"
    )
    status: DataStorageEntryStatus = Field(
        description="Status of the data storage entry"
    )
    embedding: list[float] | None = Field(
        default=None, description="Embedding vector for the content"
    )
    is_collection: bool = Field(
        default=False, description="Whether this entry is a collection"
    )
    tags: list[str] | None = Field(
        default=None,
        description="List of tags associated with the data storage entry",
    )
    parent_id: UUID | None = Field(
        default=None,
        description="ID of the parent entry if this is a sub-entry for hierarchical storage",
    )
    project_id: UUID | None = Field(
        default=None,
        description="ID of the project this data storage entry belongs to",
    )
    dataset_id: UUID | None = Field(
        default=None,
        description="ID of the dataset this entry belongs to",
    )
    file_path: str | None = Field(
        default=None,
        description="Path in the storage system where this entry is located, if a file.",
    )
    bigquery_schema: Any | None = Field(
        default=None, description="Target BigQuery schema for the data storage entry"
    )
    user_id: str = Field(description="ID of the user who created this entry")
    created_at: datetime = Field(description="Timestamp when the entry was created")
    modified_at: datetime = Field(
        description="Timestamp when the entry was last updated"
    )

    share_status: ShareStatus = Field(
        description="Share status of the data storage entry"
    )
    short_alias: str | None = Field(
        default=None, description="Short alias for the data storage entry"
    )


class DataStorageType(StrEnum):
    BIGQUERY = auto()
    GCS = auto()
    LINK = auto()
    PG_TABLE = auto()
    RAW_CONTENT = auto()
    ELASTIC_SEARCH = auto()


class DataContentType(StrEnum):
    BQ_DATASET = auto()
    BQ_TABLE = auto()
    TEXT = auto()
    TEXT_W_EMBEDDINGS = auto()
    DIRECTORY = auto()
    FILE = auto()
    INDEX = auto()
    INDEX_W_EMBEDDINGS = auto()


class DataStorageLocationPayload(BaseModel):
    storage_type: DataStorageType
    content_type: DataContentType
    content_schema: JsonValue | None = None
    metadata: JsonValue | None = None
    location: str | None = None


class DataStorageLocationConfig(BaseModel):
    """Model representing the location configuration within a DataStorageLocations object."""

    storage_type: str = Field(description="Type of storage (e.g., 'gcs', 'pg_table')")
    content_type: str = Field(description="Type of content stored")
    content_schema: JsonValue | None = Field(default=None, description="Content schema")
    metadata: JsonValue | None = Field(default=None, description="Location metadata")
    location: str | None = Field(
        default=None, description="Location path or identifier"
    )
    signed_url: str | None = Field(
        default=None,
        description="Signed URL for uploading/downloading the file to/from GCS",
    )


class DataStorageLocation(BaseModel):
    """Model representing storage locations for a data storage entry."""

    id: UUID = Field(description="Unique identifier for the storage locations")
    data_storage_id: UUID = Field(description="ID of the associated data storage entry")
    storage_config: DataStorageLocationConfig = Field(
        description="Storage location configuration"
    )
    created_at: datetime = Field(description="Timestamp when the location was created")


class DataStorageResponse(BaseModel):
    """Response model for data storage operations."""

    data_storage: DataStorageEntry = Field(description="The created data storage entry")
    storage_locations: list[DataStorageLocation] = Field(
        description="Storage location for this data entry"
    )
    content: str | None = None
    revision_id: UUID | None = None
    version: int = 0
    current_revision_id: UUID | None = None
    revision_generation: int = 0


class DataStorageRevisionSnapshot(BaseModel):
    name: str
    content: str | None = None
    storage_location: DataStorageLocationConfig | None = None
    file_path: str | None = None
    metadata: dict[str, Any] | None = None
    embedding: list[float] | None = None


class DataStorageRevision(BaseModel):
    id: UUID
    entry_id: UUID
    version: int
    parent_revision_id: UUID | None
    snapshot: DataStorageRevisionSnapshot
    created_by: str
    trajectory_id: UUID | None
    created_at: datetime
    published_at: datetime | None


class DataStorageRevisionListResponse(BaseModel):
    entry_id: UUID
    current_revision_id: UUID | None
    revisions: list[DataStorageRevision]


class DataStorageRevisionUpdate(BaseModel):
    """Create content or publish a draft using the base revision the editor read.

    Reuse the same payload and revision_id when retrying a request. A stale
    base returns a conflict; read the latest content before preparing a new update.
    """

    model_config = ConfigDict(extra="forbid")

    revision_id: UUID = Field(
        description="Client-generated ID for a new revision, or the ID of a draft to publish; distinct from the DSS entry ID"
    )
    base_revision_id: UUID = Field(
        description="Published revision used as the base, or the base of the draft being published"
    )
    content: str | None = None
    source_entry_id: UUID | None = None
    name: str | None = None
    description: str | None = Field(
        default=None, description="Update the entry description alongside the revision."
    )
    publish: bool = True

    @model_validator(mode="after")
    def validate_content(self) -> Self:
        if self.content is not None and self.source_entry_id is not None:
            raise DataStorageValidationError(
                "Provide either inline content or a completed source entry."
            )
        if (
            self.content is None
            and self.source_entry_id is None
            and (not self.publish or self.name is not None)
        ):
            raise DataStorageValidationError(
                "Provide content or a completed source entry to create a revision."
            )
        return self


class DataStorageEntryStatusResponse(BaseModel):
    id: UUID
    status: DataStorageEntryStatus


class DataStorageRequestPayload(BaseModel):
    """Payload for creating a data storage entry."""

    name: str = Field(description="Name of the data storage entry")
    description: str | None = Field(
        default=None, description="Description of the data storage entry"
    )
    content: str | None = Field(
        default=None, description="Content of the data storage entry"
    )
    embedding: list[float] | None = Field(
        default=None, description="Embedding vector for the content"
    )
    is_collection: bool = Field(
        default=False, description="Whether this entry is a collection"
    )
    parent_id: UUID | None = Field(
        default=None, description="ID of the parent entry for hierarchical storage"
    )
    project_id: UUID | None = Field(
        default=None,
        description="ID of the project this data storage entry belongs to",
    )
    dataset_id: UUID | None = Field(
        default=None,
        description="ID of existing dataset to add entry to, or None to create new dataset",
    )
    file_path: PathLike | str | None = Field(
        default=None,
        description="Filepath to store in the GCS bucket.",
    )
    existing_location: DataStorageLocationPayload | None = Field(
        default=None, description="Existing non-GCS storage metadata"
    )
    tags: list[str] | None = Field(
        default=None,
        description="List of tags associated with the data storage entry",
    )
    metadata: dict[str, Any] | None = Field(
        default=None, description="Metadata for the data storage entry"
    )


class DatasetStorage(BaseModel):
    """Pydantic model representing a DatasetStorage record."""

    id: UUID
    name: str
    user_id: str
    description: str | None = None
    created_at: datetime
    modified_at: datetime


class GetDatasetAndEntriesResponse(BaseModel):
    dataset: DatasetStorage
    data_storage_entries: list[DataStorageEntry]


class CreateDatasetPayload(BaseModel):
    """Payload for creating a dataset."""

    id: UUID | None = Field(
        default=None,
        description="ID of the dataset to create, or None to create a new dataset",
    )
    name: str = Field(description="Name of the dataset")
    description: str | None = Field(
        default=None, description="Description of the dataset"
    )


class ManifestEntry(BaseModel):
    """Model representing a single entry in a manifest file."""

    description: str | None = Field(
        default=None, description="Description of the file or directory"
    )
    metadata: dict[str, Any] | None = Field(
        default=None, description="Additional metadata for the entry"
    )


class DirectoryManifest(BaseModel):
    """Model representing the structure of a manifest file."""

    entries: dict[str, "ManifestEntry | DirectoryManifest"] = Field(
        default_factory=dict,
        description="Map of file/directory names to their manifest entries",
    )

    def get_entry_description(self, name: str) -> str | None:
        """Get description for a specific entry."""
        entry = self.entries.get(name)
        if isinstance(entry, ManifestEntry):
            return entry.description
        if isinstance(entry, DirectoryManifest):
            # For nested directories, could derive description from contents
            return None
        return None

    def get_entry_metadata(self, name: str) -> dict[str, Any] | None:
        """Get metadata for a specific entry."""
        entry = self.entries.get(name)
        if isinstance(entry, ManifestEntry):
            return entry.metadata
        return None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DirectoryManifest":
        """Create DirectoryManifest from a dictionary (loaded from JSON/YAML)."""
        entries: dict[str, ManifestEntry | DirectoryManifest] = {}
        for name, value in data.items():
            if isinstance(value, dict):
                if "description" in value or "metadata" in value:
                    # This looks like a ManifestEntry
                    entries[name] = ManifestEntry(**value)
                else:
                    # This looks like a nested directory
                    entries[name] = cls.from_dict(value)
            else:
                # Simple string description
                entries[name] = ManifestEntry(description=str(value))

        return cls(entries=entries)

    def to_dict(self) -> dict[str, Any]:
        """Convert back to dictionary format."""
        result = {}
        for name, entry in self.entries.items():
            if isinstance(entry, ManifestEntry):
                if entry.description is not None or entry.metadata is not None:
                    entry_dict = {}
                    if entry.description is not None:
                        entry_dict["description"] = entry.description
                    if entry.metadata is not None:
                        entry_dict.update(entry.metadata)
                    result[name] = entry_dict
            elif isinstance(entry, DirectoryManifest):
                result[name] = entry.to_dict()
        return result


class FileMetadata(BaseModel):
    """Model representing metadata for a file being processed."""

    path: Path = Field(description="Path to the file")
    name: str = Field(description="Name of the file")
    size: int | None = Field(default=None, description="Size of the file in bytes")
    description: str | None = Field(
        default=None, description="Description from manifest or generated"
    )
    is_directory: bool = Field(default=False, description="Whether this is a directory")
    parent_id: UUID | None = Field(
        default=None, description="Parent directory ID in the storage system"
    )
    dataset_id: UUID | None = Field(
        default=None, description="Dataset ID this file belongs to"
    )

    @classmethod
    def from_path(
        cls,
        path: Path,
        description: str | None = None,
        parent_id: UUID | None = None,
        dataset_id: UUID | None = None,
    ) -> "FileMetadata":
        """Create FileMetadata from a Path object."""
        size = None
        is_directory = path.is_dir()

        if not is_directory:
            with contextlib.suppress(OSError):
                size = path.stat().st_size

        return cls(
            path=path,
            name=path.name,
            size=size,
            description=description,
            is_directory=is_directory,
            parent_id=parent_id,
            dataset_id=dataset_id,
        )


class UploadProgress(BaseModel):
    """Model for tracking upload progress."""

    total_files: int = Field(description="Total number of files to upload")
    uploaded_files: int = Field(default=0, description="Number of files uploaded")
    total_bytes: int | None = Field(default=None, description="Total bytes to upload")
    uploaded_bytes: int = Field(default=0, description="Number of bytes uploaded")
    current_file: str | None = Field(
        default=None, description="Currently uploading file"
    )
    errors: list[str] = Field(
        default_factory=list, description="List of error messages"
    )

    @property
    def progress_percentage(self) -> float:
        """Calculate progress percentage based on files."""
        if self.total_files == 0:
            return 0.0
        return (self.uploaded_files / self.total_files) * 100.0

    @property
    def bytes_percentage(self) -> float | None:
        """Calculate progress percentage based on bytes."""
        if not self.total_bytes or self.total_bytes == 0:
            return None
        return (self.uploaded_bytes / self.total_bytes) * 100.0

    def add_error(self, error: str) -> None:
        """Add an error message."""
        self.errors.append(error)

    def increment_files(self, bytes_uploaded: int = 0) -> None:
        """Increment the uploaded files counter."""
        self.uploaded_files += 1
        self.uploaded_bytes += bytes_uploaded


class DirectoryUploadConfig(BaseModel):
    """Configuration for directory uploads."""

    name: str = Field(description="Name for the directory upload")
    description: str | None = Field(
        default=None, description="Description for the directory"
    )
    as_collection: bool = Field(
        default=False, description="Upload as single collection or hierarchically"
    )
    manifest_filename: str | None = Field(
        default=None, description="Name of manifest file to use"
    )
    ignore_patterns: list[str] = Field(
        default_factory=list, description="Patterns to ignore"
    )
    ignore_filename: str = Field(
        default=".gitignore", description="Name of ignore file to read"
    )
    base_path: str | None = Field(default=None, description="Base path for storage")
    parent_id: UUID | None = Field(default=None, description="Parent directory ID")
    dataset_id: UUID | None = Field(default=None, description="Dataset ID to use")

    def with_parent(
        self, parent_id: UUID, dataset_id: UUID | None = None
    ) -> "DirectoryUploadConfig":
        """Create a new config with parent and dataset IDs set."""
        return self.model_copy(
            update={"parent_id": parent_id, "dataset_id": dataset_id or self.dataset_id}
        )


class RawFetchResponse(BaseModel):
    """Response model for fetching a raw file."""

    filename: Path | None = Field(
        default=None, description="Name or path of the file uploaded"
    )
    content: str = Field(description="Content of the entry")
    entry_id: UUID = Field(description="ID of the entry")
    entry_name: str = Field(description="Name of the entry")


class PermittedAccessors(BaseModel):
    """Payload for updating data storage permitted accessors."""

    users: list[str] | None = Field(
        default=None,
        description="List of user emails to grant access to the data storage entry",
    )
    organizations: list[str | int] | None = Field(
        default=None,
        description="List of organization IDs to grant access to the data storage entry",
    )


# Forward reference resolution for DirectoryManifest
DirectoryManifest.model_rebuild()
