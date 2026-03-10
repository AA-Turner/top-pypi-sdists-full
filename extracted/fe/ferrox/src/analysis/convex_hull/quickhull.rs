use super::linalg::{
    compute_centroid_nd, compute_hyperplane_nd, dot_nd, norm_nd,
    point_hyperplane_signed_distance_nd, solve_linear_system, subtract_nd,
};
use super::{HULL_EPSILON, SimplexFaceND};
use crate::error::{FerroxError, Result};
use std::collections::{HashMap, HashSet};

fn distance_to_affine_hull_nd(point: &[f64], hull_points: &[Vec<f64>]) -> Result<f64> {
    if hull_points.is_empty() {
        return Ok(0.0);
    }
    if hull_points.len() == 1 {
        return norm_nd(&subtract_nd(point, &hull_points[0])?);
    }
    if hull_points.len() == 2 {
        let line_vector = subtract_nd(&hull_points[1], &hull_points[0])?;
        let point_vector = subtract_nd(point, &hull_points[0])?;
        let line_norm_sq = dot_nd(&line_vector, &line_vector)?;
        if line_norm_sq < HULL_EPSILON {
            return norm_nd(&point_vector);
        }
        let projection_weight = dot_nd(&point_vector, &line_vector)? / line_norm_sq;
        let projected_point: Vec<f64> = hull_points[0]
            .iter()
            .zip(line_vector.iter())
            .map(|(origin, direction)| origin + projection_weight * direction)
            .collect();
        return norm_nd(&subtract_nd(point, &projected_point)?);
    }

    let origin_point = &hull_points[0];
    let edge_vectors: Vec<Vec<f64>> = hull_points
        .iter()
        .skip(1)
        .map(|hull_point| subtract_nd(hull_point, origin_point))
        .collect::<Result<Vec<_>>>()?;
    let shifted_point = subtract_nd(point, origin_point)?;

    let gram_matrix: Vec<Vec<f64>> = edge_vectors
        .iter()
        .map(|row_edge| {
            edge_vectors
                .iter()
                .map(|col_edge| dot_nd(row_edge, col_edge))
                .collect::<Result<Vec<_>>>()
        })
        .collect::<Result<Vec<_>>>()?;
    let rhs_vector: Vec<f64> = edge_vectors
        .iter()
        .map(|edge| dot_nd(edge, &shifted_point))
        .collect::<Result<Vec<_>>>()?;

    if let Some(coefficients) = solve_linear_system(&gram_matrix, &rhs_vector) {
        let projected_point: Vec<f64> = origin_point
            .iter()
            .enumerate()
            .map(|(coord_idx, origin)| {
                origin
                    + coefficients
                        .iter()
                        .enumerate()
                        .map(|(edge_idx, coeff)| coeff * edge_vectors[edge_idx][coord_idx])
                        .sum::<f64>()
            })
            .collect();
        return norm_nd(&subtract_nd(point, &projected_point)?);
    }

    let mut orthogonal_basis: Vec<Vec<f64>> = vec![];
    let mut projection = vec![0.0; shifted_point.len()];
    for edge_vector in edge_vectors {
        let mut orthogonal_component = edge_vector.clone();
        for basis_vector in &orthogonal_basis {
            let basis_norm_sq = dot_nd(basis_vector, basis_vector)?;
            if basis_norm_sq > HULL_EPSILON {
                let projection_weight =
                    dot_nd(&orthogonal_component, basis_vector)? / basis_norm_sq;
                for coord_idx in 0..orthogonal_component.len() {
                    orthogonal_component[coord_idx] -= projection_weight * basis_vector[coord_idx];
                }
            }
        }
        let orthogonal_norm_sq = dot_nd(&orthogonal_component, &orthogonal_component)?;
        if orthogonal_norm_sq > HULL_EPSILON {
            let point_weight = dot_nd(&shifted_point, &orthogonal_component)? / orthogonal_norm_sq;
            for coord_idx in 0..projection.len() {
                projection[coord_idx] += point_weight * orthogonal_component[coord_idx];
            }
            orthogonal_basis.push(orthogonal_component);
        }
    }
    norm_nd(&subtract_nd(&shifted_point, &projection)?)
}

fn choose_initial_simplex_nd(points: &[Vec<f64>]) -> Result<Option<Vec<usize>>> {
    let dimension_count = points.first().map_or(0, Vec::len);
    if dimension_count == 0 || points.len() < dimension_count + 1 {
        return Ok(None);
    }

    let sample_size = points.len().min(100);
    let sample_indices: Vec<usize> = if points.len() <= sample_size {
        (0..points.len()).collect()
    } else {
        (0..sample_size)
            .map(|idx| idx * points.len() / sample_size)
            .collect()
    };

    let mut best_pair = (0usize, 1usize);
    let mut best_distance = -1.0;
    for first_idx in &sample_indices {
        for second_idx in &sample_indices {
            if first_idx >= second_idx {
                continue;
            }
            let distance = norm_nd(&subtract_nd(&points[*first_idx], &points[*second_idx])?)?;
            if distance > best_distance {
                best_distance = distance;
                best_pair = (*first_idx, *second_idx);
            }
        }
    }
    if best_distance < HULL_EPSILON {
        return Ok(None);
    }

    let mut chosen_indices = vec![best_pair.0, best_pair.1];
    let mut chosen_set: HashSet<usize> = chosen_indices.iter().copied().collect();

    while chosen_indices.len() < dimension_count + 1 {
        let current_points: Vec<Vec<f64>> = chosen_indices
            .iter()
            .map(|point_idx| points[*point_idx].clone())
            .collect();
        let mut best_candidate_idx = None;
        let mut best_candidate_distance = -1.0;

        for (point_idx, point) in points.iter().enumerate() {
            if chosen_set.contains(&point_idx) {
                continue;
            }
            let distance = distance_to_affine_hull_nd(point, &current_points)?;
            if distance > best_candidate_distance {
                best_candidate_distance = distance;
                best_candidate_idx = Some(point_idx);
            }
        }

        let Some(candidate_idx) = best_candidate_idx else {
            return Ok(None);
        };
        if best_candidate_distance < HULL_EPSILON {
            return Ok(None);
        }
        chosen_indices.push(candidate_idx);
        chosen_set.insert(candidate_idx);
    }
    Ok(Some(chosen_indices))
}

fn make_face_nd(
    points: &[Vec<f64>],
    vertex_indices: Vec<usize>,
    interior_point: &[f64],
) -> Result<SimplexFaceND> {
    let face_points: Vec<Vec<f64>> = vertex_indices
        .iter()
        .map(|point_idx| points[*point_idx].clone())
        .collect();
    let mut plane = compute_hyperplane_nd(&face_points)?;
    let centroid =
        compute_centroid_nd(&face_points).map_err(|reason| FerroxError::CompositionError {
            reason: format!("Failed to compute face centroid: {reason}"),
        })?;
    let interior_distance = point_hyperplane_signed_distance_nd(&plane, interior_point)?;
    if interior_distance > 0.0 {
        plane.normal.iter_mut().for_each(|value| *value *= -1.0);
        plane.offset *= -1.0;
    }
    Ok(SimplexFaceND {
        vertex_indices,
        plane,
        centroid,
        outside_points: HashSet::new(),
    })
}

fn assign_outside_points_nd(
    face: &mut SimplexFaceND,
    points: &[Vec<f64>],
    candidate_indices: &[usize],
) -> Result<()> {
    face.outside_points.clear();
    for point_idx in candidate_indices {
        let distance = point_hyperplane_signed_distance_nd(&face.plane, &points[*point_idx])?;
        if distance > HULL_EPSILON {
            face.outside_points.insert(*point_idx);
        }
    }
    Ok(())
}

fn farthest_outside_point_nd(
    points: &[Vec<f64>],
    face: &SimplexFaceND,
) -> Result<Option<(usize, f64)>> {
    let mut best_result: Option<(usize, f64)> = None;
    for point_idx in &face.outside_points {
        let distance = point_hyperplane_signed_distance_nd(&face.plane, &points[*point_idx])?;
        if best_result
            .as_ref()
            .is_none_or(|(_, best_distance)| distance > *best_distance)
        {
            best_result = Some((*point_idx, distance));
        }
    }
    Ok(best_result)
}

fn build_horizon_nd(faces: &[SimplexFaceND], visible_indices: &HashSet<usize>) -> Vec<Vec<usize>> {
    let mut ridge_count: HashMap<Vec<usize>, Vec<usize>> = HashMap::new();
    for face_idx in visible_indices {
        let vertices = &faces[*face_idx].vertex_indices;
        for skip_idx in 0..vertices.len() {
            let ridge: Vec<usize> = vertices
                .iter()
                .enumerate()
                .filter_map(|(idx, vertex)| if idx != skip_idx { Some(*vertex) } else { None })
                .collect();
            let mut sorted_ridge = ridge.clone();
            sorted_ridge.sort_unstable();
            match ridge_count.entry(sorted_ridge) {
                std::collections::hash_map::Entry::Vacant(vacant_entry) => {
                    vacant_entry.insert(ridge);
                }
                std::collections::hash_map::Entry::Occupied(mut occupied_entry) => {
                    occupied_entry.insert(vec![]);
                }
            }
        }
    }
    ridge_count
        .into_values()
        .filter(|ridge| !ridge.is_empty())
        .collect()
}

/// Compute the full N-dimensional convex hull with a generalized Quickhull algorithm.
pub fn compute_quickhull_nd(points: &[Vec<f64>]) -> Result<Vec<SimplexFaceND>> {
    if points.is_empty() {
        return Ok(vec![]);
    }
    let dimension_count = points[0].len();
    if points
        .iter()
        .any(|point| point.len() != dimension_count || point.is_empty())
    {
        return Err(FerroxError::CompositionError {
            reason: "All points must share one non-zero dimensionality".to_string(),
        });
    }
    if points.len() < dimension_count + 1 {
        return Ok(vec![]);
    }

    let Some(initial_simplex) = choose_initial_simplex_nd(points)? else {
        return Ok(vec![]);
    };
    let interior_point = compute_centroid_nd(
        &initial_simplex
            .iter()
            .map(|point_idx| points[*point_idx].clone())
            .collect::<Vec<Vec<f64>>>(),
    )
    .map_err(|reason| FerroxError::CompositionError {
        reason: format!("Failed to compute simplex interior point: {reason}"),
    })?;

    let mut faces = Vec::with_capacity(dimension_count + 1);
    for skip_idx in 0..=dimension_count {
        let face_vertices: Vec<usize> = initial_simplex
            .iter()
            .enumerate()
            .filter_map(|(idx, point_idx)| {
                if idx != skip_idx {
                    Some(*point_idx)
                } else {
                    None
                }
            })
            .collect();
        faces.push(make_face_nd(points, face_vertices, &interior_point)?);
    }

    let remaining_indices: Vec<usize> = (0..points.len())
        .filter(|point_idx| !initial_simplex.contains(point_idx))
        .collect();
    for face in &mut faces {
        assign_outside_points_nd(face, points, &remaining_indices)?;
    }

    loop {
        let mut chosen_face_idx = None;
        let mut chosen_point_idx = 0usize;
        let mut max_distance = -1.0;

        for (face_idx, face) in faces.iter().enumerate() {
            if face.outside_points.is_empty() {
                continue;
            }
            if let Some((point_idx, distance)) = farthest_outside_point_nd(points, face)?
                && distance > max_distance
            {
                max_distance = distance;
                chosen_face_idx = Some(face_idx);
                chosen_point_idx = point_idx;
            }
        }

        if chosen_face_idx.is_none() {
            break;
        }

        let mut visible_faces = HashSet::new();
        for (face_idx, face) in faces.iter().enumerate() {
            let distance =
                point_hyperplane_signed_distance_nd(&face.plane, &points[chosen_point_idx])?;
            if distance > HULL_EPSILON {
                visible_faces.insert(face_idx);
            }
        }

        let horizon_ridges = build_horizon_nd(&faces, &visible_faces);
        let mut candidate_points = HashSet::new();
        for face_idx in &visible_faces {
            for outside_idx in &faces[*face_idx].outside_points {
                candidate_points.insert(*outside_idx);
            }
        }

        faces = faces
            .into_iter()
            .enumerate()
            .filter(|(face_idx, _face)| !visible_faces.contains(face_idx))
            .map(|(_face_idx, face)| face)
            .collect();

        let mut new_faces = Vec::with_capacity(horizon_ridges.len());
        for ridge in horizon_ridges {
            let mut new_vertices = ridge;
            new_vertices.push(chosen_point_idx);
            new_faces.push(make_face_nd(points, new_vertices, &interior_point)?);
        }

        for candidate_idx in candidate_points {
            if candidate_idx == chosen_point_idx {
                continue;
            }
            let mut best_face_idx = None;
            let mut best_distance = HULL_EPSILON;
            for (new_face_idx, new_face) in new_faces.iter().enumerate() {
                let distance =
                    point_hyperplane_signed_distance_nd(&new_face.plane, &points[candidate_idx])?;
                if distance > best_distance {
                    best_distance = distance;
                    best_face_idx = Some(new_face_idx);
                }
            }
            if let Some(face_idx) = best_face_idx {
                new_faces[face_idx].outside_points.insert(candidate_idx);
            }
        }

        faces.extend(new_faces);
    }

    Ok(faces)
}

/// Filter hull faces to only the lower hull (downward in energy dimension).
pub fn compute_lower_hull_nd(faces: &[SimplexFaceND]) -> Vec<SimplexFaceND> {
    faces
        .iter()
        .filter(|face| {
            face.plane
                .normal
                .last()
                .is_some_and(|value| *value < -HULL_EPSILON)
        })
        .cloned()
        .collect()
}

#[derive(Debug, Clone)]
pub(super) struct SimplexModelND {
    pub(super) vertices: Vec<Vec<f64>>,
    pub(super) vertices_spatial: Vec<Vec<f64>>,
    pub(super) bbox_min: Vec<f64>,
    pub(super) bbox_max: Vec<f64>,
}
