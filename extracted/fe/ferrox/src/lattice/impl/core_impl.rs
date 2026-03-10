use super::Lattice;
use nalgebra::{Matrix3, Vector3};
use std::f64::consts::PI;

impl Lattice {
    /// Create a new lattice from a 3x3 matrix.
    ///
    /// The matrix should have lattice vectors as rows.
    pub fn new(matrix: Matrix3<f64>) -> Self {
        Self {
            matrix,
            pbc: [true, true, true],
        }
    }

    /// Create a lattice from a 2D array (row-major).
    pub fn from_array(arr: [[f64; 3]; 3]) -> Self {
        let matrix = Matrix3::from_row_slice(&[
            arr[0][0], arr[0][1], arr[0][2], arr[1][0], arr[1][1], arr[1][2], arr[2][0], arr[2][1],
            arr[2][2],
        ]);
        Self::new(matrix)
    }

    /// Create a lattice from lattice parameters.
    ///
    /// Uses pymatgen's default convention (vesta=False):
    /// - c along z-axis
    /// - a in xz-plane
    /// - b general
    ///
    /// # Arguments
    ///
    /// * `a`, `b`, `c` - Lattice vector lengths in Ångströms
    /// * `alpha`, `beta`, `gamma` - Angles in degrees
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::lattice::Lattice;
    ///
    /// // Hexagonal lattice: a = b, alpha = beta = 90°, gamma = 120°
    /// let lattice = Lattice::from_parameters(3.0, 3.0, 5.0, 90.0, 90.0, 120.0);
    /// let lengths = lattice.lengths();
    /// assert!((lengths[0] - 3.0).abs() < 1e-10);
    /// assert!((lengths[2] - 5.0).abs() < 1e-10);
    /// ```
    pub fn from_parameters(a: f64, b: f64, c: f64, alpha: f64, beta: f64, gamma: f64) -> Self {
        let alpha_rad = alpha * PI / 180.0;
        let beta_rad = beta * PI / 180.0;
        let gamma_rad = gamma * PI / 180.0;

        let cos_alpha = alpha_rad.cos();
        let cos_beta = beta_rad.cos();
        let cos_gamma = gamma_rad.cos();
        let sin_alpha = alpha_rad.sin();
        let sin_beta = beta_rad.sin();

        // pymatgen convention (vesta=False):
        // c along z-axis
        // a in xz-plane
        // b general
        // This matches pymatgen's default behavior for consistency
        let val = ((cos_alpha * cos_beta - cos_gamma) / (sin_alpha * sin_beta)).clamp(-1.0, 1.0);
        let gamma_star = val.acos();

        let matrix = Matrix3::from_rows(&[
            [a * sin_beta, 0.0, a * cos_beta].into(),
            [
                -b * sin_alpha * gamma_star.cos(),
                b * sin_alpha * gamma_star.sin(),
                b * cos_alpha,
            ]
            .into(),
            [0.0, 0.0, c].into(),
        ]);

        Self::new(matrix)
    }

    /// Create a cubic lattice with edge length `a`.
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::lattice::Lattice;
    ///
    /// let lattice = Lattice::cubic(5.43);
    /// assert!((lattice.volume() - 5.43_f64.powi(3)).abs() < 1e-10);
    /// let angles = lattice.angles();
    /// assert!((angles[0] - 90.0).abs() < 1e-10);
    /// ```
    pub fn cubic(a: f64) -> Self {
        Self::from_parameters(a, a, a, 90.0, 90.0, 90.0)
    }

    /// Create a tetragonal lattice.
    pub fn tetragonal(a: f64, c: f64) -> Self {
        Self::from_parameters(a, a, c, 90.0, 90.0, 90.0)
    }

    /// Create an orthorhombic lattice.
    pub fn orthorhombic(a: f64, b: f64, c: f64) -> Self {
        Self::from_parameters(a, b, c, 90.0, 90.0, 90.0)
    }

    /// Create a hexagonal lattice.
    pub fn hexagonal(a: f64, c: f64) -> Self {
        Self::from_parameters(a, a, c, 90.0, 90.0, 120.0)
    }

    /// Get the lattice matrix.
    pub fn matrix(&self) -> &Matrix3<f64> {
        &self.matrix
    }

    /// Get the inverse of the lattice matrix.
    ///
    /// Returns identity matrix if the lattice matrix is singular (degenerate lattice).
    /// Callers expecting valid physical lattices should verify `volume() > 0` first.
    pub fn inv_matrix(&self) -> Matrix3<f64> {
        self.matrix.try_inverse().unwrap_or_else(|| {
            tracing::warn!(
                "Singular lattice matrix (det={:.2e}), using identity inverse",
                self.matrix.determinant()
            );
            Matrix3::identity()
        })
    }

    /// Get the lattice volume.
    pub fn volume(&self) -> f64 {
        self.matrix.determinant().abs()
    }

    /// Get the lengths of the lattice vectors (a, b, c).
    pub fn lengths(&self) -> Vector3<f64> {
        Vector3::new(
            self.matrix.row(0).norm(),
            self.matrix.row(1).norm(),
            self.matrix.row(2).norm(),
        )
    }

    /// Get the lattice angles in degrees (alpha, beta, gamma).
    pub fn angles(&self) -> Vector3<f64> {
        let a = self.matrix.row(0).transpose();
        let b = self.matrix.row(1).transpose();
        let c = self.matrix.row(2).transpose();

        // Clamp cosine values to [-1, 1] to avoid NaN from floating-point drift
        let alpha = (b.dot(&c) / (b.norm() * c.norm())).clamp(-1.0, 1.0).acos() * 180.0 / PI;
        let beta = (a.dot(&c) / (a.norm() * c.norm())).clamp(-1.0, 1.0).acos() * 180.0 / PI;
        let gamma = (a.dot(&b) / (a.norm() * b.norm())).clamp(-1.0, 1.0).acos() * 180.0 / PI;

        Vector3::new(alpha, beta, gamma)
    }

    /// Convert Cartesian coordinates to fractional coordinates.
    ///
    /// Uses the formula: frac = (matrix.T)^(-1) @ cart = (matrix^(-1)).T @ cart
    /// This is consistent with get_cartesian_coords which uses: cart = matrix.T @ frac
    pub fn get_fractional_coords(&self, cart_coords: &[Vector3<f64>]) -> Vec<Vector3<f64>> {
        let inv_t = self.inv_matrix().transpose();
        cart_coords.iter().map(|c| inv_t * c).collect()
    }

    /// Convert fractional coordinates to Cartesian coordinates.
    pub fn get_cartesian_coords(&self, frac_coords: &[Vector3<f64>]) -> Vec<Vector3<f64>> {
        frac_coords
            .iter()
            .map(|f| self.matrix.transpose() * f)
            .collect()
    }

    /// Create a new lattice from a matrix and PBC settings.
    pub fn from_matrix_with_pbc(matrix: Matrix3<f64>, pbc: [bool; 3]) -> Self {
        Self { matrix, pbc }
    }

    /// Convert a single Cartesian coordinate to fractional.
    pub fn get_fractional_coord(&self, cart_coord: &Vector3<f64>) -> Vector3<f64> {
        let inv_t = self.inv_matrix().transpose();
        inv_t * cart_coord
    }

    /// Convert a single fractional coordinate to Cartesian.
    pub fn get_cartesian_coord(&self, frac_coord: &Vector3<f64>) -> Vector3<f64> {
        self.matrix.transpose() * frac_coord
    }

    /// Get the reciprocal lattice.
    ///
    /// For degenerate lattices (near-zero volume), falls back to using the
    /// inverse matrix approach to avoid producing inf/NaN vectors.
    pub fn reciprocal(&self) -> Self {
        let vol = self.volume();

        // Guard against near-zero volume to avoid inf/NaN from division.
        // Threshold chosen to match typical floating-point precision limits.
        const SMALL_EPS: f64 = 1e-15;
        if vol < SMALL_EPS {
            // Mirror inv_matrix()'s defensive behavior: use the safe inverse
            // matrix (which falls back to identity for singular matrices).
            tracing::warn!(
                "Near-zero volume ({:.2e}) in reciprocal(), using inv_matrix fallback",
                vol
            );
            let recip_matrix = self.inv_matrix().transpose() * 2.0 * PI;
            return Self::new(recip_matrix);
        }

        let a = self.matrix.row(0).transpose();
        let b = self.matrix.row(1).transpose();
        let c = self.matrix.row(2).transpose();

        let a_star = b.cross(&c) / vol;
        let b_star = c.cross(&a) / vol;
        let c_star = a.cross(&b) / vol;

        let recip_matrix =
            Matrix3::from_rows(&[a_star.transpose(), b_star.transpose(), c_star.transpose()]);

        Self::new(recip_matrix * 2.0 * PI)
    }

    /// Alias for `reciprocal()` for compatibility.
    pub fn reciprocal_lattice(&self) -> Self {
        self.reciprocal()
    }

    /// Get the metric tensor G = A * A^T.
    pub fn metric_tensor(&self) -> Matrix3<f64> {
        self.matrix * self.matrix.transpose()
    }
}

/// Lattice equality uses a fixed tolerance of 1e-10 on matrix Frobenius norm.
/// For approximate comparisons with custom tolerances, use `find_mapping`.
impl PartialEq for Lattice {
    fn eq(&self, other: &Self) -> bool {
        (self.matrix - other.matrix).norm() < 1e-10
    }
}
