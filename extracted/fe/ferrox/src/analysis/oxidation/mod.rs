//! Oxidation state guessing and bond valence analysis.
//!
//! This module provides two approaches for assigning oxidation states:
//!
//! 1. **Composition-based guessing**: Enumerate charge-balanced oxidation state
//!    combinations ranked by ICSD probability. Fast, doesn't need structure coordinates.
//!
//! 2. **BVS-based guessing**: Calculate Bond Valence Sums from actual bond distances
//!    and use Bayesian inference with ICSD priors. More accurate but requires neighbor info.
//!
//! ## Data Sources
//!
//! - ICSD occurrence probabilities for oxidation state ranking
//! - BVS statistics (mean, std) from ICSD for Gaussian likelihood
//! - O'Keeffe & Brese bond valence parameters (JACS 1991)

mod bvs;
mod composition_guess;
mod compressed_data;
mod data_structs;
mod defect_guess;
mod lazy_data;
mod probability;
mod utils;

pub use bvs::{BvNeighbor, calculate_bond_valence, calculate_bv_sum};
pub use composition_guess::{
    find_charge_balanced_assignment, get_candidate_oxi_states, oxi_state_guesses,
};
pub use data_structs::{BvParams, BvStats, OxiStateGuess};
pub use defect_guess::{
    ChargeStateGuess, guess_defect_charge_states, guess_defect_charge_states_batch,
};
pub use lazy_data::{get_bv_params, get_icsd_bv_stats, get_icsd_oxi_prob};
pub use probability::{calculate_oxi_probability, get_oxi_state_probabilities};
pub use utils::{
    ELECTRONEG_ELEMENTS, get_bv_params_for_element, get_bv_stats_for_species, get_oxi_probability,
    is_electronegative, species_key,
};

// Bond valence "softness" parameter (Brown & Altermatt, Acta Cryst. B41, 244, 1985)
const BV_SOFTNESS: f64 = 0.31;

/// Maximum permutations for charge-balanced enumeration to prevent combinatorial explosion.
pub const MAX_PERMUTATIONS: usize = 100_000;

/// Tolerance for detecting non-integer oxidation states (mixed-valence).
/// Values like 2.33 or 2.67 (from Fe3O4) deviate by 0.33 from the nearest integer,
/// which exceeds this threshold. Values within 0.25 of an integer are considered
/// representable as a single oxidation state.
pub const OXI_INT_TOLERANCE: f64 = 0.25;

#[cfg(test)]
mod tests;
