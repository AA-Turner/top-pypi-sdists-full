import logging
from typing import List

from crownstone_core.packets.assetFilter.util import AssetFilterMasterCrc

from crownstone_core.packets.assetFilter.FilterCommandPackets import FilterSummariesPacket
from crownstone_core.packets.assetFilter.builders.AssetFilter import AssetFilter

_LOGGER = logging.getLogger(__name__)

class AssetFilterSyncer:
    def __init__(self, summaries: FilterSummariesPacket, filters: List[AssetFilter], masterVersion: int = None):
        """
        Helper class to upload given filters, and remove other filters, and determines if a commit is required at all.

        After construction, read out the class variables.

        :param summaries:         The filter summaries packet of the Crownstone.
        :param filters:           The filters to be set at the Crownstone.
        :param masterVersion:     The new master version. If None, the master version will be increased by 1.
        """
        self.commitRequired = False
        self.removeIds = []
        self.uploadIds = []
        self.masterVersion = 0

        # Checks for duplicate IDs.
        masterCrc = AssetFilterMasterCrc.get_master_crc_from_filters(filters)

        # Iterate over the filters on the Crownstone, to see if there are abundant IDs, or filter CRC mismatches.
        for summary in summaries.summaries:
            foundId = False
            for filter in filters:
                if filter.getFilterId() == summary.id:
                    foundId = True
                    if filter.getCrc() != summary.crc:
                        _LOGGER.info(f"CRC mismatch, upload filderId={summary.id}")
                        self.uploadIds.append(summary.id)
                    else:
                        _LOGGER.info(f"CRC match, skip filderId={summary.id}")
            if not foundId:
                _LOGGER.info(f"Not found, remove filderId={summary.id}")
                self.removeIds.append(summary.id)

        # Iterate over given filters, to see if there are IDs that are not on the Crownstone.
        for filter in filters:
            foundId = False
            for summary in summaries.summaries:
                if filter.getFilterId() == summary.id:
                    foundId = True
            if not foundId:
                _LOGGER.info(f"Not found, upload filderId={filter.getFilterId()}")
                self.uploadIds.append(filter.getFilterId())

        # Only increase master version if there are any changes.
        if len(self.removeIds) == 0 \
                and len(self.uploadIds) == 0 \
                and masterCrc == summaries.masterCrc \
                and (masterVersion is None or summaries.masterVersion == masterVersion):
            _LOGGER.info("No changes, no commit requried.")
            self.commitRequired = False
            self.masterVersion = summaries.masterVersion
            return

        if masterVersion is None:
            self.masterVersion = summaries.masterVersion + 1
        else:
            self.masterVersion = masterVersion
        self.commitRequired = True