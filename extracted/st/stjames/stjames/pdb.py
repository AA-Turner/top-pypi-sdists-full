"""PDB structure models and serialization helpers."""

from datetime import date
from pathlib import Path
from typing import Any, Literal, NamedTuple

from pydantic import BaseModel, ConfigDict, Field, field_validator

import stjames.atomium_stjames as astj

from .atomium_stjames.mmcif import mmcif_dict_to_data_dict, mmcif_string_to_mmcif_dict
from .atomium_stjames.pdb import pdb_dict_to_data_dict, pdb_string_to_pdb_dict
from .types import Matrix3x3, Vector3D

# pdb_writer imports from this module, so this re-export must stay after the class definitions.
# The noqa suppresses E402 (not at top of file) and PLC0414 (aliased to same name, needed for re-export).


# Mostly for testing purposes
EXTRA: Literal["allow", "ignore", "forbid"] = "allow"


class PDBAtom(BaseModel):
    """An atom within a residue."""

    model_config = ConfigDict(extra=EXTRA)

    x: float
    y: float
    z: float
    element: str
    name: str | None = None
    charge: float | None = None
    occupancy: float | None = None
    alt_loc: str | None = None
    anisotropy: list[float | None] | None = None
    bvalue: float | None = None
    is_hetatm: bool | None = None


class PDBWater(BaseModel):
    """A water molecule."""

    model_config = ConfigDict(extra=EXTRA)

    name: str | None = None
    full_name: str | None = None
    atoms: dict[int, PDBAtom] = {}
    internal_id: str | None = None
    polymer: str


class PDBResidue(BaseModel):
    """Residue within a polymer chain."""

    model_config = ConfigDict(extra=EXTRA)

    name: str | None = None
    full_name: str | None = None
    atoms: dict[int, PDBAtom] = {}
    number: int


class PDBPolymer(BaseModel):
    """A polymer chain."""

    model_config = ConfigDict(extra=EXTRA)

    internal_id: str
    helices: list[list[str]] = []
    residues: dict[str, PDBResidue] = {}
    sequence: str | None = None
    strands: list[list[str]] = []


class PDBNonPolymer(BaseModel):
    """Non-polymeric molecules/atoms (e.g. ions and ligands)."""

    model_config = ConfigDict(extra=EXTRA)

    name: str
    full_name: str | None = None
    atoms: dict[int, PDBAtom]
    internal_id: str
    polymer: str


class _PDBAtomRecord(NamedTuple):
    """Atom with its canonical serialized PDB context."""

    serial: int
    atom: PDBAtom
    chain_id: str
    residue_name: str
    residue_number: str
    alt_loc: str
    entity_type: Literal["polymer", "non_polymer", "water", "branched"]

    @property
    def is_polymer(self) -> bool:
        """Whether this is a polymer atom record."""
        return self.entity_type == "polymer"


class ResidueRef(NamedTuple):
    """Address of one residue, spanning every entity type in a PDBModel."""

    entity_type: Literal["polymer", "non_polymer", "water", "branched"]
    key: str
    residue_key: str | None = None


class PDBModel(BaseModel):
    """Structure data."""

    model_config = ConfigDict(extra=EXTRA)

    polymer: dict[str, PDBPolymer] = {}
    non_polymer: dict[str, PDBNonPolymer] = {}
    branched: dict[str, Any] = {}
    water: dict[str, PDBWater] = {}
    connections: list[list[int]] = []

    @field_validator("branched")
    @classmethod
    def validate_branched_atoms(cls, branched: dict[str, Any]) -> dict[str, Any]:
        """Restore typed atom mappings while retaining branched metadata."""
        return {
            key: {**entity, "atoms": {int(serial): PDBAtom.model_validate(atom) for serial, atom in entity["atoms"].items()}}
            if isinstance(entity, dict) and "atoms" in entity
            else entity
            for key, entity in branched.items()
        }

    def all_residue_refs(self) -> list[ResidueRef]:
        """Return every atom-bearing residue ordered by its lowest atom ID.

        The resulting 0-based indices span polymers, non-polymers, waters, and
        branched entities.

        :return: residue references sorted by lowest atom ID
        """
        refs_by_serial: list[tuple[int, ResidueRef]] = []

        for chain_key, polymer in self.polymer.items():
            for res_key, residue in polymer.residues.items():
                if residue.atoms:
                    refs_by_serial.append((min(residue.atoms), ResidueRef("polymer", chain_key, res_key)))

        for key, non_polymer in self.non_polymer.items():
            if non_polymer.atoms:
                refs_by_serial.append((min(non_polymer.atoms), ResidueRef("non_polymer", key)))

        for key, water in self.water.items():
            if water.atoms:
                refs_by_serial.append((min(water.atoms), ResidueRef("water", key)))

        for key, branched in self.branched.items():
            if isinstance(branched, dict) and branched.get("atoms"):
                refs_by_serial.append((min(int(atom_id) for atom_id in branched["atoms"]), ResidueRef("branched", key)))

        refs_by_serial.sort(key=lambda pair: pair[0])
        return [ref for _, ref in refs_by_serial]

    def residue_atoms(self, ref: ResidueRef) -> dict[int, PDBAtom]:
        """Return the atoms of the residue addressed by ref.

        :param ref: residue reference, as returned by all_residue_refs
        :return: mapping of atom serial to atom
        :raises ValueError: if a polymer ref is missing its residue_key
        """
        if ref.entity_type == "polymer":
            if ref.residue_key is None:
                raise ValueError("polymer residue ref must include residue_key")
            return self.polymer[ref.key].residues[ref.residue_key].atoms
        if ref.entity_type == "non_polymer":
            return self.non_polymer[ref.key].atoms
        if ref.entity_type == "water":
            return self.water[ref.key].atoms
        if ref.entity_type == "branched":
            branched = self.branched[ref.key]
            return branched.get("atoms", {}) if isinstance(branched, dict) else {}
        raise ValueError(f"Unknown residue entity type: {ref.entity_type!r}")

    def _atom_records(self) -> list[_PDBAtomRecord]:
        """Build atom records in canonical serialized PDB order."""
        records: list[_PDBAtomRecord] = []

        for chain_id, polymer in self.polymer.items():
            serialized_chain_id = polymer.internal_id or chain_id
            for residue_id, residue in polymer.residues.items():
                residue_number = residue_id.split(".", 1)[1] if "." in residue_id else residue_id
                for serial, atom in residue.atoms.items():
                    records.append(
                        _PDBAtomRecord(
                            int(serial),
                            atom,
                            serialized_chain_id,
                            residue.name or "UNK",
                            residue_number,
                            atom.alt_loc or "",
                            "polymer",
                        )
                    )

        for residue_id, non_polymer in self.non_polymer.items():
            chain_id = non_polymer.polymer or "Z"
            residue_number = residue_id.split(".", 1)[1] if "." in residue_id else residue_id
            for serial, atom in non_polymer.atoms.items():
                records.append(
                    _PDBAtomRecord(
                        int(serial),
                        atom,
                        chain_id,
                        non_polymer.name,
                        residue_number,
                        "",
                        "non_polymer",
                    )
                )

        for residue_id, water in self.water.items():
            chain_id = residue_id.split(".")[0] if "." in residue_id else residue_id[0]
            residue_number = residue_id.split(".", 1)[1] if "." in residue_id else residue_id
            for serial, atom in water.atoms.items():
                records.append(_PDBAtomRecord(int(serial), atom, chain_id, "HOH", residue_number, "", "water"))

        for branched in self.branched.values():
            if isinstance(branched, dict) and "atoms" in branched:
                for serial, atom in branched["atoms"].items():
                    records.append(_PDBAtomRecord(int(serial), atom, "B", "BRN", "1", "", "branched"))

        records.sort(key=lambda record: record.serial)
        return records


class PDBTransformations(BaseModel):
    """Transformations applied to the structure."""

    model_config = ConfigDict(extra=EXTRA)

    chains: list[str]
    matrix: Matrix3x3
    vector: Vector3D


class PDBAssembly(BaseModel):
    """How the structure was assembled."""

    model_config = ConfigDict(extra=EXTRA)

    transformations: list[PDBTransformations]
    software: str | None = None
    buried_surface_area: float | None = None
    surface_area: float | None = None
    delta_energy: float | None = None
    id: int


class PDBCrystallography(BaseModel):
    """Crystallography related information."""

    model_config = ConfigDict(extra=EXTRA)

    space_group: str | None = None
    unit_cell: list[float] | None = None


class PDBGeometry(BaseModel):
    """Details of the geometry."""

    model_config = ConfigDict(extra=EXTRA)

    assemblies: list[PDBAssembly] = []
    crystallography: PDBCrystallography = Field(default_factory=PDBCrystallography)


class PDBQuality(BaseModel):
    """Quality metrics."""

    model_config = ConfigDict(extra=EXTRA)

    resolution: float | None = None
    rfree: float | None = None
    rvalue: float | None = None


class PDBMissingResidue(BaseModel):
    """Residue missing from PDB structure."""

    model_config = ConfigDict(extra=EXTRA)

    name: str
    id: str


class PDBExperiment(BaseModel):
    """Details of the experiment."""

    model_config = ConfigDict(extra=EXTRA)

    expression_system: str | None = None
    missing_residues: list[PDBMissingResidue] = []
    source_organism: str | None = None
    technique: str | None = None


class PDBDescription(BaseModel):
    """A description of the molecule."""

    model_config = ConfigDict(extra=EXTRA)

    code: str | None = None
    title: str | None = None
    authors: list[str] = []
    classification: str | None = None
    deposition_date: str | None = None
    keywords: list[str] = []

    @field_validator("deposition_date", mode="before")
    @classmethod
    def date_to_string(cls, v: str | date | None) -> str | None:
        if v is None:
            return v

        if isinstance(v, date):
            return v.isoformat()

        return str(v)


class PDB(BaseModel):
    """A PDB formatted file."""

    model_config = ConfigDict(extra=EXTRA)

    description: PDBDescription
    experiment: PDBExperiment
    geometry: PDBGeometry
    models: list[PDBModel] = []
    quality: PDBQuality = Field(default_factory=PDBQuality)

    def get_atom_index(
        self,
        chain: str,
        residue: int | str,
        atom: str,
        *,
        entity_type: Literal["polymer", "non_polymer", "water", "branched"] | None = None,
        model_index: int = 0,
    ) -> int:
        """Return an atom's zero-based position in serialized PDB atom-record order.

        :param chain: chain ID
        :param residue: residue number, optionally including an insertion code
        :param atom: atom name, such as `SG` or `C1`
        :param entity_type: entity collection to search
        :param model_index: zero-based model index
        :return: zero-based atom index used by workflows consuming PDB atom order
        :raises ValueError: if the model, residue, or atom cannot be identified uniquely
        """
        if model_index < 0 or model_index >= len(self.models):
            raise ValueError(f"Model index {model_index} not found.")
        model = self.models[model_index]

        residue_number = str(residue)
        records = model._atom_records()
        residue_records = [
            (index, record)
            for index, record in enumerate(records)
            if record.chain_id == chain and record.residue_number == residue_number and (entity_type is None or record.entity_type == entity_type)
        ]
        residue_id = f"{chain}.{residue_number}"
        if not residue_records:
            location = f" in {entity_type}" if entity_type is not None else ""
            raise ValueError(f"Residue {residue_id} not found{location}.")
        atom_matches = [index for index, record in residue_records if (record.atom.name or record.atom.element) == atom]
        if not atom_matches:
            raise ValueError(f"Atom {atom} not found in residue {residue_id}.")
        if len(atom_matches) > 1:
            raise ValueError(f"Atom {atom} is ambiguous in residue {residue_id}; provide entity_type.")
        return atom_matches[0]


def read_pdb(path: Path | str) -> PDB:
    """Read a pdb located at path."""
    return PDB.model_validate(astj.open(str(path), data_dict=True))


def fetch_pdb(code: str) -> PDB:
    """Fetch a pdb from the Protein Data Bank."""
    return PDB.model_validate(astj.fetch(code, data_dict=True))


def fetch_pdb_from_mmcif(code: str) -> PDB:
    """Fetch a pdb from the Protein Data Bank."""
    code += ".cif"
    return PDB.model_validate(astj.fetch(code, data_dict=True))


def pdb_from_pdb_filestring(pdb: str) -> PDB:
    """Read a PDB from a string."""
    return PDB.model_validate(pdb_dict_to_data_dict(pdb_string_to_pdb_dict(pdb)))


def pdb_from_mmcif_filestring(pdb: str) -> PDB:
    """Read a PDB from a string."""
    return PDB.model_validate(mmcif_dict_to_data_dict(mmcif_string_to_mmcif_dict(pdb)))


# pdb_writer and mmcif_writer import from this module, so these re-exports must follow all class definitions.
from .atomium_stjames.mmcif_writer import pdb_object_to_mmcif_filestring as pdb_object_to_mmcif_filestring  # noqa: E402, PLC0414
from .atomium_stjames.pdb_writer import pdb_object_to_pdb_filestring as pdb_object_to_pdb_filestring  # noqa: E402, PLC0414
