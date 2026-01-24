# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from .config_builder import ConfigBuilder
from .config_option import ConfigOption
from contrast.utils.configuration_utils import str_to_bool


class Inventory(ConfigBuilder):
    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(
                canonical_name="inventory.analyze_libraries",
                default_value=True,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="inventory.enable",
                default_value=True,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="inventory.tags", default_value="", type_cast=str
            ),
        ]
