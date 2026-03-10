use super::{DefectSupercellConfig, DefectType, find_defect_supercell, find_voronoi_interstitials};
use crate::analysis::oxidation::{ChargeStateGuess, guess_defect_charge_states};
use crate::error::Result;
use crate::structure::{Structure, WyckoffSite};
use nalgebra::Vector3;
use serde::{Deserialize, Serialize};
use std::collections::HashSet;

// === DefectEntry and Generator ===

/// Complete information about a defect for JSON serialization.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DefectEntry {
    /// Name following doped convention (e.g., "v_O_4a", "Fe_on_Ni").
    pub name: String,
    /// Type of defect.
    pub defect_type: DefectType,
    /// Index of the defect site in the original structure (None for interstitials).
    pub site_idx: Option<usize>,
    /// Fractional coordinates of the defect site.
    pub frac_coords: Vector3<f64>,
    /// Element symbol of the new species (for interstitials/substitutions).
    pub species: Option<String>,
    /// Element symbol of the original species (for vacancies/substitutions).
    pub original_species: Option<String>,
    /// Wyckoff label of the site.
    pub wyckoff: Option<String>,
    /// Site symmetry (point group).
    pub site_symmetry: Option<String>,
    /// Predicted charge states with probabilities.
    pub charge_states: Vec<ChargeStateGuess>,
    /// Number of symmetry-equivalent sites.
    pub equivalent_sites: usize,
}

/// Configuration for the defects generator.
#[derive(Debug, Clone)]
pub struct DefectsGeneratorConfig {
    /// Elements to consider as substitutional dopants.
    pub extrinsic: Vec<String>,
    /// Whether to generate vacancies.
    pub include_vacancies: bool,
    /// Whether to generate substitutions.
    pub include_substitutions: bool,
    /// Whether to generate interstitials.
    pub include_interstitials: bool,
    /// Whether to generate antisites.
    pub include_antisites: bool,
    /// Minimum image distance for supercell (Å).
    pub supercell_min_dist: f64,
    /// Maximum atoms in supercell.
    pub supercell_max_atoms: usize,
    /// Minimum distance for interstitial sites (Å).
    pub interstitial_min_dist: Option<f64>,
    /// Symmetry precision for site equivalence.
    pub symprec: f64,
    /// Maximum charge state magnitude.
    pub max_charge: i32,
}

impl Default for DefectsGeneratorConfig {
    fn default() -> Self {
        Self {
            extrinsic: vec![],
            include_vacancies: true,
            include_substitutions: true,
            include_interstitials: true,
            include_antisites: true,
            supercell_min_dist: 10.0,
            supercell_max_atoms: 200,
            interstitial_min_dist: None,
            symprec: 0.01,
            max_charge: 4,
        }
    }
}

/// Result of the defects generator.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DefectsGeneratorResult {
    /// Supercell transformation matrix.
    pub supercell_matrix: [[i32; 3]; 3],
    /// All generated vacancy defects.
    pub vacancies: Vec<DefectEntry>,
    /// All generated substitution defects.
    pub substitutions: Vec<DefectEntry>,
    /// All generated interstitial defects.
    pub interstitials: Vec<DefectEntry>,
    /// All generated antisite defects.
    pub antisites: Vec<DefectEntry>,
    /// Space group of the structure.
    pub spacegroup: Option<String>,
    /// Total number of unique defects.
    pub n_defects: usize,
}

/// Generate all point defects for a structure.
///
/// This is the main workflow function that mirrors doped's DefectsGenerator.
/// It analyzes the structure's symmetry, finds unique sites, and generates
/// all requested defect types with charge state predictions.
///
/// # Arguments
///
/// * `structure` - The primitive/conventional cell to generate defects for
/// * `config` - Configuration options
///
/// # Returns
///
/// A `DefectsGeneratorResult` containing all generated defects organized by type.
pub fn generate_all_defects(
    structure: &Structure,
    config: &DefectsGeneratorConfig,
) -> Result<DefectsGeneratorResult> {
    // Get symmetry info including Wyckoff sites
    let wyckoff_sites = structure.get_wyckoff_sites(config.symprec).ok();

    // Get space group if available
    let spacegroup = structure
        .get_symmetry_dataset(config.symprec)
        .ok()
        .map(|ds| ds.hm_symbol.clone());

    // Find unique sites by Wyckoff position to avoid duplicate defects
    // Group site indices by their orbit (representative index)
    let unique_sites = find_unique_sites(structure, &wyckoff_sites);

    // Find supercell matrix for defect calculations
    let supercell_config = DefectSupercellConfig {
        min_distance: config.supercell_min_dist,
        max_atoms: config.supercell_max_atoms,
        cubic_preference: 0.5,
    };
    let supercell_matrix = find_defect_supercell(structure, &supercell_config)?;

    // Collect elements present in the structure
    let elements_in_structure: HashSet<String> = structure
        .site_occupancies
        .iter()
        .map(|occ| occ.dominant_species().element.symbol().to_string())
        .collect();

    // Generate defects
    let vacancies = if config.include_vacancies {
        generate_vacancies(structure, &unique_sites, config)
    } else {
        vec![]
    };

    let substitutions = if config.include_substitutions {
        generate_substitutions(structure, &unique_sites, config)
    } else {
        vec![]
    };

    let interstitials = if config.include_interstitials {
        generate_interstitials(structure, config)
    } else {
        vec![]
    };

    let antisites = if config.include_antisites && elements_in_structure.len() >= 2 {
        generate_antisites(structure, &unique_sites, config)
    } else {
        vec![]
    };

    let n_defects = vacancies.len() + substitutions.len() + interstitials.len() + antisites.len();

    Ok(DefectsGeneratorResult {
        supercell_matrix,
        vacancies,
        substitutions,
        interstitials,
        antisites,
        spacegroup,
        n_defects,
    })
}

/// Information about a unique site in the structure.
#[derive(Debug, Clone)]
struct UniqueSite {
    /// Index of a representative site in this equivalence class.
    representative_idx: usize,
    /// Element at this site.
    element: String,
    /// Wyckoff information if available.
    wyckoff: Option<WyckoffSite>,
    /// Number of equivalent sites.
    multiplicity: usize,
}

/// Find unique sites grouped by Wyckoff position.
fn find_unique_sites(
    structure: &Structure,
    wyckoff_sites: &Option<Vec<WyckoffSite>>,
) -> Vec<UniqueSite> {
    let mut unique_sites: Vec<UniqueSite> = Vec::new();

    if let Some(wyckoffs) = wyckoff_sites {
        // Group sites by Wyckoff label and element
        let mut seen: HashSet<(String, String)> = HashSet::new();

        for (idx, wyckoff) in wyckoffs.iter().enumerate() {
            let element = structure.site_occupancies[idx]
                .dominant_species()
                .element
                .symbol()
                .to_string();
            let key = (wyckoff.label.clone(), element.clone());

            if seen.insert(key) {
                unique_sites.push(UniqueSite {
                    representative_idx: idx,
                    element,
                    wyckoff: Some(wyckoff.clone()),
                    multiplicity: wyckoff.multiplicity,
                });
            }
        }
    } else {
        // No symmetry info: treat every site as unique (don't collapse by element)
        for (idx, occ) in structure.site_occupancies.iter().enumerate() {
            let element = occ.dominant_species().element.symbol().to_string();
            unique_sites.push(UniqueSite {
                representative_idx: idx,
                element,
                wyckoff: None,
                multiplicity: 1,
            });
        }
    }

    unique_sites
}

/// Generate vacancy defects for unique sites.
fn generate_vacancies(
    structure: &Structure,
    unique_sites: &[UniqueSite],
    config: &DefectsGeneratorConfig,
) -> Vec<DefectEntry> {
    let mut vacancies: Vec<DefectEntry> = Vec::new();

    for site in unique_sites {
        let frac_coords = structure.frac_coords[site.representative_idx];
        let wyckoff_label = site.wyckoff.as_ref().map(|wyk| wyk.label.clone());
        let site_symmetry = site.wyckoff.as_ref().map(|wyk| wyk.site_symmetry.clone());

        // Generate name following doped convention
        let name = match &wyckoff_label {
            Some(wyk) => format!("v_{}_{}", site.element, wyk),
            None => format!("v_{}", site.element),
        };

        // Get charge states for vacancy (removing the species)
        let charge_states = guess_defect_charge_states(
            DefectType::Vacancy,
            Some(&site.element),
            None,
            None,
            config.max_charge,
        );

        vacancies.push(DefectEntry {
            name,
            defect_type: DefectType::Vacancy,
            site_idx: Some(site.representative_idx),
            frac_coords,
            species: None,
            original_species: Some(site.element.clone()),
            wyckoff: wyckoff_label,
            site_symmetry,
            charge_states,
            equivalent_sites: site.multiplicity,
        });
    }

    vacancies
}

/// Generate substitution defects for unique sites.
fn generate_substitutions(
    structure: &Structure,
    unique_sites: &[UniqueSite],
    config: &DefectsGeneratorConfig,
) -> Vec<DefectEntry> {
    let mut substitutions: Vec<DefectEntry> = Vec::new();

    // If no extrinsic dopants specified, return empty
    if config.extrinsic.is_empty() {
        return substitutions;
    }

    for site in unique_sites {
        let frac_coords = structure.frac_coords[site.representative_idx];
        let wyckoff_label = site.wyckoff.as_ref().map(|wyk| wyk.label.clone());
        let site_symmetry = site.wyckoff.as_ref().map(|wyk| wyk.site_symmetry.clone());

        for dopant in &config.extrinsic {
            // Skip if dopant is the same as the host element
            if dopant == &site.element {
                continue;
            }

            // Generate name following doped convention
            let name = format!("{}_on_{}", dopant, site.element);

            // Get charge states for substitution
            let charge_states = guess_defect_charge_states(
                DefectType::Substitution,
                None,
                Some(dopant),
                Some(&site.element),
                config.max_charge,
            );

            substitutions.push(DefectEntry {
                name,
                defect_type: DefectType::Substitution,
                site_idx: Some(site.representative_idx),
                frac_coords,
                species: Some(dopant.clone()),
                original_species: Some(site.element.clone()),
                wyckoff: wyckoff_label.clone(),
                site_symmetry: site_symmetry.clone(),
                charge_states,
                equivalent_sites: site.multiplicity,
            });
        }
    }

    substitutions
}

/// Generate interstitial defects from Voronoi analysis.
fn generate_interstitials(
    structure: &Structure,
    config: &DefectsGeneratorConfig,
) -> Vec<DefectEntry> {
    let mut interstitials: Vec<DefectEntry> = Vec::new();

    // Find Voronoi interstitial sites
    let voronoi_sites =
        find_voronoi_interstitials(structure, config.interstitial_min_dist, config.symprec);

    // Collect elements to create interstitials for
    // Use both host elements and extrinsic dopants
    // Use Vec with sort/dedup instead of HashSet for deterministic iteration order
    let mut interstitial_species: Vec<String> = structure
        .site_occupancies
        .iter()
        .map(|occ| occ.dominant_species().element.symbol().to_string())
        .collect();
    for dopant in &config.extrinsic {
        interstitial_species.push(dopant.clone());
    }
    interstitial_species.sort();
    interstitial_species.dedup();

    for (site_idx, voronoi_site) in voronoi_sites.iter().enumerate() {
        for species in &interstitial_species {
            // Generate name with site type
            let site_type_str = voronoi_site.site_type.as_str();
            let name = if site_type_str != "other" {
                format!("{}_i_{}", species, site_type_str)
            } else {
                format!("{}_i_{}", species, site_idx)
            };

            // Get charge states for interstitial
            let charge_states = guess_defect_charge_states(
                DefectType::Interstitial,
                None,
                Some(species),
                None,
                config.max_charge,
            );

            interstitials.push(DefectEntry {
                name,
                defect_type: DefectType::Interstitial,
                site_idx: None,
                frac_coords: voronoi_site.frac_coords,
                species: Some(species.clone()),
                original_species: None,
                wyckoff: voronoi_site.wyckoff_label.clone(),
                site_symmetry: None,
                charge_states,
                equivalent_sites: voronoi_site.multiplicity,
            });
        }
    }

    interstitials
}

/// Generate antisite defects for structures with multiple elements.
fn generate_antisites(
    structure: &Structure,
    unique_sites: &[UniqueSite],
    config: &DefectsGeneratorConfig,
) -> Vec<DefectEntry> {
    let mut antisites: Vec<DefectEntry> = Vec::new();

    // Get all unique elements in the structure
    // Use Vec with sort/dedup instead of HashSet for deterministic iteration order
    let mut elements: Vec<String> = unique_sites
        .iter()
        .map(|site| site.element.clone())
        .collect();
    elements.sort();
    elements.dedup();

    // Need at least 2 elements for antisites
    if elements.len() < 2 {
        return antisites;
    }

    for site in unique_sites {
        let frac_coords = structure.frac_coords[site.representative_idx];
        let wyckoff_label = site.wyckoff.as_ref().map(|wyk| wyk.label.clone());
        let site_symmetry = site.wyckoff.as_ref().map(|wyk| wyk.site_symmetry.clone());

        // Generate antisite for each other element type
        for other_element in &elements {
            if other_element == &site.element {
                continue;
            }

            // Generate name: new_element on old_element site (e.g., "Fe_Ni")
            let name = format!("{}_{}", other_element, site.element);

            // Get charge states for antisite
            let charge_states = guess_defect_charge_states(
                DefectType::Antisite,
                Some(&site.element),
                Some(other_element),
                None,
                config.max_charge,
            );

            antisites.push(DefectEntry {
                name,
                defect_type: DefectType::Antisite,
                site_idx: Some(site.representative_idx),
                frac_coords,
                species: Some(other_element.clone()),
                original_species: Some(site.element.clone()),
                wyckoff: wyckoff_label.clone(),
                site_symmetry: site_symmetry.clone(),
                charge_states,
                equivalent_sites: site.multiplicity,
            });
        }
    }

    antisites
}
