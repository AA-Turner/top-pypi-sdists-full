"""Stateless helpers shared between the runtime and management config clients.

The runtime client (``ConfigClient``) and the management client
(``ConfigClient`` in ``mgmt.config``) both need to convert generated
API responses to/from :class:`Config` models. Putting these in a
shared module avoids the runtime client depending on the management
client (and vice versa) just to share conversion code.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from smplkit._generated.config.models.config import Config as GenConfig
from smplkit._generated.config.models.config_environments_type_0 import (
    ConfigEnvironmentsType0,
)
from smplkit._generated.config.models.config_environments_type_0_additional_property import (
    ConfigEnvironmentsType0AdditionalProperty,
)
from smplkit._generated.config.models.config_items_type_0 import ConfigItemsType0
from smplkit._generated.config.models.config_resource import ConfigResource
from smplkit._generated.config.models.config_response import ConfigResponse
from smplkit.config.models import AsyncConfig, Config, ConfigEnvironment

if TYPE_CHECKING:  # pragma: no cover
    from smplkit.config.client import AsyncConfigClient, ConfigClient
    from smplkit.management.client import (
        AsyncConfigClient as AsyncMgmtConfigClient,
        ConfigClient as MgmtConfigClient,
    )


def _make_items(items: dict[str, Any] | None) -> ConfigItemsType0 | None:
    """Convert a plain items dict to the generated ConfigItemsType0 model."""
    if items is None:
        return None
    from smplkit._generated.config.models.config_item_definition import (
        ConfigItemDefinition,
    )

    obj = ConfigItemsType0()
    wrapped: dict[str, ConfigItemDefinition] = {}
    for k, v in items.items():
        if isinstance(v, dict) and "value" in v:
            wrapped[k] = ConfigItemDefinition(
                value=v["value"],
                type_=v.get("type"),
                description=v.get("description"),
            )
        else:
            wrapped[k] = ConfigItemDefinition(value=v)
    obj.additional_properties = wrapped
    return obj


def _make_environments(
    environments: dict[str, Any] | None,
) -> ConfigEnvironmentsType0 | None:
    """Convert a plain dict to the generated ConfigEnvironmentsType0.

    Per ADR-024 §2.4 the wire shape is now flat: ``{env: {key: rawValue}}``.
    """
    if environments is None:
        return None

    obj = ConfigEnvironmentsType0()
    env_props: dict[str, ConfigEnvironmentsType0AdditionalProperty] = {}
    for env_name, env_data in environments.items():
        if isinstance(env_data, ConfigEnvironment):
            raw_values: dict[str, Any] = dict(env_data._values_raw)
        elif isinstance(env_data, dict):
            raw_values = dict(env_data)
        else:
            env_props[env_name] = ConfigEnvironmentsType0AdditionalProperty()
            continue
        prop = ConfigEnvironmentsType0AdditionalProperty()
        prop.additional_properties = raw_values
        env_props[env_name] = prop
    obj.additional_properties = env_props
    return obj


def _extract_items(items: Any) -> dict[str, Any]:
    """Extract a typed items dict from a generated items object."""
    if items is None or isinstance(items, type(None)):
        return {}
    type_name = type(items).__name__
    if type_name == "Unset":
        return {}
    if isinstance(items, ConfigItemsType0):
        result: dict[str, Any] = {}
        for k, item_def in items.additional_properties.items():
            entry: dict[str, Any] = {"value": item_def.value}
            type_val = getattr(item_def, "type_", None)
            if type_val is not None and type(type_val).__name__ != "Unset":
                entry["type"] = type_val.value if hasattr(type_val, "value") else str(type_val)
            desc_val = getattr(item_def, "description", None)
            if desc_val is not None and type(desc_val).__name__ != "Unset":
                entry["description"] = desc_val
            result[k] = entry
        return result
    if isinstance(items, dict):
        return dict(items)
    return {}


def _extract_environments(environments: Any) -> dict[str, Any]:
    """Extract a plain dict from a generated environments object.

    Per ADR-024 §2.4 the wire shape is flat ``{env: {key: rawValue}}`` —
    so this is a defensive shallow copy of the per-env override maps.
    """
    if environments is None or isinstance(environments, type(None)):
        return {}
    type_name = type(environments).__name__
    if type_name == "Unset":
        return {}
    if isinstance(environments, ConfigEnvironmentsType0):
        result: dict[str, Any] = {}
        for env_name, env_prop in environments.additional_properties.items():
            if hasattr(env_prop, "additional_properties"):
                result[env_name] = dict(env_prop.additional_properties)
            else:
                result[env_name] = {}
        return result
    if isinstance(environments, dict):
        return dict(environments)
    return {}


def _extract_datetime(value: Any) -> Any:
    """Pass through datetime objects, return None for Unset/None."""
    if value is None:
        return None
    type_name = type(value).__name__
    if type_name == "Unset":
        return None
    return value


def _unset_to_none(value: Any) -> Any:
    """Convert Unset sentinels to None."""
    type_name = type(value).__name__
    if type_name == "Unset":
        return None
    return value


def _build_config_request_body(
    *,
    config_id: str | None = None,
    name: str,
    description: str | None = None,
    parent: str | None = None,
    items: dict[str, Any] | None = None,
    environments: dict[str, Any] | None = None,
) -> ConfigResponse:
    """Build a JSON:API request body for create/update operations."""
    attrs = GenConfig(
        name=name,
        description=description,
        parent=parent,
        items=_make_items(items),
        environments=_make_environments(environments),
    )
    resource = ConfigResource(attributes=attrs, id=config_id, type_="config")
    return ConfigResponse(data=resource)


def _resource_to_config(client: ConfigClient | MgmtConfigClient | None, resource: Any) -> Config:
    """Convert a ConfigResource to a Config model."""
    attrs = resource.attributes
    return Config(
        client,
        id=_unset_to_none(resource.id) or "",
        name=attrs.name,
        description=_unset_to_none(attrs.description),
        parent=_unset_to_none(attrs.parent),
        items=_extract_items(attrs.items),
        environments=_extract_environments(attrs.environments),
        created_at=_extract_datetime(attrs.created_at),
        updated_at=_extract_datetime(attrs.updated_at),
    )


def _resource_to_async_config(client: AsyncConfigClient | AsyncMgmtConfigClient | None, resource: Any) -> AsyncConfig:
    """Convert a ConfigResource to an AsyncConfig model."""
    attrs = resource.attributes
    return AsyncConfig(
        client,
        id=_unset_to_none(resource.id) or "",
        name=attrs.name,
        description=_unset_to_none(attrs.description),
        parent=_unset_to_none(attrs.parent),
        items=_extract_items(attrs.items),
        environments=_extract_environments(attrs.environments),
        created_at=_extract_datetime(attrs.created_at),
        updated_at=_extract_datetime(attrs.updated_at),
    )
