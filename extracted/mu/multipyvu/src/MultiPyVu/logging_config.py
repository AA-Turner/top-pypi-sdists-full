'''
logging_config.py is used to hold methods to help with the logging module

Server.__init__() and Client.open() each call setup_logging() every time
they run, often while another thread (e.g. the server's socket-monitoring
thread) is actively logging through the root handlers. These track whether
the root logger is already configured the way this call wants, so a repeat
call can just return instead of closing and rebuilding handlers a live
thread may be writing through. That avoids a race where RotatingFileHandler's
rename fails with WinError 32 because Windows won't rename a file another
handle still has open.
'''

import logging.config
import threading
from logging import Logger
from os import path

import yaml

from .project_vars import LOG_NAME, CLIENT_NAME, SERVER_NAME

_setup_lock = threading.Lock()
_configured_display_logger_name = None


def absolute_path(filename: str) -> str:
    """
    Finds the absolute path of a file based on its location
    relative to the gui module

    Parameters:
    -----------
    filename: str
        The file location based on its relative path from the gui module
    """
    abs_path = path.abspath(
        path.join(path.dirname(
            __file__), './'))
    return path.join(abs_path, filename)


def setup_logging(display_logger_name: bool = True):
    """
    Sets up logging configuration from YAML file.
    Can be safely called multiple times without creating duplicate handlers.

    Parameters:
    -----------
    display_logger_name: bool
        Whether to include logger name in the console output format
    """
    global _configured_display_logger_name

    with _setup_lock:
        root = logging.getLogger()
        # Server.__exit__() calls remove_logs() on the MultiVuServer
        # logger every time a Server closes (even on success), which
        # strips and closes its handlers without touching root's. So
        # root.handlers alone isn't enough to know things are still
        # configured -- check the named loggers remove_logs() can
        # strip too, or a later Server() would find MultiVuServer
        # silently handler-less for the rest of the process.
        already_configured = (
            root.handlers
            and logging.getLogger(SERVER_NAME).handlers
            and logging.getLogger(CLIENT_NAME).handlers
            and _configured_display_logger_name == display_logger_name
        )
        if already_configured:
            # Already configured this way; skip tearing down handlers
            # that another thread may currently be logging through.
            return

        yaml_path = 'logging_config.yaml'
        abs_path = path.abspath(path.join(path.dirname(__file__), './'))
        yaml_path = path.join(abs_path, yaml_path)

        try:
            with open(yaml_path, 'r') as f:
                log_config = yaml.safe_load(f.read())

                # First, clean up existing loggers to avoid duplicates
                for handler in root.handlers[:]:
                    root.removeHandler(handler)
                    handler.close()

                # Define variables
                log_config['handlers']['file']['filename'] = LOG_NAME
                formatter = 'show_name' if display_logger_name else 'no_name'
                log_config['handlers']['console']['formatter'] = formatter

                logging.config.dictConfig(log_config)
                _configured_display_logger_name = display_logger_name
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error setting up logging: {e}")
            # Optionally set up a basic configuration here
            logging.basicConfig(level=logging.INFO)


def remove_logs(logger: Logger) -> None:
    """
    Removes all references to handlers for the logger and closes the logger.
    """
    if logger:
        # Make a copy since we'll modify the list
        handlers = logger.handlers.copy()
        for handler in handlers:
            logger.removeHandler(handler)
            handler.flush()
            handler.close()
