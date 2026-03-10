use crate::element::Element;
use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use crate::species::{SiteOccupancy, Species};
use crate::structure::Structure;
use nalgebra::Vector3;
use serde::Deserialize;
use std::collections::HashMap;

// === OPTIMADE JSON Parser ===

/// A single OPTIMADE species definition.
#[derive(Debug, Deserialize)]
struct OptimadeSpeciesDef {
    name: String,
    chemical_symbols: Vec<String>,
    concentration: Vec<f64>,
}

/// Attributes block of an OPTIMADE structure resource.
#[derive(Debug, Deserialize)]
struct OptimadeAttributes {
    lattice_vectors: Option<[[f64; 3]; 3]>,
    cartesian_site_positions: Vec<[f64; 3]>,
    species_at_sites: Vec<String>,
    #[serde(default)]
    species: Option<Vec<OptimadeSpeciesDef>>,
    #[serde(default)]
    dimension_types: Option<[u8; 3]>,
}

/// A single OPTIMADE structure resource (`type: "structures"`).
#[derive(Debug, Deserialize)]
struct OptimadeResource {
    #[serde(rename = "type")]
    type_field: String,
    #[allow(dead_code)]
    id: String,
    attributes: OptimadeAttributes,
}

/// Wrapper for OPTIMADE list responses (`{"data": [...]}`).
#[derive(Debug, Deserialize)]
struct OptimadeListResponse {
    data: Vec<serde_json::Value>,
}

/// Check whether a JSON string looks like OPTIMADE format.
///
/// Returns `true` if the top-level object (or its first `data` entry) has
/// `"type": "structures"` and an `attributes` field with at least
/// `cartesian_site_positions` and `species_at_sites`.
pub fn is_optimade_json(json: &str) -> bool {
    let parsed: serde_json::Value = match serde_json::from_str(json) {
        Ok(val) => val,
        Err(_) => return false,
    };
    is_optimade_value(&parsed)
}

/// Value-level OPTIMADE detection (reused by content-sniffing in `parse_structure_json`).
pub(super) fn is_optimade_value(val: &serde_json::Value) -> bool {
    let candidate = if let Some(data) = val.get("data") {
        if let Some(arr) = data.as_array() {
            match arr.first() {
                Some(first) => first,
                None => return false,
            }
        } else {
            data
        }
    } else {
        val
    };

    candidate.get("type").and_then(|t| t.as_str()) == Some("structures")
        && candidate.get("attributes").is_some()
}

/// Build a `SiteOccupancy` from an OPTIMADE species definition.
///
/// Handles disordered sites where `chemical_symbols` has multiple entries
/// with corresponding `concentration` values.
fn optimade_species_to_site_occupancy(
    species_def: &OptimadeSpeciesDef,
    site_idx: usize,
) -> Result<SiteOccupancy> {
    if species_def.chemical_symbols.len() != species_def.concentration.len() {
        return Err(FerroxError::ParseError {
            path: "optimade".to_string(),
            reason: format!(
                "Species '{}': chemical_symbols length ({}) != concentration length ({})",
                species_def.name,
                species_def.chemical_symbols.len(),
                species_def.concentration.len()
            ),
        });
    }

    let mut pairs: Vec<(Species, f64)> = Vec::new();
    for (sym, &conc) in species_def
        .chemical_symbols
        .iter()
        .zip(&species_def.concentration)
    {
        // Skip vacancy entries
        if sym == "vacancy" || sym == "X" {
            continue;
        }
        let elem = Element::from_symbol(sym).ok_or_else(|| FerroxError::ParseError {
            path: "optimade".to_string(),
            reason: format!("Unknown element symbol '{sym}' at site {site_idx}"),
        })?;
        if !conc.is_finite() || conc <= 0.0 {
            return Err(FerroxError::ParseError {
                path: "optimade".to_string(),
                reason: format!(
                    "Invalid concentration {conc} for '{sym}' in species '{}' at site {site_idx}",
                    species_def.name
                ),
            });
        }
        pairs.push((Species::neutral(elem), conc));
    }

    if pairs.is_empty() {
        return Err(FerroxError::ParseError {
            path: "optimade".to_string(),
            reason: format!(
                "Species '{}' at site {site_idx} has no valid elements (all vacancies?)",
                species_def.name
            ),
        });
    }

    Ok(SiteOccupancy::new(pairs))
}

/// Parse a single OPTIMADE structure resource into a `Structure`.
fn parse_optimade_resource(resource: &OptimadeResource) -> Result<Structure> {
    if resource.type_field != "structures" {
        return Err(FerroxError::ParseError {
            path: "optimade".to_string(),
            reason: format!("Expected type 'structures', got '{}'", resource.type_field),
        });
    }

    let attrs = &resource.attributes;
    let n_sites = attrs.cartesian_site_positions.len();

    if attrs.species_at_sites.len() != n_sites {
        return Err(FerroxError::ParseError {
            path: "optimade".to_string(),
            reason: format!(
                "cartesian_site_positions ({n_sites}) and species_at_sites ({}) length mismatch",
                attrs.species_at_sites.len()
            ),
        });
    }

    // Build species lookup from the species definitions
    let species_map: HashMap<String, &OptimadeSpeciesDef> = attrs
        .species
        .as_ref()
        .map(|defs| defs.iter().map(|def| (def.name.clone(), def)).collect())
        .unwrap_or_default();

    // Determine PBC from dimension_types (1=periodic, 0=non-periodic)
    let pbc = attrs
        .dimension_types
        .map(|dt| [dt[0] == 1, dt[1] == 1, dt[2] == 1])
        .unwrap_or([true, true, true]);

    // Build lattice
    let lattice_vecs = attrs
        .lattice_vectors
        .ok_or_else(|| FerroxError::ParseError {
            path: "optimade".to_string(),
            reason: "Missing lattice_vectors".to_string(),
        })?;

    let mut lattice = Lattice::from_array(lattice_vecs);
    lattice.pbc = pbc;

    // Convert Cartesian positions to fractional coords and build site occupancies
    let cart_coords: Vec<Vector3<f64>> = attrs
        .cartesian_site_positions
        .iter()
        .map(|pos| Vector3::new(pos[0], pos[1], pos[2]))
        .collect();

    let frac_coords = lattice.get_fractional_coords(&cart_coords);

    let mut site_occupancies = Vec::with_capacity(n_sites);
    for (site_idx, site_label) in attrs.species_at_sites.iter().enumerate() {
        let site_occ = if let Some(species_def) = species_map.get(site_label) {
            // Use the species definition for potentially disordered sites
            optimade_species_to_site_occupancy(species_def, site_idx)?
        } else {
            // Fall back to treating species_at_sites as element symbol
            let elem = Element::from_symbol(site_label).ok_or_else(|| FerroxError::ParseError {
                path: "optimade".to_string(),
                reason: format!(
                    "Unknown element/species '{site_label}' at site {site_idx} \
                         and no matching species definition found"
                ),
            })?;
            SiteOccupancy::ordered(Species::neutral(elem))
        };
        site_occupancies.push(site_occ);
    }

    Structure::try_new_full(
        lattice,
        site_occupancies,
        frac_coords,
        pbc,
        0.0,
        HashMap::new(),
    )
}

/// Parse a single OPTIMADE JSON structure.
///
/// Accepts either a bare structure resource (`{"type": "structures", ...}`)
/// or a list response (`{"data": [...]}`), in which case the first entry is used.
///
/// # Arguments
///
/// * `json` - JSON string containing an OPTIMADE structure
///
/// # Returns
///
/// The parsed `Structure`, or an error if parsing fails.
///
/// # Example
///
/// ```rust,ignore
/// let json = r#"{"type":"structures","id":"si","attributes":{...}}"#;
/// let structure = parse_optimade_json(json)?;
/// ```
pub fn parse_optimade_json(json: &str) -> Result<Structure> {
    let val: serde_json::Value =
        serde_json::from_str(json).map_err(|err| FerroxError::JsonError {
            path: "optimade".to_string(),
            reason: err.to_string(),
        })?;
    parse_optimade_from_value(val)
}

/// Parse an OPTIMADE structure from a pre-parsed serde Value.
pub(super) fn parse_optimade_from_value(val: serde_json::Value) -> Result<Structure> {
    // If it's a list response, take the first entry
    let resource_val = if let Some(data) = val.get("data") {
        if let Some(arr) = data.as_array() {
            arr.first()
                .ok_or_else(|| FerroxError::ParseError {
                    path: "optimade".to_string(),
                    reason: "OPTIMADE list response has empty 'data' array".to_string(),
                })?
                .clone()
        } else {
            data.clone()
        }
    } else {
        val
    };

    let resource: OptimadeResource =
        serde_json::from_value(resource_val).map_err(|err| FerroxError::JsonError {
            path: "optimade".to_string(),
            reason: format!("Failed to deserialize OPTIMADE resource: {err}"),
        })?;

    parse_optimade_resource(&resource)
}

/// Parse an OPTIMADE list response containing multiple structures.
///
/// Expects `{"data": [...]}` wrapping. Each entry is parsed independently;
/// individual parse failures are returned as `Err` entries in the result vec.
///
/// # Arguments
///
/// * `json` - JSON string containing an OPTIMADE list response
///
/// # Returns
///
/// A vector of parse results, one per entry in `data`.
pub fn parse_optimade_json_list(json: &str) -> Result<Vec<Result<Structure>>> {
    let list: OptimadeListResponse =
        serde_json::from_str(json).map_err(|err| FerroxError::JsonError {
            path: "optimade".to_string(),
            reason: format!("Failed to parse OPTIMADE list response: {err}"),
        })?;

    Ok(list
        .data
        .into_iter()
        .map(|entry| {
            let resource: OptimadeResource =
                serde_json::from_value(entry).map_err(|err| FerroxError::JsonError {
                    path: "optimade".to_string(),
                    reason: format!("Failed to deserialize OPTIMADE entry: {err}"),
                })?;
            parse_optimade_resource(&resource)
        })
        .collect())
}
