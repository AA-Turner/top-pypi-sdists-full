from crownstone_core.packets.serviceDataParsers.containers.elements.AdvTypes import AdvType


class AdvErrorPacket:
    def __init__(self):
        self.type = AdvType.CROWNSTONE_ERROR

        self.crownstoneId              = None
        self.errorsBitmask             = None
        self.errorTimestamp            = None
        self.flags                     = None
        self.temperature               = None
        self.timestamp                 = None
        self.uniqueIdentifier          = None
        self.powerUsageReal            = None

    def __str__(self):
        return f"{self.type}\n"\
           f"crownstoneId:      {self.crownstoneId    }\n" \
           f"errorsBitmask:     {self.errorsBitmask   }\n" \
           f"errorTimestamp:    {self.errorTimestamp  }\n" \
           f"flags:             \n{self.flags           }\n" \
           f"temperature:       {self.temperature     }\n" \
           f"timestamp:         {self.timestamp       }\n" \
           f"uniqueIdentifier:  {self.uniqueIdentifier}\n" \
           f"powerUsageReal:    {self.powerUsageReal  }\n"
