from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.bot_request_action import BotRequestAction
from ..models.bot_request_bot import BotRequestBot
from ..models.bot_request_phase import BotRequestPhase
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="BotRequest")



@_attrs_define
class BotRequest:
    """ 
        Attributes:
            bot (BotRequestBot):
            action (BotRequestAction): `recreate` is Dependabot's only. Renovate's rebase label is
                reported as `rebase`.
            phase (BotRequestPhase): `queued`: asked, and nothing seen yet. `rebasing`: the bot
                pushed (the head changed, or the pull request was behind and
                isn't), and CI hasn't restarted yet. `expired`: the bot didn't
                act within 10 minutes. An expired request stays until the pull
                request is gone, a new request replaces it, or an hour passes.
                A request is dropped once CI shows pending after the push, 2
                minutes into `rebasing`, or when the pull request is gone.
            requested_at (datetime.datetime):
            expires_at (datetime.datetime): When the server stops waiting in the current phase: 10 minutes
                after the request while `queued` (10 minutes after
                `acknowledgedAt` once Dependabot has acknowledged), 2 minutes
                after the pickup while `rebasing`.
            acknowledged_at (datetime.datetime | Unset): When the server first saw Dependabot's thumbs-up on the
                `@dependabot rebase` comment, which is how Dependabot says it
                received the command. Absent until then, and always absent for
                Renovate and for `recreate`. A thumbs-up that arrives after the
                request expired moves it back to `queued`.
            comment_url (str | Unset): The command comment on GitHub, once the server has found it.
                Absent before that, and for Renovate.
     """

    bot: BotRequestBot
    action: BotRequestAction
    phase: BotRequestPhase
    requested_at: datetime.datetime
    expires_at: datetime.datetime
    acknowledged_at: datetime.datetime | Unset = UNSET
    comment_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        bot = self.bot.value

        action = self.action.value

        phase = self.phase.value

        requested_at = self.requested_at.isoformat()

        expires_at = self.expires_at.isoformat()

        acknowledged_at: str | Unset = UNSET
        if not isinstance(self.acknowledged_at, Unset):
            acknowledged_at = self.acknowledged_at.isoformat()

        comment_url = self.comment_url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "bot": bot,
            "action": action,
            "phase": phase,
            "requestedAt": requested_at,
            "expiresAt": expires_at,
        })
        if acknowledged_at is not UNSET:
            field_dict["acknowledgedAt"] = acknowledged_at
        if comment_url is not UNSET:
            field_dict["commentUrl"] = comment_url

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bot = BotRequestBot(d.pop("bot"))




        action = BotRequestAction(d.pop("action"))




        phase = BotRequestPhase(d.pop("phase"))




        requested_at = datetime.datetime.fromisoformat(d.pop("requestedAt"))




        expires_at = datetime.datetime.fromisoformat(d.pop("expiresAt"))




        _acknowledged_at = d.pop("acknowledgedAt", UNSET)
        acknowledged_at: datetime.datetime | Unset
        if isinstance(_acknowledged_at,  Unset):
            acknowledged_at = UNSET
        else:
            acknowledged_at = datetime.datetime.fromisoformat(_acknowledged_at)




        comment_url = d.pop("commentUrl", UNSET)

        bot_request = cls(
            bot=bot,
            action=action,
            phase=phase,
            requested_at=requested_at,
            expires_at=expires_at,
            acknowledged_at=acknowledged_at,
            comment_url=comment_url,
        )


        bot_request.additional_properties = d
        return bot_request

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
