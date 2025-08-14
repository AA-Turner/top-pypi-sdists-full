# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from .config_builder import ConfigBuilder
from .config_option import ConfigOption
from contrast.utils.configuration_utils import str_to_bool


class Reporting(ConfigBuilder):
    def __init__(self):
        super().__init__()

        self.default_options = [
            # This is an internal setting to stop Fireball from connecting
            # to TeamServer.
            ConfigOption(
                canonical_name="reporting.contrast.enable",
                default_value=True,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="reporting.logging.level",
                default_value=None,
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="reporting.logging.stdout",
                default_value=False,
                type_cast=str_to_bool,
            ),
        ]
