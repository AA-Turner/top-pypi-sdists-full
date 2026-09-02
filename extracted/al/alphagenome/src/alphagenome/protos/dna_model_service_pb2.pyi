from alphagenome.protos import dna_model_pb2 as _dna_model_pb2
from alphagenome.protos import tensor_pb2 as _tensor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PredictSequenceRequest(_message.Message):
    __slots__ = ("sequence", "organism", "ontology_terms", "requested_outputs", "model_version")
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    ORGANISM_FIELD_NUMBER: _ClassVar[int]
    ONTOLOGY_TERMS_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    sequence: str
    organism: _dna_model_pb2.Organism
    ontology_terms: _containers.RepeatedCompositeFieldContainer[_dna_model_pb2.OntologyTerm]
    requested_outputs: _containers.RepeatedScalarFieldContainer[_dna_model_pb2.OutputType]
    model_version: str
    def __init__(self, sequence: _Optional[str] = ..., organism: _Optional[_Union[_dna_model_pb2.Organism, str]] = ..., ontology_terms: _Optional[_Iterable[_Union[_dna_model_pb2.OntologyTerm, _Mapping]]] = ..., requested_outputs: _Optional[_Iterable[_Union[_dna_model_pb2.OutputType, str]]] = ..., model_version: _Optional[str] = ...) -> None: ...

class PredictSequenceResponse(_message.Message):
    __slots__ = ("output", "tensor_chunk")
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TENSOR_CHUNK_FIELD_NUMBER: _ClassVar[int]
    output: _dna_model_pb2.Output
    tensor_chunk: _tensor_pb2.TensorChunk
    def __init__(self, output: _Optional[_Union[_dna_model_pb2.Output, _Mapping]] = ..., tensor_chunk: _Optional[_Union[_tensor_pb2.TensorChunk, _Mapping]] = ...) -> None: ...

class PredictIntervalRequest(_message.Message):
    __slots__ = ("interval", "organism", "requested_outputs", "ontology_terms", "model_version")
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    ORGANISM_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    ONTOLOGY_TERMS_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    interval: _dna_model_pb2.Interval
    organism: _dna_model_pb2.Organism
    requested_outputs: _containers.RepeatedScalarFieldContainer[_dna_model_pb2.OutputType]
    ontology_terms: _containers.RepeatedCompositeFieldContainer[_dna_model_pb2.OntologyTerm]
    model_version: str
    def __init__(self, interval: _Optional[_Union[_dna_model_pb2.Interval, _Mapping]] = ..., organism: _Optional[_Union[_dna_model_pb2.Organism, str]] = ..., requested_outputs: _Optional[_Iterable[_Union[_dna_model_pb2.OutputType, str]]] = ..., ontology_terms: _Optional[_Iterable[_Union[_dna_model_pb2.OntologyTerm, _Mapping]]] = ..., model_version: _Optional[str] = ...) -> None: ...

class PredictIntervalResponse(_message.Message):
    __slots__ = ("output", "tensor_chunk")
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TENSOR_CHUNK_FIELD_NUMBER: _ClassVar[int]
    output: _dna_model_pb2.Output
    tensor_chunk: _tensor_pb2.TensorChunk
    def __init__(self, output: _Optional[_Union[_dna_model_pb2.Output, _Mapping]] = ..., tensor_chunk: _Optional[_Union[_tensor_pb2.TensorChunk, _Mapping]] = ...) -> None: ...

class PredictVariantRequest(_message.Message):
    __slots__ = ("interval", "variant", "organism", "requested_outputs", "ontology_terms", "model_version")
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    VARIANT_FIELD_NUMBER: _ClassVar[int]
    ORGANISM_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    ONTOLOGY_TERMS_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    interval: _dna_model_pb2.Interval
    variant: _dna_model_pb2.Variant
    organism: _dna_model_pb2.Organism
    requested_outputs: _containers.RepeatedScalarFieldContainer[_dna_model_pb2.OutputType]
    ontology_terms: _containers.RepeatedCompositeFieldContainer[_dna_model_pb2.OntologyTerm]
    model_version: str
    def __init__(self, interval: _Optional[_Union[_dna_model_pb2.Interval, _Mapping]] = ..., variant: _Optional[_Union[_dna_model_pb2.Variant, _Mapping]] = ..., organism: _Optional[_Union[_dna_model_pb2.Organism, str]] = ..., requested_outputs: _Optional[_Iterable[_Union[_dna_model_pb2.OutputType, str]]] = ..., ontology_terms: _Optional[_Iterable[_Union[_dna_model_pb2.OntologyTerm, _Mapping]]] = ..., model_version: _Optional[str] = ...) -> None: ...

class PredictVariantResponse(_message.Message):
    __slots__ = ("reference_output", "alternate_output", "tensor_chunk")
    REFERENCE_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    ALTERNATE_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TENSOR_CHUNK_FIELD_NUMBER: _ClassVar[int]
    reference_output: _dna_model_pb2.Output
    alternate_output: _dna_model_pb2.Output
    tensor_chunk: _tensor_pb2.TensorChunk
    def __init__(self, reference_output: _Optional[_Union[_dna_model_pb2.Output, _Mapping]] = ..., alternate_output: _Optional[_Union[_dna_model_pb2.Output, _Mapping]] = ..., tensor_chunk: _Optional[_Union[_tensor_pb2.TensorChunk, _Mapping]] = ...) -> None: ...

class ScoreIntervalRequest(_message.Message):
    __slots__ = ("interval", "organism", "interval_scorers", "model_version", "merge_stranded_gene_tracks")
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    ORGANISM_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_SCORERS_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    MERGE_STRANDED_GENE_TRACKS_FIELD_NUMBER: _ClassVar[int]
    interval: _dna_model_pb2.Interval
    organism: _dna_model_pb2.Organism
    interval_scorers: _containers.RepeatedCompositeFieldContainer[_dna_model_pb2.IntervalScorer]
    model_version: str
    merge_stranded_gene_tracks: bool
    def __init__(self, interval: _Optional[_Union[_dna_model_pb2.Interval, _Mapping]] = ..., organism: _Optional[_Union[_dna_model_pb2.Organism, str]] = ..., interval_scorers: _Optional[_Iterable[_Union[_dna_model_pb2.IntervalScorer, _Mapping]]] = ..., model_version: _Optional[str] = ..., merge_stranded_gene_tracks: bool = ...) -> None: ...

class ScoreIntervalResponse(_message.Message):
    __slots__ = ("output", "tensor_chunk")
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TENSOR_CHUNK_FIELD_NUMBER: _ClassVar[int]
    output: _dna_model_pb2.ScoreIntervalOutput
    tensor_chunk: _tensor_pb2.TensorChunk
    def __init__(self, output: _Optional[_Union[_dna_model_pb2.ScoreIntervalOutput, _Mapping]] = ..., tensor_chunk: _Optional[_Union[_tensor_pb2.TensorChunk, _Mapping]] = ...) -> None: ...

class ScoreVariantRequest(_message.Message):
    __slots__ = ("interval", "variant", "organism", "variant_scorers", "model_version", "merge_stranded_gene_tracks")
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    VARIANT_FIELD_NUMBER: _ClassVar[int]
    ORGANISM_FIELD_NUMBER: _ClassVar[int]
    VARIANT_SCORERS_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    MERGE_STRANDED_GENE_TRACKS_FIELD_NUMBER: _ClassVar[int]
    interval: _dna_model_pb2.Interval
    variant: _dna_model_pb2.Variant
    organism: _dna_model_pb2.Organism
    variant_scorers: _containers.RepeatedCompositeFieldContainer[_dna_model_pb2.VariantScorer]
    model_version: str
    merge_stranded_gene_tracks: bool
    def __init__(self, interval: _Optional[_Union[_dna_model_pb2.Interval, _Mapping]] = ..., variant: _Optional[_Union[_dna_model_pb2.Variant, _Mapping]] = ..., organism: _Optional[_Union[_dna_model_pb2.Organism, str]] = ..., variant_scorers: _Optional[_Iterable[_Union[_dna_model_pb2.VariantScorer, _Mapping]]] = ..., model_version: _Optional[str] = ..., merge_stranded_gene_tracks: bool = ...) -> None: ...

class ScoreVariantResponse(_message.Message):
    __slots__ = ("output", "tensor_chunk")
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TENSOR_CHUNK_FIELD_NUMBER: _ClassVar[int]
    output: _dna_model_pb2.ScoreVariantOutput
    tensor_chunk: _tensor_pb2.TensorChunk
    def __init__(self, output: _Optional[_Union[_dna_model_pb2.ScoreVariantOutput, _Mapping]] = ..., tensor_chunk: _Optional[_Union[_tensor_pb2.TensorChunk, _Mapping]] = ...) -> None: ...

class ScoreIsmVariantRequest(_message.Message):
    __slots__ = ("interval", "ism_interval", "organism", "variant_scorers", "interval_variant", "model_version", "merge_stranded_gene_tracks")
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    ISM_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    ORGANISM_FIELD_NUMBER: _ClassVar[int]
    VARIANT_SCORERS_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_VARIANT_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    MERGE_STRANDED_GENE_TRACKS_FIELD_NUMBER: _ClassVar[int]
    interval: _dna_model_pb2.Interval
    ism_interval: _dna_model_pb2.Interval
    organism: _dna_model_pb2.Organism
    variant_scorers: _containers.RepeatedCompositeFieldContainer[_dna_model_pb2.VariantScorer]
    interval_variant: _dna_model_pb2.Variant
    model_version: str
    merge_stranded_gene_tracks: bool
    def __init__(self, interval: _Optional[_Union[_dna_model_pb2.Interval, _Mapping]] = ..., ism_interval: _Optional[_Union[_dna_model_pb2.Interval, _Mapping]] = ..., organism: _Optional[_Union[_dna_model_pb2.Organism, str]] = ..., variant_scorers: _Optional[_Iterable[_Union[_dna_model_pb2.VariantScorer, _Mapping]]] = ..., interval_variant: _Optional[_Union[_dna_model_pb2.Variant, _Mapping]] = ..., model_version: _Optional[str] = ..., merge_stranded_gene_tracks: bool = ...) -> None: ...

class ScoreIsmVariantResponse(_message.Message):
    __slots__ = ("output", "tensor_chunk")
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TENSOR_CHUNK_FIELD_NUMBER: _ClassVar[int]
    output: _dna_model_pb2.ScoreVariantOutput
    tensor_chunk: _tensor_pb2.TensorChunk
    def __init__(self, output: _Optional[_Union[_dna_model_pb2.ScoreVariantOutput, _Mapping]] = ..., tensor_chunk: _Optional[_Union[_tensor_pb2.TensorChunk, _Mapping]] = ...) -> None: ...

class MetadataRequest(_message.Message):
    __slots__ = ("organism",)
    ORGANISM_FIELD_NUMBER: _ClassVar[int]
    organism: _dna_model_pb2.Organism
    def __init__(self, organism: _Optional[_Union[_dna_model_pb2.Organism, str]] = ...) -> None: ...

class MetadataResponse(_message.Message):
    __slots__ = ("output_metadata",)
    OUTPUT_METADATA_FIELD_NUMBER: _ClassVar[int]
    output_metadata: _containers.RepeatedCompositeFieldContainer[_dna_model_pb2.OutputMetadata]
    def __init__(self, output_metadata: _Optional[_Iterable[_Union[_dna_model_pb2.OutputMetadata, _Mapping]]] = ...) -> None: ...
