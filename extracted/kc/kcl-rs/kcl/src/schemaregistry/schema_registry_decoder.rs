//! Port of `software.amazon.kinesis.schemaregistry.SchemaRegistryDecoder`.
//!
//! Detects + decodes AWS Glue Schema Registry-encoded payloads in incoming
//! [`KinesisClientRecord`]s, attaching the resolved [`Schema`] and replacing the
//! record data with the decoded payload. Fails open (returns the original record
//! on any error).
//!
//! # TODO(port): Glue deserializer deferred
//! Java delegates to the external `GlueSchemaRegistryDeserializer`
//! (`canDeserialize`/`getSchema`/`getData`/`overrideUserAgentApp`), which has no
//! Rust equivalent yet. This port keeps the **decoder structure + the non-Glue
//! passthrough path** and puts the actual Glue deserialization behind an
//! injectable [`GlueSchemaRegistryDeserializer`] trait. When no deserializer is
//! configured (the common case — no schema registry), records pass through
//! unchanged. The lifecycle `ProcessTask` can wire a real deserializer once one
//! exists (owning wave: retrieval/lifecycle integration + a Glue SR binding).

use crate::retrieval::KinesisClientRecord;
use crate::schemaregistry::Schema;

/// The KCL user-agent app name prefix (Java `"kcl-" + KinesisClientLibraryPackage.VERSION`).
pub fn user_agent_app_name() -> String {
    format!("kcl-{}", env!("CARGO_PKG_VERSION"))
}

/// Injectable Glue Schema Registry deserializer (Java
/// `com.amazonaws.services.schemaregistry.deserializers.GlueSchemaRegistryDeserializer`).
///
/// `// TODO(port)`: the concrete Glue-backed impl is deferred (no Rust Glue SR
/// SDK). The decoder works without one via the passthrough path.
pub trait GlueSchemaRegistryDeserializer: Send + Sync {
    /// Set the deserializer's user-agent app (Java `overrideUserAgentApp`).
    fn override_user_agent_app(&self, app_name: &str);
    /// Whether `data` carries a GSR magic-byte header (Java `canDeserialize`).
    fn can_deserialize(&self, data: &[u8]) -> bool;
    /// The schema embedded in `data` (Java `getSchema`).
    fn get_schema(&self, data: &[u8]) -> Schema;
    /// The decoded application payload from `data` (Java `getData`).
    fn get_data(&self, data: &[u8]) -> Vec<u8>;
}

/// Decodes Glue Schema Registry data from [`KinesisClientRecord`]s.
pub struct SchemaRegistryDecoder {
    deserializer: Option<Box<dyn GlueSchemaRegistryDeserializer>>,
}

impl SchemaRegistryDecoder {
    /// Construct with a Glue deserializer (Java constructor; sets the
    /// deserializer's user-agent as a side effect).
    pub fn new(deserializer: Box<dyn GlueSchemaRegistryDeserializer>) -> Self {
        deserializer.override_user_agent_app(&user_agent_app_name());
        Self {
            deserializer: Some(deserializer),
        }
    }

    /// Construct a passthrough decoder (no schema registry configured). Records
    /// pass through [`decode`](Self::decode) unchanged. This is the common
    /// production path when GSR is not in use.
    pub fn passthrough() -> Self {
        Self { deserializer: None }
    }

    /// Decode a batch, returning a new list of the same length/order (input not
    /// mutated; records never dropped) — Java `decode`.
    pub fn decode(&self, records: Vec<KinesisClientRecord>) -> Vec<KinesisClientRecord> {
        records.into_iter().map(|r| self.decode_record(r)).collect()
    }

    fn decode_record(&self, record: KinesisClientRecord) -> KinesisClientRecord {
        // No deserializer configured => passthrough.
        let deserializer = match &self.deserializer {
            Some(d) => d.as_ref(),
            None => return record,
        };

        let data = match record.data() {
            None => return record,
            Some(d) => d.to_vec(),
        };

        // Java swallows any exception in the sniff/decode and returns the
        // original record (fail-open). A panic in the injected deserializer is
        // caught here to reproduce that.
        let decoded = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            if !deserializer.can_deserialize(&data) {
                return None;
            }
            let schema = deserializer.get_schema(&data);
            let record_data = deserializer.get_data(&data);
            Some((schema, record_data))
        }));

        match decoded {
            Ok(Some((schema, record_data))) => rebuild_record(&record, schema, record_data),
            Ok(None) => record,
            Err(_) => {
                tracing::warn!(
                    "Unable to decode Glue Schema Registry information from record {:?}",
                    record.sequence_number()
                );
                record
            }
        }
    }
}

/// Rebuild a [`KinesisClientRecord`] with the schema set and data replaced,
/// carrying over all other fields (Java `record.toBuilder().schema(..).data(..).build()`).
fn rebuild_record(
    record: &KinesisClientRecord,
    schema: Schema,
    data: Vec<u8>,
) -> KinesisClientRecord {
    let mut builder = KinesisClientRecord::builder()
        .maybe_sequence_number(record.sequence_number().map(|s| s.to_string()))
        .maybe_approximate_arrival_timestamp(record.approximate_arrival_timestamp())
        .data(bytes::Bytes::from(data))
        .maybe_partition_key(record.partition_key().map(|s| s.to_string()))
        .maybe_encryption_type(record.encryption_type().cloned())
        .sub_sequence_number(record.sub_sequence_number())
        .maybe_explicit_hash_key(record.explicit_hash_key().map(|s| s.to_string()))
        .aggregated(record.aggregated())
        .schema(schema);
    let _ = &mut builder;
    builder.build()
}

#[cfg(test)]
mod tests {
    use super::*;
    use bytes::Bytes;

    // A fake Glue deserializer: treats data starting with a magic byte 0x03 as
    // schema-encoded; strips the first byte and returns a fixed schema.
    struct FakeDeserializer {
        ua: std::sync::Mutex<Option<String>>,
    }

    impl GlueSchemaRegistryDeserializer for FakeDeserializer {
        fn override_user_agent_app(&self, app_name: &str) {
            *self.ua.lock().unwrap() = Some(app_name.to_string());
        }
        fn can_deserialize(&self, data: &[u8]) -> bool {
            data.first() == Some(&0x03)
        }
        fn get_schema(&self, _data: &[u8]) -> Schema {
            Schema::new("{}", "JSON", "my-schema")
        }
        fn get_data(&self, data: &[u8]) -> Vec<u8> {
            data[1..].to_vec()
        }
    }

    fn record_with_data(data: Option<Bytes>) -> KinesisClientRecord {
        KinesisClientRecord::builder()
            .sequence_number("seq-1")
            .maybe_data(data)
            .partition_key("pk")
            .build()
    }

    #[test]
    fn passthrough_returns_records_unchanged() {
        let decoder = SchemaRegistryDecoder::passthrough();
        let input = vec![record_with_data(Some(Bytes::from_static(&[0x03, 1, 2, 3])))];
        let output = decoder.decode(input.clone());
        assert_eq!(output, input);
    }

    #[test]
    fn constructor_sets_user_agent() {
        let deser = FakeDeserializer {
            ua: std::sync::Mutex::new(None),
        };
        let ua_handle = deser.ua.lock().unwrap().clone();
        assert!(ua_handle.is_none());
        let _decoder = SchemaRegistryDecoder::new(Box::new(deser));
        // The user-agent set is a side effect on the (now moved) deserializer;
        // verify indirectly by rebuilding a decoder over a shared flag.
        let flag = std::sync::Arc::new(std::sync::Mutex::new(None::<String>));
        struct SharedDeser(std::sync::Arc<std::sync::Mutex<Option<String>>>);
        impl GlueSchemaRegistryDeserializer for SharedDeser {
            fn override_user_agent_app(&self, app_name: &str) {
                *self.0.lock().unwrap() = Some(app_name.to_string());
            }
            fn can_deserialize(&self, _: &[u8]) -> bool {
                false
            }
            fn get_schema(&self, _: &[u8]) -> Schema {
                unreachable!()
            }
            fn get_data(&self, _: &[u8]) -> Vec<u8> {
                unreachable!()
            }
        }
        let _d = SchemaRegistryDecoder::new(Box::new(SharedDeser(flag.clone())));
        assert_eq!(
            flag.lock().unwrap().as_deref(),
            Some(user_agent_app_name().as_str())
        );
    }

    #[test]
    fn null_data_record_passes_through() {
        let decoder = SchemaRegistryDecoder::new(Box::new(FakeDeserializer {
            ua: std::sync::Mutex::new(None),
        }));
        let input = vec![record_with_data(None)];
        let output = decoder.decode(input.clone());
        assert_eq!(output, input);
    }

    #[test]
    fn non_encoded_data_passes_through() {
        let decoder = SchemaRegistryDecoder::new(Box::new(FakeDeserializer {
            ua: std::sync::Mutex::new(None),
        }));
        // First byte not 0x03 => not schema-encoded => unchanged.
        let input = vec![record_with_data(Some(Bytes::from_static(&[0x01, 9, 9])))];
        let output = decoder.decode(input.clone());
        assert_eq!(output, input);
    }

    #[test]
    fn encoded_data_is_decoded_and_schema_attached() {
        let decoder = SchemaRegistryDecoder::new(Box::new(FakeDeserializer {
            ua: std::sync::Mutex::new(None),
        }));
        let input = vec![record_with_data(Some(Bytes::from_static(&[0x03, 42, 43])))];
        let output = decoder.decode(input);
        assert_eq!(output.len(), 1);
        assert_eq!(
            output[0].schema(),
            Some(&Schema::new("{}", "JSON", "my-schema"))
        );
        assert_eq!(output[0].data().unwrap().as_ref(), &[42, 43]);
        // Other fields carried over.
        assert_eq!(output[0].sequence_number(), Some("seq-1"));
        assert_eq!(output[0].partition_key(), Some("pk"));
    }

    #[test]
    fn decode_preserves_order_and_count_on_mixed_batch() {
        let decoder = SchemaRegistryDecoder::new(Box::new(FakeDeserializer {
            ua: std::sync::Mutex::new(None),
        }));
        let input = vec![
            record_with_data(Some(Bytes::from_static(&[0x03, 1]))),
            record_with_data(None),
            record_with_data(Some(Bytes::from_static(&[0x01, 2]))),
        ];
        let output = decoder.decode(input);
        assert_eq!(output.len(), 3);
        assert!(output[0].schema().is_some());
        assert!(output[1].schema().is_none());
        assert!(output[2].schema().is_none());
    }
}
