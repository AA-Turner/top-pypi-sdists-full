import datetime
import logging

from crownstone_core.Exceptions import CrownstoneException
from crownstone_core.packets.ResultPacket import ResultPacket
from crownstone_core.packets.ServiceData import ServiceData
from crownstone_core.packets.microapp.MicroappMessagePacket import MicroappMessagePacket
from crownstone_core.packets.serviceDataParsers.parsers import parseOpcode7
from crownstone_core.util.Conversion import Conversion

from crownstone_uart.core.uart.uartPackets.AssetIdReport import AssetIdReport
from crownstone_uart.core.uart.uartPackets.AssetMacReport import AssetMacReport
from crownstone_uart.core.UartEventBus import UartEventBus
from crownstone_uart.core.uart.UartTypes import UartRxType, UartMessageType
from crownstone_uart.core.uart.uartPackets.AdcConfigPacket import AdcConfigPacket
from crownstone_uart.core.uart.uartPackets.CurrentSamplesPacket import CurrentSamplesPacket
from crownstone_uart.core.uart.uartPackets.PowerCalculationPacket import PowerCalculationPacket
from crownstone_uart.core.uart.uartPackets.RssiBetweenStonesPacket import RssiBetweenStonesPacket
from crownstone_uart.core.uart.uartPackets.UartCrownstoneHelloPacket import UartCrownstoneHelloPacket
from crownstone_uart.core.uart.uartPackets.UartLogArrayPacket import UartLogArrayPacket
from crownstone_uart.core.uart.uartPackets.UartLogPacket import UartLogPacket
from crownstone_uart.core.uart.uartPackets.UartMessagePacket import UartMessagePacket
from crownstone_uart.core.uart.uartPackets.UartWrapperPacket import UartWrapperPacket, PROTOCOL_MAJOR
from crownstone_uart.core.uart.uartPackets.VoltageSamplesPacket import VoltageSamplesPacket
from crownstone_uart.topics.DevTopics import DevTopics
from crownstone_uart.topics.SystemTopics import SystemTopics
from crownstone_uart.topics.UartTopics import UartTopics

_LOGGER = logging.getLogger(__name__)

class UartParser:
    """
    Receives SystemTopics.uartNewPackage messages and emits their corresponding SystemTopics.uartNewMessage events.
    Several opcodes for uartNewMessage wil subsequently be parsed (looped back) and a more specific event may
    be emitted.
    """
    
    def __init__(self):
        self.uartPackageSubscription = UartEventBus.subscribe(SystemTopics.uartNewPackage, self.parse)
        self.uartMessageSubscription = UartEventBus.subscribe(SystemTopics.uartNewMessage, self.handleUartMessage)
        self.timestampFormat = "%Y-%m-%d %H:%M:%S.%f"

    def stop(self):
        UartEventBus.unsubscribe(self.uartPackageSubscription)
        UartEventBus.unsubscribe(self.uartMessageSubscription)

    def parse(self, wrapperPacket: UartWrapperPacket):
        """
        Callback for SystemTopics.uartNewPackage, emits a message of type SystemTopic.uartNewMessage
        if the received message was of the correct protocol version and unencrypted.
        :param wrapperPacket:
        :return:
        """
        if type(wrapperPacket) is not UartWrapperPacket:
            raise TypeError(f"Invalid type: {type(wrapperPacket)}")

        if wrapperPacket.protocolMajor != PROTOCOL_MAJOR:
            _LOGGER.warning(F"Unknown protocol: {wrapperPacket.protocolMajor}.{wrapperPacket.protocolMinor}")
            return

        msgType = wrapperPacket.messageType
        if msgType == UartMessageType.UART_MESSAGE:
            uartMsg = UartMessagePacket()
            if uartMsg.parse(wrapperPacket.payload):
                UartEventBus.emit(SystemTopics.uartNewMessage, uartMsg)
        elif msgType == UartMessageType.ENCRYPTED_UART_MESSAGE:
            _LOGGER.info(f"Received encrypted msg: decryption is not implemented.")
            return
        else:
            _LOGGER.warning(F"Unknown message type: {msgType}")
            return

    def handleUartMessage(self, messagePacket: UartMessagePacket):
        try:
            self._handleUartMessage(messagePacket)
        except CrownstoneException as e:
            # TODO: don't we catch too many errors this way
            #  For example errors from code executed by emitted events.
            #  We only want to catch parse errors, but we're too lazy to put a try catch around every parse call.
            _LOGGER.error(f"Parse error: {e}")

    def _handleUartMessage(self, messagePacket: UartMessagePacket):
        """
        Callback for SystemTopics.uartNewMessage. This transforms a select number of message types
        into further specialized messages and posts those on UartEventBus.
        :param messagePacket:
        :return:
        """
        opCode = messagePacket.opCode
        parsedData = None
        # print("UART - opCode:", opCode, "payload:", messagePacket.payload)

        if opCode == UartRxType.HELLO:
            helloPacket = UartCrownstoneHelloPacket(messagePacket.payload)
            UartEventBus.emit(UartTopics.hello, helloPacket)
            pass

        elif opCode == UartRxType.SESSION_NONCE:
            _LOGGER.debug(f"Received SESSION_NONCE")
            pass

        elif opCode == UartRxType.HEARTBEAT:
            _LOGGER.debug(f"Received HEARTBEAT")
            pass

        elif opCode == UartRxType.STATUS:
            _LOGGER.debug(f"Received STATUS")
            pass

        elif opCode == UartRxType.RESULT_PACKET:
            packet = ResultPacket(messagePacket.payload)
            UartEventBus.emit(SystemTopics.resultPacket, packet)


        #################
        # Error replies #
        #################

        elif opCode == UartRxType.ERR_REPLY_PARSING_FAILED:
            _LOGGER.debug(f"Received ERR_REPLY_PARSING_FAILED")
            pass

        elif opCode == UartRxType.ERR_REPLY_STATUS:
            _LOGGER.debug(f"Received ERR_REPLY_STATUS")
            pass

        elif opCode == UartRxType.ERR_REPLY_SESSION_NONCE_MISSING:
            _LOGGER.debug(f"Received ERR_REPLY_SESSION_NONCE_MISSING")
            pass

        elif opCode == UartRxType.ERR_REPLY_DECRYPTION_FAILED:
            _LOGGER.debug(f"Received ERR_REPLY_DECRYPTION_FAILED")
            pass

        elif 9900 < opCode < 10000:
            _LOGGER.debug(f"Received ERR_REPLY {opCode}")
            pass


        ################
        #### Events ####
        ################

        elif opCode == UartRxType.UART_MESSAGE:
            stringResult = ""
            for byte in messagePacket.payload:
                stringResult += chr(byte)
            # logStr = "LOG: %15.3f - %s" % (time.time(), stringResult)
            UartEventBus.emit(UartTopics.uartMessage, {"string":stringResult, "data": messagePacket.payload})

        elif opCode == UartRxType.SESSION_NONCE_MISSING:
            _LOGGER.debug(f"Received SESSION_NONCE_MISSING")
            pass

        elif opCode == UartRxType.OWN_SERVICE_DATA:
            # service data type + device type + data type + service data (15b)
            serviceData = ServiceData(messagePacket.payload)
            serviceData.parse()
            UartEventBus.emit(DevTopics.newServiceData, serviceData.payload)

        elif opCode == UartRxType.PRESENCE_CHANGE:
            pass

        elif opCode == UartRxType.FACTORY_RESET:
            pass

        elif opCode == UartRxType.BOOTED:
            _LOGGER.debug(f"Received BOOTED")
            pass

        elif opCode == UartRxType.HUB_DATA:
            pass

        elif opCode == UartRxType.MICROAPP_DATA:
            packet = MicroappMessagePacket.fromData(messagePacket.payload)
            _LOGGER.debug(f"Received microapp message: {packet}")
            UartEventBus.emit(UartTopics.microappMessage, packet)

        elif opCode == UartRxType.MESH_SERVICE_DATA:
            # data type + service data (15b)
            result = parseOpcode7(messagePacket.payload)
            _LOGGER.debug(f"Received service data: {result}")
            if hasattr(result,"crownstoneId"):
                UartEventBus.emit(SystemTopics.stateUpdate, (result.crownstoneId, result))

        elif opCode == UartRxType.EXTERNAL_STATE_PART_0:
            pass

        elif opCode == UartRxType.EXTERNAL_STATE_PART_1:
            pass

        elif opCode == UartRxType.MESH_RESULT:
            if len(messagePacket.payload) > 1:
                crownstoneId = messagePacket.payload[0]
                packet = ResultPacket(messagePacket.payload[1:])
                UartEventBus.emit(SystemTopics.meshResultPacket, [crownstoneId, packet])

        elif opCode == UartRxType.MESH_ACK_ALL_RESULT:
            packet = ResultPacket(messagePacket.payload)
            UartEventBus.emit(SystemTopics.meshResultFinalPacket, packet)

        elif opCode == UartRxType.RSSI_PING_MESSAGE:
            # for now, you can subscribe to SystemTopics.uartNewMessage
            pass

        elif opCode == UartRxType.LOG:
            _LOGGER.debug(f"Received binary log: {messagePacket.payload}")
            packet = UartLogPacket(messagePacket.payload)
            UartEventBus.emit(UartTopics.log, packet)

        elif opCode == UartRxType.LOG_ARRAY:
            _LOGGER.debug(f"Received binary log array: {messagePacket.payload}")
            packet = UartLogArrayPacket(messagePacket.payload)
            UartEventBus.emit(UartTopics.logArray, packet)

        elif opCode == UartRxType.NEIGHBOUR_RSSI:
            _LOGGER.debug(f"Received neighbour RSSI: {messagePacket.payload}")
            packet = RssiBetweenStonesPacket(messagePacket.payload)
            UartEventBus.emit(UartTopics.rssiBetweenStones, packet)

        #######################
        # ASSET FILTER events #
        #######################

        elif opCode == UartRxType.ASSET_MAC_RSSI_REPORT:
            _LOGGER.debug(f"Received ASSET_MAC_RSSI_REPORT: {messagePacket.payload}")
            packet = AssetMacReport(messagePacket.payload)
            UartEventBus.emit(UartTopics.assetTrackingReport, packet)

        elif opCode == UartRxType.ASSET_ID_RSSI_REPORT:
            _LOGGER.debug(f"Received ASSET_ID_RSSI_REPORT: {messagePacket.payload}")
            packet = AssetIdReport(messagePacket.payload)
            UartEventBus.emit(UartTopics.assetIdReport, packet)


        ####################
        # Developer events #
        ####################

        elif opCode == UartRxType.INTERNAL_EVENT:
            pass

        elif opCode == UartRxType.MESH_CMD_TIME:
            pass

        elif opCode == UartRxType.MESH_PROFILE_LOCATION:
            pass

        elif opCode == UartRxType.MESH_SET_BEHAVIOUR_SETTINGS:
            pass

        elif opCode == UartRxType.MESH_TRACKED_DEVICE_REGISTER:
            pass

        elif opCode == UartRxType.MESH_TRACKED_DEVICE_TOKEN:
            pass

        elif opCode == UartRxType.MESH_SYNC_REQUEST:
            pass

        elif opCode == UartRxType.MESH_TRACKED_DEVICE_HEARTBEAT:
            pass


        ######################
        # Debug build events #
        ######################

        elif opCode == UartRxType.ADVERTISING_ENABLED:
            pass

        elif opCode == UartRxType.MESH_ENABLED:
            pass

        elif opCode == UartRxType.CROWNSTONE_ID:
            id = Conversion.int8_to_uint8(messagePacket.payload)
            UartEventBus.emit(DevTopics.ownCrownstoneId, id)

        elif opCode == UartRxType.MAC_ADDRESS:
            addr = Conversion.uint8_array_to_address(messagePacket.payload)
            if addr != "":
                UartEventBus.emit(DevTopics.ownMacAddress, addr)
            else:
                _LOGGER.warning("invalid address:", messagePacket.payload)

        elif opCode == UartRxType.ADC_CONFIG:
            # type is PowerCalculationsPacket
            parsedData = AdcConfigPacket(messagePacket.payload)
            UartEventBus.emit(DevTopics.newAdcConfigPacket, parsedData.getDict())

        elif opCode == UartRxType.ADC_RESTART:
            UartEventBus.emit(DevTopics.adcRestarted, None)

        elif opCode == UartRxType.POWER_LOG_CURRENT:
            # type is CurrentSamples
            parsedData = CurrentSamplesPacket(messagePacket.payload)
            UartEventBus.emit(DevTopics.newCurrentData, parsedData.getDict())

        elif opCode == UartRxType.POWER_LOG_VOLTAGE:
            # type is VoltageSamplesPacket
            parsedData = VoltageSamplesPacket(messagePacket.payload)
            UartEventBus.emit(DevTopics.newVoltageData, parsedData.getDict())

        elif opCode == UartRxType.POWER_LOG_FILTERED_CURRENT:
            # type is CurrentSamples
            parsedData = CurrentSamplesPacket(messagePacket.payload)
            UartEventBus.emit(DevTopics.newFilteredCurrentData, parsedData.getDict())

        elif opCode == UartRxType.POWER_LOG_FILTERED_VOLTAGE:
            # type is VoltageSamplesPacket
            parsedData = VoltageSamplesPacket(messagePacket.payload)
            UartEventBus.emit(DevTopics.newFilteredVoltageData, parsedData.getDict())

        elif opCode == UartRxType.POWER_LOG_POWER:
            # type is PowerCalculationsPacket
            parsedData = PowerCalculationPacket(messagePacket.payload)
            UartEventBus.emit(DevTopics.newCalculatedPowerData, parsedData.getDict())

        elif opCode == UartRxType.ASCII_LOG:
            timestamp = datetime.datetime.now()
            stringResult = ""
            for byte in messagePacket.payload:
                if byte < 128:
                    stringResult += chr(byte)
            logStr = f"ASCII LOG: [{timestamp.strftime(self.timestampFormat)}] {stringResult}"
            # sys.stdout.write(logStr)
            print(logStr.rstrip())

        elif opCode == UartRxType.FIRMWARESTATE:
            # no need to process this, that's in the test suite.
            pass

        else:
            _LOGGER.debug(f"Unknown opCode: {opCode}")

        parsedData = None
        
