from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Set, TYPE_CHECKING
from typing_extensions import Self

from istari_digital_client.legacy.v2.models.control_tag import ControlTag
from istari_digital_client.legacy.v2.models.file_archive_status import FileArchiveStatus
from istari_digital_client.legacy.v2.models.file_revision import FileRevision
from istari_digital_client.legacy.v2.models.file_revision_having import FileRevisionHaving
from istari_digital_client.legacy.v2.models.shareable import Shareable
from istari_digital_client.legacy.v2.models.archivable import Archivable
from istari_digital_client.legacy.mixin import ClientHaving
from istari_digital_client.legacy.v2.models.upstream_remote_info import UpstreamRemoteInfo
from istari_digital_client.legacy.v2.models.infosec_level import InfosecLevel
from istari_digital_client.legacy.log_utils import log_method

if TYPE_CHECKING:
    from istari_digital_client.legacy.v2.api.v2_api import Resource


class File(FileRevisionHaving, ClientHaving, Shareable, Archivable):
    """
    Represents a file and its associated metadata, revisions, and archive status.

    Provides convenience methods for retrieving the current revision, linked resource,
    and for updating descriptive properties. Inherits functionality for archiving,
    sharing, and revision access.
    """

    id: StrictStr
    created: datetime
    revisions: List[FileRevision]
    archive_status_history: List[FileArchiveStatus]
    resource_id: Optional[StrictStr] = None
    resource_type: Optional[StrictStr] = None
    created_by_id: Optional[StrictStr] = None
    control_tags: Optional[List[ControlTag]] = None
    updated: Optional[datetime] = None
    upstream_remote_info: Optional[UpstreamRemoteInfo] = None
    infosec_level: Optional[InfosecLevel] = None
    __client_fields__: ClassVar[List[str]] = ["revisions"]
    __properties: ClassVar[List[str]] = [
        "id",
        "created",
        "revisions",
        "archive_status_history",
        "resource_id",
        "resource_type",
        "created_by_id",
        "updated",
        "upstream_remote_info",
        "infosec_level",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
        arbitrary_types_allowed=True,
    )

    @property
    @log_method
    def revision(self) -> FileRevision:
        """
        Get the latest file revision.

        This is the most recently added item in the ``revisions`` list.
        """

        return self.revisions[-1]

    @property
    @log_method
    def resource(self) -> "Resource":
        """
        Retrieve the resource that this file is attached to.

        Requires that ``client``, ``resource_id``, and ``resource_type`` are all set.

        :raises ValueError: If any of the required values are missing.
        """

        if self.client is None:
            raise ValueError("client is not set")
        if self.resource_id is None:
            raise ValueError("resource_id is not set")
        if self.resource_type is None:
            raise ValueError("resource_type is not set")
        return self.client.get_resource(self.resource_type, self.resource_id)

    @property
    @log_method
    def archive_status(self) -> FileArchiveStatus:
        """
        Get the current archive status of the file.

        This is derived from the last entry in the ``archive_status_history`` list.
        """

        return self.archive_status_history[-1]

    @log_method
    def update_properties(
        self,
        description: Optional[str] = None,
        display_name: Optional[str] = None,
        external_identifier: Optional[str] = None,
        version_name: Optional[str] = None,
    ) -> "File":
        """
        Update one or more metadata properties for the latest file revision.

        This method delegates to the SDK client to update properties such as
        ``description``, ``display_name``, ``external_identifier``, and ``version_name``.

        :param description: Optional description for the file.
        :type description: str or None
        :param display_name: Optional human-readable name.
        :type display_name: str or None
        :param external_identifier: Optional external system reference.
        :type external_identifier: str or None
        :param version_name: Optional version label.
        :type version_name: str or None
        :raises ValueError: If the client is not set.
        """

        if self.client is None:
            raise ValueError("client is not set")

        return self.client.update_revision_properties(
            self.revision,
            description=description,
            display_name=display_name,
            external_identifier=external_identifier,
            version_name=version_name,
        )

    @log_method
    def update_description(self, description: str) -> "File":
        """
        Update the file’s description.

        :param description: The new description to apply.
        :type description: str
        """

        return self.update_properties(
            description=description,
        )

    @log_method
    def update_display_name(self, display_name: str) -> "File":
        """
        Update the file’s display name.

        :param display_name: The new display name to apply.
        :type display_name: str
        """

        return self.update_properties(
            display_name=display_name,
        )

    @log_method
    def update_external_identifier(self, external_identifier: str) -> "File":
        """
        Update the file’s external identifier.

        :param external_identifier: The new external identifier to apply.
        :type external_identifier: str
        """

        return self.update_properties(
            external_identifier=external_identifier,
        )

    @log_method
    def update_version_name(self, version_name: str) -> "File":
        """
        Update the file’s version name.

        :param version_name: The new version name to apply.
        :type version_name: str
        """

        return self.update_properties(
            version_name=version_name,
        )

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
        # override the default output from pydantic by calling `to_dict()` of each item in revisions (list)
        _items = []
        if self.revisions:
            for _item_revisions in self.revisions:
                if _item_revisions:
                    _items.append(_item_revisions.to_dict())
            _dict["revisions"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in archive_status_history (list)
        _items = []
        if self.archive_status_history:
            for _item_archive_status_history in self.archive_status_history:
                if _item_archive_status_history:
                    _items.append(_item_archive_status_history.to_dict())
            _dict["archive_status_history"] = _items
        # set to None if resource_id (nullable) is None
        # and model_fields_set contains the field
        if self.resource_id is None and "resource_id" in self.model_fields_set:
            _dict["resource_id"] = None

        # set to None if resource_type (nullable) is None
        # and model_fields_set contains the field
        if self.resource_type is None and "resource_type" in self.model_fields_set:
            _dict["resource_type"] = None

        # set to None if created_by_id (nullable) is None
        # and model_fields_set contains the field
        if self.created_by_id is None and "created_by_id" in self.model_fields_set:
            _dict["created_by_id"] = None

        # set to None if updated (nullable) is None
        # and model_fields_set contains the field
        if self.updated is None and "updated" in self.model_fields_set:
            _dict["updated"] = None

        # set to None if upstream_remote_info (nullable) is None
        # and model_fields_set contains the field
        if (
            self.upstream_remote_info is None
            and "upstream_remote_info" in self.model_fields_set
        ):
            _dict["upstream_remote_info"] = None
        # set to None if infosec_level (nullable) is None
        # and model_fields_set contains the field
        if self.infosec_level is None and "infosec_level" in self.model_fields_set:
            _dict["infosec_level"] = None

        # override the default output from pydantic by calling `to_dict()` of each item in control_tags (list)
        _items = []
        if self.control_tags:
            for _item_control_tags in self.control_tags:
                if _item_control_tags:
                    _items.append(_item_control_tags.to_dict())
            _dict["control_tags"] = _items
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
                "revisions": [
                    FileRevision.from_dict(_item) for _item in obj["revisions"]
                ]
                if obj.get("revisions") is not None
                else None,
                "archive_status_history": [
                    FileArchiveStatus.from_dict(_item)
                    for _item in obj["archive_status_history"]
                ]
                if obj.get("archive_status_history") is not None
                else None,
                "resource_id": obj.get("resource_id"),
                "resource_type": obj.get("resource_type"),
                "created_by_id": obj.get("created_by_id"),
                "control_tags": [
                    ControlTag.from_dict(_item) for _item in obj["control_tags"]
                ]
                if obj.get("control_tags") is not None
                else None,
                "updated": obj.get("updated", None)
                if obj.get("updated") is not None
                else None,
                "upstream_remote_info": UpstreamRemoteInfo.from_dict(
                    obj["upstream_remote_info"]
                )
                if obj.get("upstream_remote_info") is not None
                else None,
                "infosec_level": InfosecLevel.from_dict(obj["infosec_level"])
                if obj.get("infosec_level") is not None
                else None,
            }
        )
        return _obj
