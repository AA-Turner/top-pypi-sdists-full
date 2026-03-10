use nalgebra::Matrix3;

/// Find the transformation matrix between two lattice matrices.
pub(super) fn find_transformation_matrix(
    original: &Matrix3<f64>,
    transformed: &Matrix3<f64>,
) -> Matrix3<f64> {
    // transformed = transform * original
    // So transform = transformed * original^(-1)
    if let Some(inv) = original.try_inverse() {
        transformed * inv
    } else {
        Matrix3::identity()
    }
}

/// Create a shear transformation matrix.
pub(super) fn create_shear_transform(
    target_row: usize,
    source_row: usize,
    factor: i32,
) -> Matrix3<f64> {
    let mut transform = Matrix3::<f64>::identity();
    transform[(target_row, source_row)] = factor as f64;
    transform
}

/// Compute determinant of a 3x3 integer matrix.
/// Uses i64 arithmetic to avoid overflow for large transformation matrices.
pub(super) fn matrix_det_i32(matrix: &[[i32; 3]; 3]) -> i64 {
    let m00 = matrix[0][0] as i64;
    let m01 = matrix[0][1] as i64;
    let m02 = matrix[0][2] as i64;
    let m10 = matrix[1][0] as i64;
    let m11 = matrix[1][1] as i64;
    let m12 = matrix[1][2] as i64;
    let m20 = matrix[2][0] as i64;
    let m21 = matrix[2][1] as i64;
    let m22 = matrix[2][2] as i64;

    m00 * (m11 * m22 - m12 * m21) - m01 * (m10 * m22 - m12 * m20) + m02 * (m10 * m21 - m11 * m20)
}
