from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.topology_node_type_enum import TopologyNodeTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.topology_node_attrs import TopologyNodeAttrs


T = TypeVar("T", bound="TopologyNode")


@_attrs_define
class TopologyNode:
    """
    Attributes:
        id (str):
        type_ (TopologyNodeTypeEnum):
        name (str):
        attrs (TopologyNodeAttrs):
        uuid (Union[None, Unset, str]):
    """

    id: str
    type_: TopologyNodeTypeEnum
    name: str
    attrs: "TopologyNodeAttrs"
    uuid: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_.value

        name = self.name

        attrs = self.attrs.to_dict()

        uuid: Union[None, Unset, str]
        if isinstance(self.uuid, Unset):
            uuid = UNSET
        else:
            uuid = self.uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "name": name,
                "attrs": attrs,
            }
        )
        if uuid is not UNSET:
            field_dict["uuid"] = uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.topology_node_attrs import TopologyNodeAttrs

        d = dict(src_dict)
        id = d.pop("id")

        type_ = TopologyNodeTypeEnum(d.pop("type"))

        name = d.pop("name")

        attrs = TopologyNodeAttrs.from_dict(d.pop("attrs"))

        def _parse_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        uuid = _parse_uuid(d.pop("uuid", UNSET))

        topology_node = cls(
            id=id,
            type_=type_,
            name=name,
            attrs=attrs,
            uuid=uuid,
        )

        topology_node.additional_properties = d
        return topology_node

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
