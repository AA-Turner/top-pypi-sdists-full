from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_catalog_tool import ManagedAgentsCatalogTool





T = TypeVar("T", bound="ManagedAgentsCatalogConnector")



@_attrs_define
class ManagedAgentsCatalogConnector:
    """ One vendor connector in Merge's catalog, including its authentication methods, current configurability, and
    classified tool inventory.

        Example:
            {'auth_types': ['example'], 'categories': ['example'], 'configurable': True, 'description': 'example',
                'logo_url': 'https://example.com', 'name': 'example-name', 'slug': 'example', 'tools': [{'description':
                'example', 'destructive': True, 'name': 'example-name', 'read_only': True}]}

        Attributes:
            configurable (bool): True when this account can add the connector to a Tool Pack today. False means the vendor
                OAuth application is not registered yet; the connector is listed so the gap is visible, not offerable.
            name (str): Vendor display name.
            slug (str): Stable connector slug, e.g. sentry. What a registration names as external_id.
            tools (list[ManagedAgentsCatalogTool] | None): The connector's tools, sorted by name. Empty for a connector that
                is not configurable, whose tools Merge lists without classification.
            auth_types (list[str] | Unset): How the vendor can be authenticated on the hosted Link page: OAuth2, Secrets (a
                pasted token), or both.
            categories (list[str] | Unset): Merge's category labels for the vendor; sparse and noisy, shown but not filtered
                on.
            description (str | Unset): Merge's one-line description of the connector.
            logo_url (str | Unset): Vendor logo, served by Merge.
     """

    configurable: bool
    name: str
    slug: str
    tools: list[ManagedAgentsCatalogTool] | None
    auth_types: list[str] | Unset = UNSET
    categories: list[str] | Unset = UNSET
    description: str | Unset = UNSET
    logo_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_catalog_tool import ManagedAgentsCatalogTool # noqa: PLC0415
        configurable = self.configurable

        name = self.name

        slug = self.slug

        tools: list[dict[str, Any]] | None
        if isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item = tools_type_0_item_data.to_dict()
                tools.append(tools_type_0_item)


        else:
            tools = self.tools

        auth_types: list[str] | Unset = UNSET
        if not isinstance(self.auth_types, Unset):
            auth_types = self.auth_types



        categories: list[str] | Unset = UNSET
        if not isinstance(self.categories, Unset):
            categories = self.categories



        description = self.description

        logo_url = self.logo_url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "configurable": configurable,
            "name": name,
            "slug": slug,
            "tools": tools,
        })
        if auth_types is not UNSET:
            field_dict["auth_types"] = auth_types
        if categories is not UNSET:
            field_dict["categories"] = categories
        if description is not UNSET:
            field_dict["description"] = description
        if logo_url is not UNSET:
            field_dict["logo_url"] = logo_url

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_catalog_tool import ManagedAgentsCatalogTool # noqa: PLC0415
        d = dict(src_dict)
        configurable = d.pop("configurable")

        name = d.pop("name")

        slug = d.pop("slug")

        def _parse_tools(data: object) -> list[ManagedAgentsCatalogTool] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tools_type_0 = []
                _tools_type_0 = data
                for tools_type_0_item_data in (_tools_type_0):
                    tools_type_0_item = ManagedAgentsCatalogTool.from_dict(tools_type_0_item_data)



                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsCatalogTool] | None, data)

        tools = _parse_tools(d.pop("tools"))


        auth_types = cast(list[str], d.pop("auth_types", UNSET))


        categories = cast(list[str], d.pop("categories", UNSET))


        description = d.pop("description", UNSET)

        logo_url = d.pop("logo_url", UNSET)

        managed_agents_catalog_connector = cls(
            configurable=configurable,
            name=name,
            slug=slug,
            tools=tools,
            auth_types=auth_types,
            categories=categories,
            description=description,
            logo_url=logo_url,
        )


        managed_agents_catalog_connector.additional_properties = d
        return managed_agents_catalog_connector

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
