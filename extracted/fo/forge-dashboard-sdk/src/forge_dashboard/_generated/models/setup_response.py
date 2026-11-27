from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.setup_forgejo import SetupForgejo
  from ..models.setup_git_hub import SetupGitHub





T = TypeVar("T", bound="SetupResponse")



@_attrs_define
class SetupResponse:
    """ 
        Attributes:
            github (SetupGitHub):
            forgejo (SetupForgejo):
            refreshed (bool): Whether the board has finished a refresh since the process started.
                False while a forge's first read is still running, since its
                repositories can't be counted yet.
     """

    github: SetupGitHub
    forgejo: SetupForgejo
    refreshed: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.setup_forgejo import SetupForgejo # noqa: PLC0415
        from ..models.setup_git_hub import SetupGitHub # noqa: PLC0415
        github = self.github.to_dict()

        forgejo = self.forgejo.to_dict()

        refreshed = self.refreshed


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "github": github,
            "forgejo": forgejo,
            "refreshed": refreshed,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.setup_forgejo import SetupForgejo # noqa: PLC0415
        from ..models.setup_git_hub import SetupGitHub # noqa: PLC0415
        d = dict(src_dict)
        github = SetupGitHub.from_dict(d.pop("github"))




        forgejo = SetupForgejo.from_dict(d.pop("forgejo"))




        refreshed = d.pop("refreshed")

        setup_response = cls(
            github=github,
            forgejo=forgejo,
            refreshed=refreshed,
        )


        setup_response.additional_properties = d
        return setup_response

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
