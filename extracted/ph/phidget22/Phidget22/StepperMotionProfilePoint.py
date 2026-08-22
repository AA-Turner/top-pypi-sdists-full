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


class StepperMotionProfilePoint:
    """
    The drescription of the desired set of mevements

    Parameters
    ----------
    targetPosition : float, optional
        The position to move towards
    velocityLimit : float, optional
        The maximum velocity of the motion
    acceleration : float, optional
        The rate at which to accelerate
    time : float, optional
        The time after START to begin this movement
    """

    def __init__(self, targetPosition=0, velocityLimit=0, acceleration=0, time=0):
        self.targetPosition = targetPosition
        self.velocityLimit = velocityLimit
        self.acceleration = acceleration
        self.time = time

    def __str__(self):
        return (
            "[StepperMotionProfilePoint] ("
            "targetPosition: " + str(self.targetPosition) + ", "
            "velocityLimit: " + str(self.velocityLimit) + ", "
            "acceleration: " + str(self.acceleration) + ", "
            "time: " + str(self.time) + ")"
        )


class _CStepperMotionProfilePoint(ctypes.Structure):
    _fields_ = [
        ("_targetPosition", ctypes.c_double),
        ("_velocityLimit", ctypes.c_double),
        ("_acceleration", ctypes.c_double),
        ("_time", ctypes.c_double),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._targetPosition = obj.targetPosition
        c_struct._velocityLimit = obj.velocityLimit
        c_struct._acceleration = obj.acceleration
        c_struct._time = obj.time
        return c_struct

    def _to_python(self):
        obj = StepperMotionProfilePoint()
        if self._targetPosition is not None:
            obj.targetPosition = self._targetPosition
        if self._velocityLimit is not None:
            obj.velocityLimit = self._velocityLimit
        if self._acceleration is not None:
            obj.acceleration = self._acceleration
        if self._time is not None:
            obj.time = self._time
        return obj


__all__ = ["StepperMotionProfilePoint"]
