from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod

from typing_extensions import Self


class IdentityMapping(ABC):
    DATA_TYPE: str

    @classmethod
    def from_mapping_document(
        cls,
        mapping_document: t.Mapping,
        connector: str | None = None,
        storage_gateway: str | None = None,
    ) -> Self:
        """
        Instantiate an identity mapper from the provided mapping
        configuration document.
        """
        if mapping_document.get("DATA_TYPE") != cls.DATA_TYPE:
            raise ValueError("Unsupported DATA_TYPE")

        return cls._from_mapping_document(mapping_document, connector, storage_gateway)

    @classmethod
    @abstractmethod
    def _from_mapping_document(
        cls,
        mapping_document: t.Any,
        connector: str | None,
        storage_gateway: str | None,
    ):
        raise NotImplementedError
