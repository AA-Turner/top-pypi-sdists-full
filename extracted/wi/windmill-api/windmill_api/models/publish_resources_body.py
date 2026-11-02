from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.publish_resources_body_resources_item import PublishResourcesBodyResourcesItem


T = TypeVar("T", bound="PublishResourcesBody")


@_attrs_define
class PublishResourcesBody:
    """
    Attributes:
        resources (List['PublishResourcesBodyResourcesItem']):
        project_slug (str): hub project slug (3-50 chars, lowercase alphanumeric and hyphens, no leading/trailing
            hyphen)
    """

    resources: List["PublishResourcesBodyResourcesItem"]
    project_slug: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        resources = []
        for resources_item_data in self.resources:
            resources_item = resources_item_data.to_dict()

            resources.append(resources_item)

        project_slug = self.project_slug

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resources": resources,
                "project_slug": project_slug,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.publish_resources_body_resources_item import PublishResourcesBodyResourcesItem

        d = src_dict.copy()
        resources = []
        _resources = d.pop("resources")
        for resources_item_data in _resources:
            resources_item = PublishResourcesBodyResourcesItem.from_dict(resources_item_data)

            resources.append(resources_item)

        project_slug = d.pop("project_slug")

        publish_resources_body = cls(
            resources=resources,
            project_slug=project_slug,
        )

        publish_resources_body.additional_properties = d
        return publish_resources_body

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
