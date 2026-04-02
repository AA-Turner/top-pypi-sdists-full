from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SendAllAssignmentBatchesRequest")


@_attrs_define
class SendAllAssignmentBatchesRequest:
    """
    Attributes:
        batch_uuids (Union[Unset, list[UUID]]): Specific batch UUIDs to send. If empty, sends all draft batches.
    """

    batch_uuids: Union[Unset, list[UUID]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        batch_uuids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.batch_uuids, Unset):
            batch_uuids = []
            for batch_uuids_item_data in self.batch_uuids:
                batch_uuids_item = str(batch_uuids_item_data)
                batch_uuids.append(batch_uuids_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if batch_uuids is not UNSET:
            field_dict["batch_uuids"] = batch_uuids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        batch_uuids = []
        _batch_uuids = d.pop("batch_uuids", UNSET)
        for batch_uuids_item_data in _batch_uuids or []:
            batch_uuids_item = UUID(batch_uuids_item_data)

            batch_uuids.append(batch_uuids_item)

        send_all_assignment_batches_request = cls(
            batch_uuids=batch_uuids,
        )

        send_all_assignment_batches_request.additional_properties = d
        return send_all_assignment_batches_request

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
