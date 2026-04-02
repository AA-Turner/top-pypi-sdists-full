from enum import Enum


class DiskFormatEnum(str, Enum):
    AKI = "aki"
    AMI = "ami"
    ARI = "ari"
    ISO = "iso"
    QCOW2 = "qcow2"
    RAW = "raw"
    VDI = "vdi"
    VHD = "vhd"
    VMDK = "vmdk"

    def __str__(self) -> str:
        return str(self.value)
