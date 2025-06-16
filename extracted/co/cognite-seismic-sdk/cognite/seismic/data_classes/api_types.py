import dataclasses
import datetime
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Mapping, Optional

from cognite.seismic._api.traces import TracesAPI
from cognite.seismic._api.utility import _timestamp_to_datetime
from cognite.seismic.data_classes.extents import SeismicCutout, SeismicExtent, TraceHeaderField
from cognite.seismic.data_classes.geometry import Geometry
from cognite.seismic.data_classes.trace_data import ArrayData, Trace, TraceBounds

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.types_pb2 import DeduceFromTraces as DeduceFromTracesProto
    from cognite.seismic.protos.types_pb2 import DoubleTraceCoordinates as DoubleTraceCoordinatesProto
    from cognite.seismic.protos.types_pb2 import Handedness as HandednessProto
    from cognite.seismic.protos.types_pb2 import IngestionSource as IngestionSourceProto
    from cognite.seismic.protos.types_pb2 import JobStatus as JobStatusProto
    from cognite.seismic.protos.types_pb2 import P6Transformation as P6TransformationProto
    from cognite.seismic.protos.types_pb2 import SurveyGridTransformation as SurveyGridTransformationProto
    from cognite.seismic.protos.types_pb2 import TraceCorners
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import BinaryHeader as BinaryHeaderProto
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import SegyOverrides as SegyOverridesProto
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import SeismicDataType as SeismicDataTypeProto
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import SeismicStore as SeismicStoreProto
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import TextHeader as TextHeaderProto
    from google.protobuf.wrappers_pb2 import FloatValue as f32
    from google.protobuf.wrappers_pb2 import Int32Value as i32


class IngestionSource(Enum):
    """Enum of ingestion sources."""

    INVALID_SOURCE = 0
    """Indicates that a source was not specified or was invalid."""
    FILE_SOURCE = 1
    """Indicates ingestion from a file"""
    TRACE_WRITER = 2
    """Indicates creation by trace writer"""

    @staticmethod
    def _from_proto(proto):
        if proto is None or proto < 0 or proto > 2:
            raise ValueError(f"Unrecognized IngestionSource: {proto}")
        return IngestionSource(proto)

    def _to_proto(self):
        IngestionSourceProto.values()[self.value]

    # The default repr gives the enum value, which is a bit more detail than needed for end users.
    # The str value is a bit nicer.
    def __repr__(self):
        return str(self)


class SeismicDataType(Enum):
    """Used to describe what data type a file or seismic/store uses."""

    UNSPECIFIED_DATA_TYPE = 0

    POSTSTACK = 1

    PRESTACK_DEPTH_MIGRATED = 2

    @staticmethod
    def _from_proto(proto) -> "SeismicDataType":
        if proto is None or proto < 0 or proto > 2:
            raise ValueError(f"Unrecognized SeismicDataType: {proto}")
        return SeismicDataType(proto)

    def _to_proto(self):
        return SeismicDataTypeProto.values()[self.value]

    # The default repr gives the enum value, which is a bit more detail than needed for end users.
    # The str value is a bit nicer.
    def __repr__(self):
        return str(self)


@dataclass
class SegyOverrides:
    """A set of SegY header overrides for a given ingested file.

    Attributes:
        energy_source_point_offset (Optional[int])
        cdp_number_offset (Optional[int])
        inline_offset (Optional[int])
        crossline_offset (Optional[int])
        cdp_x_offset (Optional[int])
        cdp_y_offset (Optional[int])
        shotpoint_offset (Optional[int])
        cdp_trace_offset (Optional[int])
        offset_header_offset (Optional[int])
        source_group_scalar_override (Optional[float])
    """

    energy_source_point_offset: Optional[int]
    cdp_number_offset: Optional[int]
    inline_offset: Optional[int]
    crossline_offset: Optional[int]
    cdp_x_offset: Optional[int]
    cdp_y_offset: Optional[int]
    shotpoint_offset: Optional[int]
    cdp_trace_offset: Optional[int]
    offset_header_offset: Optional[int]
    source_group_scalar_override: Optional[float]

    @staticmethod
    def _from_proto(proto) -> "SegyOverrides":
        """Convert a SegyOverrides proto into a python object"""

        def get_or_none(name):
            return getattr(proto, name).value if proto.HasField(name) else None

        return SegyOverrides(
            energy_source_point_offset=get_or_none("energy_source_point_offset"),
            cdp_number_offset=get_or_none("cdp_number_offset"),
            inline_offset=get_or_none("inline_offset"),
            crossline_offset=get_or_none("crossline_offset"),
            cdp_x_offset=get_or_none("cdp_x_offset"),
            cdp_y_offset=get_or_none("cdp_y_offset"),
            shotpoint_offset=get_or_none("shotpoint_offset"),
            cdp_trace_offset=get_or_none("cdp_trace_offset"),
            offset_header_offset=get_or_none("offset_header_offset"),
            source_group_scalar_override=get_or_none("source_group_scalar_override"),
        )

    def _to_proto(self):
        def mkval(value, protof=i32):
            return protof(value=value) if value is not None else None

        return SegyOverridesProto(
            energy_source_point_offset=mkval(self.energy_source_point_offset),
            cdp_number_offset=mkval(self.cdp_number_offset),
            inline_offset=mkval(self.inline_offset),
            crossline_offset=mkval(self.crossline_offset),
            cdp_x_offset=mkval(self.cdp_x_offset),
            cdp_y_offset=mkval(self.cdp_y_offset),
            shotpoint_offset=mkval(self.shotpoint_offset),
            cdp_trace_offset=mkval(self.cdp_trace_offset),
            offset_header_offset=mkval(self.offset_header_offset),
            source_group_scalar_override=mkval(self.source_group_scalar_override, f32),
        )


@dataclass
class SourceSegyFile:
    """Represents a raw SEGY file as used in the seismicstore-aware API, particularly for ingestion.

    Attributes:
        id (int): A 64-bit integer that represents the source file internally within the seismic service.
        uuid (str): The unique string-based uuid of a source segy file.
        external_id (str): A string-based user id that uniquely identifies the file.
        name (str): Non-unique string that describes the file.
        survey_id (int): The id of the survey this file is registered against
        cloud_storage_path (str): The cloud storage path where the file is located.
        metadata (Mapping[str, str]): User-provided metadata in the form of a string to string mapping
        segy_overrides (:py:class:`~cognite.seismic.SegyOverrides`): A set of SegY overrides
        key_fields (List[:py:class:`~cognite.seismic.TraceHeaderField`]):
            The trace header fields that are used as keys for indexing
        seismic_data_type (:py:class:`~cognite.seismic.SeismicDataType`): Whether this file is pre-stack or post-stack.
        dimensions (int): File dimensionality, either 2 or 3 dimensions.
        crs (str): The coordinate reference system used for this file.

    """

    id: int
    external_id: str
    name: str
    survey_id: int
    cloud_storage_path: str
    metadata: Mapping[str, str]
    segy_overrides: SegyOverrides
    key_fields: List[TraceHeaderField]
    dimensions: int
    seismic_data_type: SeismicDataType
    crs: str
    last_modified: datetime.datetime

    uuid: str = field(repr=False)

    @staticmethod
    def _from_proto(proto) -> "SourceSegyFile":
        uuid = proto.uuid
        id = proto.id
        external_id = proto.external_id.external_id
        name = proto.name
        survey_id = proto.survey_id
        metadata = proto.metadata
        segy_overrides = SegyOverrides._from_proto(proto.segy_overrides)
        cloud_storage_path = proto.cloud_storage_path
        key_fields = [TraceHeaderField._from_proto(f) for f in proto.key_fields]
        dimensions = proto.dimensions
        seismic_data_type = SeismicDataType._from_proto(proto.seismic_data_type)
        crs = proto.crs
        last_modified = _timestamp_to_datetime(proto.last_modified)

        return SourceSegyFile(
            uuid=uuid,
            id=id,
            external_id=external_id,
            name=name,
            survey_id=survey_id,
            metadata=metadata,
            segy_overrides=segy_overrides,
            cloud_storage_path=cloud_storage_path,
            key_fields=key_fields,
            dimensions=dimensions,
            seismic_data_type=seismic_data_type,
            crs=crs,
            last_modified=last_modified,
        )


@dataclass
class TextHeader:
    """A representation of text headers used to create or edit existing headers.

    Attributes:
        header (Optional[str]): The text content of the header
        raw_header (Optional[str]): The raw bytes of a header as a string
    """

    header: Optional[str] = None
    raw_header: Optional[str] = field(repr=False, default=None)

    @staticmethod
    def _from_proto(proto: "TextHeaderProto") -> "TextHeader":
        return TextHeader(header=proto.header, raw_header=proto.raw_header)

    def _to_proto(self) -> "TextHeaderProto":
        return TextHeaderProto(header=self.header or "", raw_header=self.raw_header or "")


@dataclass
class BinaryHeader:
    """A representation of binary headers used to create or edit existing headers.

    BinaryHeader.FIELDS contains the list of valid fields. to set after the object is constructed.

    Attributes:
        traces
        trace_data_type
        fixed_length_traces
        segy_revision
        auxtraces
        interval
        interval_original
        samples
        samples_original
        ensemble_fold
        vertical_sum
        trace_type_sorting_code
        sweep_type_code
        sweep_frequency_start
        sweep_frequency_end
        sweep_length
        sweep_channel
        sweep_taper_start
        sweep_taper_end
        sweep_taper_type
        correlated_traces
        amplitude_recovery
        original_measurement_system
        impulse_signal_polarity
        vibratory_polarity_code
    """

    traces: int
    trace_data_type: int
    fixed_length_traces: int
    segy_revision: int
    auxtraces: int
    interval: int
    interval_original: int
    samples: int
    samples_original: int
    ensemble_fold: int
    vertical_sum: int
    trace_type_sorting_code: int
    sweep_type_code: int
    sweep_frequency_start: int
    sweep_frequency_end: int
    sweep_length: int
    sweep_channel: int
    sweep_taper_start: int
    sweep_taper_end: int
    sweep_taper_type: int
    correlated_traces: int
    amplitude_recovery: int
    original_measurement_system: int
    impulse_signal_polarity: int
    vibratory_polarity_code: int
    raw_header: Optional[bytes] = field(repr=False, default=None)

    @staticmethod
    def _from_proto(proto) -> "BinaryHeader":
        kw = {fld.name: getattr(proto, fld.name) for fld in dataclasses.fields(BinaryHeader)}
        if not kw["raw_header"]:
            kw["raw_header"] = None
        return BinaryHeader(**kw)

    def _to_proto(self):
        kw = {fld.name: getattr(self, fld.name) for fld in dataclasses.fields(BinaryHeader)}
        if kw["raw_header"] is None:
            kw["raw_header"] = b""
        return BinaryHeaderProto(**kw)


@dataclass
class SeismicStore:
    """Represents a seismic store.

    Attributes:
        id (int): The unique internal id of the seismic store.
        name (str): The unique name of the seismic store.
        survey_id (int): The survey this seismic store belongs to.
        survey_uuid (str): The survey this seismic store belongs to, in the old uuid format.
        ingestion_source (:py:class:`IngestionSource`): The source of the seismicstore.
        metadata (Mapping[str, str]): Any custom-defined metadata
        ingested_file (Optional[:py:class:`SourceSegyFile`]): If present, the file this SeismicStore was ingested from
        coverage (Optional[:py:class:`Geometry`]): If present, the coverage geometry for this seismic store
        text_header (Optional[:py:class:`TextHeader`]): If present, the text header for this seismic store
        binary_header (Optional[:py:class:`BinaryHeader`]): If present, the binary header for this seismic store
        storage_tier_name (List[str]): The names of the storage tiers this seismic store exists in
        extent (Optional[:py:class:`SeismicExtent`]):
            If present, a description of the traces contained in this seismic store.
        trace_header_fields (List[:py:class:`~cognite.seismic.TraceHeaderField`]):
            The trace header fields that are available for accessing indexed trace data.
        seismic_data_type (:py:class:`~cognite.seismic.SeismicDataType`):
            Whether this seismic store describes pre-stack or post-stack data.
        dimensions (int): The underlying segy file's dimensionality, either 2 or 3 dimensions.
        crs (str): The Coordinate Reference System of the seismic store
    """

    id: int = field(repr=True)
    name: str = field(repr=True)
    survey_id: int = field(repr=True)
    ingestion_source: IngestionSource = field(repr=True)
    metadata: Mapping[str, str] = field(repr=True)
    storage_tier_name: List[str] = field(repr=True)
    trace_header_fields: List[TraceHeaderField] = field(repr=True)
    dimensions: int = field(repr=True)
    seismic_data_type: SeismicDataType = field(repr=True)
    last_modified: datetime.datetime = field(repr=True)
    # Fields below excluded from repr
    survey_uuid: str = field(repr=False)
    ingested_file: Optional[SourceSegyFile] = field(repr=False)
    coverage: Optional[Geometry] = field(repr=False)
    text_header: Optional[TextHeader] = field(repr=False)
    binary_header: Optional[BinaryHeader] = field(repr=False)
    extent: Optional[SeismicExtent] = field(repr=False)
    crs: str

    _traces: TracesAPI = field(repr=False)

    @staticmethod
    def _from_proto(proto: "SeismicStoreProto", traces: TracesAPI) -> "SeismicStore":
        metadata = {}
        for key in proto.metadata:
            metadata[key] = proto.metadata[key]

        trace_header_fields = [TraceHeaderField._from_proto(f) for f in proto.trace_header_fields]
        seismic_data_type = SeismicDataType._from_proto(proto.seismic_data_type)

        # Only decode protobuf fields that are defined.
        coverage = None
        text_header = None
        binary_header = None
        extent = None
        if proto.HasField("coverage"):
            coverage = Geometry._from_proto(proto.coverage)
        if proto.HasField("text_header"):
            text_header = TextHeader._from_proto(proto.text_header)
        if proto.HasField("binary_header"):
            binary_header = BinaryHeader._from_proto(proto.binary_header)
        if proto.HasField("extent"):
            extent = SeismicExtent._from_extent_proto(proto.extent)

        last_modified = _timestamp_to_datetime(proto.last_modified)

        seismic_store = SeismicStore(
            id=proto.id,
            name=proto.name,
            survey_id=proto.survey_id_int,
            survey_uuid=proto.survey_id,
            ingestion_source=IngestionSource._from_proto(proto.ingestion_source),
            metadata=metadata,
            ingested_file=SourceSegyFile._from_proto(proto.ingested_source_file),
            coverage=coverage,
            text_header=text_header,
            binary_header=binary_header,
            storage_tier_name=list(proto.storage_tier_name),
            extent=extent,
            trace_header_fields=trace_header_fields,
            dimensions=proto.dimensions,
            seismic_data_type=seismic_data_type,
            crs=proto.crs,
            last_modified=last_modified,
            _traces=traces,
        )

        return seismic_store

    def get_segy(self, **kwargs) -> Iterator[bytes]:
        """Retrieve traces in binary format from the seismic store

        The first and second elements in the response stream will always be the text header
        and binary header of the file.

        Traces can be filtered by a geometry, by line ranges, or by a SeismicExtent object for
        more advanced line-based filtering. The line ranges are specified as tuples of either
        (start, end) or (start, end, step). If a filter is not specified, the maximum ranges
        will be assumed.

        Note that while both inline_range and xline_range may be specified at the same time,
        only one of cdp_range, shotpoint_range or energy_source_point_range may be specified.

        Args:
            inline_range (line range, optional):
                Range of inline values to include. Only valid for 3d objects.
            xline_range (line range, optional):
                Range of xline values to include. Only valid for 3d objects.
            cdp_range (line range, optional):
                Range of cdp numbers to include. Only valid for a 2d object.
            shotpoint_range (line range, optional):
                Range of shotpoint numbers to include. Only valid for a 2d object.
            energy_source_point_range (line range, optional):
                Range of energy_source_point numbers to include. Only valid for a 2d object.
            extent (:py:class:`SeismicExtent`, optional):
                A SeismicExtent object indicating which traces to include
            geometry (:py:class:`~cognite.seismic.Geometry`, optional):
                Return traces inside this geometry (if area-like) or interpolate traces onto a line
                (if line-like; only valid for 3d objects).

        Returns:
            Iterator[bytes]: A stream of buffers that, when concatenated, constitute a SEG-Y stream.
        """

        return self._traces.get_segy(seismic_store_id=self.id, **kwargs)

    def stream_traces(self, **kwargs) -> Iterator[Trace]:
        """Retrieve traces from this seismic store

        Traces can be filtered by a geometry, by line ranges, or by a SeismicExtent object for
        more advanced line-based filtering. The line ranges are specified as tuples of either
        (start, end) or (start, end, step). If a filter is not specified, the maximum ranges
        will be assumed.

        Note that while both inline_range and xline_range may be specified at the same time,
        only one of cdp_range, shotpoint_range or energy_source_point_range may be specified.

        Args:
            extent (:py:class:`~cognite.seismic.SeismicExtent`, optional):
                A SeismicExtent object indicating which traces to include
            geometry (:py:class:`~cognite.seismic.Geometry`, optional):
                Return traces inside this geometry (if area-like) or interpolate traces onto a line
                (if line-like; only valid for 3d objects).
            interpolation_method (:py:class:`~cognite.seismic.InterpolationMethod`, optional):
                Interpolation method to use when interpolating traces. Only valid if `geometry`
                is a line-like geometry.
            z_range (line range, optional): The range of depth indices to include.
                Specified as a tuple of (int, int) or (int, int, int),
                representing start index, end index, and step size respectively.
            include_trace_header (bool, optional): Whether to include trace header info in the response.

        Returns:
            Iterator[:py:class:`~cognite.seismic.data_classes.api_types.Trace`], the traces for the specified volume
        """

        return self._traces.stream_traces(seismic_store_id=self.id, **kwargs)

    def get_trace_bounds(self, **kwargs) -> TraceBounds:
        """Compute the amount of data that will be returned for a given stream_traces request for this seismic store.
        This may be used to allocate sufficient data in an array, and also describes the range of the key
        header fields used to identify traces, ie. the range of the inline and xline numbers for 3D data, or
        the CDP or shotpoint field values for 2D data.

        Parameters: See :py:meth:`~TracesAPI.stream_traces`

        Returns:
            A :py:class:`~TraceBounds` object describing the size and bounds of the returned traces
        """

        return self._traces.get_trace_bounds(seismic_store_id=self.id, **kwargs)

    def get_array(self, *, progress: Optional[bool] = None, **kwargs) -> ArrayData:
        """Store traces from this seismic store into a numpy array

        Parameters: See :py:meth:`~TracesAPI.stream_traces`.

        In addition, there's an optional boolean argument :code:`progress`, which
        turns a progress bar on or off and defaults to :code:`True`.

        Returns:
            An :py:class:`~ArrayData` object encapsulating the retrieved array (see below)
        """

        return self._traces.get_array(seismic_store_id=self.id, progress=progress, **kwargs)


@dataclass
class Seismic:
    """Represents a seismic, a cutout of a seismic store.

    Attributes:
        id (int): The unique internal id of the seismic
        external_id (str): The external id of the seismic
        crs (str): The Coordinate Reference System of the seismic
        metadata (Mapping[str, str]): Any custom-defined metadata
        text_header (Optional[:py:class:`TextHeader`]): The text header that corresponds to the seismic
        binary_header (Optional[:py:class:`BinaryHeader`]): The binary header that corresponds to the seismic
        partition_id (int): The id of the partition the seismic belongs to
        seismicstore_id (int): The id of the seismicstore the seismic is derived from
        coverage (Optional[:py:class:`~cognite.seismic.Geometry`]):
            The coverage geometry for the seismic.
        extent (Optional[:py:class:`~cognite.seismic.SeismicExtent`]):
            A detailed description of the traces included in the seismic object
        trace_header_fields (List[:py:class:`~cognite.seismic.TraceHeaderField`]):
            The trace header fields that are available for accessing indexed trace data.
        seismic_data_type (:py:class:`~cognite.seismic.SeismicDataType`):
            Whether this seismic describes pre-stack or post-stack data.
        dimensions (int): The underlying segy file's dimensionality, either 2 or 3 dimensions.
    """

    id: int = field(repr=True)
    external_id: str = field(repr=True)
    crs: str = field(repr=True)
    metadata: Mapping[str, str] = field(repr=True)
    trace_header_fields: List[TraceHeaderField] = field(repr=True)
    dimensions: int = field(repr=True)
    seismic_data_type: SeismicDataType = field(repr=True)
    last_modified: datetime.datetime = field(repr=True)

    # Fields below excluded from repr
    name: str = field(repr=False)
    text_header: Optional[TextHeader] = field(repr=False)
    binary_header: Optional[BinaryHeader] = field(repr=False)
    partition_id: int = field(repr=False)
    seismicstore_id: Optional[int] = field(repr=False)
    coverage: Optional[Geometry] = field(repr=False)
    trace_count: int = field(repr=False)
    extent: Optional[SeismicExtent] = field(repr=False)
    cutout: Optional[SeismicCutout] = field(repr=False)

    _traces: TracesAPI = field(repr=False)

    @staticmethod
    def _from_proto(proto, traces: TracesAPI) -> "Seismic":
        metadata = {}
        for key in proto.metadata:
            metadata[key] = proto.metadata[key]

        trace_header_fields = [TraceHeaderField._from_proto(f) for f in proto.trace_header_fields]
        seismic_data_type = SeismicDataType._from_proto(proto.seismic_data_type)

        # Only decode protobuf fields that are defined.
        text_header = None
        binary_header = None
        coverage = None
        extent = None
        cutout = None
        if proto.HasField("text_header"):
            text_header = TextHeader._from_proto(proto.text_header)
        if proto.HasField("binary_header"):
            binary_header = BinaryHeader._from_proto(proto.binary_header)
        if proto.HasField("extent"):
            extent = SeismicExtent._from_extent_proto(proto.extent)
        if proto.HasField("cutout"):
            cutout = SeismicCutout._from_cutout_proto(proto.cutout)
        if proto.HasField("coverage"):
            coverage = Geometry._from_proto(proto.coverage)

        last_modified = _timestamp_to_datetime(proto.last_modified)

        seismic = Seismic(
            id=proto.id,
            external_id=proto.external_id,
            name=proto.name,
            crs=proto.crs,
            metadata=metadata,
            text_header=text_header,
            binary_header=binary_header,
            extent=extent,
            cutout=cutout,
            partition_id=proto.partition_id,
            seismicstore_id=proto.seismicstore_id,
            coverage=coverage,
            trace_count=proto.trace_count,
            trace_header_fields=trace_header_fields,
            dimensions=proto.dimensions,
            seismic_data_type=seismic_data_type,
            last_modified=last_modified,
            _traces=traces,
        )

        return seismic

    def get_segy(self, **kwargs) -> Iterator[bytes]:
        """Retrieve traces in binary format from this seismic

        The first and second elements in the response stream will always be the text header
        and binary header of the file.

        Traces can be filtered by a geometry, by line ranges, or by a SeismicExtent object for
        more advanced line-based filtering. The line ranges are specified as tuples of either
        (start, end) or (start, end, step). If a filter is not specified, the maximum ranges
        will be assumed.

        Note that while both inline_range and xline_range may be specified at the same time,
        only one of cdp_range, shotpoint_range or energy_source_point_range may be specified.

        Args:
            extent (:py:class:`~cognite.seismic.SeismicExtent`, optional):
                A SeismicExtent object indicating which traces to include
            geometry (:py:class:`~cognite.seismic.Geometry`, optional):
                Return traces inside this geometry (if area-like) or interpolate traces onto a line
                (if line-like; only valid for 3d objects).

        Returns:
            Iterator[bytes]: A stream of buffers that, when concatenated, constitute a SEG-Y stream.
        """

        return self._traces.get_segy(seismic_id=self.id, **kwargs)

    def stream_traces(self, **kwargs) -> Iterator[Trace]:
        """Retrieve traces from this seismic

        Traces can be filtered by a geometry, by line ranges, or by a SeismicExtent object for
        more advanced line-based filtering. The line ranges are specified as tuples of either
        (start, end) or (start, end, step). If a filter is not specified, the maximum ranges
        will be assumed.

        Note that while both inline_range and xline_range may be specified at the same time,
        only one of cdp_range, shotpoint_range or energy_source_point_range may be specified.

        Args:
            extent (:py:class:`~cognite.seismic.SeismicExtent`, optional):
                A SeismicExtent object indicating which traces to include
            geometry (:py:class:`~cognite.seismic.Geometry`, optional):
                Return traces inside this geometry (if area-like) or interpolate traces onto a line
                (if line-like; only valid for 3d objects).
            interpolation_method (:py:class:`~cognite.seismic.InterpolationMethod`, optional):
                Interpolation method to use when interpolating traces. Only valid if `geometry`
                is a line-like geometry.
            z_range (line range, optional): The range of depth indices to include.
                Specified as a tuple of (int, int) or (int, int, int),
                representing start index, end index, and step size respectively.
            include_trace_header (bool, optional): Whether to include trace header info in the response.

        Returns:
            Iterator[:py:class:`~cognite.seismic.data_classes.api_types.Trace`], the traces for the specified volume
        """

        return self._traces.stream_traces(seismic_id=self.id, **kwargs)

    def get_trace_bounds(self, **kwargs) -> TraceBounds:
        """Compute the amount of data that will be returned for a given stream_traces request for this seismic.
        This may be used to allocate sufficient data in an array, and also describes the range of the key
        header fields used to identify traces, ie. the range of the inline and xline numbers for 3D data, or
        the CDP or shotpoint field values for 2D data.

        Parameters: See :py:meth:`~TracesAPI.stream_traces`

        Returns:
            A :py:class:`~TraceBounds` object describing the size and bounds of the returned traces
        """

        return self._traces.get_trace_bounds(seismic_id=self.id, **kwargs)

    def get_array(self, *, progress: Optional[bool] = None, **kwargs) -> ArrayData:
        """Store traces from this seismic into a numpy array

        Parameters: See :py:meth:`~TracesAPI.stream_traces`.

        In addition, there's an optional boolean argument :code:`progress`, which
        turns a progress bar on or off and defaults to :code:`True`.

        Returns:
            An :py:class:`~ArrayData` object encapsulating the retrieved array (see below)
        """

        return self._traces.get_array(seismic_id=self.id, progress=progress, **kwargs)


@dataclass
class Partition:
    """Represents a partition and its included seismics

    Attributes:
        id (int): The unique internal id for this partition
        external_id (str): The unique external id for this partition
        name (str): The human-friendly name for this partition
        seismic_ids (List[int]): A list of ids of seismics that belong to this partition
    """

    id: int = field(repr=True)
    external_id: str = field(repr=True)
    name: str = field(repr=True)
    last_modified: datetime.datetime = field(repr=True)
    seismic_ids: List[int] = field(repr=False)

    @staticmethod
    def _from_proto(proto) -> "Partition":
        seismic_ids = [i for i in proto.seismic_ids]
        last_modified = _timestamp_to_datetime(proto.last_modified)
        return Partition(
            id=proto.id,
            external_id=proto.external_id,
            name=proto.name,
            seismic_ids=seismic_ids,
            last_modified=last_modified,
        )


@dataclass
class DoubleTraceCoordinates:
    """The coordinates of a point, given in both projected coordinates (x, y) and in
    bin grid coordinates (inline, xline).

    Pass a list of three or more instances to specify the affine transformation between bin
    grid coordinates and projected coordinates by the corners of the grid.

    Attributes:
        x (float): Longitude or easting
        y (float): Latitude or northing
        inline (int): The inline coordinate of the bin grid
        xline (int): The xline coordinate of the bin grid
    """

    x: float
    y: float
    inline: int
    xline: int

    def _to_proto(self):
        return DoubleTraceCoordinatesProto(x=self.x, y=self.y, iline=self.inline, xline=self.xline)

    @staticmethod
    def _from_proto(proto) -> "DoubleTraceCoordinates":
        return DoubleTraceCoordinates(x=proto.x, y=proto.y, inline=proto.iline, xline=proto.xline)


class SurveyGridTransformation(ABC):
    """Description of an affine transformation between bin grid coordinates and projected coordinates.
    Pass a subclass of this in the :code:`grid_transformation` parameter to :code:`survey.create` or
    :code:`survey.edit` to describe the transformation on a per-survey basis.

    This is an abstract class - concrete instances will be one of :py:class:`P6Transformation` for an
    explicit mathematical description of the transformation, :py:class:`CoordList` to specify it as
    a list of correlated coordinates, or :py:class:`DeduceFromTraces` to request that the seismic
    service attempts to deduce the transformation from individual traces.
    """

    @abstractmethod
    def _to_proto(self) -> "SurveyGridTransformationProto":
        pass

    @staticmethod
    def _from_proto(proto: "SurveyGridTransformationProto") -> "SurveyGridTransformation":
        if proto.HasField("p6_transformation"):
            return P6Transformation._from_p6_transformation_proto(proto.p6_transformation)
        elif proto.HasField("trace_corners"):
            return CoordList._from_trace_corners_proto(proto.trace_corners)
        elif proto.HasField("deduce_from_traces"):
            return DeduceFromTraces._from_deduce_from_traces_proto(proto.deduce_from_traces)
        else:
            raise ValueError("Invalid SurveyGridTransformation protobuf")


class Handedness(Enum):
    """The handedness of a :py:class:`~cognite.seismic.P6Transformation`."""

    RIGHTHANDED = 0
    "Specifies that the inline axis is 90 degrees clockwise from the xline axis."
    LEFTHANDED = 1
    "Specifies that the inline axis is 90 degrees counter-clockwise from the xline axis."

    def _to_proto(self) -> "HandednessProto.ValueType":
        if self == Handedness.RIGHTHANDED:
            return HandednessProto.Value("RIGHTHANDED")
        elif self == Handedness.LEFTHANDED:
            return HandednessProto.Value("LEFTHANDED")
        else:
            raise ValueError("Unrecognized handedness")


@dataclass
class P6Transformation(SurveyGridTransformation):
    """Description of an affine transformation between bin grid coordinates and projected
    coordinates in the P6 format, loosely following IOGP guidance note 373-7-2 section 2.3.2.4.

    Attributes:
        origin (:py:class:`~cognite.seismic.DoubleTraceCoordinates`):
            The origin point of the transformation
        inline_bin_width (float): The width of bins in the inline direction
        xline_bin_width (float): The width of bins in the xline direction
        xline_azimuth (float): The direction of the xline axis, in degrees clockwise from north
        handedness (:py:class:`~cognite.seismic.Handedness`):
            The orientation of the inline vs. the xline axes. Default: RIGHTHANDED.
        inline_bin_inc (Optional[int]):
            The increment of the inline coordinate corresponding to a bin. Default: 1.
        xline_bin_inc (Optional[int]):
            The increment of the xline coordinate corresponding to a bin. Default: 1.
    """

    origin: DoubleTraceCoordinates
    inline_bin_width: float
    xline_bin_width: float
    xline_azimuth: float
    handedness: Handedness = Handedness.RIGHTHANDED
    inline_bin_inc: int = 1
    xline_bin_inc: int = 1

    def _to_proto(self) -> "SurveyGridTransformationProto":
        return SurveyGridTransformationProto(
            p6_transformation=P6TransformationProto(
                handedness=self.handedness._to_proto(),
                origin=self.origin._to_proto(),
                iline_bin_width=self.inline_bin_width,
                xline_bin_width=self.xline_bin_width,
                xline_azimuth=self.xline_azimuth,
                iline_bin_inc=self.inline_bin_inc,
                xline_bin_inc=self.xline_bin_inc,
            )
        )

    @staticmethod
    def _from_p6_transformation_proto(proto) -> "P6Transformation":
        return P6Transformation(
            origin=DoubleTraceCoordinates._from_proto(proto.origin),
            handedness=Handedness(proto.handedness),
            inline_bin_width=proto.iline_bin_width,
            xline_bin_width=proto.xline_bin_width,
            xline_azimuth=proto.xline_azimuth,
            inline_bin_inc=proto.iline_bin_inc,
            xline_bin_inc=proto.xline_bin_inc,
        )


@dataclass
class DeduceFromTraces(SurveyGridTransformation):
    """Pass an instance of this class as the grid_transformation argument to indicate that
    the seismics service should try to deduce the affine transformation between bin grid
    coordinates and projected coordinates from the trace coordinates themselves."""

    def _to_proto(self) -> "SurveyGridTransformationProto":
        return SurveyGridTransformationProto(deduce_from_traces=DeduceFromTracesProto())

    @staticmethod
    def _from_deduce_from_traces_proto(proto: "DeduceFromTracesProto") -> "DeduceFromTraces":
        return DeduceFromTraces()


@dataclass
class CoordList(SurveyGridTransformation):
    """Description of an affine transformation between bin grid coordinates and projected
    coordinates as a list of three or more points spanning the area of the bin grid.

    Attributes:
        coordinates (List[:py:class:`DoubleTraceCoordinates`]): The list of points spanning the grid.
    """

    coordinates: List[DoubleTraceCoordinates]

    def _to_proto(self) -> "SurveyGridTransformationProto":
        return SurveyGridTransformationProto(
            trace_corners=TraceCorners(corners=[c._to_proto() for c in self.coordinates])
        )

    @staticmethod
    def _from_trace_corners_proto(proto: "TraceCorners") -> "CoordList":
        return CoordList(coordinates=[DoubleTraceCoordinates._from_proto(p) for p in proto.corners])


class SurveyCoverageSource(Enum):
    """Used to request or return that a survey's coverage geometry comes from a
    specific source. Note: This must be kept in sync with the protobuf
    representation."""

    UNSPECIFIED = 0
    """Used as the default when a specific coverage source is not provided"""
    CUSTOM = 1
    """Used to specify that a custom coverage should be or was returned"""
    CALCULATED = 2
    """Used to specify that a calculated coverage should be or was returned"""

    @staticmethod
    def _from_proto(proto):
        if proto is None or proto < 0 or proto > 2:
            raise ValueError(f"Unrecognized SurveyCoverageSource: {proto}")
        return SurveyCoverageSource(proto)

    def _to_proto(self):
        SurveyCoverageSource.values()[self.value]

    # The default repr gives the enum value, which is a bit more detail than needed for end users.
    # The str value is a bit nicer.
    def __repr__(self):
        return str(self)


@dataclass
class Survey:
    """Represents a seismic survey, a grouping of related files

    Attributes:
        id (int): The unique internal id of the survey.
        external_id (str): A string-based user id that uniquely identifies the survey.
        uuid (str): The unique internal id of the survey, in the old uuid format
        name (str): A descriptive name of the survey.
        seismic_ids (List[int]): A list of seismic ids contained in the survey (if requested)
        seismic_store_ids (List[int]):
            A list of the seismic store ids contained in the survey
            (if requested; only available for data managers)
        metadata (Mapping[str, str]): Any custom-defined metadata
        coverage (:py:class:`Geometry`): If present, the coverage geometry for this survey
        survey_coverage_source (:py:class:`SurveyCoverageSource`):
            Whether the coverage is a custom-defined survey coverage, or computed from the containing
            seismic stores.
        crs (str): The coordinate reference system used by all members of this survey
        grid_transformation (:py:class:`SurveyGridTransformation`):
            Any custom-defined transformation from bin grid to projected coordinates, if requested
        custom_coverage (:py:class:`Geometry`): Any custom-defined coverage geometry, if requested
    """

    id: int = field(repr=True)
    external_id: Optional[str] = field(repr=True)
    name: str = field(repr=True)
    seismic_ids: Optional[List[int]] = field(repr=True)
    metadata: Optional[Mapping[str, str]] = field(repr=True)
    last_modified: datetime.datetime = field(repr=True)

    # Fields below are excluded from repr
    uuid: str = field(repr=False)
    seismic_store_ids: Optional[List[int]] = field(repr=False)
    coverage: Optional[Geometry] = field(repr=False)
    crs: Optional[str] = field(repr=False)
    grid_transformation: Optional[SurveyGridTransformation] = field(repr=False)
    custom_coverage: Optional[Geometry] = field(repr=False)
    survey_coverage_source: Optional[SurveyCoverageSource] = field(repr=False)

    # Note that this method converts from a SearchSurveyResult, not a Survey message.
    @staticmethod
    def _from_proto(proto) -> "Survey":
        survey = Survey._from_proto_survey(proto.survey)
        seismic_ids = proto.seismic_ids if hasattr(proto, "seismic_ids") else None
        seismic_store_ids = proto.seismic_store_ids if hasattr(proto, "seismic_store_ids") else None
        coverage = Geometry._from_proto(proto.coverage) if proto.HasField("coverage") else None
        crs = proto.survey.crs if proto.survey.crs else None
        grid_transformation = (
            SurveyGridTransformation._from_proto(proto.survey.grid_transformation)
            if proto.survey.HasField("grid_transformation")
            else None
        )
        if proto.survey.HasField("custom_coverage") and proto.survey.custom_coverage.HasField("custom_coverage"):
            custom_coverage = Geometry._from_proto(proto.survey.custom_coverage.custom_coverage)
        else:
            custom_coverage = None

        survey_coverage_source = (
            SurveyCoverageSource._from_proto(proto.coverage_source)
            if hasattr(proto, "coverage_source")
            else SurveyCoverageSource.UNSPECIFIED
        )

        survey.seismic_ids = seismic_ids
        survey.seismic_store_ids = seismic_store_ids
        survey.coverage = coverage
        survey.crs = crs
        survey.grid_transformation = grid_transformation
        survey.custom_coverage = custom_coverage
        survey.survey_coverage_source = survey_coverage_source

        return survey

    @staticmethod
    def _from_proto_survey(proto) -> "Survey":
        """From a Survey proto rather than the result of SearchSurvey"""
        survey_uuid = proto.id
        survey_id_int = proto.id_int
        # Proto default value for ints is 0. Changing it to -1 to be a little clearer
        if survey_id_int == 0:
            survey_id_int = -1
        external_id = proto.external_id.external_id if hasattr(proto, "external_id") else None
        name = proto.name if hasattr(proto, "name") else None
        metadata = proto.metadata if hasattr(proto, "metadata") else None
        last_modified = _timestamp_to_datetime(proto.last_modified)

        return Survey(
            id=survey_id_int,
            uuid=survey_uuid,
            external_id=external_id,
            name=name,
            seismic_ids=[],
            seismic_store_ids=[],
            metadata=metadata,
            coverage=None,
            crs=None,
            grid_transformation=None,
            custom_coverage=None,
            survey_coverage_source=None,
            last_modified=last_modified,
        )


class StatusCode(Enum):
    """Used to request or return the status of an ingestion job."""

    NONE = 0
    QUEUED = 1
    IN_PROGRESS = 2
    SUCCESS = 3
    FAILED = 4
    TIMEOUT = 5

    def _to_proto(self) -> "JobStatusProto.ValueType":
        if self == StatusCode.NONE:
            return JobStatusProto.Value("NONE")
        elif self == StatusCode.QUEUED:
            return JobStatusProto.Value("QUEUED")
        elif self == StatusCode.IN_PROGRESS:
            return JobStatusProto.Value("IN_PROGRESS")
        elif self == StatusCode.SUCCESS:
            return JobStatusProto.Value("SUCCESS")
        elif self == StatusCode.FAILED:
            return JobStatusProto.Value("FAILED")
        elif self == StatusCode.TIMEOUT:
            return JobStatusProto.Value("TIMEOUT")
        else:
            raise ValueError("Unrecognized StatusCode")


@dataclass
class IngestionJob:
    """The newly created ingestion job's unique id.

    Attributes:
        job_id (str): The unique id of the newly created job.
    """

    job_id: str

    @staticmethod
    def _from_proto(proto) -> "IngestionJob":
        return IngestionJob(job_id=proto.job_id)


@dataclass
class JobStatusLog:
    timestamp: datetime.datetime
    log_line: str

    @staticmethod
    def _from_proto(proto) -> "JobStatusLog":
        timestamp = datetime.datetime.fromtimestamp(proto.timestamp.seconds)
        log_line = proto.log_line
        return JobStatusLog(timestamp=timestamp, log_line=log_line)


@dataclass
class JobStatus:
    job_id: str
    file_uuid: str
    status: StatusCode
    target_storage_tier_name: Optional[str]
    started_at: datetime.datetime
    updated_at: datetime.datetime
    logs: List[JobStatusLog]

    @staticmethod
    def _from_proto(proto) -> "JobStatus":
        job_id = proto.job_id
        file_uuid = proto.file_uuid
        status_int = StatusCode(proto.status)
        target_storage_tier_name = (
            proto.target_storage_tier_name if hasattr(proto, "target_storage_tier_name") else None
        )
        target_storage_tier_name = (
            target_storage_tier_name.value if target_storage_tier_name.value is not None else None
        )
        started_at = datetime.datetime.fromtimestamp(proto.started_at.seconds)
        updated_at = datetime.datetime.fromtimestamp(proto.updated_at.seconds)
        logs = [JobStatusLog._from_proto(p) for p in proto.logs]

        return JobStatus(
            job_id=job_id,
            file_uuid=file_uuid,
            status=status_int,
            target_storage_tier_name=target_storage_tier_name,
            started_at=started_at,
            updated_at=updated_at,
            logs=logs,
        )
