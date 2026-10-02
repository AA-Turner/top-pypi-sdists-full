//! Port of `software.amazon.kinesis.leases.dynamodb.DynamoDBMultiStreamLeaseSerializer`.
//!
//! Decorates [`DynamoDBLeaseSerializer`] with the two multi-stream attributes:
//! the stream id (persisted under the **legacy** attribute name `"streamName"`)
//! and the shard id (`"shardId"`).
//!
//! # Composition over inheritance
//!
//! Java's `DynamoDBMultiStreamLeaseSerializer extends DynamoDBLeaseSerializer`
//! (calling `super.*` then adding fields). Rust has no inheritance, so this
//! struct **composes** a [`DynamoDBLeaseSerializer`] and delegates to its
//! `*_base` helpers, then adds the multi-stream attributes — reproducing the
//! `super`-then-augment pattern exactly.
//!
//! # Faithful naming quirk
//!
//! `STREAM_ID_KEY` is literally `"streamName"` (not `"streamId"`) for backward
//! compatibility, even though the field/accessor is `stream_identifier` —
//! preserved byte-for-byte.

use std::collections::HashMap;

use aws_sdk_dynamodb::types::{
    AttributeDefinition, AttributeValue, AttributeValueUpdate, ExpectedAttributeValue,
    KeySchemaElement,
};

use crate::leases::dynamo_utils::{create_attribute_value_string, safe_get_string};
use crate::leases::dynamodb::dynamodb_lease_serializer::DynamoDBLeaseSerializer;
use crate::leases::exceptions::LeasingError;
use crate::leases::{Lease, LeaseSerializer, UpdateField};

const STREAM_ID_KEY: &str = "streamName";
const SHARD_ID_KEY: &str = "shardId";

/// Multi-stream [`LeaseSerializer`] adding `streamName` + `shardId` attributes.
#[derive(Debug, Default, Clone)]
pub struct DynamoDBMultiStreamLeaseSerializer {
    base: DynamoDBLeaseSerializer,
}

impl DynamoDBMultiStreamLeaseSerializer {
    /// New serializer.
    pub fn new() -> Self {
        Self {
            base: DynamoDBLeaseSerializer::new(),
        }
    }
}

impl LeaseSerializer for DynamoDBMultiStreamLeaseSerializer {
    fn to_dynamo_record(&self, lease: &Lease) -> HashMap<String, AttributeValue> {
        // Java: validateAndCast(lease) then super.toDynamoRecord + stream/shard.
        lease.validate_multi_stream();
        let mut result = self.base.to_dynamo_record_base(lease);
        result.insert(
            STREAM_ID_KEY.to_string(),
            create_attribute_value_string(lease.stream_identifier().expect("multi-stream")),
        );
        result.insert(
            SHARD_ID_KEY.to_string(),
            create_attribute_value_string(lease.shard_id().expect("multi-stream")),
        );
        result
    }

    fn from_dynamo_record(&self, dynamo_record: &HashMap<String, AttributeValue>) -> Lease {
        // Java constructs a fresh MultiStreamLease and populates via super, then
        // sets streamIdentifier/shardId (unconditionally, even if absent).
        let mut lease = Lease::default();
        self.base.from_dynamo_record_base(dynamo_record, &mut lease);
        // Java uses the nullable setters here; we only set when present because
        // our setters take non-Option. Absent values leave the fields unset,
        // which matches Java setting them to null.
        if let Some(stream_id) = safe_get_string(dynamo_record, STREAM_ID_KEY) {
            lease.set_stream_identifier(stream_id);
        }
        if let Some(shard_id) = safe_get_string(dynamo_record, SHARD_ID_KEY) {
            lease.set_shard_id(shard_id);
        }
        lease
    }

    fn from_dynamo_record_into(
        &self,
        dynamo_record: &HashMap<String, AttributeValue>,
        lease_to_update: &mut Lease,
    ) -> Result<(), LeasingError> {
        self.base
            .from_dynamo_record_base(dynamo_record, lease_to_update);
        if let Some(stream_id) = safe_get_string(dynamo_record, STREAM_ID_KEY) {
            lease_to_update.set_stream_identifier(stream_id);
        }
        if let Some(shard_id) = safe_get_string(dynamo_record, SHARD_ID_KEY) {
            lease_to_update.set_shard_id(shard_id);
        }
        Ok(())
    }

    fn get_dynamo_hash_key(&self, lease: &Lease) -> HashMap<String, AttributeValue> {
        self.base.get_dynamo_hash_key(lease)
    }

    fn get_dynamo_hash_key_from_key(&self, lease_key: &str) -> HashMap<String, AttributeValue> {
        self.base.get_dynamo_hash_key_from_key(lease_key)
    }

    fn get_dynamo_lease_counter_expectation(
        &self,
        lease: &Lease,
    ) -> HashMap<String, ExpectedAttributeValue> {
        self.base.get_dynamo_lease_counter_expectation(lease)
    }

    fn get_dynamo_lease_owner_expectation(
        &self,
        lease: &Lease,
    ) -> HashMap<String, ExpectedAttributeValue> {
        self.base.get_dynamo_lease_owner_expectation(lease)
    }

    fn get_dynamo_nonexistant_expectation(&self) -> HashMap<String, ExpectedAttributeValue> {
        self.base.get_dynamo_nonexistant_expectation()
    }

    fn get_dynamo_existent_expectation(
        &self,
        lease_key: &str,
    ) -> Result<HashMap<String, ExpectedAttributeValue>, LeasingError> {
        self.base.get_dynamo_existent_expectation(lease_key)
    }

    fn get_dynamo_lease_counter_update(
        &self,
        lease: &Lease,
    ) -> HashMap<String, AttributeValueUpdate> {
        self.base.get_dynamo_lease_counter_update(lease)
    }

    fn get_dynamo_take_lease_update(
        &self,
        lease: &Lease,
        new_owner: &str,
    ) -> HashMap<String, AttributeValueUpdate> {
        self.base.get_dynamo_take_lease_update(lease, new_owner)
    }

    fn get_dynamo_assign_lease_update(
        &self,
        lease: &Lease,
        new_owner: &str,
    ) -> Result<HashMap<String, AttributeValueUpdate>, LeasingError> {
        self.base.get_dynamo_assign_lease_update(lease, new_owner)
    }

    fn get_dynamo_evict_lease_update(
        &self,
        lease: &Lease,
    ) -> HashMap<String, AttributeValueUpdate> {
        self.base.get_dynamo_evict_lease_update(lease)
    }

    fn get_dynamo_update_lease_update(
        &self,
        lease: &Lease,
    ) -> HashMap<String, AttributeValueUpdate> {
        // Java: validateAndCast then super.getDynamoUpdateLeaseUpdate + stream/shard.
        lease.validate_multi_stream();
        let mut result = self.base.get_dynamo_update_lease_update_base(lease);
        result.insert(
            STREAM_ID_KEY.to_string(),
            DynamoDBLeaseSerializer::put_update(create_attribute_value_string(
                lease.stream_identifier().expect("multi-stream"),
            )),
        );
        result.insert(
            SHARD_ID_KEY.to_string(),
            DynamoDBLeaseSerializer::put_update(create_attribute_value_string(
                lease.shard_id().expect("multi-stream"),
            )),
        );
        result
    }

    fn get_dynamo_update_lease_update_field(
        &self,
        lease: &Lease,
        update_field: UpdateField,
    ) -> Result<HashMap<String, AttributeValueUpdate>, LeasingError> {
        self.base
            .get_dynamo_update_lease_update_field(lease, update_field)
    }

    fn get_key_schema(&self) -> Vec<KeySchemaElement> {
        self.base.get_key_schema()
    }

    fn get_worker_id_to_lease_key_index_key_schema(&self) -> Vec<KeySchemaElement> {
        self.base.get_worker_id_to_lease_key_index_key_schema()
    }

    fn get_worker_id_to_lease_key_index_attribute_definitions(&self) -> Vec<AttributeDefinition> {
        self.base
            .get_worker_id_to_lease_key_index_attribute_definitions()
    }

    fn get_attribute_definitions(&self) -> Vec<AttributeDefinition> {
        self.base.get_attribute_definitions()
    }

    fn get_dynamo_lease_throughput_kbps_update(
        &self,
        lease: &Lease,
    ) -> HashMap<String, AttributeValueUpdate> {
        self.base.get_dynamo_lease_throughput_kbps_update(lease)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::retrieval::kpl::ExtendedSequenceNumber;

    fn multi_stream_lease(lease_key: &str) -> Lease {
        let mut lease = Lease::default();
        lease.set_lease_key(lease_key);
        lease.set_lease_counter(0);
        lease.set_owner_switches_since_checkpoint(0);
        lease.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
        lease.set_stream_identifier("acct:stream:123");
        lease.set_shard_id("shardId-000");
        lease
    }

    #[test]
    fn to_dynamo_record_adds_stream_and_shard_with_legacy_names() {
        let serializer = DynamoDBMultiStreamLeaseSerializer::new();
        let record =
            serializer.to_dynamo_record(&multi_stream_lease("acct:stream:123:shardId-000"));
        assert_eq!(
            record.get("streamName").unwrap().as_s().unwrap(),
            "acct:stream:123"
        );
        assert_eq!(
            record.get("shardId").unwrap().as_s().unwrap(),
            "shardId-000"
        );
        assert_eq!(record.get("entityType").unwrap().as_s().unwrap(), "LEASE");
    }

    #[test]
    fn round_trip_multi_stream() {
        let serializer = DynamoDBMultiStreamLeaseSerializer::new();
        let mut original = multi_stream_lease("acct:stream:123:shardId-000");
        original.set_lease_owner(Some("worker-x".to_string()));
        original.set_lease_counter(7);
        let record = serializer.to_dynamo_record(&original);
        let deserialized = serializer.from_dynamo_record(&record);
        assert!(deserialized.is_multi_stream());
        assert_eq!(deserialized.stream_identifier(), Some("acct:stream:123"));
        assert_eq!(deserialized.shard_id(), Some("shardId-000"));
        assert_eq!(deserialized.lease_owner(), Some("worker-x"));
        assert_eq!(deserialized.lease_counter(), 7);
    }

    #[test]
    fn update_lease_update_adds_stream_and_shard() {
        let serializer = DynamoDBMultiStreamLeaseSerializer::new();
        let update = serializer.get_dynamo_update_lease_update(&multi_stream_lease("k"));
        assert!(update.contains_key("streamName"));
        assert!(update.contains_key("shardId"));
    }

    #[test]
    #[should_panic(expected = "MultiStreamLease")]
    fn to_dynamo_record_panics_on_single_stream() {
        let serializer = DynamoDBMultiStreamLeaseSerializer::new();
        let mut lease = Lease::default();
        lease.set_lease_key("k");
        lease.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
        serializer.to_dynamo_record(&lease);
    }
}
