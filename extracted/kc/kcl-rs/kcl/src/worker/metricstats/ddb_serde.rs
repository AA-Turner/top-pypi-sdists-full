//! DDB (de)serialization for [`WorkerMetricStats`], replacing Java's
//! `TableSchema.fromBean` reflection-based mapping (no Rust equivalent).
//!
//! Attribute names match the Java `@DynamoDbAttribute` annotations byte-for-byte
//! (wire-compatible with Java KCL fleets):
//! - partition key: `wid` (legacy) or `leaseKey` (lease table)
//! - `entityType` (EntityType DDB value string)
//! - `lut` (lastUpdateTime, N), `sts` (metricStats, M<String, L<N>>),
//!   `opr` (operatingRange, M<String, L<N>>), `properties` (M<String, S>),
//!   `sup` (supportCode, N), `slu` (supportCodeUpdateEpochSeconds, N)
//!
//! The runtime-only fields (`metricStatsMap`, `emaAlpha`) are never serialized.

use std::collections::HashMap;

use aws_sdk_dynamodb::types::AttributeValue;

use super::worker_metric_stats::{PartitionKeyVariant, WorkerMetricStats};
use crate::leases::dynamodb::dynamodb_lease_serializer::LEASE_KEY_KEY;
use crate::leases::EntityType;
use crate::worker::metricstats::worker_metric_stats::KEY_WORKER_ID;

const ATTR_ENTITY_TYPE: &str = "entityType";
const ATTR_LAST_UPDATE_TIME: &str = "lut";
const ATTR_METRIC_STATS: &str = "sts";
const ATTR_OPERATING_RANGE: &str = "opr";
const ATTR_PROPERTIES: &str = "properties";
const ATTR_SUPPORT_CODE: &str = "sup";
const ATTR_SUPPORT_CODE_UPDATE: &str = "slu";

/// The partition-key attribute name for a table variant.
pub fn partition_key_attribute_name(variant: PartitionKeyVariant) -> &'static str {
    match variant {
        PartitionKeyVariant::LeaseTable => LEASE_KEY_KEY,
        // Base + Legacy both use the legacy "wid" PK attribute.
        PartitionKeyVariant::Base | PartitionKeyVariant::Legacy => KEY_WORKER_ID,
    }
}

/// Serialize a [`WorkerMetricStats`] to a DDB attribute map. `ignore_nulls`
/// mirrors the Enhanced Client `ignoreNulls(true)` upsert (skip `None` fields).
pub fn to_dynamo_record(stats: &WorkerMetricStats) -> HashMap<String, AttributeValue> {
    let mut item = HashMap::new();
    let pk_attr = partition_key_attribute_name(stats.partition_variant());
    if let Some(worker_id) = stats.worker_id() {
        item.insert(
            pk_attr.to_string(),
            AttributeValue::S(worker_id.to_string()),
        );
    }
    if let Some(et) = stats.entity_type() {
        item.insert(
            ATTR_ENTITY_TYPE.to_string(),
            AttributeValue::S(et.ddb_value().to_string()),
        );
    }
    if let Some(lut) = stats.last_update_time() {
        item.insert(
            ATTR_LAST_UPDATE_TIME.to_string(),
            AttributeValue::N(lut.to_string()),
        );
    }
    if let Some(metric_stats) = stats.metric_stats() {
        item.insert(
            ATTR_METRIC_STATS.to_string(),
            map_of_f64_lists(metric_stats),
        );
    }
    if let Some(operating_range) = stats.operating_range() {
        item.insert(
            ATTR_OPERATING_RANGE.to_string(),
            map_of_i64_lists(operating_range),
        );
    }
    if let Some(properties) = stats.properties() {
        let m: HashMap<String, AttributeValue> = properties
            .iter()
            .map(|(k, v)| (k.clone(), AttributeValue::S(v.clone())))
            .collect();
        item.insert(ATTR_PROPERTIES.to_string(), AttributeValue::M(m));
    }
    if let Some(sup) = stats.support_code() {
        item.insert(
            ATTR_SUPPORT_CODE.to_string(),
            AttributeValue::N(sup.to_string()),
        );
    }
    if let Some(slu) = stats.support_code_update_epoch_seconds() {
        item.insert(
            ATTR_SUPPORT_CODE_UPDATE.to_string(),
            AttributeValue::N(slu.to_string()),
        );
    }
    item
}

fn map_of_f64_lists(m: &HashMap<String, Vec<f64>>) -> AttributeValue {
    let inner: HashMap<String, AttributeValue> = m
        .iter()
        .map(|(k, list)| {
            let l: Vec<AttributeValue> = list
                .iter()
                .map(|v| AttributeValue::N(v.to_string()))
                .collect();
            (k.clone(), AttributeValue::L(l))
        })
        .collect();
    AttributeValue::M(inner)
}

fn map_of_i64_lists(m: &HashMap<String, Vec<i64>>) -> AttributeValue {
    let inner: HashMap<String, AttributeValue> = m
        .iter()
        .map(|(k, list)| {
            let l: Vec<AttributeValue> = list
                .iter()
                .map(|v| AttributeValue::N(v.to_string()))
                .collect();
            (k.clone(), AttributeValue::L(l))
        })
        .collect();
    AttributeValue::M(inner)
}

/// Deserialize a DDB attribute map into a [`WorkerMetricStats`] of the given
/// table variant.
pub fn from_dynamo_record(
    item: &HashMap<String, AttributeValue>,
    variant: PartitionKeyVariant,
) -> WorkerMetricStats {
    let pk_attr = partition_key_attribute_name(variant);
    let mut builder = match variant {
        PartitionKeyVariant::Legacy => WorkerMetricStats::legacy_builder(),
        PartitionKeyVariant::LeaseTable => WorkerMetricStats::lease_table_builder(),
        PartitionKeyVariant::Base => WorkerMetricStats::builder(),
    };
    if let Some(AttributeValue::S(worker_id)) = item.get(pk_attr) {
        builder = builder.worker_id(worker_id.clone());
    }
    if let Some(AttributeValue::S(et)) = item.get(ATTR_ENTITY_TYPE) {
        if let Some(entity_type) = EntityType::from_ddb_value(et) {
            builder = builder.entity_type(entity_type);
        }
    }
    if let Some(AttributeValue::N(lut)) = item.get(ATTR_LAST_UPDATE_TIME) {
        if let Ok(v) = lut.parse::<i64>() {
            builder = builder.last_update_time(v);
        }
    }
    if let Some(av) = item.get(ATTR_METRIC_STATS) {
        builder = builder.metric_stats(parse_f64_lists(av));
    }
    if let Some(av) = item.get(ATTR_OPERATING_RANGE) {
        builder = builder.operating_range(parse_i64_lists(av));
    }
    if let Some(AttributeValue::M(m)) = item.get(ATTR_PROPERTIES) {
        let props: HashMap<String, String> = m
            .iter()
            .filter_map(|(k, v)| match v {
                AttributeValue::S(s) => Some((k.clone(), s.clone())),
                _ => None,
            })
            .collect();
        builder = builder.properties(props);
    }
    if let Some(AttributeValue::N(sup)) = item.get(ATTR_SUPPORT_CODE) {
        if let Ok(v) = sup.parse::<i32>() {
            builder = builder.support_code(v);
        }
    }
    if let Some(AttributeValue::N(slu)) = item.get(ATTR_SUPPORT_CODE_UPDATE) {
        if let Ok(v) = slu.parse::<i64>() {
            builder = builder.support_code_update_epoch_seconds(v);
        }
    }
    builder.build()
}

fn parse_f64_lists(av: &AttributeValue) -> HashMap<String, Vec<f64>> {
    let mut result = HashMap::new();
    if let AttributeValue::M(m) = av {
        for (k, v) in m {
            if let AttributeValue::L(list) = v {
                let parsed: Vec<f64> = list
                    .iter()
                    .filter_map(|e| match e {
                        AttributeValue::N(n) => n.parse().ok(),
                        _ => None,
                    })
                    .collect();
                result.insert(k.clone(), parsed);
            }
        }
    }
    result
}

fn parse_i64_lists(av: &AttributeValue) -> HashMap<String, Vec<i64>> {
    let mut result = HashMap::new();
    if let AttributeValue::M(m) = av {
        for (k, v) in m {
            if let AttributeValue::L(list) = v {
                let parsed: Vec<i64> = list
                    .iter()
                    .filter_map(|e| match e {
                        AttributeValue::N(n) => n.parse().ok(),
                        _ => None,
                    })
                    .collect();
                result.insert(k.clone(), parsed);
            }
        }
    }
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn round_trip_lease_table() {
        let stats = WorkerMetricStats::lease_table_builder()
            .worker_id("w-1")
            .last_update_time(12345)
            .metric_stats([("C".to_string(), vec![50.0, 60.0])].into_iter().collect())
            .operating_range([("C".to_string(), vec![80i64])].into_iter().collect())
            .support_code(1)
            .support_code_update_epoch_seconds(999)
            .build();
        let item = to_dynamo_record(&stats);
        // PK attribute is leaseKey for the lease-table variant.
        assert!(item.contains_key(LEASE_KEY_KEY));
        assert_eq!(
            item.get("entityType"),
            Some(&AttributeValue::S("WORKER_METRIC_STATS".to_string()))
        );
        let back = from_dynamo_record(&item, PartitionKeyVariant::LeaseTable);
        assert_eq!(back.worker_id(), Some("w-1"));
        assert_eq!(back.last_update_time(), Some(12345));
        assert_eq!(
            back.metric_stats().unwrap().get("C").unwrap(),
            &vec![50.0, 60.0]
        );
        assert_eq!(
            back.operating_range().unwrap().get("C").unwrap(),
            &vec![80i64]
        );
        assert_eq!(back.support_code(), Some(1));
        assert_eq!(back.support_code_update_epoch_seconds(), Some(999));
    }

    #[test]
    fn legacy_uses_wid_partition_key() {
        let stats = WorkerMetricStats::legacy_builder().worker_id("w-2").build();
        let item = to_dynamo_record(&stats);
        assert!(item.contains_key(KEY_WORKER_ID));
        assert!(!item.contains_key(LEASE_KEY_KEY));
    }
}
