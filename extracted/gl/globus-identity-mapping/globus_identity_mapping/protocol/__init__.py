from __future__ import annotations

import typing as t

from typing_extensions import Self


class IdentityMappingProtocol(t.Protocol):
    DATA_TYPE: str

    @classmethod
    def from_mapping(
        cls,
        mapping_document: t.Mapping,
        connector: str | None = None,
        storage_gateway: str | None = None,
    ) -> Self:
        """
        Instantiate an identity mapper from the provided mapping
        configuration document.
        """

    @classmethod
    def map_identity(self, identity_data: t.Mapping[str, str]) -> str | None:
        """
        Map an identity resource to a connector-specific username.
        """

    def map_identities(
        self, identity_data: t.Iterable[t.Mapping[str, str]]
    ) -> list[dict[str, list[str]]]:
        """
        Map a list of identity resources to connector-specific usernames.
        """
