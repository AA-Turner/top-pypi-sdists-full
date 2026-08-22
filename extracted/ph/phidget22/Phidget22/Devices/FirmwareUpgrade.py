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
from Phidget22.DeviceID import DeviceID
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class FirmwareUpgrade(Phidget):
    r"""FirmwareUpgrade Channel class.

    **THIS IS AN INTERNAL CLASS AND SHOULD NOT BE USED BY THE END USER.**

    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._ProgressChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._ProgressChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._ProgressChange = None
        self._onProgressChange = None

        __func = PhidgetSupport.getDll().PhidgetFirmwareUpgrade_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localProgressChangeEvent(self, handle, userPtr, progress):
        if self._ProgressChange is None:
            return
        self._ProgressChange(self, progress)

    def _setOnProgressChangeHandler(self, handler):
        r"""ProgressChange event

        Occurs on firmware upgrade progress.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *FirmwareUpgrade* - The object on which the event occurred.
            * **progress** : *float* - The progress, range is 0-1.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._ProgressChange = handler

        if self._onProgressChange is None:
            fptr = self._ProgressChangeFactory(self._localProgressChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetFirmwareUpgrade_setOnProgressChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onProgressChange = fptr

    def _getActualDeviceID(self):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        The Device ID of the actual device being upgraded.

        Returns
        -------
        DeviceID
            Device ID

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ActualDeviceID = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetFirmwareUpgrade_getActualDeviceID
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ActualDeviceID))

        if result > 0:
            raise PhidgetException(result)

        return DeviceID(_ActualDeviceID.value)

    def _getActualDeviceName(self):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        The name of the actual device being upgraded.

        Returns
        -------
        str
            Name of the device

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ActualDeviceName = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().PhidgetFirmwareUpgrade_getActualDeviceName
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ActualDeviceName))

        if result > 0:
            raise PhidgetException(result)
        assert _ActualDeviceName.value is not None

        return _ActualDeviceName.value.decode("utf-8")

    def _getActualDeviceSKU(self):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        The SKU of the actual device being upgraded.

        Returns
        -------
        str
            Device SKU

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ActualDeviceSKU = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().PhidgetFirmwareUpgrade_getActualDeviceSKU
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ActualDeviceSKU))

        if result > 0:
            raise PhidgetException(result)
        assert _ActualDeviceSKU.value is not None

        return _ActualDeviceSKU.value.decode("utf-8")

    def _getActualDeviceVersion(self):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        The firmware version of the actual device being upgraded.

        Returns
        -------
        int
            Firmware version

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ActualDeviceVersion = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetFirmwareUpgrade_getActualDeviceVersion
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ActualDeviceVersion))

        if result > 0:
            raise PhidgetException(result)

        return _ActualDeviceVersion.value

    def _getActualDeviceVINTID(self):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        The VINT ID of the actual device being upgraded.

        Returns
        -------
        int
            Device VINT ID

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ActualDeviceVINTID = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetFirmwareUpgrade_getActualDeviceVINTID
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ActualDeviceVINTID))

        if result > 0:
            raise PhidgetException(result)

        return _ActualDeviceVINTID.value

    def _getProgress(self):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        The progress of the firmware update, ranging from 0 to 1.

        Returns
        -------
        float
            Firmware update progress

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Progress = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetFirmwareUpgrade_getProgress
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Progress))

        if result > 0:
            raise PhidgetException(result)

        return _Progress.value

    def _sendFirmware(self, data):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Sends firmware data to the device being upgraded.

        Parameters
        ----------
        data : bytes | Sequence[int]
            Data being sent in the firmware update

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _data = (ctypes.c_uint8 * len(data)).from_buffer_copy(bytearray(data))
        _dataLen = ctypes.c_size_t(len(data))

        __func = PhidgetSupport.getDll().PhidgetFirmwareUpgrade_sendFirmware
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_data), _dataLen)

        if result > 0:
            raise PhidgetException(result)


__all__ = ["FirmwareUpgrade", "DeviceID", "PhidgetException", "Phidget"]
