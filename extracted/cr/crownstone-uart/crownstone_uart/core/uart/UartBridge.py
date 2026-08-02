import logging
import sys
import threading
import traceback

import serial
import serial.tools.list_ports

from crownstone_uart.Constants import UART_READ_TIMEOUT, UART_WRITE_TIMEOUT
from crownstone_uart.core.UartEventBus import UartEventBus
from crownstone_uart.core.uart.UartParser import UartParser
from crownstone_uart.core.uart.UartReadBuffer import UartReadBuffer
from crownstone_uart.topics.SystemTopics import SystemTopics
from crownstone_uart.Exceptions import UartBridgeError, UartException

_LOGGER = logging.getLogger(__name__)


class UartBridge(threading.Thread):
    """
    Thread that manages a serial port instance.
    """

    def __init__(self, exception_queue, port, baudrate, writeChunkMaxSize=0):
        self.bridge_exception_queue = exception_queue
        self.baudrate = baudrate
        self.port = port
        self.writeChunkMaxSize = writeChunkMaxSize

        self.serialController = None
        self.started = False

        self.running = True
        self.parser = UartParser()
        self.eventId = UartEventBus.subscribe(SystemTopics.uartWriteData, self.write_to_uart)

        threading.Thread.__init__(self)

    def __del__(self):
        self.stop()


    def run(self):
        try:
            self.start_serial()
            self.start_reading()
        except (UartException, BaseException):
            self.bridge_exception_queue.put(sys.exc_info())


    def stop(self):
        self.running = False
        UartEventBus.unsubscribe(self.eventId)
        self.parser.stop()


    def start_serial(self):
        _LOGGER.debug(F"UartBridge: Initializing serial on port {self.port} with baudrate {self.baudrate}")
        try:
            self.serialController = serial.Serial()
            self.serialController.port = self.port
            self.serialController.baudrate = int(self.baudrate)
            self.serialController.timeout = UART_READ_TIMEOUT
            self.serialController._write_timeout = UART_WRITE_TIMEOUT
            self.serialController.open()
        except OSError or serial.SerialException or KeyboardInterrupt as serial_error:
            self.stop()
            _LOGGER.error(serial_error)
            raise UartException(UartBridgeError.CANNOT_OPEN_SERIAL_CONTROLLER, serial_error) from serial_error


    def start_reading(self):
        readBuffer = UartReadBuffer()
        self.started = True
        _LOGGER.debug(F"Read starting on serial port {self.port} {self.running}")
        try:
            while self.running:
                bytesFromSerial = self.serialController.read() # reads single byte (blocks until it is received)
                if bytesFromSerial:
                    # read all extra bytes in read buffer
                    if self.serialController.in_waiting > 0:
                        additionalBytes = self.serialController.read(self.serialController.in_waiting)
                        bytesFromSerial = bytesFromSerial + additionalBytes

                    UartEventBus.emit(SystemTopics.uartRawData, bytesFromSerial)
                    readBuffer.addByteArray(bytesFromSerial)
        except OSError or serial.SerialException:
            _LOGGER.info("Connection to USB Failed. Retrying...")
        except KeyboardInterrupt:
            self.running = False
            _LOGGER.debug("Closing serial connection.")
        except Exception as error:
            self.running = False
            _LOGGER.error(f"Error in handling UART data: {error}")
            traceback.print_exc()

        # close the serial controller
        self.serialController.close()
        self.serialController = None
        # remove the event listener pointing to the old connection
        UartEventBus.unsubscribe(self.eventId)
        self.started = False
        UartEventBus.emit(SystemTopics.connectionClosed, True)

    def write_to_uart(self, data):
        _LOGGER.debug(f"write_to_uart: {data}")
        if self.serialController is not None and self.started:
            try:
                if self.writeChunkMaxSize == 0:
                    self.serialController.write(data)
                else:
                    # writing in chunks solves issues writing to certain JLink chips. A max chunkSize of 64 was found to work well for our case.
                    chunkSize = self.writeChunkMaxSize
                    index = 0
                    while (index*chunkSize) < len(data):
                        chunkedData = data[index*chunkSize:chunkSize*(index+1)]
                        index += 1
                        self.serialController.write(chunkedData)

                UartEventBus.emit(SystemTopics.uartWriteSuccess, data)
            except serial.SerialTimeoutException as e:
                UartEventBus.emit(SystemTopics.uartWriteError, {"message":"Timeout on uart write.", "error": e})
            except serial.SerialException as e:
                UartEventBus.emit(SystemTopics.uartWriteError, {"message":"SerialException occurred during uart write", "error": e})
            except OSError as e:
                UartEventBus.emit(SystemTopics.uartWriteError, {"message":"OSError occurred during uart write.", "error": e})
            except Exception as e:
                UartEventBus.emit(SystemTopics.uartWriteError, {"message": "Unknown Exception during uart write.", "error": e})
            except:
                e = sys.exc_info()[0]
                UartEventBus.emit(SystemTopics.uartWriteError, {"message":"Unknown error during uart write.", "error": e})
        else:
            self.stop()
