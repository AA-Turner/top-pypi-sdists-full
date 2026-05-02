"""
Summary.

    Commons Module -- Common Functionality

"""
import os
import sys
import json
import inspect
import logging
import platform
import subprocess
from pathlib import Path
from spotlib._version import __version__


logger = logging.getLogger(__version__)
logger.setLevel(logging.INFO)


def get_os(detailed=False):
    """
    Summary:
        Retrieve local operating system environment characteristics
    Args:
        :user (str): USERNAME, only required when run on windows os
    Returns:
        TYPE: dict object containing key, value pairs describing
        os information
    """
    try:

        os_type = platform.system()

        if os_type == 'Linux':
            os_detail = platform.platform()
            HOME = str(Path.home())
            username = os.getenv('USER')
        elif os_type == 'Windows':
            os_detail = platform.platform()
            username = os.getenv('username') or os.getenv('USER')
            HOME = 'C:\\Users\\' + username
        else:
            logger.warning('Unsupported OS. No information')
            os_type = 'Java'
            os_detail = 'unknown'
            HOME = os.getenv('HOME')
            username = os.getenv('USER')

    except OSError as e:
        raise e
    except Exception as e:
        logger.exception(
            '%s: problem determining local os environment %s' %
            (inspect.stack()[0][3], str(e))
            )
    if detailed:
        return {
                'os_type': os_type,
                'os_detail': os_detail,
                'username': username,
                'HOME': HOME
            }
    return {'os_type': os_type}


def import_file_object(filename):
    """
    Summary:
        Imports block filesystem object
    Args:
        :filename (str): block filesystem object
    Returns:
        dictionary obj (valid json file), file data object
    """
    try:
        handle = open(filename, 'r')
        file_obj = handle.read()
        dict_obj = json.loads(file_obj)

    except OSError as e:
        logger.critical(
            'import_file_object: %s error opening %s' % (str(e), str(filename))
        )
        raise e
    except ValueError:
        logger.info(
            '%s: import_file_object: %s not json. file object returned' %
            (inspect.stack()[0][3], str(filename))
        )
        return file_obj    # reg file, not valid json
    return dict_obj


def read_local_config(cfg):
    """ Parses local config file for override values

    Args:
        :local_file (str):  filename of local config file

    Returns:
        dict object of values contained in local config file
    """
    try:
        if os.path.exists(cfg):
            config = import_file_object(cfg)
            return config
        else:
            logger.warning(
                '%s: local config file (%s) not found, cannot be read' %
                (inspect.stack()[0][3], str(cfg)))
    except OSError as e:
        logger.warning(
            'import_file_object: %s error opening %s' % (str(e), str(cfg))
        )
    return {}


def os_parityPath(path):
    """
    Converts unix paths to correct windows equivalents.
    Unix native paths remain unchanged (no effect)
    """
    path = os.path.normpath(os.path.expanduser(path))
    if path.startswith('\\'):
        return 'C:' + path
    return path


def user_home():
    """Returns os specific home dir for current user"""
    try:
        if platform.system() == 'Linux' or platform.system() == 'Darwin':
            # Linux or BSD Unix (Mac)
            return os.path.expanduser('~') or os.environ.get('HOME')

        elif platform.system() == 'Windows':
            username = os.getenv('username')
            return 'C:\\Users\\' + username

        elif platform.system() == 'Java':
            print('Unable to determine home dir, unsupported os type')
            sys.exit(1)
    except OSError as e:
        raise e
