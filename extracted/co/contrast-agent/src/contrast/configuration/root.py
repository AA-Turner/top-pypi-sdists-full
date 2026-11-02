# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from contrast_rewriter import str_to_bool

from .config_builder import ConfigBuilder
from .config_option import ConfigOption


class Root(ConfigBuilder):
    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(
                canonical_name="enable", default_value=True, type_cast=str_to_bool
            )
        ]
