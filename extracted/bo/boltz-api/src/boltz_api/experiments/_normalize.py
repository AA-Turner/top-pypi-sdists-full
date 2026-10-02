from __future__ import annotations

import base64
from os import PathLike
from enum import Enum
from typing import Union, cast
from pathlib import Path
from collections.abc import Mapping, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .inputs import (
    DNA,
    RNA,
    Bond,
    Protein,
    LigandCcd,
    BoltzModel,
    LigandSmiles,
    ModelOptions,
    PocketConstraint,
    ContactConstraint,
    LigandProteinBinding,
    ProteinProteinBinding,
)
from ._errors import ExperimentError
from ..types.protein import (
    design_start_params as protein_design_start_params,
    library_screen_start_params as protein_library_screen_start_params,
)
from ..types.predictions import structure_and_binding_start_params
from ..types.small_molecule import (
    design_start_params as small_molecule_design_start_params,
    library_screen_start_params as small_molecule_library_screen_start_params,
)

StructureSourceInput: TypeAlias = Union[
    protein_design_start_params.ProteinDesignRunInputBinderSpecificationStructureTemplateBinderSpecStructure,
    protein_design_start_params.ProteinDesignRunInputTargetStructureTemplateTargetStructure,
    protein_library_screen_start_params.TargetStructureTemplateTargetStructure,
    str,
    PathLike[str],
]
NormalizedStructureSource: TypeAlias = Union[
    protein_design_start_params.ProteinDesignRunInputBinderSpecificationStructureTemplateBinderSpecStructure,
    protein_design_start_params.ProteinDesignRunInputTargetStructureTemplateTargetStructure,
    protein_library_screen_start_params.TargetStructureTemplateTargetStructure,
]


class ProteinDesignStructureTemplateBinderSpecificationInput(TypedDict, total=False):
    chain_selection: Required[
        dict[
            str,
            protein_design_start_params.ProteinDesignRunInputBinderSpecificationStructureTemplateBinderSpecChainSelection,
        ]
    ]
    modality: Required[Literal["peptide", "antibody", "nanobody", "custom_protein"]]
    structure: Required[StructureSourceInput]
    type: Required[Literal["structure_template"]]
    rules: protein_design_start_params.ProteinDesignRunInputBinderSpecificationStructureTemplateBinderSpecRules


class ProteinDesignStructureTemplateTargetInput(TypedDict, total=False):
    chain_selection: Required[
        dict[str, protein_design_start_params.ProteinDesignRunInputTargetStructureTemplateTargetChainSelection]
    ]
    structure: Required[StructureSourceInput]
    type: Required[Literal["structure_template"]]


class ProteinLibraryScreenStructureTemplateTargetInput(TypedDict, total=False):
    chain_selection: Required[
        dict[str, protein_library_screen_start_params.TargetStructureTemplateTargetChainSelection]
    ]
    structure: Required[StructureSourceInput]
    type: Required[Literal["structure_template"]]


ProteinDesignBinderSpecificationInput: TypeAlias = Union[
    protein_design_start_params.ProteinDesignRunInputBinderSpecification,
    ProteinDesignStructureTemplateBinderSpecificationInput,
]
ProteinDesignTargetInput: TypeAlias = Union[
    protein_design_start_params.ProteinDesignRunInputTargetNoTemplateTarget,
    protein_design_start_params.ProteinDesignRunInputTargetStructureTemplateTarget,
    ProteinDesignStructureTemplateTargetInput,
]
ProteinLibraryScreenTargetInput: TypeAlias = Union[
    protein_library_screen_start_params.TargetNoTemplateTarget,
    protein_library_screen_start_params.TargetStructureTemplateTarget,
    ProteinLibraryScreenStructureTemplateTargetInput,
]
PredictionModelInput: TypeAlias = Union[Literal["boltz-2.1"], BoltzModel]
PredictionEntityInput: TypeAlias = Union[
    structure_and_binding_start_params.InputEntity,
    Protein,
    RNA,
    DNA,
    LigandCcd,
    LigandSmiles,
]
PredictionBindingInput: TypeAlias = Union[
    structure_and_binding_start_params.InputBinding,
    LigandProteinBinding,
    ProteinProteinBinding,
]
PredictionBondInput: TypeAlias = Union[
    structure_and_binding_start_params.InputBond,
    Bond,
]
PredictionConstraintInput: TypeAlias = Union[
    structure_and_binding_start_params.InputConstraint,
    PocketConstraint,
    ContactConstraint,
]
PredictionModelOptionsInput: TypeAlias = Union[
    structure_and_binding_start_params.InputModelOptions,
    ModelOptions,
]
PredictionTemplateInput: TypeAlias = structure_and_binding_start_params.InputTemplate


def normalize_prediction_request(
    *,
    entities: Iterable[PredictionEntityInput],
    model: PredictionModelInput,
    binding: PredictionBindingInput | None = None,
    bonds: Iterable[PredictionBondInput] | None = None,
    constraints: Iterable[PredictionConstraintInput] | None = None,
    model_options: PredictionModelOptionsInput | None = None,
    num_samples: int | None = None,
    templates: Iterable[PredictionTemplateInput] | None = None,
) -> structure_and_binding_start_params.StructureAndBindingStartParams:
    input_payload: structure_and_binding_start_params.Input = {
        "entities": cast(Iterable[structure_and_binding_start_params.InputEntity], _realize_value(entities))
    }
    if binding is not None:
        input_payload["binding"] = cast(structure_and_binding_start_params.InputBinding, _realize_value(binding))
    if bonds is not None:
        input_payload["bonds"] = cast(Iterable[structure_and_binding_start_params.InputBond], _realize_value(bonds))
    if constraints is not None:
        input_payload["constraints"] = cast(
            Iterable[structure_and_binding_start_params.InputConstraint],
            _realize_value(constraints),
        )
    if model_options is not None:
        input_payload["model_options"] = cast(
            structure_and_binding_start_params.InputModelOptions,
            _realize_value(model_options),
        )
    if num_samples is not None:
        input_payload["num_samples"] = num_samples
    if templates is not None:
        input_payload["templates"] = cast(
            Iterable[structure_and_binding_start_params.InputTemplate],
            _realize_value(templates),
        )

    return {
        "input": input_payload,
        "model": cast(Literal["boltz-2.1"], _realize_value(model)),
    }


def normalize_protein_design_request(
    *,
    binder_specification: ProteinDesignBinderSpecificationInput,
    num_proteins: int,
    target: ProteinDesignTargetInput,
) -> protein_design_start_params.ProteinDesignRunInput:
    return {
        "binder_specification": _normalize_protein_design_binder_specification(binder_specification),
        "num_proteins": num_proteins,
        "target": _normalize_protein_design_target(target),
    }


def normalize_protein_library_screen_request(
    *,
    proteins: Iterable[protein_library_screen_start_params.Protein],
    target: ProteinLibraryScreenTargetInput,
) -> protein_library_screen_start_params.LibraryScreenStartParams:
    return {
        "proteins": cast(Iterable[protein_library_screen_start_params.Protein], _realize_value(proteins)),
        "target": _normalize_protein_library_screen_target(target),
    }


def normalize_small_molecule_design_request(
    *,
    num_molecules: int,
    target: small_molecule_design_start_params.Target,
    chemical_space: Literal["enamine_real"] | None = None,
    molecule_filters: small_molecule_design_start_params.MoleculeFilters | None = None,
) -> small_molecule_design_start_params.DesignStartParams:
    payload: small_molecule_design_start_params.DesignStartParams = {
        "num_molecules": num_molecules,
        "target": cast(small_molecule_design_start_params.Target, _realize_value(target)),
    }
    if chemical_space is not None:
        payload["chemical_space"] = chemical_space
    if molecule_filters is not None:
        payload["molecule_filters"] = cast(
            small_molecule_design_start_params.MoleculeFilters,
            _realize_value(molecule_filters),
        )
    return payload


def normalize_small_molecule_library_screen_request(
    *,
    molecules: Iterable[small_molecule_library_screen_start_params.Molecule],
    target: small_molecule_library_screen_start_params.Target,
    molecule_filters: small_molecule_library_screen_start_params.MoleculeFilters | None = None,
) -> small_molecule_library_screen_start_params.LibraryScreenStartParams:
    payload: small_molecule_library_screen_start_params.LibraryScreenStartParams = {
        "molecules": cast(
            Iterable[small_molecule_library_screen_start_params.Molecule],
            _realize_value(molecules),
        ),
        "target": cast(small_molecule_library_screen_start_params.Target, _realize_value(target)),
    }
    if molecule_filters is not None:
        payload["molecule_filters"] = cast(
            small_molecule_library_screen_start_params.MoleculeFilters,
            _realize_value(molecule_filters),
        )
    return payload


def _normalize_protein_design_binder_specification(
    binder_specification: ProteinDesignBinderSpecificationInput,
) -> protein_design_start_params.ProteinDesignRunInputBinderSpecification:
    return cast(
        protein_design_start_params.ProteinDesignRunInputBinderSpecification,
        _normalize_structure_template_mapping(
            payload=cast(Mapping[str, object], binder_specification),
            missing_message="Structure template binder specifications must include a `structure` source",
        ),
    )


def _normalize_protein_design_target(
    target: ProteinDesignTargetInput,
) -> protein_design_start_params.ProteinDesignRunInputTarget:
    return cast(
        protein_design_start_params.ProteinDesignRunInputTarget,
        _normalize_structure_template_mapping(
            payload=cast(Mapping[str, object], target),
            missing_message="Structure template targets must include a `structure` source",
        ),
    )


def _normalize_protein_library_screen_target(
    target: ProteinLibraryScreenTargetInput,
) -> protein_library_screen_start_params.Target:
    return cast(
        protein_library_screen_start_params.Target,
        _normalize_structure_template_mapping(
            payload=cast(Mapping[str, object], target),
            missing_message="Structure template targets must include a `structure` source",
        ),
    )


def _normalize_structure_template_mapping(
    *,
    payload: Mapping[str, object],
    missing_message: str,
) -> dict[str, object]:
    normalized_payload = _realize_mapping(payload)
    if normalized_payload.get("type") != "structure_template":
        return normalized_payload

    normalized_payload["structure"] = _normalize_structure_source(
        source=normalized_payload.get("structure"),
        missing_message=missing_message,
    )
    return normalized_payload


def _normalize_structure_source(
    *,
    source: object,
    missing_message: str,
) -> NormalizedStructureSource:
    if isinstance(source, Mapping):
        normalized = _realize_mapping(cast(Mapping[str, object], source))
        source_type = normalized.get("type")
        if source_type == "url":
            url = normalized.get("url")
            if not isinstance(url, str):
                raise ValueError("Structure URL sources must include a string `url` value")
            return cast(NormalizedStructureSource, {"type": "url", "url": url})

        if source_type == "base64":
            data = normalized.get("data")
            media_type = normalized.get("media_type")
            if not isinstance(data, str) or not isinstance(media_type, str):
                raise ValueError("Base64 structure sources must include string `data` and `media_type` values")
            if media_type != "chemical/x-cif":
                raise ValueError("Base64 structure sources must set `media_type` to `chemical/x-cif`")
            return cast(
                NormalizedStructureSource,
                {
                    "type": "base64",
                    "media_type": media_type,
                    "data": data,
                },
            )

        raise ValueError("Unsupported structure source mapping; expected `type` to be `url` or `base64`")

    if isinstance(source, (str, PathLike)):
        path = Path(cast(Union[str, PathLike[str]], source)).expanduser()
        if not path.is_file():
            raise ExperimentError(f"Local CIF structure file does not exist: {path}")

        if path.suffix.lower() == ".pdb":
            raise ExperimentError("Local PDB structure paths are not supported in v1; use a CIF file instead")
        if path.suffix.lower() not in {".cif", ".mmcif"}:
            raise ExperimentError(
                "Only local CIF structure paths are supported in v1; pass an explicit URL/base64 source otherwise"
            )

        return cast(
            NormalizedStructureSource,
            {
                "type": "base64",
                "media_type": "chemical/x-cif",
                "data": base64.b64encode(path.read_bytes()).decode("ascii"),
            },
        )

    if source is None:
        raise ValueError(missing_message)
    raise ValueError("Unsupported structure source value")


def _realize_mapping(value: Mapping[str, object]) -> dict[str, object]:
    return {str(key): _realize_value(item) for key, item in value.items()}


def _realize_value(value: object) -> object:
    if isinstance(value, Enum):
        return value.value

    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        return _realize_value(to_dict())

    if isinstance(value, Mapping):
        return _realize_mapping(cast(Mapping[str, object], value))

    if isinstance(value, PathLike):
        return Path(cast(PathLike[str], value))

    if isinstance(value, (str, bytes, bytearray)) or value is None:
        return value

    if isinstance(value, Iterable):
        return [_realize_value(item) for item in cast(Iterable[object], value)]

    return value
