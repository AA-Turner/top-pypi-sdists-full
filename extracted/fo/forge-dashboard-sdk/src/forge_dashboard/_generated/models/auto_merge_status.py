from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auto_merge_status_state import AutoMergeStatusState
from ..types import UNSET, Unset






T = TypeVar("T", bound="AutoMergeStatus")



@_attrs_define
class AutoMergeStatus:
    """ Where an armed pull request stands, so the row can say why
    auto-merge is waiting or stopped in words and not by colour. Present
    while auto-merge is armed on it: on Forgejo the signed-in user's
    intent held by this app, on GitHub the forge's own auto-merge.
    Also present for ten minutes after this app cancelled an armed
    auto-merge because the pull request went empty (its branch landed on
    the base some other way): `stopped`, code `already_up_to_date` and the
    message "Auto-merge was cancelled: there is nothing left to merge."
    Auto-merge is off by then, so this is the only place the reason lives.

        Attributes:
            state (AutoMergeStatusState): `waiting` clears by itself: checks still running, a draft, a
                stack parent that hasn't merged, a rate limit. `stopped` needs the
                person: a failing check, a conflict, or a merge Forgejo refused
                (including a token without merge permission). A stopped pull
                request stays armed and merges once the cause is gone, or the
                person cancels.
            message (str): Plain words, safe to show a person.
            code (str | Unset): The same codes as `ActionError.code` (`checks_pending`,
                `checks_failing`, `conflict`, `stacked`, `permission`,
                `rate_limited`, `not_mergeable`). Omitted when the pull request
                is simply waiting for the next refresh to merge it.
     """

    state: AutoMergeStatusState
    message: str
    code: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        state = self.state.value

        message = self.message

        code = self.code


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "state": state,
            "message": message,
        })
        if code is not UNSET:
            field_dict["code"] = code

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = AutoMergeStatusState(d.pop("state"))




        message = d.pop("message")

        code = d.pop("code", UNSET)

        auto_merge_status = cls(
            state=state,
            message=message,
            code=code,
        )


        auto_merge_status.additional_properties = d
        return auto_merge_status

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
