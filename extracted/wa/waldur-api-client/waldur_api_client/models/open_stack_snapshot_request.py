import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackSnapshotRequest")


@_attrs_define
class OpenStackSnapshotRequest:
    """
    Attributes:
        name (str):
        description (Union[Unset, str]):
        metadata (Union[Unset, Any]):
        kept_until (Union[None, Unset, datetime.datetime]): Guaranteed time of snapshot retention. If null - keep
            forever.
    """

    name: str
    description: Union[Unset, str] = UNSET
    metadata: Union[Unset, Any] = UNSET
    kept_until: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        metadata = self.metadata

        kept_until: Union[None, Unset, str]
        if isinstance(self.kept_until, Unset):
            kept_until = UNSET
        elif isinstance(self.kept_until, datetime.datetime):
            kept_until = self.kept_until.isoformat()
        else:
            kept_until = self.kept_until

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if kept_until is not UNSET:
            field_dict["kept_until"] = kept_until

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        metadata = d.pop("metadata", UNSET)

        def _parse_kept_until(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                kept_until_type_0 = isoparse(data)

                return kept_until_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        kept_until = _parse_kept_until(d.pop("kept_until", UNSET))

        open_stack_snapshot_request = cls(
            name=name,
            description=description,
            metadata=metadata,
            kept_until=kept_until,
        )

        open_stack_snapshot_request.additional_properties = d
        return open_stack_snapshot_request

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
