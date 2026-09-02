from alphagenome.protos import tensor_pb2 as _tensor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Strand(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STRAND_UNSPECIFIED: _ClassVar[Strand]
    STRAND_POSITIVE: _ClassVar[Strand]
    STRAND_NEGATIVE: _ClassVar[Strand]
    STRAND_UNSTRANDED: _ClassVar[Strand]

class OntologyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ONTOLOGY_TYPE_UNSPECIFIED: _ClassVar[OntologyType]
    ONTOLOGY_TYPE_CLO: _ClassVar[OntologyType]
    ONTOLOGY_TYPE_UBERON: _ClassVar[OntologyType]
    ONTOLOGY_TYPE_CL: _ClassVar[OntologyType]
    ONTOLOGY_TYPE_EFO: _ClassVar[OntologyType]
    ONTOLOGY_TYPE_NTR: _ClassVar[OntologyType]

class BiosampleType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BIOSAMPLE_TYPE_UNSPECIFIED: _ClassVar[BiosampleType]
    BIOSAMPLE_TYPE_PRIMARY_CELL: _ClassVar[BiosampleType]
    BIOSAMPLE_TYPE_IN_VITRO_DIFFERENTIATED_CELLS: _ClassVar[BiosampleType]
    BIOSAMPLE_TYPE_CELL_LINE: _ClassVar[BiosampleType]
    BIOSAMPLE_TYPE_TISSUE: _ClassVar[BiosampleType]
    BIOSAMPLE_TYPE_TECHNICAL_SAMPLE: _ClassVar[BiosampleType]
    BIOSAMPLE_TYPE_ORGANOID: _ClassVar[BiosampleType]

class OutputType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OUTPUT_TYPE_UNSPECIFIED: _ClassVar[OutputType]
    OUTPUT_TYPE_ATAC: _ClassVar[OutputType]
    OUTPUT_TYPE_CAGE: _ClassVar[OutputType]
    OUTPUT_TYPE_DNASE: _ClassVar[OutputType]
    OUTPUT_TYPE_RNA_SEQ: _ClassVar[OutputType]
    OUTPUT_TYPE_CHIP_HISTONE: _ClassVar[OutputType]
    OUTPUT_TYPE_CHIP_TF: _ClassVar[OutputType]
    OUTPUT_TYPE_SPLICE_SITES: _ClassVar[OutputType]
    OUTPUT_TYPE_SPLICE_SITE_USAGE: _ClassVar[OutputType]
    OUTPUT_TYPE_SPLICE_JUNCTIONS: _ClassVar[OutputType]
    OUTPUT_TYPE_CONTACT_MAPS: _ClassVar[OutputType]
    OUTPUT_TYPE_PROCAP: _ClassVar[OutputType]

class Organism(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORGANISM_UNSPECIFIED: _ClassVar[Organism]
    ORGANISM_HOMO_SAPIENS: _ClassVar[Organism]
    ORGANISM_MUS_MUSCULUS: _ClassVar[Organism]

class IntervalAggregationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INTERVAL_AGGREGATION_TYPE_UNSPECIFIED: _ClassVar[IntervalAggregationType]
    INTERVAL_AGGREGATION_TYPE_MEAN: _ClassVar[IntervalAggregationType]
    INTERVAL_AGGREGATION_TYPE_SUM: _ClassVar[IntervalAggregationType]

class AggregationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AGGREGATION_TYPE_UNSPECIFIED: _ClassVar[AggregationType]
    AGGREGATION_TYPE_DIFF_MEAN: _ClassVar[AggregationType]
    AGGREGATION_TYPE_DIFF_SUM: _ClassVar[AggregationType]
    AGGREGATION_TYPE_DIFF_SUM_LOG2: _ClassVar[AggregationType]
    AGGREGATION_TYPE_L2_DIFF: _ClassVar[AggregationType]
    AGGREGATION_TYPE_L2_DIFF_LOG1P: _ClassVar[AggregationType]
    AGGREGATION_TYPE_DIFF_LOG2_SUM: _ClassVar[AggregationType]
    AGGREGATION_TYPE_ACTIVE_MEAN: _ClassVar[AggregationType]
    AGGREGATION_TYPE_ACTIVE_SUM: _ClassVar[AggregationType]

class Endedness(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENDEDNESS_UNSPECIFIED: _ClassVar[Endedness]
    ENDEDNESS_SINGLE: _ClassVar[Endedness]
    ENDEDNESS_PAIRED: _ClassVar[Endedness]
STRAND_UNSPECIFIED: Strand
STRAND_POSITIVE: Strand
STRAND_NEGATIVE: Strand
STRAND_UNSTRANDED: Strand
ONTOLOGY_TYPE_UNSPECIFIED: OntologyType
ONTOLOGY_TYPE_CLO: OntologyType
ONTOLOGY_TYPE_UBERON: OntologyType
ONTOLOGY_TYPE_CL: OntologyType
ONTOLOGY_TYPE_EFO: OntologyType
ONTOLOGY_TYPE_NTR: OntologyType
BIOSAMPLE_TYPE_UNSPECIFIED: BiosampleType
BIOSAMPLE_TYPE_PRIMARY_CELL: BiosampleType
BIOSAMPLE_TYPE_IN_VITRO_DIFFERENTIATED_CELLS: BiosampleType
BIOSAMPLE_TYPE_CELL_LINE: BiosampleType
BIOSAMPLE_TYPE_TISSUE: BiosampleType
BIOSAMPLE_TYPE_TECHNICAL_SAMPLE: BiosampleType
BIOSAMPLE_TYPE_ORGANOID: BiosampleType
OUTPUT_TYPE_UNSPECIFIED: OutputType
OUTPUT_TYPE_ATAC: OutputType
OUTPUT_TYPE_CAGE: OutputType
OUTPUT_TYPE_DNASE: OutputType
OUTPUT_TYPE_RNA_SEQ: OutputType
OUTPUT_TYPE_CHIP_HISTONE: OutputType
OUTPUT_TYPE_CHIP_TF: OutputType
OUTPUT_TYPE_SPLICE_SITES: OutputType
OUTPUT_TYPE_SPLICE_SITE_USAGE: OutputType
OUTPUT_TYPE_SPLICE_JUNCTIONS: OutputType
OUTPUT_TYPE_CONTACT_MAPS: OutputType
OUTPUT_TYPE_PROCAP: OutputType
ORGANISM_UNSPECIFIED: Organism
ORGANISM_HOMO_SAPIENS: Organism
ORGANISM_MUS_MUSCULUS: Organism
INTERVAL_AGGREGATION_TYPE_UNSPECIFIED: IntervalAggregationType
INTERVAL_AGGREGATION_TYPE_MEAN: IntervalAggregationType
INTERVAL_AGGREGATION_TYPE_SUM: IntervalAggregationType
AGGREGATION_TYPE_UNSPECIFIED: AggregationType
AGGREGATION_TYPE_DIFF_MEAN: AggregationType
AGGREGATION_TYPE_DIFF_SUM: AggregationType
AGGREGATION_TYPE_DIFF_SUM_LOG2: AggregationType
AGGREGATION_TYPE_L2_DIFF: AggregationType
AGGREGATION_TYPE_L2_DIFF_LOG1P: AggregationType
AGGREGATION_TYPE_DIFF_LOG2_SUM: AggregationType
AGGREGATION_TYPE_ACTIVE_MEAN: AggregationType
AGGREGATION_TYPE_ACTIVE_SUM: AggregationType
ENDEDNESS_UNSPECIFIED: Endedness
ENDEDNESS_SINGLE: Endedness
ENDEDNESS_PAIRED: Endedness

class Interval(_message.Message):
    __slots__ = ("chromosome", "start", "end", "strand")
    CHROMOSOME_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    STRAND_FIELD_NUMBER: _ClassVar[int]
    chromosome: str
    start: int
    end: int
    strand: Strand
    def __init__(self, chromosome: _Optional[str] = ..., start: _Optional[int] = ..., end: _Optional[int] = ..., strand: _Optional[_Union[Strand, str]] = ...) -> None: ...

class Variant(_message.Message):
    __slots__ = ("chromosome", "position", "reference_bases", "alternate_bases")
    CHROMOSOME_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_BASES_FIELD_NUMBER: _ClassVar[int]
    ALTERNATE_BASES_FIELD_NUMBER: _ClassVar[int]
    chromosome: str
    position: int
    reference_bases: str
    alternate_bases: str
    def __init__(self, chromosome: _Optional[str] = ..., position: _Optional[int] = ..., reference_bases: _Optional[str] = ..., alternate_bases: _Optional[str] = ...) -> None: ...

class OntologyTerm(_message.Message):
    __slots__ = ("ontology_type", "id")
    ONTOLOGY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ontology_type: OntologyType
    id: int
    def __init__(self, ontology_type: _Optional[_Union[OntologyType, str]] = ..., id: _Optional[int] = ...) -> None: ...

class Biosample(_message.Message):
    __slots__ = ("type", "name", "stage")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STAGE_FIELD_NUMBER: _ClassVar[int]
    type: BiosampleType
    name: str
    stage: str
    def __init__(self, type: _Optional[_Union[BiosampleType, str]] = ..., name: _Optional[str] = ..., stage: _Optional[str] = ...) -> None: ...

class GeneScorerMetadata(_message.Message):
    __slots__ = ("gene_id", "name", "strand", "type", "junction_start", "junction_end")
    GENE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STRAND_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    JUNCTION_START_FIELD_NUMBER: _ClassVar[int]
    JUNCTION_END_FIELD_NUMBER: _ClassVar[int]
    gene_id: str
    name: str
    strand: Strand
    type: str
    junction_start: int
    junction_end: int
    def __init__(self, gene_id: _Optional[str] = ..., name: _Optional[str] = ..., strand: _Optional[_Union[Strand, str]] = ..., type: _Optional[str] = ..., junction_start: _Optional[int] = ..., junction_end: _Optional[int] = ...) -> None: ...

class TrackMetadata(_message.Message):
    __slots__ = ("name", "strand", "ontology_term", "biosample", "assay", "histone_mark_code", "transcription_factor_code", "gtex_tissue", "data_source", "endedness", "genetically_modified", "nonzero_mean")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STRAND_FIELD_NUMBER: _ClassVar[int]
    ONTOLOGY_TERM_FIELD_NUMBER: _ClassVar[int]
    BIOSAMPLE_FIELD_NUMBER: _ClassVar[int]
    ASSAY_FIELD_NUMBER: _ClassVar[int]
    HISTONE_MARK_CODE_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPTION_FACTOR_CODE_FIELD_NUMBER: _ClassVar[int]
    GTEX_TISSUE_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ENDEDNESS_FIELD_NUMBER: _ClassVar[int]
    GENETICALLY_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    NONZERO_MEAN_FIELD_NUMBER: _ClassVar[int]
    name: str
    strand: Strand
    ontology_term: OntologyTerm
    biosample: Biosample
    assay: str
    histone_mark_code: str
    transcription_factor_code: str
    gtex_tissue: str
    data_source: str
    endedness: Endedness
    genetically_modified: bool
    nonzero_mean: float
    def __init__(self, name: _Optional[str] = ..., strand: _Optional[_Union[Strand, str]] = ..., ontology_term: _Optional[_Union[OntologyTerm, _Mapping]] = ..., biosample: _Optional[_Union[Biosample, _Mapping]] = ..., assay: _Optional[str] = ..., histone_mark_code: _Optional[str] = ..., transcription_factor_code: _Optional[str] = ..., gtex_tissue: _Optional[str] = ..., data_source: _Optional[str] = ..., endedness: _Optional[_Union[Endedness, str]] = ..., genetically_modified: bool = ..., nonzero_mean: _Optional[float] = ...) -> None: ...

class TracksMetadata(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.RepeatedCompositeFieldContainer[TrackMetadata]
    def __init__(self, metadata: _Optional[_Iterable[_Union[TrackMetadata, _Mapping]]] = ...) -> None: ...

class JunctionMetadata(_message.Message):
    __slots__ = ("name", "ontology_term", "biosample", "gtex_tissue", "data_source", "assay")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ONTOLOGY_TERM_FIELD_NUMBER: _ClassVar[int]
    BIOSAMPLE_FIELD_NUMBER: _ClassVar[int]
    GTEX_TISSUE_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ASSAY_FIELD_NUMBER: _ClassVar[int]
    name: str
    ontology_term: OntologyTerm
    biosample: Biosample
    gtex_tissue: str
    data_source: str
    assay: str
    def __init__(self, name: _Optional[str] = ..., ontology_term: _Optional[_Union[OntologyTerm, _Mapping]] = ..., biosample: _Optional[_Union[Biosample, _Mapping]] = ..., gtex_tissue: _Optional[str] = ..., data_source: _Optional[str] = ..., assay: _Optional[str] = ...) -> None: ...

class JunctionsMetadata(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.RepeatedCompositeFieldContainer[JunctionMetadata]
    def __init__(self, metadata: _Optional[_Iterable[_Union[JunctionMetadata, _Mapping]]] = ...) -> None: ...

class TrackData(_message.Message):
    __slots__ = ("values", "metadata", "resolution", "interval")
    VALUES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    values: _tensor_pb2.Tensor
    metadata: _containers.RepeatedCompositeFieldContainer[TrackMetadata]
    resolution: int
    interval: Interval
    def __init__(self, values: _Optional[_Union[_tensor_pb2.Tensor, _Mapping]] = ..., metadata: _Optional[_Iterable[_Union[TrackMetadata, _Mapping]]] = ..., resolution: _Optional[int] = ..., interval: _Optional[_Union[Interval, _Mapping]] = ...) -> None: ...

class JunctionData(_message.Message):
    __slots__ = ("values", "metadata", "junctions", "interval")
    VALUES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    JUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    values: _tensor_pb2.Tensor
    metadata: _containers.RepeatedCompositeFieldContainer[JunctionMetadata]
    junctions: _containers.RepeatedCompositeFieldContainer[Interval]
    interval: Interval
    def __init__(self, values: _Optional[_Union[_tensor_pb2.Tensor, _Mapping]] = ..., metadata: _Optional[_Iterable[_Union[JunctionMetadata, _Mapping]]] = ..., junctions: _Optional[_Iterable[_Union[Interval, _Mapping]]] = ..., interval: _Optional[_Union[Interval, _Mapping]] = ...) -> None: ...

class IntervalMetadata(_message.Message):
    __slots__ = ("interval", "track_metadata", "gene_metadata")
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    TRACK_METADATA_FIELD_NUMBER: _ClassVar[int]
    GENE_METADATA_FIELD_NUMBER: _ClassVar[int]
    interval: Interval
    track_metadata: _containers.RepeatedCompositeFieldContainer[TrackMetadata]
    gene_metadata: _containers.RepeatedCompositeFieldContainer[GeneScorerMetadata]
    def __init__(self, interval: _Optional[_Union[Interval, _Mapping]] = ..., track_metadata: _Optional[_Iterable[_Union[TrackMetadata, _Mapping]]] = ..., gene_metadata: _Optional[_Iterable[_Union[GeneScorerMetadata, _Mapping]]] = ...) -> None: ...

class IntervalData(_message.Message):
    __slots__ = ("values", "metadata")
    VALUES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    values: _tensor_pb2.Tensor
    metadata: IntervalMetadata
    def __init__(self, values: _Optional[_Union[_tensor_pb2.Tensor, _Mapping]] = ..., metadata: _Optional[_Union[IntervalMetadata, _Mapping]] = ...) -> None: ...

class VariantMetadata(_message.Message):
    __slots__ = ("variant", "track_metadata", "gene_metadata")
    VARIANT_FIELD_NUMBER: _ClassVar[int]
    TRACK_METADATA_FIELD_NUMBER: _ClassVar[int]
    GENE_METADATA_FIELD_NUMBER: _ClassVar[int]
    variant: Variant
    track_metadata: _containers.RepeatedCompositeFieldContainer[TrackMetadata]
    gene_metadata: _containers.RepeatedCompositeFieldContainer[GeneScorerMetadata]
    def __init__(self, variant: _Optional[_Union[Variant, _Mapping]] = ..., track_metadata: _Optional[_Iterable[_Union[TrackMetadata, _Mapping]]] = ..., gene_metadata: _Optional[_Iterable[_Union[GeneScorerMetadata, _Mapping]]] = ...) -> None: ...

class VariantData(_message.Message):
    __slots__ = ("values", "metadata")
    VALUES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    values: _tensor_pb2.Tensor
    metadata: VariantMetadata
    def __init__(self, values: _Optional[_Union[_tensor_pb2.Tensor, _Mapping]] = ..., metadata: _Optional[_Union[VariantMetadata, _Mapping]] = ...) -> None: ...

class Output(_message.Message):
    __slots__ = ("output_type", "track_data", "data", "junction_data")
    OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRACK_DATA_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    JUNCTION_DATA_FIELD_NUMBER: _ClassVar[int]
    output_type: OutputType
    track_data: TrackData
    data: _tensor_pb2.Tensor
    junction_data: JunctionData
    def __init__(self, output_type: _Optional[_Union[OutputType, str]] = ..., track_data: _Optional[_Union[TrackData, _Mapping]] = ..., data: _Optional[_Union[_tensor_pb2.Tensor, _Mapping]] = ..., junction_data: _Optional[_Union[JunctionData, _Mapping]] = ...) -> None: ...

class ScoreIntervalOutput(_message.Message):
    __slots__ = ("interval_data",)
    INTERVAL_DATA_FIELD_NUMBER: _ClassVar[int]
    interval_data: IntervalData
    def __init__(self, interval_data: _Optional[_Union[IntervalData, _Mapping]] = ...) -> None: ...

class ScoreVariantOutput(_message.Message):
    __slots__ = ("variant_data",)
    VARIANT_DATA_FIELD_NUMBER: _ClassVar[int]
    variant_data: VariantData
    def __init__(self, variant_data: _Optional[_Union[VariantData, _Mapping]] = ...) -> None: ...

class GeneMaskIntervalScorer(_message.Message):
    __slots__ = ("requested_output", "width", "aggregation_type")
    REQUESTED_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    requested_output: OutputType
    width: int
    aggregation_type: IntervalAggregationType
    def __init__(self, requested_output: _Optional[_Union[OutputType, str]] = ..., width: _Optional[int] = ..., aggregation_type: _Optional[_Union[IntervalAggregationType, str]] = ...) -> None: ...

class IntervalScorer(_message.Message):
    __slots__ = ("gene_mask",)
    GENE_MASK_FIELD_NUMBER: _ClassVar[int]
    gene_mask: GeneMaskIntervalScorer
    def __init__(self, gene_mask: _Optional[_Union[GeneMaskIntervalScorer, _Mapping]] = ...) -> None: ...

class CenterMaskScorer(_message.Message):
    __slots__ = ("width", "aggregation_type", "requested_output")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    width: int
    aggregation_type: AggregationType
    requested_output: OutputType
    def __init__(self, width: _Optional[int] = ..., aggregation_type: _Optional[_Union[AggregationType, str]] = ..., requested_output: _Optional[_Union[OutputType, str]] = ...) -> None: ...

class GeneMaskLFCScorer(_message.Message):
    __slots__ = ("requested_output",)
    REQUESTED_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    requested_output: OutputType
    def __init__(self, requested_output: _Optional[_Union[OutputType, str]] = ...) -> None: ...

class GeneMaskActiveScorer(_message.Message):
    __slots__ = ("requested_output",)
    REQUESTED_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    requested_output: OutputType
    def __init__(self, requested_output: _Optional[_Union[OutputType, str]] = ...) -> None: ...

class GeneMaskSplicingScorer(_message.Message):
    __slots__ = ("width", "requested_output")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    width: int
    requested_output: OutputType
    def __init__(self, width: _Optional[int] = ..., requested_output: _Optional[_Union[OutputType, str]] = ...) -> None: ...

class PolyadenylationScorer(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SpliceJunctionScorer(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ContactMapScorer(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class VariantScorer(_message.Message):
    __slots__ = ("center_mask", "gene_mask", "gene_mask_splicing", "pa_qtl", "splice_junction", "contact_map", "gene_mask_active")
    CENTER_MASK_FIELD_NUMBER: _ClassVar[int]
    GENE_MASK_FIELD_NUMBER: _ClassVar[int]
    GENE_MASK_SPLICING_FIELD_NUMBER: _ClassVar[int]
    PA_QTL_FIELD_NUMBER: _ClassVar[int]
    SPLICE_JUNCTION_FIELD_NUMBER: _ClassVar[int]
    CONTACT_MAP_FIELD_NUMBER: _ClassVar[int]
    GENE_MASK_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    center_mask: CenterMaskScorer
    gene_mask: GeneMaskLFCScorer
    gene_mask_splicing: GeneMaskSplicingScorer
    pa_qtl: PolyadenylationScorer
    splice_junction: SpliceJunctionScorer
    contact_map: ContactMapScorer
    gene_mask_active: GeneMaskActiveScorer
    def __init__(self, center_mask: _Optional[_Union[CenterMaskScorer, _Mapping]] = ..., gene_mask: _Optional[_Union[GeneMaskLFCScorer, _Mapping]] = ..., gene_mask_splicing: _Optional[_Union[GeneMaskSplicingScorer, _Mapping]] = ..., pa_qtl: _Optional[_Union[PolyadenylationScorer, _Mapping]] = ..., splice_junction: _Optional[_Union[SpliceJunctionScorer, _Mapping]] = ..., contact_map: _Optional[_Union[ContactMapScorer, _Mapping]] = ..., gene_mask_active: _Optional[_Union[GeneMaskActiveScorer, _Mapping]] = ...) -> None: ...

class OutputMetadata(_message.Message):
    __slots__ = ("output_type", "tracks", "junctions")
    OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRACKS_FIELD_NUMBER: _ClassVar[int]
    JUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    output_type: OutputType
    tracks: TracksMetadata
    junctions: JunctionsMetadata
    def __init__(self, output_type: _Optional[_Union[OutputType, str]] = ..., tracks: _Optional[_Union[TracksMetadata, _Mapping]] = ..., junctions: _Optional[_Union[JunctionsMetadata, _Mapping]] = ...) -> None: ...
