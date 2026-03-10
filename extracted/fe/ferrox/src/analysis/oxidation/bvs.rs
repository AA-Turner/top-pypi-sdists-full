// === Bond Valence Sum Calculation ===

use super::BV_SOFTNESS;
use super::utils::{get_bv_params_for_element, is_electronegative};
use crate::element::Element;

/// Calculate bond valence contribution from a single bond.
///
/// Uses O'Keeffe & Brese formula:
/// ```text
/// R = r1 + r2 - r1*r2*(sqrt(c1) - sqrt(c2))^2 / (c1*r1 + c2*r2)
/// vij = exp((R - distance) / BV_SOFTNESS)
/// ```
///
/// Returns `0.0` if neither element is electronegative, if both elements
/// are the same, or if either element is missing from the BV parameters table.
/// Returns the signed bond valence contribution otherwise.
pub fn calculate_bond_valence(
    element1: Element,
    element2: Element,
    distance: f64,
    scale_factor: f64,
) -> f64 {
    // BV only contributes if at least one element is electronegative
    if !is_electronegative(element1) && !is_electronegative(element2) {
        return 0.0;
    }

    // Same element doesn't contribute
    if element1 == element2 {
        return 0.0;
    }

    // Return 0.0 if BV params are missing for either element
    let params1 = match get_bv_params_for_element(element1) {
        Some(p) => p,
        None => return 0.0,
    };
    let params2 = match get_bv_params_for_element(element2) {
        Some(p) => p,
        None => return 0.0,
    };

    let r1 = params1.r;
    let r2 = params2.r;
    let c1 = params1.c;
    let c2 = params2.c;

    // O'Keeffe & Brese formula for ideal bond length
    let sqrt_c1 = c1.sqrt();
    let sqrt_c2 = c2.sqrt();
    let r_ideal = r1 + r2 - r1 * r2 * (sqrt_c1 - sqrt_c2).powi(2) / (c1 * r1 + c2 * r2);

    // Bond valence
    let vij = ((r_ideal - distance * scale_factor) / BV_SOFTNESS).exp();

    // Sign based on electronegativity (positive if element1 is more electropositive)
    let en1 = element1.electronegativity().unwrap_or(2.0);
    let en2 = element2.electronegativity().unwrap_or(2.0);
    let sign = if en1 < en2 {
        1.0
    } else if en1 > en2 {
        -1.0
    } else {
        // Equal electronegativity: no net contribution
        0.0
    };

    vij * sign
}

/// Neighbor information for BVS calculation.
#[derive(Debug, Clone)]
pub struct BvNeighbor {
    /// Element of the neighbor
    pub element: Element,
    /// Distance to the neighbor in Angstroms
    pub distance: f64,
    /// Occupancy (for disordered sites)
    pub occupancy: f64,
}

/// Calculate bond valence sum for a site given its neighbors.
///
/// # Arguments
///
/// * `site_element` - Element at the central site
/// * `neighbors` - List of neighbors with distances
/// * `scale_factor` - Distance scaling factor (default 1.015 for GGA, 1.0 for experimental)
///
/// # Returns
///
/// The bond valence sum. Missing BV parameters contribute 0.0 to the sum.
pub fn calculate_bv_sum(site_element: Element, neighbors: &[BvNeighbor], scale_factor: f64) -> f64 {
    neighbors
        .iter()
        .map(|neighbor| {
            let vij = calculate_bond_valence(
                site_element,
                neighbor.element,
                neighbor.distance,
                scale_factor,
            );
            vij * neighbor.occupancy
        })
        .sum()
}
