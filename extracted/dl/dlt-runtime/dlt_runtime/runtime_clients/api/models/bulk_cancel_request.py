from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkCancelRequest")


@_attrs_define
class BulkCancelRequest:
    """
    Attributes:
        job_refs (list[str]): Job references whose active (non-terminal) runs should be cancelled.
        dry_run (Union[Unset, bool]): If true, return runs that would be cancelled without cancelling them. Default:
            False.
    """

    job_refs: list[str]
    dry_run: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_refs = self.job_refs

        dry_run = self.dry_run

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_refs": job_refs,
            }
        )
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_refs = cast(list[str], d.pop("job_refs"))

        dry_run = d.pop("dry_run", UNSET)

        bulk_cancel_request = cls(
            job_refs=job_refs,
            dry_run=dry_run,
        )

        bulk_cancel_request.additional_properties = d
        return bulk_cancel_request

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
