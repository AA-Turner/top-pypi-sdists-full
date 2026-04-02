import datetime
from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="PaidRequestMultipart")


@_attrs_define
class PaidRequestMultipart:
    """
    Attributes:
        date (datetime.date):
        proof (Union[Unset, File]):
    """

    date: datetime.date
    proof: Union[Unset, File] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date.isoformat()

        proof: Union[Unset, types.FileTypes] = UNSET
        if not isinstance(self.proof, Unset):
            proof = self.proof.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
            }
        )
        if proof is not UNSET:
            field_dict["proof"] = proof

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("date", (None, self.date.isoformat().encode(), "text/plain")))

        if not isinstance(self.proof, Unset):
            files.append(("proof", self.proof.to_tuple()))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = isoparse(d.pop("date")).date()

        _proof = d.pop("proof", UNSET)
        proof: Union[Unset, File]
        if isinstance(_proof, Unset):
            proof = UNSET
        else:
            proof = File(payload=BytesIO(_proof))

        paid_request_multipart = cls(
            date=date,
            proof=proof,
        )

        paid_request_multipart.additional_properties = d
        return paid_request_multipart

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
