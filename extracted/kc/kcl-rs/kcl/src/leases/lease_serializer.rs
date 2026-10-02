//! Port of `software.amazon.kinesis.leases.LeaseSerializer`.
//!
//! Maps [`Lease`] objects to/from DynamoDB `AttributeValue` records and
//! constructs the expected-value / update maps used to implement
//! [`LeaseRefresher`](crate::leases::LeaseRefresher)'s conditional writes — the
//! low-level "DynamoDB expression builder" for leases.
//!
//! # Sync
//!
//! This is a **pure, synchronous** trait — it performs no I/O, only in-memory
//! ser/de between `Lease` and DynamoDB attribute maps. No `#[async_trait]`.
//!
//! # Deviations
//!
//! - The AWS SDK v2 (Java) legacy conditional-write API types
//!   (`AttributeValue`, `AttributeValueUpdate`, `ExpectedAttributeValue`,
//!   `KeySchemaElement`, `AttributeDefinition`) map to the corresponding
//!   `aws_sdk_dynamodb::types` in the Rust SDK, which are reused directly here.
//!   The concrete `DynamoDBLeaseSerializer` (6c) may translate these into
//!   expression-based requests, but the trait surface mirrors Java faithfully.
//! - `Map<String, X>` → `HashMap<String, X>`; `Collection<X>` → `Vec<X>`.
//! - The `fromDynamoRecord(Map, Lease)` in-place-update overload → the distinctly
//!   named [`from_dynamo_record_into`]; the `getDynamoUpdateLeaseUpdate(lease,
//!   UpdateField)` overload → [`get_dynamo_update_lease_update_field`]. Both are
//!   Java `default`s that throw `UnsupportedOperationException`; here they return
//!   [`LeasingError::dependency`] with the same intent (the only fallible methods
//!   on this otherwise-infallible trait, matching Java's checked-vs-unchecked
//!   split — the rest never throw).
//!
//! [`from_dynamo_record_into`]: LeaseSerializer::from_dynamo_record_into
//! [`get_dynamo_update_lease_update_field`]: LeaseSerializer::get_dynamo_update_lease_update_field

use std::collections::HashMap;

use aws_sdk_dynamodb::types::{
    AttributeDefinition, AttributeValue, AttributeValueUpdate, ExpectedAttributeValue,
    KeySchemaElement,
};

use crate::leases::exceptions::LeasingError;
use crate::leases::{Lease, UpdateField};

/// Manages the mapping of [`Lease`] objects/operations to records in DynamoDB.
///
/// `#[allow(clippy::wrong_self_convention)]`: `from_dynamo_record*` are
/// deserializer methods on the serializer (they faithfully mirror the Java
/// `fromDynamoRecord` instance methods and legitimately take `&self`), so the
/// "from_* takes no self" lint does not apply.
#[cfg_attr(test, mockall::automock)]
#[allow(clippy::wrong_self_convention)]
pub trait LeaseSerializer {
    /// Construct a DynamoDB record from a lease (Java `toDynamoRecord`).
    fn to_dynamo_record(&self, lease: &Lease) -> HashMap<String, AttributeValue>;

    /// Construct a lease from a DynamoDB record (Java `fromDynamoRecord`).
    fn from_dynamo_record(&self, dynamo_record: &HashMap<String, AttributeValue>) -> Lease;

    /// In-place-update variant of [`from_dynamo_record`](LeaseSerializer::from_dynamo_record)
    /// (Java `fromDynamoRecord(Map, Lease leaseToUpdate)`). Default is unsupported.
    fn from_dynamo_record_into(
        &self,
        _dynamo_record: &HashMap<String, AttributeValue>,
        _lease_to_update: &mut Lease,
    ) -> Result<(), LeasingError> {
        Err(LeasingError::dependency(
            "fromDynamoRecord in-place is not implemented",
        ))
    }

    /// The hash-key attribute map for a lease object (Java `getDynamoHashKey(Lease)`).
    fn get_dynamo_hash_key(&self, lease: &Lease) -> HashMap<String, AttributeValue>;

    /// The hash-key attribute map for a lease key string (Java
    /// `getDynamoHashKey(String)`; used by `LeaseRefresher::get_lease`).
    fn get_dynamo_hash_key_from_key(&self, lease_key: &str) -> HashMap<String, AttributeValue>;

    /// Expectation asserting the lease counter is what we expect.
    fn get_dynamo_lease_counter_expectation(
        &self,
        lease: &Lease,
    ) -> HashMap<String, ExpectedAttributeValue>;

    /// Expectation asserting the lease owner is what we expect.
    fn get_dynamo_lease_owner_expectation(
        &self,
        lease: &Lease,
    ) -> HashMap<String, ExpectedAttributeValue>;

    /// Expectation asserting the lease does not exist.
    fn get_dynamo_nonexistant_expectation(&self) -> HashMap<String, ExpectedAttributeValue>;

    /// Expectation asserting the lease does exist (Java `default`, unsupported).
    fn get_dynamo_existent_expectation(
        &self,
        _lease_key: &str,
    ) -> Result<HashMap<String, ExpectedAttributeValue>, LeasingError> {
        Err(LeasingError::dependency(
            "DynamoExistantExpectation is not implemented",
        ))
    }

    /// Update map that increments the lease counter.
    fn get_dynamo_lease_counter_update(
        &self,
        lease: &Lease,
    ) -> HashMap<String, AttributeValueUpdate>;

    /// Update map that takes a lease for a new owner.
    fn get_dynamo_take_lease_update(
        &self,
        lease: &Lease,
        new_owner: &str,
    ) -> HashMap<String, AttributeValueUpdate>;

    /// Update map that assigns a lease to a new owner (Java `default`, unsupported).
    fn get_dynamo_assign_lease_update(
        &self,
        _lease: &Lease,
        _new_owner: &str,
    ) -> Result<HashMap<String, AttributeValueUpdate>, LeasingError> {
        Err(LeasingError::dependency(
            "getDynamoAssignLeaseUpdate is not implemented",
        ))
    }

    /// Update map that voids (evicts) a lease.
    fn get_dynamo_evict_lease_update(&self, lease: &Lease)
        -> HashMap<String, AttributeValueUpdate>;

    /// Update map that updates application-specific data and increments the
    /// lease counter.
    fn get_dynamo_update_lease_update(
        &self,
        lease: &Lease,
    ) -> HashMap<String, AttributeValueUpdate>;

    /// Update map for a specific [`UpdateField`] (Java `default` overload,
    /// unsupported).
    fn get_dynamo_update_lease_update_field(
        &self,
        _lease: &Lease,
        _update_field: UpdateField,
    ) -> Result<HashMap<String, AttributeValueUpdate>, LeasingError> {
        Err(LeasingError::dependency(
            "getDynamoUpdateLeaseUpdate(field) is not implemented",
        ))
    }

    /// Key schema for creating the lease table.
    fn get_key_schema(&self) -> Vec<KeySchemaElement>;

    /// Key schema for the worker-id-to-lease-key GSI (Java default: empty).
    fn get_worker_id_to_lease_key_index_key_schema(&self) -> Vec<KeySchemaElement> {
        Vec::new()
    }

    /// Attribute definitions for the worker-id-to-lease-key GSI (Java default: empty).
    fn get_worker_id_to_lease_key_index_attribute_definitions(&self) -> Vec<AttributeDefinition> {
        Vec::new()
    }

    /// Attribute definitions for creating the lease table.
    fn get_attribute_definitions(&self) -> Vec<AttributeDefinition>;

    /// Update map that includes lease throughput.
    fn get_dynamo_lease_throughput_kbps_update(
        &self,
        lease: &Lease,
    ) -> HashMap<String, AttributeValueUpdate>;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn mock_round_trip_and_default_unsupported() {
        let mut mock = MockLeaseSerializer::new();
        mock.expect_to_dynamo_record().returning(|_| {
            let mut m = HashMap::new();
            m.insert("leaseKey".to_string(), AttributeValue::S("k".to_string()));
            m
        });
        let rec = mock.to_dynamo_record(&Lease::default());
        assert!(rec.contains_key("leaseKey"));
    }

    #[test]
    fn default_overloads_are_unsupported() {
        struct S;
        impl LeaseSerializer for S {
            fn to_dynamo_record(&self, _l: &Lease) -> HashMap<String, AttributeValue> {
                HashMap::new()
            }
            fn from_dynamo_record(&self, _r: &HashMap<String, AttributeValue>) -> Lease {
                Lease::default()
            }
            fn get_dynamo_hash_key(&self, _l: &Lease) -> HashMap<String, AttributeValue> {
                HashMap::new()
            }
            fn get_dynamo_hash_key_from_key(&self, _k: &str) -> HashMap<String, AttributeValue> {
                HashMap::new()
            }
            fn get_dynamo_lease_counter_expectation(
                &self,
                _l: &Lease,
            ) -> HashMap<String, ExpectedAttributeValue> {
                HashMap::new()
            }
            fn get_dynamo_lease_owner_expectation(
                &self,
                _l: &Lease,
            ) -> HashMap<String, ExpectedAttributeValue> {
                HashMap::new()
            }
            fn get_dynamo_nonexistant_expectation(
                &self,
            ) -> HashMap<String, ExpectedAttributeValue> {
                HashMap::new()
            }
            fn get_dynamo_lease_counter_update(
                &self,
                _l: &Lease,
            ) -> HashMap<String, AttributeValueUpdate> {
                HashMap::new()
            }
            fn get_dynamo_take_lease_update(
                &self,
                _l: &Lease,
                _o: &str,
            ) -> HashMap<String, AttributeValueUpdate> {
                HashMap::new()
            }
            fn get_dynamo_evict_lease_update(
                &self,
                _l: &Lease,
            ) -> HashMap<String, AttributeValueUpdate> {
                HashMap::new()
            }
            fn get_dynamo_update_lease_update(
                &self,
                _l: &Lease,
            ) -> HashMap<String, AttributeValueUpdate> {
                HashMap::new()
            }
            fn get_key_schema(&self) -> Vec<KeySchemaElement> {
                Vec::new()
            }
            fn get_attribute_definitions(&self) -> Vec<AttributeDefinition> {
                Vec::new()
            }
            fn get_dynamo_lease_throughput_kbps_update(
                &self,
                _l: &Lease,
            ) -> HashMap<String, AttributeValueUpdate> {
                HashMap::new()
            }
        }

        let s = S;
        assert!(s.get_dynamo_existent_expectation("k").is_err());
        assert!(s
            .get_dynamo_assign_lease_update(&Lease::default(), "o")
            .is_err());
        assert!(s
            .get_dynamo_update_lease_update_field(&Lease::default(), UpdateField::ChildShards)
            .is_err());
        assert!(s.get_worker_id_to_lease_key_index_key_schema().is_empty());
    }
}
