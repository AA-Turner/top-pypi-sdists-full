from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.reaped_run_config_page_dto_items_item_deleted_reason_type_0 import ReapedRunConfigPageDtoItemsItemDeletedReasonType0
from ..models.reaped_run_config_page_dto_items_item_type import ReapedRunConfigPageDtoItemsItemType
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.reaped_run_config_page_dto_properties_items_items_properties_scope_env import ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeEnv
  from ..models.reaped_run_config_page_dto_properties_items_items_properties_scope_org import ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeOrg
  from ..models.reaped_run_config_page_dto_properties_items_items_properties_scope_problem import ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeProblem
  from ..models.reaped_run_config_page_dto_properties_items_items_properties_scope_system import ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeSystem





T = TypeVar("T", bound="ReapedRunConfigPageDtoItemsItem")



@_attrs_define
class ReapedRunConfigPageDtoItemsItem:
    """ A soft-deleted run config in the recycle bin, carrying deletion provenance (when, why, and by whom) alongside the
    identity fields.

        Attributes:
            id (UUID): Stable run-config identifier (UUID). Versioned reusable solver / grader / QA / synthesizer config.
            scope (ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeEnv |
                ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeOrg |
                ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeProblem |
                ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeSystem): Scope at which this run config lives.
                Determines which environments / problems can see and bind it.
            type_ (ReapedRunConfigPageDtoItemsItemType): Identity-level discriminator. Selects payload schema, submit
                pipeline, and editor form for every version.
            name (str): Human-readable display name shown in pickers and the catalog.
            description (None | str): Free-form description of what this run config is for. Null when not provided.
            default_run_config_version_id (None): Always null for a reaped config — the scope default pin is cleared on
                soft-delete.
            tags (list[str]): Free-form tags for list filtering, matched with OR (any-of) semantics by tag-filtered list
                endpoints. Empty when the run config is untagged.
            created_by_user_id (UUID): User who created this run config.
            updated_by_user_id (None | UUID): User who last updated this run config. Null when never updated since creation.
            created_at (datetime.datetime): Timestamp when the run config was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the run config was last updated (ISO-8601, UTC).
            deleted_at (datetime.datetime): Timestamp when the run config was soft-deleted (ISO-8601, UTC).
            deleted_reason (None | ReapedRunConfigPageDtoItemsItemDeletedReasonType0): Reason the reaper removed this run
                config, or null when a user deleted it manually.
            deleted_by (None | UUID): User who manually deleted this run config, or null when the system reaper removed it.
     """

    id: UUID
    scope: ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeEnv | ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeOrg | ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeProblem | ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeSystem
    type_: ReapedRunConfigPageDtoItemsItemType
    name: str
    description: None | str
    default_run_config_version_id: None
    tags: list[str]
    created_by_user_id: UUID
    updated_by_user_id: None | UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime
    deleted_reason: None | ReapedRunConfigPageDtoItemsItemDeletedReasonType0
    deleted_by: None | UUID





    def to_dict(self) -> dict[str, Any]:
        from ..models.reaped_run_config_page_dto_properties_items_items_properties_scope_env import ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeEnv # noqa: PLC0415
        from ..models.reaped_run_config_page_dto_properties_items_items_properties_scope_org import ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeOrg # noqa: PLC0415
        from ..models.reaped_run_config_page_dto_properties_items_items_properties_scope_problem import ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeProblem # noqa: PLC0415
        from ..models.reaped_run_config_page_dto_properties_items_items_properties_scope_system import ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeSystem # noqa: PLC0415
        id = str(self.id)

        scope: dict[str, Any]
        if isinstance(self.scope, ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeSystem):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeOrg):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeEnv):
            scope = self.scope.to_dict()
        else:
            scope = self.scope.to_dict()


        type_ = self.type_.value

        name = self.name

        description: None | str
        description = self.description

        default_run_config_version_id = self.default_run_config_version_id

        tags = self.tags



        created_by_user_id = str(self.created_by_user_id)

        updated_by_user_id: None | str
        if isinstance(self.updated_by_user_id, UUID):
            updated_by_user_id = str(self.updated_by_user_id)
        else:
            updated_by_user_id = self.updated_by_user_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        deleted_at = self.deleted_at.isoformat()

        deleted_reason: None | str
        if isinstance(self.deleted_reason, ReapedRunConfigPageDtoItemsItemDeletedReasonType0):
            deleted_reason = self.deleted_reason.value
        else:
            deleted_reason = self.deleted_reason

        deleted_by: None | str
        if isinstance(self.deleted_by, UUID):
            deleted_by = str(self.deleted_by)
        else:
            deleted_by = self.deleted_by


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "scope": scope,
            "type": type_,
            "name": name,
            "description": description,
            "defaultRunConfigVersionId": default_run_config_version_id,
            "tags": tags,
            "createdByUserId": created_by_user_id,
            "updatedByUserId": updated_by_user_id,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "deletedAt": deleted_at,
            "deletedReason": deleted_reason,
            "deletedBy": deleted_by,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reaped_run_config_page_dto_properties_items_items_properties_scope_env import ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeEnv # noqa: PLC0415
        from ..models.reaped_run_config_page_dto_properties_items_items_properties_scope_org import ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeOrg # noqa: PLC0415
        from ..models.reaped_run_config_page_dto_properties_items_items_properties_scope_problem import ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeProblem # noqa: PLC0415
        from ..models.reaped_run_config_page_dto_properties_items_items_properties_scope_system import ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeSystem # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_scope(data: object) -> ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeEnv | ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeOrg | ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeProblem | ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeSystem:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_0 = ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeSystem.from_dict(data)



                return scope_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_1 = ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeOrg.from_dict(data)



                return scope_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_2 = ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeEnv.from_dict(data)



                return scope_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            scope_type_3 = ReapedRunConfigPageDtoPropertiesItemsItemsPropertiesScopeProblem.from_dict(data)



            return scope_type_3

        scope = _parse_scope(d.pop("scope"))


        type_ = ReapedRunConfigPageDtoItemsItemType(d.pop("type"))




        name = d.pop("name")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))


        default_run_config_version_id = d.pop("defaultRunConfigVersionId")

        tags = cast(list[str], d.pop("tags"))


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




        deleted_at = datetime.datetime.fromisoformat(d.pop("deletedAt"))




        def _parse_deleted_reason(data: object) -> None | ReapedRunConfigPageDtoItemsItemDeletedReasonType0:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_reason_type_0 = ReapedRunConfigPageDtoItemsItemDeletedReasonType0(data)



                return deleted_reason_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ReapedRunConfigPageDtoItemsItemDeletedReasonType0, data)

        deleted_reason = _parse_deleted_reason(d.pop("deletedReason"))


        def _parse_deleted_by(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_by_type_0 = UUID(data)



                return deleted_by_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        deleted_by = _parse_deleted_by(d.pop("deletedBy"))


        reaped_run_config_page_dto_items_item = cls(
            id=id,
            scope=scope,
            type_=type_,
            name=name,
            description=description,
            default_run_config_version_id=default_run_config_version_id,
            tags=tags,
            created_by_user_id=created_by_user_id,
            updated_by_user_id=updated_by_user_id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            deleted_reason=deleted_reason,
            deleted_by=deleted_by,
        )

        return reaped_run_config_page_dto_items_item

