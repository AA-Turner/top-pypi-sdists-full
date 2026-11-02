from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="PullRequestAutoUpdateRequest")



@_attrs_define
class PullRequestAutoUpdateRequest:
    """ Which pull request, and whether the dashboard should update its
    branch automatically.

        Attributes:
            forge (Forge):
            full_name (str): "owner/repo", matching a Repo.fullName from GET /api/v1/dashboard.
            number (int): Matching a PullRequest.number from GET /api/v1/dashboard.
            enabled (bool | None | Unset): `true` to update this pull request automatically, `false` to
                leave it alone, whatever its repo says. `null` or absent
                returns it to its repo's setting.
     """

    forge: Forge
    full_name: str
    number: int
    enabled: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        forge = self.forge.value

        full_name = self.full_name

        number = self.number

        enabled: bool | None | Unset
        if isinstance(self.enabled, Unset):
            enabled = UNSET
        else:
            enabled = self.enabled


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "fullName": full_name,
            "number": number,
        })
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        full_name = d.pop("fullName")

        number = d.pop("number")

        def _parse_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        enabled = _parse_enabled(d.pop("enabled", UNSET))


        pull_request_auto_update_request = cls(
            forge=forge,
            full_name=full_name,
            number=number,
            enabled=enabled,
        )


        pull_request_auto_update_request.additional_properties = d
        return pull_request_auto_update_request

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
