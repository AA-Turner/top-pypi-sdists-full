""" MCLI Versioning """
from __future__ import annotations

import logging
from typing import NamedTuple

logger = logging.getLogger(__name__)


class Version(NamedTuple):
    """ An Easier to work with Version Encapsulation"""
    major: int
    minor: int
    patch: int
    extras: str = ''

    def __lt__(self, o: object) -> bool:
        assert isinstance(o, Version)
        if self.major != o.major:
            return self.major < o.major
        if self.minor != o.minor:
            return self.minor < o.minor
        if self.patch != o.patch:
            return self.patch < o.patch
        if self.extras and not o.extras:
            return True
        if not self.extras and o.extras:
            return False

        if self.extras and o.extras:
            # alphas check
            # TODO: maybe more version semantics but for now lets only support alphas
            try:
                return int(self.extras.split('a')[1]) < int(o.extras.split('a')[1])
            # pylint: disable-next=bare-except
            except:
                return True
        return False

    def __eq__(self, o: object) -> bool:
        assert isinstance(o, Version)
        return self.major == o.major \
            and  self.minor == o.minor \
            and self.patch == o.patch \
            and self.extras == o.extras

    def __gt__(self, o: object) -> bool:
        assert isinstance(o, Version)
        return o < self

    @classmethod
    def from_string(cls, text: str) -> Version:
        """Parses a semantic version of the form X.Y.Z[a0-9*]?

        Does not use `v` prefix and only supports optional alpha version tags

        Args:
            text: The text to parse

        Returns:
            Returns a Version object
        """
        major, minor, patch = text.split('.')
        extras = ''
        if not patch.isdigit():
            if 'a' in patch:
                extras = patch[patch.index('a'):]
                patch = patch[:patch.index('a')]
        return Version(
            major=int(major),
            minor=int(minor),
            patch=int(patch),
            extras=extras,
        )

    def __str__(self) -> str:
        return f'{self.major}.{self.minor}.{self.patch}{self.extras}'

    @property
    def is_alpha(self) -> bool:
        return self.extras != ''


def get_formatted_version() -> str:
    """ Return version number as a string """
    # pylint: disable=import-outside-toplevel,cyclic-import
    from mcli.config import FeatureFlag, MCLIConfig
    from mcli.utils.utils_pypi import get_latest_alpha_package_version, get_latest_package_version

    latest_version = current_version = Version.from_string(__version__)
    conf = MCLIConfig.load_config()
    is_alpha = current_version.is_alpha or conf.feature_enabled(FeatureFlag.ALPHA_TESTER)
    version_output = ''
    try:
        if is_alpha:
            latest_version = get_latest_alpha_package_version()
        else:
            latest_version = get_latest_package_version()
    except Exception:  # pylint: disable=broad-except
        return 'Failed to fetch current version from PyPI.'

    if latest_version > current_version:
        version_output += f'Your current version is ({current_version}), and a new version ({latest_version}) ' + \
                          'is available, please upgrade with: ' + \
                          f'\033[1mpip install --upgrade mosaicml-cli=={str(latest_version).lstrip("v")}\033[0m. '
    else:
        version_output += 'Your version is up to date. MosaicML CLI (MCLI) ' + str(latest_version)

    return version_output


def print_version(**kwargs) -> None:
    """ Prints version """
    del kwargs
    print(get_formatted_version())


__version__ = '0.7.2'

v = Version.from_string(__version__)
__version_major__ = v.major
__version_minor__ = v.minor
__version_patch__ = v.patch
__version_extras__ = v.extras
