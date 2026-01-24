# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from contrast.agent.protect.rule.mode import Mode
from contrast.utils.configuration_utils import (
    parse_disabled_rules,
    str_to_bool,
    str_to_protect_mode_enum,
)

from .config_builder import ConfigBuilder
from .config_option import ConfigOption


class Protect(ConfigBuilder):
    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(
                canonical_name="protect.enable",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="protect.probe_analysis.enable",
                default_value=True,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="protect.samples.probed", default_value=50, type_cast=int
            ),
            ConfigOption(
                canonical_name="protect.samples.blocked",
                default_value=25,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="protect.samples.exploited",
                default_value=100,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="protect.samples.blocked_at_perimeter",
                default_value=25,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="protect.rules.bot-blocker.enable",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="protect.rules.cmd-injection.mode",
                default_value=Mode.OFF,
                type_cast=str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="protect.rules.disabled_rules",
                default_value=[],
                type_cast=parse_disabled_rules,
            ),
            ConfigOption(
                canonical_name="protect.rules.method-tampering.mode",
                default_value=Mode.OFF,
                type_cast=str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="protect.rules.nosql-injection.mode",
                default_value=Mode.OFF,
                type_cast=str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="protect.rules.path-traversal.mode",
                default_value=Mode.OFF,
                type_cast=str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="protect.rules.reflected-xss.mode",
                default_value=Mode.OFF,
                type_cast=str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="protect.rules.sql-injection.mode",
                default_value=Mode.OFF,
                type_cast=str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="protect.rules.unsafe-file-upload.mode",
                default_value=Mode.OFF,
                type_cast=str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="protect.rules.untrusted-deserialization.mode",
                default_value=Mode.OFF,
                type_cast=str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="protect.rules.xxe.mode",
                default_value=Mode.OFF,
                type_cast=str_to_protect_mode_enum,
            ),
        ]
