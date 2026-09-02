from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.publish_resource_type_body_schema import PublishResourceTypeBodySchema


T = TypeVar("T", bound="PublishResourceTypeBody")


@_attrs_define
class PublishResourceTypeBody:
    """
    Attributes:
        name (str):
        project_slug (str): hub project slug (3-50 chars, lowercase alphanumeric and hyphens, no leading/trailing
            hyphen)
        schema (Union[Unset, PublishResourceTypeBodySchema]):
        description (Union[Unset, str]):
    """

    name: str
    project_slug: str
    schema: Union[Unset, "PublishResourceTypeBodySchema"] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        project_slug = self.project_slug
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "project_slug": project_slug,
            }
        )
        if schema is not UNSET:
            field_dict["schema"] = schema
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.publish_resource_type_body_schema import PublishResourceTypeBodySchema

        d = src_dict.copy()
        name = d.pop("name")

        project_slug = d.pop("project_slug")

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, PublishResourceTypeBodySchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = PublishResourceTypeBodySchema.from_dict(_schema)

        description = d.pop("description", UNSET)

        publish_resource_type_body = cls(
            name=name,
            project_slug=project_slug,
            schema=schema,
            description=description,
        )

        publish_resource_type_body.additional_properties = d
        return publish_resource_type_body

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
