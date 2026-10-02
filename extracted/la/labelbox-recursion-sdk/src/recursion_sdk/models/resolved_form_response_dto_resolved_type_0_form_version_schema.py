from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.resolved_form_response_dto_resolved_type_0_form_version_schema_data import ResolvedFormResponseDtoResolvedType0FormVersionSchemaData
  from ..models.resolved_form_response_dto_resolved_type_0_form_version_schema_ui import ResolvedFormResponseDtoResolvedType0FormVersionSchemaUi





T = TypeVar("T", bound="ResolvedFormResponseDtoResolvedType0FormVersionSchema")



@_attrs_define
class ResolvedFormResponseDtoResolvedType0FormVersionSchema:
    """ Field schema and UI hints captured by this version.

        Attributes:
            data (ResolvedFormResponseDtoResolvedType0FormVersionSchemaData): JSON Schema describing the form fields.
            ui (ResolvedFormResponseDtoResolvedType0FormVersionSchemaUi): UI schema controlling presentation of the form
                fields.
     """

    data: ResolvedFormResponseDtoResolvedType0FormVersionSchemaData
    ui: ResolvedFormResponseDtoResolvedType0FormVersionSchemaUi





    def to_dict(self) -> dict[str, Any]:
        from ..models.resolved_form_response_dto_resolved_type_0_form_version_schema_data import ResolvedFormResponseDtoResolvedType0FormVersionSchemaData # noqa: PLC0415
        from ..models.resolved_form_response_dto_resolved_type_0_form_version_schema_ui import ResolvedFormResponseDtoResolvedType0FormVersionSchemaUi # noqa: PLC0415
        data = self.data.to_dict()

        ui = self.ui.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "data": data,
            "ui": ui,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resolved_form_response_dto_resolved_type_0_form_version_schema_data import ResolvedFormResponseDtoResolvedType0FormVersionSchemaData # noqa: PLC0415
        from ..models.resolved_form_response_dto_resolved_type_0_form_version_schema_ui import ResolvedFormResponseDtoResolvedType0FormVersionSchemaUi # noqa: PLC0415
        d = dict(src_dict)
        data = ResolvedFormResponseDtoResolvedType0FormVersionSchemaData.from_dict(d.pop("data"))




        ui = ResolvedFormResponseDtoResolvedType0FormVersionSchemaUi.from_dict(d.pop("ui"))




        resolved_form_response_dto_resolved_type_0_form_version_schema = cls(
            data=data,
            ui=ui,
        )

        return resolved_form_response_dto_resolved_type_0_form_version_schema

