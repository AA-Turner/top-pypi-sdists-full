from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.extended_jobs_jobs_item_type_1_raw_flow_notes_item_type import (
    ExtendedJobsJobsItemType1RawFlowNotesItemType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.extended_jobs_jobs_item_type_1_raw_flow_notes_item_position import (
        ExtendedJobsJobsItemType1RawFlowNotesItemPosition,
    )
    from ..models.extended_jobs_jobs_item_type_1_raw_flow_notes_item_size import (
        ExtendedJobsJobsItemType1RawFlowNotesItemSize,
    )


T = TypeVar("T", bound="ExtendedJobsJobsItemType1RawFlowNotesItem")


@_attrs_define
class ExtendedJobsJobsItemType1RawFlowNotesItem:
    """A sticky note attached to a flow for documentation and annotation

    Attributes:
        id (str): Unique identifier for the note
        text (str): Content of the note
        color (str): Color of the note (e.g., "yellow", "#ffff00")
        type (ExtendedJobsJobsItemType1RawFlowNotesItemType): Type of note - 'free' for standalone notes, 'group' for
            notes that group other nodes
        position (Union[Unset, ExtendedJobsJobsItemType1RawFlowNotesItemPosition]): Position of the note in the flow
            editor
        size (Union[Unset, ExtendedJobsJobsItemType1RawFlowNotesItemSize]): Size of the note in the flow editor
        locked (Union[Unset, bool]): Whether the note is locked and cannot be edited or moved
        contained_node_ids (Union[Unset, List[str]]): For group notes, the IDs of nodes contained within this group
    """

    id: str
    text: str
    color: str
    type: ExtendedJobsJobsItemType1RawFlowNotesItemType
    position: Union[Unset, "ExtendedJobsJobsItemType1RawFlowNotesItemPosition"] = UNSET
    size: Union[Unset, "ExtendedJobsJobsItemType1RawFlowNotesItemSize"] = UNSET
    locked: Union[Unset, bool] = False
    contained_node_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        text = self.text
        color = self.color
        type = self.type.value

        position: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.position, Unset):
            position = self.position.to_dict()

        size: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.size, Unset):
            size = self.size.to_dict()

        locked = self.locked
        contained_node_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.contained_node_ids, Unset):
            contained_node_ids = self.contained_node_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "text": text,
                "color": color,
                "type": type,
            }
        )
        if position is not UNSET:
            field_dict["position"] = position
        if size is not UNSET:
            field_dict["size"] = size
        if locked is not UNSET:
            field_dict["locked"] = locked
        if contained_node_ids is not UNSET:
            field_dict["contained_node_ids"] = contained_node_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.extended_jobs_jobs_item_type_1_raw_flow_notes_item_position import (
            ExtendedJobsJobsItemType1RawFlowNotesItemPosition,
        )
        from ..models.extended_jobs_jobs_item_type_1_raw_flow_notes_item_size import (
            ExtendedJobsJobsItemType1RawFlowNotesItemSize,
        )

        d = src_dict.copy()
        id = d.pop("id")

        text = d.pop("text")

        color = d.pop("color")

        type = ExtendedJobsJobsItemType1RawFlowNotesItemType(d.pop("type"))

        _position = d.pop("position", UNSET)
        position: Union[Unset, ExtendedJobsJobsItemType1RawFlowNotesItemPosition]
        if isinstance(_position, Unset):
            position = UNSET
        else:
            position = ExtendedJobsJobsItemType1RawFlowNotesItemPosition.from_dict(_position)

        _size = d.pop("size", UNSET)
        size: Union[Unset, ExtendedJobsJobsItemType1RawFlowNotesItemSize]
        if isinstance(_size, Unset):
            size = UNSET
        else:
            size = ExtendedJobsJobsItemType1RawFlowNotesItemSize.from_dict(_size)

        locked = d.pop("locked", UNSET)

        contained_node_ids = cast(List[str], d.pop("contained_node_ids", UNSET))

        extended_jobs_jobs_item_type_1_raw_flow_notes_item = cls(
            id=id,
            text=text,
            color=color,
            type=type,
            position=position,
            size=size,
            locked=locked,
            contained_node_ids=contained_node_ids,
        )

        extended_jobs_jobs_item_type_1_raw_flow_notes_item.additional_properties = d
        return extended_jobs_jobs_item_type_1_raw_flow_notes_item

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
