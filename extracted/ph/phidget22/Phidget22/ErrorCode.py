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

if sys.version_info >= (3, 4):
    from enum import IntEnum
else:
    from _int_enum import IntEnum


class ErrorCode(IntEnum):
    """
    Error codes returned from all API calls via Exceptions.
    """

    EPHIDGET_OK = 0
    """Call succeeded."""
    EPHIDGET_PERM = 1
    """Not Permitted"""
    EPHIDGET_NOENT = 2
    """The specified entity does not exist. This is usually a result of Net or Log API calls."""
    EPHIDGET_TIMEOUT = 3
    """Call has timed out. This can happen for a number of common reasons: Check that the Phidget you are trying to open is plugged in, and that the addressing parameters have been specified correctly. Check that the Phidget is not already open in another program, such as the Phidget Control Panel, or another program you are developing. If your Phidget has a plug or terminal block for external power, ensure it is plugged in and powered. If you are using remote Phidgets, ensure that your computer can access the remote Phidgets using the Phidget Control Panel. If you are using remote Phidgets, ensure you have enabled Server Discovery or added the server corresponding to the Phidget you are trying to open. If you are using Network Server Discovery, try extending the timeout to allow more time for the server to be discovered."""
    EPHIDGET_KEEPALIVE = 58
    """Keep Alive Failure"""
    EPHIDGET_INTERRUPTED = 4
    """The operation was interrupted; either from an error, or because the device was closed."""
    EPHIDGET_IO = 5
    """IO Issue"""
    EPHIDGET_NOMEMORY = 6
    """Memory Issue"""
    EPHIDGET_ACCESS = 7
    """Access to the resource (file) is denied. This can happen when enabling logging."""
    EPHIDGET_FAULT = 8
    """Address Issue"""
    EPHIDGET_BUSY = 9
    """Specified resource is in use. This error code is not normally used."""
    EPHIDGET_EXIST = 10
    """Object Exists"""
    EPHIDGET_NOTDIR = 11
    """Object is not a directory"""
    EPHIDGET_ISDIR = 12
    """Object is a directory"""
    EPHIDGET_INVALID = 13
    """Invalid or malformed command. This can be caused by sending a command to a device which is not supported in it's current configuration."""
    EPHIDGET_NFILE = 14
    """Too many open files in system"""
    EPHIDGET_MFILE = 15
    """Too many open files"""
    EPHIDGET_NOSPC = 16
    """The provided buffer argument size is too small."""
    EPHIDGET_FBIG = 17
    """File too Big"""
    EPHIDGET_ROFS = 18
    """Read Only Filesystem"""
    EPHIDGET_RO = 19
    """Read Only Object"""
    EPHIDGET_UNSUPPORTED = 20
    """This API call is not supported. For Class APIs this means that this API is not supported by this device. This can also mean the API is not supported on this OS, or OS configuration."""
    EPHIDGET_INVALIDARG = 21
    """One or more of the parameters passed to the function is not accepted by the channel in its current configuration."""
    EPHIDGET_AGAIN = 22
    """Try again"""
    EPHIDGET_NOTEMPTY = 26
    """Not Empty"""
    EPHIDGET_UNEXPECTED = 28
    """Something unexpected has occured. Enable library logging and have a look at the log, or contact Phidgets support."""
    EPHIDGET_DUPLICATE = 27
    """Duplicated request. Can happen with some Net API calls, such as trying to add the same server twice."""
    EPHIDGET_BADPASSWORD = 37
    """Bad Credential"""
    EPHIDGET_NETUNAVAIL = 45
    """Network Unavailable"""
    EPHIDGET_CONNREF = 35
    """Connection Refused"""
    EPHIDGET_CONNRESET = 46
    """Connection Reset"""
    EPHIDGET_HOSTUNREACH = 48
    """No route to host"""
    EPHIDGET_NODEV = 40
    """No Such Device"""
    EPHIDGET_WRONGDEVICE = 50
    """A Phidget channel object of the wrong channel class was passed into this API call."""
    EPHIDGET_PIPE = 41
    """Broken Pipe"""
    EPHIDGET_RESOLV = 44
    """Name Resolution Failure"""
    EPHIDGET_UNKNOWNVAL = 51
    """The value is unknown. This can happen right after attach, when the value has not yet been received from the Phidget. This can also happen if a device has not yet been configured / enabled. Some properties can only be read back after being set."""
    EPHIDGET_NOTATTACHED = 52
    """This can happen for a number of common reasons. Be sure you are opening the channel before trying to use it. If you are opening the channel, the program may not be waiting for the channel to be attached. If possible use openWaitForAttachment. Otherwise, be sure to check the Attached property of the channel before trying to use it."""
    EPHIDGET_INVALIDPACKET = 53
    """Invalid or Unexpected Packet"""
    EPHIDGET_2BIG = 54
    """Argument List Too Long"""
    EPHIDGET_BADVERSION = 55
    """Bad Version"""
    EPHIDGET_CLOSED = 56
    """Channel was closed. This can happen if a channel is closed while openWaitForAttachment is waiting."""
    EPHIDGET_NOTCONFIGURED = 57
    """Device is not configured enough for this API call. Have a look at the must-set properties for this device and make sure to configure them first."""
    EPHIDGET_EOF = 31
    """End of File"""
    EPHIDGET_FAILSAFE = 59
    """Failsafe Triggered on this channel. Close and Re-open the channel to resume operation."""
    EPHIDGET_UNKNOWNVALHIGH = 60
    """The value has been measured to be higher than the valid range of the sensor."""
    EPHIDGET_UNKNOWNVALLOW = 61
    """The value has been measured to be lower than the valid range of the sensor."""
    EPHIDGET_BADPOWER = 62
    """The power supply of your device is outside the acceptable range to allow operation."""
    EPHIDGET_POWERCYCLE = 63
    """Something has caused your device to decide it needs to be powered off and on to resume operation."""
    EPHIDGET_HALLSENSOR = 64
    """The hall sensor on your Brushless DC Motor Controller is Improperly Connected"""
    EPHIDGET_BADCURRENT = 65
    """Current sensor offset outside acceptable bounds. Move the sensor aways from magnetic fields and try again."""
    EPHIDGET_BADCONNECTION = 66
    """One or more required connections on the device has been deemed faulty. Check your connections and try again."""
    EPHIDGET_NACK = 67
    """An external device has responded with a NACK response. Evaluate whether this is expected and try again."""
    EPHIDGET_REJECTED = 68
    """An external device has rejected the request. Evaluate whether this is expected and try again."""

    @classmethod
    def getName(cls, val):
        if val == cls.EPHIDGET_OK:
            return "EPHIDGET_OK"
        if val == cls.EPHIDGET_PERM:
            return "EPHIDGET_PERM"
        if val == cls.EPHIDGET_NOENT:
            return "EPHIDGET_NOENT"
        if val == cls.EPHIDGET_TIMEOUT:
            return "EPHIDGET_TIMEOUT"
        if val == cls.EPHIDGET_KEEPALIVE:
            return "EPHIDGET_KEEPALIVE"
        if val == cls.EPHIDGET_INTERRUPTED:
            return "EPHIDGET_INTERRUPTED"
        if val == cls.EPHIDGET_IO:
            return "EPHIDGET_IO"
        if val == cls.EPHIDGET_NOMEMORY:
            return "EPHIDGET_NOMEMORY"
        if val == cls.EPHIDGET_ACCESS:
            return "EPHIDGET_ACCESS"
        if val == cls.EPHIDGET_FAULT:
            return "EPHIDGET_FAULT"
        if val == cls.EPHIDGET_BUSY:
            return "EPHIDGET_BUSY"
        if val == cls.EPHIDGET_EXIST:
            return "EPHIDGET_EXIST"
        if val == cls.EPHIDGET_NOTDIR:
            return "EPHIDGET_NOTDIR"
        if val == cls.EPHIDGET_ISDIR:
            return "EPHIDGET_ISDIR"
        if val == cls.EPHIDGET_INVALID:
            return "EPHIDGET_INVALID"
        if val == cls.EPHIDGET_NFILE:
            return "EPHIDGET_NFILE"
        if val == cls.EPHIDGET_MFILE:
            return "EPHIDGET_MFILE"
        if val == cls.EPHIDGET_NOSPC:
            return "EPHIDGET_NOSPC"
        if val == cls.EPHIDGET_FBIG:
            return "EPHIDGET_FBIG"
        if val == cls.EPHIDGET_ROFS:
            return "EPHIDGET_ROFS"
        if val == cls.EPHIDGET_RO:
            return "EPHIDGET_RO"
        if val == cls.EPHIDGET_UNSUPPORTED:
            return "EPHIDGET_UNSUPPORTED"
        if val == cls.EPHIDGET_INVALIDARG:
            return "EPHIDGET_INVALIDARG"
        if val == cls.EPHIDGET_AGAIN:
            return "EPHIDGET_AGAIN"
        if val == cls.EPHIDGET_NOTEMPTY:
            return "EPHIDGET_NOTEMPTY"
        if val == cls.EPHIDGET_UNEXPECTED:
            return "EPHIDGET_UNEXPECTED"
        if val == cls.EPHIDGET_DUPLICATE:
            return "EPHIDGET_DUPLICATE"
        if val == cls.EPHIDGET_BADPASSWORD:
            return "EPHIDGET_BADPASSWORD"
        if val == cls.EPHIDGET_NETUNAVAIL:
            return "EPHIDGET_NETUNAVAIL"
        if val == cls.EPHIDGET_CONNREF:
            return "EPHIDGET_CONNREF"
        if val == cls.EPHIDGET_CONNRESET:
            return "EPHIDGET_CONNRESET"
        if val == cls.EPHIDGET_HOSTUNREACH:
            return "EPHIDGET_HOSTUNREACH"
        if val == cls.EPHIDGET_NODEV:
            return "EPHIDGET_NODEV"
        if val == cls.EPHIDGET_WRONGDEVICE:
            return "EPHIDGET_WRONGDEVICE"
        if val == cls.EPHIDGET_PIPE:
            return "EPHIDGET_PIPE"
        if val == cls.EPHIDGET_RESOLV:
            return "EPHIDGET_RESOLV"
        if val == cls.EPHIDGET_UNKNOWNVAL:
            return "EPHIDGET_UNKNOWNVAL"
        if val == cls.EPHIDGET_NOTATTACHED:
            return "EPHIDGET_NOTATTACHED"
        if val == cls.EPHIDGET_INVALIDPACKET:
            return "EPHIDGET_INVALIDPACKET"
        if val == cls.EPHIDGET_2BIG:
            return "EPHIDGET_2BIG"
        if val == cls.EPHIDGET_BADVERSION:
            return "EPHIDGET_BADVERSION"
        if val == cls.EPHIDGET_CLOSED:
            return "EPHIDGET_CLOSED"
        if val == cls.EPHIDGET_NOTCONFIGURED:
            return "EPHIDGET_NOTCONFIGURED"
        if val == cls.EPHIDGET_EOF:
            return "EPHIDGET_EOF"
        if val == cls.EPHIDGET_FAILSAFE:
            return "EPHIDGET_FAILSAFE"
        if val == cls.EPHIDGET_UNKNOWNVALHIGH:
            return "EPHIDGET_UNKNOWNVALHIGH"
        if val == cls.EPHIDGET_UNKNOWNVALLOW:
            return "EPHIDGET_UNKNOWNVALLOW"
        if val == cls.EPHIDGET_BADPOWER:
            return "EPHIDGET_BADPOWER"
        if val == cls.EPHIDGET_POWERCYCLE:
            return "EPHIDGET_POWERCYCLE"
        if val == cls.EPHIDGET_HALLSENSOR:
            return "EPHIDGET_HALLSENSOR"
        if val == cls.EPHIDGET_BADCURRENT:
            return "EPHIDGET_BADCURRENT"
        if val == cls.EPHIDGET_BADCONNECTION:
            return "EPHIDGET_BADCONNECTION"
        if val == cls.EPHIDGET_NACK:
            return "EPHIDGET_NACK"
        if val == cls.EPHIDGET_REJECTED:
            return "EPHIDGET_REJECTED"
        return "<invalid enumeration value>"
