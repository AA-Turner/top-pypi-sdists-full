from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define

from ..models.runtime_image_build_architecture import RuntimeImageBuildArchitecture
from ..models.runtime_image_build_status import RuntimeImageBuildStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.runtime_image_build_attempt import RuntimeImageBuildAttempt


T = TypeVar("T", bound="RuntimeImageBuild")


@_attrs_define
class RuntimeImageBuild:
    """
    Attributes:
        id (UUID):
        name (str):
        architecture (RuntimeImageBuildArchitecture):
        status (RuntimeImageBuildStatus):
        attempt (int):
        runtime_image_id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        runtime_bundle_index_digest (str | Unset):
        runtime_bundle_manifest_digest (str | Unset):
        safe_error_code (str | Unset):
        completed_at (datetime.datetime | Unset):
        dockerfile (str | Unset):
        attempts (list[RuntimeImageBuildAttempt] | Unset):
    """

    id: UUID
    name: str
    architecture: RuntimeImageBuildArchitecture
    status: RuntimeImageBuildStatus
    attempt: int
    runtime_image_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    runtime_bundle_index_digest: str | Unset = UNSET
    runtime_bundle_manifest_digest: str | Unset = UNSET
    safe_error_code: str | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET
    dockerfile: str | Unset = UNSET
    attempts: list[RuntimeImageBuildAttempt] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        architecture = self.architecture.value

        status = self.status.value

        attempt = self.attempt

        runtime_image_id = self.runtime_image_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        runtime_bundle_index_digest = self.runtime_bundle_index_digest

        runtime_bundle_manifest_digest = self.runtime_bundle_manifest_digest

        safe_error_code = self.safe_error_code

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        dockerfile = self.dockerfile

        attempts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.attempts, Unset):
            attempts = []
            for attempts_item_data in self.attempts:
                attempts_item = attempts_item_data.to_dict()
                attempts.append(attempts_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "name": name,
                "architecture": architecture,
                "status": status,
                "attempt": attempt,
                "runtime_image_id": runtime_image_id,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if runtime_bundle_index_digest is not UNSET:
            field_dict["runtime_bundle_index_digest"] = runtime_bundle_index_digest
        if runtime_bundle_manifest_digest is not UNSET:
            field_dict["runtime_bundle_manifest_digest"] = (
                runtime_bundle_manifest_digest
            )
        if safe_error_code is not UNSET:
            field_dict["safe_error_code"] = safe_error_code
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if dockerfile is not UNSET:
            field_dict["dockerfile"] = dockerfile
        if attempts is not UNSET:
            field_dict["attempts"] = attempts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.runtime_image_build_attempt import RuntimeImageBuildAttempt

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        architecture = RuntimeImageBuildArchitecture(d.pop("architecture"))

        status = RuntimeImageBuildStatus(d.pop("status"))

        attempt = d.pop("attempt")

        runtime_image_id = d.pop("runtime_image_id")

        created_at = datetime.datetime.fromisoformat(
            d.pop("created_at").replace("Z", "+00:00")
        )

        updated_at = datetime.datetime.fromisoformat(
            d.pop("updated_at").replace("Z", "+00:00")
        )

        runtime_bundle_index_digest = d.pop("runtime_bundle_index_digest", UNSET)

        runtime_bundle_manifest_digest = d.pop("runtime_bundle_manifest_digest", UNSET)

        safe_error_code = d.pop("safe_error_code", UNSET)

        _completed_at = d.pop("completed_at", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = datetime.datetime.fromisoformat(
                _completed_at.replace("Z", "+00:00")
            )

        dockerfile = d.pop("dockerfile", UNSET)

        _attempts = d.pop("attempts", UNSET)
        attempts: list[RuntimeImageBuildAttempt] | Unset = UNSET
        if _attempts is not UNSET:
            attempts = []
            for attempts_item_data in _attempts:
                attempts_item = RuntimeImageBuildAttempt.from_dict(attempts_item_data)

                attempts.append(attempts_item)

        runtime_image_build = cls(
            id=id,
            name=name,
            architecture=architecture,
            status=status,
            attempt=attempt,
            runtime_image_id=runtime_image_id,
            created_at=created_at,
            updated_at=updated_at,
            runtime_bundle_index_digest=runtime_bundle_index_digest,
            runtime_bundle_manifest_digest=runtime_bundle_manifest_digest,
            safe_error_code=safe_error_code,
            completed_at=completed_at,
            dockerfile=dockerfile,
            attempts=attempts,
        )

        return runtime_image_build
