from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="StageClearanceResponseDto")



@_attrs_define
class StageClearanceResponseDto:
    """ Outcome of a stage clearance request, including any issue created to record an override.

        Example:
            {'cleared': True, 'overrideIssueId': None}

        Attributes:
            cleared (bool): True if the stage was successfully cleared.
            override_issue_id (None | UUID): Issue created to record an override. Null when the stage was cleared without
                override.
     """

    cleared: bool
    override_issue_id: None | UUID





    def to_dict(self) -> dict[str, Any]:
        cleared = self.cleared

        override_issue_id: None | str
        if isinstance(self.override_issue_id, UUID):
            override_issue_id = str(self.override_issue_id)
        else:
            override_issue_id = self.override_issue_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "cleared": cleared,
            "overrideIssueId": override_issue_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cleared = d.pop("cleared")

        def _parse_override_issue_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                override_issue_id_type_0 = UUID(data)



                return override_issue_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        override_issue_id = _parse_override_issue_id(d.pop("overrideIssueId"))


        stage_clearance_response_dto = cls(
            cleared=cleared,
            override_issue_id=override_issue_id,
        )

        return stage_clearance_response_dto

