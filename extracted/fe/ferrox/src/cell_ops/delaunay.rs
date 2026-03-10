use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use nalgebra::{Matrix3, Vector3};

use super::helpers::create_shear_transform;

/// Result of Delaunay reduction.
#[derive(Debug, Clone)]
pub struct DelaunayCell {
    /// The Delaunay-reduced lattice matrix
    pub matrix: Matrix3<f64>,
    /// The transformation matrix from original to Delaunay basis
    pub transformation: Matrix3<f64>,
}

/// Selling-reduced S6 representation: the 6 inner products of the 4 vectors
/// (a, b, c, d=-(a+b+c)) in a Delaunay-reduced basis. Canonicalized by selecting
/// the lexicographically smallest S6 over the 24 permutations of (a, b, c, d).
#[derive(Debug, Clone)]
pub struct SellingS6 {
    /// b·c
    pub bc: f64,
    /// a·c
    pub ac: f64,
    /// a·b
    pub ab: f64,
    /// a·d where d = -(a+b+c)
    pub ad: f64,
    /// b·d where d = -(a+b+c)
    pub bd: f64,
    /// c·d where d = -(a+b+c)
    pub cd: f64,
}

impl SellingS6 {
    /// Return as a 6-element array [bc, ac, ab, ad, bd, cd].
    pub fn as_array(&self) -> [f64; 6] {
        [self.bc, self.ac, self.ab, self.ad, self.bd, self.cd]
    }

    /// Compute the canonicalized S6 by selecting the lexicographically smallest
    /// S6 over all 24 permutations of (a, b, c, d).
    pub fn canonicalize(cell: &DelaunayCell) -> Result<Self> {
        let [av, bv, cv] = [0, 1, 2].map(|idx| cell.matrix.row(idx).transpose());
        let vecs: [Vector3<f64>; 4] = [av, bv, cv, -(av + bv + cv)];

        const PERMS: [[usize; 4]; 24] = [
            [0, 1, 2, 3],
            [0, 1, 3, 2],
            [0, 2, 1, 3],
            [0, 2, 3, 1],
            [0, 3, 1, 2],
            [0, 3, 2, 1],
            [1, 0, 2, 3],
            [1, 0, 3, 2],
            [1, 2, 0, 3],
            [1, 2, 3, 0],
            [1, 3, 0, 2],
            [1, 3, 2, 0],
            [2, 0, 1, 3],
            [2, 0, 3, 1],
            [2, 1, 0, 3],
            [2, 1, 3, 0],
            [2, 3, 0, 1],
            [2, 3, 1, 0],
            [3, 0, 1, 2],
            [3, 0, 2, 1],
            [3, 1, 0, 2],
            [3, 1, 2, 0],
            [3, 2, 0, 1],
            [3, 2, 1, 0],
        ];

        PERMS
            .iter()
            .map(|perm| {
                let [va, vb, vc, vd] = perm.map(|idx| vecs[idx]);
                Self {
                    bc: vb.dot(&vc),
                    ac: va.dot(&vc),
                    ab: va.dot(&vb),
                    ad: va.dot(&vd),
                    bd: vb.dot(&vd),
                    cd: vc.dot(&vd),
                }
            })
            .min_by(|left, right| {
                left.as_array()
                    .partial_cmp(&right.as_array())
                    .unwrap_or(std::cmp::Ordering::Equal)
            })
            .ok_or_else(|| FerroxError::InvalidLattice {
                reason: "Failed to canonicalize S6 (empty permutations)".to_string(),
            })
    }
}

/// Compute the canonicalized Selling S6 representation for a lattice.
pub fn selling_s6(lattice: &Lattice, tolerance: f64) -> Result<SellingS6> {
    let cell = delaunay_reduce(lattice, tolerance)?;
    SellingS6::canonicalize(&cell)
}

/// Compute the Delaunay-reduced cell of a lattice.
///
/// The Delaunay reduction produces a cell where all pairwise scalar products
/// of lattice vectors are non-positive (all angles ≥ 90°).
///
/// # Arguments
///
/// * `lattice` - The lattice to reduce
/// * `tolerance` - Numerical tolerance for comparisons
///
/// # Returns
///
/// The Delaunay cell information including the reduced matrix and transformation.
///
/// # Errors
///
/// Returns an error if the reduction fails to converge.
pub fn delaunay_reduce(lattice: &Lattice, tolerance: f64) -> Result<DelaunayCell> {
    // Start with LLL-reduced lattice for numerical stability
    let mut matrix = lattice.lll_matrix();
    let mut total_transform = lattice.lll_mapping();

    // Use absolute volume to handle left-handed lattices correctly
    let eps = tolerance * lattice.volume().abs().powf(1.0 / 3.0);
    const MAX_ITER: usize = 100;

    for _ in 0..MAX_ITER {
        let mut changed = false;

        // Check and fix each pair of vectors
        for idx in 0..3 {
            for jdx in (idx + 1)..3 {
                let vec_i = matrix.row(idx).transpose();
                let vec_j = matrix.row(jdx).transpose();
                let dot = vec_i.dot(&vec_j);

                if dot > eps {
                    // Reduce: replace longer vector with v_long - v_short
                    let norm_i = vec_i.norm_squared();
                    let norm_j = vec_j.norm_squared();

                    let transform = if norm_i > norm_j {
                        // Replace v_i with v_i - v_j
                        let new_row = vec_i - vec_j;
                        matrix.set_row(idx, &new_row.transpose());
                        create_shear_transform(idx, jdx, -1)
                    } else {
                        // Replace v_j with v_j - v_i
                        let new_row = vec_j - vec_i;
                        matrix.set_row(jdx, &new_row.transpose());
                        create_shear_transform(jdx, idx, -1)
                    };
                    total_transform = transform * total_transform;
                    changed = true;
                }
            }
        }

        if !changed {
            return Ok(DelaunayCell {
                matrix,
                transformation: total_transform,
            });
        }
    }

    Err(FerroxError::ReductionNotConverged {
        iterations: MAX_ITER,
    })
}
