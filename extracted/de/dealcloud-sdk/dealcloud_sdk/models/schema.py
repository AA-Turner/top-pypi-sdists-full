"""Schema models (matching real SDK with Pydantic v2)."""

from html import unescape
from typing import Any, Optional
from pydantic import BaseModel

from ..constants import field_types


class Object(BaseModel):
    """Describes a DealCloud Object."""
    apiName: Optional[str] = None
    singularName: Optional[str] = None
    pluralName: Optional[str] = None
    entryListType: Optional[int] = None
    entryListSubType: Optional[int] = None
    id: Optional[int] = None
    name: Optional[str] = None
    entryListId: Optional[int] = None

    @classmethod
    def from_api(cls, object_data: dict) -> "Object":
        """Unescape HTML characters from API response."""
        unescape_attributes = ["singularName", "pluralName"]
        for attr in unescape_attributes:
            if object_data.get(attr):
                object_data[attr] = unescape(object_data[attr])
        return cls(**object_data)


class ChoiceValue(BaseModel):
    """Describes a DealCloud Choice field value."""
    parentID: Optional[int] = None
    seqNumber: Optional[int] = None
    id: Optional[int] = None
    name: Optional[str] = None
    entryListId: Optional[int] = None


class Field(BaseModel):
    """Describes a DealCloud Field."""
    apiName: Optional[str] = None
    description: Optional[str] = None
    fieldType: Optional[int] = None
    isRequired: Optional[bool] = None
    allowDuplicates: Optional[bool] = None
    warnOnNearDuplicates: Optional[bool] = None
    isMoney: Optional[bool] = None
    isMultiSelect: Optional[bool] = None
    choiceFieldId: Optional[int] = None
    choiceOrder: Optional[int] = None
    entryLists: Optional[list[int]] = None
    systemFieldType: Optional[int] = None
    choiceValues: Optional[list[ChoiceValue]] = None
    isKey: Optional[bool] = None
    isCalculated: Optional[bool] = None
    isAttachment: Optional[bool] = None
    isStoreRequestSupported: Optional[bool] = None
    formula: Optional[str] = None
    id: Optional[int] = None
    name: Optional[str] = None
    entryListId: Optional[int] = None
    choiceMap: Optional[dict] = None

    @classmethod
    def from_api(cls, field_data: dict) -> "Field":
        """Unescape HTML and build choice map from API response."""
        unescape_attributes = ["description", "name", "formula"]
        for attr in unescape_attributes:
            if field_data.get(attr):
                field_data[attr] = unescape(field_data[attr])
        
        field_type = field_data.get("fieldType")
        if field_type and field_data.get("choiceValues"):
            if field_type == field_types.CHOICE:
                choices = field_data.get("choiceValues")
                if choices:
                    field_data["choiceMap"] = {
                        unescape(val.get("name")): val.get("id") 
                        for val in choices
                    }
        
        return cls(**field_data)


class ObjectWithFields(BaseModel):
    """Describes a DealCloud object with associated fields."""
    object: Optional[Object] = None
    fields: Optional[dict[Any, Field]] = None


class Schema(BaseModel):
    """Describes a full DealCloud object/field schema."""
    objects: Optional[dict[Any, ObjectWithFields]] = None


class MappingsType(BaseModel):
    """Describes a DealCloud object mappings type."""
    id: Optional[int] = None
    name: Optional[str] = None
    entryListId: Optional[int] = None


class Mapping(BaseModel):
    """Describes a DealCloud object mapping."""
    id: Optional[int] = None
    name: Optional[str] = None
    entryListId: Optional[int] = None


class FieldUnit(BaseModel):
    """Describes a DealCloud field unit."""
    id: Optional[int] = None
    name: Optional[str] = None


class Timezone(BaseModel):
    """Describes a DealCloud timezone."""
    id: Optional[str] = None
    name: Optional[str] = None
    displayName: Optional[str] = None


class User(BaseModel):
    """Describes a DealCloud User."""
    id: int
    name: str
    email: str
    entryListId: int


