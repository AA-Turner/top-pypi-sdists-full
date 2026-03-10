use super::linalg::solve_linear_system;
use super::quickhull::SimplexModelND;
use super::{BARYCENTRIC_TOL, HULL_EPSILON, SimplexFaceND};

fn build_simplex_models_nd(faces: &[SimplexFaceND], points: &[Vec<f64>]) -> Vec<SimplexModelND> {
    faces
        .iter()
        .filter_map(|face| {
            if face.vertex_indices.is_empty() {
                return None;
            }
            let vertices: Vec<Vec<f64>> = face
                .vertex_indices
                .iter()
                .filter_map(|point_idx| points.get(*point_idx).cloned())
                .collect();
            if vertices.len() != face.vertex_indices.len() {
                return None;
            }
            let coord_count = vertices[0].len();
            if coord_count < 2 || vertices.iter().any(|vertex| vertex.len() != coord_count) {
                return None;
            }
            let spatial_dim = coord_count - 1;
            let vertices_spatial: Vec<Vec<f64>> = vertices
                .iter()
                .map(|vertex| vertex[..spatial_dim].to_vec())
                .collect();

            let bbox_min: Vec<f64> = (0..spatial_dim)
                .map(|coord_idx| {
                    vertices_spatial
                        .iter()
                        .map(|vertex| vertex[coord_idx])
                        .fold(f64::INFINITY, f64::min)
                })
                .collect();
            let bbox_max: Vec<f64> = (0..spatial_dim)
                .map(|coord_idx| {
                    vertices_spatial
                        .iter()
                        .map(|vertex| vertex[coord_idx])
                        .fold(f64::NEG_INFINITY, f64::max)
                })
                .collect();
            Some(SimplexModelND {
                vertices,
                vertices_spatial,
                bbox_min,
                bbox_max,
            })
        })
        .collect()
}

fn point_in_simplex_nd(point: &[f64], simplex_vertices: &[Vec<f64>]) -> Option<Vec<f64>> {
    if simplex_vertices.is_empty() {
        return None;
    }
    let vertex_count = simplex_vertices.len();
    let spatial_dim = point.len();
    if vertex_count != spatial_dim + 1 {
        return None;
    }

    let first_vertex = &simplex_vertices[0];
    let edge_vectors: Vec<Vec<f64>> = simplex_vertices
        .iter()
        .skip(1)
        .map(|vertex| {
            vertex
                .iter()
                .zip(first_vertex.iter())
                .map(|(vertex_coord, first_coord)| vertex_coord - first_coord)
                .collect::<Vec<f64>>()
        })
        .collect();
    let rhs_vector: Vec<f64> = point
        .iter()
        .zip(first_vertex.iter())
        .map(|(point_coord, first_coord)| point_coord - first_coord)
        .collect();

    let mut matrix = vec![vec![0.0; spatial_dim]; spatial_dim];
    for row_idx in 0..spatial_dim {
        for col_idx in 0..spatial_dim {
            matrix[row_idx][col_idx] = edge_vectors[col_idx][row_idx];
        }
    }
    let coefficients = solve_linear_system(&matrix, &rhs_vector)?;
    let coefficient_sum: f64 = coefficients.iter().sum();
    let mut barycentric = vec![1.0 - coefficient_sum];
    barycentric.extend(coefficients);
    if barycentric.iter().all(|value| *value >= -BARYCENTRIC_TOL) {
        Some(barycentric)
    } else {
        None
    }
}

/// Compute energy above hull for query points in coordinate space.
///
/// Points must be in the same coordinate space as the hull points, with energy in
/// the final coordinate.
pub fn compute_e_above_hull_nd(
    query_points: &[Vec<f64>],
    lower_hull_facets: &[SimplexFaceND],
    all_points: &[Vec<f64>],
) -> Vec<f64> {
    let simplex_models = build_simplex_models_nd(lower_hull_facets, all_points);
    query_points
        .iter()
        .map(|query_point| {
            if query_point.len() < 2 {
                return f64::NAN;
            }
            let coord_count = query_point.len();
            let spatial_coords = &query_point[..coord_count - 1];
            let query_energy = query_point[coord_count - 1];
            let mut hull_energy: Option<f64> = None;

            for model in &simplex_models {
                let is_outside_bbox =
                    spatial_coords.iter().enumerate().any(|(coord_idx, value)| {
                        *value < model.bbox_min[coord_idx] - HULL_EPSILON
                            || *value > model.bbox_max[coord_idx] + HULL_EPSILON
                    });
                if is_outside_bbox {
                    continue;
                }

                let Some(barycentric) =
                    point_in_simplex_nd(spatial_coords, &model.vertices_spatial)
                else {
                    continue;
                };
                let simplex_energy = barycentric
                    .iter()
                    .enumerate()
                    .map(|(vertex_idx, coeff)| coeff * model.vertices[vertex_idx][coord_count - 1])
                    .sum::<f64>();
                hull_energy = Some(
                    hull_energy.map_or(simplex_energy, |min_energy| min_energy.min(simplex_energy)),
                );
            }

            let Some(reference_energy) = hull_energy else {
                return f64::NAN;
            };
            let energy_above_hull = query_energy - reference_energy;
            if energy_above_hull > HULL_EPSILON {
                energy_above_hull
            } else {
                0.0
            }
        })
        .collect()
}
