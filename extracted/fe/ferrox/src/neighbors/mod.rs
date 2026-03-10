//! Cell-list based neighbor finding for O(n) complexity.
//!
//! This module provides efficient neighbor list computation using spatial binning.
//! The cell-list algorithm partitions space into bins and only checks neighboring
//! bins, reducing complexity from O(n²) to O(n) for large systems.
//!
//! # Example
//!
//! ```rust,ignore
//! use ferrox::neighbors::{build_neighbor_list, NeighborListConfig};
//! use ferrox::structure::Structure;
//!
//! let structure = Structure::from_json(json_str)?;
//! let config = NeighborListConfig {
//!     cutoff: 5.0,
//!     ..Default::default()
//! };
//! let nl = build_neighbor_list(&structure, &config);
//! ```

mod build;
mod pair_iterator;

pub use build::{build_neighbor_list, get_site_neighbors};
pub use pair_iterator::{count_pairs, for_each_pair};

use crate::lattice::Lattice;
use nalgebra::Vector3;

/// Configuration for neighbor list computation.
#[derive(Debug, Clone)]
pub struct NeighborListConfig {
    /// Maximum distance to consider atoms as neighbors (Angstrom).
    pub cutoff: f64,
    /// Whether to include self-interactions (same atom, same image).
    pub self_interaction: bool,
    /// Numerical tolerance for distance comparisons.
    pub numerical_tol: f64,
    /// Minimum number of atoms to use cell-list algorithm instead of brute-force.
    /// Cell-list is O(n) but has setup overhead; brute-force is O(n²) but simpler.
    /// Default: 50 atoms.
    pub cell_list_threshold: usize,
}

impl Default for NeighborListConfig {
    fn default() -> Self {
        Self {
            cutoff: 5.0,
            self_interaction: false,
            numerical_tol: 1e-8,
            cell_list_threshold: 50,
        }
    }
}

/// Result of neighbor list computation.
#[derive(Debug, Clone, Default)]
pub struct NeighborList {
    /// Center atom indices (one entry per pair).
    pub center_indices: Vec<usize>,
    /// Neighbor atom indices (one entry per pair).
    pub neighbor_indices: Vec<usize>,
    /// Distance between center and neighbor (Angstrom).
    pub distances: Vec<f64>,
    /// Periodic image offset [da, db, dc] in lattice vector units.
    pub images: Vec<[i32; 3]>,
}

impl NeighborList {
    /// Create an empty neighbor list.
    pub fn new() -> Self {
        Self::default()
    }

    /// Create a neighbor list with pre-allocated capacity.
    pub fn with_capacity(capacity: usize) -> Self {
        Self {
            center_indices: Vec::with_capacity(capacity),
            neighbor_indices: Vec::with_capacity(capacity),
            distances: Vec::with_capacity(capacity),
            images: Vec::with_capacity(capacity),
        }
    }

    /// Number of neighbor pairs in the list.
    pub fn len(&self) -> usize {
        self.center_indices.len()
    }

    /// Check if the neighbor list is empty.
    pub fn is_empty(&self) -> bool {
        self.center_indices.is_empty()
    }

    /// Add a neighbor pair to the list.
    pub fn push(&mut self, center: usize, neighbor: usize, distance: f64, image: [i32; 3]) {
        self.center_indices.push(center);
        self.neighbor_indices.push(neighbor);
        self.distances.push(distance);
        self.images.push(image);
    }

    /// Merge another neighbor list into this one.
    pub fn extend(&mut self, other: NeighborList) {
        self.center_indices.extend(other.center_indices);
        self.neighbor_indices.extend(other.neighbor_indices);
        self.distances.extend(other.distances);
        self.images.extend(other.images);
    }
}

/// Internal cell-list structure for spatial binning.
struct CellList {
    /// Mapping from bin index to list of atom indices in that bin.
    bins: Vec<Vec<usize>>,
    /// Number of bins along each axis [nx, ny, nz].
    n_bins: [usize; 3],
    /// Size of each bin along each axis (in fractional coordinates).
    bin_size_frac: [f64; 3],
}

impl CellList {
    /// Build a cell list from fractional coordinates.
    ///
    /// Atoms are assigned to bins based on their fractional coordinates.
    /// The bin count is chosen so that each bin spans at least `cutoff` distance,
    /// ensuring we only need to check neighboring bins.
    fn build(frac_coords: &[Vector3<f64>], lattice: &Lattice, cutoff: f64) -> Self {
        let n_atoms = frac_coords.len();

        // Compute face distances (perpendicular heights) for each axis
        // This determines how many bins we need along each axis
        let matrix = lattice.matrix();
        let lattice_vecs = [
            matrix.row(0).transpose(),
            matrix.row(1).transpose(),
            matrix.row(2).transpose(),
        ];

        let volume = lattice.volume();

        // For each axis, compute the perpendicular distance (height)
        // height_i = volume / |a_{i+1} × a_{i+2}|
        let heights: [f64; 3] = std::array::from_fn(|idx| {
            let cross = lattice_vecs[(idx + 1) % 3].cross(&lattice_vecs[(idx + 2) % 3]);
            volume / cross.norm()
        });

        // Number of bins: at least 1, based on height / cutoff
        // We want bin_size >= cutoff so we only check 3 bins per axis (current + neighbors)
        let n_bins: [usize; 3] = std::array::from_fn(|idx| {
            let n = (heights[idx] / cutoff).floor() as usize;
            n.max(1)
        });

        // Fractional bin size
        let bin_size_frac: [f64; 3] = std::array::from_fn(|idx| 1.0 / n_bins[idx] as f64);

        // Total number of bins
        let total_bins = n_bins[0] * n_bins[1] * n_bins[2];

        // Allocate bins
        let mut bins: Vec<Vec<usize>> = vec![Vec::new(); total_bins];

        // Assign atoms to bins based on their fractional coordinates
        for (atom_idx, frac) in frac_coords.iter().enumerate() {
            // Wrap to [0, 1)
            let wrapped = wrap_frac_coords(frac);

            // Compute bin indices
            let bx = ((wrapped.x / bin_size_frac[0]).floor() as usize).min(n_bins[0] - 1);
            let by = ((wrapped.y / bin_size_frac[1]).floor() as usize).min(n_bins[1] - 1);
            let bz = ((wrapped.z / bin_size_frac[2]).floor() as usize).min(n_bins[2] - 1);

            let bin_idx = bx + by * n_bins[0] + bz * n_bins[0] * n_bins[1];
            bins[bin_idx].push(atom_idx);
        }

        // Pre-allocate capacity estimate for bins (average atoms per bin)
        let avg_per_bin = n_atoms / total_bins.max(1);
        if avg_per_bin > 0 {
            for bin in &mut bins {
                if bin.capacity() < avg_per_bin {
                    bin.reserve(avg_per_bin);
                }
            }
        }

        Self {
            bins,
            n_bins,
            bin_size_frac,
        }
    }

    /// Get the linear bin index from 3D bin coordinates.
    #[inline]
    fn bin_index(&self, bx: usize, by: usize, bz: usize) -> usize {
        bx + by * self.n_bins[0] + bz * self.n_bins[0] * self.n_bins[1]
    }

    /// Get 3D bin coordinates from a linear bin index.
    #[inline]
    fn bin_coords(&self, idx: usize) -> (usize, usize, usize) {
        let bz = idx / (self.n_bins[0] * self.n_bins[1]);
        let remainder = idx % (self.n_bins[0] * self.n_bins[1]);
        let by = remainder / self.n_bins[0];
        let bx = remainder % self.n_bins[0];
        (bx, by, bz)
    }

    /// Iterate over all neighboring bins for a given bin, including the bin itself.
    /// Returns (neighbor_bin_idx, image_offset) pairs.
    fn neighbor_bins(&self, bin_idx: usize, pbc: [bool; 3]) -> Vec<(usize, [i32; 3])> {
        let (bx, by, bz) = self.bin_coords(bin_idx);
        let mut neighbors = Vec::with_capacity(27);

        // Range of offsets to check for each axis
        let range = |axis: usize, b: usize| -> Vec<(usize, i32)> {
            let n = self.n_bins[axis];
            let mut result = Vec::with_capacity(3);

            // Current bin
            result.push((b, 0));

            // Previous bin
            if b > 0 {
                result.push((b - 1, 0));
            } else if pbc[axis] && n > 1 {
                result.push((n - 1, -1)); // wrap with image offset
            }

            // Next bin
            if b + 1 < n {
                result.push((b + 1, 0));
            } else if pbc[axis] && n > 1 {
                result.push((0, 1)); // wrap with image offset
            }

            result
        };

        let x_range = range(0, bx);
        let y_range = range(1, by);
        let z_range = range(2, bz);

        for (nx, ix) in &x_range {
            for (ny, iy) in &y_range {
                for (nz, iz) in &z_range {
                    let neighbor_idx = self.bin_index(*nx, *ny, *nz);
                    neighbors.push((neighbor_idx, [*ix, *iy, *iz]));
                }
            }
        }

        neighbors
    }
}

/// Wrap fractional coordinates to [0, 1).
#[inline]
fn wrap_frac_coords(coords: &Vector3<f64>) -> Vector3<f64> {
    Vector3::new(
        coords.x - coords.x.floor(),
        coords.y - coords.y.floor(),
        coords.z - coords.z.floor(),
    )
}

#[cfg(test)]
mod tests;
