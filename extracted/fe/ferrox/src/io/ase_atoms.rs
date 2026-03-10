use crate::element::Element;
use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use crate::species::{SiteOccupancy, Species};
use crate::structure::Structure;
use nalgebra::Vector3;
use serde::Deserialize;
use std::collections::HashMap;
use std::path::Path;

use super::extxyz::frame_to_structure;
#[allow(deprecated)]
use super::molecules::{StructureOrMolecule, frame_to_molecule, molecule_to_pymatgen_json};
use super::unified_api::structure_to_pymatgen_json;

// === ASE Atoms Dict Conversion ===

/// Represents an ASE Atoms dict structure.
#[derive(Debug, Deserialize)]
#[allow(dead_code)]
struct AseAtomsDict {
    /// Element symbols for each atom
    symbols: Vec<String>,
    /// Cartesian positions [[x1, y1, z1], ...]
    positions: Vec<[f64; 3]>,
    /// Cell matrix (3x3), optional for molecules
    #[serde(default)]
    cell: Option<[[f64; 3]; 3]>,
    /// Periodic boundary conditions [pbc_x, pbc_y, pbc_z]
    #[serde(default = "default_ase_pbc")]
    pbc: [bool; 3],
    /// Additional info dict (charge, energy, etc.)
    #[serde(default)]
    info: HashMap<String, serde_json::Value>,
}

fn default_ase_pbc() -> [bool; 3] {
    [false, false, false]
}

/// Parse ASE Atoms dict format from JSON.
///
/// Returns a Structure if a cell is present and pbc contains at least one true,
/// otherwise returns a Molecule.
///
/// # Arguments
///
/// * `json` - JSON string in ASE Atoms dict format
///
/// # Returns
///
/// Either a Structure or Molecule depending on periodicity.
///
/// # Example
///
/// ```rust,ignore
/// let json = r#"{
///     "symbols": ["Fe", "O"],
///     "positions": [[0, 0, 0], [2, 0, 0]],
///     "cell": [[4, 0, 0], [0, 4, 0], [0, 0, 4]],
///     "pbc": [true, true, true]
/// }"#;
/// let result = parse_ase_atoms_json(json)?;
/// ```
#[allow(deprecated)]
pub fn parse_ase_atoms_json(json: &str) -> Result<StructureOrMolecule> {
    let parsed: AseAtomsDict = serde_json::from_str(json).map_err(|e| FerroxError::JsonError {
        path: "inline".to_string(),
        reason: e.to_string(),
    })?;

    // Validate lengths match
    if parsed.symbols.len() != parsed.positions.len() {
        return Err(FerroxError::JsonError {
            path: "inline".to_string(),
            reason: format!(
                "symbols and positions must have same length: {} vs {}",
                parsed.symbols.len(),
                parsed.positions.len()
            ),
        });
    }

    // Parse species
    let mut species = Vec::with_capacity(parsed.symbols.len());
    for symbol in &parsed.symbols {
        let element = Element::from_symbol(symbol).ok_or_else(|| FerroxError::JsonError {
            path: "inline".to_string(),
            reason: format!("Unknown element symbol: {symbol}"),
        })?;
        species.push(Species::neutral(element));
    }

    // Parse coordinates
    let cart_coords: Vec<Vector3<f64>> = parsed
        .positions
        .iter()
        .map(|pos| Vector3::new(pos[0], pos[1], pos[2]))
        .collect();

    // Check if periodic (has cell and at least one pbc direction)
    let is_periodic = parsed.cell.is_some() && parsed.pbc.iter().any(|&p| p);

    // Extract charge from info (used by both branches)
    let charge = parsed
        .info
        .get("charge")
        .and_then(|v| v.as_f64())
        .unwrap_or(0.0);

    if is_periodic {
        // Create periodic Structure
        // ASE cell is row-major: cell[0] = a vector, cell[1] = b vector, cell[2] = c vector
        let cell = parsed.cell.unwrap();
        let matrix = nalgebra::Matrix3::from_row_slice(&[
            cell[0][0], cell[0][1], cell[0][2], cell[1][0], cell[1][1], cell[1][2], cell[2][0],
            cell[2][1], cell[2][2],
        ]);
        let mut lattice = Lattice::new(matrix);
        lattice.pbc = parsed.pbc;

        // Convert Cartesian to fractional
        let frac_coords = lattice.get_fractional_coords(&cart_coords);

        // Extract properties from info (excluding charge which is a dedicated field)
        let properties: HashMap<String, serde_json::Value> = parsed
            .info
            .into_iter()
            .filter(|(k, _)| k != "charge")
            .collect();

        // Use try_new_full to preserve pbc and charge from ASE
        let pbc = parsed.pbc;
        #[allow(deprecated)]
        Ok(StructureOrMolecule::Structure(Structure::try_new_full(
            lattice,
            species.into_iter().map(SiteOccupancy::ordered).collect(),
            frac_coords,
            pbc,
            charge,
            properties,
        )?))
    } else {
        // Create non-periodic Structure (molecule)
        let properties: HashMap<String, serde_json::Value> = parsed
            .info
            .into_iter()
            .filter(|(k, _)| k != "charge")
            .collect();

        #[allow(deprecated)]
        Ok(StructureOrMolecule::Molecule(Structure::try_new_molecule(
            species,
            cart_coords,
            charge,
            properties,
        )?))
    }
}

/// Convert a Structure to ASE Atoms dict format.
///
/// # Arguments
///
/// * `structure` - The structure to convert
///
/// # Returns
///
/// JSON Value in ASE Atoms dict format.
pub fn structure_to_ase_atoms_dict(structure: &Structure) -> serde_json::Value {
    use serde_json::json;

    // Get symbols (dominant species for each site)
    let symbols: Vec<&str> = structure
        .site_occupancies
        .iter()
        .map(|so| so.dominant_species().element.symbol())
        .collect();

    // Get Cartesian positions
    let cart_coords = structure.cart_coords();
    let positions: Vec<[f64; 3]> = cart_coords.iter().map(|c| [c.x, c.y, c.z]).collect();

    // Get cell matrix (row vectors)
    let mat = structure.lattice.matrix();
    let cell = [
        [mat[(0, 0)], mat[(0, 1)], mat[(0, 2)]],
        [mat[(1, 0)], mat[(1, 1)], mat[(1, 2)]],
        [mat[(2, 0)], mat[(2, 1)], mat[(2, 2)]],
    ];

    // Build info dict from properties, including charge if non-zero
    let mut info: serde_json::Map<String, serde_json::Value> =
        structure.properties.clone().into_iter().collect();
    if structure.charge.abs() > 1e-10 {
        info.insert("charge".to_string(), json!(structure.charge));
    }

    json!({
        "symbols": symbols,
        "positions": positions,
        "cell": cell,
        "pbc": structure.pbc,
        "info": info
    })
}

/// Convert a non-periodic structure (molecule) to ASE Atoms dict format.
///
/// # Arguments
///
/// * `structure` - The structure to convert (should have `pbc = [false, false, false]`)
///
/// # Returns
///
/// JSON Value in ASE Atoms dict format (with pbc=[false, false, false]).
pub fn molecule_to_ase_atoms_dict(structure: &Structure) -> serde_json::Value {
    use serde_json::json;

    // Get symbols (dominant species for each site)
    let symbols: Vec<&str> = structure
        .site_occupancies
        .iter()
        .map(|so| so.dominant_species().element.symbol())
        .collect();

    // Get Cartesian positions
    let cart_coords = structure.cart_coords();
    let positions: Vec<[f64; 3]> = cart_coords.iter().map(|c| [c.x, c.y, c.z]).collect();

    // Build info dict from properties, including charge
    let mut info: serde_json::Map<String, serde_json::Value> =
        structure.properties.clone().into_iter().collect();
    if structure.charge.abs() > 1e-10 {
        info.insert("charge".to_string(), json!(structure.charge));
    }

    json!({
        "symbols": symbols,
        "positions": positions,
        "cell": serde_json::Value::Null,
        "pbc": [false, false, false],
        "info": info
    })
}

/// Batch convert structures to ASE Atoms dicts.
///
/// # Arguments
///
/// * `structures` - Slice of structures to convert
///
/// # Returns
///
/// Vector of JSON Values in ASE Atoms dict format.
pub fn structures_to_ase_atoms_dicts(structures: &[Structure]) -> Vec<serde_json::Value> {
    structures.iter().map(structure_to_ase_atoms_dict).collect()
}

/// Batch convert non-periodic structures (molecules) to ASE Atoms dicts.
///
/// # Arguments
///
/// * `structures` - Slice of structures to convert (should have `pbc = [false, false, false]`)
///
/// # Returns
///
/// Vector of JSON Values in ASE Atoms dict format.
pub fn molecules_to_ase_atoms_dicts(structures: &[Structure]) -> Vec<serde_json::Value> {
    structures.iter().map(molecule_to_ase_atoms_dict).collect()
}

/// Convert ASE Atoms dict JSON string to pymatgen JSON.
///
/// This is a convenience function for conversion between formats.
/// Returns Structure JSON for periodic systems, Molecule JSON for non-periodic.
///
/// # Arguments
///
/// * `ase_json` - JSON string in ASE Atoms dict format
///
/// # Returns
///
/// JSON string in pymatgen format (Structure or Molecule based on pbc).
#[allow(deprecated)]
pub fn ase_atoms_to_pymatgen_json(ase_json: &str) -> Result<String> {
    match parse_ase_atoms_json(ase_json)? {
        StructureOrMolecule::Structure(s) => Ok(structure_to_pymatgen_json(&s)),
        StructureOrMolecule::Molecule(m) => Ok(molecule_to_pymatgen_json(&m)),
    }
}

/// Parse an XYZ file, returning either a Structure or Molecule.
///
/// If the file contains lattice information (extXYZ format), returns a Structure.
/// Otherwise, returns a Molecule.
///
/// # Arguments
///
/// * `path` - Path to the XYZ file
///
/// # Returns
///
/// Either a Structure (if lattice present) or non-periodic Structure (if no lattice).
#[allow(deprecated)]
pub fn parse_xyz_flexible(path: &Path) -> Result<StructureOrMolecule> {
    let path_str = path.to_string_lossy().to_string();
    let mut frames =
        extxyz::read_xyz_frames(&path_str, 0..).map_err(|e| FerroxError::ParseError {
            path: path.display().to_string(),
            reason: format!("XYZ read error: {e}"),
        })?;

    let frame = frames.next().ok_or_else(|| FerroxError::EmptyFile {
        path: path.display().to_string(),
    })?;

    let atoms = extxyz::RawAtoms::parse_from(&frame).map_err(|e| FerroxError::ParseError {
        path: path.display().to_string(),
        reason: format!("XYZ parse error: {e}"),
    })?;

    // Try to parse comment line - plain XYZ comments won't parse as extXYZ info, that's OK
    let info: extxyz::Info = atoms.comment.parse().unwrap_or_default();

    // Check if lattice is present
    if info.get("Lattice").is_some() {
        // Has lattice - parse as periodic structure
        Ok(StructureOrMolecule::Structure(frame_to_structure(
            &frame, path,
        )?))
    } else {
        // No lattice - parse as non-periodic structure (molecule)
        Ok(StructureOrMolecule::Molecule(frame_to_molecule(
            &frame, path,
        )?))
    }
}
