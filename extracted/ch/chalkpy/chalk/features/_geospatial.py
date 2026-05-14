from dataclasses import dataclass
from typing import Any, List, Union

import numpy as np
import pyarrow as pa


@dataclass
class LatLon:
    lat: float
    lon: float

    def __init__(  # pyright: ignore[reportMissingSuperCall]
        self,
        lat: Union[int, float],
        lon: Union[int, float],
    ):
        """
        Initialize LatLon from various input formats.

        Args:
            lat: latitude value (float or int)
            lon: longitude value (float or int)
        """
        self.lat = float(lat)
        self.lon = float(lon)

    def to_list(self) -> List[float]:
        """Convert to list [lat, lon]"""
        return [self.lat, self.lon]

    def to_tuple(self) -> tuple:
        """Convert to tuple (lat, lon)"""
        return (self.lat, self.lon)

    def to_numpy(self) -> np.ndarray:
        """Convert to numpy array [lat, lon]"""
        return np.array([self.lat, self.lon], dtype=np.float64)

    def to_dict(self) -> dict:
        """Convert to dictionary with 'lat' and 'lon' keys"""
        return {"lat": self.lat, "lon": self.lon}

    def to_arrow_struct(self) -> pa.StructScalar:
        """Convert to PyArrow struct scalar"""
        struct_type = pa.struct([("lat", pa.float64()), ("lon", pa.float64())])
        return pa.scalar(self.to_dict(), type=struct_type)

    def to_arrow_array(self) -> pa.Array:
        """Convert to PyArrow array (single element)"""
        struct_type = pa.struct([("lat", pa.float64()), ("lon", pa.float64())])
        return pa.array([self.to_dict()], type=struct_type)

    @staticmethod
    def get_arrow_schema() -> pa.DataType:
        """Get the PyArrow schema for LatLon"""
        return pa.struct([("lat", pa.float64()), ("lon", pa.float64())])

    def __repr__(self) -> str:
        return f"LatLon(lat={self.lat}, lon={self.lon})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LatLon):
            return False
        return bool(np.isclose(self.lat, other.lat) and np.isclose(self.lon, other.lon))


@dataclass
class LatLonRadians:
    lat_radians: float
    lon_radians: float

    def __init__(  # pyright: ignore[reportMissingSuperCall]
        self,
        lat_radians: Union[int, float],
        lon_radians: Union[int, float],
    ):
        """
        Initialize LatLonRadians from various input formats.

        Args:
            lat_radians: Explicit latitude value in radians (used if data is None)
            lon_radians: Explicit longitude value in radians (used if data is None)
        """
        self.lat_radians = float(lat_radians)
        self.lon_radians = float(lon_radians)

    def to_list(self) -> List[float]:
        """Convert to list [lat_radians, lon_radians]"""
        return [self.lat_radians, self.lon_radians]

    def to_tuple(self) -> tuple:
        """Convert to tuple (lat_radians, lon_radians)"""
        return (self.lat_radians, self.lon_radians)

    def to_numpy(self) -> np.ndarray:
        """Convert to numpy array [lat_radians, lon_radians]"""
        return np.array([self.lat_radians, self.lon_radians], dtype=np.float64)

    def to_dict(self) -> dict:
        """Convert to dictionary with 'lat_radians' and 'lon_radians' keys"""
        return {"lat_radians": self.lat_radians, "lon_radians": self.lon_radians}

    def to_arrow_struct(self) -> pa.StructScalar:
        """Convert to PyArrow struct scalar"""
        struct_type = pa.struct([("lat_radians", pa.float64()), ("lon_radians", pa.float64())])
        return pa.scalar(self.to_dict(), type=struct_type)

    def to_arrow_array(self) -> pa.Array:
        """Convert to PyArrow array (single element)"""
        struct_type = pa.struct([("lat_radians", pa.float64()), ("lon_radians", pa.float64())])
        return pa.array([self.to_dict()], type=struct_type)

    @staticmethod
    def get_arrow_schema() -> pa.DataType:
        """Get the PyArrow schema for LatLonRadians"""
        return pa.struct([("lat_radians", pa.float64()), ("lon_radians", pa.float64())])

    def __repr__(self) -> str:
        return f"LatLonRadians(lat_radians={self.lat_radians}, lon_radians={self.lon_radians})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LatLonRadians):
            return False
        return bool(np.isclose(self.lat_radians, other.lat_radians) and np.isclose(self.lon_radians, other.lon_radians))
