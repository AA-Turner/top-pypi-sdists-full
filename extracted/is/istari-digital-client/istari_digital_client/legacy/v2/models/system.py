from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, StrictStr
from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional, Set, Union
from typing_extensions import Self

from istari_digital_client.legacy.v2.models.access_relation import AccessRelation
from istari_digital_client.legacy.v2.models.access_subject_type import AccessSubjectType
from istari_digital_client.legacy.v2.models.file_revision import FileRevision
from istari_digital_client.legacy.v2.models.new_snapshot_tag import NewSnapshotTag
from istari_digital_client.legacy.v2.models.new_system_configuration import NewSystemConfiguration
from istari_digital_client.legacy.v2.models.new_tracked_file import NewTrackedFile
from istari_digital_client.legacy.v2.models.new_tracked_system import NewTrackedSystem
from istari_digital_client.legacy.v2.models.system_configuration import (
    SystemConfiguration,
)
from istari_digital_client.legacy.v2.models.page_snapshot_revision_search_item import (
    PageSnapshotRevisionSearchItem,
)
from istari_digital_client.legacy.v2.models.snapshot import Snapshot
from istari_digital_client.legacy.v2.models.snapshot_revision_search_item import SnapshotRevisionSearchItem
from istari_digital_client.legacy.v2.models.snapshot_subsystem_item import SnapshotSubsystemItem
from istari_digital_client.legacy.v2.models.snapshot_tag import SnapshotTag
from istari_digital_client.legacy.v2.models.snapshot_tag_revision import SnapshotTagRevision
from istari_digital_client.legacy.v2.models.tracked_file_specifier_type import TrackedFileSpecifierType
from istari_digital_client.legacy.v2.models.update_tag import UpdateTag
from istari_digital_client.legacy.v2.models.shareable import Shareable
from istari_digital_client.legacy.v2.models.archivable import Archivable
from istari_digital_client.legacy.v2.models.access_relationship import AccessRelationship
from istari_digital_client.legacy.v2.models.access_resource_type import AccessResourceType
from istari_digital_client.legacy.mixin import ClientHaving
from istari_digital_client.legacy.log_utils import log_method

if TYPE_CHECKING:
    from istari_digital_client.legacy.v2.models.subsystem_link import SubsystemLink


class System(BaseModel, ClientHaving, Shareable, Archivable):
    """
    Represents a System object that aggregates configuration, versioning, and file content
    across Snapshots. Systems can be shared, archived, and queried for associated files
    or metadata based on Snapshots or SnapshotTags.

    This model includes methods to fetch file revisions, resolve configuration baselines,
    and load structured file contents (e.g., JSON files) associated with snapshots.
    """

    id: StrictStr
    created: datetime
    created_by_id: StrictStr
    name: StrictStr
    description: StrictStr
    archive_status: StrictStr
    configurations: Optional[List[SystemConfiguration]] = None
    baseline_tagged_snapshot_id: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = [
        "id",
        "created",
        "created_by_id",
        "name",
        "description",
        "archive_status",
        "configurations",
        "baseline_tagged_snapshot_id",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    @log_method
    def _list_file_revisions_by_snapshot(
        self,
        snapshot: Optional[Union[Snapshot | str]] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        name: Optional[List[str]] = None,
        extension: Optional[List[str]] = None,
        sort: Optional[str] = None,
    ) -> PageSnapshotRevisionSearchItem:
        """
        Retrieve a paginated list of file revisions associated with a given snapshot.

        If no snapshot is specified, the system's baseline snapshot will be used.

        :param snapshot: Snapshot object or ID string to fetch revisions for.
        :param page: Page number for pagination.
        :param size: Page size for pagination.
        :param name: Optional list of file names to filter the results.
        :param extension: Optional list of file extensions to filter results (e.g., [".json"]).
        :param sort: Optional sort order, e.g., "name", "created", etc.

        :raises ValueError: If no snapshot is provided and a baseline snapshot cannot be resolved.
        """

        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )

        if snapshot is None:
            snapshot_id = (
                self.baseline_tagged_snapshot_id
                or self.client.get_system_baseline(system_id=self.id).snapshot_id
            )
            if snapshot_id is None:
                raise ValueError(
                    "No snapshot provided and no baseline snapshot exists."
                )
        elif isinstance(snapshot, Snapshot):
            snapshot_id = snapshot.id
        elif isinstance(snapshot, str):
            snapshot_id = snapshot
        else:
            raise ValueError(
                "Invalid type for snapshot. Must be Snapshot, str, or None."
            )

        return self.client.list_snapshot_revisions(
            snapshot_id=snapshot_id,
            page=page,
            size=size,
            name=name,
            extension=extension,
            sort=sort,
        )

    @log_method
    def bulk_share_by_snapshot(
        self,
        subject_id: str,
        access_relation: AccessRelation,
        snapshot: Optional[Union[Snapshot, str]] = None,
    ) -> List[AccessRelationship]:
        """
        Bulk share all files in a snapshot with a subject.

        Iterates every revision item in the given snapshot (defaulting to the system
        baseline) and grants the specified subject access to each associated resource.
        Items without a ``resource_id`` or ``resource_type`` are skipped.

        :param subject_id: The ID of the subject.
        :param access_relation: The access level to grant (VIEWER or EDITOR).
        :param snapshot: Snapshot object or ID string. Defaults to the system baseline.
        :raises ValueError: If the client is not set or no snapshot can be resolved.
        """
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )

        first_page = self._list_file_revisions_by_snapshot(snapshot=snapshot)

        relationships = [
            AccessRelationship(
                subject_type=AccessSubjectType.USER,
                subject_id=subject_id,
                relation=access_relation,
                resource_type=AccessResourceType(item.resource_type.lower()),
                resource_id=item.resource_id,
            )
            for item in first_page.iter_items()
            if item.resource_id and item.resource_type
        ]

        if not relationships:
            return []

        return self.client.bulk_create_access(access_relationship=relationships)

    @log_method
    def bulk_share_by_configuration(
        self,
        subject_id: str,
        access_relation: AccessRelation,
        configuration: Union[SystemConfiguration, str],
    ) -> List[AccessRelationship]:
        """
        Bulk share all files in the latest snapshot of a configuration with a subject.

        Resolves the most recent snapshot for the given configuration and delegates to
        ``bulk_share_by_snapshot``.

        :param subject_id: The ID of the subject.
        :param access_relation: The access level to grant (VIEWER or EDITOR).
        :param configuration: SystemConfiguration object or configuration ID string.
        :raises ValueError: If the client is not set or no snapshots exist for the configuration.
        """
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )

        if isinstance(configuration, SystemConfiguration):
            configuration_id = configuration.id
        elif isinstance(configuration, str):
            configuration_id = configuration
        else:
            raise ValueError(
                "Invalid type for configuration. Must be SystemConfiguration or str."
            )

        snapshots = self.client.list_snapshots(
            configuration_id=configuration_id, size=1, sort="-created"
        )
        if not snapshots.items:
            raise ValueError(
                f"No snapshots found for configuration '{configuration_id}'."
            )

        return self.bulk_share_by_snapshot(
            subject_id=subject_id,
            access_relation=access_relation,
            snapshot=snapshots.items[0].id,
        )

    @log_method
    def bulk_share_by_system(
        self,
        subject_id: str,
        access_relation: AccessRelation,
    ) -> List[AccessRelationship]:
        """
        Bulk share all files in the baseline snapshot of a system with a subject.

        Resolves the baseline snapshot for the given system and delegates to
        ``bulk_share_by_snapshot``.

        :param subject_id: The ID of the subject.
        :param access_relation: The access level to grant (VIEWER or EDITOR).
        :raises ValueError: If the client is not set or no baseline snapshot exists.
        """
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )

        return self.bulk_share_by_snapshot(
            subject_id=subject_id,
            access_relation=access_relation,
        )

    # -------------------------------------------------------------------------
    # Branching API
    # -------------------------------------------------------------------------

    @log_method
    def get_branch(self, name: str) -> SnapshotTag:
        """
        Look up a branch by name. Entry point for all other branching methods.

        Raises ValueError if no tag with that name exists.

        :param name: Name of the branch to look up (e.g. "main").
        """
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        for tag in self._iter_tags():
            if tag.tag == name:
                return tag
        raise ValueError(f"No branch named '{name}' found on system {self.id}.")

    @log_method
    def list_branches(self) -> list[SnapshotTag]:
        """
        Return all user branches on this system (excludes the baseline tag).

        :returns: List of SnapshotTags, one per branch.
        """
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        return [tag for tag in self._iter_tags() if not tag.is_baseline]

    @log_method
    def create_branch(self, name: str, *, from_branch: SnapshotTag) -> SnapshotTag:
        """
        Create a new branch from an existing branch.
        Like `git checkout -b <name>`.

        :param name: Name of the new branch (e.g. "feature/new-algo").
        :param from_branch: SnapshotTag to branch from (obtained via get_branch).
        """
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        if name == "baseline":
            raise ValueError("'baseline' is a reserved branch name.")
        return self.client.create_tag(
            snapshot_id=from_branch.snapshot_id,
            new_snapshot_tag=NewSnapshotTag(tag=name),
        )

    @log_method
    def add_to_branch(
        self,
        branch: SnapshotTag,
        *,
        revisions: list[FileRevision | SnapshotRevisionSearchItem] | None = None,
        subsystems: list[SubsystemLink] | None = None,
    ) -> SnapshotTag:
        """
        Add file revisions and/or subsystems to a branch in a single commit.

        :param branch: SnapshotTag to add to (obtained via get_branch).
        :param revisions: FileRevision or SnapshotRevisionSearchItem objects to add.
        :param subsystems: SubsystemLinks to add to the tracked set.
        """
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        if branch.is_baseline:
            raise ValueError("Cannot commit to the baseline branch.")
        return self._commit(branch, add=revisions, add_subsystems=subsystems)

    @log_method
    def remove_from_branch(
        self,
        branch: SnapshotTag,
        *,
        revisions: list[FileRevision | SnapshotRevisionSearchItem] | None = None,
        subsystems: list[SubsystemLink] | None = None,
    ) -> SnapshotTag:
        """
        Remove file revisions and/or subsystems from a branch in a single commit.

        :param branch: SnapshotTag to remove from (obtained via get_branch).
        :param revisions: FileRevision or SnapshotRevisionSearchItem objects to remove.
        :param subsystems: SubsystemLinks to remove from the tracked set.
        """
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        if branch.is_baseline:
            raise ValueError("Cannot commit to the baseline branch.")
        return self._commit(branch, remove=revisions, remove_subsystems=subsystems)

    @log_method
    def list_branch_revisions(
        self,
        branch: SnapshotTag,
        *,
        name: list[str] | None = None,
        extension: list[str] | None = None,
    ) -> list[SnapshotRevisionSearchItem]:
        """
        Return file revisions tracked by a branch at its current snapshot.

        :param branch: SnapshotTag to inspect (obtained via get_branch).
        :param name: Optional list of file names to filter on.
        :param extension: Optional list of file extensions to filter on (e.g. [".json"]).
        """
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        return list(self._iter_snapshot_revisions(branch.snapshot_id, name=name, extension=extension))

    @log_method
    def list_branch_subsystems(self, branch: SnapshotTag) -> list[SnapshotSubsystemItem]:
        """
        Return all subsystems tracked by a branch at its current snapshot.

        :param branch: SnapshotTag to inspect (obtained via get_branch).
        """
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        return list(self._iter_snapshot_subsystems(branch.snapshot_id))

    @log_method
    def merge_branch(self, *, from_branch: SnapshotTag, to_branch: SnapshotTag) -> SnapshotTag:
        """
        Move `to_branch` to point at the same snapshot as `from_branch`.
        Like `git merge --ff`.

        :param from_branch: Source SnapshotTag (e.g. a feature branch).
        :param to_branch: Target SnapshotTag to update (e.g. main).
        """
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        return self.client.update_tag(
            tag_id=to_branch.id,
            update_tag=UpdateTag(snapshot_id=from_branch.snapshot_id),
        )

    @log_method
    def rollback(self, branch: SnapshotTag, *, steps: int = 1) -> SnapshotTag:
        """
        Move a branch back N positions in its commit history.
        Like `git reset --hard HEAD~N`.

        Requires the tag history endpoint (server Part 2).

        :param branch: SnapshotTag to roll back (obtained via get_branch).
        :param steps: Number of commits to go back. Defaults to 1.
        """
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        if branch.is_baseline:
            raise ValueError("Cannot roll back the baseline branch.")
        if steps < 1:
            raise ValueError(f"steps must be >= 1, got {steps}.")

        history = self.client.get_tag_history(tag_id=branch.id)

        if steps >= len(history):
            raise ValueError(
                f"Cannot roll back {steps} step(s): '{branch.tag}' only has {len(history)} commit(s)."
            )

        target = history[steps]
        return self.client.update_tag(
            tag_id=branch.id,
            update_tag=UpdateTag(snapshot_id=target.snapshot_id),
        )

    @log_method
    def list_branch_history(self, branch: SnapshotTag) -> list[SnapshotTagRevision]:
        """
        Return the full commit history of a branch, newest first.
        Like `git log`.

        Requires the tag history endpoint (server Part 2).

        :param branch: SnapshotTag to inspect (obtained via get_branch).
        """
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        return self.client.get_tag_history(tag_id=branch.id)

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _commit(
        self,
        branch: SnapshotTag,
        *,
        add: list[FileRevision | SnapshotRevisionSearchItem] | None = None,
        remove: list[FileRevision | SnapshotRevisionSearchItem] | None = None,
        add_subsystems: list[SubsystemLink] | None = None,
        remove_subsystems: list[SubsystemLink] | None = None,
    ) -> SnapshotTag:
        """Apply a revision and/or subsystem delta and advance the branch pointer."""
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        snapshot = self.client.get_snapshot(snapshot_id=branch.snapshot_id)

        # File revision delta
        current_files = list(self._iter_tracked_files(snapshot.configuration_id))
        remove_revision_ids = {
            r.revision_id if isinstance(r, SnapshotRevisionSearchItem) else r.id
            for r in (remove or [])
        }
        new_tracked_files = [
            NewTrackedFile(
                specifier_type=tf.specifier_type,
                file_id=tf.file_id,
                pinned_file_revision_id=tf.pinned_file_revision_id,
            )
            for tf in current_files
            if tf.pinned_file_revision_id not in remove_revision_ids
        ]
        for r in (add or []):
            revision_id = r.revision_id if isinstance(r, SnapshotRevisionSearchItem) else r.id
            new_tracked_files.append(NewTrackedFile(
                specifier_type=TrackedFileSpecifierType.LOCKED,
                file_id=r.file_id,
                pinned_file_revision_id=revision_id,
            ))

        # Subsystem delta
        current_subsystems = list(self._iter_tracked_subsystems(snapshot.configuration_id))
        remove_subsystem_ids = {link.system.id for link in (remove_subsystems or [])}
        new_tracked_systems = [
            NewTrackedSystem(system_id=ts.id, tag_id=ts.tag_id)
            for ts in current_subsystems
            if ts.id not in remove_subsystem_ids
        ]
        for link in (add_subsystems or []):
            new_tracked_systems.append(
                NewTrackedSystem(system_id=link.system.id, tag_id=link.tag.id if link.tag else None)
            )

        cfg = self.client.create_configuration(
            system_id=self.id,
            new_system_configuration=NewSystemConfiguration(
                name=f"{branch.tag}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                tracked_files=new_tracked_files,
                tracked_systems=new_tracked_systems,
            ),
        )
        snapshot_id = self._latest_snapshot_id(cfg.id)
        return self.client.update_tag(
            tag_id=branch.id,
            update_tag=UpdateTag(snapshot_id=snapshot_id),
        )

    def _latest_snapshot_id(self, configuration_id: str) -> str:
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        page = self.client.list_snapshots(configuration_id=configuration_id, size=1, sort="-created")
        if not page.items:
            raise ValueError(f"Configuration {configuration_id} has no snapshots.")
        return page.items[0].id

    def _iter_tags(self):
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        page_num = 1
        while True:
            page = self.client.list_tags(system_id=self.id, page=page_num)
            yield from page.items
            if page_num * page.size >= page.total:
                break
            page_num += 1

    def _iter_tracked_files(self, configuration_id: str):
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        page_num = 1
        while True:
            page = self.client.list_tracked_files(configuration_id=configuration_id, page=page_num)
            yield from page.items
            if page_num * page.size >= page.total:
                break
            page_num += 1

    def _iter_snapshot_revisions(
        self,
        snapshot_id: str,
        *,
        name: list[str] | None = None,
        extension: list[str] | None = None,
    ):
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        page_num = 1
        while True:
            page = self.client.list_snapshot_revisions(
                snapshot_id=snapshot_id,
                page=page_num,
                name=name,
                extension=extension,
            )
            yield from page.items
            if page_num * page.size >= page.total:
                break
            page_num += 1

    def _iter_tracked_subsystems(self, configuration_id: str):
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        page_num = 1
        while True:
            page = self.client.list_configuration_subsystems(configuration_id=configuration_id, page=page_num)
            yield from page.items
            if page_num * page.size >= page.total:
                break
            page_num += 1

    def _iter_snapshot_subsystems(self, snapshot_id: str):
        if self.client is None:
            raise ValueError(
                "Client is not set. Please set the client before calling this method."
            )
        page_num = 1
        while True:
            page = self.client.list_snapshot_subsystems(snapshot_id=snapshot_id, page=page_num)
            yield from page.items
            if page_num * page.size >= page.total:
                break
            page_num += 1

    def to_str(self) -> str:
        """
        Return the string representation of the model using field aliases.

        This method serializes the model to a JSON-formatted string, respecting any defined aliases
        for fields instead of their original attribute names.
        """
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """
        Return the JSON string representation of the model using field aliases.

        This method serializes the model into a JSON-formatted string, using aliases for field names
        where defined instead of their raw attribute names.
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """
        Create an instance of the model from a JSON string.

        This method deserializes the given JSON string into a model instance. It expects the
        string to match the model's schema, using field aliases where applicable.

        :param json_str: JSON string representing the model.
        :type json_str: str
        """
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """
        Return the dictionary representation of the model using field aliases.

        This method differs from calling `self.model_dump(by_alias=True)` in the following way:

        - Fields with a value of `None` are included in the output only if they are nullable and
          were explicitly set during model initialization. All other `None` fields are omitted.
        """
        excluded_fields: Set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in configurations (list)
        _items = []
        if self.configurations:
            for _item_configurations in self.configurations:
                if _item_configurations:
                    _items.append(_item_configurations.to_dict())
            _dict["configurations"] = _items
        # set to None if baseline_tagged_snapshot_id (nullable) is None
        # and model_fields_set contains the field
        if (
            self.baseline_tagged_snapshot_id is None
            and "baseline_tagged_snapshot_id" in self.model_fields_set
        ):
            _dict["baseline_tagged_snapshot_id"] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """
        Create an instance of the model from a dictionary.

        This method deserializes a dictionary into a model instance. The input should use
        field aliases where applicable.

        :param obj: Dictionary representing the model.
        :type obj: Optional[Dict[str, Any]]
        """
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "id": obj.get("id"),
                "created": obj.get("created"),
                "created_by_id": obj.get("created_by_id"),
                "name": obj.get("name"),
                "description": obj.get("description"),
                "archive_status": obj.get("archive_status"),
                "configurations": [
                    SystemConfiguration.from_dict(_item)
                    for _item in obj["configurations"]
                ]
                if obj.get("configurations") is not None
                else None,
                "baseline_tagged_snapshot_id": obj.get("baseline_tagged_snapshot_id"),
            }
        )
        return _obj
