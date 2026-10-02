"""Functions for writing PDB objects to .cif (mmCIF) format strings."""

import difflib
import re
from collections.abc import Iterator
from typing import Any, NamedTuple

from ..pdb import PDB, PDBAtom, PDBModel, PDBPolymer
from .data import CODES

_REVERSE_CODES = {v: k for k, v in CODES.items()}

# Letters that appear exclusively in amino acid sequences (not nucleotides)
_PROTEIN_ONLY_LETTERS: frozenset[str] = frozenset("DEFHIKLMNPQRVWY")


def _infer_polymer_type(seq: str) -> str:
    """
    Infer the mmCIF entity_poly.type value from a one-letter code sequence.

    :param seq: one-letter code sequence string
    :return: mmCIF polymer type string
    """
    letters = set(seq.upper())
    if letters & _PROTEIN_ONLY_LETTERS:
        return "polypeptide(L)"
    if "U" in letters:
        return "polyribonucleotide"
    if "T" in letters:
        return "polydeoxyribonucleotide"
    return "polypeptide(L)"


def _compute_label_seq_ids(polymer: PDBPolymer) -> dict[str, int]:
    """
    Align observed residues to the full entity sequence and return a mapping
    of residue_id to 1-based position in the full sequence (label_seq_id).

    Falls back to sequential numbering when no full sequence is available.

    :param polymer: polymer chain to process
    :return: mapping of residue_id to label_seq_id
    """
    residue_ids = list(polymer.residues.keys())
    if not polymer.sequence:
        return {rid: i for i, rid in enumerate(residue_ids, start=1)}

    obs_one_letter = [CODES.get(res.name or "", "X") for res in polymer.residues.values()]
    full_seq = list(polymer.sequence)

    matcher = difflib.SequenceMatcher(None, obs_one_letter, full_seq, autojunk=False)
    result: dict[str, int] = {}
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for obs_idx, full_idx in zip(range(i1, i2), range(j1, j2), strict=True):
                result[residue_ids[obs_idx]] = full_idx + 1

    # Fill any unmatched observed residues with sequential fallback
    counter = max(result.values(), default=0) + 1
    for rid in residue_ids:
        if rid not in result:
            result[rid] = counter
            counter += 1

    return result


def _cif_value(v: Any) -> str:
    """
    Format a value for inclusion in a mmCIF table cell.

    :param v: value to format
    :return: mmCIF-safe string representation
    """
    if v is None:
        return "?"
    s = str(v)
    if not s or " " in s or s[0] in ('"', "'", "_"):
        return f'"{s}"'
    return s


def _format_formal_charge(charge: float | None) -> str:
    """Format atom formal charge as an mmCIF integer or unknown value."""
    if charge is None:
        return "?"
    if not float(charge).is_integer():
        raise ValueError(f"mmCIF formal charge must be an integer, got {charge}")
    return str(int(charge))


def _assign_missing_asym_ids(pdb: PDB) -> PDB:
    """Assign stable label IDs without copying atoms or changing author IDs."""
    used_ids = {
        identifier
        for model in pdb.models
        for collection in (model.polymer, model.non_polymer, model.water)
        for entity in collection.values()
        if (identifier := entity.internal_id) and identifier.strip()
    }
    # Polymer and water author IDs can also be used as label IDs by the writer.
    for model in pdb.models:
        used_ids.update(model.polymer)
        used_ids.update(water.polymer for water in model.water.values())
        used_ids.update(entry.get("internal_id", "") for entry in model.branched.values() if isinstance(entry, dict))
    assigned: dict[tuple[str, str], str] = {}
    # Reuse a label already present for the same entity in any model.
    for model in pdb.models:
        for kind, collection in (("polymer", model.polymer), ("non_polymer", model.non_polymer), ("water", model.water)):
            for key, entity in collection.items():
                if entity.internal_id and entity.internal_id.strip():
                    assigned.setdefault((kind, key), entity.internal_id)
    next_index = 1

    def label_id(kind: str, key: str, original: str | None) -> str:
        nonlocal next_index
        if original and original.strip():
            return original
        identity = (kind, key)
        if identity not in assigned:
            while (candidate := f"STJAMESASYM{next_index}") in used_ids:
                next_index += 1
            assigned[identity] = candidate
            used_ids.add(candidate)
            next_index += 1
        return assigned[identity]

    models = [
        model.model_copy(
            update={
                kind: {key: entity.model_copy(update={"internal_id": label_id(kind, key, entity.internal_id)}) for key, entity in collection.items()}
                for kind, collection in (("polymer", model.polymer), ("non_polymer", model.non_polymer), ("water", model.water))
            }
        )
        for model in pdb.models
    ]
    return pdb.model_copy(update={"models": models})


def _collect_entities(model: PDBModel) -> tuple[dict[str, str], dict[str, str]]:
    """
    Build entity_id → type and label_asym_id → entity_id mappings from a model.

    Chains sharing the same sequence are grouped under a single entity, matching
    the mmCIF convention used by the PDB.

    :param model: PDB model to inspect
    :return: tuple of (types map, asym-to-entity map)
    """
    asym_to_entity: dict[str, str] = {}
    types: dict[str, str] = {}
    seq_to_entity: dict[str, str] = {}
    counter = 1

    for chain_id, polymer in model.polymer.items():
        asym_id = polymer.internal_id or chain_id
        if asym_id not in asym_to_entity:
            seq = polymer.sequence or ""
            if seq and seq in seq_to_entity:
                eid = seq_to_entity[seq]
            else:
                eid = str(counter)
                types[eid] = "polymer"
                counter += 1
                if seq:
                    seq_to_entity[seq] = eid
            asym_to_entity[asym_id] = eid

    for _np_id, nonpoly in model.non_polymer.items():
        asym_id = nonpoly.internal_id
        if asym_id not in asym_to_entity:
            eid = str(counter)
            asym_to_entity[asym_id] = eid
            types[eid] = "non-polymer"
            counter += 1

    for _w_id, water in model.water.items():
        asym_id = water.internal_id
        if asym_id and asym_id not in asym_to_entity:
            eid = str(counter)
            asym_to_entity[asym_id] = eid
            types[eid] = "water"
            counter += 1

    for _b_id, branched in model.branched.items():
        asym_id = branched.get("internal_id") if isinstance(branched, dict) else None
        if asym_id and asym_id not in asym_to_entity:
            eid = str(counter)
            asym_to_entity[asym_id] = eid
            types[eid] = "branched"
            counter += 1

    return types, asym_to_entity


def _format_atom_row(
    atom_id: int,
    atom: PDBAtom,
    group: str,
    label_asym_id: str,
    auth_asym_id: str,
    comp_id: str,
    auth_seq_id: str,
    ins_code: str,
    model_num: int,
    entity_id: str = "?",
    seq_id: str = ".",
) -> list[str]:
    """
    Build the column values for a single atom_site row.

    :param atom_id: atom serial number
    :param atom: PDBAtom object
    :param group: ATOM or HETATM
    :param label_asym_id: internal chain identifier
    :param auth_asym_id: author chain identifier
    :param comp_id: residue/component name
    :param auth_seq_id: author sequence number string
    :param ins_code: insertion code (empty string or single char)
    :param model_num: model number (1-based)
    :param entity_id: entity ID from the entity table
    :param seq_id: 1-based residue index within the chain, or "." for non-polymers
    :return: list of cell values in atom_site column order
    """
    name = atom.name if atom.name else atom.element
    alt_loc = atom.alt_loc if atom.alt_loc else "."
    occupancy = atom.occupancy if atom.occupancy is not None else 1.0
    bvalue = atom.bvalue if atom.bvalue is not None else 0.0
    charge = _format_formal_charge(atom.charge)
    pdb_ins = ins_code if ins_code else "?"

    return [
        group,
        str(atom_id),
        atom.element,
        _cif_value(name),
        alt_loc,
        _cif_value(comp_id),
        _cif_value(label_asym_id),
        entity_id,
        seq_id,
        pdb_ins,
        f"{atom.x:.3f}",
        f"{atom.y:.3f}",
        f"{atom.z:.3f}",
        f"{occupancy:.2f}",
        f"{bvalue:.2f}",
        charge,
        auth_seq_id,
        _cif_value(comp_id),
        _cif_value(auth_asym_id),
        _cif_value(name),
        str(model_num),
    ]


_ATOM_SITE_COLUMNS = [
    "group_PDB",
    "id",
    "type_symbol",
    "label_atom_id",
    "label_alt_id",
    "label_comp_id",
    "label_asym_id",
    "label_entity_id",
    "label_seq_id",
    "pdbx_PDB_ins_code",
    "Cartn_x",
    "Cartn_y",
    "Cartn_z",
    "occupancy",
    "B_iso_or_equiv",
    "pdbx_formal_charge",
    "auth_seq_id",
    "auth_comp_id",
    "auth_asym_id",
    "auth_atom_id",
    "pdbx_PDB_model_num",
]


def _build_entity_block(types: dict[str, str]) -> list[str]:
    """
    Build the entity loop block lines.

    :param types: mapping of entity_id to entity type
    :return: mmCIF lines for the entity table
    """
    lines = [
        "loop_",
        "_entity.id",
        "_entity.type",
    ]
    for eid, etype in sorted(types.items(), key=lambda x: int(x[0])):
        lines.append(f"{eid} {_cif_value(etype)}")
    return lines


def _build_struct_asym_block(asym_to_entity: dict[str, str]) -> list[str]:
    """
    Build the struct_asym loop block lines.

    :param asym_to_entity: mapping of label_asym_id to entity_id
    :return: mmCIF lines for the struct_asym table
    """
    lines = [
        "loop_",
        "_struct_asym.id",
        "_struct_asym.entity_id",
    ]
    for asym_id, eid in sorted(asym_to_entity.items()):
        lines.append(f"{_cif_value(asym_id)} {eid}")
    return lines


def _iter_atom_site_rows(pdb: PDB, asym_to_entity: dict[str, str]) -> Iterator[tuple[int, int, list[str]]]:
    """Yield model number, atom serial, and formatted atom-site row."""
    for model_num, model in enumerate(pdb.models, start=1):
        for chain_id, polymer in model.polymer.items():
            label_asym_id = polymer.internal_id or chain_id
            entity_id = asym_to_entity.get(label_asym_id, "?")
            label_seq_ids = _compute_label_seq_ids(polymer)
            for res_id, res in polymer.residues.items():
                _auth_asym, seq_ins = res_id.split(".", 1) if "." in res_id else (chain_id, res_id)
                m = re.match(r"(-?\d+)([a-zA-Z]*)", seq_ins)
                auth_seq_id, ins_code = (m.group(1), m.group(2)) if m else (seq_ins, "")
                comp_id = res.name or "UNK"
                seq_id = str(label_seq_ids.get(res_id, "."))

                for atom_id, atom in res.atoms.items():
                    group = "HETATM" if atom.is_hetatm else "ATOM"
                    row = _format_atom_row(atom_id, atom, group, label_asym_id, chain_id, comp_id, auth_seq_id, ins_code, model_num, entity_id, seq_id)
                    yield model_num, atom_id, row

        for np_id, nonpoly in model.non_polymer.items():
            label_asym_id = nonpoly.internal_id
            entity_id = asym_to_entity.get(label_asym_id, "?")
            _auth_asym, seq_ins = np_id.split(".", 1) if "." in np_id else (nonpoly.polymer, np_id)
            m = re.match(r"(-?\d+)([a-zA-Z]*)", seq_ins)
            auth_seq_id, ins_code = (m.group(1), m.group(2)) if m else (seq_ins, "")

            for atom_id, atom in nonpoly.atoms.items():
                row = _format_atom_row(atom_id, atom, "HETATM", label_asym_id, nonpoly.polymer, nonpoly.name, auth_seq_id, ins_code, model_num, entity_id)
                yield model_num, atom_id, row

        for w_id, water in model.water.items():
            label_asym_id = water.internal_id or water.polymer
            entity_id = asym_to_entity.get(label_asym_id, "?")
            _auth_asym, seq_ins = w_id.split(".", 1) if "." in w_id else (water.polymer, w_id)
            m = re.match(r"(-?\d+)([a-zA-Z]*)", seq_ins)
            auth_seq_id, ins_code = (m.group(1), m.group(2)) if m else (seq_ins, "")

            for atom_id, atom in water.atoms.items():
                row = _format_atom_row(atom_id, atom, "HETATM", label_asym_id, water.polymer, water.name or "HOH", auth_seq_id, ins_code, model_num, entity_id)
                yield model_num, atom_id, row


class _ConnectionPartner(NamedTuple):
    """Atom identity shared by atom_site and struct_conn, independent of serials."""

    label_asym_id: str
    label_comp_id: str
    label_seq_id: str
    label_atom_id: str
    label_alt_id: str
    pdbx_PDB_ins_code: str
    auth_asym_id: str
    auth_comp_id: str
    auth_seq_id: str


_PARTNER_INDICES = tuple(_ATOM_SITE_COLUMNS.index(field) for field in _ConnectionPartner._fields)
_STRUCT_CONN_COLUMNS = [
    "id",
    "conn_type_id",
    *(
        f"pdbx_ptnr{partner}_{field.removeprefix('pdbx_')}" if field in {"label_alt_id", "pdbx_PDB_ins_code"} else f"ptnr{partner}_{field}"
        for partner in (1, 2)
        for field in _ConnectionPartner._fields
    ),
]


def _build_atom_site_block(pdb: PDB, asym_to_entity: dict[str, str]) -> tuple[list[str], dict[tuple[int, int], _ConnectionPartner]]:
    """Write atom rows, retaining identities only for explicitly connected atoms."""
    connected = {(model_num, serial) for model_num, model in enumerate(pdb.models, start=1) for connection in model.connections for serial in connection}
    partners: dict[tuple[int, int], _ConnectionPartner] = {}
    lines = ["loop_"] + [f"_atom_site.{column}" for column in _ATOM_SITE_COLUMNS]
    for model_num, serial, row in _iter_atom_site_rows(pdb, asym_to_entity):
        lines.append(" ".join(row))
        if (model_num, serial) in connected:
            partners[model_num, serial] = _ConnectionPartner(*(row[index] for index in _PARTNER_INDICES))
    return lines, partners


def _build_struct_conn_block(pdb: PDB, partners: dict[tuple[int, int], _ConnectionPartner]) -> list[str]:
    """Write the union of all models' bonds using model-independent atom identities.

    struct_conn describes shared topology, so bonds present in only some models
    will apply to every model in which both partners can be resolved.
    """
    rows: list[str] = []
    seen: set[frozenset[_ConnectionPartner]] = set()
    for model_num, model in enumerate(pdb.models, start=1):
        for connection in model.connections:
            if len(connection) < 2 or (source := partners.get((model_num, connection[0]))) is None:
                continue
            for serial in connection[1:]:
                target = partners.get((model_num, serial))
                if target is None or source == target:
                    continue
                pair = frozenset((source, target))
                if pair in seen:
                    continue
                seen.add(pair)
                kind = "disulf" if source.label_comp_id == target.label_comp_id == "CYS" and source.label_atom_id == target.label_atom_id == "SG" else "covale"
                rows.append(" ".join([f"{kind}{len(rows) + 1}", kind, *source, *target]))
    return ["loop_", *(f"_struct_conn.{column}" for column in _STRUCT_CONN_COLUMNS), *rows] if rows else []


def _collect_sequences(pdb: PDB, asym_to_entity: dict[str, str]) -> dict[str, str]:
    """
    Collect a mapping of entity_id to sequence string for polymer chains.

    Uses polymer.sequence when available, otherwise derives the sequence from
    the residue names in order using the standard three-to-one letter mapping.

    :param pdb: PDB object to inspect
    :param asym_to_entity: mapping of label_asym_id to entity_id
    :return: mapping of entity_id to one-letter sequence string
    """
    result: dict[str, str] = {}
    if not pdb.models:
        return result
    for polymer in pdb.models[0].polymer.values():
        eid = asym_to_entity.get(polymer.internal_id)
        if not eid or eid in result:
            continue
        if polymer.sequence:
            result[eid] = polymer.sequence
        else:
            seq = "".join(CODES.get(res.name, "X") for res in polymer.residues.values() if res.name)
            if seq:
                result[eid] = seq
    return result


def _build_entity_poly_seq_block(sequences: dict[str, str]) -> list[str]:
    """
    Build the entity_poly_seq loop block lines.

    :param sequences: mapping of entity_id to one-letter sequence string
    :return: mmCIF lines for the entity_poly_seq table
    """
    lines = [
        "loop_",
        "_entity_poly_seq.entity_id",
        "_entity_poly_seq.num",
        "_entity_poly_seq.mon_id",
    ]
    for eid, seq in sorted(sequences.items(), key=lambda item: int(item[0])):
        for i, aa in enumerate(seq, start=1):
            mon_id = _REVERSE_CODES.get(aa, "UNK")
            lines.append(f"{eid} {i} {mon_id}")
    return lines


def _build_entity_poly_block(sequences: dict[str, str]) -> list[str]:
    """
    Build the entity_poly loop block with one-letter sequence codes and polymer type.

    :param sequences: mapping of entity_id to one-letter sequence string
    :return: mmCIF lines for the entity_poly table
    """
    if not sequences:
        return []
    lines = [
        "loop_",
        "_entity_poly.entity_id",
        "_entity_poly.type",
        "_entity_poly.pdbx_seq_one_letter_code",
        "_entity_poly.pdbx_seq_one_letter_code_can",
    ]
    for eid, seq in sorted(sequences.items(), key=lambda item: int(item[0])):
        lines.append(f"{eid} {_cif_value(_infer_polymer_type(seq))}")
        lines.append(f";{seq}")
        lines.append(";")
        lines.append(f";{seq}")
        lines.append(";")
    return lines


def _collect_chem_comp_atoms(pdb: PDB) -> dict[str, list[tuple[str, str]]]:
    """
    Collect unique (atom_name, element) pairs per component from the first model.

    Only unique atom names per component are collected, preserving order of first
    occurrence. Used to populate the chem_comp_atom table.

    :param pdb: PDB object to inspect
    :return: mapping of comp_id to ordered list of (atom_name, element) pairs
    """
    result: dict[str, list[tuple[str, str]]] = {}
    seen: dict[str, set[str]] = {}

    if not pdb.models:
        return result

    model = pdb.models[0]
    for polymer in model.polymer.values():
        for res in polymer.residues.values():
            if not res.name:
                continue
            comp = res.name
            if comp not in seen:
                seen[comp] = set()
                result[comp] = []
            for atom in res.atoms.values():
                aname = atom.name or atom.element
                if aname not in seen[comp]:
                    seen[comp].add(aname)
                    result[comp].append((aname, atom.element))

    for nonpoly in model.non_polymer.values():
        comp = nonpoly.name
        if comp not in seen:
            seen[comp] = set()
            result[comp] = []
        for atom in nonpoly.atoms.values():
            aname = atom.name or atom.element
            if aname not in seen[comp]:
                seen[comp].add(aname)
                result[comp].append((aname, atom.element))

    return result


def _build_chem_comp_atom_block(pdb: PDB) -> list[str]:
    """
    Build the chem_comp_atom loop block from atoms present in the structure.

    Aromatic flag and stereo config default to N since PDBAtom does not store them.

    :param pdb: PDB object to inspect
    :return: mmCIF lines for the chem_comp_atom table, or empty list if no atoms
    """
    chem_comp_atoms = _collect_chem_comp_atoms(pdb)
    if not chem_comp_atoms:
        return []

    lines = [
        "loop_",
        "_chem_comp_atom.comp_id",
        "_chem_comp_atom.atom_id",
        "_chem_comp_atom.type_symbol",
        "_chem_comp_atom.pdbx_aromatic_flag",
        "_chem_comp_atom.pdbx_stereo_config",
        "_chem_comp_atom.pdbx_ordinal",
    ]
    ordinal = 1
    for comp_id in sorted(chem_comp_atoms.keys()):
        for atom_name, element in chem_comp_atoms[comp_id]:
            lines.append(f"{_cif_value(comp_id)} {_cif_value(atom_name)} {element} N N {ordinal}")
            ordinal += 1
    return lines


def _parse_res_id(res_id: str) -> tuple[str, str, str]:
    """
    Split a residue ID into (auth_asym_id, auth_seq_id, ins_code).

    :param res_id: residue ID in "CHAIN.NUMins" format
    :return: tuple of chain, sequence number, insertion code
    """
    chain, seq_ins = res_id.split(".", 1) if "." in res_id else (res_id, res_id)
    m = re.match(r"(-?\d+)([a-zA-Z]*)", seq_ins)
    if m:
        return chain, m.group(1), m.group(2) if m.group(2) else "?"
    return chain, seq_ins, "?"


def _build_struct_conf_block(pdb: PDB) -> list[str]:
    """
    Build the struct_conf loop block lines for all helices.

    :param pdb: PDB object to inspect
    :return: mmCIF lines for the struct_conf table, or empty list if no helices
    """
    rows: list[tuple[str, str, str, str, str, str, str]] = []
    for model in pdb.models:
        for polymer in model.polymer.values():
            for i, helix in enumerate(polymer.helices, start=1):
                if len(helix) < 2:
                    continue
                beg_chain, beg_seq, beg_ins = _parse_res_id(helix[0])
                end_chain, end_seq, end_ins = _parse_res_id(helix[-1])
                rows.append((f"HELX_P{i}", beg_chain, beg_seq, beg_ins, end_chain, end_seq, end_ins))

    if not rows:
        return []

    lines = [
        "loop_",
        "_struct_conf.id",
        "_struct_conf.beg_auth_asym_id",
        "_struct_conf.beg_auth_seq_id",
        "_struct_conf.pdbx_beg_PDB_ins_code",
        "_struct_conf.end_auth_asym_id",
        "_struct_conf.end_auth_seq_id",
        "_struct_conf.pdbx_end_PDB_ins_code",
    ]
    for row in rows:
        lines.append(" ".join(_cif_value(value) for value in row))
    return lines


def _build_struct_sheet_range_block(pdb: PDB) -> list[str]:
    """
    Build the struct_sheet_range loop block lines for all strands.

    :param pdb: PDB object to inspect
    :return: mmCIF lines for the struct_sheet_range table, or empty list if no strands
    """
    rows: list[tuple[str, str, str, str, str, str, str]] = []
    for model in pdb.models:
        for polymer in model.polymer.values():
            for i, strand in enumerate(polymer.strands, start=1):
                if len(strand) < 2:
                    continue
                beg_chain, beg_seq, beg_ins = _parse_res_id(strand[0])
                end_chain, end_seq, end_ins = _parse_res_id(strand[-1])
                rows.append((f"STRN{i}", beg_chain, beg_seq, beg_ins, end_chain, end_seq, end_ins))

    if not rows:
        return []

    lines = [
        "loop_",
        "_struct_sheet_range.id",
        "_struct_sheet_range.beg_auth_asym_id",
        "_struct_sheet_range.beg_auth_seq_id",
        "_struct_sheet_range.pdbx_beg_PDB_ins_code",
        "_struct_sheet_range.end_auth_asym_id",
        "_struct_sheet_range.end_auth_seq_id",
        "_struct_sheet_range.pdbx_end_PDB_ins_code",
    ]
    for row in rows:
        lines.append(" ".join(_cif_value(value) for value in row))
    return lines


def _collect_chem_comp(pdb: PDB) -> dict[str, str]:
    """
    Collect a mapping of component ID to full name for all named residues.

    Only components with a non-None full_name are included. These are written
    to the chem_comp table so that full_name survives a round-trip.

    :param pdb: PDB object to inspect
    :return: mapping of residue/component code to full name
    """
    result: dict[str, str] = {}
    for model in pdb.models:
        for polymer in model.polymer.values():
            for res in polymer.residues.values():
                if res.name and res.full_name:
                    result[res.name] = res.full_name
        for nonpoly in model.non_polymer.values():
            if nonpoly.name and nonpoly.full_name:
                result[nonpoly.name] = nonpoly.full_name
    return result


def _build_chem_comp_block(chem_comp: dict[str, str]) -> list[str]:
    """
    Build the chem_comp loop block lines.

    :param chem_comp: mapping of component code to full name
    :return: mmCIF lines for the chem_comp table
    """
    lines = [
        "loop_",
        "_chem_comp.id",
        "_chem_comp.name",
        "_chem_comp.mon_nstd_flag",
    ]
    for comp_id, name in sorted(chem_comp.items()):
        lines.append(f"{_cif_value(comp_id)} {_cif_value(name)} n")
    return lines


def _build_description_block(pdb: PDB) -> list[str]:
    """
    Build the _entry.id and _struct.title records.

    :param pdb: PDB object to serialize
    :return: lines for the description block
    """
    lines: list[str] = []
    if pdb.description.code:
        lines.append(f"_entry.id {_cif_value(pdb.description.code.upper())}")
    if pdb.description.title:
        lines.append(f"_struct.title {_cif_value(pdb.description.title)}")
    return lines


def pdb_object_to_mmcif_filestring(pdb: PDB) -> str:
    """
    Serialize a PDB object to a mmCIF format string.

    Writes entity, entity_poly, chem_comp, chem_comp_atom, struct_asym,
    entity_poly_seq, struct_conf, struct_sheet, struct_conn, and atom_site tables.

    :param pdb: PDB object to serialize
    :return: mmCIF format string
    """
    data_name = f"data_{pdb.description.code.upper()}" if pdb.description.code else "data_STRUCTURE"

    if not pdb.models:
        return f"{data_name}\n#\n"

    pdb = _assign_missing_asym_ids(pdb)
    model = pdb.models[0]
    types, asym_to_entity = _collect_entities(model)
    chem_comp = _collect_chem_comp(pdb)
    sequences = _collect_sequences(pdb, asym_to_entity)

    atom_site, partners = _build_atom_site_block(pdb, asym_to_entity)

    struct_conf = _build_struct_conf_block(pdb)
    struct_sheet = _build_struct_sheet_range_block(pdb)
    struct_conn = _build_struct_conn_block(pdb, partners)
    entity_poly = _build_entity_poly_block(sequences)
    chem_comp_atom = _build_chem_comp_atom_block(pdb)

    sections: list[list[str]] = [[data_name]]
    description = _build_description_block(pdb)
    if description:
        sections.append(description)
    sections.append(_build_entity_block(types))
    if entity_poly:
        sections.append(entity_poly)
    if chem_comp:
        sections.append(_build_chem_comp_block(chem_comp))
    if chem_comp_atom:
        sections.append(chem_comp_atom)
    sections.append(_build_struct_asym_block(asym_to_entity))
    if sequences:
        sections.append(_build_entity_poly_seq_block(sequences))
    if struct_conf:
        sections.append(struct_conf)
    if struct_sheet:
        sections.append(struct_sheet)
    if struct_conn:
        sections.append(struct_conn)
    sections.append(atom_site)

    lines: list[str] = []
    for section in sections:
        lines.extend(section)
        lines.append("#")

    return "\n".join(lines) + "\n"
