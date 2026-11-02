from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge
from ..models.pull_request_dependabot_action_request_action import PullRequestDependabotActionRequestAction






T = TypeVar("T", bound="PullRequestDependabotActionRequest")



@_attrs_define
class PullRequestDependabotActionRequest:
    """ Which pull request to act on, and which of Dependabot's own comment commands to send.

        Attributes:
            forge (Forge):
            full_name (str): "owner/repo", matching a Repo.fullName from GET /api/v1/dashboard.
            number (int): Matching a PullRequest.number from GET /api/v1/dashboard.
            action (PullRequestDependabotActionRequestAction): Which Dependabot comment command to post — "@dependabot
                rebase" or "@dependabot recreate".
     """

    forge: Forge
    full_name: str
    number: int
    action: PullRequestDependabotActionRequestAction
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        forge = self.forge.value

        full_name = self.full_name

        number = self.number

        action = self.action.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "fullName": full_name,
            "number": number,
            "action": action,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        full_name = d.pop("fullName")

        number = d.pop("number")

        action = PullRequestDependabotActionRequestAction(d.pop("action"))




        pull_request_dependabot_action_request = cls(
            forge=forge,
            full_name=full_name,
            number=number,
            action=action,
        )


        pull_request_dependabot_action_request.additional_properties = d
        return pull_request_dependabot_action_request

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
