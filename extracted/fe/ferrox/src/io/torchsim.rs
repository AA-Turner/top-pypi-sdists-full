use crate::element::Element;
use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use crate::species::{SiteOccupancy, Species};
use crate::structure::Structure;
use nalgebra::Vector3;
use std::collections::HashMap;

// === TorchSim State Conversion ===

/// Transpose cell matrix from row-major (ASE/pymatgen) to column-major (TorchSim).
fn cell_to_column_major(mat: &nalgebra::Matrix3<f64>) -> [[f64; 3]; 3] {
    [
        [mat[(0, 0)], mat[(1, 0)], mat[(2, 0)]], // column a
        [mat[(0, 1)], mat[(1, 1)], mat[(2, 1)]], // column b
        [mat[(0, 2)], mat[(1, 2)], mat[(2, 2)]], // column c
    ]
}

/// Transpose cell matrix from column-major (TorchSim) to row-major (ASE/pymatgen).
fn cell_from_column_major(cols: &[[f64; 3]; 3]) -> nalgebra::Matrix3<f64> {
    nalgebra::Matrix3::new(
        cols[0][0], cols[1][0], cols[2][0], // row 0
        cols[0][1], cols[1][1], cols[2][1], // row 1
        cols[0][2], cols[1][2], cols[2][2], // row 2
    )
}

/// Represents a TorchSim SimState for serialization.
///
/// TorchSim uses batched states where multiple systems can be stored together.
/// The `system_idx` field indicates which system each atom belongs to.
///
/// Note: Cell matrices use column-major convention (transposed from ASE).
#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct TorchSimState {
    /// Cartesian positions for all atoms, shape (n_total_atoms, 3)
    pub positions: Vec<[f64; 3]>,
    /// Atomic masses in amu, shape (n_total_atoms,)
    pub masses: Vec<f64>,
    /// Cell matrices for each system, shape (n_systems, 3, 3)
    /// Uses column-major convention: cell[i] contains columns [a, b, c]
    pub cell: Vec<[[f64; 3]; 3]>,
    /// Periodic boundary conditions [pbc_x, pbc_y, pbc_z]
    pub pbc: [bool; 3],
    /// Atomic numbers for all atoms, shape (n_total_atoms,)
    pub atomic_numbers: Vec<i32>,
    /// System index for each atom, shape (n_total_atoms,)
    /// Indicates which system (0-indexed) each atom belongs to
    pub system_idx: Vec<usize>,
    /// Total charge for each system, shape (n_systems,)
    #[serde(default)]
    pub charge: Vec<f64>,
    /// Spin multiplicity for each system, shape (n_systems,)
    #[serde(default)]
    pub spin: Vec<f64>,
}

/// Convert a single Structure to TorchSim state format.
///
/// # Arguments
///
/// * `structure` - The structure to convert
///
/// # Returns
///
/// TorchSimState with a single system (system_idx all zeros).
pub fn structure_to_torch_sim_state(structure: &Structure) -> TorchSimState {
    let n_atoms = structure.num_sites();
    let cart_coords = structure.cart_coords();

    // Positions as [x, y, z] arrays
    let positions: Vec<[f64; 3]> = cart_coords.iter().map(|c| [c.x, c.y, c.z]).collect();

    // Masses from elements
    let masses: Vec<f64> = structure
        .site_occupancies
        .iter()
        .map(|so| so.dominant_species().element.atomic_mass())
        .collect();

    // Cell matrix - transpose to column-major for TorchSim
    let cell = vec![cell_to_column_major(structure.lattice.matrix())];

    // Atomic numbers
    let atomic_numbers: Vec<i32> = structure
        .site_occupancies
        .iter()
        .map(|so| so.dominant_species().element.atomic_number() as i32)
        .collect();

    // All atoms belong to system 0
    let system_idx = vec![0usize; n_atoms];

    // Extract spin from properties if present (like ASE's atoms.info["spin"])
    let spin = structure
        .properties
        .get("spin")
        .and_then(|v| v.as_f64())
        .unwrap_or(0.0);

    TorchSimState {
        positions,
        masses,
        cell,
        pbc: structure.lattice.pbc,
        atomic_numbers,
        system_idx,
        charge: vec![structure.charge],
        spin: vec![spin],
    }
}

/// Convert multiple Structures to a batched TorchSim state.
///
/// # Arguments
///
/// * `structures` - Slice of structures to convert
///
/// # Returns
///
/// TorchSimState with all systems batched together.
///
/// # Errors
///
/// Returns an error if structures have inconsistent PBC settings.
pub fn structures_to_torch_sim_state(structures: &[Structure]) -> Result<TorchSimState> {
    if structures.is_empty() {
        return Ok(TorchSimState {
            positions: vec![],
            masses: vec![],
            cell: vec![],
            pbc: [true, true, true],
            atomic_numbers: vec![],
            system_idx: vec![],
            charge: vec![],
            spin: vec![],
        });
    }

    // Verify consistent PBC
    let first_pbc = structures[0].lattice.pbc;
    for (idx, structure) in structures.iter().enumerate().skip(1) {
        if structure.lattice.pbc != first_pbc {
            return Err(FerroxError::JsonError {
                path: "inline".to_string(),
                reason: format!(
                    "Structure {} has pbc {:?}, but structure 0 has pbc {:?}. All structures must have the same periodic boundary conditions.",
                    idx, structure.lattice.pbc, first_pbc
                ),
            });
        }
    }

    let total_atoms: usize = structures.iter().map(|s| s.num_sites()).sum();

    let mut positions = Vec::with_capacity(total_atoms);
    let mut masses = Vec::with_capacity(total_atoms);
    let mut atomic_numbers = Vec::with_capacity(total_atoms);
    let mut system_idx = Vec::with_capacity(total_atoms);
    let mut cell = Vec::with_capacity(structures.len());
    let mut charge = Vec::with_capacity(structures.len());
    let mut spin = Vec::with_capacity(structures.len());

    for (sys_idx, structure) in structures.iter().enumerate() {
        let cart_coords = structure.cart_coords();

        for (site_occ, cart) in structure.site_occupancies.iter().zip(cart_coords.iter()) {
            positions.push([cart.x, cart.y, cart.z]);
            masses.push(site_occ.dominant_species().element.atomic_mass());
            atomic_numbers.push(site_occ.dominant_species().element.atomic_number() as i32);
            system_idx.push(sys_idx);
        }

        // Cell matrix - transpose to column-major
        cell.push(cell_to_column_major(structure.lattice.matrix()));

        charge.push(structure.charge);
        // Extract spin from properties if present
        let sys_spin = structure
            .properties
            .get("spin")
            .and_then(|v| v.as_f64())
            .unwrap_or(0.0);
        spin.push(sys_spin);
    }

    Ok(TorchSimState {
        positions,
        masses,
        cell,
        pbc: first_pbc,
        atomic_numbers,
        system_idx,
        charge,
        spin,
    })
}

/// Convert TorchSim state JSON to a list of Structures.
///
/// # Arguments
///
/// * `json_str` - JSON string in TorchSim state format
///
/// # Returns
///
/// Vector of Structures, one per system in the batched state.
pub fn parse_torch_sim_state(json_str: &str) -> Result<Vec<Structure>> {
    let state: TorchSimState =
        serde_json::from_str(json_str).map_err(|e| FerroxError::JsonError {
            path: "inline".to_string(),
            reason: format!("Invalid TorchSim state JSON: {e}"),
        })?;

    torch_sim_state_to_structures(&state)
}

/// Convert a TorchSimState to a list of Structures.
///
/// # Arguments
///
/// * `state` - The TorchSim state to convert
///
/// # Returns
///
/// Vector of Structures, one per system in the batched state.
pub fn torch_sim_state_to_structures(state: &TorchSimState) -> Result<Vec<Structure>> {
    if state.positions.is_empty() {
        return Ok(vec![]);
    }

    // Validate array lengths match
    let n_atoms = state.positions.len();
    if state.atomic_numbers.len() != n_atoms || state.system_idx.len() != n_atoms {
        return Err(FerroxError::JsonError {
            path: "inline".to_string(),
            reason: format!(
                "Array length mismatch: positions={}, atomic_numbers={}, system_idx={}",
                n_atoms,
                state.atomic_numbers.len(),
                state.system_idx.len()
            ),
        });
    }
    // Validate masses length if provided
    if !state.masses.is_empty() && state.masses.len() != n_atoms {
        return Err(FerroxError::JsonError {
            path: "inline".to_string(),
            reason: format!(
                "masses length {} doesn't match positions length {}",
                state.masses.len(),
                n_atoms
            ),
        });
    }

    // Determine number of systems
    let n_systems = state.cell.len();
    if n_systems == 0 {
        return Err(FerroxError::JsonError {
            path: "inline".to_string(),
            reason: "TorchSim state has positions but no cell matrices".to_string(),
        });
    }

    // Validate system_idx bounds - ensure no atom references a non-existent system
    if let Some(&max_sid) = state.system_idx.iter().max()
        && max_sid >= n_systems
    {
        return Err(FerroxError::JsonError {
            path: "inline".to_string(),
            reason: format!(
                "system_idx contains {max_sid} but only {n_systems} cell matrices are present"
            ),
        });
    }

    // Validate charge and spin lengths if provided
    if !state.charge.is_empty() && state.charge.len() != n_systems {
        return Err(FerroxError::JsonError {
            path: "inline".to_string(),
            reason: format!(
                "charge length ({}) must match number of systems ({n_systems})",
                state.charge.len()
            ),
        });
    }
    if !state.spin.is_empty() && state.spin.len() != n_systems {
        return Err(FerroxError::JsonError {
            path: "inline".to_string(),
            reason: format!(
                "spin length ({}) must match number of systems ({n_systems})",
                state.spin.len()
            ),
        });
    }

    let mut structures = Vec::with_capacity(n_systems);

    for sys_idx in 0..n_systems {
        // Find atoms belonging to this system
        let atom_indices: Vec<usize> = state
            .system_idx
            .iter()
            .enumerate()
            .filter_map(|(idx, &sid)| (sid == sys_idx).then_some(idx))
            .collect();

        if atom_indices.is_empty() {
            return Err(FerroxError::JsonError {
                path: "inline".to_string(),
                reason: format!("System {sys_idx} has no atoms"),
            });
        }

        // Extract positions for this system
        let cart_coords: Vec<Vector3<f64>> = atom_indices
            .iter()
            .map(|&idx| {
                let pos = state.positions[idx];
                Vector3::new(pos[0], pos[1], pos[2])
            })
            .collect();

        // Extract species for this system
        let species: Result<Vec<Species>> = atom_indices
            .iter()
            .map(|&idx| {
                let z_i32 = state.atomic_numbers[idx];
                // Validate range before casting to u8 to catch negative/overflow values
                if z_i32 <= 0 || z_i32 > u8::MAX as i32 {
                    return Err(FerroxError::JsonError {
                        path: "inline".to_string(),
                        reason: format!("Invalid atomic number: {z_i32}"),
                    });
                }
                let z = z_i32 as u8;
                let elem =
                    Element::from_atomic_number(z).ok_or_else(|| FerroxError::JsonError {
                        path: "inline".to_string(),
                        reason: format!("Invalid atomic number: {z}"),
                    })?;
                Ok(Species::neutral(elem))
            })
            .collect();
        let species = species?;

        // Cell matrix - transpose from column-major back to row-major
        let mut lattice = Lattice::new(cell_from_column_major(&state.cell[sys_idx]));
        lattice.pbc = state.pbc;

        // Convert Cartesian to fractional
        let frac_coords = lattice.get_fractional_coords(&cart_coords);

        // Get charge and spin for this system
        let charge = state.charge.get(sys_idx).copied().unwrap_or(0.0);
        let spin = state.spin.get(sys_idx).copied().unwrap_or(0.0);

        // Build properties map with spin if non-zero
        let mut properties = HashMap::new();
        if spin.abs() > 1e-10 {
            properties.insert("spin".to_string(), serde_json::json!(spin));
        }

        let structure = Structure::try_new_full(
            lattice,
            species.into_iter().map(SiteOccupancy::ordered).collect(),
            frac_coords,
            state.pbc,
            charge,
            properties,
        )?;

        structures.push(structure);
    }

    Ok(structures)
}

/// Convert TorchSim state to JSON string.
///
/// # Arguments
///
/// * `state` - The TorchSim state to serialize
///
/// # Returns
///
/// JSON string representation of the state.
pub fn torch_sim_state_to_json(state: &TorchSimState) -> String {
    serde_json::to_string(state).expect("TorchSimState serialization should not fail")
}
