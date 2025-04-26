"""This is the external interface to the Rook package."""
import sys
import os
import traceback
import re

import six

from rook import utils
from rook.config import ImportServiceConfig
from rook.serverless import on_lambda
from rook.fork_utils import detect_multiprocessing

_rook = None
_debug = False
_throw_errors = False

_fork = None
_original_args = None

_TRUE_VALUES = ['y', 'Y', 'yes',  'Yes',  'YES', 'true', 'True', 'TRUE', '1', True, b'True']


def start(token=None,
          tags=None,
          host=None,
          port=None,
          debug=None,
          throw_errors=None,
          log_file=None,
          log_level=None,
          log_to_stderr=None,
          labels=None,
          use_import_hook=None,
          git_commit=None,
          git_origin=None,
          proxy=None,
          fork=None,
          enable_monitor=None,
          sources=None,
          quiet=None,
          **kwargs):
    global _rook, _debug, _throw_errors, _original_args, _fork

    for k, v in os.environ.items():
        if k.startswith("ROOKOUT_") and "LABELS" not in k:
            os.environ[k] = v.strip().strip("'\"")  # First strip for whitespaces, then ' and "

    if _rook is not None:
        return

    if _original_args:
        copy_of_original_args = _original_args
        _original_args = None

        # Disable fork support on child processes
        copy_of_original_args['fork'] = False

        start(**copy_of_original_args)
        return

    # Save original args to recover from fork
    _original_args = locals()

    if isinstance(debug, bool):
        _debug = debug
    else:
        _debug = os.environ.get('ROOKOUT_DEBUG') in _TRUE_VALUES

    if not isinstance(quiet, bool):
        quiet = os.environ.get('ROOKOUT_QUIET') in _TRUE_VALUES

    dev_debug = os.environ.get('ROOKOUT_DEV_DEBUG') in _TRUE_VALUES

    if not isinstance(log_to_stderr, bool):
        log_to_stderr = os.environ.get('ROOKOUT_LOG_TO_STDERR') in _TRUE_VALUES

    if isinstance(throw_errors, bool):
        _throw_errors = throw_errors

    if not isinstance(tags, list) and isinstance(os.environ.get('ROOKOUT_ROOK_TAGS'), six.string_types):
        raw_tags = os.environ.get('ROOKOUT_ROOK_TAGS')
        tags = [_normalize_string(tag.strip(' \'"')) for tag in raw_tags.split(';') if tag]

    if not isinstance(labels, dict) and isinstance(os.environ.get('ROOKOUT_LABELS'), six.string_types):
        raw_labels = os.environ.get('ROOKOUT_LABELS')
        labels = {}
        for label in raw_labels.split(','):
            label = _normalize_string(label.strip(' \'"'))
            keyvalue = label.split(':')
            if len(keyvalue) == 2:
                key,value = keyvalue
                if key and value:
                    _validate_label(key)
                    labels[key] = value

    if on_lambda():
        log_file = ""
    log_file = log_file or os.environ.get('ROOKOUT_LOG_FILE')
    log_level = log_level or os.environ.get('ROOKOUT_LOG_LEVEL')

    from rook.config import ControllerAddress
    host_specified = host or os.environ.get('ROOKOUT_CONTROLLER_HOST') or os.environ.get('ROOKOUT_AGENT_HOST')
    host = host_specified or ControllerAddress.HOST
    port = port or os.environ.get('ROOKOUT_CONTROLLER_PORT') or os.environ.get('ROOKOUT_AGENT_PORT') or ControllerAddress.PORT
    proxy = proxy or os.environ.get('ROOKOUT_PROXY')
    token = token or os.environ.get('ROOKOUT_TOKEN')
    use_import_hook = use_import_hook if use_import_hook is not None else os.environ.get('ROOKOUT_USE_IMPORT_HOOK',
                                                                                         True) in _TRUE_VALUES
    async_start = os.environ.get('ROOKOUT_ASYNC_START', False) in _TRUE_VALUES

    if fork is None and 'ROOKOUT_ENABLE_FORK' not in os.environ:
        _fork = detect_multiprocessing()
    else:
        _fork = fork or os.environ.get('ROOKOUT_ENABLE_FORK', False) in _TRUE_VALUES

    _enable_monitor = enable_monitor or os.environ.get('ROOKOUT_ENABLE_MONITOR') in _TRUE_VALUES

    detect_uwsgi()

    try:

        host = host.strip().rstrip("/'\"")
        token = token.strip().strip("'\"")
        proxy = proxy.strip().strip("'\"")
    except AttributeError:
        pass

    try:
        from rook.exceptions import RookMissingToken, RookInvalidToken, RookVersionNotSupported, \
            RookCommunicationException, RookInvalidOptions, RookLoadError, RookOldServers, \
            RookInvalidRateLimitConfiguration, RookWebSocketError
        try:
            from rook.config import LoggingConfiguration, GitConfig

            if git_commit is not None:
                if not isinstance(git_commit, six.string_types):
                    raise RookInvalidOptions('git_commit should be a String')
                GitConfig.GIT_COMMIT = git_commit

            if git_origin is not None:
                if not isinstance(git_origin, six.string_types):
                    raise RookInvalidOptions('git_origin should be a String')
                GitConfig.GIT_ORIGIN = git_origin

            if sources is not None and not isinstance(sources, dict):
                raise RookInvalidOptions('sources should be a dict')
                
            if not isinstance(sources, dict) and isinstance(os.environ.get('ROOKOUT_SOURCES'), six.string_types):
                raw_sources = os.environ.get('ROOKOUT_SOURCES')
                sources = {}
                for source in raw_sources.split(';'):
                    source = _normalize_string(source.strip(' \'"'))
                    keyvalue = source.split('#')
                    if len(keyvalue) == 2:
                        key,value = keyvalue
                        if key and value:                    
                            sources[key] = value
            if sources:                             
                GitConfig.SOURCES = sources

            if log_file is not None:
                if not isinstance(log_file, six.string_types):
                    raise RookInvalidOptions('log_file should be a String')
                LoggingConfiguration.FILE_NAME = log_file

            if log_level is not None:
                if not isinstance(log_level, six.string_types):
                    raise RookInvalidOptions('log_level should be a String')
                LoggingConfiguration.LOG_LEVEL = log_level

            if log_to_stderr is not None:
                LoggingConfiguration.LOG_TO_STDERR = log_to_stderr

            if quiet is not None:
                LoggingConfiguration.QUIET = quiet

            if dev_debug is not None:
                LoggingConfiguration.DEV_DEBUG = dev_debug

            if proxy is not None and not isinstance(proxy, six.string_types):
                raise RookInvalidOptions('proxy should be a String')

            if _debug:
                LoggingConfiguration.LOG_LEVEL = 'DEBUG'
                LoggingConfiguration.LOG_TO_STDERR = True
                LoggingConfiguration.DEBUG = True

            if use_import_hook is not None:
                ImportServiceConfig.USE_IMPORT_HOOK = use_import_hook

            if isinstance(tags, list):
                for tag in tags:
                    if not isinstance(tag, six.string_types):
                        raise RookInvalidOptions('Rook tags should be array of strings')
            else:
                if tags:
                    raise RookInvalidOptions('Rook tags should be array of strings')

            if not host_specified and not token:
                raise RookMissingToken()
            else:
                if token is not None:
                    _validate_token(token)

            if _debug:
                _print_user_configuration(token=token[:5] + "....." if token else None, host=host, port=port,
                                          proxy=proxy, throw_errors=throw_errors, log_level=log_level,
                                          log_to_stderr=log_to_stderr, log_file=log_file, git_commit=git_commit,
                                          git_origin=git_origin, tags=tags, labels=labels, async_start=async_start,
                                          use_import_hook=use_import_hook, fork=_fork, enable_monitor=_enable_monitor,
                                          sources=sources, quiet=quiet)

            if (host == "staging.cloud.agent.rookout.com") or (host == "cloud.agent.rookout.com"):
                raise RookOldServers()

            from rook.logger import logger
            from rook.config import VersionConfiguration
            logger.debug("Rookout SDK for Python, Version:" + VersionConfiguration.VERSION + " Commit:" + VersionConfiguration.COMMIT)

            import rook.singleton
            _rook = rook.singleton.singleton_obj

            _rook.connect(token, host, port, proxy, tags, labels, async_start, _fork, _debug, _enable_monitor, _throw_errors)
        except (RookMissingToken, RookInvalidToken, RookVersionNotSupported, RookOldServers,
                RookInvalidRateLimitConfiguration, RookWebSocketError) as e:
            if not _throw_errors:
                six.print_("[Rookout] Failed to start Rookout:", e, file=sys.stderr)
            raise
        except RookCommunicationException as e:
            if not _throw_errors:
                logger.warn("[Rookout] Failed to connect to the controller - will continue attempting in the background", e, file=sys.stderr)
            raise
        except ImportError as e:
            if not _throw_errors:
                six.print_("[Rookout] Failed to import dependencies:", e, file=sys.stderr)
            raise
        except (Exception, RookLoadError) as e:
            if not _throw_errors:
                six.print_("[Rookout] Failed initialization:", e, file=sys.stderr)
            raise
    except Exception:
        if _throw_errors:
            raise

        if _debug:
            traceback.print_exc()



def detect_uwsgi():
    try:
        import uwsgi
        from rook.logger import logger
        found_postfork = False
        if 'enable-threads' not in uwsgi.opt or uwsgi.opt['enable-threads'] not in _TRUE_VALUES:
            logger.warning("enable-threads should be set to true.\n"
                         "See: https://docs.rookout.com/docs/python-setup/#uwsgi-applications")

        import uwsgidecorators
        for hook in uwsgidecorators.postfork_chain:
            if "rook" in hook.f.__name__:
                found_postfork = True
        if not found_postfork:
            logger.debug("Couldn't find rookout in uwsgi postfork hooks.\n"
                         "See https://docs.rookout.com/docs/python-setup/#uwsgi-applications")
        else:
            logger.debug("found postfork")
    except ImportError:
        pass # Not running in uwsgi
    except Exception as e: # Not running in master mode
        if str(e) != "you have to enable the uWSGI master process to use this module":
            raise

def capture_exception(exc):
    from rook.collect import exception_collect

    exception_collect(exc)


def flush():
    global _rook
    if _rook is None:
        return

    _rook.flush()


def stop():
    global _rook
    if _rook is None:
        return

    _rook.stop()
    _rook = None


def restart(labels=None,
            tags=None):
    global _rook
    if _rook is None:
        return

    _rook.restart(tags, labels)


def _normalize_string(obj):
    if six.PY2:
        if isinstance(obj, str):
            return unicode(obj, errors="replace")
        else:
            return unicode(obj)
    else:
        return str(obj)


def _validate_token(token):
    from rook.exceptions import RookInvalidOptions

    if not isinstance(token, six.string_types):
        raise RookInvalidOptions('Rookout token should be a String')

    if len(token) != 64:
        raise RookInvalidOptions('Rookout token should be 64 characters')

    if re.match("^[0-9a-zA-Z]{0,64}$", token) is None:
        raise RookInvalidOptions('Rookout token must consist of only hexadecimal characters')


def _validate_label(label):
    from rook.exceptions import RookInvalidLabel

    if label.startswith("$"):
        raise RookInvalidLabel(label)


def _print_user_configuration(**kwargs):
    try:
        config_string = ""
        for key, value in kwargs.items():
            if value:
                config_string = config_string + ("%s: %s, " % (key, value))
        utils.quiet_print("RookOptions: " + config_string)
    except Exception:
        six.print_("Error in printing user configuration")
