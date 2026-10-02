from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.form_version_dto_schema_data import FormVersionDtoSchemaData
  from ..models.form_version_dto_schema_ui import FormVersionDtoSchemaUi





T = TypeVar("T", bound="FormVersionDtoSchema")



@_attrs_define
class FormVersionDtoSchema:
    """ Field schema and UI hints captured by this version.

        Attributes:
            data (FormVersionDtoSchemaData): JSON Schema describing the form fields.
            ui (FormVersionDtoSchemaUi): UI schema controlling presentation of the form fields.
     """

    data: FormVersionDtoSchemaData
    ui: FormVersionDtoSchemaUi





    def to_dict(self) -> dict[str, Any]:
        from ..models.form_version_dto_schema_data import FormVersionDtoSchemaData # noqa: PLC0415
        from ..models.form_version_dto_schema_ui import FormVersionDtoSchemaUi # noqa: PLC0415
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
        from ..models.form_version_dto_schema_data import FormVersionDtoSchemaData # noqa: PLC0415
        from ..models.form_version_dto_schema_ui import FormVersionDtoSchemaUi # noqa: PLC0415
        d = dict(src_dict)
        data = FormVersionDtoSchemaData.from_dict(d.pop("data"))




        ui = FormVersionDtoSchemaUi.from_dict(d.pop("ui"))




        form_version_dto_schema = cls(
            data=data,
            ui=ui,
        )

        return form_version_dto_schema

