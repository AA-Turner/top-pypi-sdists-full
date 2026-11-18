use crate::log_e;
use parking_lot::Mutex;
use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::time::Duration;

const MAX_CACHE_ENTRIES: usize = 10000;

struct MemoState {
    sha_hasher: Sha256,
    user_hash_cache: HashMap<String, u64>,
}

const TAG: &str = stringify!(MemoSha256);
pub struct MemoSha256 {
    inner: Mutex<MemoState>,
}

impl MemoSha256 {
    pub fn new() -> Self {
        Self {
            inner: Mutex::new(MemoState {
                sha_hasher: Sha256::new(),
                user_hash_cache: HashMap::new(),
            }),
        }
    }

    pub fn compute_hash(&self, input: &String) -> Option<u64> {
        let mut state = match self.inner.try_lock_for(Duration::from_secs(5)) {
            Some(state) => state,
            None => {
                log_e!(
                    TAG,
                    "Failed to acquire lock for Sha256: Failed to lock inner"
                );
                return None;
            }
        };

        if let Some(cache) = state.user_hash_cache.get(input) {
            return Some(*cache);
        }

        if state.user_hash_cache.len() > MAX_CACHE_ENTRIES {
            state.user_hash_cache.clear();
        }

        state.sha_hasher.update(input.as_bytes());
        let hash = state.sha_hasher.finalize_reset();

        match hash.split_at(size_of::<u64>()).0.try_into() {
            Ok(bytes) => {
                let u_bytes = u64::from_be_bytes(bytes);
                state.user_hash_cache.insert(input.clone(), u_bytes);
                Some(u_bytes)
            }
            _ => None,
        }
    }
}
