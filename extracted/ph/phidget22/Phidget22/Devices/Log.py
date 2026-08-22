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
from Phidget22.LogLevel import LogLevel
from Phidget22.PhidgetException import PhidgetException


class Log:
    r"""Log  class.

    The Phidget Log class is used to track and store information about the operation of programs
    using the Phidget22 library.

    For basic use of the log class, the only functions you need to worry about are **Enable** and
    **Log**. Simply **Enable** logging with log level **INFO**, and use **Log** to log your own
    messages to the log file.

    For a more in-depth explanation of the concepts behind the more obscure functions, check out the
    [Logging Explained](https://www.phidgets.com/docs/Logging_Explained) page.
    """

    def __init__(self):
        self._handle = ctypes.c_void_p()

    @staticmethod
    def disable():
        r"""
        Disables logging within the Phidget library.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetLog_disable
        __func.restype = ctypes.c_int32
        result = __func()

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def enable(level, destination):
        r"""
        Enables logging within the Phidget library.

        Parameters
        ----------
        level : LogLevel
            The logging level
        destination : str | None
            The log file path

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _level = ctypes.c_int(level)
        if destination is None:
            _destination = None
        else:
            _destination = ctypes.create_string_buffer(destination.encode("utf-8"))

        __func = PhidgetSupport.getDll().PhidgetLog_enable
        __func.restype = ctypes.c_int32
        result = __func(_level, _destination)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def getLevel():
        r"""
        Gets the log level for the phidget22 source.

        Returns
        -------
        LogLevel
            The current log level

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _level = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLog_getLevel
        __func.restype = ctypes.c_int32
        result = __func(ctypes.byref(_level))

        if result > 0:
            raise PhidgetException(result)

        return LogLevel(_level.value)

    @staticmethod
    def setLevel(level):
        r"""
        Sets the log level for all sources not prefaced with \_phidget22.

        Parameters
        ----------
        level : LogLevel
            The new log level

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _level = ctypes.c_int(level)

        __func = PhidgetSupport.getDll().PhidgetLog_setLevel
        __func.restype = ctypes.c_int32
        result = __func(_level)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def log(level, message):
        r"""
        Writes a message to the Phidget library log.

        Parameters
        ----------
        level : LogLevel
            The logging level
        message : str
            The message

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _level = ctypes.c_int(level)
        _message = ctypes.create_string_buffer(message.encode("utf-8"))

        __func = PhidgetSupport.getDll().PhidgetLog_logs
        __func.restype = ctypes.c_int32
        result = __func(_level, _message)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def loge(level, source, message):
        r"""
        Writes a message to the Phidget library log with a specified source.

        Parameters
        ----------
        level : LogLevel
            The logging level
        source : str
            The name of the log source the message is from
        message : str
            The message

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _level = ctypes.c_int(level)
        _source = ctypes.create_string_buffer(source.encode("utf-8"))
        _message = ctypes.create_string_buffer(message.encode("utf-8"))

        __func = PhidgetSupport.getDll().PhidgetLog_loges
        __func.restype = ctypes.c_int32
        result = __func(_level, _source, _message)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def rotate():
        r"""
        Manually rotate the log file. This will only have an effect if automatic rotation is
        disabled and the log file is larger than the specified maximum file size.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetLog_rotate
        __func.restype = ctypes.c_int32
        result = __func()

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def isRotating():
        r"""
        Determines if the library is automatically rotating the log file

        Returns
        -------
        bool
            If the library is automatically rotating the log file

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _isrotating = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLog_isRotating
        __func.restype = ctypes.c_int32
        result = __func(ctypes.byref(_isrotating))

        if result > 0:
            raise PhidgetException(result)

        return bool(_isrotating.value)

    @staticmethod
    def getRotating():
        r"""
        Gets the current log rotation parameters

        Returns
        -------
        tuple (int, int)
            A tuple containing:
                - size: The file size above which the log file should be rotated.
                - keepCount: The number of log files that will be kept after rotation.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _size = ctypes.c_uint64()
        _keepCount = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLog_getRotating
        __func.restype = ctypes.c_int32
        result = __func(ctypes.byref(_size), ctypes.byref(_keepCount))

        if result > 0:
            raise PhidgetException(result)

        return _size.value, _keepCount.value

    @staticmethod
    def setRotating(size, keepCount):
        r"""
        Sets log rotation parameters.

        Parameters
        ----------
        size : int
            The file size above which the file should be rotated in bytes. Min: 32768 (32 KiB) Def: 10485760 (10 MiB)
        keepCount : int
            The number of log files that should be kept after rotation. Min: 0 Def: 1 Max: 64

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _size = ctypes.c_uint64(size)
        _keepCount = ctypes.c_int(keepCount)

        __func = PhidgetSupport.getDll().PhidgetLog_setRotating
        __func.restype = ctypes.c_int32
        result = __func(_size, _keepCount)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def enableRotating():
        r"""
        Enables automatic rotation of the log file (the default).

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetLog_enableRotating
        __func.restype = ctypes.c_int32
        result = __func()

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def disableRotating():
        r"""
        Disables automatic rotation of the log file.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetLog_disableRotating
        __func.restype = ctypes.c_int32
        result = __func()

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def addSource(source, level):
        r"""
        Adds a source to the Phidget logging system. This is useful for declaring a source and
        setting its log level before sending any messages.

        Parameters
        ----------
        source : str
            The source name
        level : LogLevel
            The log level of the source

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _source = ctypes.create_string_buffer(source.encode("utf-8"))
        _level = ctypes.c_int(level)

        __func = PhidgetSupport.getDll().PhidgetLog_addSource
        __func.restype = ctypes.c_int32
        result = __func(_source, _level)

        if result > 0:
            raise PhidgetException(result)

    @staticmethod
    def getSourceLevel(source):
        r"""
        Gets the log level of the specified log source.

        Parameters
        ----------
        source : str
            The log source name

        Returns
        -------
        LogLevel
            The log level of the source

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _source = ctypes.create_string_buffer(source.encode("utf-8"))
        _level = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLog_getSourceLevel
        __func.restype = ctypes.c_int32
        result = __func(_source, ctypes.byref(_level))

        if result > 0:
            raise PhidgetException(result)

        return LogLevel(_level.value)

    @staticmethod
    def setSourceLevel(source, level):
        r"""
        Sets the log level of the specified log source.

        Parameters
        ----------
        source : str
            The log source name
        level : LogLevel
            The new log level

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _source = ctypes.create_string_buffer(source.encode("utf-8"))
        _level = ctypes.c_int(level)

        __func = PhidgetSupport.getDll().PhidgetLog_setSourceLevel
        __func.restype = ctypes.c_int32
        result = __func(_source, _level)

        if result > 0:
            raise PhidgetException(result)


__all__ = ["Log", "LogLevel", "PhidgetException"]
