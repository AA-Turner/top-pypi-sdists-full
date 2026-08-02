from crownstone_core.protocol.BlePackets import ControlStateSetPacket, ControlPacket
from crownstone_core.protocol.BluenetTypes import StateType, ControlType

from crownstone_uart.core.UartEventBus import UartEventBus
from crownstone_uart.core.uart.uartPackets.UartMessagePacket import UartMessagePacket
from crownstone_uart.core.uart.UartTypes import UartTxType, UartMessageType
from crownstone_uart.core.uart.uartPackets.UartWrapperPacket import UartWrapperPacket
from crownstone_uart.core.dataFlowManagers.UartWriter import UartWriter
from crownstone_uart.topics.SystemTopics import SystemTopics

from crownstone_core.packets.microapp.MicroappHeaderPacket import MicroappHeaderPacket
from crownstone_core.packets.microapp.MicroappInfoPacket import MicroappInfoPacket
from crownstone_core.packets.microapp.MicroappUploadPacket import MicroappUploadPacket

class UsbDevHandler:
    
    def setAdvertising(self, enabled):
        """
            Enable/ disable the advertising
            :param enabled: Boolean
            :return:
        """
        self._send(UartTxType.ENABLE_ADVERTISEMENT, self._getPayload(enabled))
    
    def setMeshing(self, enabled):
        """
            Enable/ disable the Meshing
            :param enabled: Boolean
            :return:
        """
        self._send(UartTxType.ENABLE_MESH, self._getPayload(enabled))
    
    def requestCrownstoneId(self):
        """
            Request the Crownstone ID. This is a uint16
            :return:
        """
        self._send(UartTxType.GET_CROWNSTONE_ID, [])
    
    def requestMacAddress(self):
        """
            Request the MAC address ID.
            :return:
        """
        self._send(UartTxType.GET_MAC_ADDRESS, [])
    
    def increaseCurrentRange(self):
        """
            Increase the GAIN on the current sensing
            :return:
        """
        self._send(UartTxType.ADC_CONFIG_INC_RANGE_CURRENT, [])
    
    def decreaseCurrentRange(self):
        """
            Decrease the GAIN on the current sensing
            :return:
        """
        self._send(UartTxType.ADC_CONFIG_DEC_RANGE_CURRENT, [])
    
    def increaseVoltageRange(self):
        """
            Increase the GAIN on the voltage sensing
            :return:
        """
        self._send(UartTxType.ADC_CONFIG_INC_RANGE_VOLTAGE, [])
    
    def decreaseVoltageRange(self):
        """
            Decrease the GAIN on the voltage sensing
            :return:
        """
        self._send(UartTxType.ADC_CONFIG_DEC_RANGE_VOLTAGE, [])
    
    def setDifferentialModeCurrent(self, enabled):
        """
            Enable/disable differential mode on the current sensing
            :param enabled: Boolean
            :return:
        """
        self._send(UartTxType.ADC_CONFIG_DIFFERENTIAL_CURRENT, self._getPayload(enabled))
    
    def setDifferentialModeVoltage(self, enabled):
        """
            Enable/disable differential mode on the voltage sensing
            :param enabled: Boolean
            :return:
        """
        self._send(UartTxType.ADC_CONFIG_DIFFERENTIAL_VOLTAGE, self._getPayload(enabled))

    def setVoltageChannelPin(self, pin):
        """
            Select the measurement pin for the voltage sensing
            :param pin: int [0 .. 255]
            :return:
        """
        self._send(UartTxType.ADC_CONFIG_VOLTAGE_PIN, [pin])

    def toggleVoltageChannelPin(self):
        """
            Select the measurement pin for the voltage sensing
            :return:
        """
        self._send(UartTxType.ADC_CONFIG_VOLTAGE_PIN, [])

    def setSendCurrentSamples(self, enabled):
        """
            Enable/ disable the sending of the measured current buffer.
            :param enabled: Boolean
            :return:
        """
        self._send(UartTxType.POWER_LOG_CURRENT, self._getPayload(enabled))

    def setSendVoltageSamples(self, enabled):
        """
            Enable/ disable the sending of the measured voltage buffer.
            :param enabled: Boolean
            :return:
        """
        self._send(UartTxType.POWER_LOG_VOLTAGE, self._getPayload(enabled))
    
    def setSendFilteredCurrentSamples(self, enabled):
        """
            Enable/ disable the sending of the filtered current sample buffer.
            :param enabled: Boolean
            :return:
        """
        self._send(UartTxType.POWER_LOG_FILTERED_CURRENT, self._getPayload(enabled))
     
    def setSendFilteredVoltageSamples(self, enabled):
        """
            Enable/ disable the sending of the filtered voltage sample buffer.
            :param enabled: Boolean
            :return:
        """
        self._send(UartTxType.POWER_LOG_FILTERED_VOLTAGE, self._getPayload(enabled))
    
    def setSendCalculatedSamples(self, enabled):
        """
            Enable/ disable the sending of the calculated power samples.
            :param enabled: Boolean
            :return:
        """
        self._send(UartTxType.POWER_LOG_CALCULATED_POWER, self._getPayload(enabled))

    def setUartMode(self, mode):
        """
            Set UART mode.
            :param mode: : 0=none 1=RX only, 2=TX only, 3=TX and RX
            :return:
        """
        if (mode < 0) or (mode > 3):
            return
        controlPacket = ControlStateSetPacket(StateType.UART_ENABLED).loadUInt8(mode).serialize()
        self._send(UartTxType.CONTROL, controlPacket)

    def resetCrownstone(self):
        """
            Reset the Crownstone
            :return:
        """
        resetPacket = ControlPacket(ControlType.RESET).serialize()
        self._send(UartTxType.CONTROL, resetPacket)

    def toggleRelay(self, isOn):
        val = 0
        if isOn:
            val = 1
        switchPacket = ControlPacket(ControlType.RELAY).loadUInt8(val).serialize()
        self._send(UartTxType.CONTROL, switchPacket)

    def toggleIGBTs(self, isOn):
        val = 0
        if isOn:
            val = 100
        switchPacket = ControlPacket(ControlType.PWM).loadUInt8(val).serialize()
        self._send(UartTxType.CONTROL, switchPacket)

    def toggleAllowDimming(self, isOn):
        val = 0
        if isOn:
            val = 1
        instructionPacket = ControlPacket(ControlType.ALLOW_DIMMING).loadUInt8(val).serialize()
        self._send(UartTxType.CONTROL, instructionPacket)

    def remove_microapp(self, index : int):
        """
        Remove microapp from flash memory in Bluenet. Return True if message is send correctly, it
        doesn't check if the command is set correctly in Bluenet. For now only an index of 0 can
        be given, since Bluenet only supports a single app to run.
        """
        packet = MicroappHeaderPacket(index)
        controlPacket = ControlPacket(
            ControlType.MICROAPP_REMOVE).loadByteArray(packet.serialize()).serialize()
        uartMessage   = UartMessagePacket(UartTxType.CONTROL, controlPacket).serialize()
        uartPacket    = UartWrapperPacket(UartMessageType.UART_MESSAGE, uartMessage).serialize()
        UartWriter(uartPacket).write_sync()

    def enable_microapp(self, index : int):
        """
        Enable microapp in Bluenet and load it in RAM. Return True if message is send correctly,
        it doesn't check if the command is set correctly in Bluenet. For now only an index of 0
        can be given, since Bluenet only supports a single app to run. It is recommended to run
        the validation function before enabling the microapp to make sure a microapp is able to
        run.
        """
        packet = MicroappHeaderPacket(index)
        controlPacket = ControlPacket(
            ControlType.MICROAPP_ENABLE).loadByteArray(packet.serialize()).serialize()
        uartMessage   = UartMessagePacket(UartTxType.CONTROL, controlPacket).serialize()
        uartPacket    = UartWrapperPacket(UartMessageType.UART_MESSAGE, uartMessage).serialize()
        UartWriter(uartPacket).write_sync()

    def validate_microapp(self, index : int):
        """
        validate the binary of a microapp saved in Bluenet flash memory. Return True if message is
        send correctly, it doesn't check if the command is set correctly in Bluenet. For now only
        an index of 0 can be given, since Bluenet only supports a single app to run.
        """
        packet = MicroappHeaderPacket(index)
        controlPacket = ControlPacket(
            ControlType.MICROAPP_VALIDATE).loadByteArray(packet.serialize()).serialize()
        uartMessage   = UartMessagePacket(UartTxType.CONTROL, controlPacket).serialize()
        uartPacket    = UartWrapperPacket(UartMessageType.UART_MESSAGE, uartMessage).serialize()
        UartWriter(uartPacket).write_sync()

    def disable_microapp(self, index : int):
        """
        Disable a running microapp in Bluenet by removing it from RAM. Return True if message is
        send correctly, it doesn't check if the command is set correctly in Bluenet. For now only
        an index of 0 can be given, since Bluenet only supports a single app to run.
        """
        packet = MicroappHeaderPacket(index)
        controlPacket = ControlPacket(
            ControlType.MICROAPP_DISABLE).loadByteArray(packet.serialize()).serialize()
        uartMessage   = UartMessagePacket(UartTxType.CONTROL, controlPacket).serialize()
        uartPacket    = UartWrapperPacket(UartMessageType.UART_MESSAGE, uartMessage).serialize()
        UartWriter(uartPacket).write_sync()



    def _getPayload(self, boolean):
        payload = 0
        if boolean:
            payload = 1
            
        return [payload]

    def _send(self, opCode: UartTxType, payload: list):
        # send over uart
        uartMessage = UartMessagePacket(opCode, payload).serialize()
        uartPacket = UartWrapperPacket(UartMessageType.UART_MESSAGE, uartMessage).serialize()
        UartEventBus.emit(SystemTopics.uartWriteData, uartPacket)
