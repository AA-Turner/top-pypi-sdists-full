from __future__ import annotations

from enum import Enum
from typing import Protocol, cast
from dataclasses import dataclass
from collections.abc import Mapping, Iterable, Sequence
from typing_extensions import Literal, override

__all__ = [
    "Base64Source",
    "CcdModification",
    "DNA",
    "RNA",
    "Bond",
    "Protein",
    "BoltzModel",
    "CustomMsa",
    "EmptyMsa",
    "LigandCcd",
    "LigandAtom",
    "MsaFormat",
    "ModelOptions",
    "LigandSmiles",
    "PolymerAtom",
    "LigandContact",
    "PipelineStatus",
    "PolymerContact",
    "PredictionStatus",
    "ContactConstraint",
    "PocketConstraint",
    "ProteinModification",
    "URLSource",
    "LigandProteinBinding",
    "ProteinProteinBinding",
]


class _StringEnum(str, Enum):
    @override
    def __str__(self) -> str:
        return cast(str, self.value)


class BoltzModel(_StringEnum):
    """Structure-and-binding model identifiers."""

    BOLTZ_2_1 = "boltz-2.1"


class PredictionStatus(_StringEnum):
    """Terminal and non-terminal status values for structure-and-binding predictions."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class PipelineStatus(_StringEnum):
    """Terminal and non-terminal status values for pipeline runs."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    STOPPED = "stopped"


class MsaFormat(_StringEnum):
    """Supported custom MSA file formats."""

    A3M = "a3m"
    CSV = "csv"


@dataclass(frozen=True)
class URLSource:
    """Remote HTTPS file source."""

    url: str

    def to_dict(self) -> dict[str, object]:
        return {
            "type": "url",
            "url": self.url,
        }


@dataclass(frozen=True)
class Base64Source:
    """Inline base64-encoded file source."""

    data: str
    media_type: str

    def to_dict(self) -> dict[str, object]:
        return {
            "type": "base64",
            "data": self.data,
            "media_type": self.media_type,
        }


@dataclass(frozen=True)
class CcdModification:
    """Residue or nucleotide modification identified by CCD code."""

    residue_index: int
    value: str

    def to_dict(self) -> dict[str, object]:
        return {
            "type": "ccd",
            "residue_index": self.residue_index,
            "value": self.value,
        }


ProteinModification = CcdModification


@dataclass(frozen=True)
class CustomMsa:
    """User-provided MSA for a protein entity."""

    format: Literal["a3m", "csv"] | MsaFormat
    source: URLSource | Base64Source | Mapping[str, object]

    def to_dict(self) -> dict[str, object]:
        return {
            "type": "custom",
            "format": _serialize_value(self.format),
            "source": _serialize_value(self.source),
        }


@dataclass(frozen=True)
class EmptyMsa:
    """Single-sequence mode without automatic MSA generation."""

    def to_dict(self) -> dict[str, object]:
        return {"type": "empty"}


@dataclass(frozen=True)
class Protein:
    """Protein entity in a structure-and-binding prediction."""

    value: str
    chain_ids: Sequence[str]
    cyclic: bool | None = None
    modifications: Iterable[CcdModification | Mapping[str, object]] | None = None
    msa: CustomMsa | EmptyMsa | Mapping[str, object] | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "chain_ids", _tuple_not_str(self.chain_ids, field_name="chain_ids"))
        if self.modifications is not None:
            object.__setattr__(self, "modifications", tuple(self.modifications))

    def to_dict(self) -> dict[str, object]:
        return _clean_dict(
            {
                "type": "protein",
                "value": self.value,
                "chain_ids": self.chain_ids,
                "cyclic": self.cyclic,
                "modifications": self.modifications,
                "msa": self.msa,
            }
        )


@dataclass(frozen=True)
class RNA:
    """RNA entity in a structure-and-binding prediction."""

    value: str
    chain_ids: Sequence[str]
    cyclic: bool | None = None
    modifications: Iterable[CcdModification | Mapping[str, object]] | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "chain_ids", _tuple_not_str(self.chain_ids, field_name="chain_ids"))
        if self.modifications is not None:
            object.__setattr__(self, "modifications", tuple(self.modifications))

    def to_dict(self) -> dict[str, object]:
        return _clean_dict(
            {
                "type": "rna",
                "value": self.value,
                "chain_ids": self.chain_ids,
                "cyclic": self.cyclic,
                "modifications": self.modifications,
            }
        )


@dataclass(frozen=True)
class DNA:
    """DNA entity in a structure-and-binding prediction."""

    value: str
    chain_ids: Sequence[str]
    cyclic: bool | None = None
    modifications: Iterable[CcdModification | Mapping[str, object]] | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "chain_ids", _tuple_not_str(self.chain_ids, field_name="chain_ids"))
        if self.modifications is not None:
            object.__setattr__(self, "modifications", tuple(self.modifications))

    def to_dict(self) -> dict[str, object]:
        return _clean_dict(
            {
                "type": "dna",
                "value": self.value,
                "chain_ids": self.chain_ids,
                "cyclic": self.cyclic,
                "modifications": self.modifications,
            }
        )


@dataclass(frozen=True)
class LigandCcd:
    """Ligand entity referenced by CCD code."""

    value: str
    chain_ids: Sequence[str]

    def __post_init__(self) -> None:
        object.__setattr__(self, "chain_ids", _tuple_not_str(self.chain_ids, field_name="chain_ids"))

    def to_dict(self) -> dict[str, object]:
        return {
            "type": "ligand_ccd",
            "value": self.value,
            "chain_ids": _serialize_value(self.chain_ids),
        }


@dataclass(frozen=True)
class LigandSmiles:
    """Ligand entity represented by a SMILES string."""

    value: str
    chain_ids: Sequence[str]

    def __post_init__(self) -> None:
        object.__setattr__(self, "chain_ids", _tuple_not_str(self.chain_ids, field_name="chain_ids"))

    def to_dict(self) -> dict[str, object]:
        return {
            "type": "ligand_smiles",
            "value": self.value,
            "chain_ids": _serialize_value(self.chain_ids),
        }


@dataclass(frozen=True)
class LigandProteinBinding:
    """Score binding between one ligand chain and the protein complex."""

    binder_chain_id: str

    def to_dict(self) -> dict[str, object]:
        return {
            "type": "ligand_protein_binding",
            "binder_chain_id": self.binder_chain_id,
        }


@dataclass(frozen=True)
class ProteinProteinBinding:
    """Score binding for one or more protein binder chains."""

    binder_chain_ids: Sequence[str]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "binder_chain_ids", _tuple_not_str(self.binder_chain_ids, field_name="binder_chain_ids")
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "type": "protein_protein_binding",
            "binder_chain_ids": _serialize_value(self.binder_chain_ids),
        }


@dataclass(frozen=True)
class LigandAtom:
    chain_id: str
    atom_name: str

    def to_dict(self) -> dict[str, object]:
        return {
            "type": "ligand_atom",
            "chain_id": self.chain_id,
            "atom_name": self.atom_name,
        }


@dataclass(frozen=True)
class PolymerAtom:
    chain_id: str
    residue_index: int
    atom_name: str

    def to_dict(self) -> dict[str, object]:
        return {
            "type": "polymer_atom",
            "chain_id": self.chain_id,
            "residue_index": self.residue_index,
            "atom_name": self.atom_name,
        }


@dataclass(frozen=True)
class Bond:
    atom1: LigandAtom | PolymerAtom | Mapping[str, object]
    atom2: LigandAtom | PolymerAtom | Mapping[str, object]

    def to_dict(self) -> dict[str, object]:
        return {
            "atom1": _serialize_value(self.atom1),
            "atom2": _serialize_value(self.atom2),
        }


@dataclass(frozen=True)
class PolymerContact:
    chain_id: str
    residue_index: int

    def to_dict(self) -> dict[str, object]:
        return {
            "type": "polymer_contact",
            "chain_id": self.chain_id,
            "residue_index": self.residue_index,
        }


@dataclass(frozen=True)
class LigandContact:
    chain_id: str
    atom_name: str

    def to_dict(self) -> dict[str, object]:
        return {
            "type": "ligand_contact",
            "chain_id": self.chain_id,
            "atom_name": self.atom_name,
        }


@dataclass(frozen=True)
class PocketConstraint:
    binder_chain_id: str
    contact_residues: Mapping[str, Iterable[int]]
    max_distance_angstrom: float
    force: bool | None = None

    def to_dict(self) -> dict[str, object]:
        return _clean_dict(
            {
                "type": "pocket",
                "binder_chain_id": self.binder_chain_id,
                "contact_residues": self.contact_residues,
                "max_distance_angstrom": self.max_distance_angstrom,
                "force": self.force,
            }
        )


@dataclass(frozen=True)
class ContactConstraint:
    token1: PolymerContact | LigandContact | Mapping[str, object]
    token2: PolymerContact | LigandContact | Mapping[str, object]
    max_distance_angstrom: float
    force: bool | None = None

    def to_dict(self) -> dict[str, object]:
        return _clean_dict(
            {
                "type": "contact",
                "token1": self.token1,
                "token2": self.token2,
                "max_distance_angstrom": self.max_distance_angstrom,
                "force": self.force,
            }
        )


@dataclass(frozen=True)
class ModelOptions:
    recycling_steps: int | None = None
    sampling_steps: int | None = None
    step_scale: float | None = None

    def to_dict(self) -> dict[str, object]:
        return _clean_dict(
            {
                "recycling_steps": self.recycling_steps,
                "sampling_steps": self.sampling_steps,
                "step_scale": self.step_scale,
            }
        )


class _ToDict(Protocol):
    def to_dict(self) -> dict[str, object]: ...


def _clean_dict(data: Mapping[str, object | None]) -> dict[str, object]:
    return {key: _serialize_value(value) for key, value in data.items() if value is not None}


def _serialize_value(value: object) -> object:
    if isinstance(value, Enum):
        return value.value

    if hasattr(value, "to_dict"):
        return cast(_ToDict, value).to_dict()

    if isinstance(value, Mapping):
        mapping = cast(Mapping[object, object], value)
        return {str(key): _serialize_value(item) for key, item in mapping.items()}

    if isinstance(value, (str, bytes, bytearray)) or value is None:
        return value

    if isinstance(value, Iterable):
        return [_serialize_value(item) for item in cast(Iterable[object], value)]

    return value


def _tuple_not_str(values: Sequence[str], *, field_name: str) -> tuple[str, ...]:
    if isinstance(values, str):
        raise ValueError(f"`{field_name}` must be a sequence of strings, not a string")
    return tuple(values)
