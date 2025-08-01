# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from collections import defaultdict
from collections.abc import Mapping
from functools import cached_property
import re
from threading import RLock
from typing import Any, Callable

from contrast.agent.inventory.fingerprint import artifact_fingerprint
from contrast.utils.configuration_utils import (
    DEFAULT_PATHS,
    load_yaml_config,
)
from contrast_vendor import structlog as logging
from . import ConfigOption

from .agent import Agent
from .api import Api
from .application import Application
from .assess import Assess
from .inventory import Inventory
from .observe import Observe
from .protect import Protect
from .reporting import Reporting
from .root import Root
from .server import Server

logger = logging.getLogger("contrast")

DEFAULT_TEAMSERVER_TYPE = "EOP"
PUBLIC_SASS_TEAMSERVER_TYPES = {
    "app.contrastsecurity.com": "SAAS_DEFAULT",
    "app-agents.contrastsecurity.com": "SAAS_DEFAULT",
    "eval.contrastsecurity.com": "SAAS_POV",
    "eval-agents.contrastsecurity.com": "SAAS_POV",
    "ce.contrastsecurity.com": "SAAS_CE",
    "ce-agents.contrastsecurity.com": "SAAS_CE",
    "app.contrastsecurity.jp": "SAAS_TOKYO",
    "app-agents.contrastsecurity.jp": "SAAS_TOKYO",
    "cs": "SAAS_",
}

PRIVATE_SASS_TEAMSERVER_TYPE = "SAAS_CUSTOM"
PRIVATE_SASS_DOMAIN = ["contrastsecurity.com", "contrastsecurity.jp"]

TESTING_TEAMSERVER_TYPE = "TESTING"
TESTING_TEAMSERVER_NAMES = [
    "teamserver-darpa",
    "teamserver-darpa-agents",
    "alpha.contrastsecurity.com",
    "alpha-agents.contrastsecurity.com",
    "apptwo.contrastsecurity.com",
    "apptwo-agents.contrastsecurity.com",
    "teamserver-staging.contsec.jp",  # agents host name not defined yet.
    "teamserver-staging.contsec.com",
    "teamserver-staging-agents.contsec.com",
    "security-research.contrastsecurity.com",
    "security-research-agents.contrastsecurity.com",
    "teamserver-ops.contsec.com",  # agents host name not defined yet.
]

ConfigWatcher = Callable[["Mapping"], Any]


class AgentConfig(Mapping):
    def __init__(self):
        self.config_status = None
        self._config = {}
        self.watch_map: defaultdict[str, set[Watcher]] = defaultdict(set)
        self.updates_lock = RLock()
        self.build_configs()
        self.check_for_api_config()

    # Methods like `get`, `keys`, etc are automatically implemented by the Mapping abc.
    # They are derived from the concrete implementations below. See:
    # https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes
    # --- Required Mapping methods ---

    def __getitem__(self, key):
        return self._config[key].value()

    def __iter__(self):
        return iter(self._config)

    def __len__(self):
        return len(self._config)

    # --- End Required Mapping methods ---

    def get_option(self, key: str) -> ConfigOption | None:
        return self._config.get(key, None)

    def get_loggable_value(self, key: str) -> str | None:
        option = self.get_option(key)
        return option.loggable_value() if option else None

    def add_watcher(self, f: ConfigWatcher):
        """
        Calls f with the current config, and again whenever the config changes.
        As an optimization, f is only called again when the config value it uses changes.
        For example, if the config value of "agent.logger.level" changes, but f only uses
        "protect.enable", f will not be called again.
        """
        with self.updates_lock:
            Watcher(f)(self)

    def notify_watchers(self, keys: set[str]):
        """
        Notifies watchers registered for the given keys by reloading them.
        """
        with self.updates_lock:
            key_watchers = {f for key in keys for f in self.watch_map[key]}
            for f in key_watchers:
                f(self)

    def get_loggable_config(self):
        """
        The purpose of this function is to return a copy of the effective config with their resolved values rather than
        the ConfigOption object.
        """

        loggable_config = {}
        for key in self._config:
            loggable_config[key] = self.get_loggable_value(key)

        return loggable_config

    def log_config(self):
        loggable_config = self.get_loggable_config()

        logger.info("Current Configuration", **loggable_config)

    def build_configs(self):
        """
        For each class representing different parts of the config (Agent, etc),
        take the current config and apply any overriding logic such as overriding with
        environment keys/values.

        At this time the order of precedence is:
            os.env > Config yaml

        Meaning that a config value defined in os.environ must be used instead of
        the same config defined in contrast_security.yaml

        Note that CLI args (sys.argv) are not supported. This may change if the
        agent becomes a runner.
        """
        yaml_config = load_yaml_config(DEFAULT_PATHS)
        if not yaml_config:
            logger.info("No YAML config found; using default settings")

        builders = [
            Api,
            Agent,
            Application,
            Assess,
            Inventory,
            Observe,
            Protect,
            Reporting,
            Root,
            Server,
        ]
        for builder in builders:
            status = builder().build(self._config, yaml_config)
            if status:
                # An error here indicates a failure with either the type cast of the value
                # or an error on converting api.token to the 4 API config values
                self.config_status = status

    def check_for_api_config(self):
        """
        Validate api configurations were set.

        If any api configs are missing, log at ERROR and disable the agent.

        Returns the missing values or an empty list if none were missing.
        """

        api_keys = [
            "api.url",
            "api.service_key",
            "api.api_key",
            "api.user_name",
        ]

        missing_values = []
        for key in api_keys:
            option = self.get_option(key)
            if not option or option.value() in (None, ""):
                missing_values.append(key)

        if missing_values:
            msg = (
                f"Missing a required connection value for: {', '.join(missing_values)}"
            )
            logger.error(msg)
            self.config_status = "Unable to connect to Contrast, insufficient connection properties provided."
            enable_option = self.get_option("enable")
            enable_option.override_value = False

        return missing_values

    @property
    def session_id(self):
        return self.get("application.session_id")

    @session_id.setter
    def session_id(self, session_id):
        session_id_option = self.get_option("application.session_id")
        session_id_option.ui_value = session_id

        logger.debug(
            "Set session_id",
            session_id=session_id_option.value(),
            direct_to_teamserver=1,
        )

    def get_session_metadata(self):
        user_metadata = self.get("application.session_metadata", "")
        fingerprint = artifact_fingerprint()
        if not fingerprint:
            return user_metadata
        artifact_metadata = f"artifactHash={fingerprint}"
        return (
            artifact_metadata + "," + user_metadata
            if user_metadata
            else artifact_metadata
        )

    @property
    def app_code(self):
        return self.get("application.code")

    @property
    def app_metadata(self):
        return self.get("application.metadata")

    @property
    def app_group(self):
        return self.get("application.group")

    @property
    def app_tags(self):
        return self.get("application.tags")

    @property
    def assess_tags(self):
        return self.get("assess.tags")

    @cached_property
    def is_request_audit_enabled(self):
        return self.get("api.request_audit.enable")

    @cached_property
    def assess_enabled(self):
        return self.get("assess.enable")

    @cached_property
    def should_pytest_rewrite(self):
        return self.assess_enabled and self.get("agent.python.pytest_rewrite")

    @cached_property
    def enable_automatic_middleware(self) -> bool:
        return self.get("agent.python.enable_automatic_middleware")

    @cached_property
    def application_settings_poll_interval(self):
        return self.get("agent.polling.app_settings_ms")

    @cached_property
    def server_settings_poll_interval(self):
        return self.get("agent.polling.server_settings_ms")

    @cached_property
    def heartbeat_poll_interval(self):
        return self.get("agent.polling.heartbeat_ms")

    @cached_property
    def teamserver_type(self):
        url = self.get("api.url")

        if not url:
            return ""

        for name, ts_type in PUBLIC_SASS_TEAMSERVER_TYPES.items():
            if name in url:
                # This regex matches https://cs001.contrastsecurity.com
                r_url = re.match(r".*(cs\d{3})\..*", url)
                if r_url:
                    # and gets the second group which is the matched in brackets cs001
                    # adds it to the SAAS_ type and becomes SAAS_CS001
                    numbers = r_url.group(1).upper()

                    return ts_type + numbers

                return ts_type

        for name in TESTING_TEAMSERVER_NAMES:
            if name in url:
                return TESTING_TEAMSERVER_TYPE

        for name in PRIVATE_SASS_DOMAIN:
            if name in url:
                return PRIVATE_SASS_TEAMSERVER_TYPE

        return DEFAULT_TEAMSERVER_TYPE

    def set_ui_value(self, key: str, value: object):
        """
        We have to be safe here with unknown configuration options as TeamServer can send us settings for which we do
        not have configurations. This most often happens when we're given configurations for rules that do not pertain
        to this agent.
        """
        if config_option := self.get_option(key):
            config_option.ui_value = value

    def update_ui_values(self, new_config: dict[str, object]) -> set[str]:
        """
        Update the UI values of the configuration options with the values from the new configuration.
        Watchers of the configuration options will be notified if the value of the configuration option changes.

        Returns the set of option names that changed.
        """
        with self.updates_lock:
            changed_keys = set()
            for key, value in new_config.items():
                # We have to be safe here with unknown configuration options as TeamServer can send us settings for which we do
                # not have configurations. This most often happens when we're given configurations for rules that do not pertain
                # to this agent.
                if config_option := self.get_option(key):
                    before = config_option.value()
                    config_option.ui_value = value
                    if before != config_option.value():
                        changed_keys.add(key)
            self.notify_watchers(changed_keys)
            return changed_keys


class Watcher:
    """
    A watcher is a function that is called when the configuration changes.

    The watcher wraps a function and spies on the configuration options that the function uses.
    It then registers itself in the configuration watch_map to be called when any of the
    configuration options change.
    """

    def __init__(self, f: ConfigWatcher):
        self.f = f

    def __call__(self, config: AgentConfig):
        config_spy = ConfigSpy(config)
        self.f(config_spy)
        if not config_spy._used_keys:
            logger.debug(
                "WARNING: Watcher does not use any config values. It will not be called when the config changes.",
                f=self.f,
            )

        for key in config_spy._used_keys:
            config.watch_map[key].add(self)


class ConfigSpy(Mapping):
    def __init__(self, wrapped: Mapping):
        self._wrapped = wrapped
        self._used_keys = set()

    def __getitem__(self, key):
        self._used_keys.add(key)
        return self._wrapped[key]

    def __iter__(self):
        return iter(self._wrapped)

    def __len__(self):
        return len(self._wrapped)

    def get_option(self, key: str) -> ConfigOption | None:
        if get_option := getattr(self._wrapped, "get_option", None):
            return get_option(key)
        return None
