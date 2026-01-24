from __future__ import annotations

import re
from typing import List, Optional, Tuple

from seeq import spy, sdk
from seeq.spy import _common
from seeq.spy._dependencies import Dependencies
from seeq.spy._errors import *
from seeq.spy._session import Session

SDK_MODULE_VERSION_REGEX = re.compile(r'^(\d+)\.(\d+)\.(\d+).*')
SPY_MODULE_VERSION_REGEX = re.compile(r'^(?:.*\.)?(\d+)\.(\d+)$')
SEEQ_SERVER_VERSION_REGEX = re.compile(r'^R?(?:\d+\.)?(\d+)\.(\d+)\.(\d+)(-v\w+)?(-[-\w]+)?')


def get_sdk_module_version_tuple() -> Tuple[int, int, int]:
    """
    Provides a tuple of (major, minor, patch) version of Seeq SDK module (as integers).

    The major version of the Seeq SDK should match the major version of the Seeq Server.
    You can retrieve the version of the Seeq Server (once you've logged in) via
    spy.utils.get_server_version_tuple().

    Use this function instead of parsing sdk.__version__.

    Returns
    -------
    Tuple of (major, minor, patch) version of Seeq SDK module (as integers).
    """
    match = SDK_MODULE_VERSION_REGEX.match(sdk.__version__ if hasattr(sdk, '__version__') else spy.__version__)
    seeq_module_major = int(match.group(1))
    seeq_module_minor = int(match.group(2))
    seeq_module_patch = int(match.group(3))
    return seeq_module_major, seeq_module_minor, seeq_module_patch


def get_spy_module_version_tuple() -> Tuple[int, int]:
    """
    Provides a tuple of (major, minor) version of Seeq SPy module (as
    integers).

    Use this function instead of parsing spy.__version__.

    Returns
    -------
    Tuple of (major, minor) version of Seeq SPy module (as integers).
    """
    match = SPY_MODULE_VERSION_REGEX.match(spy.__version__)
    spy_module_major = int(match.group(1))
    spy_module_minor = int(match.group(2))
    return spy_module_major, spy_module_minor


def get_server_version_tuple(session: Session) -> Tuple[int, int, int]:
    """
    Provides a tuple of (major, minor, patch) version of the Seeq Server the
    supplied session is connected to (as integers). If a session is not
    supplied, the default session is used.

    The major version of the Seeq SDK should match the major version of the
    Seeq Server. You can retrieve the version of the Seeq Server (once you've
    logged in) via spy.utils.get_server_version_tuple().

    Use this function instead of parsing sdk.__version__.

    Parameters
    ----------
    session : spy.Session, optional
        If supplied, the Session object used for the connection to Seeq
        Server. If not supplied, the default session is used.

    Returns
    -------
    Tuple of (major, minor, patch) version of Seeq Server (as integers).
    """
    _common.validate_argument_types([
        (session, 'session', Session)
    ])
    session = Session.validate(session)
    if session.server_version is None:
        raise SPyRuntimeError('Not logged in. You must be logged in to a Seeq Server and have a valid session in '
                              'order to execute this function.')

    match = SEEQ_SERVER_VERSION_REGEX.match(session.server_version)
    seeq_server_major = int(match.group(1))
    seeq_server_minor = int(match.group(2))
    seeq_server_patch = int(match.group(3))
    return seeq_server_major, seeq_server_minor, seeq_server_patch


def is_spy_module_version_at_least(required_major: int, required_minor: int = 0) -> bool:
    """
    Use this function to ensure that the SPy module meets a version requirement.

    Parameters
    ----------
    required_major : int
        The SPy major version that your notebook/script/application requires.

    required_minor : int, default 0
        The SPy minor version that your notebook/script/application requires.

    Returns
    -------
    True if the SPy version is equal to or greater than the version specified.
    """
    return _is_version_at_least((required_major, required_minor), get_spy_module_version_tuple())


def is_sdk_module_version_at_least(required_major: int, required_minor: int = 0, required_patch: int = 0) -> bool:
    """
    Use this function to ensure that the SDK module meets a version requirement.

    Parameters
    ----------
    required_major : int
        The SDK major version that your notebook/script/application requires.

    required_minor : int, default 0
        The SDK minor version that your notebook/script/application requires.

    required_patch : int, default 0
        The SDK patch version that your notebook/script/application requires.

    Returns
    -------
    True if the SDK version is equal to or greater than the version specified.
    """
    return _is_version_at_least((required_major, required_minor, required_patch), get_sdk_module_version_tuple())


def is_server_version_at_least(required_major: int, required_minor: int = 0, required_patch: int = 0,
                               session: Optional[Session] = None) -> bool:
    """
    Use this function to ensure that the Seeq Server meets a version requirement.

    Parameters
    ----------
    required_major : int
        The Seeq Server major version that your notebook/script/application requires.

    required_minor : int, default 0
        The Seeq Server minor version that your notebook/script/application requires.

    required_patch : int, default 0
        The Seeq Server patch version that your notebook/script/application requires.

    session : spy.Session, optional
        If supplied, the Session object used for the connection to Seeq
        Server. If not supplied, the default session is used.

    Returns
    -------
    True if the Seeq Server version is equal to or greater than the version specified.
    """
    return _is_version_at_least((required_major, required_minor, required_patch), get_server_version_tuple(session))


def _is_version_at_least(required: Tuple, actual: Tuple) -> bool:
    required = list(required)
    actual = list(actual)
    if len(required) > len(actual):
        raise ValueError(f'Cannot compare required version {required} against actual version {actual}. Too many '
                         'version parts specified in required version.')

    while len(required) > 0:
        required_version_part = required.pop(0)
        actual_version_part = actual.pop(0)
        if actual_version_part > required_version_part:
            return True
        elif actual_version_part < required_version_part:
            return False

    return True


SEEQ_SERVER_VERSION_WHERE_SPY_IS_IN_ITS_OWN_PACKAGE = 60


def validate_seeq_server_version(session, status, allow_version_mismatch=False):
    sdk_module_major, sdk_module_minor, _ = get_sdk_module_version_tuple()
    seeq_server_major, seeq_server_minor, seeq_server_patch = get_server_version_tuple(session)

    # The old versioning scheme is like 0.49.3 whereas the new scheme is like 50.1.8
    # See https://seeq.atlassian.net/wiki/spaces/SQ/pages/947225963/Seeq+Versioning+Simplification
    using_old_server_versioning_scheme = (seeq_server_major == 0)

    message = None

    if using_old_server_versioning_scheme:
        if sdk_module_major != seeq_server_major or \
                sdk_module_minor != seeq_server_minor:
            message = (f'The major/minor version of the seeq module ({sdk_module_major}.{sdk_module_minor}) '
                       f'does not match the major/minor version of the Seeq Server you are connected to '
                       f'({seeq_server_major}.{seeq_server_minor}) and is incompatible.')
    else:
        if sdk_module_major != seeq_server_major:
            message = (f'The major version of the seeq module ({sdk_module_major}) '
                       f'does not match the major version of the Seeq Server you are connected to '
                       f'({seeq_server_major}) and is incompatible.')

    if message is not None:
        message += (f'\n\nIt is recommended that you run spy.upgrade() or issue the following PIP command to '
                    f'install a compatible version of the seeq module:\n')
        message += generate_pip_upgrade_command(session, dependencies=[])

        if allow_version_mismatch or session.options.allow_version_mismatch:
            status.warn(message)
        else:
            raise SPyRuntimeError(message)

    return seeq_server_major, seeq_server_minor, seeq_server_patch


def generate_pip_upgrade_command(session: Session, version: Optional[str] = None, use_testpypi: bool = False,
                                 dependencies: Optional[List[str]] = None) -> str:
    sdk_module_major, sdk_module_minor, _ = get_sdk_module_version_tuple()
    seeq_server_major, seeq_server_minor, seeq_server_patch = get_server_version_tuple(session)
    compatible_module_folder = find_compatible_module(session)
    # The old versioning scheme is like 0.49.3 whereas the new scheme is like 50.1.8
    # See https://seeq.atlassian.net/wiki/spaces/SQ/pages/947225963/Seeq+Versioning+Simplification
    using_old_versioning_scheme = (seeq_server_major == 0)
    first_command = None
    if using_old_versioning_scheme:
        install_compatible_sdk = (sdk_module_major != seeq_server_major or sdk_module_minor != seeq_server_minor)
        compatible_sdk_version_specifier = f'{seeq_server_major}.{seeq_server_minor}.{seeq_server_patch}'
    else:
        install_compatible_sdk = (sdk_module_major != seeq_server_major)
        compatible_sdk_version_specifier = f'{seeq_server_major}.{seeq_server_minor}'
    repository_arg = ' --index-url https://test.pypi.org/simple/' if use_testpypi else ''
    dependency_arg = f'{Dependencies(dependencies)}'

    def _install_compatible_sdk():
        if not install_compatible_sdk:
            return None

        if compatible_module_folder is not None:
            return 'pip uninstall -y seeq'
        else:
            return f'pip install -U{repository_arg} seeq~={compatible_sdk_version_specifier}'

    if version is not None:
        if 'r' in version.lower():
            version = re.sub(pattern='r', repl='', string=version, flags=re.IGNORECASE)

        match = re.match(r'^(\d+)\..*', version)
        if not match:
            raise SPyValueError(f'version argument "{version}" is not a full version (e.g. 221.13 or 58.0.2.184.12)')

        version_major = int(match.group(1))
        if version_major < SEEQ_SERVER_VERSION_WHERE_SPY_IS_IN_ITS_OWN_PACKAGE:
            # We're going to the old single-package scheme, where seeq and spy are in the same package and the
            # versioning is something like 58.0.2.184.12. If the currently-installed sdk module is R60 or later, we must
            # uninstall the seeq-spy package so that, when the older seeq package (which includes spy directly) is
            # installed, pip doesn't think that seeq-spy is still installed as well.
            if sdk_module_major >= SEEQ_SERVER_VERSION_WHERE_SPY_IS_IN_ITS_OWN_PACKAGE:
                first_command = 'pip uninstall -y seeq-spy'

            second_command = f'pip install -U{repository_arg} seeq=={version}'
        else:
            # We're going to the new seeq-spy package scheme.
            if seeq_server_major < SEEQ_SERVER_VERSION_WHERE_SPY_IS_IN_ITS_OWN_PACKAGE:
                raise SPyValueError(f'version argument "{version}" is incompatible with Seeq Server version '
                                    f'{session.server_version}')

            first_command = _install_compatible_sdk()
            second_command = f'pip install -U{repository_arg} seeq-spy{dependency_arg}=={version}'
    else:
        if seeq_server_major >= SEEQ_SERVER_VERSION_WHERE_SPY_IS_IN_ITS_OWN_PACKAGE:
            first_command = _install_compatible_sdk()
            second_command = f'pip install -U{repository_arg} seeq-spy{dependency_arg}'
        else:
            if sdk_module_major >= SEEQ_SERVER_VERSION_WHERE_SPY_IS_IN_ITS_OWN_PACKAGE:
                first_command = 'pip uninstall -y seeq-spy'
            second_command = f'pip install -U{repository_arg} seeq~={compatible_sdk_version_specifier}'
    pip_commands = [second_command] if first_command is None else [first_command, second_command]
    pip_command = ' && '.join(pip_commands)
    return pip_command


def find_compatible_module(session: Session):
    """
    Look for a seeq module that is compatible with the version of Seeq Server we're connected to.
    This function is useful in Seeq Data Lab scenarios where the user has installed a "private" version of
    the seeq module (presumably to get a bugfix for SPy) but Seeq Server and Seeq Data Lab have been upgraded in the
    meantime and the user's best course of action is to remove the private version and resume using the "built-in"
    version, which will update with Seeq Data Lab as it is upgraded.
    :return: Path to a compatible module, None if a compatible module is not found.
    """
    seeq_module_major, seeq_module_minor, _ = get_sdk_module_version_tuple()
    seeq_server_major, seeq_server_minor, seeq_server_patch = get_server_version_tuple(session)
    try:
        # Check all installed 'seeq' distributions to find a version-compatible one
        from importlib.metadata import distributions
        for dist in distributions():
            # Use normalized name comparison for safety across Python versions
            if 'Name' in dist.metadata and dist.metadata['Name'].lower() == 'seeq':
                dist_version = dist.version
                if seeq_server_major >= 50 and dist_version.startswith(f'{seeq_server_major}.'):
                    return str(dist.locate_file(''))
                elif seeq_server_major < 50 and dist_version.startswith(f'{seeq_server_major}.{seeq_server_minor}.'):
                    return str(dist.locate_file(''))
    except (ImportError, AttributeError, KeyError):
        pass

    return None
