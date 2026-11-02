from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cloud_agent_latest_reply import CloudAgentLatestReply


T = TypeVar("T", bound="CloudAgent")


@_attrs_define
class CloudAgent:
    """
    Attributes:
        id (str):
        runtime_id (str):
        harness_id (str):
        name (str):
        status (str):
        created_at_unix_seconds (int):
        updated_at_unix_seconds (int):
        latest_reply (CloudAgentLatestReply | Unset):
    """

    id: str
    runtime_id: str
    harness_id: str
    name: str
    status: str
    created_at_unix_seconds: int
    updated_at_unix_seconds: int
    latest_reply: CloudAgentLatestReply | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        runtime_id = self.runtime_id

        harness_id = self.harness_id

        name = self.name

        status = self.status

        created_at_unix_seconds = self.created_at_unix_seconds

        updated_at_unix_seconds = self.updated_at_unix_seconds

        latest_reply: dict[str, Any] | Unset = UNSET
        if not isinstance(self.latest_reply, Unset):
            latest_reply = self.latest_reply.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "runtime_id": runtime_id,
                "harness_id": harness_id,
                "name": name,
                "status": status,
                "created_at_unix_seconds": created_at_unix_seconds,
                "updated_at_unix_seconds": updated_at_unix_seconds,
            }
        )
        if latest_reply is not UNSET:
            field_dict["latest_reply"] = latest_reply

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cloud_agent_latest_reply import CloudAgentLatestReply

        d = dict(src_dict)
        id = d.pop("id")

        runtime_id = d.pop("runtime_id")

        harness_id = d.pop("harness_id")

        name = d.pop("name")

        status = d.pop("status")

        created_at_unix_seconds = d.pop("created_at_unix_seconds")

        updated_at_unix_seconds = d.pop("updated_at_unix_seconds")

        _latest_reply = d.pop("latest_reply", UNSET)
        latest_reply: CloudAgentLatestReply | Unset
        if isinstance(_latest_reply, Unset):
            latest_reply = UNSET
        else:
            latest_reply = CloudAgentLatestReply.from_dict(_latest_reply)

        cloud_agent = cls(
            id=id,
            runtime_id=runtime_id,
            harness_id=harness_id,
            name=name,
            status=status,
            created_at_unix_seconds=created_at_unix_seconds,
            updated_at_unix_seconds=updated_at_unix_seconds,
            latest_reply=latest_reply,
        )

        return cloud_agent
