//! Minimal port of `com.amazonaws.services.schemaregistry.common.Schema`.
//!
//! The Java KCL references the AWS Glue Schema Registry `Schema` value type from
//! `KinesisClientRecord.schema`. The heavy Glue Schema Registry integration
//! (`SchemaRegistryDecoder`, `GlueSchemaRegistryDeserializer`) is **deferred** —
//! it lives in a separate AWS dependency (`software-amazon-glue-schema-registry`)
//! that has no Rust equivalent yet. See PORTING.md.
//!
//! Only the small immutable value type is ported here, with the three fields the
//! Glue `Schema` carries (`schemaDefinition`, `dataFormat`, `schemaName`), so
//! `KinesisClientRecord` can hold and compare a schema.

/// Port of the Glue Schema Registry `Schema` value object.
///
/// A plain immutable data holder with structural equality/hashing, mirroring the
/// Glue `Schema` class (which is a Lombok `@Value`-style type).
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Schema {
    schema_definition: String,
    data_format: String,
    schema_name: String,
}

impl Schema {
    /// Construct a schema from its definition, data format, and name.
    pub fn new(
        schema_definition: impl Into<String>,
        data_format: impl Into<String>,
        schema_name: impl Into<String>,
    ) -> Self {
        Self {
            schema_definition: schema_definition.into(),
            data_format: data_format.into(),
            schema_name: schema_name.into(),
        }
    }

    /// The schema definition (e.g. the Avro/JSON/Protobuf schema text).
    pub fn schema_definition(&self) -> &str {
        &self.schema_definition
    }

    /// The data format (e.g. `AVRO`, `JSON`, `PROTOBUF`).
    pub fn data_format(&self) -> &str {
        &self.data_format
    }

    /// The registered schema name.
    pub fn schema_name(&self) -> &str {
        &self.schema_name
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn stores_and_returns_fields() {
        let s = Schema::new("{}", "JSON", "my-schema");
        assert_eq!(s.schema_definition(), "{}");
        assert_eq!(s.data_format(), "JSON");
        assert_eq!(s.schema_name(), "my-schema");
    }

    #[test]
    fn equality_is_field_based() {
        let a = Schema::new("{}", "JSON", "my-schema");
        let b = Schema::new("{}", "JSON", "my-schema");
        let c = Schema::new("{}", "AVRO", "my-schema");
        assert_eq!(a, b);
        assert_ne!(a, c);
    }
}
