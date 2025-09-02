from crownstone_core.packets.serviceDataParsers.containers.elements.AdvTypes import AdvType


class AdvCrownstoneSetupState:
    def __init__(self):
        self.type = AdvType.SETUP_STATE

        self.switchState               = None
        self.flags                     = None
        self.temperature               = None
        self.powerFactor               = None
        self.powerUsageReal            = None
        self.powerUsageApparent        = None
        self.errorsBitmask             = None
        self.uniqueIdentifier          = None

    def __str__(self):
        return f"{self.type}\n"\
           f"switchState:        {self.switchState       }\n" \
           f"flags:            \n{self.flags             }\n" \
           f"temperature:        {self.temperature       }\n" \
           f"powerFactor:        {self.powerFactor       }\n" \
           f"powerUsageReal:     {self.powerUsageReal    }\n" \
           f"powerUsageApparent: {self.powerUsageApparent}\n" \
           f"errorBitmask:       {self.errorsBitmask     }\n" \
           f"uniqueIdentifier:   {self.uniqueIdentifier  }\n"