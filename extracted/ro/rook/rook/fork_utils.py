import sys
import platform
from os import environ
import inspect

PLATFORMS_WITH_FORK_SUPPORT = ('darwin', 'linux2', 'linux')
PYTHON_IMPLEMENTATION_WITH_FORK_SUPPORT = 'CPython'
# Only works with Gunicorn 0.11.2 and up
GUNICORN_ENV_VAR_NAME = 'SERVER_SOFTWARE'


def __valid_platform():
    plat = sys.platform
    return plat in PLATFORMS_WITH_FORK_SUPPORT


def __valid_implementation():
    implementation = platform.python_implementation()
    return implementation == PYTHON_IMPLEMENTATION_WITH_FORK_SUPPORT


def __is_gunicorn():
    return 'gunicorn' in environ.get(GUNICORN_ENV_VAR_NAME, '')


def __is_gunicorn_master_proc():
    if not __is_gunicorn():
        return False
    full_stack = inspect.stack(0)
    for frame in full_stack:
        # Starting a worker
        if 'gunicorn/workers/base.py' in frame[1]:
            return False
    return True


def __is_billiard_master_proc():
    try:
        billiard_process = sys.modules['billiard.process']
        return billiard_process.current_process().name == 'MainProcess'
    except KeyError:
        return False


def detect_multiprocessing():
    if not __valid_platform() or not __valid_implementation():
        return False
    is_gunicorn_master = __is_gunicorn_master_proc()
    # Billiard includes Celery
    is_billiard_master = __is_billiard_master_proc()
    return is_gunicorn_master or is_billiard_master
