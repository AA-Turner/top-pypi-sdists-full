from typing import List

from crownstone_core.Exceptions import CrownstoneException, CrownstoneError
from crownstone_core.packets.assetFilter.FilterCommandPackets import FilterSummaryPacket
from crownstone_core.packets.assetFilter.builders.AssetFilter import AssetFilter
from crownstone_core.util.BufferWriter import BufferWriter
from crownstone_core.util.CRC import crc32

def get_master_crc_from_filters(filters: List[AssetFilter], filterSummaries: List[FilterSummaryPacket] = None) -> int:
    """
    Get the master CRC from a list of filters.

    :param filters:          A list of asset filters with filter ID, that are uploaded to the Crowstone.
    :param filterSummaries:  A list of filter summaries that are already on the Crownstone.
    :returns:                The master CRC.
    """
    input_data = []
    for assetFilter in filters:
        filterId = assetFilter.getFilterId()
        crc = assetFilter.getCrc()
        input_data.append([filterId, crc])

    if filterSummaries is None:
        filterSummaries = []

    for filterSummary in filterSummaries:
        filterId = filterSummary.id
        crc = filterSummary.crc
        input_data.append([filterId, crc])

    return get_master_crc_from_filter_crcs(input_data)

def get_master_crc_from_filter_crcs(input_data : [[int, int]]) -> int:
    """
    Get the master CRC from filter CRCs.

    :param input_data:  A list of [filterId, filterCRC].
    :returns:           The master CRC.
    """
    def sort_method(val):
        return val[0]

    input_data.sort(key=sort_method)

    # Check for duplicate filter IDs.
    for i in range(0, len(input_data) - 1):
        if input_data[i][0] == input_data[i+1][0]:
            raise CrownstoneException(CrownstoneError.INVALID_INPUT, "Cannot have 2 filters with the same ID.")

    writer = BufferWriter()
    for id_and_filter_crc in input_data:
        writer.putUInt8(id_and_filter_crc[0])
        writer.putUInt32(id_and_filter_crc[1])

    return crc32(writer.getBuffer())
