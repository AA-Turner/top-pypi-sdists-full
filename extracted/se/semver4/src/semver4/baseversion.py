from __future__ import annotations
import re
import operator
from typing import Union, SupportsInt, Optional
from semver4.errors import (
    InvalidVersionPartError,
    InvalidVersionError,
    NotComparableError,
    DecreaseVersionError
)


class BaseVersion:

    _version_core_parts = []
    _valid_version_core_regex = None
    _valid_prerelease_regex = '(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*)'
    _valid_build_regex = '(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*)'

    @classmethod
    def json_encode_function(cls, obj):
        if isinstance(obj, cls):
            return obj.version
        raise TypeError(f'Object {obj.__class__} is not json serialisable')

    @classmethod
    def json_decode_function(cls, dct):
        return {k: cls(v) if isinstance(v, str) and cls.validate(v) else v for k, v in dct.items()}

    json_enc = json_encode_function
    json_dec = json_decode_function

    @classmethod
    def get_valid_version_regex(cls):
        return f'^{cls._valid_version_core_regex}(?:-{cls._valid_prerelease_regex})?(?:\+{cls._valid_build_regex})?$'

    @classmethod
    def validate(cls, version, raise_err=False):
        if re.fullmatch(cls.get_valid_version_regex(), version) is None:
            if raise_err:
                raise InvalidVersionError(f'Format of version ({version}) does not match x.y.z.f-prerelease+buildmetadata')
            return False
        return True

    def __init__(
        self,
        version: Union[str, BaseVersion] = None,
        major: Union[str, SupportsInt] = None,
        minor: Union[str, SupportsInt] = None,
        patch: Union[str, SupportsInt] = None,
        fix: Optional[Union[str, SupportsInt, None]] = 0,
        prerelease: Optional[Union[str, SupportsInt]] = None,
        build: Optional[Union[str, SupportsInt]] = None,
    ):
        self._setitem_fncs = {
            'prerelease': self._set_prerelease,
            'build': self._set_build,
            'metadata': self._set_build
        }
        try:
            if version is None:
                version = self._build_version(
                    major=major, minor=minor, patch=patch, fix=fix,
                    prerelease=prerelease, build=build
                )

            if isinstance(version, BaseVersion):
                versionparts = dict(version)
            elif isinstance(version, str):
                version = self._parse_str_version(version)
                versionparts = {
                    'major': int(version['major']),
                    'minor': int(version['minor']),
                    'patch': int(version['patch']),
                    'prerelease': version['prerelease'] if version['prerelease'] else prerelease,
                    'build': version['buildmetadata'] if version['buildmetadata'] else build
                }
                if fix is not None:
                    versionparts['fix'] = int(version['fix']) if version['fix'] else fix
            else:
                raise InvalidVersionError(f'version must be of type str or Version but is "{type(version)}"')
        except (InvalidVersionPartError, InvalidVersionError) as err:
            raise err
        else:
            self._versionparts = versionparts

    @property
    def core(self) -> str:
        return '.'.join([str(self._versionparts[p]) for p in self._version_core_parts if self._versionparts[p] or p != 'fix'])

    @property
    def major(self) -> int:
        return self._versionparts['major']

    @property
    def minor(self) -> int:
        return self._versionparts['minor']

    @property
    def patch(self) -> int:
        return self._versionparts['patch']

    @property
    def fix(self) -> int:
        return self._versionparts['fix']

    @property
    def prerelease(self) -> int:
        return self._versionparts['prerelease']

    @prerelease.setter
    def prerelease(self, value):
        self._set_prerelease(value)

    @property
    def build(self) -> int:
        return self._versionparts['build']

    @build.setter
    def build(self, value):
        self._set_build(value)

    @property
    def metadata(self) -> int:
        return self._versionparts['build']

    @metadata.setter
    def metadata(self, value):
        self._set_build(value)

    @property
    def version(self) -> str:
        return self._build_version(**self._versionparts)

    def _set_prerelease(self, value):
        self._validate_versionpart(self._valid_prerelease_regex, value)
        self._versionparts['prerelease'] = value

    def _set_build(self, value):
        self._validate_versionpart(self._valid_build_regex, value)
        self._versionparts['build'] = value

    def _validate_versionpart(self, regex: str, value: str) -> bool:
        if re.fullmatch(regex, value) is None:
            raise InvalidVersionPartError(f'Invalid value of version part: ({value})')

    def _inc_dec_version_part(self, part: str, op: 'operator') -> BaseVersion:
        for p in self._version_core_parts:
            if p > part:
                self._versionparts[p] = 0
        self._versionparts[part] = op(self._versionparts[part], 1)
        self._versionparts['prerelease'] = None
        self._versionparts['build'] = None
        return self

    def inc(self, part: str) -> BaseVersion:
        return self._inc_dec_version_part(part, operator.add)

    def dec(self, part: str) -> BaseVersion:
        if self[part] == 0:
            raise DecreaseVersionError(f'Can not decrease {part} version. It is already 0')
        return self._inc_dec_version_part(part, operator.sub)

    def inc_major(self) -> BaseVersion:
        return self.inc('major')

    def inc_minor(self) -> BaseVersion:
        return self.inc('minor')

    def inc_patch(self) -> BaseVersion:
        return self.inc('patch')

    def inc_fix(self) -> BaseVersion:
        return self.inc('fix')

    def dec_major(self) -> BaseVersion:
        return self.dec('major')

    def dec_minor(self) -> BaseVersion:
        return self.dec('minor')

    def dec_patch(self) -> BaseVersion:
        return self.dec('patch')

    def dec_fix(self) -> BaseVersion:
        return self.dec('fix')

    def _parse_str_version(self, version: str) -> re.Match[str] | None:
        if (matched := re.fullmatch(self.get_valid_version_regex(), version)) is None:
            raise InvalidVersionError(f'Format of version ({version}) does not match x.y.z.f-prerelease+buildmetadata')
        return matched

    def _compare(self, obj: BaseVersion, op: 'operator', can_equal: bool) -> bool:
        if isinstance(obj, str) and self.validate(obj):
            obj = self.__class__(obj)
        elif not isinstance(obj, BaseVersion):
            raise NotComparableError(f'Can not compare Version type and {type(obj)}')
        for versionpart in self._versionparts:
            if versionpart != 'build' and self[versionpart] != obj[versionpart]:
                return op(self[versionpart], obj[versionpart])
        return can_equal

    def __str__(self):
        return self.version

    def __repr__(self):
        return str(self)

    def __iter__(self):
        for part, value in self._versionparts.items():
            yield part, value

    def __getitem__(self, key):
        return self._versionparts[key]

    def __setitem__(self, key, value):
        try:
            fnc = self._setitem_fncs[key]
        except KeyError:
            raise KeyError(f'Can not set this item - {key}')
        else:
            fnc(value)

    def __eq__(self, obj: BaseVersion) -> bool:
        return self._compare(obj, operator.eq, can_equal=True)

    def __ne__(self, obj: BaseVersion) -> bool:
        return not self.__eq__(obj)

    def __ge__(self, obj: BaseVersion) -> bool:
        return self._compare(obj, operator.gt, can_equal=True)

    def __le__(self, obj: BaseVersion) -> bool:
        return self._compare(obj, operator.lt, can_equal=True)

    def __gt__(self, obj: BaseVersion) -> bool:
        return self._compare(obj, operator.gt, can_equal=False)

    def __lt__(self, obj: BaseVersion) -> bool:
        return self._compare(obj, operator.lt, can_equal=False)
