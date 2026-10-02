//! Port of `software.amazon.kinesis.checkpoint.dynamodb.DynamoDBCheckpointer`.

use std::sync::{Arc, Mutex};

use tokio::runtime::Handle;
use uuid::Uuid;

use crate::checkpoint::Checkpoint;
use crate::exceptions::KinesisClientLibError;
use crate::leases::exceptions::LeasingError;
use crate::leases::{LeaseCoordinator, LeaseRefresher};
use crate::processor::Checkpointer;
use crate::retrieval::kpl::ExtendedSequenceNumber;

/// DynamoDB-backed implementation of the [`Checkpointer`] SPI.
///
/// Persists checkpoint / pending-checkpoint state as fields on the shard's
/// `Lease` record via the [`LeaseCoordinator`] (for writes, using
/// optimistic-concurrency updates gated by a `concurrencyToken`) and the
/// [`LeaseRefresher`] (for reads).
///
/// # Sync → async bridge
///
/// The [`Checkpointer`] trait is **synchronous** (its callers are the
/// synchronous `RecordProcessor` callback path), but [`LeaseCoordinator`] /
/// [`LeaseRefresher`] are **async**. This struct holds a
/// [`tokio::runtime::Handle`] and runs each async operation to completion with
/// [`Handle::block_on`].
///
/// **Invariant:** these methods must **not** be called from a thread that is
/// actively driving the tokio runtime (i.e. from inside an `async` task on that
/// runtime), or `block_on` will panic. They are always invoked from the
/// `RecordProcessor` callback path, which the lifecycle & binding waves run on a
/// dedicated blocking thread — never on a runtime worker thread — so this holds.
/// In tests, construct a runtime and call from the (non-runtime) test thread.
pub struct DynamoDBCheckpointer {
    lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
    lease_refresher: Arc<dyn LeaseRefresher>,
    /// The tokio runtime handle used to drive the async lease operations.
    runtime: Handle,
    /// The current logical operation label (Java mutable `operation` field, set
    /// via [`Checkpointer::set_operation`], passed into `updateLease`).
    operation: Mutex<Option<String>>,
}

impl DynamoDBCheckpointer {
    /// Construct a checkpointer.
    ///
    /// `runtime` is the handle of the tokio runtime that drives the async lease
    /// operations (see the sync→async bridge invariant on the struct docs).
    pub fn new(
        lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
        lease_refresher: Arc<dyn LeaseRefresher>,
        runtime: Handle,
    ) -> Self {
        Self {
            lease_coordinator,
            lease_refresher,
            runtime,
            operation: Mutex::new(None),
        }
    }

    fn operation_value(&self) -> String {
        self.operation
            .lock()
            .expect("operation mutex poisoned")
            .clone()
            .unwrap_or_default()
    }

    /// Core worker (Java `@VisibleForTesting boolean setCheckpoint(String,
    /// ExtendedSequenceNumber, UUID)`). Fetches the currently-held lease,
    /// mutates it (committing the checkpoint clears any pending checkpoint and
    /// resets the owner-switch counter), then does the conditional update.
    /// Returns `false` if the lease is not currently held by this worker.
    fn set_checkpoint_uuid(
        &self,
        lease_key: &str,
        checkpoint: &ExtendedSequenceNumber,
        concurrency_token: Uuid,
    ) -> Result<bool, LeasingError> {
        let lease = self.lease_coordinator.get_currently_held_lease(lease_key);
        let mut lease = match lease {
            Some(lease) => lease,
            None => {
                tracing::info!(
                    "Worker {} could not update checkpoint for shard {} because it does not hold the lease",
                    self.lease_coordinator.worker_identifier(),
                    lease_key
                );
                return Ok(false);
            }
        };

        lease.set_checkpoint(checkpoint.clone());
        lease.set_pending_checkpoint(None);
        lease.set_pending_checkpoint_state(None);
        lease.set_owner_switches_since_checkpoint(0);

        let operation = self.operation_value();
        self.runtime.block_on(self.lease_coordinator.update_lease(
            &lease,
            concurrency_token,
            &operation,
            lease_key,
        ))
    }

    /// Core worker for prepare (Java package-visible `boolean
    /// prepareCheckpoint(String, ExtendedSequenceNumber, UUID, byte[])`). Sets
    /// only the pending checkpoint + pending state, leaving the committed
    /// checkpoint and owner-switch counter untouched. Returns `false` if the
    /// lease is not currently held.
    fn prepare_checkpoint_uuid(
        &self,
        lease_key: &str,
        pending_checkpoint: &ExtendedSequenceNumber,
        concurrency_token: Uuid,
        pending_checkpoint_state: Option<&[u8]>,
    ) -> Result<bool, LeasingError> {
        let lease = self.lease_coordinator.get_currently_held_lease(lease_key);
        let mut lease = match lease {
            Some(lease) => lease,
            None => {
                tracing::info!(
                    "Worker {} could not prepare checkpoint for shard {} because it does not hold the lease",
                    self.lease_coordinator.worker_identifier(),
                    lease_key
                );
                return Ok(false);
            }
        };

        // Java `Objects.requireNonNull(pendingCheckpoint, ...)`: pendingCheckpoint
        // is always non-null on the Rust call path (a `&ExtendedSequenceNumber`).
        lease.set_pending_checkpoint(Some(pending_checkpoint.clone()));
        lease.set_pending_checkpoint_state(pending_checkpoint_state.map(<[u8]>::to_vec));

        let operation = self.operation_value();
        self.runtime.block_on(self.lease_coordinator.update_lease(
            &lease,
            concurrency_token,
            &operation,
            lease_key,
        ))
    }
}

/// Parse a concurrency token, mirroring Java's `UUID.fromString` which throws an
/// unchecked `IllegalArgumentException` (→ `panic!`) on a malformed token.
fn parse_concurrency_token(concurrency_token: &str) -> Uuid {
    Uuid::parse_str(concurrency_token)
        .unwrap_or_else(|_| panic!("Invalid UUID string: {}", concurrency_token))
}

impl Checkpointer for DynamoDBCheckpointer {
    fn set_checkpoint(
        &self,
        lease_key: &str,
        checkpoint_value: &ExtendedSequenceNumber,
        concurrency_token: &str,
    ) -> Result<(), KinesisClientLibError> {
        let token = parse_concurrency_token(concurrency_token);
        match self.set_checkpoint_uuid(lease_key, checkpoint_value, token) {
            Ok(true) => Ok(()),
            Ok(false) => Err(KinesisClientLibError::shutdown(
                "Can't update checkpoint - instance doesn't hold the lease for this shard",
            )),
            Err(LeasingError::ProvisionedThroughput { source, .. }) => Err(throttling(
                "Got throttled while updating checkpoint.",
                source,
            )),
            Err(LeasingError::InvalidState { source, .. }) => {
                let message = format!("Unable to save checkpoint for shardId {}", lease_key);
                tracing::error!("{}", message);
                Err(invalid_state(message, source))
            }
            Err(LeasingError::Dependency { source, .. }) => Err(dependency(
                format!("Unable to save checkpoint for shardId {}", lease_key),
                source,
            )),
        }
    }

    fn get_checkpoint(
        &self,
        lease_key: &str,
    ) -> Result<Option<ExtendedSequenceNumber>, KinesisClientLibError> {
        match self
            .runtime
            .block_on(self.lease_refresher.get_lease(lease_key))
        {
            Ok(lease) => Ok(lease.and_then(|l| l.checkpoint().cloned())),
            Err(e) => Err(fetch_error(lease_key, e)),
        }
    }

    fn get_checkpoint_object(
        &self,
        lease_key: &str,
    ) -> Result<Option<Checkpoint>, KinesisClientLibError> {
        match self
            .runtime
            .block_on(self.lease_refresher.get_lease(lease_key))
        {
            Ok(None) => Ok(None),
            Ok(Some(lease)) => {
                tracing::debug!("[{}] Retrieved lease => {:?}", lease_key, lease);
                let checkpoint = lease
                    .checkpoint()
                    .cloned()
                    .expect("Checkpoint cannot be null or empty");
                Ok(Some(Checkpoint::new(
                    checkpoint,
                    lease.pending_checkpoint().cloned(),
                    lease.pending_checkpoint_state().map(<[u8]>::to_vec),
                )))
            }
            Err(e) => Err(fetch_error(lease_key, e)),
        }
    }

    fn prepare_checkpoint(
        &self,
        lease_key: &str,
        pending_checkpoint: &ExtendedSequenceNumber,
        concurrency_token: &str,
    ) -> Result<(), KinesisClientLibError> {
        self.prepare_checkpoint_with_state_impl(
            lease_key,
            pending_checkpoint,
            concurrency_token,
            None,
        )
    }

    fn prepare_checkpoint_with_state(
        &self,
        lease_key: &str,
        pending_checkpoint: &ExtendedSequenceNumber,
        concurrency_token: &str,
        pending_checkpoint_state: &[u8],
    ) -> Result<(), KinesisClientLibError> {
        self.prepare_checkpoint_with_state_impl(
            lease_key,
            pending_checkpoint,
            concurrency_token,
            Some(pending_checkpoint_state),
        )
    }

    fn set_operation(&self, operation: &str) {
        // Java `operation(@NonNull String)`.
        *self.operation.lock().expect("operation mutex poisoned") = Some(operation.to_string());
    }

    fn operation(&self) -> String {
        self.operation_value()
    }
}

impl DynamoDBCheckpointer {
    fn prepare_checkpoint_with_state_impl(
        &self,
        lease_key: &str,
        pending_checkpoint: &ExtendedSequenceNumber,
        concurrency_token: &str,
        pending_checkpoint_state: Option<&[u8]>,
    ) -> Result<(), KinesisClientLibError> {
        let token = parse_concurrency_token(concurrency_token);
        match self.prepare_checkpoint_uuid(
            lease_key,
            pending_checkpoint,
            token,
            pending_checkpoint_state,
        ) {
            Ok(true) => Ok(()),
            Ok(false) => Err(KinesisClientLibError::shutdown(
                "Can't prepare checkpoint - instance doesn't hold the lease for this shard",
            )),
            Err(LeasingError::ProvisionedThroughput { source, .. }) => Err(throttling(
                "Got throttled while preparing checkpoint.",
                source,
            )),
            Err(LeasingError::InvalidState { source, .. }) => {
                let message = format!("Unable to prepare checkpoint for shardId {}", lease_key);
                tracing::error!("{}", message);
                Err(invalid_state(message, source))
            }
            Err(LeasingError::Dependency { source, .. }) => Err(dependency(
                format!("Unable to prepare checkpoint for shardId {}", lease_key),
                source,
            )),
        }
    }
}

// --- error mapping helpers (mirror the Java catch blocks 1:1) ---

type BoxErr = crate::exceptions::BoxError;

fn throttling(message: &str, source: Option<BoxErr>) -> KinesisClientLibError {
    KinesisClientLibError::Throttling {
        message: message.to_string(),
        source,
    }
}

fn invalid_state(message: String, source: Option<BoxErr>) -> KinesisClientLibError {
    KinesisClientLibError::InvalidState { message, source }
}

fn dependency(message: String, source: Option<BoxErr>) -> KinesisClientLibError {
    KinesisClientLibError::Dependency { message, source }
}

/// `getCheckpoint`/`getCheckpointObject` wrap every leasing failure
/// (`Dependency`/`InvalidState`/`ProvisionedThroughput`) into a
/// `KinesisClientLibIOException`.
fn fetch_error(lease_key: &str, e: LeasingError) -> KinesisClientLibError {
    let message = format!("Unable to fetch checkpoint for shardId {}", lease_key);
    tracing::error!("{}", message);
    KinesisClientLibError::io_caused_by(message, Box::new(e) as BoxErr)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::{Lease, MockLeaseCoordinator, MockLeaseRefresher};

    fn esn(sn: &str) -> ExtendedSequenceNumber {
        ExtendedSequenceNumber::from_sequence_number(sn)
    }

    fn token() -> Uuid {
        Uuid::new_v4()
    }

    fn make_lease(lease_key: &str, checkpoint: &str) -> Lease {
        let mut lease = Lease::default();
        lease.set_lease_key(lease_key.to_string());
        lease.set_checkpoint(esn(checkpoint));
        lease
    }

    #[test]
    fn set_checkpoint_success_updates_lease() {
        let rt = tokio::runtime::Builder::new_multi_thread()
            .enable_all()
            .build()
            .unwrap();

        let concurrency = token();
        let mut coordinator = MockLeaseCoordinator::new();
        coordinator
            .expect_get_currently_held_lease()
            .withf(|k| k == "shard-1")
            .returning(|_| Some(make_lease("shard-1", "10")));
        coordinator
            .expect_worker_identifier()
            .returning(|| "worker-1".to_string());
        coordinator
            .expect_update_lease()
            .withf(move |lease, tok, _op, key| {
                // Committing clears pending + resets owner switches, and sets the
                // new checkpoint.
                lease.checkpoint() == Some(&esn("100"))
                    && lease.pending_checkpoint().is_none()
                    && lease.owner_switches_since_checkpoint() == 0
                    && *tok == concurrency
                    && key == "shard-1"
            })
            .returning(|_, _, _, _| Ok(true));

        let refresher = MockLeaseRefresher::new();
        let checkpointer = DynamoDBCheckpointer::new(
            Arc::new(coordinator),
            Arc::new(refresher),
            rt.handle().clone(),
        );

        checkpointer
            .set_checkpoint("shard-1", &esn("100"), &concurrency.to_string())
            .unwrap();
    }

    #[test]
    fn set_checkpoint_not_held_is_shutdown() {
        let rt = tokio::runtime::Builder::new_current_thread()
            .build()
            .unwrap();

        let mut coordinator = MockLeaseCoordinator::new();
        coordinator
            .expect_get_currently_held_lease()
            .returning(|_| None);
        coordinator
            .expect_worker_identifier()
            .returning(|| "worker-1".to_string());

        let checkpointer = DynamoDBCheckpointer::new(
            Arc::new(coordinator),
            Arc::new(MockLeaseRefresher::new()),
            rt.handle().clone(),
        );

        let err = checkpointer
            .set_checkpoint("shard-1", &esn("100"), &token().to_string())
            .unwrap_err();
        assert!(matches!(err, KinesisClientLibError::Shutdown { .. }));
    }

    #[test]
    fn set_checkpoint_throttling_maps_to_throttling() {
        let rt = tokio::runtime::Builder::new_current_thread()
            .build()
            .unwrap();

        let mut coordinator = MockLeaseCoordinator::new();
        coordinator
            .expect_get_currently_held_lease()
            .returning(|_| Some(make_lease("shard-1", "10")));
        coordinator
            .expect_worker_identifier()
            .returning(|| "w".to_string());
        coordinator
            .expect_update_lease()
            .returning(|_, _, _, _| Err(LeasingError::provisioned_throughput("throttled")));

        let checkpointer = DynamoDBCheckpointer::new(
            Arc::new(coordinator),
            Arc::new(MockLeaseRefresher::new()),
            rt.handle().clone(),
        );

        let err = checkpointer
            .set_checkpoint("shard-1", &esn("100"), &token().to_string())
            .unwrap_err();
        assert!(matches!(err, KinesisClientLibError::Throttling { .. }));
    }

    #[test]
    fn set_checkpoint_invalid_state_maps_to_invalid_state() {
        let rt = tokio::runtime::Builder::new_current_thread()
            .build()
            .unwrap();

        let mut coordinator = MockLeaseCoordinator::new();
        coordinator
            .expect_get_currently_held_lease()
            .returning(|_| Some(make_lease("shard-1", "10")));
        coordinator
            .expect_worker_identifier()
            .returning(|| "w".to_string());
        coordinator
            .expect_update_lease()
            .returning(|_, _, _, _| Err(LeasingError::invalid_state("table gone")));

        let checkpointer = DynamoDBCheckpointer::new(
            Arc::new(coordinator),
            Arc::new(MockLeaseRefresher::new()),
            rt.handle().clone(),
        );

        let err = checkpointer
            .set_checkpoint("shard-1", &esn("100"), &token().to_string())
            .unwrap_err();
        assert!(matches!(err, KinesisClientLibError::InvalidState { .. }));
        assert_eq!(
            err.message(),
            "Unable to save checkpoint for shardId shard-1"
        );
    }

    #[test]
    fn set_checkpoint_dependency_maps_to_dependency() {
        let rt = tokio::runtime::Builder::new_current_thread()
            .build()
            .unwrap();

        let mut coordinator = MockLeaseCoordinator::new();
        coordinator
            .expect_get_currently_held_lease()
            .returning(|_| Some(make_lease("shard-1", "10")));
        coordinator
            .expect_worker_identifier()
            .returning(|| "w".to_string());
        coordinator
            .expect_update_lease()
            .returning(|_, _, _, _| Err(LeasingError::dependency("ddb down")));

        let checkpointer = DynamoDBCheckpointer::new(
            Arc::new(coordinator),
            Arc::new(MockLeaseRefresher::new()),
            rt.handle().clone(),
        );

        let err = checkpointer
            .set_checkpoint("shard-1", &esn("100"), &token().to_string())
            .unwrap_err();
        assert!(matches!(err, KinesisClientLibError::Dependency { .. }));
    }

    #[test]
    fn prepare_checkpoint_sets_pending_only() {
        let rt = tokio::runtime::Builder::new_current_thread()
            .build()
            .unwrap();

        let concurrency = token();
        let mut coordinator = MockLeaseCoordinator::new();
        coordinator
            .expect_get_currently_held_lease()
            .returning(|_| make_lease("shard-1", "10").into());
        coordinator
            .expect_worker_identifier()
            .returning(|| "w".to_string());
        coordinator
            .expect_update_lease()
            .withf(|lease, _tok, _op, _key| {
                // prepare sets only the pending checkpoint; the committed
                // checkpoint stays untouched.
                lease.pending_checkpoint() == Some(&esn("200"))
                    && lease.checkpoint() == Some(&esn("10"))
                    && lease.pending_checkpoint_state() == Some(b"state".as_slice())
            })
            .returning(|_, _, _, _| Ok(true));

        let checkpointer = DynamoDBCheckpointer::new(
            Arc::new(coordinator),
            Arc::new(MockLeaseRefresher::new()),
            rt.handle().clone(),
        );

        checkpointer
            .prepare_checkpoint_with_state(
                "shard-1",
                &esn("200"),
                &concurrency.to_string(),
                b"state",
            )
            .unwrap();
    }

    #[test]
    fn get_checkpoint_reads_via_refresher() {
        let rt = tokio::runtime::Builder::new_current_thread()
            .build()
            .unwrap();

        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_get_lease()
            .withf(|k| k == "shard-1")
            .returning(|_| Ok(Some(make_lease("shard-1", "42"))));

        let checkpointer = DynamoDBCheckpointer::new(
            Arc::new(MockLeaseCoordinator::new()),
            Arc::new(refresher),
            rt.handle().clone(),
        );

        assert_eq!(
            checkpointer.get_checkpoint("shard-1").unwrap(),
            Some(esn("42"))
        );
    }

    #[test]
    fn get_checkpoint_error_maps_to_io() {
        let rt = tokio::runtime::Builder::new_current_thread()
            .build()
            .unwrap();

        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_get_lease()
            .returning(|_| Err(LeasingError::dependency("ddb down")));

        let checkpointer = DynamoDBCheckpointer::new(
            Arc::new(MockLeaseCoordinator::new()),
            Arc::new(refresher),
            rt.handle().clone(),
        );

        let err = checkpointer.get_checkpoint("shard-1").unwrap_err();
        assert!(matches!(err, KinesisClientLibError::Io { .. }));
    }

    #[test]
    fn get_checkpoint_object_builds_checkpoint() {
        let rt = tokio::runtime::Builder::new_current_thread()
            .build()
            .unwrap();

        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_get_lease().returning(|_| {
            let mut lease = make_lease("shard-1", "42");
            lease.set_pending_checkpoint(Some(esn("99")));
            Ok(Some(lease))
        });

        let checkpointer = DynamoDBCheckpointer::new(
            Arc::new(MockLeaseCoordinator::new()),
            Arc::new(refresher),
            rt.handle().clone(),
        );

        let obj = checkpointer
            .get_checkpoint_object("shard-1")
            .unwrap()
            .unwrap();
        assert_eq!(obj.checkpoint(), &esn("42"));
        assert_eq!(obj.pending_checkpoint(), Some(&esn("99")));
    }

    #[test]
    fn operation_setter_and_getter() {
        let rt = tokio::runtime::Builder::new_current_thread()
            .build()
            .unwrap();
        let checkpointer = DynamoDBCheckpointer::new(
            Arc::new(MockLeaseCoordinator::new()),
            Arc::new(MockLeaseRefresher::new()),
            rt.handle().clone(),
        );
        assert_eq!(checkpointer.operation(), "");
        checkpointer.set_operation("ProcessTask");
        assert_eq!(checkpointer.operation(), "ProcessTask");
    }
}
