//! Port of `software.amazon.kinesis.leases.LeaseDiscoverer`.
//!
//! Identifies leases assigned to the current worker that are not yet being
//! tracked/processed locally (e.g. via the `LeaseOwnerToLeaseKey` GSI, as
//! opposed to full-table renewal-based discovery). `@KinesisClientInternalApi`.
//!
//! # Async
//!
//! I/O trait (`#[async_trait]`): `discoverNewLeases` scans DynamoDB. Checked
//! exceptions → [`LeasingError`].

use async_trait::async_trait;

use crate::leases::exceptions::LeasingError;
use crate::leases::Lease;

/// Discovers leases assigned to the current worker that aren't yet tracked.
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait LeaseDiscoverer: Send + Sync {
    /// Identify the leases assigned to the current worker that are not being
    /// tracked/processed by it (Java `discoverNewLeases`).
    async fn discover_new_leases(&self) -> Result<Vec<Lease>, LeasingError>;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn mock_discover_new_leases() {
        let mut mock = MockLeaseDiscoverer::new();
        mock.expect_discover_new_leases()
            .returning(|| Ok(Vec::new()));
        assert!(mock.discover_new_leases().await.unwrap().is_empty());
    }
}
