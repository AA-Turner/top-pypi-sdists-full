from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr, StrictBool
from typing import Any, ClassVar, Dict, List, Optional, Set
from typing_extensions import Self

from istari_digital_client.legacy.v2.models.token import Token
from istari_digital_client.legacy.v2.models.readable import Readable
from istari_digital_client.legacy.mixin import ClientHaving


class SnapshotRevisionSearchItem(BaseModel, ClientHaving, Readable):
    """
    SnapshotRevisionSearchItem

    Represents a searchable snapshot revision entry. This includes a token for the
    content and a separate token for metadata properties. The item may be partially
    resolved (e.g. only includes IDs and tokens) and supports methods for reading
    its raw byte content via the associated client.
    """

    revision_id: StrictStr
    file_id: Optional[StrictStr]
    content_token: Token
    properties_token: Token
    created: datetime
    has_artifacts: bool = False
    name: Optional[StrictStr] = None
    extension: Optional[StrictStr] = None
    size: Optional[StrictInt] = None
    description: Optional[StrictStr] = None
    mime: Optional[StrictStr] = None
    version_name: Optional[StrictStr] = None
    external_identifier: Optional[StrictStr] = None
    display_name: Optional[StrictStr] = None
    schema_version: Optional[StrictStr] = None
    created_by_id: Optional[StrictStr] = None
    is_archived: Optional[StrictBool] = False
    resource_id: Optional[StrictStr] = None
    resource_type: Optional[StrictStr] = None
    tenant_id: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = [
        "revision_id",
        "file_id",
        "content_token",
        "properties_token",
        "created",
        "has_artifacts",
        "name",
        "extension",
        "size",
        "description",
        "mime",
        "version_name",
        "external_identifier",
        "display_name",
        "schema_version",
        "created_by_id",
        "is_archived",
        "resource_id",
        "resource_type",
        "tenant_id",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def read_bytes(self) -> bytes:
        """
        Read the byte contents associated with this snapshot.

        This uses the ``content_token`` to retrieve the binary content
        via the client API.

        :raises ValueError: If the client is not set.
        """
        if self._should_use_cache():
            return self._filesystem_caching_read_bytes()

        return self.read_contents()

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
        # override the default output from pydantic by calling `to_dict()` of content_token
        if self.content_token:
            _dict["content_token"] = self.content_token.to_dict()
        # override the default output from pydantic by calling `to_dict()` of properties_token
        if self.properties_token:
            _dict["properties_token"] = self.properties_token.to_dict()
        # set to None if file_id (nullable) is None
        # and model_fields_set contains the field
        if self.file_id is None and "file_id" in self.model_fields_set:
            _dict["file_id"] = None

        # set to None if name (nullable) is None
        # and model_fields_set contains the field
        if self.name is None and "name" in self.model_fields_set:
            _dict["name"] = None

        # set to None if extension (nullable) is None
        # and model_fields_set contains the field
        if self.extension is None and "extension" in self.model_fields_set:
            _dict["extension"] = None

        # set to None if size (nullable) is None
        # and model_fields_set contains the field
        if self.size is None and "size" in self.model_fields_set:
            _dict["size"] = None

        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict["description"] = None

        # set to None if mime (nullable) is None
        # and model_fields_set contains the field
        if self.mime is None and "mime" in self.model_fields_set:
            _dict["mime"] = None

        # set to None if version_name (nullable) is None
        # and model_fields_set contains the field
        if self.version_name is None and "version_name" in self.model_fields_set:
            _dict["version_name"] = None

        # set to None if external_identifier (nullable) is None
        # and model_fields_set contains the field
        if (
            self.external_identifier is None
            and "external_identifier" in self.model_fields_set
        ):
            _dict["external_identifier"] = None

        # set to None if display_name (nullable) is None
        # and model_fields_set contains the field
        if self.display_name is None and "display_name" in self.model_fields_set:
            _dict["display_name"] = None

        # set to None if schema_version (nullable) is None
        # and model_fields_set contains the field
        if self.schema_version is None and "schema_version" in self.model_fields_set:
            _dict["schema_version"] = None

        # set to None if created_by_id (nullable) is None
        # and model_fields_set contains the field
        if self.created_by_id is None and "created_by_id" in self.model_fields_set:
            _dict["created_by_id"] = None

        # set to None if resource_id (nullable) is None
        # and model_fields_set contains the field
        if self.resource_id is None and "resource_id" in self.model_fields_set:
            _dict["resource_id"] = None

        # set to None if resource_type (nullable) is None
        # and model_fields_set contains the field
        if self.resource_type is None and "resource_type" in self.model_fields_set:
            _dict["resource_type"] = None

        # set to None if tenant_id (nullable) is None
        # and model_fields_set contains the field
        if self.tenant_id is None and "tenant_id" in self.model_fields_set:
            _dict["tenant_id"] = None

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
                "content_token": Token.from_dict(obj["content_token"])
                if obj.get("content_token") is not None
                else None,
                "properties_token": Token.from_dict(obj["properties_token"])
                if obj.get("properties_token") is not None
                else None,
                "created": obj.get("created"),
                "has_artifacts": obj.get("has_artifacts"),
                "name": obj.get("name"),
                "extension": obj.get("extension"),
                "size": obj.get("size"),
                "description": obj.get("description"),
                "mime": obj.get("mime"),
                "version_name": obj.get("version_name"),
                "external_identifier": obj.get("external_identifier"),
                "display_name": obj.get("display_name"),
                "schema_version": obj.get("schema_version"),
                "created_by_id": obj.get("created_by_id"),
                "is_archived": obj.get("is_archived")
                if obj.get("is_archived") is not None
                else False,
                "resource_id": obj.get("resource_id"),
                "resource_type": obj.get("resource_type"),
                "tenant_id": obj.get("tenant_id"),
            }
        )
        return _obj
