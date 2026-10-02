//! Port of `InitialPositionInStream` and `InitialPositionInStreamExtended`.

use chrono::{DateTime, Utc};

/// Port of `software.amazon.kinesis.common.InitialPositionInStream`.
///
/// Specifies where in the stream a new application should start reading when no
/// checkpoint exists for a shard (or its parents).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum InitialPositionInStream {
    /// Start after the most recent data record (fetch new data).
    Latest,
    /// Start from the oldest available data record.
    TrimHorizon,
    /// Start from the record at or after the specified server-side timestamp.
    AtTimestamp,
}

/// Port of `software.amazon.kinesis.common.InitialPositionInStreamExtended`.
///
/// Pairs an [`InitialPositionInStream`] with the timestamp required by
/// [`InitialPositionInStream::AtTimestamp`]. Constructed only through the
/// associated functions, mirroring the private Java constructor.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct InitialPositionInStreamExtended {
    position: InitialPositionInStream,
    /// Present only for [`InitialPositionInStream::AtTimestamp`].
    timestamp: Option<DateTime<Utc>>,
}

impl InitialPositionInStreamExtended {
    /// The initial position in the stream.
    pub fn initial_position_in_stream(&self) -> InitialPositionInStream {
        self.position
    }

    /// The timestamp to start from. Valid only for `AtTimestamp`; `None` otherwise.
    pub fn timestamp(&self) -> Option<DateTime<Utc>> {
        self.timestamp
    }

    /// Port of `newInitialPosition`. Panics-equivalent: returns `Err` for
    /// `AtTimestamp`, which must use [`Self::new_initial_position_at_timestamp`].
    ///
    /// # Panics
    /// Panics with the Java `IllegalArgumentException` message if given
    /// [`InitialPositionInStream::AtTimestamp`].
    pub fn new_initial_position(position: InitialPositionInStream) -> Self {
        match position {
            InitialPositionInStream::Latest => Self {
                position: InitialPositionInStream::Latest,
                timestamp: None,
            },
            InitialPositionInStream::TrimHorizon => Self {
                position: InitialPositionInStream::TrimHorizon,
                timestamp: None,
            },
            InitialPositionInStream::AtTimestamp => {
                panic!("Invalid InitialPosition: {:?}", position)
            }
        }
    }

    /// Port of `newInitialPositionAtTimestamp`.
    pub fn new_initial_position_at_timestamp(timestamp: DateTime<Utc>) -> Self {
        Self {
            position: InitialPositionInStream::AtTimestamp,
            timestamp: Some(timestamp),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::TimeZone;

    #[test]
    fn latest_and_trim_horizon_have_no_timestamp() {
        let latest =
            InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::Latest);
        assert_eq!(
            latest.initial_position_in_stream(),
            InitialPositionInStream::Latest
        );
        assert_eq!(latest.timestamp(), None);

        let th = InitialPositionInStreamExtended::new_initial_position(
            InitialPositionInStream::TrimHorizon,
        );
        assert_eq!(
            th.initial_position_in_stream(),
            InitialPositionInStream::TrimHorizon
        );
        assert_eq!(th.timestamp(), None);
    }

    #[test]
    #[should_panic(expected = "Invalid InitialPosition")]
    fn at_timestamp_via_new_initial_position_panics() {
        InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::AtTimestamp);
    }

    #[test]
    fn at_timestamp_carries_timestamp() {
        let ts = Utc.timestamp_opt(1_000_000, 0).unwrap();
        let pos = InitialPositionInStreamExtended::new_initial_position_at_timestamp(ts);
        assert_eq!(
            pos.initial_position_in_stream(),
            InitialPositionInStream::AtTimestamp
        );
        assert_eq!(pos.timestamp(), Some(ts));
    }
}
