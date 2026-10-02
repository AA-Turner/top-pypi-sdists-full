from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_form_version_body_dto_schema import CreateFormVersionBodyDtoSchema





T = TypeVar("T", bound="CreateFormVersionBodyDto")



@_attrs_define
class CreateFormVersionBodyDto:
    """ Request body for creating a new draft version of an existing form.

        Example:
            {'schema': {'data': {'type': 'object', 'required': ['severity'], 'properties': {'severity': {'type': 'string',
                'title': 'Defect severity', 'enum': ['none', 'minor', 'major', 'critical']}, 'notes': {'type': 'string',
                'title': 'Reviewer notes'}}}, 'ui': {'severity': {'ui:widget': 'radio'}, 'notes': {'ui:widget': 'textarea'}}}}

        Attributes:
            schema (CreateFormVersionBodyDtoSchema | Unset): Optional initial schema for the new draft; defaults to a copy
                of the previous version when omitted.
     """

    schema: CreateFormVersionBodyDtoSchema | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_form_version_body_dto_schema import CreateFormVersionBodyDtoSchema # noqa: PLC0415
        schema: dict[str, Any] | Unset = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_form_version_body_dto_schema import CreateFormVersionBodyDtoSchema # noqa: PLC0415
        d = dict(src_dict)
        _schema = d.pop("schema", UNSET)
        schema: CreateFormVersionBodyDtoSchema | Unset
        if isinstance(_schema,  Unset):
            schema = UNSET
        else:
            schema = CreateFormVersionBodyDtoSchema.from_dict(_schema)




        create_form_version_body_dto = cls(
            schema=schema,
        )


        create_form_version_body_dto.additional_properties = d
        return create_form_version_body_dto

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
