//! Port of `software.amazon.kinesis.leases.dynamodb.DynamoDBLeaseRefresher`.
//!
//! The low-level DynamoDB DAO for the lease table: table lifecycle
//! (create/describe/wait-active/PITR/GSI) and all per-lease CRUD/CAS operations
//! (get/list/scan/create/renew/take/assign/evict/update/delete) using optimistic
//! concurrency via DynamoDB conditional expressions on `leaseCounter`.
//!
//! # Async translation
//!
//! Java blocks on `DynamoDbAsyncClient` futures via
//! `FutureUtils.resolveOrCancelFuture(future, timeout)`. Rust `.await`s each SDK
//! call under a `tokio::time::timeout` (`dynamo_db_request_timeout`); a timeout
//! maps to [`LeasingError::Dependency`] (Java wraps `TimeoutException` in
//! `DependencyException`).
//!
//! # Exception mapping (`AWSExceptionManager` semantics per call site)
//!
//! - `ConditionalCheckFailedException` → the write returns `false` (lost the CAS),
//!   never an error.
//! - `ProvisionedThroughputExceededException` → [`LeasingError::ProvisionedThroughput`].
//! - `ResourceNotFoundException` (on a mutation) → [`LeasingError::InvalidState`]
//!   ("...because table ... does not exist").
//! - `ResourceInUseException` (on createTable) → treated as "table already exists".
//! - `LimitExceededException` (on createTable) → [`LeasingError::ProvisionedThroughput`].
//! - anything else → [`LeasingError::Dependency`].
//!
//! # Graceful lease handoff
//!
//! `renew_lease` reproduces the full state machine: a `checkpointOwner`-not-exists
//! expectation on the steady-state renewal, the `handle_graceful_shutdown`
//! recursive retry, and the "spurious retry" false-negative recovery (re-fetch
//! and compare owner+counter to what a successful update would produce).

use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::time::Duration;

use async_trait::async_trait;
use aws_sdk_dynamodb::types::{
    AttributeAction, AttributeValue, AttributeValueUpdate, BillingMode,
    CreateGlobalSecondaryIndexAction, ExpectedAttributeValue, GlobalSecondaryIndexUpdate,
    IndexStatus, Projection, ProjectionType, ProvisionedThroughput, ReturnValue,
    ReturnValuesOnConditionCheckFailure, TableStatus, Tag,
};
use aws_sdk_dynamodb::Client;
use tokio::sync::Mutex;

use crate::common::StreamIdentifier;
use crate::leases::dynamo_utils::create_attribute_value_string;
use crate::leases::dynamodb::dynamodb_lease_serializer::{
    CHECKPOINT_OWNER, LEASE_KEY_KEY, LEASE_OWNER_KEY,
};
use crate::leases::dynamodb::lease_table_scan_segment_resolver::{
    LeaseTableScanSegmentResolver, TableDescriber,
};
use crate::leases::dynamodb::table_creator_callback::{
    TableCreatorCallback, TableCreatorCallbackInput,
};
use crate::leases::exceptions::LeasingError;
use crate::leases::{Lease, LeaseRefresher, LeaseSerializer, UpdateField};
use crate::retrieval::kpl::ExtendedSequenceNumber;

pub(crate) const LEASE_OWNER_TO_LEASE_KEY_INDEX_NAME: &str = "LeaseOwnerToLeaseKeyIndex";
const STREAM_NAME: &str = "streamName";
const DDB_STREAM_NAME: &str = ":streamName";
const DDB_LEASE_OWNER: &str = ":leaseOwner";

/// Billing-mode + capacity config for the lease table (Java `DdbTableConfig`).
///
/// The common-wave `DdbTableConfig` isn't fully ported yet; this is a minimal
/// local config carrying just what the refresher needs (billing mode + RCU/WCU).
#[derive(Debug, Clone)]
pub struct RefresherTableConfig {
    /// Billing mode (default `PAY_PER_REQUEST`).
    pub billing_mode: BillingMode,
    /// Read capacity (PROVISIONED mode).
    pub read_capacity: i64,
    /// Write capacity (PROVISIONED mode).
    pub write_capacity: i64,
}

impl Default for RefresherTableConfig {
    fn default() -> Self {
        Self {
            billing_mode: BillingMode::PayPerRequest,
            read_capacity: 10,
            write_capacity: 10,
        }
    }
}

/// DynamoDB implementation of [`LeaseRefresher`].
pub struct DynamoDBLeaseRefresher {
    table: String,
    dynamo_db_client: Client,
    serializer: Arc<dyn LeaseSerializer + Send + Sync>,
    consistent_reads: bool,
    table_creator_callback: Arc<dyn TableCreatorCallback>,
    dynamo_db_request_timeout: Duration,
    ddb_table_config: RefresherTableConfig,
    lease_table_deletion_protection_enabled: bool,
    lease_table_pitr_enabled: bool,
    tags: Vec<Tag>,
    /// In-memory "did *this* instance create the table" flag (Java `newTableCreated`).
    new_table_created: AtomicBool,
    scan_segment_resolver: LeaseTableScanSegmentResolver,
    /// Test seam: overrides `sleep(ms)` (Java's overridable sleep). Set only in tests.
    sleep_override: Mutex<Option<Duration>>,
}

impl DynamoDBLeaseRefresher {
    /// Construct a refresher. Mirrors the Java 10-arg constructor.
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        table: impl Into<String>,
        dynamo_db_client: Client,
        serializer: Arc<dyn LeaseSerializer + Send + Sync>,
        consistent_reads: bool,
        table_creator_callback: Arc<dyn TableCreatorCallback>,
        dynamo_db_request_timeout: Duration,
        ddb_table_config: RefresherTableConfig,
        lease_table_deletion_protection_enabled: bool,
        lease_table_pitr_enabled: bool,
        tags: Vec<Tag>,
    ) -> Self {
        let table = table.into();
        // Java constructs `new LeaseTableScanSegmentResolver(0, this::describeLeaseTable)` —
        // always dynamic sizing for the refresher. We build a describer closure
        // bound to the same client + table.
        let describer = Self::make_table_describer(
            dynamo_db_client.clone(),
            table.clone(),
            dynamo_db_request_timeout,
        );
        Self {
            table,
            dynamo_db_client,
            serializer,
            consistent_reads,
            table_creator_callback,
            dynamo_db_request_timeout,
            ddb_table_config,
            lease_table_deletion_protection_enabled,
            lease_table_pitr_enabled,
            tags,
            new_table_created: AtomicBool::new(false),
            scan_segment_resolver: LeaseTableScanSegmentResolver::new(0, describer),
            sleep_override: Mutex::new(None),
        }
    }

    fn make_table_describer(client: Client, table: String, timeout: Duration) -> TableDescriber {
        Arc::new(move || {
            let client = client.clone();
            let table = table.clone();
            Box::pin(async move {
                let fut = client.describe_table().table_name(&table).send();
                match tokio::time::timeout(timeout, fut).await {
                    Err(_) => Err(LeasingError::dependency("Timed out describing table")),
                    Ok(Ok(resp)) => Ok(Some(resp)),
                    Ok(Err(sdk_err)) => {
                        let e = sdk_err.into_service_error();
                        if e.is_resource_not_found_exception() {
                            Ok(None)
                        } else {
                            Err(LeasingError::dependency_caused_by(
                                "describeTable failed",
                                Box::new(e),
                            ))
                        }
                    }
                }
            })
        })
    }

    /// The table name (used by the DAO / tests).
    pub fn table_name(&self) -> &str {
        &self.table
    }

    /// Test seam: set the sleep duration used by `wait_until_lease_table_exists`
    /// polling (Java's overridable `sleep(ms)`).
    #[cfg(test)]
    pub async fn set_sleep_override(&self, d: Duration) {
        *self.sleep_override.lock().await = Some(d);
    }

    async fn sleep(&self, requested: Duration) {
        let d = { self.sleep_override.lock().await.unwrap_or(requested) };
        tokio::time::sleep(d).await;
    }

    // --- describe / status ---

    /// Java `describeLeaseTable()`: returns `Ok(None)` on ResourceNotFound.
    async fn describe_lease_table(
        &self,
    ) -> Result<
        Option<aws_sdk_dynamodb::operation::describe_table::DescribeTableOutput>,
        LeasingError,
    > {
        let fut = self
            .dynamo_db_client
            .describe_table()
            .table_name(&self.table)
            .send();
        match tokio::time::timeout(self.dynamo_db_request_timeout, fut).await {
            Err(_) => Err(LeasingError::dependency("Timed out describing lease table")),
            Ok(Ok(resp)) => Ok(Some(resp)),
            Ok(Err(sdk_err)) => {
                let e = sdk_err.into_service_error();
                if e.is_resource_not_found_exception() {
                    Ok(None)
                } else {
                    Err(LeasingError::dependency_caused_by(
                        "describeTable failed",
                        Box::new(e),
                    ))
                }
            }
        }
    }

    fn is_table_in_pay_per_request_mode(
        resp: &aws_sdk_dynamodb::operation::describe_table::DescribeTableOutput,
    ) -> bool {
        resp.table()
            .and_then(|t| t.billing_mode_summary())
            .and_then(|b| b.billing_mode())
            .map(|m| *m == BillingMode::PayPerRequest)
            .unwrap_or(false)
    }

    fn index_status_from_table(
        table: Option<&aws_sdk_dynamodb::types::TableDescription>,
        index_name: &str,
    ) -> Option<IndexStatus> {
        table?
            .global_secondary_indexes()
            .iter()
            .find(|idx| idx.index_name() == Some(index_name))
            .and_then(|idx| idx.index_status().cloned())
    }

    // --- create table ---

    fn build_create_table_request(
        &self,
        table_config: &RefresherTableConfig,
    ) -> aws_sdk_dynamodb::operation::create_table::builders::CreateTableFluentBuilder {
        let mut builder = self
            .dynamo_db_client
            .create_table()
            .table_name(&self.table)
            .set_key_schema(Some(self.serializer.get_key_schema()))
            .set_attribute_definitions(Some(self.serializer.get_attribute_definitions()))
            .deletion_protection_enabled(self.lease_table_deletion_protection_enabled)
            .set_tags(if self.tags.is_empty() {
                None
            } else {
                Some(self.tags.clone())
            });
        if table_config.billing_mode == BillingMode::PayPerRequest {
            builder = builder.billing_mode(BillingMode::PayPerRequest);
        } else {
            builder = builder
                .billing_mode(BillingMode::Provisioned)
                .provisioned_throughput(
                    ProvisionedThroughput::builder()
                        .read_capacity_units(table_config.read_capacity)
                        .write_capacity_units(table_config.write_capacity)
                        .build()
                        .expect("valid provisioned throughput"),
                );
        }
        builder
    }

    /// Java `createTableIfNotExists(request)`.
    async fn create_table_if_not_exists(
        &self,
        table_config: &RefresherTableConfig,
    ) -> Result<bool, LeasingError> {
        // If the table already exists, return the current newTableCreated flag.
        match self.describe_lease_table().await {
            Ok(Some(_)) => return Ok(self.new_table_created.load(Ordering::SeqCst)),
            Ok(None) => {}
            Err(_e) => {
                // Java logs and continues (attempts create anyway).
            }
        }

        let builder = self.build_create_table_request(table_config);
        let fut = builder.send();
        match tokio::time::timeout(self.dynamo_db_request_timeout, fut).await {
            Err(_) => Err(LeasingError::dependency("Timed out creating table")),
            Ok(Ok(_)) => {
                self.new_table_created.store(true, Ordering::SeqCst);
                Ok(self.new_table_created.load(Ordering::SeqCst))
            }
            Ok(Err(sdk_err)) => {
                let e = sdk_err.into_service_error();
                if e.is_resource_in_use_exception() {
                    // Table already exists.
                    Ok(self.new_table_created.load(Ordering::SeqCst))
                } else if e.is_limit_exceeded_exception() {
                    Err(LeasingError::provisioned_throughput_caused_by(
                        format!("Capacity exceeded when creating table {}", self.table),
                        Box::new(e),
                    ))
                } else {
                    Err(LeasingError::dependency_caused_by(
                        "createTable failed",
                        Box::new(e),
                    ))
                }
            }
        }
    }

    async fn enable_pitr(&self) -> Result<(), LeasingError> {
        let fut = self
            .dynamo_db_client
            .update_continuous_backups()
            .table_name(&self.table)
            .point_in_time_recovery_specification(
                aws_sdk_dynamodb::types::PointInTimeRecoverySpecification::builder()
                    .point_in_time_recovery_enabled(true)
                    .build()
                    .expect("valid PITR spec"),
            )
            .send();
        match tokio::time::timeout(self.dynamo_db_request_timeout, fut).await {
            Err(_) => Err(LeasingError::dependency("Timed out enabling PITR")),
            Ok(Ok(_)) => Ok(()),
            Ok(Err(sdk_err)) => Err(LeasingError::dependency_caused_by(
                "updateContinuousBackups failed",
                Box::new(sdk_err.into_service_error()),
            )),
        }
    }

    /// Java `performPostTableCreationAction()` — fires the callback once.
    async fn perform_post_table_creation_action(&self) {
        let input = TableCreatorCallbackInput::builder()
            .dynamo_db_client(self.dynamo_db_client.clone())
            .table_name(self.table.clone())
            .build();
        self.table_creator_callback.perform_action(&input);
    }

    // --- scan / list ---

    /// Java `list(limit, streamIdentifier)`: single (non-parallel) paginated scan.
    async fn list(
        &self,
        limit: Option<i32>,
        stream_identifier: Option<&StreamIdentifier>,
    ) -> Result<Vec<Lease>, LeasingError> {
        let effective_limit = limit.map(|l| l as usize).unwrap_or(usize::MAX);
        let mut result: Vec<Lease> = Vec::new();
        let mut last_evaluated_key: Option<HashMap<String, AttributeValue>> = None;

        loop {
            let mut builder = self.dynamo_db_client.scan().table_name(&self.table);
            if let Some(sid) = stream_identifier {
                builder = builder
                    .filter_expression(format!("{STREAM_NAME} = {DDB_STREAM_NAME}"))
                    .expression_attribute_values(
                        DDB_STREAM_NAME,
                        AttributeValue::S(sid.serialize()),
                    );
            }
            if let Some(k) = &last_evaluated_key {
                builder = builder.set_exclusive_start_key(Some(k.clone()));
            }

            let scan_result = self.send_scan(builder).await?;

            for item in scan_result.items() {
                if let Some(lease) = self.deserialize_lease(item) {
                    result.push(lease);
                }
                if result.len() >= effective_limit {
                    break;
                }
            }

            last_evaluated_key = scan_result.last_evaluated_key().cloned();
            let has_more = last_evaluated_key
                .as_ref()
                .map(|m| !m.is_empty())
                .unwrap_or(false);
            if !has_more || result.len() >= effective_limit {
                break;
            }
        }
        Ok(result)
    }

    async fn send_scan(
        &self,
        builder: aws_sdk_dynamodb::operation::scan::builders::ScanFluentBuilder,
    ) -> Result<aws_sdk_dynamodb::operation::scan::ScanOutput, LeasingError> {
        let fut = builder.send();
        match tokio::time::timeout(self.dynamo_db_request_timeout, fut).await {
            Err(_) => Err(LeasingError::dependency("Timed out during scan")),
            Ok(Ok(resp)) => Ok(resp),
            Ok(Err(sdk_err)) => {
                let e = sdk_err.into_service_error();
                if e.is_resource_not_found_exception() {
                    Err(LeasingError::invalid_state_caused_by(
                        format!(
                            "Cannot scan lease table {} because it does not exist.",
                            self.table
                        ),
                        Box::new(e),
                    ))
                } else if e.is_provisioned_throughput_exceeded_exception() {
                    Err(LeasingError::provisioned_throughput_caused_by(
                        "scan throttled",
                        Box::new(e),
                    ))
                } else {
                    Err(LeasingError::dependency_caused_by(
                        "scan failed",
                        Box::new(e),
                    ))
                }
            }
        }
    }

    /// Deserialize a scanned item into a `Lease`, or `None` if it's a non-lease
    /// entity or fails to deserialize (Java swallows the exception + logs).
    fn deserialize_lease(&self, item: &HashMap<String, AttributeValue>) -> Option<Lease> {
        let mut lease = Lease::default();
        // The serializer returns a default (empty) Lease for non-lease records;
        // we detect that via lease_key being unset (Java returns null).
        let is_lease = match self.serializer.from_dynamo_record_into(item, &mut lease) {
            Ok(()) => lease.lease_key().is_some(),
            Err(_) => false,
        };
        if is_lease {
            Some(lease)
        } else {
            None
        }
    }

    /// Java `scanSegment(segment, totalSegments, ...)` — fully paginated scan of
    /// one segment. Returns `(leases, failed_deserialize_keys)`.
    async fn scan_segment(
        &self,
        segment: i32,
        total_segments: i32,
    ) -> Result<(Vec<Lease>, Vec<String>), LeasingError> {
        let mut leases = Vec::new();
        let mut failed = Vec::new();
        let mut last_evaluated_key: Option<HashMap<String, AttributeValue>> = None;

        loop {
            let mut builder = self
                .dynamo_db_client
                .scan()
                .table_name(&self.table)
                .segment(segment)
                .total_segments(total_segments);
            if let Some(k) = &last_evaluated_key {
                builder = builder.set_exclusive_start_key(Some(k.clone()));
            }
            let scan_result = self.send_scan_segment(builder).await?;
            for item in scan_result.items() {
                match self.deserialize_lease(item) {
                    Some(lease) => leases.push(lease),
                    None => {
                        // A genuine deserialization failure records the key; a
                        // non-lease entity produces None too, but in the
                        // parallel path (used only on the pure lease table) all
                        // records are leases. To match Java, only record a
                        // failure key when the record HAS a leaseKey but didn't
                        // become a lease (i.e. would-be-lease that failed).
                        if let Some(k) = item.get(LEASE_KEY_KEY).and_then(|v| v.as_s().ok()) {
                            failed.push(k.clone());
                        }
                    }
                }
            }
            last_evaluated_key = scan_result.last_evaluated_key().cloned();
            let has_more = last_evaluated_key
                .as_ref()
                .map(|m| !m.is_empty())
                .unwrap_or(false);
            if !has_more {
                break;
            }
        }
        Ok((leases, failed))
    }

    async fn send_scan_segment(
        &self,
        builder: aws_sdk_dynamodb::operation::scan::builders::ScanFluentBuilder,
    ) -> Result<aws_sdk_dynamodb::operation::scan::ScanOutput, LeasingError> {
        let fut = builder.send();
        match tokio::time::timeout(self.dynamo_db_request_timeout, fut).await {
            Err(_) => Err(LeasingError::dependency("Timed out during segment scan")),
            Ok(Ok(resp)) => Ok(resp),
            Ok(Err(sdk_err)) => {
                let e = sdk_err.into_service_error();
                if e.is_resource_not_found_exception() {
                    Err(LeasingError::invalid_state_caused_by(
                        format!(
                            "Cannot scan lease table {} because it does not exist.",
                            self.table
                        ),
                        Box::new(e),
                    ))
                } else if e.is_provisioned_throughput_exceeded_exception() {
                    Err(LeasingError::provisioned_throughput_caused_by(
                        "segment scan throttled",
                        Box::new(e),
                    ))
                } else {
                    Err(LeasingError::dependency_caused_by(
                        "segment scan failed",
                        Box::new(e),
                    ))
                }
            }
        }
    }

    // --- update-item helper ---

    /// Send an updateItem, returning `Ok(Some(response))` on success,
    /// `Ok(None)` on a ConditionalCheckFailed, or an error otherwise. `operation`
    /// is used for the error message (Java `convertAndRethrowExceptions`).
    async fn send_update_item(
        &self,
        builder: aws_sdk_dynamodb::operation::update_item::builders::UpdateItemFluentBuilder,
        operation: &str,
        lease_key: &str,
    ) -> Result<Option<aws_sdk_dynamodb::operation::update_item::UpdateItemOutput>, LeasingError>
    {
        let fut = builder.send();
        match tokio::time::timeout(self.dynamo_db_request_timeout, fut).await {
            Err(_) => Err(LeasingError::dependency("Timed out during updateItem")),
            Ok(Ok(resp)) => Ok(Some(resp)),
            Ok(Err(sdk_err)) => {
                let e = sdk_err.into_service_error();
                if e.is_conditional_check_failed_exception() {
                    Ok(None)
                } else {
                    Err(self.convert_and_rethrow(operation, lease_key, e))
                }
            }
        }
    }

    /// Java `convertAndRethrowExceptions`, given a pre-classified error kind.
    /// Matches Java's `AWSExceptionManager` typed dispatch:
    /// - `ProvisionedThroughputExceeded` → `ProvisionedThroughput`
    /// - `ResourceNotFound` → `InvalidState` (table does not exist)
    /// - `Other` → `Dependency`.
    ///
    /// Classification is done at each call site via the SDK's typed
    /// `is_*_exception()` helpers (the mock harness does not populate the generic
    /// error-code metadata, so we must not rely on `ProvideErrorMetadata::code()`).
    fn convert_and_rethrow<E>(&self, operation: &str, lease_key: &str, err: E) -> LeasingError
    where
        E: MutationError + std::error::Error + Send + Sync + 'static,
    {
        if err.is_provisioned_throughput_exceeded() {
            LeasingError::provisioned_throughput_caused_by(
                "Provisioned Throughput on the lease table has been exceeded.",
                Box::new(err),
            )
        } else if err.is_resource_not_found() {
            LeasingError::invalid_state_caused_by(
                format!(
                    "Cannot {operation} lease with key {lease_key} because table {} does not exist.",
                    self.table
                ),
                Box::new(err),
            )
        } else {
            LeasingError::dependency_caused_by(format!("{operation} failed"), Box::new(err))
        }
    }
}

/// Classifies a DynamoDB service error for [`DynamoDBLeaseRefresher::convert_and_rethrow`]
/// via the SDK's typed variant checks (`is_*_exception()`).
trait MutationError {
    fn is_provisioned_throughput_exceeded(&self) -> bool;
    fn is_resource_not_found(&self) -> bool;
}

macro_rules! impl_mutation_error {
    ($ty:ty) => {
        impl MutationError for $ty {
            fn is_provisioned_throughput_exceeded(&self) -> bool {
                self.is_provisioned_throughput_exceeded_exception()
            }
            fn is_resource_not_found(&self) -> bool {
                self.is_resource_not_found_exception()
            }
        }
    };
}

impl_mutation_error!(aws_sdk_dynamodb::operation::put_item::PutItemError);
impl_mutation_error!(aws_sdk_dynamodb::operation::get_item::GetItemError);
impl_mutation_error!(aws_sdk_dynamodb::operation::update_item::UpdateItemError);
impl_mutation_error!(aws_sdk_dynamodb::operation::delete_item::DeleteItemError);

#[async_trait]
impl LeaseRefresher for DynamoDBLeaseRefresher {
    async fn create_lease_table_if_not_exists_with_capacity(
        &self,
        read_capacity: i64,
        write_capacity: i64,
    ) -> Result<bool, LeasingError> {
        // Always PROVISIONED with the given RCU/WCU; does NOT enable PITR (asymmetry preserved).
        let config = RefresherTableConfig {
            billing_mode: BillingMode::Provisioned,
            read_capacity,
            write_capacity,
        };
        self.create_table_if_not_exists(&config).await
    }

    async fn create_lease_table_if_not_exists(&self) -> Result<bool, LeasingError> {
        let config = self.ddb_table_config.clone();
        let table_exists = self.create_table_if_not_exists(&config).await?;
        if self.lease_table_pitr_enabled {
            self.enable_pitr().await?;
        }
        Ok(table_exists)
    }

    async fn lease_table_exists(&self) -> Result<bool, LeasingError> {
        let status = match self.describe_lease_table().await? {
            Some(resp) => resp.table().and_then(|t| t.table_status().cloned()),
            None => None,
        };
        Ok(matches!(
            status,
            Some(TableStatus::Active) | Some(TableStatus::Updating)
        ))
    }

    async fn wait_until_lease_table_exists(
        &self,
        seconds_between_polls: i64,
        timeout_seconds: i64,
    ) -> Result<bool, LeasingError> {
        let mut sleep_time_remaining_ms = timeout_seconds * 1000;
        while !self.lease_table_exists().await? {
            if sleep_time_remaining_ms <= 0 {
                return Ok(false);
            }
            let time_to_sleep_ms = (seconds_between_polls * 1000).min(sleep_time_remaining_ms);
            let start = std::time::Instant::now();
            self.sleep(Duration::from_millis(time_to_sleep_ms as u64))
                .await;
            sleep_time_remaining_ms -= start.elapsed().as_millis() as i64;
        }
        if self.new_table_created.load(Ordering::SeqCst) {
            self.perform_post_table_creation_action().await;
        }
        Ok(true)
    }

    async fn create_lease_owner_to_lease_key_index_if_not_exists(
        &self,
    ) -> Result<Option<String>, LeasingError> {
        let describe = self.describe_lease_table().await?;
        let mut provisioned_throughput: Option<ProvisionedThroughput> = None;
        if let Some(resp) = &describe {
            if !Self::is_table_in_pay_per_request_mode(resp) {
                if let Some(pt) = resp.table().and_then(|t| t.provisioned_throughput()) {
                    provisioned_throughput = ProvisionedThroughput::builder()
                        .read_capacity_units(pt.read_capacity_units().unwrap_or(0))
                        .write_capacity_units(pt.write_capacity_units().unwrap_or(0))
                        .build()
                        .ok();
                }
            }
            if let Some(status) =
                Self::index_status_from_table(resp.table(), LEASE_OWNER_TO_LEASE_KEY_INDEX_NAME)
            {
                return Ok(Some(status.to_string()));
            }
        }

        let gsi_action = CreateGlobalSecondaryIndexAction::builder()
            .index_name(LEASE_OWNER_TO_LEASE_KEY_INDEX_NAME)
            .set_key_schema(Some(
                self.serializer
                    .get_worker_id_to_lease_key_index_key_schema(),
            ))
            .projection(
                Projection::builder()
                    .projection_type(ProjectionType::KeysOnly)
                    .build(),
            )
            .set_provisioned_throughput(provisioned_throughput)
            .build()
            .map_err(|e| LeasingError::dependency_caused_by("invalid GSI action", Box::new(e)))?;

        let fut = self
            .dynamo_db_client
            .update_table()
            .table_name(&self.table)
            .set_attribute_definitions(Some(
                self.serializer
                    .get_worker_id_to_lease_key_index_attribute_definitions(),
            ))
            .global_secondary_index_updates(
                GlobalSecondaryIndexUpdate::builder()
                    .create(gsi_action)
                    .build(),
            )
            .send();
        match tokio::time::timeout(self.dynamo_db_request_timeout, fut).await {
            Err(_) => Err(LeasingError::dependency("Timed out creating GSI")),
            Ok(Ok(resp)) => {
                let status = Self::index_status_from_table(
                    resp.table_description(),
                    LEASE_OWNER_TO_LEASE_KEY_INDEX_NAME,
                );
                Ok(status.map(|s| s.to_string()))
            }
            Ok(Err(sdk_err)) => Err(LeasingError::dependency_caused_by(
                "updateTable(GSI) failed",
                Box::new(sdk_err.into_service_error()),
            )),
        }
    }

    async fn wait_until_lease_owner_to_lease_key_index_exists(
        &self,
        seconds_between_polls: i64,
        timeout_seconds: i64,
    ) -> bool {
        let start = std::time::Instant::now();
        let timeout = Duration::from_secs(timeout_seconds.max(0) as u64);
        while start.elapsed() < timeout {
            if let Ok(true) = self.is_lease_owner_to_lease_key_index_active().await {
                return true;
            }
            self.sleep(Duration::from_secs(seconds_between_polls.max(0) as u64))
                .await;
        }
        false
    }

    async fn is_lease_owner_to_lease_key_index_active(&self) -> Result<bool, LeasingError> {
        let describe = self.describe_lease_table().await?;
        let status = describe.as_ref().and_then(|r| {
            Self::index_status_from_table(r.table(), LEASE_OWNER_TO_LEASE_KEY_INDEX_NAME)
        });
        Ok(status == Some(IndexStatus::Active))
    }

    async fn list_leases_for_stream(
        &self,
        stream_identifier: &StreamIdentifier,
    ) -> Result<Vec<Lease>, LeasingError> {
        self.list(None, Some(stream_identifier)).await
    }

    async fn list_lease_keys_for_worker(
        &self,
        worker_identifier: &str,
    ) -> Result<Vec<String>, LeasingError> {
        let mut result = Vec::new();
        let mut exclusive_start_key: Option<HashMap<String, AttributeValue>> = None;
        loop {
            let mut builder = self
                .dynamo_db_client
                .query()
                .index_name(LEASE_OWNER_TO_LEASE_KEY_INDEX_NAME)
                .key_condition_expression(format!("{LEASE_OWNER_KEY} = {DDB_LEASE_OWNER}"))
                .expression_attribute_values(
                    DDB_LEASE_OWNER,
                    AttributeValue::S(worker_identifier.to_string()),
                )
                .table_name(&self.table);
            if let Some(k) = &exclusive_start_key {
                builder = builder.set_exclusive_start_key(Some(k.clone()));
            }
            let fut = builder.send();
            let resp = match tokio::time::timeout(self.dynamo_db_request_timeout, fut).await {
                Err(_) => return Err(LeasingError::dependency("Timed out during query")),
                Ok(Ok(resp)) => resp,
                Ok(Err(sdk_err)) => {
                    let e = sdk_err.into_service_error();
                    if e.is_resource_not_found_exception() {
                        return Err(LeasingError::invalid_state_caused_by(
                            format!("{LEASE_OWNER_TO_LEASE_KEY_INDEX_NAME} does not exists."),
                            Box::new(e),
                        ));
                    }
                    return Err(LeasingError::dependency_caused_by(
                        "query failed",
                        Box::new(e),
                    ));
                }
            };
            for item in resp.items() {
                if let Some(k) = item.get(LEASE_KEY_KEY).and_then(|v| v.as_s().ok()) {
                    result.push(k.clone());
                }
            }
            let last = resp.last_evaluated_key();
            match last {
                Some(m) if !m.is_empty() => exclusive_start_key = Some(m.clone()),
                _ => break,
            }
        }
        Ok(result)
    }

    async fn list_leases(&self) -> Result<Vec<Lease>, LeasingError> {
        self.list(None, None).await
    }

    async fn list_leases_parallely(
        &self,
        parallelism_factor: i32,
    ) -> Result<(Vec<Lease>, Vec<String>), LeasingError> {
        let total_segments = if parallelism_factor > 0 {
            parallelism_factor
        } else {
            self.scan_segment_resolver.resolve_total_segments().await
        };

        let mut all_leases = Vec::new();
        let mut all_failed = Vec::new();
        // Scan each segment. (Java fans out on an ExecutorService and joins; we
        // await each segment sequentially — the SDK client is shared and each
        // segment is independent, so behavior is equivalent, and we avoid
        // spawning to keep &self borrow-safe. The number of scan calls is
        // preserved for test parity.)
        for segment in 0..total_segments {
            let (leases, failed) = self.scan_segment(segment, total_segments).await?;
            all_leases.extend(leases);
            all_failed.extend(failed);
        }
        Ok((all_leases, all_failed))
    }

    async fn create_lease_if_not_exists(&self, lease: &Lease) -> Result<bool, LeasingError> {
        let fut = self
            .dynamo_db_client
            .put_item()
            .table_name(&self.table)
            .set_item(Some(self.serializer.to_dynamo_record(lease)))
            .set_expected(Some(self.serializer.get_dynamo_nonexistant_expectation()))
            .send();
        match tokio::time::timeout(self.dynamo_db_request_timeout, fut).await {
            Err(_) => Err(LeasingError::dependency("Timed out during putItem")),
            Ok(Ok(_)) => Ok(true),
            Ok(Err(sdk_err)) => {
                let e = sdk_err.into_service_error();
                if e.is_conditional_check_failed_exception() {
                    Ok(false)
                } else {
                    Err(self.convert_and_rethrow("create", lease.lease_key().unwrap_or(""), e))
                }
            }
        }
    }

    async fn get_lease(&self, lease_key: &str) -> Result<Option<Lease>, LeasingError> {
        let fut = self
            .dynamo_db_client
            .get_item()
            .table_name(&self.table)
            .set_key(Some(
                self.serializer.get_dynamo_hash_key_from_key(lease_key),
            ))
            .consistent_read(self.consistent_reads)
            .send();
        match tokio::time::timeout(self.dynamo_db_request_timeout, fut).await {
            Err(_) => Err(LeasingError::dependency("Timed out during getItem")),
            Ok(Ok(resp)) => {
                let item = resp.item();
                match item {
                    Some(record) if !record.is_empty() => {
                        Ok(Some(self.serializer.from_dynamo_record(record)))
                    }
                    _ => Ok(None),
                }
            }
            Ok(Err(sdk_err)) => {
                Err(self.convert_and_rethrow("get", lease_key, sdk_err.into_service_error()))
            }
        }
    }

    async fn renew_lease(&self, lease: &mut Lease) -> Result<bool, LeasingError> {
        let mut attribute_updates: HashMap<String, AttributeValueUpdate> =
            self.serializer.get_dynamo_lease_counter_update(lease);
        if lease.throughput_kbps().is_some() {
            attribute_updates.extend(
                self.serializer
                    .get_dynamo_lease_throughput_kbps_update(lease),
            );
        }
        let mut expected = self.serializer.get_dynamo_lease_counter_expectation(lease);
        if !lease.shutdown_requested() {
            expected.insert(
                CHECKPOINT_OWNER.to_string(),
                ExpectedAttributeValue::builder().exists(false).build(),
            );
        }

        let builder = self
            .dynamo_db_client
            .update_item()
            .table_name(&self.table)
            .set_key(Some(self.serializer.get_dynamo_hash_key(lease)))
            .set_expected(Some(expected))
            .set_attribute_updates(Some(attribute_updates))
            .return_values_on_condition_check_failure(ReturnValuesOnConditionCheckFailure::AllOld);

        match self
            .send_update_item(builder, "renew", lease.lease_key().unwrap_or(""))
            .await?
        {
            Some(_) => {
                lease.set_lease_counter(lease.lease_counter() + 1);
                Ok(true)
            }
            None => {
                // Conditional check failed.
                if !lease.shutdown_requested() {
                    // We can't retrieve e.item() from the mock easily, so (like
                    // Java's ddblocal workaround) fetch the DDB lease.
                    let ddb_lease = self.get_lease(lease.lease_key().unwrap_or("")).await?;
                    if let Some(ddb) = &ddb_lease {
                        if ddb.shutdown_requested() {
                            return self.handle_graceful_shutdown(lease, ddb).await;
                        }
                    }
                    // Spurious-retry detection: if the DDB lease now reflects what
                    // a successful update would have produced, treat as success.
                    let expected_owner = lease.actual_owner().map(str::to_string);
                    let expected_counter = lease.lease_counter() + 1;
                    match ddb_lease {
                        None => return Ok(false),
                        Some(updated) => {
                            if updated.lease_owner().map(str::to_string) != expected_owner
                                || updated.lease_counter() != expected_counter
                            {
                                return Ok(false);
                            }
                            // Recovered from a spurious failure.
                        }
                    }
                    lease.set_lease_counter(lease.lease_counter() + 1);
                    Ok(true)
                } else {
                    Ok(false)
                }
            }
        }
    }

    async fn take_lease(&self, lease: &mut Lease, owner: &str) -> Result<bool, LeasingError> {
        let old_owner = lease.lease_owner().map(str::to_string);
        let mut updates = self.serializer.get_dynamo_lease_counter_update(lease);
        updates.extend(self.serializer.get_dynamo_take_lease_update(lease, owner));
        let builder = self
            .dynamo_db_client
            .update_item()
            .table_name(&self.table)
            .set_key(Some(self.serializer.get_dynamo_hash_key(lease)))
            .set_expected(Some(
                self.serializer.get_dynamo_lease_counter_expectation(lease),
            ))
            .set_attribute_updates(Some(updates));

        match self
            .send_update_item(builder, "take", lease.lease_key().unwrap_or(""))
            .await?
        {
            None => Ok(false),
            Some(_) => {
                lease.set_lease_counter(lease.lease_counter() + 1);
                lease.set_lease_owner(Some(owner.to_string()));
                clear_pending_shutdown_attributes(lease);
                if old_owner.is_some() && old_owner.as_deref() != Some(owner) {
                    lease.set_owner_switches_since_checkpoint(
                        lease.owner_switches_since_checkpoint() + 1,
                    );
                }
                Ok(true)
            }
        }
    }

    async fn initiate_graceful_lease_handoff(
        &self,
        lease: &mut Lease,
        new_owner: &str,
    ) -> Result<bool, LeasingError> {
        let mut updates: HashMap<String, AttributeValueUpdate> = HashMap::new();
        // Deliberately does NOT increment leaseCounter.
        updates.insert(
            LEASE_OWNER_KEY.to_string(),
            AttributeValueUpdate::builder()
                .value(create_attribute_value_string(new_owner))
                .action(AttributeAction::Put)
                .build(),
        );
        updates.insert(
            CHECKPOINT_OWNER.to_string(),
            AttributeValueUpdate::builder()
                .value(create_attribute_value_string(
                    lease.lease_owner().expect("current owner must be set"),
                ))
                .action(AttributeAction::Put)
                .build(),
        );

        let mut expected: HashMap<String, ExpectedAttributeValue> = HashMap::new();
        expected.insert(
            LEASE_OWNER_KEY.to_string(),
            ExpectedAttributeValue::builder()
                .value(create_attribute_value_string(
                    lease.lease_owner().expect("current owner must be set"),
                ))
                .build(),
        );
        expected.insert(
            CHECKPOINT_OWNER.to_string(),
            ExpectedAttributeValue::builder().exists(false).build(),
        );
        expected.extend(
            self.serializer
                .get_dynamo_existent_expectation(lease.lease_key().unwrap_or(""))?,
        );

        let builder = self
            .dynamo_db_client
            .update_item()
            .table_name(&self.table)
            .set_key(Some(self.serializer.get_dynamo_hash_key(lease)))
            .set_expected(Some(expected))
            .set_attribute_updates(Some(updates))
            .return_values(ReturnValue::AllNew);

        match self
            .send_update_item(
                builder,
                "initiate_lease_handoff",
                lease.lease_key().unwrap_or(""),
            )
            .await?
        {
            None => Ok(false),
            Some(response) => {
                if let Some(attrs) = response.attributes() {
                    let updated = self.serializer.from_dynamo_record(attrs);
                    lease.set_lease_counter(updated.lease_counter());
                    lease.set_lease_owner(updated.lease_owner().map(str::to_string));
                    lease.set_checkpoint_owner(updated.checkpoint_owner().map(str::to_string));
                    lease.set_owner_switches_since_checkpoint(
                        updated.owner_switches_since_checkpoint(),
                    );
                }
                Ok(true)
            }
        }
    }

    async fn assign_lease(&self, lease: &mut Lease, new_owner: &str) -> Result<bool, LeasingError> {
        let updates = self
            .serializer
            .get_dynamo_assign_lease_update(lease, new_owner)?;
        let mut expected = self.serializer.get_dynamo_lease_owner_expectation(lease);
        expected.extend(
            self.serializer
                .get_dynamo_existent_expectation(lease.lease_key().unwrap_or(""))?,
        );

        let builder = self
            .dynamo_db_client
            .update_item()
            .table_name(&self.table)
            .set_key(Some(self.serializer.get_dynamo_hash_key(lease)))
            .set_expected(Some(expected))
            .set_attribute_updates(Some(updates))
            .return_values(ReturnValue::AllNew)
            .return_values_on_condition_check_failure(ReturnValuesOnConditionCheckFailure::AllOld);

        match self
            .send_update_item(builder, "assign", lease.lease_key().unwrap_or(""))
            .await?
        {
            None => Ok(false),
            Some(response) => {
                if let Some(attrs) = response.attributes() {
                    let updated = self.serializer.from_dynamo_record(attrs);
                    lease.set_lease_counter(updated.lease_counter());
                    lease.set_lease_owner(updated.lease_owner().map(str::to_string));
                    lease.set_owner_switches_since_checkpoint(
                        updated.owner_switches_since_checkpoint(),
                    );
                }
                clear_pending_shutdown_attributes(lease);
                Ok(true)
            }
        }
    }

    async fn evict_lease(&self, lease: &mut Lease) -> Result<bool, LeasingError> {
        let updates = self.serializer.get_dynamo_evict_lease_update(lease);
        let mut expected = self.serializer.get_dynamo_lease_owner_expectation(lease);
        expected.extend(
            self.serializer
                .get_dynamo_existent_expectation(lease.lease_key().unwrap_or(""))?,
        );

        let builder = self
            .dynamo_db_client
            .update_item()
            .table_name(&self.table)
            .set_key(Some(self.serializer.get_dynamo_hash_key(lease)))
            .set_expected(Some(expected))
            .set_attribute_updates(Some(updates))
            .return_values(ReturnValue::AllNew);

        match self
            .send_update_item(builder, "evict", lease.lease_key().unwrap_or(""))
            .await?
        {
            None => Ok(false),
            Some(response) => {
                if let Some(attrs) = response.attributes() {
                    let updated = self.serializer.from_dynamo_record(attrs);
                    lease.set_lease_counter(updated.lease_counter());
                    lease.set_lease_owner(updated.lease_owner().map(str::to_string));
                }
                clear_pending_shutdown_attributes(lease);
                Ok(true)
            }
        }
    }

    async fn delete_lease(&self, lease: &Lease) -> Result<(), LeasingError> {
        let fut = self
            .dynamo_db_client
            .delete_item()
            .table_name(&self.table)
            .set_key(Some(self.serializer.get_dynamo_hash_key(lease)))
            .send();
        match tokio::time::timeout(self.dynamo_db_request_timeout, fut).await {
            Err(_) => Err(LeasingError::dependency("Timed out during deleteItem")),
            Ok(Ok(_)) => Ok(()),
            Ok(Err(sdk_err)) => Err(self.convert_and_rethrow(
                "delete",
                lease.lease_key().unwrap_or(""),
                sdk_err.into_service_error(),
            )),
        }
    }

    async fn delete_all(&self) -> Result<(), LeasingError> {
        let all_leases = self.list_leases().await?;
        for lease in &all_leases {
            let fut = self
                .dynamo_db_client
                .delete_item()
                .table_name(&self.table)
                .set_key(Some(self.serializer.get_dynamo_hash_key(lease)))
                .send();
            match tokio::time::timeout(self.dynamo_db_request_timeout, fut).await {
                Err(_) => return Err(LeasingError::dependency("Timed out during deleteAll")),
                Ok(Ok(_)) => {}
                Ok(Err(sdk_err)) => {
                    return Err(self.convert_and_rethrow(
                        "deleteAll",
                        lease.lease_key().unwrap_or(""),
                        sdk_err.into_service_error(),
                    ))
                }
            }
        }
        Ok(())
    }

    async fn update_lease(&self, lease: &mut Lease) -> Result<bool, LeasingError> {
        let mut updates = self.serializer.get_dynamo_lease_counter_update(lease);
        updates.extend(self.serializer.get_dynamo_update_lease_update(lease));
        let builder = self
            .dynamo_db_client
            .update_item()
            .table_name(&self.table)
            .set_key(Some(self.serializer.get_dynamo_hash_key(lease)))
            .set_expected(Some(
                self.serializer.get_dynamo_lease_counter_expectation(lease),
            ))
            .set_attribute_updates(Some(updates));

        match self
            .send_update_item(builder, "update", lease.lease_key().unwrap_or(""))
            .await?
        {
            None => Ok(false),
            Some(_) => {
                lease.set_lease_counter(lease.lease_counter() + 1);
                Ok(true)
            }
        }
    }

    async fn update_lease_with_meta_info(
        &self,
        lease: &Lease,
        update_field: UpdateField,
    ) -> Result<(), LeasingError> {
        let updates = self
            .serializer
            .get_dynamo_update_lease_update_field(lease, update_field)?;
        let builder = self
            .dynamo_db_client
            .update_item()
            .table_name(&self.table)
            .set_key(Some(self.serializer.get_dynamo_hash_key(lease)))
            .set_expected(Some(
                self.serializer
                    .get_dynamo_existent_expectation(lease.lease_key().unwrap_or(""))?,
            ))
            .set_attribute_updates(Some(updates));
        // ConditionalCheckFailed is logged + swallowed (lease didn't exist).
        let _ = self
            .send_update_item(builder, "update", lease.lease_key().unwrap_or(""))
            .await?;
        Ok(())
    }

    async fn is_lease_table_empty(&self) -> Result<bool, LeasingError> {
        Ok(self.list(Some(1), None).await?.is_empty())
    }

    async fn get_checkpoint(
        &self,
        lease_key: &str,
    ) -> Result<Option<ExtendedSequenceNumber>, LeasingError> {
        Ok(self
            .get_lease(lease_key)
            .await?
            .and_then(|l| l.checkpoint().cloned()))
    }

    async fn get_lease_table_identifier(&self) -> Result<String, LeasingError> {
        // Java: UserAgentUtils.getConsumerId(tableArn) — a SHA-256/Base64 hash of
        // the lease-table ARN. `generate_consumer_id` returns `None` for an empty
        // ARN (Java returns `null`); we surface that as an empty identifier.
        match self.describe_lease_table().await? {
            Some(resp) => {
                let table_arn = resp.table().and_then(|t| t.table_arn()).unwrap_or("");
                Ok(crate::common::get_consumer_id(table_arn).unwrap_or_default())
            }
            None => Ok(String::new()),
        }
    }
}

impl DynamoDBLeaseRefresher {
    /// Java `handleGracefulShutdown`.
    async fn handle_graceful_shutdown(
        &self,
        lease: &mut Lease,
        ddb_lease: &Lease,
    ) -> Result<bool, LeasingError> {
        if lease.actual_owner() != ddb_lease.actual_owner() {
            return Ok(false);
        }
        if ddb_lease.checkpoint_owner() == ddb_lease.lease_owner() {
            return Ok(false);
        }
        lease.set_checkpoint_owner(ddb_lease.checkpoint_owner().map(str::to_string));
        lease.set_lease_owner(ddb_lease.lease_owner().map(str::to_string));
        // Retry lease renewal (single level; now shutdownRequested() is true so
        // the checkpointOwner-not-exists expectation is dropped).
        // Box the recursive async call to break the infinitely-sized future.
        Box::pin(self.renew_lease(lease)).await
    }
}

fn clear_pending_shutdown_attributes(lease: &mut Lease) {
    lease.set_checkpoint_owner(None);
    lease.set_checkpoint_owner_timeout_timestamp_millis(None);
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::dynamodb::dynamodb_lease_serializer::DynamoDBLeaseSerializer;
    use crate::leases::dynamodb::test_support::{mock_ddb_client, mock_ddb_client_match_any};
    use aws_sdk_dynamodb::operation::create_table::CreateTableOutput;
    use aws_sdk_dynamodb::operation::describe_table::DescribeTableOutput;
    use aws_sdk_dynamodb::operation::get_item::GetItemOutput;
    use aws_sdk_dynamodb::operation::put_item::{PutItemError, PutItemOutput};
    use aws_sdk_dynamodb::operation::query::QueryOutput;
    use aws_sdk_dynamodb::operation::scan::{ScanError, ScanOutput};
    use aws_sdk_dynamodb::operation::update_item::{UpdateItemError, UpdateItemOutput};
    use aws_sdk_dynamodb::types::error::{
        ConditionalCheckFailedException, ProvisionedThroughputExceededException,
        ResourceNotFoundException,
    };
    use aws_sdk_dynamodb::types::{GlobalSecondaryIndexDescription, TableDescription};
    use aws_smithy_mocks::mock;

    const TABLE: &str = "TestLeaseTable";

    fn serializer() -> Arc<dyn LeaseSerializer + Send + Sync> {
        Arc::new(DynamoDBLeaseSerializer::new())
    }

    fn refresher_with(client: Client) -> DynamoDBLeaseRefresher {
        DynamoDBLeaseRefresher::new(
            TABLE,
            client,
            serializer(),
            true,
            Arc::new(crate::leases::dynamodb::table_creator_callback::NoopTableCreatorCallback),
            Duration::from_secs(10),
            RefresherTableConfig::default(),
            false,
            false,
            Vec::new(),
        )
    }

    fn dummy_lease(key: &str, owner: Option<&str>) -> Lease {
        let mut lease = Lease::default();
        lease.set_lease_key(key);
        lease.set_lease_counter(0);
        lease.set_owner_switches_since_checkpoint(0);
        lease.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
        lease.set_lease_owner(owner.map(str::to_string));
        lease
    }

    fn lease_item(key: &str, owner: &str) -> HashMap<String, AttributeValue> {
        DynamoDBLeaseSerializer::new().to_dynamo_record(&dummy_lease(key, Some(owner)))
    }

    fn last_key(key: &str) -> HashMap<String, AttributeValue> {
        let mut m = HashMap::new();
        m.insert(
            LEASE_KEY_KEY.to_string(),
            AttributeValue::S(key.to_string()),
        );
        m
    }

    // --- listLeases pagination ---

    #[tokio::test]
    async fn list_leases_paginates_across_multiple_pages() {
        let page1 = ScanOutput::builder()
            .set_items(Some(vec![
                lease_item("lease1", "owner1"),
                lease_item("lease2", "owner2"),
            ]))
            .set_last_evaluated_key(Some(last_key("lease2")))
            .build();
        let page2 = ScanOutput::builder()
            .set_items(Some(vec![lease_item("lease3", "owner3")]))
            .build();
        let r1 = mock!(Client::scan).then_output(move || page1.clone());
        let r2 = mock!(Client::scan).then_output(move || page2.clone());
        let client = mock_ddb_client(&[&r1, &r2]);
        let refresher = refresher_with(client);
        let result = refresher.list_leases().await.unwrap();
        assert_eq!(result.len(), 3);
        assert_eq!(r1.num_calls(), 1);
        assert_eq!(r2.num_calls(), 1);
    }

    #[tokio::test]
    async fn list_leases_pagination_stops_when_limit_reached() {
        // page1 has 2 items + a lastEvaluatedKey; a limit of 1 should stop after
        // page1 without fetching page2.
        let page1 = ScanOutput::builder()
            .set_items(Some(vec![
                lease_item("lease1", "owner1"),
                lease_item("lease2", "owner2"),
            ]))
            .set_last_evaluated_key(Some(last_key("lease2")))
            .build();
        let r1 = mock!(Client::scan).then_output(move || page1.clone());
        // A second scan rule that must NOT be consumed.
        let page2 = ScanOutput::builder()
            .set_items(Some(vec![lease_item("lease3", "owner3")]))
            .build();
        let r2 = mock!(Client::scan).then_output(move || page2.clone());
        let client = mock_ddb_client(&[&r1, &r2]);
        let refresher = refresher_with(client);
        // is_lease_table_empty uses list(1, null): limit=1.
        let empty = refresher.is_lease_table_empty().await.unwrap();
        assert!(!empty);
        assert_eq!(r1.num_calls(), 1);
        assert_eq!(
            r2.num_calls(),
            0,
            "page 2 must not be fetched once limit is reached"
        );
    }

    // --- exception mapping ---

    #[tokio::test]
    async fn list_leases_resource_not_found_maps_to_invalid_state() {
        let rule = mock!(Client::scan).then_error(|| {
            ScanError::ResourceNotFoundException(
                ResourceNotFoundException::builder().message("nope").build(),
            )
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let err = refresher.list_leases().await.unwrap_err();
        assert!(
            matches!(err, LeasingError::InvalidState { .. }),
            "got {err:?}"
        );
        assert!(err.message().contains("does not exist"));
    }

    #[tokio::test]
    async fn list_leases_throttle_maps_to_provisioned_throughput() {
        let rule = mock!(Client::scan).then_error(|| {
            ScanError::ProvisionedThroughputExceededException(
                ProvisionedThroughputExceededException::builder()
                    .message("throttled")
                    .build(),
            )
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let err = refresher.list_leases().await.unwrap_err();
        assert!(
            matches!(err, LeasingError::ProvisionedThroughput { .. }),
            "got {err:?}"
        );
    }

    // --- createLeaseIfNotExists conditional failure ---

    #[tokio::test]
    async fn create_lease_if_not_exists_conditional_failure_returns_false() {
        let rule = mock!(Client::put_item).then_error(|| {
            PutItemError::ConditionalCheckFailedException(
                ConditionalCheckFailedException::builder().build(),
            )
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let created = refresher
            .create_lease_if_not_exists(&dummy_lease("lease1", None))
            .await
            .unwrap();
        assert!(!created);
    }

    #[tokio::test]
    async fn create_lease_if_not_exists_success_returns_true() {
        let rule = mock!(Client::put_item).then_output(|| PutItemOutput::builder().build());
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let created = refresher
            .create_lease_if_not_exists(&dummy_lease("lease1", None))
            .await
            .unwrap();
        assert!(created);
    }

    #[tokio::test]
    async fn create_lease_provisioned_throughput_maps_via_convert_and_rethrow() {
        let rule = mock!(Client::put_item).then_error(|| {
            PutItemError::ProvisionedThroughputExceededException(
                ProvisionedThroughputExceededException::builder()
                    .message("throttled")
                    .build(),
            )
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let err = refresher
            .create_lease_if_not_exists(&dummy_lease("lease1", None))
            .await
            .unwrap_err();
        assert!(
            matches!(err, LeasingError::ProvisionedThroughput { .. }),
            "got {err:?}"
        );
    }

    #[tokio::test]
    async fn get_lease_resource_not_found_maps_to_invalid_state() {
        let rule = mock!(Client::get_item).then_error(|| {
            aws_sdk_dynamodb::operation::get_item::GetItemError::ResourceNotFoundException(
                ResourceNotFoundException::builder().message("gone").build(),
            )
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let err = refresher.get_lease("lease1").await.unwrap_err();
        assert!(
            matches!(err, LeasingError::InvalidState { .. }),
            "got {err:?}"
        );
        assert!(err.message().contains("does not exist"));
    }

    // --- getLease ---

    #[tokio::test]
    async fn get_lease_returns_none_when_absent() {
        let rule = mock!(Client::get_item).then_output(|| GetItemOutput::builder().build());
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        assert_eq!(refresher.get_lease("missing").await.unwrap(), None);
    }

    #[tokio::test]
    async fn get_lease_returns_lease_when_present() {
        let rule = mock!(Client::get_item).then_output(|| {
            GetItemOutput::builder()
                .set_item(Some(lease_item("lease1", "owner1")))
                .build()
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let lease = refresher.get_lease("lease1").await.unwrap().unwrap();
        assert_eq!(lease.lease_key(), Some("lease1"));
        assert_eq!(lease.lease_owner(), Some("owner1"));
    }

    // --- renew / take / update conditional-failure returns ---

    #[tokio::test]
    async fn take_lease_conditional_failure_returns_false() {
        let rule = mock!(Client::update_item).then_error(|| {
            UpdateItemError::ConditionalCheckFailedException(
                ConditionalCheckFailedException::builder().build(),
            )
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let mut lease = dummy_lease("lease1", Some("old"));
        assert!(!refresher.take_lease(&mut lease, "new").await.unwrap());
        // counter/owner unchanged on failure
        assert_eq!(lease.lease_counter(), 0);
        assert_eq!(lease.lease_owner(), Some("old"));
    }

    #[tokio::test]
    async fn take_lease_success_mutates_counter_and_owner() {
        let rule = mock!(Client::update_item).then_output(|| UpdateItemOutput::builder().build());
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let mut lease = dummy_lease("lease1", Some("old"));
        assert!(refresher.take_lease(&mut lease, "new").await.unwrap());
        assert_eq!(lease.lease_counter(), 1);
        assert_eq!(lease.lease_owner(), Some("new"));
        assert_eq!(lease.owner_switches_since_checkpoint(), 1);
    }

    #[tokio::test]
    async fn update_lease_conditional_failure_returns_false() {
        let rule = mock!(Client::update_item).then_error(|| {
            UpdateItemError::ConditionalCheckFailedException(
                ConditionalCheckFailedException::builder().build(),
            )
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let mut lease = dummy_lease("lease1", Some("owner"));
        assert!(!refresher.update_lease(&mut lease).await.unwrap());
        assert_eq!(lease.lease_counter(), 0);
    }

    #[tokio::test]
    async fn update_lease_success_increments_counter() {
        let rule = mock!(Client::update_item).then_output(|| UpdateItemOutput::builder().build());
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let mut lease = dummy_lease("lease1", Some("owner"));
        assert!(refresher.update_lease(&mut lease).await.unwrap());
        assert_eq!(lease.lease_counter(), 1);
    }

    #[tokio::test]
    async fn renew_lease_success_increments_counter() {
        let rule = mock!(Client::update_item).then_output(|| UpdateItemOutput::builder().build());
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let mut lease = dummy_lease("lease1", Some("owner"));
        assert!(refresher.renew_lease(&mut lease).await.unwrap());
        assert_eq!(lease.lease_counter(), 1);
    }

    #[tokio::test]
    async fn renew_lease_conditional_failure_no_shutdown_returns_false_when_ddb_absent() {
        // Steady-state renewal: conditional failure, then a getLease returns None
        // (lease gone), so the renewal is a genuine failure → false.
        let update_rule = mock!(Client::update_item).then_error(|| {
            UpdateItemError::ConditionalCheckFailedException(
                ConditionalCheckFailedException::builder().build(),
            )
        });
        let get_rule = mock!(Client::get_item).then_output(|| GetItemOutput::builder().build());
        let client = mock_ddb_client(&[&update_rule, &get_rule]);
        let refresher = refresher_with(client);
        let mut lease = dummy_lease("lease1", Some("owner"));
        lease.set_lease_counter(5);
        assert!(!refresher.renew_lease(&mut lease).await.unwrap());
        assert_eq!(lease.lease_counter(), 5);
    }

    #[tokio::test]
    async fn renew_lease_spurious_failure_recovers() {
        // Conditional failure, but the re-fetched lease shows owner+counter equal
        // to what a successful update would produce → treated as success.
        let update_rule = mock!(Client::update_item).then_error(|| {
            UpdateItemError::ConditionalCheckFailedException(
                ConditionalCheckFailedException::builder().build(),
            )
        });
        // The refreshed lease has counter = 6 (== 5 + 1) and same owner.
        let mut refreshed = dummy_lease("lease1", Some("owner"));
        refreshed.set_lease_counter(6);
        let refreshed_item = DynamoDBLeaseSerializer::new().to_dynamo_record(&refreshed);
        let get_rule = mock!(Client::get_item).then_output(move || {
            GetItemOutput::builder()
                .set_item(Some(refreshed_item.clone()))
                .build()
        });
        let client = mock_ddb_client(&[&update_rule, &get_rule]);
        let refresher = refresher_with(client);
        let mut lease = dummy_lease("lease1", Some("owner"));
        lease.set_lease_counter(5);
        assert!(refresher.renew_lease(&mut lease).await.unwrap());
        assert_eq!(lease.lease_counter(), 6);
    }

    // --- evict conditional failure ---

    #[tokio::test]
    async fn evict_lease_conditional_failure_returns_false() {
        let rule = mock!(Client::update_item).then_error(|| {
            UpdateItemError::ConditionalCheckFailedException(
                ConditionalCheckFailedException::builder().build(),
            )
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let mut lease = dummy_lease("lease1", Some("owner"));
        assert!(!refresher.evict_lease(&mut lease).await.unwrap());
    }

    // --- deleteLease ---

    #[tokio::test]
    async fn delete_lease_ok() {
        let rule = mock!(Client::delete_item).then_output(|| {
            aws_sdk_dynamodb::operation::delete_item::DeleteItemOutput::builder().build()
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        refresher
            .delete_lease(&dummy_lease("lease1", None))
            .await
            .unwrap();
        assert_eq!(rule.num_calls(), 1);
    }

    // --- table create / exists ---

    #[tokio::test]
    async fn create_lease_table_creates_when_absent() {
        // describeTable → ResourceNotFound (absent), then createTable succeeds.
        let describe_rule = mock!(Client::describe_table).then_error(|| {
            aws_sdk_dynamodb::operation::describe_table::DescribeTableError::ResourceNotFoundException(
                ResourceNotFoundException::builder().message("no table").build(),
            )
        });
        let create_rule =
            mock!(Client::create_table).then_output(|| CreateTableOutput::builder().build());
        let client = mock_ddb_client(&[&describe_rule, &create_rule]);
        let refresher = refresher_with(client);
        let created = refresher.create_lease_table_if_not_exists().await.unwrap();
        assert!(created);
        assert_eq!(create_rule.num_calls(), 1);
    }

    #[tokio::test]
    async fn create_lease_table_noop_when_exists() {
        let describe_rule = mock!(Client::describe_table).then_output(|| {
            DescribeTableOutput::builder()
                .table(
                    TableDescription::builder()
                        .table_name(TABLE)
                        .table_status(TableStatus::Active)
                        .build(),
                )
                .build()
        });
        let create_rule =
            mock!(Client::create_table).then_output(|| CreateTableOutput::builder().build());
        let client = mock_ddb_client(&[&describe_rule, &create_rule]);
        let refresher = refresher_with(client);
        let created = refresher.create_lease_table_if_not_exists().await.unwrap();
        assert!(!created);
        assert_eq!(create_rule.num_calls(), 0);
    }

    #[tokio::test]
    async fn lease_table_exists_true_when_active() {
        let rule = mock!(Client::describe_table).then_output(|| {
            DescribeTableOutput::builder()
                .table(
                    TableDescription::builder()
                        .table_status(TableStatus::Active)
                        .build(),
                )
                .build()
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        assert!(refresher.lease_table_exists().await.unwrap());
    }

    #[tokio::test]
    async fn lease_table_exists_false_when_absent() {
        let rule = mock!(Client::describe_table).then_error(|| {
            aws_sdk_dynamodb::operation::describe_table::DescribeTableError::ResourceNotFoundException(
                ResourceNotFoundException::builder().message("no").build(),
            )
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        assert!(!refresher.lease_table_exists().await.unwrap());
    }

    // --- GSI status ---

    #[tokio::test]
    async fn is_lease_owner_index_active_true() {
        let gsi = GlobalSecondaryIndexDescription::builder()
            .index_name(LEASE_OWNER_TO_LEASE_KEY_INDEX_NAME)
            .index_status(IndexStatus::Active)
            .build();
        let rule = mock!(Client::describe_table).then_output(move || {
            DescribeTableOutput::builder()
                .table(
                    TableDescription::builder()
                        .table_status(TableStatus::Active)
                        .global_secondary_indexes(gsi.clone())
                        .build(),
                )
                .build()
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        assert!(refresher
            .is_lease_owner_to_lease_key_index_active()
            .await
            .unwrap());
    }

    #[tokio::test]
    async fn is_lease_owner_index_active_false_when_creating() {
        let gsi = GlobalSecondaryIndexDescription::builder()
            .index_name(LEASE_OWNER_TO_LEASE_KEY_INDEX_NAME)
            .index_status(IndexStatus::Creating)
            .build();
        let rule = mock!(Client::describe_table).then_output(move || {
            DescribeTableOutput::builder()
                .table(
                    TableDescription::builder()
                        .table_status(TableStatus::Active)
                        .global_secondary_indexes(gsi.clone())
                        .build(),
                )
                .build()
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        assert!(!refresher
            .is_lease_owner_to_lease_key_index_active()
            .await
            .unwrap());
    }

    #[tokio::test]
    async fn is_lease_owner_index_active_false_when_absent_table() {
        let rule = mock!(Client::describe_table).then_error(|| {
            aws_sdk_dynamodb::operation::describe_table::DescribeTableError::ResourceNotFoundException(
                ResourceNotFoundException::builder().message("no").build(),
            )
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        assert!(!refresher
            .is_lease_owner_to_lease_key_index_active()
            .await
            .unwrap());
    }

    // --- listLeaseKeysForWorker (query pagination + ResourceNotFound → InvalidState) ---

    #[tokio::test]
    async fn list_lease_keys_for_worker_paginates() {
        let page1 = QueryOutput::builder()
            .set_items(Some(vec![last_key("lease1"), last_key("lease2")]))
            .set_last_evaluated_key(Some(last_key("lease2")))
            .build();
        let page2 = QueryOutput::builder()
            .set_items(Some(vec![last_key("lease3")]))
            .build();
        let r1 = mock!(Client::query).then_output(move || page1.clone());
        let r2 = mock!(Client::query).then_output(move || page2.clone());
        let client = mock_ddb_client(&[&r1, &r2]);
        let refresher = refresher_with(client);
        let keys = refresher
            .list_lease_keys_for_worker("worker1")
            .await
            .unwrap();
        assert_eq!(keys, vec!["lease1", "lease2", "lease3"]);
        assert_eq!(r1.num_calls(), 1);
        assert_eq!(r2.num_calls(), 1);
    }

    #[tokio::test]
    async fn list_lease_keys_for_worker_missing_index_maps_to_invalid_state() {
        let rule = mock!(Client::query).then_error(|| {
            aws_sdk_dynamodb::operation::query::QueryError::ResourceNotFoundException(
                ResourceNotFoundException::builder()
                    .message("no index")
                    .build(),
            )
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let err = refresher
            .list_lease_keys_for_worker("worker1")
            .await
            .unwrap_err();
        assert!(matches!(err, LeasingError::InvalidState { .. }));
        assert!(err.message().contains(LEASE_OWNER_TO_LEASE_KEY_INDEX_NAME));
    }

    // --- listLeasesParallely segment sizing ---

    #[tokio::test]
    async fn list_leases_parallely_uses_default_segments_when_describe_fails() {
        // describeTable → ResourceNotFound → resolver falls back to default (10);
        // each of the 10 segments does one empty scan.
        let describe_rule = mock!(Client::describe_table).then_error(|| {
            aws_sdk_dynamodb::operation::describe_table::DescribeTableError::ResourceNotFoundException(
                ResourceNotFoundException::builder().message("no").build(),
            )
        });
        let scan_rule = mock!(Client::scan)
            .sequence()
            .output(|| ScanOutput::builder().set_items(Some(vec![])).build())
            .repeatedly()
            .build();
        let client = mock_ddb_client_match_any(&[&describe_rule, &scan_rule]);
        let refresher = refresher_with(client);
        let (leases, failed) = refresher.list_leases_parallely(0).await.unwrap();
        assert!(leases.is_empty());
        assert!(failed.is_empty());
        assert_eq!(
            scan_rule.num_calls(),
            crate::leases::dynamodb::DEFAULT_LEASE_TABLE_SCAN_PARALLELISM_FACTOR as usize
        );
    }

    #[tokio::test]
    async fn list_leases_parallely_explicit_segments_skips_describe() {
        let describe_rule =
            mock!(Client::describe_table).then_output(|| DescribeTableOutput::builder().build());
        let scan_rule = mock!(Client::scan)
            .sequence()
            .output(|| ScanOutput::builder().set_items(Some(vec![])).build())
            .repeatedly()
            .build();
        let client = mock_ddb_client_match_any(&[&describe_rule, &scan_rule]);
        let refresher = refresher_with(client);
        let (leases, _) = refresher.list_leases_parallely(3).await.unwrap();
        assert!(leases.is_empty());
        assert_eq!(
            describe_rule.num_calls(),
            0,
            "describe not called when segments > 0"
        );
        assert_eq!(scan_rule.num_calls(), 3);
    }

    #[tokio::test]
    async fn list_leases_parallely_sanity_collects_leases() {
        let scan_rule = mock!(Client::scan)
            .sequence()
            .output(|| {
                ScanOutput::builder()
                    .set_items(Some(vec![lease_item("lease1", "owner1")]))
                    .build()
            })
            .repeatedly()
            .build();
        let client = mock_ddb_client_match_any(&[&scan_rule]);
        let refresher = refresher_with(client);
        // 1 segment → 1 scan → 1 lease.
        let (leases, failed) = refresher.list_leases_parallely(1).await.unwrap();
        assert_eq!(leases.len(), 1);
        assert!(failed.is_empty());
    }

    // --- Ported DynamoDBLeaseRefresherTest (mock-based) scenarios ---
    //
    // The Java tests mostly use DynamoDBEmbedded (a real in-process DB) for true
    // CAS round-trips; the pure conditional-write/mutation LOGIC is ported here
    // against `aws_smithy_mocks`. Tests that assert on a real-DB read-back after a
    // CAS sequence (create -> assign -> get -> compare) are covered behaviorally
    // by the mock's success/conditional-failure paths.

    /// Build a refresher with a custom `RefresherTableConfig` and PITR flag.
    fn refresher_with_config(
        client: Client,
        config: RefresherTableConfig,
        pitr_enabled: bool,
    ) -> DynamoDBLeaseRefresher {
        DynamoDBLeaseRefresher::new(
            TABLE,
            client,
            serializer(),
            true,
            Arc::new(crate::leases::dynamodb::table_creator_callback::NoopTableCreatorCallback),
            Duration::from_secs(10),
            config,
            false,
            pitr_enabled,
            Vec::new(),
        )
    }

    /// A non-lease DynamoDB item (e.g. a WorkerMetricStats row) that
    /// `deserialize_lease` must skip.
    fn non_lease_item(key: &str) -> HashMap<String, AttributeValue> {
        let mut item = lease_item(key, "owner");
        item.insert(
            "entityType".to_string(),
            AttributeValue::S("WORKER_METRIC_STATS".to_string()),
        );
        item
    }

    /// Port of `DynamoDBLeaseRefresherTest.createLeaseTableWithPitr`: after the
    /// table is created, PITR is enabled via `updateContinuousBackups`.
    #[tokio::test]
    async fn create_lease_table_with_pitr() {
        let describe_rule = mock!(Client::describe_table).then_error(|| {
            aws_sdk_dynamodb::operation::describe_table::DescribeTableError::ResourceNotFoundException(
                ResourceNotFoundException::builder().message("no table").build(),
            )
        });
        let create_rule =
            mock!(Client::create_table).then_output(|| CreateTableOutput::builder().build());
        let pitr_rule = mock!(Client::update_continuous_backups).then_output(|| {
            aws_sdk_dynamodb::operation::update_continuous_backups::UpdateContinuousBackupsOutput::builder()
                .build()
        });
        let client = mock_ddb_client(&[&describe_rule, &create_rule, &pitr_rule]);
        let refresher = refresher_with_config(client, RefresherTableConfig::default(), true);
        let created = refresher.create_lease_table_if_not_exists().await.unwrap();
        assert!(created);
        assert_eq!(pitr_rule.num_calls(), 1, "PITR should be enabled once");
    }

    /// Port of `DynamoDBLeaseRefresherTest.createLeaseTableIfNotExists_billingModeProvisioned_assertCorrectModeAndCapacity`.
    #[tokio::test]
    async fn create_lease_table_billing_mode_provisioned() {
        let describe_rule = mock!(Client::describe_table).then_error(|| {
            aws_sdk_dynamodb::operation::describe_table::DescribeTableError::ResourceNotFoundException(
                ResourceNotFoundException::builder().message("no table").build(),
            )
        });
        let create_rule = mock!(Client::create_table)
            .match_requests(|req| {
                req.billing_mode() == Some(&BillingMode::Provisioned)
                    && req
                        .provisioned_throughput()
                        .map(|p| p.read_capacity_units() == 100 && p.write_capacity_units() == 200)
                        .unwrap_or(false)
            })
            .then_output(|| CreateTableOutput::builder().build());
        let client = mock_ddb_client(&[&describe_rule, &create_rule]);
        let config = RefresherTableConfig {
            billing_mode: BillingMode::Provisioned,
            read_capacity: 100,
            write_capacity: 200,
        };
        let refresher = refresher_with_config(client, config, false);
        refresher.create_lease_table_if_not_exists().await.unwrap();
        assert_eq!(
            create_rule.num_calls(),
            1,
            "createTable must be sent with Provisioned mode + 100/200 capacity"
        );
    }

    /// Port of `DynamoDBLeaseRefresherTest.createLeaseTableIfNotExists_billingModeOnDemand_assertCorrectMode`.
    #[tokio::test]
    async fn create_lease_table_billing_mode_on_demand() {
        let describe_rule = mock!(Client::describe_table).then_error(|| {
            aws_sdk_dynamodb::operation::describe_table::DescribeTableError::ResourceNotFoundException(
                ResourceNotFoundException::builder().message("no table").build(),
            )
        });
        let create_rule = mock!(Client::create_table)
            .match_requests(|req| req.billing_mode() == Some(&BillingMode::PayPerRequest))
            .then_output(|| CreateTableOutput::builder().build());
        let client = mock_ddb_client(&[&describe_rule, &create_rule]);
        let refresher = refresher_with_config(client, RefresherTableConfig::default(), false);
        refresher.create_lease_table_if_not_exists().await.unwrap();
        assert_eq!(
            create_rule.num_calls(),
            1,
            "createTable must be PAY_PER_REQUEST"
        );
    }

    /// Port of
    /// `DynamoDBLeaseRefresherTest.createLeaseTableIfNotExistsOverloadedMethod_billingModeOnDemand_assertProvisionModeWithOveridenCapacity`
    /// (and the provisioned variant): the capacity-overloaded method always
    /// forces PROVISIONED mode with the given capacity, regardless of the
    /// configured billing mode.
    #[tokio::test]
    async fn create_lease_table_overloaded_forces_provisioned_capacity() {
        let describe_rule = mock!(Client::describe_table).then_error(|| {
            aws_sdk_dynamodb::operation::describe_table::DescribeTableError::ResourceNotFoundException(
                ResourceNotFoundException::builder().message("no table").build(),
            )
        });
        let create_rule = mock!(Client::create_table)
            .match_requests(|req| {
                req.billing_mode() == Some(&BillingMode::Provisioned)
                    && req
                        .provisioned_throughput()
                        .map(|p| p.read_capacity_units() == 50 && p.write_capacity_units() == 100)
                        .unwrap_or(false)
            })
            .then_output(|| CreateTableOutput::builder().build());
        let client = mock_ddb_client(&[&describe_rule, &create_rule]);
        // Config is OnDemand, but the overloaded method forces Provisioned 50/100.
        let refresher = refresher_with_config(client, RefresherTableConfig::default(), false);
        refresher
            .create_lease_table_if_not_exists_with_capacity(50, 100)
            .await
            .unwrap();
        assert_eq!(create_rule.num_calls(), 1);
    }

    /// Port of `DynamoDBLeaseRefresherTest.initiateGracefulLeaseHandoff_sanity`.
    #[tokio::test]
    async fn initiate_graceful_lease_handoff_sanity() {
        // UpdateItem returns AllNew attributes: owner=nextOwner, checkpointOwner=currentOwner.
        let mut updated = dummy_lease("lease1", Some("nextOwner"));
        updated.set_checkpoint_owner(Some("currentOwner".to_string()));
        let updated_attrs = DynamoDBLeaseSerializer::new().to_dynamo_record(&updated);
        let rule = mock!(Client::update_item).then_output(move || {
            UpdateItemOutput::builder()
                .set_attributes(Some(updated_attrs.clone()))
                .build()
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);

        let mut lease = dummy_lease("lease1", Some("currentOwner"));
        let ok = refresher
            .initiate_graceful_lease_handoff(&mut lease, "nextOwner")
            .await
            .unwrap();
        assert!(ok);
        assert_eq!(lease.lease_owner(), Some("nextOwner"));
        assert_eq!(lease.checkpoint_owner(), Some("currentOwner"));
    }

    /// Port of `DynamoDBLeaseRefresherTest.initiateGracefulLeaseHandoff_conditionalFailure`.
    #[tokio::test]
    async fn initiate_graceful_lease_handoff_conditional_failure() {
        let rule = mock!(Client::update_item).then_error(|| {
            UpdateItemError::ConditionalCheckFailedException(
                ConditionalCheckFailedException::builder().build(),
            )
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let mut lease = dummy_lease("lease1", Some("currentOwner"));
        lease.set_checkpoint_owner(Some("currentOwner".to_string()));
        let ok = refresher
            .initiate_graceful_lease_handoff(&mut lease, "nextOwner")
            .await
            .unwrap();
        assert!(!ok);
    }

    /// Port of `DynamoDBLeaseRefresherTest.assignLease_alwaysRemoveCheckpointOwner`.
    #[tokio::test]
    async fn assign_lease_always_removes_checkpoint_owner() {
        let mut updated = dummy_lease("lease1", Some("nextOwner"));
        updated.set_lease_counter(5);
        let updated_attrs = DynamoDBLeaseSerializer::new().to_dynamo_record(&updated);
        let rule = mock!(Client::update_item).then_output(move || {
            UpdateItemOutput::builder()
                .set_attributes(Some(updated_attrs.clone()))
                .build()
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);

        let mut lease = dummy_lease("lease1", Some("currentOwner"));
        lease.set_checkpoint_owner(Some("currentOwner".to_string()));
        let ok = refresher
            .assign_lease(&mut lease, "nextOwner")
            .await
            .unwrap();
        assert!(ok);
        assert_eq!(lease.lease_owner(), Some("nextOwner"));
        // checkpointOwner is always cleared on a successful assign.
        assert_eq!(lease.checkpoint_owner(), None);
    }

    /// Port of `DynamoDBLeaseRefresherTest.assignLease_conditionalFailureBecauseCheckpointOwnerIsNotExpected`.
    #[tokio::test]
    async fn assign_lease_conditional_failure() {
        let rule = mock!(Client::update_item).then_error(|| {
            UpdateItemError::ConditionalCheckFailedException(
                ConditionalCheckFailedException::builder().build(),
            )
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let mut lease = dummy_lease("lease1", Some("nextOwner"));
        lease.set_checkpoint_owner(Some("someone else now".to_string()));
        let ok = refresher
            .assign_lease(&mut lease, "nextOwner")
            .await
            .unwrap();
        assert!(!ok);
    }

    /// Port of `DynamoDBLeaseRefresherTest.takeLease_removesCheckpointOwner`.
    #[tokio::test]
    async fn take_lease_removes_checkpoint_owner() {
        let rule = mock!(Client::update_item).then_output(|| UpdateItemOutput::builder().build());
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let mut lease = dummy_lease("1", Some("ownerA"));
        lease.set_checkpoint_owner(Some("checkpointOwner".to_string()));
        let ok = refresher.take_lease(&mut lease, "newOwner").await.unwrap();
        assert!(ok);
        assert_eq!(lease.checkpoint_owner(), None);
        assert_eq!(lease.lease_owner(), Some("newOwner"));
    }

    /// Port of `DynamoDBLeaseRefresherTest.evictLease_removesCheckpointOwner`.
    #[tokio::test]
    async fn evict_lease_removes_checkpoint_owner() {
        // evict copies the counter from the AllNew response; the real DB returns
        // the incremented counter, so the mock replays that.
        let mut evicted = dummy_lease("1", Some("ownerA"));
        evicted.set_lease_counter(1);
        let evicted_attrs = DynamoDBLeaseSerializer::new().to_dynamo_record(&evicted);
        let rule = mock!(Client::update_item).then_output(move || {
            UpdateItemOutput::builder()
                .set_attributes(Some(evicted_attrs.clone()))
                .build()
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let mut lease = dummy_lease("1", Some("ownerA"));
        lease.set_checkpoint_owner(Some("checkpointOwner".to_string()));
        let original_counter = lease.lease_counter();
        let ok = refresher.evict_lease(&mut lease).await.unwrap();
        assert!(ok);
        assert_eq!(lease.checkpoint_owner(), None);
        assert_eq!(lease.lease_counter(), original_counter + 1);
    }

    /// Port of `DynamoDBLeaseRefresherTest.evictLease_removesOwnerIfCheckpointOwnerIsNull`.
    #[tokio::test]
    async fn evict_lease_removes_owner_if_checkpoint_owner_is_null() {
        // On success the counter increments (mirrored from the AllNew response).
        let mut evicted = dummy_lease("1", None);
        evicted.set_lease_counter(1);
        let evicted_attrs = DynamoDBLeaseSerializer::new().to_dynamo_record(&evicted);
        let rule = mock!(Client::update_item).then_output(move || {
            UpdateItemOutput::builder()
                .set_attributes(Some(evicted_attrs.clone()))
                .build()
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let mut lease = dummy_lease("1", Some("ownerA"));
        let original_counter = lease.lease_counter();
        let ok = refresher.evict_lease(&mut lease).await.unwrap();
        assert!(ok);
        assert_eq!(lease.checkpoint_owner(), None);
        assert_eq!(lease.lease_counter(), original_counter + 1);
    }

    /// Port of `DynamoDBLeaseRefresherTest.evictLease_noOpIfLeaseNotExists`.
    #[tokio::test]
    async fn evict_lease_no_op_if_lease_not_exists() {
        // Conditional check fails (lease absent / owner mismatch) -> false, no
        // counter change.
        let rule = mock!(Client::update_item)
            .sequence()
            .error(|| {
                UpdateItemError::ConditionalCheckFailedException(
                    ConditionalCheckFailedException::builder().build(),
                )
            })
            .times(2)
            .build();
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        let mut lease = dummy_lease("1", Some("ownerA"));
        assert!(!refresher.evict_lease(&mut lease).await.unwrap());
        // With no owner, the notExist condition path also fails.
        lease.set_lease_owner(None);
        assert!(!refresher.evict_lease(&mut lease).await.unwrap());
    }

    // --- isLeaseTableEmpty ---

    /// Port of `DynamoDBLeaseRefresherTest.isLeaseTableEmpty_returnsTrue_whenTableIsEmpty`.
    #[tokio::test]
    async fn is_lease_table_empty_true_when_empty() {
        let rule = mock!(Client::scan)
            .then_output(|| ScanOutput::builder().set_items(Some(vec![])).build());
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        assert!(refresher.is_lease_table_empty().await.unwrap());
    }

    /// Port of `DynamoDBLeaseRefresherTest.isLeaseTableEmpty_returnsFalse_whenTableHasLeases`.
    #[tokio::test]
    async fn is_lease_table_empty_false_when_has_leases() {
        let rule = mock!(Client::scan).then_output(|| {
            ScanOutput::builder()
                .set_items(Some(vec![lease_item("l1", "o1")]))
                .build()
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        assert!(!refresher.is_lease_table_empty().await.unwrap());
    }

    /// Port of `DynamoDBLeaseRefresherTest.isLeaseTableEmpty_returnsTrue_whenOnlyNonLeaseEntitiesExist`.
    #[tokio::test]
    async fn is_lease_table_empty_true_when_only_non_lease_entities() {
        let rule = mock!(Client::scan).then_output(|| {
            ScanOutput::builder()
                .set_items(Some(vec![non_lease_item("wm1")]))
                .build()
        });
        let client = mock_ddb_client(&[&rule]);
        let refresher = refresher_with(client);
        // Non-lease entities are filtered out, so the lease table is "empty".
        assert!(refresher.is_lease_table_empty().await.unwrap());
    }

    /// Port of `DynamoDBLeaseRefresherTest.isLeaseTableEmpty_returnsFalse_whenNonLeaseEntitiesOnFirstPageAndLeaseOnSecondPage`.
    #[tokio::test]
    async fn is_lease_table_empty_false_when_lease_on_second_page() {
        let page1 = ScanOutput::builder()
            .set_items(Some(vec![non_lease_item("wm1")]))
            .set_last_evaluated_key(Some(last_key("wm1")))
            .build();
        let page2 = ScanOutput::builder()
            .set_items(Some(vec![lease_item("l1", "o1")]))
            .build();
        let r1 = mock!(Client::scan).then_output(move || page1.clone());
        let r2 = mock!(Client::scan).then_output(move || page2.clone());
        let client = mock_ddb_client(&[&r1, &r2]);
        let refresher = refresher_with(client);
        // Page 1 has only non-lease entities (0 leases) -> pagination continues to
        // page 2, which has a lease -> not empty.
        assert!(!refresher.is_lease_table_empty().await.unwrap());
        assert_eq!(r1.num_calls(), 1);
        assert_eq!(r2.num_calls(), 1);
    }

    /// Port of `DynamoDBLeaseRefresherIntegrationTest.testTableCreatorCallback`:
    /// `performPostTableCreationAction` invokes the configured
    /// `TableCreatorCallback` with the client + table name.
    #[tokio::test]
    async fn table_creator_callback_fires_on_post_table_creation() {
        use crate::leases::dynamodb::table_creator_callback::{
            TableCreatorCallback, TableCreatorCallbackInput,
        };
        use std::sync::atomic::{AtomicUsize, Ordering};

        struct Recording {
            calls: Arc<AtomicUsize>,
            table: std::sync::Mutex<Option<String>>,
        }
        impl TableCreatorCallback for Recording {
            fn perform_action(&self, input: &TableCreatorCallbackInput) {
                self.calls.fetch_add(1, Ordering::SeqCst);
                *self.table.lock().unwrap() = Some(input.table_name().to_string());
            }
        }

        let calls = Arc::new(AtomicUsize::new(0));
        let callback = Arc::new(Recording {
            calls: calls.clone(),
            table: std::sync::Mutex::new(None),
        });
        let client = mock_ddb_client(&[]);
        let refresher = DynamoDBLeaseRefresher::new(
            TABLE,
            client,
            serializer(),
            true,
            callback.clone(),
            Duration::from_secs(10),
            RefresherTableConfig::default(),
            false,
            false,
            Vec::new(),
        );

        refresher.perform_post_table_creation_action().await;

        assert_eq!(calls.load(Ordering::SeqCst), 1);
        assert_eq!(callback.table.lock().unwrap().as_deref(), Some(TABLE));
    }
}
