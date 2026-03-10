use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use crate::species::{SiteOccupancy, Species};
use crate::structure::Structure;
use nalgebra::Vector3;
use serde::Deserialize;
use std::collections::HashMap;
use std::path::Path;

use super::cif::parse_cif;
use super::extxyz::parse_extxyz;
use super::lammps::parse_lammps_dump;
use super::optimade::{is_optimade_value, parse_optimade_from_value, parse_optimade_json};
use super::poscar::parse_poscar;
use super::xdatcar::parse_xdatcar;

// === Unified API ===

/// Supported structure file formats.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StructureFormat {
    /// Pymatgen JSON format (`Structure.as_dict()`)
    PymatgenJson,
    /// VASP POSCAR/CONTCAR format
    Poscar,
    /// Extended XYZ format
    ExtXyz,
    /// Crystallographic Information File
    Cif,
    /// LAMMPS dump/trajectory format
    LammpsDump,
    /// VASP XDATCAR trajectory format
    Xdatcar,
    /// OPTIMADE JSON format (`.optimade.json`)
    Optimade,
}

impl StructureFormat {
    /// Detect format from file path (extension and filename).
    ///
    /// # Examples
    ///
    /// ```
    /// use std::path::Path;
    /// use ferrox::io::StructureFormat;
    ///
    /// assert_eq!(StructureFormat::from_path(Path::new("structure.json")), Some(StructureFormat::PymatgenJson));
    /// assert_eq!(StructureFormat::from_path(Path::new("POSCAR")), Some(StructureFormat::Poscar));
    /// assert_eq!(StructureFormat::from_path(Path::new("trajectory.xyz")), Some(StructureFormat::ExtXyz));
    /// assert_eq!(StructureFormat::from_path(Path::new("diamond.cif")), Some(StructureFormat::Cif));
    /// assert_eq!(StructureFormat::from_path(Path::new("dump.lammpstrj")), Some(StructureFormat::LammpsDump));
    /// assert_eq!(StructureFormat::from_path(Path::new("XDATCAR")), Some(StructureFormat::Xdatcar));
    /// ```
    pub fn from_path(path: &Path) -> Option<Self> {
        let name_str = path.file_name().and_then(|n| n.to_str()).unwrap_or("");
        let name_lower = name_str.to_lowercase();

        // Check for compound extensions (.lammpstrj, .lammpstrj.gz, .lmp.gz, .dump.gz)
        for suffix in [".lammpstrj", ".lammpstrj.gz", ".lmp.gz", ".dump.gz"] {
            if name_lower.ends_with(suffix) {
                return Some(Self::LammpsDump);
            }
        }

        // .optimade.json before generic .json
        if name_lower.ends_with(".optimade.json") {
            return Some(Self::Optimade);
        }

        // Check extension
        if let Some(ext) = path.extension().and_then(|e| e.to_str()) {
            let ext_lower = ext.to_lowercase();
            match ext_lower.as_str() {
                "json" => return Some(Self::PymatgenJson),
                "xyz" | "extxyz" => return Some(Self::ExtXyz),
                "cif" => return Some(Self::Cif),
                "vasp" => return Some(Self::Poscar),
                "lammpstrj" | "lmp" | "dump" => return Some(Self::LammpsDump),
                _ => {}
            }
        }

        // Check filename for XDATCAR (before POSCAR/CONTCAR since it's more specific)
        let name_upper = name_str.to_uppercase();
        if name_upper.starts_with("XDATCAR") {
            return Some(Self::Xdatcar);
        }

        // Check filename for POSCAR/CONTCAR
        if name_upper.starts_with("POSCAR") || name_upper.starts_with("CONTCAR") {
            return Some(Self::Poscar);
        }

        None
    }
}

/// Parse a structure from a file with automatic format detection.
///
/// The format is detected based on:
/// 1. File extension (`.json`, `.xyz`, `.cif`, `.vasp`, `.lammpstrj`, `.lmp`, `.dump`)
/// 2. Filename pattern (`POSCAR*`, `CONTCAR*`, `XDATCAR*`)
///
/// # Arguments
///
/// * `path` - Path to the structure file
///
/// # Returns
///
/// The parsed structure or an error if parsing fails.
///
/// # Example
///
/// ```rust,ignore
/// use ferrox::io::parse_structure;
/// use std::path::Path;
///
/// let structure = parse_structure(Path::new("structure.cif"))?;
/// ```
pub fn parse_structure(path: &Path) -> Result<Structure> {
    let format = StructureFormat::from_path(path).ok_or_else(|| FerroxError::UnknownFormat {
        path: path.display().to_string(),
    })?;

    match format {
        StructureFormat::PymatgenJson => parse_structure_file(path),
        StructureFormat::Poscar => parse_poscar(path),
        StructureFormat::ExtXyz => parse_extxyz(path),
        StructureFormat::Cif => parse_cif(path),
        StructureFormat::LammpsDump => parse_lammps_dump(path),
        StructureFormat::Xdatcar => parse_xdatcar(path),
        StructureFormat::Optimade => {
            let json = std::fs::read_to_string(path)?;
            parse_optimade_json(&json)
        }
    }
}

/// Represents a species entry in pymatgen JSON.
#[derive(Debug, Deserialize)]
#[allow(dead_code)] // Fields parsed for compatibility but not all used
pub(super) struct PymatgenSpecies {
    element: String,
    #[serde(default = "default_occu")]
    occu: f64,
    #[serde(default, deserialize_with = "deserialize_oxidation_state")]
    oxidation_state: Option<i32>,
}

/// Deserialize oxidation_state from either integer or float.
///
/// Validates that the value fits within i32 range before conversion to avoid
/// undefined behavior from overflow.
fn deserialize_oxidation_state<'de, D>(
    deserializer: D,
) -> std::result::Result<Option<i32>, D::Error>
where
    D: serde::Deserializer<'de>,
{
    use serde::de::Error;

    let value: Option<serde_json::Value> = Option::deserialize(deserializer)?;
    match value {
        None => Ok(None),
        Some(serde_json::Value::Null) => Ok(None),
        Some(serde_json::Value::Number(n)) => {
            if let Some(int_val) = n.as_i64() {
                // Check i64 fits in i32 before converting
                if int_val < i32::MIN as i64 || int_val > i32::MAX as i64 {
                    return Err(D::Error::custom(format!(
                        "oxidation_state {int_val} overflows i32 range"
                    )));
                }
                Ok(Some(int_val as i32))
            } else if let Some(float_val) = n.as_f64() {
                // Check float is finite and within i32 range before converting
                let rounded = float_val.round();
                if !rounded.is_finite() || rounded < i32::MIN as f64 || rounded > i32::MAX as f64 {
                    return Err(D::Error::custom(format!(
                        "oxidation_state {float_val} overflows i32 range"
                    )));
                }
                Ok(Some(rounded as i32))
            } else {
                Err(D::Error::custom("oxidation_state must be a number"))
            }
        }
        Some(other) => Err(D::Error::custom(format!(
            "oxidation_state must be a number, got {:?}",
            other
        ))),
    }
}

fn default_occu() -> f64 {
    1.0
}

/// Parse a species entry from pymatgen JSON, returning the Species with occupancy and metadata.
///
/// Handles element symbol normalization, oxidation state validation/conflict detection,
/// and occupancy validation.
pub(super) fn parse_species_entry(
    sp_json: &PymatgenSpecies,
    site_idx: usize,
) -> Result<(Species, f64, HashMap<String, serde_json::Value>)> {
    // Use normalize_symbol for comprehensive element parsing
    let normalized =
        crate::element::normalize_symbol(&sp_json.element).map_err(|e| FerroxError::JsonError {
            path: "inline".to_string(),
            reason: format!("Invalid element symbol '{}': {}", sp_json.element, e),
        })?;

    // Validate oxidation state range BEFORE casting to i8 (to avoid silent truncation)
    if let Some(oxi) = sp_json.oxidation_state
        && (oxi < i8::MIN as i32 || oxi > i8::MAX as i32)
    {
        return Err(FerroxError::JsonError {
            path: "inline".to_string(),
            reason: format!("Oxidation state {oxi} out of range [-128, 127]"),
        });
    }

    // Check for oxidation state conflict (safe to cast now - range validated above)
    let json_oxi = sp_json.oxidation_state.map(|o| o as i8);
    let final_oxi = match (json_oxi, normalized.oxidation_state) {
        (Some(json), Some(sym)) if json != sym => {
            return Err(FerroxError::JsonError {
                path: "inline".to_string(),
                reason: format!(
                    "Conflicting oxidation states for '{}': symbol implies {}, but JSON has {}",
                    sp_json.element,
                    sym,
                    sp_json.oxidation_state.unwrap()
                ),
            });
        }
        (Some(json), _) => Some(json),
        (None, Some(sym)) => Some(sym),
        (None, None) => None,
    };

    let sp = Species::new(normalized.element, final_oxi);

    // Validate occupancy: must be finite and in range (0.0, 1.0]
    let occu = sp_json.occu;
    if !occu.is_finite() || occu <= 0.0 || occu > 1.0 {
        return Err(FerroxError::JsonError {
            path: "inline".to_string(),
            reason: format!(
                "Site {site_idx} species {} has invalid occupancy {occu} (must be in (0.0, 1.0])",
                sp_json.element
            ),
        });
    }

    Ok((sp, occu, normalized.metadata))
}

/// Represents a site in pymatgen JSON.
///
/// For structures, `abc` (fractional coords) is required.
/// For molecules, `xyz` (Cartesian coords) is used and `abc` may be absent.
#[derive(Debug, Deserialize)]
#[allow(dead_code)] // Fields parsed for compatibility but not all used
pub(super) struct PymatgenSite {
    pub(super) species: Vec<PymatgenSpecies>,
    /// Fractional coordinates (required for structures, optional for molecules)
    #[serde(default)]
    pub(super) abc: Option<[f64; 3]>,
    /// Cartesian coordinates (optional for structures, required for molecules)
    #[serde(default)]
    pub(super) xyz: Option<[f64; 3]>,
    #[serde(default)]
    pub(super) label: Option<String>,
    #[serde(default)]
    pub(super) properties: serde_json::Value,
}

/// Represents the lattice in pymatgen JSON.
#[derive(Debug, Deserialize)]
struct PymatgenLattice {
    matrix: [[f64; 3]; 3],
    #[serde(default = "default_pbc")]
    pbc: [bool; 3],
}

fn default_pbc() -> [bool; 3] {
    [true, true, true]
}

/// Represents a pymatgen Structure JSON.
#[derive(Debug, Deserialize)]
#[allow(dead_code)] // Fields parsed for compatibility but not all used
struct PymatgenStructure {
    #[serde(rename = "@module")]
    _module: Option<String>,
    #[serde(rename = "@class")]
    _class: Option<String>,
    lattice: PymatgenLattice,
    sites: Vec<PymatgenSite>,
    #[serde(default)]
    charge: Option<f64>,
    #[serde(default)]
    properties: serde_json::Value,
}

/// Parse a structure from pymatgen's JSON format.
///
/// Supports the format produced by `Structure.as_dict()` in pymatgen.
///
/// # Expanded disorder handling
///
/// Some databases store disordered structures in an "expanded" format where
/// each partial-occupancy species is a separate site at the same fractional
/// coordinates. For example, a site shared by K (0.06) and Ba (0.88) is stored
/// as two separate JSON sites at `[0, 0, 0]` rather than one site with two
/// species entries. This function detects co-located sites (within
/// `merge_tol` in fractional coordinates) and merges them into a single
/// `SiteOccupancy` with multiple species.
///
/// # Arguments
///
/// * `json` - JSON string in pymatgen Structure.as_dict() format
///
/// # Returns
///
/// The parsed structure or an error if parsing fails.
///
/// # Example
///
/// ```rust,ignore
/// let json = r#"{
///     "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
///     "sites": [{"species": [{"element": "Fe"}], "abc": [0,0,0]}]
/// }"#;
/// let structure = parse_structure_json(json)?;
/// ```
pub fn parse_structure_json(json: &str) -> Result<Structure> {
    // Parse JSON once, then sniff format from the Value to avoid double-parsing
    let val: serde_json::Value =
        serde_json::from_str(json).map_err(|err| FerroxError::JsonError {
            path: "inline".to_string(),
            reason: err.to_string(),
        })?;

    if is_optimade_value(&val) {
        return parse_optimade_from_value(val);
    }

    parse_pymatgen_from_value(val, 1e-6)
}

/// Like [`parse_structure_json`] but with a configurable tolerance for merging
/// co-located sites. Sites whose fractional coordinates differ by less than
/// `merge_tol` in all three dimensions are merged into a single disordered site.
///
/// Set `merge_tol` to `0.0` to disable merging entirely.
pub fn parse_structure_json_with_merge_tol(json: &str, merge_tol: f64) -> Result<Structure> {
    let val: serde_json::Value =
        serde_json::from_str(json).map_err(|e| FerroxError::JsonError {
            path: "inline".to_string(),
            reason: e.to_string(),
        })?;
    parse_pymatgen_from_value(val, merge_tol)
}

/// Parse a pymatgen JSON structure from a pre-parsed serde Value.
fn parse_pymatgen_from_value(val: serde_json::Value, merge_tol: f64) -> Result<Structure> {
    let parsed: PymatgenStructure =
        serde_json::from_value(val).map_err(|e| FerroxError::JsonError {
            path: "inline".to_string(),
            reason: e.to_string(),
        })?;

    // Build lattice from row-major matrix
    let mat = &parsed.lattice.matrix;
    let matrix = nalgebra::Matrix3::new(
        mat[0][0], mat[0][1], mat[0][2], mat[1][0], mat[1][1], mat[1][2], mat[2][0], mat[2][1],
        mat[2][2],
    );
    let mut lattice = Lattice::new(matrix);
    lattice.pbc = parsed.lattice.pbc;

    // Build site occupancies and coordinates (supports disordered sites)
    let mut site_occupancies = Vec::with_capacity(parsed.sites.len());
    let mut frac_coords = Vec::with_capacity(parsed.sites.len());

    for (idx, site) in parsed.sites.iter().enumerate() {
        if site.species.is_empty() {
            return Err(FerroxError::JsonError {
                path: "inline".to_string(),
                reason: format!("Site {idx} has no species"),
            });
        }

        // Parse all species with their occupancies using shared helper
        let mut species_vec = Vec::with_capacity(site.species.len());
        let mut site_props: HashMap<String, serde_json::Value> = HashMap::new();
        let mut species_metadata: Vec<HashMap<String, serde_json::Value>> =
            Vec::with_capacity(site.species.len());

        for sp_json in &site.species {
            let (sp, occu, metadata) = parse_species_entry(sp_json, idx)?;
            species_vec.push((sp, occu));
            species_metadata.push(metadata);
        }

        // Only merge species metadata for single-species sites (no conflict possible)
        // For multi-species sites, per-species metadata would be ambiguous at site level
        if species_metadata.len() == 1 {
            for (key, val) in species_metadata.into_iter().next().unwrap() {
                site_props.insert(key, val);
            }
        }

        // Add site label if present
        if let Some(ref label) = site.label {
            site_props.insert("label".to_string(), serde_json::json!(label));
        }

        // Merge site properties from JSON (takes precedence over normalization metadata)
        if let serde_json::Value::Object(map) = &site.properties {
            for (key, val) in map {
                site_props.insert(key.clone(), val.clone());
            }
        }

        site_occupancies.push(SiteOccupancy::with_properties(species_vec, site_props));

        // For structures, abc (fractional coords) is required
        let abc = site.abc.ok_or_else(|| FerroxError::JsonError {
            path: "inline".to_string(),
            reason: format!("Site {idx} missing 'abc' (fractional coordinates)"),
        })?;
        frac_coords.push(Vector3::new(abc[0], abc[1], abc[2]));
    }

    // Merge co-located sites: when multiple sites share the same fractional
    // coordinates (within tolerance), combine their species into a single
    // SiteOccupancy. This handles the "expanded disorder" format where partial
    // occupancies are stored as separate sites at identical positions rather
    // than as multi-species entries on a single site.
    let mut merged_occupancies: Vec<SiteOccupancy> = Vec::new();
    let mut merged_coords: Vec<Vector3<f64>> = Vec::new();

    // Minimum-image distance for fractional coordinates, handles wrapping
    // so coords outside [0, 1) (e.g. -0.1 or 1.5) are compared correctly
    let periodic_dist = |a: f64, b: f64| -> f64 {
        let diff = (a - b).rem_euclid(1.0);
        diff.min(1.0 - diff)
    };

    for (occ, coord) in site_occupancies.into_iter().zip(frac_coords.into_iter()) {
        // Check if this coordinate already exists in merged list (periodic-aware)
        let existing_idx = merged_coords.iter().position(|existing| {
            periodic_dist(existing.x, coord.x) < merge_tol
                && periodic_dist(existing.y, coord.y) < merge_tol
                && periodic_dist(existing.z, coord.z) < merge_tol
        });

        if let Some(idx) = existing_idx {
            // Merge species into existing site
            merged_occupancies[idx].merge_from(&occ);
        } else {
            merged_occupancies.push(occ);
            merged_coords.push(coord);
        }
    }

    let site_occupancies = merged_occupancies;
    let frac_coords = merged_coords;

    // Extract structure-level properties from JSON
    let properties: HashMap<String, serde_json::Value> = match parsed.properties {
        serde_json::Value::Object(map) => map.into_iter().collect(),
        _ => HashMap::new(),
    };

    // Extract charge (default 0.0 for structures)
    let charge = parsed.charge.unwrap_or(0.0);

    // Use pbc from lattice (defaults to [true, true, true] if not specified)
    let pbc = parsed.lattice.pbc;

    Structure::try_new_full(
        lattice,
        site_occupancies,
        frac_coords,
        pbc,
        charge,
        properties,
    )
}

/// Serialize a structure to pymatgen's JSON format.
///
/// Produces JSON compatible with pymatgen's `Structure.from_dict()`.
///
/// # Arguments
///
/// * `structure` - The structure to serialize
///
/// # Returns
///
/// JSON string in pymatgen format.
pub fn structure_to_pymatgen_json(structure: &Structure) -> String {
    use serde_json::{Value, json};

    // Build lattice
    let mat = structure.lattice.matrix();
    let lattice = json!({
        "matrix": [
            [mat[(0, 0)], mat[(0, 1)], mat[(0, 2)]],
            [mat[(1, 0)], mat[(1, 1)], mat[(1, 2)]],
            [mat[(2, 0)], mat[(2, 1)], mat[(2, 2)]]
        ],
        "pbc": structure.lattice.pbc
    });

    // Build sites with all species and their occupancies
    let cart_coords = structure.cart_coords();
    let sites: Vec<Value> = structure
        .site_occupancies
        .iter()
        .zip(structure.frac_coords.iter())
        .zip(cart_coords.iter())
        .map(|((site_occ, frac), cart)| {
            let species_list: Vec<Value> = site_occ
                .species
                .iter()
                .map(|(sp, occ)| {
                    let mut entry = json!({
                        "element": sp.element.symbol(),
                        "occu": occ
                    });
                    if let Some(oxi) = sp.oxidation_state {
                        entry["oxidation_state"] = json!(oxi);
                    }
                    entry
                })
                .collect();

            // Extract label from properties if present (pymatgen uses top-level label)
            let label = site_occ
                .properties
                .get("label")
                .and_then(|v| v.as_str())
                .map(|s| s.to_string());

            // Build site properties (excluding label which is at top level)
            let props: serde_json::Map<String, Value> = site_occ
                .properties
                .iter()
                .filter(|(k, _)| k.as_str() != "label")
                .map(|(k, v)| (k.clone(), v.clone()))
                .collect();

            // Generate default label from species symbols if not present
            let default_label: String = site_occ
                .species
                .iter()
                .map(|(sp, _)| sp.element.symbol())
                .collect::<Vec<_>>()
                .join(",");

            // Build site JSON with both fractional and Cartesian coords
            // Always include label and properties for JavaScript compatibility
            json!({
                "species": species_list,
                "abc": [frac.x, frac.y, frac.z],
                "xyz": [cart.x, cart.y, cart.z],
                "label": label.unwrap_or(default_label),
                "properties": Value::Object(props)
            })
        })
        .collect();

    // Build structure properties
    let properties: serde_json::Map<String, Value> =
        structure.properties.clone().into_iter().collect();

    // Build full structure
    let mut result = json!({
        "@module": "pymatgen.core.structure",
        "@class": "Structure",
        "lattice": lattice,
        "sites": sites,
        "properties": properties
    });

    // Include charge if non-zero
    if structure.charge.abs() > 1e-10 {
        result["charge"] = json!(structure.charge);
    }

    result.to_string()
}

/// Parse a structure from a JSON file.
///
/// # Arguments
///
/// * `path` - Path to the JSON file
///
/// # Returns
///
/// The parsed structure or an error if parsing/reading fails.
pub fn parse_structure_file(path: &Path) -> Result<Structure> {
    let json = std::fs::read_to_string(path)?;
    parse_structure_json(&json).map_err(|e| {
        if let FerroxError::JsonError { reason, .. } = e {
            FerroxError::JsonError {
                path: path.display().to_string(),
                reason,
            }
        } else {
            e
        }
    })
}

/// Parse multiple structures from JSON files matching a glob pattern.
///
/// # Arguments
///
/// * `pattern` - Glob pattern (e.g., "structures/*.json")
///
/// # Returns
///
/// Vector of (path, structure) pairs, or error if any file fails to parse.
/// File access errors (permissions, broken symlinks) during glob iteration
/// are logged as warnings but do not cause the function to fail.
pub fn parse_structures_glob(pattern: &str) -> Result<Vec<(String, Structure)>> {
    let paths: Vec<_> = glob::glob(pattern)
        .map_err(|e| FerroxError::JsonError {
            path: pattern.to_string(),
            reason: format!("Invalid glob pattern: {e}"),
        })?
        .filter_map(|result| match result {
            Ok(path) => Some(path),
            Err(err) => {
                // Log glob errors (permissions, broken symlinks, etc.) for debugging
                tracing::warn!("Glob iteration error: {err}");
                None
            }
        })
        .collect();

    let mut results = Vec::with_capacity(paths.len());
    for path in paths {
        let structure = parse_structure_file(&path)?;
        results.push((path.display().to_string(), structure));
    }

    Ok(results)
}

/// Serialize a structure to pymatgen JSON format.
///
/// Alias for [`structure_to_pymatgen_json`] for backwards compatibility.
#[inline]
pub fn structure_to_json(structure: &Structure) -> String {
    structure_to_pymatgen_json(structure)
}
