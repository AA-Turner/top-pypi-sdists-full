// === Composition-based Oxidation State Guessing ===

use super::MAX_PERMUTATIONS;
use super::data_structs::OxiStateGuess;
use super::lazy_data::get_icsd_oxi_prob;
use super::utils::species_key;
use crate::element::Element;
use std::collections::HashMap;

/// Get oxidation states to consider for an element.
///
/// Priority: ICSD oxidation states > common oxidation states > all oxidation states
pub fn get_candidate_oxi_states(element: Element, use_all: bool) -> Vec<i8> {
    if use_all {
        element.oxidation_states().to_vec()
    } else {
        let icsd = element.icsd_oxidation_states();
        if !icsd.is_empty() {
            icsd.to_vec()
        } else {
            element.common_oxidation_states().to_vec()
        }
    }
}

/// Generate non-decreasing combinations with replacement (multiset combinations).
///
/// For k items choosing n, generates C(k+n-1, n) combinations where each
/// combination is a non-decreasing sequence. This avoids permutational
/// duplicates for indistinguishable atoms.
///
/// Returns empty vec if the number of combinations would exceed MAX_PERMUTATIONS.
pub(crate) fn combinations_with_replacement(items: &[i8], count: usize) -> Vec<Vec<i8>> {
    if count == 0 {
        return vec![vec![]];
    }
    if items.is_empty() {
        return vec![];
    }

    // Compute C(k+n-1, n) using the smaller of n and k-1 as the iteration count
    // to check against MAX_PERMUTATIONS before generating
    let k = items.len();
    let num_combinations = binomial(k + count - 1, count.min(k - 1));
    if num_combinations.is_none_or(|n| n > MAX_PERMUTATIONS) {
        return vec![];
    }

    let mut result = Vec::new();
    fn recurse(
        items: &[i8],
        count: usize,
        start: usize,
        current: &mut Vec<i8>,
        result: &mut Vec<Vec<i8>>,
    ) {
        if count == 0 {
            result.push(current.clone());
            return;
        }
        for idx in start..items.len() {
            current.push(items[idx]);
            recurse(items, count - 1, idx, current, result);
            current.pop();
        }
    }
    recurse(items, count, 0, &mut Vec::with_capacity(count), &mut result);
    result
}

/// Compute binomial coefficient C(n, k), returning None on overflow.
fn binomial(n: usize, k: usize) -> Option<usize> {
    if k > n {
        return Some(0);
    }
    let k = k.min(n - k); // Use symmetry: C(n,k) = C(n, n-k)
    let mut result: usize = 1;
    for i in 0..k {
        result = result.checked_mul(n - i)?.checked_div(i + 1)?;
    }
    Some(result)
}

/// Find charge-balanced oxidation state assignments for a composition.
///
/// # Arguments
///
/// * `elements` - Elements in the composition
/// * `amounts` - Amount of each element (must be integers for proper enumeration)
/// * `target_charge` - Desired total charge (default 0 for charge balance)
/// * `oxi_states_override` - Override oxidation states for specific elements
/// * `use_all_oxi_states` - If true, use all known oxidation states (not just common/ICSD)
/// * `max_sites` - Maximum number of sites to enumerate (None = no limit)
///
/// # Returns
///
/// Vector of possible assignments sorted by ICSD probability score.
pub fn oxi_state_guesses(
    elements: &[Element],
    amounts: &[f64],
    target_charge: i8,
    oxi_states_override: Option<&HashMap<Element, Vec<i8>>>,
    use_all_oxi_states: bool,
    max_sites: Option<usize>,
) -> Vec<OxiStateGuess> {
    // Single element: only return oxidation state 0 when target_charge == 0
    // For non-zero target_charge, let normal enumeration handle it (or return empty if impossible)
    let unique_elements: std::collections::HashSet<_> = elements.iter().collect();
    if unique_elements.len() == 1 && target_charge == 0 {
        return vec![OxiStateGuess {
            oxidation_states: HashMap::from([(elements[0].symbol().to_string(), 0.0)]),
            probability: 1.0,
        }];
    }

    // Convert to positive integers (required for enumeration)
    let int_amounts: Option<Vec<i32>> = amounts
        .iter()
        .map(|&a| {
            let rounded = a.round();
            // Must be finite, positive, integer, and within i32 range
            if rounded.is_finite()
                && rounded > 0.0
                && rounded <= i32::MAX as f64
                && (a - rounded).abs() < 1e-8
            {
                Some(rounded as i32)
            } else {
                None
            }
        })
        .collect();

    let int_amounts = match int_amounts {
        Some(v) => v,
        None => return vec![], // Invalid amounts
    };

    // Optionally reduce composition
    let (elements, int_amounts) = if let Some(max) = max_sites {
        let total: i32 = int_amounts.iter().sum();
        if total as usize > max {
            // Try to reduce by GCD
            let gcd = int_amounts
                .iter()
                .fold(0i32, |acc, &x| gcd_i32(acc, x.abs()));
            if gcd > 1 {
                let reduced: Vec<i32> = int_amounts.iter().map(|&x| x / gcd).collect();
                let reduced_total: i32 = reduced.iter().sum();
                if reduced_total as usize <= max {
                    (elements.to_vec(), reduced)
                } else {
                    return vec![]; // Can't reduce enough
                }
            } else {
                return vec![]; // No common factor
            }
        } else {
            (elements.to_vec(), int_amounts)
        }
    } else {
        (elements.to_vec(), int_amounts)
    };

    // Get oxidation states for each element
    let el_oxi_states: Vec<Vec<i8>> = elements
        .iter()
        .map(|el| {
            oxi_states_override
                .and_then(|m| m.get(el).cloned())
                .unwrap_or_else(|| get_candidate_oxi_states(*el, use_all_oxi_states))
        })
        .collect();

    // For each element, compute all possible sums and their best combinations
    let icsd_prob = get_icsd_oxi_prob();
    let mut el_sums: Vec<HashMap<i32, (f64, Vec<i8>)>> = Vec::new();

    for (idx, oxis) in el_oxi_states.iter().enumerate() {
        let count = int_amounts[idx] as usize;
        let el = elements[idx];

        let mut sum_map: HashMap<i32, (f64, Vec<i8>)> = HashMap::new();

        for combo in combinations_with_replacement(oxis, count) {
            // Try to get ALL priors for this combo; skip if any are missing
            let log_probs: Option<Vec<f64>> = combo
                .iter()
                .map(|&o| {
                    let key = species_key(el, o);
                    icsd_prob.get(&key).map(|&p| (p as f64).ln())
                })
                .collect();

            let Some(log_probs) = log_probs else {
                // Missing ICSD data for at least one oxidation state; skip this combo
                continue;
            };

            let sum: i32 = combo.iter().map(|&o| o as i32).sum();
            let score: f64 = log_probs.iter().sum();

            // Keep the best-scoring combination for each sum (higher log-prob = better)
            let entry = sum_map
                .entry(sum)
                .or_insert((f64::NEG_INFINITY, combo.clone()));
            if score > entry.0 {
                *entry = (score, combo);
            }
        }

        el_sums.push(sum_map);
    }

    // Find all combinations of element sums that achieve target charge
    let mut solutions: Vec<OxiStateGuess> = Vec::new();
    let mut permutation_count = 0;

    #[allow(clippy::too_many_arguments)]
    fn recurse(
        el_sums: &[HashMap<i32, (f64, Vec<i8>)>],
        elements: &[Element],
        int_amounts: &[i32],
        target_charge: i32,
        current_idx: usize,
        current_sum: i32,
        current_scores: &mut Vec<f64>,
        current_combos: &mut Vec<Vec<i8>>,
        solutions: &mut Vec<OxiStateGuess>,
        permutation_count: &mut usize,
    ) {
        if *permutation_count >= MAX_PERMUTATIONS {
            return;
        }

        if current_idx == el_sums.len() {
            if current_sum == target_charge {
                // Found a valid solution
                let mut oxi_states = HashMap::new();
                for (idx, combo) in current_combos.iter().enumerate() {
                    let el = elements[idx];
                    let avg: f64 =
                        combo.iter().map(|&o| o as f64).sum::<f64>() / int_amounts[idx] as f64;
                    oxi_states.insert(el.symbol().to_string(), avg);
                }
                // Sum log-probabilities (equivalent to multiplying probabilities)
                // Convert back to probability space for output (exp of log-prob)
                let log_prob: f64 = current_scores.iter().sum();
                solutions.push(OxiStateGuess {
                    oxidation_states: oxi_states,
                    probability: log_prob.exp(),
                });
            }
            *permutation_count += 1;
            return;
        }

        // Compute bounds for remaining elements
        let mut min_remaining = 0i32;
        let mut max_remaining = 0i32;
        for sums in el_sums.iter().skip(current_idx + 1) {
            if let Some(min_sum) = sums.keys().min() {
                min_remaining += min_sum;
            }
            if let Some(max_sum) = sums.keys().max() {
                max_remaining += max_sum;
            }
        }

        // Prune if target is unreachable
        for (&sum, (score, combo)) in &el_sums[current_idx] {
            let new_sum = current_sum + sum;
            let remaining_needed = target_charge - new_sum;

            if remaining_needed < min_remaining || remaining_needed > max_remaining {
                continue;
            }

            current_scores.push(*score);
            current_combos.push(combo.clone());

            recurse(
                el_sums,
                elements,
                int_amounts,
                target_charge,
                current_idx + 1,
                new_sum,
                current_scores,
                current_combos,
                solutions,
                permutation_count,
            );

            current_scores.pop();
            current_combos.pop();
        }
    }

    let mut current_scores = Vec::new();
    let mut current_combos = Vec::new();

    recurse(
        &el_sums,
        &elements,
        &int_amounts,
        target_charge as i32,
        0,
        0,
        &mut current_scores,
        &mut current_combos,
        &mut solutions,
        &mut permutation_count,
    );

    // Sort by decreasing probability (unwrap_or handles NaN gracefully by treating as equal)
    solutions.sort_by(|a, b| {
        b.probability
            .partial_cmp(&a.probability)
            .unwrap_or(std::cmp::Ordering::Equal)
    });

    solutions
}

fn gcd_i32(mut a: i32, mut b: i32) -> i32 {
    a = a.abs();
    b = b.abs();
    while b != 0 {
        (a, b) = (b, a % b);
    }
    a
}

/// Find charge-balanced oxidation state assignment using recursive search with pruning.
/// Returns the highest log-probability assignment, or None if none found.
pub fn find_charge_balanced_assignment(
    site_probs: &[Vec<(i8, f64)>],
    multiplicities: &[usize],
) -> Option<Vec<i8>> {
    let mut best = (f64::NEG_INFINITY, None);
    let mut count = 0usize;

    #[allow(clippy::too_many_arguments)]
    fn recurse(
        site_probs: &[Vec<(i8, f64)>],
        mults: &[usize],
        idx: usize,
        charge: i32,
        assignment: &mut Vec<i8>,
        log_score: f64,
        best: &mut (f64, Option<Vec<i8>>),
        count: &mut usize,
    ) {
        if *count >= MAX_PERMUTATIONS {
            return;
        }
        if idx == site_probs.len() {
            *count += 1;
            if charge == 0 && log_score > best.0 {
                *best = (log_score, Some(assignment.clone()));
            }
            return;
        }
        // Compute reachable charge bounds for remaining sites
        let (min_rem, max_rem) = site_probs[idx + 1..]
            .iter()
            .zip(&mults[idx + 1..])
            .filter(|(probs, _)| !probs.is_empty())
            .map(|(probs, &mult)| {
                let (lo, hi) = probs.iter().fold((i8::MAX, i8::MIN), |(lo, hi), &(o, _)| {
                    (lo.min(o), hi.max(o))
                });
                (lo as i32 * mult as i32, hi as i32 * mult as i32)
            })
            .fold((0, 0), |(a, b), (c, d)| (a + c, b + d));

        for &(oxi, prob) in &site_probs[idx] {
            if prob <= 0.0 {
                continue;
            }
            let new_charge = charge + oxi as i32 * mults[idx] as i32;
            if new_charge + min_rem > 0 || new_charge + max_rem < 0 {
                continue;
            }
            assignment.push(oxi);
            recurse(
                site_probs,
                mults,
                idx + 1,
                new_charge,
                assignment,
                log_score + (mults[idx] as f64) * prob.ln(),
                best,
                count,
            );
            assignment.pop();
        }
    }

    recurse(
        site_probs,
        multiplicities,
        0,
        0,
        &mut vec![],
        0.0,
        &mut best,
        &mut count,
    );
    best.1
}
