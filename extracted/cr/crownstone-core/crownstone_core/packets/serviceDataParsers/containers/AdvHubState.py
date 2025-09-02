from crownstone_core.packets.serviceDataParsers.containers.elements.AdvTypes import AdvType


class AdvHubState:
    def __init__(self):
        self.type = AdvType.HUB_STATE

        self.crownstoneId     = None
        self.hubFlags         = None
        self.hubData          = None
        self.timestamp        = None
        self.uniqueIdentifier = None
        self.validation       = None

    def __str__(self):
        return f"{self.type}\n"\
           f"crownstoneId     {self.crownstoneId    }\n" \
           f"hubFlags         {self.hubFlags        }\n" \
           f"hubData          {self.hubData         }\n" \
           f"timestamp        {self.timestamp       }\n" \
           f"uniqueIdentifier {self.uniqueIdentifier}\n" \
           f"validation       {self.validation      }\n"
