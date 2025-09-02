from enum import IntEnum

from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.util.BufferReader import BufferReader

BOOTLOADER_INFO_PROTOCOL = 1

class BootloaderBuildType(IntEnum):
    UNKNOWN                 = 0,
    DEBUG                   = 1,
    RELEASE                 = 2,
    RELEASE_WITH_DEBUG      = 3,
    RELEASE_MIN_SIZE        = 4,

class BootloaderInfoPacket(BasePacket):
    def __init__(self, data = None):
        self.protocol = 0
        self.dfuVersion = 0
        self.major = 0
        self.minor = 0
        self.patch = 0
        self.preReleaseVersion = 0
        self.buildType = BootloaderBuildType.UNKNOWN

        if data is not None:
            self.deserialize(data)

    def _deserialize(self, reader: BufferReader):
        self.protocol = reader.getUInt8()
        self.dfuVersion = reader.getUInt16()
        self.major = reader.getUInt8()
        self.minor = reader.getUInt8()
        self.patch = reader.getUInt8()
        self.preReleaseVersion = reader.getUInt8()
        self.buildType = BootloaderBuildType(reader.getUInt8())

    def toString(self):
        return f"BootloaderInfoPacket(" \
               f"protocol={self.protocol}, " \
               f"dfuVersion={self.dfuVersion}, " \
               f"major={self.major}, " \
               f"minor={self.minor}, " \
               f"patch={self.patch}, " \
               f"preReleaseVersion={self.preReleaseVersion}, " \
               f"buildType={self.buildType})"

    def __str__(self):
        return self.toString()
