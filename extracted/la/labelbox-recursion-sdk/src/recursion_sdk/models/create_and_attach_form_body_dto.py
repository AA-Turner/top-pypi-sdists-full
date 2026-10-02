from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_and_attach_form_body_dto_schema import CreateAndAttachFormBodyDtoSchema





T = TypeVar("T", bound="CreateAndAttachFormBodyDto")



@_attrs_define
class CreateAndAttachFormBodyDto:
    """ Request body for creating a new form and attaching it to the target environment or problem.

        Example:
            {'title': 'Defect Severity Rubric', 'schema': {'data': {'type': 'object', 'required': ['severity'],
                'properties': {'severity': {'type': 'string', 'title': 'Defect severity', 'enum': ['none', 'minor', 'major',
                'critical']}, 'notes': {'type': 'string', 'title': 'Reviewer notes'}}}, 'ui': {'severity': {'ui:widget':
                'radio'}, 'notes': {'ui:widget': 'textarea'}}}}

        Attributes:
            title (str | Unset): Optional human-readable title for the new bundle. Trimmed; an empty string is treated as no
                title.
            schema (CreateAndAttachFormBodyDtoSchema | Unset): Optional initial schema for the new form; defaults to an
                empty schema when omitted.
     """

    title: str | Unset = UNSET
    schema: CreateAndAttachFormBodyDtoSchema | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_and_attach_form_body_dto_schema import CreateAndAttachFormBodyDtoSchema # noqa: PLC0415
        title = self.title

        schema: dict[str, Any] | Unset = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if title is not UNSET:
            field_dict["title"] = title
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_and_attach_form_body_dto_schema import CreateAndAttachFormBodyDtoSchema # noqa: PLC0415
        d = dict(src_dict)
        title = d.pop("title", UNSET)

        _schema = d.pop("schema", UNSET)
        schema: CreateAndAttachFormBodyDtoSchema | Unset
        if isinstance(_schema,  Unset):
            schema = UNSET
        else:
            schema = CreateAndAttachFormBodyDtoSchema.from_dict(_schema)




        create_and_attach_form_body_dto = cls(
            title=title,
            schema=schema,
        )


        create_and_attach_form_body_dto.additional_properties = d
        return create_and_attach_form_body_dto

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
