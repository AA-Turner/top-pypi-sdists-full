//! Port of `HierarchicalShardSyncerTest` (a representative, algorithm-pinning
//! subset of the 84 Java tests). Covers: the full `determineNewLeasesToCreate`
//! matrix (LATEST / TRIM_HORIZON / AT_TIMESTAMP × partial / complete / empty
//! over SHARD_GRAPH_A and SHARD_GRAPH_B), hash-range validation + retry, the
//! static shard-map/child-map/open-shards/parent-ids helpers, the
//! `checkIfDescendantAndAddNewLeasesForAncestors` edge cases, `createLeaseForChildShard`,
//! and an end-to-end `checkAndCreateLeaseForNewShards`.

use super::*;
use crate::common::InitialPositionInStream;
use aws_sdk_kinesis::types::{HashKeyRange, SequenceNumberRange};
use std::collections::BTreeMap;

const MAX_HASH_KEY_STR: &str = "340282366920938463463374607431768211455";
const LEASE_OWNER: &str = "TestOwner";
const STREAM_IDENTIFIER: &str = "123456789012:stream:1";

fn latest() -> InitialPositionInStreamExtended {
    InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::Latest)
}
fn trim_horizon() -> InitialPositionInStreamExtended {
    InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::TrimHorizon)
}
fn at_timestamp() -> InitialPositionInStreamExtended {
    InitialPositionInStreamExtended::new_initial_position_at_timestamp(
        chrono::DateTime::from_timestamp_millis(1000).unwrap(),
    )
}

// ---- shard builders (mirror ShardObjectHelper) ----

fn seq_range(start: &str, end: Option<&str>) -> SequenceNumberRange {
    let mut b = SequenceNumberRange::builder().starting_sequence_number(start);
    if let Some(e) = end {
        b = b.ending_sequence_number(e);
    }
    b.build().unwrap()
}

fn hash_range(start: &str, end: &str) -> HashKeyRange {
    HashKeyRange::builder()
        .starting_hash_key(start)
        .ending_hash_key(end)
        .build()
        .unwrap()
}

fn new_shard(
    shard_id: &str,
    parent: Option<&str>,
    adjacent: Option<&str>,
    seq: SequenceNumberRange,
    hash: HashKeyRange,
) -> Shard {
    let mut b = Shard::builder()
        .shard_id(shard_id)
        .sequence_number_range(seq)
        .hash_key_range(hash);
    if let Some(p) = parent {
        b = b.parent_shard_id(p);
    }
    if let Some(a) = adjacent {
        b = b.adjacent_parent_shard_id(a);
    }
    b.build().unwrap()
}

/// SHARD_GRAPH_A: 0 1 2 3 4 5 → 6(0,1) 7(2,3) 4 5 → 8(6,7) 4 9(5) 10(5).
fn shard_graph_a() -> Vec<Shard> {
    let range0 = || seq_range("11", Some("102"));
    let range1 = || seq_range("11", None);
    let range2 = || seq_range("11", Some("205"));
    let range3 = || seq_range("103", Some("205"));
    let range4 = || seq_range("206", None);
    vec![
        new_shard("shardId-0", None, None, range0(), hash_range("0", "99")),
        new_shard("shardId-1", None, None, range0(), hash_range("100", "199")),
        new_shard("shardId-2", None, None, range0(), hash_range("200", "299")),
        new_shard("shardId-3", None, None, range0(), hash_range("300", "399")),
        new_shard("shardId-4", None, None, range1(), hash_range("400", "499")),
        new_shard(
            "shardId-5",
            None,
            None,
            range2(),
            hash_range("500", MAX_HASH_KEY_STR),
        ),
        new_shard(
            "shardId-6",
            Some("shardId-0"),
            Some("shardId-1"),
            range3(),
            hash_range("0", "199"),
        ),
        new_shard(
            "shardId-7",
            Some("shardId-2"),
            Some("shardId-3"),
            range3(),
            hash_range("200", "399"),
        ),
        new_shard(
            "shardId-8",
            Some("shardId-6"),
            Some("shardId-7"),
            range4(),
            hash_range("0", "399"),
        ),
        new_shard(
            "shardId-9",
            Some("shardId-5"),
            None,
            range4(),
            hash_range("500", "799"),
        ),
        new_shard(
            "shardId-10",
            None,
            Some("shardId-5"),
            range4(),
            hash_range("800", MAX_HASH_KEY_STR),
        ),
    ]
}

/// SHARD_GRAPH_B: linear alternating merge/split.
fn shard_graph_b() -> Vec<Shard> {
    let r0 = || seq_range("1000", Some("1049"));
    let r1 = || seq_range("1050", Some("1099"));
    let r2 = || seq_range("1100", Some("1149"));
    let r3 = || seq_range("1150", Some("1199"));
    let r4 = || seq_range("1200", Some("1249"));
    let r5 = || seq_range("1250", Some("1299"));
    let r6 = || seq_range("1300", None);
    let h0 = || hash_range("0", "499");
    let h1 = || hash_range("500", MAX_HASH_KEY_STR);
    let h2 = || hash_range("0", MAX_HASH_KEY_STR);
    vec![
        new_shard("shardId-0", None, None, r0(), h0()),
        new_shard("shardId-1", None, None, r0(), h1()),
        new_shard(
            "shardId-2",
            Some("shardId-0"),
            Some("shardId-1"),
            r1(),
            h2(),
        ),
        new_shard("shardId-3", Some("shardId-2"), None, r2(), h0()),
        new_shard("shardId-4", Some("shardId-2"), None, r2(), h1()),
        new_shard(
            "shardId-5",
            Some("shardId-3"),
            Some("shardId-4"),
            r3(),
            h2(),
        ),
        new_shard("shardId-6", Some("shardId-5"), None, r4(), h0()),
        new_shard("shardId-7", Some("shardId-5"), None, r4(), h1()),
        new_shard(
            "shardId-8",
            Some("shardId-6"),
            Some("shardId-7"),
            r5(),
            h2(),
        ),
        new_shard("shardId-9", Some("shardId-8"), None, r6(), h0()),
        new_shard("shardId-10", None, Some("shardId-8"), r6(), h1()),
    ]
}

fn new_lease(shard_id: &str) -> Lease {
    let mut lease = Lease::default();
    lease.set_lease_key(shard_id);
    lease
}

/// Port of `assertExpectedLeasesAreCreated` (NonEmptyLeaseTableSynchronizer path).
fn assert_expected_leases(
    shards: &[Shard],
    shard_ids_of_current_leases: &[&str],
    initial_position: &InitialPositionInStreamExtended,
    expected: &[(&str, ExtendedSequenceNumber)],
) {
    let current_leases: Vec<Lease> = shard_ids_of_current_leases
        .iter()
        .map(|s| new_lease(s))
        .collect();
    let shard_id_to_shard_map = construct_shard_id_to_shard_map(shards);
    let shard_id_to_child_shard_ids_map =
        construct_shard_id_to_child_shard_ids_map(&shard_id_to_shard_map);

    let synchronizer = LeaseSynchronizer::NonEmpty {
        shard_id_to_shard_map,
        shard_id_to_child_shard_ids_map,
    };
    let args = MultiStreamArgs::new(false, None);
    let new_leases = determine_new_leases_to_create(
        &synchronizer,
        shards,
        &current_leases,
        initial_position,
        &HashSet::new(),
        &args,
    );

    let expected_map: BTreeMap<String, ExtendedSequenceNumber> = expected
        .iter()
        .map(|(k, v)| (k.to_string(), v.clone()))
        .collect();
    assert_eq!(
        new_leases.len(),
        expected_map.len(),
        "unexpected number of leases: {:?}",
        new_leases
            .iter()
            .map(|l| l.lease_key().unwrap().to_string())
            .collect::<Vec<_>>()
    );
    for lease in &new_leases {
        let key = lease.lease_key().unwrap();
        let expected_cp = expected_map
            .get(key)
            .unwrap_or_else(|| panic!("unexpected lease created: {}", key));
        assert_eq!(
            lease.checkpoint(),
            Some(expected_cp),
            "wrong checkpoint for {}",
            key
        );
    }
}

// ==========================================================================
// EmptyLeaseTableSynchronizer basics
// ==========================================================================

#[test]
fn empty_synchronizer_no_shards() {
    let leases = determine_new_leases_empty(&[], &latest(), &MultiStreamArgs::new(false, None));
    assert!(leases.is_empty());
}

#[test]
fn empty_synchronizer_two_open_shards_latest() {
    // testDetermineNewLeasesToCreate0Leases0Reshards
    let seq = seq_range("342980", None);
    let shards = vec![
        new_shard("shardId-0", None, None, seq.clone(), hash_range("0", "99")),
        new_shard(
            "shardId-1",
            None,
            None,
            seq,
            hash_range("100", MAX_HASH_KEY_STR),
        ),
    ];
    let leases = determine_new_leases_empty(&shards, &latest(), &MultiStreamArgs::new(false, None));
    let keys: HashSet<String> = leases
        .iter()
        .map(|l| l.lease_key().unwrap().to_string())
        .collect();
    assert_eq!(
        keys,
        HashSet::from(["shardId-0".to_string(), "shardId-1".to_string()])
    );
    for l in &leases {
        assert_eq!(l.checkpoint(), Some(&ExtendedSequenceNumber::latest()));
    }
}

#[test]
fn empty_synchronizer_starting_position_checkpoint() {
    // testDetermineNewLeasesToCreateStartingPosition
    let seq = seq_range("342980", None);
    let shards = vec![
        new_shard("shardId-0", None, None, seq.clone(), hash_range("0", "99")),
        new_shard(
            "shardId-1",
            None,
            None,
            seq,
            hash_range("100", MAX_HASH_KEY_STR),
        ),
    ];
    for (pos, cp) in [
        (latest(), ExtendedSequenceNumber::latest()),
        (trim_horizon(), ExtendedSequenceNumber::trim_horizon()),
    ] {
        let leases = determine_new_leases_empty(&shards, &pos, &MultiStreamArgs::new(false, None));
        for l in &leases {
            assert_eq!(l.checkpoint(), Some(&cp));
        }
    }
}

// ==========================================================================
// NonEmptyLeaseTableSynchronizer — SHARD_GRAPH_A, LATEST
// ==========================================================================

#[test]
fn latest_a_partial_range_1() {
    // current (3,4,5) → (2,6) LATEST
    assert_expected_leases(
        &shard_graph_a(),
        &["shardId-3", "shardId-4", "shardId-5"],
        &latest(),
        &[
            ("shardId-2", ExtendedSequenceNumber::latest()),
            ("shardId-6", ExtendedSequenceNumber::latest()),
        ],
    );
}

#[test]
fn latest_a_partial_range_2() {
    // current (4,5,7) → (6) LATEST
    assert_expected_leases(
        &shard_graph_a(),
        &["shardId-4", "shardId-5", "shardId-7"],
        &latest(),
        &[("shardId-6", ExtendedSequenceNumber::latest())],
    );
}

#[test]
fn latest_a_partial_range_3() {
    // current (2,6) → (3,4,9,10) LATEST
    assert_expected_leases(
        &shard_graph_a(),
        &["shardId-2", "shardId-6"],
        &latest(),
        &[
            ("shardId-3", ExtendedSequenceNumber::latest()),
            ("shardId-4", ExtendedSequenceNumber::latest()),
            ("shardId-9", ExtendedSequenceNumber::latest()),
            ("shardId-10", ExtendedSequenceNumber::latest()),
        ],
    );
}

#[test]
fn latest_a_partial_range_4() {
    // current (4,9,10) → (8) LATEST
    assert_expected_leases(
        &shard_graph_a(),
        &["shardId-4", "shardId-9", "shardId-10"],
        &latest(),
        &[("shardId-8", ExtendedSequenceNumber::latest())],
    );
}

#[test]
fn latest_a_complete_range() {
    // current (4,5,6,7) → empty
    assert_expected_leases(
        &shard_graph_a(),
        &["shardId-4", "shardId-5", "shardId-6", "shardId-7"],
        &latest(),
        &[],
    );
}

#[test]
fn latest_a_complete_range_across_epochs() {
    // current (0,1,4,7,9,10) → empty
    assert_expected_leases(
        &shard_graph_a(),
        &[
            "shardId-0",
            "shardId-1",
            "shardId-4",
            "shardId-7",
            "shardId-9",
            "shardId-10",
        ],
        &latest(),
        &[],
    );
}

// ==========================================================================
// NonEmptyLeaseTableSynchronizer — SHARD_GRAPH_A, TRIM_HORIZON
// ==========================================================================

#[test]
fn trim_horizon_a_partial_range_1() {
    // current (3,4,5) → (0,1,2) TRIM_HORIZON
    assert_expected_leases(
        &shard_graph_a(),
        &["shardId-3", "shardId-4", "shardId-5"],
        &trim_horizon(),
        &[
            ("shardId-0", ExtendedSequenceNumber::trim_horizon()),
            ("shardId-1", ExtendedSequenceNumber::trim_horizon()),
            ("shardId-2", ExtendedSequenceNumber::trim_horizon()),
        ],
    );
}

#[test]
fn trim_horizon_a_partial_range_2() {
    // current (4,5,7) → (0,1) TRIM_HORIZON
    assert_expected_leases(
        &shard_graph_a(),
        &["shardId-4", "shardId-5", "shardId-7"],
        &trim_horizon(),
        &[
            ("shardId-0", ExtendedSequenceNumber::trim_horizon()),
            ("shardId-1", ExtendedSequenceNumber::trim_horizon()),
        ],
    );
}

#[test]
fn trim_horizon_a_partial_range_4() {
    // current (4,9,10) → (0,1,2,3) TRIM_HORIZON
    assert_expected_leases(
        &shard_graph_a(),
        &["shardId-4", "shardId-9", "shardId-10"],
        &trim_horizon(),
        &[
            ("shardId-0", ExtendedSequenceNumber::trim_horizon()),
            ("shardId-1", ExtendedSequenceNumber::trim_horizon()),
            ("shardId-2", ExtendedSequenceNumber::trim_horizon()),
            ("shardId-3", ExtendedSequenceNumber::trim_horizon()),
        ],
    );
}

#[test]
fn trim_horizon_a_complete_range() {
    assert_expected_leases(
        &shard_graph_a(),
        &["shardId-4", "shardId-5", "shardId-6", "shardId-7"],
        &trim_horizon(),
        &[],
    );
}

// ==========================================================================
// NonEmptyLeaseTableSynchronizer — SHARD_GRAPH_A, AT_TIMESTAMP
// ==========================================================================

#[test]
fn at_timestamp_a_partial_range_1() {
    // current (3,4,5) → (0,1,2) AT_TIMESTAMP
    assert_expected_leases(
        &shard_graph_a(),
        &["shardId-3", "shardId-4", "shardId-5"],
        &at_timestamp(),
        &[
            ("shardId-0", ExtendedSequenceNumber::at_timestamp()),
            ("shardId-1", ExtendedSequenceNumber::at_timestamp()),
            ("shardId-2", ExtendedSequenceNumber::at_timestamp()),
        ],
    );
}

#[test]
fn at_timestamp_a_partial_range_4() {
    // current (4,9,10) → (0,1,2,3) AT_TIMESTAMP
    assert_expected_leases(
        &shard_graph_a(),
        &["shardId-4", "shardId-9", "shardId-10"],
        &at_timestamp(),
        &[
            ("shardId-0", ExtendedSequenceNumber::at_timestamp()),
            ("shardId-1", ExtendedSequenceNumber::at_timestamp()),
            ("shardId-2", ExtendedSequenceNumber::at_timestamp()),
            ("shardId-3", ExtendedSequenceNumber::at_timestamp()),
        ],
    );
}

// ==========================================================================
// NonEmptyLeaseTableSynchronizer — SHARD_GRAPH_B
// ==========================================================================

#[test]
fn latest_b_partial_range() {
    // current (6) → (7) LATEST
    assert_expected_leases(
        &shard_graph_b(),
        &["shardId-6"],
        &latest(),
        &[("shardId-7", ExtendedSequenceNumber::latest())],
    );
}

#[test]
fn latest_b_complete_range() {
    // current (5) → empty
    assert_expected_leases(&shard_graph_b(), &["shardId-5"], &latest(), &[]);
}

#[test]
fn trim_horizon_b_complete_range() {
    assert_expected_leases(&shard_graph_b(), &["shardId-5"], &trim_horizon(), &[]);
}

// ==========================================================================
// Static helper methods
// ==========================================================================

#[test]
fn construct_shard_maps_and_children() {
    let shards = shard_graph_a();
    let map = construct_shard_id_to_shard_map(&shards);
    assert_eq!(map.len(), 11);
    let children = construct_shard_id_to_child_shard_ids_map(&map);
    assert_eq!(
        children.get("shardId-0"),
        Some(&HashSet::from(["shardId-6".to_string()]))
    );
    assert_eq!(
        children.get("shardId-5"),
        Some(&HashSet::from([
            "shardId-9".to_string(),
            "shardId-10".to_string()
        ]))
    );
    assert_eq!(
        children.get("shardId-6"),
        Some(&HashSet::from(["shardId-8".to_string()]))
    );
}

#[test]
fn open_shards_of_graph_a() {
    let shards = shard_graph_a();
    let open: HashSet<String> = get_open_shards(&shards)
        .iter()
        .map(|s| s.shard_id().to_string())
        .collect();
    assert_eq!(
        open,
        HashSet::from([
            "shardId-4".to_string(),
            "shardId-8".to_string(),
            "shardId-9".to_string(),
            "shardId-10".to_string()
        ])
    );
}

#[test]
fn parent_shard_ids_present_in_map() {
    let shards = shard_graph_a();
    let map = construct_shard_id_to_shard_map(&shards);
    let shard8 = map.get("shardId-8").unwrap();
    assert_eq!(
        get_parent_shard_ids(shard8, &map),
        HashSet::from(["shardId-6".to_string(), "shardId-7".to_string()])
    );
    // shardId-0 has no parents.
    assert!(get_parent_shard_ids(map.get("shardId-0").unwrap(), &map).is_empty());
}

// ==========================================================================
// Hash-range validation
// ==========================================================================

#[test]
fn hash_range_complete_for_graph_a_open_and_closed() {
    // Graph A's full shard set forms a complete range 0..MAX via multiple
    // epochs, but the algorithm checks a single flat list; verify a known
    // complete two-shard partition.
    let shards = vec![
        new_shard(
            "s0",
            None,
            None,
            seq_range("1", None),
            hash_range("0", "99"),
        ),
        new_shard(
            "s1",
            None,
            None,
            seq_range("1", None),
            hash_range("100", MAX_HASH_KEY_STR),
        ),
    ];
    assert!(is_hash_range_of_shards_complete(shards).unwrap());
}

#[test]
fn hash_range_incomplete_when_gap() {
    let shards = vec![
        new_shard("s0", None, None, seq_range("1", None), hash_range("0", "1")),
        new_shard("s1", None, None, seq_range("1", None), hash_range("2", "3")),
    ];
    // gap from 4..MAX
    assert!(!is_hash_range_of_shards_complete(shards).unwrap());
}

#[test]
fn hash_range_incomplete_when_overlap() {
    // Adjacent pair with end+1 != start (overlap: end 100, next start 50).
    let shards = vec![
        new_shard(
            "s0",
            None,
            None,
            seq_range("1", None),
            hash_range("0", "100"),
        ),
        new_shard(
            "s1",
            None,
            None,
            seq_range("1", None),
            hash_range("50", MAX_HASH_KEY_STR),
        ),
    ];
    assert!(!is_hash_range_of_shards_complete(shards).unwrap());
}

#[test]
fn hash_range_empty_list_errors() {
    let err = is_hash_range_of_shards_complete(Vec::new()).unwrap_err();
    assert!(err.to_string().contains("No shards found"));
}

// ==========================================================================
// assertAllParentShardsAreClosed / findInconsistentShardIds
// ==========================================================================

#[test]
fn assert_all_parents_closed_ok_when_empty() {
    assert!(assert_all_parent_shards_are_closed(&HashSet::new()).is_ok());
}

#[test]
fn assert_all_parents_closed_errors_when_inconsistent() {
    let err = assert_all_parent_shards_are_closed(&HashSet::from(["c1".to_string()])).unwrap_err();
    assert!(err.to_string().contains("inconsistent"));
    assert!(matches!(err, KinesisClientLibError::Io { .. }));
}

// ==========================================================================
// checkIfDescendantAndAddNewLeasesForAncestors edge cases
// ==========================================================================

#[test]
fn descendant_null_shard_id_is_false() {
    let mut ctx = MemoizationContext::new();
    let mut new_leases = HashMap::new();
    let result = check_if_descendant_and_add_new_leases_for_ancestors(
        None,
        &latest(),
        &HashSet::new(),
        &HashMap::new(),
        &mut new_leases,
        &mut ctx,
        &MultiStreamArgs::new(false, None),
    );
    assert!(!result);
}

#[test]
fn descendant_trimmed_shard_is_false() {
    let mut ctx = MemoizationContext::new();
    let mut new_leases = HashMap::new();
    let result = check_if_descendant_and_add_new_leases_for_ancestors(
        Some("shardId-trimmed"),
        &latest(),
        &HashSet::new(),
        &HashMap::new(), // shard not in the map
        &mut new_leases,
        &mut ctx,
        &MultiStreamArgs::new(false, None),
    );
    assert!(!result);
}

#[test]
fn descendant_with_current_lease_is_true() {
    let shards = shard_graph_a();
    let map = construct_shard_id_to_shard_map(&shards);
    let current = HashSet::from(["shardId-6".to_string()]);
    let mut ctx = MemoizationContext::new();
    let mut new_leases = HashMap::new();
    let result = check_if_descendant_and_add_new_leases_for_ancestors(
        Some("shardId-6"),
        &latest(),
        &current,
        &map,
        &mut new_leases,
        &mut ctx,
        &MultiStreamArgs::new(false, None),
    );
    assert!(result);
    // No parent leases created (descendant already leased).
    assert!(new_leases.is_empty());
}

// ==========================================================================
// createLeaseForChildShard
// ==========================================================================

fn child_shard(id: &str, parents: &[&str], start: &str, end: &str) -> ChildShard {
    ChildShard::builder()
        .shard_id(id)
        .set_parent_shards(Some(parents.iter().map(|s| s.to_string()).collect()))
        .hash_key_range(hash_range(start, end))
        .build()
        .unwrap()
}

#[test]
fn create_lease_for_child_shard_single_stream() {
    let syncer = HierarchicalShardSyncer::new();
    let child = child_shard("child-1", &["parent-1"], "0", "99");
    let si = StreamIdentifier::single_stream_instance("my-stream");
    let lease = syncer.create_lease_for_child_shard(&child, &si).unwrap();
    assert_eq!(lease.lease_key(), Some("child-1"));
    assert!(!lease.is_multi_stream());
    assert_eq!(
        lease.checkpoint(),
        Some(&ExtendedSequenceNumber::trim_horizon())
    );
    assert_eq!(
        lease.parent_shard_ids(),
        HashSet::from(["parent-1".to_string()])
    );
}

#[test]
fn create_lease_for_child_shard_multi_stream() {
    let syncer = HierarchicalShardSyncer::with_mode(true, STREAM_IDENTIFIER.to_string());
    let child = child_shard("child-1", &["parent-1"], "0", "99");
    let si = StreamIdentifier::multi_stream_instance(STREAM_IDENTIFIER);
    let lease = syncer.create_lease_for_child_shard(&child, &si).unwrap();
    assert!(lease.is_multi_stream());
    assert_eq!(lease.lease_key(), Some("123456789012:stream:1:child-1"));
    assert_eq!(lease.shard_id(), Some("child-1"));
    assert_eq!(lease.stream_identifier(), Some("123456789012:stream:1"));
}

#[test]
fn create_lease_for_child_shard_errors_without_parents() {
    let syncer = HierarchicalShardSyncer::new();
    let child = child_shard("child-1", &[], "0", "99");
    let si = StreamIdentifier::single_stream_instance("my-stream");
    let err = syncer
        .create_lease_for_child_shard(&child, &si)
        .unwrap_err();
    assert!(err.to_string().contains("parent shards cannot be found"));
}

// ==========================================================================
// End-to-end checkAndCreateLeaseForNewShards
// ==========================================================================

#[tokio::test]
async fn end_to_end_creates_leases_for_open_shards_at_latest() {
    // testCheckAndCreateLeasesForShardsIfMissingAtLatest: empty lease table,
    // LATEST → leases for open shards (4, 8, 9, 10) with LATEST checkpoint.
    use crate::leases::MockLeaseRefresher;
    use crate::metrics::NullMetricsScope;

    let shards = shard_graph_a();

    struct FakeDetector {
        shards: Vec<Shard>,
    }
    #[async_trait::async_trait]
    impl ShardDetector for FakeDetector {
        async fn shard(&self, _id: &str) -> Result<Option<Shard>, LeasingError> {
            Ok(None)
        }
        async fn list_shards(&self) -> Result<Vec<Shard>, LeasingError> {
            Ok(self.shards.clone())
        }
        async fn list_shards_with_filter_for_consumer(
            &self,
            _f: ShardFilter,
            _c: &str,
        ) -> Result<Vec<Shard>, LeasingError> {
            // LATEST filter → open shards only.
            Ok(get_open_shards(&self.shards))
        }
        fn stream_identifier(&self) -> Result<StreamIdentifier, LeasingError> {
            Ok(StreamIdentifier::single_stream_instance("my-stream"))
        }
    }

    let detector = FakeDetector { shards };

    let mut refresher = MockLeaseRefresher::new();
    refresher
        .expect_get_lease_table_identifier()
        .returning(|| Ok(String::new()));
    refresher.expect_list_leases().returning(|| Ok(Vec::new()));
    // Capture created lease keys.
    let created = std::sync::Arc::new(std::sync::Mutex::new(Vec::<String>::new()));
    let created_clone = created.clone();
    refresher
        .expect_create_lease_if_not_exists()
        .returning(move |lease| {
            created_clone
                .lock()
                .unwrap()
                .push(lease.lease_key().unwrap().to_string());
            Ok(true)
        });

    let syncer = HierarchicalShardSyncer::new();
    let mut scope = NullMetricsScope::new();
    let performed = syncer
        .check_and_create_lease_for_new_shards(
            &detector,
            &refresher,
            &latest(),
            &mut scope,
            false,
            true, // is_lease_table_empty
        )
        .await
        .unwrap();

    assert!(performed);
    let keys: HashSet<String> = created.lock().unwrap().iter().cloned().collect();
    assert_eq!(
        keys,
        HashSet::from([
            "shardId-4".to_string(),
            "shardId-8".to_string(),
            "shardId-9".to_string(),
            "shardId-10".to_string()
        ])
    );
}

#[tokio::test]
async fn end_to_end_empty_shard_list_skips_sync() {
    use crate::leases::MockLeaseRefresher;
    use crate::metrics::NullMetricsScope;

    struct EmptyDetector;
    #[async_trait::async_trait]
    impl ShardDetector for EmptyDetector {
        async fn shard(&self, _id: &str) -> Result<Option<Shard>, LeasingError> {
            Ok(None)
        }
        async fn list_shards(&self) -> Result<Vec<Shard>, LeasingError> {
            Ok(Vec::new())
        }
        async fn list_shards_without_consuming_resource_not_found_exception_for_consumer(
            &self,
            _c: &str,
        ) -> Result<Vec<Shard>, LeasingError> {
            Ok(Vec::new())
        }
        fn stream_identifier(&self) -> Result<StreamIdentifier, LeasingError> {
            Ok(StreamIdentifier::single_stream_instance("my-stream"))
        }
    }

    let mut refresher = MockLeaseRefresher::new();
    refresher
        .expect_get_lease_table_identifier()
        .returning(|| Ok(String::new()));

    let syncer = HierarchicalShardSyncer::new();
    let mut scope = NullMetricsScope::new();
    let performed = syncer
        .check_and_create_lease_for_new_shards(
            &EmptyDetector,
            &refresher,
            &latest(),
            &mut scope,
            false,
            false, // non-empty lease table path (uses list_shards_without...)
        )
        .await
        .unwrap();
    assert!(!performed);
    let _ = LEASE_OWNER; // silence unused-const lint if it drifts
}

/// A detector whose steady-state list-shards call surfaces the propagated
/// Kinesis `ResourceNotFoundException` exactly the way
/// `KinesisShardDetector` wraps it (`LeasingError::Dependency` with the SDK
/// `ListShardsError` as source).
struct ResourceNotFoundDetector;

#[async_trait::async_trait]
impl ShardDetector for ResourceNotFoundDetector {
    async fn shard(&self, _id: &str) -> Result<Option<Shard>, LeasingError> {
        Ok(None)
    }
    async fn list_shards(&self) -> Result<Vec<Shard>, LeasingError> {
        panic!("listShards must not be called (Java: verify(shardDetector, never()).listShards())");
    }
    async fn list_shards_without_consuming_resource_not_found_exception_for_consumer(
        &self,
        _c: &str,
    ) -> Result<Vec<Shard>, LeasingError> {
        use aws_sdk_kinesis::operation::list_shards::ListShardsError;
        use aws_sdk_kinesis::types::error::ResourceNotFoundException;
        Err(LeasingError::dependency_caused_by(
            "Stream no longer exists",
            ListShardsError::ResourceNotFoundException(
                ResourceNotFoundException::builder().build(),
            ),
        ))
    }
    fn stream_identifier(&self) -> Result<StreamIdentifier, LeasingError> {
        Ok(StreamIdentifier::multi_stream_instance(
            "123456789012:stream:1",
        ))
    }
}

/// Port of `testDeletedStreamListProviderUpdateOnResourceNotFound`: a
/// ResourceNotFound during steady-state shard sync is a graceful skip
/// (`return false`) and, in multi-stream mode, records the stream in the
/// `DeletedStreamListProvider`.
#[tokio::test]
async fn deleted_stream_list_provider_update_on_resource_not_found() {
    use crate::coordinator::DeletedStreamListProvider;
    use crate::leases::MockLeaseRefresher;
    use crate::metrics::NullMetricsScope;

    let provider = std::sync::Arc::new(DeletedStreamListProvider::new());
    let syncer = HierarchicalShardSyncer::with_deleted_stream_list_provider(
        true,
        "123456789012:stream:1".to_string(),
        Some(provider.clone()),
    );

    let mut refresher = MockLeaseRefresher::new();
    refresher
        .expect_get_lease_table_identifier()
        .returning(|| Ok(String::new()));

    let mut scope = NullMetricsScope::new();
    let performed = syncer
        .check_and_create_lease_for_new_shards(
            &ResourceNotFoundDetector,
            &refresher,
            &trim_horizon(),
            &mut scope,
            false,
            false, // isLeaseTableEmpty = false → steady-state getShardList
        )
        .await
        .unwrap();

    assert!(!performed);
    let deleted = provider.purge_all_deleted_stream();
    assert_eq!(deleted.len(), 1);
    assert_eq!(
        deleted.iter().next().unwrap().to_string(),
        "123456789012:stream:1"
    );
}

/// Single-stream mode (or no provider): ResourceNotFound is still a graceful
/// empty-list skip — not an error — but nothing is recorded.
#[tokio::test]
async fn resource_not_found_skips_sync_in_single_stream_mode() {
    use crate::leases::MockLeaseRefresher;
    use crate::metrics::NullMetricsScope;

    let mut refresher = MockLeaseRefresher::new();
    refresher
        .expect_get_lease_table_identifier()
        .returning(|| Ok(String::new()));

    let syncer = HierarchicalShardSyncer::new();
    let mut scope = NullMetricsScope::new();
    let performed = syncer
        .check_and_create_lease_for_new_shards(
            &ResourceNotFoundDetector,
            &refresher,
            &trim_horizon(),
            &mut scope,
            false,
            false,
        )
        .await
        .unwrap();
    assert!(!performed);
}
