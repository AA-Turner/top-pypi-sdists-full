from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="CloudAgentLatestReply")


@_attrs_define
class CloudAgentLatestReply:
    """
    Attributes:
        run_id (str):
        text (str):
        created_at (None | str):
        updated_at (None | str):
    """

    run_id: str
    text: str
    created_at: None | str
    updated_at: None | str

    def to_dict(self) -> dict[str, Any]:
        run_id = self.run_id

        text = self.text

        created_at: None | str
        created_at = self.created_at

        updated_at: None | str
        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "run_id": run_id,
                "text": text,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        run_id = d.pop("run_id")

        text = d.pop("text")

        def _parse_created_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        created_at = _parse_created_at(d.pop("created_at"))

        def _parse_updated_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        updated_at = _parse_updated_at(d.pop("updated_at"))

        cloud_agent_latest_reply = cls(
            run_id=run_id,
            text=text,
            created_at=created_at,
            updated_at=updated_at,
        )

        return cloud_agent_latest_reply
