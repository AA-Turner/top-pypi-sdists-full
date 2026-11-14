from enum import IntEnum

class GetImageWidth(IntEnum):
    VALUE_320 = 320
    VALUE_640 = 640
    VALUE_960 = 960
    VALUE_1280 = 1280

    def __str__(self) -> str:
        return str(self.value)
