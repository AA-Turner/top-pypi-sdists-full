#  _____ _____ _____
# |_    |   __| __  |
# |_| | |__   |    -|
# |_|_|_|_____|__|__|
# MSR Electronics GmbH
# SPDX-License-Identifier: MIT
#
#cython: language_level=3

from __future__ import absolute_import
from ft4222.cftd2xx cimport *
from ft4222.clibft4222 cimport *
from cpython.array cimport array, resize
from libc.stdio cimport printf
from libc.time cimport clock, clock_t, CLOCKS_PER_SEC
from enum import IntEnum
from .GPIO import Dir, Trigger
from .I2CMaster import ControllerStatus
from weakref import finalize as weakref_finalize

cdef extern from *:
    """
    #if defined(_WIN32) || defined(MS_WINDOWS) || defined(_MSC_VER)
      #include <malloc.h>
      #include <stdlib.h>
      #define msleep(m)  Sleep(m)
    #else
      #include <alloca.h>
      #include <unistd.h>
      #define msleep(m)  ((void) usleep((m) * 1000))
    #endif
    #define MAX_DESCRIPTION_SIZE 256
    """
    void *alloca(size_t size) nogil
    void msleep(int milliseconds) nogil
    extern const int MAX_DESCRIPTION_SIZE


class FT2XXDeviceError(Exception):
    """Exception class for status messages"""

    __ftd2xx_msgs = ['OK', 'INVALID_HANDLE', 'DEVICE_NOT_FOUND', 'DEVICE_NOT_OPENED',
                 'IO_ERROR', 'INSUFFICIENT_RESOURCES', 'INVALID_PARAMETER',
                 'INVALID_BAUD_RATE', 'DEVICE_NOT_OPENED_FOR_ERASE',
                 'DEVICE_NOT_OPENED_FOR_WRITE', 'FAILED_TO_WRITE_DEVICE0',
                 'EEPROM_READ_FAILED', 'EEPROM_WRITE_FAILED', 'EEPROM_ERASE_FAILED',
                 'EEPROM_NOT_PRESENT', 'EEPROM_NOT_PROGRAMMED', 'INVALID_ARGS',
                 'NOT_SUPPORTED', 'OTHER_ERROR', 'DEVICE_LIST_NOT_READY']

    def __init__(self, msgnum):
        self.message = self.__ftd2xx_msgs[msgnum]

    def __str__(self):
        return self.message

class FT4222DeviceError(FT2XXDeviceError):
    """Exception class for status messages"""

    __ftd4222_msgs = ['DEVICE_NOT_SUPPORTED', 'CLK_NOT_SUPPORTED','VENDER_CMD_NOT_SUPPORTED',
                  'IS_NOT_SPI_MODE', 'IS_NOT_I2C_MODE', 'IS_NOT_SPI_SINGLE_MODE',
                  'IS_NOT_SPI_MULTI_MODE', 'WRONG_I2C_ADDR', 'INVAILD_FUNCTION',
                  'INVALID_POINTER', 'EXCEEDED_MAX_TRANSFER_SIZE', 'FAILED_TO_READ_DEVICE',
                  'I2C_NOT_SUPPORTED_IN_THIS_MODE', 'GPIO_NOT_SUPPORTED_IN_THIS_MODE',
                  'GPIO_EXCEEDED_MAX_PORTNUM', 'GPIO_WRITE_NOT_SUPPORTED',
                  'GPIO_PULLUP_INVALID_IN_INPUTMODE', 'GPIO_PULLDOWN_INVALID_IN_INPUTMODE',
                  'GPIO_OPENDRAIN_INVALID_IN_OUTPUTMODE', 'INTERRUPT_NOT_SUPPORTED',
                  'GPIO_INPUT_NOT_SUPPORTED', 'EVENT_NOT_SUPPORTED', 'FUN_NOT_SUPPORT']

    def __init__(self, msgnum):
        if msgnum >= FT4222_DEVICE_NOT_SUPPORTED:
            self.message = self.__ftd4222_msgs[msgnum - FT4222_DEVICE_NOT_SUPPORTED]
        else:
            super(FT4222DeviceError, self).__init__(msgnum)

    def __str__(self):
        return self.message

class SysClock(IntEnum):
    """Chip system clock

    Attributes:
        CLK_60: 60 MHz
        CLK_24: 24 MHz
        CLK_48: 48 MHz
        CLK_80: 80 MHz

    """
    CLK_60 = 0
    CLK_24 = 1
    CLK_48 = 2
    CLK_80 = 3

class Purge(IntEnum):
    """Purge RX and TX buffers

    Attributes:
        RX: Purge RX buffer
        TX: Purge TX buffer

    """
    RX = 1
    TX = 2

def createDeviceInfoList():
    """Create the internal device info list and return number of entries"""
    cdef DWORD nb
    status = FT_CreateDeviceInfoList(&nb)
    if status == FT_OK:
        return nb
    raise FT2XXDeviceError, status

def getDeviceInfoDetail(devnum=0, update=True):
    """Get an entry from the internal device info list. Set update to
    False to avoid a slow call to createDeviceInfoList."""
    cdef:
        DWORD f, t, i, l
        FT_HANDLE h
        char n[MAX_DESCRIPTION_SIZE]
        char d[MAX_DESCRIPTION_SIZE]
    # createDeviceInfoList is slow, only run if update is True
    if update: createDeviceInfoList()
    status = FT_GetDeviceInfoDetail(devnum, &f, &t, &i, &l, n, d, &h)
    if status == FT_OK:
        return {'index': devnum, 'flags': f, 'type': t,
                'id': i, 'location': l, 'serial': n,
                'description': d, 'handle': <size_t>h}
    raise FT2XXDeviceError, status

def openBySerial(serial):
    """Open a handle to a usb device by serial number

    Args:
        serial (bytes, str): Serial number

    Returns:
        :obj:`FT4222`: Opened device

    Raises:
        FT2XXDeviceError: on error

    """
    if isinstance(serial, str):
        serial = serial.encode('utf-8')
    cdef FT_HANDLE handle
    cdef char* cserial = serial
    status = FT_OpenEx(<PVOID>cserial, FT_OPEN_BY_SERIAL_NUMBER, &handle)
    if status == FT_OK:
        return FT4222(<uintptr_t>handle, update=False)
    raise FT2XXDeviceError, status

def openByDescription(desc):
    """Open a handle to a usb device by description

    Args:
        desc (bytes, str): Description of the device

    Returns:
        :obj:`FT4222`: Opened device

    Raises:
        FT2XXDeviceError: on error

    """
    if isinstance(desc, str):
        desc = desc.encode('utf-8')
    cdef FT_HANDLE handle
    cdef char* cdesc = desc
    status = FT_OpenEx(<PVOID>cdesc, FT_OPEN_BY_DESCRIPTION, &handle)
    if status == FT_OK:
        #printf("handle: %d\n", handle)
        return FT4222(<uintptr_t>handle, update=False)
    raise FT2XXDeviceError, status

def openByLocation(locId):
    """Open a handle to a usb device by location

    Args:
        locId (int): Location id

    Returns:
        :obj:`FT4222`: Opened device

    Raises:
        FT2XXDeviceError: on error

    """
    cdef FT_HANDLE handle
    status = FT_OpenEx(<PVOID><uintptr_t>locId, FT_OPEN_BY_LOCATION, &handle)
    if status == FT_OK:
        return FT4222(<uintptr_t>handle, update=False)
    raise FT2XXDeviceError, status


cdef class _closer:
    """Wrap a hid_device *ptr and a provide a way to call hid_close() on it.
    Used internally for weakref.finalize, which only accepts Python objects.
    """

    cdef FT_HANDLE _handle

    @staticmethod
    cdef wrap(FT_HANDLE h):
        cdef _closer closer = _closer()
        closer._handle = h
        return closer

    def close(self):
        FT4222_UnInitialize(self._handle)
        FT_Close(self._handle)


cdef class FT4222:
    # Revision A chips report chipVersion as 0x42220100; revision B chips report
    # 0x42220200; revision C chips report 0x42220300.
    # Revision B chips require version 1.2 or later of LibFT4222,
    # indicated by dllVersion being greater than 0x01020000;
    # Revision C chips require version 1.3 or later of LibFT4222,
    # indicated by dllVersion being greater than 0x01030000;
    # Revision D chips require version 1.4 or later of LibFT4222,
    # indicated by dllVersion being greater than 0x01040000.
    __chip_rev_map = { 0x42220100: "Rev. A", 0x42220200: "Rev. B", 0x42220300: "Rev. C", 0x42220400: "Rev. D" }
    __chip_rev_min_lib = { 0x42220100: 0, 0x42220200: 0x01020000, 0x42220300: 0x01030000, 0x42220400: 0x01040000 }

    cdef FT_HANDLE _handle
    cdef DWORD _chip_version
    cdef DWORD _dll_version
    cdef object __weakref__  # enable weak-reference support
    cdef object _close

    def __init__(self, handle, update=True):
        self._handle = <FT_HANDLE><uintptr_t>handle
        self._chip_version = 0
        self._dll_version = 0
        self._get_version()
        self._close = weakref_finalize(self, _closer.wrap(self._handle).close)

    def close(self):
        """Closes the device."""
        FT4222_UnInitialize(self._handle)
        status = FT_Close(self._handle)
        if status != FT4222_OK:
            raise FT4222DeviceError, status
        self._close.detach()
        self._handle = NULL

    cdef _get_version(self):
        cdef FT4222_Version ver
        status = FT4222_GetVersion(self._handle, &ver)
        if status == FT4222_OK:
            self._chip_version = ver.chipVersion
            self._dll_version = ver.dllVersion

    @property
    def chipVersion(self) -> int:
        """Chip version as number"""
        return self._chip_version

    @property
    def libVersion(self) -> int:
        """Library version as number"""
        return self._dll_version

    @property
    def chipRevision(self) -> str:
        """The revision of the chip in human readable format"""
        try:
            return self.__chip_rev_map[self._chip_version]
        except KeyError:
            return "Rev. unknown"

    def __repr__(self):
        return "FT4222: chipVersion: 0x{:x} ({:s}), libVersion: 0x{:x}".format(self._chip_version, self.chipRevision, self._dll_version)

    def setTimeouts(self, read_timeout, write_timeout):
        """Set the read and write timeouts

        Args:
            read_timeout (int): Read timeout in milliseconds.
            write_timeout (int): Write timeout in milliseconds.

        Raises:
            FT2XXDeviceError: on error

        """
        status = FT_SetTimeouts(self._handle, read_timeout, write_timeout)
        if status != FT_OK:
            raise FT2XXDeviceError, status

    def setClock(self, clk):
        """Set the system clock

        Args:
            clk (:obj:`ft4222.SysClock`): Desired clock

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_SetClock(self._handle, clk)
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def getClock(self):
        """Get the system clock

        Returns:
            :obj:`ft4222.SysClock`: Clock

        Raises:
            FT4222DeviceError: on error

        """
        cdef FT4222_ClockRate clk
        status = FT4222_GetClock(self._handle, &clk)
        if status == FT4222_OK:
            return SysClock(clk)
        raise FT4222DeviceError, status

    def setSuspendOut(self, enable):
        """Enable or disable, suspend out, which will emit a signal when FT4222H enters suspend mode.

        Args:
            enable (bool): TRUE to enable suspend out and configure GPIO2 as an output pin for emitting a signal when suspended. FALSE to switch back to GPIO2

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_SetSuspendOut(self._handle, enable)
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def setWakeUpInterrupt(self, enable):
        """Enable or disable the wakeup/interrupt

        Args:
            enable (bool): True to configure GPIO3 as an input pin for wakeup/interrupt. FALSE to switch back to GPIO3.

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_SetWakeUpInterrupt(self._handle, enable)
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def getMaxTransferSize(self):
        """Get the maximum transfer size for the currently configured operating mode

        Returns:
            int: Maximum number of bytes for each transfer.

        Raises:
            FT4222DeviceError: on error
        """
        cdef uint16 maxTransferSize = 0
        status = FT4222_GetMaxTransferSize(self._handle, &maxTransferSize)
        if status == FT4222_OK:
            return maxTransferSize
        raise FT4222DeviceError, status

    def vendorCmdGet(self, req, bytesToRead):
        """Vendor get command"""
        cdef:
            array[uint8] buf = array('B', [])
        resize(buf, bytesToRead)
        status = FT_VendorCmdGet(self._handle, req, buf.data.as_uchars, bytesToRead)
        if status == FT_OK:
            return bytes(buf)
        raise FT4222DeviceError, status

    def vendorCmdSet(self, req, data):
        """Vendor set command"""
        if isinstance(data, int):
            data = bytes([data])
        elif not isinstance(data, (bytes, bytearray)):
            raise TypeError("the data argument must be of type 'int', 'bytes' or 'bytearray'")
        cdef:
            uint16 bytesSent
            uint8* cdata = data
        status = FT_VendorCmdSet(self._handle, req, cdata, len(data))
        if status != FT_OK:
            raise FT4222DeviceError, status

    def getLatencyTimer(self):
        """Get the current value of the latency timer.

        Returns:
            int: Latency timer value in milliseconds

        Raises:
            FT2XXDeviceError: on error
        """
        cdef UCHAR latency
        status = FT_GetLatencyTimer(self._handle, &latency)
        if status == FT_OK:
            return latency
        raise FT2XXDeviceError, status

    def setLatencyTimer(self, latency):
        """Set the current value of the latency timer.

        Args:
            latency (int): Latency timer value in milliseconds. Valid range is 2 - 255

        Raises:
            FT2XXDeviceError: on error
        """
        status = FT_SetLatencyTimer(self._handle, latency)
        if status != FT_OK:
            raise FT2XXDeviceError, status

    def getChipMode(self):
        """Get chip mode information.

        This function is used to attempt to get chip mode information. The chip mode information is identified
        when the system power on as defined by the {DCNF1, DCNF0} pins. If the chip mode is changed
        after the system is powered, the chip mode value would keep the value from when the system was
        powered on.

        Raises:
            FT4222DeviceError: on error
        """
        cdef uint8 chipMode
        status = FT4222_GetChipMode(self._handle, &chipMode)
        if status == FT4222_OK:
            return chipMode
        raise FT4222DeviceError, status

    def chipReset(self):
        """Software reset for device.
        This function is used to attempt to recover system after a failure. It is a software reset for device.

        Re-opening the device may be needed after calling this function.

        Raises:
            FT4222DeviceError: on error
        """
        status = FT4222_ChipReset(self._handle)
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def purge(self, mask=Purge.RX|Purge.TX):
        """This function purges receive and transmit buffers in the device.

        Args:
            mask (:obj:`ft4222.Purge`): Buffer to purge

        Raises:
            FT2XXDeviceError: on error
        """
        status = FT_Purge(self._handle, mask)
        if status != FT_OK:
            raise FT2XXDeviceError, status

    def resetDevice(self):
        """This function sends a reset command to the device.

        Raises:
            FT2XXDeviceError: on error
        """
        status = FT_ResetDevice(self._handle)
        if status != FT_OK:
            raise FT2XXDeviceError, status

    def resetPort(self):
        """Send a reset command to the port.

        This function is used to attempt to recover the port after a failure.
        It is not equivalent to an unplugreplug event.
        For the equivalent of an unplug-replug event, use `cyclePort`.

        Only available on Windows.

        Raises:
            FT2XXDeviceError: on error
        """
        status = FT_ResetPort(self._handle)
        if status != FT_OK:
            raise FT2XXDeviceError, status

    def cyclePort(self):
        """Send a cycle command to the USB port.

        The effect of this function is the same as disconnecting then reconnecting the device from USB. Possible
        use of this function is situations where a fatal error has occurred and it is difficult, or not possible, to
        recover without unplugging and replugging the USB cable. This function can also be used after reprogramming
        the EEPROM to force the FTDI device to read the new EEPROM contents which would otherwise require a physical
        disconnect-reconnect.
        As the current session is not restored when the driver is reloaded, the application must be able to recover
        after calling this function. It is ithe responisbility of the application to close the handle after successfully
        calling FT_CyclePort.
        For FT4232H, FT2232H and FT2232 devices, FT_CyclePort will only work under Windows XP and later.

        Only available on Windows.

        Raises:
            FT2XXDeviceError: on error
        """
        status = FT_CyclePort(self._handle)
        if status != FT_OK:
            raise FT2XXDeviceError, status

    def setUSBParameters(self, inTransferSize, outTransferSize):
        """Set the USB request transfer size.

        Previously, USB request transfer sizes have been set at 4096 bytes and have not been configurable.
        This function can be used to change the transfer sizes to better suit the application requirements.
        Transfer sizes must be set to a multiple of 64 bytes between 64 bytes and 64k bytes.

        When setUSBParameters() is called, the change comes into effect immediately and any data that was held
        in the driver at the time of the change is lost.

        Note that, at present, only dwInTransferSize is supported.

        Args:
            inTransferSize (:obj:`int`): Transfer size for USB IN request.
            outTransferSize (:obj:`int`): Transfer size for USB OUT request.

        Raises:
            FT2XXDeviceError: on error
        """
        status = FT_SetUSBParameters(self._handle, inTransferSize, outTransferSize)
        if status != FT_OK:
            raise FT2XXDeviceError, status

    def gpio_Init(self, *args, gpio0=Dir.INPUT, gpio1=Dir.INPUT, gpio2=Dir.INPUT, gpio3=Dir.INPUT):
        """Initialize the GPIO interface.

        Args:
            *args (:obj:`list` of :obj:`ft4222.GPIO.Dir`, optional): List containing a direction for each port.
            gpio0 (:obj:`ft4222.GPIO.Dir`, optional): Direction of gpio0
            gpio1 (:obj:`ft4222.GPIO.Dir`, optional): Direction of gpio1
            gpio2 (:obj:`ft4222.GPIO.Dir`, optional): Direction of gpio2
            gpio3 (:obj:`ft4222.GPIO.Dir`, optional): Direction of gpio3

        Raises:
            FT4222DeviceError: on error

        """
        cdef:
            GPIO_Dir ioDir[4]
        if len(args) > 0:
            for i in xrange(len(args)):
                ioDir[i] = args[i]
            for i in xrange(len(args), 4 - len(args)):
                ioDir[i] = GPIO_INPUT
        else:
            ioDir[0] = gpio0
            ioDir[1] = gpio1
            ioDir[2] = gpio2
            ioDir[3] = gpio3
        status = FT4222_GPIO_Init(self._handle, ioDir)
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def gpio_Read(self, portNum):
        """Read value from selected GPIO

        Args:
            portNum (:obj:`ft4222.GPIO.Port`): GPIO Port number

        Returns:
            bool: True if high, False otherwise

        Raises:
            FT4222DeviceError: on error

        """
        cdef:
            BOOL value
        status = FT4222_GPIO_Read(self._handle, portNum, &value)
        if status == FT4222_OK:
            return value
        raise FT4222DeviceError, status

    def gpio_Wait(self, portNum, expectedValue, timeout=0, sleep=1):
        """Blocks until the selected GPIO reaches a certain value.

        Will release the GIL while waiting.

        Args:
            portNum (:obj:`ft4222.GPIO.Port`): GPIO Port number
            expectedValue (bool): True for high, False for low
            timeout (int): timeout in milliseconds, or 0 for no timeout
            sleep (int): sleep time in milliseconds between each polling attempt, or 0 for no sleep

        Raises:
            FT4222DeviceError: on error
            TimeoutError: when timeout is exceeded

        """
        cdef:
            BOOL value
            FT4222_STATUS status
            GPIO_Port portNum_c = portNum
            BOOL expectedValue_c = expectedValue
            clock_t start = clock()
            int timeout_c = timeout
            int sleep_c = sleep

        with nogil:
            while True:
                if timeout_c > 0 and (clock() - start) / (CLOCKS_PER_SEC / 1000) > timeout_c:
                    raise TimeoutError

                status = FT4222_GPIO_Read(self._handle, portNum_c, &value)
                if status == FT4222_OK:
                    if value == expectedValue_c:
                        break
                else:
                    raise FT4222DeviceError, status

                if sleep_c > 0:
                    msleep(sleep_c)

    def gpio_Write(self, portNum, value):
        """Write value to given GPIO

        Args:
            portNum (:obj:`ft4222.GPIO.Port`): GPIO Port number
            value (bool): True for high, False for low

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_GPIO_Write(self._handle, portNum, value)
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def gpio_SetInputTrigger(self, portNum, trigger):
        """Set software trigger conditions on the specified GPIO pin.

        Args:
            portNum (:obj:`ft4222.GPIO.Port`): GPIO Port number
            trigger (:obj:`ft4222.GPIO.Trigger`): Combination of trigger conditions

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_GPIO_SetInputTrigger(self._handle, portNum, trigger)
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def gpio_GetTriggerStatus(self, portNum):
        """Get the size of trigger event queue.

        Args:
            portNum (:obj:`ft4222.GPIO.Port`): GPIO Port number

        Returns:
            int: Size of the trigger queue

        Raises:
            FT4222DeviceError: on error

        """
        cdef:
            uint16 queueSize
        status = FT4222_GPIO_GetTriggerStatus(self._handle, portNum, &queueSize)
        if status == FT4222_OK:
            return queueSize
        raise FT4222DeviceError, status

    def gpio_ReadTriggerQueue(self, portNum, readSize=None):
        """Get events recorded in the trigger event queue.

        Args:
            portNum (:obj:`ft4222.GPIO.Port`): GPIO Port number
            readSize (:obj:`int`, optional): Size of the queue, :obj:`gpio_GetTriggerStatus()` gets called if omitted

        Returns:
            :obj:`list` of :obj:`ft4222.GPIO.Trigger`: Trigger queue as list

        Raises:
            FT4222DeviceError: on error

        """
        if readSize == None:
            readSize = self.gpio_GetTriggerStatus(portNum)
        cdef:
            GPIO_Trigger *events = <GPIO_Trigger*>alloca(portNum * sizeof(GPIO_Trigger))
            uint16 sizeRead
        status = FT4222_GPIO_ReadTriggerQueue(self._handle, portNum, events, readSize, &sizeRead)
        if status == FT4222_OK:
            res = []
            for i in xrange(readSize):
                res.append(Trigger(events[i]))
            return res
        raise FT4222DeviceError, status


    def i2cMaster_Init(self, kbps=100):
        """Initialize the FT4222H as an I2C master with the requested I2C speed.

        Args:
            kbps (int): Speed in kb/s

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_I2CMaster_Init(self._handle, kbps)
        if status != FT4222_OK:
            raise FT4222DeviceError, status
        # current version (v1.3) of ftdi's lib can only handle clock rates down to 60kHz
        # although the chip can handle clock rates down to ~23.6kHz
        # there's a undocumented ways to achieve this
        if kbps < 60:
            #             Operating Clock Freq
            # SCL Freq = -----------------------  | M = 6 or 8; N = 1, 2, 3, …, 127
            #                 M*(N+1)
            #
            #       Operating Clock Freq             24MHz
            # N =  ---------------------- - 1   => ---------- - 1
            #            M * SCL Freq               8 * kbps
            #
            n = max(min(int(round(24000000.0 / (8 * 1000 * kbps) - 1)), 127), 1)
            self.setClock(SysClock.CLK_24)
            self.vendorCmdSet(0x52, n)

    def i2cMaster_Read(self, addr, bytesToRead):
        """Read data from the specified I2C slave device with START and STOP conditions.

        Args:
            addr (int): I2C slave address
            bytesToRead (int): Number of bytes to read from slave

        Returns:
            bytes: Bytes read from slave

        Raises:
            FT4222DeviceError: on error

        """
        cdef:
            array[uint8] buf = array('B', [])
            uint16 bytesRead
        resize(buf, bytesToRead)
        status = FT4222_I2CMaster_Read(self._handle, addr, buf.data.as_uchars, bytesToRead, &bytesRead)
        resize(buf, bytesRead)
        if status == FT4222_OK:
            return bytes(buf)
        raise FT4222DeviceError, status

    def i2cMaster_Write(self, addr, data):
        """Write data to the specified I2C slave device with START and STOP conditions.

        Args:
            addr (int): I2C slave address
            data (int, bytes, bytearray): Data to write to slave

        Returns:
            int: Bytes sent to slave

        Raises:
            FT4222DeviceError: on error

        """
        if isinstance(data, int):
            data = bytes([data])
        elif not isinstance(data, (bytes, bytearray)):
            raise TypeError("the data argument must be of type 'int', 'bytes' or 'bytearray'")
        cdef:
            uint16 bytesSent
            uint8* cdata = data
        status = FT4222_I2CMaster_Write(self._handle, addr, cdata, len(data), &bytesSent)
        if status == FT4222_OK:
            return bytesSent
        raise FT4222DeviceError, status

    def i2cMaster_ReadEx(self, addr, flag, bytesToRead):
        """Read data from the specified I2C slave device with the specified I2C condition.

        Args:
            addr (int): I2C slave address
            flag (:obj:`ft4222.I2CMaster.Flag`): Flag to control start- and stopbit generation
            bytesToRead (int): Number of bytes to read from slave

        Returns:
            bytes: Bytes read from slave

        Raises:
            FT4222DeviceError: on error

        """
        cdef:
            array[uint8] buf = array('B', [])
            uint16 bytesRead
        resize(buf, bytesToRead)
        status = FT4222_I2CMaster_ReadEx(self._handle, addr, flag, buf.data.as_uchars, bytesToRead, &bytesRead)
        resize(buf, bytesRead)
        if status == FT4222_OK:
            return bytes(buf)
        raise FT4222DeviceError, status

    def i2cMaster_WriteEx(self, addr, flag, data):
        """Write data to the specified I2C slave device with the specified I2C condition.

        Args:
            addr (int): I2C slave address
            flag (:obj:`ft4222.I2CMaster.Flag`): Flag to control start- and stopbit generation
            data (int, bytes, bytearray): Data to write to slave

        Returns:
            int: Bytes sent to slave

        Raises:
            FT4222DeviceError: on error

        """
        if isinstance(data, int):
            data = bytes([data])
        elif not isinstance(data, (bytes, bytearray)):
            raise TypeError("the data argument must be of type 'int', 'bytes' or 'bytearray'")
        cdef:
            uint16 bytesSent
            uint8* cdata = data
        status = FT4222_I2CMaster_WriteEx(self._handle, addr, flag, cdata, len(data), &bytesSent)
        if status == FT4222_OK:
            return bytesSent
        raise FT4222DeviceError, status

    def i2cMaster_Reset(self):
        """Reset the I2C master device.

        If the I2C bus encounters errors or works abnormally, this function will reset the I2C device.
        It is not necessary to call I2CMaster_Init again after calling this reset function.

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_I2CMaster_Reset(self._handle)
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def i2cMaster_GetStatus(self):
        """Read the status of the I2C master controller.

        This can be used to poll a slave until its write-cycle is complete.

        Returns:
            :obj:`ft4222.I2CMaster.ControllerStatus`: Controller status

        Raises:
            FT4222DeviceError: on error

        """
        cdef uint8 cs
        status = FT4222_I2CMaster_GetStatus(self._handle, &cs)
        if status == FT4222_OK:
            return ControllerStatus(cs)
        raise FT4222DeviceError, status


    def i2cSlave_Init(self):
        """Initialize the FT4222H as an I2C slave device (default address 0x40).

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_I2CSlave_Init(self._handle)
        if status != FT4222_OK:
            raise FT4222DeviceError(status)

    def i2cSlave_GetAddress(self):
        """Get the current address of the I2C slave device.

        Returns:
            int: current slave address

        Raises:
            FT4222DeviceError: on error

        """
        cdef uint8 addr
        status = FT4222_I2CSlave_GetAddress(self._handle, &addr)
        if status != FT4222_OK:
            raise FT4222DeviceError(status)
        return addr

    def i2cSlave_SetAddress(self, addr):
        """Set the address of the I2C slave device.

        Args:
            addr (int): new I2C slave address

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_I2CSlave_SetAddress(self._handle, addr)
        if status != FT4222_OK:
            raise FT4222DeviceError(status)

    def i2cSlave_GetRxStatus(self):
        """Get the number of bytes in the receive queue.

        Returns:
            int: number of bytes in receive queue

        Raises:
            FT4222DeviceError: on error

        """
        cdef uint16 rxSize
        status = FT4222_I2CSlave_GetRxStatus(self._handle, &rxSize)
        if status != FT4222_OK:
            raise FT4222DeviceError(status)
        return rxSize

    def i2cSlave_Read(self, bytesToRead):
        """Read data from the buffer of the I2C slave device.

        Args:
            bytesToRead (int): number of bytes to read from slave device buffer

        Returns:
            bytes: data read from the slave device buffer

        Raises:
            FT4222DeviceError: on error

        """
        cdef array[uint8] buf = array('B', [])
        cdef uint16 bytesRead
        resize(buf, bytesToRead)

        status = FT4222_I2CSlave_Read(self._handle, buf.data.as_uchars, bytesToRead, &bytesRead)
        if status != FT4222_OK:
            raise FT4222DeviceError(status)

        resize(buf, bytesRead)
        return bytes(buf)

    def i2cSlave_Write(self, data):
        """Write data to the buffer of the I2C slave device.

        Args:
            data (int, bytes, bytearray): data to write to I2C slave device buffer

        Returns:
            int: number of bytes written to the I2C slave device buffer

        Raises:
            FT4222DeviceError: on error

        """
        if isinstance(data, int):
            data = bytes([data])
        elif not isinstance(data, (bytes, bytearray)):
            raise TypeError("The data argument must be of type 'int', 'bytes' or 'bytearray'")

        cdef uint16 bytesSent
        cdef uint8* cdata = <uint8*> data

        status = FT4222_I2CSlave_Write(self._handle, cdata, <uint16> len(data), &bytesSent)
        if status != FT4222_OK:
            raise FT4222DeviceError(status)
        return bytesSent

    def i2cSlave_Reset(self):
        """Reset the I2C slave device.

        Maintains slave address, response word, and clock stretch enable.
        Clears any queued RX or TX buffer data.

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_I2CSlave_Reset(self._handle)
        if status != FT4222_OK:
            raise FT4222DeviceError(status)

    def i2cSlave_SetClockStretch(self, enable):
        """Enable or disable I2C clock stretch (default disabled).

        Only supported on chip revisions C & D

        Args:
            enable (bool): enable clock stretch

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_I2CSlave_SetClockStretch(self._handle, enable)
        if status != FT4222_OK:
            raise FT4222DeviceError(status)

    def i2cSlave_SetRespWord(self, response):
        """Response from I2C slave device when the device is not ready (default 0xFF).

        Only takes effect when clock stretch is disabled.
        Only supported on chip revisions C & D.

        Args:
            response (int): default response byte value

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_I2CSlave_SetRespWord(self._handle, response)
        if status != FT4222_OK:
            raise FT4222DeviceError(status)

    def spi_Reset(self):
        """Reset the SPI master or slave device

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_SPI_Reset(self._handle);
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def spi_ResetTransaction(self, spiIdx):
        """Reset the SPI transaction

        Args:
            spiIdx (int): The index of the SPI transaction, which ranges from 0~3 depending on the mode of the chip.

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_SPI_ResetTransaction(self._handle, spiIdx);
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def spi_SetDrivingStrength(self, clkStrength, ioStrength, ssoStrength):
        """Reset the SPI master or slave device.

        Args:
            clkStrength (:obj:`ft4222.SPI.DrivingStrength`): Driving strength clock pin (master only)
            ioStrength (:obj:`ft4222.SPI.DrivingStrength`): Driving strength io pin
            ssoStrength (:obj:`ft4222.SPI.DrivingStrength`): Driving strength sso pin (master only)

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_SPI_SetDrivingStrength(self._handle, clkStrength, ioStrength, ssoStrength);
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def spiMaster_Init(self, mode, clock, cpol, cpha, ssoMap):
        """Initialize as an SPI master under all modes.

        Args:
            mode (:obj:`ft4222.SPIMaster.Mode`): SPI transmission lines / mode
            clock (:obj:`ft4222.SPIMaster.Clock`): Clock divider
            cpol (:obj:`ft4222.SPI.Cpol`): Clock polarity
            cpha (:obj:`ft4222.SPI.Cpha`): Clock phase
            ssoMap (:obj:`ft4222.SPIMaster.SlaveSelect`): Slave selection output pins

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_SPIMaster_Init(self._handle, mode, clock, cpol, cpha, ssoMap);
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def spiMaster_SetLines(self, mode):
        """Switch the FT4222H SPI master to single, dual, or quad mode.

        This overrides the mode passed to FT4222_SPIMaster_init. This might be needed if a
        device accepts commands in single mode but data transfer is to use dual or quad mode.

        Args:
            mode (:obj:`ft4222.SPIMaster.Mode`): SPI transmission lines / mode

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_SPIMaster_SetLines(self._handle, mode);
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def spiMaster_SingleRead(self, bytesToRead, isEndTransaction):
        """Read data from a SPI slave in single mode

        Args:
            bytesToRead (int): Number of bytes to read
            isEndTransaction (bool): If True the slave select pin will be raised at the end

        Returns:
            bytes: Bytes read from slave

        Raises:
            FT4222DeviceError: on error

        """
        cdef:
            array[uint8] buf = array('B', [])
            uint16 bytesRead
        resize(buf, bytesToRead)
        status = FT4222_SPIMaster_SingleRead(self._handle, buf.data.as_uchars, bytesToRead, &bytesRead, isEndTransaction)
        if status == FT4222_OK:
            resize(buf, bytesRead)
            return bytes(buf)
        raise FT4222DeviceError, status

    def spiMaster_SingleWrite(self, data, isEndTransaction):
        """Write data to a SPI slave in single mode

        Args:
            data (bytes, bytearray, int): Data to write to slave
            isEndTransaction (bool): If True the slave select pin will be raised at the end

        Returns:
            int: Bytes sent to slave

        Raises:
            FT4222DeviceError: on error

        """
        if isinstance(data, int):
            data = bytes([data])
        elif not isinstance(data, (bytes, bytearray)):
            raise TypeError("the data argument must be of type 'int', 'bytes' or 'bytearray'")
        cdef:
            uint16 bytesSent
            uint8* cdata = data
        status = FT4222_SPIMaster_SingleWrite(self._handle, cdata, len(data), &bytesSent, isEndTransaction);
        if status == FT4222_OK:
            return bytesSent
        raise FT4222DeviceError, status

    def spiMaster_SingleReadWrite(self, data, isEndTransaction):
        """Write and read data to and from a SPI slave in single mode

        Args:
            data (bytes, bytearray, int): Data to write to slave
            isEndTransaction (bool): If True the slave select pin will be raised at the end

        Returns:
            bytes: Bytes read from slave

        Raises:
            FT4222DeviceError: on error

        """
        if isinstance(data, int):
            data = bytes([data])
        elif not isinstance(data, (bytes, bytearray)):
            raise TypeError("the data argument must be of type 'int', 'bytes' or 'bytearray'")
        cdef:
            uint16 sizeTransferred
            uint8* cdata = data
            array[uint8] buf = array('B', [])
        resize(buf, len(data))
        status = FT4222_SPIMaster_SingleReadWrite(self._handle, buf.data.as_uchars, cdata, len(data), &sizeTransferred, isEndTransaction);
        if status == FT4222_OK:
            resize(buf, sizeTransferred)
            return bytes(buf)
        raise FT4222DeviceError, status

    def spiMaster_MultiReadWrite(self, singleWrite, multiWrite, bytesToRead):
        """Write and read data to and from a SPI slave in dual- or quad-mode (multi-mode).

        Args:
            singleWrite (bytes, bytearray, int): Data to write to slave in signle-line mode (max. 15 bytes)
            multiWrite (bytes, bytearray, int): Data to write to slave in multi-line mode (max. 65535 bytes)
            bytesToRead (int):  Number of bytes to read on multi-line (max. 65535 bytes)

        Returns:
            bytes: Bytes read from slave in multi-line mode

        Raises:
            FT4222DeviceError: on error

        """
        if isinstance(singleWrite, int):
            singleWrite = bytes([singleWrite])
        elif not isinstance(singleWrite, (bytes, bytearray)):
            raise TypeError("the singleWrite argument must be of type 'int', 'bytes' or 'bytearray'")
        if isinstance(multiWrite, int):
            multiWrite = bytes([multiWrite])
        elif not isinstance(multiWrite, (bytes, bytearray)):
            raise TypeError("the multiWrite argument must be of type 'int', 'bytes' or 'bytearray'")
        write = singleWrite + multiWrite
        cdef:
            uint8* cdata = write
            array[uint8] buf = array('B', [])
            uint32 bytesRead
        resize(buf, bytesToRead)
        status = FT4222_SPIMaster_MultiReadWrite(self._handle, buf.data.as_uchars, cdata, len(singleWrite), len(multiWrite), bytesToRead, &bytesRead);
        if status == FT4222_OK:
            resize(buf, bytesRead)
            return bytes(buf)
        raise FT4222DeviceError, status

    def spiMaster_EndTransaction(self):
        """End the current SPI transaction.

        Raises:
            FT4222DeviceError: on error

        """
        cdef:
            DWORD bytesSent;
        status = FT_Write(self._handle, <unsigned char*>NULL, 0, &bytesSent);
        if status == FT_OK:
            return
        raise FT4222DeviceError, status

    def spiSlave_Init(self):
        """Initialize the FT4222H as an SPI slave. Default SPI_SlaveProtocol is SPI_SLAVE_WITH_PROTOCOL.

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_SPISlave_Init(self._handle);
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def spiSlave_InitEx(self, proto):
        """Initialize as an SPI slave under all modes.

        Args:
            mode (:obj:`ft4222.SPISlave.Protocol`): SPI slave protocol

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_SPISlave_InitEx(self._handle,proto);
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def spiSlave_Read(self, bytesToRead):
        """Read data from the receive queue of the SPI slave device.

        Args:
            bytesToRead (int): Number of bytes to read

        Returns:
            bytes: Bytes read from slave

        Raises:
            FT4222DeviceError: on error

        """
        cdef:
            array[uint8] buf = array('B', [])
            uint16 sizeRead
        resize(buf, bytesToRead)

        status = FT4222_SPISlave_Read(self._handle, buf.data.as_uchars, bytesToRead, &sizeRead);
        if status == FT4222_OK:
            resize(buf, sizeRead)
            return bytes(buf)
        raise FT4222DeviceError, status

    def spiSlave_SetMode(self, cpol, cpha):
        """Set SPI slave cpol and cpha. The Default value of cpol is (:obj:`ft4222.SPI.Cpol.CLK_IDLE_LOW`) , default value of cpha is (:obj:`ft4222.SPI.Cpol.CLK_LEADING`)

        Args:
            cpol (:obj:`ft4222.SPI.Cpol`): Clock polarity
            cpha (:obj:`ft4222.SPI.Cpha`): Clock phase

        Raises:
            FT4222DeviceError: on error

        """
        status = FT4222_SPISlave_SetMode(self._handle, cpol, cpha);
        if status != FT4222_OK:
            raise FT4222DeviceError, status

    def spiSlave_GetRxStatus(self):
        """Get number of bytes in the receive queue.

        Returns:
            pRxSize (uint16): Number of bytes in the receive queue

        Raises:
            FT4222DeviceError: on error

        """
        cdef:
            uint16 pRxSize

        status = FT4222_SPISlave_GetRxStatus(self._handle, &pRxSize);

        if status == FT4222_OK:
            return pRxSize
        raise FT4222DeviceError, status

    def spiSlave_Write(self, data):
        """Write data to the transmit queue of the SPI slave device.

        Args:
            data (bytes, bytearray, int): Data to write to slave

        Returns:
            sizeTransferred (uint16): Number of bytes written to the device.

        Raises:
            FT4222DeviceError: on error

        """
        if isinstance(data, int):
            data = bytes([data])
        elif not isinstance(data, (bytes, bytearray)):
            raise TypeError("the data argument must be of type 'int', 'bytes' or 'bytearray'")
        cdef:
            uint16 sizeTransferred
            uint8* cdata = data

        status = FT4222_SPISlave_Write(self._handle, cdata, len(data), &sizeTransferred);
        if status == FT4222_OK:
            return sizeTransferred
        raise FT4222DeviceError, status
