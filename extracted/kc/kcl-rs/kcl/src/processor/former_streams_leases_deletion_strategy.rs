//! Port of `software.amazon.kinesis.processor.FormerStreamsLeasesDeletionStrategy`.

use std::time::Duration;

use crate::common::StreamIdentifier;

/// Strategy type discriminant identifying the different lease-cleanup strategies.
///
/// Port of the nested `StreamsLeasesDeletionType` enum.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum StreamsLeasesDeletionType {
    /// Do not delete leases for former streams.
    NoStreamsLeasesDeletion,
    /// Auto-detect former streams (by diffing the tracker's stream list) and
    /// delete their leases after a wait period.
    FormerStreamsAutoDetectionDeferredDeletion,
    /// Delete leases for a customer-provided list of streams after a wait period.
    ProvidedStreamsDeferredDeletion,
}

/// Strategy controlling how/whether KCL deletes DynamoDB leases belonging to
/// streams that are no longer tracked.
///
/// Ported faithfully as a trait (mirroring the Java interface + nested type
/// hierarchy) rather than a Rust sum type, to preserve the exact public API the
/// coordinator/lease-cleanup subsystem consumes. The methods that "don't apply"
/// to a given strategy panic with the same message Java throws
/// (`UnsupportedOperationException`), matching Java's runtime contract.
pub trait FormerStreamsLeasesDeletionStrategy {
    /// Stream identifiers whose leases need to be cleaned up in the lease table.
    ///
    /// # Panics
    /// Some strategies do not supply this list (it is auto-detected elsewhere)
    /// and panic with `StreamIdentifiers not required`, mirroring Java's
    /// `UnsupportedOperationException`.
    fn stream_identifiers_for_lease_cleanup(&self) -> Vec<StreamIdentifier>;

    /// Duration to wait before deleting the leases for former streams.
    fn wait_period_to_delete_former_streams(&self) -> Duration;

    /// The strategy type discriminant.
    fn lease_deletion_type(&self) -> StreamsLeasesDeletionType;
}

/// Strategy for not cleaning up leases for former streams.
///
/// Port of the nested `NoLeaseDeletionStrategy` final class.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq, Hash)]
pub struct NoLeaseDeletionStrategy;

impl FormerStreamsLeasesDeletionStrategy for NoLeaseDeletionStrategy {
    fn stream_identifiers_for_lease_cleanup(&self) -> Vec<StreamIdentifier> {
        panic!("StreamIdentifiers not required");
    }

    fn wait_period_to_delete_former_streams(&self) -> Duration {
        Duration::ZERO
    }

    fn lease_deletion_type(&self) -> StreamsLeasesDeletionType {
        StreamsLeasesDeletionType::NoStreamsLeasesDeletion
    }
}

/// Strategy for auto-detecting former streams (from the multi-stream tracker's
/// stream list) and performing deferred deletion.
///
/// Port of the nested `AutoDetectionAndDeferredDeletionStrategy` abstract class.
/// Java leaves `waitPeriodToDeleteFormerStreams()` abstract; here a concrete
/// wrapper carries the wait period so callers can construct it directly.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct AutoDetectionAndDeferredDeletionStrategy {
    wait_period: Duration,
}

impl AutoDetectionAndDeferredDeletionStrategy {
    /// Construct with the deferred-deletion wait period.
    pub fn new(wait_period: Duration) -> Self {
        Self { wait_period }
    }
}

impl FormerStreamsLeasesDeletionStrategy for AutoDetectionAndDeferredDeletionStrategy {
    fn stream_identifiers_for_lease_cleanup(&self) -> Vec<StreamIdentifier> {
        panic!("StreamIdentifiers not required");
    }

    fn wait_period_to_delete_former_streams(&self) -> Duration {
        self.wait_period
    }

    fn lease_deletion_type(&self) -> StreamsLeasesDeletionType {
        StreamsLeasesDeletionType::FormerStreamsAutoDetectionDeferredDeletion
    }
}

/// Strategy to delete leases for a customer-provided list of former streams,
/// with deferred deletion.
///
/// Port of the nested `ProvidedStreamsDeferredDeletionStrategy` abstract class.
/// Java leaves `streamIdentifiersForLeaseCleanup()` and
/// `waitPeriodToDeleteFormerStreams()` abstract; here a concrete wrapper carries
/// both so callers can construct it directly.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct ProvidedStreamsDeferredDeletionStrategy {
    stream_identifiers: Vec<StreamIdentifier>,
    wait_period: Duration,
}

impl ProvidedStreamsDeferredDeletionStrategy {
    /// Construct with the streams to clean up and the deferred-deletion wait period.
    pub fn new(stream_identifiers: Vec<StreamIdentifier>, wait_period: Duration) -> Self {
        Self {
            stream_identifiers,
            wait_period,
        }
    }
}

impl FormerStreamsLeasesDeletionStrategy for ProvidedStreamsDeferredDeletionStrategy {
    fn stream_identifiers_for_lease_cleanup(&self) -> Vec<StreamIdentifier> {
        self.stream_identifiers.clone()
    }

    fn wait_period_to_delete_former_streams(&self) -> Duration {
        self.wait_period
    }

    fn lease_deletion_type(&self) -> StreamsLeasesDeletionType {
        StreamsLeasesDeletionType::ProvidedStreamsDeferredDeletion
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn no_lease_deletion_defaults() {
        let s = NoLeaseDeletionStrategy;
        assert_eq!(
            s.lease_deletion_type(),
            StreamsLeasesDeletionType::NoStreamsLeasesDeletion
        );
        assert_eq!(s.wait_period_to_delete_former_streams(), Duration::ZERO);
    }

    #[test]
    #[should_panic(expected = "StreamIdentifiers not required")]
    fn no_lease_deletion_cleanup_panics() {
        NoLeaseDeletionStrategy.stream_identifiers_for_lease_cleanup();
    }

    #[test]
    #[should_panic(expected = "StreamIdentifiers not required")]
    fn auto_detection_cleanup_panics() {
        AutoDetectionAndDeferredDeletionStrategy::new(Duration::from_secs(5))
            .stream_identifiers_for_lease_cleanup();
    }

    #[test]
    fn auto_detection_type_and_wait() {
        let s = AutoDetectionAndDeferredDeletionStrategy::new(Duration::from_secs(10));
        assert_eq!(
            s.lease_deletion_type(),
            StreamsLeasesDeletionType::FormerStreamsAutoDetectionDeferredDeletion
        );
        assert_eq!(
            s.wait_period_to_delete_former_streams(),
            Duration::from_secs(10)
        );
    }

    #[test]
    fn provided_streams_returns_list() {
        let ids = vec![StreamIdentifier::single_stream_instance("a")];
        let s = ProvidedStreamsDeferredDeletionStrategy::new(ids.clone(), Duration::from_secs(1));
        assert_eq!(
            s.lease_deletion_type(),
            StreamsLeasesDeletionType::ProvidedStreamsDeferredDeletion
        );
        assert_eq!(s.stream_identifiers_for_lease_cleanup(), ids);
        assert_eq!(
            s.wait_period_to_delete_former_streams(),
            Duration::from_secs(1)
        );
    }
}
