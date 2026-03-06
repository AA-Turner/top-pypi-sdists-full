//! WASM bindings for Materials Project data processing.
//!
//! JavaScript handles HTTP (`fetch()`), Rust handles the heavy lifting:
//! gzip decompression, JSONL parsing, filtering, and field selection.

use std::collections::HashSet;
use std::io::{BufRead, BufReader};

use flate2::read::GzDecoder;
use serde_json::Value;
use wasm_bindgen::prelude::*;

/// Process gzip-compressed JSONL data with optional filtering and field selection.
#[wasm_bindgen(js_name = "processJsonlGz")]
pub fn process_jsonl_gz(
    data: &[u8],
    filter: JsValue,
    fields: JsValue,
    limit: JsValue,
) -> Result<JsValue, JsError> {
    process_data(
        BufReader::new(GzDecoder::new(data)),
        &filter,
        &fields,
        &limit,
    )
}

/// Process plain (uncompressed) JSONL data with optional filtering.
#[wasm_bindgen(js_name = "processJsonl")]
pub fn process_jsonl(
    data: &[u8],
    filter: JsValue,
    fields: JsValue,
    limit: JsValue,
) -> Result<JsValue, JsError> {
    process_data(BufReader::new(data), &filter, &fields, &limit)
}

fn process_data(
    reader: impl BufRead,
    filter_js: &JsValue,
    fields_js: &JsValue,
    limit_js: &JsValue,
) -> Result<JsValue, JsError> {
    let filter = parse_js_filter(filter_js)?;
    let field_set = parse_js_fields(fields_js)?;
    let max_docs = parse_js_limit(limit_js)?;

    let mut results: Vec<Value> = Vec::new();
    let mut consecutive_errors: u32 = 0;
    const MAX_CONSECUTIVE_ERRORS: u32 = 100;
    for line_result in reader.lines() {
        let line = match line_result {
            Ok(line) => {
                consecutive_errors = 0;
                line
            }
            Err(_) => {
                consecutive_errors += 1;
                if consecutive_errors >= MAX_CONSECUTIVE_ERRORS {
                    break;
                }
                continue;
            }
        };
        let trimmed = line.trim();
        if trimmed.is_empty() {
            continue;
        }
        let mut doc: Value = match serde_json::from_str(trimmed) {
            Ok(v) => v,
            Err(_) => continue,
        };
        if !doc.is_object() || !matches_filter(&doc, &filter) {
            continue;
        }
        if let Some(cap) = max_docs {
            if results.len() >= cap {
                break;
            }
        }
        if let Some(ref fset) = field_set {
            if let Some(obj) = doc.as_object_mut() {
                obj.retain(|key, _| fset.contains(key));
            }
        }
        results.push(doc);
    }

    serde_wasm_bindgen::to_value(&results)
        .map_err(|err| JsError::new(&format!("Serialization error: {err}")))
}

// === JS value parsing ===

fn parse_js_limit(limit: &JsValue) -> Result<Option<usize>, JsError> {
    if limit.is_undefined() || limit.is_null() {
        return Ok(None);
    }
    let val = limit
        .as_f64()
        .ok_or_else(|| JsError::new("limit must be a number"))?;
    if !val.is_finite() || val < 0.0 || val > usize::MAX as f64 || val.fract() != 0.0 {
        return Err(JsError::new(
            "limit must be a non-negative integer within usize range",
        ));
    }
    Ok(Some(val as usize))
}

fn parse_js_fields(fields_js: &JsValue) -> Result<Option<HashSet<String>>, JsError> {
    if fields_js.is_undefined() || fields_js.is_null() {
        return Ok(None);
    }
    let arr: Vec<String> = serde_wasm_bindgen::from_value(fields_js.clone())
        .map_err(|err| JsError::new(&format!("Invalid fields array: {err}")))?;
    Ok(Some(arr.into_iter().collect()))
}

fn parse_js_filter(filter_js: &JsValue) -> Result<ParsedFilter, JsError> {
    if filter_js.is_undefined() || filter_js.is_null() {
        return Ok(ParsedFilter::default());
    }

    let val: Value = serde_wasm_bindgen::from_value(filter_js.clone())
        .map_err(|err| JsError::new(&format!("Invalid filter: {err}")))?;

    let str_set = |key: &str| -> Option<HashSet<String>> {
        val.get(key).and_then(Value::as_array).map(|arr| {
            arr.iter()
                .filter_map(Value::as_str)
                .map(String::from)
                .collect()
        })
    };

    Ok(ParsedFilter {
        chemsys: val.get("chemsys").and_then(Value::as_str).map(|cs| {
            cs.split(',')
                .map(|s| s.trim().split('-').map(|e| e.trim().to_owned()).collect())
                .collect()
        }),
        elements: str_set("elements"),
        exclude_elements: str_set("exclude_elements"),
        material_ids: str_set("material_ids"),
        formula: val.get("formula").and_then(Value::as_str).map(String::from),
        energy_above_hull_max: val.get("energy_above_hull_max").and_then(Value::as_f64),
        band_gap_min: val.get("band_gap_min").and_then(Value::as_f64),
        band_gap_max: val.get("band_gap_max").and_then(Value::as_f64),
        nsites_min: val.get("nsites_min").and_then(Value::as_u64),
        nsites_max: val.get("nsites_max").and_then(Value::as_u64),
    })
}

// === Filter logic (mirrors src/mp.rs SearchFilter::matches) ===

#[derive(Default)]
struct ParsedFilter {
    chemsys: Option<Vec<HashSet<String>>>,
    elements: Option<HashSet<String>>,
    exclude_elements: Option<HashSet<String>>,
    material_ids: Option<HashSet<String>>,
    formula: Option<String>,
    energy_above_hull_max: Option<f64>,
    band_gap_min: Option<f64>,
    band_gap_max: Option<f64>,
    nsites_min: Option<u64>,
    nsites_max: Option<u64>,
}

fn extract_elements(doc: &Value) -> Option<HashSet<String>> {
    doc.get("elements").and_then(Value::as_array).map(|arr| {
        arr.iter()
            .filter_map(Value::as_str)
            .map(String::from)
            .collect()
    })
}

fn matches_filter(doc: &Value, filter: &ParsedFilter) -> bool {
    if let Some(ref systems) = filter.chemsys {
        match extract_elements(doc) {
            Some(ref elems) if !elems.is_empty() => {
                if !systems.iter().any(|sys| elems.is_subset(sys)) {
                    return false;
                }
            }
            _ => return false,
        }
    }
    if let Some(ref required) = filter.elements {
        match extract_elements(doc) {
            Some(ref elems) if required.is_subset(elems) => {}
            _ => return false,
        }
    }
    if let Some(ref excluded) = filter.exclude_elements {
        if let Some(ref elems) = extract_elements(doc) {
            if !excluded.is_disjoint(elems) {
                return false;
            }
        }
    }
    macro_rules! check_field {
        ($field:expr, $key:expr, $op:tt) => {
            if let Some(bound) = $field {
                match doc.get($key).and_then(Value::as_f64) {
                    Some(val) if val $op bound => {}
                    _ => return false,
                }
            }
        };
    }
    if let Some(ref ids) = filter.material_ids {
        match doc.get("material_id").and_then(Value::as_str) {
            Some(mid) if ids.contains(mid) => {}
            _ => return false,
        }
    }
    if let Some(ref formula) = filter.formula {
        match doc.get("formula_pretty").and_then(Value::as_str) {
            Some(fp) if fp == formula => {}
            _ => return false,
        }
    }
    check_field!(filter.energy_above_hull_max, "energy_above_hull", <=);
    check_field!(filter.band_gap_min, "band_gap", >=);
    check_field!(filter.band_gap_max, "band_gap", <=);
    if let Some(min) = filter.nsites_min {
        match doc.get("nsites").and_then(Value::as_u64) {
            Some(val) if val >= min => {}
            _ => return false,
        }
    }
    if let Some(max) = filter.nsites_max {
        match doc.get("nsites").and_then(Value::as_u64) {
            Some(val) if val <= max => {}
            _ => return false,
        }
    }
    true
}
