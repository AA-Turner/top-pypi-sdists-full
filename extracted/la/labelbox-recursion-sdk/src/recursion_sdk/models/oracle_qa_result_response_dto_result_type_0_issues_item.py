from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.oracle_qa_result_response_dto_result_type_0_issues_item_severity import OracleQaResultResponseDtoResultType0IssuesItemSeverity






T = TypeVar("T", bound="OracleQaResultResponseDtoResultType0IssuesItem")



@_attrs_define
class OracleQaResultResponseDtoResultType0IssuesItem:
    """ Single issue surfaced by a QA evaluation, attached to a QA job result.

        Attributes:
            type_ (str): Category label for the issue, defined by the QA image.
            severity (OracleQaResultResponseDtoResultType0IssuesItemSeverity): Severity level: an error blocks acceptance, a
                warning highlights a concern, and info is purely informational.
            description (str): Human-readable explanation of the issue.
     """

    type_: str
    severity: OracleQaResultResponseDtoResultType0IssuesItemSeverity
    description: str





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        severity = self.severity.value

        description = self.description


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
            "severity": severity,
            "description": description,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        severity = OracleQaResultResponseDtoResultType0IssuesItemSeverity(d.pop("severity"))




        description = d.pop("description")

        oracle_qa_result_response_dto_result_type_0_issues_item = cls(
            type_=type_,
            severity=severity,
            description=description,
        )

        return oracle_qa_result_response_dto_result_type_0_issues_item

