from typing import NamedTuple

from fyuneru.lib import NonSerializable


class ImportItem(NamedTuple):
    info: any
    preData: list | NonSerializable


class CameraConfigV3(NamedTuple):
    name: str
    extrinsic: list
    intrinsic: list
    distortion: dict | NonSerializable
    projectionModel: str | NonSerializable


class D3V3Info(NamedTuple):
    urls: list[str]
    imgUrls: list | NonSerializable
    locations: list | NonSerializable
    cameraConfigs: list[CameraConfigV3] | NonSerializable


class Location(NamedTuple):
    name: str
    urls: list[str] | NonSerializable
    posMatrix: list[float]
