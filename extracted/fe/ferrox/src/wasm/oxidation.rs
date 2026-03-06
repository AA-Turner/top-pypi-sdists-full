//! Oxidation state analysis WASM bindings.
//!
//! Full parity with Python oxidation API. Uses strongly-typed JsCrystal and
//! JsOxiStateGuess/JsOxidationStates outputs.

use serde_wasm_bindgen::from_value;
use wasm_bindgen::prelude::*;

use crate::composition::Composition;
use crate::element::Element;
use crate::io::parse_structure_json;
use crate::oxidation;
use crate::structure::Structure;
use crate::wasm_types::{
    JsCrystal, JsOxiStateGuess, JsOxidationStatePair, JsOxidationStates, WasmResult,
};

/// Extract elements and amounts from a structure's composition.
fn get_elements_and_amounts(struc: &Structure) -> (Vec<Element>, Vec<f64>) {
    get_elements_and_amounts_from_comp(&struc.composition())
}

/// Extract elements and amounts from a composition.
fn get_elements_and_amounts_from_comp(comp: &Composition) -> (Vec<Element>, Vec<f64>) {
    let elements: Vec<Element> = comp.elements();
    let amounts: Vec<f64> = elements.iter().map(|elem| comp.get(*elem)).collect();
    (elements, amounts)
}

/// Guess oxidation states for a structure or formula.
///
/// Accepts either a structure (JsCrystal object) or a formula string like "Fe2O3".
/// When passing a structure, use the JsCrystal object directly. When passing
/// a formula, use a string.
#[wasm_bindgen]
pub fn oxi_state_guesses(
    structure_or_formula: JsValue,
    all_states: bool,
) -> WasmResult<Vec<JsOxiStateGuess>> {
    let result: Result<Vec<JsOxiStateGuess>, String> = (|| {
        let (elements, amounts) = if structure_or_formula.is_string() {
            let s = structure_or_formula
                .as_string()
                .ok_or("Expected string or structure")?;
            let input = s.trim_start();
            if input.starts_with('{') {
                let struc = parse_structure_json(input)
                    .map_err(|err| format!("Invalid structure JSON: {err}"))?;
                get_elements_and_amounts(&struc)
            } else {
                let comp = Composition::from_formula(input)
                    .map_err(|err| format!("Invalid formula: {err}"))?;
                get_elements_and_amounts_from_comp(&comp)
            }
        } else {
            let js_crystal: JsCrystal = from_value(structure_or_formula)
                .map_err(|err| format!("Invalid structure: {err}"))?;
            let struc = js_crystal.to_structure()?;
            get_elements_and_amounts(&struc)
        };

        // Default options mirror Python-side behavior: neutral target charge and no overrides.
        let guesses = oxidation::oxi_state_guesses(&elements, &amounts, 0, None, all_states, None);

        Ok(guesses
            .into_iter()
            .map(|guess| JsOxiStateGuess {
                oxidation_states: guess
                    .oxidation_states
                    .into_iter()
                    .map(|(elem, oxi)| JsOxidationStatePair {
                        element: elem,
                        oxidation_state: oxi,
                    })
                    .collect(),
                probability: guess.probability,
            })
            .collect())
    })();
    result.into()
}

/// Run oxi-state guessing for a structure and return the best guess.
fn guess_best_oxi(struc: &Structure) -> Result<oxidation::OxiStateGuess, String> {
    let (elements, amounts) = get_elements_and_amounts(struc);
    let guesses = oxidation::oxi_state_guesses(&elements, &amounts, 0, None, false, None);
    guesses
        .into_iter()
        .next()
        .ok_or_else(|| "No valid oxidation state assignments found".to_string())
}

/// Add oxidation states from guesses to a structure.
#[wasm_bindgen]
pub fn add_charges_from_oxi_state_guesses(structure: JsCrystal) -> WasmResult<JsCrystal> {
    let result: Result<JsCrystal, String> = (|| {
        let mut struc = structure.to_structure()?;
        let best = guess_best_oxi(&struc)?;
        for site_occ in struc.site_occupancies.iter_mut() {
            for (sp, _) in site_occ.species.iter_mut() {
                if let Some(&oxi) = best.oxidation_states.get(sp.element.symbol()) {
                    let rounded_oxi = oxi.round();
                    if rounded_oxi.is_finite()
                        && rounded_oxi >= f64::from(i8::MIN)
                        && rounded_oxi <= f64::from(i8::MAX)
                    {
                        sp.oxidation_state = Some(rounded_oxi as i8);
                    } else {
                        sp.oxidation_state = None;
                    }
                }
            }
        }
        Ok(JsCrystal::from_structure(&struc))
    })();
    result.into()
}

/// Compute bond valence sums for each site.
#[wasm_bindgen]
pub fn compute_bv_sums(
    structure: JsCrystal,
    max_radius: f64,
    scale_factor: f64,
) -> WasmResult<Vec<f64>> {
    let result: Result<Vec<f64>, String> = (|| {
        if !max_radius.is_finite() || max_radius <= 0.0 {
            return Err("max_radius must be positive and finite".to_string());
        }
        if !scale_factor.is_finite() || scale_factor <= 0.0 {
            return Err("scale_factor must be positive and finite".to_string());
        }

        let struc = structure.to_structure()?;
        let mut sums = Vec::with_capacity(struc.num_sites());
        let all_neighbors = struc.get_all_neighbors(max_radius);

        for (site_idx, site_neighbors) in all_neighbors.iter().enumerate() {
            let site_element = struc.site_occupancies[site_idx].dominant_species().element;
            let bv_neighbors: Vec<oxidation::BvNeighbor> = site_neighbors
                .iter()
                .filter_map(|&(neighbor_idx, distance, _image)| {
                    let neighbor_site = &struc.site_occupancies[neighbor_idx];
                    let maybe_dominant_neighbor = neighbor_site
                        .species
                        .iter()
                        .filter(|(_, occupancy)| occupancy.is_finite())
                        .max_by(|a, b| a.1.total_cmp(&b.1));
                    let (neighbor_sp, neighbor_occ) = maybe_dominant_neighbor?;
                    Some(oxidation::BvNeighbor {
                        element: neighbor_sp.element,
                        distance,
                        occupancy: *neighbor_occ,
                    })
                })
                .collect();
            sums.push(oxidation::calculate_bv_sum(
                site_element,
                &bv_neighbors,
                scale_factor,
            ));
        }
        Ok(sums)
    })();
    result.into()
}

/// Guess oxidation states using structure's composition.
#[wasm_bindgen]
pub fn guess_oxidation_states(structure: JsCrystal) -> WasmResult<JsOxidationStates> {
    let result: Result<JsOxidationStates, String> = (|| {
        let struc = structure.to_structure()?;
        let best = guess_best_oxi(&struc)?;
        let mut element_symbols: Vec<String> = best.oxidation_states.keys().cloned().collect();
        element_symbols.sort();
        let oxidation_states: Vec<f64> = element_symbols
            .iter()
            .map(|elem| *best.oxidation_states.get(elem).unwrap())
            .collect();

        Ok(JsOxidationStates {
            elements: element_symbols,
            oxidation_states,
        })
    })();
    result.into()
}

/// Add oxidation states by element.
///
/// oxi_states: JS object mapping element symbol to oxidation state (e.g. { "Fe": 3, "O": -2 })
#[wasm_bindgen]
pub fn add_oxidation_state_by_element(
    structure: JsCrystal,
    oxi_states: JsValue,
) -> WasmResult<JsCrystal> {
    let result: Result<JsCrystal, String> = (|| {
        let oxi_map: std::collections::HashMap<String, i8> =
            from_value(oxi_states).map_err(|err| format!("Invalid oxi_states object: {err}"))?;
        let mut struc = structure.to_structure()?;

        for site_occ in struc.site_occupancies.iter_mut() {
            for (sp, _) in site_occ.species.iter_mut() {
                if let Some(&oxi) = oxi_map.get(sp.element.symbol()) {
                    sp.oxidation_state = Some(oxi);
                }
            }
        }
        Ok(JsCrystal::from_structure(&struc))
    })();
    result.into()
}

/// Add oxidation states by site.
///
/// oxi_states length must match number of sites.
#[wasm_bindgen]
pub fn add_oxidation_state_by_site(
    structure: JsCrystal,
    oxi_states: Vec<i8>,
) -> WasmResult<JsCrystal> {
    let result: Result<JsCrystal, String> = (|| {
        let mut struc = structure.to_structure()?;
        if oxi_states.len() != struc.num_sites() {
            return Err(format!(
                "Number of oxidation states ({}) must match number of sites ({})",
                oxi_states.len(),
                struc.num_sites()
            ));
        }
        for (idx, &oxi) in oxi_states.iter().enumerate() {
            for (sp, _) in struc.site_occupancies[idx].species.iter_mut() {
                sp.oxidation_state = Some(oxi);
            }
        }
        Ok(JsCrystal::from_structure(&struc))
    })();
    result.into()
}

/// Remove oxidation states from a structure.
#[wasm_bindgen]
pub fn remove_oxidation_states(structure: JsCrystal) -> WasmResult<JsCrystal> {
    let result: Result<JsCrystal, String> = (|| {
        let mut struc = structure.to_structure()?;
        for site_occ in struc.site_occupancies.iter_mut() {
            for (sp, _) in site_occ.species.iter_mut() {
                sp.oxidation_state = None;
            }
        }
        Ok(JsCrystal::from_structure(&struc))
    })();
    result.into()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::element::Element;
    use crate::lattice::Lattice;
    use crate::species::Species;
    use crate::structure::Structure;
    use nalgebra::Vector3;
    use wasm_bindgen::JsValue;

    fn oxi_at(struc: &Structure, site_idx: usize) -> Option<i8> {
        struc.site_occupancies[site_idx].species[0]
            .0
            .oxidation_state
    }

    fn nacl_structure() -> Structure {
        Structure::new(
            Lattice::cubic(5.0),
            vec![Species::neutral(Element::Na), Species::neutral(Element::Cl)],
            vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
        )
    }

    fn fe2o3_structure() -> Structure {
        Structure::new(
            Lattice::cubic(5.0),
            vec![
                Species::neutral(Element::Fe),
                Species::neutral(Element::Fe),
                Species::neutral(Element::O),
                Species::neutral(Element::O),
                Species::neutral(Element::O),
            ],
            vec![
                Vector3::new(0.0, 0.0, 0.0),
                Vector3::new(0.5, 0.5, 0.5),
                Vector3::new(0.25, 0.25, 0.25),
                Vector3::new(0.75, 0.75, 0.25),
                Vector3::new(0.25, 0.75, 0.75),
            ],
        )
    }

    #[test]
    fn test_add_charges_from_oxi_state_guesses() {
        let struc = nacl_structure();
        let js_crystal = JsCrystal::from_structure(&struc);
        let result = add_charges_from_oxi_state_guesses(js_crystal);
        let WasmResult::Ok { ok: out } = result else {
            panic!("add_charges_from_oxi_state_guesses should succeed");
        };
        let back = out.to_structure().unwrap();
        assert_eq!(oxi_at(&back, 0), Some(1));
        assert_eq!(oxi_at(&back, 1), Some(-1));
    }

    #[test]
    fn test_compute_bv_sums() {
        let struc = fe2o3_structure();
        let js_crystal = JsCrystal::from_structure(&struc);
        let result = compute_bv_sums(js_crystal, 4.0, 1.0);
        let WasmResult::Ok { ok: sums } = result else {
            panic!("compute_bv_sums should succeed");
        };
        assert_eq!(sums.len(), 5);
    }

    #[test]
    fn test_guess_oxidation_states() {
        let struc = nacl_structure();
        let js_crystal = JsCrystal::from_structure(&struc);
        let result = guess_oxidation_states(js_crystal);
        let WasmResult::Ok { ok: states } = result else {
            panic!("guess_oxidation_states should succeed");
        };
        assert_eq!(states.elements.len(), 2);
        let na_idx = states.elements.iter().position(|e| e == "Na").unwrap();
        let cl_idx = states.elements.iter().position(|e| e == "Cl").unwrap();
        assert!((states.oxidation_states[na_idx] - 1.0).abs() < 0.01);
        assert!((states.oxidation_states[cl_idx] - (-1.0)).abs() < 0.01);
    }

    // These tests use JsValue/serde_wasm_bindgen APIs that panic on non-wasm32 targets.
    #[cfg(target_arch = "wasm32")]
    #[test]
    fn test_oxi_state_guesses_formula_string() {
        let result = oxi_state_guesses(JsValue::from_str("NaCl"), true);
        let WasmResult::Ok { ok: guesses } = result else {
            panic!("oxi_state_guesses should succeed for formula input");
        };
        assert!(!guesses.is_empty());
    }

    #[cfg(target_arch = "wasm32")]
    #[test]
    fn test_add_oxidation_state_by_element() {
        let struc = nacl_structure();
        let js_crystal = JsCrystal::from_structure(&struc);
        let oxi_map = serde_wasm_bindgen::to_value(&serde_json::json!({
            "Na": 1,
            "Cl": -1
        }))
        .unwrap();
        let result = add_oxidation_state_by_element(js_crystal, oxi_map);
        let WasmResult::Ok { ok: out } = result else {
            panic!("add_oxidation_state_by_element should succeed");
        };
        let back = out.to_structure().unwrap();
        assert_eq!(oxi_at(&back, 0), Some(1));
        assert_eq!(oxi_at(&back, 1), Some(-1));
    }

    #[test]
    fn test_add_oxidation_state_by_site() {
        let struc = nacl_structure();
        let js_crystal = JsCrystal::from_structure(&struc);
        let result = add_oxidation_state_by_site(js_crystal, vec![1, -1]);
        let WasmResult::Ok { ok: out } = result else {
            panic!("add_oxidation_state_by_site should succeed");
        };
        let back = out.to_structure().unwrap();
        assert_eq!(oxi_at(&back, 0), Some(1));
        assert_eq!(oxi_at(&back, 1), Some(-1));
    }

    #[test]
    fn test_remove_oxidation_states() {
        let struc = Structure::new(
            Lattice::cubic(5.0),
            vec![
                Species::new(Element::Na, Some(1)),
                Species::new(Element::Cl, Some(-1)),
            ],
            vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
        );
        let js_crystal = JsCrystal::from_structure(&struc);
        let result = remove_oxidation_states(js_crystal);
        let WasmResult::Ok { ok: out } = result else {
            panic!("remove_oxidation_states should succeed");
        };
        let back = out.to_structure().unwrap();
        assert_eq!(oxi_at(&back, 0), None);
        assert_eq!(oxi_at(&back, 1), None);
    }

    #[test]
    fn test_compute_bv_sums_invalid_params() {
        let struc = nacl_structure();
        let js_crystal = JsCrystal::from_structure(&struc);
        let result = compute_bv_sums(js_crystal, -1.0, 1.0);
        let WasmResult::Err { error } = result else {
            panic!("compute_bv_sums should fail for negative max_radius");
        };
        assert!(error.contains("max_radius"));
    }
}
