from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.form_with_initial_version_response_dto_version_schema_data import FormWithInitialVersionResponseDtoVersionSchemaData
  from ..models.form_with_initial_version_response_dto_version_schema_ui import FormWithInitialVersionResponseDtoVersionSchemaUi





T = TypeVar("T", bound="FormWithInitialVersionResponseDtoVersionSchema")



@_attrs_define
class FormWithInitialVersionResponseDtoVersionSchema:
    """ Field schema and UI hints captured by this version.

        Attributes:
            data (FormWithInitialVersionResponseDtoVersionSchemaData): JSON Schema describing the form fields.
            ui (FormWithInitialVersionResponseDtoVersionSchemaUi): UI schema controlling presentation of the form fields.
     """

    data: FormWithInitialVersionResponseDtoVersionSchemaData
    ui: FormWithInitialVersionResponseDtoVersionSchemaUi





    def to_dict(self) -> dict[str, Any]:
        from ..models.form_with_initial_version_response_dto_version_schema_data import FormWithInitialVersionResponseDtoVersionSchemaData # noqa: PLC0415
        from ..models.form_with_initial_version_response_dto_version_schema_ui import FormWithInitialVersionResponseDtoVersionSchemaUi # noqa: PLC0415
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
        from ..models.form_with_initial_version_response_dto_version_schema_data import FormWithInitialVersionResponseDtoVersionSchemaData # noqa: PLC0415
        from ..models.form_with_initial_version_response_dto_version_schema_ui import FormWithInitialVersionResponseDtoVersionSchemaUi # noqa: PLC0415
        d = dict(src_dict)
        data = FormWithInitialVersionResponseDtoVersionSchemaData.from_dict(d.pop("data"))




        ui = FormWithInitialVersionResponseDtoVersionSchemaUi.from_dict(d.pop("ui"))




        form_with_initial_version_response_dto_version_schema = cls(
            data=data,
            ui=ui,
        )

        return form_with_initial_version_response_dto_version_schema

