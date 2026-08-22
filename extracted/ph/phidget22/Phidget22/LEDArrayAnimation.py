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
from Phidget22.LEDArrayAnimationType import LEDArrayAnimationType


class LEDArrayAnimation:
    """
    LED animation description

    Parameters
    ----------
    startAddress : int, optional
        Which LED to start the animation from
    endAddress : int, optional
        Which LED the animation will end on
    time : int, optional
        Time between changes in ms
    animationType : LEDArrayAnimationType, optional
        The type of animation
    """

    def __init__(
        self,
        startAddress=0,
        endAddress=0,
        time=0,
        animationType=LEDArrayAnimationType.ANIMATION_TYPE_FORWARD_SCROLL,
    ):
        self.startAddress = startAddress
        self.endAddress = endAddress
        self.time = time
        self.animationType = animationType

    def __str__(self):
        return (
            "[LEDArrayAnimation] ("
            "startAddress: " + str(self.startAddress) + ", "
            "endAddress: " + str(self.endAddress) + ", "
            "time: " + str(self.time) + ", "
            "animationType: " + str(LEDArrayAnimationType.getName(self.animationType)) + ")"
        )


class _CLEDArrayAnimation(ctypes.Structure):
    _fields_ = [
        ("_startAddress", ctypes.c_uint32),
        ("_endAddress", ctypes.c_uint32),
        ("_time", ctypes.c_uint32),
        ("_animationType", ctypes.c_int),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._startAddress = obj.startAddress
        c_struct._endAddress = obj.endAddress
        c_struct._time = obj.time
        c_struct._animationType = obj.animationType
        return c_struct

    def _to_python(self):
        obj = LEDArrayAnimation()
        if self._startAddress is not None:
            obj.startAddress = self._startAddress
        if self._endAddress is not None:
            obj.endAddress = self._endAddress
        if self._time is not None:
            obj.time = self._time
        if self._animationType is not None:
            obj.animationType = LEDArrayAnimationType(self._animationType)
        return obj


__all__ = ["LEDArrayAnimation", "LEDArrayAnimationType"]
