from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_config_list_item_list_dto_item_type import RunConfigListItemListDtoItemType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.run_config_list_item_list_dto_items_properties_scope_env import RunConfigListItemListDtoItemsPropertiesScopeEnv
  from ..models.run_config_list_item_list_dto_items_properties_scope_org import RunConfigListItemListDtoItemsPropertiesScopeOrg
  from ..models.run_config_list_item_list_dto_items_properties_scope_problem import RunConfigListItemListDtoItemsPropertiesScopeProblem
  from ..models.run_config_list_item_list_dto_items_properties_scope_system import RunConfigListItemListDtoItemsPropertiesScopeSystem





T = TypeVar("T", bound="RunConfigListItemListDtoItem")



@_attrs_define
class RunConfigListItemListDtoItem:
    """ A run-config identity augmented with the distinct harness images used across all its versions. Returned by the
    scope-list endpoints so list pages can filter by image without fetching each version.

        Attributes:
            id (UUID): Stable run-config identifier (UUID). Versioned reusable solver / grader / QA / synthesizer config.
            scope (RunConfigListItemListDtoItemsPropertiesScopeEnv | RunConfigListItemListDtoItemsPropertiesScopeOrg |
                RunConfigListItemListDtoItemsPropertiesScopeProblem | RunConfigListItemListDtoItemsPropertiesScopeSystem): Scope
                at which this run config lives. Determines which environments / problems can see and bind it.
            type_ (RunConfigListItemListDtoItemType): Identity-level discriminator. Selects payload schema, submit pipeline,
                and editor form for every version.
            name (str): Human-readable display name shown in pickers and the catalog.
            description (None | str): Free-form description of what this run config is for. Null when not provided.
            tags (list[str]): Free-form tags for list filtering, matched with OR (any-of) semantics by tag-filtered list
                endpoints. Empty when the run config is untagged.
            created_by_user_id (UUID): User who created this run config.
            updated_by_user_id (None | UUID): User who last updated this run config. Null when never updated since creation.
            created_at (datetime.datetime): Timestamp when the run config was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the run config was last updated (ISO-8601, UTC).
            images (list[str]): Distinct harness image URLs across all non-deleted versions of this run config, in no
                guaranteed order. Empty for snapshot-type configs and for agent-harness configs whose versions set no image. A
                config matches an image facet when any entry here is selected.
            default_run_config_version_id (None | Unset | UUID): Locked version pinned as the role-agnostic default at this
                scope. Resolved after explicit problem-version / environment bindings miss, walking problem → env → org →
                system. Null when no default is set.
     """

    id: UUID
    scope: RunConfigListItemListDtoItemsPropertiesScopeEnv | RunConfigListItemListDtoItemsPropertiesScopeOrg | RunConfigListItemListDtoItemsPropertiesScopeProblem | RunConfigListItemListDtoItemsPropertiesScopeSystem
    type_: RunConfigListItemListDtoItemType
    name: str
    description: None | str
    tags: list[str]
    created_by_user_id: UUID
    updated_by_user_id: None | UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    images: list[str]
    default_run_config_version_id: None | Unset | UUID = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_config_list_item_list_dto_items_properties_scope_env import RunConfigListItemListDtoItemsPropertiesScopeEnv # noqa: PLC0415
        from ..models.run_config_list_item_list_dto_items_properties_scope_org import RunConfigListItemListDtoItemsPropertiesScopeOrg # noqa: PLC0415
        from ..models.run_config_list_item_list_dto_items_properties_scope_problem import RunConfigListItemListDtoItemsPropertiesScopeProblem # noqa: PLC0415
        from ..models.run_config_list_item_list_dto_items_properties_scope_system import RunConfigListItemListDtoItemsPropertiesScopeSystem # noqa: PLC0415
        id = str(self.id)

        scope: dict[str, Any]
        if isinstance(self.scope, RunConfigListItemListDtoItemsPropertiesScopeSystem):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, RunConfigListItemListDtoItemsPropertiesScopeOrg):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, RunConfigListItemListDtoItemsPropertiesScopeEnv):
            scope = self.scope.to_dict()
        else:
            scope = self.scope.to_dict()


        type_ = self.type_.value

        name = self.name

        description: None | str
        description = self.description

        tags = self.tags



        created_by_user_id = str(self.created_by_user_id)

        updated_by_user_id: None | str
        if isinstance(self.updated_by_user_id, UUID):
            updated_by_user_id = str(self.updated_by_user_id)
        else:
            updated_by_user_id = self.updated_by_user_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        images = self.images



        default_run_config_version_id: None | str | Unset
        if isinstance(self.default_run_config_version_id, Unset):
            default_run_config_version_id = UNSET
        elif isinstance(self.default_run_config_version_id, UUID):
            default_run_config_version_id = str(self.default_run_config_version_id)
        else:
            default_run_config_version_id = self.default_run_config_version_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "scope": scope,
            "type": type_,
            "name": name,
            "description": description,
            "tags": tags,
            "createdByUserId": created_by_user_id,
            "updatedByUserId": updated_by_user_id,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "images": images,
        })
        if default_run_config_version_id is not UNSET:
            field_dict["defaultRunConfigVersionId"] = default_run_config_version_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_config_list_item_list_dto_items_properties_scope_env import RunConfigListItemListDtoItemsPropertiesScopeEnv # noqa: PLC0415
        from ..models.run_config_list_item_list_dto_items_properties_scope_org import RunConfigListItemListDtoItemsPropertiesScopeOrg # noqa: PLC0415
        from ..models.run_config_list_item_list_dto_items_properties_scope_problem import RunConfigListItemListDtoItemsPropertiesScopeProblem # noqa: PLC0415
        from ..models.run_config_list_item_list_dto_items_properties_scope_system import RunConfigListItemListDtoItemsPropertiesScopeSystem # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_scope(data: object) -> RunConfigListItemListDtoItemsPropertiesScopeEnv | RunConfigListItemListDtoItemsPropertiesScopeOrg | RunConfigListItemListDtoItemsPropertiesScopeProblem | RunConfigListItemListDtoItemsPropertiesScopeSystem:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_0 = RunConfigListItemListDtoItemsPropertiesScopeSystem.from_dict(data)



                return scope_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_1 = RunConfigListItemListDtoItemsPropertiesScopeOrg.from_dict(data)



                return scope_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_2 = RunConfigListItemListDtoItemsPropertiesScopeEnv.from_dict(data)



                return scope_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            scope_type_3 = RunConfigListItemListDtoItemsPropertiesScopeProblem.from_dict(data)



            return scope_type_3

        scope = _parse_scope(d.pop("scope"))


        type_ = RunConfigListItemListDtoItemType(d.pop("type"))




        name = d.pop("name")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))


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




        images = cast(list[str], d.pop("images"))


        def _parse_default_run_config_version_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                default_run_config_version_id_type_0 = UUID(data)



                return default_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        default_run_config_version_id = _parse_default_run_config_version_id(d.pop("defaultRunConfigVersionId", UNSET))


        run_config_list_item_list_dto_item = cls(
            id=id,
            scope=scope,
            type_=type_,
            name=name,
            description=description,
            tags=tags,
            created_by_user_id=created_by_user_id,
            updated_by_user_id=updated_by_user_id,
            created_at=created_at,
            updated_at=updated_at,
            images=images,
            default_run_config_version_id=default_run_config_version_id,
        )

        return run_config_list_item_list_dto_item

