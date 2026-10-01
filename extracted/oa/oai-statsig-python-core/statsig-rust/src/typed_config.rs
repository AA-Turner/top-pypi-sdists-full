use std::time::Duration;

use parking_lot::{Condvar, Mutex};

#[derive(Default)]
pub struct ConfigUpdates {
    state: Mutex<UpdateState>,
    changed: Condvar,
}

#[derive(Default)]
struct UpdateState {
    pending: bool,
    closed: bool,
}

impl ConfigUpdates {
    pub(crate) fn notify(&self) {
        let mut state = self.state.lock();
        if state.closed {
            return;
        }
        state.pending = true;
        self.changed.notify_one();
    }

    pub fn wait(&self, timeout: Duration) -> Option<bool> {
        let mut state = self.state.lock();
        self.changed
            .wait_while_for(&mut state, |state| !state.pending && !state.closed, timeout);
        if state.closed {
            return None;
        }
        Some(std::mem::take(&mut state.pending))
    }

    pub fn close(&self) {
        let mut state = self.state.lock();
        state.closed = true;
        state.pending = false;
        self.changed.notify_all();
    }
}

#[cfg(test)]
mod tests;
