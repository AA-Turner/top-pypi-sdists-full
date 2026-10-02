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
  from ..models.form_version_dto_schema import FormVersionDtoSchema





T = TypeVar("T", bound="FormVersionDto")



@_attrs_define
class FormVersionDto:
    """ One version of a form. Versions follow a draft to published lifecycle and answers are tied to a specific version.

        Example:
            {'id': '77e4ffc9-3d40-472c-b160-f163e02df324', 'formId': '8f0a9cbe-5235-412f-b4b9-8241d4099661',
                'versionNumber': 1, 'schema': {'data': {'type': 'object', 'required': ['severity'], 'properties': {'severity':
                {'type': 'string', 'title': 'Defect severity', 'enum': ['none', 'minor', 'major', 'critical']}, 'notes':
                {'type': 'string', 'title': 'Reviewer notes'}}}, 'ui': {'severity': {'ui:widget': 'radio'}, 'notes':
                {'ui:widget': 'textarea'}}}, 'publishedAt': '2026-01-16T14:20:00.000Z', 'publishedByUserId':
                '49dea803-7390-49c4-abb1-5629718fc9cd', 'updatedByUserId': '49dea803-7390-49c4-abb1-5629718fc9cd', 'createdAt':
                '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-16T14:20:00.000Z'}

        Attributes:
            id (UUID): Stable form-version identifier (UUID).
            form_id (UUID): Parent form this version belongs to.
            version_number (int): Monotonically increasing version number, starting at 1 for the first version. Example: 1.
            schema (FormVersionDtoSchema): Field schema and UI hints captured by this version.
            published_at (datetime.datetime | None): Timestamp when this version was published (ISO-8601, UTC). Null for
                drafts.
            published_by_user_id (None | UUID): User who published this version; null for drafts that have not yet been
                published.
            updated_by_user_id (UUID): User who last edited this version.
            created_at (datetime.datetime): Timestamp when this version was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when this version was last updated (ISO-8601, UTC).
     """

    id: UUID
    form_id: UUID
    version_number: int
    schema: FormVersionDtoSchema
    published_at: datetime.datetime | None
    published_by_user_id: None | UUID
    updated_by_user_id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        from ..models.form_version_dto_schema import FormVersionDtoSchema # noqa: PLC0415
        id = str(self.id)

        form_id = str(self.form_id)

        version_number = self.version_number

        schema = self.schema.to_dict()

        published_at: None | str
        if isinstance(self.published_at, datetime.datetime):
            published_at = self.published_at.isoformat()
        else:
            published_at = self.published_at

        published_by_user_id: None | str
        if isinstance(self.published_by_user_id, UUID):
            published_by_user_id = str(self.published_by_user_id)
        else:
            published_by_user_id = self.published_by_user_id

        updated_by_user_id = str(self.updated_by_user_id)

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "formId": form_id,
            "versionNumber": version_number,
            "schema": schema,
            "publishedAt": published_at,
            "publishedByUserId": published_by_user_id,
            "updatedByUserId": updated_by_user_id,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.form_version_dto_schema import FormVersionDtoSchema # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        form_id = UUID(d.pop("formId"))




        version_number = d.pop("versionNumber")

        schema = FormVersionDtoSchema.from_dict(d.pop("schema"))




        def _parse_published_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                published_at_type_0 = datetime.datetime.fromisoformat(data)



                return published_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        published_at = _parse_published_at(d.pop("publishedAt"))


        def _parse_published_by_user_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                published_by_user_id_type_0 = UUID(data)



                return published_by_user_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        published_by_user_id = _parse_published_by_user_id(d.pop("publishedByUserId"))


        updated_by_user_id = UUID(d.pop("updatedByUserId"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        form_version_dto = cls(
            id=id,
            form_id=form_id,
            version_number=version_number,
            schema=schema,
            published_at=published_at,
            published_by_user_id=published_by_user_id,
            updated_by_user_id=updated_by_user_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        return form_version_dto

