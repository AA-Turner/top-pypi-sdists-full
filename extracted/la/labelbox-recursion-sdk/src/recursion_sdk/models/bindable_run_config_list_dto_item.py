from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.bindable_run_config_list_dto_item_type import BindableRunConfigListDtoItemType
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.bindable_run_config_list_dto_item_locked_versions_item import BindableRunConfigListDtoItemLockedVersionsItem
  from ..models.bindable_run_config_list_dto_items_properties_scope_env import BindableRunConfigListDtoItemsPropertiesScopeEnv
  from ..models.bindable_run_config_list_dto_items_properties_scope_org import BindableRunConfigListDtoItemsPropertiesScopeOrg
  from ..models.bindable_run_config_list_dto_items_properties_scope_problem import BindableRunConfigListDtoItemsPropertiesScopeProblem
  from ..models.bindable_run_config_list_dto_items_properties_scope_system import BindableRunConfigListDtoItemsPropertiesScopeSystem





T = TypeVar("T", bound="BindableRunConfigListDtoItem")



@_attrs_define
class BindableRunConfigListDtoItem:
    """ Compact bindable run-config identity with nested locked-version summaries for environment binding selectors.

        Attributes:
            id (UUID): Stable run-config identity identifier.
            name (str): Human-readable display name shown in binding selectors.
            scope (BindableRunConfigListDtoItemsPropertiesScopeEnv | BindableRunConfigListDtoItemsPropertiesScopeOrg |
                BindableRunConfigListDtoItemsPropertiesScopeProblem | BindableRunConfigListDtoItemsPropertiesScopeSystem): Scope
                at which this run config lives. Bindable catalogs include system, org, and env scopes only.
            type_ (BindableRunConfigListDtoItemType): Identity-level discriminator used for role slot filtering in
                selectors.
            default_run_config_version_id (None | UUID): Locked version pinned as the role-agnostic default at this scope,
                or null when unset.
            locked_versions (list[BindableRunConfigListDtoItemLockedVersionsItem]): Locked, non-deleted versions for this
                identity, newest-first. Empty when no locked version exists.
     """

    id: UUID
    name: str
    scope: BindableRunConfigListDtoItemsPropertiesScopeEnv | BindableRunConfigListDtoItemsPropertiesScopeOrg | BindableRunConfigListDtoItemsPropertiesScopeProblem | BindableRunConfigListDtoItemsPropertiesScopeSystem
    type_: BindableRunConfigListDtoItemType
    default_run_config_version_id: None | UUID
    locked_versions: list[BindableRunConfigListDtoItemLockedVersionsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.bindable_run_config_list_dto_item_locked_versions_item import BindableRunConfigListDtoItemLockedVersionsItem # noqa: PLC0415
        from ..models.bindable_run_config_list_dto_items_properties_scope_env import BindableRunConfigListDtoItemsPropertiesScopeEnv # noqa: PLC0415
        from ..models.bindable_run_config_list_dto_items_properties_scope_org import BindableRunConfigListDtoItemsPropertiesScopeOrg # noqa: PLC0415
        from ..models.bindable_run_config_list_dto_items_properties_scope_problem import BindableRunConfigListDtoItemsPropertiesScopeProblem # noqa: PLC0415
        from ..models.bindable_run_config_list_dto_items_properties_scope_system import BindableRunConfigListDtoItemsPropertiesScopeSystem # noqa: PLC0415
        id = str(self.id)

        name = self.name

        scope: dict[str, Any]
        if isinstance(self.scope, BindableRunConfigListDtoItemsPropertiesScopeSystem):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, BindableRunConfigListDtoItemsPropertiesScopeOrg):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, BindableRunConfigListDtoItemsPropertiesScopeEnv):
            scope = self.scope.to_dict()
        else:
            scope = self.scope.to_dict()


        type_ = self.type_.value

        default_run_config_version_id: None | str
        if isinstance(self.default_run_config_version_id, UUID):
            default_run_config_version_id = str(self.default_run_config_version_id)
        else:
            default_run_config_version_id = self.default_run_config_version_id

        locked_versions = []
        for locked_versions_item_data in self.locked_versions:
            locked_versions_item = locked_versions_item_data.to_dict()
            locked_versions.append(locked_versions_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "name": name,
            "scope": scope,
            "type": type_,
            "defaultRunConfigVersionId": default_run_config_version_id,
            "lockedVersions": locked_versions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bindable_run_config_list_dto_item_locked_versions_item import BindableRunConfigListDtoItemLockedVersionsItem # noqa: PLC0415
        from ..models.bindable_run_config_list_dto_items_properties_scope_env import BindableRunConfigListDtoItemsPropertiesScopeEnv # noqa: PLC0415
        from ..models.bindable_run_config_list_dto_items_properties_scope_org import BindableRunConfigListDtoItemsPropertiesScopeOrg # noqa: PLC0415
        from ..models.bindable_run_config_list_dto_items_properties_scope_problem import BindableRunConfigListDtoItemsPropertiesScopeProblem # noqa: PLC0415
        from ..models.bindable_run_config_list_dto_items_properties_scope_system import BindableRunConfigListDtoItemsPropertiesScopeSystem # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        name = d.pop("name")

        def _parse_scope(data: object) -> BindableRunConfigListDtoItemsPropertiesScopeEnv | BindableRunConfigListDtoItemsPropertiesScopeOrg | BindableRunConfigListDtoItemsPropertiesScopeProblem | BindableRunConfigListDtoItemsPropertiesScopeSystem:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_0 = BindableRunConfigListDtoItemsPropertiesScopeSystem.from_dict(data)



                return scope_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_1 = BindableRunConfigListDtoItemsPropertiesScopeOrg.from_dict(data)



                return scope_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_2 = BindableRunConfigListDtoItemsPropertiesScopeEnv.from_dict(data)



                return scope_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            scope_type_3 = BindableRunConfigListDtoItemsPropertiesScopeProblem.from_dict(data)



            return scope_type_3

        scope = _parse_scope(d.pop("scope"))


        type_ = BindableRunConfigListDtoItemType(d.pop("type"))




        def _parse_default_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                default_run_config_version_id_type_0 = UUID(data)



                return default_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        default_run_config_version_id = _parse_default_run_config_version_id(d.pop("defaultRunConfigVersionId"))


        locked_versions = []
        _locked_versions = d.pop("lockedVersions")
        for locked_versions_item_data in (_locked_versions):
            locked_versions_item = BindableRunConfigListDtoItemLockedVersionsItem.from_dict(locked_versions_item_data)



            locked_versions.append(locked_versions_item)


        bindable_run_config_list_dto_item = cls(
            id=id,
            name=name,
            scope=scope,
            type_=type_,
            default_run_config_version_id=default_run_config_version_id,
            locked_versions=locked_versions,
        )

        return bindable_run_config_list_dto_item

