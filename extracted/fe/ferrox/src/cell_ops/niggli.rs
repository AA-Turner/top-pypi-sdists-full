use crate::error::Result;
use crate::lattice::Lattice;
use nalgebra::Matrix3;

use super::helpers::find_transformation_matrix;

/// Niggli form type for classification.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum NiggliForm {
    /// Type I: All off-diagonal products have the same sign (all positive or all negative)
    TypeI,
    /// Type II: Off-diagonal products have mixed signs or zeros
    TypeII,
}

/// Result of Niggli reduction.
#[derive(Debug, Clone)]
pub struct NiggliCell {
    /// The Niggli-reduced lattice matrix (rows are lattice vectors)
    pub matrix: Matrix3<f64>,
    /// The transformation matrix from original to Niggli basis
    pub transformation: Matrix3<f64>,
    /// The Niggli form type
    pub form: NiggliForm,
}

/// Niggli-reduced G6 representation: the 6 unique components of the metric tensor
/// of the Niggli-reduced lattice. Used as a canonical lattice key for identity/dedup.
#[derive(Debug, Clone)]
pub struct NiggliG6 {
    /// a·a (squared length of first basis vector)
    pub a2: f64,
    /// b·b (squared length of second basis vector)
    pub b2: f64,
    /// c·c (squared length of third basis vector)
    pub c2: f64,
    /// 2(b·c) (twice the dot product of second and third vectors)
    pub bc_2: f64,
    /// 2(a·c) (twice the dot product of first and third vectors)
    pub ac_2: f64,
    /// 2(a·b) (twice the dot product of first and second vectors)
    pub ab_2: f64,
}

impl NiggliG6 {
    /// Extract G6 components from a Niggli-reduced cell matrix.
    /// Rows of the matrix are the lattice basis vectors a, b, c.
    pub fn from_niggli_cell(cell: &NiggliCell) -> Self {
        let [av, bv, cv] = [0, 1, 2].map(|idx| cell.matrix.row(idx).transpose());
        Self {
            a2: av.dot(&av),
            b2: bv.dot(&bv),
            c2: cv.dot(&cv),
            bc_2: 2.0 * bv.dot(&cv),
            ac_2: 2.0 * av.dot(&cv),
            ab_2: 2.0 * av.dot(&bv),
        }
    }

    /// Return as a 6-element array [a², b², c², 2bc, 2ac, 2ab].
    pub fn as_array(&self) -> [f64; 6] {
        [self.a2, self.b2, self.c2, self.bc_2, self.ac_2, self.ab_2]
    }
}

/// Compute the Niggli G6 representation for a lattice.
pub fn niggli_g6(lattice: &Lattice, tolerance: f64) -> Result<NiggliG6> {
    let cell = niggli_reduce(lattice, tolerance)?;
    Ok(NiggliG6::from_niggli_cell(&cell))
}

/// Compute the Niggli-reduced cell of a lattice.
///
/// The Niggli reduction produces a unique reduced cell with:
/// - a ≤ b ≤ c (ordered by length)
/// - Specific conditions on angles depending on form type
///
/// # Arguments
///
/// * `lattice` - The lattice to reduce
/// * `tolerance` - Numerical tolerance for comparisons
///
/// # Returns
///
/// The Niggli cell information including the reduced matrix and transformation.
///
/// # Errors
///
/// Returns an error if the reduction fails to converge.
pub fn niggli_reduce(lattice: &Lattice, tolerance: f64) -> Result<NiggliCell> {
    let niggli_lattice = lattice.get_niggli_reduced(tolerance)?;
    let niggli_matrix = *niggli_lattice.matrix();

    // Find transformation matrix
    let transformation = find_transformation_matrix(lattice.matrix(), &niggli_matrix);

    // Determine form type
    let metric = niggli_matrix * niggli_matrix.transpose();
    let ksi = 2.0 * metric[(1, 2)];
    let eta = 2.0 * metric[(0, 2)];
    let zeta = 2.0 * metric[(0, 1)];

    let form = if ksi * eta * zeta > 0.0 {
        NiggliForm::TypeI
    } else {
        NiggliForm::TypeII
    };

    Ok(NiggliCell {
        matrix: niggli_matrix,
        transformation,
        form,
    })
}

/// Check if a lattice is already Niggli-reduced.
///
/// # Arguments
///
/// * `lattice` - The lattice to check
/// * `tolerance` - Numerical tolerance for comparisons
///
/// # Returns
///
/// `true` if the lattice satisfies Niggli conditions.
pub fn is_niggli_reduced(lattice: &Lattice, tolerance: f64) -> bool {
    let lengths = lattice.lengths();
    let matrix = lattice.matrix();
    let metric = matrix * matrix.transpose();

    // Check a ≤ b ≤ c
    if lengths[0] > lengths[1] + tolerance || lengths[1] > lengths[2] + tolerance {
        return false;
    }

    // Get metric tensor components
    let a_sq = metric[(0, 0)];
    let b_sq = metric[(1, 1)];
    let ksi = 2.0 * metric[(1, 2)];
    let eta = 2.0 * metric[(0, 2)];
    let zeta = 2.0 * metric[(0, 1)];

    // Check Type I or Type II conditions
    // Use absolute volume to handle left-handed lattices correctly
    let eps = tolerance * lattice.volume().abs().powf(1.0 / 3.0);

    if ksi * eta * zeta > 0.0 {
        // Type I: all off-diagonal products positive or all negative
        // Check |ξ| ≤ B, |η| ≤ A, |ζ| ≤ A
        ksi.abs() <= b_sq + eps && eta.abs() <= a_sq + eps && zeta.abs() <= a_sq + eps
    } else {
        // Type II: mixed signs or zeros
        // Additional checks for Type II
        let sum = ksi.abs() + eta.abs() + zeta.abs();
        sum <= (a_sq + b_sq) + eps
            && ksi.abs() <= b_sq + eps
            && eta.abs() <= a_sq + eps
            && zeta.abs() <= a_sq + eps
    }
}
