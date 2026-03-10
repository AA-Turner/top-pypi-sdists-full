use crate::element::Element;
use crate::error::{FerroxError, Result};
use crate::species::{SiteOccupancy, Species};
use crate::structure::Structure;
use nalgebra::Vector3;
use serde::Deserialize;
use std::collections::HashMap;
use std::path::Path;

use super::unified_api::{PymatgenSite, parse_species_entry};
use super::writers::format_extxyz_value;

// === Molecule Parsers ===

/// Represents a pymatgen Molecule JSON structure.
#[derive(Debug, Deserialize)]
#[allow(dead_code)] // Fields parsed for compatibility but not all used
struct PymatgenMolecule {
    #[serde(rename = "@module")]
    _module: Option<String>,
    #[serde(rename = "@class")]
    _class: Option<String>,
    sites: Vec<PymatgenSite>,
    #[serde(default)]
    charge: f64,
    #[serde(default)]
    properties: serde_json::Value,
}

/// Parse a molecule from pymatgen's Molecule JSON format.
///
/// Supports the format produced by `Molecule.as_dict()` in pymatgen.
///
/// # Arguments
///
/// * `json` - JSON string in pymatgen Molecule.as_dict() format
///
/// # Returns
///
/// The parsed molecule or an error if parsing fails.
///
/// # Example
///
/// ```rust,ignore
/// let json = r#"{
///     "sites": [
///         {"species": [{"element": "O"}], "xyz": [0, 0, 0]},
///         {"species": [{"element": "H"}], "xyz": [0.96, 0, 0]},
///         {"species": [{"element": "H"}], "xyz": [-0.24, 0.93, 0]}
///     ],
///     "charge": 0
/// }"#;
/// let molecule = parse_molecule_json(json)?;
/// ```
pub fn parse_molecule_json(json: &str) -> Result<Structure> {
    let parsed: PymatgenMolecule =
        serde_json::from_str(json).map_err(|e| FerroxError::JsonError {
            path: "inline".to_string(),
            reason: e.to_string(),
        })?;

    // Build site occupancies and coordinates
    let mut site_occupancies = Vec::with_capacity(parsed.sites.len());
    let mut cart_coords = Vec::with_capacity(parsed.sites.len());

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

        // Only merge species metadata for single-species sites
        if species_metadata.len() == 1 {
            for (key, val) in species_metadata.into_iter().next().unwrap() {
                site_props.insert(key, val);
            }
        }

        // Add site label if present
        if let Some(ref label) = site.label {
            site_props.insert("label".to_string(), serde_json::json!(label));
        }

        // Merge site properties from JSON
        if let serde_json::Value::Object(map) = &site.properties {
            for (key, val) in map {
                site_props.insert(key.clone(), val.clone());
            }
        }

        site_occupancies.push(SiteOccupancy::with_properties(species_vec, site_props));

        // Molecules require Cartesian (xyz) coordinates - fractional (abc) coordinates
        // don't make sense without a lattice to convert them
        let coords = site.xyz.ok_or_else(|| FerroxError::JsonError {
            path: "inline".to_string(),
            reason: format!(
                "Site {idx} missing 'xyz' (Cartesian coordinates required for molecules)"
            ),
        })?;
        cart_coords.push(Vector3::new(coords[0], coords[1], coords[2]));
    }

    // Extract molecule-level properties from JSON
    let properties: HashMap<String, serde_json::Value> = match parsed.properties {
        serde_json::Value::Object(map) => map.into_iter().collect(),
        _ => HashMap::new(),
    };

    Structure::try_new_molecule_from_occupancies(
        site_occupancies,
        cart_coords,
        parsed.charge,
        properties,
    )
}

/// Serialize a non-periodic structure (molecule) to pymatgen's Molecule JSON format.
///
/// Produces JSON compatible with pymatgen's `Molecule.from_dict()`.
///
/// # Arguments
///
/// * `structure` - The structure to serialize (should have `pbc = [false, false, false]`)
///
/// # Returns
///
/// JSON string in pymatgen Molecule format.
pub fn molecule_to_pymatgen_json(structure: &Structure) -> String {
    use serde_json::{Value, json};

    let cart_coords = structure.cart_coords();

    // Build sites with all species and their occupancies
    let sites: Vec<Value> = structure
        .site_occupancies
        .iter()
        .zip(cart_coords.iter())
        .map(|(site_occ, cart)| {
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

            // Extract label from properties if present
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

            json!({
                "species": species_list,
                "xyz": [cart.x, cart.y, cart.z],
                "label": label.unwrap_or(default_label),
                "properties": Value::Object(props)
            })
        })
        .collect();

    // Build molecule properties
    let properties: serde_json::Map<String, Value> =
        structure.properties.clone().into_iter().collect();

    // Build full molecule
    let result = json!({
        "@module": "pymatgen.core.structure",
        "@class": "Molecule",
        "charge": structure.charge,
        "sites": sites,
        "properties": properties
    });

    result.to_string()
}

/// Parse a molecule from a plain XYZ file (no lattice required).
///
/// This function parses standard XYZ format with Cartesian coordinates.
/// For files with lattice information, use [`parse_extxyz`] instead.
///
/// # Arguments
///
/// * `path` - Path to the XYZ file
///
/// # Returns
///
/// The parsed structure (non-periodic) or an error if parsing fails.
pub fn parse_xyz(path: &Path) -> Result<Structure> {
    let frames = parse_xyz_molecules(path)?;
    frames
        .into_iter()
        .next()
        .ok_or_else(|| FerroxError::EmptyFile {
            path: path.display().to_string(),
        })?
}

/// Parse a molecule from XYZ content string.
///
/// # Arguments
///
/// * `content` - XYZ file content as string
///
/// # Returns
///
/// The parsed structure (non-periodic) or an error if parsing fails.
pub fn parse_xyz_str(content: &str) -> Result<Structure> {
    frame_to_molecule(content, Path::new("inline"))
}

/// Parse all frames from an XYZ file as molecules.
///
/// Returns a vector of molecules for all frames in the file.
///
/// # Arguments
///
/// * `path` - Path to the XYZ file
///
/// # Returns
///
/// Vector of `Result<Structure>` (non-periodic) for each frame.
pub fn parse_xyz_molecules(path: &Path) -> Result<Vec<Result<Structure>>> {
    let path_str = path.to_string_lossy().to_string();
    let frames = extxyz::read_xyz_frames(&path_str, 0..).map_err(|e| FerroxError::ParseError {
        path: path.display().to_string(),
        reason: format!("XYZ read error: {e}"),
    })?;

    Ok(frames
        .map(|frame| frame_to_molecule(&frame, path))
        .collect())
}

pub(super) fn frame_to_molecule(frame: &str, path: &Path) -> Result<Structure> {
    let atoms = extxyz::RawAtoms::parse_from(frame).map_err(|e| FerroxError::ParseError {
        path: path.display().to_string(),
        reason: format!("XYZ parse error: {e}"),
    })?;

    // Try to parse comment line for properties (but NOT lattice - this is for molecules)
    // Plain XYZ comments (like "Water" or "Methane") won't parse as extXYZ info - that's OK
    let info: extxyz::Info = atoms.comment.parse().unwrap_or_default();

    // Parse species and coordinates
    let mut species = Vec::with_capacity(atoms.atoms.len());
    let mut cart_coords = Vec::with_capacity(atoms.atoms.len());

    for atom in &atoms.atoms {
        let element =
            Element::from_symbol(atom.element).ok_or_else(|| FerroxError::ParseError {
                path: path.display().to_string(),
                reason: format!("Unknown element symbol: {}", atom.element),
            })?;
        species.push(Species::neutral(element));
        cart_coords.push(Vector3::new(
            atom.position[0],
            atom.position[1],
            atom.position[2],
        ));
    }

    // Extract properties (energy, charge, etc.)
    let mut properties = HashMap::new();
    let mut charge = 0.0;

    if let Some(energy_value) = info.get("energy")
        && let Some(energy) = energy_value.as_f64()
    {
        properties.insert("energy".to_string(), serde_json::json!(energy));
    }

    if let Some(charge_value) = info.get("charge")
        && let Some(ch) = charge_value.as_f64()
    {
        charge = ch;
    }

    // Store other info as properties (exclude structure-specific and already-handled keys)
    let skip_keys = ["Lattice", "pbc", "energy", "charge", "Properties"];
    for (key, value) in info.raw_map().iter() {
        if !skip_keys.contains(&key.as_str()) {
            properties.insert(key.to_string(), value.clone());
        }
    }

    Structure::try_new_molecule(species, cart_coords, charge, properties)
}

/// Convert a non-periodic structure (molecule) to plain XYZ format string.
///
/// # Arguments
///
/// * `structure` - The structure to serialize (should have `pbc = [false, false, false]`)
/// * `comment` - Optional comment (defaults to formula)
///
/// # Returns
///
/// XYZ format string.
pub fn molecule_to_xyz(structure: &Structure, comment: Option<&str>) -> String {
    let mut lines = vec![structure.num_sites().to_string()];

    // Comment line (second line)
    let comment_str = comment
        .map(|c| c.to_string())
        .unwrap_or_else(|| structure.composition().reduced_formula());
    lines.push(comment_str);

    // Atom lines: Element X Y Z
    let cart_coords = structure.cart_coords();
    for (site_occ, cart) in structure.site_occupancies.iter().zip(cart_coords.iter()) {
        let symbol = site_occ.dominant_species().element.symbol();
        lines.push(format!(
            "{} {:20.16} {:20.16} {:20.16}",
            symbol, cart.x, cart.y, cart.z
        ));
    }

    lines.join("\n") + "\n"
}

/// Convert a non-periodic structure (molecule) to extXYZ format string with properties.
///
/// This produces an extXYZ file but without lattice information,
/// suitable for molecular data with attached properties.
///
/// # Arguments
///
/// * `structure` - The structure to serialize (should have `pbc = [false, false, false]`)
/// * `properties` - Optional additional properties for the comment line
///
/// # Returns
///
/// extXYZ format string (without lattice).
pub fn molecule_to_extxyz(
    structure: &Structure,
    properties: Option<&HashMap<String, serde_json::Value>>,
) -> String {
    // Line 1: Number of atoms
    let mut lines = vec![structure.num_sites().to_string()];

    // Line 2: Comment with properties (no lattice for molecules)
    // Format: pbc="F F F" [other properties]
    let mut comment_parts = vec!["pbc=\"F F F\"".to_string()];

    // Add charge if non-zero
    if structure.charge.abs() > 1e-10 {
        comment_parts.push(format!("charge={}", structure.charge));
    }

    // Add molecule properties and additional properties
    let all_props = structure
        .properties
        .iter()
        .chain(properties.into_iter().flatten());
    for (key, value) in all_props {
        if key != "pbc"
            && key != "charge"
            && let Some(value_str) = format_extxyz_value(value)
        {
            comment_parts.push(format!("{key}={value_str}"));
        }
    }

    lines.push(comment_parts.join(" "));

    // Atom lines: Element X Y Z (Cartesian coordinates)
    let cart_coords = structure.cart_coords();
    for (site_occ, cart) in structure.site_occupancies.iter().zip(cart_coords.iter()) {
        let symbol = site_occ.dominant_species().element.symbol();
        lines.push(format!(
            "{} {:20.16} {:20.16} {:20.16}",
            symbol, cart.x, cart.y, cart.z
        ));
    }

    lines.join("\n") + "\n"
}

/// Write a non-periodic structure (molecule) to an XYZ file.
///
/// # Arguments
///
/// * `structure` - The structure to write (should have `pbc = [false, false, false]`)
/// * `path` - Path to the output file
/// * `comment` - Optional comment line
///
/// # Returns
///
/// Result indicating success or file I/O error.
pub fn write_xyz(structure: &Structure, path: &Path, comment: Option<&str>) -> Result<()> {
    let content = molecule_to_xyz(structure, comment);
    std::fs::write(path, content)?;
    Ok(())
}

/// Deprecated: Use `Structure` with `is_molecule()` instead.
///
/// This enum is kept for backward compatibility but will be removed in a future version.
/// Since `Structure` now has `pbc` and `charge` fields, it can represent both periodic
/// and non-periodic systems.
#[derive(Debug, Clone)]
#[deprecated(
    since = "0.1.0",
    note = "Use Structure with is_molecule() check instead"
)]
pub enum StructureOrMolecule {
    /// A periodic crystal structure with lattice
    Structure(Structure),
    /// A non-periodic structure (molecule) - internally just Structure with pbc=[false,false,false]
    Molecule(Structure),
}
