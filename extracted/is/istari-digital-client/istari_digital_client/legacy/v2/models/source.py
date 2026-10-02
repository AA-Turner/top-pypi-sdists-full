from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Set, TYPE_CHECKING
from typing_extensions import Self

from istari_digital_client.legacy.mixin import ClientHaving
from istari_digital_client.legacy.log_utils import log_method

if TYPE_CHECKING:
    from istari_digital_client.legacy.v2.models.file import File
    from istari_digital_client.legacy.v2.api.v2_api import Resource
    from istari_digital_client.legacy.v2.models.file_revision import FileRevision


class Source(BaseModel, ClientHaving):
    """
    Represents an upstream source that contributed to the creation of another resource.

    A Source links a file revision to a target resource such as a model, snapshot, or job.
    It captures the lineage and relationship metadata describing how a particular file
    revision was used during processing or composition.

    This class supports resolution of the original file, its revision, and the associated
    resource, provided that the client is initialized.
    """

    revision_id: StrictStr
    file_id: Optional[StrictStr] = None
    resource_type: Optional[StrictStr] = None
    resource_id: Optional[StrictStr] = None
    relationship_identifier: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = [
        "revision_id",
        "file_id",
        "resource_type",
        "resource_id",
        "relationship_identifier",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    @property
    @log_method
    def file(self) -> Optional["File"]:
        """
        Retrieve the file associated with this source.

        This requires that ``file_id`` is set and that the client is available.
        If either is missing, this returns ``None``.
        """
        if self.file_id is None or self.client is None:
            return None
        return self.client.get_file(self.file_id)

    @property
    @log_method
    def resource(self) -> Optional["Resource"]:
        """
        Retrieve the resource this source was used to support.

        This requires that ``resource_type`` and ``resource_id`` are set,
        and that the client is available. If any of these are missing, this returns ``None``.
        """
        if (
            self.resource_type is None
            or self.resource_id is None
            or self.client is None
        ):
            return None
        return self.client.get_resource(self.resource_type, self.resource_id)

    @property
    @log_method
    def revision(self) -> Optional["FileRevision"]:
        """
        Retrieve the file revision that represents the source content.

        This requires that ``revision_id`` is set and that the client is available.
        If either is missing, this returns ``None``.
        """
        if self.revision_id is None or self.client is None:
            return None
        return self.client.get_revision(self.revision_id)

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
        # set to None if file_id (nullable) is None
        # and model_fields_set contains the field
        if self.file_id is None and "file_id" in self.model_fields_set:
            _dict["file_id"] = None

        # set to None if resource_type (nullable) is None
        # and model_fields_set contains the field
        if self.resource_type is None and "resource_type" in self.model_fields_set:
            _dict["resource_type"] = None

        # set to None if resource_id (nullable) is None
        # and model_fields_set contains the field
        if self.resource_id is None and "resource_id" in self.model_fields_set:
            _dict["resource_id"] = None

        # set to None if relationship_identifier (nullable) is None
        # and model_fields_set contains the field
        if (
            self.relationship_identifier is None
            and "relationship_identifier" in self.model_fields_set
        ):
            _dict["relationship_identifier"] = None

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
                "revision_id": obj.get("revision_id"),
                "file_id": obj.get("file_id"),
                "resource_type": obj.get("resource_type"),
                "resource_id": obj.get("resource_id"),
                "relationship_identifier": obj.get("relationship_identifier"),
            }
        )
        return _obj
