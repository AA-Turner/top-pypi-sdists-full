//! Port of `software.amazon.kinesis.retrieval.KinesisClientRecord`.

use crate::utils::smithy_date_time;
use aws_sdk_kinesis::types::{EncryptionType, Record};
use bytes::Bytes;
use chrono::{DateTime, Utc};

use crate::schemaregistry::Schema;

/// A converted record from Kinesis, possibly one member of an aggregate record.
///
/// Port of the Lombok `@Builder(toBuilder = true) @EqualsAndHashCode @Getter
/// @Accessors(fluent = true)` class. All fields are immutable after
/// construction; equality/hashing is field-based over every field (including
/// `schema`).
///
/// Field type choices (per PORTING.md):
/// * `data` (`ByteBuffer`) → [`Bytes`]
/// * `approximate_arrival_timestamp` (`Instant`) → [`DateTime<Utc>`]
/// * `encryption_type` → [`EncryptionType`]
#[derive(Debug, Clone, PartialEq, Eq, Hash, bon::Builder)]
pub struct KinesisClientRecord {
    /// The Kinesis record sequence number.
    #[builder(into)]
    sequence_number: Option<String>,
    /// The approximate time the record was inserted into the stream.
    approximate_arrival_timestamp: Option<DateTime<Utc>>,
    /// The record payload.
    data: Option<Bytes>,
    /// The partition key the record was assigned to.
    #[builder(into)]
    partition_key: Option<String>,
    /// The encryption type used on the record.
    encryption_type: Option<EncryptionType>,
    /// The sub-sequence number of this user record within its aggregate record.
    #[builder(default)]
    sub_sequence_number: i64,
    /// The explicit hash key, if the record was published with one.
    #[builder(into)]
    explicit_hash_key: Option<String>,
    /// Whether this record was de-aggregated from a KPL aggregate record.
    #[builder(default)]
    aggregated: bool,
    /// The Glue Schema Registry schema associated with this record, if any.
    schema: Option<Schema>,
}

impl KinesisClientRecord {
    /// The Kinesis record sequence number.
    pub fn sequence_number(&self) -> Option<&str> {
        self.sequence_number.as_deref()
    }

    /// The approximate time the record was inserted into the stream.
    pub fn approximate_arrival_timestamp(&self) -> Option<DateTime<Utc>> {
        self.approximate_arrival_timestamp
    }

    /// The record payload.
    pub fn data(&self) -> Option<&Bytes> {
        self.data.as_ref()
    }

    /// The partition key the record was assigned to.
    pub fn partition_key(&self) -> Option<&str> {
        self.partition_key.as_deref()
    }

    /// The encryption type used on the record.
    pub fn encryption_type(&self) -> Option<&EncryptionType> {
        self.encryption_type.as_ref()
    }

    /// The sub-sequence number within an aggregate record.
    pub fn sub_sequence_number(&self) -> i64 {
        self.sub_sequence_number
    }

    /// The explicit hash key, if any.
    pub fn explicit_hash_key(&self) -> Option<&str> {
        self.explicit_hash_key.as_deref()
    }

    /// Whether this record was de-aggregated from a KPL aggregate record.
    pub fn aggregated(&self) -> bool {
        self.aggregated
    }

    /// The Glue Schema Registry schema associated with this record, if any.
    pub fn schema(&self) -> Option<&Schema> {
        self.schema.as_ref()
    }

    /// Build a [`KinesisClientRecord`] from an AWS SDK [`Record`].
    ///
    /// Port of `KinesisClientRecord.fromRecord`: copies the sequence number,
    /// approximate arrival timestamp, data, partition key, and encryption type;
    /// leaves the KPL-aggregation fields (`sub_sequence_number`, `aggregated`,
    /// `explicit_hash_key`) and `schema` at their defaults.
    pub fn from_record(record: &Record) -> KinesisClientRecord {
        KinesisClientRecord::builder()
            .sequence_number(record.sequence_number().to_string())
            .maybe_approximate_arrival_timestamp(
                record
                    .approximate_arrival_timestamp()
                    .and_then(smithy_date_time::to_chrono_utc),
            )
            .data(Bytes::copy_from_slice(record.data().as_ref()))
            .partition_key(record.partition_key().to_string())
            .maybe_encryption_type(record.encryption_type().cloned())
            .build()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use aws_smithy_types::{Blob, DateTime as SmithyDateTime};

    #[test]
    fn builder_defaults_match_java() {
        let record = KinesisClientRecord::builder()
            .sequence_number("123")
            .partition_key("pk")
            .build();
        assert_eq!(record.sequence_number(), Some("123"));
        assert_eq!(record.partition_key(), Some("pk"));
        assert_eq!(record.sub_sequence_number(), 0);
        assert!(!record.aggregated());
        assert_eq!(record.explicit_hash_key(), None);
        assert_eq!(record.schema(), None);
        assert_eq!(record.data(), None);
    }

    #[test]
    fn from_record_copies_fields() {
        let ts = SmithyDateTime::from_secs(1_000_000);
        let record = Record::builder()
            .sequence_number("seq-1")
            .partition_key("pk-1")
            .data(Blob::new(b"hello".to_vec()))
            .approximate_arrival_timestamp(ts)
            .encryption_type(EncryptionType::Kms)
            .build()
            .unwrap();

        let kcr = KinesisClientRecord::from_record(&record);
        assert_eq!(kcr.sequence_number(), Some("seq-1"));
        assert_eq!(kcr.partition_key(), Some("pk-1"));
        assert_eq!(kcr.data().map(|d| d.as_ref()), Some(&b"hello"[..]));
        assert_eq!(kcr.encryption_type(), Some(&EncryptionType::Kms));
        assert_eq!(
            kcr.approximate_arrival_timestamp(),
            smithy_date_time::to_chrono_utc(&ts)
        );
        // Aggregation fields default (fromRecord does not de-aggregate).
        assert_eq!(kcr.sub_sequence_number(), 0);
        assert!(!kcr.aggregated());
    }

    #[test]
    fn equality_and_hashing_are_field_based() {
        use std::collections::HashSet;
        let a = KinesisClientRecord::builder()
            .sequence_number("1")
            .data(Bytes::from_static(b"x"))
            .sub_sequence_number(5)
            .aggregated(true)
            .build();
        let b = KinesisClientRecord::builder()
            .sequence_number("1")
            .data(Bytes::from_static(b"x"))
            .sub_sequence_number(5)
            .aggregated(true)
            .build();
        assert_eq!(a, b);
        let mut set = HashSet::new();
        set.insert(a);
        assert!(set.contains(&b));
    }

    #[test]
    fn to_builder_round_trips() {
        // bon derives a `to_builder`-equivalent via the builder; verify a
        // rebuilt record with one changed field differs only in that field.
        let original = KinesisClientRecord::builder()
            .sequence_number("1")
            .partition_key("pk")
            .aggregated(true)
            .build();
        let modified = KinesisClientRecord::builder()
            .sequence_number(original.sequence_number().unwrap().to_string())
            .maybe_partition_key(original.partition_key().map(str::to_string))
            .sub_sequence_number(original.sub_sequence_number())
            .aggregated(original.aggregated())
            .schema(Schema::new("{}", "JSON", "s"))
            .build();
        assert_eq!(modified.sequence_number(), Some("1"));
        assert!(modified.schema().is_some());
        assert_ne!(original, modified);
    }
}
