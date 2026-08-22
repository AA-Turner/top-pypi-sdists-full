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
from Phidget22.CodeInfo import CodeInfo
from Phidget22.CodeInfo import _CCodeInfo
from Phidget22.IRCodeEncoding import IRCodeEncoding
from Phidget22.IRCodeLength import IRCodeLength
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class IR(Phidget):
    r"""IR Channel class.

    The Infrared Remote class lets you read and transmit command codes from infrared remotes that
    the majority of household appliances use. You can use this class to construct and transmit
    commands from scratch, or learn and retransmit codes from the remote controller of your
    appliance.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._CodeFactory = ctypes.WINFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_char_p,
                ctypes.c_uint32,
                ctypes.c_int,
            )
        else:
            self._CodeFactory = ctypes.CFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_char_p,
                ctypes.c_uint32,
                ctypes.c_int,
            )
        self._Code = None
        self._onCode = None

        if sys.platform == "win32":
            self._LearnFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(_CCodeInfo)
            )
        else:
            self._LearnFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(_CCodeInfo)
            )
        self._Learn = None
        self._onLearn = None

        if sys.platform == "win32":
            self._RawDataFactory = ctypes.WINFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_int32),
                ctypes.c_size_t,
            )
        else:
            self._RawDataFactory = ctypes.CFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_int32),
                ctypes.c_size_t,
            )
        self._RawData = None
        self._onRawData = None

        __func = PhidgetSupport.getDll().PhidgetIR_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localCodeEvent(self, handle, userPtr, code, bitCount, isRepeat):
        if self._Code is None:
            return
        code = code.decode("utf-8")
        self._Code(self, code, bitCount, isRepeat)

    def setOnCodeHandler(self, handler):
        r"""Code event

        This event is fired every time a code is received and correctly decoded.

        *   The code is represented by a hexadecimal string (array of bytes) with a length of 1/4 of
        `bitCount`.
        *   The MSBit is considered to be the first bit received and will be in array index 0 of
        `code`
        *   Repeat will be true if a repeat is detected (either timing wise or via a repeat code)

        *   False repeasts can happen if two separate button presses happen close together

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *IR* - The object on which the event occurred.
            * **code** : *str* - The code string
            * **bitCount** : *int* - The length of the received code in bits
            * **isRepeat** : *bool* - 'true' if a repeat is detected

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._Code = handler

        if self._onCode is None:
            fptr = self._CodeFactory(self._localCodeEvent)
            __func = PhidgetSupport.getDll().PhidgetIR_setOnCodeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onCode = fptr

    def _localLearnEvent(self, handle, userPtr, code, codeInfo):
        if self._Learn is None:
            return
        code = code.decode("utf-8")
        if codeInfo is not None:
            codeInfo = codeInfo.contents._to_python()
        self._Learn(self, code, codeInfo)

    def setOnLearnHandler(self, handler):
        r"""Learn event

        This event fires when a button has been held down long enough for the channel to have
        learned the CodeInfo values

        *   A code is usually learned after 1 second, or after 4 repeats.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *IR* - The object on which the event occurred.
            * **code** : *str* - The code string
            * **codeInfo** : *CodeInfo* - Contains the data for characterizing the code.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._Learn = handler

        if self._onLearn is None:
            fptr = self._LearnFactory(self._localLearnEvent)
            __func = PhidgetSupport.getDll().PhidgetIR_setOnLearnHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onLearn = fptr

    def _localRawDataEvent(self, handle, userPtr, data, dataLen):
        if self._RawData is None:
            return
        data = [data[i] for i in range(dataLen)]
        self._RawData(self, data)

    def setOnRawDataHandler(self, handler):
        r"""RawData event

        This event will fire every time the channel gets more data

        *   This will happen at most once every 8ms.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *IR* - The object on which the event occurred.
            * **data** : *list[int]* - The data being received

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._RawData = handler

        if self._onRawData is None:
            fptr = self._RawDataFactory(self._localRawDataEvent)
            __func = PhidgetSupport.getDll().PhidgetIR_setOnRawDataHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onRawData = fptr

    def getLastCode(self):
        r"""
        The last code the channel has received.

        *   The code is represented by a hexadecimal string (array of bytes).

        Returns
        -------
        tuple (str, int)
            A tuple containing:
                - code: The last received code
                - bitCount: length of the received code in bits

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _code = (ctypes.c_char * 33)()
        _codeLen = ctypes.c_size_t(33)
        _bitCount = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetIR_getLastCode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_code), _codeLen, ctypes.byref(_bitCount))

        if result > 0:
            raise PhidgetException(result)
        assert _code.value is not None

        return _code.value.decode("utf-8"), _bitCount.value

    def getLastLearnedCode(self):
        r"""
        The last code the channel has learned.

        *   The code is represented by a hexadecimal string (array of bytes).
        *   The `codeInfo` structure holds data that describes the learned code.

        Returns
        -------
        tuple (str, CodeInfo)
            A tuple containing:
                - code: The last learned code
                - codeInfo: contains the data for characterizing the code

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _code = (ctypes.c_char * 33)()
        _codeLen = ctypes.c_size_t(33)
        _codeInfo = _CCodeInfo()

        __func = PhidgetSupport.getDll().PhidgetIR_getLastLearnedCode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_code), _codeLen, ctypes.byref(_codeInfo))

        if result > 0:
            raise PhidgetException(result)
        assert _code.value is not None

        return _code.value.decode("utf-8"), _codeInfo._to_python()

    def transmit(self, code, codeInfo):
        r"""
        Transmits a code

        *   `code` data is transmitted MSBit first.
        *   MSByte is in array index 0 of `code`
        *   LSBit is right justified, therefore, MSBit may be in bit position 0-7 (of array index 0)
        depending on the bit count.

        Parameters
        ----------
        code : str
            code data
        codeInfo : CodeInfo
            contains the data for characterizing the code.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _code = ctypes.create_string_buffer(code.encode("utf-8"))
        _codeInfo = _CCodeInfo._from_python(codeInfo)

        __func = PhidgetSupport.getDll().PhidgetIR_transmit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _code, ctypes.byref(_codeInfo))

        if result > 0:
            raise PhidgetException(result)

    def transmitRaw(self, data, carrierFrequency, dutyCycle, gap):
        r"""
        Transmits **raw** data as a series of pulses and spaces.

        *   `data` must start and end with a pulse.

        *   Each element is a positive time in μs
        *   `dataLength` has a maximum length of 200, however, streams should be kept must shorter
        than this (less than 100ms between gaps).

        *   `dataLength` must be an odd number

        *   Leave `carrierFrequency` as 0 for default.

        *   `carrierFrequency` has a range of 10kHz - 1MHz

        *   Leave `dutyCycle` as 0 for default

        *   `dutyCycle` can have a value between 0.1 and 0.5

        *   Specifying a `gap` will guarantee a gap time (no transmitting) after data is sent.

        *   gap time is in μs
        *   gap time can be set to 0

        Parameters
        ----------
        data : Sequence[int]
            data to send.
        carrierFrequency : int
            carrier frequency in Hz
        dutyCycle : float
            the duty cycle
        gap : int
            the gap time in μs

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _data = (ctypes.c_uint32 * len(data))(*data)
        _dataLen = ctypes.c_size_t(len(data))
        _carrierFrequency = ctypes.c_uint32(carrierFrequency)
        _dutyCycle = ctypes.c_double(dutyCycle)
        _gap = ctypes.c_uint32(gap)

        __func = PhidgetSupport.getDll().PhidgetIR_transmitRaw
        __func.restype = ctypes.c_int32
        result = __func(
            self._handle, ctypes.byref(_data), _dataLen, _carrierFrequency, _dutyCycle, _gap
        )

        if result > 0:
            raise PhidgetException(result)

    def transmitRepeat(self):
        r"""
        Transmits a repeat of the last transmited code.

        *   Depending on the CodeInfo structure, this may be a retransmission of the code itself, or
        there may be a special repeat code.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetIR_transmitRepeat
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    RAW_DATA_LONG_SPACE = 4294967295
    """The value for a long space in raw data"""

    IR_MAX_CODE_BIT_COUNT = 128
    """Maximum bit count for sent / received data"""

    IR_MAX_CODE_STR_LENGTH = 33
    """Maximum bit count for sent / received data"""


__all__ = ["IR", "CodeInfo", "IRCodeEncoding", "IRCodeLength", "PhidgetException", "Phidget"]
