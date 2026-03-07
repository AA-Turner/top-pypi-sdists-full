//! Brillouin zone computation for crystal lattices.
//!
//! Computes the first Brillouin zone (Wigner-Seitz cell in reciprocal space)
//! by intersecting half-spaces defined by perpendicular bisector planes of
//! reciprocal lattice vectors.
//!
//! # Algorithm
//!
//! 1. Compute the reciprocal lattice from the real-space lattice
//! 2. Generate candidate reciprocal lattice vectors G = h·b₁ + k·b₂ + l·b₃
//! 3. For each G, define a Bragg plane (perpendicular bisector at G/2)
//! 4. Find BZ vertices as intersections of 3 planes that satisfy all half-space constraints
//! 5. Group vertices into faces by their generating Bragg planes
//! 6. Compute the BZ volume via signed tetrahedra
//!
//! # Examples
//!
//! ```rust,ignore
//! use ferrox::lattice::Lattice;
//! use ferrox::analysis::brillouin::compute_brillouin_zone;
//!
//! let lattice = Lattice::cubic(4.0);
//! let bz = compute_brillouin_zone(&lattice);
//! assert_eq!(bz.faces.len(), 6); // cube has 6 faces
//! ```

use nalgebra::{Matrix3, Vector3};

use crate::lattice::Lattice;

/// Numerical tolerance for geometric comparisons.
const TOL: f64 = 1e-8;

/// Tolerance for classifying a vertex as lying on a Bragg plane.
/// Larger than TOL to accommodate accumulated floating-point error
/// from solving 3×3 linear systems.
const ON_PLANE_TOL: f64 = 1e-6;

/// A polygonal face of the Brillouin zone.
#[derive(Debug, Clone)]
pub struct BrillouinFace {
    /// Indices into `BrillouinZone.vertices` defining this face polygon,
    /// ordered counterclockwise when viewed from outside.
    pub vertices: Vec<usize>,
    /// Outward face normal (unit vector).
    pub normal: Vector3<f64>,
    /// Miller indices [h, k, l] of the reciprocal lattice vector that
    /// generated this face's Bragg plane.
    pub miller_index: [i32; 3],
}

/// The first Brillouin zone of a crystal lattice.
#[derive(Debug, Clone)]
pub struct BrillouinZone {
    /// Vertex positions in reciprocal space (Å⁻¹).
    pub vertices: Vec<Vector3<f64>>,
    /// Polygonal faces of the BZ boundary.
    pub faces: Vec<BrillouinFace>,
    /// Volume of the BZ (Å⁻³), equal to (2π)³ / V_real.
    pub volume: f64,
}

/// A Bragg plane (perpendicular bisector of a reciprocal lattice vector).
#[derive(Debug, Clone)]
struct BraggPlane {
    /// Unit normal vector pointing from origin toward the reciprocal lattice point.
    normal: Vector3<f64>,
    /// Distance from origin to the plane (= |G| / 2).
    distance: f64,
    /// Miller indices (h, k, l) of the reciprocal lattice vector G.
    miller_index: [i32; 3],
}

/// Lattice type classification for high-symmetry k-point selection.
#[derive(Debug, Clone, Copy, PartialEq)]
enum LatticeType {
    SimpleCubic,
    FccPrimitive,
    BccPrimitive,
    Hexagonal,
    Tetragonal,
    Orthorhombic,
    Other,
}

/// Compute the first Brillouin zone for a given real-space lattice.
///
/// Returns a `BrillouinZone` containing the vertices, faces, and volume
/// of the Wigner-Seitz cell in reciprocal space.
pub fn compute_brillouin_zone(lattice: &Lattice) -> BrillouinZone {
    let recip = lattice.reciprocal();
    let recip_matrix = recip.matrix();

    let planes = generate_bragg_planes(recip_matrix);
    let vertices = find_bz_vertices(&planes);
    let faces = build_faces(&vertices, &planes);
    let volume = compute_volume(&vertices, &faces);

    BrillouinZone {
        vertices,
        faces,
        volume,
    }
}

/// Return labeled high-symmetry k-points in Cartesian reciprocal coordinates.
///
/// Classifies the lattice type from its metric and returns the standard
/// Setyawan-Curtarolo k-path points for that type. Points are returned as
/// `(label, position)` pairs in Cartesian reciprocal space (Å⁻¹).
pub fn get_high_symmetry_points(lattice: &Lattice) -> Vec<(String, Vector3<f64>)> {
    let recip = lattice.reciprocal();
    let recip_matrix = recip.matrix();
    let lattice_type = classify_lattice(lattice);

    let frac_points: Vec<(&str, Vector3<f64>)> = match lattice_type {
        LatticeType::SimpleCubic => vec![
            ("Gamma", Vector3::new(0.0, 0.0, 0.0)),
            ("X", Vector3::new(0.0, 0.5, 0.0)),
            ("M", Vector3::new(0.5, 0.5, 0.0)),
            ("R", Vector3::new(0.5, 0.5, 0.5)),
        ],
        LatticeType::FccPrimitive => vec![
            ("Gamma", Vector3::new(0.0, 0.0, 0.0)),
            ("K", Vector3::new(3.0 / 8.0, 3.0 / 8.0, 3.0 / 4.0)),
            ("L", Vector3::new(0.5, 0.5, 0.5)),
            ("U", Vector3::new(5.0 / 8.0, 1.0 / 4.0, 5.0 / 8.0)),
            ("W", Vector3::new(0.5, 1.0 / 4.0, 3.0 / 4.0)),
            ("X", Vector3::new(0.5, 0.0, 0.5)),
        ],
        LatticeType::BccPrimitive => vec![
            ("Gamma", Vector3::new(0.0, 0.0, 0.0)),
            ("H", Vector3::new(0.5, -0.5, 0.5)),
            ("N", Vector3::new(0.0, 0.0, 0.5)),
            ("P", Vector3::new(0.25, 0.25, 0.25)),
        ],
        LatticeType::Hexagonal => vec![
            ("Gamma", Vector3::new(0.0, 0.0, 0.0)),
            ("A", Vector3::new(0.0, 0.0, 0.5)),
            ("H", Vector3::new(1.0 / 3.0, 1.0 / 3.0, 0.5)),
            ("K", Vector3::new(1.0 / 3.0, 1.0 / 3.0, 0.0)),
            ("L", Vector3::new(0.5, 0.0, 0.5)),
            ("M", Vector3::new(0.5, 0.0, 0.0)),
        ],
        LatticeType::Tetragonal => vec![
            ("Gamma", Vector3::new(0.0, 0.0, 0.0)),
            ("A", Vector3::new(0.5, 0.5, 0.5)),
            ("M", Vector3::new(0.5, 0.5, 0.0)),
            ("R", Vector3::new(0.0, 0.5, 0.5)),
            ("X", Vector3::new(0.0, 0.5, 0.0)),
            ("Z", Vector3::new(0.0, 0.0, 0.5)),
        ],
        LatticeType::Orthorhombic => vec![
            ("Gamma", Vector3::new(0.0, 0.0, 0.0)),
            ("R", Vector3::new(0.5, 0.5, 0.5)),
            ("S", Vector3::new(0.5, 0.5, 0.0)),
            ("T", Vector3::new(0.0, 0.5, 0.5)),
            ("U", Vector3::new(0.5, 0.0, 0.5)),
            ("X", Vector3::new(0.5, 0.0, 0.0)),
            ("Y", Vector3::new(0.0, 0.5, 0.0)),
            ("Z", Vector3::new(0.0, 0.0, 0.5)),
        ],
        LatticeType::Other => vec![("Gamma", Vector3::new(0.0, 0.0, 0.0))],
    };

    // Convert fractional reciprocal coords to Cartesian:
    // k_cart = frac.x * b1 + frac.y * b2 + frac.z * b3 = B^T * frac
    let recip_t = recip_matrix.transpose();
    frac_points
        .into_iter()
        .map(|(name, frac)| (name.to_string(), recip_t * frac))
        .collect()
}

// === Internal helpers ===

/// Classify lattice type from its metric (lengths and angles).
fn classify_lattice(lattice: &Lattice) -> LatticeType {
    let lengths = lattice.lengths();
    let angles = lattice.angles();
    let (len_a, len_b, len_c) = (lengths.x, lengths.y, lengths.z);
    let (alpha, beta, gamma) = (angles.x, angles.y, angles.z);

    const ANG_TOL: f64 = 1.5; // degrees
    const LEN_REL_TOL: f64 = 0.02;

    let ab_eq = (len_a - len_b).abs() / len_a.max(1e-10) < LEN_REL_TOL;
    let bc_eq = (len_b - len_c).abs() / len_b.max(1e-10) < LEN_REL_TOL;
    let ac_eq = (len_a - len_c).abs() / len_a.max(1e-10) < LEN_REL_TOL;
    let all_eq = ab_eq && bc_eq;

    let all_90 = (alpha - 90.0).abs() < ANG_TOL
        && (beta - 90.0).abs() < ANG_TOL
        && (gamma - 90.0).abs() < ANG_TOL;

    if all_eq && all_90 {
        return LatticeType::SimpleCubic;
    }

    if all_eq {
        if (alpha - 60.0).abs() < ANG_TOL
            && (beta - 60.0).abs() < ANG_TOL
            && (gamma - 60.0).abs() < ANG_TOL
        {
            return LatticeType::FccPrimitive;
        }
        // BCC primitive: angles = acos(-1/3) ≈ 109.47°
        let bcc_angle = (-1.0_f64 / 3.0).acos().to_degrees();
        if (alpha - bcc_angle).abs() < ANG_TOL * 2.0
            && (beta - bcc_angle).abs() < ANG_TOL * 2.0
            && (gamma - bcc_angle).abs() < ANG_TOL * 2.0
        {
            return LatticeType::BccPrimitive;
        }
    }

    // Hexagonal: a ≈ b, alpha ≈ beta ≈ 90°, gamma ≈ 120°
    let ab_90 = (alpha - 90.0).abs() < ANG_TOL && (beta - 90.0).abs() < ANG_TOL;
    if ab_eq && ab_90 && (gamma - 120.0).abs() < ANG_TOL {
        return LatticeType::Hexagonal;
    }

    // Tetragonal: two equal lengths, all angles 90°
    if (ab_eq || bc_eq || ac_eq) && all_90 {
        return LatticeType::Tetragonal;
    }

    // Orthorhombic: three unequal lengths, all angles 90°
    if all_90 {
        return LatticeType::Orthorhombic;
    }

    LatticeType::Other
}

/// Generate Bragg planes from reciprocal lattice vectors G = h·b₁ + k·b₂ + l·b₃.
///
/// Considers all (h, k, l) in [-2, 2]³ and prunes dominated parallel planes
/// (keeping only the closest to the origin for each direction).
fn generate_bragg_planes(recip_matrix: &Matrix3<f64>) -> Vec<BraggPlane> {
    let b1 = recip_matrix.row(0).transpose().into_owned();
    let b2 = recip_matrix.row(1).transpose().into_owned();
    let b3 = recip_matrix.row(2).transpose().into_owned();

    let mut all_planes = Vec::new();

    for h in -2i32..=2 {
        for k in -2i32..=2 {
            for l in -2i32..=2 {
                if h == 0 && k == 0 && l == 0 {
                    continue;
                }
                let g_vec = b1 * h as f64 + b2 * k as f64 + b3 * l as f64;
                let g_norm = g_vec.norm();
                if g_norm < TOL {
                    continue;
                }
                all_planes.push(BraggPlane {
                    normal: g_vec / g_norm,
                    distance: g_norm / 2.0,
                    miller_index: [h, k, l],
                });
            }
        }
    }

    // Prune dominated planes: for each direction, keep only the closest plane.
    // Planes with anti-parallel normals are different faces (opposite sides of BZ).
    let mut pruned: Vec<BraggPlane> = Vec::new();
    'outer: for plane in &all_planes {
        for existing in &mut pruned {
            let dot = existing.normal.dot(&plane.normal);
            if (dot - 1.0).abs() < TOL {
                if plane.distance < existing.distance - TOL {
                    *existing = plane.clone();
                }
                continue 'outer;
            }
        }
        pruned.push(plane.clone());
    }

    pruned.sort_by(|a, b| a.distance.total_cmp(&b.distance));
    pruned
}

/// Find BZ vertices as intersections of exactly 3 Bragg planes
/// that lie within all half-spaces.
fn find_bz_vertices(planes: &[BraggPlane]) -> Vec<Vector3<f64>> {
    let n_planes = planes.len();
    let mut vertices = Vec::new();

    for idx_i in 0..n_planes {
        for idx_j in (idx_i + 1)..n_planes {
            for idx_k in (idx_j + 1)..n_planes {
                // Build system N · v = d where rows of N are plane normals
                let matrix = Matrix3::from_rows(&[
                    planes[idx_i].normal.transpose(),
                    planes[idx_j].normal.transpose(),
                    planes[idx_k].normal.transpose(),
                ]);

                if matrix.determinant().abs() < 1e-12 {
                    continue;
                }
                let Some(inv) = matrix.try_inverse() else {
                    continue;
                };

                let rhs = Vector3::new(
                    planes[idx_i].distance,
                    planes[idx_j].distance,
                    planes[idx_k].distance,
                );
                let vertex = inv * rhs;

                // Reject vertices outside any half-space
                let inside = planes
                    .iter()
                    .all(|plane| vertex.dot(&plane.normal) <= plane.distance + TOL);
                if !inside {
                    continue;
                }

                let is_dup = vertices
                    .iter()
                    .any(|existing: &Vector3<f64>| (existing - vertex).norm() < TOL * 10.0);
                if !is_dup {
                    vertices.push(vertex);
                }
            }
        }
    }

    vertices
}

/// Group vertices into faces based on which Bragg plane they lie on,
/// and order face vertices counterclockwise when viewed from outside.
fn build_faces(vertices: &[Vector3<f64>], planes: &[BraggPlane]) -> Vec<BrillouinFace> {
    let mut faces = Vec::new();

    for plane in planes {
        let face_vert_indices: Vec<usize> = vertices
            .iter()
            .enumerate()
            .filter(|(_, vert)| (vert.dot(&plane.normal) - plane.distance).abs() < ON_PLANE_TOL)
            .map(|(idx, _)| idx)
            .collect();

        if face_vert_indices.len() < 3 {
            continue;
        }

        let ordered = order_face_vertices(vertices, &face_vert_indices, &plane.normal);

        faces.push(BrillouinFace {
            vertices: ordered,
            normal: plane.normal,
            miller_index: plane.miller_index,
        });
    }

    faces
}

/// Order coplanar vertices counterclockwise when viewed from the normal direction.
///
/// Projects vertices onto a local 2D coordinate system in the plane and sorts
/// by polar angle around the centroid.
fn order_face_vertices(
    all_vertices: &[Vector3<f64>],
    face_indices: &[usize],
    normal: &Vector3<f64>,
) -> Vec<usize> {
    let centroid: Vector3<f64> = face_indices
        .iter()
        .map(|&idx| all_vertices[idx])
        .fold(Vector3::zeros(), |acc, vert| acc + vert)
        / face_indices.len() as f64;

    let first_dir = all_vertices[face_indices[0]] - centroid;
    let u_axis = if first_dir.norm() > TOL {
        first_dir.normalize()
    } else {
        let seed = if normal.x.abs() < 0.9 {
            Vector3::x()
        } else {
            Vector3::y()
        };
        normal.cross(&seed).normalize()
    };
    let w_axis = normal.cross(&u_axis).normalize();

    let mut indexed_angles: Vec<(usize, f64)> = face_indices
        .iter()
        .map(|&idx| {
            let relative = all_vertices[idx] - centroid;
            let angle = relative.dot(&w_axis).atan2(relative.dot(&u_axis));
            (idx, angle)
        })
        .collect();

    indexed_angles.sort_by(|a, b| a.1.total_cmp(&b.1));
    indexed_angles.into_iter().map(|(idx, _)| idx).collect()
}

/// Compute polyhedron volume via signed tetrahedra (divergence theorem).
///
/// For each triangulated face, sums the signed volume of tetrahedra formed
/// with the origin. Works for any closed convex polyhedron.
fn compute_volume(vertices: &[Vector3<f64>], faces: &[BrillouinFace]) -> f64 {
    let mut total = 0.0;

    for face in faces {
        if face.vertices.len() < 3 {
            continue;
        }
        let v0 = vertices[face.vertices[0]];
        for k in 1..(face.vertices.len() - 1) {
            let v1 = vertices[face.vertices[k]];
            let v2 = vertices[face.vertices[k + 1]];
            total += v0.dot(&v1.cross(&v2));
        }
    }

    total.abs() / 6.0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn classify_simple_cubic() {
        let lattice = Lattice::cubic(5.0);
        assert_eq!(classify_lattice(&lattice), LatticeType::SimpleCubic);
    }

    #[test]
    fn classify_fcc_primitive() {
        let a_conv = 4.0;
        let lattice = Lattice::from_array([
            [0.0, a_conv / 2.0, a_conv / 2.0],
            [a_conv / 2.0, 0.0, a_conv / 2.0],
            [a_conv / 2.0, a_conv / 2.0, 0.0],
        ]);
        assert_eq!(classify_lattice(&lattice), LatticeType::FccPrimitive);
    }

    #[test]
    fn classify_bcc_primitive() {
        let a_conv = 4.0;
        let lattice = Lattice::from_array([
            [-a_conv / 2.0, a_conv / 2.0, a_conv / 2.0],
            [a_conv / 2.0, -a_conv / 2.0, a_conv / 2.0],
            [a_conv / 2.0, a_conv / 2.0, -a_conv / 2.0],
        ]);
        assert_eq!(classify_lattice(&lattice), LatticeType::BccPrimitive);
    }

    #[test]
    fn classify_hexagonal() {
        let lattice = Lattice::hexagonal(3.0, 5.0);
        assert_eq!(classify_lattice(&lattice), LatticeType::Hexagonal);
    }

    #[test]
    fn classify_tetragonal() {
        let lattice = Lattice::from_array([[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 6.0]]);
        assert_eq!(classify_lattice(&lattice), LatticeType::Tetragonal);
    }

    #[test]
    fn classify_orthorhombic() {
        let lattice = Lattice::from_array([[3.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 5.0]]);
        assert_eq!(classify_lattice(&lattice), LatticeType::Orthorhombic);
    }

    #[test]
    fn classify_triclinic_as_other() {
        let lattice = Lattice::from_array([[3.0, 0.5, 0.2], [0.3, 4.0, 0.4], [0.1, 0.6, 5.0]]);
        assert_eq!(classify_lattice(&lattice), LatticeType::Other);
        let points = get_high_symmetry_points(&lattice);
        assert_eq!(points.len(), 1);
        assert_eq!(points[0].0, "Gamma");
        assert!(points[0].1.norm() < 1e-10, "Gamma should be at origin");
    }

    #[test]
    fn high_symmetry_kpoint_labels() {
        let a_bcc = 4.0;
        // (lattice, expected_labels)
        let cases: Vec<(Lattice, &[&str])> = vec![
            (Lattice::cubic(5.0), &["Gamma", "X", "M", "R"]),
            (
                Lattice::from_array([
                    [-a_bcc / 2.0, a_bcc / 2.0, a_bcc / 2.0],
                    [a_bcc / 2.0, -a_bcc / 2.0, a_bcc / 2.0],
                    [a_bcc / 2.0, a_bcc / 2.0, -a_bcc / 2.0],
                ]),
                &["Gamma", "H", "N", "P"],
            ),
            (
                Lattice::hexagonal(3.0, 5.0),
                &["Gamma", "A", "H", "K", "L", "M"],
            ),
            (
                Lattice::from_array([[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 6.0]]),
                &["Gamma", "A", "M", "R", "X", "Z"],
            ),
            (
                Lattice::from_array([[3.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 5.0]]),
                &["Gamma", "R", "S", "T", "U", "X", "Y", "Z"],
            ),
        ];
        for (lattice, expected_labels) in &cases {
            let points = get_high_symmetry_points(lattice);
            assert_eq!(
                points.len(),
                expected_labels.len(),
                "wrong count for {expected_labels:?}"
            );
            let labels: Vec<&str> = points.iter().map(|(lbl, _)| lbl.as_str()).collect();
            for &expected in *expected_labels {
                assert!(labels.contains(&expected), "missing k-point {expected}");
            }
        }
    }

    #[test]
    fn bragg_planes_prune_dominated() {
        let recip = Lattice::cubic(4.0).reciprocal();
        let total_raw = 5_usize.pow(3) - 1; // 124 raw planes from [-2,2]³
        let planes = generate_bragg_planes(recip.matrix());
        // Pruning removes dominated parallel planes (e.g. (2,0,0) dominated by (1,0,0))
        assert!(planes.len() >= 6, "Need at least 6 nearest planes");
        assert!(
            planes.len() < total_raw,
            "Pruning should reduce from {total_raw}"
        );
        // Planes should be sorted by distance
        for pair in planes.windows(2) {
            assert!(pair[0].distance <= pair[1].distance + TOL);
        }
    }
}
