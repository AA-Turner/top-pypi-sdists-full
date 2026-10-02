//! Port of `software.amazon.kinesis.checkpoint.SentinelCheckpoint`.

/// Enumeration of the sentinel values of checkpoints.
///
/// Used during initialization of shard consumers to determine the starting
/// point in the shard and to flag that a shard has been completely processed.
///
/// The string forms ([`Self::as_str`]) match the Java enum constant names, as
/// these values are persisted verbatim in the checkpoint store and compared as
/// strings throughout the KCL.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum SentinelCheckpoint {
    /// Start from the first available record in the shard.
    TrimHorizon,
    /// Start from the latest record in the shard.
    Latest,
    /// We've completely processed all records in this shard.
    ShardEnd,
    /// Start from the record at or after the specified server-side timestamp.
    AtTimestamp,
}

impl SentinelCheckpoint {
    /// The Java enum constant name (equivalent to `name()` / `toString()`).
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::TrimHorizon => "TRIM_HORIZON",
            Self::Latest => "LATEST",
            Self::ShardEnd => "SHARD_END",
            Self::AtTimestamp => "AT_TIMESTAMP",
        }
    }

    /// All sentinel constants, mirroring `SentinelCheckpoint.values()`.
    pub const ALL: [SentinelCheckpoint; 4] = [
        Self::TrimHorizon,
        Self::Latest,
        Self::ShardEnd,
        Self::AtTimestamp,
    ];

    /// Parse from the Java constant name; `None` if not a sentinel value.
    pub fn from_name(name: &str) -> Option<SentinelCheckpoint> {
        Self::ALL.into_iter().find(|s| s.as_str() == name)
    }

    /// Whether the given string is one of the sentinel constant names.
    pub fn is_sentinel(name: &str) -> bool {
        Self::from_name(name).is_some()
    }
}

impl std::fmt::Display for SentinelCheckpoint {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(self.as_str())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn names_match_java_constants() {
        assert_eq!(SentinelCheckpoint::TrimHorizon.as_str(), "TRIM_HORIZON");
        assert_eq!(SentinelCheckpoint::Latest.as_str(), "LATEST");
        assert_eq!(SentinelCheckpoint::ShardEnd.as_str(), "SHARD_END");
        assert_eq!(SentinelCheckpoint::AtTimestamp.as_str(), "AT_TIMESTAMP");
    }

    #[test]
    fn sentinel_membership() {
        assert!(SentinelCheckpoint::is_sentinel("SHARD_END"));
        assert!(!SentinelCheckpoint::is_sentinel("12345"));
        assert!(!SentinelCheckpoint::is_sentinel("shard_end"));
    }
}
