from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.resolved_field_permissions_dto_job_fields import ResolvedFieldPermissionsDtoJobFields
  from ..models.resolved_field_permissions_dto_version_fields import ResolvedFieldPermissionsDtoVersionFields





T = TypeVar("T", bound="ResolvedFieldPermissionsDto")



@_attrs_define
class ResolvedFieldPermissionsDto:
    """ Resolved per-field permission state for the current user in a given environment, after merging environment-level and
    user-level overrides on top of base permissions.

        Attributes:
            version_fields (ResolvedFieldPermissionsDtoVersionFields): Per-field editability map for problem-version fields
                (true = editable, false = locked).
            job_fields (ResolvedFieldPermissionsDtoJobFields): Per-field editability map for run-modal fields (true =
                editable, false = locked to the env template default).
            denied_permissions (list[str]): Resource:action permissions explicitly denied by overrides for this
                user/environment.
     """

    version_fields: ResolvedFieldPermissionsDtoVersionFields
    job_fields: ResolvedFieldPermissionsDtoJobFields
    denied_permissions: list[str]





    def to_dict(self) -> dict[str, Any]:
        from ..models.resolved_field_permissions_dto_job_fields import ResolvedFieldPermissionsDtoJobFields # noqa: PLC0415
        from ..models.resolved_field_permissions_dto_version_fields import ResolvedFieldPermissionsDtoVersionFields # noqa: PLC0415
        version_fields = self.version_fields.to_dict()

        job_fields = self.job_fields.to_dict()

        denied_permissions = self.denied_permissions




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "versionFields": version_fields,
            "jobFields": job_fields,
            "deniedPermissions": denied_permissions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resolved_field_permissions_dto_job_fields import ResolvedFieldPermissionsDtoJobFields # noqa: PLC0415
        from ..models.resolved_field_permissions_dto_version_fields import ResolvedFieldPermissionsDtoVersionFields # noqa: PLC0415
        d = dict(src_dict)
        version_fields = ResolvedFieldPermissionsDtoVersionFields.from_dict(d.pop("versionFields"))




        job_fields = ResolvedFieldPermissionsDtoJobFields.from_dict(d.pop("jobFields"))




        denied_permissions = cast(list[str], d.pop("deniedPermissions"))


        resolved_field_permissions_dto = cls(
            version_fields=version_fields,
            job_fields=job_fields,
            denied_permissions=denied_permissions,
        )

        return resolved_field_permissions_dto

