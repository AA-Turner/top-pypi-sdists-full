import logging
import threading
import time
import sys
import queue

from crownstone_core.protocol.BlePackets import ControlPacket
from crownstone_core.protocol.BluenetTypes import ControlType

from crownstone_uart.core.dataFlowManagers.Collector import Collector
from crownstone_uart.core.uart.uartPackets.UartCommandHelloPacket import UartCommandHelloPacket
from crownstone_uart.core.uart.uartPackets.UartCrownstoneHelloPacket import UartCrownstoneHelloPacket
from crownstone_uart.core.uart.uartPackets.UartMessagePacket import UartMessagePacket

from crownstone_uart.core.UartEventBus import UartEventBus
from crownstone_uart.core.uart.uartPackets.UartWrapperPacket import UartWrapperPacket
from crownstone_uart.core.uart.UartTypes import UartTxType, UartMessageType
from crownstone_uart.core.uart.UartBridge import UartBridge

from crownstone_uart.topics.UartTopics import UartTopics
from crownstone_uart.topics.SystemTopics import SystemTopics

from crownstone_uart.Exceptions import UartException

from serial.tools import list_ports

_LOGGER = logging.getLogger(__name__)

class UartManager(threading.Thread):

    def __init__(self, exception_queue):
        self.port = None     # Port configured by user.
        self.baudRate = 230400
        self.writeChunkMaxSize = 0
        self.manager_exception_queue = exception_queue
        self.running = True
        self._availablePorts = list(list_ports.comports())
        self._attemptingIndex = 0
        self._uartBridge = None
        self.ready = False

        self.eventId = UartEventBus.subscribe(SystemTopics.connectionClosed, self.resetEvent)

        self.custom_port_set = False

        threading.Thread.__init__(self)

    def __del__(self):
        self.stop()

    def config(self, port, baudRate = 230400, writeChunkMaxSize=0):
        if port is not None:
            self.custom_port_set = True
        self.port            = port
        self.baudRate        = baudRate
        self.writeChunkMaxSize = writeChunkMaxSize

    def run(self):
        try:
            self.initialize()
        except (UartException, BaseException):
            self.manager_exception_queue.put(sys.exc_info())

    def stop(self):
        self.running = False
        UartEventBus.unsubscribe(self.eventId)
        if self._uartBridge is not None:
            self._uartBridge.stop()

    def resetEvent(self, eventData=None):
        if self.ready:
            self._uartBridge.stop()
            while self._uartBridge.running:
                time.sleep(0.1)
            self.reset()

            self.ready = False
            self.initialize()

    def reset(self):
        if self.running:
            self._attemptingIndex = 0
            self._availablePorts = list(list_ports.comports())
            self._uartBridge = None
            self.port = None

    def echo(self, string):
        controlPacket = ControlPacket(ControlType.UART_MESSAGE).loadString(string).serialize()
        uartMessage   = UartMessagePacket(UartTxType.CONTROL, controlPacket).serialize()
        uartPacket    = UartWrapperPacket(UartMessageType.UART_MESSAGE, uartMessage).serialize()
        UartEventBus.emit(SystemTopics.uartWriteData, uartPacket)

    def writeHello(self):
        helloPacket = UartCommandHelloPacket().serialize()
        uartMessage = UartMessagePacket(UartTxType.HELLO, helloPacket).serialize()
        uartPacket = UartWrapperPacket(UartMessageType.UART_MESSAGE, uartMessage).serialize()
        UartEventBus.emit(SystemTopics.uartWriteData, uartPacket)

    def initialize(self):
        if not self.custom_port_set:
            _LOGGER.warning(F"By not providing a specific port to find the Crownstone dongle, we will try to connect and handshake with all available ports one by one until we find the dongle."
                            F"\nPorts that will be checked are:"
                            F"\n{[port.device for port in self._availablePorts]}")

        while self.running and not self.ready:
            self.ready = False
            _LOGGER.debug(F"Initializing... {self.port} {self.baudRate}")

            # if the user provides his own port, we check if it is in the list of ports we have
            # if it exists, we start there and skip the handshake.
            # if it is not in the list, we attempt the connection regardless, this might change in the future.
            if self.port is not None:
                found_port = False
                index = 0
                # check if the provided port is among the listed ports.
                for testPort in self._availablePorts:
                    if self.port == testPort.device:
                        found_port = True
                        self._attemptingIndex = index
                        break
                    index += 1
                # if it is not in the list of available ports
                if not found_port:
                    # we will attempt it anyway
                    _LOGGER.warning(F"Could not find provided port {self.port}")
                else:
                    _LOGGER.debug(F"Setup connection to {self.port}")
                self.setupConnection(self.port, performHandshake=False)
                continue


            if self.port is None:
                if self._attemptingIndex >= len(self._availablePorts): # this also catches len(self._availablePorts) == 0
                    _LOGGER.warning("No Crownstone USB connected? Retrying...")
                    time.sleep(1)
                    self.reset()
                else:
                    self._attemptConnection(self._attemptingIndex)


    def _attemptConnection(self, index, handshake=True):
        attemptingPort = self._availablePorts[index]
        self.setupConnection(attemptingPort.device, handshake)


    def setupConnection(self, port, performHandshake=True):
        _LOGGER.debug(F"Setting up connection... port={port} baudRate={self.baudRate} performHandshake={performHandshake}")
        bridge_exception_queue = queue.Queue()
        self._uartBridge = UartBridge(bridge_exception_queue, port, self.baudRate, self.writeChunkMaxSize)
        self._uartBridge.start()

        def initialize_bridge():
            # handle exceptions that happen in thread while initializing
            while not self._uartBridge.started and self.running:
                try:
                    exception, exception_value, trace = bridge_exception_queue.get(block=False)
                    self._uartBridge.join()
                    raise exception(exception_value)
                except queue.Empty:
                    pass
                    
                time.sleep(0.1)
        
        # attempt serial connection with the dongle
        initialize_bridge()

        # this is true by default if no handshake is required
        handshake_succesfull = True

        if performHandshake:
            collector = Collector(timeout=0.25, topic=UartTopics.hello)
            self.writeHello()
            reply = collector.receive_sync()

            handshake_succesfull = False
            if isinstance(reply, UartCrownstoneHelloPacket):
                handshake_succesfull = True
                _LOGGER.debug("Handshake successful")
            else:
                if self.port == port:
                    _LOGGER.warning("Handshake failed: no reply from the crownstone.")
                else:
                    _LOGGER.debug("Handshake failed: no reply from the crownstone.")

        if not handshake_succesfull:
            _LOGGER.debug("Reinitialization required")
            self._attemptingIndex += 1
            self._uartBridge.stop()

            initialize_bridge()

        else:
            _LOGGER.info("Connection established to {}".format(port))
            self.port = port
            self.ready = True
            UartEventBus.emit(SystemTopics.connectionEstablished)



    def is_ready(self) -> bool:
        return self.ready
