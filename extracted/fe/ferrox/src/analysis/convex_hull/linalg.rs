use super::{HULL_EPSILON, HyperplaneND};
use crate::error::{FerroxError, Result};

pub(super) fn subtract_nd(vector_a: &[f64], vector_b: &[f64]) -> Result<Vec<f64>> {
    if vector_a.len() != vector_b.len() {
        return Err(FerroxError::CompositionError {
            reason: format!(
                "Vector dimension mismatch: {} vs {}",
                vector_a.len(),
                vector_b.len()
            ),
        });
    }
    Ok(vector_a
        .iter()
        .zip(vector_b.iter())
        .map(|(value_a, value_b)| value_a - value_b)
        .collect())
}

pub(super) fn dot_nd(vector_a: &[f64], vector_b: &[f64]) -> Result<f64> {
    if vector_a.len() != vector_b.len() {
        return Err(FerroxError::CompositionError {
            reason: format!(
                "Vector dimension mismatch: {} vs {}",
                vector_a.len(),
                vector_b.len()
            ),
        });
    }
    Ok(vector_a
        .iter()
        .zip(vector_b.iter())
        .map(|(value_a, value_b)| value_a * value_b)
        .sum())
}

pub(super) fn norm_nd(vector: &[f64]) -> Result<f64> {
    Ok(dot_nd(vector, vector)?.sqrt())
}

pub(super) fn normalize_nd(vector: &[f64]) -> Result<Vec<f64>> {
    let vector_norm = norm_nd(vector)?;
    if vector_norm < HULL_EPSILON {
        return Ok(vec![0.0; vector.len()]);
    }
    Ok(vector.iter().map(|value| value / vector_norm).collect())
}

pub(super) fn determinant(matrix: &[Vec<f64>]) -> Result<f64> {
    let matrix_size = matrix.len();
    if matrix_size == 0 {
        return Ok(1.0);
    }
    if matrix.iter().any(|row| row.len() != matrix_size) {
        return Err(FerroxError::CompositionError {
            reason: "Determinant requires a square matrix".to_string(),
        });
    }

    let mut work_matrix = matrix.to_vec();
    let mut determinant_value = 1.0;

    for pivot_col in 0..matrix_size {
        let mut pivot_row = pivot_col;
        let mut pivot_abs = work_matrix[pivot_row][pivot_col].abs();
        for (row_idx, row_values) in work_matrix.iter().enumerate().skip(pivot_col + 1) {
            let candidate_abs = row_values[pivot_col].abs();
            if candidate_abs > pivot_abs {
                pivot_abs = candidate_abs;
                pivot_row = row_idx;
            }
        }

        if pivot_abs < HULL_EPSILON {
            return Ok(0.0);
        }

        if pivot_row != pivot_col {
            work_matrix.swap(pivot_row, pivot_col);
            determinant_value = -determinant_value;
        }

        let pivot_value = work_matrix[pivot_col][pivot_col];
        determinant_value *= pivot_value;
        let pivot_row_values = work_matrix[pivot_col].clone();

        for row_values in work_matrix.iter_mut().skip(pivot_col + 1) {
            let factor = row_values[pivot_col] / pivot_value;
            for (row_value, pivot_elem) in row_values
                .iter_mut()
                .skip(pivot_col + 1)
                .zip(pivot_row_values.iter().skip(pivot_col + 1))
            {
                *row_value -= factor * pivot_elem;
            }
        }
    }

    Ok(determinant_value)
}

pub(super) fn compute_hyperplane_nd(face_points: &[Vec<f64>]) -> Result<HyperplaneND> {
    let point_count = face_points.len();
    let dimension_count = face_points.first().map_or(0, Vec::len);
    if point_count < 2 {
        return Ok(HyperplaneND {
            normal: vec![0.0; dimension_count],
            offset: 0.0,
        });
    }
    if face_points
        .iter()
        .any(|point| point.len() != dimension_count)
    {
        return Err(FerroxError::CompositionError {
            reason: "Face points have inconsistent dimensions".to_string(),
        });
    }

    let edge_vectors: Vec<Vec<f64>> = face_points
        .iter()
        .skip(1)
        .map(|point| subtract_nd(point, &face_points[0]))
        .collect::<Result<Vec<_>>>()?;

    let mut normal_components = Vec::with_capacity(dimension_count);
    for col_skip_idx in 0..dimension_count {
        let submatrix: Vec<Vec<f64>> = edge_vectors
            .iter()
            .map(|row| {
                let mut reduced_row = Vec::with_capacity(dimension_count - 1);
                for (col_idx, value) in row.iter().enumerate() {
                    if col_idx != col_skip_idx {
                        reduced_row.push(*value);
                    }
                }
                reduced_row
            })
            .collect();

        let sign = if col_skip_idx % 2 == 0 { 1.0 } else { -1.0 };
        normal_components.push(sign * determinant(&submatrix)?);
    }

    let normalized_normal = normalize_nd(&normal_components)?;
    let offset = -dot_nd(&normalized_normal, &face_points[0])?;
    Ok(HyperplaneND {
        normal: normalized_normal,
        offset,
    })
}

pub(super) fn point_hyperplane_signed_distance_nd(
    plane: &HyperplaneND,
    point: &[f64],
) -> Result<f64> {
    Ok(dot_nd(&plane.normal, point)? + plane.offset)
}

pub(super) fn compute_centroid_nd(points: &[Vec<f64>]) -> std::result::Result<Vec<f64>, String> {
    if points.is_empty() {
        return Ok(vec![]);
    }
    let dimension_count = points[0].len();
    if let Some((point_idx, point)) = points
        .iter()
        .enumerate()
        .find(|(_, point)| point.len() != dimension_count)
    {
        return Err(format!(
            "Point dimension mismatch at index {point_idx}: expected {dimension_count}, got {}",
            point.len()
        ));
    }
    Ok((0..dimension_count)
        .map(|coord_idx| {
            points.iter().map(|point| point[coord_idx]).sum::<f64>() / points.len() as f64
        })
        .collect())
}

pub(super) fn solve_linear_system(matrix_a: &[Vec<f64>], vector_b: &[f64]) -> Option<Vec<f64>> {
    let system_size = matrix_a.len();
    if system_size == 0 {
        return Some(vec![]);
    }
    if vector_b.len() != system_size || matrix_a.iter().any(|row| row.len() != system_size) {
        return None;
    }

    let mut augmented: Vec<Vec<f64>> = matrix_a
        .iter()
        .zip(vector_b.iter())
        .map(|(row, rhs)| {
            let mut merged = row.clone();
            merged.push(*rhs);
            merged
        })
        .collect();

    for pivot_col in 0..system_size {
        let mut pivot_row = pivot_col;
        for row_idx in (pivot_col + 1)..system_size {
            if augmented[row_idx][pivot_col].abs() > augmented[pivot_row][pivot_col].abs() {
                pivot_row = row_idx;
            }
        }

        if augmented[pivot_row][pivot_col].abs() < HULL_EPSILON {
            return None;
        }
        if pivot_row != pivot_col {
            augmented.swap(pivot_row, pivot_col);
        }
        let pivot_row_values = augmented[pivot_col].clone();

        for row_idx in (pivot_col + 1)..system_size {
            let factor = augmented[row_idx][pivot_col] / augmented[pivot_col][pivot_col];
            for (row_value, pivot_value) in augmented[row_idx]
                .iter_mut()
                .take(system_size + 1)
                .skip(pivot_col)
                .zip(
                    pivot_row_values
                        .iter()
                        .take(system_size + 1)
                        .skip(pivot_col),
                )
            {
                *row_value -= factor * pivot_value;
            }
        }
    }

    let mut solution = vec![0.0; system_size];
    for row_idx in (0..system_size).rev() {
        let mut rhs_value = augmented[row_idx][system_size];
        for col_idx in (row_idx + 1)..system_size {
            rhs_value -= augmented[row_idx][col_idx] * solution[col_idx];
        }
        solution[row_idx] = rhs_value / augmented[row_idx][row_idx];
    }
    Some(solution)
}
