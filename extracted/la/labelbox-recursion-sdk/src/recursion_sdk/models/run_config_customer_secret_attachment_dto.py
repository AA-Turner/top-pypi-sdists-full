from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_config_customer_secret_attachment_dto_injection_mode import RunConfigCustomerSecretAttachmentDtoInjectionMode
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.run_config_customer_secret_attachment_dto_properties_scope_env import RunConfigCustomerSecretAttachmentDtoPropertiesScopeEnv
  from ..models.run_config_customer_secret_attachment_dto_properties_scope_org import RunConfigCustomerSecretAttachmentDtoPropertiesScopeOrg
  from ..models.run_config_customer_secret_attachment_dto_properties_scope_problem import RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblem
  from ..models.run_config_customer_secret_attachment_dto_properties_scope_problem_version import RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblemVersion
  from ..models.run_config_customer_secret_attachment_dto_properties_scope_system import RunConfigCustomerSecretAttachmentDtoPropertiesScopeSystem





T = TypeVar("T", bound="RunConfigCustomerSecretAttachmentDto")



@_attrs_define
class RunConfigCustomerSecretAttachmentDto:
    """ Attachment of a customer secret to a specific run-config version. Each draft version owns its own attachment set;
    new drafts inherit from the parent locked version.

        Example:
            {'runConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad', 'customerSecretId':
                'a1b2c3d4-5e6f-4a7b-8c9d-0e1f2a3b4c5d', 'name': 'ANTHROPIC_API_KEY', 'injectionMode': 'proxy', 'upstreamHost':
                'api.anthropic.com', 'headerName': 'x-api-key', 'scope': {'level': 'env', 'id':
                '784e2386-e297-4f9d-a886-838422383b65'}, 'createdAt': '2026-01-15T09:35:00.000Z'}

        Attributes:
            run_config_version_id (UUID): Run-config version that owns this attachment.
            customer_secret_id (UUID): Customer secret attached to the run-config version.
            name (str): Environment-variable name of the attached secret, denormalized so consumers do not need a second
                fetch.
            injection_mode (RunConfigCustomerSecretAttachmentDtoInjectionMode): Injection mode of this attachment (proxy =
                egress-proxy swap, direct = plain env injection). Matches the secret's mode, except for attachments made before
                the secret gained an upstream host and header or before the mode was enforced.
            upstream_host (None | str): Upstream hostname of the attached secret, denormalized for display; null for direct-
                only secrets.
            header_name (None | str): HTTP header of the attached secret, denormalized for display; null for direct-only
                secrets.
            scope (RunConfigCustomerSecretAttachmentDtoPropertiesScopeEnv |
                RunConfigCustomerSecretAttachmentDtoPropertiesScopeOrg |
                RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblem |
                RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblemVersion |
                RunConfigCustomerSecretAttachmentDtoPropertiesScopeSystem): Scope of the attached secret, denormalized for
                display.
            created_at (datetime.datetime): Timestamp when the attachment was created (ISO-8601, UTC).
     """

    run_config_version_id: UUID
    customer_secret_id: UUID
    name: str
    injection_mode: RunConfigCustomerSecretAttachmentDtoInjectionMode
    upstream_host: None | str
    header_name: None | str
    scope: RunConfigCustomerSecretAttachmentDtoPropertiesScopeEnv | RunConfigCustomerSecretAttachmentDtoPropertiesScopeOrg | RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblem | RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblemVersion | RunConfigCustomerSecretAttachmentDtoPropertiesScopeSystem
    created_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_config_customer_secret_attachment_dto_properties_scope_env import RunConfigCustomerSecretAttachmentDtoPropertiesScopeEnv # noqa: PLC0415
        from ..models.run_config_customer_secret_attachment_dto_properties_scope_org import RunConfigCustomerSecretAttachmentDtoPropertiesScopeOrg # noqa: PLC0415
        from ..models.run_config_customer_secret_attachment_dto_properties_scope_problem import RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblem # noqa: PLC0415
        from ..models.run_config_customer_secret_attachment_dto_properties_scope_problem_version import RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblemVersion # noqa: PLC0415
        from ..models.run_config_customer_secret_attachment_dto_properties_scope_system import RunConfigCustomerSecretAttachmentDtoPropertiesScopeSystem # noqa: PLC0415
        run_config_version_id = str(self.run_config_version_id)

        customer_secret_id = str(self.customer_secret_id)

        name = self.name

        injection_mode = self.injection_mode.value

        upstream_host: None | str
        upstream_host = self.upstream_host

        header_name: None | str
        header_name = self.header_name

        scope: dict[str, Any]
        if isinstance(self.scope, RunConfigCustomerSecretAttachmentDtoPropertiesScopeSystem):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, RunConfigCustomerSecretAttachmentDtoPropertiesScopeOrg):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, RunConfigCustomerSecretAttachmentDtoPropertiesScopeEnv):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblem):
            scope = self.scope.to_dict()
        else:
            scope = self.scope.to_dict()


        created_at = self.created_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "runConfigVersionId": run_config_version_id,
            "customerSecretId": customer_secret_id,
            "name": name,
            "injectionMode": injection_mode,
            "upstreamHost": upstream_host,
            "headerName": header_name,
            "scope": scope,
            "createdAt": created_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_config_customer_secret_attachment_dto_properties_scope_env import RunConfigCustomerSecretAttachmentDtoPropertiesScopeEnv # noqa: PLC0415
        from ..models.run_config_customer_secret_attachment_dto_properties_scope_org import RunConfigCustomerSecretAttachmentDtoPropertiesScopeOrg # noqa: PLC0415
        from ..models.run_config_customer_secret_attachment_dto_properties_scope_problem import RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblem # noqa: PLC0415
        from ..models.run_config_customer_secret_attachment_dto_properties_scope_problem_version import RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblemVersion # noqa: PLC0415
        from ..models.run_config_customer_secret_attachment_dto_properties_scope_system import RunConfigCustomerSecretAttachmentDtoPropertiesScopeSystem # noqa: PLC0415
        d = dict(src_dict)
        run_config_version_id = UUID(d.pop("runConfigVersionId"))




        customer_secret_id = UUID(d.pop("customerSecretId"))




        name = d.pop("name")

        injection_mode = RunConfigCustomerSecretAttachmentDtoInjectionMode(d.pop("injectionMode"))




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


        def _parse_scope(data: object) -> RunConfigCustomerSecretAttachmentDtoPropertiesScopeEnv | RunConfigCustomerSecretAttachmentDtoPropertiesScopeOrg | RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblem | RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblemVersion | RunConfigCustomerSecretAttachmentDtoPropertiesScopeSystem:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_0 = RunConfigCustomerSecretAttachmentDtoPropertiesScopeSystem.from_dict(data)



                return scope_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_1 = RunConfigCustomerSecretAttachmentDtoPropertiesScopeOrg.from_dict(data)



                return scope_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_2 = RunConfigCustomerSecretAttachmentDtoPropertiesScopeEnv.from_dict(data)



                return scope_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_3 = RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblem.from_dict(data)



                return scope_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            scope_type_4 = RunConfigCustomerSecretAttachmentDtoPropertiesScopeProblemVersion.from_dict(data)



            return scope_type_4

        scope = _parse_scope(d.pop("scope"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        run_config_customer_secret_attachment_dto = cls(
            run_config_version_id=run_config_version_id,
            customer_secret_id=customer_secret_id,
            name=name,
            injection_mode=injection_mode,
            upstream_host=upstream_host,
            header_name=header_name,
            scope=scope,
            created_at=created_at,
        )

        return run_config_customer_secret_attachment_dto

