use crate::element::Element;
use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use crate::species::Species;
use crate::structure::Structure;
use nalgebra::Vector3;
use std::path::Path;

// === POSCAR Parser ===

/// Parse a structure from VASP POSCAR format.
///
/// Supports VASP 5+ format with element symbols. VASP 4 format (without symbols)
/// is not supported and will return an error.
///
/// # Arguments
///
/// * `path` - Path to the POSCAR/CONTCAR file
///
/// # Returns
///
/// The parsed structure or an error if parsing fails.
pub fn parse_poscar(path: &Path) -> Result<Structure> {
    let content = std::fs::read_to_string(path)?;
    parse_poscar_str_impl(&content, &path.display().to_string())
}

/// Parse a structure from POSCAR content string.
///
/// # Arguments
///
/// * `content` - POSCAR file content as string
///
/// # Returns
///
/// The parsed structure or an error if parsing fails.
pub fn parse_poscar_str(content: &str) -> Result<Structure> {
    parse_poscar_str_impl(content, "inline")
}

/// Internal POSCAR parser implementation.
///
/// POSCAR format (VASP 5+):
/// ```text
/// Comment line
/// scale_factor (positive) OR -volume (negative)
/// a1 a2 a3       # lattice vector a
/// b1 b2 b3       # lattice vector b
/// c1 c2 c3       # lattice vector c
/// El1 El2 ...    # element symbols (VASP 5+)
/// N1 N2 ...      # atom counts per element
/// [Selective dynamics]  # optional
/// Direct|Cartesian      # coordinate type
/// x1 y1 z1 [T T T] [El] # coordinates with optional selective dynamics and element
/// ...
/// ```
fn parse_poscar_str_impl(content: &str, path: &str) -> Result<Structure> {
    let err = |reason: String| FerroxError::ParseError {
        path: path.to_string(),
        reason,
    };

    // Split into non-empty lines, preserving original for coordinate parsing
    let lines: Vec<&str> = content.lines().collect();
    if lines.len() < 8 {
        return Err(err("POSCAR must have at least 8 lines".to_string()));
    }

    // Line 0: Comment (ignored)
    // Line 1: Scale factor
    let scale_str = lines[1].trim();
    let scale_raw: f64 = scale_str
        .parse()
        .map_err(|_| err(format!("Invalid scale factor: '{scale_str}'")))?;
    if !scale_raw.is_finite() || scale_raw == 0.0 {
        return Err(err(format!(
            "Scale factor must be finite and non-zero, got '{scale_str}'"
        )));
    }

    // Lines 2-4: Lattice vectors (3x3)
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
        if !parts.iter().all(|v| v.is_finite()) {
            return Err(err(format!(
                "Non-finite lattice vector component in vector {}",
                idx + 1
            )));
        }
        lattice_vecs[idx] = [parts[0], parts[1], parts[2]];
    }

    // Compute actual scale factor (handle negative = volume specification)
    let scale = if scale_raw < 0.0 {
        // Negative scale means the absolute value is the desired volume
        let det = lattice_vecs[0][0]
            * (lattice_vecs[1][1] * lattice_vecs[2][2] - lattice_vecs[1][2] * lattice_vecs[2][1])
            - lattice_vecs[0][1]
                * (lattice_vecs[1][0] * lattice_vecs[2][2]
                    - lattice_vecs[1][2] * lattice_vecs[2][0])
            + lattice_vecs[0][2]
                * (lattice_vecs[1][0] * lattice_vecs[2][1]
                    - lattice_vecs[1][1] * lattice_vecs[2][0]);
        (scale_raw.abs() / det.abs()).powf(1.0 / 3.0)
    } else {
        scale_raw
    };

    // Build scaled lattice matrix
    let matrix = nalgebra::Matrix3::from_row_slice(&[
        lattice_vecs[0][0] * scale,
        lattice_vecs[0][1] * scale,
        lattice_vecs[0][2] * scale,
        lattice_vecs[1][0] * scale,
        lattice_vecs[1][1] * scale,
        lattice_vecs[1][2] * scale,
        lattice_vecs[2][0] * scale,
        lattice_vecs[2][1] * scale,
        lattice_vecs[2][2] * scale,
    ]);
    let lattice = Lattice::new(matrix);

    // Line 5: Either element symbols (VASP 5+) or atom counts (VASP 4)
    let line5_parts: Vec<&str> = lines[5].split_whitespace().collect();

    // VASP 4 format (no element symbols) - reject early
    if line5_parts
        .first()
        .is_some_and(|s| s.parse::<usize>().is_ok())
    {
        return Err(err(
            "VASP 4 format (no element symbols) not supported. Use VASP 5+ format.".to_string(),
        ));
    }

    // Clean VASP 6.4.2+ POTCAR hash format (e.g., "Mg_pv/f474ac0d" -> "Mg")
    let clean_symbol = |s: &str| {
        s.split('/')
            .next()
            .unwrap_or(s)
            .split('_')
            .next()
            .unwrap_or(s)
            .to_string()
    };

    // VASP 5+ format - line 5 is element symbols
    let mut all_symbols: Vec<String> = line5_parts.iter().map(|s| clean_symbol(s)).collect();
    let mut all_counts = Vec::new();
    let mut line_idx = 6;

    // Handle multi-line symbols/counts (atoms > 20 groups wrap to multiple lines)
    // POSCAR format: symbols come first, then counts, then coordinate type
    // Once we've read ANY counts, we stop looking for more symbols
    let mut reading_counts = false;
    while line_idx < lines.len() {
        let line = lines[line_idx].trim();
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.is_empty() {
            line_idx += 1;
            continue;
        }

        // Check if first part is a number (counts line)
        if parts[0].parse::<usize>().is_ok() {
            reading_counts = true;
            for part in &parts {
                let count: usize = part
                    .parse()
                    .map_err(|_| err(format!("Invalid atom count: '{part}'")))?;
                all_counts.push(count);
            }
            line_idx += 1;
            continue;
        }

        // If we've already started reading counts, this must be the coordinate type line
        // (prevents "c" for Cartesian being matched as Carbon element)
        if reading_counts {
            break;
        }

        // Check if first part is a valid element symbol (more symbols line)
        // Only valid before we start reading counts
        let first_cleaned = clean_symbol(parts[0]);
        if Element::from_symbol(&first_cleaned).is_some() {
            for part in &parts {
                all_symbols.push(clean_symbol(part));
            }
            line_idx += 1;
            continue;
        }

        // Not counts and not element symbols - must be coordinate type line (Direct/Cartesian/Selective)
        break;
    }

    let (symbols, counts, coord_line_start) = (all_symbols, all_counts, line_idx);

    if symbols.len() != counts.len() {
        return Err(err(format!(
            "Number of element symbols ({}) doesn't match number of counts ({})",
            symbols.len(),
            counts.len()
        )));
    }

    // Validate and expand element symbols
    let mut species = Vec::new();
    for (symbol, &count) in symbols.iter().zip(counts.iter()) {
        let element = Element::from_symbol(symbol)
            .ok_or_else(|| err(format!("Unknown element symbol: '{symbol}'")))?;
        for _ in 0..count {
            species.push(Species::neutral(element));
        }
    }

    let total_atoms: usize = counts.iter().sum();

    // Find coordinate type line (Direct/Cartesian or Selective dynamics)
    let mut coord_start = coord_line_start;
    if coord_start >= lines.len() {
        return Err(err("Missing coordinate type line".to_string()));
    }

    // Skip optional "Selective dynamics" line
    if lines[coord_start].trim().to_lowercase().starts_with('s') {
        coord_start += 1;
        if coord_start >= lines.len() {
            return Err(err(
                "Missing coordinate type line after Selective dynamics".to_string()
            ));
        }
    }

    let is_cartesian = lines[coord_start].trim().to_lowercase().starts_with('c');
    coord_start += 1;

    // Parse coordinates
    let mut coords = Vec::with_capacity(total_atoms);
    for idx in 0..total_atoms {
        let line_idx = coord_start + idx;
        if line_idx >= lines.len() {
            return Err(err(format!(
                "Expected {} coordinates but only found {}",
                total_atoms, idx
            )));
        }

        let line = lines[line_idx];
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() < 3 {
            return Err(err(format!(
                "Coordinate line {} must have at least 3 values",
                idx + 1
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
                idx + 1
            )));
        }

        coords.push(Vector3::new(x, y, z));
    }

    // Convert to fractional if Cartesian (apply scale)
    let frac_coords = if is_cartesian {
        let cart_coords: Vec<Vector3<f64>> = coords
            .into_iter()
            .map(|c| Vector3::new(c.x * scale, c.y * scale, c.z * scale))
            .collect();
        lattice.get_fractional_coords(&cart_coords)
    } else {
        coords
    };

    Structure::try_new(lattice, species, frac_coords)
}
