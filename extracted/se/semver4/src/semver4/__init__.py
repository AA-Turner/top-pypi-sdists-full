from __future__ import annotations
from typing import SupportsInt
from semver4.baseversion import BaseVersion
from semver4.errors import FixPartNotSupported


__version__ = '0.0.1-beta.8'


class Version4(BaseVersion):

    _valid_version_core_regex = '(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:\.(?P<fix>0|[1-9]\d*))?'
    _version_core_parts = ['major', 'minor', 'patch', 'fix']

    def _build_version(self, **parts):
        ma, mi, pa, fx, pre, bl = parts['major'], parts['minor'], parts['patch'], parts['fix'], parts['prerelease'], parts['build']
        return f'{ma}.{mi}.{pa}{f".{fx}" if fx else ""}{f"-{pre}" if pre else ""}{f"+{bl}" if bl else ""}'

    def _inc_dec_version_part(self, part: str, op: 'operator') -> BaseVersion:
        if part == 'fix':
            self._versionparts['fix'] = op(self._versionparts[part], 1)
            self._versionparts['prerelease'] = None
            self._versionparts['build'] = None
            return self
        self._versionparts['fix'] = 0
        return super()._inc_dec_version_part(part, op)


class SemVersion(BaseVersion):

    _valid_version_core_regex = '(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)'
    _version_core_parts = ['major', 'minor', 'patch']

    def __init__(
            self,
            version: str | BaseVersion = None,
            major: str | SupportsInt = None,
            minor: str | SupportsInt = None,
            patch: str | SupportsInt = None,
            prerelease: str | SupportsInt | None = None,
            build: str | SupportsInt | None = None
    ):
        super().__init__(version, major, minor, patch, None, prerelease, build)

    @property
    def fix(self) -> int:
        raise FixPartNotSupported('This class supports standard semantic version format 2.0')

    def _build_version(self, **parts):
        ma, mi, pa, pre, build = parts['major'], parts['minor'], parts['patch'], parts['prerelease'], parts['build']
        return f'{ma}.{mi}.{pa}{f"-{pre}" if pre else ""}{f"+{build}" if build else ""}'


Version = Version4
