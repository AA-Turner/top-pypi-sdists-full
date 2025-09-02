from crownstone_core.packets.serviceDataParsers.containers.elements.AdvTypes import AdvType


class AdvAlternativeState:
    def __init__(self):
        self.type = AdvType.ALTERNATIVE_STATE

        self.crownstoneId             = None
        self.switchState              = None
        self.flags                    = None
        self.behaviourMasterHash      = None
        self.assetFilterMasterVersion = None
        self.assetFilterMasterCRC     = None
        self.timestamp                = None
        self.uniqueIdentifier         = None
        self.validation               = None

    def __str__(self):
        return f"{self.type}\n"\
           f"crownstoneId              {self.crownstoneId       }\n" \
           f"switchState               {self.switchState        }\n" \
           f"flags                     \n{self.flags            }\n" \
           f"behaviourMasterHash       {self.behaviourMasterHash}\n" \
           f"assetFilterMasterVersion  {self.assetFilterMasterVersion}\n" \
           f"assetFilterMasterCRC      {self.assetFilterMasterCRC}\n" \
           f"timestamp                 {self.timestamp          }\n" \
           f"uniqueIdentifier          {self.uniqueIdentifier   }\n" \
           f"validation                {self.validation         }\n"