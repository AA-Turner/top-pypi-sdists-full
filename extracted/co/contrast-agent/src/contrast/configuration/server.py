# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from contrast.utils.configuration_utils import get_hostname

from .config_builder import ConfigBuilder
from .config_option import ConfigOption


class Server(ConfigBuilder):
    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(
                canonical_name="server.name",
                default_value=get_hostname(),
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="server.path", default_value="/", type_cast=str
            ),
            ConfigOption(canonical_name="server.type", default_value="", type_cast=str),
            ConfigOption(
                canonical_name="server.version", default_value="", type_cast=str
            ),
            ConfigOption(
                canonical_name="server.environment", default_value="", type_cast=str
            ),
            ConfigOption(canonical_name="server.tags", default_value="", type_cast=str),
        ]
