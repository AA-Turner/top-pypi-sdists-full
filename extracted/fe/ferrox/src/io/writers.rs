use crate::error::{FerroxError, Result};
use crate::species::OCCUPANCY_TOL;
use crate::structure::Structure;
use std::collections::HashMap;
use std::path::Path;

use super::unified_api::{StructureFormat, structure_to_pymatgen_json};

// === Structure Writers ===

/// Convert a structure to VASP POSCAR format string.
///
/// The output uses VASP 5+ format with element symbols.
///
/// # Arguments
///
/// * `structure` - The structure to serialize
/// * `comment` - Optional comment line (defaults to reduced formula)
///
/// # Returns
///
/// POSCAR format string.
///
/// # Example
///
/// ```rust,ignore
/// let poscar_string = structure_to_poscar(&structure, None);
/// ```
pub fn structure_to_poscar(structure: &Structure, comment: Option<&str>) -> String {
    let mat = structure.lattice.matrix();

    // Check for disordered/partial-occupancy sites and collect warnings
    // POSCAR format cannot represent multi-species or partial occupancy sites
    let warnings: Vec<String> = structure
        .site_occupancies
        .iter()
        .enumerate()
        .filter_map(|(idx, site_occ)| {
            let total_occ = site_occ.total_occupancy();
            let is_disordered = !site_occ.is_ordered();
            let has_partial_occ = (total_occ - 1.0).abs() > OCCUPANCY_TOL;

            if !is_disordered && !has_partial_occ {
                return None;
            }

            let species_str = site_occ
                .species
                .iter()
                .map(|(sp, occ)| format!("{sp}:{occ:.3}"))
                .collect::<Vec<_>>()
                .join(", ");
            let dominant = site_occ.dominant_species();

            Some(if is_disordered && has_partial_occ {
                format!(
                    "  Site {idx}: disordered+partial (total={total_occ:.3}): [{species_str}] -> {dominant}"
                )
            } else if is_disordered {
                format!("  Site {idx}: disordered: [{species_str}] -> {dominant}")
            } else {
                format!("  Site {idx}: partial occupancy (total={total_occ:.3}): [{species_str}]")
            })
        })
        .collect();

    if !warnings.is_empty() {
        tracing::warn!(
            "POSCAR cannot represent disorder/partial occupancy. {} site(s) simplified:\n{}",
            warnings.len(),
            warnings.join("\n")
        );
    }

    // Group sites by element (POSCAR requires contiguous blocks)
    // Use IndexMap to preserve insertion order (first occurrence)
    let mut element_sites: indexmap::IndexMap<&str, Vec<usize>> = indexmap::IndexMap::new();
    for (idx, site_occ) in structure.site_occupancies.iter().enumerate() {
        let symbol = site_occ.dominant_species().element.symbol();
        element_sites.entry(symbol).or_default().push(idx);
    }

    // Build the POSCAR string
    let mut lines = Vec::new();

    // Line 1: Comment (use provided or fall back to formula)
    lines.push(match comment {
        Some(c) if !c.is_empty() => c.to_string(),
        _ => structure.composition().reduced_formula(),
    });

    // Line 2: Scaling factor
    lines.push("1.0".to_string());

    // Lines 3-5: Lattice vectors (rows are a, b, c)
    for row in 0..3 {
        lines.push(format!(
            "  {:20.16}  {:20.16}  {:20.16}",
            mat[(row, 0)],
            mat[(row, 1)],
            mat[(row, 2)]
        ));
    }

    // Line 6: Element symbols
    let symbols: Vec<&str> = element_sites.keys().copied().collect();
    lines.push(format!("  {}", symbols.join("  ")));

    // Line 7: Element counts
    let counts: Vec<String> = element_sites
        .values()
        .map(|v| v.len().to_string())
        .collect();
    lines.push(format!("  {}", counts.join("  ")));

    // Line 8: Direct (fractional coordinates)
    lines.push("Direct".to_string());

    // Coordinate lines (in element order)
    for indices in element_sites.values() {
        for &idx in indices {
            let frac = &structure.frac_coords[idx];
            lines.push(format!(
                "  {:20.16}  {:20.16}  {:20.16}",
                frac.x, frac.y, frac.z
            ));
        }
    }

    lines.join("\n") + "\n"
}

/// Write a structure to a POSCAR file.
///
/// # Arguments
///
/// * `structure` - The structure to write
/// * `path` - Path to the output file
/// * `comment` - Optional comment line
///
/// # Returns
///
/// Result indicating success or file I/O error.
pub fn write_poscar(structure: &Structure, path: &Path, comment: Option<&str>) -> Result<()> {
    let content = structure_to_poscar(structure, comment);
    std::fs::write(path, content)?;
    Ok(())
}

/// Format a JSON value for extXYZ comment line.
/// Returns None for arrays/objects which can't be represented inline.
pub(super) fn format_extxyz_value(value: &serde_json::Value) -> Option<String> {
    match value {
        serde_json::Value::Number(n) => Some(n.to_string()),
        serde_json::Value::String(s) => {
            // Escape quotes, backslashes, and newlines to prevent malformed output
            let escaped = s
                .replace('\\', "\\\\")
                .replace('"', "\\\"")
                .replace('\n', "\\n");
            Some(format!("\"{}\"", escaped))
        }
        serde_json::Value::Bool(b) => Some(b.to_string()),
        _ => None, // Skip arrays/objects
    }
}

/// Convert a structure to extXYZ format string.
///
/// The output follows the extended XYZ format with lattice in the comment line.
///
/// # Arguments
///
/// * `structure` - The structure to serialize
/// * `properties` - Optional additional properties for the comment line
///
/// # Returns
///
/// extXYZ format string.
pub fn structure_to_extxyz(
    structure: &Structure,
    properties: Option<&HashMap<String, serde_json::Value>>,
) -> String {
    let mat = structure.lattice.matrix();
    let pbc = structure.lattice.pbc;

    // Line 1: Number of atoms
    let mut lines = vec![structure.num_sites().to_string()];

    // Line 2: Comment with Lattice and properties
    // Format: Lattice="ax ay az bx by bz cx cy cz" pbc="T T T" [other properties]
    let lattice_str = format!(
        "{:.10} {:.10} {:.10} {:.10} {:.10} {:.10} {:.10} {:.10} {:.10}",
        mat[(0, 0)],
        mat[(0, 1)],
        mat[(0, 2)],
        mat[(1, 0)],
        mat[(1, 1)],
        mat[(1, 2)],
        mat[(2, 0)],
        mat[(2, 1)],
        mat[(2, 2)]
    );

    let pbc_str = pbc.map(|b| if b { "T" } else { "F" }).join(" ");

    let mut comment_parts = vec![
        format!("Lattice=\"{}\"", lattice_str),
        format!("pbc=\"{}\"", pbc_str),
    ];

    // Add structure properties and additional properties
    let all_props = structure
        .properties
        .iter()
        .chain(properties.into_iter().flatten());
    for (key, value) in all_props {
        if key != "Lattice"
            && key != "pbc"
            && let Some(value_str) = format_extxyz_value(value)
        {
            comment_parts.push(format!("{}={}", key, value_str));
        }
    }

    lines.push(comment_parts.join(" "));

    // Atom lines: Element X Y Z (Cartesian coordinates)
    let cart_coords = structure.cart_coords();
    for (site_occ, cart) in structure.site_occupancies.iter().zip(cart_coords.iter()) {
        let symbol = site_occ.dominant_species().element.symbol();
        lines.push(format!(
            "{} {:20.16} {:20.16} {:20.16}",
            symbol, cart.x, cart.y, cart.z
        ));
    }

    lines.join("\n") + "\n"
}

/// Write a structure to an extXYZ file.
///
/// # Arguments
///
/// * `structure` - The structure to write
/// * `path` - Path to the output file
/// * `properties` - Optional additional properties
///
/// # Returns
///
/// Result indicating success or file I/O error.
pub fn write_extxyz(
    structure: &Structure,
    path: &Path,
    properties: Option<&HashMap<String, serde_json::Value>>,
) -> Result<()> {
    let content = structure_to_extxyz(structure, properties);
    std::fs::write(path, content)?;
    Ok(())
}

/// Write a structure to a file with automatic format detection.
///
/// The format is determined by the file extension:
/// - `.json` - Pymatgen JSON format
/// - `.cif` - CIF format
/// - `.xyz`, `.extxyz` - extXYZ format
/// - `.vasp`, `POSCAR*`, `CONTCAR*` - POSCAR format
///
/// # Arguments
///
/// * `structure` - The structure to write
/// * `path` - Path to the output file
///
/// # Returns
///
/// Result indicating success or error.
pub fn write_structure(structure: &Structure, path: &Path) -> Result<()> {
    let format = StructureFormat::from_path(path).ok_or_else(|| FerroxError::UnknownFormat {
        path: path.display().to_string(),
    })?;

    match format {
        StructureFormat::PymatgenJson => {
            std::fs::write(path, structure_to_pymatgen_json(structure))?;
        }
        StructureFormat::Poscar => write_poscar(structure, path, None)?,
        StructureFormat::ExtXyz => write_extxyz(structure, path, None)?,
        StructureFormat::Cif => crate::io::cif::write_cif(structure, path, None)?,
        StructureFormat::LammpsDump => {
            return Err(FerroxError::InvalidArgument {
                reason: "Writing LAMMPS dump format is not yet supported".to_string(),
            });
        }
        StructureFormat::Xdatcar => {
            return Err(FerroxError::InvalidArgument {
                reason: "Writing XDATCAR format is not yet supported".to_string(),
            });
        }
        StructureFormat::Optimade => {
            return Err(FerroxError::InvalidArgument {
                reason: "Writing OPTIMADE JSON format is not yet supported".to_string(),
            });
        }
    }
    Ok(())
}
