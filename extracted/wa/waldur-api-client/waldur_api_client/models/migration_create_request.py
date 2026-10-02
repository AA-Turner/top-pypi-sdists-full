from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mapping_request import MappingRequest


T = TypeVar("T", bound="MigrationCreateRequest")


@_attrs_define
class MigrationCreateRequest:
    """
    Attributes:
        src_resource (UUID):
        dst_offering (UUID):
        dst_plan (UUID):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        mappings (Union[Unset, MappingRequest]):
    """

    src_resource: UUID
    dst_offering: UUID
    dst_plan: UUID
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    mappings: Union[Unset, "MappingRequest"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        src_resource = str(self.src_resource)

        dst_offering = str(self.dst_offering)

        dst_plan = str(self.dst_plan)

        name = self.name

        description = self.description

        mappings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.mappings, Unset):
            mappings = self.mappings.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "src_resource": src_resource,
                "dst_offering": dst_offering,
                "dst_plan": dst_plan,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if mappings is not UNSET:
            field_dict["mappings"] = mappings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mapping_request import MappingRequest

        d = dict(src_dict)
        src_resource = UUID(d.pop("src_resource"))

        dst_offering = UUID(d.pop("dst_offering"))

        dst_plan = UUID(d.pop("dst_plan"))

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _mappings = d.pop("mappings", UNSET)
        mappings: Union[Unset, MappingRequest]
        if isinstance(_mappings, Unset):
            mappings = UNSET
        else:
            mappings = MappingRequest.from_dict(_mappings)

        migration_create_request = cls(
            src_resource=src_resource,
            dst_offering=dst_offering,
            dst_plan=dst_plan,
            name=name,
            description=description,
            mappings=mappings,
        )

        migration_create_request.additional_properties = d
        return migration_create_request

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
