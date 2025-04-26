import os
from enum import Enum
from typing import Optional

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.types_pb2 import CRS as CRSProto
    from cognite.seismic.protos.types_pb2 import GeoJson
    from cognite.seismic.protos.types_pb2 import Geometry as GeometryProto
    from cognite.seismic.protos.types_pb2 import InterpolationMethod as InterpolationMethodProto
    from cognite.seismic.protos.types_pb2 import Wkt
    from google.protobuf.json_format import MessageToDict
    from google.protobuf.struct_pb2 import Struct


class InterpolationMethod(Enum):
    """Method for interpolating between traces when filtering by linear geometries."""

    NearestTrace = 0
    "Set values to those of the nearest trace"
    InverseDistanceWeighting = 1
    "Linear interpolation between traces weighted by inverse distance"

    def _to_proto(self) -> "InterpolationMethodProto.ValueType":
        if self == InterpolationMethod.NearestTrace:
            return InterpolationMethodProto.Value("NEAREST_TRACE")
        elif self == InterpolationMethod.InverseDistanceWeighting:
            return InterpolationMethodProto.Value("INVERSE_DISTANCE_WEIGHTING")
        else:
            raise ValueError("Unrecognized InterpolationMethod")


class Geometry:
    """Represents a CRS + shape, in either a WKT format or a GeoJSON.

    Attributes:
        crs (str): The CRS of the shape.
        geojson (Optional[dict]): If exists, the GeoJSON representation of this shape
        wkt (Optional[str]): If exists, the Well Known Text representation of this shape
    """

    crs: str
    geojson: Optional[dict]
    wkt: Optional[str]

    def __init__(self, crs: str, *, geojson=None, wkt=None):
        if (geojson is None) and (wkt is None):
            raise ValueError("You must specify one of: geojson, wkt")
        if (geojson is not None) and (wkt is not None):
            raise ValueError("You must specify either of: geojson, wkt")
        self.crs = crs
        self.geojson = geojson
        self.wkt = wkt

    def __repr__(self):
        if self.geojson:
            return f"Geometry(crs={repr(self.crs)}, geojson={self.geojson})"
        else:
            return f"Geometry(crs={repr(self.crs)}, wkt={repr(self.wkt)})"

    @staticmethod
    def _from_proto(proto) -> Optional["Geometry"]:
        """Convert a Geometry proto into a Geometry object.

        May return None if neither geojson nor wkt are specified.
        """
        crs = proto.crs.crs
        geojson = MessageToDict(proto.geo.json) or None
        wkt = proto.wkt.geometry or None
        if geojson is None and wkt is None:
            return None
        return Geometry(crs=crs, geojson=geojson, wkt=wkt)

    def _to_proto(self):
        crs_proto = CRSProto(crs=self.crs)
        if self.geojson is not None:
            struct = Struct()
            struct.update(self.geojson)
            return GeometryProto(crs=crs_proto, geo=GeoJson(json=struct))
        if self.wkt is not None:
            return GeometryProto(crs=crs_proto, wkt=Wkt(geometry=self.wkt))
