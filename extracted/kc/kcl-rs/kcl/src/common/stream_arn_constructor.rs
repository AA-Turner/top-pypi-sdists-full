//! Port of `software.amazon.kinesis.common.StreamArnConstructor` and its default
//! implementation `DefaultKinesisStreamArnConstructor`.

use aws_config::Region;

use crate::common::arn::Arn;

/// Resource prefix for a Kinesis stream ARN (`stream/`).
///
/// This prefix is implicitly assumed by
/// [`StreamIdentifier`](crate::common::StreamIdentifier)'s ARN regex, which
/// expects `stream/` after the account id — the two must stay in sync.
pub const STREAM_RESOURCE_PREFIX: &str = "stream/";

/// The Kinesis service name segment of an ARN
/// (`KinesisAsyncClient.SERVICE_NAME` in the Java SDK).
pub const KINESIS_SERVICE_NAME: &str = "kinesis";

/// Strategy interface for building a Kinesis stream ARN from
/// region/account/streamName, allowing the ARN-construction logic to be swapped
/// (e.g. for non-standard AWS partitions or test doubles).
///
/// Port of the Java `StreamArnConstructor` interface.
pub trait StreamArnConstructor {
    /// Construct a Kinesis stream ARN of the form
    /// `arn:<partition>:kinesis:<region>:<account>:stream/<name>`.
    fn construct_stream_arn(&self, region: &Region, account_id: &str, stream_name: &str) -> Arn;
}

/// Default implementation of [`StreamArnConstructor`] building a Kinesis stream
/// ARN from region/account/streamName.
///
/// Port of `DefaultKinesisStreamArnConstructor`. The Java version resolves the
/// partition via `region.metadata().partition().id()`; the Rust AWS SDK does not
/// expose equivalent region-metadata partition lookup, so the partition is
/// inferred from the region id prefix (see [`partition_for_region`]).
#[derive(Debug, Default, Clone, Copy)]
pub struct DefaultKinesisStreamArnConstructor;

impl StreamArnConstructor for DefaultKinesisStreamArnConstructor {
    fn construct_stream_arn(&self, region: &Region, account_id: &str, stream_name: &str) -> Arn {
        Arn::new(
            partition_for_region(region.as_ref()),
            KINESIS_SERVICE_NAME,
            Some(region.as_ref().to_string()),
            Some(account_id.to_string()),
            format!("{}{}", STREAM_RESOURCE_PREFIX, stream_name),
        )
    }
}

/// Infer the AWS partition for a region id, replicating the AWS SDK's
/// `Region.metadata().partition().id()` mapping:
///
/// - `cn-*` region ids belong to the `aws-cn` partition;
/// - `us-gov-*` region ids belong to the `aws-us-gov` partition;
/// - everything else belongs to the standard `aws` partition.
pub fn partition_for_region(region_id: &str) -> &'static str {
    if region_id.starts_with("cn-") {
        "aws-cn"
    } else if region_id.starts_with("us-gov-") {
        "aws-us-gov"
    } else {
        "aws"
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn constructs_standard_partition_arn() {
        let c = DefaultKinesisStreamArnConstructor;
        let arn = c.construct_stream_arn(&Region::new("us-west-1"), "123456789012", "stream-name");
        assert_eq!(
            arn.to_string(),
            "arn:aws:kinesis:us-west-1:123456789012:stream/stream-name"
        );
        assert_eq!(arn.partition(), "aws");
        assert_eq!(arn.service(), "kinesis");
        assert_eq!(arn.region(), Some("us-west-1"));
        assert_eq!(arn.account_id(), Some("123456789012"));
        assert_eq!(arn.resource().resource_type(), Some("stream"));
        assert_eq!(arn.resource().resource(), "stream-name");
    }

    #[test]
    fn china_partition() {
        let c = DefaultKinesisStreamArnConstructor;
        let arn = c.construct_stream_arn(&Region::new("cn-north-1"), "123456789012", "s");
        assert_eq!(
            arn.to_string(),
            "arn:aws-cn:kinesis:cn-north-1:123456789012:stream/s"
        );
    }

    #[test]
    fn gov_partition() {
        let c = DefaultKinesisStreamArnConstructor;
        let arn = c.construct_stream_arn(&Region::new("us-gov-west-1"), "123456789012", "s");
        assert_eq!(
            arn.to_string(),
            "arn:aws-us-gov:kinesis:us-gov-west-1:123456789012:stream/s"
        );
    }

    #[test]
    fn constructed_arn_matches_stream_identifier_validation() {
        // The ARN built here must pass StreamIdentifier's ARN regex byte-for-byte.
        let c = DefaultKinesisStreamArnConstructor;
        let arn = c.construct_stream_arn(&Region::new("us-east-1"), "123456789012", "my-stream");
        // Should not panic.
        let si = crate::common::StreamIdentifier::single_stream_instance_from_arn(arn.clone());
        assert_eq!(si.stream_name(), "my-stream");
        assert_eq!(si.account_id_optional(), Some("123456789012"));
    }

    #[test]
    fn partition_inference() {
        assert_eq!(partition_for_region("us-east-1"), "aws");
        assert_eq!(partition_for_region("eu-central-1"), "aws");
        assert_eq!(partition_for_region("cn-north-1"), "aws-cn");
        assert_eq!(partition_for_region("cn-northwest-1"), "aws-cn");
        assert_eq!(partition_for_region("us-gov-east-1"), "aws-us-gov");
        assert_eq!(partition_for_region("us-gov-west-1"), "aws-us-gov");
    }
}
