from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.allowed_action_blocked import AllowedActionBlocked





T = TypeVar("T", bound="AllowedAction")



@_attrs_define
class AllowedAction:
    """ 
        Attributes:
            action (str): One of the values below today, and the server may learn more.
                A client should treat a value it doesn't know as an action it
                can't offer, not as an error. Declared with `x-extensible-enum`
                so adding a value is a minor SDK release.
            primary (bool | Unset): True on the one action a client draws as the pull request's main
                button, and absent on every other entry. At most one entry in the
                list has it, never a blocked one, and a pull request can have none.
                The server decides it, so a client renders it and holds no rule of
                its own; a client that doesn't know the field still gets the
                whole list. Which action it is:
                `close` for an empty pull request; `merge` when Merge is offered
                and not blocked, unless the CI is failing (Merge is then only open
                because the failing checks aren't required, and `status` explains
                it); `update_branch`, or `renovate_rebase` or `dependabot_rebase`
                for a bot pull request, when being behind the base branch is what
                holds Merge back. A bot pull request that is behind also has its
                rebase here whatever else holds Merge back (checks running or
                failing, auto-merge armed), unless it conflicts, is a draft, is
                stacked, or its workflow runs wait for approval. In that last
                case, for any author, whenever Merge is blocked or not yet known
                and the checks aren't running, Merge gives the approval as its
                reason. If the pull request is also behind (and not stacked, a
                draft or empty), `update_branch`, the bot rebases and
                `dependabot_recreate` are listed blocked with the same code and
                message and a `next` of their own, so none is primary and a client
                draws each locked with the reason. Every other state has
                none: checks running or failing on a pull request that is not a
                behind bot one, a conflict, a draft, a stack parent, or the
                forge's own block. `status` gives the reason there.
            blocked (AllowedActionBlocked | Unset): Present when the action is offered but can't be taken yet. Merge
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
     """

    action: str
    primary: bool | Unset = UNSET
    blocked: AllowedActionBlocked | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.allowed_action_blocked import AllowedActionBlocked # noqa: PLC0415
        action = self.action

        primary = self.primary

        blocked: dict[str, Any] | Unset = UNSET
        if not isinstance(self.blocked, Unset):
            blocked = self.blocked.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "action": action,
        })
        if primary is not UNSET:
            field_dict["primary"] = primary
        if blocked is not UNSET:
            field_dict["blocked"] = blocked

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.allowed_action_blocked import AllowedActionBlocked # noqa: PLC0415
        d = dict(src_dict)
        action = d.pop("action")

        primary = d.pop("primary", UNSET)

        _blocked = d.pop("blocked", UNSET)
        blocked: AllowedActionBlocked | Unset
        if isinstance(_blocked,  Unset):
            blocked = UNSET
        else:
            blocked = AllowedActionBlocked.from_dict(_blocked)




        allowed_action = cls(
            action=action,
            primary=primary,
            blocked=blocked,
        )


        allowed_action.additional_properties = d
        return allowed_action

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
