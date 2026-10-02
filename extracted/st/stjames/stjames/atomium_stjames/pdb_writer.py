"""Functions for writing PDB objects to .pdb file format strings."""

import re
from datetime import datetime

from ..pdb import PDB, PDBAtom, PDBModel, PDBPolymer, _PDBAtomRecord
from .pdb import inverse_make_sequences


def _build_atom_lines(model: PDBModel) -> list[str]:
    """Build ATOM/HETATM/ANISOU/TER lines for a model, sorted by atom serial."""
    lines: list[str] = []
    atom_records = model._atom_records()

    # Write lines, inserting TER at polymer chain boundaries
    prev_chain: str | None = None
    prev_polymer = False
    last_poly: _PDBAtomRecord | None = None

    for atom_record in atom_records:
        # TER when leaving a polymer chain
        if prev_polymer and (not atom_record.is_polymer or atom_record.chain_id != prev_chain) and last_poly:
            lines.append(_format_ter_line(last_poly))

        lines.append(
            _format_atom_line(
                atom_record.serial,
                atom_record.atom,
                atom_record.chain_id,
                atom_record.residue_name,
                atom_record.residue_number,
                atom_record.alt_loc,
            )
        )

        if atom_record.atom.anisotropy and atom_record.atom.anisotropy != [0, 0, 0, 0, 0, 0]:
            lines.append(
                _format_anisou_line(
                    atom_record.serial,
                    atom_record.atom,
                    atom_record.chain_id,
                    atom_record.residue_name,
                    atom_record.residue_number,
                    atom_record.alt_loc,
                )
            )

        if atom_record.is_polymer:
            last_poly = atom_record
        prev_chain = atom_record.chain_id
        prev_polymer = atom_record.is_polymer

    # Final TER if ended on polymer
    if prev_polymer and last_poly:
        lines.append(_format_ter_line(last_poly))

    return lines


def _format_ter_line(atom_record: _PDBAtomRecord) -> str:
    """Format a TER record after the given atom."""
    match = re.match(r"(-?\d+)([a-zA-Z]*)", atom_record.residue_number)
    if match:
        num, ins = match.groups()
        ins = ins or " "
    else:
        num, ins = atom_record.residue_number, " "
    return f"TER   {atom_record.serial + 1:>5}      {atom_record.residue_name:>3} {atom_record.chain_id}{int(num):>4}{ins}"


def _format_atom_line(
    serial: int,
    atom: PDBAtom,
    chain_id: str,
    res_name: str,
    res_num: str | None,
    alt_loc: str = "",
) -> str:
    """
    Return a single PDB ATOM/HETATM record line as a string.

    See https://files.wwpdb.org/pub/pdb/doc/format_descriptions/Format_v33_Letter.pdf for details
    """
    record_type = "HETATM" if atom.is_hetatm else "ATOM  "
    alt_loc_char = alt_loc if alt_loc else " "
    residue_name = (res_name or "UNK")[:3]
    chain_char = (chain_id or "A")[:1]
    residue_num_str = "1"
    insertion_code = " "
    if res_num:
        match = re.match(r"(-?\d+)([a-zA-Z]*)", res_num)
        if match:
            residue_num_str, insertion_code = match.groups()
            insertion_code = insertion_code if insertion_code != "" else " "

    residue_num = int(residue_num_str)

    # Format charge: PDB uses e.g. "1-", "2+" in columns 79-80 (number then sign)
    chg = "  "
    if atom.charge and abs(atom.charge) > 0:
        chg_val = abs(int(atom.charge)) if float(atom.charge).is_integer() else abs(atom.charge)
        sign = "+" if atom.charge > 0 else "-"
        chg = f"{chg_val}{sign}"

    atom_name = atom.name if atom.name else atom.element

    # PDB atom name formatting (columns 13-16):
    # - 4-char names: use as-is
    # - Names starting with digit (e.g. 1H, 2H): left-justify
    # - Other short names: add leading space (element in cols 13-14)
    if len(atom_name) >= 4:
        formatted_atom_name = atom_name[:4]
    elif atom_name[0].isdigit():
        formatted_atom_name = f"{atom_name:<4}"
    else:
        formatted_atom_name = f" {atom_name:<3}"

    occupancy = atom.occupancy if atom.occupancy else 1.0

    return (
        f"{record_type}"
        f"{serial:5d} "  # atom serial number (columns 7-11)
        f"{formatted_atom_name}"  # atom name (columns 13-16)
        f"{alt_loc_char}"  # altLoc (column 17)
        f"{residue_name:>3}"  # residue name (columns 18-20)
        f" {chain_char}"  # chain ID (column 22)
        f"{residue_num:4d}"  # residue sequence number (columns 23-26)
        f"{insertion_code}"
        f"   "  # columns 27-30 (spacing)
        f"{atom.x:8.3f}"  # x (columns 31-38)
        f"{atom.y:8.3f}"  # y (columns 39-46)
        f"{atom.z:8.3f}"  # z (columns 47-54)
        f"{occupancy:6.2f}"  # occupancy (columns 55-60)
        f"{atom.bvalue or 0.0:6.2f}"  # temp factor (columns 61-66)
        f"          "  # columns 67-76 (padding)
        f"{atom.element:>2}"  # element (columns 77-78)
        f"{chg:>2}"  # charge (columns 79-80)
    )


def _format_anisou_line(
    serial: int,
    atom: PDBAtom,
    chain_id: str,
    res_name: str,
    res_num: str | None,
    alt_loc: str = "",
) -> str:
    """
    Return a single PDB ANISOU record line as a string.

    See https://files.wwpdb.org/pub/pdb/doc/format_descriptions/Format_v33_Letter.pdf for details
    """
    alt_loc_char = alt_loc if alt_loc else " "
    residue_name = (res_name or "UNK")[:3]
    chain_char = (chain_id or "A")[:1]
    residue_num_str = "1"
    insertion_code = " "
    if res_num:
        match = re.match(r"(-?\d+)([a-zA-Z]*)", res_num)
        if match:
            residue_num_str, insertion_code = match.groups()
            insertion_code = insertion_code if insertion_code != "" else " "

    residue_num = int(residue_num_str)

    # Format charge: PDB uses e.g. "1-", "2+" in columns 79-80 (number then sign)
    chg = "  "
    if atom.charge and abs(atom.charge) > 0:
        chg_val = abs(int(atom.charge)) if float(atom.charge).is_integer() else abs(atom.charge)
        sign = "+" if atom.charge > 0 else "-"
        chg = f"{chg_val}{sign}"

    atom_name = atom.name if atom.name else atom.element

    # PDB atom name formatting (columns 13-16):
    # - 4-char names: use as-is
    # - Names starting with digit (e.g. 1H, 2H): left-justify
    # - Other short names: add leading space (element in cols 13-14)
    if len(atom_name) >= 4:
        formatted_atom_name = atom_name[:4]
    elif atom_name[0].isdigit():
        formatted_atom_name = f"{atom_name:<4}"
    else:
        formatted_atom_name = f" {atom_name:<3}"

    if atom.anisotropy:
        aniso_parts = []
        for val in atom.anisotropy:
            if val is None:
                # Write missing data as spaces
                aniso_parts.append(f"{'':>7}")
            else:
                aniso_parts.append(f"{_float_to_pdb_string(val):>7}")
        aniso_lines = "".join(aniso_parts)
    else:
        aniso_lines = f"{'':>7}" * 6

    return (
        f"ANISOU"
        f"{serial:5d} "  # atom serial number (columns 7-11)
        f"{formatted_atom_name}"  # atom name (columns 13-16)
        f"{alt_loc_char}"  # altLoc (column 17)
        f"{residue_name:>3}"  # residue name (columns 18-20)
        f" {chain_char}"  # chain ID (column 22)
        f"{residue_num:4d}"  # residue sequence number (columns 23-26)
        f"{insertion_code}"
        f" "
        f"{aniso_lines}"
        f"      "  # columns 70-76 (padding)
        f"{atom.element:>2}"  # element (columns 77-78)
        f"{chg:>2}"  # charge (columns 79-80)
    )


def _format_conect_line(atoms: list[int]) -> str:
    """
    Format a CONECT record line.

    :param atoms: atom serial numbers to connect
    :return: formatted CONECT line
    """
    line = "CONECT"
    for atom in atoms:
        line += f"{atom:5d}"
    return line


def _float_to_pdb_string(x: float) -> str:
    """
    Format a float for use in a PDB ANISOU record.

    :param x: value to format
    :return: formatted string with 5 significant digits
    """
    sign = "-" if x < 0 else ""
    a = abs(x)
    if a < 1:
        s = f"{a:.4f}"
        significant = s[2:].lstrip("0")
        return sign + significant
    else:
        s = f"{a:.4f}"
        integer_part, fractional_part = s.split(".")
        needed = 5 - len(integer_part)
        result = integer_part + fractional_part[:needed]
        return sign + result


def _helix_list_to_pdb_helix(polymer_dict: dict[str, PDBPolymer], helices: list[list[str]]) -> list[str]:
    """
    Convert helix data to PDB HELIX records.

    :param polymer_dict: mapping of chain IDs to polymer data
    :param helices: list of helix residue ID ranges
    :return: HELIX record lines
    """
    helix_lines = []
    for i, helix in enumerate(helices, start=1):
        start_aa_name = polymer_dict[helix[0][0]].residues[helix[0]].name
        end_aa_name = polymer_dict[helix[-1][0]].residues[helix[-1]].name
        helix_line = f"HELIX  {i:>3} {i:>3} {start_aa_name} {helix[0][0]} {helix[0][2:]:>4}  {end_aa_name} {helix[-1][0]} {helix[-1][2:]:>4}  1{len(helix):>36}"
        helix_lines.append(helix_line)
    return helix_lines


def _strand_list_to_pdb_sheets(polymer_dict: dict[str, PDBPolymer], strands: list[list[str]]) -> list[str]:
    """
    Convert strand data to PDB SHEET records.

    :param polymer_dict: mapping of chain IDs to polymer data
    :param strands: list of strand residue ID ranges
    :return: SHEET record lines
    """
    strand_lines = []
    for i, strand in enumerate(strands, start=1):
        start_aa_name = polymer_dict[strand[0][0]].residues[strand[0]].name
        end_aa_name = polymer_dict[strand[-1][0]].residues[strand[-1]].name
        helix_line = (
            f"SHEET  {i:>3} {strand[0][0]:>3}{len(strands):>2} {start_aa_name} {strand[0][0]}{strand[0][2:]:>4}  "
            f"{end_aa_name} {strand[-1][0]}{strand[-1][2:]:>4} {-1 if i != 1 else 0:>2}"
        )
        strand_lines.append(helix_line)
    return strand_lines


def _build_header_section(pdb: PDB) -> list[str]:
    """
    Build PDB HEADER, TITLE, EXPDTA, and AUTHOR lines.

    :param pdb: PDB object to read
    :return: header record lines
    """

    def _format_date(date_str: str | None) -> str | None:
        if date_str is None:
            return None
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        return date_obj.strftime("%d-%b-%y").upper()

    header = f"HEADER    {pdb.description.classification or '':<40}{_format_date(pdb.description.deposition_date) or '':<10}  {pdb.description.code or '':<5}"
    title = f"TITLE     {pdb.description.title or '':<70}"
    exp_dta = f"EXPDTA    {pdb.experiment.technique or '':<69}"
    authors = f"AUTHOR    {','.join(pdb.description.authors).upper():<69}"
    return [header, title, exp_dta, authors]


def _build_source_section(pdb: PDB) -> list[str]:
    """
    Build SOURCE organism and expression system lines.

    :param pdb: PDB object to read
    :return: SOURCE record lines
    """
    organism_line = f"SOURCE    ORGANISM_SCIENTIFIC: {(pdb.experiment.source_organism + ';') if pdb.experiment.source_organism else '':<69}"
    expression_line = f"SOURCE    EXPRESSION_SYSTEM: {(pdb.experiment.expression_system + ';') if pdb.experiment.expression_system else '':<69}"
    return [organism_line, expression_line]


def _build_keyword_section(pdb: PDB) -> list[str]:
    """
    Build KEYWDS lines.

    :param pdb: PDB object to read
    :return: KEYWDS record lines
    """
    lines = []
    for i, keyword in enumerate(pdb.description.keywords):
        if i == len(pdb.description.keywords) - 1:
            lines.append(f"KEYWDS    {keyword:<79}")
        else:
            lines.append(f"KEYWDS    {keyword + ',':<79}")
    return lines


def _build_secondary_structure_and_seqres(pdb: PDB, full_name_dict: dict[str, str]) -> tuple[list[str], list[str]]:
    """
    Build secondary structure and SEQRES lines, and collect HETNAM data.

    :param pdb: PDB object to read
    :param full_name_dict: mapping to populate with heterogen full names
    :return: tuple of (seqres lines, chain IDs)
    """
    seqres_lines = []
    chains = []

    for model in pdb.models:
        for chain_id, polymer in model.polymer.items():
            chains.append(chain_id)
            for strand_line in _strand_list_to_pdb_sheets(model.polymer, polymer.strands):
                seqres_lines.append(strand_line)
            for helix_line in _helix_list_to_pdb_helix(model.polymer, polymer.helices):
                seqres_lines.append(helix_line)
            if polymer.sequence:
                seqres_lines.extend(inverse_make_sequences(polymer.sequence, chain_id))
            for _, residue in polymer.residues.items():
                if residue.full_name and residue.name:
                    full_name_dict[residue.name] = residue.full_name
        for _, non_polymer in model.non_polymer.items():
            if non_polymer.full_name and non_polymer.name:
                full_name_dict[non_polymer.name] = non_polymer.full_name

    return seqres_lines, chains


def _build_hetname_section(full_name_dict: dict[str, str]) -> list[str]:
    """
    Build HETNAM lines for non-polymer molecules.

    :param full_name_dict: mapping of residue codes to full names
    :return: HETNAM record lines
    """
    lines = []
    for name, full_name in full_name_dict.items():
        if len(full_name) > 55:
            for i in range(0, len(full_name), 55):
                lines.append(f"HETNAM  {int(i / 55):>2} {name:<3} {full_name[i : i + 55]:<55}")
        else:
            lines.append(f"HETNAM     {name:<3} {full_name:<55}")
    return lines


def _build_remark_section(pdb: PDB, chains: list[str]) -> list[str]:
    """
    Build REMARK lines for resolution, R-factors, biomolecule, and missing residues.

    :param pdb: PDB object to read
    :param chains: chain IDs for BIOMT records
    :return: REMARK record lines
    """
    lines = []
    lines.append(f"REMARK   2 RESOLUTION. {pdb.quality.resolution or '':>7} ANGSTROMS.")
    if pdb.quality.rfree:
        lines.append(f"REMARK   3   FREE R VALUE                     : {pdb.quality.rfree or ''}")
    if pdb.quality.rvalue:
        lines.append(f"REMARK   3   R VALUE            (WORKING SET) : {pdb.quality.rvalue or ''}")

    lines.append("REMARK 350")
    lines.append("REMARK 350 COORDINATES FOR A COMPLETE MULTIMER REPRESENTING THE KNOWN")
    lines.append("REMARK 350 BIOLOGICALLY SIGNIFICANT OLIGOMERIZATION STATE OF THE")
    lines.append("REMARK 350 MOLECULE CAN BE GENERATED BY APPLYING BIOMT TRANSFORMATIONS")
    lines.append("REMARK 350 GIVEN BELOW.  BOTH NON-CRYSTALLOGRAPHIC AND")
    lines.append("REMARK 350 CRYSTALLOGRAPHIC OPERATIONS ARE GIVEN.")
    lines.append("REMARK 350")
    lines.append("REMARK 350 BIOMOLECULE: 1")
    lines.append("REMARK 350 AUTHOR DETERMINED BIOLOGICAL UNIT: MONOMERIC")
    lines.append(f"REMARK 350 APPLY THE FOLLOWING TO CHAINS: {', '.join(chains)}")
    lines.append("REMARK 350   BIOMT1   1  1.000000  0.000000  0.000000        0.00000")
    lines.append("REMARK 350   BIOMT2   1  0.000000  1.000000  0.000000        0.00000")
    lines.append("REMARK 350   BIOMT3   1  0.000000  0.000000  1.000000        0.00000")

    lines.append("REMARK 465 MISSING RESIDUES")
    lines.append("REMARK 465 THE FOLLOWING RESIDUES WERE NOT LOCATED IN THE")
    lines.append("REMARK 465 EXPERIMENT. (M=MODEL NUMBER; RES=RESIDUE NAME; C=CHAIN")
    lines.append("REMARK 465 IDENTIFIER; SSSEQ=SEQUENCE NUMBER; I=INSERTION CODE.)")
    lines.append("REMARK 465")
    lines.append("REMARK 465   M RES C SSSEQI")
    for missing_residue in pdb.experiment.missing_residues:
        lines.append(f"REMARK 465     {missing_residue.name} {missing_residue.id[0]}   {missing_residue.id[2:]}")
    return lines


def _build_crystallography_section(pdb: PDB) -> list[str]:
    """
    Build the CRYST1 line if unit cell data is present.

    :param pdb: PDB object to read
    :return: CRYST1 record lines
    """
    lines = []
    if pdb.geometry.crystallography.unit_cell:
        lines.append(
            f"CRYST1{pdb.geometry.crystallography.unit_cell[0]:>9}"
            f"{pdb.geometry.crystallography.unit_cell[1]:>9}"
            f"{pdb.geometry.crystallography.unit_cell[2]:>9}"
            f"{pdb.geometry.crystallography.unit_cell[3]:>7}"
            f"{pdb.geometry.crystallography.unit_cell[4]:>7}"
            f"{pdb.geometry.crystallography.unit_cell[5]:>7} "
            f"{pdb.geometry.crystallography.space_group or '':<11}"
        )
    return lines


def pdb_object_to_pdb_filestring(
    pdb: PDB,
    header: bool = False,
    source: bool = False,
    keyword: bool = False,
    seqres: bool = True,
    hetnam: bool = True,
    remark: bool = False,
    crystallography: bool = False,
) -> str:
    """
    Serialize a PDB object to a .pdb format string.

    :param pdb: PDB object to serialize
    :param header: include HEADER/TITLE/EXPDTA/AUTHOR lines
    :param source: include SOURCE lines
    :param keyword: include KEYWDS lines
    :param seqres: include SEQRES and secondary structure lines
    :param hetnam: include HETNAM lines
    :param remark: include REMARK lines
    :param crystallography: include CRYST1 line
    :return: .pdb format string
    """
    pdb_lines: list[str] = []
    chains: list[str] = []

    if header:
        pdb_lines.extend(_build_header_section(pdb))

    if source:
        pdb_lines.extend(_build_source_section(pdb))

    if keyword:
        pdb_lines.extend(_build_keyword_section(pdb))

    full_name_dict: dict[str, str] = {}
    seqres_lines, chains = _build_secondary_structure_and_seqres(pdb, full_name_dict)

    if seqres:
        pdb_lines.extend(seqres_lines)

    if hetnam:
        pdb_lines.extend(_build_hetname_section(full_name_dict))

    if remark:
        pdb_lines.extend(_build_remark_section(pdb, chains))

    if crystallography:
        pdb_lines.extend(_build_crystallography_section(pdb))

    for model_index, model in enumerate(pdb.models, start=1):
        if len(pdb.models) > 1:
            pdb_lines.append(f"MODEL     {model_index:>4}")

        pdb_lines.extend(_build_atom_lines(model))

        if len(pdb.models) > 1:
            pdb_lines.append("ENDMDL")

        # CONECT records
        for connection in getattr(model, "connections", []):
            pdb_lines.append(_format_conect_line(connection))

    # PDB standard ends with an END record
    pdb_lines.append("END")
    return "\n".join(pdb_lines) + "\n"
