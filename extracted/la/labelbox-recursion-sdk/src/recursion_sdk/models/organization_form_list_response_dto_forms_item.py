from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.organization_form_list_response_dto_forms_item_form import OrganizationFormListResponseDtoFormsItemForm





T = TypeVar("T", bound="OrganizationFormListResponseDtoFormsItem")



@_attrs_define
class OrganizationFormListResponseDtoFormsItem:
    """ Summary entry for an org-attached form bundle, used by the org catalog and the env / problem picker.

        Attributes:
            form (OrganizationFormListResponseDtoFormsItemForm): The org-attached form bundle.
            organization_id (UUID): Owning organization.
            latest_published_version_number (int | None): Latest published version number for this bundle, or null when no
                version is published yet.
            attached_at (datetime.datetime): Timestamp when this bundle was attached at the organization scope (ISO-8601,
                UTC).
     """

    form: OrganizationFormListResponseDtoFormsItemForm
    organization_id: UUID
    latest_published_version_number: int | None
    attached_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        from ..models.organization_form_list_response_dto_forms_item_form import OrganizationFormListResponseDtoFormsItemForm # noqa: PLC0415
        form = self.form.to_dict()

        organization_id = str(self.organization_id)

        latest_published_version_number: int | None
        latest_published_version_number = self.latest_published_version_number

        attached_at = self.attached_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "form": form,
            "organizationId": organization_id,
            "latestPublishedVersionNumber": latest_published_version_number,
            "attachedAt": attached_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_form_list_response_dto_forms_item_form import OrganizationFormListResponseDtoFormsItemForm # noqa: PLC0415
        d = dict(src_dict)
        form = OrganizationFormListResponseDtoFormsItemForm.from_dict(d.pop("form"))




        organization_id = UUID(d.pop("organizationId"))




        def _parse_latest_published_version_number(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        latest_published_version_number = _parse_latest_published_version_number(d.pop("latestPublishedVersionNumber"))


        attached_at = datetime.datetime.fromisoformat(d.pop("attachedAt"))




        organization_form_list_response_dto_forms_item = cls(
            form=form,
            organization_id=organization_id,
            latest_published_version_number=latest_published_version_number,
            attached_at=attached_at,
        )

        return organization_form_list_response_dto_forms_item

