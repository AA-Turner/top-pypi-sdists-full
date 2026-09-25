from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobResultResponse")


@_attrs_define
class JobResultResponse:
    """
    Attributes:
        date_added (datetime.datetime): datetime with the constraint that the value must have timezone info
        date_updated (datetime.datetime): datetime with the constraint that the value must have timezone info
        engine_version (int):
        id (UUID):
        job_ref (str):
        result_type (str):
        run_id (UUID):
        agent_status (None | str | Unset): The agent's self-report, which may legitimately disagree with the run's own
            status: a failed agent inside a succeeded run is normal.
        cost_usd (None | str | Unset): Decimal string, never a float.
        input_tokens (int | None | Unset):
        loop_type (None | str | Unset):
        model (None | str | Unset):
        output_tokens (int | None | Unset):
        result (Any | Unset): The job's declared output. Shape is job-defined.
        stop_reason (None | str | Unset):
        summary (None | str | Unset): Model-authored markdown, unbounded. Untrusted — render as user content.
        total_tokens (int | None | Unset):
        turn_count (int | None | Unset):
    """

    date_added: datetime.datetime
    date_updated: datetime.datetime
    engine_version: int
    id: UUID
    job_ref: str
    result_type: str
    run_id: UUID
    agent_status: None | str | Unset = UNSET
    cost_usd: None | str | Unset = UNSET
    input_tokens: int | None | Unset = UNSET
    loop_type: None | str | Unset = UNSET
    model: None | str | Unset = UNSET
    output_tokens: int | None | Unset = UNSET
    result: Any | Unset = UNSET
    stop_reason: None | str | Unset = UNSET
    summary: None | str | Unset = UNSET
    total_tokens: int | None | Unset = UNSET
    turn_count: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        engine_version = self.engine_version

        id = str(self.id)

        job_ref = self.job_ref

        result_type = self.result_type

        run_id = str(self.run_id)

        agent_status: None | str | Unset
        if isinstance(self.agent_status, Unset):
            agent_status = UNSET
        else:
            agent_status = self.agent_status

        cost_usd: None | str | Unset
        if isinstance(self.cost_usd, Unset):
            cost_usd = UNSET
        else:
            cost_usd = self.cost_usd

        input_tokens: int | None | Unset
        if isinstance(self.input_tokens, Unset):
            input_tokens = UNSET
        else:
            input_tokens = self.input_tokens

        loop_type: None | str | Unset
        if isinstance(self.loop_type, Unset):
            loop_type = UNSET
        else:
            loop_type = self.loop_type

        model: None | str | Unset
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        output_tokens: int | None | Unset
        if isinstance(self.output_tokens, Unset):
            output_tokens = UNSET
        else:
            output_tokens = self.output_tokens

        result = self.result

        stop_reason: None | str | Unset
        if isinstance(self.stop_reason, Unset):
            stop_reason = UNSET
        else:
            stop_reason = self.stop_reason

        summary: None | str | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        else:
            summary = self.summary

        total_tokens: int | None | Unset
        if isinstance(self.total_tokens, Unset):
            total_tokens = UNSET
        else:
            total_tokens = self.total_tokens

        turn_count: int | None | Unset
        if isinstance(self.turn_count, Unset):
            turn_count = UNSET
        else:
            turn_count = self.turn_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date_added": date_added,
                "date_updated": date_updated,
                "engine_version": engine_version,
                "id": id,
                "job_ref": job_ref,
                "result_type": result_type,
                "run_id": run_id,
            }
        )
        if agent_status is not UNSET:
            field_dict["agent_status"] = agent_status
        if cost_usd is not UNSET:
            field_dict["cost_usd"] = cost_usd
        if input_tokens is not UNSET:
            field_dict["input_tokens"] = input_tokens
        if loop_type is not UNSET:
            field_dict["loop_type"] = loop_type
        if model is not UNSET:
            field_dict["model"] = model
        if output_tokens is not UNSET:
            field_dict["output_tokens"] = output_tokens
        if result is not UNSET:
            field_dict["result"] = result
        if stop_reason is not UNSET:
            field_dict["stop_reason"] = stop_reason
        if summary is not UNSET:
            field_dict["summary"] = summary
        if total_tokens is not UNSET:
            field_dict["total_tokens"] = total_tokens
        if turn_count is not UNSET:
            field_dict["turn_count"] = turn_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date_added = isoparse(d.pop("date_added"))

        date_updated = isoparse(d.pop("date_updated"))

        engine_version = d.pop("engine_version")

        id = UUID(d.pop("id"))

        job_ref = d.pop("job_ref")

        result_type = d.pop("result_type")

        run_id = UUID(d.pop("run_id"))

        def _parse_agent_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agent_status = _parse_agent_status(d.pop("agent_status", UNSET))

        def _parse_cost_usd(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        cost_usd = _parse_cost_usd(d.pop("cost_usd", UNSET))

        def _parse_input_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        input_tokens = _parse_input_tokens(d.pop("input_tokens", UNSET))

        def _parse_loop_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        loop_type = _parse_loop_type(d.pop("loop_type", UNSET))

        def _parse_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_output_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        output_tokens = _parse_output_tokens(d.pop("output_tokens", UNSET))

        result = d.pop("result", UNSET)

        def _parse_stop_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        stop_reason = _parse_stop_reason(d.pop("stop_reason", UNSET))

        def _parse_summary(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        summary = _parse_summary(d.pop("summary", UNSET))

        def _parse_total_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_tokens = _parse_total_tokens(d.pop("total_tokens", UNSET))

        def _parse_turn_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        turn_count = _parse_turn_count(d.pop("turn_count", UNSET))

        job_result_response = cls(
            date_added=date_added,
            date_updated=date_updated,
            engine_version=engine_version,
            id=id,
            job_ref=job_ref,
            result_type=result_type,
            run_id=run_id,
            agent_status=agent_status,
            cost_usd=cost_usd,
            input_tokens=input_tokens,
            loop_type=loop_type,
            model=model,
            output_tokens=output_tokens,
            result=result,
            stop_reason=stop_reason,
            summary=summary,
            total_tokens=total_tokens,
            turn_count=turn_count,
        )

        job_result_response.additional_properties = d
        return job_result_response

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
