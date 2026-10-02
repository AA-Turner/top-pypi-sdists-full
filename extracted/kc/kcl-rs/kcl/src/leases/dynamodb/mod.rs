//! Port of `software.amazon.kinesis.leases.dynamodb` — the DynamoDB-backed
//! storage layer of the leasing subsystem (sub-wave 6d-1).
//!
//! This wave ports the **storage** classes only (serializers, refresher, table
//! DAO, discoverer, scan-segment resolver, table-creator callback). The
//! *coordination* impls (`DynamoDBLeaseCoordinator`/`Taker`/`Renewer` and
//! `DynamoDBLeaseManagementFactory`) are a separate wave.
//!
//! # Async I/O over a real `aws_sdk_dynamodb::Client`
//!
//! Java blocks on the `DynamoDbAsyncClient` futures via
//! `FutureUtils.resolveOrCancelFuture(future, timeout)` (a blocking
//! `future.get(timeout)` + cancel-on-timeout). The Rust port stays async: each
//! SDK call is `.await`ed under a `tokio::time::timeout` mirroring the
//! `dynamoDbRequestTimeout`. Conditional-write semantics (optimistic locking via
//! the lease counter), exception→[`LeasingError`](crate::leases::exceptions::LeasingError)
//! mapping, and backoff/retry loops are preserved 1:1.

pub mod dynamodb_lease_coordinator;
pub mod dynamodb_lease_discoverer;
pub mod dynamodb_lease_management_factory;
pub mod dynamodb_lease_refresher;
pub mod dynamodb_lease_renewer;
pub mod dynamodb_lease_serializer;
pub mod dynamodb_lease_table_dao;
pub mod dynamodb_lease_taker;
pub mod dynamodb_multi_stream_lease_serializer;
pub mod lease_table_scan_segment_resolver;
pub mod table_creator_callback;

#[cfg(test)]
pub(crate) mod test_support;

pub use dynamodb_lease_coordinator::DynamoDBLeaseCoordinator;
pub use dynamodb_lease_discoverer::DynamoDBLeaseDiscoverer;
pub use dynamodb_lease_management_factory::DynamoDBLeaseManagementFactory;
pub use dynamodb_lease_refresher::{DynamoDBLeaseRefresher, RefresherTableConfig};
pub use dynamodb_lease_renewer::DynamoDBLeaseRenewer;
pub use dynamodb_lease_serializer::{DynamoDBLeaseSerializer, LEASE_KEY_KEY};
pub use dynamodb_lease_table_dao::DynamoDBLeaseTableDao;
pub use dynamodb_lease_taker::DynamoDBLeaseTaker;
pub use dynamodb_multi_stream_lease_serializer::DynamoDBMultiStreamLeaseSerializer;
pub use lease_table_scan_segment_resolver::{
    LeaseTableScanSegmentResolver, TableDescriber, DEFAULT_LEASE_TABLE_SCAN_PARALLELISM_FACTOR,
};
pub use table_creator_callback::{
    NoopTableCreatorCallback, TableCreatorCallback, TableCreatorCallbackInput,
};
