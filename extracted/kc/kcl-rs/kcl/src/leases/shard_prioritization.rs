//! Port of `software.amazon.kinesis.leases.ShardPrioritization`,
//! `NoOpShardPrioritization`, and `ParentsFirstShardPrioritization`.

use std::collections::HashMap;

use crate::leases::ShardInfo;

/// Strategy that reorders/filters a list of [`ShardInfo`] before shard
/// consumers are created for them (e.g. process parents before children).
///
/// The result may contain fewer elements than the input.
pub trait ShardPrioritization {
    /// Returns a new list of shards ordered by priority, possibly filtered.
    fn prioritize(&self, original: Vec<ShardInfo>) -> Vec<ShardInfo>;
}

/// [`ShardPrioritization`] that returns the input list unmodified.
#[derive(Debug, Default, Clone, Copy)]
pub struct NoOpShardPrioritization;

impl NoOpShardPrioritization {
    pub fn new() -> Self {
        Self
    }
}

impl ShardPrioritization for NoOpShardPrioritization {
    fn prioritize(&self, original: Vec<ShardInfo>) -> Vec<ShardInfo> {
        original
    }
}

/// [`ShardPrioritization`] that prioritizes parent shards first.
///
/// It computes each shard's *depth* (the length of its longest ancestor chain),
/// returns shards sorted ascending by depth, and filters out any shard deeper
/// than `max_depth` — it doesn't make sense to work on a shard with too many
/// unfinished parents.
///
/// Depth rules (memoized recursive DFS):
/// * a shard not present in the input (parent expired/gone) => depth `0`;
/// * a completed shard (`checkpoint == SHARD_END`) => depth `0` (already fully
///   processed, doesn't block);
/// * otherwise depth = `1 + max(parent depths)`.
///
/// Cycle detection uses an explicit "in-progress" set (white/gray/black DFS
/// coloring) instead of Java's sentinel node.
#[derive(Debug, Clone, Copy)]
pub struct ParentsFirstShardPrioritization {
    max_depth: i32,
}

/// Depth marker while a shard's depth is being computed.
enum Progress {
    InProgress,
    Done(i32),
}

impl ParentsFirstShardPrioritization {
    /// Create a parents-first prioritization filtering shards deeper than
    /// `max_depth`.
    ///
    /// # Panics
    /// Panics (Java `IllegalArgumentException`) if `max_depth <= 0`. Depth 0
    /// means the shard is completed or cannot be found, so such shards can never
    /// be processed.
    pub fn new(max_depth: i32) -> Self {
        if max_depth <= 0 {
            panic!(
                "Max depth cannot be negative or zero. Provided value: {}",
                max_depth
            );
        }
        Self { max_depth }
    }

    fn populate_depth(
        shard_id: &str,
        shards: &HashMap<String, ShardInfo>,
        processed_nodes: &mut HashMap<String, Progress>,
        // parallel map holding the ShardInfo for each computed node, mirroring
        // Java's SortingNode carrying its ShardInfo
        ordered: &mut HashMap<String, ShardInfo>,
    ) -> i32 {
        if let Some(progress) = processed_nodes.get(shard_id) {
            match progress {
                Progress::InProgress => panic!(
                    "Circular dependency detected. Shard Id {} is processed twice",
                    shard_id
                ),
                Progress::Done(depth) => return *depth,
            }
        }

        let shard_info = match shards.get(shard_id) {
            // parent doesn't exist in our list, so this shard is a root-level node
            None => return 0,
            Some(si) => si,
        };

        if shard_info.is_completed() {
            // completed shards are treated as 0-level
            return 0;
        }

        // Track progress and detect circular dependencies.
        processed_nodes.insert(shard_id.to_string(), Progress::InProgress);

        let mut max_parent_depth = 0;
        for parent_id in shard_info.parent_shard_ids() {
            max_parent_depth = max_parent_depth.max(Self::populate_depth(
                &parent_id,
                shards,
                processed_nodes,
                ordered,
            ));
        }

        let current_node_level = max_parent_depth + 1;
        let previous =
            processed_nodes.insert(shard_id.to_string(), Progress::Done(current_node_level));
        debug_assert!(
            matches!(previous, Some(Progress::InProgress)),
            "Validation failed. Depth for shardId {} was populated twice",
            shard_id
        );
        ordered.insert(shard_id.to_string(), shard_info.clone());

        current_node_level
    }
}

impl ShardPrioritization for ParentsFirstShardPrioritization {
    fn prioritize(&self, original: Vec<ShardInfo>) -> Vec<ShardInfo> {
        let mut shards: HashMap<String, ShardInfo> = HashMap::new();
        for shard_info in &original {
            shards.insert(shard_info.shard_id().to_string(), shard_info.clone());
        }

        let mut processed_nodes: HashMap<String, Progress> = HashMap::new();
        let mut ordered_infos_map: HashMap<String, ShardInfo> = HashMap::new();

        for shard_info in &original {
            Self::populate_depth(
                shard_info.shard_id(),
                &shards,
                &mut processed_nodes,
                &mut ordered_infos_map,
            );
        }

        // Collect (depth, ShardInfo) pairs for the nodes that were populated
        // (i.e. real, non-completed shards present in the input).
        let mut nodes: Vec<(i32, ShardInfo)> = Vec::with_capacity(ordered_infos_map.len());
        for (shard_id, info) in ordered_infos_map {
            if let Some(Progress::Done(depth)) = processed_nodes.get(&shard_id) {
                nodes.push((*depth, info));
            }
        }

        // Sort ascending by depth (Java sorts SortingNode by depth). Stable sort
        // keeps insertion order for ties.
        nodes.sort_by_key(|(depth, _)| *depth);

        nodes
            .into_iter()
            .filter(|(depth, _)| *depth <= self.max_depth)
            .map(|(_, info)| info)
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::retrieval::kpl::ExtendedSequenceNumber;

    fn shard(id: &str, parents: &[&str], completed: bool) -> ShardInfo {
        let checkpoint = if completed {
            Some(ExtendedSequenceNumber::shard_end())
        } else {
            Some(ExtendedSequenceNumber::latest())
        };
        ShardInfo::single_stream(
            id,
            Some("token".to_string()),
            parents.iter().map(|s| s.to_string()),
            checkpoint,
        )
    }

    fn ids(infos: &[ShardInfo]) -> Vec<String> {
        infos.iter().map(|s| s.shard_id().to_string()).collect()
    }

    #[test]
    fn no_op_returns_input_unchanged() {
        let input = vec![shard("a", &[], false), shard("b", &["a"], false)];
        let out = NoOpShardPrioritization::new().prioritize(input.clone());
        assert_eq!(ids(&out), ids(&input));
    }

    #[test]
    #[should_panic(expected = "Max depth cannot be negative or zero")]
    fn zero_max_depth_panics() {
        ParentsFirstShardPrioritization::new(0);
    }

    /// Port of `ParentsFirstShardPrioritizationUnitTest.testMaxDepthPositiveShouldNotFail`.
    #[test]
    fn positive_max_depth_should_not_fail() {
        // Constructing with a positive max depth must not panic.
        let _ = ParentsFirstShardPrioritization::new(1);
    }

    #[test]
    fn parents_come_before_children() {
        // c -> b -> a (a is root)
        let input = vec![
            shard("c", &["b"], false),
            shard("a", &[], false),
            shard("b", &["a"], false),
        ];
        let out = ParentsFirstShardPrioritization::new(10).prioritize(input);
        // depths: a=1, b=2, c=3
        assert_eq!(ids(&out), vec!["a", "b", "c"]);
    }

    #[test]
    fn filters_shards_deeper_than_max_depth() {
        // a=1, b=2, c=3 ; max_depth 2 excludes c
        let input = vec![
            shard("a", &[], false),
            shard("b", &["a"], false),
            shard("c", &["b"], false),
        ];
        let out = ParentsFirstShardPrioritization::new(2).prioritize(input);
        assert_eq!(ids(&out), vec!["a", "b"]);
    }

    #[test]
    fn missing_parent_makes_shard_root_level() {
        // b's parent "missing" is not in the input -> b depth = 1
        let input = vec![shard("b", &["missing"], false)];
        let out = ParentsFirstShardPrioritization::new(5).prioritize(input);
        assert_eq!(ids(&out), vec!["b"]);
    }

    #[test]
    fn completed_shard_is_excluded_but_counts_as_depth_zero_parent() {
        // a is completed (depth 0, not populated); b's depth = 1
        let input = vec![shard("a", &[], true), shard("b", &["a"], false)];
        let out = ParentsFirstShardPrioritization::new(5).prioritize(input);
        // Completed shards are never populated, so only b appears.
        assert_eq!(ids(&out), vec!["b"]);
    }

    #[test]
    #[should_panic(expected = "Circular dependency detected")]
    fn cycle_panics() {
        // a -> b -> a
        let input = vec![shard("a", &["b"], false), shard("b", &["a"], false)];
        ParentsFirstShardPrioritization::new(10).prioritize(input);
    }
}
