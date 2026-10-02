//! Port of `software.amazon.kinesis.coordinator.delegate`.
//!
//! The abstract `CoordinatorStateDAODelegate` and its two concrete subclasses
//! (`LeaseTableCoordinatorStateDAODelegate`,
//! `LegacyTableCoordinatorStateDAODelegate`) fold into a single
//! [`CoordinatorStateDaoDelegate`] struct discriminated by [`DelegateKind`].

pub mod coordinator_state_dao_delegate;

pub use coordinator_state_dao_delegate::{
    CoordinatorStateDaoDelegate, DelegateKind, LEGACY_COORDINATOR_STATE_HASH_KEY,
};
