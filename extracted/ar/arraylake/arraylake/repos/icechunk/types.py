import json
from datetime import datetime
from enum import StrEnum
from typing import Any, NewType

from icechunk import Diff, SnapshotInfo
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer, field_validator
from zarr import AsyncArray, AsyncGroup
from zarr.abc.metadata import Metadata

from arraylake.types import datetime_to_isoformat

CommitId = NewType("CommitId", str)
TagName = NewType("TagName", str)
BranchName = NewType("BranchName", str)


class Commit(BaseModel):
    id: CommitId = Field(alias="_id")
    message: str
    commit_time: datetime
    parent_id: CommitId | None = None
    author_name: str | None = None
    author_email: EmailStr | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    @classmethod
    def from_snapshot(cls, snapshot: SnapshotInfo) -> "Commit":
        return cls(
            _id=CommitId(snapshot.id),
            message=snapshot.message,
            commit_time=snapshot.written_at,
            author_name=snapshot.metadata.get("author_name"),
            author_email=snapshot.metadata.get("author_email"),
            parent_id=CommitId(snapshot.parent_id) if snapshot.parent_id else None,
            metadata=dict(snapshot.metadata or {}),
        )

    @field_serializer("commit_time")
    def serialize_commit_time(self, commit_time: datetime) -> str:
        return datetime_to_isoformat(commit_time)


class CommitDiff(BaseModel):
    from_commit_id: CommitId | None
    to_commit_id: CommitId
    new_groups: list[str]
    new_arrays: list[str]
    deleted_groups: list[str]
    deleted_arrays: list[str]
    updated_groups: list[str]
    updated_arrays: list[str]
    updated_chunks: dict[str, int]

    @classmethod
    def from_diff(cls, from_commit_id: str | None, to_commit_id: str, diff: Diff | None) -> "CommitDiff":
        if diff is None:
            return cls.empty(from_commit_id, to_commit_id)

        updated_chunks = {chunk_id: len(chunk_indices) for chunk_id, chunk_indices in diff.updated_chunks.items()}

        return cls(
            from_commit_id=CommitId(from_commit_id) if from_commit_id else None,
            to_commit_id=CommitId(to_commit_id),
            new_groups=list(diff.new_groups),
            new_arrays=list(diff.new_arrays),
            deleted_groups=list(diff.deleted_groups),
            deleted_arrays=list(diff.deleted_arrays),
            updated_groups=list(diff.updated_groups),
            updated_arrays=list(diff.updated_arrays),
            updated_chunks=updated_chunks,
        )

    @classmethod
    def empty(cls, from_commit_id: str | None, to_commit_id: str) -> "CommitDiff":
        return cls(
            from_commit_id=CommitId(from_commit_id) if from_commit_id else None,
            to_commit_id=CommitId(to_commit_id),
            new_groups=[],
            new_arrays=[],
            deleted_groups=[],
            deleted_arrays=[],
            updated_groups=[],
            updated_arrays=[],
            updated_chunks={},
        )


class Branch(BaseModel):
    id: BranchName = Field(alias="_id")
    commit_id: CommitId
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


class CreateBranchRequest(BaseModel):
    name: BranchName
    commit_id: CommitId


class Tag(BaseModel):
    id: TagName
    commit_id: CommitId


class CreateTagRequest(BaseModel):
    name: TagName
    commit_id: CommitId


class Tree(BaseModel):
    path: str
    metadata: Metadata
    children: dict[str, "Tree"]
    model_config = {"arbitrary_types_allowed": True}

    @classmethod
    async def from_node(cls, node: AsyncGroup | AsyncArray, prefix: str = "", depth: int = 10) -> "Tree":
        if depth == 0 or not isinstance(node, AsyncGroup):
            return Tree(path=node.path, metadata=node.metadata, children={})

        children = {}
        async for name, member in node.members():
            if len(prefix) > 0 and not (prefix.startswith(member.path) or member.path.startswith(prefix)):
                continue
            children[name] = await Tree.from_node(member, prefix=prefix, depth=depth - 1)

        return Tree(path=node.path, metadata=node.metadata, children=children)

    @field_serializer("metadata")
    def metadata_field_serializer(self, v: Metadata):
        return json.loads(json.dumps(v.to_dict()))


class GCResult(BaseModel):
    bytes_deleted: int
    chunks_deleted: int
    manifests_deleted: int
    snapshots_deleted: int
    attributes_deleted: int
    transaction_logs_deleted: int
    job_run_id: str | None = None


class ExpirationResult(BaseModel):
    released_snapshots: set[str]
    edited_snapshots: set[str]
    deleted_tags: set[str]
    deleted_branches: set[str]
    job_run_id: str | None = None


# Dataset Tree types for xarray-style representation


class ArrayClassification(StrEnum):
    """Classification of an array as coordinate or data variable (xarray convention)."""

    COORDINATE = "coordinate"
    DATA_VARIABLE = "data_variable"


class ArrayPreview(BaseModel):
    """Preview of array values (first and last few elements)."""

    first_values: list[Any]  # First N values
    last_values: list[Any]  # Last N values
    total_size: int  # Total number of elements


class ClassifiedArray(BaseModel):
    """Array metadata with xarray-style classification."""

    path: str
    name: str
    shape: list[int]
    dtype: str
    dimension_names: list[str]
    attributes: dict[str, Any]
    chunk_shape: list[int]
    shard_shape: list[int] | None = None  # Outer shard shape; None for unsharded arrays
    fill_value: Any = None
    codecs: list[dict[str, Any]] = []  # List of codec configurations
    classification: ArrayClassification
    preview: ArrayPreview | None = None  # Only populated for coordinates
    nbytes: int | None = None  # Total bytes consumed by array elements (uncompressed); None for variable-length dtypes
    chunk_nbytes: int | None = None  # Bytes per chunk (uncompressed); None for variable-length dtypes


class DatasetNode(BaseModel):
    """A group node with classified arrays (represents one xarray Dataset)."""

    path: str
    name: str
    attributes: dict[str, Any]
    dimensions: dict[str, int]  # dim_name -> size
    coordinates: list[ClassifiedArray]
    data_variables: list[ClassifiedArray]
    child_groups: list[str]  # Names of direct child groups (for navigation)
    members_truncated: bool = False
    is_xarray_compatible: bool = True  # False if dimensions conflict or arrays lack dimension_names
    nbytes: int = 0  # Total bytes consumed by all arrays (uncompressed)
    # Returning spec_version in this response to avoid another roundtrip in the web app for IC spec version
    spec_version: int | None = None  # Icechunk spec version (1 or 2)
    model_config = {"arbitrary_types_allowed": True}

    @field_validator("spec_version", mode="before")
    @classmethod
    def validate_spec_version(cls, value: Any) -> int | None:
        """Convert SpecVersion enum to int during validation."""
        if value is None:
            return None
        # Handle icechunk.SpecVersion which has __int__ method
        return int(value)

    @field_serializer("spec_version")
    @classmethod
    def serialize_spec_version(cls, value: Any) -> int | None:
        """Serialize SpecVersion to int for API responses."""
        if value is None:
            return None
        # Handle icechunk.SpecVersion which has __int__ method
        return int(value)
