//! Port of `software.amazon.kinesis.schemaregistry`.
//!
//! The minimal Glue Schema Registry [`Schema`] value type plus the
//! [`SchemaRegistryDecoder`] **structure + non-Glue passthrough path**. The
//! actual Glue deserialization is behind the injectable
//! [`GlueSchemaRegistryDeserializer`] trait and remains deferred (no Rust Glue
//! Schema Registry SDK yet). See PORTING.md.

pub mod schema;
pub mod schema_registry_decoder;

pub use schema::Schema;
pub use schema_registry_decoder::{GlueSchemaRegistryDeserializer, SchemaRegistryDecoder};
