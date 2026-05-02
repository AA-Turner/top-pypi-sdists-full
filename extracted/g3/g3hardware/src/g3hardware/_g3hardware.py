from __future__ import annotations

import collections.abc
import itertools
import jinja2
import logging
import os
import re
import typing
import yaml

from dataclasses import dataclass
from lxml import etree


logger = logging.getLogger('g3hardware')


class HardwareModuleConfigItemDict(typing.TypedDict):
    """
    A typed dictionary representing configuration data of a hardware module.
    """
    type: str
    """The type of the hardware module."""
    version: str
    """The firmware version of the hardware module."""
    settings: typing.NotRequired[typing.Optional[str]]
    """The settings template for the hardware module."""
    tb: typing.NotRequired[typing.Optional[str]]
    """The Terminal Base module type for the hardware module."""
    bm: typing.NotRequired[typing.Optional[str]]
    """The Bus module type for the hardware module."""


@dataclass
class HardwareModuleConfigQuery:
    """
    A dataclass representing a hardware module configuration query result.
    """
    type: str
    """The type of the hardware module."""
    key: str
    """The key in the module configuration data."""
    is_type_found: bool = False
    """A flag indicating if the module type is found in the configuration."""
    is_key_found: bool = False
    """A flag indicating if the key is found in the module configuration."""
    value: typing.Optional[str] = None
    """The value of the key in the module configuration."""

    def is_found(self) -> bool:
        """Check if the module type and key are found in the configuration.

        Returns:
            bool: True if the module type and key are found, False otherwise.
        """
        return self.is_type_found and self.is_key_found


def load_config() -> dict[str, HardwareModuleConfigItemDict]:
    """Load the configuration data from the labrary's "config.yaml" file.

    Returns:
        dict[str, HardwareModuleConfigItemDict]: The configuration data.\
            Dictionary keys are lowercase module types, and values are\
            dictionaries containing the module type, firmware version,\
            settings template, Terminal Base module type, and Bus module type.
    """
    py_module_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(py_module_dir, 'config.yaml')
    with open(config_file, 'r') as f:
        data = yaml.safe_load(f)
    config: dict[str, HardwareModuleConfigItemDict] = {}
    for key, value in data.items():
        value['type'] = key
        value.setdefault('tb', None)
        value.setdefault('bm', None)
        version = value.setdefault('version', None)
        if version is not None:
            value['version'] = version.strip()
        settings = value.setdefault('settings', None)
        if settings is not None:
            value['settings'] = settings.strip()
        config[key.lower()] = value
    return config


class HardwareModuleConfig:
    """
    A utility providing methods for formatting module types and retrieving
    terminal base module types, bus module types, and settings templates
    for a given module type.

    The configuration data is loaded from the "config.yaml" file. Note that
    this utility is intended to be used as a singleton, and the configuration
    data is loaded only once when the module is imported and is shared among
    all instances of the class.
    """
    _config = load_config()

    @classmethod
    def update(cls, item: HardwareModuleConfigItemDict) -> None:
        """Update the configuration dictionary with the given item.

        Args:
            item (HardwareModuleConfigItemDict): The item to be added or\
                updated in the configuration dictionary. The item must include\
                the following keys: "type" (str, required, the type of\
                the module), "version" (str, required, the firmware version of\
                the module), "settings" (str | None, optional, the settings\
                template for the module), "tb" (str | None, optional,\
                the Terminal Base module type, "bm" (str | None, optional,\
                the Bus module type).
        """
        item.setdefault('settings', None)
        cls._config[item['type'].lower()] = item

    @classmethod
    def _get_value(
        cls, type_: str, itemdict_key: str, empty_str_to_none: bool = False
    ) -> HardwareModuleConfigQuery:
        """Retrieve a value from a `HardwareModuleConfigItemDict` assosiated
        with the given module type.

        Args:
            type_ (str): The type of the hardware module.
            itemdict_key (str): The key corresponding to the value in\
                the module's `HardwareModuleConfigItemDict` dictionary.
            empty_str_to_none (bool): If True, an empty string value will be\
                converted to None. Default is False.

        Returns:
            HardwareModuleConfigQuery: A query result object containing\
                the retrieved value and the query status.
        """
        logger.debug(
            'Retrieving "%s" for module "%s" from the configuration data.',
            itemdict_key, type_
            )
        result = HardwareModuleConfigQuery(type_, itemdict_key)
        item_data = cls._config.get(type_.lower().strip())
        if item_data is None:
            logger.warning('No data found for module "%s".', type_)
            return result
        result.is_type_found = True
        if itemdict_key not in item_data:
            logger.warning(
                'No value found for module key "%s/%s".', type_, itemdict_key
                )
            return result
        result.is_key_found = True
        value = item_data[itemdict_key]  # type: ignore
        if value == '':
            if empty_str_to_none:
                logger.debug(
                    'Retrieved value is an empty string. Converting to None.'
                    )
                value = None
            else:
                logger.debug('Retrieved value is an empty string.')
        result.value = value
        return result

    @classmethod
    def format_type(cls, type_: str) -> str:
        """Format the given module type to a standard form, if possible.
        For example, type "x20csl8101" is formatted to "X20cSL8101".

        Args:
            type_ (str): The module type to be formatted.

        Returns:
            str: The formatted module type.
        """
        logger.debug('Formatting type "%s".', type_)
        formatted = cls._get_value(type_, 'type')
        if not formatted.value:
            logger.warning('Failed to format type "%s".', type_)
            return type_
        if (value := formatted.value) != type_:
            logger.debug('Formatted type "%s" to "%s".', type_, value)
        else:
            logger.debug('Type "%s" is already formatted.', type_)
        return value

    @classmethod
    def get_tb(cls, type_: str) -> HardwareModuleConfigQuery:
        """Get the Terminal Base module for the specified type.

        Args:
            type_ (str): The type of terminal.

        Returns:
            str | None: The Terminal Base module if found, None otherwise.
        """
        return cls._get_value(type_, 'tb', empty_str_to_none=True)

    @classmethod
    def get_bm(cls, type_: str) -> HardwareModuleConfigQuery:
        """Get the Bus module for a given type.

        Args:
            type_ (str): The type of the bus module.

        Returns:
            Optional[str]: The Bus module if found, None otherwise.
        """
        return cls._get_value(type_, 'bm', empty_str_to_none=True)

    @classmethod
    def get_settings(cls, type_: str) -> HardwareModuleConfigQuery:
        """Get the settings for a given type.

        Args:
            type_ (str): The type of the settings.

        Returns:
            Optional[str]: The settings if found, None otherwise.
        """
        return cls._get_value(type_, 'settings', empty_str_to_none=False)

    @classmethod
    def get_version(cls, type_: str) -> HardwareModuleConfigQuery:
        """Get the firmware version for a given type.

        Args:
            type_ (str): The type of the firmware version.

        Returns:
            Optional[str]: The firmware version if found, None otherwise.
        """
        return cls._get_value(type_, 'version', empty_str_to_none=False)


def format_type(type_: str) -> str:
    """Format the given module type to a standard form, if possible.
    For example, type "x20csl8101" is formatted to "X20cSL8101".

    Args:
        type_ (str): The module type to be formatted.

    Returns:
        str: The formatted module type.
    """
    return HardwareModuleConfig.format_type(type_)


class HardwareModuleSettingsTemplateLoader(jinja2.BaseLoader):
    """
    A custom Jinja2 template loader.

    This loader retrieves the settings templates for hardware module
    from the `HardwareModuleConfig` utility.
    """
    def get_source(
        self, environment: jinja2.Environment, template: str
    ) -> tuple[str, str | None, typing.Callable[[], bool] | None]:
        result = HardwareModuleConfig.get_settings(template)
        if result.is_key_found is False:
            raise jinja2.exceptions.TemplateNotFound(template)
        template_contents = result.value or ''
        return template_contents, None, lambda: True


class HardwareModuleSettingsTemplateFormatter:
    """
    A utility providing methods for loading and formatting hardware module
    templates using the Jinja2 templating engine.
    """

    def __init__(self):
        self.env = jinja2.Environment(
            loader=HardwareModuleSettingsTemplateLoader(),
            undefined=jinja2.make_logging_undefined(
                logger, jinja2.DebugUndefined
                )
            )

    def get_template(self, type_: str) -> jinja2.Template:
        """Get the template for a module of the specified type. If no template
        if found for the specified type, the default template will be used.

        Args:
            type_: The type of the module.

        Returns:
            The Jinja2 template for the module.
        """
        type_ = HardwareModuleConfig.format_type(type_)
        logger.info('Loading settings template for module "%s".', type_)
        try:
            return self.env.get_template(type_)
        except jinja2.exceptions.TemplateNotFound:
            logger.error(
                'No template found for module of type "%s". '
                'Default template will be used instead.', type_
                )
            try:
                return self.env.get_template('default')
            except jinja2.exceptions.TemplateNotFound:
                raise RuntimeError(
                    'No default template found. Please make sure that '
                    'the "default" key exists in "g3hardware/config.yaml".'
                    )

    def format_template(self, template: jinja2.Template, **kwargs) -> str:
        """Render the given Jinja2 template with the provided arguments.

        Args:
            template (jinja2.Template): The Jinja2 template to render.
            **kwargs: Keyword arguments to pass to the template.

        Returns:
            str: The rendered template as a string.
        """
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Rendering settings template with args: %s.', kwargs)
        else:
            logger.info('Rendering settings template.')
        return template.render(**kwargs)


class HardwareModuleFactory:
    """
    A factory class for creating hardware modules with their dependencies.
    """

    def __init__(self) -> None:
        # 1 is reserved for X20cSL8101
        self._safemoduleid_counter = itertools.count(2)

    def reset_safemoduleid_counter(self) -> None:
        """Reset the safemoduleid counter to 2."""
        self._safemoduleid_counter = itertools.count(2)

    @staticmethod
    def _get_required_dependency(
        type_: str, dep_type: typing.Literal['tb', 'bm']
    ) -> str:
        """Get the required dependency module based on
        the given module type and dependency type.

        Args:
            type_ (str): The type of the module requiring the dependency.
            dep_type (typing.Literal['tb', 'bm']): The type of\
                the dependency module.

        Returns:
            str: The required dependency module.

        Raises:
            ValueError: If the dependency type is invalid.
            RuntimeError: If a dependency module is required but not found.
        """
        if dep_type == 'tb':
            dep = HardwareModuleConfig.get_tb(type_)
        elif dep_type == 'bm':
            dep = HardwareModuleConfig.get_bm(type_)
        else:
            raise ValueError(f'Invalid dependency type "{dep_type}".')
        if not dep.is_found() or dep.value is None:
            raise RuntimeError('A dependency module is required.')
        return dep.value

    def _init_module(
        self, type_: str, name_suffix: str, **kwargs
    ) -> HardwareModule:
        """Create a new `HardwareModule` object.

        Args:
            type_ (str): The type of the module.
            name_suffix (str): The suffix to be added to the module name.
            **kwargs: Additional keyword arguments to be passed to\
                the `HardwareModule` constructor to format module settings.

        Returns:
            HardwareModule: The newly created `HardwareModule` object.
        """
        type_ = HardwareModuleConfig.format_type(type_)
        if (
            is_safety_type(type_) and  # only safety modules need this
            ((type_ != 'X20cSL8101') and        # (except for X20cSL8101)
            (type_ != 'X20cSL8100')) and         # (except for X20cSL8100)
            'safemoduleid' not in kwargs
        ):
            safemoduleid = next(self._safemoduleid_counter)
            kwargs['safemoduleid'] = safemoduleid
        return HardwareModule(type_, name=f'{type_}_{name_suffix}', **kwargs)

    def _new_default(
        self, type_: str, name_suffix: str, **kwargs
    ) -> HardwareModule:
        """Create a standard `HardwareModule` object with its optional
        Bus module and Terminal Base module dependencies based on
        the given module type and name suffix of the module group.

        Args:
            type_ (str): The type of the hardware module.
            name_suffix (str): The suffix to be added to the name\
                of the hardware module.
            **kwargs: Additional keyword arguments to be passed to\
                the module constructor to format module settings.

        Returns:
            HardwareModule: The created default `HardwareModule` object.
        """
        module = self._init_module(type_, name_suffix, **kwargs)
        logger.info('Creating dependencies for module "%s".', module.name)
        if (tb_type := HardwareModuleConfig.get_tb(type_).value):
            tb = self._init_module(tb_type, name_suffix, **kwargs)
            module.add_dependency(tb)
            module.add_connection('SS1', tb, 'SS')
        if (bm_type := HardwareModuleConfig.get_bm(type_).value):
            bm = self._init_module(bm_type, name_suffix, **kwargs)
            module.add_dependency(bm)
            module.add_connection('SL', bm, 'SL1')
        return module

    def _new_sl8101(self, name_suffix: str, **kwargs) -> HardwareModule:
        """Create an instance of the X20cSL8101 hardware module and
        its dependencies with the specified name suffix and
        additional settings arguments.

        Args:
            name_suffix (str): The suffix to be added to the module name and\
                the names of its dependencies.
            **kwargs: Additional keyword arguments to be passed to\
                the module constructor to format module settings.

        Returns:
            HardwareModule: The created X20cSL8101 hardware module instance.
        """
        sl8101 = self._init_module('X20cSL8101', name_suffix, **kwargs)
        logger.info('Creating dependencies for module "%s".', sl8101.name)
        tb_type = self._get_required_dependency('X20cSL8101', 'tb')
        tb = self._init_module(tb_type, name_suffix, **kwargs)
        mk0213 = self._init_module('X20cMK0213', name_suffix, **kwargs)
        sl8101.add_dependency(tb)
        sl8101.add_dependency(mk0213)
        sl8101.add_connection('SS1', tb, 'SS')
        mk0213.add_connection('SL', sl8101, 'SL1')
        return sl8101

    def _new_sl8100(self, name_suffix: str, **kwargs) -> HardwareModule:
        """Create an instance of the X20cSL8100 hardware module and
        its dependencies with the specified name suffix and
        additional settings arguments.

        Args:
            name_suffix (str): The suffix to be added to the module name and\
                the names of its dependencies.
            **kwargs: Additional keyword arguments to be passed to\
                the module constructor to format module settings.

        Returns:
            HardwareModule: The created X20cSL8100 hardware module instance.
        """
        sl8100 = self._init_module('X20cSL8100', name_suffix, **kwargs)
        logger.info('Creating dependencies for module "%s".', sl8100.name)
        tb_type = self._get_required_dependency('X20cSL8100', 'tb')
        tb = self._init_module(tb_type, name_suffix, **kwargs)
        mk0213 = self._init_module('X20cMK0213', name_suffix, **kwargs)
        sl8100.add_dependency(tb)
        sl8100.add_dependency(mk0213)
        sl8100.add_connection('SS1', tb, 'SS')
        mk0213.add_connection('SL', sl8100, 'SL1')
        return sl8100

    def _new_bc0083(self, name_suffix: str, **kwargs) -> HardwareModule:
        """Create an instance of the X20cBC0083 hardware module and
        its dependencies with the specified name suffix and
        additional settings arguments.

        Args:
            name_suffix (str): The suffix to be added to the module name and\
                the names of its dependencies.
            **kwargs: Additional keyword arguments to be passed to\
                the module constructor to format module settings.

        Returns:
            HardwareModule: The created X20cBC0083 hardware module instance.
        """
        bc0083 = self._init_module('X20cBC0083', name_suffix, **kwargs)
        logger.info('Creating dependencies for module "%s".', bc0083.name)
        bb_type = self._get_required_dependency('X20cBC0083', 'bm')
        tb_type = self._get_required_dependency('X20cBC0083', 'tb')
        bb = self._init_module(bb_type, name_suffix, **kwargs)
        tb = self._init_module(tb_type, name_suffix, **kwargs)
        ps9400 = self._init_module('X20cPS9400', name_suffix, **kwargs)
        bc0083.add_dependency(bb)
        bc0083.add_dependency(tb)
        bc0083.add_dependency(ps9400)
        bc0083.add_connection('SL', bb, 'SL1')
        ps9400.add_connection('PS', bb, 'PS1')
        ps9400.add_connection('SS1', tb, 'SS')
        return bc0083

    def _new_bc8083(self, name_suffix: str, **kwargs) -> HardwareModule:
        """Create an instance of the X20cBC8083 hardware module and
        its dependencies with the specified name suffix and
        additional settings arguments.

        Args:
            name_suffix (str): The suffix to be added to the module name and\
                the names of its dependencies.
            **kwargs: Additional keyword arguments to be passed to\
                the module constructor to format module settings.

        Returns:
            HardwareModule: The created X20cBC8083 hardware module instance.
        """
        bc8083 = self._init_module('X20cBC8083', name_suffix, **kwargs)
        logger.info('Creating dependencies for module "%s".', bc8083.name)
        bb_type = self._get_required_dependency('X20cBC8083', 'bm')
        tb_type = self._get_required_dependency('X20cBC8083', 'tb')
        bb = self._init_module(bb_type, name_suffix, **kwargs)
        tb = self._init_module(tb_type, name_suffix, **kwargs)
        hb2821 = self._init_module('X20cHB2881', name_suffix, **kwargs)
        ps9400 = self._init_module('X20cPS9400', name_suffix, **kwargs)
        bc8083.add_dependency(bb)
        bc8083.add_dependency(tb)
        bc8083.add_dependency(hb2821)
        bc8083.add_dependency(ps9400)
        bc8083.add_connection('SL', bb, 'SL1')
        hb2821.add_connection('SS', bb, 'SS1')
        ps9400.add_connection('PS', bb, 'PS1')
        ps9400.add_connection('SS1', tb, 'SS')
        return bc8083

    def _new_si9100(self, name_suffix: str, **kwargs) -> HardwareModule:
        """Create an instance of the X20cSI9100 hardware module and
        its dependencies with the specified name suffix and
        additional settings arguments.

        Args:
            name_suffix (str): The suffix to be added to the module name and\
                the names of its dependencies.
            **kwargs: Additional keyword arguments to be passed to\
                the module constructor to format module settings.

        Returns:
            HardwareModule: The created X20cSI9100 hardware module instance.
        """
        si9100 = self._init_module('X20cSI9100', name_suffix, **kwargs)
        logger.info('Creating dependencies for module "%s".', si9100.name)
        bm_type = self._get_required_dependency('X20cSI9100', 'bm')
        tb_type = self._get_required_dependency('X20cSI9100', 'tb')
        bm = self._init_module(bm_type, name_suffix)
        tb_1 = self._init_module(tb_type, f'{name_suffix}_1')
        tb_2 = self._init_module(tb_type, f'{name_suffix}_2')
        si9100.add_dependency(bm)
        si9100.add_dependency(tb_1)
        si9100.add_dependency(tb_2)
        si9100.add_connection('SS1', tb_1, 'SS')
        si9100.add_connection('SS2', tb_2, 'SS')
        si9100.add_connection('SL', bm, 'SL1')
        return si9100

    def new(self, type_: str, name_suffix: str, **kwargs) -> HardwareModule:
        """Create a new hardware module and its dependencies based on
        the given type and the name suffix. The dependencies are
        connected to the module according to the module type.

        Args:
            type_ (str): The type of the hardware module (case insensitive).
            name_suffix (str): The suffix to be added to the module name and\
                the names of its dependencies. For example, if the module type\
                is "X20cDI9371" and the name suffix is "A", the module name\
                will be "X20cDI9371_A", and the names of its dependencies\
                will be "X20TB12_A" and "X20cBM11_A".

            **kwargs: Additional keyword arguments to be passed to
                the module constructor to format module settings.

        Returns:
            HardwareModule: The created hardware module.
        """
        special_types = {
            'x20csl8100': self._new_sl8100,
            'x20csl8101': self._new_sl8101,
            'x20cbc0083': self._new_bc0083,
            'x20cbc8083': self._new_bc8083,
            'x20csi9100': self._new_si9100,
            }
        type_lower = type_.lower()
        if (type_lower) in special_types:
            create_method = special_types[type_lower]
            return create_method(name_suffix, **kwargs)
        return self._new_default(type_, name_suffix, **kwargs)


class HardwareModuleConnectionDict(typing.TypedDict):
    """A typed dictionary representing module connection data."""
    module: HardwareModule
    """The connected module."""
    conn: typing.Optional[etree._Element]
    """The connection XML element."""


class HardwareModule:
    """
    A hardware module representation.

    This class provides methods for creating, formatting, and managing hardware
    modules and their dependencies. It also provides methods for adding and
    removing connections between modules. Finally, it provides methods for
    converting the module and its dependencies to a string representation.
    """
    _version_pattern = re.compile(r"\d+\.\d+\.\d+\.\d+")
    _template_formatter = HardwareModuleSettingsTemplateFormatter()
    _factory = HardwareModuleFactory()
    DEFAULT_VERSION = '1.0.0.0'
    """The default firmware version for a hardware module."""

    def __init__(
        self,
        type_: str,
        name: str,
        version: str | None = None,
        **settings_template_kwargs
    ) -> None:
        """Create a new hardware module.

        Args:
            type_ (str): The type of the hardware module (case insensitive).
            name (str): The name of the hardware module.
            version (str | None, optional): The firmware version of\
                the hardware module. If None, the default version is used.\
                Default is None.
        """
        type_ = HardwareModuleConfig.format_type(type_)
        logger.info('Creating new module "%s" of type "%s".', name, type_)
        version = self._init_get_version(version, type_)
        settings = self._init_get_settings(type_, **settings_template_kwargs)
        self._xml = self._init_get_module_xml(type_, name, version, settings)
        self._dependencies: dict[str, HardwareModule] = {}
        self._connections: dict[str, HardwareModuleConnectionDict] = {}
        logger.info(
            'New module "%s" of type "%s" has been created.', name, type_
            )

    def __str__(self) -> str:
        return self.to_str(with_dependencies=False)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(name="{self.name}", '
            f'type="{self.type_}", version="{self.version}")'
            )

    def _init_get_version(self, version: str | None, type_: str) -> str:
        """Validate the firmware version for the hardware module.

        Args:
            version (str | None): The firmware version of the module.\
                If None, the default version from the module configuration\
                data will be used. If the default version is not found,\
                the global `DEFAULT_VERSION` value will be used.
            type_ (str): The type of the hardware module.

        Returns:
            str: The validated firmware version for the hardware module.
        """
        if version is None:
            result = HardwareModuleConfig.get_version(type_)
            if result.is_found() and result.value:
                version = result.value
            else:
                logger.warning(
                    'No firmware version found for module type "%s". '
                    'Using default version "%s".', type_, self.DEFAULT_VERSION
                    )
                version = self.DEFAULT_VERSION
        self._validate_version(version)
        return version

    def _init_get_settings(self, type_: str, **kwargs) -> str:
        """Get the formatted settings XML template for the hardware module.

        Args:
            type_ (str): The type of the hardware module.

        Returns:
            str: The formatted settings for the hardware module.
        """
        return self._template_formatter.format_template(
            self._template_formatter.get_template(type_), **kwargs
            )

    def _init_get_module_xml(
        self, type_: str, name: str, version: str, settings: str | None
    ) -> etree._Element:
        """Create the XML representation of the hardware module.

        Args:
            type_ (str): The type of the hardware module.
            name (str): The name of the hardware module.
            version (str): The firmware version of the hardware module.
            settings (str | None): The settings XML template for the module.

        Returns:
            etree._Element: The XML representation of the hardware module.
        """
        if settings:
            if "X20cCP" in type_:
                xml = (
                    f'<Module Type="{type_}" Name="CPU" Version="{version}">'
                    f'{settings}'
                    f'</Module>'
                    )
            else:
                xml = (
                    f'<Module Type="{type_}" Name="{name}" Version="{version}">'
                    f'{settings}'
                    f'</Module>'
                    )
        else:
            xml = f'<Module Type="{type_}" Name="{name}" Version="{version}"/>'
        return etree.fromstring(xml)

    @classmethod
    def new(cls, type_: str, name_suffix: str, **kwargs) -> HardwareModule:
        """Create a new hardware module and its dependencies based on
        the given type and the name suffix. The dependencies are
        connected to the module according to the module type.

        Args:
            type_ (str): The type of the hardware module (case insensitive).
            name_suffix (str): The suffix to be added to the module name and\
                the names of its dependencies. For example, if the module type\
                is "X20cDI9371" and the name suffix is "A", the module name\
                will be "X20cDI9371_A", and the names of its dependencies\
                will be "X20TB12_A" and "X20cBM11_A".

            **kwargs: Additional keyword arguments to be passed to
                the module constructor to format module settings.

        Returns:
            HardwareModule: The created hardware module.
        """
        return cls._factory.new(type_, name_suffix, **kwargs)

    @classmethod
    def reset_safemoduleid_counter(cls) -> None:
        """Reset the safemoduleid counter to 2 (the counter is used by
        the `new` constructor to assign unique safemoduleid values
        to safety modules).
        """
        cls._factory.reset_safemoduleid_counter()

    @property
    def is_safety(self) -> bool:
        """Check if the hardware module is a safety module."""
        return is_safety_type(self.type_)

    @property
    def xml(self) -> etree._Element:
        """The XML representation of the hardware module."""
        return self._xml

    def _get_attrib_as_str(self, attrib: str) -> str:
        """Get the value of the specified XML attribute as a string.

        Args:
            attrib (str): The name of the attribute.

        Returns:
            str: The value of the attribute as a string.
        """
        value = self._xml.attrib[attrib]
        if isinstance(value, bytes):
            return value.decode()
        return value

    @property
    def name(self) -> str:
        """The name of the hardware module."""
        return self._get_attrib_as_str('Name')

    @name.setter
    def name(self, name: str) -> None:
        """Set the 'Name' XML attribute of the hardware module.

        Args:
            name (str): The new name of the hardware module.
        """
        self._xml.attrib['Name'] = name

    @property
    def type_(self) -> str:
        """The type of the hardware module."""
        return self._get_attrib_as_str('Type')

    def _validate_version(self, version: str) -> None:
        """Validate the firmware version of the hardware module.

        Args:
            version (str): The firmware version to validate.

        Raises:
            ValueError: If the version is invalid.
        """
        if re.match(self._version_pattern, version) is None:
            raise ValueError(
                f'Invalid firmware version "{version}". '
                f'Expected format: "X.Y.Z.W".'
                )

    @property
    def version(self) -> str:
        """The firmware version of the hardware module."""
        return self._get_attrib_as_str('Version')

    @version.setter
    def version(self, version: str) -> None:
        """Set the 'Version' XML attribute of the hardware module.

        Args:
            version (str): The new firmware version of the hardware module.
        """
        self._validate_version(version)
        self._xml.attrib['Version'] = version

    @property
    def dependencies(self) -> dict[str, HardwareModule]:
        """A dictionary of dependency modules of the hardware module
        (Bus modules, Terminal Block modules, etc.). The keys are
        the names of the dependency modules, and the values are
        the dependency modules themselves.
        """
        return {dep.name: dep for dep in self._dependencies.values()}

    @property
    def connections(self) -> dict[str, HardwareModule]:
        """A dictionary of connected modules. The keys are the names
        of the connected modules, and the values are the connected modules
        themselves.
        """
        return {
            conn: conn_data['module']
            for conn, conn_data in self._connections.items()
            }

    def add_dependency(self, dependency: HardwareModule) -> None:
        """Add a dependency module to the current hardware module.

        Args:
            dependency (HardwareModule): The dependency module to be added.

        Raises:
            ValueError: If the dependency is already registered.
        """
        if dependency.name in self._dependencies:
            raise ValueError(
                f'Module "{dependency.name}" is already registered '
                f'as a dependency of module "{self.name}".'
                )
        self._dependencies[dependency.name] = dependency

    def remove_dependency(self, dependency: HardwareModule) -> None:
        """Remove a dependency module from the hardware module.

        Args:
            dependency (HardwareModule): The dependency to be removed.
        """
        if dependency.name in self._dependencies:
            del self._dependencies[dependency.name]

    @staticmethod
    def _get_connection_xml(
        connector: str, target_module: str, target_connector: str
    ) -> etree._Element:
        """Create an XML representation of a connection between
        two hardware modules.

        Args:
            connector (str): Type of the connector of the current module.
            target_module (str): Name of the target module.
            target_connector (str): Type of the connector of the target module.

        Returns:
            etree._Element: The XML representation of the connection.
        """
        return etree.Element(
            'Connection',
            Connector=connector,
            TargetModule=target_module,
            TargetConnector=target_connector
            )

    @staticmethod
    def _get_cable_xml(
        cable_type: str, length: float, version: str
    ) -> etree._Element:
        """Create an XML representation of a cable.

        Args:
            cable_type (str): Type of the cable.
            length (float): Length of the cable.
            version (str): Version of the cable.

        Returns:
            etree._Element: The XML representation of the cable.
        """
        return etree.Element(
            'Cable',
            Type=cable_type,
            Length=str(length),
            Version=version
            )

    @staticmethod
    def _get_conn_dict(
        module: HardwareModule, conn: etree._Element | None
    ) -> HardwareModuleConnectionDict:
        """Instantiate a `HardwareModuleConnectionDict` connection dictionary.

        Args:
            module (HardwareModule): The connected module.
            conn (etree._Element | None): The connection XML element.

        Returns:
            HardwareModuleConnectionDict: The connection typed dictionary.
        """
        return {'module': module, 'conn': conn}

    def add_connection(
        self,
        connector: str,
        target_module: HardwareModule,
        target_connector: str
    ) -> None:
        """Add a connection between the current module and another module.

        Args:
            connector (str): Type of the connector of the current module.
            target_module (HardwareModule): The module to connect to.
            target_connector (str): Type of the connector of the target module.
        """
        self.remove_connection(connector)
        connection = self._get_connection_xml(
            connector, target_module.name, target_connector
            )
        self._xml.append(connection)
        conn_self = self._get_conn_dict(target_module, connection)
        self._connections[connector] = conn_self
        conn_target = target_module._get_conn_dict(self, None)
        target_module._connections[target_connector] = conn_target

    def add_connection_plk(
        self,
        connector: str,
        target_module: HardwareModule,
        target_connector: str,
        node_number: typing.Optional[int] = None,
        cable_length: float = 10.0,
        cable_version: str = '1.0.0.3',
    ) -> None:
        """Add a PLK connection between the current module and another module.

        Args:
            connector (str): Type of the connector of the current module.
            target_module (HardwareModule): The module to connect to.
            target_connector (str): Type of the connector of the target module.
            node_number (typing.Optional[int], optional): The node number of\
                the connection. Defaults to None.
            cable_length (float, optional): The length of the POWERLINK cable.\
                Defaults to 10.0.
            cable_version (str, optional): The version of the POWERLINK cable.\
                Defaults to '1.0.0.3'.
        """
        self.add_connection(connector, target_module, target_connector)
        if (connection := self._connections[connector]['conn']) is not None:
            if node_number is not None:
                connection.attrib['NodeNumber'] = str(node_number)
            cable = self._get_cable_xml(
                'PowerlinkCable', cable_length, cable_version
                )
            connection.append(cable)

    def _pop_connection(self, connector: str) -> HardwareModuleConnectionDict:
        """Remove a connection from the current module and return it.

        Args:
            connector (str): The connector to remove the connection from.

        Returns:
            HardwareModuleConnectionDict: The removed connection.
        """
        connection = self._connections.pop(connector)
        if (conn := connection['conn']) is not None:
            self._xml.remove(conn)
        return connection

    def remove_connection(self, connector: str) -> None:
        """Remove a connection from the current module.

        Args:
            connector (str): The connector to remove the connection from.
        """
        if connector in self._connections:
            connection = self._pop_connection(connector)
            connected_module = connection['module']
            other_connections = connected_module._connections
            for other_connector, other_connection in other_connections.items():
                if other_connection['module'] == self:
                    connected_module._pop_connection(other_connector)
                    break

    def to_str(self, with_dependencies: bool = True, **kwargs) -> str:
        """Convert the hardware module to a XML string representation.

        Args:
            with_dependencies (bool, optional): Include the dependencies\
                of the module in the string representation. Defaults to True.

        Returns:
            str: The XML string representation of the hardware module.
        """
        self_as_str = etree.tostring(self._xml, **kwargs).decode().strip()
        if with_dependencies is False:
            return self_as_str
        depenendencies_as_str = "\n".join(
            dep.to_str(with_dependencies=True, **kwargs)
            for dep in self._dependencies.values()
            )
        return f'{self_as_str}\n{depenendencies_as_str}'.strip()


class HardwareIsle(collections.abc.Sequence[HardwareModule]):
    """
    A hardware isle representation. A hardware isle is a sequence of
    hardware modules, where the first module is the "head" module, such as
    a CPU module, and the rest are "tail" modules.

    This class provides methods for creating, formatting, and managing hardware
    isles and their modules. It also provides methods for adding and removing
    connections between isles and their modules. Finally, it provides methods
    for converting the isle and its modules to a string representation.

    This class implements the `collections.abc.Sequence` interface, which
    allows to access the modules in the isle using indexing and iteration.
    The head module is always at index 0. It is also possible to connect
    hardware isles to each other, forming a chain of isles. Connected isles
    can be traversed in both directions using the `prev_isle` and `next_isle`
    properties.
    """
    HEAD_TYPES = ['X20cCP1584', 'X20cCP3687X', 'X20cCP1684', 'X20cSL8101', 'X20cSL8100', 'X20cBC0083', 'X20cBC8083']
    """The types of modules that can form a hardware isle."""
    POWERLINK_CABLE_LENGTH = 10
    """The default length of the POWERLINK cable."""
    POWERLINK_CABLE_VERSION = "1.0.0.3"
    """The default version of the POWERLINK cable."""
    _nodenumber_counter = itertools.count(2)

    def __init__(
        self,
        head: HardwareModule,
        *tail: HardwareModule
    ) -> None:
        """Create a new hardware isle.

        Args:
            head (HardwareModule): The head module of the hardware isle.\
                The head module must be a module that can form a hardware isle.
            *tail (HardwareModule): The tail modules of the hardware isle.

        Raises:
            TypeError: If the head module cannot form a hardware isle.
        """
        if not self.is_isle_head(head):
            raise TypeError(
                f'Module "{head.name}" of type "{head.type_}" '
                f'cannot form a hardware isle.'
                )
        self._modules: list[HardwareModule] = [head]
        for module in tail:
            self.connect(module)
        self.node_number = next(self._nodenumber_counter)
        self._prev_isle: typing.Optional[HardwareIsle] = None
        self._next_isle: typing.Optional[HardwareIsle] = None

    def __str__(self) -> str:
        return self.to_str(with_connected_isles=False)

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        tail = ", ".join(repr(module) for module in self.tail)
        return f'{cls_name}(head={repr(self.head)}, tail=*[{tail}])'

    @typing.overload
    def __getitem__(self, i: int) -> HardwareModule:
        ...

    @typing.overload
    def __getitem__(self, s: slice) -> list[HardwareModule]:
        ...

    def __getitem__(self, index: typing.Union[int, slice]):
        return self._modules[index]

    def __len__(self) -> int:
        return len(self._modules)

    @classmethod
    def reset_nodenumber_counter(cls) -> None:
        """Reset the nodenumber counter to 2."""
        cls._nodenumber_counter = itertools.count(2)

    @classmethod
    def is_isle_head(cls, module: HardwareModule) -> bool:
        """Check if the given module can be an Isle head.

        Args:
            module (HardwareModule): The module to check.

        Returns:
            bool: True if the module can be an Isle head, False otherwise.
        """
        return module.type_ in cls.HEAD_TYPES

    @property
    def head(self) -> HardwareModule:
        """The head module of the hardware isle."""
        return self._modules[0]

    @property
    def tail(self) -> list[HardwareModule]:
        """The tail modules of the hardware isle."""
        return self._modules[1:]

    @property
    def prev_isle(self) -> typing.Optional[HardwareIsle]:
        """The previous isle connected to the current isle."""
        return self._prev_isle

    @prev_isle.setter
    def prev_isle(self, isle: HardwareIsle) -> None:
        """Set the previous isle connected to the current isle.

        Args:
            isle (HardwareIsle): The previous isle to connect to.
        """
        isle._connect_isle(self)
        self._prev_isle = isle

    @property
    def next_isle(self) -> typing.Optional[HardwareIsle]:
        """The next isle connected to the current isle."""
        return self._next_isle

    @next_isle.setter
    def next_isle(self, isle: HardwareIsle) -> None:
        """Set the next isle connected to the current isle.

        Args:
            isle (HardwareIsle): The next isle to connect to.
        """
        self._connect_isle(isle)
        isle._prev_isle = self

    @staticmethod
    def _get_module_bm(module: HardwareModule) -> HardwareModule:
        """Get the Bus module (or Bus Base) dependency of a module.

        Args:
            module (HardwareModule): The module to get the Bus module\
                dependency from.

        Raises:
            ValueError: If the module does not have a Bus module or\
                Bus Base module dependency.

        Returns:
            HardwareModule: The Bus module dependency of the module.
        """
        for dep in module.dependencies.values():
            if is_bm_type(dep.type_):
                return dep
        raise ValueError(
            f'Module "{module.name}" of type "{module.type_}" '
            f'does not have a Bus module or Bus Base module depencency.'
            )

    def _get_tail_connector(self) -> tuple[HardwareModule, str]:
        """Get the target module and connector type for the tail module.

        Returns:
            tuple[HardwareModule, str]: The target module and connector type.
        """
        connect_to = self._modules[-1]
        match connect_to.type_:
            case "X20cCP1584":
                return connect_to, "IF6"
            case "X20cCP3687X":
                return connect_to, "IF6"
            case "X20cCP1684":
                return connect_to, "IF6"
            case "X20cSL8101":
                return connect_to, "IF1"
            case "X20cSL8100":
                return connect_to, "IF1"
            case "X20cBC0083" | "X20cBC8083":
                return self._get_module_bm(connect_to), "IF1"
            case _:
                return self._get_module_bm(connect_to), "X2X2"

    def _connect_to_cp1584(self, to_connect: HardwareIsle) -> None:
        """Connect the current isle to an isle with a X20cCP1584 head module.

        Args:
            to_connect (HardwareIsle): The isle to connect to.
        """
        to_connect.head.add_connection_plk(
            connector="PLK1",
            target_module=self.head,
            target_connector="IF3",
            node_number=self.node_number,
            cable_length=self.POWERLINK_CABLE_LENGTH,
            cable_version=self.POWERLINK_CABLE_VERSION
            )

    def _connect_to_X20cCP3687X(self, to_connect: HardwareIsle) -> None:
        """Connect the current isle to an isle with a X20cCP3687X head module.

        Args:
            to_connect (HardwareIsle): The isle to connect to.
        """
        to_connect.head.add_connection_plk(
            connector="PLK1",
            target_module=self.head,
            target_connector="IF3",
            node_number=self.node_number,
            cable_length=self.POWERLINK_CABLE_LENGTH,
            cable_version=self.POWERLINK_CABLE_VERSION
            )
        
    def _connect_to_X20cCP1684(self, to_connect: HardwareIsle) -> None:
        """Connect the current isle to an isle with a X20cCP1684 head module.

        Args:
            to_connect (HardwareIsle): The isle to connect to.
        """
        to_connect.head.add_connection_plk(
            connector="PLK1",
            target_module=self.head,
            target_connector="IF3",
            node_number=self.node_number,
            cable_length=self.POWERLINK_CABLE_LENGTH,
            cable_version=self.POWERLINK_CABLE_VERSION
            )

    def _connect_to_head(
        self, connector: str, target: HardwareIsle, target_connector: str
    ) -> None:
        """Connect the current isle to another isle.

        This is a generic utility method utilized by the `_connect_to_*`
        methods except `_connect_to_cp1584`.

        Args:
            connector (str): The connector type of the current isle.
            target (HardwareIsle): The isle to connect to.
            target_connector (str): The connector type of the target isle.
        """
        self.head.add_connection_plk(
            connector=connector,
            target_module=target.head,
            target_connector=target_connector,
            node_number=self.node_number,
            cable_length=self.POWERLINK_CABLE_LENGTH,
            cable_version=self.POWERLINK_CABLE_VERSION
            )
        target.head.add_connection_plk(
            connector=target_connector,
            target_module=self.head,
            target_connector=connector,
            node_number=target.node_number,
            cable_length=self.POWERLINK_CABLE_LENGTH,
            cable_version=self.POWERLINK_CABLE_VERSION
            )

    def _connect_to_sl0101_bc0083(self, to_connect: HardwareIsle) -> None:
        """Connect the current isle to an isle with a X20cSL8101 or X20cBC0083
        head module.

        Args:
            to_connect (HardwareIsle): The isle to connect to.
        """
        self._connect_to_head("PLK2", to_connect, "PLK1")

    def _connect_to_bc8083(self, to_connect: HardwareIsle) -> None:
        """Connect the current isle to an isle with a X20cBC8083 head module.

        Args:
            to_connect (HardwareIsle): The isle to connect to.
        """

        def get_module_dependency_hb2881(
            module: HardwareModule
        ) -> HardwareModule | None:
            """Get the X20cHB2881 module dependency of a given module.
            If there is no such dependency, return None.
            """
            for dep in module.dependencies.values():
                if dep.type_ == "X20cHB2881":
                    return dep
            return None

        if self.head.type_ != "X20cBC8083":
            self._connect_to_head("PLK2", to_connect, "PLK1")
        else:
            to_connect_hb2881 = get_module_dependency_hb2881(to_connect.head)
            isle_head_hb2881 = get_module_dependency_hb2881(self.head)
            if to_connect_hb2881 and isle_head_hb2881:
                isle_head_hb2881.add_connection_plk(
                    connector="ETH2",
                    target_module=to_connect_hb2881,
                    target_connector="ETH1",
                    cable_length=self.POWERLINK_CABLE_LENGTH,
                    cable_version=self.POWERLINK_CABLE_VERSION
                )
                to_connect_hb2881.add_connection_plk(
                    connector="ETH1",
                    target_module=isle_head_hb2881,
                    target_connector="ETH2",
                    cable_length=self.POWERLINK_CABLE_LENGTH,
                    cable_version=self.POWERLINK_CABLE_VERSION
                )
            else:
                self._connect_to_head("PLK2", to_connect, "PLK1")

    def _connect_isle(self, isle: HardwareIsle):
        """Connect the current isle to another isle.

        Args:
            isle (HardwareIsle): The isle to connect to.
        """
        connectors = {
            'X20cCP1584': self._connect_to_cp1584,
            'X20cCP3687X': self._connect_to_X20cCP3687X,
            'X20cCP1684': self._connect_to_X20cCP1684,
            'X20cSL8101': self._connect_to_sl0101_bc0083,
            'X20cSL8100': self._connect_to_sl0101_bc0083,
            'X20cBC0083': self._connect_to_sl0101_bc0083,
            'X20cBC8083': self._connect_to_bc8083
            }
        connector = connectors[self.head.type_]
        connector(isle)
        self._next_isle = isle

    def connect(self, module: HardwareModule | HardwareIsle) -> None:
        """Connect a hardware module or a hardware isle to the current isle.

        Note that if the given module is a module that forms a hardware isle,
        it must be connected as a hardware isle object. For example, if the
        module is a X20cCP1584 CPU module, it must form a hardware isle object,
        and this object can be then connected to the current isle.

        Args:
            module (HardwareModule | HardwareIsle): The module or isle\
                to connect to the current isle.

        Raises:
            TypeError: If the given hardware module is a module that forms\
                a hardware isle, but does not form a hardware isle.
        """
        if isinstance(module, HardwareIsle):
            self.next_isle = module
            return
        if self.is_isle_head(module):
            raise TypeError(
                f'Module "{module.name}" of type "{module.type_}" '
                f'must be added as a hardware isle object.'
                )
        module_bm = self._get_module_bm(module)
        target_module, target_connector = self._get_tail_connector()
        module_bm.add_connection("X2X1", target_module, target_connector)
        self._modules.append(module)

    def _isle_to_str(self, **kwargs) -> str:
        """Convert the modules in the `_modules` list of this hardware isle
        object to a single chained XML string representation.

        Returns:
            str: The XML string representation of the isle modules.
        """
        return '\n'.join(
            module.to_str(with_dependencies=True, **kwargs)
            for module in self._modules
            )

    def to_str(self, with_connected_isles: bool = True, **kwargs) -> str:
        """Convert the hardware isle to a XML string representation.

        This method effectively chains the XML string representations of
        the hardware modules in the isle. It also optionally includes
        the XML string representations of the connected isles.

        Args:
            with_connected_isles (bool, optional): Whether to include\
                connected isles in the representation. Defaults to True.

        Returns:
            str: The XML string representation of the hardware isle.
        """
        if with_connected_isles is False:
            self._isle_to_str(**kwargs)
        to_str: list[str] = []
        isle = self
        while isle.prev_isle:
            isle = isle.prev_isle
        while isle:
            to_str.append(isle._isle_to_str(**kwargs))
            isle = isle.next_isle  # type: ignore
        return '\n'.join(to_str)


def is_safety_type(type_: str) -> bool:
    """Check if the given module type if a safety module.

    Args:
        type_ (str): The module type to check (case sensitive).\
            Example: "X20cSL8101".

    Returns:
        bool: True if the module is a safety module, False otherwise.
    """
    return re.match(r"^X20c?(S)", type_) is not None


def is_tb_type(type_: str) -> bool:
    """Check if the given module is a Terminal Base module.

    Args:
        type_ (str): The module type to check (case sensitive).\
            Example: "X20TB12".

    Returns:
        bool: True if the module is a Terminal Base module, False otherwise.
    """
    return re.match(r"^X20TB\d{2}$", type_) is not None


def is_bm_type(type_: str) -> bool:
    """Check if the given module is a Bus module.

    Args:
        type_ (str): The module type to check (case sensitive).\
            Example: "X20TB12".

    Returns:
        bool: True if the module is a Bus module, False otherwise.
    """
    return re.match(r"^X20c?(BM|BB)\d{2}$", type_) is not None


def is_cpu_type(type_: str) -> bool:
    """Check if the given module is a CPU.

    Args:
        type_ (str): The module type to check (case sensitive).\
            Example: "X20cCP1584".

    Returns:
        bool: True if the module is a CPU module, False otherwise.
    """
    cpu_types = ['X20cCP1584','X20cCP3687X','X20cCP1684']
    return type_ in cpu_types


def is_isle_head_type(type_: str) -> bool:
    """Check if the given module type can form a hardware isle.

    Args:
        type_ (str): The module type to check (case sensitive).\
            Example: "X20cCP1584".

    Returns:
        bool: True if the module can form a hardware isle, False otherwise.
    """
    return type_ in HardwareIsle.HEAD_TYPES
