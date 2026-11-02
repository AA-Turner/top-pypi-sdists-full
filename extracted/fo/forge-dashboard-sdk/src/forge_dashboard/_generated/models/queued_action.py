from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge
from ..models.queued_action_action import QueuedActionAction
from ..models.queued_action_status import QueuedActionStatus
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="QueuedAction")



@_attrs_define
class QueuedAction:
    """ A safe action queued to run when a rate-limited forge resets. A
    client shows a `queued` one as "Update branch queued for 14:32"
    with Cancel, and a final one in its Activity list.

        Attributes:
            id (str): Opaque. What DELETE /api/v1/queued-actions/{id} takes.
            action (QueuedActionAction):
            forge (Forge):
            full_name (str): "owner/repo".
            number (int):
            status (QueuedActionStatus): `queued`: waiting for the reset. `done`: the action ran.
                `skipped`: the server re-read the pull request at the reset and
                it no longer needed the action, so nothing was done; `code` and
                `message` say why ("Already merged"). `failed`: the action ran
                and the forge refused, with the structured `code` and `message`
                an immediate action would have answered.
            run_at (datetime.datetime): When the forge's budget comes back, which is when the server
                looks again. If the budget is spent again by then, it moves to
                the new reset instead of failing.
            created_at (datetime.datetime):
            finished_at (datetime.datetime | Unset): Only on a final status.
            code (str | Unset): Only on `skipped` and `failed`. A value of ActionError.code,
                for example `already_merged`, `already_closed`, `not_open`,
                `already_up_to_date`, `conflict`, `already_requested`,
                `permission`.
            message (str | Unset): Only on `skipped` and `failed`. Plain words safe to show a person.
     """

    id: str
    action: QueuedActionAction
    forge: Forge
    full_name: str
    number: int
    status: QueuedActionStatus
    run_at: datetime.datetime
    created_at: datetime.datetime
    finished_at: datetime.datetime | Unset = UNSET
    code: str | Unset = UNSET
    message: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        action = self.action.value

        forge = self.forge.value

        full_name = self.full_name

        number = self.number

        status = self.status.value

        run_at = self.run_at.isoformat()

        created_at = self.created_at.isoformat()

        finished_at: str | Unset = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat()

        code = self.code

        message = self.message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "action": action,
            "forge": forge,
            "fullName": full_name,
            "number": number,
            "status": status,
            "runAt": run_at,
            "createdAt": created_at,
        })
        if finished_at is not UNSET:
            field_dict["finishedAt"] = finished_at
        if code is not UNSET:
            field_dict["code"] = code
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        action = QueuedActionAction(d.pop("action"))




        forge = Forge(d.pop("forge"))




        full_name = d.pop("fullName")

        number = d.pop("number")

        status = QueuedActionStatus(d.pop("status"))




        run_at = datetime.datetime.fromisoformat(d.pop("runAt"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        _finished_at = d.pop("finishedAt", UNSET)
        finished_at: datetime.datetime | Unset
        if isinstance(_finished_at,  Unset):
            finished_at = UNSET
        else:
            finished_at = datetime.datetime.fromisoformat(_finished_at)




        code = d.pop("code", UNSET)

        message = d.pop("message", UNSET)

        queued_action = cls(
            id=id,
            action=action,
            forge=forge,
            full_name=full_name,
            number=number,
            status=status,
            run_at=run_at,
            created_at=created_at,
            finished_at=finished_at,
            code=code,
            message=message,
        )


        queued_action.additional_properties = d
        return queued_action

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
