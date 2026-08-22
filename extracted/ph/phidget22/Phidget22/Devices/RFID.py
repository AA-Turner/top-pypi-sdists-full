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
from Phidget22.RFIDProtocol import RFIDProtocol
from Phidget22.RFIDChipset import RFIDChipset
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget
from Phidget22.NDEFRecords import NDEFURIRecord, NDEFTextRecord, _cast_ndef_record


class RFID(Phidget):
    r"""RFID Channel class.

    The RFID class provides methods for Phidget RFID boards to read and write (if writing is
    supported) to RFID tags.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._TagFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int
            )
        else:
            self._TagFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int
            )
        self._Tag = None
        self._onTag = None

        if sys.platform == "win32":
            self._TagLostFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int
            )
        else:
            self._TagLostFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int
            )
        self._TagLost = None
        self._onTagLost = None

        __func = PhidgetSupport.getDll().PhidgetRFID_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localTagEvent(self, handle, userPtr, Tag, Protocol):
        if self._Tag is None:
            return
        Tag = Tag.decode("utf-8")
        Protocol = RFIDProtocol(Protocol)
        self._Tag(self, Tag, Protocol)

    def setOnTagHandler(self, handler):
        r"""Tag event

        Occurs when an RFID tag is detected.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *RFID* - The object on which the event occurred.
            * **Tag** : *str* - Data from the tag
            * **Protocol** : *RFIDProtocol* - Communication protocol of the tag

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._Tag = handler

        if self._onTag is None:
            fptr = self._TagFactory(self._localTagEvent)
            __func = PhidgetSupport.getDll().PhidgetRFID_setOnTagHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onTag = fptr

    def _localTagLostEvent(self, handle, userPtr, Tag, Protocol):
        if self._TagLost is None:
            return
        Tag = Tag.decode("utf-8")
        Protocol = RFIDProtocol(Protocol)
        self._TagLost(self, Tag, Protocol)

    def setOnTagLostHandler(self, handler):
        r"""TagLost event

        Occurs when an RFID tag that was being read is no longer seen by the reader. Typically this
        indicates the tag has been removed from the read range, though it could also happen due to
        interference from multiple tags entering the read range at the same time.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *RFID* - The object on which the event occurred.
            * **Tag** : *str* - Data from the lost tag
            * **Protocol** : *RFIDProtocol* - Communication protocol of the lost tag

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._TagLost = handler

        if self._onTagLost is None:
            fptr = self._TagLostFactory(self._localTagLostEvent)
            __func = PhidgetSupport.getDll().PhidgetRFID_setOnTagLostHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onTagLost = fptr

    def getAntennaEnabled(self):
        r"""
        The on/off state of the antenna.

        *   You can turn the antenna off to save power.
        *   You must turn the antenna on in order to detect and read RFID tags.

        Returns
        -------
        bool
            The state of the antenna

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _AntennaEnabled = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetRFID_getAntennaEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_AntennaEnabled))

        if result > 0:
            raise PhidgetException(result)

        return bool(_AntennaEnabled.value)

    def setAntennaEnabled(self, AntennaEnabled):
        r"""
        The on/off state of the antenna.

        *   You can turn the antenna off to save power.
        *   You must turn the antenna on in order to detect and read RFID tags.

        Parameters
        ----------
        AntennaEnabled : bool
            The state of the antenna

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _AntennaEnabled = ctypes.c_int(AntennaEnabled)

        __func = PhidgetSupport.getDll().PhidgetRFID_setAntennaEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _AntennaEnabled)

        if result > 0:
            raise PhidgetException(result)

    def getLastTag(self):
        r"""
        Gets the most recently detected tag's data, even if that tag is no longer within read range.

        *   Only valid after at least one tag has been detected.

        Returns
        -------
        tuple (str, RFIDProtocol)
            A tuple containing:
                - tagString: The data stored on the most recently read tag
                - protocol: Protocol of the most recently detected tag

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _tagString = (ctypes.c_char * 25)()
        _tagStringLen = ctypes.c_size_t(25)
        _protocol = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetRFID_getLastTag
        __func.restype = ctypes.c_int32
        result = __func(
            self._handle, ctypes.byref(_tagString), _tagStringLen, ctypes.byref(_protocol)
        )

        if result > 0:
            raise PhidgetException(result)
        assert _tagString.value is not None

        return _tagString.value.decode("utf-8"), RFIDProtocol(_protocol.value)

    def getTagPresent(self):
        r"""
        This property is true if a compatibile RFID tag is detected by the reader.

        *   `TagPresent` will remain true until the tag is out of range and can no longer be
        interacted with.

        Returns
        -------
        bool
            Tag is in range

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TagPresent = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetRFID_getTagPresent
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_TagPresent))

        if result > 0:
            raise PhidgetException(result)

        return bool(_TagPresent.value)

    def write(self, tagString, protocol, lockTag):
        r"""
        Writes data to the tag being currently read by the reader. Not specifying a tag chipset will
        default to writing T5577-style tags.

        *   You cannot write to a read-only or locked tag.

        Parameters
        ----------
        tagString : str
            The data to write to the tag
        protocol : RFIDProtocol
            The communication protocol to use
        lockTag : bool
            If true, permanently locks the tag so that it cannot be re-written after this write.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _tagString = ctypes.create_string_buffer(tagString.encode("utf-8"))
        _protocol = ctypes.c_int(protocol)
        _lockTag = ctypes.c_int(lockTag)

        __func = PhidgetSupport.getDll().PhidgetRFID_write
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _tagString, _protocol, _lockTag)

        if result > 0:
            raise PhidgetException(result)

    def writeWithChipset(self, tagString, protocol, lockTag, chipset):
        r"""
        Writes data to the tag being currently read by the reader, with a specified tag chipset.

        *   You cannot write to a read-only or locked tag.

        Parameters
        ----------
        tagString : str
            The data to write to the tag
        protocol : RFIDProtocol
            The communication protocol to use
        lockTag : bool
            If true, permanently locks the tag so that it cannot be re-written after this write.
        chipset : RFIDChipset
            The chipset to write for

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _tagString = ctypes.create_string_buffer(tagString.encode("utf-8"))
        _protocol = ctypes.c_int(protocol)
        _lockTag = ctypes.c_int(lockTag)
        _chipset = ctypes.c_int(chipset)

        __func = PhidgetSupport.getDll().PhidgetRFID_writeWithChipset
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _tagString, _protocol, _lockTag, _chipset)

        if result > 0:
            raise PhidgetException(result)


__all__ = [
    "RFID",
    "RFIDProtocol",
    "RFIDChipset",
    "PhidgetException",
    "Phidget",
    "NDEFURIRecord",
    "NDEFTextRecord",
]
