//! Port of `software.amazon.kinesis.retrieval.IteratorBuilder`.
//!
//! Builds `SubscribeToShard`/`StartingPosition` and `GetShardIterator` requests
//! with the correct [`ShardIteratorType`] based on a sequence-number string that
//! may be a real sequence number or a sentinel (`LATEST`/`TRIM_HORIZON`/
//! `AT_TIMESTAMP`), distinguishing an initial connect from a reconnect.
//!
//! The Java generic higher-order `apply` (parameterized over builder-setter
//! method references) is replaced by two small helpers that build the correct
//! shape directly (per the arch-map's recommended port).

use crate::utils::smithy_date_time;
use aws_sdk_kinesis::operation::get_shard_iterator::builders::GetShardIteratorInputBuilder;
use aws_sdk_kinesis::operation::subscribe_to_shard::builders::SubscribeToShardInputBuilder;
use aws_sdk_kinesis::types::builders::StartingPositionBuilder;
use aws_sdk_kinesis::types::{ShardIteratorType, StartingPosition};

use crate::checkpoint::SentinelCheckpoint;
use crate::common::InitialPositionInStreamExtended;

/// Map a sequence-number string to a sentinel [`ShardIteratorType`], or fall back
/// to `default_iterator_type` if it is not a sentinel name.
///
/// Port of `SHARD_ITERATOR_MAPPING.getOrDefault(sequenceNumber, defaultIteratorType)`.
fn iterator_type_for(
    sequence_number: &str,
    default_iterator_type: ShardIteratorType,
) -> ShardIteratorType {
    if sequence_number == SentinelCheckpoint::Latest.as_str() {
        ShardIteratorType::Latest
    } else if sequence_number == SentinelCheckpoint::TrimHorizon.as_str() {
        ShardIteratorType::TrimHorizon
    } else if sequence_number == SentinelCheckpoint::AtTimestamp.as_str() {
        ShardIteratorType::AtTimestamp
    } else {
        default_iterator_type
    }
}

/// Build a [`StartingPosition`] with the resolved iterator type, filling the
/// timestamp for `AT_TIMESTAMP` and the sequence number for
/// `AT_SEQUENCE_NUMBER`/`AFTER_SEQUENCE_NUMBER`.
///
/// Port of the private generic `apply` for the `StartingPosition.Builder` case.
fn build_starting_position(
    sequence_number: &str,
    initial_position: &InitialPositionInStreamExtended,
    default_iterator_type: ShardIteratorType,
) -> StartingPosition {
    let iterator_type = iterator_type_for(sequence_number, default_iterator_type);
    let mut builder: StartingPositionBuilder =
        StartingPosition::builder().r#type(iterator_type.clone());
    builder = match iterator_type {
        ShardIteratorType::AtTimestamp => {
            let ts = initial_position
                .timestamp()
                .expect("AT_TIMESTAMP initial position must carry a timestamp");
            builder.timestamp(smithy_date_time::from_chrono_utc(ts))
        }
        ShardIteratorType::AtSequenceNumber | ShardIteratorType::AfterSequenceNumber => {
            builder.sequence_number(sequence_number)
        }
        _ => builder,
    };
    builder
        .build()
        .expect("StartingPosition requires only the (always-set) iterator type")
}

/// Set the resolved iterator type (and timestamp / sequence number as needed) on
/// a [`GetShardIteratorInputBuilder`].
///
/// Port of the private generic `apply` for the `GetShardIteratorRequest.Builder`
/// case.
fn apply_get_shard_iterator(
    builder: GetShardIteratorInputBuilder,
    sequence_number: &str,
    initial_position: &InitialPositionInStreamExtended,
    default_iterator_type: ShardIteratorType,
) -> GetShardIteratorInputBuilder {
    let iterator_type = iterator_type_for(sequence_number, default_iterator_type);
    let builder = builder.shard_iterator_type(iterator_type.clone());
    match iterator_type {
        ShardIteratorType::AtTimestamp => {
            let ts = initial_position
                .timestamp()
                .expect("AT_TIMESTAMP initial position must carry a timestamp");
            builder.timestamp(smithy_date_time::from_chrono_utc(ts))
        }
        ShardIteratorType::AtSequenceNumber | ShardIteratorType::AfterSequenceNumber => {
            builder.starting_sequence_number(sequence_number)
        }
        _ => builder,
    }
}

/// Set the starting position on a `SubscribeToShard` request for an **initial**
/// connect (default iterator type `AT_SEQUENCE_NUMBER`).
///
/// Port of `IteratorBuilder.request(SubscribeToShardRequest.Builder, ...)`.
pub fn subscribe_to_shard_request(
    builder: SubscribeToShardInputBuilder,
    sequence_number: &str,
    initial_position: &InitialPositionInStreamExtended,
) -> SubscribeToShardInputBuilder {
    builder.starting_position(build_starting_position(
        sequence_number,
        initial_position,
        ShardIteratorType::AtSequenceNumber,
    ))
}

/// Set the starting position on a `SubscribeToShard` request for a **reconnect**
/// (default iterator type `AFTER_SEQUENCE_NUMBER`, since the given sequence
/// number was already delivered/processed).
///
/// Port of `IteratorBuilder.reconnectRequest(SubscribeToShardRequest.Builder, ...)`.
pub fn subscribe_to_shard_reconnect_request(
    builder: SubscribeToShardInputBuilder,
    sequence_number: &str,
    initial_position: &InitialPositionInStreamExtended,
) -> SubscribeToShardInputBuilder {
    builder.starting_position(build_starting_position(
        sequence_number,
        initial_position,
        ShardIteratorType::AfterSequenceNumber,
    ))
}

/// Build a `StartingPosition` for an **initial** connect (default
/// `AT_SEQUENCE_NUMBER`). Port of `IteratorBuilder.request(StartingPosition.Builder, ...)`.
pub fn starting_position_request(
    sequence_number: &str,
    initial_position: &InitialPositionInStreamExtended,
) -> StartingPosition {
    build_starting_position(
        sequence_number,
        initial_position,
        ShardIteratorType::AtSequenceNumber,
    )
}

/// Build a `StartingPosition` for a **reconnect** (default
/// `AFTER_SEQUENCE_NUMBER`). Port of `IteratorBuilder.reconnectRequest(StartingPosition.Builder, ...)`.
pub fn starting_position_reconnect_request(
    sequence_number: &str,
    initial_position: &InitialPositionInStreamExtended,
) -> StartingPosition {
    build_starting_position(
        sequence_number,
        initial_position,
        ShardIteratorType::AfterSequenceNumber,
    )
}

/// Configure a `GetShardIterator` request for an **initial** connect (default
/// `AT_SEQUENCE_NUMBER`). Port of
/// `IteratorBuilder.request(GetShardIteratorRequest.Builder, ...)`.
pub fn get_shard_iterator_request(
    builder: GetShardIteratorInputBuilder,
    sequence_number: &str,
    initial_position: &InitialPositionInStreamExtended,
) -> GetShardIteratorInputBuilder {
    apply_get_shard_iterator(
        builder,
        sequence_number,
        initial_position,
        ShardIteratorType::AtSequenceNumber,
    )
}

/// Configure a `GetShardIterator` request for a **reconnect** (default
/// `AFTER_SEQUENCE_NUMBER`). Port of
/// `IteratorBuilder.reconnectRequest(GetShardIteratorRequest.Builder, ...)`.
pub fn get_shard_iterator_reconnect_request(
    builder: GetShardIteratorInputBuilder,
    sequence_number: &str,
    initial_position: &InitialPositionInStreamExtended,
) -> GetShardIteratorInputBuilder {
    apply_get_shard_iterator(
        builder,
        sequence_number,
        initial_position,
        ShardIteratorType::AfterSequenceNumber,
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::{InitialPositionInStream, InitialPositionInStreamExtended};
    use aws_sdk_kinesis::operation::get_shard_iterator::GetShardIteratorInput;
    use aws_sdk_kinesis::operation::subscribe_to_shard::SubscribeToShardInput;
    use chrono::{DateTime, Utc};

    const SHARD_ID: &str = "Shard-001";
    const STREAM_NAME: &str = "Stream";
    const CONSUMER_ARN: &str = "arn:stream";
    const SEQUENCE_NUMBER: &str = "1234";

    fn timestamp() -> DateTime<Utc> {
        "2018-04-26T13:03:00Z".parse().unwrap()
    }

    fn sts_base() -> SubscribeToShardInputBuilder {
        SubscribeToShardInput::builder()
            .shard_id(SHARD_ID)
            .consumer_arn(CONSUMER_ARN)
    }

    fn gsi_base() -> GetShardIteratorInputBuilder {
        GetShardIteratorInput::builder()
            .shard_id(SHARD_ID)
            .stream_name(STREAM_NAME)
    }

    // -- SubscribeToShard (StartingPosition) --

    #[test]
    fn subscribe_latest() {
        let pos =
            InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::Latest);
        let req = subscribe_to_shard_request(sts_base(), SentinelCheckpoint::Latest.as_str(), &pos)
            .build()
            .unwrap();
        verify_sts_base(&req);
        let sp = req.starting_position().unwrap();
        assert_eq!(*sp.r#type(), ShardIteratorType::Latest);
        assert_eq!(sp.sequence_number(), None);
        assert_eq!(sp.timestamp(), None);
    }

    #[test]
    fn subscribe_trim_horizon() {
        let pos = InitialPositionInStreamExtended::new_initial_position(
            InitialPositionInStream::TrimHorizon,
        );
        let req =
            subscribe_to_shard_request(sts_base(), SentinelCheckpoint::TrimHorizon.as_str(), &pos)
                .build()
                .unwrap();
        verify_sts_base(&req);
        let sp = req.starting_position().unwrap();
        assert_eq!(*sp.r#type(), ShardIteratorType::TrimHorizon);
        assert_eq!(sp.sequence_number(), None);
        assert_eq!(sp.timestamp(), None);
    }

    #[test]
    fn subscribe_sequence_number() {
        let pos = InitialPositionInStreamExtended::new_initial_position(
            InitialPositionInStream::TrimHorizon,
        );
        let req = subscribe_to_shard_request(sts_base(), SEQUENCE_NUMBER, &pos)
            .build()
            .unwrap();
        verify_sts_base(&req);
        let sp = req.starting_position().unwrap();
        assert_eq!(*sp.r#type(), ShardIteratorType::AtSequenceNumber);
        assert_eq!(sp.sequence_number(), Some(SEQUENCE_NUMBER));
        assert_eq!(sp.timestamp(), None);
    }

    #[test]
    fn subscribe_reconnect_uses_after_sequence_number() {
        let pos = InitialPositionInStreamExtended::new_initial_position(
            InitialPositionInStream::TrimHorizon,
        );
        let req = subscribe_to_shard_reconnect_request(sts_base(), SEQUENCE_NUMBER, &pos)
            .build()
            .unwrap();
        verify_sts_base(&req);
        let sp = req.starting_position().unwrap();
        assert_eq!(*sp.r#type(), ShardIteratorType::AfterSequenceNumber);
        assert_eq!(sp.sequence_number(), Some(SEQUENCE_NUMBER));
        assert_eq!(sp.timestamp(), None);
    }

    #[test]
    fn subscribe_timestamp() {
        let pos = InitialPositionInStreamExtended::new_initial_position_at_timestamp(timestamp());
        let req =
            subscribe_to_shard_request(sts_base(), SentinelCheckpoint::AtTimestamp.as_str(), &pos)
                .build()
                .unwrap();
        verify_sts_base(&req);
        let sp = req.starting_position().unwrap();
        assert_eq!(*sp.r#type(), ShardIteratorType::AtTimestamp);
        assert_eq!(sp.sequence_number(), None);
        assert_eq!(
            smithy_date_time::to_chrono_utc(sp.timestamp().unwrap()).unwrap(),
            timestamp()
        );
    }

    // -- GetShardIterator --

    #[test]
    fn get_shard_latest() {
        let pos =
            InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::Latest);
        let req = get_shard_iterator_request(gsi_base(), SentinelCheckpoint::Latest.as_str(), &pos)
            .build()
            .unwrap();
        verify_gsi_base(&req);
        assert_eq!(req.shard_iterator_type(), Some(&ShardIteratorType::Latest));
        assert_eq!(req.starting_sequence_number(), None);
        assert_eq!(req.timestamp(), None);
    }

    #[test]
    fn get_shard_trim_horizon() {
        let pos = InitialPositionInStreamExtended::new_initial_position(
            InitialPositionInStream::TrimHorizon,
        );
        let req =
            get_shard_iterator_request(gsi_base(), SentinelCheckpoint::TrimHorizon.as_str(), &pos)
                .build()
                .unwrap();
        verify_gsi_base(&req);
        assert_eq!(
            req.shard_iterator_type(),
            Some(&ShardIteratorType::TrimHorizon)
        );
        assert_eq!(req.starting_sequence_number(), None);
        assert_eq!(req.timestamp(), None);
    }

    #[test]
    fn get_shard_sequence_number() {
        let pos = InitialPositionInStreamExtended::new_initial_position(
            InitialPositionInStream::TrimHorizon,
        );
        let req = get_shard_iterator_request(gsi_base(), SEQUENCE_NUMBER, &pos)
            .build()
            .unwrap();
        verify_gsi_base(&req);
        assert_eq!(
            req.shard_iterator_type(),
            Some(&ShardIteratorType::AtSequenceNumber)
        );
        assert_eq!(req.starting_sequence_number(), Some(SEQUENCE_NUMBER));
        assert_eq!(req.timestamp(), None);
    }

    #[test]
    fn get_shard_reconnect_uses_after_sequence_number() {
        let pos = InitialPositionInStreamExtended::new_initial_position(
            InitialPositionInStream::TrimHorizon,
        );
        let req = get_shard_iterator_reconnect_request(gsi_base(), SEQUENCE_NUMBER, &pos)
            .build()
            .unwrap();
        verify_gsi_base(&req);
        assert_eq!(
            req.shard_iterator_type(),
            Some(&ShardIteratorType::AfterSequenceNumber)
        );
        assert_eq!(req.starting_sequence_number(), Some(SEQUENCE_NUMBER));
        assert_eq!(req.timestamp(), None);
    }

    #[test]
    fn get_shard_timestamp() {
        let pos = InitialPositionInStreamExtended::new_initial_position_at_timestamp(timestamp());
        let req =
            get_shard_iterator_request(gsi_base(), SentinelCheckpoint::AtTimestamp.as_str(), &pos)
                .build()
                .unwrap();
        verify_gsi_base(&req);
        assert_eq!(
            req.shard_iterator_type(),
            Some(&ShardIteratorType::AtTimestamp)
        );
        assert_eq!(req.starting_sequence_number(), None);
        assert_eq!(
            smithy_date_time::to_chrono_utc(req.timestamp().unwrap()).unwrap(),
            timestamp()
        );
    }

    fn verify_sts_base(req: &SubscribeToShardInput) {
        assert_eq!(req.shard_id(), Some(SHARD_ID));
        assert_eq!(req.consumer_arn(), Some(CONSUMER_ARN));
    }

    fn verify_gsi_base(req: &GetShardIteratorInput) {
        assert_eq!(req.stream_name(), Some(STREAM_NAME));
        assert_eq!(req.shard_id(), Some(SHARD_ID));
    }
}
