from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_group_entry_request import ProjectGroupEntryRequest


T = TypeVar("T", bound="ServiceProviderProjectGroupImportRequest")


@_attrs_define
class ServiceProviderProjectGroupImportRequest:
    """
    Attributes:
        service_provider (UUID):
        groups (list['ProjectGroupEntryRequest']):
        allow_outside_range (Union[Unset, bool]): Accept a GID outside the range project groups draw from, e.g. one a
            directory assigned before Waldur managed it. Default: False.
    """

    service_provider: UUID
    groups: list["ProjectGroupEntryRequest"]
    allow_outside_range: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_provider = str(self.service_provider)

        groups = []
        for groups_item_data in self.groups:
            groups_item = groups_item_data.to_dict()
            groups.append(groups_item)

        allow_outside_range = self.allow_outside_range

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_provider": service_provider,
                "groups": groups,
            }
        )
        if allow_outside_range is not UNSET:
            field_dict["allow_outside_range"] = allow_outside_range

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_group_entry_request import ProjectGroupEntryRequest

        d = dict(src_dict)
        service_provider = UUID(d.pop("service_provider"))

        groups = []
        _groups = d.pop("groups")
        for groups_item_data in _groups:
            groups_item = ProjectGroupEntryRequest.from_dict(groups_item_data)

            groups.append(groups_item)

        allow_outside_range = d.pop("allow_outside_range", UNSET)

        service_provider_project_group_import_request = cls(
            service_provider=service_provider,
            groups=groups,
            allow_outside_range=allow_outside_range,
        )

        service_provider_project_group_import_request.additional_properties = d
        return service_provider_project_group_import_request

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
