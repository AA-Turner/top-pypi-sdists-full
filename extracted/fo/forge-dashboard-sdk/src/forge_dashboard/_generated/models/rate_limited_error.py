from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="RateLimitedError")



@_attrs_define
class RateLimitedError:
    """ A read the forge rate-limited.

        Attributes:
            error (str):
            field (str | Unset): Present when the rejection is about one field of the request
                body (a settings save, for instance), named as it appears there,
                so a client can mark that input without parsing `error`.
            resets_at (datetime.datetime | Unset): When the exhausted budget comes back. Absent when the forge didn't say,
                and when it limited the request with budget still left (GitHub's secondary limit), since no reset time is known
                then. On Forgejo it comes from the `Retry-After` header.
     """

    error: str
    field: str | Unset = UNSET
    resets_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        error = self.error

        field = self.field

        resets_at: str | Unset = UNSET
        if not isinstance(self.resets_at, Unset):
            resets_at = self.resets_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "error": error,
        })
        if field is not UNSET:
            field_dict["field"] = field
        if resets_at is not UNSET:
            field_dict["resetsAt"] = resets_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = d.pop("error")

        field = d.pop("field", UNSET)

        _resets_at = d.pop("resetsAt", UNSET)
        resets_at: datetime.datetime | Unset
        if isinstance(_resets_at,  Unset):
            resets_at = UNSET
        else:
            resets_at = datetime.datetime.fromisoformat(_resets_at)




        rate_limited_error = cls(
            error=error,
            field=field,
            resets_at=resets_at,
        )


        rate_limited_error.additional_properties = d
        return rate_limited_error

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
