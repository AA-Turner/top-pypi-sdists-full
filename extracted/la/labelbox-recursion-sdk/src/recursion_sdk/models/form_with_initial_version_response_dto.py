from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.form_with_initial_version_response_dto_form import FormWithInitialVersionResponseDtoForm
  from ..models.form_with_initial_version_response_dto_version import FormWithInitialVersionResponseDtoVersion





T = TypeVar("T", bound="FormWithInitialVersionResponseDto")



@_attrs_define
class FormWithInitialVersionResponseDto:
    """ Response returned when creating a form alongside its first version in a single call.

        Example:
            {'form': {'id': '8f0a9cbe-5235-412f-b4b9-8241d4099661', 'title': 'Defect Severity Rubric', 'createdAt':
                '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-16T14:20:00.000Z'}, 'version': {'id':
                '77e4ffc9-3d40-472c-b160-f163e02df324', 'formId': '8f0a9cbe-5235-412f-b4b9-8241d4099661', 'versionNumber': 1,
                'schema': {'data': {'type': 'object', 'required': ['severity'], 'properties': {'severity': {'type': 'string',
                'title': 'Defect severity', 'enum': ['none', 'minor', 'major', 'critical']}, 'notes': {'type': 'string',
                'title': 'Reviewer notes'}}}, 'ui': {'severity': {'ui:widget': 'radio'}, 'notes': {'ui:widget': 'textarea'}}},
                'publishedAt': '2026-01-16T14:20:00.000Z', 'publishedByUserId': '49dea803-7390-49c4-abb1-5629718fc9cd',
                'updatedByUserId': '49dea803-7390-49c4-abb1-5629718fc9cd', 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt':
                '2026-01-16T14:20:00.000Z'}}

        Attributes:
            form (FormWithInitialVersionResponseDtoForm): The created form.
            version (FormWithInitialVersionResponseDtoVersion): The initial version associated with the form.
     """

    form: FormWithInitialVersionResponseDtoForm
    version: FormWithInitialVersionResponseDtoVersion





    def to_dict(self) -> dict[str, Any]:
        from ..models.form_with_initial_version_response_dto_form import FormWithInitialVersionResponseDtoForm # noqa: PLC0415
        from ..models.form_with_initial_version_response_dto_version import FormWithInitialVersionResponseDtoVersion # noqa: PLC0415
        form = self.form.to_dict()

        version = self.version.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "form": form,
            "version": version,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.form_with_initial_version_response_dto_form import FormWithInitialVersionResponseDtoForm # noqa: PLC0415
        from ..models.form_with_initial_version_response_dto_version import FormWithInitialVersionResponseDtoVersion # noqa: PLC0415
        d = dict(src_dict)
        form = FormWithInitialVersionResponseDtoForm.from_dict(d.pop("form"))




        version = FormWithInitialVersionResponseDtoVersion.from_dict(d.pop("version"))




        form_with_initial_version_response_dto = cls(
            form=form,
            version=version,
        )

        return form_with_initial_version_response_dto

