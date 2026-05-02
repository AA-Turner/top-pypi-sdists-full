import typing

from ..visualization_table import SHVProjectTypeDict
from ..visualization_table import SHVVarDict  # noqa: F401


class HWModuleDict(typing.TypedDict):
    type: str
    cabinet: str | None
    name_suffix: str


class HWIsleDict(typing.TypedDict):
    head: HWModuleDict
    tail: list[HWModuleDict]


class SWDeviceConfigDict(typing.TypedDict):
    config: dict[str, typing.Any]
    function: str
    connector: dict[str, str | typing.Any]
    devType: str
    iomap: typing.NotRequired[dict[str, str]]


class SWDeviceVisuDict(typing.TypedDict):
    SHVDeviceType: str
    SHVDeviceTypeVariant: typing.NotRequired[str]


class SWDeviceDict(typing.TypedDict):
    general: dict[str, typing.Any]
    control: SWDeviceConfigDict
    test: SWDeviceConfigDict
    visu: SWDeviceVisuDict
    children: dict[str, 'SWModuleDict']


SWModuleDict: typing.TypeAlias = dict[str, SWDeviceDict]
SWZoneDict: typing.TypeAlias = dict[str, SWModuleDict]
SWSystemDict: typing.TypeAlias = dict[str, SWZoneDict]


class SystemDict(typing.TypedDict):
    Hardware: list[HWIsleDict]
    Software: SWSystemDict
    Visu: dict[str, SHVProjectTypeDict]
