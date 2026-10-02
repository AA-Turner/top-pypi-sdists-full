from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.taiga_image_dto_build_status import TaigaImageDtoBuildStatus
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="TaigaImageDto")



@_attrs_define
class TaigaImageDto:
    """ One row in the org-scoped Taiga image catalog.

        Attributes:
            id (UUID): Stable identifier (UUID) for a row in the org-scoped Taiga image catalog.
            organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
            name (str): User-facing label for a catalog entry. Unique within an org so the env integration picker is
                unambiguous.
            description (None | str): Optional human notes about the image — what was built, when, with which deps.
            user_dockerfile (str): Free-form Dockerfile lines authored by the user. Inserted between the platform-managed
                head + tail templates at build time. Typically 'RUN pip install …' or 'RUN apt-get install …' — see the dialog's
                preview for the full assembled file. Empty means 'platform base, no extras'.
            build_status (TaigaImageDtoBuildStatus): Build lifecycle of a Taiga image catalog row.
            cloud_build_id (None | str): Google Cloud Build operation id. Set when the build is submitted; null while in
                'pending'.
            build_log_url (None | str): Cloud Build console URL — exposed in the admin UI as "View logs".
            build_error (None | str): Failure message from the build worker — set only when buildStatus = 'failed'.
            built_image_url (None | str): Resolved registry URI (with digest) once the build succeeds. Null until
                buildStatus = 'ready'.
            taiga_source_uploaded_at (datetime.datetime | None): ISO-8601 UTC timestamp of the successful POST /api/docker-
                images/register on Taiga. Null until the taiga_image_source_upload JobsV2 child completes. Populated
                independently from buildStatus — a row can be 'ready' for a short window before source upload finishes.
            taiga_source_id (None | str): Taiga-side docker-image uuid returned by POST /api/docker-images/register. Stored
                for cross-reference; not a foreign key (Taiga owns the lifetime of that row).
            taiga_source_path (None | str): Taiga-side source-tarball path returned by POST /api/docker-images/register —
                the location where Taiga claims the uploaded tarball was stored. Nullable: per a 2026-06-17 audit of
                taiga.ant.dev, legacy direct-POST uploads leave this null; only the new presigned-PUT flow populates it. Surface
                as a post-mortem "where did it go" pointer; the bytes can be re-fetched via Taiga's docker-image download
                endpoint.
            created_by_id (None | UUID): User who created this catalog entry; null for legacy or system-created entries.
            created_at (datetime.datetime): ISO-8601 UTC timestamp when the catalog entry was created.
            updated_at (datetime.datetime): ISO-8601 UTC timestamp when the catalog entry was last updated.
     """

    id: UUID
    organization_id: UUID
    name: str
    description: None | str
    user_dockerfile: str
    build_status: TaigaImageDtoBuildStatus
    cloud_build_id: None | str
    build_log_url: None | str
    build_error: None | str
    built_image_url: None | str
    taiga_source_uploaded_at: datetime.datetime | None
    taiga_source_id: None | str
    taiga_source_path: None | str
    created_by_id: None | UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        organization_id = str(self.organization_id)

        name = self.name

        description: None | str
        description = self.description

        user_dockerfile = self.user_dockerfile

        build_status = self.build_status.value

        cloud_build_id: None | str
        cloud_build_id = self.cloud_build_id

        build_log_url: None | str
        build_log_url = self.build_log_url

        build_error: None | str
        build_error = self.build_error

        built_image_url: None | str
        built_image_url = self.built_image_url

        taiga_source_uploaded_at: None | str
        if isinstance(self.taiga_source_uploaded_at, datetime.datetime):
            taiga_source_uploaded_at = self.taiga_source_uploaded_at.isoformat()
        else:
            taiga_source_uploaded_at = self.taiga_source_uploaded_at

        taiga_source_id: None | str
        taiga_source_id = self.taiga_source_id

        taiga_source_path: None | str
        taiga_source_path = self.taiga_source_path

        created_by_id: None | str
        if isinstance(self.created_by_id, UUID):
            created_by_id = str(self.created_by_id)
        else:
            created_by_id = self.created_by_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "organizationId": organization_id,
            "name": name,
            "description": description,
            "userDockerfile": user_dockerfile,
            "buildStatus": build_status,
            "cloudBuildId": cloud_build_id,
            "buildLogUrl": build_log_url,
            "buildError": build_error,
            "builtImageUrl": built_image_url,
            "taigaSourceUploadedAt": taiga_source_uploaded_at,
            "taigaSourceId": taiga_source_id,
            "taigaSourcePath": taiga_source_path,
            "createdById": created_by_id,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        organization_id = UUID(d.pop("organizationId"))




        name = d.pop("name")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))


        user_dockerfile = d.pop("userDockerfile")

        build_status = TaigaImageDtoBuildStatus(d.pop("buildStatus"))




        def _parse_cloud_build_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        cloud_build_id = _parse_cloud_build_id(d.pop("cloudBuildId"))


        def _parse_build_log_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        build_log_url = _parse_build_log_url(d.pop("buildLogUrl"))


        def _parse_build_error(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        build_error = _parse_build_error(d.pop("buildError"))


        def _parse_built_image_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        built_image_url = _parse_built_image_url(d.pop("builtImageUrl"))


        def _parse_taiga_source_uploaded_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                taiga_source_uploaded_at_type_0 = datetime.datetime.fromisoformat(data)



                return taiga_source_uploaded_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        taiga_source_uploaded_at = _parse_taiga_source_uploaded_at(d.pop("taigaSourceUploadedAt"))


        def _parse_taiga_source_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        taiga_source_id = _parse_taiga_source_id(d.pop("taigaSourceId"))


        def _parse_taiga_source_path(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        taiga_source_path = _parse_taiga_source_path(d.pop("taigaSourcePath"))


        def _parse_created_by_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_by_id_type_0 = UUID(data)



                return created_by_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        created_by_id = _parse_created_by_id(d.pop("createdById"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        taiga_image_dto = cls(
            id=id,
            organization_id=organization_id,
            name=name,
            description=description,
            user_dockerfile=user_dockerfile,
            build_status=build_status,
            cloud_build_id=cloud_build_id,
            build_log_url=build_log_url,
            build_error=build_error,
            built_image_url=built_image_url,
            taiga_source_uploaded_at=taiga_source_uploaded_at,
            taiga_source_id=taiga_source_id,
            taiga_source_path=taiga_source_path,
            created_by_id=created_by_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        return taiga_image_dto

