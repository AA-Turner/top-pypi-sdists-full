use std::collections::HashSet;

use parking_lot::RwLock;

use crate::{log_e, read_lock_or_else, write_lock_or_noop};

const TAG: &str = "IdListAccesses";

pub(crate) trait IdListAccessRecorder {
    fn record(&self, name: &str);
}

impl IdListAccessRecorder for () {
    fn record(&self, _: &str) {}
}

#[derive(Default)]
pub(crate) struct IdListAccesses {
    seen: HashSet<String>,
    pub(super) pending: Vec<String>,
}

impl IdListAccesses {
    pub(super) fn discard_pending(&mut self) {
        // Only unsent accesses can be retried after collection is re-enabled.
        for name in self.pending.drain(..) {
            self.seen.remove(&name);
        }
    }
}

impl IdListAccessRecorder for RwLock<IdListAccesses> {
    fn record(&self, name: &str) {
        {
            let accesses = read_lock_or_else!(self, {
                log_e!(TAG, "Failed to acquire read lock");
                return;
            });
            if accesses.seen.contains(name) {
                return;
            }
        }

        let mut accesses = write_lock_or_noop!(TAG, self);
        // Recheck under the write lock so concurrent first accesses emit once.
        if accesses.seen.insert(name.to_owned()) {
            accesses.pending.push(name.to_owned());
        }
    }
}

#[cfg(test)]
#[path = "__tests__/id_list_accesses_tests.rs"]
mod tests;
