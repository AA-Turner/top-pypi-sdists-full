use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use nalgebra::Vector3;

use super::Structure;

// === Slab Generation ===

/// Configuration for slab generation.
#[derive(Debug, Clone)]
pub struct SlabConfig {
    /// Miller indices (h, k, l) defining the surface orientation.
    pub miller_index: [i32; 3],
    /// Minimum thickness of the slab in Angstroms (or unit planes if in_unit_planes=true).
    pub min_slab_size: f64,
    /// Minimum vacuum layer thickness in Angstroms.
    pub min_vacuum_size: f64,
    /// If true, center the slab in the vacuum region.
    pub center_slab: bool,
    /// If true, min_slab_size is interpreted as number of unit planes, not Angstroms.
    pub in_unit_planes: bool,
    /// If true, reduce to primitive surface unit cell (not yet implemented).
    pub primitive: bool,
    /// Symmetry precision for identifying unique terminations.
    pub symprec: f64,
    /// If Some(idx), only generate the termination at this index (0-indexed).
    /// This avoids computing all terminations when only one is needed.
    pub termination_index: Option<usize>,
}

impl Default for SlabConfig {
    fn default() -> Self {
        Self {
            miller_index: [1, 0, 0],
            min_slab_size: 10.0,
            min_vacuum_size: 10.0,
            center_slab: true,
            in_unit_planes: false,
            primitive: false,
            symprec: 0.01,
            termination_index: None,
        }
    }
}

impl SlabConfig {
    /// Create a new SlabConfig with the given Miller indices.
    #[must_use]
    pub fn new(miller_index: [i32; 3]) -> Self {
        Self {
            miller_index,
            ..Default::default()
        }
    }

    /// Set the minimum slab thickness in Angstroms.
    #[must_use]
    pub fn with_min_slab_size(mut self, size: f64) -> Self {
        self.min_slab_size = size;
        self
    }

    /// Set the minimum vacuum layer thickness in Angstroms.
    #[must_use]
    pub fn with_min_vacuum_size(mut self, size: f64) -> Self {
        self.min_vacuum_size = size;
        self
    }

    /// Set whether to center the slab in the vacuum region.
    #[must_use]
    pub fn with_center_slab(mut self, center: bool) -> Self {
        self.center_slab = center;
        self
    }

    /// Set whether min_slab_size is in unit planes (true) or Angstroms (false).
    #[must_use]
    pub fn with_in_unit_planes(mut self, in_planes: bool) -> Self {
        self.in_unit_planes = in_planes;
        self
    }

    /// Set whether to reduce to primitive surface unit cell (not yet implemented).
    #[must_use]
    pub fn with_primitive(mut self, primitive: bool) -> Self {
        self.primitive = primitive;
        self
    }

    /// Set the symmetry precision for identifying unique terminations.
    #[must_use]
    pub fn with_symprec(mut self, symprec: f64) -> Self {
        self.symprec = symprec;
        self
    }

    /// Set a specific termination index to generate (0-indexed).
    /// When set, only this termination is computed, avoiding unnecessary work.
    #[must_use]
    pub fn with_termination_index(mut self, index: usize) -> Self {
        self.termination_index = Some(index);
        self
    }
}

/// Compute the interplanar spacing (d-spacing) for the given Miller indices.
///
/// # Panics
/// Panics if `hkl` is `[0, 0, 0]` (division by zero).
#[allow(dead_code)] // Used in tests; useful utility for crystallography
pub(crate) fn compute_d_spacing(lattice: &Lattice, hkl: [i32; 3]) -> f64 {
    debug_assert!(hkl != [0, 0, 0], "Miller indices cannot all be zero");
    // d = 1 / |G| where G = h*b1 + k*b2 + l*b3 (reciprocal lattice vector)
    let inv_t = lattice.inv_matrix().transpose();
    let hkl_vec = Vector3::new(hkl[0] as f64, hkl[1] as f64, hkl[2] as f64);
    let g_vec = inv_t * hkl_vec;
    1.0 / g_vec.norm()
}

/// Reduce Miller indices to their smallest integer representation (coprime).
pub(crate) fn reduce_miller_indices(hkl: [i32; 3]) -> [i32; 3] {
    fn gcd(a: i32, b: i32) -> i32 {
        if b == 0 { a.abs() } else { gcd(b, a % b) }
    }
    let g = gcd(gcd(hkl[0], hkl[1]), hkl[2]);
    if g == 0 {
        hkl
    } else {
        [hkl[0] / g, hkl[1] / g, hkl[2] / g]
    }
}

/// Compute GCD of two integers using Euclidean algorithm.
fn int_gcd(a: i32, b: i32) -> i32 {
    if b == 0 { a.abs() } else { int_gcd(b, a % b) }
}

/// Compute LCM of two integers, avoiding intermediate overflow.
/// Returns None if result would overflow i32.
fn int_lcm_checked(a: i32, b: i32) -> Option<i32> {
    if a == 0 || b == 0 {
        return Some(0);
    }
    let gcd = int_gcd(a, b);
    let a_div = a.abs() / gcd;
    // Use checked multiplication to detect overflow
    a_div.checked_mul(b.abs())
}

/// Compute LCM of two integers, saturating at i32::MAX on overflow.
fn int_lcm(a: i32, b: i32) -> i32 {
    int_lcm_checked(a, b).unwrap_or(i32::MAX)
}

/// Calculate the slab transformation matrix using pymatgen's algorithm.
/// This produces minimal supercells by using LCM-based in-plane vector construction.
///
/// The algorithm (matching pymatgen's SlabGenerator):
/// 1. For Miller indices that are 0, use the corresponding basis vector (it's in-plane)
/// 2. For non-zero indices, use LCM trick to construct minimal in-plane vectors
/// 3. For c-direction, use the basis vector with maximum projection onto surface normal
pub(crate) fn get_slab_transformation(lattice: &Lattice, hkl: [i32; 3]) -> [[i32; 3]; 3] {
    let [h, k, l] = reduce_miller_indices(hkl);

    // Calculate surface normal in Cartesian coordinates
    let inv_t = lattice.inv_matrix().transpose();
    let hkl_vec = Vector3::new(h as f64, k as f64, l as f64);
    let normal = inv_t * hkl_vec;
    let normal_len = normal.norm();
    let normal = if normal_len > 1e-10 {
        normal / normal_len
    } else {
        Vector3::new(0.0, 0.0, 1.0)
    };

    let miller = [h, k, l];
    let eye: [[i32; 3]; 3] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];

    let mut slab_scale_factor: Vec<[i32; 3]> = Vec::new();
    let mut non_orth_ind: Vec<(usize, f64)> = Vec::new();

    for (idx, &miller_idx) in miller.iter().enumerate() {
        if miller_idx == 0 {
            slab_scale_factor.push(eye[idx]);
        } else {
            let lat_vec = lattice.matrix().row(idx).transpose();
            let lat_len = lat_vec.norm();
            let d = (normal.dot(&lat_vec)).abs() / lat_len;
            non_orth_ind.push((idx, d));
        }
    }

    if non_orth_ind.len() > 1 {
        let lcm_miller = non_orth_ind
            .iter()
            .map(|&(idx, _)| miller[idx].abs())
            .fold(1, int_lcm);
        'outer: for i in 0..non_orth_ind.len() {
            for j in (i + 1)..non_orth_ind.len() {
                let (ii, _) = non_orth_ind[i];
                let (jj, _) = non_orth_ind[j];
                let mut scale_factor = [0i32; 3];
                scale_factor[ii] = -(lcm_miller / miller[ii]);
                scale_factor[jj] = lcm_miller / miller[jj];
                slab_scale_factor.push(reduce_miller_indices(scale_factor));
                if slab_scale_factor.len() == 2 {
                    break 'outer;
                }
            }
        }
    }

    let c_index = if non_orth_ind.is_empty() {
        2
    } else {
        non_orth_ind
            .iter()
            .max_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal))
            .map(|&(idx, _)| idx)
            .unwrap_or(2)
    };
    slab_scale_factor.push(eye[c_index]);

    while slab_scale_factor.len() < 3 {
        for basis in &eye {
            if !slab_scale_factor.contains(basis) {
                slab_scale_factor.push(*basis);
                break;
            }
        }
    }

    let mut result = [[0i32; 3]; 3];
    for (i, v) in slab_scale_factor.iter().take(3).enumerate() {
        result[i] = *v;
    }

    // Use i64 to avoid overflow for large Miller indices
    let r = |i: usize, j: usize| result[i][j] as i64;
    let det = r(0, 0) * (r(1, 1) * r(2, 2) - r(1, 2) * r(2, 1))
        - r(0, 1) * (r(1, 0) * r(2, 2) - r(1, 2) * r(2, 0))
        + r(0, 2) * (r(1, 0) * r(2, 1) - r(1, 1) * r(2, 0));

    if det < 0 {
        for row in &mut result {
            for val in row {
                *val = -*val;
            }
        }
    }

    result
}

/// Identify unique atomic layers along the c-axis (surface normal direction).
/// Returns fractional z-coordinates of each layer, sorted ascending.
/// Uses single-linkage clustering: atoms are in same layer if within `tol` of first atom in layer.
pub(crate) fn identify_layer_positions(frac_coords: &[Vector3<f64>], tol: f64) -> Vec<f64> {
    if frac_coords.is_empty() {
        return vec![];
    }

    let mut z_coords: Vec<f64> = frac_coords.iter().map(|fc| fc.z).collect();
    z_coords.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));

    // Group into layers - compare to first z in layer (not rolling average)
    let mut layer_positions = Vec::new();
    let mut layer_start = z_coords[0];
    let mut layer_sum = z_coords[0];
    let mut layer_count = 1usize;

    for &z_coord in &z_coords[1..] {
        // Compare to first atom in layer, not rolling average (fixes clustering bug)
        if (z_coord - layer_start).abs() < tol {
            layer_sum += z_coord;
            layer_count += 1;
        } else {
            layer_positions.push(layer_sum / layer_count as f64);
            layer_start = z_coord;
            layer_sum = z_coord;
            layer_count = 1;
        }
    }
    layer_positions.push(layer_sum / layer_count as f64);

    layer_positions
}

/// Maximum allowed n_layers to prevent integer overflow when casting to i32.
const MAX_SLAB_LAYERS: usize = 10_000;

/// Maximum allowed supercell determinant (atoms in oriented cell) to prevent memory issues.
const MAX_SUPERCELL_DET: i32 = 100_000;

/// Maximum allowed total atoms in final slab (det × n_layers × original_atoms).
const MAX_SLAB_ATOMS: usize = 100_000;

impl Structure {
    /// Generate a surface slab with the specified configuration.
    ///
    /// Returns a single slab structure with the default (bottom) termination.
    /// For all unique terminations, use `generate_slabs()`.
    pub fn make_slab(&self, config: &SlabConfig) -> Result<Self> {
        // Use termination_index=0 to avoid generating all terminations
        let mut config = config.clone();
        if config.termination_index.is_none() {
            config.termination_index = Some(0);
        }
        let slabs = self.generate_slabs(&config)?;
        slabs
            .into_iter()
            .next()
            .ok_or_else(|| FerroxError::InvalidStructure {
                index: 0,
                reason: "No slab could be generated".to_string(),
            })
    }

    /// Generate all unique surface terminations for the given slab configuration.
    ///
    /// Returns a vector of slab structures, each with a different surface termination.
    ///
    /// # Differences from pymatgen's SlabGenerator
    ///
    /// - **Unit cell size**: The transformation matrix may produce larger supercells than
    ///   pymatgen's minimal algorithm for some Miller indices (e.g., (111)). The surface
    ///   is mathematically equivalent but with more atoms in the periodic unit.
    /// - **Layer counting**: Uses `ceil(min_slab_size / proj_height)` where `proj_height` is the
    ///   projection of the c-vector onto the surface normal, matching pymatgen's SlabGenerator.
    /// - **Primitive reduction**: The `primitive` option is not yet implemented.
    pub fn generate_slabs(&self, config: &SlabConfig) -> Result<Vec<Self>> {
        let hkl = config.miller_index;
        if hkl == [0, 0, 0] {
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: "Miller indices cannot all be zero".to_string(),
            });
        }
        if self.num_sites() == 0 {
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: "Cannot generate slab from empty structure".to_string(),
            });
        }
        if !config.min_slab_size.is_finite() || config.min_slab_size <= 0.0 {
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: "min_slab_size must be positive and finite".to_string(),
            });
        }
        if !config.min_vacuum_size.is_finite() || config.min_vacuum_size < 0.0 {
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: "min_vacuum_size must be non-negative and finite".to_string(),
            });
        }
        if !config.symprec.is_finite() || config.symprec <= 0.0 {
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: "symprec must be positive and finite".to_string(),
            });
        }

        // Create oriented unit cell with a,b in surface plane
        let transform = get_slab_transformation(&self.lattice, hkl);
        // Use i64 to avoid overflow for large Miller indices
        let t = |i: usize, j: usize| transform[i][j] as i64;
        let det = t(0, 0) * (t(1, 1) * t(2, 2) - t(1, 2) * t(2, 1))
            - t(0, 1) * (t(1, 0) * t(2, 2) - t(1, 2) * t(2, 0))
            + t(0, 2) * (t(1, 0) * t(2, 1) - t(1, 1) * t(2, 0));
        if det.abs() > MAX_SUPERCELL_DET as i64 {
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: format!(
                    "Miller indices {:?} require supercell with {} unit cells, exceeding maximum of {}",
                    hkl,
                    det.abs(),
                    MAX_SUPERCELL_DET
                ),
            });
        }

        // Pre-compute expected total atoms to avoid creating huge structures
        // Estimate proj_height = abs(dot(normal, c_vec)) like pymatgen
        let inv_t = self.lattice.inv_matrix().transpose();
        let hkl_vec = Vector3::new(hkl[0] as f64, hkl[1] as f64, hkl[2] as f64);
        let normal = inv_t * hkl_vec;
        let normal = normal / normal.norm();
        let c_row = Vector3::new(
            transform[2][0] as f64,
            transform[2][1] as f64,
            transform[2][2] as f64,
        );
        let c_vec_estimate = self.lattice.matrix() * c_row;
        let proj_height_estimate = normal.dot(&c_vec_estimate).abs();
        let n_layers_estimate = if config.in_unit_planes {
            config.min_slab_size.ceil() as usize
        } else {
            (config.min_slab_size / proj_height_estimate).ceil() as usize
        }
        .max(1);
        let expected_atoms =
            self.frac_coords.len() * (det.unsigned_abs() as usize) * n_layers_estimate;
        if expected_atoms > MAX_SLAB_ATOMS {
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: format!(
                    "Slab would contain ~{} atoms ({} sites × {} unit cells × {} layers), exceeding maximum of {}. \
                     Consider using smaller Miller indices or reducing min_slab_size.",
                    expected_atoms,
                    self.frac_coords.len(),
                    det.abs(),
                    n_layers_estimate,
                    MAX_SLAB_ATOMS
                ),
            });
        }

        let oriented = self.make_supercell(transform)?;

        // Identify unique layer positions in the oriented cell (single repeat)
        // This preserves all distinct terminations within one unit cell
        let oriented_layers = identify_layer_positions(&oriented.frac_coords, config.symprec);
        let unique_terminations = oriented_layers.len().max(1);

        // Calculate surface normal for layer thickness calculation
        let inv_t = self.lattice.inv_matrix().transpose();
        let hkl_vec = Vector3::new(hkl[0] as f64, hkl[1] as f64, hkl[2] as f64);
        let normal = inv_t * hkl_vec;
        let normal = normal / normal.norm();

        // Determine slab thickness in number of unit cells
        // Use _proj_height = abs(dot(normal, c_vec)) to match pymatgen's behavior
        // This gives the actual slab thickness contribution per layer
        let c_vec = oriented.lattice.matrix().row(2).transpose();
        let proj_height = normal.dot(&c_vec).abs();
        let n_layers = if config.in_unit_planes {
            config.min_slab_size.ceil() as usize
        } else {
            (config.min_slab_size / proj_height).ceil() as usize
        }
        .max(1);

        // Prevent integer overflow when casting to i32
        if n_layers > MAX_SLAB_LAYERS {
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: format!(
                    "Slab would require {} layers, exceeding maximum of {}",
                    n_layers, MAX_SLAB_LAYERS
                ),
            });
        }

        // Stack along c-axis
        let slab_supercell = if n_layers > 1 {
            oriented.make_supercell([[1, 0, 0], [0, 1, 0], [0, 0, n_layers as i32]])?
        } else {
            oriented
        };

        // Use layer positions from supercell for shifting, but limit to unique terminations
        // Scale symprec by n_layers: fractional layer spacing is compressed by factor of n_layers
        // in the supercell, so tolerance must shrink proportionally to avoid merging distinct layers
        let scaled_symprec = config.symprec / n_layers as f64;
        let layer_positions = identify_layer_positions(&slab_supercell.frac_coords, scaled_symprec);
        let termination_count = unique_terminations.min(layer_positions.len()).max(1);

        // Determine which terminations to generate
        let (start_idx, end_idx) = match config.termination_index {
            Some(idx) if idx < termination_count => (idx, idx + 1),
            Some(idx) => {
                return Err(FerroxError::InvalidStructure {
                    index: 0,
                    reason: format!(
                        "termination_index {} out of range (0..{})",
                        idx, termination_count
                    ),
                });
            }
            None => (0, termination_count),
        };

        let mut slabs = Vec::with_capacity(end_idx - start_idx);

        for (term_idx, &shift) in layer_positions
            .iter()
            .enumerate()
            .skip(start_idx)
            .take(end_idx - start_idx)
        {
            let mut slab = slab_supercell.clone();

            // Shift z-coordinates and wrap
            for fc in &mut slab.frac_coords {
                fc.z -= shift;
            }
            slab.wrap_to_unit_cell();

            // Add vacuum by scaling c-axis
            let current_c = slab.lattice.lengths().z;
            let total_c = current_c + config.min_vacuum_size;
            let scale = total_c / current_c;

            let mut new_matrix = *slab.lattice.matrix();
            for idx in 0..3 {
                new_matrix[(2, idx)] *= scale;
            }

            // Rescale z-coordinates to account for vacuum
            let slab_frac = current_c / total_c;
            for fc in &mut slab.frac_coords {
                fc.z *= slab_frac;
            }

            // Center slab in vacuum if requested
            if config.center_slab {
                let shift_z = (config.min_vacuum_size / total_c) / 2.0;
                for fc in &mut slab.frac_coords {
                    fc.z += shift_z;
                }
            }

            // Update lattice matrix and set slab PBC (periodic in a,b but not c)
            slab.lattice = Lattice::new(new_matrix);
            slab.set_pbc([true, true, false]);

            // Store metadata
            slab.properties
                .insert("termination_index".to_string(), serde_json::json!(term_idx));
            slab.properties
                .insert("miller_index".to_string(), serde_json::json!(hkl));

            slabs.push(slab);
        }

        Ok(slabs)
    }
}
