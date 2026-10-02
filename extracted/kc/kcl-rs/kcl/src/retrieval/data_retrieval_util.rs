//! Port of `software.amazon.kinesis.retrieval.DataRetrievalUtil`.

use aws_sdk_kinesis::types::ChildShard;

/// Validates the combination of a shard-end indicator and a child-shards list,
/// catching malformed service responses before they corrupt lease bookkeeping.
///
/// `shard_end_indicator` is `nextShardIterator` for a `GetRecordsResponse`, and
/// `continuationSequenceNumber` for a `SubscribeToShardEvent`.
///
/// Rule (port of `isValidResult`), preserving the exact boolean logic:
/// 1. **ShardEnd scenario**: `shard_end_indicator` should be `None` and
///    `child_shards` should be a non-empty list.
/// 2. **Non-ShardEnd scenario**: `shard_end_indicator` should be `Some` and
///    `child_shards` should be empty.
///
/// Both empty and both present are invalid. For the ShardEnd scenario, every
/// child shard must have non-empty parent shards (missing parents break child
/// lease creation during `ShardConsumer` shutdown).
pub fn is_valid_result(shard_end_indicator: Option<&str>, child_shards: &[ChildShard]) -> bool {
    let child_shards_empty = child_shards.is_empty();

    if (shard_end_indicator.is_none() && child_shards_empty)
        || (shard_end_indicator.is_some() && !child_shards_empty)
    {
        return false;
    }

    // ShardEnd scenario: validate each child shard has parent shards.
    if !child_shards_empty {
        for child_shard in child_shards {
            if child_shard.parent_shards().is_empty() {
                return false;
            }
        }
    }

    true
}

#[cfg(test)]
mod tests {
    use super::*;

    fn child_with_parents(id: &str, parents: &[&str]) -> ChildShard {
        let mut b = ChildShard::builder().shard_id(id);
        for p in parents {
            b = b.parent_shards(*p);
        }
        b.build().unwrap()
    }

    fn child_without_parents(id: &str) -> ChildShard {
        // parent_shards is a required field; set it to an explicit empty list to
        // model a child shard whose parent shards are missing.
        ChildShard::builder()
            .shard_id(id)
            .set_parent_shards(Some(vec![]))
            .build()
            .unwrap()
    }

    #[test]
    fn both_absent_is_invalid() {
        assert!(!is_valid_result(None, &[]));
    }

    #[test]
    fn both_present_is_invalid() {
        assert!(!is_valid_result(
            Some("iterator"),
            &[child_with_parents("c1", &["p1"])]
        ));
    }

    #[test]
    fn non_shard_end_valid() {
        // shard_end_indicator present, no child shards -> valid.
        assert!(is_valid_result(Some("iterator"), &[]));
    }

    #[test]
    fn shard_end_valid_with_parents() {
        assert!(is_valid_result(
            None,
            &[
                child_with_parents("c1", &["p1"]),
                child_with_parents("c2", &["p1", "p2"])
            ]
        ));
    }

    #[test]
    fn shard_end_invalid_missing_parents() {
        assert!(!is_valid_result(None, &[child_without_parents("c1")]));
    }
}
