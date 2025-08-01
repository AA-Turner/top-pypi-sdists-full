# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
# pylint: disable=too-many-lines
from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timezone
from email.utils import format_datetime
from functools import cached_property
import json
import os
import pathlib
from urllib.parse import urlparse

from contrast import AGENT_CURR_WORKING_DIR

from contrast.agent import scope
from contrast.utils.decorators import fail_quietly
from contrast.agent.framework import _ServerTypeFramework, Server
from contrast.agent.reaction_processor import ReactionProcessor
from contrast.configuration.config_option import (
    CONTRAST_UI_SRC,
    USER_CONFIGURATION_FILE_SRC,
    DEFAULT_VALUE_SRC,
)
from contrast.configuration.agent_config import AgentConfig
from contrast.utils.loggers.logger import (
    STDOUT,
    STDERR,
)
from contrast.utils.singleton import Singleton
from contrast.utils.string_utils import truncate
from contrast.utils.timer import now_ms
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

ASSESS_STACKTRACES = "assess.stacktraces"
ASSESS_DISABLED_RULE_CONFIG_KEY = "assess.rules.disabled_rules"
EXPORTED_CONFIG_FILE_NAME = "contrast_connection.json"

UNIX_EPOCH_HTTP = format_datetime(
    datetime.fromtimestamp(0, tz=timezone.utc), usegmt=True
)
"""
String representation of the unix epoch (1 January 1970) in HTTP-format. Used in the
`If-Modified-Since` header before we have a `Last-Modified` time.
"""


def apply_server_settings(
    config: AgentConfig,
    server_settings_json: dict,
    settings: Settings | None = None,
):
    """
    Applies v1 server settings from the UI to config and settings.

    Eventually, all changes should go through config so that settings
    will be removed.
    """
    from contrast.reporting.teamserver_responses.server_settings import (
        ServerSettings,
    )

    server_features = ServerSettings(server_settings_json)
    ui_config = server_features.common_config()
    logger.debug("Received updated server features", config=ui_config)
    if _changed := config.update_ui_values(ui_config):
        config.log_config()

    if settings:
        settings.set_protect_rules()
        settings.last_server_update_time_ms = now_ms()


def apply_ts_feature_settings(
    config: AgentConfig,
    response_body: dict,
    settings: Settings | None = None,
):
    """
    Applies NG server settings from the UI to config and settings.

    Eventually, all changes should go through config so that settings
    will be removed.
    """
    from contrast.reporting.teamserver_responses.ng_server_settings import (
        NGServerSettings,
    )

    server_features = NGServerSettings(response_body)
    ui_config = server_features.common_config()
    logger.debug("Received updated server features", config=ui_config)
    if _changed := config.update_ui_values(ui_config):
        config.log_config()

    if settings:
        settings.set_protect_rules()
        settings.last_server_update_time_ms = now_ms()


def _apply_application_settings(
    config: AgentConfig,
    application_settings_json: dict,
    settings: Settings | None,
    last_modified: str | None,
):
    """
    Applies v1 app settings from the UI to config and settings.

    Eventually, all changes should go through config so that settings
    will be removed.
    """
    from contrast.reporting.teamserver_responses.application_settings import (
        ApplicationSettings,
    )

    app_settings = ApplicationSettings(application_settings_json)
    ui_config = app_settings.common_config()
    logger.debug("Received updated application settings", config=ui_config)

    if _changed := config.update_ui_values(ui_config):
        config.log_config()

    if settings:
        settings.config.set_ui_value(
            ASSESS_DISABLED_RULE_CONFIG_KEY, app_settings.disabled_assess_rules
        )
        # This is the only place session_id is set by TS.
        # If session id is set in the config, that value will be echoed back by TS
        if app_settings.session_id:
            settings.config.set_ui_value(
                "application.session_id", app_settings.session_id
            )
        settings.set_protect_rules()
        known_rules = set(settings.protect_rules)
        logger.debug("Checking for rules: %s", known_rules)
        if app_settings.protect_rules:
            for definition in app_settings.protect_rules:
                logger.debug("Definition: %s  --- %s", definition.id, definition.mode)
                settings.config.set_ui_value(
                    f"protect.rules.{definition.id}.mode", definition.mode
                )
                if definition.id in known_rules:
                    known_rules.remove(definition.id)
        logger.debug("Remaining rules: %s", known_rules)
        for rule_name in known_rules:
            settings.config.set_ui_value(f"protect.rules.{rule_name}.mode", None)
        settings.last_app_update_time_ms = now_ms()
        if last_modified:
            settings.app_settings_last_modified = last_modified


class Settings(Singleton):
    @scope.contrast_scope()
    def init(self, framework_name: str | None = None):
        """
        Agent settings for the entire lifetime of the agent.

        Singletons should override init, not __init__.
        """
        # We need to initialize config to None because other methods
        # on Settings are called within this init function. It's
        # not obvious because these calls come through import patches.
        self.config = None

        self.config_features = {}
        self.last_server_update_time_ms = 0
        self.last_app_update_time_ms = 0
        # HTTP-style timestamp used in `If-Modified-Since` / `Last-Modified` headers
        # Generally, the AgentStartup response will give us a real value here before we
        # need to send this in a request to teamserver, but we have the unix epoch as a
        # fallback just in case.
        self.app_settings_last_modified: str = UNIX_EPOCH_HTTP
        self.heartbeat = None
        self.server_settings_thread = None
        self.application_settings_thread = None
        self.server = Server()
        self.sys_module_count = 0

        # Server
        self.server_path = None
        self.server_type = None

        # Rules
        self.protect_rules = dict()

        # circular import
        from contrast.agent.assess.rules.response.autocomplete_missing_rule import (
            AutocompleteMissingRule,
        )
        from contrast.agent.assess.rules.response.cache_controls_rule import (
            CacheControlsRule,
        )
        from contrast.agent.assess.rules.response.clickjacking_rule import (
            ClickjackingRule,
        )

        from contrast.agent.assess.rules.response.x_content_type_rule import (
            XContentTypeRule,
        )

        from contrast.agent.assess.rules.response.csp_header_missing_rule import (
            CspHeaderMissingRule,
        )

        from contrast.agent.assess.rules.response.x_xss_protection_disabled_rule import (
            XXssProtectionDisabledRule,
        )

        from contrast.agent.assess.rules.response.hsts_header_rule import HstsHeaderRule

        from contrast.agent.assess.rules.response.csp_header_insecure_rule import (
            CspHeaderInsecureRule,
        )

        from contrast.agent.assess.rules.response.parameter_pollution_rule import (
            ParameterPollutionRule,
        )

        self.assess_response_rules = [
            AutocompleteMissingRule(),
            CacheControlsRule(),
            ClickjackingRule(),
            XContentTypeRule(),
            CspHeaderMissingRule(),
            XXssProtectionDisabledRule(),
            HstsHeaderRule(),
            CspHeaderInsecureRule(),
            ParameterPollutionRule(),
        ]

        # Initialize config
        self.config = AgentConfig()

        self.server_type = (
            self.config["server.type"]
            or _ServerTypeFramework(framework_name).name_lower
        )

        self.agent_runtime_window = now_ms()

        logger.info("Contrast Agent finished loading settings.")

    @cached_property
    def is_proxy_enabled(self):
        return self.config.get("api.proxy.enable")

    @cached_property
    def proxy_url(self):
        return self.config.get("api.proxy.url")

    @cached_property
    def api_url_scheme(self):
        scheme = urlparse(self.api_url).scheme
        return scheme

    @property
    def ignore_cert_errors(self):
        return self.config.get("api.certificate.ignore_cert_errors")

    @property
    def ca_file(self):
        return self.config.get("api.certificate.ca_file")

    @property
    def client_cert_file(self):
        return self.config.get("api.certificate.cert_file")

    @property
    def client_private_key(self):
        return self.config.get("api.certificate.key_file")

    @cached_property
    def api_service_key(self):
        return self.config.get("api.service_key")

    @cached_property
    def api_url(self):
        """Normalizes the URL to remove any whitespace or trailing slash"""
        return self.config.get("api.url").strip().rstrip("/")

    @cached_property
    def api_key(self):
        return self.config.get("api.api_key")

    @cached_property
    def api_user_name(self):
        return self.config.get("api.user_name")

    def is_agent_config_enabled(self):
        if self.config is None:
            return True

        return self.config.get("enable")

    @cached_property
    def max_sources(self):
        return self.config.get("assess.max_context_source_events")

    @cached_property
    def max_propagation(self):
        return self.config.get("assess.max_propagation_events")

    @cached_property
    def max_vulnerability_count(self):
        """Max number of vulnerabilities per rule type to report for one
        agent run `time_limit_threshold` time period"""
        return self.config.get("assess.max_rule_reported")

    @cached_property
    def agent_runtime_threshold(self):
        return self.config.get("assess.time_limit_threshold")

    @cached_property
    def app_path(self):
        return self.config.get("application.path")

    @cached_property
    def app_version(self):
        return self.config.get("application.version")

    @property
    def pid(self):
        """
        pid is used in our CMDi protect rule.

        pid must be unique for each worker process of an app.
        :return: int current process id
        """
        return os.getpid()

    def establish_heartbeat(self, reporting_client):
        """
        Initialize Heartbeat between Agent and TS if it has not been already initialized.
        """
        if self.heartbeat is None:
            # Circular import
            from contrast.agent.heartbeat_thread import HeartbeatThread

            self.heartbeat = HeartbeatThread(reporting_client)
            self.heartbeat.start()

    def establish_server_settings_thread(self, reporting_client):
        """
        Initialize Server Settings poll between Agent and TS if it has not been already
        initialized.
        """
        if self.server_settings_thread is None:
            # Circular import
            from contrast.agent.settings_threads import ServerSettingsThread

            self.server_settings_thread = ServerSettingsThread(reporting_client)
            self.server_settings_thread.start()

    def establish_application_settings_thread(self, reporting_client):
        """
        Initialize Application Settings poll between Agent and TS if it has not been
        already initialized.
        """
        if self.application_settings_thread is None:
            # Circular import
            from contrast.agent.settings_threads import ApplicationSettingsThread

            self.application_settings_thread = ApplicationSettingsThread(
                reporting_client
            )
            self.application_settings_thread.start()

    def apply_ts_feature_settings(self, response_body):
        apply_ts_feature_settings(self.config, response_body, self)

    def process_ts_reactions(self, response_body):
        # App startup/activity wrap reactions in a settings dict whereas
        # Server startup/activity has it at the top level response dict
        reactions = response_body.get("settings", {}).get("reactions", None)

        if not reactions:
            reactions = response_body.get("reactions", None)

        if not reactions:
            return

        ReactionProcessor.process(reactions, self)

    def apply_application_settings(
        self, application_settings_json: dict, last_modified: str | None = None
    ):
        """
        Update stored application settings using the provided dict. This corresponds to
        the teamserver v1 API ApplicationSettings1.0 object.

        `last_modified` is an HTTP-style timestamp from the `Last-Modified` header. If
        set to None, the previous known last update time will be maintained; note that
        the last update time is initially set to the unix epoch.
        """
        _apply_application_settings(
            self.config, application_settings_json, self, last_modified
        )

    def apply_identification(self, identification_json: dict | None):
        if not identification_json:
            return
        self.application_uuid = identification_json.get("application_uuid", None)
        self.organization_uuid = identification_json.get("organization_uuid", None)
        self.server_uuid = identification_json.get("server_uuid", None)
        self.session_id = identification_json.get("session_id", None)

    def apply_server_settings(self, server_settings_json: dict):
        apply_server_settings(self.config, server_settings_json, self)

    def is_inventory_enabled(self):
        """
        inventory.enable = false: Disables both route coverage and library analysis and reporting
        """
        return self.config.get("inventory.enable")

    def is_analyze_libs_enabled(self):
        """
        inventory.analyze_libraries = false: Disables only library analysis/reporting
        """
        return (
            self.config is not None
            and self.config.get("inventory.analyze_libraries")
            and self.is_inventory_enabled()
        )

    def set_protect_rules(self):
        from contrast.agent.protect.rule.rules_builder import build_protect_rules

        self.protect_rules = build_protect_rules()

    def get_server_path(self):
        """
        Working Directory of the server

        Default is root
        """
        if self.server_path is None:
            self.server_path = self.config.get("server.path") or truncate(
                AGENT_CURR_WORKING_DIR
            )

        return self.server_path

    def is_assess_rule_disabled(self, rule_id):
        """
        Rules disabled in config override all disabled rules from TS per common config
        """
        disabled_rules = self.config.get(ASSESS_DISABLED_RULE_CONFIG_KEY)
        return disabled_rules is not None and rule_id in disabled_rules

    def enabled_response_rules(self):
        return (
            [
                rule
                for rule in self.assess_response_rules
                if not self.is_assess_rule_disabled(rule.name)
            ]
            if self.config.get("assess.enable_scan_response")
            else []
        )

    def is_collect_stacktraces_all(self):
        return self.config is not None and self.config.get(ASSESS_STACKTRACES) == "ALL"

    def is_collect_stacktraces_some(self):
        return self.config is not None and self.config.get(ASSESS_STACKTRACES) == "SOME"

    def is_collect_stacktraces_none(self):
        return self.config is not None and self.config.get(ASSESS_STACKTRACES) == "NONE"

    def build_proxy_url(self):
        if self.proxy_url:
            # self.api_url_scheme is the key of the scheme we are proxying
            # self.proxy_url is the actual proxy url and port
            # https://requests.readthedocs.io/en/latest/user/advanced/#proxies
            return {self.api_url_scheme: self.proxy_url}

        return {}

    @cached_property
    def contrast_ui_status(self):
        config_name = "enable"
        error_msg = "Unable to connect to Contrast; configuration details from the Contrast UI will not be included."

        enable_option = self.config.get_option(config_name)
        if enable_option is None or enable_option.ui_value is False:
            # This indicates we were told to shut down by Contrast UI
            return error_msg

        return None

    def generate_effective_config(self):
        """
        The purpose of this function is to export as many of the configuration values found in AgentConfig
        to the effective_config list. This list will be logged to disk. Some values that where set using
        the Contrast UI where saved to AgentConfig in attempt to have a single place storing all settings.

        In some cases this wasn't immediately feasible due to when and how we reload those settings
        """
        status = self.contrast_ui_status or self.config.config_status or "Success"
        report_creation_time = datetime.now(timezone.utc).strftime(RFC3339_FORMAT)
        config = {
            "report_create": report_creation_time,
            "config": {
                "status": status,
                "effective_config": [],
                "user_configuration_file": [],
                "environment_variable": [],
                "contrast_ui": [],
            },
        }

        effective_config = config["config"]["effective_config"]
        env_config = config["config"]["environment_variable"]
        ui_config = config["config"]["contrast_ui"]

        user_config = defaultdict(list)

        for key in self.config:
            option = self.config.get_option(key)
            if option is None or not option.log_effective_config:
                continue

            # The spec states this value is not included if we can't communicate with Contrast UI
            if (
                option.source() == CONTRAST_UI_SRC
                and self.contrast_ui_status is not None
            ):
                continue

            value = option.loggable_value()

            # If the value is unset and has no default value, we should skip it.
            # For instance, if a proxy isn't set, there's no reason to report those configuration values.
            if option.source() == DEFAULT_VALUE_SRC and value in ("", "[]"):
                continue

            config_entry = {
                "canonical_name": option.canonical_name,
                "name": option.provided_name(),
                "source": option.source(),
                "value": value,
            }
            if option.source() == USER_CONFIGURATION_FILE_SRC:
                config_entry["filename"] = option.file_name()

            effective_config.append(config_entry)

            if option.env_value is not None:
                config_entry = {
                    "canonical_name": option.canonical_name,
                    "name": option.provided_name(),
                    "value": option.to_string(option.env_value),
                }
                env_config.append(config_entry)
            if option.ui_value is not None:
                config_entry = {
                    "canonical_name": option.canonical_name,
                    # provided name is only for env vars
                    "name": option.canonical_name,
                    "value": option.to_string(option.ui_value),
                }
                ui_config.append(config_entry)
            if option.file_values:
                for val, filename in zip(option.file_values, option.file_sources):
                    config_entry = {
                        "canonical_name": option.canonical_name,
                        # provided name is only for env vars
                        "name": option.canonical_name,
                        "value": option.to_string(val),
                    }
                    user_config[filename].append(config_entry)

        config["config"]["user_configuration_file"] = [
            {"path": filename, "values": values}
            for filename, values in user_config.items()
        ]

        # PYT-3808: Don't send properties that are null or empty lists
        config["config"] = {
            k: v for k, v in config["config"].items() if v not in ([], None)
        }

        return config

    @fail_quietly("Failed to export effective config")
    def log_effective_config(self):
        """
        If we have a directory to which to log safely, we are to add the effective configuration json file to that
        location. For other instances, such as STDOUT or un-writable directories, there is no need to write the file as
        the configuration is contained in our standard logs.
        """
        if (
            self.config.get("agent.logger.stdout")
            or self.config.get("agent.logger.stderr")
            or self.config.get("agent.logger.path") in (STDOUT, STDERR)
        ):
            return
        path = pathlib.Path(self.config.get("agent.logger.path")).parent.resolve()
        filename = f"{path}/{EXPORTED_CONFIG_FILE_NAME}"

        try:
            with open(filename, "w") as f:
                json.dump(self.generate_effective_config(), f, indent=4)
        except PermissionError as perm_error:
            logger.warning(
                "Failed to export effective config",
                filename=filename,
                error=str(perm_error),
            )
            return


RFC3339_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
