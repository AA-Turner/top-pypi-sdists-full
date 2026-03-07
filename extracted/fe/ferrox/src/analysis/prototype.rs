//! AFLOW prototype structure labeling.
//!
//! Computes protostructure labels in the AFLOW format:
//! `{prototype_formula}_{pearson_symbol}_{spg_num}_{wyckoff_positions}:{chemical_system}`
//!
//! The prototype formula anonymizes elements with alphabetical letters (A, B, C, ...),
//! sorted by element symbol. Wyckoff positions are canonicalized by choosing the
//! relabeling with the lowest alphabetical weight.
//!
//! Ported from the Python implementation in matbench-discovery.

use std::collections::HashMap;
use std::io::Read;
use std::sync::LazyLock;

use flate2::read::GzDecoder;

use crate::composition::{Composition, gcd_i64};
use crate::element::Element;
use crate::error::{FerroxError, Result};
use crate::structure::Structure;

// === Embedded Wyckoff Data (gzipped) ===

const WYCKOFF_MULTIPLICITIES_GZ: &[u8] = include_bytes!("../data/wyckoff_multiplicities.json.gz");
const WYCKOFF_RELABELINGS_GZ: &[u8] = include_bytes!("../data/wyckoff_relabelings.json.gz");

fn decompress_json_str(gz_data: &[u8]) -> String {
    let mut decoder = GzDecoder::new(gz_data);
    let mut json = String::new();
    decoder
        .read_to_string(&mut json)
        .expect("Failed to decompress gzipped JSON");
    json
}

/// Wyckoff position multiplicities: spg_num -> {letter: multiplicity}.
static WYCKOFF_MULTIPLICITIES: LazyLock<HashMap<i32, HashMap<char, usize>>> = LazyLock::new(|| {
    let json_str = decompress_json_str(WYCKOFF_MULTIPLICITIES_GZ);
    let raw: HashMap<String, HashMap<String, usize>> =
        serde_json::from_str(&json_str).expect("Failed to parse wyckoff_multiplicities.json");
    raw.into_iter()
        .map(|(spg_str, letters)| {
            let spg: i32 = spg_str.parse().unwrap();
            let letter_map = letters
                .into_iter()
                .map(|(letter, mult)| (letter.chars().next().unwrap(), mult))
                .collect();
            (spg, letter_map)
        })
        .collect()
});

/// Wyckoff position relabelings: spg_num -> list of char-to-char mappings.
/// Each mapping represents an equivalent choice of origin for the space group.
static WYCKOFF_RELABELINGS: LazyLock<HashMap<i32, Vec<HashMap<char, char>>>> =
    LazyLock::new(|| {
        let json_str = decompress_json_str(WYCKOFF_RELABELINGS_GZ);
        let raw: HashMap<String, Vec<HashMap<String, String>>> =
            serde_json::from_str(&json_str).expect("Failed to parse wyckoff_relabelings.json");
        raw.into_iter()
            .map(|(spg_str, relabelings)| {
                let spg: i32 = spg_str.parse().unwrap();
                let mappings = relabelings
                    .into_iter()
                    .map(|rel| {
                        rel.into_iter()
                            .map(|(from, to)| {
                                (from.chars().next().unwrap(), to.chars().next().unwrap())
                            })
                            .collect()
                    })
                    .collect();
                (spg, mappings)
            })
            .collect()
    });

// === Helper Functions ===

/// Split a string into alternating groups of alphabetic and numeric characters.
///
/// E.g., "2a3b" -> ["2", "a", "3", "b"]
fn split_alpha_numeric(input: &str) -> Vec<String> {
    let mut groups: Vec<String> = Vec::new();
    let mut current = String::new();
    let mut prev_is_alpha: Option<bool> = None;

    for ch in input.chars() {
        let is_alpha = ch.is_alphabetic();
        if prev_is_alpha != Some(is_alpha) && !current.is_empty() {
            groups.push(std::mem::take(&mut current));
        }
        current.push(ch);
        prev_is_alpha = Some(is_alpha);
    }
    if !current.is_empty() {
        groups.push(current);
    }
    groups
}

/// Get anonymized prototype formula (AFLOW-style).
///
/// Elements are sorted alphabetically by symbol and mapped to A, B, C, ...
/// Amounts are reduced by GCD when all amounts are integers.
///
/// # Examples
///
/// ```
/// use ferrox::composition::Composition;
/// use ferrox::analysis::prototype::get_prototype_formula;
///
/// let comp = Composition::from_formula("Fe2O3").unwrap();
/// assert_eq!(get_prototype_formula(&comp), Some("A2B3".to_string()));
///
/// let comp = Composition::from_formula("NaCl").unwrap();
/// assert_eq!(get_prototype_formula(&comp), Some("AB".to_string()));
/// ```
pub fn get_prototype_formula(composition: &Composition) -> Option<String> {
    let elem_comp = composition.element_composition();
    if elem_comp.is_empty() {
        return None;
    }

    // Sort elements alphabetically by symbol
    let mut elem_amounts: Vec<(&str, f64)> = elem_comp
        .iter()
        .map(|(sp, &amt)| (sp.element.symbol(), amt))
        .collect();
    elem_amounts.sort_by_key(|(sym, _)| *sym);

    // GCD reduction when all amounts are integers
    let all_int = elem_amounts
        .iter()
        .all(|(_, amt)| (amt - amt.round()).abs() < 1e-8);

    let gcd = if all_int {
        elem_amounts
            .iter()
            .map(|(_, amt)| amt.round() as i64)
            .reduce(gcd_i64)
            .unwrap_or(1)
    } else {
        1
    };

    if elem_amounts.len() > 26 {
        return None;
    }

    let mut parts = Vec::new();
    for (idx, (_, amt)) in elem_amounts.iter().enumerate() {
        let letter = (b'A' + idx as u8) as char;
        let reduced = amt / gcd as f64;
        let rounded = reduced.round();
        if (reduced - 1.0).abs() < 1e-8 {
            parts.push(letter.to_string());
        } else if (reduced - rounded).abs() < 1e-8 {
            parts.push(format!("{letter}{}", rounded as i64));
        } else {
            parts.push(format!("{letter}{reduced}"));
        }
    }

    Some(parts.concat())
}

/// Canonicalize Wyckoff position labels for a given space group.
///
/// Applies all valid origin relabelings and selects the one with the lowest
/// alphabetical weight, ensuring a canonical labeling independent of arbitrary
/// origin choices.
///
/// # Arguments
///
/// * `element_wyckoffs` - Wyckoff substring with element groups separated by underscores
///   (e.g., "2a_3b" means element 1 has two 'a' sites, element 2 has three 'b' sites)
/// * `spg_num` - International space group number (1-230)
pub fn canonicalize_wyckoffs(element_wyckoffs: &str, spg_num: i32) -> Result<String> {
    let relabelings =
        WYCKOFF_RELABELINGS
            .get(&spg_num)
            .ok_or_else(|| FerroxError::InvalidStructure {
                index: 0,
                reason: format!("No Wyckoff relabelings for space group {spg_num}"),
            })?;

    relabelings
        .iter()
        .map(|trans| {
            // Apply character-level translation (only lowercase letters are remapped)
            let translated: String = element_wyckoffs
                .chars()
                .map(|ch| trans.get(&ch).copied().unwrap_or(ch))
                .collect();

            let mut score: i32 = 0;
            let mut sorted_groups: Vec<String> = Vec::new();

            for el_wyckoff in translated.split('_') {
                let groups = split_alpha_numeric(el_wyckoff);

                // Parse (count, letter) pairs from alternating numeric/alpha groups.
                // A leading letter implies count=1. E.g. "a2b" → [(1,"a"), (2,"b")].
                let mut pairs: Vec<(usize, &str)> = Vec::new();
                let mut pending_count: Option<usize> = None;
                for grp in &groups {
                    if grp.chars().all(|ch| ch.is_ascii_digit()) {
                        pending_count = Some(grp.parse().unwrap_or(1));
                    } else {
                        pairs.push((pending_count.take().unwrap_or(1), grp.as_str()));
                    }
                }
                debug_assert!(
                    pending_count.is_none(),
                    "trailing number without Wyckoff letter in '{el_wyckoff}'"
                );
                pairs.sort_by_key(|(_, letter)| *letter);

                let sorted_str: String = pairs
                    .iter()
                    .map(|(count, letter)| {
                        if *count == 1 {
                            letter.to_string()
                        } else {
                            format!("{count}{letter}")
                        }
                    })
                    .collect();
                sorted_groups.push(sorted_str);

                for (_, letter_str) in &pairs {
                    for ch in letter_str.chars() {
                        score += ch as i32 - 96;
                    }
                }
            }

            (sorted_groups.join("_"), score)
        })
        .min_by(|left, right| left.1.cmp(&right.1).then(left.0.cmp(&right.0)))
        .map(|(label, _)| label)
        .ok_or_else(|| FerroxError::InvalidStructure {
            index: 0,
            reason: format!("No Wyckoff relabelings for space group {spg_num}"),
        })
}

/// Count the number of Wyckoff positions in an AFLOW protostructure label.
///
/// # Arguments
///
/// * `protostructure_label` - Label in the format `aflow_label:chemsys`
///
/// # Examples
///
/// ```
/// use ferrox::analysis::prototype::count_wyckoff_positions;
///
/// // AB_cF8_225_a_b -> 2 Wyckoff positions (1 × a + 1 × b)
/// assert_eq!(count_wyckoff_positions("AB_cF8_225_a_b:Na-Cl").unwrap(), 2);
/// ```
pub fn count_wyckoff_positions(protostructure_label: &str) -> Result<usize> {
    let aflow_label = protostructure_label
        .split(':')
        .next()
        .expect("split always yields at least one element");

    // Skip prototype formula, Pearson symbol, and spg number (first 3 underscore-separated parts)
    let parts: Vec<&str> = aflow_label.splitn(4, '_').collect();
    if parts.len() < 4 {
        return Err(FerroxError::InvalidStructure {
            index: 0,
            reason: "Invalid protostructure label: missing required parts".to_string(),
        });
    }

    let wyk_letters = parts[3].replace('_', "");
    if wyk_letters.trim().is_empty() {
        return Err(FerroxError::InvalidStructure {
            index: 0,
            reason: "Invalid protostructure label: empty Wyckoff positions".to_string(),
        });
    }

    let mut count = 0usize;
    let mut num_buf = String::new();
    for ch in wyk_letters.chars() {
        if ch.is_alphabetic() {
            count += if num_buf.is_empty() {
                1
            } else {
                let val = num_buf.parse::<usize>().unwrap_or(1);
                num_buf.clear();
                val
            };
        } else {
            num_buf.push(ch);
        }
    }
    if !num_buf.is_empty() {
        return Err(FerroxError::InvalidStructure {
            index: 0,
            reason: format!(
                "Invalid protostructure label: trailing digits '{num_buf}' without Wyckoff letter"
            ),
        });
    }

    Ok(count)
}

// === Structure Method ===

impl Structure {
    /// Get AFLOW-style protostructure label.
    ///
    /// The label encodes the prototype formula, Pearson symbol, space group number,
    /// canonicalized Wyckoff positions, and chemical system in the format:
    /// `{prototype_formula}_{pearson_symbol}_{spg_num}_{wyckoff_positions}:{chemical_system}`
    ///
    /// # Arguments
    ///
    /// * `symprec` - Symmetry precision for space group detection (Angstroms)
    ///
    /// # Examples
    ///
    /// ```rust,ignore
    /// let label = nacl_structure.get_protostructure_label(0.1)?;
    /// assert_eq!(label, "AB_cF8_225_a_b:Cl-Na");
    /// ```
    pub fn get_protostructure_label(&self, symprec: f64) -> Result<String> {
        let dataset = self.get_symmetry_dataset(symprec)?;
        self.protostructure_label_from_dataset(&dataset)
    }

    /// Compute AFLOW protostructure label from a pre-computed MoyoDataset.
    ///
    /// Use this when the dataset is already available (e.g. from `get_all_metadata`)
    /// to avoid recomputing symmetry.
    pub fn protostructure_label_from_dataset(&self, dataset: &moyo::MoyoDataset) -> Result<String> {
        let spg_num = dataset.number;
        let comp = self.composition();

        // Group sites by orbit
        let mut orbit_groups: HashMap<usize, Vec<usize>> = HashMap::new();
        for (idx, &orbit_id) in dataset.orbits.iter().enumerate() {
            orbit_groups.entry(orbit_id).or_default().push(idx);
        }

        let species = self.species();

        // Create equivalent_wyckoff_labels: (element_symbol, orbit_size, wyckoff_letter)
        let mut equiv_labels: Vec<(&str, usize, char)> = orbit_groups
            .values()
            .map(|orbit| {
                let first_idx = orbit[0];
                let element = species[first_idx].element.symbol();
                let count = orbit.len();
                let wyckoff = dataset.wyckoffs[first_idx];
                (element, count, wyckoff)
            })
            .collect();
        equiv_labels.sort_by(|left, right| left.0.cmp(right.0).then(left.2.cmp(&right.2)));

        let multiplicities =
            WYCKOFF_MULTIPLICITIES
                .get(&spg_num)
                .ok_or_else(|| FerroxError::InvalidStructure {
                    index: 0,
                    reason: format!("No Wyckoff multiplicities for space group {spg_num}"),
                })?;

        // Group by element and build Wyckoff strings
        let mut element_dict: Vec<(&str, usize)> = Vec::new();
        let mut element_wyckoffs: Vec<String> = Vec::new();

        let mut label_idx = 0;
        while label_idx < equiv_labels.len() {
            let current_element = equiv_labels[label_idx].0;
            let start = label_idx;

            while label_idx < equiv_labels.len() && equiv_labels[label_idx].0 == current_element {
                label_idx += 1;
            }
            let label_group = &equiv_labels[start..label_idx];

            // Sum Wyckoff multiplicities for this element
            let total_mult: usize =
                label_group
                    .iter()
                    .try_fold(0usize, |acc, (_, _, wyk_letter)| {
                        multiplicities
                        .get(wyk_letter)
                        .copied()
                        .map(|mult| acc + mult)
                        .ok_or_else(|| FerroxError::InvalidStructure {
                            index: 0,
                            reason: format!(
                                "Unknown Wyckoff letter '{wyk_letter}' for space group {spg_num}"
                            ),
                        })
                    })?;
            element_dict.push((current_element, total_mult));

            // Count consecutive same Wyckoff letters (run-length encoding)
            let mut wyckoff_counts: Vec<(usize, char)> = Vec::new();
            for &(_, _, wyk_letter) in label_group {
                if let Some(last) = wyckoff_counts.last_mut()
                    && last.1 == wyk_letter
                {
                    last.0 += 1;
                    continue;
                }
                wyckoff_counts.push((1, wyk_letter));
            }

            let wyckoff_str: String = wyckoff_counts
                .iter()
                .map(|(count, letter)| {
                    if *count == 1 {
                        letter.to_string()
                    } else {
                        format!("{count}{letter}")
                    }
                })
                .collect();
            element_wyckoffs.push(wyckoff_str);
        }

        let all_wyckoffs = element_wyckoffs.join("_");
        let canonical = canonicalize_wyckoffs(&all_wyckoffs, spg_num)?;

        let proto_formula =
            get_prototype_formula(&comp).ok_or_else(|| FerroxError::InvalidStructure {
                index: 0,
                reason: "Could not compute prototype formula".to_string(),
            })?;

        let chemsys = comp.chemical_system();

        // Verify Wyckoff multiplicities match the actual composition
        let observed_comp = Composition::from_elements(element_dict.iter().map(|&(sym, amt)| {
            (
                Element::from_symbol(sym).expect("valid element symbol"),
                amt as f64,
            )
        }));
        let expected_formula = comp.reduced_formula();
        let observed_formula = observed_comp.reduced_formula();

        if observed_formula != expected_formula {
            let label = format!(
                "{proto_formula}_{}_{}_{canonical}",
                dataset.pearson_symbol, spg_num
            );
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: format!(
                    "Invalid WP multiplicities - {label}:{chemsys}, \
                     expected {observed_formula} to be {expected_formula}"
                ),
            });
        }

        Ok(format!(
            "{proto_formula}_{}_{}_{canonical}:{chemsys}",
            dataset.pearson_symbol, spg_num
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::element::Element;
    use crate::lattice::Lattice;
    use crate::species::Species;

    #[test]
    fn test_get_prototype_formula_binary() {
        let cases: &[(&[(Element, f64)], &str)] = &[
            (&[(Element::Fe, 2.0), (Element::O, 3.0)], "A2B3"),
            (&[(Element::Na, 1.0), (Element::Cl, 1.0)], "AB"),
            (&[(Element::H, 2.0), (Element::O, 1.0)], "A2B"),
            (&[(Element::Ca, 1.0), (Element::F, 2.0)], "AB2"),
        ];
        for (elements, expected) in cases {
            let comp = Composition::from_elements(elements.iter().copied());
            assert_eq!(
                get_prototype_formula(&comp).as_deref(),
                Some(*expected),
                "elements: {elements:?}"
            );
        }
    }

    #[test]
    fn test_get_prototype_formula_gcd_reduction() {
        // Fe4O6 should reduce to A2B3 (same as Fe2O3)
        let comp = Composition::from_elements([(Element::Fe, 4.0), (Element::O, 6.0)]);
        assert_eq!(get_prototype_formula(&comp).as_deref(), Some("A2B3"));
    }

    #[test]
    fn test_get_prototype_formula_ternary() {
        let comp = Composition::from_formula("LiFePO4").unwrap();
        assert_eq!(get_prototype_formula(&comp).as_deref(), Some("ABC4D"));
    }

    #[test]
    fn test_get_prototype_formula_empty() {
        let comp = Composition::from_elements([]);
        assert_eq!(get_prototype_formula(&comp), None);
    }

    #[test]
    fn test_split_alpha_numeric() {
        assert_eq!(split_alpha_numeric("2a3b"), vec!["2", "a", "3", "b"]);
        assert_eq!(split_alpha_numeric("a"), vec!["a"]);
        assert_eq!(split_alpha_numeric("12c"), vec!["12", "c"]);
        assert_eq!(
            split_alpha_numeric("1a2b3c"),
            vec!["1", "a", "2", "b", "3", "c"]
        );
    }

    #[test]
    fn test_canonicalize_wyckoffs_identity() {
        // Space group 1 has only one relabeling (identity)
        let result = canonicalize_wyckoffs("1a", 1).unwrap();
        assert_eq!(result, "a");
    }

    #[test]
    fn test_count_wyckoff_positions() {
        assert_eq!(count_wyckoff_positions("AB_cF8_225_a_b:Cl-Na").unwrap(), 2);
        assert_eq!(
            count_wyckoff_positions("A2B3_hR10_167_c_e:Al-O").unwrap(),
            2
        );
        assert_eq!(count_wyckoff_positions("AB_oP8_62_c_c:Fe-Si").unwrap(), 2);
    }

    #[test]
    fn test_count_wyckoff_positions_with_multiplier() {
        // "2a" means 2 Wyckoff positions of type a
        assert_eq!(count_wyckoff_positions("A_cI2_229_2a:Fe").unwrap_or(0), 2);
    }

    #[test]
    fn test_count_wyckoff_positions_invalid() {
        assert!(count_wyckoff_positions("invalid").is_err());
        assert!(count_wyckoff_positions("A_B").is_err());
    }

    #[test]
    fn test_count_wyckoff_positions_trailing_digits_rejected() {
        // Trailing digits without a Wyckoff letter are malformed
        assert!(count_wyckoff_positions("A_cF4_225_a2:Cu").is_err());
        assert!(count_wyckoff_positions("AB_cF8_225_a_3:Na-Cl").is_err());
    }

    /// Helper to build an FCC conventional cell for testing.
    fn make_fcc_conventional(element: Element, latt_param: f64) -> Structure {
        Structure::new(
            Lattice::cubic(latt_param),
            vec![Species::neutral(element); 4],
            vec![
                nalgebra::Vector3::new(0.0, 0.0, 0.0),
                nalgebra::Vector3::new(0.5, 0.5, 0.0),
                nalgebra::Vector3::new(0.5, 0.0, 0.5),
                nalgebra::Vector3::new(0.0, 0.5, 0.5),
            ],
        )
    }

    #[test]
    fn test_protostructure_label_fcc_cu() {
        let cu = make_fcc_conventional(Element::Cu, 3.6);
        let label = cu.get_protostructure_label(1e-4).unwrap();
        assert!(
            label.starts_with("A_"),
            "label should start with 'A_': {label}"
        );
        assert!(
            label.contains("225"),
            "label should contain spg 225: {label}"
        );
        assert!(
            label.ends_with(":Cu"),
            "label should end with ':Cu': {label}"
        );
    }

    #[test]
    fn test_protostructure_label_nacl() {
        let lattice = Lattice::cubic(5.64);
        let mut species = vec![Species::neutral(Element::Na); 4];
        species.extend(vec![Species::neutral(Element::Cl); 4]);
        let frac_coords = vec![
            nalgebra::Vector3::new(0.0, 0.0, 0.0),
            nalgebra::Vector3::new(0.5, 0.5, 0.0),
            nalgebra::Vector3::new(0.5, 0.0, 0.5),
            nalgebra::Vector3::new(0.0, 0.5, 0.5),
            nalgebra::Vector3::new(0.5, 0.0, 0.0),
            nalgebra::Vector3::new(0.0, 0.5, 0.0),
            nalgebra::Vector3::new(0.0, 0.0, 0.5),
            nalgebra::Vector3::new(0.5, 0.5, 0.5),
        ];
        let nacl = Structure::new(lattice, species, frac_coords);
        let label = nacl.get_protostructure_label(0.1).unwrap();
        assert!(
            label.starts_with("AB_"),
            "label should start with 'AB_': {label}"
        );
        assert!(
            label.contains("225"),
            "label should contain spg 225: {label}"
        );
        assert!(
            label.ends_with(":Cl-Na"),
            "label should end with ':Cl-Na': {label}"
        );
    }
}
