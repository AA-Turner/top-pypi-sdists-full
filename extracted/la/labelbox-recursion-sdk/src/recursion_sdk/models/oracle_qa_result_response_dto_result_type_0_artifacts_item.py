from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="OracleQaResultResponseDtoResultType0ArtifactsItem")



@_attrs_define
class OracleQaResultResponseDtoResultType0ArtifactsItem:
    """ Downloadable artifact produced by a QA container alongside its result JSON.

        Attributes:
            filename (str): Display name for the artifact as written by the QA container.
            url (str): HTTP(S) URL where the artifact bytes can be fetched.
     """

    filename: str
    url: str





    def to_dict(self) -> dict[str, Any]:
        filename = self.filename

        url = self.url


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "filename": filename,
            "url": url,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        filename = d.pop("filename")

        url = d.pop("url")

        oracle_qa_result_response_dto_result_type_0_artifacts_item = cls(
            filename=filename,
            url=url,
        )

        return oracle_qa_result_response_dto_result_type_0_artifacts_item

