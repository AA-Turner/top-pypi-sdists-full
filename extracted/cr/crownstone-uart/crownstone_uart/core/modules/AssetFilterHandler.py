import logging
from typing import List

from crownstone_core.packets.assetFilter.FilterCommandPackets import FilterSummariesPacket, FilterSummaryPacket
from crownstone_core.packets.assetFilter.builders.AssetFilter import AssetFilter
from crownstone_core.packets.assetFilter.util import AssetFilterMasterCrc
from crownstone_core.packets.assetFilter.util.AssetFilterChunker import FilterChunker
from crownstone_core.packets.assetFilter.util.AssetFilterSyncer import AssetFilterSyncer
from crownstone_core.protocol.ControlPackets import ControlPacketsGenerator

from crownstone_uart.core.modules.ControlHandler import ControlHandler

_LOGGER = logging.getLogger(__name__)

class AssetFilterHandler:
    def __init__(self, control: ControlHandler):
        self.control = control
        pass

    async def setFilters(self, filters: List[AssetFilter], masterVersion: int = None) -> int:
        """
        Makes sure the given filters are set at the Crownstone.
        Uploads and removes filters where necessary.
        :param filters:           The asset filter to be uploaded.
        :param masterVersion:     The new master version. If None, the master version will be increased by 1.
        :return:                  The new master version.
        """
        _LOGGER.info(f"setFilters")
        summaries = await self.getFilterSummaries()
        syncer = AssetFilterSyncer(summaries, filters, masterVersion)
        if not syncer.commitRequired:
            return syncer.masterVersion

        for filterId in syncer.removeIds:
            await self.removeFilter(filterId)

        for filter in filters:
            if filter.getFilterId() in syncer.uploadIds:
                await self.uploadFilter(filter)

        await self.commitFilterChanges(syncer.masterVersion, filters)
        return syncer.masterVersion

    async def getFilterSummaries(self) -> FilterSummariesPacket:
        """
        Get a summary of the filters that are on the Crownstones.
        This can be used to determine:
        - Which filters should be changed.
        - What the next master version should be.
        - How much space there is left for new filters.
        - The new master CRC.

        :return:   The filter summaries packet.
        """
        _LOGGER.info(f"getFilterSummaries")
        result = await self.control._writeControlAndGetResult(ControlPacketsGenerator.getGetFilterSummariesPacket())
        summaries = FilterSummariesPacket(result.payload)
        return summaries

    async def uploadFilter(self, filter: AssetFilter):
        """
        Upload an asset filter to the Crownstones.
        Once all changes are made, don't forget to commit them.

        :param filter:  The asset filter to be uploaded.
        """
        _LOGGER.info(f"uploadFilter {filter}")
        chunker = FilterChunker(filter, 128)
        for i in range(0, chunker.getAmountOfChunks()):
            chunk = chunker.getChunk()
            await self.control._writeControlAndWaitForSuccess(ControlPacketsGenerator.getUploadFilterPacket(chunk))

    async def removeFilter(self, filterId):
        """
        Remove an asset filter from the Crownstones.
        Once all changes are made, don't forget to commit them.

        :param filterId:     The filter ID to be removed.
        """
        _LOGGER.info(f"removeFilter id={filterId}")
        return await self.control._writeControlAndWaitForSuccess(ControlPacketsGenerator.getRemoveFilterPacket(filterId))

    async def commitFilterChanges(self, masterVersion: int, filters: List[AssetFilter], filterSummaries: List[FilterSummaryPacket] = None):
        """
        Commit the changes made by upload and/or remove.

        :param masterVersion:     The new master version, should be higher than previous master version.
        :param filters:           A list of asset filters with filter ID, that are uploaded to the Crowstone.
        :param filterSummaries :  A list of filter summaries that are already on the Crownstone.
        """
        _LOGGER.info(f"commitFilterChanges masterVersion={masterVersion}")
        masterCrc = AssetFilterMasterCrc.get_master_crc_from_filters(filters, filterSummaries)
        await self.control._writeControlAndWaitForSuccess(ControlPacketsGenerator.getCommitFilterChangesPacket(masterVersion, masterCrc))
