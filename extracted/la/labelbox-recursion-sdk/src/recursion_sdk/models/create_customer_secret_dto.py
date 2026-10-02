from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_customer_secret_dto_injection_mode import CreateCustomerSecretDtoInjectionMode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_customer_secret_dto_properties_scope_env import CreateCustomerSecretDtoPropertiesScopeEnv
  from ..models.create_customer_secret_dto_properties_scope_org import CreateCustomerSecretDtoPropertiesScopeOrg
  from ..models.create_customer_secret_dto_properties_scope_problem import CreateCustomerSecretDtoPropertiesScopeProblem
  from ..models.create_customer_secret_dto_properties_scope_problem_version import CreateCustomerSecretDtoPropertiesScopeProblemVersion
  from ..models.create_customer_secret_dto_properties_scope_system import CreateCustomerSecretDtoPropertiesScopeSystem





T = TypeVar("T", bound="CreateCustomerSecretDto")



@_attrs_define
class CreateCustomerSecretDto:
    """ Request body for creating a customer secret. Carries the credential value and metadata; the value is stored securely
    and never returned again.

        Example:
            {'scope': {'level': 'env', 'id': '784e2386-e297-4f9d-a886-838422383b65'}, 'name': 'ANTHROPIC_API_KEY',
                'injectionMode': 'proxy', 'upstreamHost': 'api.anthropic.com', 'headerName': 'x-api-key', 'value': 'paste your
                real Anthropic API key here'}

        Attributes:
            scope (CreateCustomerSecretDtoPropertiesScopeEnv | CreateCustomerSecretDtoPropertiesScopeOrg |
                CreateCustomerSecretDtoPropertiesScopeProblem | CreateCustomerSecretDtoPropertiesScopeProblemVersion |
                CreateCustomerSecretDtoPropertiesScopeSystem): Scope at which the new secret will be visible.
            name (str): Environment-variable name the runner will see when the secret is attached.
            value (str): Full ready-to-send header value (for example, a complete bearer token); stored verbatim and
                substituted in by the egress proxy.
            injection_mode (CreateCustomerSecretDtoInjectionMode | Unset): Injection mode of the new secret; its attachments
                always use the secret's mode. Defaults to 'proxy' when omitted. A 'proxy' secret requires upstreamHost and
                headerName; a 'direct' secret must omit both.
            upstream_host (str | Unset): Upstream hostname the egress proxy will substitute the credential for. Required for
                proxy secrets; omit for direct-only secrets.
            header_name (str | Unset): HTTP header the egress proxy will inject the credential into. Required for proxy
                secrets; omit for direct-only secrets.
     """

    scope: CreateCustomerSecretDtoPropertiesScopeEnv | CreateCustomerSecretDtoPropertiesScopeOrg | CreateCustomerSecretDtoPropertiesScopeProblem | CreateCustomerSecretDtoPropertiesScopeProblemVersion | CreateCustomerSecretDtoPropertiesScopeSystem
    name: str
    value: str
    injection_mode: CreateCustomerSecretDtoInjectionMode | Unset = UNSET
    upstream_host: str | Unset = UNSET
    header_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_customer_secret_dto_properties_scope_env import CreateCustomerSecretDtoPropertiesScopeEnv # noqa: PLC0415
        from ..models.create_customer_secret_dto_properties_scope_org import CreateCustomerSecretDtoPropertiesScopeOrg # noqa: PLC0415
        from ..models.create_customer_secret_dto_properties_scope_problem import CreateCustomerSecretDtoPropertiesScopeProblem # noqa: PLC0415
        from ..models.create_customer_secret_dto_properties_scope_problem_version import CreateCustomerSecretDtoPropertiesScopeProblemVersion # noqa: PLC0415
        from ..models.create_customer_secret_dto_properties_scope_system import CreateCustomerSecretDtoPropertiesScopeSystem # noqa: PLC0415
        scope: dict[str, Any]
        if isinstance(self.scope, CreateCustomerSecretDtoPropertiesScopeSystem):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, CreateCustomerSecretDtoPropertiesScopeOrg):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, CreateCustomerSecretDtoPropertiesScopeEnv):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, CreateCustomerSecretDtoPropertiesScopeProblem):
            scope = self.scope.to_dict()
        else:
            scope = self.scope.to_dict()


        name = self.name

        value = self.value

        injection_mode: str | Unset = UNSET
        if not isinstance(self.injection_mode, Unset):
            injection_mode = self.injection_mode.value


        upstream_host = self.upstream_host

        header_name = self.header_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "scope": scope,
            "name": name,
            "value": value,
        })
        if injection_mode is not UNSET:
            field_dict["injectionMode"] = injection_mode
        if upstream_host is not UNSET:
            field_dict["upstreamHost"] = upstream_host
        if header_name is not UNSET:
            field_dict["headerName"] = header_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_customer_secret_dto_properties_scope_env import CreateCustomerSecretDtoPropertiesScopeEnv # noqa: PLC0415
        from ..models.create_customer_secret_dto_properties_scope_org import CreateCustomerSecretDtoPropertiesScopeOrg # noqa: PLC0415
        from ..models.create_customer_secret_dto_properties_scope_problem import CreateCustomerSecretDtoPropertiesScopeProblem # noqa: PLC0415
        from ..models.create_customer_secret_dto_properties_scope_problem_version import CreateCustomerSecretDtoPropertiesScopeProblemVersion # noqa: PLC0415
        from ..models.create_customer_secret_dto_properties_scope_system import CreateCustomerSecretDtoPropertiesScopeSystem # noqa: PLC0415
        d = dict(src_dict)
        def _parse_scope(data: object) -> CreateCustomerSecretDtoPropertiesScopeEnv | CreateCustomerSecretDtoPropertiesScopeOrg | CreateCustomerSecretDtoPropertiesScopeProblem | CreateCustomerSecretDtoPropertiesScopeProblemVersion | CreateCustomerSecretDtoPropertiesScopeSystem:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_0 = CreateCustomerSecretDtoPropertiesScopeSystem.from_dict(data)



                return scope_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_1 = CreateCustomerSecretDtoPropertiesScopeOrg.from_dict(data)



                return scope_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_2 = CreateCustomerSecretDtoPropertiesScopeEnv.from_dict(data)



                return scope_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_3 = CreateCustomerSecretDtoPropertiesScopeProblem.from_dict(data)



                return scope_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            scope_type_4 = CreateCustomerSecretDtoPropertiesScopeProblemVersion.from_dict(data)



            return scope_type_4

        scope = _parse_scope(d.pop("scope"))


        name = d.pop("name")

        value = d.pop("value")

        _injection_mode = d.pop("injectionMode", UNSET)
        injection_mode: CreateCustomerSecretDtoInjectionMode | Unset
        if isinstance(_injection_mode,  Unset):
            injection_mode = UNSET
        else:
            injection_mode = CreateCustomerSecretDtoInjectionMode(_injection_mode)




        upstream_host = d.pop("upstreamHost", UNSET)

        header_name = d.pop("headerName", UNSET)

        create_customer_secret_dto = cls(
            scope=scope,
            name=name,
            value=value,
            injection_mode=injection_mode,
            upstream_host=upstream_host,
            header_name=header_name,
        )


        create_customer_secret_dto.additional_properties = d
        return create_customer_secret_dto

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
