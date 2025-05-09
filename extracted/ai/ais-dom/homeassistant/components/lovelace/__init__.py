"""Support for the Lovelace UI."""
import logging

import voluptuous as vol

from homeassistant.components import frontend, websocket_api
from homeassistant.config import async_hass_config_yaml, async_process_component_config
from homeassistant.const import CONF_FILENAME, CONF_MODE, CONF_RESOURCES
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import collection, config_validation as cv
from homeassistant.helpers.service import async_register_admin_service
from homeassistant.helpers.typing import ConfigType
from homeassistant.loader import async_get_integration

from . import dashboard, resources, websocket
from .const import (  # noqa: F401
    CONF_ICON,
    CONF_REQUIRE_ADMIN,
    CONF_SHOW_IN_SIDEBAR,
    CONF_TITLE,
    CONF_URL_PATH,
    DASHBOARD_BASE_CREATE_FIELDS,
    DEFAULT_ICON,
    DOMAIN,
    EVENT_LOVELACE_UPDATED,
    MODE_STORAGE,
    MODE_YAML,
    RESOURCE_CREATE_FIELDS,
    RESOURCE_RELOAD_SERVICE_SCHEMA,
    RESOURCE_SCHEMA,
    RESOURCE_UPDATE_FIELDS,
    SERVICE_RELOAD_RESOURCES,
    STORAGE_DASHBOARD_CREATE_FIELDS,
    STORAGE_DASHBOARD_UPDATE_FIELDS,
    url_slug,
)
from .system_health import system_health_info  # noqa: F401

_LOGGER = logging.getLogger(__name__)

CONF_DASHBOARDS = "dashboards"

YAML_DASHBOARD_SCHEMA = vol.Schema(
    {
        **DASHBOARD_BASE_CREATE_FIELDS,
        vol.Required(CONF_MODE): MODE_YAML,
        vol.Required(CONF_FILENAME): cv.path,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Optional(DOMAIN, default={}): vol.Schema(
            {
                vol.Optional(CONF_MODE, default=MODE_STORAGE): vol.All(
                    vol.Lower, vol.In([MODE_YAML, MODE_STORAGE])
                ),
                vol.Optional(CONF_DASHBOARDS): cv.schema_with_slug_keys(
                    YAML_DASHBOARD_SCHEMA, slug_validator=url_slug
                ),
                vol.Optional(CONF_RESOURCES): [RESOURCE_SCHEMA],
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Lovelace commands."""
    mode = config[DOMAIN][CONF_MODE]
    yaml_resources = config[DOMAIN].get(CONF_RESOURCES)

    frontend.async_register_built_in_panel(hass, DOMAIN, config={"mode": mode})

    # ais fix migration dashboards - remove in version 1.0
    # run this only if lovelace_dashboards not exist and lovelace exists
    storage_path = "/data/data/com.termux/files/home/AIS/.storage/"
    import os
    import shutil

    if os.path.exists(storage_path + "lovelace") and not os.path.exists(
        storage_path + "lovelace_dashboards"
    ):
        ais_dom_lovelace_path = (
            str(os.path.dirname(__file__)) + "/ais_dom_lovelace_full"
        )
        ais_dom_dashboards_path = (
            str(os.path.dirname(__file__)) + "/lovelace_dashboards"
        )
        # 1. move current lovelace
        shutil.move(storage_path + "lovelace", storage_path + "lovelace.lovelace_dom")
        # 2. copy ais dom lovelace as default lovelace
        shutil.copy(ais_dom_lovelace_path, storage_path + "lovelace")
        # 3. copy lovelace_dashboards
        shutil.copy(ais_dom_dashboards_path, storage_path + "lovelace_dashboards")

    async def reload_resources_service_handler(service_call: ServiceCall) -> None:
        """Reload yaml resources."""
        try:
            conf = await async_hass_config_yaml(hass)
        except HomeAssistantError as err:
            _LOGGER.error(err)
            return

        integration = await async_get_integration(hass, DOMAIN)

        config = await async_process_component_config(hass, conf, integration)

        if config is None:
            raise HomeAssistantError("Config validation failed")

        resource_collection = await create_yaml_resource_col(
            hass, config[DOMAIN].get(CONF_RESOURCES)
        )
        hass.data[DOMAIN]["resources"] = resource_collection

    default_config: dashboard.LovelaceConfig
    if mode == MODE_YAML:
        default_config = dashboard.LovelaceYAML(hass, None, None)
        resource_collection = await create_yaml_resource_col(hass, yaml_resources)

        async_register_admin_service(
            hass,
            DOMAIN,
            SERVICE_RELOAD_RESOURCES,
            reload_resources_service_handler,
            schema=RESOURCE_RELOAD_SERVICE_SCHEMA,
        )

    else:
        default_config = dashboard.LovelaceStorage(hass, None)

        if yaml_resources is not None:
            _LOGGER.warning(
                "Lovelace is running in storage mode. Define resources via user"
                " interface"
            )

        resource_collection = resources.ResourceStorageCollection(hass, default_config)

        collection.DictStorageCollectionWebsocket(
            resource_collection,
            "lovelace/resources",
            "resource",
            RESOURCE_CREATE_FIELDS,
            RESOURCE_UPDATE_FIELDS,
        ).async_setup(hass, create_list=False)

    websocket_api.async_register_command(hass, websocket.websocket_lovelace_config)
    websocket_api.async_register_command(hass, websocket.websocket_lovelace_save_config)
    websocket_api.async_register_command(
        hass, websocket.websocket_lovelace_delete_config
    )
    websocket_api.async_register_command(hass, websocket.websocket_lovelace_resources)

    websocket_api.async_register_command(hass, websocket.websocket_lovelace_dashboards)

    hass.data[DOMAIN] = {
        # We store a dictionary mapping url_path: config. None is the default.
        "mode": mode,
        "dashboards": {None: default_config},
        "resources": resource_collection,
        "yaml_dashboards": config[DOMAIN].get(CONF_DASHBOARDS, {}),
    }

    if hass.config.recovery_mode:
        return True

    async def storage_dashboard_changed(change_type, item_id, item):
        """Handle a storage dashboard change."""
        url_path = item[CONF_URL_PATH]

        if change_type == collection.CHANGE_REMOVED:
            frontend.async_remove_panel(hass, url_path)
            await hass.data[DOMAIN]["dashboards"].pop(url_path).async_delete()
            return

        if change_type == collection.CHANGE_ADDED:
            existing = hass.data[DOMAIN]["dashboards"].get(url_path)

            if existing:
                _LOGGER.warning(
                    "Cannot register panel at %s, it is already defined in %s",
                    url_path,
                    existing,
                )
                return

            hass.data[DOMAIN]["dashboards"][url_path] = dashboard.LovelaceStorage(
                hass, item
            )

            update = False
        else:
            hass.data[DOMAIN]["dashboards"][url_path].config = item
            update = True

        try:
            _register_panel(hass, url_path, MODE_STORAGE, item, update)
        except ValueError:
            _LOGGER.warning("Failed to %s panel %s from storage", change_type, url_path)

    # Process YAML dashboards
    for url_path, dashboard_conf in hass.data[DOMAIN]["yaml_dashboards"].items():
        # For now always mode=yaml
        lovelace_config = dashboard.LovelaceYAML(hass, url_path, dashboard_conf)
        hass.data[DOMAIN]["dashboards"][url_path] = lovelace_config

        try:
            _register_panel(hass, url_path, MODE_YAML, dashboard_conf, False)
        except ValueError:
            _LOGGER.warning("Panel url path %s is not unique", url_path)

    # Process storage dashboards
    dashboards_collection = dashboard.DashboardsCollection(hass)

    dashboards_collection.async_add_listener(storage_dashboard_changed)
    await dashboards_collection.async_load()

    collection.DictStorageCollectionWebsocket(
        dashboards_collection,
        "lovelace/dashboards",
        "dashboard",
        STORAGE_DASHBOARD_CREATE_FIELDS,
        STORAGE_DASHBOARD_UPDATE_FIELDS,
    ).async_setup(hass, create_list=False)

    return True


async def create_yaml_resource_col(hass, yaml_resources):
    """Create yaml resources collection."""
    if yaml_resources is None:
        default_config = dashboard.LovelaceYAML(hass, None, None)
        try:
            ll_conf = await default_config.async_load(False)
        except HomeAssistantError:
            pass
        else:
            if CONF_RESOURCES in ll_conf:
                _LOGGER.warning(
                    "Resources need to be specified in your configuration.yaml. Please"
                    " see the docs"
                )
                yaml_resources = ll_conf[CONF_RESOURCES]

    return resources.ResourceYAMLCollection(yaml_resources or [])


@callback
def _register_panel(hass, url_path, mode, config, update):
    """Register a panel."""
    kwargs = {
        "frontend_url_path": url_path,
        "require_admin": config[CONF_REQUIRE_ADMIN],
        "config": {"mode": mode},
        "update": update,
    }

    if config[CONF_SHOW_IN_SIDEBAR]:
        kwargs["sidebar_title"] = config[CONF_TITLE]
        kwargs["sidebar_icon"] = config.get(CONF_ICON, DEFAULT_ICON)

    frontend.async_register_built_in_panel(hass, DOMAIN, **kwargs)
