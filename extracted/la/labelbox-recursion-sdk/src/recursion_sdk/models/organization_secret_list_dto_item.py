from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="OrganizationSecretListDtoItem")



@_attrs_define
class OrganizationSecretListDtoItem:
    """ A credential scoped to an organization for outbound requests to a specific upstream.

        Attributes:
            id (UUID): Stable organization-secret identifier (UUID).
            organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
            name (str): Human-readable name uniquely identifying the secret within the organization.
            upstream_host (None | str): Upstream host the secret authenticates against. Null on legacy pre-migration
                bindings.
            header_name (None | str): HTTP header name used to inject the secret value upstream. Null on legacy pre-
                migration bindings.
            created_at (datetime.datetime): Timestamp when the organization secret was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the organization secret was last updated (ISO-8601, UTC).
     """

    id: UUID
    organization_id: UUID
    name: str
    upstream_host: None | str
    header_name: None | str
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        organization_id = str(self.organization_id)

        name = self.name

        upstream_host: None | str
        upstream_host = self.upstream_host

        header_name: None | str
        header_name = self.header_name

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "organizationId": organization_id,
            "name": name,
            "upstreamHost": upstream_host,
            "headerName": header_name,
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


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        organization_secret_list_dto_item = cls(
            id=id,
            organization_id=organization_id,
            name=name,
            upstream_host=upstream_host,
            header_name=header_name,
            created_at=created_at,
            updated_at=updated_at,
        )

        return organization_secret_list_dto_item

