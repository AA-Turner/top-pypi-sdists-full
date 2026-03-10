use super::StructureMatcher;
use crate::lattice::Lattice;
use crate::pbc::{is_coord_subset_pbc, pbc_shortest_vectors, wrap_frac_coords_pbc};
use crate::structure::Structure;
use nalgebra::{Matrix3, Vector3};
use pathfinding::kuhn_munkres::kuhn_munkres_min;
use pathfinding::matrix::Matrix as PathMatrix;
use std::f64::consts::PI;

impl StructureMatcher {
    pub(super) fn cart_dists(
        &self,
        s1_fc: &[Vector3<f64>],
        s2_fc: &[Vector3<f64>],
        avg_lattice: &Lattice,
        mask: &[Vec<bool>],
        normalization: f64,
    ) -> Option<(Vec<f64>, Vector3<f64>, Vec<usize>)> {
        let n1 = s1_fc.len();
        let n2 = s2_fc.len();

        if n2 > n1 || n2 == 0 {
            return None;
        }

        // Get shortest vectors
        let (vecs, d2, _) = pbc_shortest_vectors(avg_lattice, s2_fc, s1_fc, Some(mask), None);

        // Solve linear assignment problem
        // Convert to integer costs (multiply by large factor for precision)
        let scale = 1e10;
        let mut cost_matrix = PathMatrix::new(n2, n1, i64::MAX / 2);

        for idx in 0..n2 {
            for jdx in 0..n1 {
                if !mask[idx][jdx] {
                    // Clamp to avoid overflow (masked cells already have i64::MAX / 2)
                    cost_matrix[(idx, jdx)] =
                        (d2[idx][jdx] * scale).min(i64::MAX as f64 / 2.0) as i64;
                }
            }
        }

        let (_total_cost, assignment) = kuhn_munkres_min(&cost_matrix);
        let mapping: Vec<usize> = assignment.to_vec();

        // Compute translation and distances
        let mut short_vecs = Vec::with_capacity(n2);
        for (idx, &jdx) in mapping.iter().enumerate() {
            if jdx < vecs[idx].len() {
                short_vecs.push(vecs[idx][jdx]);
            } else {
                return None;
            }
        }

        // Translation is mean of short vectors (guard against empty vector)
        if short_vecs.is_empty() {
            return None;
        }
        let translation: Vector3<f64> =
            short_vecs.iter().fold(Vector3::zeros(), |acc, v| acc + v) / short_vecs.len() as f64;

        // Distances after translation adjustment
        let distances: Vec<f64> = short_vecs
            .iter()
            .map(|v| (v - translation).norm() * normalization)
            .collect();

        let f_translation = avg_lattice.get_fractional_coords(&[translation])[0];

        Some((distances, f_translation, mapping))
    }

    /// Check if two fractional coordinate sets match within tolerance.
    pub(super) fn cmp_fstruct(
        s1_fc: &[Vector3<f64>],
        s2_fc: &[Vector3<f64>],
        frac_tol: [f64; 3],
        mask: &[Vec<bool>],
        pbc: [bool; 3],
    ) -> bool {
        is_coord_subset_pbc(s2_fc, s1_fc, frac_tol, mask, pbc)
    }

    /// Strict matching - s1 should contain all sites in s2.
    pub(super) fn strict_match(
        &self,
        struct1: &Structure,
        struct2: &Structure,
        supercell_factor: usize,
        break_on_match: bool,
        use_rms: bool,
    ) -> Option<(f64, Vec<f64>, Vec<usize>)> {
        if struct1.lattice.pbc != struct2.lattice.pbc {
            return None;
        }

        let mask = self.get_mask(struct1, struct2);

        if mask.is_empty() {
            return None;
        }

        let (struct1_translation_indices, struct2_translation_idx) =
            self.get_translation_indices(&mask);

        // Check dimensions
        if struct2.num_sites() > struct1.num_sites() {
            return None;
        }

        // Check that a valid matching is possible
        for row in &mask {
            if row.iter().all(|&x| x) {
                return None;
            }
        }

        let mut best_match: Option<(f64, Vec<f64>, Vec<usize>)> = None;

        // For non-periodic matching, avoid enumerating periodic lattice mappings.
        let lattices = if struct1.lattice.pbc.iter().any(|&is_periodic| is_periodic) {
            self.sorted_lattice_candidates(&struct2.lattice, struct1, supercell_factor)
        } else {
            vec![(struct2.lattice.clone(), Matrix3::identity())]
        };

        if lattices.is_empty() {
            return None;
        }

        // Loop over all lattice mappings
        for (latt, _scale_m) in &lattices {
            let avg_lattice = Self::average_lattice(latt, &struct2.lattice);

            // Compute fractional coordinate tolerance
            let normalization = (struct1.num_sites() as f64 / avg_lattice.volume()).powf(1.0 / 3.0);
            let recip_lengths = avg_lattice.reciprocal().lengths();
            let scale = self.site_pos_tol / (PI * normalization);
            let frac_coord_tol = [
                recip_lengths[0] * scale,
                recip_lengths[1] * scale,
                recip_lengths[2] * scale,
            ];

            // Get fractional coords in the aligned lattice
            let s1_cart = struct1.cart_coords();
            let mut s1_fc = latt.get_fractional_coords(&s1_cart);
            // Wrap to [0, 1)
            for coord in &mut s1_fc {
                *coord = wrap_frac_coords_pbc(coord, struct1.lattice.pbc);
            }

            let s2_fc = &struct2.frac_coords;

            // Try different translations
            for &s1i in &struct1_translation_indices {
                if s1i >= s1_fc.len() || struct2_translation_idx >= s2_fc.len() {
                    continue;
                }

                let mut translation = s1_fc[s1i] - s2_fc[struct2_translation_idx];
                for axis in 0..3 {
                    if !struct1.lattice.pbc[axis] {
                        translation[axis] = 0.0;
                    }
                }
                let translated_s2_fc: Vec<Vector3<f64>> =
                    s2_fc.iter().map(|frac| frac + translation).collect();

                // Check if fractional coords match
                if Self::cmp_fstruct(
                    &s1_fc,
                    &translated_s2_fc,
                    frac_coord_tol,
                    &mask,
                    struct1.lattice.pbc,
                ) {
                    // Compute distances
                    if let Some((distances, _adjusted_translation, mapping)) = self.cart_dists(
                        &s1_fc,
                        &translated_s2_fc,
                        &avg_lattice,
                        &mask,
                        normalization,
                    ) {
                        let val = if use_rms {
                            let sum_sq: f64 = distances.iter().map(|d| d * d).sum();
                            (sum_sq / distances.len() as f64).sqrt()
                        } else {
                            distances.iter().copied().fold(0.0, f64::max)
                        };

                        if best_match.as_ref().is_none_or(|m| val < m.0) {
                            best_match = Some((val, distances.clone(), mapping));

                            if (break_on_match || val < 1e-5) && val < self.site_pos_tol {
                                return best_match;
                            }
                        }
                    }
                }
            }
        }

        best_match.filter(|m| m.0 < self.site_pos_tol)
    }

    /// Internal match function.
    pub(super) fn match_internal(
        &self,
        struct1: &Structure,
        struct2: &Structure,
        supercell_factor: usize,
        s1_supercell: bool,
        break_on_match: bool,
        use_rms: bool,
    ) -> Option<(f64, Vec<f64>, Vec<usize>)> {
        let ratio = if s1_supercell {
            supercell_factor as f64
        } else {
            1.0 / supercell_factor as f64
        };

        if (struct1.num_sites() as f64 * ratio) >= struct2.num_sites() as f64 {
            self.strict_match(struct1, struct2, supercell_factor, break_on_match, use_rms)
        } else {
            self.strict_match(struct2, struct1, supercell_factor, break_on_match, use_rms)
        }
    }

    pub(super) fn explicit_supercell_matrices(supercell_factor: usize) -> Vec<[[i32; 3]; 3]> {
        let mut scaling_matrices = Vec::new();
        for factor_a in 1..=supercell_factor {
            if !supercell_factor.is_multiple_of(factor_a) {
                continue;
            }
            let remaining_after_a = supercell_factor / factor_a;
            for factor_d in 1..=remaining_after_a {
                if !remaining_after_a.is_multiple_of(factor_d) {
                    continue;
                }
                let factor_f = remaining_after_a / factor_d;
                let Some(factor_a_i32) = i32::try_from(factor_a).ok() else {
                    continue;
                };
                let Some(factor_d_i32) = i32::try_from(factor_d).ok() else {
                    continue;
                };
                let Some(factor_f_i32) = i32::try_from(factor_f).ok() else {
                    continue;
                };

                // Enumerate upper-triangular Hermite-like matrices with determinant n.
                for offset_b in 0..factor_d {
                    let Some(offset_b_i32) = i32::try_from(offset_b).ok() else {
                        continue;
                    };
                    for offset_c in 0..factor_f {
                        let Some(offset_c_i32) = i32::try_from(offset_c).ok() else {
                            continue;
                        };
                        for offset_e in 0..factor_f {
                            let Some(offset_e_i32) = i32::try_from(offset_e).ok() else {
                                continue;
                            };
                            scaling_matrices.push([
                                [factor_a_i32, offset_b_i32, offset_c_i32],
                                [0, factor_d_i32, offset_e_i32],
                                [0, 0, factor_f_i32],
                            ]);
                        }
                    }
                }
            }
        }
        scaling_matrices
    }

    pub(super) fn match_with_explicit_supercell(
        &self,
        struct1: &Structure,
        struct2: &Structure,
    ) -> bool {
        let (smaller_structure, larger_structure) = if struct1.num_sites() <= struct2.num_sites() {
            (struct1, struct2)
        } else {
            (struct2, struct1)
        };

        if smaller_structure.num_sites() == 0 || larger_structure.num_sites() == 0 {
            return false;
        }
        if larger_structure.num_sites() % smaller_structure.num_sites() != 0 {
            return false;
        }

        let exact_supercell_factor = larger_structure.num_sites() / smaller_structure.num_sites();
        if exact_supercell_factor <= 1 {
            return false;
        }

        for scaling_matrix in Self::explicit_supercell_matrices(exact_supercell_factor) {
            let Ok(expanded_structure) = smaller_structure.make_supercell(scaling_matrix) else {
                continue;
            };
            if self
                .match_internal(&expanded_structure, larger_structure, 1, true, true, false)
                .is_some_and(|(match_value, _, _)| match_value <= self.site_pos_tol)
            {
                return true;
            }
        }

        false
    }
}
