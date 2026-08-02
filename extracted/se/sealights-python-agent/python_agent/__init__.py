import os
import sys
from logging.config import dictConfig

# Python 3.13 compatibility: handle potential import issues gracefully
try:
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning

    urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    # Fallback for potential import issues on Python 3.13
    try:
        import urllib3
        from urllib3.exceptions import InsecureRequestWarning

        urllib3.disable_warnings(InsecureRequestWarning)
    except ImportError:
        # If urllib3 is not available, continue without warnings suppression
        pass
__legacy_mode__ = os.environ.get("SL_LEGACY_MODE", "false").lower() == "true"


__version__ = "2.10.17"


__package_name__ = "sealights_python_agent"

# Python 3.13 support notification
if sys.version_info >= (3, 13):
    import logging

    logger = logging.getLogger(__name__)
    logger.debug(
        f"Sealights Python Agent v{__version__} running on Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )

####################  PyNext Mode  ####################
if not __legacy_mode__:
    log_level = os.environ.get("SL_LOG_LEVEL", "ERROR").upper()
    is_debug = os.environ.get("SL_DEBUG", "false").lower() == "true"
    current_level = "DEBUG" if is_debug else log_level
    save_log_file = os.environ.get("SL_SAVE_LOG_FILE", "false").lower() == "true"
    LOG_CONF = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [SL][%(levelname)s]: %(message)s [%(filename)s:%(lineno)d]",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            },
            "standard-debug": {
                "format": "%(asctime)s [SL][%(levelname)s]: %(message)s [%(filename)s:%(lineno)d] [pid:%(process)d|%(thread)d]",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            },
        },
        "handlers": {
            "cli": {
                "class": "logging.StreamHandler",
                "level": current_level,
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
            "cli-debug": {
                "class": "logging.StreamHandler",
                "level": current_level,
                "formatter": "standard-debug",
                "stream": "ext://sys.stdout",
            },
        },
    }
    handlers = []
    if is_debug:
        handlers.append("cli-debug")
    else:
        handlers.append("cli")
    if save_log_file:
        LOG_CONF["handlers"].update(
            {
                "sealights-file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": current_level,
                    "formatter": "standard-debug",
                    "filename": "sealights-python-agent.log",
                    "mode": "a",
                    "maxBytes": 10485760,
                    "backupCount": 10,
                }
            }
        )
        handlers.append("sealights-file")
    LOG_CONF["loggers"] = {
        "python_agent": {
            "handlers": handlers,
            "level": current_level,
            "propagate": True,
        },
    }
####################  End PyNext Mode  ###############

####################  Legacy Mode  ####################
else:
    print("------- Sealights Agent Is Running In Legacy Mode --------")
    LOG_CONF = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "sealights-standard": {
                "format": "%(asctime)s SEALIGHTS %(levelname)s: [%(process)d|%(thread)d] %(name)s %(message)s"
            },
            "standard": {"format": "%(asctime)s SEALIGHTS %(levelname)s: %(message)s"},
        },
        "handlers": {
            "cli": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "__main__": {"handlers": ["cli"], "level": "DEBUG", "propagate": True},
            "python_agent.build_scanner.executors": {
                "handlers": ["cli"],
                "level": "DEBUG",
                "propagate": True,
            },
            "python_agent.test_listener.executors": {
                "handlers": ["cli"],
                "level": "DEBUG",
                "propagate": True,
            },
            "python_agent.common.token": {
                "handlers": ["cli"],
                "level": "DEBUG",
                "propagate": True,
            },
            "python_agent.admin": {
                "handlers": ["cli"],
                "level": "DEBUG",
                "propagate": True,
            },
            "python_agent.common.configuration_manager": {
                "handlers": ["cli"],
                "level": "DEBUG",
                "propagate": True,
            },
            "python_agent.common.environment_variables_resolver": {
                "handlers": ["cli"],
                "level": "DEBUG",
                "propagate": True,
            },
            "urllib3.connectionpool": {
                "handlers": [],
                "level": "WARN",
                "propagate": False,
            },
            "pip": {"handlers": [], "level": "WARN", "propagate": False},
            "python_agent.serverless": {
                "handlers": ["cli"],
                "level": "INFO",
                "propagate": True,
            },
        },
    }
    if os.environ.get("SL_DEBUG"):
        LOG_CONF["handlers"].update(
            {
                "sealights-console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "sealights-standard",
                    "stream": "ext://sys.stdout",
                },
                "sealights-file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "sealights-standard",
                    "filename": "sealights-python-agent.log",
                    "mode": "a",
                    "maxBytes": 10485760,
                    "backupCount": 10,
                },
            }
        )
        LOG_CONF["loggers"].update(
            {
                "python_agent": {
                    "handlers": ["sealights-console", "sealights-file"],
                    "level": "DEBUG",
                    "propagate": False,
                }
            }
        )
####################  End Legacy Mode  ####################

dictConfig(LOG_CONF)
