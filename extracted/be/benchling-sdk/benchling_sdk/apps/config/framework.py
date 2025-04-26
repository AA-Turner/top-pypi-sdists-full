from __future__ import annotations

from typing import Dict, List, Optional, OrderedDict, Protocol, Tuple, Union

from benchling_api_client.v2.extensions import UnknownType
from ordered_set import OrderedSet

from benchling_sdk.apps.config.errors import (
    ConfigItemLinkedResourceError,
    InaccessibleConfigItemError,
    MissingRequiredConfigItemError,
    UnsupportedConfigItemError,
)
from benchling_sdk.apps.config.types import ConfigItemPath, ConfigurationReference
from benchling_sdk.benchling import Benchling
from benchling_sdk.models import (
    AppConfigItem,
    EntitySchemaAppConfigItem,
    FieldAppConfigItem,
    GenericApiIdentifiedAppConfigItem,
    InaccessibleResource,
    LinkedAppConfigResourceSummary,
    ListAppConfigurationItemsSort,
)


class _DefaultOrderedDict(OrderedDict):
    _root_path: List[str]

    def __init__(self, root_path: List[str]) -> None:
        super().__init__()
        self._root_path = root_path

    def __missing__(self, key):
        return ConfigItemWrapper(None, [*self._root_path, key])


class ConfigProvider(Protocol):
    """
    Config provider.

    Provides a list of ConfigurationReference.
    """

    def config(self) -> List[ConfigurationReference]:
        """Implement to provide a list of configuration items, for instance from Benchling APIs."""
        pass


class BenchlingConfigProvider(ConfigProvider):
    """
    Benchling Config provider.

    Provides a BenchlingAppConfiguration retrieved from Benchling's API.
    """

    _app_id: str
    _benchling: Benchling

    def __init__(self, benchling: Benchling, app_id: str):
        """
        Initialize Benchling Config Provider.

        :param benchling: A Benchling instance.
        :param app_id: The app_id from which to retrieve configuration.
        """
        self._app_id = app_id
        self._benchling = benchling

    def config(self) -> List[ConfigurationReference]:
        """Provide a Benchling app configuration from Benchling's APIs."""
        app_pages = self._benchling.apps.list_app_configuration_items(
            app_id=self._app_id,
            page_size=100,
            sort=ListAppConfigurationItemsSort.CREATEDATASC,
        )

        # Eager load all config items for now since we don't yet have a way of lazily querying by path
        all_config_pages = list(app_pages)
        # Punt on UnknownType for now as apps using manifests with new types +
        # older client could lead to unpredictable results
        all_config_items = [
            _supported_config_item(config_item) for page in all_config_pages for config_item in page
        ]

        return all_config_items


class StaticConfigProvider(ConfigProvider):
    """
    Static Config provider.

    Provides a BenchlingAppConfiguration from a static declaration. Useful for mocking or testing.
    """

    _configuration_items: List[ConfigurationReference]

    def __init__(self, configuration_items: List[ConfigurationReference]):
        """
        Initialize Static Config Provider.

        :param configuration_items: The configuration items to return.
        """
        self._configuration_items = configuration_items

    def config(self) -> List[ConfigurationReference]:
        """Provide Benchling app configuration items from a static reference."""
        return self._configuration_items


class ConfigItemWrapper:
    """
    Config Item Wrapper.

    A decorator class for AppConfigItem to assist with typesafe access to its values.
    Access the `item` attribute for the original config item, if present.
    """

    item: Optional[ConfigurationReference]
    path: List[str]

    def __init__(self, item: Optional[ConfigurationReference], path: List[str]) -> None:
        """Init Pathed Config Item."""
        self.item = item
        self.path = path

    def required(self) -> RequiredConfigItemWrapper:
        """Return a `RequiredPathedConfigItem` to enforce that config item is not optional."""
        if self.item is None:
            raise MissingRequiredConfigItemError(
                f"Required config item {self.path} is missing from the config store"
            )
        return RequiredConfigItemWrapper(self.item, self.path)

    def linked_resource(self) -> Optional[LinkedAppConfigResourceSummary]:
        """
        Return an optional LinkedAppConfigResourceSummary.

        Raises exceptions if the config item is not of the type that supports linked resources,
        or the linked resource is inaccessible.
        """
        if self.item is not None:
            # Python can't compare isinstance for Union types until Python 3.10 so just do this for now
            # from: https://github.com/python/typing/discussions/1132#discussioncomment-2560441
            # elif isinstance(self.item, get_args(LinkedResourceConfigurationReference)):
            if isinstance(
                self.item, (EntitySchemaAppConfigItem, FieldAppConfigItem, GenericApiIdentifiedAppConfigItem)
            ):
                if self.item.linked_resource is None:
                    return None
                elif isinstance(self.item.linked_resource, LinkedAppConfigResourceSummary):
                    return self.item.linked_resource
                elif isinstance(self.item.linked_resource, InaccessibleResource):
                    raise InaccessibleConfigItemError(
                        f"The linked resource for config item {self.path} was inaccessible. "
                        f"The caller does not have permissions to the resource."
                    )
                raise UnsupportedConfigItemError(
                    f"Unable to read app configuration with unsupported type: {self.item}"
                )
            raise ConfigItemLinkedResourceError(
                f"Type mismatch: The config item {self.item} type never has a linked resource"
            )
        return None

    def value(self) -> Union[str, float, int, bool, None]:
        """Return the value of the config item, if present."""
        return self.item.value if self.item else None

    def value_str(self) -> Optional[str]:
        """Return the value of the config item as a string, if present."""
        return str(self.value()) if self.value() else None

    def __bool__(self) -> bool:
        return self.value() is not None


class RequiredConfigItemWrapper(ConfigItemWrapper):
    """
    Required Config Item Wrapper.

    A decorator class for AppConfigItem to assist with typesafe access to its values.
    Enforces that a config item is present, and that it's value is not None.
    Access the `item` attribute for the original config item.
    """

    item: ConfigurationReference

    def __init__(self, item: ConfigurationReference, path: List[str]) -> None:
        """Init Required Pathed Config Item."""
        super().__init__(item, path)

    def linked_resource(self) -> LinkedAppConfigResourceSummary:
        """
        Return a LinkedAppConfigResourceSummary.

        Raises exceptions if the config item is not of the type that supports linked resources,
        or the linked resource is inaccessible.
        """
        linked_resource = super().linked_resource()
        if linked_resource is None:
            raise MissingRequiredConfigItemError(
                f"Required config item {self.path} is missing a linked resource"
            )
        return linked_resource

    def value(self) -> Union[str, float, int, bool]:
        """Return the value of the config item."""
        if self.item.value is None:
            raise MissingRequiredConfigItemError(
                f"Required config item {self.path} is missing from the config store"
            )
        return self.item.value

    def value_str(self) -> str:
        """Return the value of the config item as a string."""
        return str(self.value())


class ConfigItemStore:
    """
    Dependency Link Store.

    Marshals an app configuration from the configuration provider into an indexed structure.
    Only retrieves app configuration once unless its cache is invalidated.
    """

    _configuration_provider: ConfigProvider
    _configuration: Optional[List[ConfigurationReference]] = None
    _configuration_dict: Optional[Dict[ConfigItemPath, ConfigItemWrapper]] = None
    _array_path_row_names: Dict[Tuple[str, ...], OrderedSet[str]]

    def __init__(self, configuration_provider: ConfigProvider):
        """
        Initialize Dependency Link Store.

        :param configuration_provider: A ConfigProvider that will be invoked to provide the
        underlying config from which to organize dependency links.
        """
        self._configuration_provider = configuration_provider
        self._array_path_row_names = dict()

    @property
    def configuration(self) -> List[ConfigurationReference]:
        """
        Get the underlying configuration.

        Return the raw, stored configuration. Can be used if the provided accessors are inadequate
        to find particular configuration items.
        """
        if not self._configuration:
            self._configuration = self._configuration_provider.config()
        return self._configuration

    @property
    def configuration_path_dict(self) -> Dict[ConfigItemPath, ConfigItemWrapper]:
        """
        Config links.

        Return a dict of configuration item paths to their corresponding configuration items.
        """
        if not self._configuration_dict:
            self._configuration_dict = {
                tuple(item.path): ConfigItemWrapper(item, item.path) for item in self.configuration
            }
        return self._configuration_dict

    def config_by_path(self, path: List[str]) -> ConfigItemWrapper:
        """
        Config by path.

        Find an app config item by its exact path match, if it exists. Does not search partial paths.
        """
        # Since we eager load all config now, we know that missing path means it's not configured in Benchling
        # Later if we support lazy loading, we'll need to differentiate what's in our cache versus missing
        return self.configuration_path_dict.get(tuple(path), ConfigItemWrapper(None, path))

    def config_keys_by_path(self, path: List[str]) -> OrderedSet[str]:
        """
        Config keys by path.

        Find a set of app config keys at the specified path, if any. Does not return keys that are nested
        beyond the current level.

        For instance, given paths:
        ["One", "Two"]
        ["One", "Two", "Three"]
        ["One", "Two", "Four"]
        ["One", "Two", "Three", "Five"]
        ["Zero", "One", "Two", "Three"]

        The expected return from this method when path=["One", "Two"] is a set {"Three", "Four"}.
        """
        # Convert path to tuple, as list is not hashable for dict keys
        path_tuple = tuple(path)
        if path_tuple not in self._array_path_row_names:
            self._array_path_row_names[path_tuple] = OrderedSet(
                [
                    config_item.path[len(path)]
                    # Use the list instead of configuration_dict to preserve order
                    for config_item in self.configuration
                    # The +1 is the name of the array row
                    if len(config_item.path) >= len(path) + 1
                    # Ignoring flake8 error E203 because black keeps putting in whitespace padding :
                    and config_item.path[0 : len(path_tuple)] == path
                    and config_item.value is not None
                ]
            )
        return self._array_path_row_names[path_tuple]

    def array_rows_to_dict(self, path: List[str]) -> OrderedDict[str, Dict[str, ConfigItemWrapper]]:
        """Given a path to the root of a config array, return each element as a named dict."""
        array_keys = self.config_keys_by_path(path)
        # Although we don't have a way of preserving order when pulling array elements from the API right now
        # we should intentionally order these to accommodate a potential ordered future
        array_elements_map = _DefaultOrderedDict(root_path=path)
        for key in array_keys:
            array_elements_map[key] = _DefaultOrderedDict(root_path=[*path, key])
            # Don't care about order for the keys within a row, only the order of the rows themselves
            for array_element_key in self.config_keys_by_path([*path, key]):
                if self.config_by_path([*path, key, array_element_key]) is not None:
                    array_elements_map[key][array_element_key] = self.config_by_path(
                        [*path, key, array_element_key]
                    )
        return array_elements_map

    def invalidate_cache(self) -> None:
        """
        Invalidate Cache.

        Will force retrieval of configuration from the ConfigProvider the next time the link store is accessed.
        """
        self._configuration = None
        self._configuration_dict = None
        self._array_path_row_names = dict()


def _supported_config_item(config_item: AppConfigItem) -> ConfigurationReference:
    if isinstance(config_item, UnknownType):
        raise UnsupportedConfigItemError(
            f"Unable to read app configuration with unsupported type: {config_item}"
        )
    return config_item
