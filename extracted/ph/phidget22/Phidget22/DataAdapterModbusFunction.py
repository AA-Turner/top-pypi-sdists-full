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


class DataAdapterModbusFunction(IntEnum):
    """
    Modbus function codes for coil, register, and diagnostic operations
    """

    MODBUS_COIL_READ = 1
    """Read coils (FC01)"""
    MODBUS_DISCRETE_INPUT_READ = 2
    """Read discrete inputs (FC02)"""
    MODBUS_REGISTER_READ_HOLDING = 3
    """Read holding registers (FC03)"""
    MODBUS_REGISTER_READ_INPUT = 4
    """Read input registers (FC04)"""
    MODBUS_COIL_WRITE_SINGLE = 5
    """Write single coil (FC05)"""
    MODBUS_REGISTER_WRITE_SINGLE = 6
    """Write single register (FC06)"""
    MODBUS_COIL_WRITE_MULTIPLE = 15
    """Write multiple coils (FC15)"""
    MODBUS_REGISTER_WRITE_MULTIPLE = 16
    """Write multiple registers (FC16)"""

    @classmethod
    def getName(cls, val):
        if val == cls.MODBUS_COIL_READ:
            return "MODBUS_COIL_READ"
        if val == cls.MODBUS_DISCRETE_INPUT_READ:
            return "MODBUS_DISCRETE_INPUT_READ"
        if val == cls.MODBUS_REGISTER_READ_HOLDING:
            return "MODBUS_REGISTER_READ_HOLDING"
        if val == cls.MODBUS_REGISTER_READ_INPUT:
            return "MODBUS_REGISTER_READ_INPUT"
        if val == cls.MODBUS_COIL_WRITE_SINGLE:
            return "MODBUS_COIL_WRITE_SINGLE"
        if val == cls.MODBUS_REGISTER_WRITE_SINGLE:
            return "MODBUS_REGISTER_WRITE_SINGLE"
        if val == cls.MODBUS_COIL_WRITE_MULTIPLE:
            return "MODBUS_COIL_WRITE_MULTIPLE"
        if val == cls.MODBUS_REGISTER_WRITE_MULTIPLE:
            return "MODBUS_REGISTER_WRITE_MULTIPLE"
        return "<invalid enumeration value>"
