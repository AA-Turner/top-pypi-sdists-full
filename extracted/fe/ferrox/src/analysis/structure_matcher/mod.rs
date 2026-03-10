//! Structure matching algorithm.
//!
//! This module provides `StructureMatcher` for comparing crystal structures,
//! implementing the same algorithm as pymatgen's StructureMatcher.

mod api_impl;
mod matching_impl;
mod preprocess_impl;

use crate::element::Element;
use crate::error::OnError;
use std::collections::HashMap;

// Constants for structure distance calculation
/// Penalty (squared distance) added for each unmatched source site
const UNMATCHED_SOURCE_PENALTY: f64 = 10.0;
/// Penalty (squared distance) added for each unmatched target site
const UNMATCHED_TARGET_PENALTY: f64 = 5.0;
/// Weight applied to composition (Jaccard) distance in combined metric
const COMPOSITION_WEIGHT: f64 = 5.0;
/// Distance returned when structures have completely disjoint element sets
const DISJOINT_COMPOSITION_DISTANCE: f64 = 11.0;
/// Maximum finite distance returned when comparing empty vs non-empty structure
const EMPTY_STRUCTURE_DISTANCE: f64 = 1e9;
/// Minimum lattice volume to avoid division by zero in normalization
const MIN_LATTICE_VOLUME: f64 = 1e-12;
/// Highest atomic number supported by `Element::from_atomic_number()` (includes pseudo-elements).
const MAX_SUPPORTED_ATOMIC_NUMBER: u8 = 121;

/// Type of comparator to use for species matching.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum ComparatorType {
    /// Exact species match (element + oxidation state).
    #[default]
    Species,
    /// Element-only matching (ignores oxidation state).
    Element,
}

/// Predefined element-to-class mappings for anonymous prototype matching.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AnonymousClassMapping {
    /// ACX mapping: A (anions), C (cations), X (halides).
    Acx,
    /// CEA mapping: C (alkali/alkaline), E (electropositive), A (anions).
    Cea,
    /// Metal vs non-metal mapping.
    MetalNonMetal,
}

/// Anonymous matching mode for `fit_anonymous`.
#[derive(Debug, Clone, Copy)]
pub enum AnonymousMatchMode<'a> {
    /// Original pymatgen-style anonymous matching via one-to-one element permutation.
    ElementPermutation,
    /// Class-based matching using one of the predefined mapping families.
    Predefined(AnonymousClassMapping),
    /// Class-based matching using a custom element -> class label mapping.
    Custom(&'a HashMap<Element, String>),
}

impl AnonymousClassMapping {
    /// Parse a mapping name from user input.
    ///
    /// Accepted values:
    /// - `ACX`
    /// - `CEA`
    /// - `Metal/Non-metal` (also `metal_nonmetal`, `metal_non_metal`)
    pub fn from_name(mapping_name: &str) -> Option<Self> {
        let normalized_name = mapping_name.trim().to_ascii_lowercase();
        match normalized_name.as_str() {
            "acx" => Some(Self::Acx),
            "cea" => Some(Self::Cea),
            "metal/non-metal" | "metal_nonmetal" | "metal_non_metal" => Some(Self::MetalNonMetal),
            _ => None,
        }
    }

    /// Return the class label for an element under this mapping.
    fn class_for_element(&self, element: Element) -> Option<&'static str> {
        match self {
            Self::Acx => match element {
                Element::Si
                | Element::Ge
                | Element::Sn
                | Element::Sb
                | Element::Bi
                | Element::S
                | Element::Se
                | Element::Te => Some("A"),
                Element::Al
                | Element::Ga
                | Element::In
                | Element::Sc
                | Element::Y
                | Element::Li
                | Element::Na
                | Element::K
                | Element::Rb
                | Element::Cs
                | Element::Mg
                | Element::Ca
                | Element::Sr
                | Element::Ba => Some("C"),
                Element::Cl | Element::Br | Element::I => Some("X"),
                _ => None,
            },
            Self::Cea => match element {
                Element::Si
                | Element::Ge
                | Element::Sn
                | Element::Sb
                | Element::Bi
                | Element::S
                | Element::Se
                | Element::Te => Some("A"),
                Element::Al | Element::Ga | Element::In | Element::Sc | Element::Y => Some("E"),
                Element::Li
                | Element::Na
                | Element::K
                | Element::Rb
                | Element::Cs
                | Element::Mg
                | Element::Ca
                | Element::Sr
                | Element::Ba => Some("C"),
                _ => None,
            },
            Self::MetalNonMetal => {
                if element.is_metal() {
                    Some("M")
                } else {
                    Some("X")
                }
            }
        }
    }
}

/// Configuration and state for structure matching.
#[derive(Debug, Clone)]
pub struct StructureMatcher {
    /// Fractional length tolerance for lattice vectors.
    pub latt_len_tol: f64,
    /// Site position tolerance (normalized).
    pub site_pos_tol: f64,
    /// Angle tolerance in degrees.
    pub angle_tol: f64,
    /// Whether to reduce to primitive cell first.
    pub primitive_cell: bool,
    /// Whether to scale volumes to match.
    pub scale: bool,
    /// Whether to attempt supercell matching.
    pub attempt_supercell: bool,
    /// The comparator type to use for species matching.
    pub comparator_type: ComparatorType,
    /// Error handling behavior.
    pub on_error: OnError,
}

impl Default for StructureMatcher {
    fn default() -> Self {
        Self {
            latt_len_tol: 0.2,
            site_pos_tol: 0.3,
            angle_tol: 5.0,
            // Match pymatgen's default: reduce to primitive cell before matching
            primitive_cell: true,
            scale: true,
            attempt_supercell: false,
            comparator_type: ComparatorType::Species,
            on_error: OnError::Skip,
        }
    }
}

#[cfg(test)]
mod tests;
