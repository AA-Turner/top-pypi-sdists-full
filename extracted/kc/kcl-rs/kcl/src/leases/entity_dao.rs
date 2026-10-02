//! Port of `software.amazon.kinesis.leases.EntityDAO`.
//!
//! DAO that reads **all** entity types (Lease, WorkerMetricStats,
//! CoordinatorState, ...) co-located in a single consolidated lease table in one
//! DynamoDB scan, grouping them by [`EntityType`]. `@KinesisClientInternalApi`.
//!
//! # Async
//!
//! I/O trait (`#[async_trait]`): scans DynamoDB. Checked exceptions →
//! [`LeasingError`].
//!
//! # Deviations
//!
//! - Nested Java `interface Entity { EntityType getEntityType(); }` → the
//!   [`Entity`] trait (implemented by `Lease` and, later, `WorkerMetricStats` /
//!   `CoordinatorState`). It is `Send + Sync` so scan results can hold
//!   `Box<dyn Entity>`.
//! - Nested `@Value @Builder class EntityScanList` → the [`EntityScanList`]
//!   struct (both fields default to empty via `bon::Builder`).
//! - `scanEntities(EntityType...)` varargs → `scan_entities(&[EntityType])`.
//! - Records lacking an `entityType` attribute are treated as
//!   [`EntityType::Lease`] — a contract the concrete impl (6c) must preserve.

use std::collections::HashMap;

use async_trait::async_trait;
use bon::Builder;

use crate::leases::exceptions::LeasingError;
use crate::leases::{EntityType, Lease};

/// An entity stored in the lease table (Java nested `EntityDAO.Entity`).
///
/// Implemented by [`Lease`](crate::leases::Lease) and, in later waves,
/// `WorkerMetricStats` / `CoordinatorState`. Used by the DAO to group scan
/// results by type.
pub trait Entity: Send + Sync {
    /// The [`EntityType`] identifying what kind of entity this is.
    fn get_entity_type(&self) -> EntityType;

    /// Downcast support (Rust replacement for Java `instanceof`), so callers
    /// like `MigrationAwareLAMDataManager` can extract concrete `Lease` /
    /// `WorkerMetricStats` from a scanned `Box<dyn Entity>`.
    fn into_any(self: Box<Self>) -> Box<dyn std::any::Any>;
}

/// `Lease implements EntityDAO.Entity` in Java (a `Lease` always reports
/// [`EntityType::Lease`]).
impl Entity for Lease {
    fn get_entity_type(&self) -> EntityType {
        self.entity_type()
    }
    fn into_any(self: Box<Self>) -> Box<dyn std::any::Any> {
        self
    }
}

/// Scan result for a single entity type (Java nested `EntityDAO.EntityScanList`).
///
/// Holds the successfully-deserialized entities and the partition keys of items
/// that were identified as this type but failed deserialization (so callers can
/// emit metrics/log rather than failing the whole scan). Both default to empty.
#[derive(Builder)]
pub struct EntityScanList {
    /// Successfully-deserialized entities of this type.
    #[builder(default)]
    pub entities: Vec<Box<dyn Entity>>,

    /// Partition keys of items identified as this type but not deserializable.
    #[builder(default)]
    pub deserialization_failures: Vec<String>,
}

/// Reads all entity types from the lease table in a single DDB scan.
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait EntityDAO: Send + Sync {
    /// Scan all entities and group them by [`EntityType`]. Records without an
    /// `entityType` attribute are treated as [`EntityType::Lease`].
    async fn scan_all_entities(&self) -> Result<HashMap<EntityType, EntityScanList>, LeasingError>;

    /// Scan entities filtered to only the specified entity types.
    async fn scan_entities(
        &self,
        entity_types: &[EntityType],
    ) -> Result<HashMap<EntityType, EntityScanList>, LeasingError>;

    /// Shut down any resources held by this DAO (e.g. parallel-scan thread
    /// pools). Idempotent; default is a no-op.
    async fn shutdown(&self) {}
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn entity_scan_list_defaults_empty() {
        let l = EntityScanList::builder().build();
        assert!(l.entities.is_empty());
        assert!(l.deserialization_failures.is_empty());
    }

    #[tokio::test]
    async fn mock_scan_all_entities_and_shutdown() {
        let mut mock = MockEntityDAO::new();
        mock.expect_scan_all_entities()
            .returning(|| Ok(HashMap::new()));
        mock.expect_shutdown().returning(|| ());
        assert!(mock.scan_all_entities().await.unwrap().is_empty());
        mock.shutdown().await;
    }
}
