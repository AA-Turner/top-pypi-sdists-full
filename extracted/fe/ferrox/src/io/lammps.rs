use crate::element::Element;
use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use crate::species::Species;
use crate::structure::Structure;
use std::path::Path;

// === LAMMPS Dump Parsers ===

/// Parse a 3x3 lattice matrix from LAMMPS box bounds lines.
///
/// Orthogonal boxes have 2 columns per line (lo, hi).
/// Triclinic boxes have 3 columns (lo_bound, hi_bound, tilt).
/// See https://docs.lammps.org/Howto_triclinic.html
/// Returns (lattice_matrix, box_origin) where box_origin is (xlo, ylo, zlo).
fn parse_lammps_box(
    box_lines: [&str; 3],
    is_triclinic: bool,
) -> std::result::Result<(nalgebra::Matrix3<f64>, nalgebra::Vector3<f64>), String> {
    let parse_row = |line: &str| -> std::result::Result<Vec<f64>, String> {
        line.split_whitespace()
            .map(|tok| {
                tok.parse::<f64>()
                    .map_err(|_| format!("invalid box bound value: {tok}"))
            })
            .collect()
    };

    let rows: Vec<Vec<f64>> = box_lines
        .iter()
        .map(|line| parse_row(line))
        .collect::<std::result::Result<_, _>>()?;

    if !is_triclinic {
        if rows.iter().any(|row| row.len() < 2) {
            return Err("orthogonal box bounds require 2 values per line".into());
        }
        let (xlo, ylo, zlo) = (rows[0][0], rows[1][0], rows[2][0]);
        let lx = rows[0][1] - xlo;
        let ly = rows[1][1] - ylo;
        let lz = rows[2][1] - zlo;
        return Ok((
            nalgebra::Matrix3::new(lx, 0.0, 0.0, 0.0, ly, 0.0, 0.0, 0.0, lz),
            nalgebra::Vector3::new(xlo, ylo, zlo),
        ));
    }

    // Triclinic: [lo_bound, hi_bound, tilt] with tilts xy, xz, yz
    if rows.iter().any(|row| row.len() < 3) {
        return Err("triclinic box bounds require 3 values per line".into());
    }
    let (xlo_b, xhi_b, xy) = (rows[0][0], rows[0][1], rows[0][2]);
    let (ylo_b, yhi_b, xz) = (rows[1][0], rows[1][1], rows[1][2]);
    let (zlo_b, zhi_b, yz) = (rows[2][0], rows[2][1], rows[2][2]);

    // True box origin after unslanting (LAMMPS convention)
    let xlo = xlo_b - f64::min(0.0, f64::min(xy, f64::min(xz, xy + xz)));
    let ylo = ylo_b - f64::min(0.0, yz);
    let zlo = zlo_b;

    let lx = xhi_b - f64::max(0.0, f64::max(xy, f64::max(xz, xy + xz))) - xlo_b
        + f64::min(0.0, f64::min(xy, f64::min(xz, xy + xz)));
    let ly = yhi_b - f64::max(0.0, yz) - ylo_b + f64::min(0.0, yz);
    let lz = zhi_b - zlo_b;

    Ok((
        nalgebra::Matrix3::new(lx, 0.0, 0.0, xy, ly, 0.0, xz, yz, lz),
        nalgebra::Vector3::new(xlo, ylo, zlo),
    ))
}

/// Map a LAMMPS integer atom type to an element.
///
/// Default mapping: type 1 -> H, type 2 -> He, ... (periodic table order).
fn lammps_type_to_element(atom_type: u8) -> Element {
    Element::from_atomic_number(atom_type).unwrap_or(Element::Dummy)
}

/// Parse a single LAMMPS dump frame from lines starting at `idx`.
///
/// Returns the parsed Structure and the updated line index, or None if no frame found.
fn parse_lammps_frame(
    lines: &[&str],
    start_idx: usize,
    path: &str,
) -> std::result::Result<Option<(Structure, usize)>, FerroxError> {
    let err = |reason: String| FerroxError::ParseError {
        path: path.to_string(),
        reason,
    };
    let mut idx = start_idx;
    let n_lines = lines.len();

    // Skip to ITEM: TIMESTEP
    while idx < n_lines && !lines[idx].starts_with("ITEM: TIMESTEP") {
        idx += 1;
    }
    if idx >= n_lines {
        return Ok(None);
    }
    idx += 1; // skip header
    if idx >= n_lines {
        return Err(err("unexpected end of file after ITEM: TIMESTEP".into()));
    }
    idx += 1; // skip timestep value

    // ITEM: NUMBER OF ATOMS
    while idx < n_lines && !lines[idx].starts_with("ITEM: NUMBER OF ATOMS") {
        idx += 1;
    }
    if idx >= n_lines {
        return Err(err("missing ITEM: NUMBER OF ATOMS".into()));
    }
    idx += 1;
    if idx >= n_lines {
        return Err(err("unexpected end of file after NUMBER OF ATOMS".into()));
    }
    let num_atoms: usize = lines[idx]
        .trim()
        .parse()
        .map_err(|_| err(format!("invalid atom count: {}", lines[idx].trim())))?;
    idx += 1;

    // ITEM: BOX BOUNDS
    while idx < n_lines && !lines[idx].starts_with("ITEM: BOX BOUNDS") {
        idx += 1;
    }
    if idx >= n_lines {
        return Err(err("missing ITEM: BOX BOUNDS".into()));
    }
    let box_header = lines[idx];
    let is_triclinic = box_header.contains("xy xz yz");

    let pbc = {
        let after_bounds = box_header
            .strip_prefix("ITEM: BOX BOUNDS")
            .unwrap_or("")
            .trim();
        // Remove "xy xz yz" prefix if triclinic
        let tokens_str = if is_triclinic {
            after_bounds
                .strip_prefix("xy xz yz")
                .unwrap_or(after_bounds)
                .trim()
        } else {
            after_bounds
        };
        let tokens: Vec<&str> = tokens_str.split_whitespace().collect();
        if tokens.len() >= 3 {
            [
                tokens[0].starts_with('p'),
                tokens[1].starts_with('p'),
                tokens[2].starts_with('p'),
            ]
        } else {
            [true, true, true]
        }
    };

    idx += 1;
    if idx + 3 > n_lines {
        return Err(err("incomplete box bounds".into()));
    }
    let (lattice_matrix, box_origin) =
        parse_lammps_box([lines[idx], lines[idx + 1], lines[idx + 2]], is_triclinic)
            .map_err(&err)?;
    idx += 3;

    // ITEM: ATOMS
    while idx < n_lines && !lines[idx].starts_with("ITEM: ATOMS") {
        idx += 1;
    }
    if idx >= n_lines {
        return Err(err("missing ITEM: ATOMS".into()));
    }
    let atoms_header = lines[idx];
    let col_names: Vec<&str> = atoms_header
        .strip_prefix("ITEM: ATOMS")
        .unwrap_or("")
        .split_whitespace()
        .collect();
    let col_idx = |name: &str| {
        col_names
            .iter()
            .position(|&col| col.eq_ignore_ascii_case(name))
    };
    idx += 1;

    // Determine position columns: unwrapped > scaled > regular
    let (pos_cols, use_scaled) = if let (Some(px), Some(py), Some(pz)) =
        (col_idx("xu"), col_idx("yu"), col_idx("zu"))
    {
        ([px, py, pz], false)
    } else if let (Some(px), Some(py), Some(pz)) = (col_idx("xs"), col_idx("ys"), col_idx("zs")) {
        ([px, py, pz], true)
    } else if let (Some(px), Some(py), Some(pz)) = (col_idx("x"), col_idx("y"), col_idx("z")) {
        ([px, py, pz], false)
    } else {
        return Err(err(
            "LAMMPS ATOMS header missing position columns (x/y/z, xs/ys/zs, or xu/yu/zu)".into(),
        ));
    };

    let type_col = col_idx("type");
    let element_col = col_idx("element");

    if type_col.is_none() && element_col.is_none() {
        return Err(err(
            "LAMMPS ATOMS header missing identity column (type or element)".into(),
        ));
    }

    // Parse atom data
    let mut species_list = Vec::with_capacity(num_atoms);
    let mut positions = Vec::with_capacity(num_atoms);

    for _ in 0..num_atoms {
        if idx >= n_lines {
            break;
        }
        let parts: Vec<&str> = lines[idx].split_whitespace().collect();
        idx += 1;

        let max_needed = *pos_cols.iter().max().unwrap_or(&0);
        if parts.len() <= max_needed {
            continue;
        }

        let parse_f = |col: usize| -> std::result::Result<f64, FerroxError> {
            parts[col].parse::<f64>().map_err(|_| {
                err(format!(
                    "invalid coordinate value '{}' in column {col}",
                    parts[col]
                ))
            })
        };

        let raw_x = parse_f(pos_cols[0])?;
        let raw_y = parse_f(pos_cols[1])?;
        let raw_z = parse_f(pos_cols[2])?;

        let pos = if use_scaled {
            // Scaled coords are fractional [0,1) within the box — no origin shift needed
            let frac = nalgebra::Vector3::new(raw_x, raw_y, raw_z);
            lattice_matrix.transpose() * frac
        } else {
            // Cartesian coords are absolute — subtract box origin so
            // get_fractional_coords produces correct [0,1) fractions
            nalgebra::Vector3::new(raw_x, raw_y, raw_z) - box_origin
        };

        // Prefer explicit element names over heuristic type-to-element mapping
        let element = if let Some(ec) = element_col {
            if ec < parts.len() {
                Element::from_symbol(parts[ec]).unwrap_or(Element::Dummy)
            } else {
                Element::Dummy
            }
        } else if let Some(tc) = type_col {
            if tc < parts.len() {
                let atom_type: u8 = parts[tc].parse().unwrap_or(1);
                lammps_type_to_element(atom_type)
            } else {
                Element::Dummy
            }
        } else {
            Element::Dummy
        };

        species_list.push(Species::neutral(element));
        positions.push(pos);
    }

    if positions.is_empty() {
        return Err(err("no atoms parsed in LAMMPS frame".into()));
    }
    if positions.len() != num_atoms {
        return Err(err(format!(
            "expected {num_atoms} atoms but parsed only {}",
            positions.len()
        )));
    }

    let lattice = Lattice::from_matrix_with_pbc(lattice_matrix, pbc);
    // Convert Cartesian positions to fractional
    let frac_coords = lattice.get_fractional_coords(&positions);

    let structure = Structure::new(lattice, species_list, frac_coords);
    Ok(Some((structure, idx)))
}

/// Read a file as a string, auto-detecting gzip from the `.gz` extension.
pub(super) fn read_file_maybe_gzipped(path: &Path) -> Result<String> {
    use std::io::Read;
    let file = std::fs::File::open(path)?;
    let mut content = String::new();
    if path.extension().and_then(|ext| ext.to_str()) == Some("gz") {
        flate2::read::GzDecoder::new(file).read_to_string(&mut content)?;
    } else {
        std::io::BufReader::new(file).read_to_string(&mut content)?;
    }
    Ok(content)
}

/// Parse a single structure from a LAMMPS dump file (plain or gzipped).
///
/// For multi-frame trajectory files, only the first frame is returned.
/// Use [`parse_lammps_trajectory`] to get all frames.
pub fn parse_lammps_dump(path: &Path) -> Result<Structure> {
    let content = read_file_maybe_gzipped(path)?;
    parse_lammps_dump_str(&content)
}

/// Parse a single structure from a LAMMPS dump string.
///
/// Only the first frame is parsed. For multi-frame content, use
/// [`parse_lammps_trajectory_str`].
pub fn parse_lammps_dump_str(content: &str) -> Result<Structure> {
    let lines: Vec<&str> = content.lines().collect();
    match parse_lammps_frame(&lines, 0, "inline")? {
        Some((structure, _)) => Ok(structure),
        None => Err(FerroxError::EmptyFile {
            path: "inline".to_string(),
        }),
    }
}

/// Parse all frames from a LAMMPS dump/trajectory file (plain or gzipped).
pub fn parse_lammps_trajectory(path: &Path) -> Result<Vec<Result<Structure>>> {
    let content = read_file_maybe_gzipped(path)?;
    Ok(parse_lammps_trajectory_str(&content))
}

/// Parse all frames from a LAMMPS dump/trajectory string.
pub fn parse_lammps_trajectory_str(content: &str) -> Vec<Result<Structure>> {
    let lines: Vec<&str> = content.lines().collect();
    let mut frames = Vec::new();
    let mut idx = 0;
    loop {
        match parse_lammps_frame(&lines, idx, "inline") {
            Ok(Some((structure, next_idx))) => {
                frames.push(Ok(structure));
                idx = next_idx;
            }
            Ok(None) => break,
            Err(err) => {
                frames.push(Err(err));
                break;
            }
        }
    }
    frames
}
