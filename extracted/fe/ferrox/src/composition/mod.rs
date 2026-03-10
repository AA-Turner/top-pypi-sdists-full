//! Chemical composition handling.
//!
//! This module provides the [`Composition`] type for representing chemical compositions
//! with support for formula parsing, reduced formulas, oxidation-state-aware [`Species`],
//! and fast hashing for deduplication.
//!
//! ```
//! use ferrox::composition::Composition;
//!
//! let comp = Composition::from_formula("Ca3(PO4)2").unwrap();
//! assert_eq!(comp.reduced_formula(), "Ca3P2O8");
//! assert_eq!(comp.num_atoms(), 13.0); // 3 + 2 + 8
//! assert_eq!(comp.chemical_system(), "Ca-O-P");
//! ```

use crate::species::Species;
use indexmap::IndexMap;
use regex::Regex;
use serde::{Deserialize, Serialize};
use std::sync::LazyLock;

mod helpers;
mod operator_impls;
mod traits;

mod r#impl;

pub use helpers::gcd_i64;
pub(crate) use helpers::{format_amount, gcd_float, hill_sort_key, parse_formula_recursive};

/// Tolerance for floating point comparisons.
pub(crate) const AMOUNT_TOLERANCE: f64 = 1e-8;

/// Quantize an amount to an integer for consistent Eq/Hash behavior.
/// Uses AMOUNT_TOLERANCE as the quantization step.
#[inline]
pub(crate) fn quantize_amount(amt: f64) -> i64 {
    (amt / AMOUNT_TOLERANCE).round() as i64
}

/// Helper for serde skip_serializing_if: returns true if value is false.
fn is_false(v: &bool) -> bool {
    !*v
}

/// Regex for parsing element-amount pairs in formulas.
static ELEMENT_AMOUNT_RE: LazyLock<Regex> = LazyLock::new(|| {
    Regex::new(r"([A-Z][a-z]*)(\d*\.?\d*)").expect("Invalid ELEMENT_AMOUNT_RE regex")
});

/// Regex for finding parenthesized groups with multipliers.
static PAREN_GROUP_RE: LazyLock<Regex> = LazyLock::new(|| {
    Regex::new(r"\(([^\(\)]+)\)\s*(\d*\.?\d*)").expect("Invalid PAREN_GROUP_RE regex")
});

/// A chemical composition mapping species to amounts.
///
/// # Examples
///
/// ```
/// use ferrox::composition::Composition;
/// use ferrox::element::Element;
///
/// let comp = Composition::from_elements([(Element::Fe, 2.0), (Element::O, 3.0)]);
/// assert_eq!(comp.reduced_formula(), "Fe2O3");
/// assert_eq!(comp.chemical_system(), "Fe-O");
/// ```
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Composition {
    /// Species and their amounts (preserved insertion order).
    species: IndexMap<Species, f64>,
    /// Whether to allow negative amounts (default: false).
    #[serde(default, skip_serializing_if = "is_false")]
    allow_negative: bool,
}

#[cfg(test)]
mod tests;
