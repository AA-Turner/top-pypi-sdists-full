# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast_rewriter import str_to_bool

from .config_builder import ConfigBuilder
from .config_option import ConfigOption


class Shield(ConfigBuilder):
    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(
                canonical_name="shield.enable",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="shield.rate_limit_window_ms",
                default_value=3_600_000,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="shield.refresh_interval_ms",
                default_value=300_000,
                type_cast=int,
            ),
        ]
