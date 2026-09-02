from .version import VERSION
import six
import os

_TRUE_VALUES = ['y', 'Y', 'yes',  'Yes',  'YES', 'true', 'True', 'TRUE', '1', True]


class LoggingConfiguration(object):
    LOGGER_NAME = "rook"
    FILE_NAME = "rookout/python-rook.log"
    LOG_TO_STDERR = False
    LOG_LEVEL = "INFO"
    PROPAGATE_LOGS = False
    LOG_TO_REMOTE = False
    DEBUG = False
    DEV_DEBUG = False
    QUIET = False


class VersionConfiguration(object):
    VERSION = VERSION
    COMMIT = "CommitGoesHere"


class ControllerAddress(object):
    HOST = 'wss://control.rookout.com'
    PORT = 443


class AgentComConfiguration(object):
    COMMAND_THREAD_NAME = "rookout_agent_com"
    MAX_MESSAGE_LENGTH = 1024 * 1024
    MAX_QUEUE_MESSAGES_LENGTH = 15 * 1024 * 1024
    BACK_OFF = 0.2
    MAX_SLEEP = 60
    TIMEOUT = 3
    REQUEST_TIMEOUT_SECS = 30
    PING_TIMEOUT = 30
    PING_INTERVAL = 10
    RESET_BACKOFF_TIMEOUT = 3*60.0
    FLUSH_TIMEOUT = 3
    MAX_QUEUED_MESSAGES = 1000
    AGENT_COM_INCOMING_MAX_MESSAGE_SIZE = 500 * 1024


class OutputWsConfiguration(object):
    MAX_STATUS_UPDATES = 200
    MAX_LOG_ITEMS = 200
    MAX_AUG_MESSAGES = 1000
    BUCKET_REFRESH_RATE = 5


class RateLimiter(object):
    MIN_RATE_LIMIT_VALUE_NS = 8000
    GLOBAL_RATE_LIMIT_QUOTA_MS = ""
    GLOBAL_RATE_LIMIT_WINDOW_SIZE_MS = ""
    GLOBAL_RATE_LIMIT = os.environ.get("ROOKOUT_GLOBAL_RATE_LIMIT", "")
    USING_GLOBAL_RATE_LIMITER = False


class InstrumentationConfig(object):
    ENGINE = "auto"
    MIN_TIME_BETWEEN_HITS_MS = 100
    MAX_AUG_TIME_MS = 400


class ImportServiceConfig(object):
    USE_IMPORT_HOOK = True
    SYS_MODULES_QUERY_INTERVAL = 0.25
    THREAD_NAME = "rookout_import_service_thread"


class HttpServerServiceConfig(object):
    SERVICES_NAMES = ""


class GitConfig(object):
    GIT_COMMIT = None
    GIT_ORIGIN = None
    SOURCES = {}


class ShutdownConfig(object):
    IS_SHUTTING_DOWN = False


class DumpConfig(object):
    STRING_CACHE_USERMESSAGE = False
    PROTOBUF_VERSION_2 = False


def update_config(new_config):
    from rook.logger import logger

    try:
        for key, val in six.iteritems(new_config):
            if key == 'PYTHON_StringCache_UserMessage':
                logger.debug("Updating StringCache_UserMessage value to: " + str(val in _TRUE_VALUES))
                DumpConfig.STRING_CACHE_USERMESSAGE = val in _TRUE_VALUES
                continue
            if key == 'PYTHON_PROTOBUF_VERSION_2':
                protobuf_2_env_var = os.environ.get('ROOKOUT_Protobuf_Version2')

                if protobuf_2_env_var:
                    logger.debug("Updating ROOKOUT_Protobuf_Version2 value to: " + str(protobuf_2_env_var in _TRUE_VALUES))
                    DumpConfig.PROTOBUF_VERSION_2 = protobuf_2_env_var in _TRUE_VALUES
                else:
                    logger.debug("Updating ROOKOUT_Protobuf_Version2 value to: " + str(val in _TRUE_VALUES))
                    DumpConfig.PROTOBUF_VERSION_2 = val in _TRUE_VALUES
                continue
            if key == "PYTHON_GLOBAL_RATE_LIMIT_QUOTA_MS":
                if RateLimiter.GLOBAL_RATE_LIMIT == "":
                    RateLimiter.GLOBAL_RATE_LIMIT_QUOTA_MS = val

                    if RateLimiter.GLOBAL_RATE_LIMIT_WINDOW_SIZE_MS != "":
                        RateLimiter.GLOBAL_RATE_LIMIT = RateLimiter.GLOBAL_RATE_LIMIT_QUOTA_MS + "/" + \
                                                        RateLimiter.GLOBAL_RATE_LIMIT_WINDOW_SIZE_MS
                        logger.debug("Updating GLOBAL_RATE_LIMIT value to: " + RateLimiter.GLOBAL_RATE_LIMIT)
                else:
                    logger.debug("GLOBAL_RATE_LIMIT already set to: " + RateLimiter.GLOBAL_RATE_LIMIT)
            if key == "PYTHON_GLOBAL_RATE_LIMIT_WINDOW_SIZE_MS":
                if RateLimiter.GLOBAL_RATE_LIMIT == "":
                    RateLimiter.GLOBAL_RATE_LIMIT_WINDOW_SIZE_MS = val

                    if RateLimiter.GLOBAL_RATE_LIMIT_QUOTA_MS != "":
                        RateLimiter.GLOBAL_RATE_LIMIT = RateLimiter.GLOBAL_RATE_LIMIT_QUOTA_MS + "/" + \
                                                        RateLimiter.GLOBAL_RATE_LIMIT_WINDOW_SIZE_MS
                        logger.debug("Updating GLOBAL_RATE_LIMIT value to: " + RateLimiter.GLOBAL_RATE_LIMIT)

    except BaseException:
        logger.exception("Failed to update configuration: " + str(new_config))
