# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import atexit
import sys
import sysconfig
import threading
import warnings
from collections.abc import Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from os import environ
from typing import TYPE_CHECKING, Literal, Optional

import contrast
from contrast import AGENT_CURR_WORKING_DIR, __version__, loader, policy_v2
from contrast.agent import (
    agent_lib,
    patch_controller,
    sys_monitoring,
    thread_watcher,
)
from contrast.agent.assess import contrast_event
from contrast.agent.assess.rules.providers.enable import run_providers_in_thread
from contrast.agent.assess.sampling import SamplerConfig, update_sampler_config
from contrast.agent.exclusions import Exclusions
from contrast.agent.framework import UNKNOWN_FRAMEWORK, Framework
from contrast.agent.inventory import runtime_environment
from contrast.agent.inventory.library_reader import LibraryReader
from contrast.agent.policy import registry_v2
from contrast.agent.settings import Settings
from contrast.configuration.agent_config import AgentConfig
from contrast.reporting import Reporter, get_reporting_client
from contrast.reporting.request_masker import RequestMasker
from contrast.utils import timer
from contrast.utils.configuration_utils import get_platform
from contrast.utils.decorators import fail_loudly, fail_quietly
from contrast.utils.exceptions.deprecation_warning import ContrastDeprecationWarning
from contrast.utils.locale import DEFAULT_ENCODING
from contrast.utils.loggers.logger import (
    configure_agent_logger,
    configure_syslog_logger,
    setup_basic_agent_logger,
    setup_security_logger,
)
from contrast.utils.namespace import Namespace
from contrast_rewriter import initialize_rewriter_logger, is_rewriter_enabled

if TYPE_CHECKING:
    from contrast.agent.policy.registry_v2 import EventHandler


# NOTE: policy is currently loaded/generated on import. It is applied explicitly in
# policy/applicator.py
from contrast import policy  # noqa: F401

logger = setup_basic_agent_logger()
LOGS_SEPARATOR = "-" * 120

SHARED_WARNING_MESSAGE = """
For specific circumstances where explicit middleware configuration is still
required, set `agent.python.enable_automatic_middleware` to `false` in the
configuration file or set `CONTRAST__AGENT__PYTHON__ENABLE_AUTOMATIC_MIDDLEWARE=false`
in your environment to suppress this warning.

Please see the documentation for additional details:
    https://docs.contrastsecurity.com/en/python-middleware.html
"""

MIDDLEWARE_WITHOUT_SITECUSTOMIZE_WARNING = f"""
Explicit middleware configuration is no longer required or recommended. Instead,
users should run their application with the `contrast-python-run` command, which
automatically detects and enables framework-specific middleware.
{SHARED_WARNING_MESSAGE}
"""

NO_EXPLICIT_MIDDLEWARE_WARNING = f"""
Explicit middleware configuration is generally no longer necessary when using
the `contrast-python-run` command.
{SHARED_WARNING_MESSAGE}
"""

NO_SPECIFIC_MIDDLEWARE_WARNING = """
Using framework-specific middleware is no longer recommended for {}.
Use contrast.{}.ContrastMiddleware instead.
"""

PROTECT_MISMATCH_MESSAGE = (
    "Protect enabled in local config but disabled in Contrast UI. It is running."
)
ASSESS_MISMATCH_MESSAGE = (
    "Assess enabled in local config but disabled in Contrast UI. It is running."
)

if not contrast.telemetry_disabled():
    from contrast.agent.telemetry import Telemetry
else:
    Telemetry = None

Watcher = Optional  # A Watcher is a type that will watch config changes.


class module(Namespace):
    server_environment: str | None = None
    init_lock: threading.Lock = threading.Lock()
    sampling_cfg: Watcher[SamplerConfig] = None
    exclusions: Watcher[Exclusions] = None
    request_data_masker: Watcher[RequestMasker] = None
    event_handlers: dict[str, list[EventHandler]] = {}

    is_initialized = False
    id: int | None = None
    settings: Settings | None = None
    reporting_client: Reporter | None = None
    first_request: bool = True
    assess_enabled: bool = False
    assess_tags = ""
    observe_enabled: bool = False
    protect_enabled: bool = False

    automatic_middleware: ContextVar = ContextVar("automatic_middleware", default=False)

    deprecated_middleware: tuple[str, bool] | None = None

    configured_app_name: str | None = None
    configured_server_name: str | None = None

    # NOTE: these fields can be set prior to initialization
    framework: Framework = UNKNOWN_FRAMEWORK
    app_name: str | None = None


def is_runner_in_use() -> bool:
    return environ.get("CONTRAST_INSTALLATION_TOOL") == "CONTRAST_PYTHON_RUN"


def free_threading_available() -> bool:
    """
    Indicates if free-threading -could- be enabled, not whether or not it is actually
    enabled. The config option Py_GIL_DISABLED is slightly misleading.
    """
    if sys.version_info[:2] < (3, 13):
        return False
    return bool(sysconfig.get_config_var("Py_GIL_DISABLED"))


def free_threading_enabled() -> bool:
    """
    Indicates whether or not free-threading is actually enabled.
    """
    if sys.version_info[:2] < (3, 13):
        return False
    return not sys._is_gil_enabled()


@fail_quietly(return_value=False)
def jit_available() -> bool:
    """
    Indicates whether or not the JIT is built into this version of python.

    Potentially unreliable in 3.13.
    """
    if sys.version_info[:2] < (3, 13):
        return False
    if sys.version_info[:2] == (3, 13):
        return "_Py_JIT" in sysconfig.get_config_var("PY_CORE_CFLAGS")

    from sys import _jit

    return _jit.is_available()


@fail_quietly(return_value=False)
def jit_enabled() -> bool:
    """
    Indicates whether or not the JIT is currently enabled in this python process.

    Potentially unreliable in 3.13.
    """
    if sys.version_info[:2] < (3, 13):
        return False
    if sys.version_info[:2] == (3, 13):
        import _testinternalcapi

        get_optimizer = getattr(_testinternalcapi, "get_optimizer", lambda: None)
        return get_optimizer() is not None

    from sys import _jit

    return _jit.is_enabled()


@fail_quietly(return_value="unknown")
def tail_call_interpreter() -> bool | Literal["unknown"]:
    """
    Indicates whether or not the tail call interpreter is enabled in this python process.

    See https://docs.python.org/3.14/whatsnew/3.14.html#a-new-type-of-interpreter for details
    on the tail call interpreter.
    """
    return bool(sysconfig.get_config_var("Py_TAIL_CALL_INTERP"))


def _log_environment(settings: Settings):
    """
    Log current working directory, python version and pip version
    """
    log_level = settings.config.get_option("agent.logger.level").value().upper()

    logger.info(
        "ENVIRONMENT",
        python_version=sys.version,
        agent_version=__version__,
        assess_enabled=module.assess_enabled,
        protect_enabled=module.protect_enabled,
        using_runner=is_runner_in_use(),
        using_rewriter=is_rewriter_enabled(),
        preinstrument_flag=patch_controller.is_preinstrument_flag_set(),
        using_sys_monitoring=sys_monitoring.is_enabled(),
        log_level=log_level,
        configured_application_name=module.configured_app_name,
        detected_application_name=module.app_name,
        detected_framework=module.framework,
        discovered_webserver=settings.server,
        cwd=AGENT_CURR_WORKING_DIR,
        executable=sys.executable,
        platform=get_platform(),
        free_threading_available=free_threading_available(),
        free_threading_enabled=free_threading_enabled(),
        jit_available=jit_available(),
        jit_enabled=jit_enabled(),
        tail_call_interpreter=tail_call_interpreter(),
        default_encoding=DEFAULT_ENCODING,
        debug_info={"sys.argv": sys.argv} if log_level == "DEBUG" else None,
    )

    # py39: remove
    if sys.version_info[:2] == (3, 9):
        _log_and_warn(
            "Contrast Security support for Python 3.9 is deprecated "
            "as this version reached its end-of-life in October 2025 (PEP 596). "
            "A future version of the Contrast Python Agent may drop support for Python 3.9."
        )


def _warn_for_misleading_config(settings: Settings):
    protect_option = settings.config.get_option("protect.enable")
    protect_enabled = protect_option.value()
    if protect_enabled and not protect_option.ui_value:
        logger.warning(PROTECT_MISMATCH_MESSAGE)

    assess_option = settings.config.get_option("assess.enable")
    assess_enabled = assess_option.value()
    if assess_enabled and not assess_option.ui_value:
        logger.warning(ASSESS_MISMATCH_MESSAGE)

    if (
        settings.is_agent_config_enabled()
        and not protect_enabled
        and not assess_enabled
    ):
        logger.warning("Neither Protect nor Assess is enabled. Neither is running.")


def add_config_watchers(config: AgentConfig) -> None:
    """
    Adds all config watchers to the config object.
    """
    config.add_watcher(configure_agent_logger)
    config.add_watcher(configure_syslog_logger)
    config.add_watcher(set_assess_enabled)
    config.add_watcher(set_observe_enabled)
    config.add_watcher(set_protect_enabled)
    config.add_watcher(set_exclusions)
    config.add_watcher(set_data_masking)
    config.add_watcher(set_server_environment_and_sampler)
    config.add_watcher(
        lambda cfg: agent_lib.initialize(cfg) if cfg["protect.enable"] else None
    )


def initialize_libraries(reporter: Reporter):
    """
    Read libraries from the application
    """
    LibraryReader(reporter).start()


@fail_loudly("Unable to initialize Contrast Agent Settings.", return_value=False)
def initialize_settings():
    """
    Initialize agent settings.

    Returns True on settings being initialized and False if any failure.
    """
    module.settings = Settings()

    return True


def initialize_application(reporting_client: Reporter, settings: Settings) -> bool:
    if ui_settings := reporting_client.initialize_application(
        settings.config,
        server_type=settings.server_type,
    ):
        settings.apply_server_settings(ui_settings.get("server_settings", {}))
        settings.apply_application_settings(ui_settings.get("application_settings", {}))
        settings.apply_identification(ui_settings.get("identification", {}))
        return True
    return False


def is_initialized() -> bool:
    return module.is_initialized


def get_settings():
    return module.settings


def get_server_environment():
    return module.server_environment


def _get_app_name(config: Mapping, app_name):
    if config and (config_name := config.get("application.name")):
        return config_name

    return app_name if app_name else "root"


def get_app_name():
    return module.configured_app_name or _get_app_name(
        module.settings.config, module.app_name
    )


def _get_server_name(config: Mapping):
    """
    Hostname of the server

    Default is socket.gethostname() or localhost
    """
    if config:
        return config.get("server.name")
    return None


def get_server_name():
    return module.configured_server_name or _get_server_name(module.settings.config)


def is_first_request():
    return module.first_request


def set_first_request(val: bool):
    module.first_request = val


def set_assess_enabled(config: Mapping):
    module.assess_enabled = config["assess.enable"]


def set_protect_enabled(config: Mapping):
    module.protect_enabled = config["protect.enable"]


def set_observe_enabled(config: Mapping):
    module.observe_enabled = config["observe.enable"]


@fail_loudly("Failed to register detected framework")
def set_detected_framework(distribution_name: str):
    """
    Registers the detected framework by its distribution name.

    It is safe to call this method prior to initialization of agent state. In
    order to be effective, this method should be called prior to middleware
    initialization.
    """
    module.framework = Framework(distribution_name)


def detected_framework() -> Framework:
    return module.framework


@fail_loudly("Failed to register application name")
def set_application_name(name: str | None):
    """
    Registers the name of the application

    It is safe to call this method prior to initialization of agent state. In
    order to be effective, this method should be called prior to middleware
    initialization.
    """
    module.app_name = name


def set_server_environment_and_sampler(config):
    module.server_environment = config.get("server.environment")

    update_sampler_config(config)


def set_exclusions(config: Mapping):
    module.exclusions = Exclusions(config)


def set_data_masking(config: Mapping):
    module.request_data_masker = RequestMasker(config)


def _log_and_warn(msg):
    warnings.warn(msg, ContrastDeprecationWarning, stacklevel=2)
    logger.warning(msg)


def _check_middleware_warnings():
    # NOTE: currently, we are skipping framework-specific middleware deprecation
    # warnings. In the future, we might want to actually deprecate these. For now,
    # however, we are holding off.
    # this should be `if module.deprecated_middleware is not None:`
    if False:
        (  # pylint: disable=unpacking-non-sequence
            framework,
            is_asgi,
        ) = module.deprecated_middleware
        message = NO_SPECIFIC_MIDDLEWARE_WARNING.format(
            framework, "asgi" if is_asgi else "wsgi"
        )
        _log_and_warn(message)

    # This configuration suppresses both warnings
    if not module.settings.config.enable_automatic_middleware:
        return

    # Warn for the case where middleware is only explicitly configured,
    # missing sitecustomize early rewrites and patches.
    if not loader.SITECUSTOMIZE_LOADED:
        _log_and_warn(MIDDLEWARE_WITHOUT_SITECUSTOMIZE_WARNING)
    # Warn for the case where middleware is explicitly configured but also detected automatically
    # An actual warning doesn't seem necessary in this case, just a log message
    elif not module.automatic_middleware.get():
        logger.warning(NO_EXPLICIT_MIDDLEWARE_WARNING)


def initialize():
    """
    If this method is called more than once per process, we use the is_initialized
    flag to only run the following work once:
        - library analysis thread initialization
        - turning on patches
        - hardcoded rule providers
        - scanning config rules
        - environment logging
        - loading common configuration
        - initializing settings

    In order to avoid a warning message, callers should check is_initialized()
    prior to calling this function.
    """
    with module.init_lock:
        if module.is_initialized:
            _check_middleware_warnings()
            logger.warning("Attempted to initialize agent state more than once")
            return

        module.id = id(module)

        logger.info(
            "Initializing Contrast Agent %s",
            __name__,
            id=module.id,
            version=__version__,
        )

        if not initialize_settings():
            return

        if module.settings is None:
            logger.warning("Contrast Agent is not enabled.")
            return

        module.configured_server_name = _get_server_name(module.settings.config)
        module.configured_app_name = _get_app_name(
            module.settings.config, module.app_name
        )
        module.assess_tags = module.settings.config["assess.tags"]

        if not module.settings.is_agent_config_enabled():
            logger.warning("Contrast Agent is disabled by local configuration.")
            module.settings.log_effective_config()
            return

        add_config_watchers(module.settings.config)
        setup_security_logger(module.settings.config)
        module.settings.config.log_config()

        # NOTE (TODO: PYT-3016)
        # This assumes that initialize is only ever called from middleware.
        # If at some point this no longer holds, it may be necessary to pass a
        # flag to initialize indicating whether these warnings should be
        # processed or not.
        _check_middleware_warnings()

        # The rewriter is applied long before we have any settings or logger so
        # the deferred logs are finally processed here
        initialize_rewriter_logger(logger)

        module.reporting_client = get_reporting_client(module.settings.config)
        module.reporting_client.start()
        if module.settings.config[
            "reporting.contrast.enable"
        ] and not initialize_application(module.reporting_client, module.settings):
            disable_agent(reason="Unable to initialize application in Contrast UI")
            module.settings.log_effective_config()
            return

        _warn_for_misleading_config(module.settings)

        preinstrument = patch_controller.is_preinstrument_flag_set()

        if module.assess_enabled or preinstrument:
            sys_monitoring.enable()

        # Eventually this should be handled by Fireball.

        module.reporting_client.new_effective_config(
            module.settings.generate_effective_config()
        )

        # This MUST happen after the initialization calls for TeamServer messaging
        # (sending server start and application start) to ensure that TeamServer will
        # accept the messages sent by our background reporting threads
        # Skip telemetry since it is enabled later in this method
        thread_watcher.ensure_running(module, skip_telemetry=True)

        module.settings.log_effective_config()

        if (
            module.settings.is_inventory_enabled() or preinstrument
        ) and module.settings.is_analyze_libs_enabled():
            initialize_libraries(module.reporting_client)

        if module.settings.config["reporting.contrast.enable"]:
            runtime_environment.report_server_runtime(
                module.reporting_client,
                module.settings.config.get("server.discover_cloud_resource"),
            )

        registry_v2.register_policy_definitions(policy_v2.definitions())
        module.event_handlers = registry_v2.generate_policy_event_handlers(
            assess=module.assess_enabled,
            observe=module.observe_enabled,
            protect=module.protect_enabled,
        )

        patch_controller.enable_patches(preinstrument=preinstrument)

        if module.assess_enabled or preinstrument:
            # For now agent runtime starts before config scanning
            # this will be reset when time_limit_threshold is reached,
            # it doesn't symbolize the total agent runtime for all time.
            module.settings.agent_runtime_window = timer.now_ms()

            contrast_event.initialize(module.settings.config)

            run_providers_in_thread()
            # NOTE (TODO: PYT-3016) This should stay in middleware
            # scan_configs_in_thread()

        _log_environment(module.settings)

        if (module.protect_enabled or preinstrument) and not agent_lib.initialize(
            module.settings.config
        ):
            disable_agent(reason="Unable to initialize Protect analysis library")
            return

        if free_threading_enabled():
            disable_agent(
                reason=(
                    "Free-threading is enabled in this python process - Contrast cannot"
                    " run in this environment"
                )
            )
            return

        if jit_enabled():
            disable_agent(
                reason=(
                    "Python's experimental JIT compiler is enabled in this process -"
                    " Contrast cannot run in this environment"
                )
            )
            return

        logger.info(
            "Finished Initializing Contrast Agent %s",
            __name__,
            id=module.id,
        )

        if Telemetry is not None:
            contrast.TELEMETRY = Telemetry()
            contrast.TELEMETRY.start()
            atexit.register(contrast.TELEMETRY.stop)

        module.is_initialized = True


def disable_agent(reason: str):
    logger.error("Fatal error: Disabling Contrast", reason=reason)
    if module.settings and module.settings.config:
        enable_option = module.settings.config.get_option("enable")
        enable_option.override_value = False


def detected_deprecated_middleware(*, framework: str = "", is_asgi: bool = False):
    module.deprecated_middleware = (framework, is_asgi)


@contextmanager
def automatic_middleware():
    """
    Context manager to be used by automatic middleware hooks when initializing middleware

    This enables us to determine when middleware is initialized from within our
    automatic middleware hooks without having to change the API of any
    middleware classes.
    """
    try:
        module.automatic_middleware.set(True)
        yield
    finally:
        module.automatic_middleware.set(False)


def in_automatic_middleware() -> bool:
    return module.automatic_middleware.get()
