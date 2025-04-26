""" Checks PyPI for version updates """

from __future__ import annotations

import sys
import textwrap
from datetime import datetime, timedelta
from typing import Optional

import requests

from mcli import config, version
from mcli.api.exceptions import MCLIException
from mcli.config import FeatureFlag, MCLIConfig

_current_version = version.Version(
    major=version.__version_major__,
    minor=version.__version_minor__,
    patch=version.__version_patch__,
    extras=version.__version_extras__,
)


def get_latest_package_version(
    package_name: str = 'mosaicml-cli',
    current_version: version.Version = _current_version,
) -> version.Version:
    """Gets the latest release version of mcli from PyPI

    Returns:
        Version tuple
    """
    try:
        r = requests.get(f'https://pypi.org/pypi/{package_name}/json', timeout=10).json()
        version_number = r.get('info', {}).get('version', None)
        return version.Version.from_string(version_number)
    except:  # pylint: disable=bare-except
        return current_version


def get_latest_alpha_package_version(
    package_name: str = 'mosaicml-cli',
    current_version: version.Version = _current_version,
) -> version.Version:
    """Gets the latest alpha version of mcli from PyPI

    Returns:
        Version tuple
    """
    try:
        r = requests.get(f'https://pypi.org/pypi/{package_name}/json', timeout=10).json()
        version_numbers = r.get('releases', {}).keys()
        all_versions = sorted([version.Version.from_string(x) for x in version_numbers], reverse=True)
        return all_versions[0]
    except:  # pylint: disable=bare-except
        return current_version


class NeedsUpdateError(MCLIException):
    """Raised if mcli requires an update
    """


def _is_check_needed(last_checked: datetime, check_frequency: float) -> bool:
    """Determine if an upgrade check is needed
    """
    time_since = (datetime.now() - last_checked).total_seconds() / (60 * 60 * 24)
    return time_since >= check_frequency


def _update_check_time(conf: MCLIConfig, check_again_in: Optional[float] = None):
    """Update the last-checked time in the config

    Arguments:
        conf: The MCLI config
        check_again_in: Optional number of minutes in which to check for updates again.
            Defaults to the update check frequency
    """
    conf.last_update_check = datetime.now()
    if check_again_in is not None:
        conf.last_update_check = conf.last_update_check - timedelta(days=config.UPDATE_CHECK_FREQUENCY_DAYS,
                                                                    minutes=-1 * check_again_in)
    conf.save_config()


def check_new_update_available(
    package_name: str = 'mosaicml-cli',
    current_version: Optional[version.Version] = None,
) -> None:
    """Check if a new mcli package is available in PyPI

    Doesn't check if:
    - User has checked recently
    - User is set as 'dev'

    Required upgrades if:
    - Behind >= 1 major version
    - Behind >= 1 minor version
    - Behind > 1 patch version
    - Behind and on an alpha release
    - An alpha tester with a new alpha version available

    Suggests upgrade if:
    - Behind 1 patch version

    Raises:
        NeedsUpdateError: Raised if the user is too far behind on updates
    """
    if current_version is None:
        # Lazy sets current_version for monkeypatched tests
        current_version = _current_version

    conf = MCLIConfig.load_config()

    # Don't check if user is on dev/local mode
    if conf.mcli_mode.is_alternate():
        return

    if conf.disable_upgrade:
        return

    # Don't check if user checked recently
    alpha_tester: bool = conf.feature_enabled(FeatureFlag.ALPHA_TESTER)
    check_frequency: float = config.UPDATE_CHECK_FREQUENCY_DAYS if not alpha_tester else 2.0 / 24.0
    if not _is_check_needed(conf.last_update_check, check_frequency):
        return

    short_package_name = 'MCLI' if package_name == 'mosaicml-cli' else package_name

    if current_version.is_alpha or alpha_tester:
        latest_version = get_latest_alpha_package_version(
            package_name=package_name,
            current_version=current_version,
        )
    else:
        latest_version = get_latest_package_version(
            package_name=package_name,
            current_version=current_version,
        )

    if current_version > latest_version:
        print(f'{short_package_name} Version up to date! Prerelease found!\n', file=sys.stderr)
        _update_check_time(conf)
        return

    if current_version == latest_version:
        _update_check_time(conf)
        return

    print(
        textwrap.dedent(f"""
        New version of {short_package_name} detected

        ------------------------------
        Local version: \t\t{current_version}
        Most recent version: \t{latest_version}
        ------------------------------

        Upgrade with:
        pip install --upgrade mosaicml-cli=={latest_version}
        """),
        file=sys.stderr,
    )
    if alpha_tester:
        print('Thanks for being an Alpha tester!', file=sys.stderr)

    version_update_required_message = textwrap.dedent(
        f"Please update your {short_package_name} version to continue using {short_package_name}")

    # On an old alpha, so update is required
    if alpha_tester and current_version.is_alpha:
        print(f'Pre-release out of date.\n{version_update_required_message}', file=sys.stderr)
        raise NeedsUpdateError

    # A new alpha is available (only alpha testers will hit this)
    if alpha_tester and latest_version.is_alpha:
        print(f'Pre-release update available.\n{version_update_required_message}', file=sys.stderr)
        raise NeedsUpdateError

    if current_version.major != latest_version.major:
        print(f'Major version out of sync.\n{version_update_required_message}', file=sys.stderr)
        raise NeedsUpdateError

    if current_version.minor != latest_version.minor:
        print(f'Minor version out of sync.\n{version_update_required_message}', file=sys.stderr)
        raise NeedsUpdateError

    if conf.internal and latest_version.patch != current_version.patch:
        _update_check_time(conf, check_again_in=120)
    else:
        _update_check_time(conf)
