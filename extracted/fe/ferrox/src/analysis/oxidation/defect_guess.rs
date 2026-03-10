// === Defect Charge State Guessing ===

use super::lazy_data::get_icsd_oxi_prob;
use crate::defects::DefectType;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Result of charge state guessing for a defect.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChargeStateGuess {
    /// The predicted charge state.
    pub charge: i32,
    /// Probability/confidence of this charge state (0-1).
    pub probability: f64,
    /// Human-readable reasoning for this charge state.
    pub reasoning: String,
}

/// Get normalized oxidation state probabilities for an element from ICSD data.
///
/// Returns a vector of (oxidation_state, probability) pairs sorted by decreasing probability.
pub(crate) fn get_element_oxi_probs(symbol: &str) -> Vec<(i8, f64)> {
    let icsd_data = get_icsd_oxi_prob();
    let prefix = format!("{symbol}:");

    let probs: Vec<(i8, u32)> = icsd_data
        .iter()
        .filter(|(key, _)| key.starts_with(&prefix))
        .filter_map(|(key, &count)| {
            let oxi_str = key.strip_prefix(&prefix)?;
            let oxi: i8 = oxi_str.parse().ok()?;
            Some((oxi, count))
        })
        .collect();

    // Normalize to probabilities
    let total: u32 = probs.iter().map(|(_, count)| count).sum();
    if total == 0 {
        return vec![];
    }

    let mut normalized: Vec<(i8, f64)> = probs
        .iter()
        .map(|&(oxi, count)| (oxi, count as f64 / total as f64))
        .collect();

    // Sort by decreasing probability (unwrap_or handles NaN gracefully by treating as equal)
    normalized.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));

    normalized
}

/// Format an oxidation state with superscript notation.
pub(crate) fn format_oxi_state(oxi: i8) -> String {
    let abs_oxi = oxi.abs();
    let sign = if oxi > 0 {
        "+"
    } else if oxi < 0 {
        "-"
    } else {
        ""
    };
    if abs_oxi == 1 && oxi != 0 {
        format!("^{{{sign}}}")
    } else if oxi == 0 {
        String::new()
    } else {
        format!("^{{{abs_oxi}{sign}}}")
    }
}

/// Guess likely charge states for a point defect.
///
/// Uses ICSD oxidation state probabilities to predict which charge states
/// are most likely for a given defect based on the species involved.
///
/// # Arguments
///
/// * `defect_type` - Type of defect (Vacancy, Interstitial, Substitution, Antisite)
/// * `removed_species` - Element symbol removed (for Vacancy, Antisite)
/// * `added_species` - Element symbol added (for Interstitial, Substitution, Antisite)
/// * `original_species` - Original element (for Substitution)
/// * `max_charge` - Maximum absolute charge to consider (default: 4)
///
/// # Returns
///
/// Vector of `ChargeStateGuess` sorted by decreasing probability.
///
/// # Examples
///
/// ```rust,ignore
/// use ferrox::defects::DefectType;
/// use ferrox::analysis::oxidation::guess_defect_charge_states;
///
/// // Oxygen vacancy in oxide: O^{2-} removed => +2, +1, 0 likely
/// let charges = guess_defect_charge_states(
///     DefectType::Vacancy, Some("O"), None, None, 4
/// );
/// // Returns: [{charge: 2, prob: ~0.85}, {charge: 1, prob: ~0.10}, ...]
/// ```
pub fn guess_defect_charge_states(
    defect_type: DefectType,
    removed_species: Option<&str>,
    added_species: Option<&str>,
    original_species: Option<&str>,
    max_charge: i32,
) -> Vec<ChargeStateGuess> {
    let mut guesses: Vec<ChargeStateGuess> = Vec::new();

    match defect_type {
        DefectType::Vacancy => {
            // Vacancy: charge = -oxidation_state of removed species
            let Some(removed) = removed_species else {
                return vec![];
            };
            let oxi_probs = get_element_oxi_probs(removed);
            if oxi_probs.is_empty() {
                // No ICSD data; return neutral only
                return vec![ChargeStateGuess {
                    charge: 0,
                    probability: 1.0,
                    reasoning: format!("V_{{{removed}}}: no ICSD data, assuming neutral"),
                }];
            }

            for (oxi, prob) in oxi_probs {
                let charge = -(oxi as i32);
                if charge.abs() <= max_charge {
                    let oxi_fmt = format_oxi_state(oxi);
                    guesses.push(ChargeStateGuess {
                        charge,
                        probability: prob,
                        reasoning: format!("{removed}{oxi_fmt} vacancy => {charge:+}"),
                    });
                }
            }

            // Always include neutral with small probability if not already present
            if !guesses.iter().any(|guess| guess.charge == 0) {
                guesses.push(ChargeStateGuess {
                    charge: 0,
                    probability: 0.01,
                    reasoning: format!("V_{{{removed}}}^0: neutral defect"),
                });
            }
        }
        DefectType::Interstitial => {
            // Interstitial: charge = oxidation_state of added species
            let Some(added) = added_species else {
                return vec![];
            };
            let oxi_probs = get_element_oxi_probs(added);
            if oxi_probs.is_empty() {
                return vec![ChargeStateGuess {
                    charge: 0,
                    probability: 1.0,
                    reasoning: format!("{added}_i: no ICSD data, assuming neutral"),
                }];
            }

            for (oxi, prob) in oxi_probs {
                let charge = oxi as i32;
                if charge.abs() <= max_charge {
                    let oxi_fmt = format_oxi_state(oxi);
                    guesses.push(ChargeStateGuess {
                        charge,
                        probability: prob,
                        reasoning: format!("{added}{oxi_fmt} interstitial => {charge:+}"),
                    });
                }
            }

            // Always include neutral with small probability if not already present
            if !guesses.iter().any(|guess| guess.charge == 0) {
                guesses.push(ChargeStateGuess {
                    charge: 0,
                    probability: 0.01,
                    reasoning: format!("{added}_i^0: neutral defect"),
                });
            }
        }
        DefectType::Substitution => {
            // Substitution: charge = new_oxidation - original_oxidation
            let (Some(added), Some(original)) = (added_species, original_species) else {
                return vec![];
            };
            let added_oxi_probs = get_element_oxi_probs(added);
            let original_oxi_probs = get_element_oxi_probs(original);

            if added_oxi_probs.is_empty() || original_oxi_probs.is_empty() {
                return vec![ChargeStateGuess {
                    charge: 0,
                    probability: 1.0,
                    reasoning: format!("{added}_{{{original}}}: no ICSD data, assuming neutral"),
                }];
            }

            // Consider all combinations, weight by product of probabilities
            let mut charge_probs: HashMap<i32, (f64, String)> = HashMap::new();

            for &(added_oxi, added_prob) in &added_oxi_probs {
                for &(orig_oxi, orig_prob) in &original_oxi_probs {
                    let charge = (added_oxi as i32) - (orig_oxi as i32);
                    if charge.abs() <= max_charge {
                        let combined_prob = added_prob * orig_prob;
                        let added_fmt = format_oxi_state(added_oxi);
                        let orig_fmt = format_oxi_state(orig_oxi);
                        let reasoning = format!(
                            "{added}{added_fmt} on {original}{orig_fmt} site => {charge:+}"
                        );

                        charge_probs
                            .entry(charge)
                            .and_modify(|(prob, _)| *prob += combined_prob)
                            .or_insert((combined_prob, reasoning));
                    }
                }
            }

            guesses = charge_probs
                .into_iter()
                .map(|(charge, (prob, reasoning))| ChargeStateGuess {
                    charge,
                    probability: prob,
                    reasoning,
                })
                .collect();

            // Always include neutral with small probability if not already present
            if !guesses.iter().any(|guess| guess.charge == 0) {
                guesses.push(ChargeStateGuess {
                    charge: 0,
                    probability: 0.01,
                    reasoning: format!("{added}_{{{original}}}^0: neutral defect"),
                });
            }
        }
        DefectType::Antisite => {
            // Antisite: effectively two substitutions, charge = (A_oxi - B_oxi) + (B_oxi - A_oxi) = 0
            // But individual sites can have different oxidation states
            let (Some(added), Some(removed)) = (added_species, removed_species) else {
                return vec![];
            };
            let added_oxi_probs = get_element_oxi_probs(added);
            let removed_oxi_probs = get_element_oxi_probs(removed);

            if added_oxi_probs.is_empty() || removed_oxi_probs.is_empty() {
                return vec![ChargeStateGuess {
                    charge: 0,
                    probability: 1.0,
                    reasoning: format!("{added}_{{{removed}}}: no ICSD data, assuming neutral"),
                }];
            }

            // For antisite pairs, consider charge as difference in oxidation states
            // between the two swapped atoms at their new sites
            let mut charge_probs: HashMap<i32, (f64, String)> = HashMap::new();

            for &(added_oxi, added_prob) in &added_oxi_probs {
                for &(removed_oxi, removed_prob) in &removed_oxi_probs {
                    // Defect charge = (new species oxi) - (expected oxi at site)
                    // e.g., Na(+1) on Cl(-1) site: charge = +1 - (-1) = +2
                    let charge = (added_oxi as i32) - (removed_oxi as i32);
                    if charge.abs() <= max_charge {
                        let combined_prob = added_prob * removed_prob;
                        let added_fmt = format_oxi_state(added_oxi);
                        let removed_fmt = format_oxi_state(removed_oxi);
                        let reasoning = format!(
                            "{removed}{removed_fmt} <-> {added}{added_fmt} antisite => {charge:+}"
                        );

                        charge_probs
                            .entry(charge)
                            .and_modify(|(prob, _)| *prob += combined_prob)
                            .or_insert((combined_prob, reasoning));
                    }
                }
            }

            guesses = charge_probs
                .into_iter()
                .map(|(charge, (prob, reasoning))| ChargeStateGuess {
                    charge,
                    probability: prob,
                    reasoning,
                })
                .collect();

            // Always include neutral with small probability if not already present
            if !guesses.iter().any(|guess| guess.charge == 0) {
                guesses.push(ChargeStateGuess {
                    charge: 0,
                    probability: 0.01,
                    reasoning: format!("{added}_{{{removed}}} antisite: neutral defect"),
                });
            }
        }
    }

    // Normalize probabilities so they sum to 1
    let total_prob: f64 = guesses.iter().map(|guess| guess.probability).sum();
    if total_prob > 0.0 {
        for guess in &mut guesses {
            guess.probability /= total_prob;
        }
    }

    // Sort by probability descending (unwrap_or handles NaN gracefully by treating as equal)
    guesses.sort_by(|a, b| {
        b.probability
            .partial_cmp(&a.probability)
            .unwrap_or(std::cmp::Ordering::Equal)
    });

    guesses
}

/// Guess charge states for multiple defects at once.
///
/// Convenience wrapper for batch processing of defects.
///
/// # Arguments
///
/// * `defects` - Slice of tuples: (defect_type, removed_species, added_species, original_species)
/// * `max_charge` - Maximum absolute charge to consider
///
/// # Returns
///
/// Vector of charge state guess vectors, one per defect.
#[allow(clippy::type_complexity)]
pub fn guess_defect_charge_states_batch(
    defects: &[(DefectType, Option<&str>, Option<&str>, Option<&str>)],
    max_charge: i32,
) -> Vec<Vec<ChargeStateGuess>> {
    defects
        .iter()
        .map(|(defect_type, removed, added, original)| {
            guess_defect_charge_states(*defect_type, *removed, *added, *original, max_charge)
        })
        .collect()
}
