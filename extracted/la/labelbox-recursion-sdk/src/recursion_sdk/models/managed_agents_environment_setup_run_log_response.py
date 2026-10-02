from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_environment_setup_run_log_chunk import ManagedAgentsEnvironmentSetupRunLogChunk





T = TypeVar("T", bound="ManagedAgentsEnvironmentSetupRunLogResponse")



@_attrs_define
class ManagedAgentsEnvironmentSetupRunLogResponse:
    """ A page of a setup run's log with the cursor for the next page. stdout, stderr, marker (the script line about to
    run), and system (control-plane phase notes) are interleaved in capture order.

        Example:
            {'lines': [{'at': '2026-02-18T09:30:00Z', 'line': 1, 'seq': 1, 'stream': 'example', 'text': 'example'}],
                'next_after': 1, 'status': 'example', 'truncated': True}

        Attributes:
            lines (list[ManagedAgentsEnvironmentSetupRunLogChunk] | None): Log lines after the requested cursor, in order.
                Empty when the run has produced nothing new within the wait.
            next_after (int): Cursor to pass as after on the next call. Equal to the request's after when no new lines were
                returned.
            status (str): The run's status when the page was read. Stop tailing once it is succeeded, failed, or cancelled
                and the page is empty.
            truncated (bool | Unset): True when the run produced more output than is kept (4 MiB). The head is retained; the
                stderr tail is on the run.
     """

    lines: list[ManagedAgentsEnvironmentSetupRunLogChunk] | None
    next_after: int
    status: str
    truncated: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_environment_setup_run_log_chunk import ManagedAgentsEnvironmentSetupRunLogChunk # noqa: PLC0415
        lines: list[dict[str, Any]] | None
        if isinstance(self.lines, list):
            lines = []
            for lines_type_0_item_data in self.lines:
                lines_type_0_item = lines_type_0_item_data.to_dict()
                lines.append(lines_type_0_item)


        else:
            lines = self.lines

        next_after = self.next_after

        status = self.status

        truncated = self.truncated


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "lines": lines,
            "next_after": next_after,
            "status": status,
        })
        if truncated is not UNSET:
            field_dict["truncated"] = truncated

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_environment_setup_run_log_chunk import ManagedAgentsEnvironmentSetupRunLogChunk # noqa: PLC0415
        d = dict(src_dict)
        def _parse_lines(data: object) -> list[ManagedAgentsEnvironmentSetupRunLogChunk] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                lines_type_0 = []
                _lines_type_0 = data
                for lines_type_0_item_data in (_lines_type_0):
                    lines_type_0_item = ManagedAgentsEnvironmentSetupRunLogChunk.from_dict(lines_type_0_item_data)



                    lines_type_0.append(lines_type_0_item)

                return lines_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsEnvironmentSetupRunLogChunk] | None, data)

        lines = _parse_lines(d.pop("lines"))


        next_after = d.pop("next_after")

        status = d.pop("status")

        truncated = d.pop("truncated", UNSET)

        managed_agents_environment_setup_run_log_response = cls(
            lines=lines,
            next_after=next_after,
            status=status,
            truncated=truncated,
        )


        managed_agents_environment_setup_run_log_response.additional_properties = d
        return managed_agents_environment_setup_run_log_response

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
