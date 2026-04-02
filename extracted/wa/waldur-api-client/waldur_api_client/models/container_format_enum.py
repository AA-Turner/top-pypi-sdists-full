from enum import Enum


class ContainerFormatEnum(str, Enum):
    AKI = "aki"
    AMI = "ami"
    ARI = "ari"
    BARE = "bare"
    OVF = "ovf"

    def __str__(self) -> str:
        return str(self.value)
