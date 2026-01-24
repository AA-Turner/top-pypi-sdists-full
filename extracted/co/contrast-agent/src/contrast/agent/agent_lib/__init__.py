# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections.abc import Mapping
import os.path
import ctypes

from threading import Lock
from contrast.utils.loggers import DEFAULT_LOG_PATH, DEFAULT_LOG_LEVEL
from contrast.utils.decorators import fail_loudly

from contrast_agent_lib import lib_contrast, constants
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")
INIT_LOCK = Lock()
IS_INITIALIZED = False


class CCheckQuerySinkResult(ctypes.Structure):
    _fields_ = [
        ("start_index", ctypes.c_ulonglong),
        ("end_index", ctypes.c_ulonglong),
        ("boundary_overrun_index", ctypes.c_ulonglong),
        ("input_boundary_index", ctypes.c_ulonglong),
    ]


lib_contrast.init_with_options.argtypes = [
    ctypes.c_bool,
    ctypes.c_char_p,
    ctypes.c_char_p,
]
lib_contrast.init_with_options.restype = ctypes.c_int

lib_contrast.change_log_settings.argtypes = [
    ctypes.c_bool,
    ctypes.c_char_p,
]
lib_contrast.change_log_settings.restype = ctypes.c_int
lib_contrast.evaluate_header_input.argtypes = (
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_longlong,
    ctypes.c_longlong,
    ctypes.POINTER(ctypes.c_size_t),
    ctypes.POINTER(ctypes.POINTER(constants.CEvalResult)),
)
lib_contrast.check_sql_injection_query.argtypes = (
    ctypes.c_uint32,
    ctypes.c_uint32,
    ctypes.c_uint32,
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.POINTER(CCheckQuerySinkResult)),
)
lib_contrast.evaluate_header_input.restype = ctypes.c_int
lib_contrast.check_sql_injection_query.restype = ctypes.c_int


@fail_loudly("Failed to initialize contrast-agent-lib", return_value=False)
def initialize(config: Mapping):
    global IS_INITIALIZED
    if not IS_INITIALIZED:
        with INIT_LOCK:
            if not IS_INITIALIZED:
                logger.debug("Initializing agent-lib")
                _init_with_options(
                    enable_logging=True,
                    log_dir=_get_log_dir(config),
                    log_level=_get_log_level(config),
                )
                IS_INITIALIZED = True
    return True


def _init_with_options(enable_logging: bool, log_dir: str, log_level: str):
    """
    Python translation of `init_with_options` + error handling
    """
    c_enable_logging = ctypes.c_bool(enable_logging)
    c_log_dir = ctypes.c_char_p(bytes(log_dir, "utf8"))
    c_log_level = ctypes.c_char_p(bytes(log_level, "utf8"))

    def is_valid_return(code):
        return code == 0

    call(
        lib_contrast.init_with_options,
        is_valid_return,
        c_enable_logging,
        c_log_dir,
        c_log_level,
    )


def update_log_options(log_level: str):
    valid_return = True

    if not IS_INITIALIZED:
        return False

    c_enable_logging = ctypes.c_bool(True)
    c_log_level = ctypes.c_char_p(bytes(log_level, "utf8"))

    def is_valid_return(code):
        valid_return = code == 0
        return valid_return

    call(
        lib_contrast.change_log_settings,
        is_valid_return,
        c_enable_logging,
        c_log_level,
    )

    return valid_return


def call(c_fn, is_valid_return, *args):
    """
    Calls the provided agent-lib function with the specified positional args.

    If the function returns normally, returns the result. Otherwise, retrieves the
    corresponding error message using `last_error_message` and logs profusely.
    @param is_valid_return: function used to handle the return from the agent lib call.
        This was added because different calls to agent lib have different return codes

    This function must remain synchronous - do not use `async def`! Error handling for
    agent-lib functions must occur without another task in the same thread interrupting.
    """
    if not IS_INITIALIZED:
        logger.debug("WARNING: call to agent-lib before initialization")

    fn_result = c_fn(*args)

    if is_valid_return(fn_result):
        return fn_result

    logger.debug(
        "Error from agent-lib - will retrieve error message. "
        "function: %s; args: %s; return: %s",
        c_fn.__name__,
        [getattr(a, "value", a) for a in args],
        fn_result,
    )

    # +1 prevents off-by-1 edge cases
    message_length = lib_contrast.last_error_message_length() + 1
    stack_length = lib_contrast.last_error_stack_length() + 1

    c_message_length = ctypes.c_int(message_length)
    c_stack_length = ctypes.c_int(stack_length)

    c_message_buffer = ctypes.create_string_buffer(message_length)
    c_stack_buffer = ctypes.create_string_buffer(stack_length)

    result = lib_contrast.last_error_message(
        c_message_buffer,
        c_message_length,
        c_stack_buffer,
        c_stack_length,
    )

    if result >= 0:
        logger.debug(
            "Error message from agent-lib: %s; stack: %s",
            c_message_buffer.value.decode("utf8"),
            c_stack_buffer.value.decode("utf8") or "<no stack info>",
        )
    else:
        logger.debug(
            "Failed to retrieve agent-lib last error message. "
            "last_error_message return: %s",
            result,
        )

    return fn_result


def _get_log_dir(config: Mapping):
    """
    For now, use the same directory as the agent logger specified in the local config.
    """
    agent_log_dir = config.get("agent.logger.path", DEFAULT_LOG_PATH)
    # works even for STDOUT because of `dirname`
    return os.path.abspath(os.path.dirname(agent_log_dir))


def _get_log_level(config: Mapping):
    level = config.get("agent.logger.level", DEFAULT_LOG_LEVEL)
    return level.upper()
