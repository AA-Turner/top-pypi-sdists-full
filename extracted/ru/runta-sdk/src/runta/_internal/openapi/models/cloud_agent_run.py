from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="CloudAgentRun")


@_attrs_define
class CloudAgentRun:
    """
    Attributes:
        id (str):
        agent_id (str):
        status (str):
        prompt (None | str):
        result (None | str):
        error (None | str):
        parent_run_id (None | str):
        dsh_session_id (None | str):
        created_at (None | str):
        updated_at (None | str):
    """

    id: str
    agent_id: str
    status: str
    prompt: None | str
    result: None | str
    error: None | str
    parent_run_id: None | str
    dsh_session_id: None | str
    created_at: None | str
    updated_at: None | str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        agent_id = self.agent_id

        status = self.status

        prompt: None | str
        prompt = self.prompt

        result: None | str
        result = self.result

        error: None | str
        error = self.error

        parent_run_id: None | str
        parent_run_id = self.parent_run_id

        dsh_session_id: None | str
        dsh_session_id = self.dsh_session_id

        created_at: None | str
        created_at = self.created_at

        updated_at: None | str
        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "agent_id": agent_id,
                "status": status,
                "prompt": prompt,
                "result": result,
                "error": error,
                "parent_run_id": parent_run_id,
                "dsh_session_id": dsh_session_id,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        agent_id = d.pop("agent_id")

        status = d.pop("status")

        def _parse_prompt(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        prompt = _parse_prompt(d.pop("prompt"))

        def _parse_result(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        result = _parse_result(d.pop("result"))

        def _parse_error(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error = _parse_error(d.pop("error"))

        def _parse_parent_run_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        parent_run_id = _parse_parent_run_id(d.pop("parent_run_id"))

        def _parse_dsh_session_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        dsh_session_id = _parse_dsh_session_id(d.pop("dsh_session_id"))

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

        cloud_agent_run = cls(
            id=id,
            agent_id=agent_id,
            status=status,
            prompt=prompt,
            result=result,
            error=error,
            parent_run_id=parent_run_id,
            dsh_session_id=dsh_session_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        return cloud_agent_run
