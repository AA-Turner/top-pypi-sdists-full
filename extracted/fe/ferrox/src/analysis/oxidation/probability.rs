// === Oxidation State Probability Calculation ===

use super::lazy_data::get_icsd_oxi_prob;
use super::utils::{get_bv_stats_for_species, get_oxi_probability};
use crate::element::Element;

/// Calculate posterior probability for an oxidation state given a BV sum.
///
/// Uses Bayesian approach:
/// ```text
/// P(oxi | BV) ∝ P(BV | oxi) × P(oxi)
/// ```
///
/// where P(BV | oxi) is Gaussian from ICSD statistics and P(oxi) is ICSD occurrence.
pub fn calculate_oxi_probability(element: Element, oxidation_state: i8, bv_sum: f64) -> f64 {
    // Get ICSD prior probability
    let prior = get_oxi_probability(element, oxidation_state).unwrap_or(0) as f64;
    if prior == 0.0 {
        return 0.0;
    }

    // Get BVS statistics for Gaussian likelihood
    let stats = match get_bv_stats_for_species(element, oxidation_state) {
        Some(s) if s.std > 0.0 => s,
        _ => return 0.0,
    };

    // Skip oxidation state 0 (neutral)
    if oxidation_state == 0 {
        return 0.0;
    }

    // Gaussian likelihood: P(BV | oxi) = exp(-(BV - μ)² / (2σ²)) / σ
    let likelihood = (-(bv_sum - stats.mean).powi(2) / (2.0 * stats.std.powi(2))).exp() / stats.std;

    // Posterior (unnormalized)
    prior * likelihood
}

/// Get all possible oxidation states for an element with their probabilities given a BV sum.
///
/// Returns a vector of (oxidation_state, probability) sorted by decreasing probability.
pub fn get_oxi_state_probabilities(element: Element, bv_sum: f64) -> Vec<(i8, f64)> {
    let icsd_data = get_icsd_oxi_prob();
    let prefix = format!("{}:", element.symbol());

    let mut probs: Vec<(i8, f64)> = icsd_data
        .keys()
        .filter(|k| k.starts_with(&prefix))
        .filter_map(|k| {
            let oxi_str = k.strip_prefix(&prefix)?;
            let oxi: i8 = oxi_str.parse().ok()?;
            let prob = calculate_oxi_probability(element, oxi, bv_sum);
            if prob > 0.0 { Some((oxi, prob)) } else { None }
        })
        .collect();

    // Normalize probabilities
    let total: f64 = probs.iter().map(|(_, p)| p).sum();
    if total > 0.0 {
        for (_, p) in &mut probs {
            *p /= total;
        }
    }

    // Sort by decreasing probability (unwrap_or handles NaN gracefully by treating as equal)
    probs.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));

    probs
}
