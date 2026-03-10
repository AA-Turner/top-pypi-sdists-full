// === Utility Functions ===

use super::data_structs::{BvParams, BvStats};
use super::lazy_data::{get_bv_params, get_icsd_bv_stats, get_icsd_oxi_prob};
use crate::element::Element;

/// Format species key for looking up in ICSD data maps.
///
/// Returns "Element:oxidation_state" (e.g., "Fe:3", "O:-2", "Fe:0").
pub fn species_key(element: Element, oxidation_state: i8) -> String {
    format!("{}:{}", element.symbol(), oxidation_state)
}

/// Get ICSD occurrence count for a species.
///
/// Returns None if species not in ICSD data.
pub fn get_oxi_probability(element: Element, oxidation_state: i8) -> Option<u32> {
    let key = species_key(element, oxidation_state);
    get_icsd_oxi_prob().get(&key).copied()
}

/// Get ICSD BVS statistics for a species.
///
/// Returns None if species not in ICSD data.
pub fn get_bv_stats_for_species(element: Element, oxidation_state: i8) -> Option<&'static BvStats> {
    let key = species_key(element, oxidation_state);
    get_icsd_bv_stats().get(&key)
}

/// Get BV parameters for an element.
///
/// Returns None if element not in BV parameters table.
pub fn get_bv_params_for_element(element: Element) -> Option<&'static BvParams> {
    get_bv_params().get(element.symbol())
}

/// List of electronegative elements from O'Keeffe & Brese.
/// BV sum only contributes when at least one atom is electronegative.
pub const ELECTRONEG_ELEMENTS: &[Element] = &[
    Element::H,
    Element::B,
    Element::C,
    Element::Si,
    Element::N,
    Element::P,
    Element::As,
    Element::Sb,
    Element::O,
    Element::S,
    Element::Se,
    Element::Te,
    Element::F,
    Element::Cl,
    Element::Br,
    Element::I,
];

/// Check if an element is electronegative (for BV calculation).
pub fn is_electronegative(element: Element) -> bool {
    ELECTRONEG_ELEMENTS.contains(&element)
}
