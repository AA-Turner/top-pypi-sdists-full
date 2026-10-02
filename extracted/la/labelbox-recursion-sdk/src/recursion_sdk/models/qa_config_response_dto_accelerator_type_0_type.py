from enum import StrEnum

class QaConfigResponseDtoAcceleratorType0Type(StrEnum):
    GPU = "gpu"
    TPU = "tpu"

    def __str__(self) -> str:
        return str(self.value)
