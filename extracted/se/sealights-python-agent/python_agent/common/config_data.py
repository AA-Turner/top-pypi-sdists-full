from enum import Enum
import uuid

from python_agent.common import constants
from python_agent.common.constants import DEFAULT_WORKSPACEPATH
from python_agent.utils import CommandType, to_str_obj


class ScmConfigArgs(object):
    def __init__(self, scm_provider, scm_version, scm_base_url, scm_type):
        self.scmProvider = scm_provider
        self.scmVersion = scm_version
        self.scmBaseUrl = scm_base_url
        self.scmType = scm_type


class ConfigData(object):
    def __init__(
        self,
        token=None,
        customer_id=None,
        server=None,
        proxy=None,
        build_session_id=None,
        is_compress=True,
    ):
        self.agentId = str(uuid.uuid4())
        self.agentType = None
        self.token = token
        self.server = server
        self.proxy = proxy
        self.isCompress = is_compress
        self.buildSessionId = build_session_id
        self.customerId = customer_id
        self.appName = None
        self.buildName = None
        self.branchName = None
        self.labId = None
        self.testStage = constants.DEFAULT_ENV
        self.additionalParams = {}
        self.workspacepath = DEFAULT_WORKSPACEPATH
        self.include = None
        self.exclude = None
        self.isInitialColor = True
        self.initialColor = constants.INITIAL_COLOR
        self.args = None
        self.program = None
        self.isSendLogs = False
        self.isOfflineMode = False
        self.scmType = constants.GIT_SCM
        self.scmProvider = None
        self.scmVersion = None
        self.scmBaseUrl = None
        self.commitHistoryLength = constants.DEFAULT_COMMIT_LOG_SIZE
        self.tokenFile = None
        self.buildSessionIdFile = None
        self.covReport = None
        self.perTest = True
        # Existing send-interval knobs (unchanged, default 10s). The alias
        # ``footprintsSendIntervalSecs`` from BE/CLI/env writes to these.
        self.interval = constants.INTERVAL_IN_MILLISECONDS
        self.intervalSeconds = constants.INTERVAL_IN_SECONDS
        self.footprintsBufferThresholdMB = (
            constants.FOOTPRINTS_BUFFER_THRESHOLD_MB_DEFAULT
        )
        # New: optional override for the previously-hardcoded collect interval
        # in FootprintsManager (was hardcoded to 1 second). ``None`` means
        # "keep today's hardcoded 1 second". The alias
        # ``footprintsCollectIntervalSecs`` from BE/CLI/env writes here.
        self._add_coverage_interval_seconds = None
        self.testSelection = {
            "enable": True,
            "interval": constants.TEST_RECOMMENDATION.interval_sec,
            "timeout": constants.TEST_RECOMMENDATION.timeout_sec,
        }
        self.testSelectionStatus = None
        self.test_selection_enable = True
        self.isDisabled = False
        self.testGroupId = None
        self.testProjectId = None
        self.prID = None
        self.auto_execution = False
        self.drop_init_footprints = False
        self.command_type = None
        self.command_name = None
        self.resolved_bsid_from_labid = False

    def apply_scm_args(self, scm_args):
        """
        Overrides scm properties by not None values of scm_args
        None scm_args are ignored
        :param scm_args:
        :return:
        """
        if scm_args:
            if scm_args.scmProvider:
                self.scmProvider = scm_args.scmProvider
            if scm_args.scmBaseUrl:
                self.scmBaseUrl = scm_args.scmBaseUrl
            if scm_args.scmVersion:
                self.scmVersion = scm_args.scmVersion
            if scm_args.scmType:
                self.scmType = scm_args.scmType

    def apply_build_session(self, build_session_params):
        self.buildSessionId = build_session_params.buildSessionId
        self.appName = build_session_params.appName
        self.branchName = build_session_params.branchName
        self.buildName = build_session_params.buildName
        self.resolved_bsid_from_labid = True

    def __str__(self):
        return "ConfigData:\n" + to_str_obj(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def get_is_disabled(self):
        return self.isDisabled

    def set_command_type(self, command_type):
        """
        Set the command type. If an Enum is provided, extract its value.
        This prevents JSON serialization issues with Enum objects.

        Args:
            command_type: Either a CommandType Enum or its int value
        """
        if isinstance(command_type, Enum):
            self.command_type = command_type.value
        else:
            self.command_type = command_type

    def get_command_type(self):
        return self.command_type

    def set_coverage_test_stage(self, testStage):
        if self.command_type != CommandType.TEST.value:
            self.testStage = testStage
