//! Port of `software.amazon.kinesis.leader.LeaderLock`.
//!
//! Data model of the KCL leader lock: a [`CoordinatorState`] subtype whose key
//! is the singleton `"Leader"` hash key and whose entity type is
//! `CoordinatorStateType::LeaderLock`, with an empty attributes map.
//!
//! Java `LeaderLock extends CoordinatorState`. In this port `CoordinatorState`
//! is an enum, so `LeaderLock` is expressed as (a) the [`LEADER_HASH_KEY`]
//! constant and (b) the [`leader_lock_state`] constructor returning a
//! [`CoordinatorState`] value — preserving both usage patterns
//! (`LeaderLock::LEADER_HASH_KEY` and `new LeaderLock().serialize()`).

use std::collections::HashMap;

use crate::coordinator::CoordinatorState;
use crate::leases::CoordinatorStateType;

/// Java `LeaderLock.LEADER_HASH_KEY = "Leader"` — the singleton lock record key.
pub const LEADER_HASH_KEY: &str = "Leader";

/// Build the leader-lock [`CoordinatorState`] value (Java `new LeaderLock()`):
/// key `"Leader"`, entity type `LEADER_LOCK`, empty attributes.
pub fn leader_lock_state() -> CoordinatorState {
    CoordinatorState::generic(
        Some(LEADER_HASH_KEY.to_string()),
        Some(CoordinatorStateType::LeaderLock),
        Some(HashMap::new()),
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn leader_hash_key_verbatim() {
        assert_eq!(LEADER_HASH_KEY, "Leader");
    }

    #[test]
    fn leader_lock_state_shape() {
        let state = leader_lock_state();
        assert_eq!(state.key(), Some(LEADER_HASH_KEY));
        assert_eq!(
            state.coordinator_state_entity_type(),
            Some(CoordinatorStateType::LeaderLock)
        );
        // serialize() carries the entityType attribute + nothing else.
        let serialized = state.serialize();
        assert!(serialized.contains_key(crate::coordinator::ENTITY_TYPE_ATTRIBUTE_NAME));
    }
}
