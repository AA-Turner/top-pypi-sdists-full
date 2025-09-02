import logging
import math
from enum import Enum
from typing import List

from crownstone_core import Conversion
from crownstone_core.Exceptions import CrownstoneException, CrownstoneError
from crownstone_core.util.Bitmasks import set_bit, get_bitmask
from crownstone_core.util.CRC import crc32

from crownstone_core.util.Cuckoofilter import CuckooFilter

from crownstone_core.packets.assetFilter.AssetFilterPackets import AssetFilterPacket
from crownstone_core.packets.assetFilter.ExactMatchFilter import ExactMatchFilter
from crownstone_core.packets.assetFilter.FilterOutputPackets import FilterOutputDescriptionType, FilterOutputDescription
from crownstone_core.packets.assetFilter.InputDescriptionPackets import *
from crownstone_core.packets.assetFilter.FilterMetaDataPackets import FilterType, FilterMetaData, FilterFlags
from crownstone_core.packets.assetFilter.builders.AssetIdSourceBuilder import AssetIdSourceBuilder

_LOGGER = logging.getLogger(__name__)

class OptimizeOutputStrategy(Enum):
    # No optimization.
    NONE = 0,

    # Only crownstones that believe to be nearest. Note that this is not the same as nearest only, as it takes some time to settle.
    # Experimental: may be removed or changed in a later release.
    NEAREST = 1,

class AssetFilter(BasePacket):
    def __init__(self, filterId: int = None):
        """
        Class that helps to build an asset filter packet.
        1. Choose the filter input:        filterByX()
        2. Optionally, set configurations: setX()
        3. Choose the output:              outputX()

        :param filterId:     The ID of this filter, the index at which it is placed on the Crownstones.
        """
        self._filterId = filterId
        self._filterType: FilterType = None
        self._input: InputDescriptionPacket = None
        self._outputType: FilterOutputDescriptionType = None
        self._assetIdSourceBuilder: AssetIdSourceBuilder = None
        self._assets = []
        self._profileId = 255
        self._exclude = False
        self._maxFilterSize = 512

        # Cache
        self._packet: AssetFilterPacket = None
        self._crc = None

    def getCrc(self) -> int:
        self._buildIfNeeded()
        return self._crc

    def getFilterId(self) -> int:
        return self._filterId


    def filterByMacAddress(self, macAddresses: List[str]):
        """
        Assets are filtered by their MAC address.
        :param macAddresses: List of mac addresses to be added to the filter, in the form of "12:34:56:78:AB:CD".
        """
        self._resetCache()
        self._input = InputDescriptionMacAddress()
        self._assets = []
        for mac in macAddresses:
            self._assets.append(Conversion.address_to_uint8_array(mac))
        return self

    def filterByName(self, names: List[str], complete: bool = True):
        """
        Assets are filtered by their name (case sensitive).
        :param names:     List of names to be added filter.
        :param complete:  Whether to look for the complete or shortened name.
        """
        self._resetCache()
        adType = 0x09 if complete else 0x08
        self._input = InputDescriptionFullAdData(adType)

        self._assets = []
        for name in names:
            self._assets.append(Conversion.string_to_uint8_array(name))
        return self

    def filterByNameWithWildcards(self, name: str, complete: bool = True):
        """
        Assets are filtered by their name (case sensitive).
        :param name:      Name, with wildcards, to be added filter.
                          '?' matches any single character
                          '*' matches zero or more characters, only at the end of a name.
                          Example: "??_dev*" will match:  "my_dev", and "01_device"
                                             won't match: "your_device", or "_dev"
        :param complete:  Whether to look for the complete or shortened name.
        """
        self._resetCache()
        if len(name) > 31:
            raise CrownstoneException(CrownstoneError.INVALID_SIZE, f"Name is too long: {name}")
        bitmask = 0
        asset_name = ""
        for i in range(0, len(name)):
            if name[i] != '?':
                bitmask = set_bit(bitmask, i)
                asset_name += name[i]
        if name[-1] == '*':
            bitmask = set_bit(bitmask, len(name) - 1, False)
            asset_name = asset_name[:-1]
        else:
            # Set all remaining bits. If there is more data, it will be used as input.
            for i in range(len(name), 32):
                bitmask = set_bit(bitmask, i)

        _LOGGER.info(f"name={name} bitmask={bitmask:032b} asset_name={asset_name}")

        adType = 0x09 if complete else 0x08
        self._input = InputDescriptionMaskedAdData(adType, bitmask)
        self._assets = [Conversion.string_to_uint8_array(asset_name)]
        return self

    def filterByCompanyId(self, companyIds: List[int]):
        """
        Assets are filtered by their 16 bit company ID.
        :param companyIds: A list of 16 bit company IDs. As can be found on
                           https://www.bluetooth.com/specifications/assigned-numbers/company-identifiers/
        """
        self._resetCache()
        self._input = InputDescriptionMaskedAdData(0xFF, get_bitmask([0, 1]))
        self._assets = []
        for companyId in companyIds:
            self._assets.append(Conversion.uint16_to_uint8_array(companyId))
        return self

    def filterByAdData(self, adType: int, assets: List[list], bitmask: int = None):
        """
        Assets are recognized by the data of a single AD structure in a BLE advertisement.
        :param adType:  The 8 bit GAP number.
                        See "Generic Access Profile" on https://www.bluetooth.com/specifications/assigned-numbers/
        :param assets:  A list of assets, where each asset is represented by a list of bytes.
        :param bitmask: A 32 bits mask where the Nth bit represents the Nth byte in the AD data.
                        The data that is used as input for the filter, is a concatenation of all bytes that have their
                        associated bit set.
                        Example: if the AD data is: [10, 11, 12, 13, 14] and the bitmask is 22 (0000...00010110), then
                        the data that the filter uses is [11, 12, 14], and matched against each given asset.
        """
        self._resetCache()
        if bitmask is None:
            self._input = InputDescriptionFullAdData(adType)
        else:
            self._input = InputDescriptionMaskedAdData(adType, bitmask)
        self._assets = assets
        return self


    def setFilterId(self, filterId: int):
        """
        Set the ID of this filter, the index at which it is placed on the Crownstones.

        :param filterId:     The ID of this filter.
        """
        self._resetCache()
        self._filterId = filterId
        return self

    def setFilterType(self, filterType: FilterType):
        """
        Set the filter type.

        Each filter type has its pros and cons:
        - Cuckoo: stores a list of 2 bytes hashes of the asset data. This means there can be false positives.
            Use this type when:
                - You have many asset entries, each more than 2B of data.
                - You have asset entries of varying length.
            Examples:
                - 50 MAC addresses.
                - 10 names of different length.
        - Exact match: stores a list of the whole asset data. It only accepts same length entries, and does not compress the data.
            Use this type when:
                - You have a few assets to add.
                - You do not want any false positives.
            Examples:
                - 10 MAC addresses.
                - A list of company IDs.
                - A name.
        """
        self._resetCache()
        self._filterType = filterType
        return self

    def setExclude(self, exclude=True):
        """
        Make this an exclude filter.

        Any asset that passes an exclude filter, will be prevented from passing any other filter.
        An exclude filter has no output, so you don't have to choose one.

        :param exclude: True to make this an exclude filter.
        """
        self._resetCache()
        self._exclude = exclude
        return self

    def setProfileId(self, profileId: int):
        """
        By setting a profile ID, any asset advertisement that passes this filter will be treated as this profile ID
        for behaviours. If the localization cannot determine which room the asset is in, it will be still be treated as
        being in the sphere.

        :param profileId:    The profile ID for behaviour. 255 for no profile ID.
        """
        self._resetCache()
        self._profileId = profileId
        return self

    def setMaxFilterSize(self, maxFilterSize):
        """
        Set the max size (in bytes) of this filter.

        This will be taken into account when choosing the filter type.
        """
        self._resetCache()
        self._maxFilterSize = maxFilterSize
        return self

    def outputMacRssiReport(self):
        """
        If an asset advertisement passes the filter, the Crownstone will send a report to the hub with the assets' MAC address and the RSSI.
        """
        self._resetCache()
        self._outputType = FilterOutputDescriptionType.MAC_ADDRESS
        self._assetIdSourceBuilder = None
        return self

    def outputAssetId(self, basedOn: AssetIdSourceBuilder = None, optimizeStrategy: OptimizeOutputStrategy = OptimizeOutputStrategy.NONE) -> AssetIdSourceBuilder:
        """
        If an asset advertisement passes the filter, the Crownstones will attempt to localize it, and will identify it
        by a 3 byte asset ID. The asset ID is a hash over data from the advertisement, which can be different data than
        what it's filtered by. Select this data with the AssetIdBuilder.

        :param basedOn: Determines what data to base the short asset ID on.
        :param optimizeStrategy: Strategy to optimize number of mesh messages. Experimental, may be removed or changed in a later release.
        """
        self._resetCache()
        if optimizeStrategy == OptimizeOutputStrategy.NEAREST:
            self._outputType = FilterOutputDescriptionType.ASSET_ID_NEAREST_CROWNSTONE
        else:
            self._outputType = FilterOutputDescriptionType.ASSET_ID

        if basedOn is None:
            self._assetIdSourceBuilder = AssetIdSourceBuilder()
        else:
            self._assetIdSourceBuilder = basedOn
        return self._assetIdSourceBuilder

    def outputNone(self):
        """
        If an asset advertisement passes the filter, the Crownstone will only update its local presence information. No mesh traffic is generated.
        """
        self._resetCache()
        self._outputType = FilterOutputDescriptionType.NONE
        self._assetIdSourceBuilder = None
        return self


    def build(self) -> AssetFilterPacket:
        # Check variables
        if self._filterId is None:
            raise CrownstoneException(CrownstoneError.DATA_MISSING, f"No filter ID set.")
        if self._input is None:
            raise CrownstoneException(CrownstoneError.DATA_MISSING, f"No filter input set.")
        if (self._outputType is None) and (not self._exclude):
            raise CrownstoneException(CrownstoneError.DATA_MISSING, f"No filter output set.")

        # Determine output description
        outputType = FilterOutputDescriptionType.MAC_ADDRESS
        if self._outputType is not None:
            outputType = self._outputType

        inFormat = None
        if self._assetIdSourceBuilder is not None:
            inFormat = self._assetIdSourceBuilder.build()

        output = FilterOutputDescription(outputType, inFormat)

        # Remove duplicates.
        uniqueAssets = []
        for asset in self._assets:
            if asset not in uniqueAssets:
                uniqueAssets.append(asset)
        self._assets = uniqueAssets

        # Determine filter type to use if it hasn't been set.
        if self._filterType is None:
            equalSize = True
            assetSize = len(self._assets[0])
            totalSize = 0
            for asset in self._assets:
                if len(asset) != assetSize:
                    equalSize = False
                totalSize += len(asset)
            _LOGGER.debug(f"equalSize={equalSize} totalSize={totalSize}")

            filterOverhead = 100 # TODO: this is a very rough estimate.
            if totalSize + filterOverhead < self._maxFilterSize and equalSize:
                self._filterType = FilterType.EXACT_MATCH
            else:
                self._filterType = FilterType.CUCKOO

        # Build the meta data.
        metaData = FilterMetaData(self._filterType, self._input, output, self._profileId, FilterFlags(exclude=self._exclude))

        # Construct and fill the filter.
        if self._filterType == FilterType.EXACT_MATCH:
            filterData = ExactMatchFilter()
            for asset in self._assets:
                filterData.add(asset)
        elif self._filterType == FilterType.CUCKOO:
            # TODO: move this to cuckoo filter implementation.
            initialNestsPerBucket = 4
            requiredBucketCount = len(self._assets) / 0.95 / initialNestsPerBucket
            bucketCountLog2 = max(0, math.ceil(math.log2(requiredBucketCount)))
            bucketCount = math.pow(2, bucketCountLog2)
            nestsPerBucket = math.ceil(len(self._assets) / bucketCount)

            cuckooFilter = CuckooFilter(bucketCountLog2, nestsPerBucket)
            for asset in self._assets:
                if not cuckooFilter.add(asset):
                    raise CrownstoneException(CrownstoneError.INVALID_SIZE, "Failed to add asset to cuckoo filter.")
            filterData = cuckooFilter.getData()
        else:
            raise CrownstoneException(CrownstoneError.UNKNOWN_TYPE, f"Unknown filter type: {self._filterType}")

        self._packet = AssetFilterPacket(metaData, filterData)
        self._crc = crc32(self.serialize())
        return self._packet

    def _resetCache(self):
        if self._packet is not None:
            _LOGGER.debug("Removing cache")
            self._packet = None
            self._crc = None

    def _buildIfNeeded(self):
        if self._packet is None:
            self.build()

    def _serialize(self, writer: BufferWriter):
        self._buildIfNeeded()
        self._packet.serialize(writer)

    def __str__(self):
        self._buildIfNeeded()
        return f"AssetFilter(filterId={self._filterId} packet={self._packet})"
