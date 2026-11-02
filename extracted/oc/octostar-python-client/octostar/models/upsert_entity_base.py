from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    Tuple,
    Optional,
    BinaryIO,
    TextIO,
    TYPE_CHECKING,
)

from typing import List


import attr

from ..types import UNSET, Unset

from typing import Union
from ..types import UNSET, Unset


T = TypeVar("T", bound="UpsertEntityBase")


@attr.s(auto_attribs=True)
class UpsertEntityBase:
    """
    ### Attributes:
    * `entity_id (Union[Unset, str])`: None
    * `entity_type (Union[Unset, str])`: None
    * `entity_label (Union[Unset, str])`: None
    * `os_item_content_type (Union[Unset, str])`: None
    * `os_last_updated_by (Union[Unset, str])`: None
    * `os_workspace (Union[Unset, str])`: None
    * `os_deleted_at (Union[Unset, str])`: None
    * `os_parent_folder (Union[Unset, str])`: None
    * `os_deleted_by (Union[Unset, str])`: None
    * `os_icon (Union[Unset, str])`: None
    * `description (Union[Unset, str])`: None
    * `os_textsearchfield (Union[Unset, str])`: None
    * `os_item_content (Union[Unset, str])`: None
    * `os_last_updated_at (Union[Unset, str])`: None
    * `os_item_type (Union[Unset, str])`: None
    * `os_hidden_at (Union[Unset, str])`: None
    * `os_hidden_by (Union[Unset, str])`: None
    * `os_entity_uid (Union[Unset, str])`: None
    * `os_file_pointer (Union[Unset, str])`: None
    * `os_custom_icon (Union[Unset, str])`: None
    * `os_created_by (Union[Unset, str])`: None
    * `os_concept (Union[Unset, str])`: None
    * `os_created_at (Union[Unset, str])`: None
    * `os_item_name (Union[Unset, str])`: None
    * `concept_name (Union[Unset, str])`: None
    """

    entity_id: Union[Unset, str] = UNSET
    entity_type: Union[Unset, str] = UNSET
    entity_label: Union[Unset, str] = UNSET
    os_item_content_type: Union[Unset, str] = UNSET
    os_last_updated_by: Union[Unset, str] = UNSET
    os_workspace: Union[Unset, str] = UNSET
    os_deleted_at: Union[Unset, str] = UNSET
    os_parent_folder: Union[Unset, str] = UNSET
    os_deleted_by: Union[Unset, str] = UNSET
    os_icon: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    os_textsearchfield: Union[Unset, str] = UNSET
    os_item_content: Union[Unset, str] = UNSET
    os_last_updated_at: Union[Unset, str] = UNSET
    os_item_type: Union[Unset, str] = UNSET
    os_hidden_at: Union[Unset, str] = UNSET
    os_hidden_by: Union[Unset, str] = UNSET
    os_entity_uid: Union[Unset, str] = UNSET
    os_file_pointer: Union[Unset, str] = UNSET
    os_custom_icon: Union[Unset, str] = UNSET
    os_created_by: Union[Unset, str] = UNSET
    os_concept: Union[Unset, str] = UNSET
    os_created_at: Union[Unset, str] = UNSET
    os_item_name: Union[Unset, str] = UNSET
    concept_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entity_id = self.entity_id
        entity_type = self.entity_type
        entity_label = self.entity_label
        os_item_content_type = self.os_item_content_type
        os_last_updated_by = self.os_last_updated_by
        os_workspace = self.os_workspace
        os_deleted_at = self.os_deleted_at
        os_parent_folder = self.os_parent_folder
        os_deleted_by = self.os_deleted_by
        os_icon = self.os_icon
        description = self.description
        os_textsearchfield = self.os_textsearchfield
        os_item_content = self.os_item_content
        os_last_updated_at = self.os_last_updated_at
        os_item_type = self.os_item_type
        os_hidden_at = self.os_hidden_at
        os_hidden_by = self.os_hidden_by
        os_entity_uid = self.os_entity_uid
        os_file_pointer = self.os_file_pointer
        os_custom_icon = self.os_custom_icon
        os_created_by = self.os_created_by
        os_concept = self.os_concept
        os_created_at = self.os_created_at
        os_item_name = self.os_item_name
        concept_name = self.concept_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if entity_id is not UNSET:
            field_dict["entity_id"] = entity_id
        if entity_type is not UNSET:
            field_dict["entity_type"] = entity_type
        if entity_label is not UNSET:
            field_dict["entity_label"] = entity_label
        if os_item_content_type is not UNSET:
            field_dict["os_item_content_type"] = os_item_content_type
        if os_last_updated_by is not UNSET:
            field_dict["os_last_updated_by"] = os_last_updated_by
        if os_workspace is not UNSET:
            field_dict["os_workspace"] = os_workspace
        if os_deleted_at is not UNSET:
            field_dict["os_deleted_at"] = os_deleted_at
        if os_parent_folder is not UNSET:
            field_dict["os_parent_folder"] = os_parent_folder
        if os_deleted_by is not UNSET:
            field_dict["os_deleted_by"] = os_deleted_by
        if os_icon is not UNSET:
            field_dict["os_icon"] = os_icon
        if description is not UNSET:
            field_dict["description"] = description
        if os_textsearchfield is not UNSET:
            field_dict["os_textsearchfield"] = os_textsearchfield
        if os_item_content is not UNSET:
            field_dict["os_item_content"] = os_item_content
        if os_last_updated_at is not UNSET:
            field_dict["os_last_updated_at"] = os_last_updated_at
        if os_item_type is not UNSET:
            field_dict["os_item_type"] = os_item_type
        if os_hidden_at is not UNSET:
            field_dict["os_hidden_at"] = os_hidden_at
        if os_hidden_by is not UNSET:
            field_dict["os_hidden_by"] = os_hidden_by
        if os_entity_uid is not UNSET:
            field_dict["os_entity_uid"] = os_entity_uid
        if os_file_pointer is not UNSET:
            field_dict["os_file_pointer"] = os_file_pointer
        if os_custom_icon is not UNSET:
            field_dict["os_custom_icon"] = os_custom_icon
        if os_created_by is not UNSET:
            field_dict["os_created_by"] = os_created_by
        if os_concept is not UNSET:
            field_dict["os_concept"] = os_concept
        if os_created_at is not UNSET:
            field_dict["os_created_at"] = os_created_at
        if os_item_name is not UNSET:
            field_dict["os_item_name"] = os_item_name
        if concept_name is not UNSET:
            field_dict["concept_name"] = concept_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_id = d.pop("entity_id", UNSET)

        entity_type = d.pop("entity_type", UNSET)

        entity_label = d.pop("entity_label", UNSET)

        os_item_content_type = d.pop("os_item_content_type", UNSET)

        os_last_updated_by = d.pop("os_last_updated_by", UNSET)

        os_workspace = d.pop("os_workspace", UNSET)

        os_deleted_at = d.pop("os_deleted_at", UNSET)

        os_parent_folder = d.pop("os_parent_folder", UNSET)

        os_deleted_by = d.pop("os_deleted_by", UNSET)

        os_icon = d.pop("os_icon", UNSET)

        description = d.pop("description", UNSET)

        os_textsearchfield = d.pop("os_textsearchfield", UNSET)

        os_item_content = d.pop("os_item_content", UNSET)

        os_last_updated_at = d.pop("os_last_updated_at", UNSET)

        os_item_type = d.pop("os_item_type", UNSET)

        os_hidden_at = d.pop("os_hidden_at", UNSET)

        os_hidden_by = d.pop("os_hidden_by", UNSET)

        os_entity_uid = d.pop("os_entity_uid", UNSET)

        os_file_pointer = d.pop("os_file_pointer", UNSET)

        os_custom_icon = d.pop("os_custom_icon", UNSET)

        os_created_by = d.pop("os_created_by", UNSET)

        os_concept = d.pop("os_concept", UNSET)

        os_created_at = d.pop("os_created_at", UNSET)

        os_item_name = d.pop("os_item_name", UNSET)

        concept_name = d.pop("concept_name", UNSET)

        upsert_entity_base = cls(
            entity_id=entity_id,
            entity_type=entity_type,
            entity_label=entity_label,
            os_item_content_type=os_item_content_type,
            os_last_updated_by=os_last_updated_by,
            os_workspace=os_workspace,
            os_deleted_at=os_deleted_at,
            os_parent_folder=os_parent_folder,
            os_deleted_by=os_deleted_by,
            os_icon=os_icon,
            description=description,
            os_textsearchfield=os_textsearchfield,
            os_item_content=os_item_content,
            os_last_updated_at=os_last_updated_at,
            os_item_type=os_item_type,
            os_hidden_at=os_hidden_at,
            os_hidden_by=os_hidden_by,
            os_entity_uid=os_entity_uid,
            os_file_pointer=os_file_pointer,
            os_custom_icon=os_custom_icon,
            os_created_by=os_created_by,
            os_concept=os_concept,
            os_created_at=os_created_at,
            os_item_name=os_item_name,
            concept_name=concept_name,
        )

        upsert_entity_base.additional_properties = d
        return upsert_entity_base

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
