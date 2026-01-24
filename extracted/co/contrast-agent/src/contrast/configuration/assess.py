# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from .config_builder import ConfigBuilder
from .config_option import ConfigOption
from contrast.utils.configuration_utils import (
    parse_disabled_rules,
    parse_event_detail_option,
    parse_stacktraces_options,
    str_to_bool,
)


class Assess(ConfigBuilder):
    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(
                canonical_name="assess.enable",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="assess.enable_scan_response",
                default_value=True,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="assess.sampling.enable",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="assess.sampling.baseline",
                default_value=5,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="assess.sampling.request_frequency",
                default_value=10,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="assess.sampling.window_ms",
                default_value=180_000,
                type_cast=int,
            ),
            ConfigOption(canonical_name="assess.tags", default_value="", type_cast=str),
            ConfigOption(
                canonical_name="assess.rules.disabled_rules",
                default_value=[],
                type_cast=parse_disabled_rules,
            ),
            ConfigOption(
                canonical_name="assess.stacktraces",
                default_value="ALL",
                type_cast=parse_stacktraces_options,
            ),
            ConfigOption(
                canonical_name="assess.max_context_source_events",
                default_value=100,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="assess.max_propagation_events",
                default_value=2000,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="assess.time_limit_threshold",
                default_value=300000,  # 5 minutes in ms
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="assess.max_rule_reported",
                default_value=100,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="assess.event_detail",
                default_value="minimal",
                type_cast=parse_event_detail_option,
            ),
        ]
