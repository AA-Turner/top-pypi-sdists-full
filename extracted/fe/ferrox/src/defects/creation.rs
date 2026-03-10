use super::{DefectStructure, PointDefect};
use crate::error::{FerroxError, Result, check_site_bounds, check_sites_different};
use crate::pbc::wrap_frac_coords_pbc;
use crate::species::{SiteOccupancy, Species};
use crate::structure::Structure;
use nalgebra::Vector3;

// === Defect Creation Functions ===

/// Create a vacancy by removing an atom at the specified site index.
///
/// # Arguments
///
/// * `structure` - The original structure.
/// * `site_idx` - Index of the site to remove.
///
/// # Returns
///
/// A `DefectStructure` containing the structure with the vacancy and defect info.
///
/// # Errors
///
/// Returns an error if the site index is out of bounds.
pub fn create_vacancy(structure: &Structure, site_idx: usize) -> Result<DefectStructure> {
    check_site_bounds(site_idx, structure.num_sites(), "site_idx")?;

    // Get the original species and position before removal
    let original_species = *structure.site_occupancies[site_idx].dominant_species();
    let position = structure.frac_coords[site_idx];

    // Create new structure without the site
    let new_structure = structure.remove_sites(&[site_idx])?;

    let defect = PointDefect::vacancy(site_idx, position, original_species);

    Ok(DefectStructure {
        structure: new_structure,
        defect,
    })
}

/// Create a substitutional defect by replacing the species at a site.
///
/// # Arguments
///
/// * `structure` - The original structure.
/// * `site_idx` - Index of the site to substitute.
/// * `new_species` - The species to place at the site.
///
/// # Returns
///
/// A `DefectStructure` containing the structure with the substitution.
///
/// # Errors
///
/// Returns an error if the site index is out of bounds.
pub fn create_substitution(
    structure: &Structure,
    site_idx: usize,
    new_species: Species,
) -> Result<DefectStructure> {
    check_site_bounds(site_idx, structure.num_sites(), "site_idx")?;

    // Get the original species and position
    let original_species = *structure.site_occupancies[site_idx].dominant_species();
    let position = structure.frac_coords[site_idx];

    // Create new site occupancies with the substituted species
    let mut new_occupancies = structure.site_occupancies.clone();
    new_occupancies[site_idx] = SiteOccupancy::ordered(new_species);

    let new_structure = Structure::try_new_from_occupancies(
        structure.lattice.clone(),
        new_occupancies,
        structure.frac_coords.clone(),
    )?;

    let defect = PointDefect::substitution(site_idx, position, new_species, original_species);

    Ok(DefectStructure {
        structure: new_structure,
        defect,
    })
}

/// Create an antisite pair by swapping species at two sites.
///
/// # Arguments
///
/// * `structure` - The original structure.
/// * `site_a_idx` - Index of the first site.
/// * `site_b_idx` - Index of the second site.
///
/// # Returns
///
/// The structure with swapped species at the two sites.
///
/// # Errors
///
/// Returns an error if either site index is out of bounds or if the sites have
/// the same species (no antisite possible).
pub fn create_antisite_pair(
    structure: &Structure,
    site_a_idx: usize,
    site_b_idx: usize,
) -> Result<Structure> {
    let num_sites = structure.num_sites();
    check_site_bounds(site_a_idx, num_sites, "site_a_idx")?;
    check_site_bounds(site_b_idx, num_sites, "site_b_idx")?;
    check_sites_different(site_a_idx, site_b_idx)?;

    // Check that sites have different species (otherwise antisite is meaningless)
    let occ_a = &structure.site_occupancies[site_a_idx];
    let occ_b = &structure.site_occupancies[site_b_idx];
    if occ_a == occ_b {
        return Err(FerroxError::InvalidStructure {
            index: site_a_idx,
            reason: format!(
                "sites {} and {} have identical species, cannot create antisite",
                site_a_idx, site_b_idx
            ),
        });
    }

    // Swap site occupancies
    let mut new_occupancies = structure.site_occupancies.clone();
    new_occupancies.swap(site_a_idx, site_b_idx);

    Structure::try_new_from_occupancies(
        structure.lattice.clone(),
        new_occupancies,
        structure.frac_coords.clone(),
    )
}

/// Create an interstitial by adding an atom at a fractional position.
///
/// # Arguments
///
/// * `structure` - The original structure.
/// * `position` - Fractional coordinates for the interstitial.
/// * `species` - The species to add.
///
/// # Returns
///
/// A `DefectStructure` containing the structure with the interstitial.
pub fn create_interstitial(
    structure: &Structure,
    position: Vector3<f64>,
    species: Species,
) -> Result<DefectStructure> {
    // Append new site to the structure, wrapping coords only along periodic axes
    let wrapped_position = wrap_frac_coords_pbc(&position, structure.lattice.pbc);
    let mut new_occupancies = structure.site_occupancies.clone();
    let mut new_coords = structure.frac_coords.clone();

    new_occupancies.push(SiteOccupancy::ordered(species));
    new_coords.push(wrapped_position);

    let new_structure = Structure::try_new_from_occupancies(
        structure.lattice.clone(),
        new_occupancies,
        new_coords,
    )?;

    let defect = PointDefect::interstitial(wrapped_position, species);

    Ok(DefectStructure {
        structure: new_structure,
        defect,
    })
}
