from __future__ import annotations
import pprint
import re  # noqa: F401
import json
import uuid
import logging
from pathlib import Path
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr
from typing import Any, Dict, List, Optional, Set, TYPE_CHECKING, ClassVar
from typing_extensions import Self

from istari_digital_client.legacy.v2.models.properties import Properties
from istari_digital_client.legacy.v2.models.file_revision_archive_status import (
    FileRevisionArchiveStatus,
)
from istari_digital_client.legacy.v2.models.archive_status_name import ArchiveStatusName
from istari_digital_client.legacy.v2.models.product import Product
from istari_digital_client.legacy.v2.models.source import Source
from istari_digital_client.legacy.v2.models.token import Token
from istari_digital_client.legacy.v2.models.readable import Readable
from istari_digital_client.legacy.v2.models.archivable import Archivable
from istari_digital_client.legacy.mixin import ClientHaving
from istari_digital_client.legacy.log_utils import log_method

import istari_digital_core

if TYPE_CHECKING:
    from istari_digital_client.legacy.v2.models.file import File
    from istari_digital_client.legacy.v2.api.v2_api import Resource

logger = logging.getLogger("istari-digital-client.token_reader")


class FileRevision(BaseModel, ClientHaving, Readable, Archivable):
    """
    Represents a single revision of a file.

    A `FileRevision` encapsulates the file's metadata, content access tokens,
    archive status, and optional links to sources and products. It supports reading
    the file's contents and retrieving associated metadata with optional filesystem
    caching.
    """

    id: StrictStr
    created: datetime
    file_id: Optional[StrictStr]
    content_token: Token
    properties_token: Token
    archive_status_history: List[FileRevisionArchiveStatus]
    name: Optional[StrictStr] = None
    stem: Optional[StrictStr] = None
    suffix: Optional[StrictStr] = None
    extension: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    size: Optional[StrictInt] = None
    mime: Optional[StrictStr] = None
    version_name: Optional[StrictStr] = None
    external_identifier: Optional[StrictStr] = None
    display_name: Optional[StrictStr] = None
    sources: Optional[List[Source]] = None
    products: Optional[List[Product]] = None
    created_by_id: Optional[StrictStr] = None
    updated: Optional[datetime] = None

    __client_fields__: ClassVar[List[str]] = ["sources", "products"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
        arbitrary_types_allowed=True,
    )

    def __post_init__(self):
        self.stem = Path(self.name).stem if self.name else None
        self.suffix = Path(self.name).suffix if self.name else None

    def read_bytes(self) -> bytes:
        if self._should_use_cache():
            return self._filesystem_caching_read_bytes()

        return self.read_contents()

    @property
    def properties(self) -> Properties:
        return self.read_properties()

    @property
    @log_method
    def file(self) -> Optional["File"]:
        """
        Retrieve the file this revision belongs to.

        :raises ReadError: If ``file_id`` or ``client`` is not set.
        """

        if self.file_id is None:
            raise ValueError("File ID is not set")
        if self.client is None:
            raise ValueError("Client is not set")
        return self.client.get_file(self.file_id)

    @property
    @log_method
    def resource(self) -> Optional["Resource"]:
        """
        Retrieve the resource this revision is indirectly linked to through its file.

        Returns ``None`` if any of ``client``, ``file``, ``resource_id``, or ``resource_type`` is missing.
        """

        file = self.file
        if (
            file is None
            or self.client is None
            or file.resource_type is None
            or file.resource_id is None
        ):
            return None

        return self.client.get_resource(file.resource_type, file.resource_id)

    @log_method
    def source_revision_ids(self) -> Optional[list[str]]:
        """
        Return a list of revision IDs from the sources associated with this revision.

        Returns ``None`` if no sources are present.
        """

        if not self.sources:
            return None
        return [source.revision_id for source in self.sources]

    @log_method
    def source_product_ids(self) -> Optional[list[str]]:
        """
        Return a list of revision IDs from the products associated with this revision.

        Returns ``None`` if no products are present.
        """

        if not self.products:
            return None
        return [product.revision_id for product in self.products]

    @property
    @log_method
    def archive_status(self) -> FileRevisionArchiveStatus:
        """
        Get the current archive status of this revision.

        This is the last entry in the ``archive_status_history`` list.
        """

        return self.archive_status_history[-1]

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
        # override the default output from pydantic by calling `to_dict()` of each item in archive_status_history (list)
        _items = []
        if self.archive_status_history:
            for _item_archive_status_history in self.archive_status_history:
                if _item_archive_status_history:
                    _items.append(_item_archive_status_history.to_dict())
            _dict["archive_status_history"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in sources (list)
        _items = []
        if self.sources:
            for _item_sources in self.sources:
                if _item_sources:
                    _items.append(_item_sources.to_dict())
            _dict["sources"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in products (list)
        _items = []
        if self.products:
            for _item_products in self.products:
                if _item_products:
                    _items.append(_item_products.to_dict())
            _dict["products"] = _items
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

        # set to None if created_by_id (nullable) is None
        # and model_fields_set contains the field
        if self.created_by_id is None and "created_by_id" in self.model_fields_set:
            _dict["created_by_id"] = None

        # set to None if updated (nullable) is None
        # and model_fields_set contains the field
        if self.updated is None and "updated" in self.model_fields_set:
            _dict["updated"] = None

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
                "file_id": obj.get("file_id"),
                "content_token": Token.from_dict(obj["content_token"])
                if obj.get("content_token") is not None
                else None,
                "properties_token": Token.from_dict(obj["properties_token"])
                if obj.get("properties_token") is not None
                else None,
                "archive_status_history": [
                    FileRevisionArchiveStatus.from_dict(_item)
                    for _item in obj["archive_status_history"]
                ]
                if obj.get("archive_status_history") is not None
                else None,
                "name": obj.get("name"),
                "extension": obj.get("extension"),
                "size": obj.get("size"),
                "description": obj.get("description"),
                "mime": obj.get("mime"),
                "version_name": obj.get("version_name"),
                "external_identifier": obj.get("external_identifier"),
                "display_name": obj.get("display_name"),
                "sources": [Source.from_dict(_item) for _item in obj["sources"]]
                if obj.get("sources") is not None
                else None,
                "products": [Product.from_dict(_item) for _item in obj["products"]]
                if obj.get("products") is not None
                else None,
                "created_by_id": obj.get("created_by_id"),
                "updated": obj.get("updated")
                if obj.get("updated") is not None
                else None,
            }
        )
        _obj.stem = Path(_obj.name).stem if _obj.name else None
        _obj.suffix = Path(_obj.name).suffix if _obj.name else None

        return _obj

    @classmethod
    def from_storage_revision(
        cls,
        storage_revision: istari_digital_core.Revision,
        sources: Optional[List[Source]],
    ) -> Self:
        """
        Create a ``FileRevision`` from a core storage-layer revision.

        :param storage_revision: A storage-layer revision object from ``istari_digital_core``.
        :type storage_revision: istari_digital_core.Revision
        :param sources: Optional list of sources associated with this revision.
        :type sources: list[Source] or None
        """

        file_revision_id = str(uuid.uuid4())

        file_revision_archive_status = FileRevisionArchiveStatus(
            id=str(uuid.uuid4()),
            created=datetime.now(timezone.utc),
            name=ArchiveStatusName.ACTIVE,
            reason="Initial",
            created_by_id=None,
            file_revision_id=file_revision_id,
        )

        return cls(
            id=file_revision_id,
            created=datetime.now(timezone.utc),
            file_id=None,
            content_token=Token.from_storage_token(storage_revision.content_token),
            properties_token=Token.from_storage_token(
                storage_revision.properties_token
            ),
            archive_status_history=[file_revision_archive_status],
            name=storage_revision.properties.file_name,
            extension=storage_revision.properties.extension,
            size=storage_revision.properties.size,
            description=storage_revision.properties.description,
            mime=storage_revision.properties.mime,
            version_name=storage_revision.properties.version_name,
            external_identifier=storage_revision.properties.external_identifier,
            display_name=storage_revision.properties.display_name,
            sources=sources,
            products=None,
            created_by_id=None,
            updated=None,
        )
