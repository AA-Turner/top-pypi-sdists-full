# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

import os
from contrast_vendor import structlog as logging


logger = logging.getLogger("contrast")

ENV_PREFIX = "CONTRAST"


def env_name(name):
    return "__".join([x for x in [ENV_PREFIX, name.replace(".", "__")] if x]).upper()


class ConfigBuilder:
    def __init__(self):
        self.default_options = []

    def build(self, config: dict, yaml_config: list[tuple[dict, str]]):
        """
        Given a dict config, iterate over the default_options and check if
        the corresponding config key/value should be either :
        1. replaced by an existing env var
        2. keep existing config key/val but type-cast the value
        3. add a new key/default_value to the config

        :param config: dict config
        :return: str if error was set, config dict is updated pass by reference
        """
        error = None
        for option in self.default_options:
            option_name = option.canonical_name
            type_cast = option.type_cast
            env_key = env_name(option_name)
            env_override = os.environ.get(env_key)
            if env_override is not None:
                try:
                    option.env_value = type_cast(env_override)
                    option.name = env_key
                except Exception as e:
                    logger.exception("Failed to initialize config")
                    if error is None:
                        error = f"Invalid value on {option.canonical_name} - {e}"
            for cfg, filename in yaml_config:
                file_override = cfg.get(option_name, None)
                if file_override is not None:
                    if not option.file_values and not option.file_sources:
                        option.file_values = []
                        option.file_sources = []
                    try:
                        option.file_values.append(type_cast(file_override))
                        option.file_sources.append(filename)
                    except Exception as e:
                        logger.exception("Failed to initialize config")
                        if error is None:
                            error = f"Invalid value on {option_name} - {e}"
            config[option_name] = option
        return error
