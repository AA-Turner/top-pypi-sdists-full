"""Define Pydantic Class models for VRSATILE models."""
from __future__ import annotations
from enum import Enum
from typing import List, Optional, Union, Any, Literal

from pydantic import BaseModel, StrictInt, StrictStr, \
    model_validator, field_validator, Field

from ga4gh.vrsatile.pydantic import return_value, BaseModelForbidExtra
from ga4gh.vrsatile.pydantic.vrs_models import CURIE, Allele, CopyNumberChange, \
    CopyNumberCount, Haplotype, Text, VariationSet, SequenceLocation, \
    ChromosomeLocation, SEQUENCE, Gene


class VODClassName(str, Enum):
    """Define VOD class names."""

    VARIATION_DESCRIPTOR = "VariationDescriptor"
    LOCATION_DESCRIPTOR = "LocationDescriptor"
    SEQUENCE_DESCRIPTOR = "SequenceDescriptor"
    GENE_DESCRIPTOR = "GeneDescriptor"
    CATEGORICAL_VARIATION_DESCRIPTOR = "CategoricalVariationDescriptor"


class VRSATILETypes(str, Enum):
    """Define types used in VRSATILE."""

    EXTENSION = "Extension"
    EXPRESSION = "Expression"


class MoleculeContext(str, Enum):
    """The structural variant type associated with this variant."""

    GENOMIC = "genomic"
    TRANSCRIPT = "transcript"
    PROTEIN = "protein"


class Extension(BaseModelForbidExtra):
    """The Extension class provides VODs with a means to extend descriptions
    with other attributes unique to a content provider. These extensions are
    not expected to be natively understood under VRSATILE, but may be used
    for pre-negotiated exchange of message attributes when needed.
    """

    type: Literal[VRSATILETypes.EXTENSION] = VRSATILETypes.EXTENSION
    name: StrictStr
    value: Any


class ExpressionSyntax(str, Enum):
    """Possible values for the Expression `syntax` property."""

    HGVS_C = "hgvs.c"
    HGVS_P = "hgvs.p"
    HGVS_G = "hgvs.g"
    HGVS_M = "hgvs.m"
    HGVS_N = "hgvs.n"
    HGVS_R = "hgvs.r"
    ISCN = "iscn"
    GNOMAD = "gnomad"
    SPDI = "spdi"


class Expression(BaseModelForbidExtra):
    """Representation of a variation by a specified nomenclature or syntax for
    a Variation object. Common examples of expressions for the description of
    molecular variation include the HGVS and ISCN nomenclatures.
    """

    type: Literal[VRSATILETypes.EXPRESSION] = VRSATILETypes.EXPRESSION
    syntax: ExpressionSyntax
    value: StrictStr
    syntax_version: Optional[StrictStr] = None


class ValueObjectDescriptor(BaseModel, extra="allow"):
    """The root class of all VODs is the abstract Value Object Descriptor
    class. All attributes of this parent class are inherited by child classes.
    """

    id: CURIE
    type: StrictStr
    label: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    xrefs: Optional[List[CURIE]] = None
    alternate_labels: Optional[List[StrictStr]] = None
    extensions: Optional[List[Extension]] = None

    _get_id_val = field_validator('id')(return_value)
    _get_xrefs_val = field_validator('xrefs')(return_value)


class SequenceDescriptor(BaseModelForbidExtra, ValueObjectDescriptor):
    """This descriptor is intended to reference VRS Sequence value objects."""

    type: Literal[VODClassName.SEQUENCE_DESCRIPTOR] = \
        VODClassName.SEQUENCE_DESCRIPTOR
    sequence_id: Optional[CURIE] = None
    sequence: Optional[SEQUENCE] = None
    residue_type: Optional[CURIE] = None

    @model_validator(mode="after")
    def check_sequence_or_sequence_id_present(cls, values):
        """Check that at least one of {`sequence`, `sequence_id`} is set."""
        msg = 'Must give values for either `sequence`, `sequence_id`, or both'
        value, value_id = values.sequence, values.sequence_id
        assert value or value_id, msg
        return values

    _get_sequence_id_val = \
        field_validator('sequence_id')(return_value)
    _get_sequence_val = field_validator('sequence')(return_value)
    _get_residue_type_val = \
        field_validator('residue_type')(return_value)


class LocationDescriptor(BaseModelForbidExtra, ValueObjectDescriptor):
    """This descriptor is intended to reference VRS Location value objects."""

    type: Literal[VODClassName.LOCATION_DESCRIPTOR] = \
        VODClassName.LOCATION_DESCRIPTOR
    location_id: Optional[CURIE] = None
    location: Optional[Union[SequenceLocation, ChromosomeLocation]] = None

    @model_validator(mode="after")
    def check_location_or_location_id_present(cls, values):
        """Check that at least one of {`location`, `location_id`} is set."""
        msg = 'Must give values for either `location`, `location_id`, or both'
        value, value_id = values.location, values.location_id
        assert value or value_id, msg
        return values

    _get_location_id_val = \
        field_validator('location_id')(return_value)


class GeneDescriptor(BaseModelForbidExtra, ValueObjectDescriptor):
    """This descriptor is intended to reference VRS Gene value objects."""

    type: Literal[VODClassName.GENE_DESCRIPTOR] = VODClassName.GENE_DESCRIPTOR
    gene_id: Optional[CURIE] = None
    gene: Optional[Gene] = None

    @model_validator(mode="after")
    def check_gene_or_gene_id_present(cls, values):
        """Check that at least one of {`gene`, `gene_id`} is set."""
        msg = 'Must give values for either `gene`, `gene_id`, or both'
        value, value_id = values.gene, values.gene_id
        assert value or value_id, msg
        return values

    _get_gene_id_val = field_validator('gene_id')(return_value)


class VCFRecord(BaseModelForbidExtra):
    """This data class is used when it is desirable to pass data as expected
    from a VCF record.
    """

    genome_assembly: StrictStr
    chrom: StrictStr
    pos: StrictInt
    id: Optional[StrictStr] = None
    ref: StrictStr
    alt: StrictStr
    qual: Optional[StrictStr] = None
    filter: Optional[StrictStr] = None
    info: Optional[StrictStr] = None


class VariationDescriptor(BaseModelForbidExtra, ValueObjectDescriptor):
    """This descriptor is intended as an class for describing VRS Variation
    value objects.
    """

    type: Literal[VODClassName.VARIATION_DESCRIPTOR] = \
        VODClassName.VARIATION_DESCRIPTOR
    variation_id: Optional[CURIE] = None
    variation: Optional[Union[Allele, Haplotype, CopyNumberChange, CopyNumberCount,
                              Text, VariationSet]] = None
    molecule_context: Optional[MoleculeContext] = None
    structural_type: Optional[CURIE] = None
    expressions: Optional[List[Expression]] = None
    vcf_record: Optional[VCFRecord] = None
    gene_context: Optional[Union[CURIE, GeneDescriptor]] = None
    vrs_ref_allele_seq: Optional[SEQUENCE] = None
    allelic_state: Optional[CURIE] = None

    _get_variation_id_val = \
        field_validator('variation_id')(return_value)
    _get_structural_type_val = \
        field_validator('structural_type')(return_value)
    _get_gene_context_val = \
        field_validator('gene_context')(return_value)
    _get_vrs_allele_ref_seq_val = \
        field_validator('vrs_ref_allele_seq')(return_value)
    _get_allelic_state_val = \
        field_validator('allelic_state')(return_value)


class CategoricalVariationType(str, Enum):
    """Possible types for Categorical Variations."""

    CANONICAL_VARIATION = "CanonicalVariation"
    COMPLEX_VARIATION = "ComplexVariation"


class CategoricalVariation(BaseModelForbidExtra):
    """A representation of a categorically-defined `functional domain
    <https://en.wikipedia.org/wiki/Domain_of_a_function>`_ for variation, in
    which individual variation instances may be members.
    """

    id: Optional[CURIE] = Field(None, alias="_id")
    type: CategoricalVariationType
    complement: bool

    _get_id_val = field_validator("id")(return_value)


class CanonicalVariation(CategoricalVariation):
    """A categorical variation domain characterized by a representative
    Variation context to which members lift-over, project, translate, or
    otherwise directly align.
    """

    type: Literal[CategoricalVariationType.CANONICAL_VARIATION] = \
        CategoricalVariationType.CANONICAL_VARIATION
    variation: Optional[Union[Allele, Haplotype, CopyNumberChange, CopyNumberCount,
                              Text, VariationSet]] = None


class ComplexVariationOperator(str, Enum):
    """Possible values for the Complex Variation's `operator` field."""

    AND = "AND"
    OR = "OR"


class ComplexVariation(CategoricalVariation):
    """A categorical variation domain jointly characterized by two or more
    other categorical variation domains.
    """

    type: Literal[CategoricalVariationType.COMPLEX_VARIATION] = \
        CategoricalVariationType.COMPLEX_VARIATION
    operands: List[CategoricalVariation]
    operator: ComplexVariationOperator

    @model_validator(mode="after")
    def check_operands_length(cls, values):
        """Check that `operands` contains >=2 objects"""
        assert len(values.operands) >= 2
        return values


class VariationMember(BaseModel):
    """A compact class for representing a variation context that is a member of
    a Categorical Variation. It supports one or more Expressions of a Variation
    and optionally an associated VRS ID.
    """

    type: Literal["VariationMember"] = "VariationMember"
    expressions: List[Expression]
    variation_id: Optional[CURIE] = None

    _get_variation_id_val = \
        field_validator("variation_id")(return_value)

    @model_validator(mode="after")
    def check_expressions_length(cls, values):
        """Check that `expressions` contains >=1 objects"""
        assert len(values.expressions) >= 1
        return values


class CategoricalVariationDescriptor(VariationDescriptor):
    """This descriptor class is used for describing Categorical Variation
    value objects.
    """

    type: Literal[VODClassName.CATEGORICAL_VARIATION_DESCRIPTOR] = \
        VODClassName.CATEGORICAL_VARIATION_DESCRIPTOR
    version: Optional[StrictStr] = None
    categorical_variation_id: Optional[CURIE] = None
    categorical_variation: Optional[Union[CanonicalVariation,
                                          ComplexVariation]] = None
    members: Optional[List[VariationMember]] = None

    _get_categorical_variation_id_val = \
        field_validator("categorical_variation_id")(return_value)
