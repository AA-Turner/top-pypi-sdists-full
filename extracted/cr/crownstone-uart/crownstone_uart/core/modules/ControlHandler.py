import asyncio
import logging
from typing import List

from crownstone_core.Exceptions import CrownstoneException, CrownstoneError
from crownstone_core.packets.ResultPacket import ResultPacket
from crownstone_core.packets.assetFilter.FilterCommandPackets import FilterSummaryPacket, FilterSummariesPacket
from crownstone_core.packets.assetFilter.builders.AssetFilter import AssetFilter
from crownstone_core.packets.assetFilter.util import AssetFilterMasterCrc
from crownstone_core.packets.assetFilter.util.AssetFilterChunker import FilterChunker
from crownstone_core.packets.assetFilter.util.AssetFilterSyncer import AssetFilterSyncer

from crownstone_core.protocol.BluenetTypes import ResultValue
from crownstone_core.protocol.ControlPackets import ControlPacketsGenerator
from crownstone_uart.core.UartEventBus import UartEventBus
from crownstone_uart.core.dataFlowManagers.Collector import Collector
from crownstone_uart.core.uart.UartTypes import UartTxType, UartMessageType
from crownstone_uart.core.uart.uartPackets.UartMessagePacket import UartMessagePacket
from crownstone_uart.core.uart.uartPackets.UartWrapperPacket import UartWrapperPacket
from crownstone_uart.topics.SystemTopics import SystemTopics

_LOGGER = logging.getLogger(__name__)

class ControlHandler:

    async def factoryReset(self):
        _LOGGER.info("factory reset")
        await self._writeControlAndWaitForSuccess(ControlPacketsGenerator.getCommandFactoryResetPacket())

    async def setFilters(self, filters: List[AssetFilter], masterVersion: int = None) -> int:
        """
        Makes sure the given filters are set at the Crownstone.
        Uploads and removes filters where necessary.
        :param filters:           The asset filter to be uploaded.
        :param masterVersion:     The new master version. If None, the master version will be increased by 1.
        :return:                  The new master version.
        """
        _LOGGER.info(f"setFilters")
        _LOGGER.warning("This function will move to the assetFilter.")
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
        _LOGGER.warning("This function will move to the assetFilter.")
        result = await self._write(ControlPacketsGenerator.getGetFilterSummariesPacket())
        if result is None:
            raise CrownstoneException(CrownstoneError.DATA_MISSING, "No summaries received")
        summaries = FilterSummariesPacket(result)
        return summaries

    async def uploadFilter(self, filter: AssetFilter):
        """
        Upload an asset filter to the Crownstones.
        Once all changes are made, don't forget to commit them.

        :param filter:  The asset filter to be uploaded.
        """
        _LOGGER.info(f"uploadFilter {filter}")
        _LOGGER.warning("This function will move to the assetFilter.")
        chunker = FilterChunker(filter, 128)
        result = None
        for i in range(0, chunker.getAmountOfChunks()):
            chunk = chunker.getChunk()
            result = await self._write(ControlPacketsGenerator.getUploadFilterPacket(chunk))
        return result

    async def removeFilter(self, filterId):
        """
        Remove an asset filter from the Crownstones.
        Once all changes are made, don't forget to commit them.

        :param filterId:     The filter ID to be removed.
        """
        _LOGGER.info(f"removeFilter id={filterId}")
        _LOGGER.warning("This function will move to the assetFilter.")
        return await self._write(ControlPacketsGenerator.getRemoveFilterPacket(filterId))

    async def commitFilterChanges(self, masterVersion: int, filters: List[AssetFilter], filterSummaries: List[FilterSummaryPacket] = None):
        """
        Commit the changes made by upload and/or remove.

        :param masterVersion:     The new master version, should be higher than previous master version.
        :param filters:           A list of asset filters with filter ID, that are uploaded to the Crowstone.
        :param filterSummaries :  A list of filter summaries that are already on the Crownstone.
        """
        _LOGGER.info(f"commitFilterChanges masterVersion={masterVersion}")
        _LOGGER.warning("This function will move to the assetFilter.")
        masterCrc = AssetFilterMasterCrc.get_master_crc_from_filters(filters, filterSummaries)
        return await self._write(ControlPacketsGenerator.getCommitFilterChangesPacket(masterVersion, masterCrc))


    async def _write(self, controlPacket: [int], successCodes = [ResultValue.SUCCESS, ResultValue.SUCCESS_NO_CHANGE, ResultValue.WAIT_FOR_SUCCESS]) -> [int] or None:
        """
        Returns the result payload.
        TODO: return result packet.
        TODO: use a ControlPacket as param, instead of int array.
        """
        _LOGGER.debug(f"Write control packet {controlPacket}")
        uartMessage = UartMessagePacket(UartTxType.CONTROL, controlPacket).serialize()
        uartPacket = UartWrapperPacket(UartMessageType.UART_MESSAGE, uartMessage).serialize()

        resultCollector = Collector(timeout=1, topic=SystemTopics.resultPacket)
        # send the message to the Crownstone
        UartEventBus.emit(SystemTopics.uartWriteData, uartPacket)

        # wait for the collectors to fill
        commandResultData = await resultCollector.receive()

        if commandResultData is not None:
            if commandResultData.resultCode not in successCodes:
                raise CrownstoneException(commandResultData.resultCode, f"Command has failed: result code is {commandResultData.resultCode}")
            return commandResultData.payload
        return None

    async def _writeControlAndGetResult(
            self,
            controlPacket,
            acceptedResultValues = [ResultValue.SUCCESS, ResultValue.SUCCESS_NO_CHANGE],
            timeout = None
    ) -> ResultPacket:
        """
        Writes the control packet, checks the result value, and returns the result packet.
        :param controlPacket:          Serialized control packet to write.
        :param acceptedResultValues:   List of result values that are ok.
        :param timeout:                Timeout in seconds.
        :returns:                      The result packet.
        """
        _LOGGER.debug(f"Write control packet {controlPacket}")
        uartMessage = UartMessagePacket(UartTxType.CONTROL, controlPacket).serialize()
        uartPacket = UartWrapperPacket(UartMessageType.UART_MESSAGE, uartMessage).serialize()

        if timeout is None:
            timeout = 3

        # Setup the result collector
        resultCollector = Collector(timeout=timeout, topic=SystemTopics.resultPacket)

        # Send the message to the Crownstone
        UartEventBus.emit(SystemTopics.uartWriteData, uartPacket)

        # Wait for the result
        resultPacket: ResultPacket = await resultCollector.receive()
        _LOGGER.debug(f"resultPacket={resultPacket}")

        if resultPacket is None:
            raise CrownstoneException(CrownstoneError.TIMEOUT, f"No result received within {timeout} seconds")
        if not resultPacket.valid:
            raise CrownstoneException(CrownstoneError.INCORRECT_RESPONSE_LENGTH, "Result is invalid")
        if resultPacket.resultCode not in acceptedResultValues:
            raise CrownstoneException(CrownstoneError.RESULT_NOT_SUCCESS, f"Result code is {resultPacket.resultCode}")
        return resultPacket

    async def _writeControlAndWaitForSuccess(
            self,
            controlPacket,
            timeout = 10,
            acceptedResultValues = [ResultValue.SUCCESS, ResultValue.SUCCESS_NO_CHANGE]
    ) -> ResultPacket:
        """
        Writes the control packet, and waits for success.
        :param controlPacket:          Serialized control packet to write.
        :param timeout:                Timeout in seconds.
        :param acceptedResultValues:   List of result values that are considered a success.
        :returns:                      The result packet.
        """
        _LOGGER.debug(f"Write control packet {controlPacket}")
        uartMessage = UartMessagePacket(UartTxType.CONTROL, controlPacket).serialize()
        uartPacket = UartWrapperPacket(UartMessageType.UART_MESSAGE, uartMessage).serialize()

        # Setup the result collector
        resultCollector = Collector(timeout=timeout, topic=SystemTopics.resultPacket)

        # Send the message to the Crownstone
        UartEventBus.emit(SystemTopics.uartWriteData, uartPacket)

        while True:
            # Wait for the result
            resultPacket: ResultPacket = await resultCollector.receiveNext()
            _LOGGER.debug(f"resultPacket={resultPacket}")

            if resultPacket is None:
                resultCollector._cleanup()
                raise CrownstoneException(CrownstoneError.TIMEOUT, f"No success received within {timeout} seconds")
            if resultPacket.resultCode in acceptedResultValues:
                resultCollector._cleanup()
                return resultPacket
            if not resultPacket.valid:
                resultCollector._cleanup()
                raise CrownstoneException(CrownstoneError.INCORRECT_RESPONSE_LENGTH, "Result is invalid")
            if resultPacket.resultCode == ResultValue.WAIT_FOR_SUCCESS:
                continue
            if resultPacket.resultCode not in acceptedResultValues:
                resultCollector._cleanup()
                raise CrownstoneException(CrownstoneError.RESULT_NOT_SUCCESS,
                                          f"Result code is {resultPacket.resultCode}")
            resultCollector._cleanup()
            return resultPacket
