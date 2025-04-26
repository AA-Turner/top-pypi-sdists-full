import os
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Mapping, Optional, Tuple, Union

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.types_pb2 import CRS, GeoJson, Geometry, Wkt
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import CoverageSpec, Identifier
    from google.protobuf.struct_pb2 import Struct
    from google.protobuf.timestamp_pb2 import Timestamp


Metadata = Dict[str, str]
LineRange = Union[Tuple[int, int], Tuple[int, int, int]]


def _timestamp_to_datetime(ts: "Timestamp") -> datetime:
    """Works around protobuf 3.19 not supporting timezone argument in Timestamp.ToDatetime"""
    return datetime.fromtimestamp(ts.seconds + ts.nanos * 1e-9, timezone.utc)


class Direction(Enum):
    """Enum of the major direction of VolumeDefs"""

    INLINE = 0
    XLINE = 1


def _get_identifier(id: Optional[int] = None, external_id: Optional[str] = None) -> "Identifier":
    """Turn an id or external id into a v1.Identifier.

    Returns:
        Identifier: The created Identifier
    """
    if (id is not None) and (external_id is not None):
        raise Exception("You should only specify one of: id, external_id")
    if id is not None:
        return Identifier(id=id)
    elif external_id is not None:
        return Identifier(external_id=external_id)
    raise Exception("You must specify at least one of: id, external_id")


def _get_coverage_spec(crs: Optional[str] = None, format: Optional[str] = None) -> "CoverageSpec":
    """Turns an optional crs and an optional string into a CoverageSpec."""
    if format is None:
        format = "wkt"

    if format == "wkt":
        return CoverageSpec(crs=crs or "", format=CoverageSpec.Format.WKT)
    elif format == "geojson":
        return CoverageSpec(crs=crs or "", format=CoverageSpec.Format.GEOJSON)
    else:
        raise ValueError(f"Unknown format {format}")


def make_geometry(crs: Optional[str] = None, wkt: Optional[str] = None, geo_json: Optional[dict] = None):
    """Make a Geometry proto from python sdk arguments"""

    if wkt is not None and geo_json is not None:
        raise ValueError("Provide either wkt or gejson, not both")

    wrapped_crs = None if crs is None else CRS(crs=crs)

    if wkt is not None:
        return Geometry(crs=wrapped_crs, wkt=Wkt(geometry=wkt))
    elif geo_json is not None:
        geo_json_struct = Struct()
        geo_json_struct.update(geo_json)
        return Geometry(crs=wrapped_crs, geo=GeoJson(json=geo_json_struct))
    else:
        return None


def _get_exact_match_filter(metadata: Mapping[str, str]):
    """Create an exact key-value match for SearchSpec"""

    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import Filter, KeyValueExactMatch, MetadataFilter

    metadata_filter = MetadataFilter()
    for key, val in metadata.items():
        filter = Filter(key_value_exact_match=KeyValueExactMatch(key=key, value=val))
        metadata_filter.filters.append(filter)
    return metadata_filter


# The minimum seconds (float) of sleeping
_MIN_SLEEPING = 0.1
_MAX_SLEEPING = 5.0


def _backoffs():
    sleeping = _MIN_SLEEPING
    while True:
        yield sleeping
        sleeping = min(sleeping * 2, _MAX_SLEEPING)
