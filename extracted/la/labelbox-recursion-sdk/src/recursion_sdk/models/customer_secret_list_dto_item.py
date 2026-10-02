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
  from ..models.customer_secret_list_dto_items_properties_scope_env import CustomerSecretListDtoItemsPropertiesScopeEnv
  from ..models.customer_secret_list_dto_items_properties_scope_org import CustomerSecretListDtoItemsPropertiesScopeOrg
  from ..models.customer_secret_list_dto_items_properties_scope_problem import CustomerSecretListDtoItemsPropertiesScopeProblem
  from ..models.customer_secret_list_dto_items_properties_scope_problem_version import CustomerSecretListDtoItemsPropertiesScopeProblemVersion
  from ..models.customer_secret_list_dto_items_properties_scope_system import CustomerSecretListDtoItemsPropertiesScopeSystem





T = TypeVar("T", bound="CustomerSecretListDtoItem")



@_attrs_define
class CustomerSecretListDtoItem:
    """ A reusable customer-managed credential reference. The credential value itself is never returned after creation; only
    metadata is exposed.

        Attributes:
            id (UUID): Stable customer-secret identifier (UUID).
            scope (CustomerSecretListDtoItemsPropertiesScopeEnv | CustomerSecretListDtoItemsPropertiesScopeOrg |
                CustomerSecretListDtoItemsPropertiesScopeProblem | CustomerSecretListDtoItemsPropertiesScopeProblemVersion |
                CustomerSecretListDtoItemsPropertiesScopeSystem): Scope at which this secret is visible and reusable.
            name (str): Environment-variable name the runner sees when the secret is attached.
            upstream_host (None | str): Upstream hostname the egress proxy substitutes the real credential for; null for
                direct-only secrets.
            header_name (None | str): HTTP header the egress proxy injects the credential into for outbound requests; null
                for direct-only secrets.
            placeholder_value (str): Vendor-shaped placeholder injected into the runner environment for proxy-mode
                attachments, where the egress proxy substitutes the real credential on the wire. Inert for direct-mode
                attachments, which inject the real value as a plain env var.
            created_by_user_id (UUID): User who created the secret.
            updated_by_user_id (None | UUID): User who last updated the secret; null when the secret has never been edited
                after creation.
            created_at (datetime.datetime): Timestamp when the secret was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the secret was last updated (ISO-8601, UTC).
     """

    id: UUID
    scope: CustomerSecretListDtoItemsPropertiesScopeEnv | CustomerSecretListDtoItemsPropertiesScopeOrg | CustomerSecretListDtoItemsPropertiesScopeProblem | CustomerSecretListDtoItemsPropertiesScopeProblemVersion | CustomerSecretListDtoItemsPropertiesScopeSystem
    name: str
    upstream_host: None | str
    header_name: None | str
    placeholder_value: str
    created_by_user_id: UUID
    updated_by_user_id: None | UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        from ..models.customer_secret_list_dto_items_properties_scope_env import CustomerSecretListDtoItemsPropertiesScopeEnv # noqa: PLC0415
        from ..models.customer_secret_list_dto_items_properties_scope_org import CustomerSecretListDtoItemsPropertiesScopeOrg # noqa: PLC0415
        from ..models.customer_secret_list_dto_items_properties_scope_problem import CustomerSecretListDtoItemsPropertiesScopeProblem # noqa: PLC0415
        from ..models.customer_secret_list_dto_items_properties_scope_problem_version import CustomerSecretListDtoItemsPropertiesScopeProblemVersion # noqa: PLC0415
        from ..models.customer_secret_list_dto_items_properties_scope_system import CustomerSecretListDtoItemsPropertiesScopeSystem # noqa: PLC0415
        id = str(self.id)

        scope: dict[str, Any]
        if isinstance(self.scope, CustomerSecretListDtoItemsPropertiesScopeSystem):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, CustomerSecretListDtoItemsPropertiesScopeOrg):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, CustomerSecretListDtoItemsPropertiesScopeEnv):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, CustomerSecretListDtoItemsPropertiesScopeProblem):
            scope = self.scope.to_dict()
        else:
            scope = self.scope.to_dict()


        name = self.name

        upstream_host: None | str
        upstream_host = self.upstream_host

        header_name: None | str
        header_name = self.header_name

        placeholder_value = self.placeholder_value

        created_by_user_id = str(self.created_by_user_id)

        updated_by_user_id: None | str
        if isinstance(self.updated_by_user_id, UUID):
            updated_by_user_id = str(self.updated_by_user_id)
        else:
            updated_by_user_id = self.updated_by_user_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "scope": scope,
            "name": name,
            "upstreamHost": upstream_host,
            "headerName": header_name,
            "placeholderValue": placeholder_value,
            "createdByUserId": created_by_user_id,
            "updatedByUserId": updated_by_user_id,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customer_secret_list_dto_items_properties_scope_env import CustomerSecretListDtoItemsPropertiesScopeEnv # noqa: PLC0415
        from ..models.customer_secret_list_dto_items_properties_scope_org import CustomerSecretListDtoItemsPropertiesScopeOrg # noqa: PLC0415
        from ..models.customer_secret_list_dto_items_properties_scope_problem import CustomerSecretListDtoItemsPropertiesScopeProblem # noqa: PLC0415
        from ..models.customer_secret_list_dto_items_properties_scope_problem_version import CustomerSecretListDtoItemsPropertiesScopeProblemVersion # noqa: PLC0415
        from ..models.customer_secret_list_dto_items_properties_scope_system import CustomerSecretListDtoItemsPropertiesScopeSystem # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_scope(data: object) -> CustomerSecretListDtoItemsPropertiesScopeEnv | CustomerSecretListDtoItemsPropertiesScopeOrg | CustomerSecretListDtoItemsPropertiesScopeProblem | CustomerSecretListDtoItemsPropertiesScopeProblemVersion | CustomerSecretListDtoItemsPropertiesScopeSystem:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_0 = CustomerSecretListDtoItemsPropertiesScopeSystem.from_dict(data)



                return scope_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_1 = CustomerSecretListDtoItemsPropertiesScopeOrg.from_dict(data)



                return scope_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_2 = CustomerSecretListDtoItemsPropertiesScopeEnv.from_dict(data)



                return scope_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_3 = CustomerSecretListDtoItemsPropertiesScopeProblem.from_dict(data)



                return scope_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            scope_type_4 = CustomerSecretListDtoItemsPropertiesScopeProblemVersion.from_dict(data)



            return scope_type_4

        scope = _parse_scope(d.pop("scope"))


        name = d.pop("name")

        def _parse_upstream_host(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        upstream_host = _parse_upstream_host(d.pop("upstreamHost"))


        def _parse_header_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        header_name = _parse_header_name(d.pop("headerName"))


        placeholder_value = d.pop("placeholderValue")

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




        customer_secret_list_dto_item = cls(
            id=id,
            scope=scope,
            name=name,
            upstream_host=upstream_host,
            header_name=header_name,
            placeholder_value=placeholder_value,
            created_by_user_id=created_by_user_id,
            updated_by_user_id=updated_by_user_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        return customer_secret_list_dto_item

