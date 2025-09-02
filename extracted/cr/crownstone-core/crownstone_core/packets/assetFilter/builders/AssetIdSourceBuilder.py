from crownstone_core.packets.assetFilter.InputDescriptionPackets import *

class AssetIdSourceBuilder:
    def __init__(self):
        self.inFormat: InputDescriptionPacket = None

    def build(self) -> InputDescriptionPacket:
        return self.inFormat

    def basedOnMac(self):
        """
        Base an asset ID on its MAC address.
        Use this if all assets (that pass the filter) have a static, and unique MAC address.
        """
        self.inFormat = InputDescriptionMacAddress()

    def basedOnName(self, complete: bool = True):
        """
        Base an asset ID on its name.
        Use this if all assets (that pass the filter) have a static, and unique name.

        :param complete:  Whether to look for the complete or shortened name.
        """
        adType = 0x09 if complete else 0x08
        self.inFormat = InputDescriptionFullAdData(adType)

    def basedOnManufacturerData(self):
        """
        Base an asset ID on the manufacturer data.
        Use this if all assets (that pass the filter) have static, and unique manufacturer data.
        """
        self.inFormat = InputDescriptionFullAdData(0xFF)

    def basedOnAdData(self, adType: int, bitmask: int = None):
        """
        Base an asset ID on AD data.
        :param adType:  The 8 bit GAP number.
                        See "Generic Access Profile" on https://www.bluetooth.com/specifications/assigned-numbers/
        :param bitmask: A 32 bits mask where the Nth bit represents the Nth byte in the AD data.
                        The data that is used as input for the filter, is a concatenation of all bytes that have their
                        associated bit set.
                        Example: if the AD data is: [10, 11, 12, 13, 14] and the bitmask is 22 (0000...00010110), then
                        the data that the filter uses is [11, 12, 14], and matched against each given asset.
        """
        if bitmask is None:
            self.inFormat = InputDescriptionFullAdData(adType)
        else:
            self.inFormat = InputDescriptionMaskedAdData(adType, bitmask)