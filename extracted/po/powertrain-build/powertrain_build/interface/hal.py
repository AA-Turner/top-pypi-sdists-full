# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Python module used for abstracting Hardware Abstraction Layer specifications"""
import re
from pathlib import Path
from ruamel.yaml import YAML
from powertrain_build.interface.csp_api import CspApi
from powertrain_build.lib import logger

LOGGER = logger.create_logger('base')


def get_hal_list(app):
    """Get translated hal name from yaml file

    Args:
        app (Application): Pybuild project
    Returns:
        cmake (str): a string contains translated hal name
    """
    translation_files = app.get_translation_files()
    hala = HALA(app)
    hala.parse_definition(translation_files)
    hal_translations = hala.get_map()

    hals = set()
    for definitions in hala.translations.values():
        for definition in definitions:
            hal_abbreviation = definition[hala.position.api.value]
            real_hal_name = get_real_hal_name(hal_abbreviation, hal_translations)
            hals.add((hal_abbreviation, real_hal_name))

    cmake = ""
    for hal_abbreviation, real_hal_name in hals:
        lib = re.sub('-', '_', f'hal_{hal_abbreviation}' + '_libhal_' + real_hal_name).upper()
        include = re.sub('-', '_', f'hal_{hal_abbreviation}' + '_include_dir').upper()
        cmake += f"LIST(APPEND extra_libraries ${{{lib}}})\n"
        cmake += f"LIST(APPEND EXTRA_INCLUDE_DIRS ${{{include}}})\n"
    return cmake


def strip_hal_name(hal_name):
    """Strip hal name

    Args:
        hal_name (str): hal name
    Returns:
        (str): stripped hal name
    """
    return hal_name.replace('_hal', '')


def verify_name(hal_name, api_map):
    """Verify hal name

    Args:
        hal_name (str): hal name
        api_map (dict): hal translation map
    """
    if strip_hal_name(hal_name) not in api_map:
        raise HalTranslationException(
            f"{hal_name} does not exist in the hal translation file."
        )


def get_real_hal_name(hal_name, translation_map):
    """Get real hal name from translation map file.

    Args:
        hal_name (str): hal abreviation

    Returns:
        real_hal_name (str): real name of a hal
    """
    verify_name(hal_name, translation_map)
    return translation_map.get(strip_hal_name(hal_name))


class UnknownAccessorError(Exception):
    """Error when setting a producer and there already exists one"""
    def __init__(self, hal, signal, accessor):
        """Set error message

        Args:
            hal (HAL): Hal where the problem is
            signal (Signal): Signal with the problem
            accessor (str): Unknown accessor type
        """
        super().__init__()
        self.message = f"Accessor of type {accessor} for {signal.name} in {hal.name} is not handled"


class HalTranslationException(Exception):
    """Class for hal translation exceptions"""


class HALA(CspApi):
    """Hardware abstraction layer abstraction"""

    def __repr__(self):
        """String representation of HALA"""
        return (f"<HALA {self.name}"
                f" app_side insignals: {len(self.signal_names['app']['insignals'])}"
                f" app_side outsignals: {len(self.signal_names['app']['outsignals'])}>")

    def get_map(self):
        """Get hal translation map

        Returns:
            (dict): hal translation map
        """
        path = self.get_map_file()
        if path.is_file():
            return self._get_hal_translation(path)
        return {}

    @staticmethod
    def get_map_file():
        """Get hal translation map file

        Returns:
            (Path): hal translation map file
        """
        return Path("Projects", "CSP", "hal_list.yaml")

    def get_api_name(self, api_name):
        real_hal_name = get_real_hal_name(
            api_name,
            self.api_map
        )
        return real_hal_name

    def verify_api(self, api_name):
        verify_name(api_name, self.api_map)

    @staticmethod
    def _get_hal_translation(path):
        """Get translated hal names

        Args:
            path (Path): path to the hal translation list.
        Returns:
            hal_translation_content (dict): translated hal names
        """
        hal_translation_content = None
        if path and path.is_file():
            with path.open("r") as file_handler:
                yaml = YAML(typ="safe", pure=True)
                hal_translation_content = yaml.load(file_handler)

        if not hal_translation_content:
            if hal_translation_content is None:
                raise HalTranslationException(
                    "No hal translation file given."
                )
            if isinstance(hal_translation_content, dict):
                raise HalTranslationException(
                    "Hal translation file are empty."
                )
            raise HalTranslationException("Bad hal translation format.")
        return hal_translation_content

    def check_endpoints(self):
        pass

    def extract_endpoint_definitions(self, raw):
        """Extract endpoint definitions from raw data

        Args:
            (dict): endpoint definitions
        """
        self.parse_api_definitions(raw.get("hal", {}))

    @staticmethod
    def extract_definition(definition):
        """Extract definition from hal

        Args:
            definition (dict): hal definition

        Returns:
            (dict): hal definition
        """
        if isinstance(definition, list):
            specifications = {
                'hals': definition
            }
        else:
            specifications = {
                'properties': definition.get('properties', []),
                'methods': definition.get('methods', [])
            }
        return specifications
