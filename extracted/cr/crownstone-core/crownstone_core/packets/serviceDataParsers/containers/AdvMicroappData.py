from crownstone_core.packets.serviceDataParsers.containers.elements.AdvTypes import AdvType


class AdvMicroappData:
    def __init__(self):
        self.type = AdvType.MICROAPP_DATA

        self.crownstoneId     = None
        self.microappUuid     = None
        self.microappData     = None
        self.flags            = None
        self.uniqueIdentifier = None
        self.validation       = None

    def __str__(self):
        return f"{self.type}\n"\
           f"crownstoneId     {self.crownstoneId    }\n" \
           f"microappUuid     {self.microappUuid    }\n" \
           f"microappData     {self.microappData    }\n" \
           f"flags            {self.flags           }\n" \
           f"uniqueIdentifier {self.uniqueIdentifier}\n" \
           f"validation       {self.validation      }\n"
