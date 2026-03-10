use super::Lattice;
use nalgebra::{Matrix3, Vector3};
use std::collections::{HashMap, HashSet};
use std::f64::consts::PI;

impl Lattice {
    // -------------------------------------------------------------------------
    // Lattice mapping
    // -------------------------------------------------------------------------

    /// Find all lattice vector mappings to a target lattice within tolerance.
    ///
    /// This finds integer transformation matrices that map this lattice to the target.
    /// In highly mismatched cells this unconstrained search can be expensive since it
    /// explores broad candidate sets for all three lattice vectors.
    ///
    /// For matcher/supercell workflows where a specific `|det(scale_matrix)|` is known,
    /// prefer `find_all_mappings_with_determinant` to reduce combinatorial cost while
    /// preserving equivalent determinant-filtered results.
    ///
    /// # Arguments
    ///
    /// * `target` - The target lattice to map to
    /// * `len_tol` - Fractional length tolerance
    /// * `ang_tol` - Angle tolerance in degrees
    /// * `skip_rotation_matrix` - If true, don't compute rotation matrices
    ///
    /// # Returns
    ///
    /// A vector of (aligned_lattice, rotation_matrix, scale_matrix) tuples.
    pub fn find_all_mappings(
        &self,
        target: &Lattice,
        len_tol: f64,
        ang_tol: f64,
        skip_rotation_matrix: bool,
    ) -> Vec<(Lattice, Option<Matrix3<f64>>, Matrix3<i32>)> {
        self.find_all_mappings_internal(target, len_tol, ang_tol, skip_rotation_matrix, None)
    }

    /// Find all lattice mappings while constraining the absolute determinant.
    ///
    /// This is useful for supercell-aware matching where only mappings with a
    /// specific `|det(scale_matrix)|` are relevant.
    ///
    /// Returns an empty vector when `target_abs_determinant == 0`.
    pub fn find_all_mappings_with_determinant(
        &self,
        target: &Lattice,
        len_tol: f64,
        ang_tol: f64,
        skip_rotation_matrix: bool,
        target_abs_determinant: usize,
    ) -> Vec<(Lattice, Option<Matrix3<f64>>, Matrix3<i32>)> {
        if target_abs_determinant == 0 {
            return vec![];
        }
        self.find_all_mappings_internal(
            target,
            len_tol,
            ang_tol,
            skip_rotation_matrix,
            Some(target_abs_determinant),
        )
    }

    fn find_all_mappings_internal(
        &self,
        target: &Lattice,
        len_tol: f64,
        ang_tol: f64,
        skip_rotation_matrix: bool,
        target_abs_determinant: Option<usize>,
    ) -> Vec<(Lattice, Option<Matrix3<f64>>, Matrix3<i32>)> {
        let target_lengths = target.lengths();
        let target_angles = target.angles();
        if let Some(det_abs) = target_abs_determinant {
            let source_volume = self.volume().abs();
            let target_volume = target.volume().abs();
            if source_volume <= f64::EPSILON || target_volume <= f64::EPSILON {
                return vec![];
            }
            let mapped_volume = source_volume * det_abs as f64;
            let (volume_ratio_min, volume_ratio_max) = Self::compatible_volume_ratio_bounds(
                len_tol,
                ang_tol,
                [target_angles[0], target_angles[1], target_angles[2]],
            );
            if mapped_volume < target_volume * volume_ratio_min
                || mapped_volume > target_volume * volume_ratio_max
            {
                return vec![];
            }
        }
        let max_length = target_lengths.max() * (1.0 + len_tol);

        // Search range for lattice vector candidates
        // Need extra margin for oblique cells where Cartesian lengths differ from lattice params
        let search_range = (max_length / self.lengths().min()).ceil() as i32 + 2;

        // Collect candidate vectors for each target length
        let mut cands_a = Vec::new();
        let mut cands_b = Vec::new();
        let mut cands_c = Vec::new();

        for idx in -search_range..=search_range {
            for jdx in -search_range..=search_range {
                for kdx in -search_range..=search_range {
                    if idx == 0 && jdx == 0 && kdx == 0 {
                        continue;
                    }
                    let frac = Vector3::new(idx as f64, jdx as f64, kdx as f64);
                    let cart = self.matrix.transpose() * frac;
                    let length = cart.norm();

                    // Check if this vector matches any target length
                    // Use symmetric tolerance: ratio should be in (1/(1+len_tol), 1+len_tol)
                    // Note: pymatgen uses strict inequalities (< and >), not <=/>=
                    // This matches pymatgen's behavior where ±len_tol% means ratio in (1/1.2, 1.2)
                    let ratio_a = length / target_lengths[0];
                    let ratio_b = length / target_lengths[1];
                    let ratio_c = length / target_lengths[2];

                    let lo = 1.0 / (1.0 + len_tol);
                    let hi = 1.0 + len_tol;

                    if ratio_a > lo && ratio_a < hi {
                        cands_a.push((Vector3::new(idx, jdx, kdx), cart, length));
                    }
                    if ratio_b > lo && ratio_b < hi {
                        cands_b.push((Vector3::new(idx, jdx, kdx), cart, length));
                    }
                    if ratio_c > lo && ratio_c < hi {
                        cands_c.push((Vector3::new(idx, jdx, kdx), cart, length));
                    }
                }
            }
        }

        let mut results = Vec::new();

        // For determinant-constrained searches, index C-candidates by integer vector.
        let cands_c_by_frac = target_abs_determinant.map(|_| {
            let mut candidate_map: HashMap<(i32, i32, i32), (Vector3<f64>, f64)> = HashMap::new();
            for (frac_vector, cart_vector, vector_length) in &cands_c {
                candidate_map.insert(
                    (frac_vector[0], frac_vector[1], frac_vector[2]),
                    (*cart_vector, *vector_length),
                );
            }
            candidate_map
        });

        // Check all combinations for angle matching
        for (fa, ca, la) in &cands_a {
            for (fb, cb, lb) in &cands_b {
                // Check gamma angle (between a and b)
                let cos_gamma = ca.dot(cb) / (la * lb);
                let gamma = cos_gamma.clamp(-1.0, 1.0).acos() * 180.0 / PI;
                if (gamma - target_angles[2]).abs() > ang_tol {
                    continue;
                }

                let determinant_normal = Self::cross_i32(fa, fb);
                let fc_candidates: Vec<(Vector3<i32>, Vector3<f64>, f64)> =
                    if let Some(target_abs_det) = target_abs_determinant {
                        let Some(cands_c_map) = cands_c_by_frac.as_ref() else {
                            continue;
                        };
                        Self::solve_fc_vectors_for_determinant(
                            &determinant_normal,
                            target_abs_det as i32,
                            search_range,
                        )
                        .into_iter()
                        .filter_map(|frac_vector| {
                            cands_c_map
                                .get(&(frac_vector[0], frac_vector[1], frac_vector[2]))
                                .map(|(cart_vector, vector_length)| {
                                    (frac_vector, *cart_vector, *vector_length)
                                })
                        })
                        .collect()
                    } else {
                        cands_c
                            .iter()
                            .map(|(frac_vector, cart_vector, vector_length)| {
                                (*frac_vector, *cart_vector, *vector_length)
                            })
                            .collect()
                    };

                for (fc, cc, lc) in fc_candidates {
                    // Check alpha angle (between b and c)
                    let cos_alpha = cb.dot(&cc) / (lb * lc);
                    let alpha = cos_alpha.clamp(-1.0, 1.0).acos() * 180.0 / PI;
                    if (alpha - target_angles[0]).abs() > ang_tol {
                        continue;
                    }

                    // Check beta angle (between a and c)
                    let cos_beta = ca.dot(&cc) / (la * lc);
                    let beta = cos_beta.clamp(-1.0, 1.0).acos() * 180.0 / PI;
                    if (beta - target_angles[1]).abs() > ang_tol {
                        continue;
                    }

                    // Build scale matrix (integer)
                    let scale_m = Matrix3::new(
                        fa[0], fa[1], fa[2], fb[0], fb[1], fb[2], fc[0], fc[1], fc[2],
                    );

                    // Check determinant is non-zero
                    let det = scale_m.map(|x| x as f64).determinant();
                    if det.abs() < 1e-8 {
                        continue;
                    }

                    // Build aligned matrix
                    let aligned_m =
                        Matrix3::from_rows(&[ca.transpose(), cb.transpose(), cc.transpose()]);
                    let aligned_lattice = Lattice::new(aligned_m);

                    // Compute rotation matrix if requested
                    let rotation_m = if skip_rotation_matrix {
                        None
                    } else {
                        // rotation_m * aligned_m = target.matrix
                        aligned_m
                            .transpose()
                            .try_inverse()
                            .map(|inv| target.matrix.transpose() * inv)
                            .map(|r| r.transpose())
                    };

                    results.push((aligned_lattice, rotation_m, scale_m));
                }
            }
        }

        results
    }

    fn cross_i32(vector_a: &Vector3<i32>, vector_b: &Vector3<i32>) -> Vector3<i32> {
        Vector3::new(
            vector_a[1] * vector_b[2] - vector_a[2] * vector_b[1],
            vector_a[2] * vector_b[0] - vector_a[0] * vector_b[2],
            vector_a[0] * vector_b[1] - vector_a[1] * vector_b[0],
        )
    }

    fn solve_fc_vectors_for_determinant(
        determinant_normal: &Vector3<i32>,
        target_abs_det: i32,
        search_range: i32,
    ) -> Vec<Vector3<i32>> {
        if target_abs_det <= 0 {
            return vec![];
        }

        let normal_x = determinant_normal[0];
        let normal_y = determinant_normal[1];
        let normal_z = determinant_normal[2];
        if normal_x == 0 && normal_y == 0 && normal_z == 0 {
            return vec![];
        }

        let solve_axis = [
            (normal_x.abs(), 0usize),
            (normal_y.abs(), 1usize),
            (normal_z.abs(), 2usize),
        ]
        .into_iter()
        .max_by_key(|(abs_component, _)| *abs_component)
        .map(|(_, axis_idx)| axis_idx)
        .unwrap_or(2usize);

        let mut solved_vectors = HashSet::new();
        for signed_det in [target_abs_det, -target_abs_det] {
            for first_coord in -search_range..=search_range {
                for second_coord in -search_range..=search_range {
                    let maybe_solution = match solve_axis {
                        0 => {
                            if normal_x == 0 {
                                None
                            } else {
                                let remainder =
                                    signed_det - normal_y * first_coord - normal_z * second_coord;
                                if remainder % normal_x == 0 {
                                    let solved_coord = remainder / normal_x;
                                    Some(Vector3::new(solved_coord, first_coord, second_coord))
                                } else {
                                    None
                                }
                            }
                        }
                        1 => {
                            if normal_y == 0 {
                                None
                            } else {
                                let remainder =
                                    signed_det - normal_x * first_coord - normal_z * second_coord;
                                if remainder % normal_y == 0 {
                                    let solved_coord = remainder / normal_y;
                                    Some(Vector3::new(first_coord, solved_coord, second_coord))
                                } else {
                                    None
                                }
                            }
                        }
                        _ => {
                            if normal_z == 0 {
                                None
                            } else {
                                let remainder =
                                    signed_det - normal_x * first_coord - normal_y * second_coord;
                                if remainder % normal_z == 0 {
                                    let solved_coord = remainder / normal_z;
                                    Some(Vector3::new(first_coord, second_coord, solved_coord))
                                } else {
                                    None
                                }
                            }
                        }
                    };
                    if let Some(solution_vector) = maybe_solution
                        && solution_vector[0].abs() <= search_range
                        && solution_vector[1].abs() <= search_range
                        && solution_vector[2].abs() <= search_range
                    {
                        solved_vectors.insert(solution_vector);
                    }
                }
            }
        }

        let mut sorted_vectors: Vec<_> = solved_vectors.into_iter().collect();
        sorted_vectors.sort_unstable_by_key(|vector| (vector[0], vector[1], vector[2]));
        sorted_vectors
    }

    fn compatible_volume_ratio_bounds(
        len_tol: f64,
        ang_tol: f64,
        target_angles: [f64; 3],
    ) -> (f64, f64) {
        let lo = 1.0 / (1.0 + len_tol);
        let hi = 1.0 + len_tol;
        let length_ratio_min = lo.powi(3);
        let length_ratio_max = hi.powi(3);

        let target_factor =
            Self::angle_volume_factor(target_angles[0], target_angles[1], target_angles[2]);
        if target_factor <= f64::EPSILON {
            return (0.0, f64::INFINITY);
        }

        let alpha_candidates = [
            (target_angles[0] - ang_tol).clamp(1e-3, 179.999),
            (target_angles[0] + ang_tol).clamp(1e-3, 179.999),
        ];
        let beta_candidates = [
            (target_angles[1] - ang_tol).clamp(1e-3, 179.999),
            (target_angles[1] + ang_tol).clamp(1e-3, 179.999),
        ];
        let gamma_candidates = [
            (target_angles[2] - ang_tol).clamp(1e-3, 179.999),
            (target_angles[2] + ang_tol).clamp(1e-3, 179.999),
        ];

        let mut angle_ratio_min = f64::INFINITY;
        let mut angle_ratio_max = 0.0_f64;
        for alpha_deg in alpha_candidates {
            for beta_deg in beta_candidates {
                for gamma_deg in gamma_candidates {
                    let factor = Self::angle_volume_factor(alpha_deg, beta_deg, gamma_deg);
                    let ratio = factor / target_factor;
                    angle_ratio_min = angle_ratio_min.min(ratio);
                    angle_ratio_max = angle_ratio_max.max(ratio);
                }
            }
        }

        (
            (length_ratio_min * angle_ratio_min).max(0.0),
            length_ratio_max * angle_ratio_max,
        )
    }

    fn angle_volume_factor(alpha_deg: f64, beta_deg: f64, gamma_deg: f64) -> f64 {
        let alpha_rad = alpha_deg.to_radians();
        let beta_rad = beta_deg.to_radians();
        let gamma_rad = gamma_deg.to_radians();
        let cos_alpha = alpha_rad.cos();
        let cos_beta = beta_rad.cos();
        let cos_gamma = gamma_rad.cos();
        let squared_factor = 1.0 + 2.0 * cos_alpha * cos_beta * cos_gamma
            - cos_alpha * cos_alpha
            - cos_beta * cos_beta
            - cos_gamma * cos_gamma;
        squared_factor.max(0.0).sqrt()
    }

    /// Find the first mapping between this lattice and another.
    ///
    /// # Returns
    ///
    /// `Some((aligned_lattice, rotation_matrix, scale_matrix))` if found, `None` otherwise.
    ///
    /// When multiple mappings exist, selects the one closest to identity (smallest Frobenius
    /// norm difference from identity matrix) for deterministic behavior.
    pub fn find_mapping(
        &self,
        target: &Lattice,
        len_tol: f64,
        ang_tol: f64,
        skip_rotation_matrix: bool,
    ) -> Option<(Lattice, Option<Matrix3<f64>>, Matrix3<i32>)> {
        let mut mappings = self.find_all_mappings(target, len_tol, ang_tol, skip_rotation_matrix);

        if mappings.is_empty() {
            return None;
        }

        // Sort by distance from identity scale matrix for deterministic selection
        let identity = Matrix3::<i32>::identity();
        mappings.sort_by(|a, b| {
            let dist_a: i32 = (a.2 - identity).iter().map(|x| x.abs()).sum();
            let dist_b: i32 = (b.2 - identity).iter().map(|x| x.abs()).sum();
            dist_a.cmp(&dist_b)
        });

        mappings.into_iter().next()
    }
}
