from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Set, TYPE_CHECKING
from typing_extensions import Self

from istari_digital_client.legacy.v2.models.comment import Comment
from istari_digital_client.legacy.v2.models.file import File
from istari_digital_client.legacy.v2.models.function_auth_type import FunctionAuthType
from istari_digital_client.legacy.v2.models.resource_archive_status import (
    ResourceArchiveStatus,
)
from istari_digital_client.legacy.v2.models.file_having import FileHaving
from istari_digital_client.legacy.mixin import ClientHaving
from istari_digital_client.legacy.log_utils import log_method


class FunctionAuthSecret(FileHaving, ClientHaving):
    """
    Represents a function authentication secret backed by a file.

    A `FunctionAuthSecret` contains metadata and secret file content used for authentication
    (e.g., bearer tokens, API keys). It includes optional identifiers, expiration, and audit fields.
    """

    id: StrictStr
    created: datetime
    file: File
    comments: List[Comment]
    archive_status_history: List[ResourceArchiveStatus]
    created_by_id: StrictStr
    function_auth_type: FunctionAuthType
    sha: Optional[StrictStr] = None
    salt: Optional[StrictStr] = None
    auth_integration_id: Optional[StrictStr] = None
    expiration: Optional[datetime] = None
    __client_fields__: ClassVar[List[str]] = ["file", "comments"]
    __properties: ClassVar[List[str]] = [
        "id",
        "created",
        "file",
        "comments",
        "archive_status_history",
        "created_by_id",
        "auth_integration_id",
        "function_auth_type",
        "sha",
        "salt",
        "expiration",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    @log_method
    def to_str(self) -> str:
        """
        Return the string representation of the model using field aliases.

        This method serializes the model to a JSON-formatted string, respecting any defined aliases
        for fields instead of their original attribute names.
        """
        return pprint.pformat(self.model_dump(by_alias=True))

    @log_method
    def to_json(self) -> str:
        """
        Return the JSON string representation of the model using field aliases.

        This method serializes the model into a JSON-formatted string, using aliases for field names
        where defined instead of their raw attribute names.
        """
        return json.dumps(self.to_dict())

    @classmethod
    @log_method
    def from_json(cls, json_str: str) -> Optional[Self]:
        """
        Create an instance of the model from a JSON string.

        This method deserializes the given JSON string into a model instance. It expects the
        string to match the model's schema, using field aliases where applicable.

        :param json_str: JSON string representing the model.
        :type json_str: str
        """
        return cls.from_dict(json.loads(json_str))

    @log_method
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
        # override the default output from pydantic by calling `to_dict()` of file
        if self.file:
            _dict["file"] = self.file.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in comments (list)
        _items = []
        if self.comments:
            for _item_comments in self.comments:
                if _item_comments:
                    _items.append(_item_comments.to_dict())
            _dict["comments"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in archive_status_history (list)
        _items = []
        if self.archive_status_history:
            for _item_archive_status_history in self.archive_status_history:
                if _item_archive_status_history:
                    _items.append(_item_archive_status_history.to_dict())
            _dict["archive_status_history"] = _items
        # set to None if expiration (nullable) is None
        # and model_fields_set contains the field
        if self.expiration is None and "expiration" in self.model_fields_set:
            _dict["expiration"] = None

        return _dict

    @classmethod
    @log_method
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
                "file": File.from_dict(obj["file"])
                if obj.get("file") is not None
                else None,
                "comments": [Comment.from_dict(_item) for _item in obj["comments"]]
                if obj.get("comments") is not None
                else None,
                "archive_status_history": [
                    ResourceArchiveStatus.from_dict(_item)
                    for _item in obj["archive_status_history"]
                ]
                if obj.get("archive_status_history") is not None
                else None,
                "created_by_id": obj.get("created_by_id"),
                "auth_integration_id": obj.get("auth_integration_id"),
                "function_auth_type": obj.get("function_auth_type"),
                "sha": obj.get("sha"),
                "salt": obj.get("salt"),
                "expiration": obj.get("expiration"),
            }
        )
        return _obj
