from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_catalog_connector import ManagedAgentsCatalogConnector





T = TypeVar("T", bound="ManagedAgentsCatalog")



@_attrs_define
class ManagedAgentsCatalog:
    """ The vendor catalog behind built-in integrations: every connector Merge Agent Handler fronts, its tools with read-
    only and destructive classification, and whether this deployment's account can configure it today. Read-only;
    nothing here is an authorization.

        Example:
            {'connectors': [{'auth_types': ['example'], 'categories': ['example'], 'configurable': True, 'description':
                'example', 'logo_url': 'https://example.com', 'name': 'example-name', 'slug': 'example', 'tools':
                [{'description': 'example', 'destructive': True, 'name': 'example-name', 'read_only': True}]}], 'refreshed_at':
                '2026-02-18T09:30:00Z'}

        Attributes:
            connectors (list[ManagedAgentsCatalogConnector] | None): Every connector in Merge's catalog, sorted by name.
                Filtered by the search query when one was given.
            refreshed_at (datetime.datetime): When this catalog was last read from Merge. Served from a per-replica cache
                refreshed about daily.
     """

    connectors: list[ManagedAgentsCatalogConnector] | None
    refreshed_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_catalog_connector import ManagedAgentsCatalogConnector # noqa: PLC0415
        connectors: list[dict[str, Any]] | None
        if isinstance(self.connectors, list):
            connectors = []
            for connectors_type_0_item_data in self.connectors:
                connectors_type_0_item = connectors_type_0_item_data.to_dict()
                connectors.append(connectors_type_0_item)


        else:
            connectors = self.connectors

        refreshed_at = self.refreshed_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "connectors": connectors,
            "refreshed_at": refreshed_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_catalog_connector import ManagedAgentsCatalogConnector # noqa: PLC0415
        d = dict(src_dict)
        def _parse_connectors(data: object) -> list[ManagedAgentsCatalogConnector] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                connectors_type_0 = []
                _connectors_type_0 = data
                for connectors_type_0_item_data in (_connectors_type_0):
                    connectors_type_0_item = ManagedAgentsCatalogConnector.from_dict(connectors_type_0_item_data)



                    connectors_type_0.append(connectors_type_0_item)

                return connectors_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsCatalogConnector] | None, data)

        connectors = _parse_connectors(d.pop("connectors"))


        refreshed_at = datetime.datetime.fromisoformat(d.pop("refreshed_at"))




        managed_agents_catalog = cls(
            connectors=connectors,
            refreshed_at=refreshed_at,
        )


        managed_agents_catalog.additional_properties = d
        return managed_agents_catalog

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
