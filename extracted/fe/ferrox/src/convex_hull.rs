//! Convex hull construction and 0 K energetics.
//!
//! This module implements a generalized N-dimensional lower convex hull and
//! energy-above-hull (`e_above_hull`) calculations inspired by matterviz and
//! pymatgen convex-hull logic.

use crate::composition::Composition;
use crate::element::Element;
use crate::error::{FerroxError, Result};
use std::collections::{BTreeSet, HashMap, HashSet};

/// Numerical tolerance used throughout hull calculations.
const HULL_EPSILON: f64 = 1e-9;
/// Slightly relaxed tolerance for barycentric membership checks.
const BARYCENTRIC_TOL: f64 = HULL_EPSILON * 1.001;

/// Input entry for convex-hull calculations.
#[derive(Debug, Clone)]
pub struct ConvexHullEntry {
    /// Optional external identifier (e.g. mp-id).
    pub entry_id: Option<String>,
    /// Composition of the phase.
    pub composition: Composition,
    /// Total energy (eV) of the entry.
    pub energy: f64,
    /// Optional precomputed per-atom energy (eV/atom).
    pub energy_per_atom: Option<f64>,
    /// Optional precomputed formation energy (eV/atom).
    pub e_form_per_atom: Option<f64>,
    /// Optional total-energy correction (eV).
    pub correction: Option<f64>,
}

impl ConvexHullEntry {
    /// Construct a new entry from composition and total energy.
    pub fn new(composition: Composition, energy: f64) -> Self {
        Self {
            entry_id: None,
            composition,
            energy,
            energy_per_atom: None,
            e_form_per_atom: None,
            correction: None,
        }
    }

    /// Build a stable key for this entry.
    pub fn id_or_formula(&self) -> String {
        self.entry_id
            .clone()
            .unwrap_or_else(|| self.composition.reduced_formula())
    }

    /// Return true if this entry is unary.
    pub fn is_unary(&self) -> bool {
        self.composition.element_composition().num_elements() == 1
    }

    /// Return this entry's corrected energy per atom.
    pub fn corrected_energy_per_atom(&self) -> Result<f64> {
        let atom_count = self.composition.num_atoms();
        if !atom_count.is_finite() || atom_count <= 0.0 {
            return Err(FerroxError::CompositionError {
                reason: format!(
                    "Entry {} has non-positive atom count ({atom_count})",
                    self.id_or_formula()
                ),
            });
        }

        let value = if let Some(correction_total) = self.correction {
            let total_energy = if let Some(energy_per_atom) = self.energy_per_atom {
                energy_per_atom * atom_count
            } else {
                self.energy
            };
            (total_energy + correction_total) / atom_count
        } else if let Some(energy_per_atom) = self.energy_per_atom {
            energy_per_atom
        } else {
            self.energy / atom_count
        };

        if !value.is_finite() {
            return Err(FerroxError::CompositionError {
                reason: format!("Entry {} has non-finite energy", self.id_or_formula()),
            });
        }
        Ok(value)
    }
}

/// Hyperplane in N dimensions: `normal · x + offset = 0`.
#[derive(Debug, Clone)]
pub struct HyperplaneND {
    /// Unit normal vector.
    pub normal: Vec<f64>,
    /// Plane offset.
    pub offset: f64,
}

/// Facet on an N-dimensional convex hull.
#[derive(Debug, Clone)]
pub struct SimplexFaceND {
    /// Point indices defining this facet.
    pub vertex_indices: Vec<usize>,
    /// Facet hyperplane.
    pub plane: HyperplaneND,
    /// Facet centroid.
    pub centroid: Vec<f64>,
    /// Point indices known to lie outside this facet.
    pub outside_points: HashSet<usize>,
}

/// Lower hull model built from reference entries.
#[derive(Debug, Clone)]
pub struct LowerHullND {
    /// Element ordering used for barycentric-like coordinates.
    pub element_order: Vec<Element>,
    /// Points used to construct the hull.
    pub reference_points: Vec<Vec<f64>>,
    /// Lower hull facets (downward in energy dimension).
    pub lower_facets: Vec<SimplexFaceND>,
}

fn subtract_nd(vector_a: &[f64], vector_b: &[f64]) -> Result<Vec<f64>> {
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

fn dot_nd(vector_a: &[f64], vector_b: &[f64]) -> Result<f64> {
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

fn norm_nd(vector: &[f64]) -> Result<f64> {
    Ok(dot_nd(vector, vector)?.sqrt())
}

fn normalize_nd(vector: &[f64]) -> Result<Vec<f64>> {
    let vector_norm = norm_nd(vector)?;
    if vector_norm < HULL_EPSILON {
        return Ok(vec![0.0; vector.len()]);
    }
    Ok(vector.iter().map(|value| value / vector_norm).collect())
}

fn determinant(matrix: &[Vec<f64>]) -> Result<f64> {
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

fn compute_hyperplane_nd(face_points: &[Vec<f64>]) -> Result<HyperplaneND> {
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

fn point_hyperplane_signed_distance_nd(plane: &HyperplaneND, point: &[f64]) -> Result<f64> {
    Ok(dot_nd(&plane.normal, point)? + plane.offset)
}

fn compute_centroid_nd(points: &[Vec<f64>]) -> std::result::Result<Vec<f64>, String> {
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

fn solve_linear_system(matrix_a: &[Vec<f64>], vector_b: &[f64]) -> Option<Vec<f64>> {
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
struct SimplexModelND {
    vertices: Vec<Vec<f64>>,
    vertices_spatial: Vec<Vec<f64>>,
    bbox_min: Vec<f64>,
    bbox_max: Vec<f64>,
}

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

/// Find the lowest-energy unary references for each element.
pub fn find_lowest_energy_unary_refs(entries: &[ConvexHullEntry]) -> Result<HashMap<Element, f64>> {
    let mut lowest_refs: HashMap<Element, f64> = HashMap::new();
    for entry in entries {
        if !entry.is_unary() {
            continue;
        }
        let element_composition = entry.composition.element_composition();
        let Some(element) = element_composition.unique_elements().iter().next().copied() else {
            continue;
        };
        let entry_energy = entry.corrected_energy_per_atom()?;
        lowest_refs
            .entry(element)
            .and_modify(|current_energy| {
                if entry_energy < *current_energy {
                    *current_energy = entry_energy;
                }
            })
            .or_insert(entry_energy);
    }
    Ok(lowest_refs)
}

/// Compute formation energy per atom for an entry.
pub fn compute_e_form_per_atom(
    entry: &ConvexHullEntry,
    unary_refs: &HashMap<Element, f64>,
) -> Result<f64> {
    if let Some(precomputed_e_form) = entry.e_form_per_atom
        && precomputed_e_form.is_finite()
    {
        return Ok(precomputed_e_form);
    }

    let atom_count = entry.composition.num_atoms();
    if !atom_count.is_finite() || atom_count <= 0.0 {
        return Err(FerroxError::CompositionError {
            reason: format!(
                "Entry {} has non-positive atom count ({atom_count})",
                entry.id_or_formula()
            ),
        });
    }

    let elemental_composition = entry.composition.element_composition();
    let mut composition_elements: Vec<Element> = elemental_composition
        .unique_elements()
        .into_iter()
        .collect();
    composition_elements.sort_unstable_by_key(Element::atomic_number);
    let mut ref_energy_sum = 0.0;
    for element in composition_elements {
        let amount = elemental_composition.get_element_total(element);
        let Some(unary_ref_energy) = unary_refs.get(&element).copied() else {
            return Err(FerroxError::CompositionError {
                reason: format!(
                    "Missing unary reference for element {} while computing formation energy of {}",
                    element.symbol(),
                    entry.id_or_formula()
                ),
            });
        };
        ref_energy_sum += (amount / atom_count) * unary_ref_energy;
    }
    Ok(entry.corrected_energy_per_atom()? - ref_energy_sum)
}

fn has_finite_precomputed_e_form(entry: &ConvexHullEntry) -> bool {
    entry.e_form_per_atom.is_some_and(f64::is_finite)
}

fn compute_entry_e_form(
    entry: &ConvexHullEntry,
    unary_refs: Option<&HashMap<Element, f64>>,
) -> Result<f64> {
    if let Some(precomputed_e_form) = entry.e_form_per_atom
        && precomputed_e_form.is_finite()
    {
        return Ok(precomputed_e_form);
    }
    let Some(unary_refs) = unary_refs else {
        return Err(FerroxError::CompositionError {
            reason: format!(
                "Entry {} requires absolute energy inputs because e_form_per_atom is missing",
                entry.id_or_formula()
            ),
        });
    };
    compute_e_form_per_atom(entry, unary_refs)
}

fn sorted_elements_from_entries(entries: &[ConvexHullEntry]) -> Vec<Element> {
    let mut elements: BTreeSet<(u8, Element)> = BTreeSet::new();
    for entry in entries {
        for element in entry.composition.element_composition().unique_elements() {
            elements.insert((element.atomic_number(), element));
        }
    }
    elements.into_iter().map(|(_, element)| element).collect()
}

fn composition_to_spatial_coords(
    composition: &Composition,
    element_order: &[Element],
) -> Result<Vec<f64>> {
    if element_order.is_empty() {
        return Err(FerroxError::CompositionError {
            reason: "Cannot build coordinates for an empty element set".to_string(),
        });
    }
    let atom_count = composition.num_atoms();
    if !atom_count.is_finite() || atom_count <= 0.0 {
        return Err(FerroxError::CompositionError {
            reason: format!("Invalid composition atom count: {atom_count}"),
        });
    }

    let elemental_composition = composition.element_composition();
    let element_set: HashSet<Element> = element_order.iter().copied().collect();
    for present_element in elemental_composition.unique_elements() {
        if !element_set.contains(&present_element) {
            return Err(FerroxError::CompositionError {
                reason: format!(
                    "Composition includes element {} outside reference element set",
                    present_element.symbol()
                ),
            });
        }
    }

    if element_order.len() == 1 {
        return Ok(vec![]);
    }
    let spatial_dim = element_order.len() - 1;
    let mut coords = Vec::with_capacity(spatial_dim);
    for element in &element_order[..spatial_dim] {
        coords.push(elemental_composition.get_element_total(*element) / atom_count);
    }
    Ok(coords)
}

fn entry_to_hull_point(
    entry: &ConvexHullEntry,
    element_order: &[Element],
    e_form_per_atom: f64,
) -> Result<Vec<f64>> {
    let mut point = composition_to_spatial_coords(&entry.composition, element_order)?;
    point.push(e_form_per_atom);
    Ok(point)
}

fn should_inject_synthetic_corners(
    reference_entries: &[ConvexHullEntry],
    unary_refs: Option<&HashMap<Element, f64>>,
) -> bool {
    unary_refs.is_some() || !reference_entries.iter().any(ConvexHullEntry::is_unary)
}

/// Build lower hull from reference entries.
pub fn build_lower_hull(reference_entries: &[ConvexHullEntry]) -> Result<LowerHullND> {
    if reference_entries.is_empty() {
        return Err(FerroxError::CompositionError {
            reason: "Reference entries cannot be empty".to_string(),
        });
    }

    let element_order = sorted_elements_from_entries(reference_entries);
    if element_order.is_empty() {
        return Err(FerroxError::CompositionError {
            reason: "Reference entries contain no valid elements".to_string(),
        });
    }

    let needs_unary_refs = reference_entries
        .iter()
        .any(|entry| !has_finite_precomputed_e_form(entry));
    let unary_refs = if needs_unary_refs {
        Some(find_lowest_energy_unary_refs(reference_entries)?)
    } else {
        None
    };
    let mut reference_points = Vec::with_capacity(reference_entries.len() + element_order.len());

    for entry in reference_entries {
        let e_form_per_atom = compute_entry_e_form(entry, unary_refs.as_ref())?;
        reference_points.push(entry_to_hull_point(entry, &element_order, e_form_per_atom)?);
    }

    if should_inject_synthetic_corners(reference_entries, unary_refs.as_ref()) {
        let n_elements = element_order.len();
        let spatial_dim = n_elements.saturating_sub(1);
        for element_idx in 0..n_elements {
            let mut corner_point = vec![0.0; spatial_dim + 1];
            if n_elements > 1 && element_idx < spatial_dim {
                corner_point[element_idx] = 1.0;
            }
            let corner_exists = reference_points.iter().any(|point| {
                point.len() == corner_point.len()
                    && point
                        .iter()
                        .zip(corner_point.iter())
                        .all(|(coord, corner_coord)| (coord - corner_coord).abs() < HULL_EPSILON)
            });
            if !corner_exists {
                reference_points.push(corner_point);
            }
        }
    }

    let all_facets = compute_quickhull_nd(&reference_points)?;
    let lower_facets = compute_lower_hull_nd(&all_facets);

    Ok(LowerHullND {
        element_order,
        reference_points,
        lower_facets,
    })
}

/// Compute `e_above_hull` values for entries against a reference hull.
pub fn calculate_e_above_hull(
    entries: &[ConvexHullEntry],
    reference_entries: &[ConvexHullEntry],
) -> Result<Vec<f64>> {
    if entries.is_empty() {
        return Ok(vec![]);
    }
    let hull_model = build_lower_hull(reference_entries)?;
    let needs_unary_refs = entries
        .iter()
        .chain(reference_entries.iter())
        .any(|entry| !has_finite_precomputed_e_form(entry));
    let unary_refs = if needs_unary_refs {
        Some(find_lowest_energy_unary_refs(reference_entries)?)
    } else {
        None
    };
    if hull_model.element_order.len() == 1 || hull_model.lower_facets.is_empty() {
        let reference_min_e_form =
            reference_entries
                .iter()
                .try_fold(f64::INFINITY, |current_min, entry| {
                    compute_entry_e_form(entry, unary_refs.as_ref())
                        .map(|value| current_min.min(value))
                })?;
        return entries
            .iter()
            .map(|entry| {
                compute_entry_e_form(entry, unary_refs.as_ref())
                    .map(|value| (value - reference_min_e_form).max(0.0))
            })
            .collect();
    }

    let query_points: Vec<Vec<f64>> = entries
        .iter()
        .map(|entry| {
            let e_form_per_atom = compute_entry_e_form(entry, unary_refs.as_ref())?;
            entry_to_hull_point(entry, &hull_model.element_order, e_form_per_atom)
        })
        .collect::<Result<Vec<_>>>()?;

    Ok(compute_e_above_hull_nd(
        &query_points,
        &hull_model.lower_facets,
        &hull_model.reference_points,
    ))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::iter::zip;

    fn make_entry(formula: &str, e_form_per_atom: f64, entry_id: &str) -> ConvexHullEntry {
        let composition =
            Composition::from_formula(formula).expect("formula should parse in tests");
        ConvexHullEntry {
            entry_id: Some(entry_id.to_string()),
            composition,
            energy: e_form_per_atom,
            energy_per_atom: Some(e_form_per_atom),
            e_form_per_atom: Some(e_form_per_atom),
            correction: None,
        }
    }

    fn make_entry_total_energy(
        formula: &str,
        total_energy: f64,
        entry_id: &str,
    ) -> ConvexHullEntry {
        let composition =
            Composition::from_formula(formula).expect("formula should parse in tests");
        ConvexHullEntry {
            entry_id: Some(entry_id.to_string()),
            composition,
            energy: total_energy,
            energy_per_atom: None,
            e_form_per_atom: None,
            correction: None,
        }
    }

    #[test]
    fn test_corrected_energy_per_atom_variants() {
        let test_cases = [(None, -4.0), (Some(0.6), -3.8)];
        for (case_idx, (correction, expected_value)) in test_cases.into_iter().enumerate() {
            let mut entry = make_entry_total_energy("Li2O", -12.0, &format!("li2o_{case_idx}"));
            entry.correction = correction;
            let corrected_value = entry
                .corrected_energy_per_atom()
                .expect("corrected energy should compute");
            assert_approx_eq(corrected_value, expected_value, 1e-12);
        }
    }

    fn assert_approx_eq(actual_value: f64, expected_value: f64, tolerance: f64) {
        assert!(
            (actual_value - expected_value).abs() < tolerance,
            "expected {actual_value} to be within {tolerance} of {expected_value}"
        );
    }

    fn assert_distances_approx_eq(
        actual_distances: &[f64],
        expected_distances: &[f64],
        tolerance: f64,
    ) {
        assert_eq!(actual_distances.len(), expected_distances.len());
        for (actual_distance, expected_distance) in zip(actual_distances, expected_distances) {
            assert_approx_eq(*actual_distance, *expected_distance, tolerance);
        }
    }

    #[test]
    fn test_find_lowest_energy_unary_refs_selects_lowest_polymorph() {
        let refs = vec![
            make_entry("Li", -0.1, "li_high"),
            make_entry("Li", -0.3, "li_low"),
            make_entry("O", -0.4, "o"),
            make_entry("LiO", -1.0, "lio"),
        ];
        let unary_refs = find_lowest_energy_unary_refs(&refs).expect("unary refs should build");
        assert_eq!(unary_refs.len(), 2);
        assert_approx_eq(unary_refs[&Element::Li], -0.3, 1e-12);
        assert_approx_eq(unary_refs[&Element::O], -0.4, 1e-12);
    }

    #[test]
    fn test_compute_e_form_per_atom_with_missing_reference_errors() {
        let entry = make_entry_total_energy("LiO", -8.0, "lio");
        let refs = HashMap::from([(Element::Li, -1.0)]);
        let result = compute_e_form_per_atom(&entry, &refs);
        let error = result.expect_err("missing unary reference should fail");
        let FerroxError::CompositionError { reason } = error else {
            panic!("expected CompositionError");
        };
        assert!(reason.contains("Missing unary reference for element O"));
    }

    #[test]
    fn test_compute_e_form_per_atom_prefers_precomputed_value() {
        let entry = make_entry("LiO", -123.0, "lio_precomputed");
        let refs = HashMap::from([(Element::Li, -1.0), (Element::O, -2.0)]);
        let value =
            compute_e_form_per_atom(&entry, &refs).expect("precomputed value should be used");
        assert_approx_eq(value, -123.0, 1e-12);
    }

    #[test]
    fn test_build_lower_hull_requires_non_empty_references() {
        let result = build_lower_hull(&[]);
        let error = result.expect_err("empty references should fail");
        let FerroxError::CompositionError { reason } = error else {
            panic!("expected CompositionError");
        };
        assert!(reason.contains("Reference entries cannot be empty"));
    }

    #[test]
    fn test_build_lower_hull_requires_terminal_entries_for_elements() {
        let refs = vec![make_entry_total_energy("LiO", -8.0, "lio_only")];
        let result = build_lower_hull(&refs);
        let error = result.expect_err("missing unary references should fail");
        let FerroxError::CompositionError { reason } = error else {
            panic!("expected CompositionError");
        };
        assert!(reason.contains("Missing unary reference for element Li"));
    }

    #[test]
    fn test_binary_e_above_hull() {
        let references = vec![
            make_entry("Li", 0.0, "li"),
            make_entry("O", 0.0, "o"),
            make_entry("LiO", -1.0, "lio"),
            make_entry("Li2O", -0.2, "li2o"),
        ];
        let queries = vec![make_entry("Li2O", -0.2, "li2o")];
        let distances =
            calculate_e_above_hull(&queries, &references).expect("binary hull should compute");
        assert_distances_approx_eq(&distances, &[0.466_666_666_7], 1e-6);
    }

    #[test]
    fn test_unary_system_e_above_hull_is_non_negative_formation_energy() {
        let references = vec![make_entry("Fe", 0.0, "fe_ref")];
        let queries = vec![
            make_entry("Fe", 0.5, "fe_unstable"),
            make_entry("Fe", -0.5, "fe_lower"),
        ];
        let distances =
            calculate_e_above_hull(&queries, &references).expect("unary hull should compute");
        assert_distances_approx_eq(&distances, &[0.5, 0.0], 1e-12);
    }

    #[test]
    fn test_unary_system_with_multiple_reference_entries_uses_reference_minimum() {
        let references = vec![
            make_entry("Fe", -0.5, "fe_ref_low"),
            make_entry("Fe", 0.0, "fe_ref_high"),
        ];
        let queries = vec![make_entry("Fe", 0.2, "fe_query")];
        let distances =
            calculate_e_above_hull(&queries, &references).expect("unary hull should compute");
        assert_distances_approx_eq(&distances, &[0.7], 1e-12);
    }

    #[test]
    fn test_calculate_e_above_hull_errors_on_empty_refs() {
        let queries = vec![make_entry("Li", 0.0, "li")];
        let result = calculate_e_above_hull(&queries, &[]);
        let error = result.expect_err("empty references should fail");
        let FerroxError::CompositionError { reason } = error else {
            panic!("expected CompositionError");
        };
        assert!(reason.contains("Reference entries cannot be empty"));
    }

    #[test]
    fn test_calculate_e_above_hull_errors_on_missing_element_in_reference_system() {
        let references = vec![
            make_entry("Li", 0.0, "li_ref"),
            make_entry("O", 0.0, "o_ref"),
        ];
        let queries = vec![make_entry_total_energy("LiF", -0.4, "lif")];
        let result = calculate_e_above_hull(&queries, &references);
        let error = result.expect_err("missing reference element should fail");
        let FerroxError::CompositionError { reason } = error else {
            panic!("expected CompositionError");
        };
        assert!(reason.contains("Missing unary reference for element F"));
    }

    #[test]
    fn test_calculate_e_above_hull_returns_empty_for_empty_query_batch() {
        let references = vec![make_entry("Li", 0.0, "li"), make_entry("O", 0.0, "o")];
        let distances =
            calculate_e_above_hull(&[], &references).expect("empty query should return empty");
        assert!(distances.is_empty());
    }

    #[test]
    fn test_batch_results_match_single_entry_calls() {
        let references = vec![
            make_entry("Li", 0.0, "li"),
            make_entry("O", 0.0, "o"),
            make_entry("LiO", -1.0, "lio"),
            make_entry("Li2O", -0.2, "li2o"),
        ];
        let queries = vec![
            make_entry("Li2O", -0.2, "q1"),
            make_entry("LiO", -1.0, "q2"),
            make_entry("LiO", -0.7, "q3"),
        ];
        let batch = calculate_e_above_hull(&queries, &references).expect("batch should compute");
        assert_eq!(batch.len(), queries.len());
        for (query, batch_value) in zip(&queries, &batch) {
            let single = calculate_e_above_hull(std::slice::from_ref(query), &references)
                .expect("single should compute");
            assert!((single[0] - batch_value).abs() < 1e-12);
        }
    }

    #[test]
    fn test_ternary_same_composition_above_hull_positive_distance() {
        let references = vec![
            make_entry("Li", 0.0, "li"),
            make_entry("Na", 0.0, "na"),
            make_entry("K", 0.0, "k"),
            make_entry("LiNaK", -1.0, "linak_stable"),
        ];
        let queries = vec![
            make_entry("LiNaK", -0.8, "linak_unstable"),
            make_entry("LiNaK", -1.0, "linak_on_hull"),
        ];
        let distances =
            calculate_e_above_hull(&queries, &references).expect("ternary should compute");
        assert_distances_approx_eq(&distances, &[0.2, 0.0], 1e-12);
    }

    #[test]
    fn test_quinary_general_nd_hull() {
        let references = vec![
            make_entry("Li", 0.0, "li"),
            make_entry("Na", 0.0, "na"),
            make_entry("K", 0.0, "k"),
            make_entry("Rb", 0.0, "rb"),
            make_entry("Cs", 0.0, "cs"),
            make_entry("LiNaKRbCs", -0.2, "mixed_stable"),
        ];
        let queries = vec![
            make_entry("LiNaKRbCs", -0.1, "mixed_unstable"),
            make_entry("Li", 0.0, "li_query"),
        ];
        let distances =
            calculate_e_above_hull(&queries, &references).expect("quinary hull should compute");
        assert_distances_approx_eq(&distances, &[0.1, 0.0], 1e-8);
    }

    #[test]
    fn test_degenerate_hull_falls_back_to_non_negative_formation_energy() {
        let references = vec![
            make_entry("Li", 0.0, "li"),
            make_entry("Na", 0.0, "na"),
            make_entry("K", 0.0, "k"),
            make_entry("LiNaK", 0.0, "linak"),
        ];
        let queries = vec![
            make_entry("LiNaK", 0.2, "query_positive"),
            make_entry("LiNaK", -0.1, "query_negative"),
        ];
        let distances =
            calculate_e_above_hull(&queries, &references).expect("degenerate hull should compute");
        assert_distances_approx_eq(&distances, &[0.2, 0.0], 1e-12);
    }

    #[test]
    fn test_compute_quickhull_nd_returns_empty_for_underdetermined_inputs() {
        let test_cases: Vec<Vec<Vec<f64>>> = vec![
            vec![],
            vec![vec![0.0, 0.0]],
            vec![vec![0.0, 0.0], vec![1.0, 0.0]],
            vec![
                vec![0.0, 0.0, 0.0],
                vec![1.0, 0.0, 0.0],
                vec![0.0, 1.0, 0.0],
            ],
        ];
        for points in test_cases {
            let facets = compute_quickhull_nd(&points).expect("quickhull should not error");
            assert!(facets.is_empty());
        }
    }

    #[test]
    fn test_compute_quickhull_nd_5d_simplex_has_6_facets() {
        let points = vec![
            vec![0.0, 0.0, 0.0, 0.0, 0.0],
            vec![1.0, 0.0, 0.0, 0.0, 0.0],
            vec![0.0, 1.0, 0.0, 0.0, 0.0],
            vec![0.0, 0.0, 1.0, 0.0, 0.0],
            vec![0.0, 0.0, 0.0, 1.0, 0.0],
            vec![0.0, 0.0, 0.0, 0.0, 1.0],
        ];
        let facets = compute_quickhull_nd(&points).expect("quickhull should compute in 5D");
        assert_eq!(facets.len(), 6);
    }

    #[test]
    fn test_compute_lower_hull_nd_filters_by_last_normal_component() {
        let face_up = SimplexFaceND {
            vertex_indices: vec![0, 1, 2],
            plane: HyperplaneND {
                normal: vec![0.0, 0.0, 1.0],
                offset: 0.0,
            },
            centroid: vec![0.0, 0.0, 0.0],
            outside_points: HashSet::new(),
        };
        let face_down = SimplexFaceND {
            vertex_indices: vec![0, 1, 2],
            plane: HyperplaneND {
                normal: vec![0.0, 0.0, -1.0],
                offset: 0.0,
            },
            centroid: vec![0.0, 0.0, 0.0],
            outside_points: HashSet::new(),
        };
        let lower = compute_lower_hull_nd(&[face_up, face_down.clone()]);
        assert_eq!(lower.len(), 1);
        assert_eq!(lower[0].vertex_indices, face_down.vertex_indices);
    }

    #[test]
    fn test_compute_e_above_hull_nd_interpolates_simple_triangle() {
        let points = vec![
            vec![0.0, 0.0, 0.0],
            vec![1.0, 0.0, 0.0],
            vec![0.0, 1.0, 0.0],
        ];
        let lower_face = SimplexFaceND {
            vertex_indices: vec![0, 1, 2],
            plane: HyperplaneND {
                normal: vec![0.0, 0.0, -1.0],
                offset: 0.0,
            },
            centroid: vec![0.0, 0.0, 0.0],
            outside_points: HashSet::new(),
        };
        let query_points = vec![vec![0.25, 0.25, 0.0], vec![0.25, 0.25, 0.4]];
        let distances = compute_e_above_hull_nd(&query_points, &[lower_face], &points);
        assert_distances_approx_eq(&distances, &[0.0, 0.4], 1e-12);
    }

    #[test]
    fn test_compute_e_above_hull_nd_returns_nan_outside_domain() {
        let points = vec![
            vec![0.0, 0.0, 0.0],
            vec![1.0, 0.0, 0.0],
            vec![0.0, 1.0, 0.0],
        ];
        let lower_face = SimplexFaceND {
            vertex_indices: vec![0, 1, 2],
            plane: HyperplaneND {
                normal: vec![0.0, 0.0, -1.0],
                offset: 0.0,
            },
            centroid: vec![0.0, 0.0, 0.0],
            outside_points: HashSet::new(),
        };
        let query_points = vec![vec![1.2, 1.2, 0.1]];
        let distances = compute_e_above_hull_nd(&query_points, &[lower_face], &points);
        assert!(distances[0].is_nan());
    }

    #[test]
    fn test_compute_e_above_hull_nd_returns_nan_when_hull_is_empty() {
        let points = vec![
            vec![0.0, 0.0, 0.0],
            vec![1.0, 0.0, 0.0],
            vec![0.0, 1.0, 0.0],
        ];
        let distances = compute_e_above_hull_nd(&[vec![0.25, 0.25, 0.1]], &[], &points);
        assert!(distances[0].is_nan());
    }

    #[test]
    fn test_compute_e_above_hull_nd_returns_nan_for_malformed_facets() {
        let points = vec![
            vec![0.0, 0.0, 0.0],
            vec![1.0, 0.0, 0.0],
            vec![0.0, 1.0, 0.0],
        ];
        let malformed_empty_face = SimplexFaceND {
            vertex_indices: vec![],
            plane: HyperplaneND {
                normal: vec![0.0, 0.0, -1.0],
                offset: 0.0,
            },
            centroid: vec![],
            outside_points: HashSet::new(),
        };
        let malformed_oob_face = SimplexFaceND {
            vertex_indices: vec![0, 1, 99],
            plane: HyperplaneND {
                normal: vec![0.0, 0.0, -1.0],
                offset: 0.0,
            },
            centroid: vec![0.0, 0.0, 0.0],
            outside_points: HashSet::new(),
        };
        let distances = compute_e_above_hull_nd(
            &[vec![0.25, 0.25, 0.1]],
            &[malformed_empty_face, malformed_oob_face],
            &points,
        );
        assert!(distances[0].is_nan());
    }

    #[test]
    fn test_sorted_elements_from_entries_uses_atomic_number_ordering() {
        let refs = vec![
            make_entry("Na", 0.0, "na"),
            make_entry("Li", 0.0, "li"),
            make_entry("O", 0.0, "o"),
        ];
        let ordering = sorted_elements_from_entries(&refs);
        assert_eq!(ordering, vec![Element::Li, Element::O, Element::Na]);
    }

    #[test]
    fn test_reference_and_query_with_same_entries_are_all_on_hull() {
        let references = vec![
            make_entry("Li", 0.0, "li"),
            make_entry("O", 0.0, "o"),
            make_entry("LiO", -1.0, "lio"),
        ];
        let mut queries = references.clone();
        queries.push(make_entry("LiO", -0.8, "lio_above"));
        let distances = calculate_e_above_hull(&queries, &references)
            .expect("self-hull distances should compute");
        assert_distances_approx_eq(&distances, &[0.0, 0.0, 0.0, 0.2], 1e-12);
    }

    #[test]
    fn test_precomputed_e_form_reference_set_is_used_without_synthetic_zero_corners() {
        let references = vec![
            make_entry("Li", 1.0, "li"),
            make_entry("O", 1.0, "o"),
            make_entry("LiO", 0.5, "lio"),
        ];
        let distances =
            calculate_e_above_hull(&references, &references).expect("self-hull should compute");
        assert_distances_approx_eq(&distances, &[0.0, 0.0, 0.0], 1e-12);
    }
}
