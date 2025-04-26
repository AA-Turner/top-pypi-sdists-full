from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np
from cognite.seismic.data_classes.extents import RangeInclusive, TraceHeaderField


@dataclass
class ArrayData:
    """Encapsulates the array returned from :py:meth:`~TracesAPI.get_array`,
    along with metadata about coordinates. Below, the number d refers to the dimensionality
    of the requested seismic object, and is either 2 or 3. The number p is 1 for pre-stack data
    and 0 for post-stack data.

    Attributes:
        trace_data (:py:class:`~numpy.ma.MaskedArray`):
            (d+p)-dimensional numpy MaskedArray containing the requested trace data. The first d-1 dimensions are indexed
            by (inline, crossline) for 3d data, and the 2d header (cdp, shotpoint or energy_source_point) for 2d data.
            Prestack data will have a dimension following these for the `cdp_trace` indexing.
            The last dimension indexes the depth.
        crs: The coordinate system used
        coord_x (:py:class:`~numpy.ma.MaskedArray`):
            (d-1)-dimensional array containing the x coordinate of the corresponding trace in `trace_data`
        coord_y (:py:class:`~numpy.ma.MaskedArray`):
            (d-1)-dimensional array containing the y coordinate of the corresponding trace in `trace_data`
        z_range (:py:class:`~cognite.seismic.RangeInclusive`):
            The range of depth indices described by the last dimension of `trace_data`
        cdp_trace_range (:py:class:`~cognite.seismic.RangeInclusive`):
            The range of `CDP_TRACE` headers that will be returned. Only populated for pre-stack data.

    If the queried object is 3D, the returned data will be :py:class:`ArrayData3d`.
    If the queried object is 2d, the returned data will be :py:class:`ArrayData2d`.
    These subclasses contain additional information about the array.
    """

    trace_data: np.ma.MaskedArray
    crs: str
    coord_x: np.ma.MaskedArray
    coord_y: np.ma.MaskedArray
    cdp_trace_range: Optional[RangeInclusive]
    z_range: RangeInclusive


@dataclass
class ArrayData3d(ArrayData):
    """Encapsulates the array returned from :py:meth:`~TracesAPI.get_array`, with 3d-specific
    information. In addition to the fields in :py:class:`ArrayData`, there are the fields:

    Attributes:
        inline_range (:py:class:`~cognite.seismic.RangeInclusive`):
            The range of inline numbers described by the first dimension of the `trace_data`,
            or None if the array is empty
        xline_range (:py:class:`~cognite.seismic.RangeInclusive`):
            The range of xline numbers described by the second dimension of the `trace_data`,
            or None if the array is empty
    """

    inline_range: Optional[RangeInclusive]
    xline_range: Optional[RangeInclusive]

    def __repr__(self) -> str:
        return f"""ArrayData3d(
    trace_data=<array of shape {self.trace_data.shape}>,
    crs={repr(self.crs)},
    coord_x=<array of shape {self.coord_x.shape}>,
    coord_y=<array of shape {self.coord_x.shape}>,
    inline_range={repr(self.inline_range)},
    xline_range={repr(self.xline_range)},
    cdp_trace_range={repr(self.cdp_trace_range)},
    z_range={repr(self.z_range)}
)"""


@dataclass
class ArrayData2d(ArrayData):
    """Encapsulates the array returned from :py:meth:`~TracesAPI.get_array`, with 2d-specific
    information. In addition to the fields in :py:class:`ArrayData`, there are the fields:

    Attributes:
        trace_key_header (:py:class:`~cognite.seismic.TraceHeaderField`):
            Which trace header the array is indexed by
        trace_key_values (:py:class:`~numpy.ma.MaskedArray`):
            1-dimensional array containing the values of the given trace key header
            for each corresponding trace in `trace_data`
    """

    trace_key_header: TraceHeaderField
    trace_key_values: np.ma.MaskedArray

    def __repr__(self) -> str:
        return f"""ArrayData2d(
    trace_data=<array of shape {self.trace_data.shape}>,
    crs={repr(self.crs)},
    coord_x=<array of shape {self.coord_x.shape}>,
    coord_y=<array of shape {self.coord_y.shape}>,
    trace_key_header={repr(self.trace_key_header)},
    trace_key_values=<array of shape {self.trace_key_values.shape}>,
    cdp_trace_range={repr(self.cdp_trace_range)},
    z_range={repr(self.z_range)}
)"""


@dataclass
class TraceBounds:
    """Information about the traces that would be returned from a corresponding
    :py:meth:`~TracesAPI.stream_traces` call

    Attributes:
        num_traces (int): The number of traces that will be streamed
        sample_count (int): The number of samples in each trace
        size_kilobytes (int): An estimate of the total streaming size in kilobytes (= 1024 bytes)
        crs (str): The coordinate reference system the returned trace coordinates will be given in
        z_range (:py:class:`~cognite.seismic.RangeInclusive`):
            The range of depth indices that will be returned in each trace
        cdp_trace_range (:py:class:`~cognite.seismic.RangeInclusive`):
            The range of `CDP_TRACE` headers that will be returned. Only populated for pre-stack data.

    If the queried object is a 3D object and was not queried by a line-like geometry,
    the returned bounds will be :py:class:`TraceBounds3d`. If the queried object is 2D,
    the returned bounds will be :py:class:`TraceBounds2d`. These subclasses contain additional
    information about the trace bounds.
    """

    num_traces: int
    sample_count: int
    size_kilobytes: int
    crs: str
    cdp_trace_bounds: Optional[RangeInclusive]
    z_range: RangeInclusive

    @staticmethod
    def _from_proto(proto) -> "TraceBounds":
        num_traces = proto.num_traces
        size_kilobytes = (num_traces * proto.trace_size_bytes) // 1024
        sample_count = proto.sample_count
        crs = proto.crs
        z_range = RangeInclusive._from_proto(proto.z_range)
        if proto.HasField("cdp_trace_bounds"):
            cdp_trace_bounds = RangeInclusive._from_proto(proto.cdp_trace_bounds)
        else:
            cdp_trace_bounds = None

        if proto.HasField("three_dee_bounds"):
            bounds = proto.three_dee_bounds
            inline_bounds = None
            xline_bounds = None
            if bounds.HasField("inline"):
                inline_bounds = RangeInclusive._from_proto(bounds.inline)
            if bounds.HasField("crossline"):
                xline_bounds = RangeInclusive._from_proto(proto.three_dee_bounds.crossline)
            return TraceBounds3d(
                num_traces=num_traces,
                size_kilobytes=size_kilobytes,
                sample_count=sample_count,
                crs=crs,
                z_range=z_range,
                inline_bounds=inline_bounds,
                xline_bounds=xline_bounds,
                cdp_trace_bounds=cdp_trace_bounds,
            )
        elif proto.HasField("two_dee_bounds"):
            requested_bounds = proto.two_dee_bounds.requested_bounds
            trace_key_header = TraceHeaderField._from_proto(requested_bounds.trace_key)
            trace_key_bounds = None
            if requested_bounds.HasField("trace_range"):
                trace_key_bounds = RangeInclusive._from_proto(requested_bounds.trace_range)
            return TraceBounds2d(
                num_traces=num_traces,
                size_kilobytes=size_kilobytes,
                sample_count=sample_count,
                crs=crs,
                z_range=z_range,
                trace_key_header=trace_key_header,
                trace_key_bounds=trace_key_bounds,
                cdp_trace_bounds=cdp_trace_bounds,
            )
        else:
            return TraceBounds(
                num_traces=num_traces,
                size_kilobytes=size_kilobytes,
                sample_count=sample_count,
                crs=crs,
                z_range=z_range,
                cdp_trace_bounds=cdp_trace_bounds,
            )


@dataclass
class TraceBounds3d(TraceBounds):
    """Information about the traces that would be returned from a corresponding
    :py:meth:`~TracesAPI.stream_traces` call, with 3d-specific information. In
    addition to the fields in :py:class:`TraceBounds`, there are the following
    fields:

    Attributes:
        inline_bounds (:py:class:`~cognite.seismic.RangeInclusive`):
            The smallest range including all the returned inline numbers, or None if there are none.
        xline_bounds (:py:class:`~cognite.seismic.RangeInclusive`):
            The smallest range including all the returned xline numbers, or None if there are none.
    """

    inline_bounds: Optional[RangeInclusive]
    xline_bounds: Optional[RangeInclusive]


@dataclass
class TraceBounds2d(TraceBounds):
    """Information about the traces that would be returned from a corresponding
    :py:meth:`~TracesAPI.stream_traces` call, with 2d-specific information. In
    addition to the fields in :py:class:`TraceBounds`, there are the following
    fields:

    Attributes:
        trace_key_header (:py:class:`~cognite.seismic.TraceHeaderField`):
            The trace header the array is indexed by
        trace_key_bounds (:py:class:`~cognite.seismic.RangeInclusive`):
            The smallest range including all the returned trace key values, or None if there are none.
    """

    trace_key_header: TraceHeaderField
    trace_key_bounds: Optional[RangeInclusive]


@dataclass
class Coordinate:
    """Represents physical coordinates in a given CRS.

    Attributes:
        crs (str): The coordinate reference system of the coordinate. Generally should be an EPSG code.
        x (float): The x value of the coordinate.
        y (float): The y value of the coordinate.
    """

    crs: str
    x: float
    y: float

    @staticmethod
    def _from_proto(proto) -> "Coordinate":
        return Coordinate(crs=proto.crs, x=proto.x, y=proto.y)


@dataclass
class Trace:
    """Represents a seismic trace identified by a single (inline, xline) pair
    (if the underlying object is 3D) or a single 2D header value (if 2D).

    Attributes:
        trace_header (bytes): The raw trace header.
        inline (int): The inline number, if available
        xline (int): The xline number, if available
        cdp (int): The cdp number, if available
        shotpoint (int): The shotpoint number, if available
        energy_source_point (int): The energy source point number, if available
        cdp_trace (int): The cdp trace number, if available
        offset (int): The offset number, if available
        trace (List[float]): The trace values
        coordinate (:py:class:`Coordinate`): The coordinate of the trace
    """

    trace_header: bytes = field(repr=False)
    inline: Optional[int]
    xline: Optional[int]
    cdp: Optional[int]
    shotpoint: Optional[int]
    energy_source_point: Optional[int]
    cdp_trace: Optional[int]
    offset: Optional[int]
    trace: List[float]
    coordinate: Coordinate

    @staticmethod
    def _from_proto(proto) -> "Trace":
        def get_or_none(name):
            return getattr(proto, name).value if proto.HasField(name) else None

        return Trace(
            trace_header=proto.trace_header,
            inline=get_or_none("iline"),
            xline=get_or_none("xline"),
            cdp=get_or_none("cdp"),
            shotpoint=get_or_none("shotpoint"),
            energy_source_point=get_or_none("energy_source_point"),
            cdp_trace=get_or_none("cdp_trace"),
            offset=get_or_none("offset"),
            trace=proto.trace,
            coordinate=Coordinate._from_proto(proto.coordinate),
        )
