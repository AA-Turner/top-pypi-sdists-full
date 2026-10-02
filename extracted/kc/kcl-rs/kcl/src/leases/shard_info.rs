//! Port of `software.amazon.kinesis.leases.ShardInfo`.

use std::hash::{Hash, Hasher};

use crate::leases::Lease;
use crate::retrieval::kpl::ExtendedSequenceNumber;

/// Passes shard-related info between classes, and serves as the key of the map
/// of shard consumers.
///
/// # Equality / hashing
///
/// Equality and hashing **exclude the `checkpoint`** (it is used only for
/// debugging output). Only `concurrency_token`, `parent_shard_ids`, `shard_id`,
/// and the serialized stream identifier (with `None` treated as `""`)
/// participate — matching the Java `EqualsBuilder`/`HashCodeBuilder`.
///
/// `parent_shard_ids` is a `Vec<String>` **sorted once at construction** (Java
/// `Collections.sort`), so equality is order-independent while iteration order
/// is deterministic (e.g. for `ParentsFirstShardPrioritization`).
#[derive(Debug, Clone)]
pub struct ShardInfo {
    stream_identifier_ser_opt: Option<String>,
    shard_id: String,
    concurrency_token: Option<String>,
    /// Sorted list of parent shard IDs.
    parent_shard_ids: Vec<String>,
    checkpoint: Option<ExtendedSequenceNumber>,
}

impl PartialEq for ShardInfo {
    fn eq(&self, other: &Self) -> bool {
        self.concurrency_token == other.concurrency_token
            && self.parent_shard_ids == other.parent_shard_ids
            && self.shard_id == other.shard_id
            && self.stream_identifier_ser_opt.as_deref().unwrap_or("")
                == other.stream_identifier_ser_opt.as_deref().unwrap_or("")
    }
}

impl Eq for ShardInfo {}

impl Hash for ShardInfo {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.concurrency_token.hash(state);
        self.parent_shard_ids.hash(state);
        self.shard_id.hash(state);
        self.stream_identifier_ser_opt
            .as_deref()
            .unwrap_or("")
            .hash(state);
    }
}

impl ShardInfo {
    /// Create a `ShardInfo`.
    ///
    /// `parent_shard_ids` is copied and sorted into canonical order at
    /// construction. `stream_identifier_ser` is optional (single-stream when
    /// `None`).
    pub fn new(
        shard_id: impl Into<String>,
        concurrency_token: Option<String>,
        parent_shard_ids: impl IntoIterator<Item = String>,
        checkpoint: Option<ExtendedSequenceNumber>,
        stream_identifier_ser: Option<String>,
    ) -> Self {
        let mut parents: Vec<String> = parent_shard_ids.into_iter().collect();
        // Store parent shard Ids in canonical order (makes equals order-independent).
        parents.sort();
        Self {
            shard_id: shard_id.into(),
            concurrency_token,
            parent_shard_ids: parents,
            checkpoint,
            stream_identifier_ser_opt: stream_identifier_ser,
        }
    }

    /// Single-stream constructor (no serialized stream identifier). Mirrors the
    /// 4-arg Java constructor.
    pub fn single_stream(
        shard_id: impl Into<String>,
        concurrency_token: Option<String>,
        parent_shard_ids: impl IntoIterator<Item = String>,
        checkpoint: Option<ExtendedSequenceNumber>,
    ) -> Self {
        Self::new(
            shard_id,
            concurrency_token,
            parent_shard_ids,
            checkpoint,
            None,
        )
    }

    // ---- getters ----

    pub fn shard_id(&self) -> &str {
        &self.shard_id
    }
    pub fn concurrency_token(&self) -> Option<&str> {
        self.concurrency_token.as_deref()
    }
    pub fn checkpoint(&self) -> Option<&ExtendedSequenceNumber> {
        self.checkpoint.as_ref()
    }
    pub fn stream_identifier_ser_opt(&self) -> Option<&str> {
        self.stream_identifier_ser_opt.as_deref()
    }

    /// A defensive copy of the sorted parent shard IDs.
    pub fn parent_shard_ids(&self) -> Vec<String> {
        self.parent_shard_ids.clone()
    }

    /// Whether the shard has been completely processed (checkpoint is
    /// `SHARD_END`).
    pub fn is_completed(&self) -> bool {
        self.checkpoint.as_ref() == Some(&ExtendedSequenceNumber::shard_end())
    }

    /// Derive the lease key from a `ShardInfo` (using its own shard id).
    pub fn lease_key(&self) -> String {
        self.lease_key_with_override(&self.shard_id)
    }

    /// Derive the lease key using an override shard id.
    ///
    /// Delegates to the multi-stream lease-key format when a serialized stream
    /// identifier is present; otherwise returns the raw shard id override. This
    /// is the single canonical place where multi-stream vs single-stream
    /// lease-key format is decided.
    pub fn lease_key_with_override(&self, shard_id_override: &str) -> String {
        match &self.stream_identifier_ser_opt {
            Some(stream_id) => Lease::multi_stream_lease_key(stream_id, shard_id_override),
            None => shard_id_override.to_string(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const CONCURRENCY_TOKEN: &str = "concurrency-token-uuid";
    const SHARD_ID: &str = "shardId-test";

    fn parent_shard_ids() -> Vec<String> {
        vec!["shard-1".to_string(), "shard-2".to_string()]
    }

    fn test_shard_info() -> ShardInfo {
        ShardInfo::single_stream(
            SHARD_ID,
            Some(CONCURRENCY_TOKEN.to_string()),
            parent_shard_ids(),
            Some(ExtendedSequenceNumber::latest()),
        )
    }

    #[test]
    fn equals_with_same_args() {
        let a = test_shard_info();
        let b = ShardInfo::single_stream(
            SHARD_ID,
            Some(CONCURRENCY_TOKEN.to_string()),
            parent_shard_ids(),
            Some(ExtendedSequenceNumber::latest()),
        );
        assert_eq!(a, b);
    }

    #[test]
    fn equals_for_different_token() {
        let base = test_shard_info();
        let diff = ShardInfo::single_stream(
            SHARD_ID,
            Some("other-token".to_string()),
            parent_shard_ids(),
            Some(ExtendedSequenceNumber::latest()),
        );
        assert_ne!(diff, base);
        let null_token = ShardInfo::single_stream(
            SHARD_ID,
            None,
            parent_shard_ids(),
            Some(ExtendedSequenceNumber::latest()),
        );
        assert_ne!(null_token, base);
    }

    #[test]
    fn equals_for_differently_ordered_parent_ids() {
        let reordered = ShardInfo::single_stream(
            SHARD_ID,
            Some(CONCURRENCY_TOKEN.to_string()),
            vec!["shard-2".to_string(), "shard-1".to_string()],
            Some(ExtendedSequenceNumber::latest()),
        );
        assert_eq!(reordered, test_shard_info());
    }

    #[test]
    fn equals_for_parent_ids() {
        let base = test_shard_info();
        let diff = ShardInfo::single_stream(
            SHARD_ID,
            Some(CONCURRENCY_TOKEN.to_string()),
            vec!["shard-3".to_string(), "shard-4".to_string()],
            Some(ExtendedSequenceNumber::latest()),
        );
        assert_ne!(diff, base);
        let empty_parents = ShardInfo::single_stream(
            SHARD_ID,
            Some(CONCURRENCY_TOKEN.to_string()),
            Vec::<String>::new(),
            Some(ExtendedSequenceNumber::latest()),
        );
        assert_ne!(empty_parents, base);
    }

    #[test]
    fn checkpoint_excluded_from_equals_and_hash() {
        use std::collections::hash_map::DefaultHasher;

        let base = ShardInfo::single_stream(
            SHARD_ID,
            Some(CONCURRENCY_TOKEN.to_string()),
            parent_shard_ids(),
            Some(ExtendedSequenceNumber::trim_horizon()),
        );
        let different_checkpoint = ShardInfo::single_stream(
            SHARD_ID,
            Some(CONCURRENCY_TOKEN.to_string()),
            parent_shard_ids(),
            Some(ExtendedSequenceNumber::from_sequence_number("1234")),
        );
        let null_checkpoint = ShardInfo::single_stream(
            SHARD_ID,
            Some(CONCURRENCY_TOKEN.to_string()),
            parent_shard_ids(),
            None,
        );

        assert_eq!(base, different_checkpoint);
        assert_eq!(base, null_checkpoint);

        let hash = |s: &ShardInfo| {
            let mut h = DefaultHasher::new();
            s.hash(&mut h);
            h.finish()
        };
        assert_eq!(hash(&base), hash(&different_checkpoint));
        assert_eq!(hash(&base), hash(&null_checkpoint));
    }

    #[test]
    fn same_hash_code_for_same_args() {
        use std::collections::hash_map::DefaultHasher;
        let hash = |s: &ShardInfo| {
            let mut h = DefaultHasher::new();
            s.hash(&mut h);
            h.finish()
        };
        let a = test_shard_info();
        let b = ShardInfo::single_stream(
            SHARD_ID,
            Some(CONCURRENCY_TOKEN.to_string()),
            parent_shard_ids(),
            Some(ExtendedSequenceNumber::latest()),
        );
        assert_eq!(hash(&a), hash(&b));
    }

    #[test]
    fn is_completed_when_shard_end() {
        let completed = ShardInfo::single_stream(
            SHARD_ID,
            None,
            Vec::<String>::new(),
            Some(ExtendedSequenceNumber::shard_end()),
        );
        assert!(completed.is_completed());
        assert!(!test_shard_info().is_completed());
    }

    #[test]
    fn lease_key_single_vs_multi_stream() {
        let single = test_shard_info();
        assert_eq!(single.lease_key(), SHARD_ID);

        let multi = ShardInfo::new(
            SHARD_ID,
            None,
            Vec::<String>::new(),
            None,
            Some("account:stream:123".to_string()),
        );
        assert_eq!(
            multi.lease_key(),
            format!("account:stream:123:{}", SHARD_ID)
        );
        assert_eq!(
            multi.lease_key_with_override("override"),
            "account:stream:123:override"
        );
    }
}
