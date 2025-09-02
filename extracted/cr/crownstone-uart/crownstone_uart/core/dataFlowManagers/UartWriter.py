import asyncio, logging, time
from typing import List

from crownstone_core.Exceptions import CrownstoneException
from crownstone_core.packets.ResultPacket import ResultPacket
from crownstone_core.protocol.BluenetTypes import ResultValue

from crownstone_uart.Constants import UART_WRITE_TIMEOUT
from crownstone_uart.core.UartEventBus import UartEventBus
from crownstone_uart.topics.SystemTopics import SystemTopics

_LOGGER = logging.getLogger(__name__)

"""
This class will handle the event flow around writing to uart and receiving errors or result codes.

Usage of code duplication is because asyncio is difficult when obtaining event loops. You cant get one if you're already in async method, etc.
To avoid this annoying behaviour, we duplicate the code a bit.
"""
class UartWriter:
    def __init__(self, dataToSend: List[int], interval = 0.001):
        """
        This class will handle the event flow around writing to uart and receiving errors or result codes.
        :param dataToSend: This is your data packet
        :param interval: Polling interval. Don't touch. This is cheap and local only. It does not do uart things.
        """
        self.dataToSend : List[int] = dataToSend
        self.interval = interval

        self.error   = None
        self.success = False
        self.result  = None

        self.cleanupIds = []
        self.cleanupIds.append(UartEventBus.subscribe(SystemTopics.resultPacket,     self._handleResult))
        self.cleanupIds.append(UartEventBus.subscribe(SystemTopics.uartWriteSuccess, self._handleSuccess))
        self.cleanupIds.append(UartEventBus.subscribe(SystemTopics.uartWriteError,   self._handleError))

    def __del__(self):
        for cleanupId in self.cleanupIds:
            UartEventBus.unsubscribe(cleanupId)

    def _handleError(self, errorData):
        _LOGGER.error("Error during uart write", errorData)
        self.error = errorData
        raise errorData["error"]

    def _handleResult(self, data: ResultPacket):
        self.result = data
        _LOGGER.debug("Uart result packet received")

    def _handleSuccess(self, data: List[int]):
        if data == self.dataToSend:
            _LOGGER.debug("Uart write successful")
            self.success = True

    async def write_with_result(self, success_codes=None, result_timeout=1) -> ResultPacket:
        """
        write_with_result will take the data packet you have provided to the constructor and send it over UART.
        It will wait for an incoming result packet and return it once it has been received.

        You can optionally provide a list of ResultValue result codes. If the list is empty [] all resultPackets will be returned.
        Otherwise it will use your provided list to filter on. If you leave it None, we will default to ResultValue.SUCCESS.

        If a resultcode is not in the list, an CrownstoneException will be raised. You can await the result. If the write fails, an CrownstoneException will be raised.

        :param success_codes: List[ResultValue]
        :param result_timeout: time to wait on a result in seconds before raising a timeout CrownstoneException. This should be higher than the UART_WRITE_TIMEOUT
        :return: ResultPacket
        """

        if success_codes is None:
            success_codes = [ResultValue.SUCCESS]
        UartEventBus.emit(SystemTopics.uartWriteData, self.dataToSend)
        counter = 0
        while counter < result_timeout:
            if self.result:
                return self._checkResult(success_codes)

            await asyncio.sleep(self.interval)
            counter += self.interval

        self._wrapUpFailedResult(result_timeout)

    def write_with_result_sync(self, success_codes : List[ResultValue]=None, result_timeout=0.25) -> ResultPacket:
        """
        write_with_result_sync will take the data packet you have provided to the constructor and send it over UART.
        It will wait for an incoming result packet and return it once it has been received.

        You can optionally provide a list of ResultValue result codes. If the list is empty [] all resultPackets will be returned.
        Otherwise it will use your provided list to filter on. If you leave it None, we will default to ResultValue.SUCCESS.

        If a resultcode is not in the list, an CrownstoneException will be raised. This method is blocking.
        If the write fails, an CrownstoneException will be raised.
        :return:

        :param success_codes: List[ResultValue]
        :param result_timeout: time to wait on a result in seconds before raising a timeout error. This should be higher than the UART_WRITE_TIMEOUT
        :return: ResultPacket
        """
        if success_codes is None:
            success_codes = [ResultValue.SUCCESS]
        UartEventBus.emit(SystemTopics.uartWriteData, self.dataToSend)
        counter = 0
        while counter < result_timeout:
            if self.result:
                return self._checkResult(success_codes)

            time.sleep(self.interval)
            counter += self.interval

        self._wrapUpFailedResult(result_timeout)

    async def write(self) -> True:
        """
        write will take the data packet you have provided to the constructor and send it over UART.
        You can await the success of the write. If the write fails, an CrownstoneException will be raised.
        :return:
        """

        UartEventBus.emit(SystemTopics.uartWriteData, self.dataToSend)
        counter = 0
        while counter < 2*UART_WRITE_TIMEOUT:
            if self.success:
                # cleanup the listener(s)
                self.__del__()
                return True

            await asyncio.sleep(self.interval)
            counter += self.interval


        self._wrapUpFailedWrite()
    
    def write_sync(self) -> True:
        """
        write_sync will take the data packet you have provided to the constructor and send it over UART.
        This method is blocking. If the write fails, an CrownstoneException will be raised.
        :return:
        """

        UartEventBus.emit(SystemTopics.uartWriteData, self.dataToSend)
        counter = 0
        while counter < 2 * UART_WRITE_TIMEOUT:
            if self.success:
                # cleanup the listener(s)
                self.__del__()
                return True

            time.sleep(self.interval)
            counter += self.interval
        self._wrapUpFailedWrite()



    def _checkResult(self, success_codes):
        if success_codes == [] or self.result.resultCode in success_codes:
            self.__del__()
            return self.result
        else:
            # TODO: Invalid error type.
            raise CrownstoneException(
                "WRITE_EXCEPTION",
                "Incorrect result type. Got " + str(self.result.resultCode) + ", expected one of " + str(success_codes),
                400
            )


    def _wrapUpFailedResult(self, wait_until_result):
        self.__del__()
        # TODO: Invalid error type.
        raise CrownstoneException("WRITE_EXCEPTION", "No result received after writing to UART. Waited for " + str(
            wait_until_result) + " seconds", 404)


    def _wrapUpFailedWrite(self):
        # we should never arrive here. If the write went wrong, an error should have been thrown by the write method before we get here.
        self.__del__()
        # TODO: Invalid error type.
        raise CrownstoneException("WRITE_EXCEPTION", "Write not completed, but no error was thrown.", 500)
