use std::collections::HashMap;
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};

use parking_lot::Mutex;

use super::download::MAX_IN_FLIGHT_HYDRATION_BYTES;
use super::{HydrationFailureReason, ResolvedSpecValues, VerifiedRemoteValues};
use crate::interned_string::InternedString;

/// The producer's latest definition, including the original origin for relative blob URLs.
pub(crate) struct PendingBlobDefinition {
    pub(crate) data: Vec<u8>,
    pub(crate) checksum: String,
    pub(crate) source_url: Arc<str>,
}

pub(crate) struct PendingBlobConfig {
    pub(crate) definition: Arc<PendingBlobDefinition>,
    verified: VerifiedRemoteValues,
    pub(crate) failed_blobs: HashMap<String, HydrationFailureReason>,
}

type PendingConfigs = HashMap<InternedString, Arc<PendingBlobConfig>>;

#[derive(Default)]
pub(crate) struct IncompleteBlobConfigs {
    pub(crate) pending: PendingConfigs,
    verified_bytes: u64,
}

pub(crate) struct PartialBlobRefresh<'a> {
    previous: Option<&'a IncompleteBlobConfigs>,
    state: Mutex<IncompleteBlobConfigs>,
    has_deferred: AtomicBool,
}

impl<'a> PartialBlobRefresh<'a> {
    pub(crate) fn new(previous: Option<&'a IncompleteBlobConfigs>) -> Self {
        let pending = previous.map(|p| p.pending.clone()).unwrap_or_default();
        Self {
            previous,
            state: Mutex::new(IncompleteBlobConfigs {
                pending,
                verified_bytes: previous.map_or(0, |configs| configs.verified_bytes),
            }),
            has_deferred: AtomicBool::new(false),
        }
    }

    pub(super) fn previous_proofs(&self, name: &InternedString) -> Option<&VerifiedRemoteValues> {
        Some(&self.previous?.pending.get(name)?.verified)
    }

    pub(crate) fn was_pending(&self, name: &InternedString) -> bool {
        self.previous
            .is_some_and(|previous| previous.pending.contains_key(name))
    }

    pub(crate) fn clear_config(&self, name: &InternedString) {
        if self.previous.is_some() || self.has_deferred.load(Ordering::Acquire) {
            self.state.lock().remove(name);
        }
    }

    pub(crate) fn defer(
        &self,
        name: &InternedString,
        definition: Arc<PendingBlobDefinition>,
        values: ResolvedSpecValues,
    ) {
        let mut state = self.state.lock();
        state.remove(name);
        let mut verified = values.provenance;
        // Charge the original verified byte length for each retained config/SHA pair.
        // Excess proofs can be downloaded again on a later repair.
        verified.retain(|_, value| {
            let total = state.verified_bytes + value.byte_length();
            if total > MAX_IN_FLIGHT_HYDRATION_BYTES as u64 {
                return false;
            }
            state.verified_bytes = total;
            true
        });
        state.pending.insert(
            name.clone(),
            Arc::new(PendingBlobConfig {
                definition,
                verified,
                failed_blobs: values.failed_blobs,
            }),
        );
        self.has_deferred.store(true, Ordering::Release);
    }

    pub(crate) fn carried_configs(&self) -> Vec<(InternedString, Arc<PendingBlobConfig>)> {
        let Some(previous) = self.previous else {
            return Vec::new();
        };
        let state = self.state.lock();
        state
            .pending
            .iter()
            .filter(|(name, config)| {
                previous
                    .pending
                    .get(*name)
                    .is_some_and(|old| Arc::ptr_eq(old, config))
            })
            .map(|(name, config)| (name.clone(), Arc::clone(config)))
            .collect()
    }

    pub(crate) fn take_incomplete(&self) -> Option<Box<IncompleteBlobConfigs>> {
        let mut state = self.state.lock();
        if state.pending.is_empty() {
            return None;
        }
        Some(Box::new(std::mem::take(&mut *state)))
    }
}

impl IncompleteBlobConfigs {
    fn remove(&mut self, name: &InternedString) {
        if let Some(config) = self.pending.remove(name) {
            self.verified_bytes -= config
                .verified
                .values()
                .map(|value| value.byte_length())
                .sum::<u64>();
        }
    }
}
