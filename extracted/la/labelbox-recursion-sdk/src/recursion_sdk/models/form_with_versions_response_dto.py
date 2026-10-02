from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.form_with_versions_response_dto_form import FormWithVersionsResponseDtoForm
  from ..models.form_with_versions_response_dto_versions_item import FormWithVersionsResponseDtoVersionsItem





T = TypeVar("T", bound="FormWithVersionsResponseDto")



@_attrs_define
class FormWithVersionsResponseDto:
    """ Response bundling a form with the full list of its versions.

        Example:
            {'form': {'id': '8f0a9cbe-5235-412f-b4b9-8241d4099661', 'title': 'Defect Severity Rubric', 'createdAt':
                '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-16T14:20:00.000Z'}, 'versions': [{'id':
                '77e4ffc9-3d40-472c-b160-f163e02df324', 'formId': '8f0a9cbe-5235-412f-b4b9-8241d4099661', 'versionNumber': 1,
                'schema': {'data': {'type': 'object', 'required': ['severity'], 'properties': {'severity': {'type': 'string',
                'title': 'Defect severity', 'enum': ['none', 'minor', 'major', 'critical']}, 'notes': {'type': 'string',
                'title': 'Reviewer notes'}}}, 'ui': {'severity': {'ui:widget': 'radio'}, 'notes': {'ui:widget': 'textarea'}}},
                'publishedAt': '2026-01-16T14:20:00.000Z', 'publishedByUserId': '49dea803-7390-49c4-abb1-5629718fc9cd',
                'updatedByUserId': '49dea803-7390-49c4-abb1-5629718fc9cd', 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt':
                '2026-01-16T14:20:00.000Z'}]}

        Attributes:
            form (FormWithVersionsResponseDtoForm): The form metadata.
            versions (list[FormWithVersionsResponseDtoVersionsItem]): All versions of the form, ordered by creation time.
     """

    form: FormWithVersionsResponseDtoForm
    versions: list[FormWithVersionsResponseDtoVersionsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.form_with_versions_response_dto_form import FormWithVersionsResponseDtoForm # noqa: PLC0415
        from ..models.form_with_versions_response_dto_versions_item import FormWithVersionsResponseDtoVersionsItem # noqa: PLC0415
        form = self.form.to_dict()

        versions = []
        for versions_item_data in self.versions:
            versions_item = versions_item_data.to_dict()
            versions.append(versions_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "form": form,
            "versions": versions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.form_with_versions_response_dto_form import FormWithVersionsResponseDtoForm # noqa: PLC0415
        from ..models.form_with_versions_response_dto_versions_item import FormWithVersionsResponseDtoVersionsItem # noqa: PLC0415
        d = dict(src_dict)
        form = FormWithVersionsResponseDtoForm.from_dict(d.pop("form"))




        versions = []
        _versions = d.pop("versions")
        for versions_item_data in (_versions):
            versions_item = FormWithVersionsResponseDtoVersionsItem.from_dict(versions_item_data)



            versions.append(versions_item)


        form_with_versions_response_dto = cls(
            form=form,
            versions=versions,
        )

        return form_with_versions_response_dto

