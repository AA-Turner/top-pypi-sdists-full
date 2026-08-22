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
from Phidget22.ChannelClass import ChannelClass
from Phidget22.ChannelSubclass import ChannelSubclass
from Phidget22.DeviceClass import DeviceClass
from Phidget22.DeviceID import DeviceID
from Phidget22.ErrorEventCode import ErrorEventCode
from Phidget22.PhidgetException import PhidgetException


class Phidget:
    r"""Phidget  class.

    The core Phidget class deals with functionality common to all Phidgets, such as opening and
    closing them, or setting Attach, Detach, Error event handlers.

    This class is also used to specify the associations between the Phidget software objects and
    their corresponding physical devices, and makes it possible to determine which Phidget is which
    in cases where it might otherwise be ambiguous.

    This class contains various functions such as **Release**, **Retain**, and **getParent**
    designed to be used with the **Phidget Manager**. These specialized functions may be safely
    ignored if your application does not require a **Manager**. You can check the **Manager API**
    for more information.
    """

    def __init__(self):
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._AttachFactory = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)
        else:
            self._AttachFactory = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)
        self._Attach = None
        self._onAttach = None

        if sys.platform == "win32":
            self._DetachFactory = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)
        else:
            self._DetachFactory = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)
        self._Detach = None
        self._onDetach = None

        if sys.platform == "win32":
            self._ErrorFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p
            )
        else:
            self._ErrorFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p
            )
        self._Error = None
        self._onError = None

        if sys.platform == "win32":
            self._PropertyChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p
            )
        else:
            self._PropertyChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p
            )
        self._PropertyChange = None
        self._onPropertyChange = None

    def __eq__(self, other):
        return (
            hasattr(other, "handle")
            and self._handle is not None
            and other._handle is not None
            and self._handle.value == other._handle.value
        )

    def __hash__(self):
        if self._handle is None or self._handle.value is None:
            return 0
        return self._handle.value

    def __str__(self):
        _value = (ctypes.c_char * 65536)()
        _valueLen = ctypes.c_int32(65536)
        if self.getIsChannel():
            __func = PhidgetSupport.getDll().channelInfo
        else:
            __func = PhidgetSupport.getDll().deviceInfo
        __func(self._handle, ctypes.byref(_value), _valueLen)
        return _value.value.decode("utf- 8")

    @classmethod
    def _from_handle(cls, handle):
        instance = cls()
        instance._handle = ctypes.c_void_p(handle)
        return instance

    def __del__(self):
        if self._handle is None:
            return
        __func = PhidgetSupport.getDll().Phidget_delete
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))
        self._handle = None
        if res > 0:
            raise PhidgetException(res)

    def _localAttachEvent(self, handle, userPtr):
        if self._Attach is None:
            return
        self._Attach(self)

    def setOnAttachHandler(self, handler):
        r"""Attach event

        Occurs when the channel is attached to a physical channel on a Phidget.

        `Attach` must be registered prior to calling `open()`, and will be called when the Phidget
        library matches the channel with a physical channel on a Phidget. `Attach` may be called
        more than once if the channel is detached during its lifetime.

        `Attach` is the recommended place to configuration properties of the channel such as the
        data interval or change trigger.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Phidget* - The object on which the event occurred.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._Attach = handler

        if self._onAttach is None:
            fptr = self._AttachFactory(self._localAttachEvent)
            __func = PhidgetSupport.getDll().Phidget_setOnAttachHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onAttach = fptr

    def _localDetachEvent(self, handle, userPtr):
        if self._Detach is None:
            return
        self._Detach(self)

    def setOnDetachHandler(self, handler):
        r"""Detach event

        Occurs when the channel is detached from a Phidget device channel.`Detach` typically occurs
        when the Phidget device is removed from the system.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Phidget* - The object on which the event occurred.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._Detach = handler

        if self._onDetach is None:
            fptr = self._DetachFactory(self._localDetachEvent)
            __func = PhidgetSupport.getDll().Phidget_setOnDetachHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onDetach = fptr

    def _localErrorEvent(self, handle, userPtr, Code, Description):
        if self._Error is None:
            return
        Code = ErrorEventCode(Code)
        Description = Description.decode("utf-8")
        self._Error(self, Code, Description)

    def setOnErrorHandler(self, handler):
        r"""Error event

        `Error` is called when an error condition has been detected.

        See the documentation for your specific channel class to see what error events it might
        throw.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Phidget* - The object on which the event occurred.
            * **Code** : *ErrorEventCode* - The error code
            * **Description** : *str* - The error description

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._Error = handler

        if self._onError is None:
            fptr = self._ErrorFactory(self._localErrorEvent)
            __func = PhidgetSupport.getDll().Phidget_setOnErrorHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onError = fptr

    def _localPropertyChangeEvent(self, handle, userPtr, propertyName):
        if self._PropertyChange is None:
            return
        propertyName = propertyName.decode("utf-8")
        self._PropertyChange(self, propertyName)

    def setOnPropertyChangeHandler(self, handler):
        r"""PropertyChange event

        Occurs when a property is changed externally from the user channel, usually from a network
        client attached to the same channel.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Phidget* - The object on which the event occurred.
            * **propertyName** : *str* - The name of the property that has changed

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._PropertyChange = handler

        if self._onPropertyChange is None:
            fptr = self._PropertyChangeFactory(self._localPropertyChangeEvent)
            __func = PhidgetSupport.getDll().Phidget_setOnPropertyChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onPropertyChange = fptr

    @staticmethod
    def finalize(flags):
        r"""
        Release memory and threads used by the Phidget library. Should be called prior to unloading
        the library from the address space.

        This function is intended for use in special cases where it is desired for the Phidget
        library to be unloaded before a program's termination. All other API calls are unsafe after
        calling this.

        Parameters
        ----------
        flags : int
            Reserved for future use. Pass 0.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _flags = ctypes.c_int(flags)

        __func = PhidgetSupport.getDll().Phidget_finalize
        __func.restype = ctypes.c_int32
        result = __func(_flags)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def getLibraryVersion():
        r"""
        Gets the version of the Phidget library being used by the program in human readable form.

        Returns
        -------
        str
            The Phidget library version.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _LibraryVersion = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().Phidget_getLibraryVersion
        __func.restype = ctypes.c_int32
        result = __func(ctypes.byref(_LibraryVersion))

        if result > 0:
            raise PhidgetException(result)
        assert _LibraryVersion.value is not None

        return _LibraryVersion.value.decode("utf-8")

    @staticmethod
    def getLibraryVersionNumber():
        r"""
        Gets the version of the Phidget library being used by the program as a version number
        string.

        Returns
        -------
        str
            The Phidget library version number.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _LibraryVersionNumber = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().Phidget_getLibraryVersionNumber
        __func.restype = ctypes.c_int32
        result = __func(ctypes.byref(_LibraryVersionNumber))

        if result > 0:
            raise PhidgetException(result)
        assert _LibraryVersionNumber.value is not None

        return _LibraryVersionNumber.value.decode("utf-8")

    @staticmethod
    def resetLibrary():
        r"""
        Closes all channels, and stops all threads. The library is reset to a newly loaded state.
        All channel handles have been freed.

        This function is intended for use in special cases where the library cannot be unloaded
        between program runs, such as LabVIEW and Unity Editor.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().Phidget_resetLibrary
        __func.restype = ctypes.c_int32
        result = __func()

        if result > 0:
            raise PhidgetException(result)

    def _getClientVersion(self):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Gets the network protocol version of the client, for a network attached channel.

        Returns
        -------
        tuple (int, int)
            A tuple containing:
                - major: The Major version
                - minor: The Minor version

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _major = ctypes.c_int()
        _minor = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getClientVersion
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_major), ctypes.byref(_minor))

        if result > 0:
            raise PhidgetException(result)

        return _major.value, _minor.value

    def _getDeviceFirmwareUpgradeString(self):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Gets the string which will match the filename of the firmware upgrade file

        Returns
        -------
        str
            The firmware upgrade string

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeviceFirmwareUpgradeString = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().Phidget_getDeviceFirmwareUpgradeString
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DeviceFirmwareUpgradeString))

        if result > 0:
            raise PhidgetException(result)
        assert _DeviceFirmwareUpgradeString.value is not None

        return _DeviceFirmwareUpgradeString.value.decode("utf-8")

    def _getDeviceSKU_Revision(self):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Gets the SKU\_Revision of the Phidget which this channel is a part of. If there are multiple
        possible SKU\_Revisions, they will be separated by a /. The SKU\_Revision is a string used
        to identify the exact revision of the device, and can be found on the packaging or on the
        device itself.

        Returns
        -------
        str
            The SKU\_Revision of the device the channel is a part of

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeviceSKU_Revision = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().Phidget_getDeviceSKU_Revision
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DeviceSKU_Revision))

        if result > 0:
            raise PhidgetException(result)
        assert _DeviceSKU_Revision.value is not None

        return _DeviceSKU_Revision.value.decode("utf-8")

    def _getDeviceVINTID(self):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Gets the vint id for the Phidget which this channel is a part of.

        Returns
        -------
        int
            The vint id of the channels device

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeviceVINTID = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().Phidget_getDeviceVINTID
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DeviceVINTID))

        if result > 0:
            raise PhidgetException(result)

        return _DeviceVINTID.value

    def _getServerVersion(self):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Gets the protocol version of the remote Network Server, for a network attached channel.

        Returns
        -------
        tuple (int, int)
            A tuple containing:
                - major: The Major version
                - minor: The Minor version

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _major = ctypes.c_int()
        _minor = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getServerVersion
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_major), ctypes.byref(_minor))

        if result > 0:
            raise PhidgetException(result)

        return _major.value, _minor.value

    def _reboot(self):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Reboots the device into the regular firmware.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().Phidget_reboot
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def _rebootFirmwareUpgrade(self, upgradeTimeout):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Reboots the device into firmware upgrade mode.

        Parameters
        ----------
        upgradeTimeout : int
            The reboot timeout

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _upgradeTimeout = ctypes.c_uint32(upgradeTimeout)

        __func = PhidgetSupport.getDll().Phidget_rebootFirmwareUpgrade
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _upgradeTimeout)

        if result > 0:
            raise PhidgetException(result)

    def getAttached(self):
        r"""
        Gets the attached status of channel. A Phidget is attached after it has been opened and the
        Phidget library finds and connects to the corresponding hardware device.

        *   Most API calls are only valid on attached Phidgets.

        Returns
        -------
        bool
            True if the channel is attached

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Attached = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getAttached
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Attached))

        if result > 0:
            raise PhidgetException(result)

        return bool(_Attached.value)

    def getChannel(self):
        r"""
        Gets the channel index of the channel on the device.

        Returns
        -------
        int
            The channel index

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Channel = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getChannel
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Channel))

        if result > 0:
            raise PhidgetException(result)

        return _Channel.value

    def setChannel(self, Channel):
        r"""
        Specifies the channel index to be opened. The default channel is 0. Set to `ANY_CHANNEL` to
        open any channel on the specified device.

        If setting this property, it must be set before the channel is opened. The behaviour of
        setting this property while the channel is open is undefined.

        Parameters
        ----------
        Channel : int
            The channel index

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Channel = ctypes.c_int(Channel)

        __func = PhidgetSupport.getDll().Phidget_setChannel
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Channel)

        if result > 0:
            raise PhidgetException(result)

    def getChannelClass(self):
        r"""
        Gets the channel class of the channel.

        Returns
        -------
        ChannelClass
            The channel class

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ChannelClass = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getChannelClass
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ChannelClass))

        if result > 0:
            raise PhidgetException(result)

        return ChannelClass(_ChannelClass.value)

    def getChannelClassName(self):
        r"""
        Gets the name of the channel class the channel belongs to.

        Returns
        -------
        str
            The name of the channel's class

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ChannelClassName = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().Phidget_getChannelClassName
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ChannelClassName))

        if result > 0:
            raise PhidgetException(result)
        assert _ChannelClassName.value is not None

        return _ChannelClassName.value.decode("utf-8")

    def getChannelName(self):
        r"""
        Gets the channel's name. This name serves as a description of the specific nature of the
        channel.

        Returns
        -------
        str
            The channel's name

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ChannelName = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().Phidget_getChannelName
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ChannelName))

        if result > 0:
            raise PhidgetException(result)
        assert _ChannelName.value is not None

        return _ChannelName.value.decode("utf-8")

    def getChannelPersistence(self):
        r"""
        Controls whether the state of this channel persists across attach and close. By default,
        channels are reset on attach and close. Note that any defaults listed in the API must be set
        by the user when Persistence is enabled.

        Returns
        -------
        bool
            Channel state persistence across open-close cycles

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ChannelPersistence = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getChannelPersistence
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ChannelPersistence))

        if result > 0:
            raise PhidgetException(result)

        return bool(_ChannelPersistence.value)

    def setChannelPersistence(self, ChannelPersistence):
        r"""
        Controls whether the state of this channel persists across attach and close. By default,
        channels are reset on attach and close. Note that any defaults listed in the API must be set
        by the user when Persistence is enabled.

        Parameters
        ----------
        ChannelPersistence : bool
            Channel state persistence across open-close cycles

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ChannelPersistence = ctypes.c_int(ChannelPersistence)

        __func = PhidgetSupport.getDll().Phidget_setChannelPersistence
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _ChannelPersistence)

        if result > 0:
            raise PhidgetException(result)

    def getChannelSubclass(self):
        r"""
        Gets the subclass for this channel. Allows for identifying channels with specific
        characteristics without needing to know the exact device and channel index.

        Returns
        -------
        ChannelSubclass
            The channel's subclass

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ChannelSubclass = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getChannelSubclass
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ChannelSubclass))

        if result > 0:
            raise PhidgetException(result)

        return ChannelSubclass(_ChannelSubclass.value)

    def close(self):
        r"""
        Closes a Phidget channel that has been opened.`close()` will release the channel on the
        Phidget device.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().Phidget_close
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def getDeviceChannelCount(self, cls):
        r"""
        Gets the number of channels of the specified channel class on the device. Pass
        `Phidget22.ChannelClass.PHIDCHCLASS_NOTHING` to get the total number of channels.

        Parameters
        ----------
        cls : ChannelClass
            The Channel Class

        Returns
        -------
        int
            The Channel Count

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _cls = ctypes.c_int(cls)
        _count = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().Phidget_getDeviceChannelCount
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _cls, ctypes.byref(_count))

        if result > 0:
            raise PhidgetException(result)

        return _count.value

    def getDeviceClass(self):
        r"""
        Gets the device class for the Phidget which this channel is a part of.

        Returns
        -------
        DeviceClass
            The class of the device the channel is a part of.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeviceClass = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getDeviceClass
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DeviceClass))

        if result > 0:
            raise PhidgetException(result)

        return DeviceClass(_DeviceClass.value)

    def getDeviceClassName(self):
        r"""
        Gets the name of the device class for the Phidget which this channel is a part of.

        Returns
        -------
        str
            The class name of the device the channel is a part of.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeviceClassName = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().Phidget_getDeviceClassName
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DeviceClassName))

        if result > 0:
            raise PhidgetException(result)
        assert _DeviceClassName.value is not None

        return _DeviceClassName.value.decode("utf-8")

    def getDeviceID(self):
        r"""
        Gets the Device ID for the Phidget which this channel is a part of.

        Returns
        -------
        DeviceID
            The device id of the device the channel is a part of

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeviceID = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getDeviceID
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DeviceID))

        if result > 0:
            raise PhidgetException(result)

        return DeviceID(_DeviceID.value)

    def getDeviceLabel(self):
        r"""
        Gets the label of the Phidget which this channel is a part of. A device label is a custom
        string used to more easily identify a Phidget. Labels are written to a Phidget using
        `writeDeviceLabel()`, or by right-clicking the device and setting a label in the Phidget
        Control Panel for Windows.

        Returns
        -------
        str
            The device label

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeviceLabel = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().Phidget_getDeviceLabel
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DeviceLabel))

        if result > 0:
            raise PhidgetException(result)
        assert _DeviceLabel.value is not None

        return _DeviceLabel.value.decode("utf-8")

    def setDeviceLabel(self, DeviceLabel):
        r"""
        Specifies the label of the Phidget to be opened. Leave un-set to open any label. A device
        label is a custom string used to more easily identify a Phidget. Labels are written to a
        Phidget using `writeDeviceLabel()`, or by right-clicking the device and setting a label in
        the Phidget Control Panel for Windows.

        If setting this property, it must be set before the channel is opened. The behaviour of
        setting this property while the channel is open is undefined.

        Parameters
        ----------
        DeviceLabel : str
            The device label

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeviceLabel = ctypes.create_string_buffer(DeviceLabel.encode("utf-8"))

        __func = PhidgetSupport.getDll().Phidget_setDeviceLabel
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _DeviceLabel)

        if result > 0:
            raise PhidgetException(result)

    def getDeviceName(self):
        r"""
        Gets the name of the Phidget which this channel is a part of.

        Returns
        -------
        str
            The name of the device the channel is a part of

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeviceName = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().Phidget_getDeviceName
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DeviceName))

        if result > 0:
            raise PhidgetException(result)
        assert _DeviceName.value is not None

        return _DeviceName.value.decode("utf-8")

    def getDeviceSerialNumber(self):
        r"""
        Gets the serial number of the Phidget which this channel is a part of.
        If the channel is part of a VINT device, this will be the serial number of the VINT Hub the
        device is attached to.

        Returns
        -------
        int
            The device serial number

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeviceSerialNumber = ctypes.c_int32()

        __func = PhidgetSupport.getDll().Phidget_getDeviceSerialNumber
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DeviceSerialNumber))

        if result > 0:
            raise PhidgetException(result)

        return _DeviceSerialNumber.value

    def setDeviceSerialNumber(self, DeviceSerialNumber):
        r"""
        Specifies the serial number of the Phidget to be opened. Leave un-set, or set to
        `ANY_SERIAL_NUMBER` to open any serial number.
        If the channel is part of a VINT device, this will be the serial number of the VINT Hub the
        device is attached to.

        If setting this property, it must be set before the channel is opened. The behaviour of
        setting this property while the channel is open is undefined.

        Parameters
        ----------
        DeviceSerialNumber : int
            The device serial number

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeviceSerialNumber = ctypes.c_int32(DeviceSerialNumber)

        __func = PhidgetSupport.getDll().Phidget_setDeviceSerialNumber
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _DeviceSerialNumber)

        if result > 0:
            raise PhidgetException(result)

    def getDeviceSKU(self):
        r"""
        Gets the SKU of the Phidget which this channel is a part of. If there are multiple possible
        SKUs, they will be separated by a /.

        Returns
        -------
        str
            The SKU of the device the channel is a part of

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeviceSKU = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().Phidget_getDeviceSKU
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DeviceSKU))

        if result > 0:
            raise PhidgetException(result)
        assert _DeviceSKU.value is not None

        return _DeviceSKU.value.decode("utf-8")

    def getDeviceVersion(self):
        r"""
        Gets the firmware version of the Phidget which this channel is a part of.

        Returns
        -------
        int
            The version of the device the channel is a part of

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeviceVersion = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getDeviceVersion
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DeviceVersion))

        if result > 0:
            raise PhidgetException(result)

        return _DeviceVersion.value

    def getHub(self):
        r"""
        Gets the hub that this channel is attached to.

        Returns
        -------
        Phidget
            The hub the channels device is attached to

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Hub = ctypes.c_void_p()

        __func = PhidgetSupport.getDll().Phidget_getHub
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Hub))

        if result > 0:
            raise PhidgetException(result)

        __Hub = Phidget()
        __Hub._handle = _Hub

        return __Hub

    def getHubPort(self):
        r"""
        Gets the hub port index of the VINT Hub port that the channel is attached to.

        Returns
        -------
        int
            The hub port index

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _HubPort = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getHubPort
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_HubPort))

        if result > 0:
            raise PhidgetException(result)

        return _HubPort.value

    def setHubPort(self, HubPort):
        r"""
        Specifies the hub port index of the VINT Hub port to open this channel on. Leave un-set, or
        set to `ANY_HUB_PORT` to open the channel on any VINT Hub port

        If setting this property, it must be set before the channel is opened. The behaviour of
        setting this property while the channel is open is undefined.

        Parameters
        ----------
        HubPort : int
            The hub port index

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _HubPort = ctypes.c_int(HubPort)

        __func = PhidgetSupport.getDll().Phidget_setHubPort
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _HubPort)

        if result > 0:
            raise PhidgetException(result)

    def getHubPortCount(self):
        r"""
        Gets the number of VINT ports present on the VINT Hub that the channel is attached to.

        Returns
        -------
        int
            The number of ports on the VINT Hub

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _HubPortCount = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getHubPortCount
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_HubPortCount))

        if result > 0:
            raise PhidgetException(result)

        return _HubPortCount.value

    def getHubPortSpeed(self):
        r"""
        Configures the communication speed for this VINT device. Both the `HubPortSupportsSetSpeed`
        and `VINTDeviceSupportsSetSpeed` must be true in order to set the hub port speed.Available
        speeds are: 100000, 160000, 250000, 400000, 500000, 800000 and 1000000. Setting any other
        speed will select the nearest lower supported speed. The upper speed is bound by the lesser
        of `MaxHubPortSpeed` and `MaxVINTDeviceSpeed`. Set the speed to `AUTO_HUBPORTSPEED` to
        enable Auto Set Speed on Hubs that support it (enabled by default).

        Returns
        -------
        int
            The VINT Device communication speed

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _HubPortSpeed = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().Phidget_getHubPortSpeed
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_HubPortSpeed))

        if result > 0:
            raise PhidgetException(result)

        return _HubPortSpeed.value

    def setHubPortSpeed(self, HubPortSpeed):
        r"""
        Configures the communication speed for this VINT device. Both the `HubPortSupportsSetSpeed`
        and `VINTDeviceSupportsSetSpeed` must be true in order to set the hub port speed.Available
        speeds are: 100000, 160000, 250000, 400000, 500000, 800000 and 1000000. Setting any other
        speed will select the nearest lower supported speed. The upper speed is bound by the lesser
        of `MaxHubPortSpeed` and `MaxVINTDeviceSpeed`. Set the speed to `AUTO_HUBPORTSPEED` to
        enable Auto Set Speed on Hubs that support it (enabled by default).

        Parameters
        ----------
        HubPortSpeed : int
            The VINT Device communication speed

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _HubPortSpeed = ctypes.c_uint32(HubPortSpeed)

        __func = PhidgetSupport.getDll().Phidget_setHubPortSpeed
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _HubPortSpeed)

        if result > 0:
            raise PhidgetException(result)

    def getMaxHubPortSpeed(self):
        r"""
        The max communication speed of a high-speed capable VINT Port.

        Returns
        -------
        int
            The VINT Port max speed

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxHubPortSpeed = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().Phidget_getMaxHubPortSpeed
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxHubPortSpeed))

        if result > 0:
            raise PhidgetException(result)

        return _MaxHubPortSpeed.value

    def getHubPortSupportsAutoSetSpeed(self):
        r"""
        Indicates that the communication speed of this VINT port can be set automatically.

        Returns
        -------
        bool
            The VINT Port supports auto set speed

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _HubPortSupportsAutoSetSpeed = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getHubPortSupportsAutoSetSpeed
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_HubPortSupportsAutoSetSpeed))

        if result > 0:
            raise PhidgetException(result)

        return bool(_HubPortSupportsAutoSetSpeed.value)

    def getHubPortSupportsSetSpeed(self):
        r"""
        Indicates that the communication speed of this VINT port can be set.

        Returns
        -------
        bool
            The VINT Port supports set speed

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _HubPortSupportsSetSpeed = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getHubPortSupportsSetSpeed
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_HubPortSupportsSetSpeed))

        if result > 0:
            raise PhidgetException(result)

        return bool(_HubPortSupportsSetSpeed.value)

    def getIsChannel(self):
        r"""
        Returns true if this represents a channel, false if this represents a device. Mostly for use
        alongside `getParent()` to distinguish channel handles from device handles.

        Returns
        -------
        bool
            True if the handle is for a channel.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IsChannel = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getIsChannel
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_IsChannel))

        if result > 0:
            raise PhidgetException(result)

        return bool(_IsChannel.value)

    def getIsHubPortDevice(self):
        r"""
        Gets whether this channel is a VINT Hub port channel, or part of a VINT device attached to a
        hub port.

        Returns
        -------
        bool
            The hub port mode (True if the channel is a hub port itself)

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IsHubPortDevice = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getIsHubPortDevice
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_IsHubPortDevice))

        if result > 0:
            raise PhidgetException(result)

        return bool(_IsHubPortDevice.value)

    def setIsHubPortDevice(self, IsHubPortDevice):
        r"""
        Specifies whether this channel should be opened on a VINT Hub port directly, or on a VINT
        device attached to a hub port.

        If setting this property, it must be set before the channel is opened. The behaviour of
        setting this property while the channel is open is undefined.

        Parameters
        ----------
        IsHubPortDevice : bool
            The hub port mode (True if the channel is a hub port itself)

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IsHubPortDevice = ctypes.c_int(IsHubPortDevice)

        __func = PhidgetSupport.getDll().Phidget_setIsHubPortDevice
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _IsHubPortDevice)

        if result > 0:
            raise PhidgetException(result)

    def getIsLocal(self):
        r"""
        Returns true when this channel is attached directly on the local machine, or false
        otherwise.

        Returns
        -------
        bool
            True if the channel is attached to a local device

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IsLocal = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getIsLocal
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_IsLocal))

        if result > 0:
            raise PhidgetException(result)

        return bool(_IsLocal.value)

    def setIsLocal(self, IsLocal):
        r"""
        Set to True if the channel is to be opened locally, and not over a network. If both this and
        `IsRemote` are set to False (the default), the channel will be opened either locally or
        remotely, on whichever matching channel is found first.

        If setting this property, it must be set before the channel is opened. The behaviour of
        setting this property while the channel is open is undefined.

        Parameters
        ----------
        IsLocal : bool
            True if the channel is attached to a local device

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IsLocal = ctypes.c_int(IsLocal)

        __func = PhidgetSupport.getDll().Phidget_setIsLocal
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _IsLocal)

        if result > 0:
            raise PhidgetException(result)

    def getIsOpen(self):
        r"""
        Returns true if `open()` has been called on this channel.

        Returns
        -------
        bool
            True if the channel is opened.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IsOpen = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getIsOpen
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_IsOpen))

        if result > 0:
            raise PhidgetException(result)

        return bool(_IsOpen.value)

    def getIsRemote(self):
        r"""
        Returns true when this channel is attached via a Phidget network server, or false otherwise.

        Returns
        -------
        bool
            True if the channel is attached to a network device

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IsRemote = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getIsRemote
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_IsRemote))

        if result > 0:
            raise PhidgetException(result)

        return bool(_IsRemote.value)

    def setIsRemote(self, IsRemote):
        r"""
        Set to True if the channel is to be opened remotely, rather than locally. If both this and
        `IsLocal` are set to False (the default), the channel will be opened either locally or
        remotely, on whichever matching channel is found first.

        In order for your program to have access to remote Phidgets, you must use the **Networking
        API** to `Net.enableServerDiscovery()` or `Net.addServer()`.

        If setting this property, it must be set before the channel is opened. The behaviour of
        setting this property while the channel is open is undefined.

        Parameters
        ----------
        IsRemote : bool
            True if the channel is attached to a network device

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IsRemote = ctypes.c_int(IsRemote)

        __func = PhidgetSupport.getDll().Phidget_setIsRemote
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _IsRemote)

        if result > 0:
            raise PhidgetException(result)

    def open(self):
        r"""
        Opens the Phidget channel. The specific channel to be opened can be specified by setting any
        of the following properties:

        *   DeviceSerialNumber
        *   DeviceLabel
        *   Channel
        *   HubPort
        *   IsHubPortDevice
        *   ServerName
        *   IsLocal
        *   IsRemote

        `open()` will return immediately, with the attachment process proceeding asynchronously. Use
        the Attach event or Attached property to determine when the channel is ready to use.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().Phidget_open
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def openWaitForAttachment(self, timeout):
        r"""
        Opens the Phidget channel and waits a defined amount of time for the device to attach.The
        specific channel to be opened can be specified by setting any of the following properties:

        *   DeviceSerialNumber
        *   DeviceLabel
        *   Channel
        *   HubPort
        *   IsHubPortDevice
        *   ServerName
        *   IsLocal
        *   IsRemote

        `openWaitForAttachment()` will block until the channel is attached or a timeout occurs. A
        timeout value of 0 will wait forever.

        Parameters
        ----------
        timeout : int
            Timeout in milliseconds

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _timeout = ctypes.c_uint32(timeout)

        __func = PhidgetSupport.getDll().Phidget_openWaitForAttachment
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _timeout)

        if result > 0:
            raise PhidgetException(result)

    def getParent(self):
        r"""
        Gets the handle of the parent device of the given Phidget handle.

        For example, this would refer to the device the channel is a part of, or the Hub that a
        device is plugged into.

        This is useful when used alongside a **Phidget Manager** to create device trees like the one
        in the Phidget Control Panel.

        *   This can be used to travel up the device tree and get device information at each step.
        *   The root device will return a null handle
        *   Parent handles always refer to devices. See `getIsChannel()`

        Returns
        -------
        Phidget | None
            The handle of the parent

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Parent = ctypes.c_void_p()

        __func = PhidgetSupport.getDll().Phidget_getParent
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Parent))

        if result > 0:
            raise PhidgetException(result)

        __Parent = Phidget()
        __Parent._handle = _Parent

        return __Parent

    def getServerHostname(self):
        r"""
        Gets the hostname of the Phidget network server for network attached Phidgets.
        Fails if the channel is not connected to a Phidget network server.

        Returns
        -------
        str
            The hostname of the channel's server

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ServerHostname = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().Phidget_getServerHostname
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ServerHostname))

        if result > 0:
            raise PhidgetException(result)
        assert _ServerHostname.value is not None

        return _ServerHostname.value.decode("utf-8")

    def getServerName(self):
        r"""
        Gets the name of the Phidget network server the channel is attached to, if any.
        Fails if the channel is not connected to a Phidget network server.

        Returns
        -------
        str
            The name of the Phidget network server the channel is from

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ServerName = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().Phidget_getServerName
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ServerName))

        if result > 0:
            raise PhidgetException(result)
        assert _ServerName.value is not None

        return _ServerName.value.decode("utf-8")

    def setServerName(self, ServerName):
        r"""
        Specifies that this channel will be opened remotely, on a Phidget network server with this
        name.

        This function should only be used if you want your Phidget to be found on a specific server,
        and does not need to be specified if the Phidget can be on any any available server.

        In order for your program to have access to remote Phidgets, you must use the **Networking
        API** to `Net.enableServerDiscovery()` or `Net.addServer()`.

        If setting this property, it must be set before the channel is opened. The behaviour of
        setting this property while the channel is open is undefined.

        Parameters
        ----------
        ServerName : str
            The name of the Phidget network server the channel is from

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ServerName = ctypes.create_string_buffer(ServerName.encode("utf-8"))

        __func = PhidgetSupport.getDll().Phidget_setServerName
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _ServerName)

        if result > 0:
            raise PhidgetException(result)

    def getServerPeerName(self):
        r"""
        Gets the peer name (address and port) of the Phidget server for network attached Phidgets,
        formatted as: `address:port`
        Fails if the channel is not connected to a Phidget network server.

        Returns
        -------
        str
            The address and port of the channel's server

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ServerPeerName = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().Phidget_getServerPeerName
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ServerPeerName))

        if result > 0:
            raise PhidgetException(result)
        assert _ServerPeerName.value is not None

        return _ServerPeerName.value.decode("utf-8")

    def getServerUniqueName(self):
        r"""
        Gets the unique name for the server the channel is attached to, if any. This is either a
        unique mDNS name, or the name specified in `Net.addServer()`
        Fails if the channel is not connected to a Phidget network server.

        Returns
        -------
        str
            The unique name of the server

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ServerUniqueName = ctypes.c_char_p()

        __func = PhidgetSupport.getDll().Phidget_getServerUniqueName
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ServerUniqueName))

        if result > 0:
            raise PhidgetException(result)
        assert _ServerUniqueName.value is not None

        return _ServerUniqueName.value.decode("utf-8")

    def getMaxVINTDeviceSpeed(self):
        r"""
        The max communication speed of a high-speed capable VINT Device.

        Returns
        -------
        int
            The VINT Device max commuinication speed

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxVINTDeviceSpeed = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().Phidget_getMaxVINTDeviceSpeed
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxVINTDeviceSpeed))

        if result > 0:
            raise PhidgetException(result)

        return _MaxVINTDeviceSpeed.value

    def getVINTDeviceSupportsAutoSetSpeed(self):
        r"""
        Indicates that the communication speed of this VINT device can be set automatically.

        Returns
        -------
        bool
            The VINT Device supports auto set speed

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VINTDeviceSupportsAutoSetSpeed = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getVINTDeviceSupportsAutoSetSpeed
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_VINTDeviceSupportsAutoSetSpeed))

        if result > 0:
            raise PhidgetException(result)

        return bool(_VINTDeviceSupportsAutoSetSpeed.value)

    def getVINTDeviceSupportsSetSpeed(self):
        r"""
        Indicates that the communication speed of this VINT device can be set.

        Returns
        -------
        bool
            The VINT Device supports set speed

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VINTDeviceSupportsSetSpeed = ctypes.c_int()

        __func = PhidgetSupport.getDll().Phidget_getVINTDeviceSupportsSetSpeed
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_VINTDeviceSupportsSetSpeed))

        if result > 0:
            raise PhidgetException(result)

        return bool(_VINTDeviceSupportsSetSpeed.value)

    def writeDeviceLabel(self, deviceLabel):
        r"""
        Writes a label to the device in the form of a string in the device flash memory. This label
        can then be used to identify the device, and will persist across power cycles.

        The label can be at most 10 UTF-16 code units. Most unicode characters take up a single code
        unit, but some, such as emoji, can take several.

        Some older devices can not have their labels set from Windows. For these devices the label
        should be set from Linux or macOS.

        Note: You should be careful when writing labels in your code, because the label is stored in
        flash which can only be re-written around 10,000 times before it will no longer write. If
        your program is complex, be sure to test it thoroughly before using WriteLabel to avoid
        accidentally burning out the flash.

        Parameters
        ----------
        deviceLabel : str
            The device label

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _deviceLabel = ctypes.create_string_buffer(deviceLabel.encode("utf-8"))

        __func = PhidgetSupport.getDll().Phidget_writeDeviceLabel
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _deviceLabel)

        if result > 0:
            raise PhidgetException(result)

    ANY_SERIAL_NUMBER = -1
    """Pass to <code>setDeviceSerialNumber()</code> to open any serial number."""

    ANY_HUB_PORT = -1
    """Pass to <code>setHubPort()</code> to open any hub port."""

    ANY_CHANNEL = -1
    """Pass to <code>setChannel()</code> to open any channel."""

    ANY_LABEL = None
    """Pass to <code>setDeviceLabel()</code> to open any label."""

    INFINITE_TIMEOUT = 0
    """Pass to <code>openWaitForAttachment()</code> for an infinite timeout."""

    DEFAULT_TIMEOUT = 1000
    """Pass to <code>openWaitForAttachment()</code> for the default timeout."""

    AUTO_HUBPORTSPEED = 0
    """Pass to <code>setHubPortSpeed()</code> to set the Hub Port speed automatically when supported by both the hub port and the VINT device."""


__all__ = [
    "Phidget",
    "ChannelClass",
    "ChannelSubclass",
    "DeviceClass",
    "DeviceID",
    "ErrorEventCode",
    "PhidgetException",
]
