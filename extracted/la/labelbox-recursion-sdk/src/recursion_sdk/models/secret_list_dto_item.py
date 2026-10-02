from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="SecretListDtoItem")



@_attrs_define
class SecretListDtoItem:
    """ An environment-scoped secret binding. The secret value itself lives in Secret Manager; this record carries only
    metadata and policy.

        Attributes:
            id (UUID): Stable environment-secret identifier (UUID).
            environment_id (UUID): Environment that owns this secret binding.
            name (str): Environment-variable name the egress proxy injects the credential under.
            upstream_host (None | str): Upstream host the secret is allowed to be sent to. Null on legacy bindings predating
                the swap-credential runtime path.
            header_name (None | str): HTTP header the secret value is written into on outbound requests. Null on legacy
                bindings predating the swap-credential runtime path.
            created_at (datetime.datetime): Timestamp when the secret was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the secret was last updated (ISO-8601, UTC).
     """

    id: UUID
    environment_id: UUID
    name: str
    upstream_host: None | str
    header_name: None | str
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        environment_id = str(self.environment_id)

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
            "environmentId": environment_id,
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




        environment_id = UUID(d.pop("environmentId"))




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




        secret_list_dto_item = cls(
            id=id,
            environment_id=environment_id,
            name=name,
            upstream_host=upstream_host,
            header_name=header_name,
            created_at=created_at,
            updated_at=updated_at,
        )

        return secret_list_dto_item

