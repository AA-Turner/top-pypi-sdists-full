from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.organization_form_list_response_dto_forms_item import OrganizationFormListResponseDtoFormsItem





T = TypeVar("T", bound="OrganizationFormListResponseDto")



@_attrs_define
class OrganizationFormListResponseDto:
    """ Response listing the form bundles in an organization catalog.

        Example:
            {'forms': [{'form': {'id': '8f0a9cbe-5235-412f-b4b9-8241d4099661', 'title': 'Defect Severity Rubric',
                'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-16T14:20:00.000Z'}, 'organizationId': '60b52abd-
                bbea-4c69-987a-103cfd752060', 'latestPublishedVersionNumber': 1, 'attachedAt': '2026-01-16T14:20:00.000Z'}]}

        Attributes:
            forms (list[OrganizationFormListResponseDtoFormsItem]): Form bundles attached to the organization, ordered by
                most-recently-attached.
     """

    forms: list[OrganizationFormListResponseDtoFormsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.organization_form_list_response_dto_forms_item import OrganizationFormListResponseDtoFormsItem # noqa: PLC0415
        forms = []
        for forms_item_data in self.forms:
            forms_item = forms_item_data.to_dict()
            forms.append(forms_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "forms": forms,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_form_list_response_dto_forms_item import OrganizationFormListResponseDtoFormsItem # noqa: PLC0415
        d = dict(src_dict)
        forms = []
        _forms = d.pop("forms")
        for forms_item_data in (_forms):
            forms_item = OrganizationFormListResponseDtoFormsItem.from_dict(forms_item_data)



            forms.append(forms_item)


        organization_form_list_response_dto = cls(
            forms=forms,
        )

        return organization_form_list_response_dto

