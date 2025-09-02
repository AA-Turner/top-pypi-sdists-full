from . import TimestampValidationMixin, UpdateableMixin
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Any, ClassVar, TypeVar, Type, Dict, Optional
from bson import ObjectId
from ...models.utils.types import StrObjectId
from ...models.utils.types.serializer_type import SerializerType
import logging
import json
from datetime import datetime
from zoneinfo import ZoneInfo
# Create and configure logger
logger = logging.getLogger("chatty_asset_model")

T = TypeVar('T', bound='ChattyAssetModel')

class ChattyAssetPreview(TimestampValidationMixin, BaseModel):
    """
    This is a preview of a ChattyAssetModel.
    It's used for listing methods that doesn't require all the data of the asset.
    It's used for frequently accessed assets like Tags, Fast Answers, Products, that don't need pagination.
    """
    id: StrObjectId = Field(frozen=True, alias="_id")
    name: str
    company_id: StrObjectId = Field(frozen=True)
    created_at: datetime
    deleted_at: Optional[datetime] = Field(default=None)

    model_config = ConfigDict(
        populate_by_name=True
                )

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return {
            "_id": 1,
            "name": 1,
            "created_at": 1,
            "company_id": 1,
            "deleted_at": 1
        }

    @classmethod
    def not_found(cls, id: StrObjectId, company_id: StrObjectId) -> 'ChattyAssetPreview':
        return cls(
            _id=id,
            name=f"Not found {id}",
            company_id=company_id,
            created_at=datetime.now(tz=ZoneInfo("UTC")),
            updated_at=datetime.now(tz=ZoneInfo("UTC")),
            deleted_at=datetime.now(tz=ZoneInfo("UTC"))
        )

    @classmethod
    def from_dict(cls, data: dict) -> 'ChattyAssetPreview':
        return cls(**data)

    @classmethod
    def from_asset(cls, asset: 'CompanyAssetModel') -> 'ChattyAssetPreview':
        return cls(
            _id=asset.id,
            name=getattr(asset, "name", "no name"),
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            deleted_at=asset.deleted_at
        )

class ChattyAssetModel(TimestampValidationMixin, UpdateableMixin, BaseModel):
    id: StrObjectId = Field(alias="_id", default_factory=lambda: str(ObjectId()), frozen=True)
    exclude_fields: ClassVar[dict[SerializerType, set[str]]] = {}
    preview_class: ClassVar[Optional[type[ChattyAssetPreview]]] = None
    description: Optional[str] = Field(default=None, description="Description of the asset that could be used as context for Chatty AI agents")
    model_config = ConfigDict(
        populate_by_name=True)

    @property
    def identifier(self) -> StrObjectId:
        return self.id

    @property
    def ID(self) -> StrObjectId:
        return self.id

    def __eq__(self, other: 'ChattyAssetModel') -> bool:
        return self.id == other.id


    def __hash__(self) -> int:
        return hash(self.id)

    def __lt__(self, other: 'ChattyAssetModel') -> bool:
        return self.created_at < other.created_at

    def __gt__(self, other: 'ChattyAssetModel') -> bool:
        return self.created_at > other.created_at

    @classmethod
    def default_create_instance_method(cls: Type[T], data: dict) -> T:
        return cls(**data)

    def model_dump(
        self,
        *args,
        serializer: SerializerType = SerializerType.API,
        **kwargs
    ) -> dict[str, Any]:
        # Get fields to exclude for this serializer type
        exclude = self.exclude_fields.get(serializer, set())

        # Add exclude to kwargs if not present, or update existing exclude
        if 'exclude' in kwargs:
            if isinstance(kwargs['exclude'], set):
                kwargs['exclude'].update(exclude)
            else:
                kwargs['exclude'] = exclude
        else:
            kwargs['exclude'] = exclude

        kwargs["by_alias"] = True
        data = super().model_dump(*args, **kwargs)
        ordered_data = {}

        # Handle id/_id field based on serializer type
        id_value = data.pop('_id')
        if serializer == SerializerType.FRONTEND_ASSET_PREVIEW or serializer == SerializerType.FRONTEND:
            ordered_data['id'] = id_value
        elif serializer == SerializerType.DATABASE:
            ordered_data['_id'] = ObjectId(id_value) if isinstance(id_value, str) else id_value
        else:  # API and other cases
            ordered_data['_id'] = id_value

        # Handle name field if present
        if 'name' in data:
            ordered_data['name'] = data.pop('name')

        # Add remaining fields
        ordered_data.update(data)
        return ordered_data

    def model_dump_json(
        self,
        *args,
        serializer: SerializerType = SerializerType.API,  # Default to API for JSON
        **kwargs
    ) -> Dict[str, Any]:
        # Just add serializer to kwargs and let parent handle the JSON conversion
        ordered_data = {}
        dumped_json = super().model_dump_json(*args, exclude=self.exclude_fields.get(serializer, set()), **kwargs)
        loaded_json = json.loads(dumped_json)
        if serializer == SerializerType.FRONTEND or serializer == SerializerType.FRONTEND_ASSET_PREVIEW:
            loaded_json["id"] = self.id
            loaded_json.pop("_id", None)
        if serializer == SerializerType.DATABASE:
            id = loaded_json.pop("_id", None)
            if not id:
                id = loaded_json.pop("id", None)
            loaded_json["_id"] = ObjectId(id)
            loaded_json["created_at"] = datetime.fromisoformat(loaded_json["created_at"])
            loaded_json["updated_at"] = datetime.fromisoformat(loaded_json["updated_at"])
            loaded_json["deleted_at"] = datetime.fromisoformat(loaded_json["deleted_at"]) if loaded_json["deleted_at"] else None
            if loaded_json.get("start_time"):
                loaded_json["start_time"] = datetime.fromisoformat(loaded_json["start_time"])
            if loaded_json.get("end_time"):
                loaded_json["end_time"] = datetime.fromisoformat(loaded_json["end_time"])

        ordered_data["name"] = loaded_json.pop("name", None)
        ordered_data.update(loaded_json)
        return ordered_data

class CompanyAssetModel(ChattyAssetModel):
    company_id: StrObjectId = Field(frozen=True)
