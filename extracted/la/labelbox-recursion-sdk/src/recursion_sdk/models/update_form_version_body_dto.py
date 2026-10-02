from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.update_form_version_body_dto_schema import UpdateFormVersionBodyDtoSchema





T = TypeVar("T", bound="UpdateFormVersionBodyDto")



@_attrs_define
class UpdateFormVersionBodyDto:
    """ Request body for replacing the schema content of a draft form version.

        Example:
            {'schema': {'data': {'type': 'object', 'required': ['severity'], 'properties': {'severity': {'type': 'string',
                'title': 'Defect severity', 'enum': ['none', 'minor', 'major', 'critical']}, 'notes': {'type': 'string',
                'title': 'Reviewer notes'}}}, 'ui': {'severity': {'ui:widget': 'radio'}, 'notes': {'ui:widget': 'textarea'}}}}

        Attributes:
            schema (UpdateFormVersionBodyDtoSchema): New schema content to overwrite the existing draft.
     """

    schema: UpdateFormVersionBodyDtoSchema
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.update_form_version_body_dto_schema import UpdateFormVersionBodyDtoSchema # noqa: PLC0415
        schema = self.schema.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "schema": schema,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_form_version_body_dto_schema import UpdateFormVersionBodyDtoSchema # noqa: PLC0415
        d = dict(src_dict)
        schema = UpdateFormVersionBodyDtoSchema.from_dict(d.pop("schema"))




        update_form_version_body_dto = cls(
            schema=schema,
        )


        update_form_version_body_dto.additional_properties = d
        return update_form_version_body_dto

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
