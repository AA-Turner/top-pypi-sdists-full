//! Port of `software.amazon.kinesis.coordinator.streamInfo.StreamInfo`.

use std::collections::HashMap;

use aws_sdk_dynamodb::types::{AttributeAction, AttributeValue, AttributeValueUpdate};

use crate::coordinator::coordinator_state::ENTITY_TYPE_ATTRIBUTE_NAME;
use crate::leases::{CoordinatorStateType, EntityType};

/// DDB attribute name for the stream id. Java `StreamInfo.STREAM_ID_ATTRIBUTE_NAME`.
pub const STREAM_ID_ATTRIBUTE_NAME: &str = "streamId";

/// Data model of the StreamInfo state — tracks the Kinesis-assigned `streamId`
/// keyed by the stream's string identifier.
///
/// In Java `StreamInfo extends CoordinatorState`. Here it is a standalone struct
/// (see [`crate::coordinator::coordinator_state`] module docs); its
/// `coordinatorStateEntityType` is always `STREAM_INFO`.
#[derive(Debug, Clone, PartialEq)]
pub struct StreamInfo {
    key: String,
    stream_id: String,
    /// Java inherits a generic `attributes` map from `CoordinatorState`
    /// (some tests `setAttributes`). Preserved for fidelity; not part of
    /// `serialize()` output beyond the base behavior.
    attributes: Option<HashMap<String, AttributeValue>>,
}

impl StreamInfo {
    /// Java `StreamInfo(String key, String streamId)`.
    pub fn new(key: impl Into<String>, stream_id: impl Into<String>) -> Self {
        Self {
            key: key.into(),
            stream_id: stream_id.into(),
            attributes: None,
        }
    }

    pub fn key(&self) -> &str {
        &self.key
    }

    pub fn stream_id(&self) -> &str {
        &self.stream_id
    }

    pub fn coordinator_state_entity_type(&self) -> CoordinatorStateType {
        CoordinatorStateType::StreamInfo
    }

    pub fn entity_type(&self) -> EntityType {
        EntityType::StreamInfo
    }

    /// Java `setAttributes` (inherited Lombok `@Data` setter).
    pub fn set_attributes(&mut self, attributes: HashMap<String, AttributeValue>) {
        self.attributes = Some(attributes);
    }

    pub fn attributes(&self) -> Option<&HashMap<String, AttributeValue>> {
        self.attributes.as_ref()
    }

    /// Java `serialize()`: `super.serialize()` (entityType + generic attributes)
    /// then adds the `streamId` attribute.
    pub fn serialize(&self) -> HashMap<String, AttributeValue> {
        let mut result = HashMap::new();
        // super.serialize(): entityType is always STREAM_INFO for StreamInfo.
        result.insert(
            ENTITY_TYPE_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(CoordinatorStateType::StreamInfo.ddb_value().to_string()),
        );
        if let Some(attrs) = &self.attributes {
            for (k, v) in attrs {
                result.insert(k.clone(), v.clone());
            }
        }
        result.insert(
            STREAM_ID_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(self.stream_id.clone()),
        );
        result
    }

    /// Base `getDynamoUpdate()` (StreamInfo does not override): all generic
    /// attributes → `PUT` updates.
    pub fn get_dynamo_update(&self) -> HashMap<String, AttributeValueUpdate> {
        let mut updates = HashMap::new();
        if let Some(attrs) = &self.attributes {
            for (attribute, value) in attrs {
                updates.insert(
                    attribute.clone(),
                    AttributeValueUpdate::builder()
                        .value(value.clone())
                        .action(AttributeAction::Put)
                        .build(),
                );
            }
        }
        updates
    }

    /// Java `static StreamInfo deserialize(String key, Map attributes)`.
    /// Returns `None` (Java `null` + WARN log) if `attributes` is `None` or the
    /// `streamId` attribute is missing/malformed.
    pub fn deserialize(
        key: impl Into<String>,
        attributes: Option<&HashMap<String, AttributeValue>>,
    ) -> Option<StreamInfo> {
        let attributes = attributes?;
        match attributes
            .get(STREAM_ID_ATTRIBUTE_NAME)
            .and_then(|v| v.as_s().ok())
        {
            Some(stream_id) => Some(StreamInfo::new(key, stream_id.clone())),
            None => {
                tracing::warn!("Unable to deserialize StreamInfo (missing/invalid streamId)");
                None
            }
        }
    }

    /// Java `static String multiStreamLeaseKeyToStreamIdentifier(String)`.
    ///
    /// Splits on `':'` with a limit of 4, returns the joined first 3
    /// colon-separated parts (`accountId:streamName:creationEpoch`). Returns the
    /// input unchanged if fewer than 3 parts.
    ///
    /// # Panics
    /// Panics (Java `IllegalArgumentException`) on a `None`/empty input — modeled
    /// here as an empty `&str` panicking.
    pub fn multi_stream_lease_key_to_stream_identifier(multi_stream_lease_key: &str) -> String {
        if multi_stream_lease_key.is_empty() {
            panic!("multiStreamLeaseKey must not be null or empty");
        }
        // Java String.split(":", 4): at most 4 substrings, the last holds the
        // remainder including any further colons.
        let parts: Vec<&str> = multi_stream_lease_key.splitn(4, ':').collect();
        if parts.len() < 3 {
            return multi_stream_lease_key.to_string();
        }
        format!("{}:{}:{}", parts[0], parts[1], parts[2])
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn get_entity_type_returns_stream_info() {
        let s = StreamInfo::new("stream-key-1", "stream-id-1");
        assert_eq!(s.entity_type(), EntityType::StreamInfo);
        assert_eq!(s.entity_type().ddb_value(), "STREAM");
        assert_eq!(
            s.coordinator_state_entity_type(),
            CoordinatorStateType::StreamInfo
        );
    }

    #[test]
    fn test_serialize() {
        let s = StreamInfo::new("stream-key-1", "my-stream-id");
        let serialized = s.serialize();
        assert!(serialized.contains_key("entityType"));
        assert_eq!(
            serialized.get("entityType").unwrap().as_s().unwrap(),
            "STREAM"
        );
        assert!(serialized.contains_key(STREAM_ID_ATTRIBUTE_NAME));
        assert_eq!(
            serialized
                .get(STREAM_ID_ATTRIBUTE_NAME)
                .unwrap()
                .as_s()
                .unwrap(),
            "my-stream-id"
        );
    }

    #[test]
    fn deserialize_valid_attributes_returns_stream_info() {
        let mut attrs = HashMap::new();
        attrs.insert(
            STREAM_ID_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S("deserialized-stream-id".to_string()),
        );
        let d = StreamInfo::deserialize("stream-key-2", Some(&attrs)).unwrap();
        assert_eq!(d.stream_id(), "deserialized-stream-id");
        assert_eq!(d.key(), "stream-key-2");
        assert_eq!(d.entity_type(), EntityType::StreamInfo);
    }

    #[test]
    fn deserialize_null_attributes_returns_none() {
        assert!(StreamInfo::deserialize("key", None).is_none());
    }

    #[test]
    fn deserialize_missing_stream_id_returns_none() {
        let attrs = HashMap::new();
        assert!(StreamInfo::deserialize("key", Some(&attrs)).is_none());
    }

    #[test]
    fn serialize_then_deserialize_round_trip() {
        let original = StreamInfo::new("key-1", "stream-456");
        let mut serialized = original.serialize();
        assert!(serialized.contains_key("entityType"));
        assert_eq!(
            serialized.get("entityType").unwrap().as_s().unwrap(),
            "STREAM"
        );
        // Simulate DAO: remove entityType before passing to deserializer.
        serialized.remove("entityType");
        let d = StreamInfo::deserialize("key-1", Some(&serialized)).unwrap();
        assert_eq!(d.stream_id(), "stream-456");
        assert_eq!(d.entity_type(), EntityType::StreamInfo);
        assert_eq!(
            d.coordinator_state_entity_type(),
            CoordinatorStateType::StreamInfo
        );
    }

    #[test]
    fn multi_stream_lease_key_valid_key_extracts_identifier() {
        assert_eq!(
            StreamInfo::multi_stream_lease_key_to_stream_identifier("account:stream:123:shard-001"),
            "account:stream:123"
        );
    }

    #[test]
    fn multi_stream_lease_key_two_part_key_returns_as_is() {
        assert_eq!(
            StreamInfo::multi_stream_lease_key_to_stream_identifier("simple:key"),
            "simple:key"
        );
    }

    #[test]
    #[should_panic(expected = "must not be null or empty")]
    fn multi_stream_lease_key_empty_panics() {
        StreamInfo::multi_stream_lease_key_to_stream_identifier("");
    }
}
