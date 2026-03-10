use crate::element::Element;
use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use crate::species::{SiteOccupancy, Species};
use crate::structure::Structure;
use nalgebra::Vector3;
use std::collections::HashMap;
use std::path::Path;

// === extXYZ Parser ===

/// Parse a single structure from an extXYZ file.
///
/// For multi-frame trajectory files, only the first frame is returned.
/// Use [`parse_extxyz_trajectory`] to get all frames.
///
/// # Arguments
///
/// * `path` - Path to the XYZ/extXYZ file
///
/// # Returns
///
/// The parsed structure or an error if parsing fails.
pub fn parse_extxyz(path: &Path) -> Result<Structure> {
    let frames = parse_extxyz_trajectory(path)?;
    frames
        .into_iter()
        .next()
        .ok_or_else(|| FerroxError::EmptyFile {
            path: path.display().to_string(),
        })?
}

/// Parse all frames from an extXYZ trajectory file.
///
/// Returns a vector of structures for all frames in the file.
///
/// # Arguments
///
/// * `path` - Path to the XYZ/extXYZ file
///
/// # Returns
///
/// Vector of `Result<Structure>` for each frame.
pub fn parse_extxyz_trajectory(path: &Path) -> Result<Vec<Result<Structure>>> {
    let path_str = path.to_string_lossy().to_string();
    // Use 0.. to read all frames
    let frames = extxyz::read_xyz_frames(&path_str, 0..).map_err(|e| FerroxError::ParseError {
        path: path.display().to_string(),
        reason: format!("extXYZ read error: {e}"),
    })?;

    Ok(frames
        .map(|frame| frame_to_structure(&frame, path))
        .collect())
}

pub(super) fn frame_to_structure(frame: &str, path: &Path) -> Result<Structure> {
    let atoms = extxyz::RawAtoms::parse_from(frame).map_err(|e| FerroxError::ParseError {
        path: path.display().to_string(),
        reason: format!("extXYZ parse error: {e}"),
    })?;

    // Parse comment line for lattice and properties
    let info: extxyz::Info = atoms.comment.parse().map_err(|e| FerroxError::ParseError {
        path: path.display().to_string(),
        reason: format!("extXYZ info parse error: {e}"),
    })?;

    // Extract lattice (REQUIRED for crystal structures)
    let lattice_value = info
        .get("Lattice")
        .ok_or_else(|| FerroxError::MissingLattice {
            path: path.display().to_string(),
        })?;

    // Parse lattice - format is "ax ay az bx by bz cx cy cz" as a JSON string or array
    let lattice_str = match lattice_value {
        serde_json::Value::String(s) => s.clone(),
        serde_json::Value::Array(arr) => {
            // Array of 9 numbers - reject non-numeric values with error (don't silently drop)
            let mut values = Vec::with_capacity(arr.len());
            for (idx, v) in arr.iter().enumerate() {
                let num = v.as_f64().ok_or_else(|| FerroxError::ParseError {
                    path: path.display().to_string(),
                    reason: format!("Lattice array element {idx} is not a number: {v}"),
                })?;
                values.push(num.to_string());
            }
            values.join(" ")
        }
        _ => {
            return Err(FerroxError::ParseError {
                path: path.display().to_string(),
                reason: "Lattice must be a string or array".to_string(),
            });
        }
    };

    let lattice_vals: Vec<f64> = lattice_str
        .split_whitespace()
        .map(|s| {
            s.parse::<f64>().map_err(|e| FerroxError::ParseError {
                path: path.display().to_string(),
                reason: format!("Invalid lattice value '{s}': {e}"),
            })
        })
        .collect::<Result<_>>()?;

    if lattice_vals.len() != 9 {
        return Err(FerroxError::ParseError {
            path: path.display().to_string(),
            reason: format!(
                "Lattice must have 9 values (3x3 matrix), got {}",
                lattice_vals.len()
            ),
        });
    }

    // Build lattice matrix (rows are lattice vectors a, b, c)
    let matrix = nalgebra::Matrix3::from_row_slice(&lattice_vals);
    let mut lattice = Lattice::new(matrix);

    // Parse PBC if present (default to [true, true, true])
    if let Some(pbc_value) = info.get("pbc") {
        lattice.pbc = parse_pbc_value(pbc_value);
    }

    // Parse species and coordinates
    let mut species = Vec::with_capacity(atoms.atoms.len());
    let mut cart_coords = Vec::with_capacity(atoms.atoms.len());

    for atom in &atoms.atoms {
        let element =
            Element::from_symbol(atom.element).ok_or_else(|| FerroxError::ParseError {
                path: path.display().to_string(),
                reason: format!("Unknown element symbol: {}", atom.element),
            })?;
        species.push(Species::neutral(element));

        // extXYZ uses Cartesian coordinates
        cart_coords.push(Vector3::new(
            atom.position[0],
            atom.position[1],
            atom.position[2],
        ));
    }

    // Convert Cartesian to fractional using Lattice method
    let frac_coords = lattice.get_fractional_coords(&cart_coords);

    // Extract properties (energy, charge, etc.)
    let mut properties = HashMap::new();
    let mut charge = 0.0;

    if let Some(energy_value) = info.get("energy")
        && let Some(energy) = energy_value.as_f64()
    {
        properties.insert("energy".to_string(), serde_json::json!(energy));
    }

    if let Some(charge_value) = info.get("charge")
        && let Some(ch) = charge_value.as_f64()
    {
        charge = ch;
    }

    // Store other info as properties (exclude structure-specific and already-handled keys)
    let skip_keys = ["Lattice", "pbc", "energy", "charge", "Properties"];
    for (key, value) in info.raw_map().iter() {
        if !skip_keys.contains(&key.as_str()) {
            properties.insert(key.to_string(), value.clone());
        }
    }

    // Use try_new_full to preserve pbc from lattice
    let pbc = lattice.pbc;
    Structure::try_new_full(
        lattice,
        species.into_iter().map(SiteOccupancy::ordered).collect(),
        frac_coords,
        pbc,
        charge,
        properties,
    )
}

fn parse_pbc_value(pbc_value: &serde_json::Value) -> [bool; 3] {
    match pbc_value {
        serde_json::Value::String(s) => {
            let parts: Vec<&str> = s.split_whitespace().collect();
            if parts.len() >= 3 {
                [
                    parts[0] == "T" || parts[0].eq_ignore_ascii_case("true"),
                    parts[1] == "T" || parts[1].eq_ignore_ascii_case("true"),
                    parts[2] == "T" || parts[2].eq_ignore_ascii_case("true"),
                ]
            } else {
                [true, true, true]
            }
        }
        serde_json::Value::Array(arr) if arr.len() >= 3 => [
            arr[0].as_bool().unwrap_or(true),
            arr[1].as_bool().unwrap_or(true),
            arr[2].as_bool().unwrap_or(true),
        ],
        _ => [true, true, true],
    }
}
