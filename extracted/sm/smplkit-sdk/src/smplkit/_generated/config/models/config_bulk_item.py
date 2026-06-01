from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.config_bulk_item_items_type_0 import ConfigBulkItemItemsType0


T = TypeVar("T", bound="ConfigBulkItem")


@_attrs_define
class ConfigBulkItem:
    """One config declaration reported by an SDK during bulk registration.

    Each item declares an entire config from code — the config's key,
    optional parent reference, and the items the calling code uses with
    their declared types, default values, and descriptions.

        Example:
            {'description': 'Plan-limit configuration declared by the billing service.', 'environment': 'production', 'id':
                'billing', 'items': {'plan.max_seats': {'description': 'Maximum seats per organization on this plan.', 'type':
                'NUMBER', 'value': 5}}, 'name': 'Billing', 'parent': 'common', 'service': 'billing-service'}

        Attributes:
            id (str): Config key as declared in code. URL-safe and stable for the lifetime of the config.
            name (None | str | Unset): Display name. Defaults to a humanized version of the `id` when omitted.
            description (None | str | Unset): Optional human-readable description of the config.
            parent (None | str | Unset): Parent config key. Used only when creating a new (discovered) config. Ignored on
                subsequent observations of an existing config — discovery never modifies parent on a config that already exists.
            items (ConfigBulkItemItemsType0 | None | Unset): Items declared by the SDK with their types, defaults, and
                descriptions. Used to populate items on a newly-discovered config; ignored on subsequent observations of an
                existing config.
            service (None | str | Unset): Service reporting the declaration. Defaults to `unknown`.
            environment (None | str | Unset): Environment reporting the declaration. Defaults to `unknown`.
    """

    id: str
    name: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    parent: None | str | Unset = UNSET
    items: ConfigBulkItemItemsType0 | None | Unset = UNSET
    service: None | str | Unset = UNSET
    environment: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.config_bulk_item_items_type_0 import ConfigBulkItemItemsType0

        id = self.id

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        parent: None | str | Unset
        if isinstance(self.parent, Unset):
            parent = UNSET
        else:
            parent = self.parent

        items: dict[str, Any] | None | Unset
        if isinstance(self.items, Unset):
            items = UNSET
        elif isinstance(self.items, ConfigBulkItemItemsType0):
            items = self.items.to_dict()
        else:
            items = self.items

        service: None | str | Unset
        if isinstance(self.service, Unset):
            service = UNSET
        else:
            service = self.service

        environment: None | str | Unset
        if isinstance(self.environment, Unset):
            environment = UNSET
        else:
            environment = self.environment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if parent is not UNSET:
            field_dict["parent"] = parent
        if items is not UNSET:
            field_dict["items"] = items
        if service is not UNSET:
            field_dict["service"] = service
        if environment is not UNSET:
            field_dict["environment"] = environment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.config_bulk_item_items_type_0 import ConfigBulkItemItemsType0

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_parent(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent = _parse_parent(d.pop("parent", UNSET))

        def _parse_items(data: object) -> ConfigBulkItemItemsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                items_type_0 = ConfigBulkItemItemsType0.from_dict(data)

                return items_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ConfigBulkItemItemsType0 | None | Unset, data)

        items = _parse_items(d.pop("items", UNSET))

        def _parse_service(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        service = _parse_service(d.pop("service", UNSET))

        def _parse_environment(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        environment = _parse_environment(d.pop("environment", UNSET))

        config_bulk_item = cls(
            id=id,
            name=name,
            description=description,
            parent=parent,
            items=items,
            service=service,
            environment=environment,
        )

        config_bulk_item.additional_properties = d
        return config_bulk_item

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
