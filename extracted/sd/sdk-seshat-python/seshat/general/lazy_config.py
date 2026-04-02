import importlib
import os

from seshat.general import config as default_config

CONFIG_MODULE_DIR = "SESHAT_CONFIG_MODULE"


class LazyConfig:
    def setup(self):
        pass


class Config:
    _explicit_configs = set()

    def __init__(self, config_module=None):
        if not config_module:
            config_module = os.environ.get(CONFIG_MODULE_DIR)
            if not config_module:
                config_module = "seshat.general.config"

        self.setup(config_module)

    def setup(self, config_module):
        for config_key in dir(default_config):
            if config_key.isupper():
                setattr(self, config_key, getattr(default_config, config_key))

        custom_module = importlib.import_module(config_module)

        for config_key in dir(custom_module):
            if config_key.isupper():
                setattr(self, config_key, getattr(custom_module, config_key))
                self._explicit_configs.add(config_key)

    def is_overridden(self, config_key):
        return config_key in self._explicit_configs


configs = Config()
