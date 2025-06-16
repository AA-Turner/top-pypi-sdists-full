import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, Iterator, List, Mapping, Optional, Set, Tuple, Union

from cognite.seismic._api.utility import Direction, LineRange
from cognite.seismic.data_classes.errors import Seismic3dDefHeaderError
from cognite.seismic.data_classes.geometry import Geometry

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.types_pb2 import LineDescriptor
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import MinorLines
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import Seismic2dExtent as Seismic2dExtentProto
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import Seismic3dDef as Seismic3dDefProto
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import Seismic3dExtent as Seismic3dExtentProto
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import Seismic3dRect as Seismic3dRectProto
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import Seismic3dRects as Seismic3dRectsProto
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import SeismicCutout as SeismicCutoutProto
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import SeismicExtent as SeismicExtentProto
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import (
        SeismicTraceGroupExtent as SeismicTraceGroupExtentProto,
    )
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import (
        SeismicTraceGroupLines as SeismicTraceGroupLinesProto,
    )
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import TraceHeaderField as TraceHeaderFieldProto
    from cognite.seismic.protos.v1.seismic_service_messages_pb2 import (
        CreateSeismicRequest,
        SegYSeismicRequest,
        StreamTracesRequest,
    )
    from google.protobuf.wrappers_pb2 import Int32Value as i32


class TraceHeaderField(Enum):
    """Used to reference a key trace header field."""

    INLINE = 3
    "Inline number in a 3D grid"
    CROSSLINE = 4
    "Crossline number in a 3d grid"

    CDP = 2
    "Common depth point number"
    ENERGY_SOURCE_POINT = 1
    """Energy source point number. Usually means the same as shotpoint, but has
    a different standard location according to the SEGY spec."""
    SHOTPOINT = 5
    """Shotpoint number. Usually means the same as energy source point, but has
    a different standard location according to the SEGY spec."""

    CDP_TRACE = 6
    """Trace number within ensemble.
    Used by prestack migrated files."""

    OFFSET = 7
    """Distance from center of source point to the center of the receiver group.
    Used by prestack migrated files."""

    @staticmethod
    def _from_proto(proto) -> "TraceHeaderField":
        if proto is None or proto < 1 or proto > 7:
            raise ValueError(f"Unrecognized TraceHeaderField: {proto}")
        return TraceHeaderField(proto)

    def _to_proto(self):
        return TraceHeaderFieldProto.values()[self.value]

    # The default repr gives the enum value, which is a bit more detail than needed for end users.
    # The str value is a bit nicer.
    def __repr__(self):
        return str(self)


class RangeInclusive:
    """Represents an inclusive range of inlines/xlines or depth coordinates.

    Attributes:
        start: The first linenumber encompassed by the range
        stop: The last linenumber encompassed by the range
        step: The distance between linenumbers"""

    start: int
    stop: int
    step: int

    def __init__(self, start: int, stop: int, step: Optional[int] = None):
        if step == 0:
            raise ValueError("RangeInclusive(): step must be nonzero")
        if step is None:
            step = 1 if stop >= start else -1
        self.start = start
        self.stop = start + ((stop - start) // step) * step
        self.step = step

    @staticmethod
    def _from_proto(proto: "LineDescriptor") -> "RangeInclusive":
        start = proto.min.value
        if start is None:
            raise ValueError("LineDescriptor: start is None")
        stop = proto.max.value
        if stop is None:
            raise ValueError("LineDescriptor: stop is None")
        step = proto.step.value if proto.step is not None and proto.step.value != 0 else 1
        return RangeInclusive(start, stop, step)

    @staticmethod
    def from_linerange(linerange: LineRange) -> "RangeInclusive":
        """Construct a RangeInclusive from a (start, stop) or (start, stop, step) tuple"""
        if len(linerange) == 2:
            if linerange[0] < linerange[1]:
                step = 1
            else:
                step = -1
            return RangeInclusive(linerange[0], linerange[1], step)
        elif len(linerange) == 3:
            return RangeInclusive(*linerange)
        else:
            raise ValueError("LineRange must have 2 or 3 elements")

    @staticmethod
    def _from_inds(inds: Iterable[int]) -> List["RangeInclusive"]:
        """Builds an optimal list of ranges from a list of indices"""

        def pop_range(first: int, sorted_rest: Iterator[int]) -> Tuple["RangeInclusive", Optional[int]]:
            step = 1
            prev = None
            for cur in sorted_rest:
                if prev is None:
                    step = cur - first
                    prev = cur
                else:
                    if prev + step == cur:
                        prev = cur
                    else:
                        return RangeInclusive(first, prev, step), cur
            if prev is None:
                return RangeInclusive(first, first), None
            else:
                return RangeInclusive(first, cur, step), None

        inds = iter(sorted(inds))
        ranges = []
        first = None
        try:
            first = next(inds)
        except StopIteration:
            pass
        while first is not None:
            r, first = pop_range(first, inds)
            ranges.append(r)

        return ranges

    def _to_proto(self) -> "LineDescriptor":
        this = self.to_positive()
        step = None if this.step == 1 else i32(value=this.step)
        return LineDescriptor(min=i32(value=this.start), max=i32(value=this.stop), step=step)

    @staticmethod
    def _widest(ranges: Iterable[Tuple[int, int]]) -> "RangeInclusive":
        """Finds the widest range among the (min, max) tuples in ranges, and returns the result as a RangeInclusive"""
        min_start = None
        max_stop = None
        for start, stop in ranges:
            if min_start is None or start < min_start:
                min_start = start
            if max_stop is None or stop > max_stop:
                max_stop = stop
        if min_start is None or max_stop is None:
            raise ValueError("Empty range")
        return RangeInclusive(min_start, max_stop)

    def index(self, line: int) -> int:
        """Compute the index of a given linenumber in this range"""
        out_of_range = ValueError(f"line {line} out of range")
        incompatible = ValueError(f"line {line} incompatible with step {self.step} starting from {self.start}")
        if self.step > 0:
            if line < self.start or line > self.stop:
                raise out_of_range
            if (line - self.start) % self.step != 0:
                raise incompatible
            return (line - self.start) // self.step
        else:
            if line > self.start or line < self.stop:
                raise out_of_range
            if (line - self.start) % self.step != 0:
                raise incompatible
            return (self.start - line) // (-self.step)

    def to_linerange(self) -> LineRange:
        """Return a (start, stop) or a (start, stop, step) tuple"""
        if self.step == 1:
            return (self.start, self.stop)
        else:
            return (self.start, self.stop, self.step)

    def to_positive(self) -> "RangeInclusive":
        """Return an equivalent RangeInclusive where the step size is always positive"""
        if self.step > 0:
            return self
        else:
            return RangeInclusive(self.stop, self.start, -self.step)

    def __len__(self) -> int:
        """Return the number of lines described by this range"""
        return (self.stop - self.start) // self.step + 1

    def __iter__(self):
        cur = self.start
        while (self.step > 0 and cur <= self.stop) or (self.step < 0 and cur >= self.stop):
            yield cur
            cur += self.step

    def __contains__(self, line: int) -> bool:
        return line >= self.start and line <= self.stop and (line - self.start) % self.step == 0

    def __repr__(self):
        return f"RangeInclusive({self.start}, {self.stop}, {self.step})"

    def __eq__(self, other):
        same_start_stop = self.start == other.start and self.stop == other.stop
        if self.start == self.stop:
            # Singleton ranges, so it doesn't matter what the steps are
            return same_start_stop
        else:
            return same_start_stop and self.step == other.step


class SeismicCutout(ABC):
    """
    Describes how a Seismic object is cut out of the containing
    SeismicStore. This is an abstract class: Concrete instances will be one of the following:

    * A subclass of :py:class:`SeismicExtent` for describing exactly which traces to include
    * A geometry wrapped in a :py:class:`GeometryCutout` object
    * :py:class:`EmptyCutout` to explicitly describe an empty seismic object
    * :py:class:`FullCutout` to describe a seismic containing all the data in the seismic store
    """

    @abstractmethod
    def _to_cutout_proto(self) -> "SeismicCutoutProto":
        pass

    @abstractmethod
    def _merge_into_create_seismic_request(self, request: "CreateSeismicRequest"):
        pass

    @staticmethod
    def _from_cutout_proto(proto: "SeismicCutoutProto") -> "SeismicCutout":
        if proto.HasField("two_dee_extent"):
            return Seismic2dExtent._from_proto(proto.two_dee_extent)
        elif proto.HasField("three_dee_extent"):
            return Seismic3dExtent._from_proto(proto.three_dee_extent)
        elif proto.HasField("geometry"):
            geometry = Geometry._from_proto(proto.geometry)
            if geometry is None:
                raise Exception("Invalid SeismicCutout protobuf")
            return GeometryCutout(geometry=geometry)
        elif proto.empty:
            return EmptyCutout()
        elif proto.full:
            return FullCutout()
        else:
            raise Exception("Invalid SeismicCutout protobuf")


class SeismicExtent(SeismicCutout):
    """Describes a selection of traces in a seismic object. This is an abstract
    class: Concrete instances will be either :py:class:`Seismic2dExtent` or a
    subclass of :py:class:`Seismic3dExtent`"""

    @staticmethod
    def _from_extent_proto(proto: "SeismicExtentProto") -> "SeismicExtent":
        if proto.HasField("two_dee_extent"):
            return Seismic2dExtent._from_proto(proto.two_dee_extent)
        elif proto.HasField("three_dee_extent"):
            return Seismic3dExtent._from_proto(proto.three_dee_extent)
        else:
            raise Exception("Invalid SeismicExtent protobuf")

    @abstractmethod
    def _to_extent_proto(self) -> "SeismicExtentProto":
        pass

    @abstractmethod
    def dimensions(self) -> int:
        pass

    @abstractmethod
    def _merge_into_stream_traces_request(self, request: "StreamTracesRequest"):
        pass

    @abstractmethod
    def _merge_into_segy_seismic_request(self, request: "SegYSeismicRequest"):
        pass


@dataclass
class EmptyCutout(SeismicCutout):
    """Describes an empty cutout"""

    def _to_cutout_proto(self) -> "SeismicCutoutProto":
        return SeismicCutoutProto(empty=True)

    def _merge_into_create_seismic_request(self, request: "CreateSeismicRequest"):
        request.empty = True


@dataclass
class FullCutout(SeismicCutout):
    """Describes a cutout filling its entire containing seismic store"""

    def _to_cutout_proto(self) -> "SeismicCutoutProto":
        return SeismicCutoutProto(full=True)

    def _merge_into_create_seismic_request(self, request: "CreateSeismicRequest"):
        # Leave the volume oneof as null
        pass


@dataclass
class GeometryCutout(SeismicCutout):
    """Describes a cutout by a geometry.

    Attributes:
        geometry(:py:class:`~cognite.seismic.Geometry`): The geometry to cut by
    """

    geometry: Geometry

    def _to_cutout_proto(self) -> "SeismicCutoutProto":
        return SeismicCutoutProto(geometry=self.geometry._to_proto())

    def _merge_into_create_seismic_request(self, request: "CreateSeismicRequest"):
        request.geometry.MergeFrom(self.geometry._to_proto())


@dataclass
class Seismic2dExtent(SeismicExtent):
    """Describes a selection of traces in a 2d seismic object.

    Attributes:
        trace_key (:py:class:`TraceHeaderField`): Which trace header field to select traces by
        ranges (List[:py:class:`RangeInclusive`]): A list of ranges of trace header values to include
    """

    trace_key: TraceHeaderField
    ranges: List[RangeInclusive]

    @staticmethod
    def from_lineranges(trace_key: TraceHeaderField, ranges: Iterable[LineRange]) -> "Seismic2dExtent":
        return Seismic2dExtent(trace_key, [RangeInclusive.from_linerange(r) for r in ranges])

    @staticmethod
    def cdp_ranges(ranges: Iterable[LineRange]) -> "Seismic2dExtent":
        """Create an extent filtering by a union of cdp ranges"""
        return Seismic2dExtent.from_lineranges(TraceHeaderField.CDP, ranges)

    @staticmethod
    def cdp_range(range: LineRange) -> "Seismic2dExtent":
        """Create an extent filtering by a single cdp range"""
        return Seismic2dExtent.cdp_ranges([range])

    @staticmethod
    def shotpoint_ranges(ranges: Iterable[LineRange]) -> "Seismic2dExtent":
        """Create an extent filtering by a union of shotpoint ranges"""
        return Seismic2dExtent.from_lineranges(TraceHeaderField.SHOTPOINT, ranges)

    @staticmethod
    def shotpoint_range(range: LineRange) -> "Seismic2dExtent":
        """Create an extent filtering by a single shotpoint range"""
        return Seismic2dExtent.shotpoint_ranges([range])

    @staticmethod
    def energy_source_point_ranges(ranges: Iterable[LineRange]) -> "Seismic2dExtent":
        """Create an extent filtering by a union of energy source point ranges"""
        return Seismic2dExtent.from_lineranges(TraceHeaderField.ENERGY_SOURCE_POINT, ranges)

    @staticmethod
    def energy_source_point_range(range: LineRange) -> "Seismic2dExtent":
        """Create an extent filtering by a single energy source point range"""
        return Seismic2dExtent.energy_source_point_ranges([range])

    @staticmethod
    def _from_proto(proto: "Seismic2dExtentProto") -> "Seismic2dExtent":
        trace_key = TraceHeaderField._from_proto(proto.trace_key)
        ranges = [RangeInclusive._from_proto(ld) for ld in proto.trace_ranges]
        return Seismic2dExtent(trace_key=trace_key, ranges=ranges)

    def _to_2d_extent_proto(self) -> "Seismic2dExtentProto":
        trace_ranges = [r._to_proto() for r in self.ranges]
        return Seismic2dExtentProto(trace_key=self.trace_key._to_proto(), trace_ranges=trace_ranges)

    def _to_extent_proto(self) -> "SeismicExtentProto":
        return SeismicExtentProto(two_dee_extent=self._to_2d_extent_proto())

    def _to_cutout_proto(self) -> "SeismicCutoutProto":
        return SeismicCutoutProto(two_dee_extent=self._to_2d_extent_proto())

    def _merge_into_create_seismic_request(self, request: "CreateSeismicRequest"):
        request.two_dee_extent.MergeFrom(self._to_2d_extent_proto())

    def _merge_into_stream_traces_request(self, request: "StreamTracesRequest"):
        request.two_dee_extent.MergeFrom(self._to_2d_extent_proto())

    def _merge_into_segy_seismic_request(self, request: "SegYSeismicRequest"):
        request.two_dee_extent.MergeFrom(self._to_2d_extent_proto())

    def dimensions(self) -> int:
        return 2


class Seismic3dExtent(SeismicExtent):
    """Describes a selection of traces in a 3d seismic object. This is an abstract
    class: Concrete instances will be either :py:class:`Seismic3dRect`,
    :py:class:`Seismic3dRects`, or :py:class:`Seismic3dDef`"""

    @staticmethod
    def _from_proto(proto: "Seismic3dExtentProto") -> "Seismic3dExtent":
        if proto.HasField("rects"):
            if len(proto.rects.rects) == 1:
                return Seismic3dRect._from_rect_proto(proto.rects.rects[0])
            else:
                return Seismic3dRects._from_rects_proto(proto.rects)
        elif proto.HasField("def"):
            return Seismic3dDef._from_3d_def_proto(getattr(proto, "def"))
        else:
            raise Exception("Invalid Seimsic3dExtent proto")

    @abstractmethod
    def _to_3d_extent_proto(self) -> "Seismic3dExtentProto":
        pass

    def _to_extent_proto(self) -> "SeismicExtentProto":
        return SeismicExtentProto(three_dee_extent=self._to_3d_extent_proto())

    def _to_cutout_proto(self) -> "SeismicCutoutProto":
        return SeismicCutoutProto(three_dee_extent=self._to_3d_extent_proto())

    def _merge_into_create_seismic_request(self, request: "CreateSeismicRequest"):
        request.three_dee_extent.MergeFrom(self._to_3d_extent_proto())

    def _merge_into_stream_traces_request(self, request: "StreamTracesRequest"):
        request.three_dee_extent.MergeFrom(self._to_3d_extent_proto())

    def _merge_into_segy_seismic_request(self, request: "SegYSeismicRequest"):
        request.three_dee_extent.MergeFrom(self._to_3d_extent_proto())

    def dimensions(self) -> int:
        return 3

    @abstractmethod
    def get_xline(self, inline: int) -> List[int]:
        """Get every crossline for a given inline

        Returns:
            A list of crosslines"""
        pass

    @abstractmethod
    def get_inline(self, xline: int) -> List[int]:
        """Get every inline for a given crossline

        Returns:
            A list of inlines"""
        pass

    @abstractmethod
    def get_inline_ranges(self) -> Mapping[int, Tuple[int, int]]:
        """Get the minimum and maximum inlines for each crossline

        Returns:
            A mapping inline->[crossline min, crossline max]"""
        pass

    @abstractmethod
    def get_xline_ranges(self) -> Mapping[int, Tuple[int, int]]:
        """Get the minimum and maximum crosslines for each inline.

        Returns:
            A mapping inline->[crossline min, crossline max]
        """
        pass

    @abstractmethod
    def get_xline_counts(self) -> Mapping[int, int]:
        """Get the number of crosslines for each inline.

        Returns:
            A mapping inline->number of crosslines
        """
        pass

    @abstractmethod
    def get_inline_counts(self) -> Mapping[int, int]:
        """Get the number of inlines for each crossline

        Returns:
            A mapping crossline->number of inlines"""
        pass

    @abstractmethod
    def get_bounding_box(self) -> Optional["Seismic3dRect"]:
        """Get the bounding box of the extent,
        described as a Seismic3dRect where the step size is meaningless."""
        pass


@dataclass
class SeismicTraceGroupExtent:
    """Describes a selection of traces in a prestack migrated seismic object.
    To be used with either a Seismic2dExtent or Seismic3dExtent to fully describe the object.

    Attributes:
        group_header (:py:class:`TraceHeaderField`): Which trace group header field to select traces by
        ranges (List[:py:class:`RangeInclusive`]): A list of ranges of trace group header values to include
    """

    group_header: TraceHeaderField
    ranges: List[RangeInclusive]

    @staticmethod
    def from_lineranges(trace_key: TraceHeaderField, ranges: Iterable[LineRange]) -> "SeismicTraceGroupExtent":
        return SeismicTraceGroupExtent(trace_key, [RangeInclusive.from_linerange(r) for r in ranges])

    @staticmethod
    def cdp_trace_ranges(ranges: Iterable[LineRange]) -> "SeismicTraceGroupExtent":
        """Create an extent filtering by a union of cdp_trace ranges"""
        return SeismicTraceGroupExtent.from_lineranges(TraceHeaderField.CDP_TRACE, ranges)

    @staticmethod
    def cdp_trace_range(range: LineRange) -> "SeismicTraceGroupExtent":
        """Create an extent filtering by a single cdp_trace range"""
        return SeismicTraceGroupExtent.cdp_trace_ranges([range])

    @staticmethod
    def offset_ranges(ranges: Iterable[LineRange]) -> "SeismicTraceGroupExtent":
        """Create an extent filtering by a union of offset ranges"""
        return SeismicTraceGroupExtent.from_lineranges(TraceHeaderField.OFFSET, ranges)

    @staticmethod
    def offset_range(range: LineRange) -> "SeismicTraceGroupExtent":
        """Create an extent filtering by a single offset range"""
        return SeismicTraceGroupExtent.offset_ranges([range])

    @staticmethod
    def _from_proto(proto: "SeismicTraceGroupExtentProto") -> "SeismicTraceGroupExtent":
        group_header = TraceHeaderField._from_proto(proto.group_header)
        ranges = [RangeInclusive._from_proto(ld) for ld in proto.lines.lines]
        return SeismicTraceGroupExtent(group_header=group_header, ranges=ranges)

    def _to_trace_group_extent_proto(self) -> "SeismicTraceGroupExtentProto":
        lines = SeismicTraceGroupLinesProto(lines=[r._to_proto() for r in self.ranges])
        return SeismicTraceGroupExtentProto(group_header=self.group_header._to_proto(), lines=lines)

    def _merge_into_create_seismic_request(self, request: "CreateSeismicRequest"):
        request.trace_group_extent.MergeFrom(self._to_trace_group_extent_proto())

    def _merge_into_stream_traces_request(self, request: "StreamTracesRequest"):
        request.trace_group_filter.MergeFrom(self._to_trace_group_extent_proto())

    def _merge_into_segy_seismic_request(self, request: "SegYSeismicRequest"):
        request.trace_group_filter.MergeFrom(self._to_trace_group_extent_proto())


@dataclass
class Seismic3dRect(Seismic3dExtent):
    """Describes a selection of traces in a 3d seismic object as a stepped rectangle.

    To construct a :code:`Seismic3dRect`, pass either a :py:class:`RangeInclusive` for the
    :code:`inline` and :code:`xline` arguments, or a tuple describing the start, and, and
    optionally step.

    A pair :code:`(il, xl)` is considered to be part of this extent if
    :code:`il` is part of the range :code:`inline` and :code:`xl` is part of the range
    :code:`xline`.

    Attributes:
        inline (:py:class:`RangeInclusive`): The range of inline values to include
        xline (:py:class:`RangeInclusive`): The range of xline values to include
    """

    inline: RangeInclusive
    xline: RangeInclusive

    def __init__(self, inline: Union[RangeInclusive, LineRange], xline: Union[RangeInclusive, LineRange]):
        if not isinstance(inline, RangeInclusive):
            inline = RangeInclusive.from_linerange(inline)
        if not isinstance(xline, RangeInclusive):
            xline = RangeInclusive.from_linerange(xline)
        self.inline = inline
        self.xline = xline

    @staticmethod
    def _from_rect_proto(proto: "Seismic3dRectProto") -> "Seismic3dRect":
        inline = RangeInclusive._from_proto(proto.inline_range)
        xline = RangeInclusive._from_proto(proto.xline_range)
        return Seismic3dRect(inline=inline, xline=xline)

    def _to_proto(self) -> "Seismic3dRectProto":
        return Seismic3dRectProto(inline_range=self.inline._to_proto(), xline_range=self.xline._to_proto())

    def _to_3d_extent_proto(self) -> "Seismic3dExtentProto":
        return Seismic3dRects([self])._to_3d_extent_proto()

    def get_xline(self, inline: int) -> List[int]:
        if inline in self.inline:
            return [x for x in self.xline]
        return []

    def get_inline(self, xline: int) -> List[int]:
        if xline in self.xline:
            return [x for x in self.inline]
        return []

    def get_xline_counts(self) -> Mapping[int, int]:
        mapping = {}
        for inline in self.inline:
            mapping[inline] = len(self.xline)
        return mapping

    def get_inline_counts(self) -> Mapping[int, int]:
        mapping = {}
        for xline in self.xline:
            mapping[xline] = len(self.inline)
        return mapping

    def get_xline_ranges(self) -> Mapping[int, Tuple[int, int]]:
        mapping = {}
        for x in self.inline:
            mapping[x] = (self.xline.start, self.xline.stop)
        return mapping

    def get_inline_ranges(self) -> Mapping[int, Tuple[int, int]]:
        mapping = {}
        for x in self.xline:
            mapping[x] = (self.inline.start, self.inline.stop)
        return mapping

    def get_bounding_box(self) -> "Seismic3dRect":
        return self


def _bounding_box_from_xline_range(xline_range: Mapping[int, Tuple[int, int]]) -> Optional["Seismic3dRect"]:
    """Computes the bounding box of all the inlines and xlines based on a
    mapping from inlines to xline intervals. Returns None if the mapping was empty."""
    inline_min, inline_max = None, None
    xline_min, xline_max = None, None
    for inline, xline in xline_range.items():
        x_start, x_stop = xline
        if inline_min is None:
            inline_min, inline_max = inline, inline
            xline_min, xline_max = x_start, x_stop
        else:
            inline_min = inline_min if inline_min < inline else inline
            inline_max = inline_max if inline_max > inline else inline
            xline_min = xline_min if xline_min < x_start else x_start
            xline_max = xline_max if xline_max > x_stop else x_stop
    if inline_min is None or inline_max is None or xline_min is None or xline_max is None:
        return None
    else:
        return Seismic3dRect((inline_min, inline_max), (xline_min, xline_max))


@dataclass
class Seismic3dRects(Seismic3dExtent):
    """Describes a selection of traces in a 3d seismic object as a union of stepped rectangles.

    A pair :code:`(il, xl)` is considered to be part of this extent if it is part of at least one
    of the rectangles in :code:`rects`.

    Attributes:
        rects (List[:py:class:`Seismic3dRect`]): The list of rectangles in the union
    """

    rects: List[Seismic3dRect]

    @staticmethod
    def _from_rects_proto(proto: "Seismic3dRectsProto") -> "Seismic3dRects":
        return Seismic3dRects(rects=[Seismic3dRect._from_rect_proto(r) for r in proto.rects])

    def _to_proto(self) -> "Seismic3dRectsProto":
        return Seismic3dRectsProto(rects=[r._to_proto() for r in self.rects])

    def _to_3d_extent_proto(self) -> "Seismic3dExtentProto":
        return Seismic3dExtentProto(rects=self._to_proto())

    def get_inline(self, xline: int) -> List[int]:
        rects = [rect.get_inline(xline) for rect in self.rects]
        output: Set[int] = set()
        for inlines in rects:
            output = output.union(inlines)
        return list(output)

    def get_xline(self, inline: int) -> List[int]:
        rects = [rect.get_xline(inline) for rect in self.rects]
        output: Set[int] = set()
        for xlines in rects:
            output = output.union(xlines)
        return list(output)

    # These counting methods could be more elegant, but this is the easiest way
    # to solve a fairly difficult problem for now.

    def get_inline_counts(self) -> Mapping[int, int]:
        bbox = self.get_bounding_box()
        mapping: Dict[int, int] = {}
        if bbox is None:
            return mapping
        for xline in bbox.xline:
            inlines: Set[int] = set()
            for rect in self.rects:
                inlines = inlines.union(rect.get_inline(xline))
            if len(inlines) > 0:
                mapping[xline] = len(inlines)
        return mapping

    def get_xline_counts(self) -> Mapping[int, int]:
        bbox = self.get_bounding_box()
        mapping: Dict[int, int] = {}
        if bbox is None:
            return mapping
        for inline in bbox.inline:
            xlines: Set[int] = set()
            for rect in self.rects:
                xlines = xlines.union(rect.get_xline(inline))
            if len(xlines) > 0:
                mapping[inline] = len(xlines)
        return mapping

    @staticmethod
    def _merge_ranges(rects) -> Mapping[int, Tuple[int, int]]:
        mapping: Dict[int, Tuple[int, int]] = {}
        for rect in rects:
            for line, range_ in rect.items():
                if line in mapping:
                    start, stop = mapping[line]
                    start = start if start < range_[0] else range_[0]
                    stop = stop if stop > range_[1] else range_[1]
                    mapping[line] = (start, stop)
                else:
                    mapping[line] = range_
        return mapping

    def get_inline_ranges(self) -> Mapping[int, Tuple[int, int]]:
        rects = [rect.get_inline_ranges() for rect in self.rects]
        return Seismic3dRects._merge_ranges(rects)

    def get_xline_ranges(self) -> Mapping[int, Tuple[int, int]]:
        rects = [rect.get_xline_ranges() for rect in self.rects]
        return Seismic3dRects._merge_ranges(rects)

    def get_bounding_box(self) -> Optional["Seismic3dRect"]:
        return _bounding_box_from_xline_range(self.get_xline_ranges())


@dataclass
class Seismic3dDef(Seismic3dExtent):
    """
    Describes a selection of traces in a 3d seismic object as a mapping. For
    each major line (inline or xline) to include, provide a list of minor line
    ranges (xline or inline, respectively) to include for that major line.

    If :code:`major_header == Inline` and :code:`minor_header == Crossline`, a pair
    :code:`(il, xl)` is considered to be part of this extent if
    :code:`lines[il]` is populated and :code:`xl` is part of at least one of
    the ranges in :code:`lines[il]`. The situation with the opposite major / minor
    header is similar.

    Attributes:
        major_header (:py:class:`TraceHeaderField`): Either Inline or Crossline
        minor_header (:py:class:`TraceHeaderField`): Either Crossline or Inline, and different from major_header
        lines (Dict[int, List[:py:class:`RangeInclusive`]]): The mapping from major lines to minor ranges
    """

    major_header: TraceHeaderField
    minor_header: TraceHeaderField
    lines: Dict[int, List[RangeInclusive]]

    @staticmethod
    def _from_3d_def_proto(proto: "Seismic3dDefProto") -> "Seismic3dDef":
        major_header = TraceHeaderField._from_proto(proto.major_header)
        minor_header = TraceHeaderField._from_proto(proto.minor_header)
        lines: Dict[int, List[RangeInclusive]] = {}
        for major, minor_lines in proto.lines.items():
            lines[major] = [RangeInclusive._from_proto(ld) for ld in minor_lines.ranges]

        return Seismic3dDef(major_header=major_header, minor_header=minor_header, lines=lines)

    def _to_proto(self) -> "Seismic3dDefProto":
        lines = {major: MinorLines(ranges=[r._to_proto() for r in ranges]) for major, ranges in self.lines.items()}
        return Seismic3dDefProto(
            major_header=self.major_header._to_proto(), minor_header=self.minor_header._to_proto(), lines=lines
        )

    def _to_3d_extent_proto(self) -> "Seismic3dExtentProto":
        ext = Seismic3dExtentProto()
        getattr(ext, "def").MergeFrom(self._to_proto())
        return ext

    @staticmethod
    def inline_major(lines: Mapping[int, List[LineRange]]) -> "Seismic3dDef":
        """Create a Seismic3dDef mapping inlines to xline ranges

        Args:
            lines (Mapping[int, List[LineRange]]):
                A mapping from inline numbers to xline ranges in the
                (start, stop) or (start, stop, step) format.

        Returns:
            A :py:class:`Seismic3dDef` extent.
        """
        return Seismic3dDef.from_lineranges(Direction.INLINE, lines)

    @staticmethod
    def xline_major(lines: Mapping[int, List[LineRange]]) -> "Seismic3dDef":
        """Create a Seismic3dDef mapping xlines to inline ranges

        Args:
            lines (Mapping[int, List[LineRange]]):
                A mapping from xline numbers to inline ranges in the
                (start, stop) or (start, stop, step) format.

        Returns:
            A :py:class:`Seismic3dDef` extent.
        """
        return Seismic3dDef.from_lineranges(Direction.XLINE, lines)

    @staticmethod
    def from_lineranges(major_dir: Direction, lines: Mapping[int, List[LineRange]]) -> "Seismic3dDef":
        if major_dir == Direction.INLINE:
            major_header = TraceHeaderField.INLINE
            minor_header = TraceHeaderField.CROSSLINE
        elif major_dir == Direction.XLINE:
            major_header = TraceHeaderField.CROSSLINE
            minor_header = TraceHeaderField.INLINE
        lines_r = {major: [RangeInclusive.from_linerange(r) for r in ranges] for major, ranges in lines.items()}
        return Seismic3dDef(major_header=major_header, minor_header=minor_header, lines=lines_r)

    @staticmethod
    def _merge_ranges(left: RangeInclusive, right: RangeInclusive) -> RangeInclusive:
        """Merge ranges by creating the smallest range (with step size 1) that contains both left and right."""
        return RangeInclusive(
            left.start if left.start < right.start else right.start, left.stop if left.stop > right.stop else right.stop
        )

    def get_minor(self, major: int) -> List[int]:
        """Get all minor line numbers for a major line"""
        minors: Set[int] = set()
        for range_ in self.lines.get(major, []):
            minors = minors.union(x for x in range_)
        return list(minors)

    def get_minors(self) -> Mapping[int, List[int]]:
        """Get all minor line numbers for each major line"""
        mapping = {}
        for major, ranges in self.lines.items():
            minors: Set[int] = set()
            for r in ranges:
                minors = minors.union(x for x in r)
            mapping[major] = list(minors)
        return mapping

    def get_major(self, minor: int) -> List[int]:
        """Get all major line numbers for a minor line"""
        majors = []
        for major, ranges in self.lines.items():
            for r in ranges:
                if minor in r:
                    majors.append(major)
                    continue
        return majors

    def get_majors(self) -> Mapping[int, List[int]]:
        """Get all major line numbers for each minor line"""
        mapping: Dict[int, Set[int]] = {}
        for major, ranges in self.lines.items():
            for r in ranges:
                for minor in r:
                    mapping.setdefault(minor, set()).add(major)
        return {minor: list(majors) for minor, majors in mapping.items()}

    def get_minor_range(self) -> Mapping[int, Tuple[int, int]]:
        """Get the minor line number range for each major line"""
        from functools import reduce

        mapping: Dict[int, Tuple[int, int]] = {}
        for line, ranges in self.lines.items():
            range_ = reduce(Seismic3dDef._merge_ranges, ranges)
            mapping[line] = (range_.start, range_.stop)
        return mapping

    def get_major_range(self) -> Mapping[int, Tuple[int, int]]:
        mapping: Dict[int, Tuple[int, int]] = {}
        for line, ranges in self.lines.items():
            for range_ in ranges:
                for minor in range_:
                    if minor in mapping:
                        start, stop = mapping[minor]
                        start = start if start < line else line
                        stop = stop if stop > line else line
                        mapping[minor] = (start, stop)
                    else:
                        mapping[minor] = (line, line)
        return mapping

    def get_major_count(self) -> Mapping[int, int]:
        # This is the transpose of the 3dDef and is hard to calculate memory-efficiently.
        return {xline: len(inlines) for xline, inlines in self.get_majors().items()}

    def get_minor_count(self) -> Mapping[int, int]:
        return {major: len(self.get_minor(major)) for major in self.lines}

    def get_inlines(self) -> Mapping[int, List[int]]:
        if self.major_header == TraceHeaderField.INLINE:
            return self.get_majors()
        elif self.major_header == TraceHeaderField.CROSSLINE:
            return self.get_minors()
        else:
            raise Seismic3dDefHeaderError(self.major_header)

    def get_xlines(self) -> Mapping[int, List[int]]:
        if self.major_header == TraceHeaderField.INLINE:
            return self.get_minors()
        elif self.major_header == TraceHeaderField.CROSSLINE:
            return self.get_majors()
        else:
            raise Seismic3dDefHeaderError(self.major_header)

    def get_inline(self, xline: int) -> List[int]:
        if self.major_header == TraceHeaderField.INLINE:
            return self.get_major(xline)
        elif self.major_header == TraceHeaderField.CROSSLINE:
            return self.get_minor(xline)
        else:
            raise Seismic3dDefHeaderError(self.major_header)

    def get_xline(self, inline: int) -> List[int]:
        if self.major_header == TraceHeaderField.INLINE:
            return self.get_minor(inline)
        elif self.major_header == TraceHeaderField.CROSSLINE:
            return self.get_major(inline)
        else:
            raise Seismic3dDefHeaderError(self.major_header)

    def get_inline_ranges(self) -> Mapping[int, Tuple[int, int]]:
        if self.major_header == TraceHeaderField.INLINE:
            return self.get_major_range()
        elif self.major_header == TraceHeaderField.CROSSLINE:
            return self.get_minor_range()
        else:
            raise Seismic3dDefHeaderError(self.major_header)

    def get_xline_ranges(self) -> Mapping[int, Tuple[int, int]]:
        if self.major_header == TraceHeaderField.INLINE:
            return self.get_minor_range()
        elif self.major_header == TraceHeaderField.CROSSLINE:
            return self.get_major_range()
        else:
            raise Seismic3dDefHeaderError(self.major_header)

    def get_inline_counts(self) -> Mapping[int, int]:
        if self.major_header == TraceHeaderField.INLINE:
            return self.get_minor_count()
        elif self.major_header == TraceHeaderField.CROSSLINE:
            return self.get_major_count()
        else:
            raise Seismic3dDefHeaderError(self.major_header)

    def get_xline_counts(self) -> Mapping[int, int]:
        if self.major_header == TraceHeaderField.INLINE:
            return self.get_major_count()
        elif self.major_header == TraceHeaderField.CROSSLINE:
            return self.get_minor_count()
        else:
            raise Seismic3dDefHeaderError(self.major_header)

    def get_bounding_box(self) -> Optional["Seismic3dRect"]:
        return _bounding_box_from_xline_range(self.get_xline_ranges())
