use nalgebra::{Matrix3, Vector3};

use super::Structure;

// === Supercell Helper Functions ===

/// Generate all fractional lattice points inside a supercell.
///
/// For a scaling matrix S, finds all integer vectors (i, j, k) such that
/// S^(-1) * (i, j, k) is in [0, 1)^3. These are the lattice translation
/// vectors needed to fill the supercell.
pub(super) fn lattice_points_in_supercell(scaling_matrix: &[[i32; 3]; 3]) -> Vec<Vector3<f64>> {
    // Compute determinant using i64 to avoid overflow for large scaling matrices
    let mat: [[i64; 3]; 3] =
        std::array::from_fn(|row| std::array::from_fn(|col| scaling_matrix[row][col] as i64));
    let det = mat[0][0] * (mat[1][1] * mat[2][2] - mat[1][2] * mat[2][1])
        - mat[0][1] * (mat[1][0] * mat[2][2] - mat[1][2] * mat[2][0])
        + mat[0][2] * (mat[1][0] * mat[2][1] - mat[1][1] * mat[2][0]);
    let n_points = det.unsigned_abs() as usize;

    if n_points == 0 {
        return vec![];
    }

    // Fast path for diagonal matrices (most common case)
    let is_diagonal = scaling_matrix[0][1] == 0
        && scaling_matrix[0][2] == 0
        && scaling_matrix[1][0] == 0
        && scaling_matrix[1][2] == 0
        && scaling_matrix[2][0] == 0
        && scaling_matrix[2][1] == 0;

    if is_diagonal {
        // For diagonal entry s, valid integers i satisfy 0 <= i/s < 1:
        // - If s > 0: i ∈ {0, 1, ..., s-1}
        // - If s < 0: i ∈ {s+1, s+2, ..., 0}
        fn diag_range(s: i32) -> std::ops::Range<i32> {
            if s > 0 { 0..s } else { s + 1..1 }
        }
        let (sx, sy, sz) = (
            scaling_matrix[0][0],
            scaling_matrix[1][1],
            scaling_matrix[2][2],
        );
        let mut points = Vec::with_capacity(n_points);
        for idx in diag_range(sx) {
            for jdx in diag_range(sy) {
                for kdx in diag_range(sz) {
                    points.push(Vector3::new(idx as f64, jdx as f64, kdx as f64));
                }
            }
        }
        return points;
    }

    // General case: search all candidates and filter by inverse transform
    let scale = Matrix3::new(
        scaling_matrix[0][0] as f64,
        scaling_matrix[0][1] as f64,
        scaling_matrix[0][2] as f64,
        scaling_matrix[1][0] as f64,
        scaling_matrix[1][1] as f64,
        scaling_matrix[1][2] as f64,
        scaling_matrix[2][0] as f64,
        scaling_matrix[2][1] as f64,
        scaling_matrix[2][2] as f64,
    );

    let inv_scale = match scale.try_inverse() {
        Some(inv) => inv,
        None => return vec![], // Zero determinant
    };

    let mut points = Vec::with_capacity(n_points);

    // Search range: need to cover all points that could map into the unit cell
    let max_val = scaling_matrix
        .iter()
        .flat_map(|row| row.iter())
        .map(|&x| x.abs())
        .max()
        .unwrap_or(1);
    let search_range = max_val * 2;

    const TOL: f64 = 1e-10;
    for idx in -search_range..=search_range {
        for jdx in -search_range..=search_range {
            for kdx in -search_range..=search_range {
                let lattice_pt = Vector3::new(idx as f64, jdx as f64, kdx as f64);
                let frac = inv_scale * lattice_pt;

                // Check if transformed point is in [0, 1)^3 (with tolerance)
                if frac[0] >= -TOL
                    && frac[0] < 1.0 - TOL
                    && frac[1] >= -TOL
                    && frac[1] < 1.0 - TOL
                    && frac[2] >= -TOL
                    && frac[2] < 1.0 - TOL
                {
                    points.push(lattice_pt);
                }
            }
        }
    }

    // Sanity check: we should have exactly |det| points
    debug_assert_eq!(
        points.len(),
        n_points,
        "Expected {} lattice points, found {}",
        n_points,
        points.len()
    );

    points
}

// === Mul Trait Implementations for Supercell ===

impl std::ops::Mul<i32> for &Structure {
    type Output = Structure;

    /// Create an n x n x n uniform supercell.
    ///
    /// # Panics
    ///
    /// Panics if n <= 0.
    fn mul(self, n: i32) -> Structure {
        assert!(n > 0, "Supercell scaling must be positive, got {n}");
        self.make_supercell_diag([n, n, n])
    }
}

impl std::ops::Mul<[i32; 3]> for &Structure {
    type Output = Structure;

    /// Create an nx x ny x nz diagonal supercell.
    ///
    /// # Panics
    ///
    /// Panics if any n <= 0.
    fn mul(self, ns: [i32; 3]) -> Structure {
        assert!(
            ns.iter().all(|&n| n > 0),
            "Supercell scaling must be positive, got {ns:?}"
        );
        self.make_supercell_diag(ns)
    }
}
