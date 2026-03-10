use super::Lattice;
use crate::error::Result;
use nalgebra::{Matrix3, Vector3};
use std::f64::consts::PI;

impl Lattice {
    // -------------------------------------------------------------------------
    // LLL Reduction (Lenstra-Lenstra-Lovász)
    // -------------------------------------------------------------------------

    /// Perform LLL lattice basis reduction.
    ///
    /// Returns (reduced_matrix, mapping) where:
    /// - reduced_matrix is the LLL-reduced lattice matrix
    /// - mapping transforms original coords to LLL coords
    ///
    /// # Arguments
    ///
    /// * `delta` - Reduction parameter, typically 0.75
    fn calculate_lll(&self, delta: f64) -> (Matrix3<f64>, Matrix3<f64>) {
        // Work with column vectors (transpose of our row-major matrix)
        let mut a = self.matrix.transpose();
        let mut mapping = Matrix3::<f64>::identity();

        // Gram-Schmidt orthogonalization
        let mut b = Matrix3::<f64>::zeros();
        let mut u = Matrix3::<f64>::zeros();
        let mut m = Vector3::<f64>::zeros();

        // Initialize Gram-Schmidt
        b.set_column(0, &a.column(0));
        m[0] = b.column(0).dot(&b.column(0));

        for idx in 1..3 {
            for jdx in 0..idx {
                // Guard against division by zero for degenerate lattices
                u[(idx, jdx)] = if m[jdx] > f64::EPSILON {
                    a.column(idx).dot(&b.column(jdx)) / m[jdx]
                } else {
                    0.0
                };
            }
            let mut b_col = a.column(idx).clone_owned();
            for jdx in 0..idx {
                b_col -= u[(idx, jdx)] * b.column(jdx);
            }
            b.set_column(idx, &b_col);
            m[idx] = b.column(idx).dot(&b.column(idx));
        }

        let mut k = 2usize;
        // LLL typically converges in O(n^3 log B) iterations where B is input size.
        // For 3D lattices, 1000 iterations is extremely generous.
        const MAX_LLL_ITER: usize = 1000;
        let mut iter_count = 0;

        while k <= 3 {
            iter_count += 1;
            if iter_count > MAX_LLL_ITER {
                // LLL should always converge, but guard against numerical issues
                break;
            }
            // Size reduction
            for idx in (1..k).rev() {
                let q = u[(k - 1, idx - 1)].round();
                if q != 0.0 {
                    // Reduce the k-th basis vector
                    let a_col_im1 = a.column(idx - 1).clone_owned();
                    let mut a_col_km1 = a.column(k - 1).clone_owned();
                    a_col_km1 -= q * a_col_im1;
                    a.set_column(k - 1, &a_col_km1);

                    let map_col_im1 = mapping.column(idx - 1).clone_owned();
                    let mut map_col_km1 = mapping.column(k - 1).clone_owned();
                    map_col_km1 -= q * map_col_im1;
                    mapping.set_column(k - 1, &map_col_km1);

                    // Update GS coefficients
                    for jdx in 0..idx {
                        u[(k - 1, jdx)] -= q * u[(idx - 1, jdx)];
                    }
                    u[(k - 1, idx - 1)] -= q;
                }
            }

            // Check Lovász condition
            let b_km1_norm_sq = b.column(k - 1).dot(&b.column(k - 1));
            let b_km2_norm_sq = b.column(k - 2).dot(&b.column(k - 2));
            let u_val = u[(k - 1, k - 2)];

            if b_km1_norm_sq >= (delta - u_val * u_val) * b_km2_norm_sq {
                k += 1;
            } else {
                // Swap k-th and (k-1)-th basis vectors
                let temp_col = a.column(k - 1).clone_owned();
                a.set_column(k - 1, &a.column(k - 2).clone_owned());
                a.set_column(k - 2, &temp_col);

                let temp_map = mapping.column(k - 1).clone_owned();
                mapping.set_column(k - 1, &mapping.column(k - 2).clone_owned());
                mapping.set_column(k - 2, &temp_map);

                // Update Gram-Schmidt coefficients
                for col_idx in (k - 1)..=k.min(3) {
                    for jdx in 0..(col_idx - 1) {
                        // Guard against division by zero for degenerate lattices
                        u[(col_idx - 1, jdx)] = if m[jdx] > f64::EPSILON {
                            a.column(col_idx - 1).dot(&b.column(jdx)) / m[jdx]
                        } else {
                            0.0
                        };
                    }
                    let mut b_col = a.column(col_idx - 1).clone_owned();
                    for jdx in 0..(col_idx - 1) {
                        b_col -= u[(col_idx - 1, jdx)] * b.column(jdx);
                    }
                    b.set_column(col_idx - 1, &b_col);
                    m[col_idx - 1] = b.column(col_idx - 1).dot(&b.column(col_idx - 1));
                }

                if k > 2 {
                    k -= 1;
                }
            }
        }

        // Transpose back to row vectors
        (a.transpose(), mapping.transpose())
    }

    /// Get the LLL-reduced lattice.
    ///
    /// The Lenstra-Lenstra-Lovász (LLL) algorithm produces a basis with
    /// nearly orthogonal vectors, which is useful for PBC calculations.
    ///
    /// # Arguments
    ///
    /// * `delta` - The reduction parameter (typically 0.75)
    pub fn get_lll_reduced(&self, delta: f64) -> Self {
        let (lll_matrix, _) = self.calculate_lll(delta);
        Self::new(lll_matrix)
    }

    /// Get the LLL-reduced matrix with default delta=0.75.
    pub fn lll_matrix(&self) -> Matrix3<f64> {
        self.calculate_lll(0.75).0
    }

    /// Get the transformation matrix to LLL-reduced basis.
    pub fn lll_mapping(&self) -> Matrix3<f64> {
        self.calculate_lll(0.75).1
    }

    /// Get the inverse of the LLL mapping.
    pub fn lll_inverse(&self) -> Matrix3<f64> {
        let mapping = self.lll_mapping();
        mapping.try_inverse().unwrap_or_else(|| {
            tracing::warn!(
                "Singular LLL mapping matrix (det={:.2e}), using identity inverse",
                mapping.determinant()
            );
            Matrix3::identity()
        })
    }

    /// Convert fractional coordinates to LLL-reduced fractional coordinates.
    pub fn get_lll_frac_coords(&self, frac_coords: &[Vector3<f64>]) -> Vec<Vector3<f64>> {
        let inv = self.lll_inverse();
        frac_coords.iter().map(|f| inv * f).collect()
    }

    /// Convert LLL fractional coordinates back to original basis.
    pub fn get_frac_coords_from_lll(&self, lll_frac_coords: &[Vector3<f64>]) -> Vec<Vector3<f64>> {
        let mapping = self.lll_mapping();
        lll_frac_coords.iter().map(|f| mapping * f).collect()
    }

    // -------------------------------------------------------------------------
    // Niggli Reduction (Grosse-Kunstleve algorithm)
    // -------------------------------------------------------------------------

    /// Get the Niggli-reduced lattice.
    ///
    /// Uses the numerically stable algorithm by Grosse-Kunstleve, Sauter & Adams,
    /// Acta Cryst. A60, 1-6 (2004). doi:10.1107/S010876730302186X
    ///
    /// # Arguments
    ///
    /// * `tol` - Numerical tolerance (default 1e-5)
    ///
    /// # Errors
    ///
    /// Returns an error if the reduction fails to converge.
    pub fn get_niggli_reduced(&self, tol: f64) -> Result<Self> {
        // Start with LLL-reduced matrix for numerical stability
        let matrix = self.lll_matrix();
        // Use absolute volume to handle left-handed lattices correctly
        let eps = tol * self.volume().abs().powf(1.0 / 3.0);

        // Define metric tensor G = M * M^T
        let mut g = matrix * matrix.transpose();

        // Niggli reduction typically converges in ~10 iterations for most lattices.
        // 100 is a safe upper bound; if exceeded, the algorithm returns an error.
        const MAX_ITER: usize = 100;

        for _ in 0..MAX_ITER {
            // Extract metric tensor components
            // A = G[0,0], B = G[1,1], C = G[2,2]
            // E = 2*G[1,2], N = 2*G[0,2], Y = 2*G[0,1]
            let (mut a_val, mut b_val, mut c_val) = (g[(0, 0)], g[(1, 1)], g[(2, 2)]);
            let (mut e_val, mut n_val, mut y_val) =
                (2.0 * g[(1, 2)], 2.0 * g[(0, 2)], 2.0 * g[(0, 1)]);

            // A1: Ensure A <= B
            if b_val + eps < a_val
                || (f64::abs(a_val - b_val) < eps && f64::abs(e_val) > f64::abs(n_val) + eps)
            {
                let xform = Matrix3::new(0.0, -1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, -1.0);
                g = xform.transpose() * g * xform;
                // Update values needed for A2 check (a_val recomputed after A3/A4)
                b_val = g[(1, 1)];
                c_val = g[(2, 2)];
                e_val = 2.0 * g[(1, 2)];
                n_val = 2.0 * g[(0, 2)];
                y_val = 2.0 * g[(0, 1)];
            }

            // A2: Ensure B <= C
            if c_val + eps < b_val
                || (f64::abs(b_val - c_val) < eps && f64::abs(n_val) > f64::abs(y_val) + eps)
            {
                let xform = Matrix3::new(-1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, -1.0, 0.0);
                g = xform.transpose() * g * xform;
                continue;
            }

            // A3 & A4: Sign adjustment
            let sign_e = if f64::abs(e_val) < eps {
                0.0
            } else {
                e_val.signum()
            };
            let sign_n = if f64::abs(n_val) < eps {
                0.0
            } else {
                n_val.signum()
            };
            let sign_y = if f64::abs(y_val) < eps {
                0.0
            } else {
                y_val.signum()
            };

            if sign_e * sign_n * sign_y == 1.0 {
                // A3
                let i_val = if sign_e == -1.0 { -1.0 } else { 1.0 };
                let j_val = if sign_n == -1.0 { -1.0 } else { 1.0 };
                let k_val = if sign_y == -1.0 { -1.0 } else { 1.0 };
                let xform = Matrix3::new(i_val, 0.0, 0.0, 0.0, j_val, 0.0, 0.0, 0.0, k_val);
                g = xform.transpose() * g * xform;
            } else if sign_e * sign_n * sign_y == 0.0 || sign_e * sign_n * sign_y == -1.0 {
                // A4
                let mut i_val = if sign_e == 1.0 { -1.0 } else { 1.0 };
                let mut j_val = if sign_n == 1.0 { -1.0 } else { 1.0 };
                let mut k_val = if sign_y == 1.0 { -1.0 } else { 1.0 };

                if i_val * j_val * k_val == -1.0 {
                    if sign_y == 0.0 {
                        k_val = -1.0;
                    } else if sign_n == 0.0 {
                        j_val = -1.0;
                    } else if sign_e == 0.0 {
                        i_val = -1.0;
                    }
                }
                let xform = Matrix3::new(i_val, 0.0, 0.0, 0.0, j_val, 0.0, 0.0, 0.0, k_val);
                g = xform.transpose() * g * xform;
            }

            // Recompute values after sign adjustment (c_val not needed for A5-A8)
            a_val = g[(0, 0)];
            b_val = g[(1, 1)];
            e_val = 2.0 * g[(1, 2)];
            n_val = 2.0 * g[(0, 2)];
            y_val = 2.0 * g[(0, 1)];

            // A5
            if f64::abs(e_val) > b_val + eps
                || (f64::abs(e_val - b_val) < eps && y_val - eps > 2.0 * n_val)
                || (f64::abs(e_val + b_val) < eps && -eps > y_val)
            {
                let sign = -e_val.signum();
                let xform = Matrix3::new(1.0, 0.0, 0.0, 0.0, 1.0, sign, 0.0, 0.0, 1.0);
                g = xform.transpose() * g * xform;
                continue;
            }

            // A6
            if f64::abs(n_val) > a_val + eps
                || (f64::abs(a_val - n_val) < eps && y_val - eps > 2.0 * e_val)
                || (f64::abs(a_val + n_val) < eps && -eps > y_val)
            {
                let sign = -n_val.signum();
                let xform = Matrix3::new(1.0, 0.0, sign, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0);
                g = xform.transpose() * g * xform;
                continue;
            }

            // A7
            if f64::abs(y_val) > a_val + eps
                || (f64::abs(a_val - y_val) < eps && n_val - eps > 2.0 * e_val)
                || (f64::abs(a_val + y_val) < eps && -eps > n_val)
            {
                let sign = -y_val.signum();
                let xform = Matrix3::new(1.0, sign, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0);
                g = xform.transpose() * g * xform;
                continue;
            }

            // A8
            if -eps > e_val + n_val + y_val + a_val + b_val
                || (f64::abs(e_val + n_val + y_val + a_val + b_val) < eps
                    && eps < y_val + (a_val + n_val) * 2.0)
            {
                let xform = Matrix3::new(1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0);
                g = xform.transpose() * g * xform;
                continue;
            }

            // Converged - construct lattice from metric tensor
            let a_len = g[(0, 0)].sqrt();
            let b_len = g[(1, 1)].sqrt();
            let c_len = g[(2, 2)].sqrt();

            let e_final = 2.0 * g[(1, 2)];
            let n_final = 2.0 * g[(0, 2)];
            let y_final = 2.0 * g[(0, 1)];

            // Clamp cosine values to [-1, 1] to avoid NaN from floating-point drift
            let alpha = (e_final / (2.0 * b_len * c_len)).clamp(-1.0, 1.0).acos() * 180.0 / PI;
            let beta = (n_final / (2.0 * a_len * c_len)).clamp(-1.0, 1.0).acos() * 180.0 / PI;
            let gamma = (y_final / (2.0 * a_len * b_len)).clamp(-1.0, 1.0).acos() * 180.0 / PI;

            let niggli_lattice = Self::from_parameters(a_len, b_len, c_len, alpha, beta, gamma);

            // Use find_mapping to get an aligned version (consistent with pymatgen).
            // This ensures the Niggli-reduced lattice has consistent orientation
            // relative to the original lattice, which is crucial for structure matching.
            if let Some((aligned, _, _)) =
                self.find_mapping(&niggli_lattice, tol, 5.0 * tol * 180.0 / PI, true)
            {
                // Ensure positive determinant (right-handed coordinate system).
                // The mapping may flip handedness; negating the matrix restores it.
                // This preserves volume sign convention and is consistent with pymatgen.
                return if aligned.matrix.determinant() > 0.0 {
                    Ok(aligned)
                } else {
                    Ok(Self::new(-aligned.matrix))
                };
            }

            // Fallback if no mapping found
            return Ok(niggli_lattice);
        }

        Err(crate::error::FerroxError::ReductionNotConverged {
            iterations: MAX_ITER,
        })
    }

    /// Get the Niggli-reduced lattice with default tolerance.
    pub fn get_niggli_reduced_default(&self) -> Result<Self> {
        self.get_niggli_reduced(1e-5)
    }
}
