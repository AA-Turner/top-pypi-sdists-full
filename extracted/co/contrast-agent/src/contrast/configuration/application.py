# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from contrast.utils.configuration_utils import str_to_bool
from .config_builder import ConfigBuilder
from .config_option import ConfigOption
from contrast import AGENT_CURR_WORKING_DIR
import os


class Application(ConfigBuilder):
    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(
                canonical_name="application.code", default_value="", type_cast=str
            ),
            ConfigOption(
                canonical_name="application.group", default_value="", type_cast=str
            ),
            ConfigOption(
                canonical_name="application.sensitive_data_masking_policy.mask_attack_vector",
                default_value=False,
                type_cast=str_to_bool,
                log_effective_config=False,
            ),
            ConfigOption(
                canonical_name="application.sensitive_data_masking_policy.mask_http_body",
                default_value=False,
                type_cast=str_to_bool,
                log_effective_config=False,
            ),
            ConfigOption(
                canonical_name="application.sensitive_data_masking_policy.rules",
                default_value=[],
                type_cast=list,
                log_effective_config=False,
            ),
            ConfigOption(
                canonical_name="application.input_exclusions",
                default_value=[],
                type_cast=list,
                log_effective_config=False,
            ),
            ConfigOption(
                canonical_name="application.metadata", default_value="", type_cast=str
            ),
            ConfigOption(
                # TODO: PYT-2852 Revisit application name detection
                canonical_name="application.name",
                default_value=os.path.basename(AGENT_CURR_WORKING_DIR),
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="application.path", default_value="/", type_cast=str
            ),
            ConfigOption(
                canonical_name="application.tags", default_value="", type_cast=str
            ),
            ConfigOption(
                canonical_name="application.version", default_value="", type_cast=str
            ),
            ConfigOption(
                canonical_name="application.session_id", default_value="", type_cast=str
            ),
            ConfigOption(
                canonical_name="application.session_metadata",
                default_value="",
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="application.url_exclusions",
                default_value=[],
                type_cast=list,
                log_effective_config=False,
            ),
        ]
