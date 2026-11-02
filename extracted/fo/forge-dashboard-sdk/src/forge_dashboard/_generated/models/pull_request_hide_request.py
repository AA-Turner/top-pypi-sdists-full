from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge
from ..types import UNSET, Unset






T = TypeVar("T", bound="PullRequestHideRequest")



@_attrs_define
class PullRequestHideRequest:
    """ Which pull request to hide, and for how long. Without `days` it stays
    hidden until it is restored.

        Attributes:
            forge (Forge):
            full_name (str): "owner/repo", matching a Repo.fullName from GET /api/v1/dashboard.
            number (int): Matching a PullRequest.number from GET /api/v1/dashboard.
            days (int | Unset): Hide for this many days, then show it again on its own.
     """

    forge: Forge
    full_name: str
    number: int
    days: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        forge = self.forge.value

        full_name = self.full_name

        number = self.number

        days = self.days


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "fullName": full_name,
            "number": number,
        })
        if days is not UNSET:
            field_dict["days"] = days

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        full_name = d.pop("fullName")

        number = d.pop("number")

        days = d.pop("days", UNSET)

        pull_request_hide_request = cls(
            forge=forge,
            full_name=full_name,
            number=number,
            days=days,
        )


        pull_request_hide_request.additional_properties = d
        return pull_request_hide_request

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
