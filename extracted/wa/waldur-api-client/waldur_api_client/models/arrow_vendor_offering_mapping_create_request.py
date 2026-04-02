from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArrowVendorOfferingMappingCreateRequest")


@_attrs_define
class ArrowVendorOfferingMappingCreateRequest:
    """
    Attributes:
        settings (UUID):
        arrow_vendor_name (str): Arrow vendor name (e.g., 'Microsoft', 'Amazon Web Services')
        offering (UUID):
        plan (Union[None, UUID, Unset]):
        is_active (Union[Unset, bool]): Whether this mapping is active
    """

    settings: UUID
    arrow_vendor_name: str
    offering: UUID
    plan: Union[None, UUID, Unset] = UNSET
    is_active: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        settings = str(self.settings)

        arrow_vendor_name = self.arrow_vendor_name

        offering = str(self.offering)

        plan: Union[None, Unset, str]
        if isinstance(self.plan, Unset):
            plan = UNSET
        elif isinstance(self.plan, UUID):
            plan = str(self.plan)
        else:
            plan = self.plan

        is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "settings": settings,
                "arrow_vendor_name": arrow_vendor_name,
                "offering": offering,
            }
        )
        if plan is not UNSET:
            field_dict["plan"] = plan
        if is_active is not UNSET:
            field_dict["is_active"] = is_active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        settings = UUID(d.pop("settings"))

        arrow_vendor_name = d.pop("arrow_vendor_name")

        offering = UUID(d.pop("offering"))

        def _parse_plan(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                plan_type_0 = UUID(data)

                return plan_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        plan = _parse_plan(d.pop("plan", UNSET))

        is_active = d.pop("is_active", UNSET)

        arrow_vendor_offering_mapping_create_request = cls(
            settings=settings,
            arrow_vendor_name=arrow_vendor_name,
            offering=offering,
            plan=plan,
            is_active=is_active,
        )

        arrow_vendor_offering_mapping_create_request.additional_properties = d
        return arrow_vendor_offering_mapping_create_request

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
