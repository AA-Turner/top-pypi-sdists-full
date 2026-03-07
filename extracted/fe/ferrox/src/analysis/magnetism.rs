//! Collinear magnetic structure analysis.
//!
//! Provides classification of magnetic ordering (FM, AFM, FiM, NM) and
//! extraction of magnetic properties from structures with `magmom` site properties.

use std::collections::HashSet;

use crate::structure::Structure;

/// Magnetic ordering classification.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MagneticOrdering {
    /// Ferromagnetic: all magnetic moments aligned in same direction.
    FM,
    /// Antiferromagnetic: magnetic moments cancel (net moment ~0).
    AFM,
    /// Ferrimagnetic: partial cancellation (opposing moments of different magnitude).
    FiM,
    /// Non-magnetic: no significant magnetic moments.
    NM,
    /// Unknown ordering (e.g. non-collinear or ambiguous).
    Unknown,
}

impl MagneticOrdering {
    /// String label for this ordering.
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::FM => "FM",
            Self::AFM => "AFM",
            Self::FiM => "FiM",
            Self::NM => "NM",
            Self::Unknown => "Unknown",
        }
    }
}

/// Results of a collinear magnetic structure analysis.
#[derive(Debug, Clone, Default)]
pub struct MagneticAnalysis {
    /// Whether the structure has magmom site properties at all.
    pub has_magmoms: bool,
    /// Whether the structure is classified as magnetic (any |magmom| > threshold).
    pub is_magnetic: Option<bool>,
    /// Classified magnetic ordering.
    pub ordering: Option<MagneticOrdering>,
    /// Per-site magnetic moments (collinear, scalar).
    pub magmoms: Option<Vec<f64>>,
    /// Sum of all site magnetic moments.
    pub total_magmom: Option<f64>,
    /// Maximum |magmom| across all sites.
    pub max_abs_magmom: Option<f64>,
    /// Number of sites with |magmom| > threshold.
    pub num_magnetic_sites: Option<usize>,
    /// Number of symmetry-unique magnetic sites (requires orbit info).
    pub num_unique_magnetic_sites: Option<usize>,
    /// Element symbols of magnetic species.
    pub types_of_magnetic_species: Option<Vec<String>>,
    /// Total magnetization in μB (absolute value of sum).
    pub total_magnetization: Option<f64>,
    /// Total magnetization normalized by volume (μB/Å³).
    pub total_magnetization_normalized_vol: Option<f64>,
    /// Total magnetization normalized by formula units (μB/f.u.).
    pub total_magnetization_normalized_formula_units: Option<f64>,
}

/// Result of extracting magmoms: scalar values plus whether non-collinear vectors were found.
struct ExtractedMagmoms {
    values: Vec<f64>,
    has_non_collinear: bool,
}

/// Extract collinear (scalar) magmoms from a structure's site properties.
///
/// Returns `None` if no magmom properties are present on any site.
/// For non-collinear 3-vector magmoms, projects to scalar magnitude and sets
/// `has_non_collinear = true` so the caller can classify as `Unknown`.
fn extract_magmoms(structure: &Structure) -> Option<ExtractedMagmoms> {
    let mut magmoms = Vec::with_capacity(structure.num_sites());
    let mut has_any = false;
    let mut has_non_collinear = false;

    for site_occ in &structure.site_occupancies {
        match site_occ.properties.get("magmom") {
            Some(serde_json::Value::Number(num)) => {
                magmoms.push(num.as_f64().unwrap_or(0.0));
                has_any = true;
            }
            Some(serde_json::Value::Array(arr)) if arr.len() == 3 => {
                // Treat null/non-numeric components as 0.0 rather than skipping them
                let mag: f64 = arr
                    .iter()
                    .map(|val| val.as_f64().unwrap_or(0.0))
                    .map(|comp| comp * comp)
                    .sum::<f64>()
                    .sqrt();
                magmoms.push(mag);
                has_any = true;
                has_non_collinear = true;
            }
            Some(serde_json::Value::Array(arr)) => {
                tracing::warn!(
                    "ignoring magmom array of length {} (expected scalar or 3-vector)",
                    arr.len()
                );
                magmoms.push(0.0);
            }
            _ => {
                magmoms.push(0.0);
            }
        }
    }

    has_any.then_some(ExtractedMagmoms {
        values: magmoms,
        has_non_collinear,
    })
}

/// Classify magnetic ordering from a set of collinear magmoms (single pass).
fn classify_ordering(magmoms: &[f64], threshold: f64) -> MagneticOrdering {
    let mut has_positive = false;
    let mut has_negative = false;
    let mut magnetic_sum = 0.0_f64;
    let mut any_magnetic = false;

    for &mag in magmoms {
        if mag.abs() > threshold {
            any_magnetic = true;
            magnetic_sum += mag;
            if mag > threshold {
                has_positive = true;
            }
            if mag < -threshold {
                has_negative = true;
            }
        }
    }

    if !any_magnetic {
        MagneticOrdering::NM
    } else if has_positive != has_negative {
        MagneticOrdering::FM
    } else if magnetic_sum.abs() < threshold {
        MagneticOrdering::AFM
    } else {
        MagneticOrdering::FiM
    }
}

impl Structure {
    /// Perform collinear magnetic structure analysis.
    ///
    /// Extracts magmom from site properties and classifies magnetic ordering.
    /// If orbits are provided (from symmetry analysis), also computes
    /// `num_unique_magnetic_sites`.
    ///
    /// # Arguments
    ///
    /// * `threshold` - Minimum |magmom| to consider a site magnetic (typically 0.1 μB)
    /// * `orbits` - Optional orbit indices from symmetry analysis for unique-site counting
    pub fn magnetic_analysis(&self, threshold: f64, orbits: Option<&[usize]>) -> MagneticAnalysis {
        let Some(extracted) = extract_magmoms(self) else {
            return MagneticAnalysis::default();
        };
        let magmoms = extracted.values;
        // Non-collinear magmoms lose sign info when projected to scalar magnitude,
        // so FM/AFM/FiM classification is unreliable — use Unknown instead.
        let ordering = if extracted.has_non_collinear {
            MagneticOrdering::Unknown
        } else {
            classify_ordering(&magmoms, threshold)
        };
        let is_magnetic = magmoms.iter().any(|mag| mag.abs() > threshold);
        let max_abs_magmom = magmoms.iter().map(|mag| mag.abs()).fold(0.0_f64, f64::max);
        // For non-collinear moments, magnitudes are unsigned so scalar sum is
        // physically meaningless (opposing vectors won't cancel). Set to None.
        let total_magmom = (!extracted.has_non_collinear).then(|| magmoms.iter().sum::<f64>());

        // Indices of sites with |magmom| exceeding the threshold
        let magnetic_site_indices: Vec<usize> = magmoms
            .iter()
            .enumerate()
            .filter(|(_, mag)| mag.abs() > threshold)
            .map(|(idx, _)| idx)
            .collect();

        // Count symmetry-unique magnetic sites via orbit assignments
        let num_unique_magnetic_sites = orbits.map(|orbit_ids| {
            magnetic_site_indices
                .iter()
                .filter_map(|&idx| orbit_ids.get(idx).copied())
                .collect::<HashSet<usize>>()
                .len()
        });

        // Collect distinct element symbols of magnetic species
        let mut magnetic_elements: Vec<String> = magnetic_site_indices
            .iter()
            .map(|&idx| {
                self.site_occupancies[idx]
                    .dominant_species()
                    .element
                    .symbol()
                    .to_string()
            })
            .collect::<HashSet<_>>()
            .into_iter()
            .collect();
        magnetic_elements.sort();

        // Magnetization and normalizations (None when non-collinear)
        let total_magnetization = total_magmom.map(|tm| tm.abs());
        let vol = self.volume();
        let total_magnetization_normalized_vol =
            total_magnetization.and_then(|tm| (vol > 1e-12).then(|| tm / vol));
        let reduced_factor = self.composition().get_reduced_factor();
        let total_magnetization_normalized_formula_units =
            total_magnetization.and_then(|tm| (reduced_factor > 0.5).then(|| tm / reduced_factor));

        MagneticAnalysis {
            has_magmoms: true,
            is_magnetic: Some(is_magnetic),
            ordering: Some(ordering),
            total_magmom,
            max_abs_magmom: Some(max_abs_magmom),
            num_magnetic_sites: Some(magnetic_site_indices.len()),
            num_unique_magnetic_sites,
            types_of_magnetic_species: Some(magnetic_elements),
            total_magnetization,
            total_magnetization_normalized_vol,
            total_magnetization_normalized_formula_units,
            magmoms: Some(magmoms),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::element::Element;
    use crate::lattice::Lattice;
    use crate::species::{SiteOccupancy, Species};
    use nalgebra::Vector3;
    use std::collections::HashMap;

    /// Build a structure with per-site magmom properties.
    fn make_magnetic_structure(elements: &[Element], magmoms: &[f64]) -> Structure {
        let lattice = Lattice::cubic(4.0);
        let num_sites = elements.len();
        let site_occupancies: Vec<SiteOccupancy> = elements
            .iter()
            .zip(magmoms.iter())
            .map(|(&elem, &mag)| {
                let mut props = HashMap::new();
                props.insert(
                    "magmom".to_string(),
                    serde_json::Value::Number(serde_json::Number::from_f64(mag).unwrap()),
                );
                SiteOccupancy::with_properties(vec![(Species::neutral(elem), 1.0)], props)
            })
            .collect();

        let frac_coords: Vec<Vector3<f64>> = (0..num_sites)
            .map(|idx| Vector3::new(idx as f64 / num_sites as f64, 0.0, 0.0))
            .collect();

        Structure::new_from_occupancies(lattice, site_occupancies, frac_coords)
    }

    #[test]
    fn test_no_magmoms() {
        // Structure without magmom properties yields has_magmoms=false
        let structure = Structure::new(
            Lattice::cubic(3.0),
            vec![Species::neutral(Element::Fe)],
            vec![Vector3::new(0.0, 0.0, 0.0)],
        );
        let analysis = structure.magnetic_analysis(0.1, None);
        assert!(!analysis.has_magmoms);
        assert!(analysis.ordering.is_none());
        assert!(analysis.magmoms.is_none());
    }

    #[test]
    fn test_collinear_ordering_classification() {
        let cases: &[(&[f64], MagneticOrdering, bool, f64)] = &[
            (&[3.0, 3.0], MagneticOrdering::FM, true, 6.0),
            (&[3.0, -3.0], MagneticOrdering::AFM, true, 0.0),
            (&[3.0, -1.0], MagneticOrdering::FiM, true, 2.0),
            (&[0.01, -0.01], MagneticOrdering::NM, false, 0.0),
        ];
        for (magmoms, expected_ord, expected_magnetic, expected_total) in cases {
            let structure = make_magnetic_structure(&[Element::Fe, Element::Fe], magmoms);
            let analysis = structure.magnetic_analysis(0.1, None);
            assert!(analysis.has_magmoms);
            assert_eq!(
                analysis.ordering,
                Some(*expected_ord),
                "magmoms={magmoms:?}"
            );
            assert_eq!(
                analysis.is_magnetic,
                Some(*expected_magnetic),
                "magmoms={magmoms:?}"
            );
            assert!(
                (analysis.total_magmom.unwrap() - expected_total).abs() < 1e-10,
                "magmoms={magmoms:?}: total_magmom={:?}",
                analysis.total_magmom,
            );
        }
    }

    #[test]
    fn test_volume_normalization() {
        // Magnetization normalized by volume should equal |total|/volume
        let structure = make_magnetic_structure(&[Element::Fe], &[5.0]);
        let analysis = structure.magnetic_analysis(0.1, None);
        let vol = structure.volume();
        let expected = 5.0 / vol;
        assert!((analysis.total_magnetization_normalized_vol.unwrap() - expected).abs() < 1e-10,);
    }

    #[test]
    fn test_ordering_as_str() {
        // as_str() round-trips to expected labels
        assert_eq!(MagneticOrdering::FM.as_str(), "FM");
        assert_eq!(MagneticOrdering::AFM.as_str(), "AFM");
        assert_eq!(MagneticOrdering::FiM.as_str(), "FiM");
        assert_eq!(MagneticOrdering::NM.as_str(), "NM");
        assert_eq!(MagneticOrdering::Unknown.as_str(), "Unknown");
    }

    #[test]
    fn test_unique_magnetic_sites_with_orbits() {
        // Orbit assignments collapse equivalent magnetic sites
        let structure = make_magnetic_structure(
            &[Element::Fe, Element::Fe, Element::Fe, Element::Fe],
            &[3.0, 3.0, -3.0, -3.0],
        );
        // Sites 0,1 share orbit 0; sites 2,3 share orbit 1
        let orbits = [0, 0, 1, 1];
        let analysis = structure.magnetic_analysis(0.1, Some(&orbits));
        assert_eq!(analysis.num_unique_magnetic_sites, Some(2));
    }

    #[test]
    fn test_magnetic_species_filtering() {
        // Only above-threshold elements appear in types_of_magnetic_species
        let cases: &[(&[Element], &[f64], usize)] = &[
            (
                &[Element::Fe, Element::O, Element::Fe],
                &[3.0, 0.0, -3.0],
                2,
            ),
            (&[Element::Fe, Element::Si], &[3.0, 0.0], 1),
        ];
        for (elems, magmoms, expected_mag_sites) in cases {
            let analysis = make_magnetic_structure(elems, magmoms).magnetic_analysis(0.1, None);
            assert_eq!(
                analysis.num_magnetic_sites,
                Some(*expected_mag_sites),
                "{elems:?}"
            );
            assert_eq!(
                analysis.types_of_magnetic_species,
                Some(vec!["Fe".to_string()]),
                "{elems:?}",
            );
        }
    }

    /// Build a structure with per-site 3-vector magmom properties.
    fn make_vector_magnetic_structure(elements: &[Element], magmoms: &[[f64; 3]]) -> Structure {
        let lattice = Lattice::cubic(4.0);
        let num_sites = elements.len();
        let site_occupancies: Vec<SiteOccupancy> = elements
            .iter()
            .zip(magmoms.iter())
            .map(|(&elem, mag)| {
                let mut props = HashMap::new();
                props.insert(
                    "magmom".to_string(),
                    serde_json::json!([mag[0], mag[1], mag[2]]),
                );
                SiteOccupancy::with_properties(vec![(Species::neutral(elem), 1.0)], props)
            })
            .collect();
        let frac_coords: Vec<Vector3<f64>> = (0..num_sites)
            .map(|idx| Vector3::new(idx as f64 / num_sites as f64, 0.0, 0.0))
            .collect();
        Structure::new_from_occupancies(lattice, site_occupancies, frac_coords)
    }

    #[test]
    fn test_non_collinear_ordering_and_magnitude() {
        // 3-vector magmoms → Unknown ordering, total_magmom = None
        let structure = make_vector_magnetic_structure(
            &[Element::Fe, Element::Fe],
            &[[0.0, 0.0, 3.0], [3.0, 4.0, 0.0]],
        );
        let analysis = structure.magnetic_analysis(0.1, None);
        assert!(analysis.has_magmoms);
        assert_eq!(analysis.ordering, Some(MagneticOrdering::Unknown));
        assert_eq!(analysis.total_magmom, None);
        assert_eq!(analysis.num_magnetic_sites, Some(2));
        // [0,0,3]→3.0, [3,4,0]→5.0
        let magmoms = analysis.magmoms.unwrap();
        assert!((magmoms[0] - 3.0).abs() < 1e-10);
        assert!((magmoms[1] - 5.0).abs() < 1e-10);
    }

    /// Build a single-Fe-site structure with the given magmom JSON value.
    fn fe_with_magmom(magmom: serde_json::Value) -> Structure {
        let mut props = HashMap::new();
        props.insert("magmom".to_string(), magmom);
        let occ = SiteOccupancy::with_properties(vec![(Species::neutral(Element::Fe), 1.0)], props);
        Structure::new_from_occupancies(
            Lattice::cubic(4.0),
            vec![occ],
            vec![Vector3::new(0.0, 0.0, 0.0)],
        )
    }

    #[test]
    fn test_vector_magmom_null_components_treated_as_zero() {
        // [null, null, 5.0] → null components become 0.0 → magnitude sqrt(0+0+25) = 5.0
        let magmoms = fe_with_magmom(serde_json::json!([null, null, 5.0]))
            .magnetic_analysis(0.1, None)
            .magmoms
            .unwrap();
        assert!((magmoms[0] - 5.0).abs() < 1e-10);
    }

    #[test]
    fn test_non_3_vector_magmom_treated_as_non_magnetic() {
        // 2-element array is invalid — not detected as magmom at all
        let analysis = fe_with_magmom(serde_json::json!([3.0, 4.0])).magnetic_analysis(0.1, None);
        assert!(
            !analysis.has_magmoms,
            "2-element array should not count as valid magmom"
        );
        assert_eq!(analysis.ordering, None);
        assert_eq!(analysis.magmoms, None);

        // Valid 3-vector IS detected
        let valid = fe_with_magmom(serde_json::json!([3.0, 4.0, 0.0])).magnetic_analysis(0.1, None);
        assert!(valid.has_magmoms);
        assert!((valid.magmoms.unwrap()[0] - 5.0).abs() < 1e-10);
    }
}
