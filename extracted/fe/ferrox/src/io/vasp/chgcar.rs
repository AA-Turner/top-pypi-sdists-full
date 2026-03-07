//! CHGCAR parsing and Fourier coefficient extraction.
//!
//! Reads VASP CHGCAR (optionally gzipped) files, performs 3D FFT, and extracts
//! low-frequency Fourier coefficients within a |G| cutoff sphere. Supports
//! collinear spin-polarized (ISPIN=2) and non-spin-polarized files.
//!
//! Batch processing uses rayon for file-level parallelism and within-file
//! parallel 1D FFT slices.

use crate::element::Element;
use crate::error::{FerroxError, Result, check_positive};
use crate::lattice::Lattice;
use crate::species::{SiteOccupancy, Species};
use crate::structure::Structure;
use flate2::read::GzDecoder;
use nalgebra::{Matrix3, Vector3};
use rustfft::FftPlanner;
use rustfft::num_complex::Complex;
use serde::Serialize;
use std::collections::HashMap;
use std::f64::consts::PI;
use std::fs::File;
use std::io::{BufReader, Read};
use std::path::Path;
use std::sync::Arc;

#[cfg(feature = "rayon")]
use rayon::prelude::*;

/// Default |G| cutoff in Angstrom⁻¹.
pub const DEFAULT_G_MAX: f64 = 8.0;

/// Raw volumetric data from a CHGCAR file.
#[derive(Debug)]
pub struct ChgcarData {
    /// Crystal structure (lattice + sites).
    pub structure: Structure,
    /// Grid dimensions [NGX, NGY, NGZ].
    pub grid_shape: [usize; 3],
    /// Total charge density × volume, C-ordered [ix][iy][iz].
    pub total: Vec<f64>,
    /// Spin-difference charge density × volume (None if non-spin-polarized).
    pub diff: Option<Vec<f64>>,
}

/// Extracted Fourier coefficients and metadata.
#[derive(Debug, Serialize)]
pub struct FourierResult {
    /// Max Miller indices [H, K, L] stored.
    pub hkl_range: [i32; 3],
    /// |G| cutoff used (Å⁻¹).
    pub g_max: f64,
    /// Real-space lattice matrix (rows = vectors, Å).
    pub lattice: [[f64; 3]; 3],
    /// Reciprocal lattice with 2π (Å⁻¹).
    pub recip_lattice: [[f64; 3]; 3],
    /// Original VASP grid [NGX, NGY, NGZ].
    pub grid_shape: [usize; 3],
    /// Nyquist |G| of the VASP grid (Å⁻¹).
    pub g_nyquist: f64,
    /// Whether the source was spin-polarized (ISPIN=2).
    pub is_spin_polarized: bool,
    /// Total valence electron count.
    pub total_electrons: f64,
    /// Total magnetization (0 if non-spin-polarized).
    pub total_magnetization: f64,
    /// Shape of coefficient arrays (2H+1, 2K+1, 2L+1).
    pub coeff_shape: [usize; 3],
    /// Number of G-vectors inside the |G| sphere.
    pub n_coeffs_inside_sphere: usize,
    /// Real parts of Fourier coefficients (spin-up or total), flattened C-order.
    pub rho_real: Vec<f64>,
    /// Imaginary parts of Fourier coefficients (spin-up or total).
    pub rho_imag: Vec<f64>,
    /// Real parts for spin-down channel (only if spin-polarized).
    #[serde(skip_serializing_if = "Option::is_none")]
    pub rho_down_real: Option<Vec<f64>>,
    /// Imaginary parts for spin-down channel.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub rho_down_imag: Option<Vec<f64>>,
    /// Cell volume (ų).
    pub volume: f64,
}

/// Strip VASP 6 POTCAR suffixes like "Fe_pv" -> "Fe", "O/GW" -> "O".
fn clean_symbol(raw: &str) -> &str {
    raw.split('/')
        .next()
        .unwrap_or(raw)
        .split('_')
        .next()
        .unwrap_or(raw)
}

// === CHGCAR Parsing ===

/// Parse a VASP CHGCAR file (plain or gzipped).
pub fn parse_chgcar(path: &Path) -> Result<ChgcarData> {
    let file = File::open(path)?;

    let mut content = String::new();
    if path.extension().and_then(|e| e.to_str()) == Some("gz") {
        GzDecoder::new(file).read_to_string(&mut content)?;
    } else {
        BufReader::new(file).read_to_string(&mut content)?;
    }

    parse_chgcar_str(&content, &path.display().to_string())
}

/// Parse CHGCAR from a string.
fn parse_chgcar_str(content: &str, source: &str) -> Result<ChgcarData> {
    let err = |reason: String| FerroxError::ParseError {
        path: source.to_string(),
        reason,
    };

    let lines: Vec<&str> = content.lines().collect();
    if lines.len() < 10 {
        return Err(err("CHGCAR too short".to_string()));
    }

    // Line 0: comment
    // Line 1: scale factor (positive = multiplicative, negative = target volume)
    let scale_raw: f64 = lines[1]
        .trim()
        .parse()
        .map_err(|_| err("bad scale factor".to_string()))?;
    if scale_raw == 0.0 || !scale_raw.is_finite() {
        return Err(err(format!(
            "scale factor must be finite and non-zero, got {scale_raw}"
        )));
    }

    // Lines 2-4: lattice vectors (read raw first, scale applied after)
    let mut lattice_arr = [[0.0_f64; 3]; 3];
    for row_idx in 0..3 {
        let vals: Vec<f64> = lines[2 + row_idx]
            .split_whitespace()
            .map(|tok| tok.parse::<f64>())
            .collect::<std::result::Result<Vec<_>, _>>()
            .map_err(|_| err(format!("bad lattice vector line {}", 2 + row_idx)))?;
        if vals.len() < 3 {
            return Err(err(format!(
                "lattice vector line {} has <3 values",
                2 + row_idx
            )));
        }
        lattice_arr[row_idx][..3].copy_from_slice(&vals[..3]);
    }

    // Compute actual scale (negative means |scale_raw| is the desired cell volume)
    let scale = if scale_raw < 0.0 {
        let det = lattice_arr[0][0]
            * (lattice_arr[1][1] * lattice_arr[2][2] - lattice_arr[1][2] * lattice_arr[2][1])
            - lattice_arr[0][1]
                * (lattice_arr[1][0] * lattice_arr[2][2] - lattice_arr[1][2] * lattice_arr[2][0])
            + lattice_arr[0][2]
                * (lattice_arr[1][0] * lattice_arr[2][1] - lattice_arr[1][1] * lattice_arr[2][0]);
        (scale_raw.abs() / det.abs()).powf(1.0 / 3.0)
    } else {
        scale_raw
    };

    for val in lattice_arr.iter_mut().flatten() {
        *val *= scale;
    }
    let lattice = Lattice::from_array(lattice_arr);

    // Lines 5+: element symbols and counts (may wrap across multiple lines)
    let mut all_symbols: Vec<&str> = lines[5].split_whitespace().collect();
    let mut all_counts: Vec<usize> = Vec::new();
    let mut line_idx = 6;
    let mut reading_counts = false;

    while line_idx < lines.len() {
        let trimmed = lines[line_idx].trim();
        let parts: Vec<&str> = trimmed.split_whitespace().collect();
        if parts.is_empty() {
            line_idx += 1;
            continue;
        }

        if parts[0].parse::<usize>().is_ok() {
            reading_counts = true;
            for part in &parts {
                let count: usize = part
                    .parse()
                    .map_err(|_| err(format!("invalid atom count: '{part}'")))?;
                all_counts.push(count);
            }
            line_idx += 1;
            continue;
        }

        if reading_counts {
            break;
        }

        if Element::from_symbol(clean_symbol(parts[0])).is_some() {
            all_symbols.extend(parts);
            line_idx += 1;
            continue;
        }

        break;
    }

    if all_symbols.len() != all_counts.len() {
        return Err(err(format!(
            "element/count mismatch: {} symbols vs {} counts",
            all_symbols.len(),
            all_counts.len()
        )));
    }

    let n_atoms: usize = all_counts.iter().sum();

    // Next line: "Selective dynamics" or "Direct"/"Cartesian"
    let mut coord_line_idx = line_idx;
    if coord_line_idx < lines.len() && lines[coord_line_idx].trim().to_lowercase().starts_with('s')
    {
        coord_line_idx += 1;
    }

    if coord_line_idx >= lines.len() {
        return Err(err(
            "CHGCAR truncated: missing coordinate mode (Direct/Cartesian)".to_string(),
        ));
    }
    let is_cartesian = {
        let mode = lines[coord_line_idx].trim().to_lowercase();
        mode.starts_with('c') || mode.starts_with('k')
    };
    coord_line_idx += 1;

    // Parse atomic coordinates
    let mut frac_coords = Vec::with_capacity(n_atoms);
    let inv_matrix = if is_cartesian {
        Some(lattice.inv_matrix())
    } else {
        None
    };

    for atom_idx in 0..n_atoms {
        let line = lines
            .get(coord_line_idx + atom_idx)
            .ok_or_else(|| err(format!("missing coordinate line for atom {atom_idx}")))?;
        let vals: Vec<f64> = line
            .split_whitespace()
            .take(3)
            .map(|tok| tok.parse::<f64>())
            .collect::<std::result::Result<Vec<_>, _>>()
            .map_err(|_| err(format!("bad coordinate at atom {atom_idx}")))?;
        if vals.len() < 3 {
            return Err(err(format!(
                "coordinate line for atom {atom_idx} has {} values, need 3",
                vals.len()
            )));
        }

        let frac = if let Some(inv) = &inv_matrix {
            let cart = Vector3::new(vals[0] * scale, vals[1] * scale, vals[2] * scale);
            inv * cart
        } else {
            Vector3::new(vals[0], vals[1], vals[2])
        };
        frac_coords.push(frac);
    }

    let mut site_occupancies = Vec::with_capacity(n_atoms);
    for (elem_idx, (elem_str, &count)) in all_symbols.iter().zip(&all_counts).enumerate() {
        let sym = clean_symbol(elem_str);
        let element = Element::from_symbol(sym).ok_or_else(|| {
            err(format!(
                "unknown element '{elem_str}' (cleaned: '{sym}') at index {elem_idx}"
            ))
        })?;
        let species = Species::new(element, None);
        for _ in 0..count {
            site_occupancies.push(SiteOccupancy::ordered(species));
        }
    }

    let structure = Structure {
        lattice,
        site_occupancies,
        frac_coords,
        pbc: [true, true, true],
        charge: 0.0,
        properties: HashMap::new(),
    };

    // Find volumetric data start: skip past coordinates + blank line
    let mut data_start = coord_line_idx + n_atoms;
    while data_start < lines.len() && lines[data_start].trim().is_empty() {
        data_start += 1;
    }

    // Grid dimensions
    if data_start >= lines.len() {
        return Err(err(
            "CHGCAR truncated: no grid dimensions after coordinate block".to_string(),
        ));
    }
    let grid_vals: Vec<usize> = lines[data_start]
        .split_whitespace()
        .map(|tok| tok.parse::<usize>())
        .collect::<std::result::Result<Vec<_>, _>>()
        .map_err(|_| err(format!("bad grid dimensions at line {data_start}")))?;
    if grid_vals.len() < 3 {
        return Err(err("grid dimensions line has <3 values".to_string()));
    }
    let ngx = grid_vals[0];
    let ngy = grid_vals[1];
    let ngz = grid_vals[2];
    if ngx == 0 || ngy == 0 || ngz == 0 {
        return Err(err(format!(
            "grid dimensions must be positive, got {ngx}x{ngy}x{ngz}"
        )));
    }
    let n_grid = ngx * ngy * ngz;
    data_start += 1;

    // Read volumetric data (Fortran ordering: x fastest)
    let (total_fortran, lines_consumed) = read_volumetric_data(&lines[data_start..], n_grid)
        .map_err(|msg| err(format!("reading total charge data: {msg}")))?;

    // Reorder from Fortran to C order
    let total = fortran_to_c_order(&total_fortran, ngx, ngy, ngz);

    // Look for spin-difference data (second dataset)
    let diff_start = data_start + lines_consumed;
    let diff = find_second_dataset(&lines, diff_start, ngx, ngy, ngz)
        .map_err(|msg| err(format!("reading diff charge data: {msg}")))?;

    Ok(ChgcarData {
        structure,
        grid_shape: [ngx, ngy, ngz],
        total,
        diff,
    })
}

/// Read n_values floats from lines (5 per line in VASP format).
/// Returns (values, number_of_lines_consumed).
fn read_volumetric_data(
    lines: &[&str],
    n_values: usize,
) -> std::result::Result<(Vec<f64>, usize), String> {
    let mut values = Vec::with_capacity(n_values);
    let mut line_count = 0;

    for line in lines {
        if values.len() >= n_values {
            break;
        }
        let trimmed = line.trim();
        if trimmed.is_empty() {
            line_count += 1;
            continue;
        }
        for tok in trimmed.split_whitespace() {
            if values.len() >= n_values {
                break;
            }
            let val: f64 = tok
                .parse()
                .map_err(|_| format!("non-numeric token '{tok}' at data line {line_count}"))?;
            values.push(val);
        }
        line_count += 1;
    }

    if values.len() < n_values {
        return Err(format!("expected {n_values} values, got {}", values.len()));
    }

    Ok((values, line_count))
}

/// Reorder 3D data from Fortran order (x-fastest) to C order (z-fastest).
fn fortran_to_c_order(fortran: &[f64], ngx: usize, ngy: usize, ngz: usize) -> Vec<f64> {
    let mut c_order = vec![0.0; ngx * ngy * ngz];
    for (flat_idx, &val) in fortran.iter().enumerate() {
        let ix = flat_idx % ngx;
        let iy = (flat_idx / ngx) % ngy;
        let iz = flat_idx / (ngx * ngy);
        c_order[ix * ngy * ngz + iy * ngz + iz] = val;
    }
    c_order
}

/// Try to find and parse a second volumetric dataset (spin difference).
fn find_second_dataset(
    lines: &[&str],
    start: usize,
    ngx: usize,
    ngy: usize,
    ngz: usize,
) -> std::result::Result<Option<Vec<f64>>, String> {
    let n_grid = ngx * ngy * ngz;

    // Skip augmentation data and blank lines until we find a grid dimension line
    let mut idx = start;
    while idx < lines.len() {
        let trimmed = lines[idx].trim();

        // Skip blank lines and augmentation occupancy lines
        if trimmed.is_empty() || trimmed.starts_with("augmentation") {
            idx += 1;
            continue;
        }

        // Try parsing as grid dimensions
        let tokens: Vec<&str> = trimmed.split_whitespace().collect();
        if tokens.len() == 3
            && let (Ok(gx), Ok(gy), Ok(gz)) = (
                tokens[0].parse::<usize>(),
                tokens[1].parse::<usize>(),
                tokens[2].parse::<usize>(),
            )
            && gx == ngx
            && gy == ngy
            && gz == ngz
        {
            let (diff_fortran, _) = read_volumetric_data(&lines[idx + 1..], n_grid)?;
            let diff = fortran_to_c_order(&diff_fortran, ngx, ngy, ngz);
            return Ok(Some(diff));
        }

        // If it's a line of floats (augmentation data), skip it
        let is_float_line = tokens.iter().all(|tok| tok.parse::<f64>().is_ok());
        if is_float_line {
            idx += 1;
            continue;
        }

        // Unknown line, stop searching
        break;
    }

    Ok(None)
}

// === 3D FFT ===

/// Perform a 3D FFT in-place on C-ordered data [ix][iy][iz].
///
/// Uses rayon to parallelize batches of 1D FFTs along each axis.
fn fft_3d(data: &mut [Complex<f64>], ngx: usize, ngy: usize, ngz: usize) {
    let n_total = ngx * ngy * ngz;
    assert_eq!(data.len(), n_total, "data length must match ngx*ngy*ngz");

    let mut planner = FftPlanner::new();
    let fft_z = planner.plan_fft_forward(ngz);
    let fft_y = planner.plan_fft_forward(ngy);
    let fft_x = planner.plan_fft_forward(ngx);

    // Helper: apply FFT to contiguous chunks, parallel when rayon is available
    fn fft_chunks(data: &mut [Complex<f64>], chunk_size: usize, fft: &Arc<dyn rustfft::Fft<f64>>) {
        #[cfg(feature = "rayon")]
        {
            data.par_chunks_mut(chunk_size).for_each(|chunk| {
                let mut scratch = vec![Complex::default(); fft.get_inplace_scratch_len()];
                fft.process_with_scratch(chunk, &mut scratch);
            });
        }
        #[cfg(not(feature = "rayon"))]
        {
            let mut scratch = vec![Complex::default(); fft.get_inplace_scratch_len()];
            for chunk in data.chunks_mut(chunk_size) {
                fft.process_with_scratch(chunk, &mut scratch);
            }
        }
    }

    // Step 1: FFT along z (innermost axis, contiguous chunks of ngz)
    fft_chunks(data, ngz, &fft_z);

    // Step 2: FFT along y (stride = ngz within each x-slice of size ngy*ngz)
    // Gather strided y-data into a contiguous buffer, FFT, scatter back
    let fft_y_ref = &fft_y;
    let process_y_slice = |x_slice: &mut [Complex<f64>]| {
        let mut buffer = vec![Complex::default(); ngy];
        let mut scratch = vec![Complex::default(); fft_y_ref.get_inplace_scratch_len()];
        for iz in 0..ngz {
            for iy in 0..ngy {
                buffer[iy] = x_slice[iy * ngz + iz];
            }
            fft_y_ref.process_with_scratch(&mut buffer, &mut scratch);
            for iy in 0..ngy {
                x_slice[iy * ngz + iz] = buffer[iy];
            }
        }
    };
    #[cfg(feature = "rayon")]
    data.par_chunks_mut(ngy * ngz).for_each(process_y_slice);
    #[cfg(not(feature = "rayon"))]
    data.chunks_mut(ngy * ngz).for_each(process_y_slice);

    // Step 3: FFT along x (stride = ngy*ngz, spans full array)
    // Transpose to make x innermost, FFT, transpose back
    let mut transposed = vec![Complex::default(); n_total];
    for ix in 0..ngx {
        for iy in 0..ngy {
            for iz in 0..ngz {
                transposed[(iy * ngz + iz) * ngx + ix] = data[ix * ngy * ngz + iy * ngz + iz];
            }
        }
    }

    fft_chunks(&mut transposed, ngx, &fft_x);

    for ix in 0..ngx {
        for iy in 0..ngy {
            for iz in 0..ngz {
                data[ix * ngy * ngz + iy * ngz + iz] = transposed[(iy * ngz + iz) * ngx + ix];
            }
        }
    }
}

// === Fourier Extraction ===

/// Extract low-frequency Fourier coefficients from parsed CHGCAR data.
///
/// Mirrors the logic of `extract_fourier_from_chgcar.py`: FFT the real-space
/// charge density, keep all G-vectors within |G| < `g_max`, and store the
/// result as a dense (2H+1)×(2K+1)×(2L+1) complex array.
pub fn extract_fourier_modes(data: &ChgcarData, g_max: f64) -> Result<FourierResult> {
    check_positive(g_max, "g_max")?;

    let lattice = &data.structure.lattice;
    let grid = data.grid_shape;
    let [ngx, ngy, ngz] = grid;
    let n_grid = ngx * ngy * ngz;
    let n_grid_f = n_grid as f64;

    let is_spin_polarized = data.diff.is_some();

    // Reciprocal lattice (crystallographic, without 2π)
    let latt_matrix = lattice.matrix();
    let vol = lattice.volume();

    let a = latt_matrix.row(0).transpose();
    let b = latt_matrix.row(1).transpose();
    let c = latt_matrix.row(2).transpose();
    let a_star = b.cross(&c) / vol;
    let b_star = c.cross(&a) / vol;
    let c_star = a.cross(&b) / vol;

    let recip_with_2pi = Matrix3::from_rows(&[
        (a_star * 2.0 * PI).transpose(),
        (b_star * 2.0 * PI).transpose(),
        (c_star * 2.0 * PI).transpose(),
    ]);

    // Real-space lattice vector lengths
    let real_lengths = [a.norm(), b.norm(), c.norm()];
    let recip_lengths = [a_star.norm(), b_star.norm(), c_star.norm()];

    // hkl_max from g_max, capped below Nyquist.
    // For even N, h=N/2 and h=-N/2 alias to the same FFT bin via rem_euclid,
    // so cap at (N-1)/2 (integer division) to keep only unique G-vectors.
    let nyquist: [usize; 3] = std::array::from_fn(|idx| (grid[idx] - 1) / 2);
    let hkl_max: [i32; 3] = std::array::from_fn(|idx| {
        ((g_max * real_lengths[idx] / (2.0 * PI)).ceil() as usize).min(nyquist[idx]) as i32
    });

    let g_nyquist = 2.0
        * PI
        * nyquist
            .iter()
            .zip(&recip_lengths)
            .map(|(&nq, &rl)| nq as f64 * rl)
            .fold(f64::INFINITY, f64::min);

    let shape_3d: [usize; 3] = std::array::from_fn(|idx| (2 * hkl_max[idx] + 1) as usize);
    // Perform FFT
    if is_spin_polarized {
        let rho_total = &data.total;
        let rho_diff = data.diff.as_ref().unwrap();

        // Spin decomposition: up = (total + diff)/2, down = (total - diff)/2
        let mut rho_up: Vec<Complex<f64>> = rho_total
            .iter()
            .zip(rho_diff.iter())
            .map(|(&tot, &diff)| Complex::new((tot + diff) / 2.0, 0.0))
            .collect();
        let mut rho_down: Vec<Complex<f64>> = rho_total
            .iter()
            .zip(rho_diff.iter())
            .map(|(&tot, &diff)| Complex::new((tot - diff) / 2.0, 0.0))
            .collect();

        for rho in [&mut rho_up, &mut rho_down] {
            fft_3d(rho, ngx, ngy, ngz);
            for val in rho.iter_mut() {
                *val /= n_grid_f;
            }
        }

        let total_up = rho_up[0].re;
        let total_down = rho_down[0].re;

        let ExtractedCoeffs {
            mut reals,
            mut imags,
            n_inside,
        } = extract_coefficients(&[&rho_up, &rho_down], grid, hkl_max, &recip_with_2pi, g_max);
        let down_imag = imags.pop().unwrap();
        let up_imag = imags.pop().unwrap();
        let down_real = reals.pop().unwrap();
        let up_real = reals.pop().unwrap();

        Ok(build_result(
            hkl_max,
            g_max,
            latt_matrix,
            &recip_with_2pi,
            grid,
            g_nyquist,
            true,
            total_up + total_down,
            total_up - total_down,
            shape_3d,
            n_inside,
            up_real,
            up_imag,
            Some(down_real),
            Some(down_imag),
            vol,
        ))
    } else {
        let mut rho_g: Vec<Complex<f64>> = data
            .total
            .iter()
            .map(|&val| Complex::new(val, 0.0))
            .collect();

        fft_3d(&mut rho_g, ngx, ngy, ngz);

        for val in &mut rho_g {
            *val /= n_grid_f;
        }

        let total_electrons = rho_g[0].re;

        let ExtractedCoeffs {
            mut reals,
            mut imags,
            n_inside,
        } = extract_coefficients(&[&rho_g], grid, hkl_max, &recip_with_2pi, g_max);
        let rho_real = reals.pop().unwrap();
        let rho_imag = imags.pop().unwrap();

        Ok(build_result(
            hkl_max,
            g_max,
            latt_matrix,
            &recip_with_2pi,
            grid,
            g_nyquist,
            false,
            total_electrons,
            0.0,
            shape_3d,
            n_inside,
            rho_real,
            rho_imag,
            None,
            None,
            vol,
        ))
    }
}

/// Per-channel real/imag coefficient arrays and G-vector count.
struct ExtractedCoeffs {
    /// Real parts for each channel, flattened C-order.
    reals: Vec<Vec<f64>>,
    /// Imaginary parts for each channel, flattened C-order.
    imags: Vec<Vec<f64>>,
    /// Number of G-vectors inside the |G| sphere.
    n_inside: usize,
}

/// Extract Fourier coefficients from one or more FFT channels.
///
/// Each channel produces a (real, imag) pair of Vec<f64>. Returns the
/// extracted channel pairs plus the number of G-vectors inside the sphere.
fn extract_coefficients(
    channels: &[&[Complex<f64>]],
    grid: [usize; 3],
    hkl_max: [i32; 3],
    recip_with_2pi: &Matrix3<f64>,
    g_max: f64,
) -> ExtractedCoeffs {
    let [ngx, ngy, ngz] = grid;
    let [big_h, big_k, big_l] = hkl_max;
    let sk = (2 * big_k + 1) as usize;
    let sl = (2 * big_l + 1) as usize;
    let n_coeffs = (2 * big_h + 1) as usize * sk * sl;
    let g_max_sq = g_max * g_max;

    let mut reals: Vec<Vec<f64>> = channels.iter().map(|_| vec![0.0; n_coeffs]).collect();
    let mut imags: Vec<Vec<f64>> = channels.iter().map(|_| vec![0.0; n_coeffs]).collect();
    let mut n_inside = 0_usize;

    let recip_t = recip_with_2pi.transpose();
    for h in -big_h..=big_h {
        for k in -big_k..=big_k {
            for l in -big_l..=big_l {
                let hkl = Vector3::new(h as f64, k as f64, l as f64);
                let g_mag_sq = (recip_t * hkl).norm_squared();
                if g_mag_sq > g_max_sq {
                    continue;
                }

                let out_idx = ((h + big_h) as usize) * sk * sl
                    + ((k + big_k) as usize) * sl
                    + (l + big_l) as usize;
                let fft_idx = h.rem_euclid(ngx as i32) as usize * ngy * ngz
                    + k.rem_euclid(ngy as i32) as usize * ngz
                    + l.rem_euclid(ngz as i32) as usize;

                for (ch_idx, &channel) in channels.iter().enumerate() {
                    reals[ch_idx][out_idx] = channel[fft_idx].re;
                    imags[ch_idx][out_idx] = channel[fft_idx].im;
                }
                n_inside += 1;
            }
        }
    }

    ExtractedCoeffs {
        reals,
        imags,
        n_inside,
    }
}

#[allow(clippy::too_many_arguments)]
fn build_result(
    hkl_range: [i32; 3],
    g_max: f64,
    latt_matrix: &Matrix3<f64>,
    recip_with_2pi: &Matrix3<f64>,
    grid_shape: [usize; 3],
    g_nyquist: f64,
    is_spin_polarized: bool,
    total_electrons: f64,
    total_magnetization: f64,
    coeff_shape: [usize; 3],
    n_coeffs_inside_sphere: usize,
    rho_real: Vec<f64>,
    rho_imag: Vec<f64>,
    rho_down_real: Option<Vec<f64>>,
    rho_down_imag: Option<Vec<f64>>,
    volume: f64,
) -> FourierResult {
    let to_arr = |mat: &Matrix3<f64>| -> [[f64; 3]; 3] {
        [
            [mat[(0, 0)], mat[(0, 1)], mat[(0, 2)]],
            [mat[(1, 0)], mat[(1, 1)], mat[(1, 2)]],
            [mat[(2, 0)], mat[(2, 1)], mat[(2, 2)]],
        ]
    };

    FourierResult {
        hkl_range,
        g_max,
        lattice: to_arr(latt_matrix),
        recip_lattice: to_arr(recip_with_2pi),
        grid_shape,
        g_nyquist,
        is_spin_polarized,
        total_electrons,
        total_magnetization,
        coeff_shape,
        n_coeffs_inside_sphere,
        rho_real,
        rho_imag,
        rho_down_real,
        rho_down_imag,
        volume,
    }
}

/// Process multiple CHGCAR files in parallel.
///
/// Returns results and total wall-clock time in seconds.
#[cfg(feature = "rayon")]
pub fn process_batch(paths: &[&Path], g_max: f64) -> Result<(Vec<Result<FourierResult>>, f64)> {
    check_positive(g_max, "g_max")?;
    let start = std::time::Instant::now();
    let results: Vec<Result<FourierResult>> = paths
        .par_iter()
        .map(|path| {
            let data = parse_chgcar(path)?;
            extract_fourier_modes(&data, g_max)
        })
        .collect();
    let elapsed = start.elapsed().as_secs_f64();
    Ok((results, elapsed))
}

/// Process multiple CHGCAR files sequentially (fallback without rayon).
#[cfg(not(feature = "rayon"))]
pub fn process_batch(paths: &[&Path], g_max: f64) -> Result<(Vec<Result<FourierResult>>, f64)> {
    check_positive(g_max, "g_max")?;
    let start = std::time::Instant::now();
    let results: Vec<Result<FourierResult>> = paths
        .iter()
        .map(|path| {
            let data = parse_chgcar(path)?;
            extract_fourier_modes(&data, g_max)
        })
        .collect();
    let elapsed = start.elapsed().as_secs_f64();
    Ok((results, elapsed))
}
