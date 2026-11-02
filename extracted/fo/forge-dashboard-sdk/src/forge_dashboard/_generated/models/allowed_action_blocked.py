from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="AllowedActionBlocked")



@_attrs_define
class AllowedActionBlocked:
    """ Present when the action is offered but can't be taken yet. Merge
    is blocked rather than hidden while waiting or fixing something can
    unlock it. An empty pull request, which nothing can unlock, has no
    `merge` entry at all: see `status`.
    A request that is already waiting is never listed blocked. While
    Renovate's rebase checkbox in the pull request description is
    ticked, whether from this app or on the forge, `renovate_rebase`
    is absent and `cancel_renovate_rebase` is listed instead. A
    Renovate rebase asked for through this app with no checkbox
    behind it, and a Dependabot rebase or recreate that is pending,
    list neither request nor cancel: Dependabot has no command to
    withdraw one. The request is offered again once the bot has
    acted or the request has expired.

        Attributes:
            code (str): The same codes as `ActionError.code`. The server may learn
                more, so a client should show `message` for a code it doesn't
                know. Declared with `x-extensible-enum`.
            message (str): Plain words, safe to show a person.
            next_ (str | Unset): What unlocks it, when something does.
     """

    code: str
    message: str
    next_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        next_ = self.next_


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "code": code,
            "message": message,
        })
        if next_ is not UNSET:
            field_dict["next"] = next_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        next_ = d.pop("next", UNSET)

        allowed_action_blocked = cls(
            code=code,
            message=message,
            next_=next_,
        )


        allowed_action_blocked.additional_properties = d
        return allowed_action_blocked

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
