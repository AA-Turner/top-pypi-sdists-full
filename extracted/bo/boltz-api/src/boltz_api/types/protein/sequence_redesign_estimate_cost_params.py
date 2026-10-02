# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr

__all__ = [
    "SequenceRedesignEstimateCostParams",
    "BinderProteinSequenceRedesignRunInput",
    "BinderProteinSequenceRedesignRunInputEntity",
    "BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignTargetEntity",
    "BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntity",
    "BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotif",
    "BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotifFilter",
    "BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotifFilterExcludedAminoAcidsDesignFilter",
    "BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotifFilterMaxHydrophobicFractionDesignFilter",
    "BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotifFilterExcludedSequenceMotifsDesignFilter",
    "BinderProteinSequenceRedesignRunInputStructure",
    "BinderProteinSequenceRedesignRunInputStructureURLSource",
    "BinderProteinSequenceRedesignRunInputStructureCifBase64Source",
    "BinderProteinSequenceRedesignRunInputGlobalDesignFilter",
    "BinderProteinSequenceRedesignRunInputGlobalDesignFilterExcludedAminoAcidsDesignFilter",
    "BinderProteinSequenceRedesignRunInputGlobalDesignFilterMaxHydrophobicFractionDesignFilter",
    "BinderProteinSequenceRedesignRunInputGlobalDesignFilterExcludedSequenceMotifsDesignFilter",
    "GenericProteinSequenceRedesignRunInput",
    "GenericProteinSequenceRedesignRunInputEntity",
    "GenericProteinSequenceRedesignRunInputEntityDesignMotif",
    "GenericProteinSequenceRedesignRunInputEntityDesignMotifFilter",
    "GenericProteinSequenceRedesignRunInputEntityDesignMotifFilterExcludedAminoAcidsDesignFilter",
    "GenericProteinSequenceRedesignRunInputEntityDesignMotifFilterMaxHydrophobicFractionDesignFilter",
    "GenericProteinSequenceRedesignRunInputEntityDesignMotifFilterExcludedSequenceMotifsDesignFilter",
    "GenericProteinSequenceRedesignRunInputStructure",
    "GenericProteinSequenceRedesignRunInputStructureURLSource",
    "GenericProteinSequenceRedesignRunInputStructureCifBase64Source",
    "GenericProteinSequenceRedesignRunInputGlobalDesignFilter",
    "GenericProteinSequenceRedesignRunInputGlobalDesignFilterExcludedAminoAcidsDesignFilter",
    "GenericProteinSequenceRedesignRunInputGlobalDesignFilterMaxHydrophobicFractionDesignFilter",
    "GenericProteinSequenceRedesignRunInputGlobalDesignFilterExcludedSequenceMotifsDesignFilter",
]


class BinderProteinSequenceRedesignRunInput(TypedDict, total=False):
    entities: Required[Iterable[BinderProteinSequenceRedesignRunInputEntity]]
    """Every chain in the input CIF, assigned exactly once as target or binder."""

    num_proteins: Required[int]
    """Number of unique filter-passing redesigned proteins to generate."""

    structure: Required[BinderProteinSequenceRedesignRunInputStructure]
    """How to provide a CIF structure file.

    URLs are auto-detected; base64 uploads must use chemical/x-cif media type.
    """

    type: Required[Literal["binder"]]

    global_design_filters: Iterable[BinderProteinSequenceRedesignRunInputGlobalDesignFilter]
    """Filters applied to every redesigned region.

    When omitted, cysteine is excluded. Pass [] to disable global filters.
    """

    idempotency_key: str

    workspace_id: str
    """Workspace to run this redesign in."""


class BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignTargetEntity(TypedDict, total=False):
    """A fixed target chain from the input CIF."""

    chain_id: Required[str]

    role: Required[Literal["target"]]

    type: Required[Literal["from_template"]]


class BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotifFilterExcludedAminoAcidsDesignFilter(
    TypedDict, total=False
):
    amino_acids: Required[SequenceNotStr[str]]
    """
    Single-letter amino-acid codes that must not occur in the filtered designed
    region.
    """

    type: Required[Literal["excluded_amino_acids"]]


class BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotifFilterMaxHydrophobicFractionDesignFilter(
    TypedDict, total=False
):
    max_fraction: Required[float]

    type: Required[Literal["max_hydrophobic_fraction"]]


class BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotifFilterExcludedSequenceMotifsDesignFilter(
    TypedDict, total=False
):
    motifs: Required[SequenceNotStr[str]]
    """Sequence motifs that must not occur. X matches any single residue."""

    type: Required[Literal["excluded_sequence_motifs"]]


BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotifFilter: TypeAlias = Union[
    BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotifFilterExcludedAminoAcidsDesignFilter,
    BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotifFilterMaxHydrophobicFractionDesignFilter,
    BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotifFilterExcludedSequenceMotifsDesignFilter,
]


class BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotif(TypedDict, total=False):
    filters: Required[
        Iterable[BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotifFilter]
    ]
    """Filters applied to this motif in addition to global_design_filters."""

    residues: Required[Iterable[int]]
    """0-indexed residues to redesign on this chain."""

    type: Required[Literal["residues"]]


class BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntity(TypedDict, total=False):
    chain_id: Required[str]

    role: Required[Literal["binder"]]

    type: Required[Literal["from_template"]]

    design_motifs: Iterable[BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntityDesignMotif]
    """Residues to redesign. Omit this field to keep the binder chain fixed."""


BinderProteinSequenceRedesignRunInputEntity: TypeAlias = Union[
    BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignTargetEntity,
    BinderProteinSequenceRedesignRunInputEntityBinderSequenceRedesignBinderEntity,
]


class BinderProteinSequenceRedesignRunInputStructureURLSource(TypedDict, total=False):
    type: Required[Literal["url"]]

    url: Required[str]


class BinderProteinSequenceRedesignRunInputStructureCifBase64Source(TypedDict, total=False):
    data: Required[str]
    """Base64-encoded CIF file contents"""

    media_type: Required[Literal["chemical/x-cif"]]
    """Must be chemical/x-cif for CIF files"""

    type: Required[Literal["base64"]]


BinderProteinSequenceRedesignRunInputStructure: TypeAlias = Union[
    BinderProteinSequenceRedesignRunInputStructureURLSource,
    BinderProteinSequenceRedesignRunInputStructureCifBase64Source,
]


class BinderProteinSequenceRedesignRunInputGlobalDesignFilterExcludedAminoAcidsDesignFilter(TypedDict, total=False):
    amino_acids: Required[SequenceNotStr[str]]
    """
    Single-letter amino-acid codes that must not occur in the filtered designed
    region.
    """

    type: Required[Literal["excluded_amino_acids"]]


class BinderProteinSequenceRedesignRunInputGlobalDesignFilterMaxHydrophobicFractionDesignFilter(TypedDict, total=False):
    max_fraction: Required[float]

    type: Required[Literal["max_hydrophobic_fraction"]]


class BinderProteinSequenceRedesignRunInputGlobalDesignFilterExcludedSequenceMotifsDesignFilter(TypedDict, total=False):
    motifs: Required[SequenceNotStr[str]]
    """Sequence motifs that must not occur. X matches any single residue."""

    type: Required[Literal["excluded_sequence_motifs"]]


BinderProteinSequenceRedesignRunInputGlobalDesignFilter: TypeAlias = Union[
    BinderProteinSequenceRedesignRunInputGlobalDesignFilterExcludedAminoAcidsDesignFilter,
    BinderProteinSequenceRedesignRunInputGlobalDesignFilterMaxHydrophobicFractionDesignFilter,
    BinderProteinSequenceRedesignRunInputGlobalDesignFilterExcludedSequenceMotifsDesignFilter,
]


class GenericProteinSequenceRedesignRunInput(TypedDict, total=False):
    entities: Required[Iterable[GenericProteinSequenceRedesignRunInputEntity]]
    """Every chain in the input CIF, assigned exactly once."""

    num_proteins: Required[int]
    """Number of unique filter-passing redesigned proteins to generate."""

    structure: Required[GenericProteinSequenceRedesignRunInputStructure]
    """How to provide a CIF structure file.

    URLs are auto-detected; base64 uploads must use chemical/x-cif media type.
    """

    type: Required[Literal["generic"]]

    global_design_filters: Iterable[GenericProteinSequenceRedesignRunInputGlobalDesignFilter]
    """Filters applied to every redesigned region.

    When omitted, cysteine is excluded. Pass [] to disable global filters.
    """

    idempotency_key: str

    workspace_id: str
    """Workspace to run this redesign in."""


class GenericProteinSequenceRedesignRunInputEntityDesignMotifFilterExcludedAminoAcidsDesignFilter(
    TypedDict, total=False
):
    amino_acids: Required[SequenceNotStr[str]]
    """
    Single-letter amino-acid codes that must not occur in the filtered designed
    region.
    """

    type: Required[Literal["excluded_amino_acids"]]


class GenericProteinSequenceRedesignRunInputEntityDesignMotifFilterMaxHydrophobicFractionDesignFilter(
    TypedDict, total=False
):
    max_fraction: Required[float]

    type: Required[Literal["max_hydrophobic_fraction"]]


class GenericProteinSequenceRedesignRunInputEntityDesignMotifFilterExcludedSequenceMotifsDesignFilter(
    TypedDict, total=False
):
    motifs: Required[SequenceNotStr[str]]
    """Sequence motifs that must not occur. X matches any single residue."""

    type: Required[Literal["excluded_sequence_motifs"]]


GenericProteinSequenceRedesignRunInputEntityDesignMotifFilter: TypeAlias = Union[
    GenericProteinSequenceRedesignRunInputEntityDesignMotifFilterExcludedAminoAcidsDesignFilter,
    GenericProteinSequenceRedesignRunInputEntityDesignMotifFilterMaxHydrophobicFractionDesignFilter,
    GenericProteinSequenceRedesignRunInputEntityDesignMotifFilterExcludedSequenceMotifsDesignFilter,
]


class GenericProteinSequenceRedesignRunInputEntityDesignMotif(TypedDict, total=False):
    filters: Required[Iterable[GenericProteinSequenceRedesignRunInputEntityDesignMotifFilter]]
    """Filters applied to this motif in addition to global_design_filters."""

    residues: Required[Iterable[int]]
    """0-indexed residues to redesign on this chain."""

    type: Required[Literal["residues"]]


class GenericProteinSequenceRedesignRunInputEntity(TypedDict, total=False):
    chain_id: Required[str]

    type: Required[Literal["from_template"]]

    design_motifs: Iterable[GenericProteinSequenceRedesignRunInputEntityDesignMotif]
    """Residues to redesign. Omit this field to keep the chain fixed."""


class GenericProteinSequenceRedesignRunInputStructureURLSource(TypedDict, total=False):
    type: Required[Literal["url"]]

    url: Required[str]


class GenericProteinSequenceRedesignRunInputStructureCifBase64Source(TypedDict, total=False):
    data: Required[str]
    """Base64-encoded CIF file contents"""

    media_type: Required[Literal["chemical/x-cif"]]
    """Must be chemical/x-cif for CIF files"""

    type: Required[Literal["base64"]]


GenericProteinSequenceRedesignRunInputStructure: TypeAlias = Union[
    GenericProteinSequenceRedesignRunInputStructureURLSource,
    GenericProteinSequenceRedesignRunInputStructureCifBase64Source,
]


class GenericProteinSequenceRedesignRunInputGlobalDesignFilterExcludedAminoAcidsDesignFilter(TypedDict, total=False):
    amino_acids: Required[SequenceNotStr[str]]
    """
    Single-letter amino-acid codes that must not occur in the filtered designed
    region.
    """

    type: Required[Literal["excluded_amino_acids"]]


class GenericProteinSequenceRedesignRunInputGlobalDesignFilterMaxHydrophobicFractionDesignFilter(
    TypedDict, total=False
):
    max_fraction: Required[float]

    type: Required[Literal["max_hydrophobic_fraction"]]


class GenericProteinSequenceRedesignRunInputGlobalDesignFilterExcludedSequenceMotifsDesignFilter(
    TypedDict, total=False
):
    motifs: Required[SequenceNotStr[str]]
    """Sequence motifs that must not occur. X matches any single residue."""

    type: Required[Literal["excluded_sequence_motifs"]]


GenericProteinSequenceRedesignRunInputGlobalDesignFilter: TypeAlias = Union[
    GenericProteinSequenceRedesignRunInputGlobalDesignFilterExcludedAminoAcidsDesignFilter,
    GenericProteinSequenceRedesignRunInputGlobalDesignFilterMaxHydrophobicFractionDesignFilter,
    GenericProteinSequenceRedesignRunInputGlobalDesignFilterExcludedSequenceMotifsDesignFilter,
]

SequenceRedesignEstimateCostParams: TypeAlias = Union[
    BinderProteinSequenceRedesignRunInput, GenericProteinSequenceRedesignRunInput
]
