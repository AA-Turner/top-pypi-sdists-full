//! I/O utilities for structure parsing and file format support.
//!
//! This module provides functions for parsing structures from various formats:
//! - Pymatgen JSON (`Structure.as_dict()`)
//! - VASP POSCAR/CONTCAR
//! - extXYZ (Extended XYZ format)
//! - CIF (Crystallographic Information File) — see [`cif`]
//! - LAMMPS dump/trajectory (`.lammpstrj`, `.lmp`, `.dump`)
//! - VASP XDATCAR trajectory (`XDATCAR*`)
//!
//! Submodules:
//! - [`cif`] — CIF parser with symmetry expansion
//! - `lmdb` — LMDB-backed dataset storage for ML training data (requires `lmdb` feature)
//! - `mp` — Materials Project API and S3 open-data clients (requires `mp` feature)
//! - [`vasp`] — VASP-specific file formats (CHGCAR, etc.)
//!
//! Use [`parse_structure`] for automatic format detection, or the format-specific
//! functions for explicit control.

pub mod cif;
#[cfg(feature = "lmdb")]
pub mod lmdb;
#[cfg(feature = "mp")]
pub mod mp;
pub mod vasp;

mod ase_atoms;
mod extxyz;
mod lammps;
mod molecules;
mod optimade;
mod poscar;
mod torchsim;
mod unified_api;
mod writers;
mod xdatcar;

pub use ase_atoms::{
    ase_atoms_to_pymatgen_json, molecule_to_ase_atoms_dict, molecules_to_ase_atoms_dicts,
    parse_ase_atoms_json, parse_xyz_flexible, structure_to_ase_atoms_dict,
    structures_to_ase_atoms_dicts,
};
pub use extxyz::{parse_extxyz, parse_extxyz_trajectory};
pub use lammps::{
    parse_lammps_dump, parse_lammps_dump_str, parse_lammps_trajectory, parse_lammps_trajectory_str,
};
#[allow(deprecated)]
pub use molecules::StructureOrMolecule;
pub use molecules::{
    molecule_to_extxyz, molecule_to_pymatgen_json, molecule_to_xyz, parse_molecule_json, parse_xyz,
    parse_xyz_molecules, parse_xyz_str, write_xyz,
};
pub use optimade::{is_optimade_json, parse_optimade_json, parse_optimade_json_list};
pub use poscar::{parse_poscar, parse_poscar_str};
pub use torchsim::{
    TorchSimState, parse_torch_sim_state, structure_to_torch_sim_state,
    structures_to_torch_sim_state, torch_sim_state_to_json, torch_sim_state_to_structures,
};
pub use unified_api::{
    StructureFormat, parse_structure, parse_structure_file, parse_structure_json,
    parse_structure_json_with_merge_tol, parse_structures_glob, structure_to_json,
    structure_to_pymatgen_json,
};
pub use writers::{
    structure_to_extxyz, structure_to_poscar, write_extxyz, write_poscar, write_structure,
};
pub use xdatcar::{
    parse_xdatcar, parse_xdatcar_str, parse_xdatcar_trajectory, parse_xdatcar_trajectory_str,
};

#[cfg(test)]
mod tests;
