import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rancher_cluster_template_node import RancherClusterTemplateNode


T = TypeVar("T", bound="RancherClusterTemplate")


@_attrs_define
class RancherClusterTemplate:
    """
    Attributes:
        uuid (UUID):
        name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        nodes (list['RancherClusterTemplateNode']):
        description (Union[Unset, str]):
    """

    uuid: UUID
    name: str
    created: datetime.datetime
    modified: datetime.datetime
    nodes: list["RancherClusterTemplateNode"]
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        nodes = []
        for nodes_item_data in self.nodes:
            nodes_item = nodes_item_data.to_dict()
            nodes.append(nodes_item)

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "created": created,
                "modified": modified,
                "nodes": nodes,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rancher_cluster_template_node import RancherClusterTemplateNode

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        nodes = []
        _nodes = d.pop("nodes")
        for nodes_item_data in _nodes:
            nodes_item = RancherClusterTemplateNode.from_dict(nodes_item_data)

            nodes.append(nodes_item)

        description = d.pop("description", UNSET)

        rancher_cluster_template = cls(
            uuid=uuid,
            name=name,
            created=created,
            modified=modified,
            nodes=nodes,
            description=description,
        )

        rancher_cluster_template.additional_properties = d
        return rancher_cluster_template

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
