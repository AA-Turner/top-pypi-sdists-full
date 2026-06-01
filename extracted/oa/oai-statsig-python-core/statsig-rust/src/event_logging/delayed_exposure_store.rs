use super::{
    event_logger::{EventLogger, ExposureTrigger, PreparedDelayedExposure},
    event_queue::queued_expo::EnqueueExposureOp,
};
use crate::{interned_string::InternedString, log_d, log_e, statsig_types_raw::PartialLayerRaw};
use parking_lot::{Mutex, MutexGuard};
use std::collections::{HashMap, HashSet, VecDeque};
use std::sync::Arc;
use uuid::Uuid;

const TAG: &str = stringify!(DelayedExposureStore);
const DEFAULT_MAX_TOKENS: usize = 10_000;

pub struct DelayedExposureStore {
    inner: Mutex<DelayedExposureStoreInner>,
    max_tokens: usize,
}

struct DelayedExposureStoreInner {
    entries: HashMap<String, DelayedExposureEntry>,
    insertion_order: VecDeque<String>,
    consumed: u64,
    released: u64,
    missing: u64,
    evicted: u64,
}

enum DelayedExposureEntry {
    Prepared(PreparedDelayedExposure),
    Layer(Box<DelayedLayerExposure>),
}

struct DelayedLayerExposure {
    partial_raw: PartialLayerRaw,
    logged_params: HashSet<String>,
}

impl DelayedExposureStore {
    pub fn new() -> Self {
        Self {
            inner: Mutex::new(DelayedExposureStoreInner {
                entries: HashMap::new(),
                insertion_order: VecDeque::new(),
                consumed: 0,
                released: 0,
                missing: 0,
                evicted: 0,
            }),
            max_tokens: DEFAULT_MAX_TOKENS,
        }
    }

    pub fn insert_prepared(&self, prepared: PreparedDelayedExposure) -> String {
        self.insert(DelayedExposureEntry::Prepared(prepared))
    }

    pub fn insert_layer(&self, partial_raw: PartialLayerRaw) -> String {
        self.insert(DelayedExposureEntry::Layer(Box::new(
            DelayedLayerExposure {
                partial_raw,
                logged_params: HashSet::new(),
            },
        )))
    }

    pub fn log_delayed_exposure(&self, token: &str, event_logger: &Arc<EventLogger>) -> bool {
        let entry = {
            let Some(mut inner) = self.try_lock_inner("log_delayed_exposure") else {
                return false;
            };

            match inner.entries.remove(token) {
                Some(entry) => {
                    inner.consumed += 1;
                    log_d!(
                        TAG,
                        "consumed delayed exposure token; outstanding={}",
                        inner.entries.len()
                    );
                    entry
                }
                None => {
                    inner.missing += 1;
                    return false;
                }
            }
        };

        match entry {
            DelayedExposureEntry::Prepared(prepared) => {
                event_logger.enqueue_prepared(prepared);
                true
            }
            DelayedExposureEntry::Layer(_) => false,
        }
    }

    pub fn log_delayed_layer_parameter_exposure(
        &self,
        token: &str,
        parameter_name: &str,
        event_logger: &Arc<EventLogger>,
    ) -> bool {
        let prepared = {
            let Some(mut inner) = self.try_lock_inner("log_delayed_layer_parameter_exposure")
            else {
                return false;
            };

            let Some(DelayedExposureEntry::Layer(layer)) = inner.entries.get_mut(token) else {
                inner.missing += 1;
                return false;
            };

            if !layer.logged_params.insert(parameter_name.to_string()) {
                return true;
            }

            let operation = EnqueueExposureOp::layer_param_exposure_from_partial_raw(
                InternedString::from_str_ref(parameter_name),
                ExposureTrigger::Auto,
                layer.partial_raw.clone(),
            );

            event_logger.prepare_event(operation)
        };

        if let Some(prepared) = prepared {
            event_logger.enqueue_prepared(prepared);
        }

        true
    }

    pub fn release(&self, token: &str) -> bool {
        let Some(mut inner) = self.try_lock_inner("release") else {
            return false;
        };

        match inner.entries.remove(token) {
            Some(_) => {
                inner.released += 1;
                log_d!(
                    TAG,
                    "released delayed exposure token; outstanding={}",
                    inner.entries.len()
                );
                true
            }
            None => {
                inner.missing += 1;
                false
            }
        }
    }

    pub fn release_many(&self, tokens: &[String]) -> usize {
        tokens.iter().filter(|token| self.release(token)).count()
    }

    pub fn clear(&self) {
        let Some(mut inner) = self.try_lock_inner("clear") else {
            return;
        };

        let count = inner.entries.len();
        inner.entries.clear();
        inner.insertion_order.clear();
        log_d!(TAG, "cleared delayed exposure store; dropped={count}");
    }

    fn insert(&self, entry: DelayedExposureEntry) -> String {
        let token = Uuid::new_v4().to_string();
        let Some(mut inner) = self.try_lock_inner("insert") else {
            return token;
        };

        inner.entries.insert(token.clone(), entry);
        inner.insertion_order.push_back(token.clone());

        while inner.entries.len() > self.max_tokens {
            let Some(oldest) = inner.insertion_order.pop_front() else {
                break;
            };

            if inner.entries.remove(&oldest).is_some() {
                inner.evicted += 1;
            }
        }

        log_d!(
            TAG,
            "created delayed exposure token; outstanding={}",
            inner.entries.len()
        );
        token
    }

    fn try_lock_inner(&self, operation: &str) -> Option<MutexGuard<'_, DelayedExposureStoreInner>> {
        match self.inner.try_lock_for(crate::macros::LOCK_TIMEOUT) {
            Some(inner) => Some(inner),
            None => {
                log_e!(
                    TAG,
                    "Failed to lock delayed exposure store for {}",
                    operation
                );
                None
            }
        }
    }
}

impl Default for DelayedExposureStore {
    fn default() -> Self {
        Self::new()
    }
}
