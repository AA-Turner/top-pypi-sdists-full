//! Port of `software.amazon.kinesis.leader` — coordinator-sub-wave 10c.
//!
//! Leader-election building blocks layered on the 10a `LeaderDecider` trait:
//! - [`leader_lock`] — the `LeaderLock` `CoordinatorState` subtype (constant +
//!   constructor).
//! - [`migration_adaptive_leader_decider`] — a decorator that hot-swaps the
//!   concrete decider based on migration state.
//! - [`ddb_lock`] — a **reimplementation** of the `AmazonDynamoDBLockClient`
//!   algorithm (acquire / heartbeat-renew / steal / release) over
//!   `aws_sdk_dynamodb` conditional writes (no Rust analog of the Java library).
//! - [`dynamodb_lock_based_leader_decider`] — the `LeaderDecider` impl using the
//!   DDB lock.

pub mod ddb_lock;
pub mod dynamodb_lock_based_leader_decider;
pub mod leader_lock;
pub mod migration_adaptive_leader_decider;

pub use ddb_lock::{DdbLockClient, LockClock, LockError, LockItem};
pub use dynamodb_lock_based_leader_decider::DynamoDBLockBasedLeaderDecider;
pub use leader_lock::{leader_lock_state, LEADER_HASH_KEY};
pub use migration_adaptive_leader_decider::MigrationAdaptiveLeaderDecider;
