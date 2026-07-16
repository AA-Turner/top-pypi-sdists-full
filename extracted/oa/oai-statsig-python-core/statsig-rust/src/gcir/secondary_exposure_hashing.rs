//! Secondary-exposure deduplication and gate-name hashing for GCIR responses.
//!
//! The straightforward implementation uses a `HashSet` for every exposure list.
//! In production, most lists contain only a handful of entries, so allocating the
//! set costs more than the small amount of dedupe work. Lists of up to eight
//! entries therefore use a fixed-size stack buffer and a linear scan. This is
//! intentionally more complicated than the naive solution: it avoids the common
//! allocation while capping the scan at 28 comparisons for eight unique entries.
//! Larger lists retain the allocating `HashSet` path so their lookup work remains
//! expected O(n) rather than becoming quadratic.

use crate::{
    evaluation::evaluator_result::EvaluatorResult, hashing::HashUtil,
    interned_string::InternedString, HashAlgorithm, SecondaryExposure,
};
use std::collections::{HashMap, HashSet};

const SMALL_EXPOSURE_DEDUPE_LIMIT: usize = 8;

pub(crate) fn hash_secondary_exposures(
    result: &mut EvaluatorResult,
    hashing: &HashUtil,
    hash_algorithm: &HashAlgorithm,
    memo: &mut HashMap<InternedString, InternedString>,
) {
    let mut processor = SecondaryExposureHashProcessor::new(hashing, hash_algorithm, memo);

    if !result.secondary_exposures.is_empty() {
        processor.dedupe_and_hash_gates(&mut result.secondary_exposures);
    }

    if let Some(undelegated_secondary_exposures) = result.undelegated_secondary_exposures.as_mut() {
        processor.dedupe_and_hash_gates(undelegated_secondary_exposures);
    }
}

#[derive(Clone, Copy, Eq, Hash, PartialEq)]
struct SecondaryExposureDedupeKey {
    gate_name_hash: u64,
    rule_id_hash: u64,
    gate_value_hash: u64,
}

impl From<&SecondaryExposure> for SecondaryExposureDedupeKey {
    fn from(exposure: &SecondaryExposure) -> Self {
        // Interned strings cache these hashes. Reusing them avoids hashing three
        // string values again merely to build the dedupe key.
        Self {
            gate_name_hash: exposure.gate.hash,
            rule_id_hash: exposure.rule_id.hash,
            gate_value_hash: exposure.gate_value.hash,
        }
    }
}

struct SecondaryExposureHashProcessor<'a> {
    hashing: &'a HashUtil,
    hash_algorithm: &'a HashAlgorithm,
    memo: &'a mut HashMap<InternedString, InternedString>,
}

impl<'a> SecondaryExposureHashProcessor<'a> {
    fn new(
        hashing: &'a HashUtil,
        hash_algorithm: &'a HashAlgorithm,
        memo: &'a mut HashMap<InternedString, InternedString>,
    ) -> Self {
        Self {
            hashing,
            hash_algorithm,
            memo,
        }
    }

    /// Removes duplicate secondary exposures and hashes gate names in place.
    fn dedupe_and_hash_gates(&mut self, exposures: &mut Vec<SecondaryExposure>) {
        if exposures.len() <= SMALL_EXPOSURE_DEDUPE_LIMIT {
            self.dedupe_small_and_hash_gates(exposures);
            return;
        }

        self.dedupe_large_and_hash_gates(exposures);
    }

    fn dedupe_small_and_hash_gates(&mut self, exposures: &mut Vec<SecondaryExposure>) {
        let mut seen = SmallSecondaryExposureDedupe::new();
        exposures.retain_mut(|exposure| {
            if !seen.insert(SecondaryExposureDedupeKey::from(&*exposure)) {
                return false;
            }

            self.hash_gate(exposure);
            true
        });
    }

    fn dedupe_large_and_hash_gates(&mut self, exposures: &mut Vec<SecondaryExposure>) {
        let mut seen = HashSet::<SecondaryExposureDedupeKey>::with_capacity(exposures.len());
        exposures.retain_mut(|exposure| {
            if !seen.insert(SecondaryExposureDedupeKey::from(&*exposure)) {
                return false;
            }

            self.hash_gate(exposure);
            true
        });
    }

    fn hash_gate(&mut self, exposure: &mut SecondaryExposure) {
        match self.memo.get(&exposure.gate) {
            Some(hash) => {
                exposure.gate = hash.clone();
            }
            None => {
                let hash = self.hashing.hash(&exposure.gate, self.hash_algorithm);
                let interned_hash = InternedString::from_string_uninterned(hash);
                let old = std::mem::replace(&mut exposure.gate, interned_hash.clone());
                self.memo.insert(old, interned_hash);
            }
        }
    }
}

struct SmallSecondaryExposureDedupe {
    seen: [SecondaryExposureDedupeKey; SMALL_EXPOSURE_DEDUPE_LIMIT],
    len: usize,
}

impl SmallSecondaryExposureDedupe {
    fn new() -> Self {
        Self {
            seen: [SecondaryExposureDedupeKey {
                gate_name_hash: 0,
                rule_id_hash: 0,
                gate_value_hash: 0,
            }; SMALL_EXPOSURE_DEDUPE_LIMIT],
            len: 0,
        }
    }

    fn insert(&mut self, key: SecondaryExposureDedupeKey) -> bool {
        if self.seen[..self.len].contains(&key) {
            return false;
        }

        self.seen[self.len] = key;
        self.len += 1;
        true
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn exposure(gate: &str, gate_value: &str, rule_id: &str) -> SecondaryExposure {
        SecondaryExposure {
            gate: InternedString::from_str_ref(gate),
            gate_value: InternedString::from_str_ref(gate_value),
            rule_id: InternedString::from_str_ref(rule_id),
        }
    }

    fn assert_exposure(exposure: &SecondaryExposure, gate: &str, gate_value: &str, rule_id: &str) {
        assert_eq!(exposure.gate.as_str(), gate);
        assert_eq!(exposure.gate_value.as_str(), gate_value);
        assert_eq!(exposure.rule_id.as_str(), rule_id);
    }

    #[test]
    fn dedupes_hashes_and_reuses_memo_for_both_exposure_lists() {
        let duplicate = exposure("gate-a", "true", "rule-a");
        let mut result = EvaluatorResult {
            secondary_exposures: vec![
                duplicate.clone(),
                duplicate,
                exposure("gate-a", "false", "rule-a"),
                exposure("gate-a", "true", "rule-b"),
                exposure("gate-b", "false", "rule-c"),
            ],
            undelegated_secondary_exposures: Some(vec![
                exposure("gate-b", "true", "rule-d"),
                exposure("gate-b", "true", "rule-d"),
                exposure("gate-a", "false", "rule-e"),
            ]),
            ..Default::default()
        };
        let hashing = HashUtil::new();
        let hash_algorithm = HashAlgorithm::Djb2;
        let gate_a_hash = hashing.hash("gate-a", &hash_algorithm);
        let gate_b_hash = hashing.hash("gate-b", &hash_algorithm);
        let mut memo = HashMap::new();

        hash_secondary_exposures(&mut result, &hashing, &hash_algorithm, &mut memo);

        assert_eq!(result.secondary_exposures.len(), 4);
        assert_exposure(
            &result.secondary_exposures[0],
            &gate_a_hash,
            "true",
            "rule-a",
        );
        assert_exposure(
            &result.secondary_exposures[1],
            &gate_a_hash,
            "false",
            "rule-a",
        );
        assert_exposure(
            &result.secondary_exposures[2],
            &gate_a_hash,
            "true",
            "rule-b",
        );
        assert_exposure(
            &result.secondary_exposures[3],
            &gate_b_hash,
            "false",
            "rule-c",
        );

        let undelegated = result.undelegated_secondary_exposures.unwrap();
        assert_eq!(undelegated.len(), 2);
        assert_exposure(&undelegated[0], &gate_b_hash, "true", "rule-d");
        assert_exposure(&undelegated[1], &gate_a_hash, "false", "rule-e");

        assert_eq!(memo.len(), 2);
        assert_eq!(
            memo.get(&InternedString::from_str_ref("gate-a"))
                .unwrap()
                .as_str(),
            gate_a_hash
        );
        assert_eq!(
            memo.get(&InternedString::from_str_ref("gate-b"))
                .unwrap()
                .as_str(),
            gate_b_hash
        );
    }

    #[test]
    fn dedupe_handles_small_list_boundary_and_large_list_path() {
        for input_len in [SMALL_EXPOSURE_DEDUPE_LIMIT, SMALL_EXPOSURE_DEDUPE_LIMIT + 1] {
            let mut exposures = (0..SMALL_EXPOSURE_DEDUPE_LIMIT)
                .map(|index| exposure(&format!("gate-{index}"), "true", &format!("rule-{index}")))
                .collect::<Vec<_>>();

            if input_len > SMALL_EXPOSURE_DEDUPE_LIMIT {
                exposures.push(exposures[3].clone());
            }

            let mut result = EvaluatorResult {
                secondary_exposures: exposures,
                ..Default::default()
            };

            hash_secondary_exposures(
                &mut result,
                &HashUtil::new(),
                &HashAlgorithm::None,
                &mut HashMap::new(),
            );

            assert_eq!(
                result.secondary_exposures.len(),
                SMALL_EXPOSURE_DEDUPE_LIMIT,
                "input_len={input_len}"
            );
            for (index, exposure) in result.secondary_exposures.iter().enumerate() {
                assert_exposure(
                    exposure,
                    &format!("gate-{index}"),
                    "true",
                    &format!("rule-{index}"),
                );
            }
        }
    }
}
