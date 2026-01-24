# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

import base64
import json

from contrast.utils.configuration_utils import str_to_bool
from .config_builder import ConfigBuilder
from .config_option import ConfigOption
from contrast import AGENT_CURR_WORKING_DIR


from contrast_vendor import structlog as logging


logger = logging.getLogger("contrast")


class Api(ConfigBuilder):
    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(canonical_name="api.url", default_value="", type_cast=str),
            ConfigOption(
                canonical_name="api.service_key",
                default_value="",
                type_cast=str,
                redacted=True,
            ),
            ConfigOption(
                canonical_name="api.api_key",
                default_value="",
                type_cast=str,
                redacted=True,
            ),
            ConfigOption(
                canonical_name="api.user_name",
                default_value="",
                type_cast=str,
                redacted=True,
            ),
            ConfigOption(
                canonical_name="api.token",
                default_value="",
                type_cast=str,
                redacted=True,
            ),
            ConfigOption(
                canonical_name="api.reporting_client",
                default_value="fireball",
                type_cast=str,
                log_effective_config=False,
            ),
            ConfigOption(
                canonical_name="api.request_audit.enable",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="api.request_audit.path",
                default_value=AGENT_CURR_WORKING_DIR,
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="api.request_audit.requests",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="api.request_audit.responses",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="api.certificate.enable",
                default_value=True,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="api.certificate.ignore_cert_errors",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="api.certificate.ca_file",
                default_value="",
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="api.certificate.cert_file",
                default_value="",
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="api.certificate.key_file",
                default_value="",
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="api.proxy.enable",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="api.proxy.url",
                default_value="",
                type_cast=str,
                redacted=True,
            ),
        ]

    def build(self, config: dict, yaml_config: list[tuple[dict, str]]):
        api_keys = {
            "api.url": "url",
            "api.service_key": "service_key",  # pragma: allowlist secret
            "api.api_key": "api_key",  # pragma: allowlist secret
            "api.user_name": "user_name",
        }

        error = super().build(config, yaml_config)

        if error:
            return error

        api_token = config.get("api.token")

        if not (token_value := api_token.value()):
            api_token.log_effective_config = False
            return None

        try:
            api_values = json.loads(base64.b64decode(token_value, validate=True))
        except Exception as e:
            error = f"Invalid value on {api_token.canonical_name} - {e}"
            return error

        for api_config_key, api_config_key_teamserver in api_keys.items():
            option = config.get(api_config_key)
            if not option.is_definitely_static():
                if (
                    new_value := api_values.get(api_config_key_teamserver, None)
                ) is None:
                    error = f"Invalid value on {api_token.canonical_name}"
                    logger.error(
                        "Unable to set %s based on %s",
                        option.canonical_name,
                        api_token.canonical_name,
                    )
                    break

                option.override_value = new_value
                option.log_effective_config = False
            else:
                logger.info(
                    f"Using configured value for {option.canonical_name} set using {option.source()} instead of api.token"
                )

        return error
