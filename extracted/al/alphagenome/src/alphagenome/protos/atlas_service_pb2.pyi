from alphagenome.protos import dna_model_pb2 as _dna_model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VariantScorerInfo(_message.Message):
    __slots__ = ("name", "is_signed")
    NAME_FIELD_NUMBER: _ClassVar[int]
    IS_SIGNED_FIELD_NUMBER: _ClassVar[int]
    name: str
    is_signed: bool
    def __init__(self, name: _Optional[str] = ..., is_signed: bool = ...) -> None: ...

class GeneScorersMetadata(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.RepeatedCompositeFieldContainer[_dna_model_pb2.GeneScorerMetadata]
    def __init__(self, metadata: _Optional[_Iterable[_Union[_dna_model_pb2.GeneScorerMetadata, _Mapping]]] = ...) -> None: ...

class Metadata(_message.Message):
    __slots__ = ("tracks", "gene_scorers")
    TRACKS_FIELD_NUMBER: _ClassVar[int]
    GENE_SCORERS_FIELD_NUMBER: _ClassVar[int]
    tracks: _dna_model_pb2.TracksMetadata
    gene_scorers: GeneScorersMetadata
    def __init__(self, tracks: _Optional[_Union[_dna_model_pb2.TracksMetadata, _Mapping]] = ..., gene_scorers: _Optional[_Union[GeneScorersMetadata, _Mapping]] = ...) -> None: ...

class DenseVariantScore(_message.Message):
    __slots__ = ("variant_scorer", "metadata", "shape", "scores", "calibrated_scores")
    VARIANT_SCORER_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    CALIBRATED_SCORES_FIELD_NUMBER: _ClassVar[int]
    variant_scorer: VariantScorerInfo
    metadata: _containers.RepeatedCompositeFieldContainer[Metadata]
    shape: _containers.RepeatedScalarFieldContainer[int]
    scores: bytes
    calibrated_scores: bytes
    def __init__(self, variant_scorer: _Optional[_Union[VariantScorerInfo, _Mapping]] = ..., metadata: _Optional[_Iterable[_Union[Metadata, _Mapping]]] = ..., shape: _Optional[_Iterable[int]] = ..., scores: _Optional[bytes] = ..., calibrated_scores: _Optional[bytes] = ...) -> None: ...

class DenseVariantScores(_message.Message):
    __slots__ = ("variant", "interval", "scores")
    VARIANT_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    variant: _dna_model_pb2.Variant
    interval: _dna_model_pb2.Interval
    scores: _containers.RepeatedCompositeFieldContainer[DenseVariantScore]
    def __init__(self, variant: _Optional[_Union[_dna_model_pb2.Variant, _Mapping]] = ..., interval: _Optional[_Union[_dna_model_pb2.Interval, _Mapping]] = ..., scores: _Optional[_Iterable[_Union[DenseVariantScore, _Mapping]]] = ...) -> None: ...

class VariantScorerMetadata(_message.Message):
    __slots__ = ("variant_scorer", "metadata")
    VARIANT_SCORER_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    variant_scorer: VariantScorerInfo
    metadata: _containers.RepeatedCompositeFieldContainer[Metadata]
    def __init__(self, variant_scorer: _Optional[_Union[VariantScorerInfo, _Mapping]] = ..., metadata: _Optional[_Iterable[_Union[Metadata, _Mapping]]] = ...) -> None: ...

class ListDenseVariantScoresRequest(_message.Message):
    __slots__ = ("interval", "organism", "page_size", "page_token", "filter")
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    ORGANISM_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    interval: _dna_model_pb2.Interval
    organism: _dna_model_pb2.Organism
    page_size: int
    page_token: str
    filter: str
    def __init__(self, interval: _Optional[_Union[_dna_model_pb2.Interval, _Mapping]] = ..., organism: _Optional[_Union[_dna_model_pb2.Organism, str]] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., filter: _Optional[str] = ...) -> None: ...

class ListDenseVariantScoresResponse(_message.Message):
    __slots__ = ("variant_scores", "next_page_token", "interval")
    VARIANT_SCORES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    variant_scores: _containers.RepeatedCompositeFieldContainer[DenseVariantScores]
    next_page_token: str
    interval: _dna_model_pb2.Interval
    def __init__(self, variant_scores: _Optional[_Iterable[_Union[DenseVariantScores, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., interval: _Optional[_Union[_dna_model_pb2.Interval, _Mapping]] = ...) -> None: ...

class GetDenseVariantScoresRequest(_message.Message):
    __slots__ = ("variant", "organism", "filter")
    VARIANT_FIELD_NUMBER: _ClassVar[int]
    ORGANISM_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    variant: _dna_model_pb2.Variant
    organism: _dna_model_pb2.Organism
    filter: str
    def __init__(self, variant: _Optional[_Union[_dna_model_pb2.Variant, _Mapping]] = ..., organism: _Optional[_Union[_dna_model_pb2.Organism, str]] = ..., filter: _Optional[str] = ...) -> None: ...

class ListVariantScoresMetadataRequest(_message.Message):
    __slots__ = ("organism",)
    ORGANISM_FIELD_NUMBER: _ClassVar[int]
    organism: _dna_model_pb2.Organism
    def __init__(self, organism: _Optional[_Union[_dna_model_pb2.Organism, str]] = ...) -> None: ...

class ListVariantScoresMetadataResponse(_message.Message):
    __slots__ = ("variant_scorer_metadata",)
    VARIANT_SCORER_METADATA_FIELD_NUMBER: _ClassVar[int]
    variant_scorer_metadata: _containers.RepeatedCompositeFieldContainer[VariantScorerMetadata]
    def __init__(self, variant_scorer_metadata: _Optional[_Iterable[_Union[VariantScorerMetadata, _Mapping]]] = ...) -> None: ...
