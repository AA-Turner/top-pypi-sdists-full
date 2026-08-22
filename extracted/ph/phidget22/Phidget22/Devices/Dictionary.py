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


class Dictionary(Phidget):
    r"""Dictionary Channel class.

    Dictionaries are useful for passing information between multiple programs using Phidgets. A
    common example would be to have one program controlling your application that receives commands
    sent via a Phidget dictionary from a web interface, as outlined in many of our
    [articles](https://www.phidgets.com/?view=articles).

    Keys can be thought of as being similar to variable names, with their values as their associated
    value. Phidget dictionaries contain groups of related key-value pairs, and are stored on a
    central [Phigdet Network Server](https://www.phidgets.com/docs/Phidget_Network_Server).
    Dictionaries, and the key-value pairs within may be accessed from programs that have access to
    the [Phigdet Network Server](https://www.phidgets.com/docs/Phidget_Network_Server).

    The Dictionary API supports connecting to a dictionary on the server, managing key-value pairs,
    and monitoring changes made to the dictionary.

    More information on Phidget Dictionaries can be found on the [Phidget
    Dictionary](https://www.phidgets.com/docs/Phidget_Dictionary) support page.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._AddFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p
            )
        else:
            self._AddFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p
            )
        self._Add = None
        self._onAdd = None

        if sys.platform == "win32":
            self._RemoveFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p
            )
        else:
            self._RemoveFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p
            )
        self._Remove = None
        self._onRemove = None

        if sys.platform == "win32":
            self._UpdateFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p
            )
        else:
            self._UpdateFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p
            )
        self._Update = None
        self._onUpdate = None

        __func = PhidgetSupport.getDll().PhidgetDictionary_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localAddEvent(self, handle, userPtr, key, value):
        if self._Add is None:
            return
        key = key.decode("utf-8")
        value = value.decode("utf-8")
        self._Add(self, key, value)

    def setOnAddHandler(self, handler):
        r"""Add event

        Occurs when a new key value pair is added to the dictionary.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Dictionary* - The object on which the event occurred.
            * **key** : *str* - The key that was added
            * **value** : *str* - The value of the new key

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._Add = handler

        if self._onAdd is None:
            fptr = self._AddFactory(self._localAddEvent)
            __func = PhidgetSupport.getDll().PhidgetDictionary_setOnAddHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onAdd = fptr

    def _localRemoveEvent(self, handle, userPtr, key):
        if self._Remove is None:
            return
        key = key.decode("utf-8")
        self._Remove(self, key)

    def setOnRemoveHandler(self, handler):
        r"""Remove event

        Occurs when a key is removed from the dictionary.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Dictionary* - The object on which the event occurred.
            * **key** : *str* - The key that was removed

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._Remove = handler

        if self._onRemove is None:
            fptr = self._RemoveFactory(self._localRemoveEvent)
            __func = PhidgetSupport.getDll().PhidgetDictionary_setOnRemoveHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onRemove = fptr

    def _localUpdateEvent(self, handle, userPtr, key, value):
        if self._Update is None:
            return
        key = key.decode("utf-8")
        value = value.decode("utf-8")
        self._Update(self, key, value)

    def setOnUpdateHandler(self, handler):
        r"""Update event

        Occurs when a change is made to a key value pair in the dictionary.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Dictionary* - The object on which the event occurred.
            * **key** : *str* - The key whose value was updated
            * **value** : *str* - The new value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._Update = handler

        if self._onUpdate is None:
            fptr = self._UpdateFactory(self._localUpdateEvent)
            __func = PhidgetSupport.getDll().PhidgetDictionary_setOnUpdateHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onUpdate = fptr

    @staticmethod
    def _addDictionary(deviceSerialNumber, label):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Adds a new dictionary to the system.

        The serial number must be greater than 1000.

        Parameters
        ----------
        deviceSerialNumber : int
            the serial number to assign the new dictionary (> 1000)
        label : str
            the label to assign the new dictionary

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _deviceSerialNumber = ctypes.c_int(deviceSerialNumber)
        _label = ctypes.create_string_buffer(label.encode("utf-8"))

        __func = PhidgetSupport.getDll().PhidgetDictionary_addDictionary
        __func.restype = ctypes.c_int32
        result = __func(_deviceSerialNumber, _label)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def _enableControlDictionary():
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Adds a new dictionary that exports the control interface from the system

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetDictionary_enableControlDictionary
        __func.restype = ctypes.c_int32
        result = __func()

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def _enableStatsDictionary():
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Adds a new dictionary that exports runtime statistics from the system

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetDictionary_enableStatsDictionary
        __func.restype = ctypes.c_int32
        result = __func()

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def _loadDictionary(dictionarySerialNumber, file):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Loads data from a file into the specified dictionary.

        *   The data is loaded from a file of the form key=value
        *   Blank lines are ignored
        *   Whitespace before and after the key and value is stripped
        *   Only the first = is observed
        *   Lines starting with # are ignored

        Parameters
        ----------
        dictionarySerialNumber : int
            the serial number of the dictionary to load into
        file : str
            path to the file to load the data from

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _dictionarySerialNumber = ctypes.c_int(dictionarySerialNumber)
        _file = ctypes.create_string_buffer(file.encode("utf-8"))

        __func = PhidgetSupport.getDll().PhidgetDictionary_loadDictionary
        __func.restype = ctypes.c_int32
        result = __func(_dictionarySerialNumber, _file)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def _removeDictionary(deviceSerialNumber):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Removes a dictionary from the system.

        Parameters
        ----------
        deviceSerialNumber : int
            the serial number of the dictionary

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _deviceSerialNumber = ctypes.c_int(deviceSerialNumber)

        __func = PhidgetSupport.getDll().PhidgetDictionary_removeDictionary
        __func.restype = ctypes.c_int32
        result = __func(_deviceSerialNumber)

        if result > 0:
            raise PhidgetException(result)

    def add(self, key, value):
        r"""
        Adds a new key value pair to the dictionary. It is an error if the key already exits.

        Parameters
        ----------
        key : str
            The key to add
        value : str
            The value to add

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _key = ctypes.create_string_buffer(key.encode("utf-8"))
        _value = ctypes.create_string_buffer(value.encode("utf-8"))

        __func = PhidgetSupport.getDll().PhidgetDictionary_add
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _key, _value)

        if result > 0:
            raise PhidgetException(result)

    def removeAll(self):
        r"""
        Removes every key from the dictionary

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetDictionary_removeAll
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def get(self, key):
        r"""
        Gets the value associated with the given key from the dictionary

        Parameters
        ----------
        key : str
            The key whose value is desired

        Returns
        -------
        str | None
            The value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _key = ctypes.create_string_buffer(key.encode("utf-8"))
        _value = (ctypes.c_char * 65536)()
        _valueLen = ctypes.c_size_t(65536)

        __func = PhidgetSupport.getDll().PhidgetDictionary_get
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _key, ctypes.byref(_value), _valueLen)

        if result > 0:
            raise PhidgetException(result)
        assert _value.value is not None

        return _value.value.decode("utf-8")

    def remove(self, key):
        r"""
        Removes the key from the dictionary

        Parameters
        ----------
        key : str
            The key to remove

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _key = ctypes.create_string_buffer(key.encode("utf-8"))

        __func = PhidgetSupport.getDll().PhidgetDictionary_remove
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _key)

        if result > 0:
            raise PhidgetException(result)

    def scan(self, start):
        r"""
        Scans the keys in the dictionary, indexed by `start` or the first key in the dictionary if
        start is `NULL` or an empty String.

        *   The result is formated as a newline seperated list of keys
        *   The list begins at the key following the start key
        *   The list might not contain all of the keys in the dictionary
        *   To continue scanning, call the method again with the last entry from the previous result
        *   When all of the keys have been scanned, a zero length string is returned
        *   Keys added during the scan may be missed, and keys deleted during the scan may be
        included

        Parameters
        ----------
        start : str | None
            The key to start the scan from (or the first key if null)

        Returns
        -------
        str
            The list of keys

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if start is None:
            _start = None
        else:
            _start = ctypes.create_string_buffer(start.encode("utf-8"))
        _keyList = (ctypes.c_char * 65536)()
        _keyListLen = ctypes.c_size_t(65536)

        __func = PhidgetSupport.getDll().PhidgetDictionary_scan
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _start, ctypes.byref(_keyList), _keyListLen)

        if result > 0:
            raise PhidgetException(result)
        assert _keyList.value is not None

        return _keyList.value.decode("utf-8")

    def set(self, key, value):
        r"""
        Sets the value of a key, or creates the key value pair if the key does not already exist.

        Parameters
        ----------
        key : str
            The key to set
        value : str
            The value to set

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _key = ctypes.create_string_buffer(key.encode("utf-8"))
        _value = ctypes.create_string_buffer(value.encode("utf-8"))

        __func = PhidgetSupport.getDll().PhidgetDictionary_set
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _key, _value)

        if result > 0:
            raise PhidgetException(result)

    def update(self, key, value):
        r"""
        Updates a key value pair in the dictionary. It is an error if the key does not exist.

        Parameters
        ----------
        key : str
            The key to update
        value : str
            The value to set

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _key = ctypes.create_string_buffer(key.encode("utf-8"))
        _value = ctypes.create_string_buffer(value.encode("utf-8"))

        __func = PhidgetSupport.getDll().PhidgetDictionary_update
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _key, _value)

        if result > 0:
            raise PhidgetException(result)


__all__ = ["Dictionary", "PhidgetException", "Phidget"]
