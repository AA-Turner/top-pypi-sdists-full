from crownstone_core.packets.serviceDataParsers.containers.elements.AdvTypes import AdvType


class AdvExternalErrorPacket:
    def __init__(self):
        self.type = AdvType.EXTERNAL_ERROR

        self.crownstoneId              = None
        self.errorsBitmask             = None
        self.errorTimestamp            = None
        self.flags                     = None
        self.temperature               = None
        self.rssiOfExternalCrownstone  = None
        self.timestamp                 = None
        self.uniqueIdentifier          = None
        self.validation                = None

    def __str__(self):
        return f"{self.type}\n"\
           f"crownstoneId             {self.crownstoneId            }\n" \
           f"errorsBitmask            {self.errorsBitmask           }\n" \
           f"errorTimestamp           {self.errorTimestamp          }\n" \
           f"flags                    {self.flags                   }\n" \
           f"temperature              {self.temperature             }\n" \
           f"rssiOfExternalCrownstone {self.rssiOfExternalCrownstone}\n" \
           f"timestamp                {self.timestamp               }\n" \
           f"uniqueIdentifier         {self.uniqueIdentifier        }\n" \
           f"validation               {self.validation              }\n"