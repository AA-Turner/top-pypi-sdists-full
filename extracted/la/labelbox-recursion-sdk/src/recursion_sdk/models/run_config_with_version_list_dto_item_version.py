from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_config_with_version_list_dto_item_version_type import RunConfigWithVersionListDtoItemVersionType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.run_config_with_version_list_dto_item_version_config import RunConfigWithVersionListDtoItemVersionConfig
  from ..models.run_config_with_version_list_dto_item_version_config_schema_type_0 import RunConfigWithVersionListDtoItemVersionConfigSchemaType0
  from ..models.run_config_with_version_list_dto_item_version_config_template_type_0 import RunConfigWithVersionListDtoItemVersionConfigTemplateType0
  from ..models.run_config_with_version_list_dto_item_version_probe import RunConfigWithVersionListDtoItemVersionProbe





T = TypeVar("T", bound="RunConfigWithVersionListDtoItemVersion")



@_attrs_define
class RunConfigWithVersionListDtoItemVersion:
    """ The inlined single version (used by snapshot list responses to display version data without N+1 fetches).

        Attributes:
            id (UUID): Stable run-config-version identifier (UUID). Points at one specific version of a run config.
            run_config_id (UUID): Owning run-config identity.
            type_ (RunConfigWithVersionListDtoItemVersionType): Type discriminator copied from the parent run-config
                identity for client-side dispatch without a second request.
            version_number (int): Monotonically increasing version number within the owning run config. Example: 3.
            config (RunConfigWithVersionListDtoItemVersionConfig): Full payload for this version. Shape is keyed by the
                parent identity type.
            probe (RunConfigWithVersionListDtoItemVersionProbe): Probe spec used to verify this version before locking.
                Edits to this field clear the verification timestamp and the most-recent probe pointer.
            locked_at (datetime.datetime | None): Timestamp when the version was locked (ISO-8601, UTC). Null while still a
                draft. Locked versions are immutable and bindable to roles.
            locked_by_user_id (None | UUID): User who locked this version. Null while still a draft.
            verified_at (datetime.datetime | None): Timestamp when the most recent probe verified this draft (ISO-8601,
                UTC). Cleared when config / probe / attachments change. A passing probe before locking is recommended but not
                required.
            last_probe_run_id (None | UUID): Pointer to the most recent probe-run for this draft. Cleared when config /
                probe / attachments change. The pointed-to row carries the transcript and judge result.
            parent_run_config_version_id (None | UUID): Locked version this draft was forked from. Null when the draft was
                created from scratch (v1).
            notes (None | str): Free-form notes attached to this version. Null when not provided.
            created_by_user_id (UUID): User who created this version.
            updated_by_user_id (None | UUID): User who last updated this version. Null when never updated since creation.
            created_at (datetime.datetime): Timestamp when the version was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the version was last updated (ISO-8601, UTC).
            config_template (None | RunConfigWithVersionListDtoItemVersionConfigTemplateType0 | Unset): Container-authored
                default config values (placeholder values, not {}) for this version, generic across any run-config type. Read-
                only guidance the tuning create-form seeds from. Null/omitted when the container provides none.
            config_schema (None | RunConfigWithVersionListDtoItemVersionConfigSchemaType0 | Unset): Container-authored JSON
                Schema describing this version's config contract, generic across any run-config type. Validated against at
                tuning-run create when present; null/omitted skips validation.
     """

    id: UUID
    run_config_id: UUID
    type_: RunConfigWithVersionListDtoItemVersionType
    version_number: int
    config: RunConfigWithVersionListDtoItemVersionConfig
    probe: RunConfigWithVersionListDtoItemVersionProbe
    locked_at: datetime.datetime | None
    locked_by_user_id: None | UUID
    verified_at: datetime.datetime | None
    last_probe_run_id: None | UUID
    parent_run_config_version_id: None | UUID
    notes: None | str
    created_by_user_id: UUID
    updated_by_user_id: None | UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    config_template: None | RunConfigWithVersionListDtoItemVersionConfigTemplateType0 | Unset = UNSET
    config_schema: None | RunConfigWithVersionListDtoItemVersionConfigSchemaType0 | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_config_with_version_list_dto_item_version_config import RunConfigWithVersionListDtoItemVersionConfig # noqa: PLC0415
        from ..models.run_config_with_version_list_dto_item_version_config_schema_type_0 import RunConfigWithVersionListDtoItemVersionConfigSchemaType0 # noqa: PLC0415
        from ..models.run_config_with_version_list_dto_item_version_config_template_type_0 import RunConfigWithVersionListDtoItemVersionConfigTemplateType0 # noqa: PLC0415
        from ..models.run_config_with_version_list_dto_item_version_probe import RunConfigWithVersionListDtoItemVersionProbe # noqa: PLC0415
        id = str(self.id)

        run_config_id = str(self.run_config_id)

        type_ = self.type_.value

        version_number = self.version_number

        config = self.config.to_dict()

        probe = self.probe.to_dict()

        locked_at: None | str
        if isinstance(self.locked_at, datetime.datetime):
            locked_at = self.locked_at.isoformat()
        else:
            locked_at = self.locked_at

        locked_by_user_id: None | str
        if isinstance(self.locked_by_user_id, UUID):
            locked_by_user_id = str(self.locked_by_user_id)
        else:
            locked_by_user_id = self.locked_by_user_id

        verified_at: None | str
        if isinstance(self.verified_at, datetime.datetime):
            verified_at = self.verified_at.isoformat()
        else:
            verified_at = self.verified_at

        last_probe_run_id: None | str
        if isinstance(self.last_probe_run_id, UUID):
            last_probe_run_id = str(self.last_probe_run_id)
        else:
            last_probe_run_id = self.last_probe_run_id

        parent_run_config_version_id: None | str
        if isinstance(self.parent_run_config_version_id, UUID):
            parent_run_config_version_id = str(self.parent_run_config_version_id)
        else:
            parent_run_config_version_id = self.parent_run_config_version_id

        notes: None | str
        notes = self.notes

        created_by_user_id = str(self.created_by_user_id)

        updated_by_user_id: None | str
        if isinstance(self.updated_by_user_id, UUID):
            updated_by_user_id = str(self.updated_by_user_id)
        else:
            updated_by_user_id = self.updated_by_user_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        config_template: dict[str, Any] | None | Unset
        if isinstance(self.config_template, Unset):
            config_template = UNSET
        elif isinstance(self.config_template, RunConfigWithVersionListDtoItemVersionConfigTemplateType0):
            config_template = self.config_template.to_dict()
        else:
            config_template = self.config_template

        config_schema: dict[str, Any] | None | Unset
        if isinstance(self.config_schema, Unset):
            config_schema = UNSET
        elif isinstance(self.config_schema, RunConfigWithVersionListDtoItemVersionConfigSchemaType0):
            config_schema = self.config_schema.to_dict()
        else:
            config_schema = self.config_schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "runConfigId": run_config_id,
            "type": type_,
            "versionNumber": version_number,
            "config": config,
            "probe": probe,
            "lockedAt": locked_at,
            "lockedByUserId": locked_by_user_id,
            "verifiedAt": verified_at,
            "lastProbeRunId": last_probe_run_id,
            "parentRunConfigVersionId": parent_run_config_version_id,
            "notes": notes,
            "createdByUserId": created_by_user_id,
            "updatedByUserId": updated_by_user_id,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })
        if config_template is not UNSET:
            field_dict["configTemplate"] = config_template
        if config_schema is not UNSET:
            field_dict["configSchema"] = config_schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_config_with_version_list_dto_item_version_config import RunConfigWithVersionListDtoItemVersionConfig # noqa: PLC0415
        from ..models.run_config_with_version_list_dto_item_version_config_schema_type_0 import RunConfigWithVersionListDtoItemVersionConfigSchemaType0 # noqa: PLC0415
        from ..models.run_config_with_version_list_dto_item_version_config_template_type_0 import RunConfigWithVersionListDtoItemVersionConfigTemplateType0 # noqa: PLC0415
        from ..models.run_config_with_version_list_dto_item_version_probe import RunConfigWithVersionListDtoItemVersionProbe # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        run_config_id = UUID(d.pop("runConfigId"))




        type_ = RunConfigWithVersionListDtoItemVersionType(d.pop("type"))




        version_number = d.pop("versionNumber")

        config = RunConfigWithVersionListDtoItemVersionConfig.from_dict(d.pop("config"))




        probe = RunConfigWithVersionListDtoItemVersionProbe.from_dict(d.pop("probe"))




        def _parse_locked_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                locked_at_type_0 = datetime.datetime.fromisoformat(data)



                return locked_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        locked_at = _parse_locked_at(d.pop("lockedAt"))


        def _parse_locked_by_user_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                locked_by_user_id_type_0 = UUID(data)



                return locked_by_user_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        locked_by_user_id = _parse_locked_by_user_id(d.pop("lockedByUserId"))


        def _parse_verified_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                verified_at_type_0 = datetime.datetime.fromisoformat(data)



                return verified_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        verified_at = _parse_verified_at(d.pop("verifiedAt"))


        def _parse_last_probe_run_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_probe_run_id_type_0 = UUID(data)



                return last_probe_run_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        last_probe_run_id = _parse_last_probe_run_id(d.pop("lastProbeRunId"))


        def _parse_parent_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                parent_run_config_version_id_type_0 = UUID(data)



                return parent_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        parent_run_config_version_id = _parse_parent_run_config_version_id(d.pop("parentRunConfigVersionId"))


        def _parse_notes(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        notes = _parse_notes(d.pop("notes"))


        created_by_user_id = UUID(d.pop("createdByUserId"))




        def _parse_updated_by_user_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_by_user_id_type_0 = UUID(data)



                return updated_by_user_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        updated_by_user_id = _parse_updated_by_user_id(d.pop("updatedByUserId"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        def _parse_config_template(data: object) -> None | RunConfigWithVersionListDtoItemVersionConfigTemplateType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                config_template_type_0 = RunConfigWithVersionListDtoItemVersionConfigTemplateType0.from_dict(data)



                return config_template_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunConfigWithVersionListDtoItemVersionConfigTemplateType0 | Unset, data)

        config_template = _parse_config_template(d.pop("configTemplate", UNSET))


        def _parse_config_schema(data: object) -> None | RunConfigWithVersionListDtoItemVersionConfigSchemaType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                config_schema_type_0 = RunConfigWithVersionListDtoItemVersionConfigSchemaType0.from_dict(data)



                return config_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunConfigWithVersionListDtoItemVersionConfigSchemaType0 | Unset, data)

        config_schema = _parse_config_schema(d.pop("configSchema", UNSET))


        run_config_with_version_list_dto_item_version = cls(
            id=id,
            run_config_id=run_config_id,
            type_=type_,
            version_number=version_number,
            config=config,
            probe=probe,
            locked_at=locked_at,
            locked_by_user_id=locked_by_user_id,
            verified_at=verified_at,
            last_probe_run_id=last_probe_run_id,
            parent_run_config_version_id=parent_run_config_version_id,
            notes=notes,
            created_by_user_id=created_by_user_id,
            updated_by_user_id=updated_by_user_id,
            created_at=created_at,
            updated_at=updated_at,
            config_template=config_template,
            config_schema=config_schema,
        )

        return run_config_with_version_list_dto_item_version

