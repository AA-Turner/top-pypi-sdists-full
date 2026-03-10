use crate::element::Element;
use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use crate::species::Species;
use crate::structure::Structure;
use nalgebra::Vector3;
use std::path::Path;

use super::lammps::read_file_maybe_gzipped;

// === XDATCAR Parser ===

/// Parse the POSCAR-like header of an XDATCAR file (lines 0-6).
///
/// Returns `(lattice, species, total_atoms)` where species is already expanded
/// by element counts.
fn parse_xdatcar_header(lines: &[&str], path: &str) -> Result<(Lattice, Vec<Species>, usize)> {
    let err = |reason: String| FerroxError::ParseError {
        path: path.to_string(),
        reason,
    };

    if lines.len() < 8 {
        return Err(err("XDATCAR must have at least 8 lines".to_string()));
    }

    // Line 1: scale factor
    let scale_str = lines[1].trim();
    let scale: f64 = scale_str
        .parse()
        .map_err(|_| err(format!("Invalid scale factor: '{scale_str}'")))?;
    if !scale.is_finite() || scale == 0.0 {
        return Err(err(format!(
            "Scale factor must be finite and non-zero, got '{scale_str}'"
        )));
    }

    // Lines 2-4: lattice vectors
    let mut lattice_vecs = [[0.0f64; 3]; 3];
    for (idx, line) in lines[2..5].iter().enumerate() {
        let parts: Vec<f64> = line
            .split_whitespace()
            .take(3)
            .map(|s| {
                s.parse()
                    .map_err(|_| err(format!("Invalid lattice vector component: '{s}'")))
            })
            .collect::<Result<_>>()?;
        if parts.len() != 3 {
            return Err(err(format!(
                "Lattice vector {} must have 3 components, got {}",
                idx + 1,
                parts.len()
            )));
        }
        lattice_vecs[idx] = [parts[0], parts[1], parts[2]];
    }

    // Handle negative scale = volume specification (same as POSCAR convention)
    let effective_scale = if scale < 0.0 {
        let det = lattice_vecs[0][0]
            * (lattice_vecs[1][1] * lattice_vecs[2][2] - lattice_vecs[1][2] * lattice_vecs[2][1])
            - lattice_vecs[0][1]
                * (lattice_vecs[1][0] * lattice_vecs[2][2]
                    - lattice_vecs[1][2] * lattice_vecs[2][0])
            + lattice_vecs[0][2]
                * (lattice_vecs[1][0] * lattice_vecs[2][1]
                    - lattice_vecs[1][1] * lattice_vecs[2][0]);
        (scale.abs() / det.abs()).powf(1.0 / 3.0)
    } else {
        scale
    };

    let matrix = nalgebra::Matrix3::from_row_slice(&[
        lattice_vecs[0][0] * effective_scale,
        lattice_vecs[0][1] * effective_scale,
        lattice_vecs[0][2] * effective_scale,
        lattice_vecs[1][0] * effective_scale,
        lattice_vecs[1][1] * effective_scale,
        lattice_vecs[1][2] * effective_scale,
        lattice_vecs[2][0] * effective_scale,
        lattice_vecs[2][1] * effective_scale,
        lattice_vecs[2][2] * effective_scale,
    ]);
    let lattice = Lattice::new(matrix);

    // Line 5: element symbols
    let symbols: Vec<&str> = lines[5].split_whitespace().collect();
    // Line 6: element counts
    let counts: Vec<usize> = lines[6]
        .split_whitespace()
        .map(|s| {
            s.parse::<usize>()
                .map_err(|_| err(format!("Invalid element count: '{s}'")))
        })
        .collect::<Result<_>>()?;

    if symbols.len() != counts.len() {
        return Err(err(format!(
            "Element names/counts mismatch: {} names vs {} counts",
            symbols.len(),
            counts.len()
        )));
    }

    if counts.contains(&0) {
        return Err(err("Element counts must be positive".to_string()));
    }

    // Expand to per-atom species list
    let mut species = Vec::new();
    for (symbol, &count) in symbols.iter().zip(counts.iter()) {
        let element = Element::from_symbol(symbol)
            .ok_or_else(|| err(format!("Unknown element symbol: '{symbol}'")))?;
        for _ in 0..count {
            species.push(Species::neutral(element));
        }
    }

    let total_atoms: usize = counts.iter().sum();
    Ok((lattice, species, total_atoms))
}

/// Parse all frames from an XDATCAR string, returning structures for each frame.
///
/// The XDATCAR format consists of a POSCAR-like header (comment, scale factor,
/// lattice vectors, element names, counts) followed by sequential frames of
/// fractional coordinates, each preceded by a `Direct configuration= N` line.
///
/// # Arguments
///
/// * `content` - XDATCAR file content as a string
///
/// # Returns
///
/// Vector of `Result<Structure>` for each frame found.
pub fn parse_xdatcar_trajectory_str(content: &str) -> Vec<Result<Structure>> {
    let lines: Vec<&str> = content.lines().collect();
    let (lattice, species, total_atoms) = match parse_xdatcar_header(&lines, "inline") {
        Ok(header) => header,
        Err(err) => return vec![Err(err)],
    };

    let mut frames = Vec::new();
    let mut line_idx = 7;

    while line_idx < lines.len() {
        // Find next "Direct configuration=" line
        let config_idx = lines[line_idx..]
            .iter()
            .position(|line| {
                let trimmed = line.trim().to_lowercase();
                trimmed.starts_with("direct")
            })
            .map(|offset| line_idx + offset);

        let Some(config_idx) = config_idx else {
            break;
        };

        line_idx = config_idx + 1;

        // Parse fractional coordinates for this frame
        let frame_result = (|| -> Result<Structure> {
            let err = |reason: String| FerroxError::ParseError {
                path: "inline".to_string(),
                reason,
            };

            let mut frac_coords = Vec::with_capacity(total_atoms);
            for atom_idx in 0..total_atoms {
                let coord_line_idx = line_idx + atom_idx;
                if coord_line_idx >= lines.len() {
                    return Err(err(format!(
                        "Frame truncated: expected {total_atoms} atoms but only found {atom_idx}"
                    )));
                }

                let parts: Vec<&str> = lines[coord_line_idx].split_whitespace().collect();
                if parts.len() < 3 {
                    return Err(err(format!(
                        "Coordinate line must have at least 3 values, got {}",
                        parts.len()
                    )));
                }

                let x: f64 = parts[0]
                    .parse()
                    .map_err(|_| err(format!("Invalid x coordinate: '{}'", parts[0])))?;
                let y: f64 = parts[1]
                    .parse()
                    .map_err(|_| err(format!("Invalid y coordinate: '{}'", parts[1])))?;
                let z: f64 = parts[2]
                    .parse()
                    .map_err(|_| err(format!("Invalid z coordinate: '{}'", parts[2])))?;

                if !x.is_finite() || !y.is_finite() || !z.is_finite() {
                    return Err(err(format!(
                        "Non-finite coordinate at atom {}: ({x}, {y}, {z})",
                        atom_idx + 1
                    )));
                }

                frac_coords.push(Vector3::new(x, y, z));
            }

            Structure::try_new(lattice.clone(), species.clone(), frac_coords)
        })();

        frames.push(frame_result);
        line_idx += total_atoms;
    }

    frames
}

/// Parse all frames from an XDATCAR trajectory file.
///
/// # Arguments
///
/// * `path` - Path to the XDATCAR file
///
/// # Returns
///
/// Vector of `Result<Structure>` for each frame.
pub fn parse_xdatcar_trajectory(path: &Path) -> Result<Vec<Result<Structure>>> {
    let content = read_file_maybe_gzipped(path)?;
    Ok(parse_xdatcar_trajectory_str(&content))
}

/// Parse a single structure from an XDATCAR string (first frame only).
///
/// For multi-frame content, use [`parse_xdatcar_trajectory_str`].
///
/// # Arguments
///
/// * `content` - XDATCAR file content as a string
///
/// # Returns
///
/// The parsed structure from the first frame.
pub fn parse_xdatcar_str(content: &str) -> Result<Structure> {
    let frames = parse_xdatcar_trajectory_str(content);
    match frames.into_iter().next() {
        Some(result) => result,
        None => Err(FerroxError::EmptyFile {
            path: "inline".to_string(),
        }),
    }
}

/// Parse a single structure from an XDATCAR file (first frame only).
///
/// For multi-frame trajectory files, use [`parse_xdatcar_trajectory`].
///
/// # Arguments
///
/// * `path` - Path to the XDATCAR file
///
/// # Returns
///
/// The parsed structure from the first frame.
pub fn parse_xdatcar(path: &Path) -> Result<Structure> {
    let content = read_file_maybe_gzipped(path)?;
    parse_xdatcar_str(&content)
}
