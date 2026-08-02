import asyncio

from crownstone_core.Exceptions import CrownstoneException
from crownstone_core.protocol.BlePackets import ControlStateSetPacket
from crownstone_core.protocol.BluenetTypes import StateType, ResultValue

from crownstone_uart.core.dataFlowManagers.Collector import Collector
from crownstone_uart.core.UartEventBus import UartEventBus
from crownstone_uart.core.uart.uartPackets.UartMessagePacket import UartMessagePacket
from crownstone_uart.core.uart.UartTypes import UartTxType, UartMessageType
from crownstone_uart.core.uart.uartPackets.UartWrapperPacket import UartWrapperPacket
from crownstone_uart.topics.SystemTopics import SystemTopics


class StateHandler:

    async def setPowerZero(self, mW: int):
        controlPacket = ControlStateSetPacket(StateType.POWER_ZERO).loadInt32(mW).serialize()
        uartMessage   = UartMessagePacket(UartTxType.CONTROL, controlPacket).serialize()
        uartPacket    = UartWrapperPacket(UartMessageType.UART_MESSAGE, uartMessage).serialize()

        resultCollector = Collector(timeout=1,  topic=SystemTopics.resultPacket)
        # send the message to the Crownstone
        UartEventBus.emit(SystemTopics.uartWriteData, uartPacket)

        # wait for the collectors to fill
        commandResultData = await resultCollector.receive()

        if commandResultData is not None:
            if commandResultData.resultCode is ResultValue.BUSY:
                await asyncio.sleep(0.2)
                return await self.setPowerZero(mW)
            elif commandResultData.resultCode is not ResultValue.SUCCESS:
                raise CrownstoneException(commandResultData.resultCode, "Command has failed.")
