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


class GPGGA:
    """
    NMEA GGA Sentence

    Parameters
    ----------
    latitude : float, optional
        Latitude
    longitude : float, optional
        Longitude
    fixQuality : int, optional
        GPS quality indicator
    numSatellites : int, optional
        Number of satellites in use
    horizontalDilution : float, optional
        Horizontal dilution of precision
    altitude : float, optional
        Mean sea level altitude
    heightOfGeoid : float, optional
        Geoidal separation
    """

    def __init__(
        self,
        latitude=0,
        longitude=0,
        fixQuality=0,
        numSatellites=0,
        horizontalDilution=0,
        altitude=0,
        heightOfGeoid=0,
    ):
        self.latitude = latitude
        self.longitude = longitude
        self.fixQuality = fixQuality
        self.numSatellites = numSatellites
        self.horizontalDilution = horizontalDilution
        self.altitude = altitude
        self.heightOfGeoid = heightOfGeoid

    def __str__(self):
        return (
            "[GPGGA] ("
            "latitude: " + str(self.latitude) + ", "
            "longitude: " + str(self.longitude) + ", "
            "fixQuality: " + str(self.fixQuality) + ", "
            "numSatellites: " + str(self.numSatellites) + ", "
            "horizontalDilution: " + str(self.horizontalDilution) + ", "
            "altitude: " + str(self.altitude) + ", "
            "heightOfGeoid: " + str(self.heightOfGeoid) + ")"
        )


class _CGPGGA(ctypes.Structure):
    _fields_ = [
        ("_latitude", ctypes.c_double),
        ("_longitude", ctypes.c_double),
        ("_fixQuality", ctypes.c_int16),
        ("_numSatellites", ctypes.c_int16),
        ("_horizontalDilution", ctypes.c_double),
        ("_altitude", ctypes.c_double),
        ("_heightOfGeoid", ctypes.c_double),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._latitude = obj.latitude
        c_struct._longitude = obj.longitude
        c_struct._fixQuality = obj.fixQuality
        c_struct._numSatellites = obj.numSatellites
        c_struct._horizontalDilution = obj.horizontalDilution
        c_struct._altitude = obj.altitude
        c_struct._heightOfGeoid = obj.heightOfGeoid
        return c_struct

    def _to_python(self):
        obj = GPGGA()
        if self._latitude is not None:
            obj.latitude = self._latitude
        if self._longitude is not None:
            obj.longitude = self._longitude
        if self._fixQuality is not None:
            obj.fixQuality = self._fixQuality
        if self._numSatellites is not None:
            obj.numSatellites = self._numSatellites
        if self._horizontalDilution is not None:
            obj.horizontalDilution = self._horizontalDilution
        if self._altitude is not None:
            obj.altitude = self._altitude
        if self._heightOfGeoid is not None:
            obj.heightOfGeoid = self._heightOfGeoid
        return obj


__all__ = ["GPGGA"]
