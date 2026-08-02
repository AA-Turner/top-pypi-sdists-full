import datetime
import json
import logging
import os

from python_agent.build_scanner.executors.config import Config
from python_agent.common.autoupgrade.autoupgrade_manager import AutoUpgrade
from python_agent.common.config_data import ConfigData
from python_agent.common.constants import (
    BUILD_SESSION_ID_FILE,
    TOKEN_FILE,
    CONFIG_ENV_VARIABLE,
)
from python_agent.common.environment_variables_resolver import (
    EnvironmentVariablesResolver,
)
from python_agent.common.http.backend_proxy import BackendProxy
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.common.log.sealights_logging import SealightsHTTPHandler
from python_agent.common.token.token_parser import TokenParser
from python_agent.test_listener.integrations.multiprocessing_patcher import (
    patch_multiprocessing,
)
from python_agent.utils import CommandType

log = logging.getLogger(__name__)

# A list off properties, which should be converted to integer
INT_PROPERTIES = [
    "commitHistoryLength",
    # v3 footprints tunables (env-var coercion; remote-config uses its own
    # typed merge in python_agent.common.http.remote_config_merge).
    "footprintsBufferThresholdMB",
    "_add_coverage_interval_seconds",
    # intervalSeconds is also int-valued but writes to this attribute via the
    # env alias `FOOTPRINTSSENDINTERVALSECS`. Keep explicit for clarity.
    "intervalSeconds",
]


class ConfigurationManager(object):
    def __init__(self):
        self.config_data = ConfigData()
        self.env_resolver = EnvironmentVariablesResolver(
            INT_PROPERTIES, self.config_data
        )

    def init_configuration(
        self,
        command_type,
        token,
        buildsessionid,
        labid,
        tokenfile=TOKEN_FILE,
        buildsessionidfile=BUILD_SESSION_ID_FILE,
        proxy=None,
        testprojectid=None,
        prid=None,
        scm_args=None,
        test_selection_enable=True,
        # --- New CLI kwargs (SLDEV-26009) -----------------------------------
        # These are applied FIRST in try_load_configuration so that env vars
        # and then remote config can still override them. This reverses the
        # pre-SLDEV-26009 behavior where AgentExecution wrote CLI values
        # AFTER remote config and CLI effectively always won. Remote config
        # is now the authoritative source for tunables.
        #
        # All of them default to None = "caller did not pass a CLI value".
        interval=None,
        per_test=None,
        footprints_send_interval_secs=None,
        footprints_collect_interval_secs=None,
        footprints_buffer_threshold_mb=None,
    ):
        try:
            self.config_data.set_command_type(command_type)
            self.try_load_configuration(
                scm_args,
                token,
                buildsessionid,
                tokenfile,
                buildsessionidfile,
                proxy,
                command_type,
                test_selection_enable,
                labid,
                testprojectid,
                prid,
                interval=interval,
                per_test=per_test,
                footprints_send_interval_secs=footprints_send_interval_secs,
                footprints_collect_interval_secs=footprints_collect_interval_secs,
                footprints_buffer_threshold_mb=footprints_buffer_threshold_mb,
            )
            self.init_features()
            return self.config_data
        except Exception as e:
            ConsoleMessageTemplates.render_and_print(
                "common.general.agent-ended-error",
                command=self.config_data.get_command_type(),
                error=str(e),
                dateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            raise e

    def try_load_configuration_from_config_environment_variable(self):
        config_data = os.environ.get(CONFIG_ENV_VARIABLE)
        if config_data:
            config_data = json.loads(config_data)
            self.config_data.__dict__.update(config_data)

    def _try_load_configuration_from_environment_variables(self):
        self.config_data.__dict__.update(self.env_resolver.resolve())

    def _try_load_configuration_from_server(self, backend_proxy):
        result = backend_proxy.get_remote_configuration(self.config_data)
        self.config_data.__dict__.update(result)

    def init_features(self):
        self.init_logging()
        patch_multiprocessing()

    def _apply_cli_values(
        self,
        interval=None,
        per_test=None,
        footprints_send_interval_secs=None,
        footprints_collect_interval_secs=None,
        footprints_buffer_threshold_mb=None,
    ):
        """
        Apply values passed directly on the command line to config_data.

        Runs BEFORE env vars and remote config, so both can override any CLI
        value. This is the intentional precedence after SLDEV-26009:

            defaults -> CLI -> env -> remote (remote wins)

        Only mutates attributes when the caller actually passed a non-None
        value so that unspecified CLI flags keep the defaults in place.
        """
        if interval is not None:
            self.config_data.interval = interval
            self.config_data.intervalSeconds = interval / 1000
        if per_test is not None:
            self.config_data.perTest = per_test
        if footprints_send_interval_secs is not None:
            self.config_data.intervalSeconds = footprints_send_interval_secs
            self.config_data.interval = footprints_send_interval_secs * 1000
        if footprints_collect_interval_secs is not None:
            self.config_data._add_coverage_interval_seconds = (
                footprints_collect_interval_secs
            )
        if footprints_buffer_threshold_mb is not None:
            self.config_data.footprintsBufferThresholdMB = (
                footprints_buffer_threshold_mb
            )

    def try_load_configuration(
        self,
        scm_args,
        token,
        buildsessionid,
        tokenfile,
        buildsessionidfile,
        proxy,
        command_type,
        test_selection_enable,
        labid,
        testprojectid,
        prid,
        # New CLI kwargs (optional) - see _apply_cli_values for semantics.
        interval=None,
        per_test=None,
        footprints_send_interval_secs=None,
        footprints_collect_interval_secs=None,
        footprints_buffer_threshold_mb=None,
    ):
        self.config_data.proxy = proxy
        self.config_data.test_selection_enable = test_selection_enable
        if testprojectid:
            self.config_data.testProjectId = testprojectid
        if prid:
            self.config_data.prID = prid
        self.config_data.apply_scm_args(scm_args)
        # Precedence order: CLI -> env -> remote. Apply CLI first so env and
        # remote can still override.
        self._apply_cli_values(
            interval=interval,
            per_test=per_test,
            footprints_send_interval_secs=footprints_send_interval_secs,
            footprints_collect_interval_secs=footprints_collect_interval_secs,
            footprints_buffer_threshold_mb=footprints_buffer_threshold_mb,
        )
        self._try_load_configuration_from_environment_variables()
        is_resolved_token = self.resolve_token_data(
            token, tokenfile, self.config_data.tokenFile
        )
        if not is_resolved_token:
            return self.disable_sealights("Missing or invalid token")

        backend_proxy = BackendProxy(self.config_data)
        if command_type != CommandType.CONFIG:
            resolved_lab_id = self.resolve_lab_id(labid)
            is_resolved_build_session_id = self.resolve_build_session_id(
                buildsessionid,
                buildsessionidfile,
                resolved_lab_id,
                backend_proxy,
                command_type,
            )
            if not is_resolved_build_session_id:
                ConsoleMessageTemplates.render_and_print(
                    "common.test-listener.missing-build-session-or-lab-id",
                )
                if command_type in [CommandType.SCAN, CommandType.TEST]:
                    raise Exception("Missing build session or lab id")
                return self.disable_sealights("Missing build session or lab id")
            self._try_load_configuration_from_server(backend_proxy)

    def update_build_session_data(self, build_session_data):
        self.config_data.__dict__.update(build_session_data.__dict__)
        if not build_session_data.additionalParams:
            return
        for config, value in list(build_session_data.additionalParams.items()):
            setattr(self.config_data, config, value)

    def update_token_data(self, token, token_data):
        self.config_data.token = token
        self.config_data.customerId = token_data.customerId
        self.config_data.server = token_data.server

    def resolve_token_data(self, token, tokenfile, env_tokenfile):
        token = (
            token
            or self.config_data.token
            or self.read_from_file(tokenfile)
            or self.read_from_file(env_tokenfile)
        )
        if not token:
            log.error(
                "--token, --tokenfile options or sl.token or sl.tokenFile environment variables must be provided"
            )
            return False
        token_data, token = TokenParser.parse_and_validate(token)
        self.update_token_data(token, token_data)
        return True

    def _upgrade_agent(self):
        auto_upgrade = AutoUpgrade(self.config_data)
        auto_upgrade.upgrade()

    def resolve_lab_id(self, labid) -> str:
        return labid or self.config_data.labId

    def resolve_build_session_id(
        self,
        buildsessionid,
        buildsessionidfile,
        resolved_lab_id,
        backend_proxy,
        command_type,
    ):
        should_resolve_from_lab_id = False
        explicit_bsid = buildsessionid or self.config_data.buildSessionId
        if command_type == CommandType.START and resolved_lab_id and not explicit_bsid:
            should_resolve_from_lab_id = True
        build_session_id = (
            buildsessionid
            or self.config_data.buildSessionId
            or self.read_from_file(buildsessionidfile)
            or self.read_from_file(self.config_data.buildSessionIdFile)
        )
        build_session = None

        if build_session_id:
            build_session = self.resolve_build_session_from_id(
                build_session_id, backend_proxy
            )
        if not build_session_id and resolved_lab_id:
            should_resolve_from_lab_id = True
        if should_resolve_from_lab_id:
            log.debug("Resolving from Lab ID %s", resolved_lab_id)
            build_session = self.resolve_build_session_from_labid(
                resolved_lab_id, backend_proxy, command_type
            )
            if build_session:
                self.config_data.apply_build_session(build_session)
        self.config_data.labId = resolved_lab_id
        if not build_session:
            return False
        self.update_build_session_data(build_session)
        return True

    def resolve_build_session_from_labid(self, labid, backend_proxy, command_type):
        build_session = backend_proxy.get_build_session_from_labid(
            labid, self.config_data
        )
        if build_session:
            msg_cont = ""
            if command_type == CommandType.START:
                Config.write_build_session_to_file(build_session.buildSessionId)
                msg_cont = " and saved to file"
            log.info(
                f"build session id was resolved using lab id{msg_cont}. build session id: %s. labid: %s"
                % (build_session.buildSessionId, labid)
            )

        else:
            log.error(
                "build session id was not resolved using lab id: %s. Supply buildsessionid or make sure you have a running app configured with this labid"
                % labid
            )
        return build_session

    def resolve_build_session_from_id(self, build_session_id, backend_proxy):
        try:
            build_session = backend_proxy.get_build_session(
                self.config_data, build_session_id
            )
            return build_session
        except Exception as e:
            log.error(
                "Failed to resolve build session id: %s. Error: %s"
                % (build_session_id, str(e))
            )
            return None

    def read_from_file(self, file_path):
        if file_path and os.path.isfile(file_path):
            with open(os.path.abspath(file_path), "r") as f:
                value = f.read()
                return value.rstrip()
        return None

    def init_logging(self):
        if self.config_data.isSendLogs:
            sl_handler = SealightsHTTPHandler(self.config_data, capacity=50)
            sl_formatter = logging.Formatter(
                "%(asctime)s %(levelname)s [%(process)d|%(thread)d] %(name)s: %(message)s"
            )
            sl_handler.setFormatter(sl_formatter)
            agent_logger = logging.getLogger("python_agent")
            agent_logger.addHandler(sl_handler)

    def init_coloring(self):
        self.init_coloring_incoming()
        self.init_coloring_outgoing()

    def init_coloring_outgoing(self):
        pass

    def init_coloring_incoming(self):
        from python_agent.test_listener.web_frameworks import __all__

        for web_framework_name in __all__:
            web_framework = __import__(
                "%s.%s.%s.%s"
                % (
                    "python_agent",
                    "test_listener",
                    "web_frameworks",
                    web_framework_name,
                ),
                fromlist=[web_framework_name],
            )
            bootstrap_method = getattr(web_framework, "bootstrap", None)
            if bootstrap_method:
                bootstrap_method()
                log.debug("Bootstrapped Framework: %s" % web_framework_name)
        log.info("Bootstrapped Frameworks: %s" % __all__)

    def disable_sealights(self, reason=None):
        self.config_data.isDisabled = True
        log.warning("Sealights is disabled")
        if self.config_data.command_type in [CommandType.CONFIG, CommandType.SCAN]:
            ConsoleMessageTemplates.render_and_print(
                "common.general.agent-ended-error",
                command="config",
                error=reason,
                dateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
        else:
            ConsoleMessageTemplates.render_and_print(
                "common.general.agent-ended-warnings",
                command=self.config_data.command_type,
                error=reason,
                dateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
