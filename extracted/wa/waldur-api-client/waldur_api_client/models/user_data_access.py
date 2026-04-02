from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.administrative_access import AdministrativeAccess
    from ..models.data_access_summary import DataAccessSummary
    from ..models.organizational_access import OrganizationalAccess
    from ..models.service_provider_access import ServiceProviderAccess


T = TypeVar("T", bound="UserDataAccess")


@_attrs_define
class UserDataAccess:
    """
    Attributes:
        administrative_access (AdministrativeAccess):
        organizational_access (list['OrganizationalAccess']):
        service_provider_access (list['ServiceProviderAccess']):
        summary (DataAccessSummary):
    """

    administrative_access: "AdministrativeAccess"
    organizational_access: list["OrganizationalAccess"]
    service_provider_access: list["ServiceProviderAccess"]
    summary: "DataAccessSummary"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        administrative_access = self.administrative_access.to_dict()

        organizational_access = []
        for organizational_access_item_data in self.organizational_access:
            organizational_access_item = organizational_access_item_data.to_dict()
            organizational_access.append(organizational_access_item)

        service_provider_access = []
        for service_provider_access_item_data in self.service_provider_access:
            service_provider_access_item = service_provider_access_item_data.to_dict()
            service_provider_access.append(service_provider_access_item)

        summary = self.summary.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "administrative_access": administrative_access,
                "organizational_access": organizational_access,
                "service_provider_access": service_provider_access,
                "summary": summary,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.administrative_access import AdministrativeAccess
        from ..models.data_access_summary import DataAccessSummary
        from ..models.organizational_access import OrganizationalAccess
        from ..models.service_provider_access import ServiceProviderAccess

        d = dict(src_dict)
        administrative_access = AdministrativeAccess.from_dict(d.pop("administrative_access"))

        organizational_access = []
        _organizational_access = d.pop("organizational_access")
        for organizational_access_item_data in _organizational_access:
            organizational_access_item = OrganizationalAccess.from_dict(organizational_access_item_data)

            organizational_access.append(organizational_access_item)

        service_provider_access = []
        _service_provider_access = d.pop("service_provider_access")
        for service_provider_access_item_data in _service_provider_access:
            service_provider_access_item = ServiceProviderAccess.from_dict(service_provider_access_item_data)

            service_provider_access.append(service_provider_access_item)

        summary = DataAccessSummary.from_dict(d.pop("summary"))

        user_data_access = cls(
            administrative_access=administrative_access,
            organizational_access=organizational_access,
            service_provider_access=service_provider_access,
            summary=summary,
        )

        user_data_access.additional_properties = d
        return user_data_access

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
