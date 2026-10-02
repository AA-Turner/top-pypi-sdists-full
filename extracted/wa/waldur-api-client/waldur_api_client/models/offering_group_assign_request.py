from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingGroupAssignRequest")


@_attrs_define
class OfferingGroupAssignRequest:
    """
    Attributes:
        offering_group (Union[None, UUID]): OfferingGroup UUID. Pass null to remove the assignment.
    """

    offering_group: Union[None, UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_group: Union[None, str]
        if isinstance(self.offering_group, UUID):
            offering_group = str(self.offering_group)
        else:
            offering_group = self.offering_group

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_group": offering_group,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_offering_group(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                offering_group_type_0 = UUID(data)

                return offering_group_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        offering_group = _parse_offering_group(d.pop("offering_group"))

        offering_group_assign_request = cls(
            offering_group=offering_group,
        )

        offering_group_assign_request.additional_properties = d
        return offering_group_assign_request

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
