# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from contrast.utils.configuration_utils import (
    str_to_bool,
)

from .config_builder import ConfigBuilder
from .config_option import ConfigOption


class Observe(ConfigBuilder):
    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(
                canonical_name="observe.enable",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="observe.ai_usage.enable",
                default_value=False,  # TODO: PYT-4045 flip to True when AI usage is ready for release.
                type_cast=str_to_bool,
            ),
        ]
