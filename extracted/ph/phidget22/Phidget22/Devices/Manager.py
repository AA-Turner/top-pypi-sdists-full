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
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class Manager:
    r"""Manager  class.

    The Phidget Manager allows tracking of which Phidgets are available to be controlled from the
    current program. This is useful for listing all available Phidgets so you can select which ones
    to use at runtime.

    You do not need to use a Phidget Manager if you know what Phidgets will be required for your
    application in advance.

    Phidget channels that become available will each send an **Attach** event, and Phidgets that are
    removed from the system will send corresponding **Detach** events. If you are using a Phidget
    Manager, your program is responsible for keeping track of available Phidgets using these events.
    """

    def __init__(self):
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._AttachFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p
            )
        else:
            self._AttachFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p
            )
        self._Attach = None
        self._onAttach = None

        if sys.platform == "win32":
            self._DetachFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p
            )
        else:
            self._DetachFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p
            )
        self._Detach = None
        self._onDetach = None

        __func = PhidgetSupport.getDll().PhidgetManager_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        if self._handle is None:
            return
        __func = PhidgetSupport.getDll().PhidgetManager_delete
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))
        self._handle = None
        if res > 0:
            raise PhidgetException(res)

    def _localAttachEvent(self, handle, userPtr, Channel):
        if self._Attach is None:
            return
        __func = PhidgetSupport.getDll().Phidget_retain
        __func.restype = ctypes.c_int32
        result = __func(ctypes.c_void_p(Channel))
        if result > 0:
            raise PhidgetException(result)
        ph = Phidget._from_handle(Channel)
        self._Attach(self, ph)

    def setOnAttachHandler(self, handler):
        r"""Attach event

        Occurs when a channel is attached.

        *   Phidget channels you get from the manager are informational only, you can read
        information about them such as serial number, class, name, etc. but they are not opened. In
        order to interact with one, you must `create` and `open` a Phidget object of the correct
        type.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Manager* - The object on which the event occurred.
            * **Channel** : *Phidget* - The Phidget channel that attached

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._Attach = handler

        if self._onAttach is None:
            fptr = self._AttachFactory(self._localAttachEvent)
            __func = PhidgetSupport.getDll().PhidgetManager_setOnAttachHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onAttach = fptr

    def _localDetachEvent(self, handle, userPtr, Channel):
        if self._Detach is None:
            return
        __func = PhidgetSupport.getDll().Phidget_retain
        __func.restype = ctypes.c_int32
        result = __func(ctypes.c_void_p(Channel))
        if result > 0:
            raise PhidgetException(result)
        ph = Phidget._from_handle(Channel)
        self._Detach(self, ph)

    def setOnDetachHandler(self, handler):
        r"""Detach event

        Occurs when a channel is detached.

        *   Phidget channels you get from the manager are informational only, you can read
        information about them such as serial number, class, name, etc. but they are not opened. In
        order to interact with one, you must `create` and `open` a Phidget object of the correct
        type.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Manager* - The object on which the event occurred.
            * **Channel** : *Phidget* - The Phidget channel that detached

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._Detach = handler

        if self._onDetach is None:
            fptr = self._DetachFactory(self._localDetachEvent)
            __func = PhidgetSupport.getDll().PhidgetManager_setOnDetachHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onDetach = fptr

    def close(self):
        r"""
        Closes a Phidget Manager that has been opened.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetManager_close
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def open(self):
        r"""
        Opens the Phidget Manager.

        Be sure to register **Attach** and **Detach** event handlers for the Manager before opening
        it, to ensure you program doesn't miss the events reported for devices already connected to
        your system.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetManager_open
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)


__all__ = ["Manager", "PhidgetException", "Phidget"]
