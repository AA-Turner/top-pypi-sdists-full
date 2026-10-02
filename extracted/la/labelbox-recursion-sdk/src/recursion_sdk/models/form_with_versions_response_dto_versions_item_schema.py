from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.form_with_versions_response_dto_versions_item_schema_data import FormWithVersionsResponseDtoVersionsItemSchemaData
  from ..models.form_with_versions_response_dto_versions_item_schema_ui import FormWithVersionsResponseDtoVersionsItemSchemaUi





T = TypeVar("T", bound="FormWithVersionsResponseDtoVersionsItemSchema")



@_attrs_define
class FormWithVersionsResponseDtoVersionsItemSchema:
    """ Field schema and UI hints captured by this version.

        Attributes:
            data (FormWithVersionsResponseDtoVersionsItemSchemaData): JSON Schema describing the form fields.
            ui (FormWithVersionsResponseDtoVersionsItemSchemaUi): UI schema controlling presentation of the form fields.
     """

    data: FormWithVersionsResponseDtoVersionsItemSchemaData
    ui: FormWithVersionsResponseDtoVersionsItemSchemaUi





    def to_dict(self) -> dict[str, Any]:
        from ..models.form_with_versions_response_dto_versions_item_schema_data import FormWithVersionsResponseDtoVersionsItemSchemaData # noqa: PLC0415
        from ..models.form_with_versions_response_dto_versions_item_schema_ui import FormWithVersionsResponseDtoVersionsItemSchemaUi # noqa: PLC0415
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
        from ..models.form_with_versions_response_dto_versions_item_schema_data import FormWithVersionsResponseDtoVersionsItemSchemaData # noqa: PLC0415
        from ..models.form_with_versions_response_dto_versions_item_schema_ui import FormWithVersionsResponseDtoVersionsItemSchemaUi # noqa: PLC0415
        d = dict(src_dict)
        data = FormWithVersionsResponseDtoVersionsItemSchemaData.from_dict(d.pop("data"))




        ui = FormWithVersionsResponseDtoVersionsItemSchemaUi.from_dict(d.pop("ui"))




        form_with_versions_response_dto_versions_item_schema = cls(
            data=data,
            ui=ui,
        )

        return form_with_versions_response_dto_versions_item_schema

