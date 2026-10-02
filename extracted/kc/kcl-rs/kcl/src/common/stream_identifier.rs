//! Port of `software.amazon.kinesis.common.StreamIdentifier`.

use std::hash::{Hash, Hasher};

use crate::common::arn::Arn;

/// Stream type identifier for Amazon Kinesis Data Streams.
pub const STREAM_TYPE_KINESIS: &str = "Kinesis";

fn all_ascii_digits(s: &str) -> bool {
    !s.is_empty() && s.bytes().all(|b| b.is_ascii_digit())
}

/// Parse a serialized [`StreamIdentifier`]: `<accountId>:<streamName>:<creationEpoch>`.
///
/// Equivalent to the Java pattern
/// `^(?P<accountId>[0-9]+):(?P<streamName>[^:]+):(?P<creationEpoch>[0-9]+)$`:
/// exactly three colon-separated fields, digits : non-empty : digits.
fn parse_stream_identifier(serialized: &str) -> Option<(&str, &str, &str)> {
    let mut parts = serialized.split(':');
    let account_id = parts.next()?;
    let stream_name = parts.next()?;
    let creation_epoch = parts.next()?;
    if parts.next().is_some() {
        return None; // more than two colons — streamName is [^:]+
    }
    (all_ascii_digits(account_id) && !stream_name.is_empty() && all_ascii_digits(creation_epoch))
        .then_some((account_id, stream_name, creation_epoch))
}

/// Validate a stream ARN string: `arn:aws*:kinesis:<region>:<accountId>:stream/<streamName>`.
///
/// Equivalent to the Java pattern
/// `^arn:aws[^:]*:kinesis:(?P<region>[-a-z0-9]+):(?P<accountId>[0-9]{12}):stream/(?P<streamName>.+)$`
/// (where `.` does not match a newline).
fn is_valid_stream_arn(arn: &str) -> bool {
    let mut parts = arn.splitn(6, ':');
    let (
        Some(scheme),
        Some(partition),
        Some(service),
        Some(region),
        Some(account_id),
        Some(resource),
    ) = (
        parts.next(),
        parts.next(),
        parts.next(),
        parts.next(),
        parts.next(),
        parts.next(),
    )
    else {
        return false;
    };
    scheme == "arn"
        && partition.starts_with("aws")
        && service == "kinesis"
        && !region.is_empty()
        && region
            .bytes()
            .all(|b| b == b'-' || b.is_ascii_lowercase() || b.is_ascii_digit())
        && account_id.len() == 12
        && all_ascii_digits(account_id)
        && resource
            .strip_prefix("stream/")
            .is_some_and(|stream_name| !stream_name.is_empty() && !stream_name.contains('\n'))
}

/// Identifies a Kinesis stream, in either single-stream mode (just a name) or
/// multi-stream mode (`account:stream:creationEpoch`).
///
/// Equality and hashing intentionally exclude `stream_arn` and `stream_type`
/// (Java `@EqualsAndHashCode.Exclude`), so two identifiers are equal iff their
/// account id, stream name, and creation epoch match.
#[derive(Debug, Clone)]
pub struct StreamIdentifier {
    account_id_optional: Option<String>,
    stream_name: String,
    stream_creation_epoch_optional: Option<i64>,
    stream_arn_optional: Option<Arn>,
    stream_type: String,
}

impl PartialEq for StreamIdentifier {
    fn eq(&self, other: &Self) -> bool {
        self.account_id_optional == other.account_id_optional
            && self.stream_name == other.stream_name
            && self.stream_creation_epoch_optional == other.stream_creation_epoch_optional
    }
}

impl Eq for StreamIdentifier {}

impl Hash for StreamIdentifier {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.account_id_optional.hash(state);
        self.stream_name.hash(state);
        self.stream_creation_epoch_optional.hash(state);
    }
}

impl StreamIdentifier {
    // ---- accessors (Lombok fluent @Getter) ----

    pub fn account_id_optional(&self) -> Option<&str> {
        self.account_id_optional.as_deref()
    }

    pub fn stream_name(&self) -> &str {
        &self.stream_name
    }

    pub fn stream_creation_epoch_optional(&self) -> Option<i64> {
        self.stream_creation_epoch_optional
    }

    pub fn stream_arn_optional(&self) -> Option<&Arn> {
        self.stream_arn_optional.as_ref()
    }

    pub fn stream_type(&self) -> &str {
        &self.stream_type
    }

    /// Serialize this identifier: `account:stream:creationEpoch` in multi-stream
    /// mode, or just the stream name in single-stream mode.
    pub fn serialize(&self) -> String {
        match self.stream_creation_epoch_optional {
            None => self.stream_name.clone(),
            Some(epoch) => format!(
                "{}:{}:{}",
                self.account_id_optional
                    .as_deref()
                    .expect("account id present in multi-stream mode"),
                self.stream_name,
                epoch
            ),
        }
    }

    // ---- factory methods ----

    /// Multi-stream instance from a serialized `account:stream:creationEpoch` string.
    ///
    /// # Panics
    /// Panics (Java `IllegalArgumentException`) if the string cannot be parsed,
    /// or if the creation epoch is not `> 0`.
    pub fn multi_stream_instance(serialized: &str) -> StreamIdentifier {
        Self::multi_stream_instance_with_type(serialized, STREAM_TYPE_KINESIS)
    }

    /// Multi-stream instance from a serialized string with an explicit stream type.
    pub fn multi_stream_instance_with_type(
        serialized: &str,
        stream_type: &str,
    ) -> StreamIdentifier {
        if let Some((account_id, stream_name, creation_epoch)) = parse_stream_identifier(serialized)
        {
            let creation_epoch: i64 = creation_epoch
                .parse()
                .expect("creation epoch must fit in i64");
            validate_creation_epoch(creation_epoch);
            return StreamIdentifier {
                account_id_optional: Some(account_id.to_string()),
                stream_name: stream_name.to_string(),
                stream_creation_epoch_optional: Some(creation_epoch),
                stream_arn_optional: None,
                stream_type: stream_type.to_string(),
            };
        }
        panic!("Unable to deserialize StreamIdentifier from {}", serialized);
    }

    /// Multi-stream instance from a stream ARN and creation epoch.
    ///
    /// # Panics
    /// Panics if the ARN is invalid or the creation epoch is not `> 0`.
    pub fn multi_stream_instance_from_arn(
        stream_arn: Arn,
        creation_epoch: i64,
    ) -> StreamIdentifier {
        validate_arn(&stream_arn);
        validate_creation_epoch(creation_epoch);
        StreamIdentifier {
            account_id_optional: stream_arn.account_id().map(str::to_string),
            stream_name: stream_arn.resource().resource().to_string(),
            stream_creation_epoch_optional: Some(creation_epoch),
            stream_arn_optional: Some(stream_arn),
            stream_type: STREAM_TYPE_KINESIS.to_string(),
        }
    }

    /// Single-stream instance from a stream name.
    ///
    /// # Panics
    /// Panics (Java `Validate.notEmpty`) if the stream name is empty.
    pub fn single_stream_instance(stream_name: &str) -> StreamIdentifier {
        Self::single_stream_instance_with_type(stream_name, STREAM_TYPE_KINESIS)
    }

    /// Single-stream instance from a stream name with an explicit stream type.
    pub fn single_stream_instance_with_type(
        stream_name: &str,
        stream_type: &str,
    ) -> StreamIdentifier {
        if stream_name.is_empty() {
            panic!("StreamName should not be empty");
        }
        StreamIdentifier {
            account_id_optional: None,
            stream_name: stream_name.to_string(),
            stream_creation_epoch_optional: None,
            stream_arn_optional: None,
            stream_type: stream_type.to_string(),
        }
    }

    /// Single-stream instance from a stream ARN.
    ///
    /// # Panics
    /// Panics if the ARN is invalid.
    pub fn single_stream_instance_from_arn(stream_arn: Arn) -> StreamIdentifier {
        validate_arn(&stream_arn);
        StreamIdentifier {
            account_id_optional: stream_arn.account_id().map(str::to_string),
            stream_name: stream_arn.resource().resource().to_string(),
            stream_creation_epoch_optional: None,
            stream_arn_optional: Some(stream_arn),
            stream_type: STREAM_TYPE_KINESIS.to_string(),
        }
    }
}

/// Verify the ARN follows the expected format and has a region.
///
/// # Panics
/// Panics (Java `IllegalArgumentException`) if the ARN is invalid.
pub fn validate_arn(stream_arn: &Arn) {
    if !is_valid_stream_arn(&stream_arn.to_string()) || stream_arn.region().is_none() {
        panic!("Invalid streamArn {}", stream_arn);
    }
}

/// # Panics
/// Panics if `creation_epoch <= 0`.
fn validate_creation_epoch(creation_epoch: i64) {
    if creation_epoch <= 0 {
        panic!("Creation epoch must be > 0; received {}", creation_epoch);
    }
}

impl std::fmt::Display for StreamIdentifier {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.serialize())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // ---- Ported from `StreamIdentifierTest.java` constants/helpers ----
    const STREAM_NAME: &str = "stream-name";
    const PARTITION: &str = "aws";
    const SERVICE: &str = "kinesis";
    const KINESIS_REGION: &str = "us-west-1";
    const TEST_ACCOUNT_ID: &str = "123456789012";
    const RESOURCE: &str = "stream/stream-name";
    const EPOCH: i64 = 1680616058;

    /// Java `createArn(...)` — build an `Arn` from parts. A `None` region maps
    /// to an absent region segment (`Arn::new` treats empty as absent).
    fn create_arn_parts(
        partition: &str,
        service: &str,
        region: Option<&str>,
        account: Option<&str>,
        resource: &str,
    ) -> Arn {
        Arn::new(
            partition.to_string(),
            service.to_string(),
            region.map(|s| s.to_string()),
            account.map(|s| s.to_string()),
            resource.to_string(),
        )
    }

    /// Java `createArn()` — the DEFAULT_ARN.
    fn default_arn() -> Arn {
        create_arn_parts(
            PARTITION,
            SERVICE,
            Some(KINESIS_REGION),
            Some(TEST_ACCOUNT_ID),
            RESOURCE,
        )
    }

    /// Java `serialize()` — a valid `account:stream:epoch` serialization.
    fn serialize_pattern() -> String {
        format!("{}:{}:{}", TEST_ACCOUNT_ID, STREAM_NAME, EPOCH)
    }

    /// Java `assertActualStreamIdentifierExpected(expectedArn, actual)`.
    fn assert_actual_expected(expected_arn: Option<&Arn>, actual: &StreamIdentifier) {
        assert_eq!(actual.stream_name(), STREAM_NAME);
        assert_eq!(actual.account_id_optional(), Some(TEST_ACCOUNT_ID));
        assert_eq!(actual.stream_arn_optional(), expected_arn);
    }

    /// Port of `testMultiStreamDeserializationFail`: serializations that must
    /// NOT parse into a `StreamIdentifier` (Java expects `IllegalArgumentException`,
    /// here a `panic!`). Each pattern is exercised in an isolated
    /// `catch_unwind` so one bad pattern doesn't abort the rest.
    #[test]
    fn multi_stream_deserialization_fail() {
        let patterns = [
            ":stream-name:123",              // missing account id
            "123456789abc:stream-name:123",  // 12-char alphanumeric account id
            "123456789012::123",             // missing stream name
            "123456789012:stream-name",      // missing delimiter and creation epoch
            "123456789012:stream-name:",     // missing creation epoch
            "123456789012:stream-name:-123", // negative creation epoch
            "123456789012:stream-name:abc",  // non-numeric creation epoch
            "",
            "::",                           // missing account id, stream name, and epoch
            "123456789012:stream:name:123", // stream name may not contain ':'
        ];
        for pattern in patterns {
            let result =
                std::panic::catch_unwind(|| StreamIdentifier::multi_stream_instance(pattern));
            assert!(
                result.is_err(),
                "Serialization {pattern:?} should not have created a StreamIdentifier"
            );
        }
    }

    /// Port of `testMultiStreamByArnWithInvalidStreamArnFail`: ARNs that must
    /// NOT be accepted by `multi_stream_instance_from_arn`.
    #[test]
    fn multi_stream_by_arn_with_invalid_stream_arn_fail() {
        let invalid_arns = vec![
            create_arn_parts(
                "abc",
                SERVICE,
                Some(KINESIS_REGION),
                Some(TEST_ACCOUNT_ID),
                RESOURCE,
            ), // invalid partition
            create_arn_parts(
                PARTITION,
                "dynamodb",
                Some(KINESIS_REGION),
                Some(TEST_ACCOUNT_ID),
                RESOURCE,
            ), // incorrect service
            create_arn_parts(PARTITION, SERVICE, None, Some(TEST_ACCOUNT_ID), RESOURCE), // missing region
            create_arn_parts(PARTITION, SERVICE, Some(KINESIS_REGION), None, RESOURCE), // missing account id
            create_arn_parts(
                PARTITION,
                SERVICE,
                Some(KINESIS_REGION),
                Some("123456789"),
                RESOURCE,
            ), // account id not 12 digits
            create_arn_parts(
                PARTITION,
                SERVICE,
                Some(KINESIS_REGION),
                Some("123456789abc"),
                RESOURCE,
            ), // 12-char alphanumeric account id
            create_arn_parts(
                PARTITION,
                SERVICE,
                Some(KINESIS_REGION),
                Some(TEST_ACCOUNT_ID),
                "table/name",
            ), // incorrect resource type
            Arn::from_string("arn:aws:dynamodb:us-east-2:123456789012:table/myDynamoDBTable")
                .unwrap(), // valid ARN, wrong resource
        ];
        for arn in invalid_arns {
            let display = arn.to_string();
            let result = std::panic::catch_unwind(|| {
                StreamIdentifier::multi_stream_instance_from_arn(arn, EPOCH)
            });
            assert!(
                result.is_err(),
                "Arn {display} should not have created a StreamIdentifier"
            );
        }
    }

    /// Port of `testNegativeCreationEpoch`.
    #[test]
    #[should_panic(expected = "Creation epoch must be > 0")]
    fn negative_creation_epoch() {
        StreamIdentifier::multi_stream_instance_from_arn(default_arn(), -123);
    }

    /// Port of `testSingleStreamInstanceFromArn`.
    #[test]
    fn single_stream_instance_from_arn() {
        let arn = default_arn();
        let actual = StreamIdentifier::single_stream_instance_from_arn(arn.clone());
        assert_actual_expected(Some(&arn), &actual);
        assert_eq!(actual.stream_creation_epoch_optional(), None);
        assert_eq!(actual.serialize(), actual.stream_name());
    }

    /// Port of `testSingleStreamInstanceWithName`.
    #[test]
    fn single_stream_instance_with_name() {
        let actual = StreamIdentifier::single_stream_instance(STREAM_NAME);
        assert_eq!(actual.stream_creation_epoch_optional(), None);
        assert_eq!(actual.account_id_optional(), None);
        assert_eq!(actual.stream_arn_optional(), None);
        assert_eq!(actual.stream_name(), STREAM_NAME);
    }

    /// Port of `testMultiStreamInstanceWithIdentifierSerialization`.
    #[test]
    fn multi_stream_instance_with_identifier_serialization() {
        let actual = StreamIdentifier::multi_stream_instance(&serialize_pattern());
        assert_actual_expected(None, &actual);
        assert_eq!(actual.stream_creation_epoch_optional(), Some(EPOCH));
    }

    /// Port of `testStreamTypeDefaultsToKinesis`.
    #[test]
    fn stream_type_defaults_to_kinesis() {
        assert_eq!(
            StreamIdentifier::single_stream_instance(STREAM_NAME).stream_type(),
            STREAM_TYPE_KINESIS
        );
        assert_eq!(
            StreamIdentifier::multi_stream_instance(&serialize_pattern()).stream_type(),
            STREAM_TYPE_KINESIS
        );
    }

    /// Port of `testStreamTypeExcludedFromEquality`.
    #[test]
    fn stream_type_excluded_from_equality() {
        let kinesis =
            StreamIdentifier::single_stream_instance_with_type(STREAM_NAME, STREAM_TYPE_KINESIS);
        let other =
            StreamIdentifier::single_stream_instance_with_type(STREAM_NAME, "OtherStreamType");
        assert_eq!(kinesis, other);
    }

    #[test]
    fn single_stream_serializes_to_name() {
        let si = StreamIdentifier::single_stream_instance("my-stream");
        assert_eq!(si.serialize(), "my-stream");
        assert_eq!(si.stream_name(), "my-stream");
        assert_eq!(si.account_id_optional(), None);
        assert_eq!(si.stream_creation_epoch_optional(), None);
        assert_eq!(si.stream_type(), STREAM_TYPE_KINESIS);
    }

    #[test]
    #[should_panic(expected = "StreamName should not be empty")]
    fn single_stream_empty_name_panics() {
        StreamIdentifier::single_stream_instance("");
    }

    #[test]
    fn multi_stream_parses_and_serializes() {
        let si = StreamIdentifier::multi_stream_instance("123456789012:my-stream:1680000000");
        assert_eq!(si.account_id_optional(), Some("123456789012"));
        assert_eq!(si.stream_name(), "my-stream");
        assert_eq!(si.stream_creation_epoch_optional(), Some(1680000000));
        assert_eq!(si.serialize(), "123456789012:my-stream:1680000000");
    }

    #[test]
    #[should_panic(expected = "Unable to deserialize StreamIdentifier")]
    fn multi_stream_bad_format_panics() {
        StreamIdentifier::multi_stream_instance("not-valid");
    }

    #[test]
    #[should_panic(expected = "Creation epoch must be > 0")]
    fn multi_stream_zero_epoch_panics() {
        StreamIdentifier::multi_stream_instance("123456789012:my-stream:0");
    }

    #[test]
    fn multi_stream_from_arn() {
        let arn =
            Arn::from_string("arn:aws:kinesis:us-east-1:123456789012:stream/my-stream").unwrap();
        let si = StreamIdentifier::multi_stream_instance_from_arn(arn.clone(), 1680000000);
        assert_eq!(si.account_id_optional(), Some("123456789012"));
        assert_eq!(si.stream_name(), "my-stream");
        assert_eq!(si.stream_creation_epoch_optional(), Some(1680000000));
        assert_eq!(si.stream_arn_optional(), Some(&arn));
    }

    /// Pins the hand-rolled ARN validator to the semantics of the Java pattern
    /// `^arn:aws[^:]*:kinesis:(?P<region>[-a-z0-9]+):(?P<accountId>[0-9]{12}):stream/(?P<streamName>.+)$`.
    #[test]
    fn stream_arn_validator_matches_java_pattern() {
        // ':' and '/' are legal inside the stream-name remainder (`.+`).
        assert!(is_valid_stream_arn(
            "arn:aws:kinesis:us-east-1:123456789012:stream/my:odd/name"
        ));
        // Partition needs only the "aws" prefix (`aws[^:]*`).
        assert!(is_valid_stream_arn(
            "arn:aws-cn:kinesis:cn-north-1:123456789012:stream/s"
        ));
        // Region must be non-empty [-a-z0-9]+.
        assert!(!is_valid_stream_arn(
            "arn:aws:kinesis::123456789012:stream/s"
        ));
        assert!(!is_valid_stream_arn(
            "arn:aws:kinesis:US-EAST-1:123456789012:stream/s"
        ));
        // Resource must be stream/<non-empty>.
        assert!(!is_valid_stream_arn(
            "arn:aws:kinesis:us-east-1:123456789012:stream/"
        ));
        assert!(!is_valid_stream_arn(
            "arn:aws:kinesis:us-east-1:123456789012:streams/s"
        ));
    }

    #[test]
    fn single_stream_from_arn_has_no_epoch() {
        let arn =
            Arn::from_string("arn:aws:kinesis:us-east-1:123456789012:stream/my-stream").unwrap();
        let si = StreamIdentifier::single_stream_instance_from_arn(arn);
        assert_eq!(si.stream_name(), "my-stream");
        assert_eq!(si.stream_creation_epoch_optional(), None);
    }

    #[test]
    #[should_panic(expected = "Invalid streamArn")]
    fn invalid_arn_panics() {
        // Missing 12-digit account id / wrong format.
        let arn = Arn::from_string("arn:aws:s3:us-east-1:123:bucket/x").unwrap();
        StreamIdentifier::single_stream_instance_from_arn(arn);
    }

    #[test]
    fn equality_excludes_arn_and_type() {
        let arn =
            Arn::from_string("arn:aws:kinesis:us-east-1:123456789012:stream/my-stream").unwrap();
        let a = StreamIdentifier::multi_stream_instance_from_arn(arn, 1680000000);
        let b = StreamIdentifier::multi_stream_instance("123456789012:my-stream:1680000000");
        // b has no ARN and default type, a has an ARN — still equal.
        assert_eq!(a, b);
    }
}
