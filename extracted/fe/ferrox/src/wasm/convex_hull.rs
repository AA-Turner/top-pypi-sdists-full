//! Convex-hull WASM bindings.

use serde::{Deserialize, Serialize};
use tsify_next::Tsify;
use wasm_bindgen::prelude::*;

use crate::analysis::convex_hull::{
    ConvexHullEntry, calculate_e_above_hull as calculate_e_above_hull_rs,
};
use crate::composition::Composition;
use crate::wasm_types::WasmResult;

#[derive(Debug, Clone, Serialize, Deserialize, Tsify)]
#[tsify(into_wasm_abi, from_wasm_abi)]
pub struct JsConvexHullEntry {
    pub entry_id: Option<String>,
    pub composition: String,
    pub energy: Option<f64>,
    pub energy_per_atom: Option<f64>,
    pub e_form_per_atom: Option<f64>,
    pub correction: Option<f64>,
}

#[derive(Debug, Clone, Serialize, Deserialize, Tsify)]
#[tsify(into_wasm_abi)]
pub struct JsConvexHullDistance {
    pub entry_id: String,
    pub e_above_hull: f64,
}

fn parse_hull_entry(
    entry_idx: usize,
    js_entry: &JsConvexHullEntry,
) -> Result<ConvexHullEntry, String> {
    let composition = Composition::from_formula(&js_entry.composition)
        .map_err(|err| format!("entries[{entry_idx}].composition formula parse failed: {err}"))?;
    let atom_count = composition.num_atoms();
    if !atom_count.is_finite() || atom_count <= 0.0 {
        return Err(format!(
            "entries[{entry_idx}] has invalid atom count: {atom_count}"
        ));
    }

    let energy_total = js_entry.energy;
    let energy_per_atom = js_entry.energy_per_atom;

    if let Some(value) = energy_total
        && !value.is_finite()
    {
        return Err(format!("entries[{entry_idx}].energy must be finite"));
    }
    if let Some(value) = energy_per_atom
        && !value.is_finite()
    {
        return Err(format!(
            "entries[{entry_idx}].energy_per_atom must be finite"
        ));
    }
    if let (Some(total_energy), Some(per_atom_energy)) = (energy_total, energy_per_atom)
        && ((total_energy / atom_count) - per_atom_energy).abs() > 1e-8
    {
        return Err(format!(
            "entries[{entry_idx}] has inconsistent 'energy' and 'energy_per_atom'"
        ));
    }

    if let Some(e_form_per_atom) = js_entry.e_form_per_atom
        && !e_form_per_atom.is_finite()
    {
        return Err(format!(
            "entries[{entry_idx}].e_form_per_atom must be finite"
        ));
    }
    if let Some(correction) = js_entry.correction
        && !correction.is_finite()
    {
        return Err(format!("entries[{entry_idx}].correction must be finite"));
    }

    let energy = if let Some(total_energy) = energy_total {
        total_energy
    } else if let Some(per_atom_energy) = energy_per_atom {
        per_atom_energy * atom_count
    } else if js_entry.e_form_per_atom.is_some() {
        f64::NAN
    } else {
        return Err(format!(
            "entries[{entry_idx}] requires one of: energy, energy_per_atom, e_form_per_atom"
        ));
    };

    Ok(ConvexHullEntry {
        entry_id: js_entry.entry_id.clone(),
        composition,
        energy,
        energy_per_atom,
        e_form_per_atom: js_entry.e_form_per_atom,
        correction: js_entry.correction,
    })
}

fn parse_hull_entries(entries: &[JsConvexHullEntry]) -> Result<Vec<ConvexHullEntry>, String> {
    entries
        .iter()
        .enumerate()
        .map(|(entry_idx, entry)| parse_hull_entry(entry_idx, entry))
        .collect()
}

fn parse_query_and_refs(
    entries: Vec<JsConvexHullEntry>,
    reference_entries: Option<Vec<JsConvexHullEntry>>,
) -> Result<(Vec<ConvexHullEntry>, Option<Vec<ConvexHullEntry>>), String> {
    let query_entries = parse_hull_entries(&entries)?;
    let reference_entries = reference_entries
        .as_ref()
        .map(|reference_entries| parse_hull_entries(reference_entries))
        .transpose()?;
    Ok((query_entries, reference_entries))
}

#[wasm_bindgen]
pub fn calculate_e_above_hull(
    entries: Vec<JsConvexHullEntry>,
    reference_entries: Option<Vec<JsConvexHullEntry>>,
) -> WasmResult<Vec<f64>> {
    let result: Result<Vec<f64>, String> = (|| {
        let (query_entries, reference_entries) = parse_query_and_refs(entries, reference_entries)?;
        let ref_entries = reference_entries.as_deref().unwrap_or(&query_entries);
        calculate_e_above_hull_rs(&query_entries, ref_entries).map_err(|err| err.to_string())
    })();
    result.into()
}

#[wasm_bindgen]
pub fn calculate_e_above_hull_map(
    entries: Vec<JsConvexHullEntry>,
    reference_entries: Option<Vec<JsConvexHullEntry>>,
) -> WasmResult<Vec<JsConvexHullDistance>> {
    let result: Result<Vec<JsConvexHullDistance>, String> = (|| {
        let (query_entries, reference_entries) = parse_query_and_refs(entries, reference_entries)?;
        let ref_entries = reference_entries.as_deref().unwrap_or(&query_entries);
        let mut seen_ids = std::collections::HashSet::with_capacity(query_entries.len());
        for entry in &query_entries {
            let entry_id = entry.id_or_formula();
            if !seen_ids.insert(entry_id.clone()) {
                return Err(format!("Duplicate entry id in query entries: {entry_id}"));
            }
        }
        let distances = calculate_e_above_hull_rs(&query_entries, ref_entries)
            .map_err(|err| err.to_string())?;
        let mut out = Vec::with_capacity(query_entries.len());
        for (entry, distance) in query_entries.iter().zip(distances.iter()) {
            let entry_id = entry.id_or_formula();
            out.push(JsConvexHullDistance {
                entry_id,
                e_above_hull: *distance,
            });
        }
        Ok(out)
    })();
    result.into()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::wasm_types::WasmResult;

    fn make_entry(formula: &str, e_form_per_atom: f64, entry_id: &str) -> JsConvexHullEntry {
        JsConvexHullEntry {
            entry_id: Some(entry_id.to_string()),
            composition: formula.to_string(),
            energy: None,
            energy_per_atom: None,
            e_form_per_atom: Some(e_form_per_atom),
            correction: None,
        }
    }

    #[test]
    fn test_calculate_e_above_hull_binary_known_answer() {
        let reference_entries = vec![
            make_entry("Li", 0.0, "li"),
            make_entry("O", 0.0, "o"),
            make_entry("LiO", -1.0, "lio"),
            make_entry("Li2O", -0.2, "li2o"),
        ];
        let query_entries = vec![make_entry("Li2O", -0.2, "li2o_query")];
        let result = calculate_e_above_hull(query_entries, Some(reference_entries));
        let WasmResult::Ok { ok: distances } = result else {
            panic!("expected WasmResult::Ok");
        };
        assert_eq!(distances.len(), 1);
        assert!((distances[0] - 0.466_666_666_7).abs() < 1e-8);
    }

    #[test]
    fn test_calculate_e_above_hull_map_uses_entry_ids() {
        let reference_entries = vec![
            make_entry("Li", 0.0, "li"),
            make_entry("O", 0.0, "o"),
            make_entry("LiO", -1.0, "lio"),
        ];
        let query_entries = vec![
            make_entry("LiO", -1.0, "lio_on_hull"),
            make_entry("LiO", -0.8, "lio_above"),
        ];
        let result = calculate_e_above_hull_map(query_entries, Some(reference_entries));
        let WasmResult::Ok { ok: distances } = result else {
            panic!("expected WasmResult::Ok");
        };
        assert_eq!(distances.len(), 2);
        assert_eq!(distances[0].entry_id, "lio_on_hull");
        assert!(distances[0].e_above_hull.abs() < 1e-12);
        assert_eq!(distances[1].entry_id, "lio_above");
        assert!((distances[1].e_above_hull - 0.2).abs() < 1e-12);
    }

    #[test]
    fn test_calculate_e_above_hull_map_errors_on_duplicate_ids() {
        let reference_entries = vec![
            make_entry("Li", 0.0, "li"),
            make_entry("O", 0.0, "o"),
            make_entry("LiO", -1.0, "lio"),
        ];
        let query_entries = vec![
            make_entry("LiO", -1.0, "dup"),
            make_entry("LiO", -0.8, "dup"),
        ];
        let result = calculate_e_above_hull_map(query_entries, Some(reference_entries));
        let WasmResult::Err { error } = result else {
            panic!("expected WasmResult::Err");
        };
        assert!(error.contains("Duplicate entry id in query entries: dup"));
    }
}
