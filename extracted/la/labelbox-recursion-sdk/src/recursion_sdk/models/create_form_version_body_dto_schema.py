from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.create_form_version_body_dto_schema_data import CreateFormVersionBodyDtoSchemaData
  from ..models.create_form_version_body_dto_schema_ui import CreateFormVersionBodyDtoSchemaUi





T = TypeVar("T", bound="CreateFormVersionBodyDtoSchema")



@_attrs_define
class CreateFormVersionBodyDtoSchema:
    """ Optional initial schema for the new draft; defaults to a copy of the previous version when omitted.

        Attributes:
            data (CreateFormVersionBodyDtoSchemaData): JSON Schema describing the form fields.
            ui (CreateFormVersionBodyDtoSchemaUi): UI schema controlling presentation of the form fields.
     """

    data: CreateFormVersionBodyDtoSchemaData
    ui: CreateFormVersionBodyDtoSchemaUi
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_form_version_body_dto_schema_data import CreateFormVersionBodyDtoSchemaData # noqa: PLC0415
        from ..models.create_form_version_body_dto_schema_ui import CreateFormVersionBodyDtoSchemaUi # noqa: PLC0415
        data = self.data.to_dict()

        ui = self.ui.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "data": data,
            "ui": ui,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_form_version_body_dto_schema_data import CreateFormVersionBodyDtoSchemaData # noqa: PLC0415
        from ..models.create_form_version_body_dto_schema_ui import CreateFormVersionBodyDtoSchemaUi # noqa: PLC0415
        d = dict(src_dict)
        data = CreateFormVersionBodyDtoSchemaData.from_dict(d.pop("data"))




        ui = CreateFormVersionBodyDtoSchemaUi.from_dict(d.pop("ui"))




        create_form_version_body_dto_schema = cls(
            data=data,
            ui=ui,
        )


        create_form_version_body_dto_schema.additional_properties = d
        return create_form_version_body_dto_schema

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
