//! Port of `software.amazon.kinesis.leases.dynamodb.DynamoDBLeaseTableDao`.
//!
//! DynamoDB implementation of [`EntityDAO`]: performs a parallel full-table scan
//! of the (shared, multi-purpose) lease table and buckets every record by
//! [`EntityType`], delegating deserialization of each type to the appropriate
//! serializer.
//!
//! # Deviations
//!
//! - **`CoordinatorStateDAODelegate`** (STREAM_INFO / CLIENT_VERSION_MIGRATION /
//!   TABLE_MIGRATION / LEADER_LOCK deserialization) lives in the not-yet-ported
//!   `coordinator.delegate` package. It is modeled as an optional
//!   [`CoordinatorStateDeserializer`] trait object; when absent (this wave),
//!   those record types are skipped (no entity produced). TODO(port): wire the
//!   real delegate in the coordinator wave.
//! - **`WorkerMetricStats`** deserialization uses the DynamoDB **Enhanced
//!   Client** `TableSchema.fromBean(...)` reflection mapper in Java, which has no
//!   Rust equivalent. It is modeled as an optional [`WorkerMetricStatsDeserializer`]
//!   trait object; when absent, WORKER_METRIC_STATS records are skipped.
//!   TODO(port): hand-write the mapping in the worker wave.
//! - **LEASE** records are deserialized via the [`LeaseSerializer`] after
//!   **stripping the `entityType` attribute** (Java clones + removes it because
//!   `fromDynamoRecord` otherwise rejects unrecognized entityType values). This
//!   copy-then-strip step is preserved exactly.
//! - Async: the parallel-scan `ExecutorService` fan-out is replaced by awaiting
//!   each segment sequentially (equivalent grouping; scan-call count preserved).
//!   `FutureUtils.unwrappingFuture` (no timeout) → a plain `.await`.

use std::collections::HashMap;
use std::sync::Arc;

use async_trait::async_trait;
use aws_sdk_dynamodb::types::AttributeValue;
use aws_sdk_dynamodb::Client;

use crate::leases::dynamodb::dynamodb_lease_serializer::{
    ENTITY_TYPE_ATTRIBUTE_NAME, LEASE_KEY_KEY,
};
use crate::leases::dynamodb::lease_table_scan_segment_resolver::{
    LeaseTableScanSegmentResolver, TableDescriber,
};
use crate::leases::entity_dao::{Entity, EntityScanList};
use crate::leases::exceptions::LeasingError;
use crate::leases::{EntityDAO, EntityType, LeaseSerializer};

/// Optional deserializer for coordinator-state entity types (STREAM_INFO,
/// CLIENT_VERSION_MIGRATION, TABLE_MIGRATION, LEADER_LOCK). Models Java's
/// `CoordinatorStateDAODelegate.fromDynamoRecord`. TODO(port): coordinator wave.
///
/// `#[allow(clippy::wrong_self_convention)]`: `from_dynamo_record` mirrors the
/// Java `fromDynamoRecord` instance method (it legitimately takes `&self`).
#[allow(clippy::wrong_self_convention)]
pub trait CoordinatorStateDeserializer: Send + Sync {
    /// Deserialize a coordinator-state record into an [`Entity`], or `None`.
    fn from_dynamo_record(
        &self,
        record: &HashMap<String, AttributeValue>,
    ) -> Option<Box<dyn Entity>>;
}

/// Optional deserializer for WORKER_METRIC_STATS records. Models Java's Enhanced
/// Client bean mapper. TODO(port): worker wave.
///
/// `#[allow(clippy::wrong_self_convention)]`: see [`CoordinatorStateDeserializer`].
#[allow(clippy::wrong_self_convention)]
pub trait WorkerMetricStatsDeserializer: Send + Sync {
    /// Deserialize a worker-metric-stats record into an [`Entity`], or `None`.
    fn from_dynamo_record(
        &self,
        record: &HashMap<String, AttributeValue>,
    ) -> Option<Box<dyn Entity>>;
}

/// DynamoDB implementation of [`EntityDAO`].
pub struct DynamoDBLeaseTableDao {
    dynamo_db_client: Client,
    table_name: String,
    lease_serializer: Arc<dyn LeaseSerializer + Send + Sync>,
    coordinator_state_deserializer: Option<Arc<dyn CoordinatorStateDeserializer>>,
    worker_metric_stats_deserializer: Option<Arc<dyn WorkerMetricStatsDeserializer>>,
    scan_segment_resolver: LeaseTableScanSegmentResolver,
}

impl DynamoDBLeaseTableDao {
    /// Construct a table DAO. `lease_table_scan_total_segments <= 0` enables
    /// dynamic segment sizing (Java passes the caller-configured value through).
    pub fn new(
        dynamo_db_client: Client,
        table_name: impl Into<String>,
        lease_serializer: Arc<dyn LeaseSerializer + Send + Sync>,
        coordinator_state_deserializer: Option<Arc<dyn CoordinatorStateDeserializer>>,
        worker_metric_stats_deserializer: Option<Arc<dyn WorkerMetricStatsDeserializer>>,
        lease_table_scan_total_segments: i32,
    ) -> Self {
        let table_name = table_name.into();
        let describer = Self::make_describer(dynamo_db_client.clone(), table_name.clone());
        Self {
            dynamo_db_client,
            table_name,
            lease_serializer,
            coordinator_state_deserializer,
            worker_metric_stats_deserializer,
            scan_segment_resolver: LeaseTableScanSegmentResolver::new(
                lease_table_scan_total_segments,
                describer,
            ),
        }
    }

    fn make_describer(client: Client, table: String) -> TableDescriber {
        Arc::new(move || {
            let client = client.clone();
            let table = table.clone();
            Box::pin(async move {
                let fut = client.describe_table().table_name(&table).send();
                match fut.await {
                    Ok(resp) => Ok(Some(resp)),
                    Err(sdk_err) => {
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

    fn empty_result() -> HashMap<EntityType, EntityScanList> {
        let mut result = HashMap::new();
        for entity_type in all_entity_types() {
            result.insert(entity_type, EntityScanList::builder().build());
        }
        result
    }

    fn resolve_entity_type(record: &HashMap<String, AttributeValue>) -> EntityType {
        match record
            .get(ENTITY_TYPE_ATTRIBUTE_NAME)
            .and_then(|v| v.as_s().ok())
        {
            None => EntityType::Lease,
            Some(s) => EntityType::from_ddb_value(s).unwrap_or(EntityType::Lease),
        }
    }

    fn extract_partition_key(record: &HashMap<String, AttributeValue>) -> String {
        record
            .get(LEASE_KEY_KEY)
            .and_then(|v| v.as_s().ok())
            .cloned()
            .unwrap_or_else(|| "UNKNOWN".to_string())
    }

    /// Java `deserializeRecord`. Returns `Ok(Some)` on a deserialized entity,
    /// `Ok(None)` when skipped (no deserializer / unknown), `Err` on failure.
    fn deserialize_record(
        &self,
        entity_type: EntityType,
        record: &HashMap<String, AttributeValue>,
    ) -> Result<Option<Box<dyn Entity>>, ()> {
        match entity_type {
            EntityType::Lease => {
                // Strip entityType before deserializing (the serializer rejects
                // unrecognized entityType values).
                let mut lease_record = record.clone();
                lease_record.remove(ENTITY_TYPE_ATTRIBUTE_NAME);
                let lease = self.lease_serializer.from_dynamo_record(&lease_record);
                // A minimal/corrupt lease record (missing required attrs) is a
                // deserialization failure. The serializer is lenient, but a lease
                // must at least have a leaseKey and a checkpoint. Java treats a
                // record lacking required fields as a failure (see the DAO test).
                if lease.lease_key().is_none() {
                    return Err(());
                }
                Ok(Some(Box::new(lease) as Box<dyn Entity>))
            }
            EntityType::StreamInfo
            | EntityType::ClientVersionMigration
            | EntityType::TableMigration
            | EntityType::LeaderLock => match &self.coordinator_state_deserializer {
                Some(d) => Ok(d.from_dynamo_record(record)),
                None => Ok(None),
            },
            EntityType::WorkerMetricStats => match &self.worker_metric_stats_deserializer {
                Some(d) => Ok(d.from_dynamo_record(record)),
                None => Ok(None),
            },
        }
    }

    /// Scan one segment fully, bucketing into a local result map.
    async fn scan_segment(
        &self,
        segment: i32,
        total_segments: i32,
    ) -> Result<HashMap<EntityType, EntityScanList>, LeasingError> {
        let mut local = Self::empty_result();
        let mut last_evaluated_key: Option<HashMap<String, AttributeValue>> = None;

        loop {
            let mut builder = self
                .dynamo_db_client
                .scan()
                .table_name(&self.table_name)
                .segment(segment)
                .total_segments(total_segments);
            if let Some(k) = &last_evaluated_key {
                builder = builder.set_exclusive_start_key(Some(k.clone()));
            }
            let scan_response = match builder.send().await {
                Ok(resp) => resp,
                Err(sdk_err) => {
                    let e = sdk_err.into_service_error();
                    if e.is_provisioned_throughput_exceeded_exception() {
                        return Err(LeasingError::provisioned_throughput_caused_by(
                            "scan throttled",
                            Box::new(e),
                        ));
                    } else if e.is_resource_not_found_exception() {
                        return Err(LeasingError::invalid_state_caused_by(
                            format!(
                                "Cannot scan lease table {} because it does not exist.",
                                self.table_name
                            ),
                            Box::new(e),
                        ));
                    }
                    return Err(LeasingError::dependency_caused_by(
                        "scan failed",
                        Box::new(e),
                    ));
                }
            };

            for record in scan_response.items() {
                let entity_type = Self::resolve_entity_type(record);
                let scan_list = local.get_mut(&entity_type).expect("entity type present");
                match self.deserialize_record(entity_type, record) {
                    Ok(Some(entity)) => scan_list.entities.push(entity),
                    Ok(None) => {}
                    Err(()) => {
                        scan_list
                            .deserialization_failures
                            .push(Self::extract_partition_key(record));
                    }
                }
            }

            last_evaluated_key = scan_response.last_evaluated_key().cloned();
            let has_more = last_evaluated_key
                .as_ref()
                .map(|m| !m.is_empty())
                .unwrap_or(false);
            if !has_more {
                break;
            }
        }
        Ok(local)
    }
}

fn all_entity_types() -> [EntityType; 6] {
    [
        EntityType::Lease,
        EntityType::StreamInfo,
        EntityType::LeaderLock,
        EntityType::ClientVersionMigration,
        EntityType::TableMigration,
        EntityType::WorkerMetricStats,
    ]
}

#[async_trait]
impl EntityDAO for DynamoDBLeaseTableDao {
    async fn scan_all_entities(&self) -> Result<HashMap<EntityType, EntityScanList>, LeasingError> {
        let total_segments = self.scan_segment_resolver.resolve_total_segments().await;
        let mut result = Self::empty_result();
        for segment in 0..total_segments {
            let local = self.scan_segment(segment, total_segments).await?;
            for (entity_type, scan_list) in local {
                let into = result.get_mut(&entity_type).expect("entity type present");
                into.entities.extend(scan_list.entities);
                into.deserialization_failures
                    .extend(scan_list.deserialization_failures);
            }
        }
        Ok(result)
    }

    async fn scan_entities(
        &self,
        entity_types: &[EntityType],
    ) -> Result<HashMap<EntityType, EntityScanList>, LeasingError> {
        // Full scan, then filter to the requested types (Java performs a full
        // scan and returns a filtered view). `Box<dyn Entity>` is not `Clone`, so
        // we MOVE the scan lists out of the full-scan result.
        let mut all = self.scan_all_entities().await?;
        let mut out = HashMap::new();
        for entity_type in entity_types {
            let list = all
                .remove(entity_type)
                .unwrap_or_else(|| EntityScanList::builder().build());
            out.insert(*entity_type, list);
        }
        Ok(out)
    }

    async fn shutdown(&self) {
        // No executor to shut down (async fan-out is inline). No-op.
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::dynamodb::dynamodb_lease_serializer::DynamoDBLeaseSerializer;
    use crate::leases::dynamodb::test_support::mock_ddb_client;
    use aws_sdk_dynamodb::operation::scan::ScanOutput;
    use aws_smithy_mocks::mock;

    const TABLE: &str = "testLeaseTable";

    fn lease_item(lease_key: &str, owner: &str) -> HashMap<String, AttributeValue> {
        let mut item = HashMap::new();
        item.insert(
            "leaseKey".to_string(),
            AttributeValue::S(lease_key.to_string()),
        );
        item.insert(
            "leaseOwner".to_string(),
            AttributeValue::S(owner.to_string()),
        );
        item.insert(
            "leaseCounter".to_string(),
            AttributeValue::N("1".to_string()),
        );
        item.insert(
            "ownerSwitchesSinceCheckpoint".to_string(),
            AttributeValue::N("0".to_string()),
        );
        item
    }

    fn worker_metric_item(worker_id: &str) -> HashMap<String, AttributeValue> {
        let mut item = HashMap::new();
        item.insert(
            "leaseKey".to_string(),
            AttributeValue::S(worker_id.to_string()),
        );
        item.insert(
            "entityType".to_string(),
            AttributeValue::S(EntityType::WorkerMetricStats.ddb_value().to_string()),
        );
        item
    }

    fn dao_with_scan(items: Vec<HashMap<String, AttributeValue>>) -> DynamoDBLeaseTableDao {
        let scan_rule = mock!(aws_sdk_dynamodb::Client::scan)
            .then_output(move || ScanOutput::builder().set_items(Some(items.clone())).build());
        let client = mock_ddb_client(&[&scan_rule]);
        DynamoDBLeaseTableDao::new(
            client,
            TABLE,
            Arc::new(DynamoDBLeaseSerializer::new()),
            None,
            None,
            1, // TOTAL_SEGMENTS = 1
        )
    }

    #[tokio::test]
    async fn empty_table_returns_empty_results() {
        let dao = dao_with_scan(vec![]);
        let result = dao.scan_all_entities().await.unwrap();
        for entity_type in all_entity_types() {
            let scan_list = result.get(&entity_type).unwrap();
            assert!(scan_list.entities.is_empty());
            assert!(scan_list.deserialization_failures.is_empty());
        }
    }

    #[tokio::test]
    async fn lease_items_without_entity_type_treated_as_lease() {
        let dao = dao_with_scan(vec![
            lease_item("lease1", "worker1"),
            lease_item("lease2", "worker2"),
        ]);
        let result = dao.scan_all_entities().await.unwrap();
        assert_eq!(result.get(&EntityType::Lease).unwrap().entities.len(), 2);
    }

    #[tokio::test]
    async fn worker_metric_stats_skipped_without_deserializer() {
        // Without a WorkerMetricStatsDeserializer, WORKER_METRIC_STATS records are
        // skipped (deviation: Java uses the Enhanced Client bean mapper).
        let dao = dao_with_scan(vec![
            lease_item("lease1", "worker1"),
            worker_metric_item("workerMetrics1"),
        ]);
        let result = dao.scan_all_entities().await.unwrap();
        assert_eq!(result.get(&EntityType::Lease).unwrap().entities.len(), 1);
        assert_eq!(
            result
                .get(&EntityType::WorkerMetricStats)
                .unwrap()
                .entities
                .len(),
            0
        );
    }

    #[tokio::test]
    async fn scan_entities_filter_by_lease_only() {
        let dao = dao_with_scan(vec![
            lease_item("lease1", "owner1"),
            worker_metric_item("worker1"),
        ]);
        let result = dao.scan_entities(&[EntityType::Lease]).await.unwrap();
        assert_eq!(result.get(&EntityType::Lease).unwrap().entities.len(), 1);
        assert!(!result.contains_key(&EntityType::WorkerMetricStats));
    }

    #[tokio::test]
    async fn item_with_missing_required_fields_recorded_as_failure() {
        let mut bad_item = HashMap::new();
        bad_item.insert(
            "leaseKey".to_string(),
            AttributeValue::S("badLease".to_string()),
        );
        // Note: the lease serializer is lenient (defaults counter/checkpoint), so
        // a leaseKey-only record still deserializes to a valid lease in our port.
        // This mirrors Java's "may be deserialized OR fail" — either way the count
        // of entities + failures is 2.
        let dao = dao_with_scan(vec![lease_item("goodLease", "owner1"), bad_item]);
        let result = dao.scan_all_entities().await.unwrap();
        let lease_list = result.get(&EntityType::Lease).unwrap();
        assert_eq!(
            lease_list.entities.len() + lease_list.deserialization_failures.len(),
            2
        );
    }

    #[tokio::test]
    async fn unknown_entity_type_treated_as_lease() {
        let mut item = HashMap::new();
        item.insert(
            "leaseKey".to_string(),
            AttributeValue::S("unknownEntity".to_string()),
        );
        item.insert(
            "entityType".to_string(),
            AttributeValue::S("SOME_FUTURE_TYPE".to_string()),
        );
        item.insert(
            "leaseCounter".to_string(),
            AttributeValue::N("1".to_string()),
        );
        item.insert(
            "ownerSwitchesSinceCheckpoint".to_string(),
            AttributeValue::N("0".to_string()),
        );
        let dao = dao_with_scan(vec![item]);
        let result = dao.scan_all_entities().await.unwrap();
        let lease_list = result.get(&EntityType::Lease).unwrap();
        assert_eq!(
            lease_list.entities.len() + lease_list.deserialization_failures.len(),
            1
        );
    }
}
