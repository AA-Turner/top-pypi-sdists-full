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

import ctypes
from Phidget22._phidget_support import PhidgetSupport
from Phidget22.HubPortMode import HubPortMode
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class Hub(Phidget):
    r"""Hub Channel class.

    The hub class allows you to control power to VINT hub ports.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        __func = PhidgetSupport.getDll().PhidgetHub_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _setFirmwareUpgradeFlag(self, port, timeout):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Sets a flag on this hub port which forces the next VINT devices plugged in to stay in
        firmware upgrade mode.

        Parameters
        ----------
        port : int
            The port the device is plugged into
        timeout : int
            The time to leave the flag set for

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _port = ctypes.c_int(port)
        _timeout = ctypes.c_uint32(timeout)

        __func = PhidgetSupport.getDll().PhidgetHub_setFirmwareUpgradeFlag
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _port, _timeout)

        if result > 0:
            raise PhidgetException(result)

    def setPortAutoSetSpeed(self, port, state):
        r"""
        Enables / disables Auto Set Speed on the hub port. When enabled, and a supported VINT device
        is attached, the **HubPortSpeed** will automatically be set to the fastest reliable speed.
        This is enabled by default on supported VINT Hubs.

        Parameters
        ----------
        port : int
            The Hub port
        state : bool
            The AutoSetSpeed state

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _port = ctypes.c_int(port)
        _state = ctypes.c_int(state)

        __func = PhidgetSupport.getDll().PhidgetHub_setPortAutoSetSpeed
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _port, _state)

        if result > 0:
            raise PhidgetException(result)

    def getPortMaxSpeed(self, port):
        r"""
        The max communication speed of a high-speed capable VINT Port.

        Parameters
        ----------
        port : int
            The Hub port

        Returns
        -------
        int
            The max speed

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _port = ctypes.c_int(port)
        _state = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetHub_getPortMaxSpeed
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _port, ctypes.byref(_state))

        if result > 0:
            raise PhidgetException(result)

        return _state.value

    def getPortMode(self, port):
        r"""
        Gets the mode of the selected hub port. VINT devices will not show up when the port is in
        digital/analog mode.

        Parameters
        ----------
        port : int
            The port being read

        Returns
        -------
        HubPortMode
            The mode the port is in

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _port = ctypes.c_int(port)
        _mode = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetHub_getPortMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _port, ctypes.byref(_mode))

        if result > 0:
            raise PhidgetException(result)

        return HubPortMode(_mode.value)

    def setPortMode(self, port, mode):
        r"""
        Sets the mode of the selected port. This could be used to set a port back to VINT mode if it
        was left in digital/analog mode.

        Parameters
        ----------
        port : int
            The port being set
        mode : HubPortMode
            The mode the port is being set to

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _port = ctypes.c_int(port)
        _mode = ctypes.c_int(mode)

        __func = PhidgetSupport.getDll().PhidgetHub_setPortMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _port, _mode)

        if result > 0:
            raise PhidgetException(result)

    def getPortPower(self, port):
        r"""
        Gets the VINT Hub Port power state

        Parameters
        ----------
        port : int
            The Hub port

        Returns
        -------
        bool
            The power state

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _port = ctypes.c_int(port)
        _state = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetHub_getPortPower
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _port, ctypes.byref(_state))

        if result > 0:
            raise PhidgetException(result)

        return bool(_state.value)

    def setPortPower(self, port, state):
        r"""
        Controls power to the VINT Hub Port.

        Parameters
        ----------
        port : int
            The Hub port
        state : bool
            The power state

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _port = ctypes.c_int(port)
        _state = ctypes.c_int(state)

        __func = PhidgetSupport.getDll().PhidgetHub_setPortPower
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _port, _state)

        if result > 0:
            raise PhidgetException(result)

    def getPortSupportsAutoSetSpeed(self, port):
        r"""
        Indicates that this VINT Port support Auto Set Speed.

        Parameters
        ----------
        port : int
            The Hub port

        Returns
        -------
        bool
            The supported state

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _port = ctypes.c_int(port)
        _state = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetHub_getPortSupportsAutoSetSpeed
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _port, ctypes.byref(_state))

        if result > 0:
            raise PhidgetException(result)

        return bool(_state.value)

    def getPortSupportsSetSpeed(self, port):
        r"""
        Indicates that the communication speed of this VINT port can be set.

        Parameters
        ----------
        port : int
            The Hub port

        Returns
        -------
        bool
            The supported state

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _port = ctypes.c_int(port)
        _state = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetHub_getPortSupportsSetSpeed
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _port, ctypes.byref(_state))

        if result > 0:
            raise PhidgetException(result)

        return bool(_state.value)


__all__ = ["Hub", "HubPortMode", "PhidgetException", "Phidget"]
