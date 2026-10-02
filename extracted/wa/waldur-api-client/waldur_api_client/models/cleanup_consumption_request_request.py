from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CleanupConsumptionRequestRequest")


@_attrs_define
class CleanupConsumptionRequestRequest:
    """
    Attributes:
        period_from (Union[Unset, str]): YYYY-MM format
        period_to (Union[Unset, str]): YYYY-MM format
        resource_uuid (Union[Unset, UUID]):
        only_finalized (Union[Unset, bool]):  Default: False.
        only_unfinalized (Union[Unset, bool]):  Default: False.
        dry_run (Union[Unset, bool]):  Default: True.
    """

    period_from: Union[Unset, str] = UNSET
    period_to: Union[Unset, str] = UNSET
    resource_uuid: Union[Unset, UUID] = UNSET
    only_finalized: Union[Unset, bool] = False
    only_unfinalized: Union[Unset, bool] = False
    dry_run: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period_from = self.period_from

        period_to = self.period_to

        resource_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.resource_uuid, Unset):
            resource_uuid = str(self.resource_uuid)

        only_finalized = self.only_finalized

        only_unfinalized = self.only_unfinalized

        dry_run = self.dry_run

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if period_from is not UNSET:
            field_dict["period_from"] = period_from
        if period_to is not UNSET:
            field_dict["period_to"] = period_to
        if resource_uuid is not UNSET:
            field_dict["resource_uuid"] = resource_uuid
        if only_finalized is not UNSET:
            field_dict["only_finalized"] = only_finalized
        if only_unfinalized is not UNSET:
            field_dict["only_unfinalized"] = only_unfinalized
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period_from = d.pop("period_from", UNSET)

        period_to = d.pop("period_to", UNSET)

        _resource_uuid = d.pop("resource_uuid", UNSET)
        resource_uuid: Union[Unset, UUID]
        if isinstance(_resource_uuid, Unset):
            resource_uuid = UNSET
        else:
            resource_uuid = UUID(_resource_uuid)

        only_finalized = d.pop("only_finalized", UNSET)

        only_unfinalized = d.pop("only_unfinalized", UNSET)

        dry_run = d.pop("dry_run", UNSET)

        cleanup_consumption_request_request = cls(
            period_from=period_from,
            period_to=period_to,
            resource_uuid=resource_uuid,
            only_finalized=only_finalized,
            only_unfinalized=only_unfinalized,
            dry_run=dry_run,
        )

        cleanup_consumption_request_request.additional_properties = d
        return cleanup_consumption_request_request

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
