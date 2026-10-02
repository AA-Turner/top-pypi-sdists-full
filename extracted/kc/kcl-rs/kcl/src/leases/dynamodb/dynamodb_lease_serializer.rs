//! Port of `software.amazon.kinesis.leases.dynamodb.DynamoDBLeaseSerializer`.
//!
//! Concrete [`LeaseSerializer`] implementation that maps [`Lease`] ↔ DynamoDB
//! attribute maps and builds the expectation / update maps used by
//! [`DynamoDBLeaseRefresher`](super::DynamoDBLeaseRefresher) for every CAS-style
//! operation. This pins the exact DynamoDB attribute layout, byte-for-byte.
//!
//! # Attribute schema (verbatim from Java)
//!
//! | attribute (DDB)                        | source                                     |
//! |----------------------------------------|--------------------------------------------|
//! | `leaseKey` (S, HASH key)               | `lease.lease_key`                          |
//! | `leaseOwner` (S)                       | `lease.lease_owner` (omitted if unset)     |
//! | `leaseCounter` (N)                     | `lease.lease_counter`                      |
//! | `ownerSwitchesSinceCheckpoint` (N)     | `lease.owner_switches_since_checkpoint`    |
//! | `checkpoint` (S)                       | `lease.checkpoint.sequence_number`         |
//! | `checkpointSubSequenceNumber` (N)      | `lease.checkpoint.sub_sequence_number`     |
//! | `parentShardId` (SS)                   | `lease.parent_shard_ids` (omitted if empty)|
//! | `childShardIds` (SS)                   | `lease.child_shard_ids` (omitted if empty) |
//! | `pendingCheckpoint` (S)                | `lease.pending_checkpoint.sequence_number` |
//! | `pendingCheckpointSubSequenceNumber`(N)| `lease.pending_checkpoint.sub_seq`         |
//! | `pendingCheckpointState` (B)           | see Java quirk below                       |
//! | `startingHashKey`/`endingHashKey` (S)  | `lease.hash_key_range_for_lease`           |
//! | `throughputKBps` (N)                   | `lease.throughput_kbps`                    |
//! | `checkpointOwner` (S)                  | `lease.checkpoint_owner`                   |
//! | `entityType` (S)                       | always `"LEASE"`                           |
//!
//! # Faithful Java quirk preserved
//!
//! In `toDynamoRecord`, when `pendingCheckpointState` is present the Java code
//! writes `DynamoUtils.createAttributeValue(lease.checkpoint().subSequenceNumber())`
//! — i.e. it stores the checkpoint's **sub-sequence-number as a number** under
//! the `pendingCheckpointState` key, *not* the actual byte state (an apparent
//! copy-paste bug). We reproduce this byte-for-byte so the wire format matches.

use std::collections::HashMap;

use aws_sdk_dynamodb::types::{
    AttributeAction, AttributeDefinition, AttributeValue, AttributeValueUpdate,
    ExpectedAttributeValue, KeySchemaElement, KeyType, ScalarAttributeType,
};

use crate::common::HashKeyRangeForLease;
use crate::leases::dynamo_utils::{
    create_attribute_value_double, create_attribute_value_long, create_attribute_value_string,
    create_attribute_value_string_set, safe_get_byte_array, safe_get_double, safe_get_long,
    safe_get_string, safe_get_string_set,
};
use crate::leases::exceptions::LeasingError;
use crate::leases::{EntityType, Lease, LeaseSerializer, UpdateField};
use crate::retrieval::kpl::ExtendedSequenceNumber;

// --- attribute-name constants (verbatim) ---
pub(crate) const LEASE_COUNTER_KEY: &str = "leaseCounter";
pub(crate) const OWNER_SWITCHES_KEY: &str = "ownerSwitchesSinceCheckpoint";
pub(crate) const CHECKPOINT_SUBSEQUENCE_NUMBER_KEY: &str = "checkpointSubSequenceNumber";
pub(crate) const PENDING_CHECKPOINT_SEQUENCE_KEY: &str = "pendingCheckpoint";
pub(crate) const PENDING_CHECKPOINT_SUBSEQUENCE_KEY: &str = "pendingCheckpointSubSequenceNumber";
pub(crate) const PENDING_CHECKPOINT_STATE_KEY: &str = "pendingCheckpointState";
pub(crate) const PARENT_SHARD_ID_KEY: &str = "parentShardId";
pub(crate) const CHILD_SHARD_IDS_KEY: &str = "childShardIds";
pub(crate) const STARTING_HASH_KEY: &str = "startingHashKey";
pub(crate) const ENDING_HASH_KEY: &str = "endingHashKey";
pub(crate) const THROUGHPUT_KBPS: &str = "throughputKBps";
pub(crate) const CHECKPOINT_SEQUENCE_NUMBER_KEY: &str = "checkpoint";
pub(crate) const CHECKPOINT_OWNER: &str = "checkpointOwner";
pub(crate) const LEASE_OWNER_KEY: &str = "leaseOwner";
/// The DynamoDB partition-key attribute name for a lease (Java `LEASE_KEY_KEY`).
pub const LEASE_KEY_KEY: &str = "leaseKey";
/// The DynamoDB `entityType` attribute name (Java `ENTITY_TYPE_ATTRIBUTE_NAME`).
pub const ENTITY_TYPE_ATTRIBUTE_NAME: &str = "entityType";

/// Basic [`LeaseSerializer`] for single-stream leases. Also serves as the
/// superclass behavior for
/// [`DynamoDBMultiStreamLeaseSerializer`](super::DynamoDBMultiStreamLeaseSerializer).
#[derive(Debug, Default, Clone)]
pub struct DynamoDBLeaseSerializer;

/// `#[allow(clippy::wrong_self_convention)]`: `from_dynamo_record_base` mirrors
/// the Java `fromDynamoRecord` instance method (it legitimately takes `&self`).
#[allow(clippy::wrong_self_convention)]
impl DynamoDBLeaseSerializer {
    /// New serializer.
    pub fn new() -> Self {
        Self
    }

    /// Java `putUpdate(AttributeValue)` (protected) — a `PUT` action wrapping the
    /// value. Used by the multi-stream subclass, hence `pub(crate)`.
    pub(crate) fn put_update(attribute_value: AttributeValue) -> AttributeValueUpdate {
        AttributeValueUpdate::builder()
            .value(attribute_value)
            .action(AttributeAction::Put)
            .build()
    }

    fn attribute_value_update_for_add() -> AttributeValueUpdate {
        AttributeValueUpdate::builder()
            .value(create_attribute_value_long(1))
            .action(AttributeAction::Add)
            .build()
    }

    fn build_expected_attribute_value_if_exists_or_value(
        value: Option<&str>,
    ) -> ExpectedAttributeValue {
        match value {
            None => ExpectedAttributeValue::builder().exists(false).build(),
            Some(v) => ExpectedAttributeValue::builder()
                .value(create_attribute_value_string(v))
                .build(),
        }
    }

    /// Common `toDynamoRecord` body — the multi-stream subclass calls this then
    /// adds its own fields. `pub(crate)` so the subclass can reuse it.
    pub(crate) fn to_dynamo_record_base(&self, lease: &Lease) -> HashMap<String, AttributeValue> {
        let mut result = HashMap::new();

        result.insert(
            LEASE_KEY_KEY.to_string(),
            create_attribute_value_string(lease.lease_key().expect("lease key must be set")),
        );
        result.insert(
            LEASE_COUNTER_KEY.to_string(),
            create_attribute_value_long(lease.lease_counter()),
        );

        if let Some(owner) = lease.lease_owner() {
            result.insert(
                LEASE_OWNER_KEY.to_string(),
                create_attribute_value_string(owner),
            );
        }

        result.insert(
            OWNER_SWITCHES_KEY.to_string(),
            create_attribute_value_long(lease.owner_switches_since_checkpoint()),
        );

        let checkpoint = lease.checkpoint().expect("checkpoint must be set");
        result.insert(
            CHECKPOINT_SEQUENCE_NUMBER_KEY.to_string(),
            create_attribute_value_string(checkpoint.sequence_number()),
        );
        result.insert(
            CHECKPOINT_SUBSEQUENCE_NUMBER_KEY.to_string(),
            create_attribute_value_long(checkpoint.sub_sequence_number()),
        );

        let parent_shard_ids = lease.parent_shard_ids();
        if !parent_shard_ids.is_empty() {
            result.insert(
                PARENT_SHARD_ID_KEY.to_string(),
                create_attribute_value_string_set(sorted(parent_shard_ids)),
            );
        }
        let child_shard_ids = lease.child_shard_ids();
        if !child_shard_ids.is_empty() {
            result.insert(
                CHILD_SHARD_IDS_KEY.to_string(),
                create_attribute_value_string_set(sorted(child_shard_ids)),
            );
        }

        if let Some(pending) = lease.pending_checkpoint() {
            if !pending.sequence_number().is_empty() {
                result.insert(
                    PENDING_CHECKPOINT_SEQUENCE_KEY.to_string(),
                    create_attribute_value_string(pending.sequence_number()),
                );
                result.insert(
                    PENDING_CHECKPOINT_SUBSEQUENCE_KEY.to_string(),
                    create_attribute_value_long(pending.sub_sequence_number()),
                );
            }
        }

        if lease.pending_checkpoint_state().is_some() {
            // Faithful Java quirk: writes the CHECKPOINT sub-sequence-number
            // (a number), not the actual byte state, under this key.
            result.insert(
                PENDING_CHECKPOINT_STATE_KEY.to_string(),
                create_attribute_value_long(checkpoint.sub_sequence_number()),
            );
        }

        if let Some(range) = lease.hash_key_range_for_lease() {
            result.insert(
                STARTING_HASH_KEY.to_string(),
                create_attribute_value_string(range.serialized_starting_hash_key()),
            );
            result.insert(
                ENDING_HASH_KEY.to_string(),
                create_attribute_value_string(range.serialized_ending_hash_key()),
            );
        }

        if let Some(kbps) = lease.throughput_kbps() {
            result.insert(
                THROUGHPUT_KBPS.to_string(),
                create_attribute_value_double(kbps),
            );
        }

        if let Some(checkpoint_owner) = lease.checkpoint_owner() {
            result.insert(
                CHECKPOINT_OWNER.to_string(),
                create_attribute_value_string(checkpoint_owner),
            );
        }

        result.insert(
            ENTITY_TYPE_ATTRIBUTE_NAME.to_string(),
            create_attribute_value_string(lease.entity_type().ddb_value()),
        );
        result
    }

    /// Common `fromDynamoRecord(map, leaseToUpdate)` body. Returns `false`
    /// (Java returns `null`) if the entity type is a non-lease type. `pub(crate)`
    /// so the multi-stream subclass can reuse it.
    pub(crate) fn from_dynamo_record_base(
        &self,
        dynamo_record: &HashMap<String, AttributeValue>,
        lease_to_update: &mut Lease,
    ) -> bool {
        let entity_type = safe_get_string(dynamo_record, ENTITY_TYPE_ATTRIBUTE_NAME);

        // Backward compatibility: a lease with no entityType (or the LEASE value)
        // is deserialized as a Lease. Any other entity type is not a lease.
        let is_lease = match &entity_type {
            None => true,
            Some(v) => v == EntityType::Lease.ddb_value(),
        };
        if !is_lease {
            return false;
        }

        if let Some(k) = safe_get_string(dynamo_record, LEASE_KEY_KEY) {
            lease_to_update.set_lease_key(k);
        }
        lease_to_update.set_lease_owner(safe_get_string(dynamo_record, LEASE_OWNER_KEY));
        lease_to_update
            .set_lease_counter(safe_get_long(dynamo_record, LEASE_COUNTER_KEY).unwrap_or(0));

        lease_to_update.set_owner_switches_since_checkpoint(
            safe_get_long(dynamo_record, OWNER_SWITCHES_KEY).unwrap_or(0),
        );
        lease_to_update.set_checkpoint(ExtendedSequenceNumber::new(
            safe_get_string(dynamo_record, CHECKPOINT_SEQUENCE_NUMBER_KEY).unwrap_or_default(),
            safe_get_long(dynamo_record, CHECKPOINT_SUBSEQUENCE_NUMBER_KEY),
        ));
        lease_to_update
            .set_parent_shard_ids(safe_get_string_set(dynamo_record, PARENT_SHARD_ID_KEY));
        lease_to_update
            .set_child_shard_ids(safe_get_string_set(dynamo_record, CHILD_SHARD_IDS_KEY));

        let pending_seq = safe_get_string(dynamo_record, PENDING_CHECKPOINT_SEQUENCE_KEY);
        if let Some(seq) = pending_seq {
            if !seq.is_empty() {
                lease_to_update.set_pending_checkpoint(Some(ExtendedSequenceNumber::new(
                    seq,
                    safe_get_long(dynamo_record, PENDING_CHECKPOINT_SUBSEQUENCE_KEY),
                )));
            }
        }

        lease_to_update.set_pending_checkpoint_state(safe_get_byte_array(
            dynamo_record,
            PENDING_CHECKPOINT_STATE_KEY,
        ));

        let starting = safe_get_string(dynamo_record, STARTING_HASH_KEY);
        let ending = safe_get_string(dynamo_record, ENDING_HASH_KEY);
        if let (Some(s), Some(e)) = (&starting, &ending) {
            if !s.is_empty() && !e.is_empty() {
                lease_to_update.set_hash_key_range(HashKeyRangeForLease::deserialize(s, e));
            }
        }

        if let Some(kbps) = safe_get_double(dynamo_record, THROUGHPUT_KBPS) {
            lease_to_update.set_throughput_kbps(kbps);
        }

        if let Some(owner) = safe_get_string(dynamo_record, CHECKPOINT_OWNER) {
            lease_to_update.set_checkpoint_owner(Some(owner));
        }

        true
    }

    /// Common `getDynamoUpdateLeaseUpdate(lease)` body. `pub(crate)` for the
    /// subclass.
    pub(crate) fn get_dynamo_update_lease_update_base(
        &self,
        lease: &Lease,
    ) -> HashMap<String, AttributeValueUpdate> {
        let mut result = HashMap::new();
        let checkpoint = lease.checkpoint().expect("checkpoint must be set");
        result.insert(
            CHECKPOINT_SEQUENCE_NUMBER_KEY.to_string(),
            Self::put_update(create_attribute_value_string(checkpoint.sequence_number())),
        );
        result.insert(
            CHECKPOINT_SUBSEQUENCE_NUMBER_KEY.to_string(),
            Self::put_update(create_attribute_value_long(
                checkpoint.sub_sequence_number(),
            )),
        );
        result.insert(
            OWNER_SWITCHES_KEY.to_string(),
            Self::put_update(create_attribute_value_long(
                lease.owner_switches_since_checkpoint(),
            )),
        );

        let has_pending = lease
            .pending_checkpoint()
            .map(|p| !p.sequence_number().is_empty())
            .unwrap_or(false);
        if has_pending {
            let pending = lease.pending_checkpoint().unwrap();
            result.insert(
                PENDING_CHECKPOINT_SEQUENCE_KEY.to_string(),
                Self::put_update(create_attribute_value_string(pending.sequence_number())),
            );
            result.insert(
                PENDING_CHECKPOINT_SUBSEQUENCE_KEY.to_string(),
                Self::put_update(create_attribute_value_long(pending.sub_sequence_number())),
            );
        } else {
            result.insert(PENDING_CHECKPOINT_SEQUENCE_KEY.to_string(), delete_update());
            result.insert(
                PENDING_CHECKPOINT_SUBSEQUENCE_KEY.to_string(),
                delete_update(),
            );
        }

        if let Some(state) = lease.pending_checkpoint_state() {
            result.insert(
                PENDING_CHECKPOINT_STATE_KEY.to_string(),
                Self::put_update(super::super::dynamo_utils::create_attribute_value_bytes(
                    state,
                )),
            );
        } else {
            result.insert(PENDING_CHECKPOINT_STATE_KEY.to_string(), delete_update());
        }

        let child_shard_ids = lease.child_shard_ids();
        if !child_shard_ids.is_empty() {
            result.insert(
                CHILD_SHARD_IDS_KEY.to_string(),
                Self::put_update(create_attribute_value_string_set(sorted(child_shard_ids))),
            );
        }

        if let Some(range) = lease.hash_key_range_for_lease() {
            result.insert(
                STARTING_HASH_KEY.to_string(),
                Self::put_update(create_attribute_value_string(
                    range.serialized_starting_hash_key(),
                )),
            );
            result.insert(
                ENDING_HASH_KEY.to_string(),
                Self::put_update(create_attribute_value_string(
                    range.serialized_ending_hash_key(),
                )),
            );
        }

        result
    }

    /// Java `getDynamoLeaseCounterExpectation(Long)`.
    pub fn get_dynamo_lease_counter_expectation_from_counter(
        &self,
        lease_counter: i64,
    ) -> HashMap<String, ExpectedAttributeValue> {
        let mut result = HashMap::new();
        result.insert(
            LEASE_COUNTER_KEY.to_string(),
            ExpectedAttributeValue::builder()
                .value(create_attribute_value_long(lease_counter))
                .build(),
        );
        result
    }

    /// Java `getDynamoLeaseCounterUpdate(Long)`.
    pub fn get_dynamo_lease_counter_update_from_counter(
        &self,
        lease_counter: i64,
    ) -> HashMap<String, AttributeValueUpdate> {
        let mut result = HashMap::new();
        result.insert(
            LEASE_COUNTER_KEY.to_string(),
            AttributeValueUpdate::builder()
                .value(create_attribute_value_long(lease_counter + 1))
                .action(AttributeAction::Put)
                .build(),
        );
        result
    }
}

fn delete_update() -> AttributeValueUpdate {
    AttributeValueUpdate::builder()
        .action(AttributeAction::Delete)
        .build()
}

/// A stable, sorted `Vec<String>` from a `HashSet<String>`. Java stores
/// `parentShardIds`/`childShardIds` as `HashSet` and hands them to
/// `DynamoUtils.createAttributeValue(Collection)` (which builds an `SS`). Order
/// within a DDB string-set is not semantically meaningful, but we sort for a
/// deterministic wire form (tests compare sets, not order).
fn sorted(set: std::collections::HashSet<String>) -> Vec<String> {
    let mut v: Vec<String> = set.into_iter().collect();
    v.sort();
    v
}

impl LeaseSerializer for DynamoDBLeaseSerializer {
    fn to_dynamo_record(&self, lease: &Lease) -> HashMap<String, AttributeValue> {
        self.to_dynamo_record_base(lease)
    }

    fn from_dynamo_record(&self, dynamo_record: &HashMap<String, AttributeValue>) -> Lease {
        let mut lease = Lease::default();
        self.from_dynamo_record_base(dynamo_record, &mut lease);
        lease
    }

    fn from_dynamo_record_into(
        &self,
        dynamo_record: &HashMap<String, AttributeValue>,
        lease_to_update: &mut Lease,
    ) -> Result<(), LeasingError> {
        self.from_dynamo_record_base(dynamo_record, lease_to_update);
        Ok(())
    }

    fn get_dynamo_hash_key(&self, lease: &Lease) -> HashMap<String, AttributeValue> {
        self.get_dynamo_hash_key_from_key(lease.lease_key().expect("lease key must be set"))
    }

    fn get_dynamo_hash_key_from_key(&self, lease_key: &str) -> HashMap<String, AttributeValue> {
        let mut result = HashMap::new();
        result.insert(
            LEASE_KEY_KEY.to_string(),
            create_attribute_value_string(lease_key),
        );
        result
    }

    fn get_dynamo_lease_counter_expectation(
        &self,
        lease: &Lease,
    ) -> HashMap<String, ExpectedAttributeValue> {
        self.get_dynamo_lease_counter_expectation_from_counter(lease.lease_counter())
    }

    fn get_dynamo_lease_owner_expectation(
        &self,
        lease: &Lease,
    ) -> HashMap<String, ExpectedAttributeValue> {
        let mut result = HashMap::new();
        result.insert(
            LEASE_OWNER_KEY.to_string(),
            Self::build_expected_attribute_value_if_exists_or_value(lease.lease_owner()),
        );
        result.insert(
            CHECKPOINT_OWNER.to_string(),
            Self::build_expected_attribute_value_if_exists_or_value(lease.checkpoint_owner()),
        );
        result
    }

    fn get_dynamo_nonexistant_expectation(&self) -> HashMap<String, ExpectedAttributeValue> {
        let mut result = HashMap::new();
        result.insert(
            LEASE_KEY_KEY.to_string(),
            ExpectedAttributeValue::builder().exists(false).build(),
        );
        result
    }

    fn get_dynamo_existent_expectation(
        &self,
        lease_key: &str,
    ) -> Result<HashMap<String, ExpectedAttributeValue>, LeasingError> {
        let mut result = HashMap::new();
        result.insert(
            LEASE_KEY_KEY.to_string(),
            ExpectedAttributeValue::builder()
                .exists(true)
                .value(create_attribute_value_string(lease_key))
                .build(),
        );
        Ok(result)
    }

    fn get_dynamo_lease_counter_update(
        &self,
        lease: &Lease,
    ) -> HashMap<String, AttributeValueUpdate> {
        self.get_dynamo_lease_counter_update_from_counter(lease.lease_counter())
    }

    fn get_dynamo_take_lease_update(
        &self,
        lease: &Lease,
        new_owner: &str,
    ) -> HashMap<String, AttributeValueUpdate> {
        let mut result = HashMap::new();
        result.insert(
            LEASE_OWNER_KEY.to_string(),
            AttributeValueUpdate::builder()
                .value(create_attribute_value_string(new_owner))
                .action(AttributeAction::Put)
                .build(),
        );
        // takeLease/assignLease want the checkpoint owner deleted (fresh assignment).
        result.insert(CHECKPOINT_OWNER.to_string(), delete_update());

        let old_owner = lease.lease_owner();
        let checkpoint_owner = lease.checkpoint_owner();
        // if checkpoint owner is not null, this update removes the checkpoint owner
        // and transfers ownership to the leaseOwner, so increment the owner-switch key.
        let increment = (old_owner.is_some() && old_owner != Some(new_owner))
            || (checkpoint_owner.is_some() && checkpoint_owner == Some(new_owner));
        if increment {
            result.insert(
                OWNER_SWITCHES_KEY.to_string(),
                AttributeValueUpdate::builder()
                    .value(create_attribute_value_long(1))
                    .action(AttributeAction::Add)
                    .build(),
            );
        }
        result
    }

    fn get_dynamo_assign_lease_update(
        &self,
        lease: &Lease,
        new_owner: &str,
    ) -> Result<HashMap<String, AttributeValueUpdate>, LeasingError> {
        let mut result = self.get_dynamo_take_lease_update(lease, new_owner);
        // assign uses ADD(1) on the counter (atomic increment) instead of PUT(counter+1).
        result.insert(
            LEASE_COUNTER_KEY.to_string(),
            Self::attribute_value_update_for_add(),
        );
        Ok(result)
    }

    fn get_dynamo_evict_lease_update(
        &self,
        lease: &Lease,
    ) -> HashMap<String, AttributeValueUpdate> {
        let mut result = HashMap::new();
        // if checkpointOwner is null, remove the leaseOwner; otherwise leave the
        // leaseOwner so the pending new owner can inherit it.
        if lease.checkpoint_owner().is_none() {
            result.insert(LEASE_OWNER_KEY.to_string(), delete_update());
        }
        // always remove checkpointOwner (ok even if null).
        result.insert(CHECKPOINT_OWNER.to_string(), delete_update());
        result.insert(
            LEASE_COUNTER_KEY.to_string(),
            Self::attribute_value_update_for_add(),
        );
        result
    }

    fn get_dynamo_update_lease_update(
        &self,
        lease: &Lease,
    ) -> HashMap<String, AttributeValueUpdate> {
        self.get_dynamo_update_lease_update_base(lease)
    }

    fn get_dynamo_update_lease_update_field(
        &self,
        lease: &Lease,
        update_field: UpdateField,
    ) -> Result<HashMap<String, AttributeValueUpdate>, LeasingError> {
        let mut result = HashMap::new();
        match update_field {
            UpdateField::ChildShards => {
                let child_shard_ids = lease.child_shard_ids();
                if !child_shard_ids.is_empty() {
                    result.insert(
                        CHILD_SHARD_IDS_KEY.to_string(),
                        Self::put_update(create_attribute_value_string_set(sorted(
                            child_shard_ids,
                        ))),
                    );
                }
            }
            UpdateField::HashKeyRange => {
                if let Some(range) = lease.hash_key_range_for_lease() {
                    result.insert(
                        STARTING_HASH_KEY.to_string(),
                        Self::put_update(create_attribute_value_string(
                            range.serialized_starting_hash_key(),
                        )),
                    );
                    result.insert(
                        ENDING_HASH_KEY.to_string(),
                        Self::put_update(create_attribute_value_string(
                            range.serialized_ending_hash_key(),
                        )),
                    );
                }
            }
        }
        Ok(result)
    }

    fn get_key_schema(&self) -> Vec<KeySchemaElement> {
        vec![KeySchemaElement::builder()
            .attribute_name(LEASE_KEY_KEY)
            .key_type(KeyType::Hash)
            .build()
            .expect("valid key schema")]
    }

    fn get_worker_id_to_lease_key_index_key_schema(&self) -> Vec<KeySchemaElement> {
        vec![
            KeySchemaElement::builder()
                .attribute_name(LEASE_OWNER_KEY)
                .key_type(KeyType::Hash)
                .build()
                .expect("valid key schema"),
            KeySchemaElement::builder()
                .attribute_name(LEASE_KEY_KEY)
                .key_type(KeyType::Range)
                .build()
                .expect("valid key schema"),
        ]
    }

    fn get_worker_id_to_lease_key_index_attribute_definitions(&self) -> Vec<AttributeDefinition> {
        vec![
            AttributeDefinition::builder()
                .attribute_name(LEASE_OWNER_KEY)
                .attribute_type(ScalarAttributeType::S)
                .build()
                .expect("valid attribute definition"),
            AttributeDefinition::builder()
                .attribute_name(LEASE_KEY_KEY)
                .attribute_type(ScalarAttributeType::S)
                .build()
                .expect("valid attribute definition"),
        ]
    }

    fn get_attribute_definitions(&self) -> Vec<AttributeDefinition> {
        vec![AttributeDefinition::builder()
            .attribute_name(LEASE_KEY_KEY)
            .attribute_type(ScalarAttributeType::S)
            .build()
            .expect("valid attribute definition")]
    }

    fn get_dynamo_lease_throughput_kbps_update(
        &self,
        lease: &Lease,
    ) -> HashMap<String, AttributeValueUpdate> {
        let mut result = HashMap::new();
        result.insert(
            THROUGHPUT_KBPS.to_string(),
            AttributeValueUpdate::builder()
                .value(create_attribute_value_double(
                    lease.throughput_kbps().expect("throughput must be set"),
                ))
                .action(AttributeAction::Put)
                .build(),
        );
        result
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn minimal_lease(lease_key: &str) -> Lease {
        let mut lease = Lease::default();
        lease.set_lease_key(lease_key);
        lease.set_lease_counter(0);
        lease.set_owner_switches_since_checkpoint(0);
        lease.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
        lease
    }

    fn minimal_record(lease_key: &str) -> HashMap<String, AttributeValue> {
        let mut record = HashMap::new();
        record.insert(
            LEASE_KEY_KEY.to_string(),
            AttributeValue::S(lease_key.to_string()),
        );
        record.insert(
            LEASE_COUNTER_KEY.to_string(),
            AttributeValue::N("0".to_string()),
        );
        record.insert(
            OWNER_SWITCHES_KEY.to_string(),
            AttributeValue::N("0".to_string()),
        );
        record.insert(
            CHECKPOINT_SEQUENCE_NUMBER_KEY.to_string(),
            AttributeValue::S("TRIM_HORIZON".to_string()),
        );
        record.insert(
            CHECKPOINT_SUBSEQUENCE_NUMBER_KEY.to_string(),
            AttributeValue::N("0".to_string()),
        );
        record
    }

    // --- toDynamoRecord tests ---

    #[test]
    fn to_dynamo_record_includes_entity_type_attribute() {
        let serializer = DynamoDBLeaseSerializer::new();
        let record = serializer.to_dynamo_record(&minimal_lease("shard-001"));
        assert!(record.contains_key("entityType"));
        assert_eq!(record.get("entityType").unwrap().as_s().unwrap(), "LEASE");
    }

    #[test]
    fn to_dynamo_record_entity_type_is_lease() {
        let serializer = DynamoDBLeaseSerializer::new();
        let mut lease = minimal_lease("shard-002");
        lease.set_lease_owner(Some("worker-1".to_string()));
        let record = serializer.to_dynamo_record(&lease);
        assert_eq!(
            record.get("entityType").unwrap().as_s().unwrap(),
            EntityType::Lease.ddb_value()
        );
        assert_eq!(
            record.get("leaseOwner").unwrap().as_s().unwrap(),
            "worker-1"
        );
    }

    // --- fromDynamoRecord backward compatibility tests ---

    #[test]
    fn from_dynamo_record_with_no_entity_type_deserializes_as_lease() {
        let serializer = DynamoDBLeaseSerializer::new();
        let record = minimal_record("shard-001");
        let result = serializer.from_dynamo_record(&record);
        assert_eq!(result.lease_key(), Some("shard-001"));
    }

    #[test]
    fn from_dynamo_record_with_lease_entity_type_deserializes_as_lease() {
        let serializer = DynamoDBLeaseSerializer::new();
        let mut record = minimal_record("shard-002");
        record.insert(
            "entityType".to_string(),
            AttributeValue::S("LEASE".to_string()),
        );
        let result = serializer.from_dynamo_record(&record);
        assert_eq!(result.lease_key(), Some("shard-002"));
    }

    #[test]
    fn from_dynamo_record_with_worker_metric_stats_entity_type_returns_empty_lease() {
        // Java returns null; our from_dynamo_record returns a default (empty) Lease
        // (leaseKey unset). The DAO strips entityType before calling this, so this
        // only matters for the direct serializer contract: a non-lease record does
        // not populate the lease.
        let serializer = DynamoDBLeaseSerializer::new();
        let mut record = minimal_record("worker-metrics-key");
        record.insert(
            "entityType".to_string(),
            AttributeValue::S("WORKER_METRIC_STATS".to_string()),
        );
        let result = serializer.from_dynamo_record(&record);
        assert_eq!(result.lease_key(), None);
    }

    #[test]
    fn from_dynamo_record_into_returns_false_for_non_lease() {
        let serializer = DynamoDBLeaseSerializer::new();
        for entity in [
            "WORKER_METRIC_STATS",
            "STREAM",
            "LEADER",
            "CLIENT_VERSION_MIGRATION",
            "TABLE_MIGRATION",
            "SOME_FUTURE_TYPE",
        ] {
            let mut record = minimal_record("k");
            record.insert(
                "entityType".to_string(),
                AttributeValue::S(entity.to_string()),
            );
            let mut lease = Lease::default();
            let is_lease = serializer.from_dynamo_record_base(&record, &mut lease);
            assert!(!is_lease, "{entity} must not be a lease");
            assert_eq!(lease.lease_key(), None);
        }
    }

    #[test]
    fn from_dynamo_record_lease_entity_type_populates() {
        let serializer = DynamoDBLeaseSerializer::new();
        let mut record = minimal_record("shard-004");
        record.insert(
            "entityType".to_string(),
            AttributeValue::S("LEASE".to_string()),
        );
        let mut lease = Lease::default();
        let is_lease = serializer.from_dynamo_record_base(&record, &mut lease);
        assert!(is_lease);
        assert_eq!(lease.lease_key(), Some("shard-004"));
    }

    // --- fromDynamoRecord with existing lease (update) ---

    /// Port of `DynamoDBLeaseSerializerTest.fromDynamoRecord_withExistingLease_noEntityType_updatesLease`.
    ///
    /// Java's `fromDynamoRecord(record, existingLease)` updates the passed-in
    /// lease in place; here `from_dynamo_record_base(record, &mut existing)` is the
    /// same seam (`from_dynamo_record_into` wraps it). No entityType => backward
    /// compat => deserialize into the existing lease.
    #[test]
    fn from_dynamo_record_with_existing_lease_no_entity_type_updates_lease() {
        let serializer = DynamoDBLeaseSerializer::new();
        let record = minimal_record("shard-003");
        // Deliberately no entityType attribute.
        let mut existing_lease = Lease::default();
        let is_lease = serializer.from_dynamo_record_base(&record, &mut existing_lease);
        assert!(is_lease);
        assert_eq!(existing_lease.lease_key(), Some("shard-003"));
    }

    /// Port of `DynamoDBLeaseSerializerTest.fromDynamoRecord_withExistingLease_leaseEntityType_updatesLease`.
    #[test]
    fn from_dynamo_record_with_existing_lease_lease_entity_type_updates_lease() {
        let serializer = DynamoDBLeaseSerializer::new();
        let mut record = minimal_record("shard-004");
        record.insert(
            "entityType".to_string(),
            AttributeValue::S("LEASE".to_string()),
        );
        let mut existing_lease = Lease::default();
        let is_lease = serializer.from_dynamo_record_base(&record, &mut existing_lease);
        assert!(is_lease);
        assert_eq!(existing_lease.lease_key(), Some("shard-004"));
    }

    /// Port of `DynamoDBLeaseSerializerTest.fromDynamoRecord_withExistingLease_nonLeaseEntityType_returnsNull`.
    ///
    /// A non-LEASE entity type leaves the existing lease untouched; Java returns
    /// `null`, which is `is_lease == false` here.
    #[test]
    fn from_dynamo_record_with_existing_lease_non_lease_entity_type_returns_null() {
        let serializer = DynamoDBLeaseSerializer::new();
        let mut record = minimal_record("worker-key");
        record.insert(
            "entityType".to_string(),
            AttributeValue::S("WORKER_METRIC_STATS".to_string()),
        );
        let mut existing_lease = Lease::default();
        let is_lease = serializer.from_dynamo_record_base(&record, &mut existing_lease);
        assert!(!is_lease);
        // The existing lease was left untouched (leaseKey never set).
        assert_eq!(existing_lease.lease_key(), None);
    }

    // --- Round-trip test ---

    #[test]
    fn round_trip_serialize_deserialize_preserves_lease_fields() {
        let serializer = DynamoDBLeaseSerializer::new();
        let mut original = minimal_lease("shard-round-trip");
        original.set_lease_owner(Some("test-owner".to_string()));
        original.set_lease_counter(42);

        let record = serializer.to_dynamo_record(&original);
        let deserialized = serializer.from_dynamo_record(&record);

        assert_eq!(deserialized.lease_key(), Some("shard-round-trip"));
        assert_eq!(deserialized.lease_owner(), Some("test-owner"));
        assert_eq!(deserialized.lease_counter(), 42);
    }

    #[test]
    fn entity_type_constant_matches() {
        assert_eq!(ENTITY_TYPE_ATTRIBUTE_NAME, "entityType");
    }

    // --- key schema / attribute definitions ---

    #[test]
    fn key_schema_and_attribute_definitions() {
        let serializer = DynamoDBLeaseSerializer::new();
        let ks = serializer.get_key_schema();
        assert_eq!(ks.len(), 1);
        assert_eq!(ks[0].attribute_name(), "leaseKey");
        assert_eq!(ks[0].key_type(), &KeyType::Hash);

        let defs = serializer.get_attribute_definitions();
        assert_eq!(defs.len(), 1);
        assert_eq!(defs[0].attribute_name(), "leaseKey");

        let gsi_ks = serializer.get_worker_id_to_lease_key_index_key_schema();
        assert_eq!(gsi_ks.len(), 2);
        assert_eq!(gsi_ks[0].attribute_name(), "leaseOwner");
        assert_eq!(gsi_ks[0].key_type(), &KeyType::Hash);
        assert_eq!(gsi_ks[1].attribute_name(), "leaseKey");
        assert_eq!(gsi_ks[1].key_type(), &KeyType::Range);

        let gsi_defs = serializer.get_worker_id_to_lease_key_index_attribute_definitions();
        assert_eq!(gsi_defs.len(), 2);
    }

    // --- update / expectation builders ---

    #[test]
    fn lease_counter_update_is_put_counter_plus_one() {
        let serializer = DynamoDBLeaseSerializer::new();
        let mut lease = minimal_lease("k");
        lease.set_lease_counter(5);
        let update = serializer.get_dynamo_lease_counter_update(&lease);
        let avu = update.get(LEASE_COUNTER_KEY).unwrap();
        assert_eq!(avu.action(), Some(&AttributeAction::Put));
        assert_eq!(avu.value().unwrap().as_n().unwrap(), "6");
    }

    #[test]
    fn assign_lease_update_uses_add_on_counter() {
        let serializer = DynamoDBLeaseSerializer::new();
        let mut lease = minimal_lease("k");
        lease.set_lease_counter(5);
        lease.set_lease_owner(Some("old".to_string()));
        let update = serializer
            .get_dynamo_assign_lease_update(&lease, "new")
            .unwrap();
        let avu = update.get(LEASE_COUNTER_KEY).unwrap();
        assert_eq!(avu.action(), Some(&AttributeAction::Add));
        assert_eq!(avu.value().unwrap().as_n().unwrap(), "1");
        // owner PUT + checkpointOwner DELETE
        assert_eq!(
            update.get(LEASE_OWNER_KEY).unwrap().action(),
            Some(&AttributeAction::Put)
        );
        assert_eq!(
            update.get(CHECKPOINT_OWNER).unwrap().action(),
            Some(&AttributeAction::Delete)
        );
        // owner switches incremented because old != new
        assert_eq!(
            update.get(OWNER_SWITCHES_KEY).unwrap().action(),
            Some(&AttributeAction::Add)
        );
    }

    #[test]
    fn take_lease_update_owner_switch_from_checkpoint_owner() {
        let serializer = DynamoDBLeaseSerializer::new();
        let mut lease = minimal_lease("k");
        // graceful-handoff completion case: checkpointOwner == new owner
        lease.set_lease_owner(None);
        lease.set_checkpoint_owner(Some("new".to_string()));
        let update = serializer.get_dynamo_take_lease_update(&lease, "new");
        assert_eq!(
            update.get(OWNER_SWITCHES_KEY).unwrap().action(),
            Some(&AttributeAction::Add)
        );
    }

    #[test]
    fn take_lease_update_no_switch_when_same_owner() {
        let serializer = DynamoDBLeaseSerializer::new();
        let mut lease = minimal_lease("k");
        lease.set_lease_owner(Some("same".to_string()));
        let update = serializer.get_dynamo_take_lease_update(&lease, "same");
        assert!(!update.contains_key(OWNER_SWITCHES_KEY));
    }

    #[test]
    fn evict_lease_update_deletes_owner_when_no_checkpoint_owner() {
        let serializer = DynamoDBLeaseSerializer::new();
        let mut lease = minimal_lease("k");
        lease.set_lease_owner(Some("owner".to_string()));
        let update = serializer.get_dynamo_evict_lease_update(&lease);
        assert_eq!(
            update.get(LEASE_OWNER_KEY).unwrap().action(),
            Some(&AttributeAction::Delete)
        );
        assert_eq!(
            update.get(CHECKPOINT_OWNER).unwrap().action(),
            Some(&AttributeAction::Delete)
        );
        assert_eq!(
            update.get(LEASE_COUNTER_KEY).unwrap().action(),
            Some(&AttributeAction::Add)
        );
    }

    #[test]
    fn evict_lease_update_keeps_owner_when_checkpoint_owner_set() {
        let serializer = DynamoDBLeaseSerializer::new();
        let mut lease = minimal_lease("k");
        lease.set_lease_owner(Some("owner".to_string()));
        lease.set_checkpoint_owner(Some("cp".to_string()));
        let update = serializer.get_dynamo_evict_lease_update(&lease);
        assert!(!update.contains_key(LEASE_OWNER_KEY));
        assert_eq!(
            update.get(CHECKPOINT_OWNER).unwrap().action(),
            Some(&AttributeAction::Delete)
        );
    }

    #[test]
    fn nonexistant_and_existent_expectations() {
        let serializer = DynamoDBLeaseSerializer::new();
        let ne = serializer.get_dynamo_nonexistant_expectation();
        assert_eq!(ne.get(LEASE_KEY_KEY).unwrap().exists(), Some(false));
        let ex = serializer.get_dynamo_existent_expectation("k").unwrap();
        assert_eq!(ex.get(LEASE_KEY_KEY).unwrap().exists(), Some(true));
        assert_eq!(
            ex.get(LEASE_KEY_KEY)
                .unwrap()
                .value()
                .unwrap()
                .as_s()
                .unwrap(),
            "k"
        );
    }

    #[test]
    fn lease_owner_expectation_uses_exists_false_when_null() {
        let serializer = DynamoDBLeaseSerializer::new();
        let lease = minimal_lease("k"); // no owner, no checkpoint owner
        let exp = serializer.get_dynamo_lease_owner_expectation(&lease);
        assert_eq!(exp.get(LEASE_OWNER_KEY).unwrap().exists(), Some(false));
        assert_eq!(exp.get(CHECKPOINT_OWNER).unwrap().exists(), Some(false));
    }

    #[test]
    fn update_lease_update_deletes_pending_when_absent() {
        let serializer = DynamoDBLeaseSerializer::new();
        let lease = minimal_lease("k");
        let update = serializer.get_dynamo_update_lease_update(&lease);
        assert_eq!(
            update
                .get(PENDING_CHECKPOINT_SEQUENCE_KEY)
                .unwrap()
                .action(),
            Some(&AttributeAction::Delete)
        );
        assert_eq!(
            update.get(PENDING_CHECKPOINT_STATE_KEY).unwrap().action(),
            Some(&AttributeAction::Delete)
        );
        assert_eq!(
            update.get(CHECKPOINT_SEQUENCE_NUMBER_KEY).unwrap().action(),
            Some(&AttributeAction::Put)
        );
    }

    #[test]
    fn throughput_update() {
        let serializer = DynamoDBLeaseSerializer::new();
        let mut lease = minimal_lease("k");
        lease.set_throughput_kbps(12.5);
        let update = serializer.get_dynamo_lease_throughput_kbps_update(&lease);
        let avu = update.get(THROUGHPUT_KBPS).unwrap();
        assert_eq!(avu.action(), Some(&AttributeAction::Put));
        assert_eq!(avu.value().unwrap().as_n().unwrap(), "12.5");
    }
}
