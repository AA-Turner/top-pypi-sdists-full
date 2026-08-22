# coding=utf-8
# Copyright (c) 2015-2026 Phidgets Inc.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import ctypes
from Phidget22._phidget_support import PhidgetSupport
from Phidget22._native_async_support import AsyncSupport
from Phidget22.ErrorCode import ErrorCode
from Phidget22.DataAdapterVoltage import DataAdapterVoltage
from Phidget22.DataAdapterEndianness import DataAdapterEndianness
from Phidget22.DataAdapterFrequency import DataAdapterFrequency
from Phidget22.DataAdapterSPIChipSelect import DataAdapterSPIChipSelect
from Phidget22.DataAdapterSPIMode import DataAdapterSPIMode
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class DataAdapter(Phidget):
    r"""DataAdapter Channel class.

    The Data Adapter class is used to interface third party devices and microcontrollers with
    Phidgets.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def getDataAdapterVoltage(self):
        r"""
        The voltage used to communicate with and power the external device.

        Returns
        -------
        DataAdapterVoltage
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DataAdapterVoltage = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_getDataAdapterVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataAdapterVoltage))

        if result > 0:
            raise PhidgetException(result)

        return DataAdapterVoltage(_DataAdapterVoltage.value)

    def setDataAdapterVoltage(self, DataAdapterVoltage):
        r"""
        The voltage used to communicate with and power the external device.

        Parameters
        ----------
        DataAdapterVoltage : DataAdapterVoltage
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DataAdapterVoltage = ctypes.c_int(DataAdapterVoltage)

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_setDataAdapterVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _DataAdapterVoltage)

        if result > 0:
            raise PhidgetException(result)

    def getDataBits(self):
        r"""
        Configures the number of data bits used for communication. Refer to the documentation for
        the device you are communicating with.

        Returns
        -------
        int
            The number of data bits

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DataBits = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_getDataBits
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataBits))

        if result > 0:
            raise PhidgetException(result)

        return _DataBits.value

    def setDataBits(self, DataBits):
        r"""
        Configures the number of data bits used for communication. Refer to the documentation for
        the device you are communicating with.

        Parameters
        ----------
        DataBits : int
            The number of data bits

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DataBits = ctypes.c_uint32(DataBits)

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_setDataBits
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _DataBits)

        if result > 0:
            raise PhidgetException(result)

    def getMinDataBits(self):
        r"""
        The minimum number of data bits

        Returns
        -------
        int
            The number of data bits

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinDataBits = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_getMinDataBits
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinDataBits))

        if result > 0:
            raise PhidgetException(result)

        return _MinDataBits.value

    def getMaxDataBits(self):
        r"""
        The maximum number of data bits

        Returns
        -------
        int
            The number of data bits

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxDataBits = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_getMaxDataBits
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataBits))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataBits.value

    def getEndianness(self):
        r"""
        Configures endianness of each byte.

        Returns
        -------
        DataAdapterEndianness
            The endianness of the data bytes.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Endianness = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_getEndianness
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Endianness))

        if result > 0:
            raise PhidgetException(result)

        return DataAdapterEndianness(_Endianness.value)

    def setEndianness(self, Endianness):
        r"""
        Configures endianness of each byte.

        Parameters
        ----------
        Endianness : DataAdapterEndianness
            The endianness of the data bytes.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Endianness = ctypes.c_int(Endianness)

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_setEndianness
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Endianness)

        if result > 0:
            raise PhidgetException(result)

    def getFrequency(self):
        r"""
        The rate at which data is transmitted over the communication lines in bits per second.

        Returns
        -------
        DataAdapterFrequency
            The communication frequency to use for future data transfers.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Frequency = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_getFrequency
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Frequency))

        if result > 0:
            raise PhidgetException(result)

        return DataAdapterFrequency(_Frequency.value)

    def setFrequency(self, Frequency):
        r"""
        The rate at which data is transmitted over the communication lines in bits per second.

        Parameters
        ----------
        Frequency : DataAdapterFrequency
            The communication frequency to use for future data transfers.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Frequency = ctypes.c_int(Frequency)

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_setFrequency
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Frequency)

        if result > 0:
            raise PhidgetException(result)

    def i2cComplexTransaction(self, address, I2CPacketString, data):
        r"""
                Initiates a set of write and read transactions to happen in quick succession.

                Parameters
                ----------
                address : int
                    The address of the I2C device
                I2CPacketString : str
                    Specify the bytes of your I2C packet using 's' for start, 'R' for read, 'T' for write, and 'p' for stop. Only one stop condition per call is supported.

        For example, if you wanted to write two bytes, generate a repeat start, write one more byte, then read three bytes, the string would be "sTTsTsRRRp".

        You can also use numbers to indicate the number of bytes, e.g. "sT2sTsR3p"
                data : bytes | Sequence[int]
                    The entire set of data to send, in order from first to last. The length of this data must match the total number of bytes specified to be sent in the **I2CPacketString**.

                Returns
                -------
                bytes
                    The received data. This will be made up of all 'R' bytes as specified in the **I2CPacketString**, in order from first to last.

                Raises
                ------
                PhidgetError
                    A Phidget error occurred.
        """
        _address = ctypes.c_int32(address)
        _I2CPacketString = ctypes.create_string_buffer(I2CPacketString.encode("utf-8"))
        _data = (ctypes.c_uint8 * len(data)).from_buffer_copy(bytearray(data))
        _dataLen = ctypes.c_size_t(len(data))
        _recvData = (ctypes.c_uint8 * 127)()
        _recvDataLen = ctypes.c_size_t(127)

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_i2cComplexTransaction
        __func.restype = ctypes.c_int32
        result = __func(
            self._handle,
            _address,
            _I2CPacketString,
            ctypes.byref(_data),
            _dataLen,
            ctypes.byref(_recvData),
            ctypes.byref(_recvDataLen),
        )

        if result > 0:
            raise PhidgetException(result)

        return ctypes.string_at(_recvData, _recvDataLen.value)

    def i2cSendReceive(self, address, data, receiveLength):
        r"""
        Write a number of bytes and immediately read a number of bytes over I2C.

        Parameters
        ----------
        address : int
            The address of the I2C device
        data : bytes | Sequence[int]
            The data to send.
        receiveLength : int
            The number of bytes to receive. Must be ≤ `MaxReceivePacketLength`.

        Returns
        -------
        bytes
            The received data.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _address = ctypes.c_int32(address)
        _data = (ctypes.c_uint8 * len(data)).from_buffer_copy(bytearray(data))
        _dataLen = ctypes.c_size_t(len(data))
        _recvData = (ctypes.c_uint8 * receiveLength)()
        _receiveLength = ctypes.c_size_t(receiveLength)

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_i2cSendReceive
        __func.restype = ctypes.c_int32
        result = __func(
            self._handle,
            _address,
            ctypes.byref(_data),
            _dataLen,
            ctypes.byref(_recvData),
            _receiveLength,
        )

        if result > 0:
            raise PhidgetException(result)

        return ctypes.string_at(_recvData, _receiveLength.value)

    def getMaxReceivePacketLength(self):
        r"""
        The maximum length of a packet that can be received in bytes.

        Returns
        -------
        int
            The maximum length of a received packet.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxReceivePacketLength = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_getMaxReceivePacketLength
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxReceivePacketLength))

        if result > 0:
            raise PhidgetException(result)

        return _MaxReceivePacketLength.value

    def sendPacket(self, data):
        r"""
        Transmits a packet of data using the selected protocol information on the corresponding
        communication terminals to any connected device(s).

        Parameters
        ----------
        data : bytes | Sequence[int]
            The data to send.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _data = (ctypes.c_uint8 * len(data)).from_buffer_copy(bytearray(data))
        _dataLen = ctypes.c_size_t(len(data))

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_sendPacket
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_data), _dataLen)

        if result > 0:
            raise PhidgetException(result)

    def sendPacket_async(self, data, asyncHandler):
        """
        Provided for Python2.7 compatibility. See sendPacketAsync for method details.
        """
        _data = (ctypes.c_uint8 * len(data)).from_buffer_copy(bytearray(data))
        _dataLen = ctypes.c_size_t(len(data))

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_sendPacket_async
        __func(self._handle, ctypes.byref(_data), _dataLen, _asyncHandler, _ctx)

    def sendPacketAsync(self, data):
        r"""
        Transmits a packet of data using the selected protocol information on the corresponding
        communication terminals to any connected device(s).

        Parameters
        ----------
        data : bytes | Sequence[int]
            The data to send.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.sendPacket_async, data)

    def getMaxSendPacketLength(self):
        r"""
        The maximum length of a packet that can be sent in bytes.

        Returns
        -------
        int
            The maximum length of a sent packet.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxSendPacketLength = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_getMaxSendPacketLength
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxSendPacketLength))

        if result > 0:
            raise PhidgetException(result)

        return _MaxSendPacketLength.value

    def sendPacketWaitResponse(self, data):
        r"""
        Sends a packet and waits for a corresponding response from the external device, until the
        timeout elapses.

        Parameters
        ----------
        data : bytes | Sequence[int]
            The data to send.

        Returns
        -------
        bytes
            The received data.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _data = (ctypes.c_uint8 * len(data)).from_buffer_copy(bytearray(data))
        _dataLen = ctypes.c_size_t(len(data))
        _recvData = (ctypes.c_uint8 * 1024)()
        _recvDataLen = ctypes.c_size_t(1024)

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_sendPacketWaitResponse
        __func.restype = ctypes.c_int32
        result = __func(
            self._handle,
            ctypes.byref(_data),
            _dataLen,
            ctypes.byref(_recvData),
            ctypes.byref(_recvDataLen),
        )

        if result > 0:
            raise PhidgetException(result)

        return ctypes.string_at(_recvData, _recvDataLen.value)

    def getSPIChipSelect(self):
        r"""
        Configures functionality of the SPI chip select pin

        Returns
        -------
        DataAdapterSPIChipSelect
            The SPI chip select polarity.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SPIChipSelect = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_getSPIChipSelect
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_SPIChipSelect))

        if result > 0:
            raise PhidgetException(result)

        return DataAdapterSPIChipSelect(_SPIChipSelect.value)

    def setSPIChipSelect(self, SPIChipSelect):
        r"""
        Configures functionality of the SPI chip select pin

        Parameters
        ----------
        SPIChipSelect : DataAdapterSPIChipSelect
            The SPI chip select polarity.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SPIChipSelect = ctypes.c_int(SPIChipSelect)

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_setSPIChipSelect
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _SPIChipSelect)

        if result > 0:
            raise PhidgetException(result)

    def getSPIMode(self):
        r"""
        Configures SCLK polarity and phase.

        Returns
        -------
        DataAdapterSPIMode
            The SPI mode.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SPIMode = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_getSPIMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_SPIMode))

        if result > 0:
            raise PhidgetException(result)

        return DataAdapterSPIMode(_SPIMode.value)

    def setSPIMode(self, SPIMode):
        r"""
        Configures SCLK polarity and phase.

        Parameters
        ----------
        SPIMode : DataAdapterSPIMode
            The SPI mode.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SPIMode = ctypes.c_int(SPIMode)

        __func = PhidgetSupport.getDll().PhidgetDataAdapter_setSPIMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _SPIMode)

        if result > 0:
            raise PhidgetException(result)


__all__ = [
    "ErrorCode",
    "DataAdapter",
    "DataAdapterVoltage",
    "DataAdapterEndianness",
    "DataAdapterFrequency",
    "DataAdapterSPIChipSelect",
    "DataAdapterSPIMode",
    "PhidgetException",
    "Phidget",
]
