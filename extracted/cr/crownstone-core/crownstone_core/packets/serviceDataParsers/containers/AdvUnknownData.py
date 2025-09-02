from crownstone_core.packets.serviceDataParsers.containers.elements.AdvTypes import AdvType


class AdvUnknownData:
    def __init__(self):
        self.type = AdvType.UNKNOWN_DATA
        self.data       = None

    def __str__(self):
        return f"{self.type}\n"\
           f"data:       {self.data       }\n"
