"""
Summary:
    spotlib Project-level Defaults and Settings

Module Attributes:
    - user_home (TYPE str):
        $HOME environment variable, present for most Unix and Unix-like POSIX systems
    - config_dir (TYPE str):
        directory name default for stsaval config files (.stsaval)
    - config_path (TYPE str):
        default for stsaval config files, includes config_dir (~/.stsaval)
    - key_deprecation (TYPE str):
        Deprecation logic that spotlib uses when 2 keys exist for a user.
"""

import os
import inspect
import logging
from spotlib.common import read_local_config, get_os, os_parityPath
from spotlib._version import __version__



logger = logging.getLogger(__version__)
logger.setLevel(logging.INFO)


# --  project-level DEFAULTS  ------------------------------------------------


try:

    env_info = get_os(detailed=True)
    OS = env_info['os_type']

except KeyError as e:
    logger.critical(
        '%s: %s variable is required and not found in the environment' %
        (inspect.stack()[0][3], str(e)))
    raise e

else:
    # local vars -- this section executes as default; if windows, execute diff
    # section with appropriate pathnames

    # project
    PACKAGE = 'spotlib'
    PACKAGE_CLI = 'spotcli'
    LICENSE = 'GPL v3'
    LICENSE_DESC = 'General Public License v3'
    version = __version__

    # filesystem location
    root = '/tmp'

    # config parameters
    config_dir = '.config'
    config_subdir = PACKAGE
    config_filename = 'spotlib.conf'
    config_dirpath = os_parityPath(os.path.join(config_dir, config_subdir))
    config_path = os_parityPath(os.path.join(config_dirpath, config_filename))

    # logging parameters
    enable_logging = False
    log_mode = 'STREAM'
    log_filename = 'spotlib.log'
    log_dir = os_parityPath(os.path.join(root, 'logs'))
    log_path = os_parityPath(os.path.join(log_dir, log_filename))

    seed_config = {
        "PROJECT": {
            "PACKAGE": PACKAGE,
            "PACKAGE_CLI": PACKAGE_CLI,
            "PACKAGE_VERSION": version
        },
        "CONFIG": {
            "CONFIG_DATE": "",
            "CONFIG_FILENAME": config_filename,
            "CONFIG_DIR": config_dirpath,
            "CONFIG_SUBDIR": config_subdir,
            "CONFIG_PATH": config_path
        },
        "LOGGING": {
            "ENABLE_LOGGING": enable_logging,
            "LOG_FILENAME": log_filename,
            "LOG_PATH": log_path,
            "LOG_MODE": log_mode,
            "SYSLOG_FILE": False
        }
    }

try:

    if not os.path.exists(log_dir) and log_mode == 'FILE':
        os.makedirs(log_dir)

    if os.path.exists(config_path):
        # parse config file
        local_config = read_local_config(cfg=config_path)
        # fail to read, set to default config
        if not local_config:
            local_config = seed_config
    else:
        local_config = seed_config

except OSError as e:
    logger.exception(
        '%s: Error when attempting to access or create local log and config %s' %
        (inspect.stack()[0][3], str(e))
    )
    raise e
