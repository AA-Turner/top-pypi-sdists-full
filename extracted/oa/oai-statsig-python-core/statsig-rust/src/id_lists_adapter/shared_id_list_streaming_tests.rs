//! Publisher-only compaction tests. The ordinary public/private path stays eager.
use crate::id_lists_adapter::id_list_ids::CompactionPolicy;
use std::collections::HashMap;
use std::fs;
use std::sync::Arc;

use super::shared_id_list_format::{digest, write_list};
use super::{IdList, IdListIds, IdListMetadata, IdListUpdate, SharedIdListStore};

const LARGE: usize = 600_000;
fn publisher_limit() -> usize {
    super::id_list_ids::batch_compaction_limits(LARGE).0
}
fn scratch_limit() -> usize {
    super::id_list_ids::batch_compaction_limits(LARGE).1
}
fn crossing() -> usize {
    publisher_limit() + 1
}
fn key(index: usize) -> String {
    format!("{index:08x}")
}
fn metadata() -> IdListMetadata {
    IdListMetadata {
        name: "members".into(),
        url: "http://fixture/list".into(),
        file_id: Some("file1".into()),
        size: 100,
        creation_time: 1,
    }
}
fn store(root: &tempfile::TempDir) -> SharedIdListStore {
    SharedIdListStore::new(root.path(), "stream-key", "source", false).unwrap()
}
fn lists(count: usize) -> HashMap<String, IdList> {
    HashMap::from([(
        "members".into(),
        IdList {
            metadata: metadata(),
            ids: Arc::new((0..count).map(key).collect()),
        },
    )])
}
fn body(add: std::ops::Range<usize>, remove: std::ops::Range<usize>) -> String {
    let mut result = String::with_capacity((add.len() + remove.len()) * 10);
    for index in add {
        result.push('+');
        result.push_str(&key(index));
        result.push('\n');
    }
    for index in remove {
        result.push('-');
        result.push_str(&key(index));
        result.push('\n');
    }
    result
}
fn update(list: &mut IdList, body: &str, publisher: bool) {
    let change = IdListUpdate {
        new_metadata: list.metadata.clone(),
        raw_changeset: Some(body.to_owned()),
    };
    if publisher {
        list.apply_update_for_publish(change);
    } else {
        list.apply_update(change);
    }
}
fn entry(store: &SharedIdListStore) -> serde_json::Value {
    let manifest: serde_json::Value =
        serde_json::from_slice(&fs::read(store.directory().join("manifest.json")).unwrap())
            .unwrap();
    manifest["lists"]["members"].clone()
}
fn canonical_hash(ids: &IdListIds) -> String {
    let namespace = digest(&serde_json::to_vec(&("stream-key", "source")).unwrap());
    let mut file = tempfile::tempfile().unwrap();
    write_list(&mut file, &namespace, "members", ids).unwrap()
}

#[test]
fn publisher_crossing_streams_exactly_the_same_base_as_eager_private_mutation() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let pinned = writer
        .publish(&lease, &lists(LARGE), &HashMap::new(), 1)
        .unwrap();
    let original_file = entry(&writer)["data_file"].clone();
    let replacements = publisher_limit().max(65_536) / 2 + 1;
    let changes = body(1_000_000..1_000_000 + replacements, 0..replacements);
    let mut eager = pinned.lists["members"].clone();
    let mut streamed = eager.clone();
    update(&mut eager, &changes, false);
    update(&mut streamed, &changes, true);
    assert!(eager.ids.owned_capacities_for_test().is_some());
    assert!(streamed.ids.owned_capacities_for_test().is_none());
    let pending = streamed.ids.pending().unwrap();
    assert!(pending.requires_full_base);
    assert_eq!(pending.changes.len(), replacements * 2);
    assert_eq!(*streamed.ids, *eager.ids);
    assert_eq!(streamed.metadata.size, 100 + changes.len() as u64);
    assert_eq!(streamed.ids.partition_counts(), (LARGE, 0));
    println!(
        "streaming_capacity base_members={LARGE} pending_members={} pending_capacity={:?} eager_capacity={:?}",
        pending.changes.len(),
        streamed.ids.pending_capacities_for_test(),
        eager.ids.owned_capacities_for_test()
    );
    let expected_hash = canonical_hash(&eager.ids);
    let source = Arc::downgrade(&streamed.ids);
    let next = HashMap::from([("members".into(), streamed)]);
    let committed = writer.publish(&lease, &next, &HashMap::new(), 2).unwrap();
    drop(next);
    assert!(source.upgrade().is_none());
    assert_ne!(entry(&writer)["data_file"], original_file);
    assert_eq!(
        entry(&writer)["data_file"],
        format!("list-{expected_hash}.ids")
    );
    assert!(entry(&writer).get("delta_file").is_none());
    assert_eq!(*committed.lists["members"].ids, *eager.ids);
    assert!(committed.lists["members"].ids.is_mapped());
    assert!(committed.lists["members"].ids.pending().is_none());
    assert!(pinned.lists["members"].ids.contains(&key(0)));
    assert!(!pinned.lists["members"].ids.contains(&key(1_000_000)));
    assert_eq!(
        *store(&root).load().unwrap().unwrap().lists["members"].ids,
        *eager.ids
    );
}

#[test]
fn full_base_decision_stays_sticky_after_same_batch_reversals() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let pinned = writer
        .publish(&lease, &lists(LARGE), &HashMap::new(), 1)
        .unwrap();
    let original_file = entry(&writer)["data_file"].clone();
    let changes = body(
        1_000_000..1_000_000 + crossing(),
        1_000_000..1_000_000 + crossing(),
    );
    let mut staged = pinned.lists["members"].clone();
    update(&mut staged, &changes, true);
    let pending = staged.ids.pending().unwrap();
    assert!(pending.requires_full_base);
    assert_eq!(pending.changes.len(), 0);
    assert!(staged.ids.owned_capacities_for_test().is_none());
    assert_eq!(*staged.ids, *pinned.lists["members"].ids);
    let committed = writer
        .publish(
            &lease,
            &HashMap::from([("members".into(), staged)]),
            &HashMap::new(),
            2,
        )
        .unwrap();
    assert_eq!(entry(&writer)["data_file"], original_file);
    assert!(entry(&writer).get("delta_file").is_none());
    assert_eq!(
        committed.lists["members"].metadata.size,
        100 + changes.len() as u64
    );
}

#[test]
fn oversized_removal_batch_falls_back_at_actual_count_scratch_bound_then_shrinks() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let pinned = writer
        .publish(&lease, &lists(LARGE), &HashMap::new(), 1)
        .unwrap();
    let mut staged = pinned.lists["members"].clone();
    let ids = Arc::make_mut(&mut staged.ids);
    let scratch_limit = scratch_limit();
    let mut max_pending = 0;
    let mut materialized_at = None;
    let mut max_capacity = 0;
    for index in 0..LARGE * 9 / 10 {
        assert!(ids.set(&key(index), false, CompactionPolicy::Batch));
        if let Some(pending) = ids.pending() {
            max_pending = max_pending.max(pending.changes.len());
            max_capacity = max_capacity.max(ids.pending_capacities_for_test().unwrap().0);
            if index + 1 > publisher_limit() {
                assert!(pending.requires_full_base);
            }
        } else if materialized_at.is_none() {
            materialized_at = Some(index + 1);
        }
    }
    assert_eq!(max_pending, scratch_limit);
    assert_eq!(materialized_at, Some(scratch_limit + 1));
    assert!(ids.owned_capacities_for_test().is_some());
    assert_eq!(ids.len(), LARGE / 10);
    println!(
        "streaming_mass_shrink base_members={LARGE} maximum_completed_pending={max_pending} maximum_observed_pending_capacity={max_capacity} fallback_operation={} owned_capacity={:?}",
        materialized_at.unwrap(),
        ids.owned_capacities_for_test()
    );
    let committed = writer
        .publish(
            &lease,
            &HashMap::from([("members".into(), staged)]),
            &HashMap::new(),
            2,
        )
        .unwrap();
    assert!(entry(&writer).get("delta_file").is_none());
    let ids = &committed.lists["members"].ids;
    assert_eq!(ids.len(), LARGE / 10);
    assert!(!ids.contains(&key(0)));
    assert!(ids.contains(&key(LARGE - 1)));
    assert!(ids.mapped_bytes() < pinned.lists["members"].ids.mapped_bytes() / 2);
    assert!(pinned.lists["members"].ids.contains(&key(0)));
}

#[test]
fn empty_tiny_noop_and_generation_reset_keep_their_existing_semantics() {
    for count in [0, 1, 4] {
        let root = tempfile::tempdir().unwrap();
        let writer = store(&root);
        let lease = writer.try_acquire_lease().unwrap().unwrap();
        let pinned = writer
            .publish(&lease, &lists(count), &HashMap::new(), 1)
            .unwrap();
        let mut staged = pinned.lists["members"].clone();
        let initial_ids = Arc::clone(&staged.ids);
        staged.apply_update_for_publish(IdListUpdate {
            new_metadata: staged.metadata.clone(),
            raw_changeset: None,
        });
        assert!(Arc::ptr_eq(&initial_ids, &staged.ids));
        update(&mut staged, &body(0..0, 0..count), true);
        assert!(staged.ids.is_empty());
        let empty = writer
            .publish(
                &lease,
                &HashMap::from([("members".into(), staged.clone())]),
                &HashMap::new(),
                2,
            )
            .unwrap();
        assert_eq!(empty.lists["members"].ids.mapped_bytes(), 128);
        assert!(entry(&writer).get("delta_file").is_none());
        let mut reset = staged.metadata.clone();
        reset.creation_time += 1;
        let body = "+resetval\n+🦀\n";
        staged.apply_update_for_publish(IdListUpdate {
            new_metadata: reset.clone(),
            raw_changeset: Some(body.into()),
        });
        assert_eq!(staged.ids.partition_counts(), (1, 1));
        assert!(staged.ids.owned_capacities_for_test().is_some());
        assert!(staged.ids.pending().is_none());
        assert_eq!(staged.metadata.size, body.len() as u64);
        assert!(staged.ids.contains("resetval"));
        assert!(staged.ids.contains("🦀"));
        reset.creation_time -= 1;
        staged.apply_update_for_publish(IdListUpdate {
            new_metadata: reset,
            raw_changeset: Some("+stale-old-key\n".into()),
        });
        assert!(!staged.ids.contains("stale-old-key"));
        assert_eq!(staged.metadata.size, body.len() as u64);
    }
}

#[test]
fn growth_batch_uses_streaming_until_the_scratch_bound_and_handles_fallback_keys() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let pinned = writer
        .publish(&lease, &lists(LARGE), &HashMap::new(), 1)
        .unwrap();
    let mut changes = body(1_000_000..1_000_000 + crossing(), 0..0);
    changes.push_str("+fallback-🦀\n+éééé\n+fallback-🦀\n");
    let mut staged = pinned.lists["members"].clone();
    update(&mut staged, &changes, true);
    assert!(staged.ids.pending().unwrap().requires_full_base);
    assert_eq!(staged.ids.pending().unwrap().changes.len(), crossing() + 2);
    assert_eq!(staged.ids.partition_counts(), (LARGE + crossing() + 1, 1));
    assert!(staged.ids.owned_capacities_for_test().is_none());
    let committed = writer
        .publish(
            &lease,
            &HashMap::from([("members".into(), staged)]),
            &HashMap::new(),
            2,
        )
        .unwrap();
    assert!(committed.lists["members"].ids.contains("fallback-🦀"));
    assert!(committed.lists["members"].ids.contains("éééé"));
    assert_eq!(committed.lists["members"].ids.len(), LARGE + crossing() + 2);
    assert!(entry(&writer).get("delta_file").is_none());
}

#[test]
fn cold_successor_compacts_existing_cumulative_delta_and_preserves_old_pins() {
    let root = tempfile::tempdir().unwrap();
    let first = store(&root);
    let first_lease = first.try_acquire_lease().unwrap().unwrap();
    let initial = first
        .publish(&first_lease, &lists(LARGE), &HashMap::new(), 1)
        .unwrap();
    let mut staged = initial.lists["members"].clone();
    let first_changes = publisher_limit() / 2;
    let final_changes = crossing();
    update(&mut staged, &body(0..0, 0..first_changes), true);
    let old = first
        .publish(
            &first_lease,
            &HashMap::from([("members".into(), staged)]),
            &HashMap::new(),
            2,
        )
        .unwrap();
    assert_eq!(old.lists["members"].ids.delta_len_for_test(), first_changes);
    drop(first_lease);
    drop(first);
    let successor = store(&root);
    let lease = successor.try_acquire_lease().unwrap().unwrap();
    let loaded = successor.load().unwrap().unwrap();
    let mut staged = loaded.lists["members"].clone();
    let prior_cursor = staged.metadata.size;
    let changes = body(0..0, first_changes..final_changes);
    update(&mut staged, &changes, true);
    assert!(staged.ids.pending().unwrap().requires_full_base);
    assert_eq!(staged.ids.pending().unwrap().changes.len(), final_changes);
    assert!(staged.ids.owned_capacities_for_test().is_none());
    let committed = successor
        .publish(
            &lease,
            &HashMap::from([("members".into(), staged)]),
            &HashMap::new(),
            3,
        )
        .unwrap();
    assert!(entry(&successor).get("delta_file").is_none());
    assert_eq!(
        committed.lists["members"].metadata.size,
        prior_cursor + changes.len() as u64
    );
    assert_eq!(committed.lists["members"].ids.len(), LARGE - final_changes);
    assert!(old.lists["members"].ids.contains(&key(first_changes)));
    assert!(!committed.lists["members"].ids.contains(&key(first_changes)));
    assert!(initial.lists["members"].ids.contains(&key(0)));
}

#[test]
fn failed_streamed_publication_preserves_old_cursor_and_retries_same_candidate() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let initial = writer
        .publish(&lease, &lists(LARGE), &HashMap::new(), 1)
        .unwrap();
    let previous_manifest = fs::read(writer.directory().join("manifest.json")).unwrap();
    let changes = body(1_000_000..1_000_000 + crossing(), 0..0);
    let mut staged = initial.lists["members"].clone();
    update(&mut staged, &changes, true);
    assert!(staged.ids.pending().unwrap().requires_full_base);
    let expected = canonical_hash(&staged.ids);
    let orphan = writer.directory().join(format!("list-{expected}.ids"));
    fs::write(&orphan, b"incomplete").unwrap();
    let next = HashMap::from([("members".into(), staged)]);
    assert!(writer.publish(&lease, &next, &HashMap::new(), 2).is_err());
    assert_eq!(
        fs::read(writer.directory().join("manifest.json")).unwrap(),
        previous_manifest
    );
    let loaded = store(&root).load().unwrap().unwrap();
    assert_eq!(loaded.lists["members"].metadata.size, 100);
    assert!(!loaded.lists["members"].ids.contains(&key(1_000_000)));
    assert!(next["members"].ids.pending().unwrap().requires_full_base);
    fs::remove_file(orphan).unwrap();
    let committed = writer.publish(&lease, &next, &HashMap::new(), 2).unwrap();
    assert_eq!(entry(&writer)["data_file"], format!("list-{expected}.ids"));
    assert!(entry(&writer).get("delta_file").is_none());
    assert_eq!(
        committed.lists["members"].metadata.size,
        100 + changes.len() as u64
    );
    assert!(committed.lists["members"].ids.contains(&key(1_000_000)));
    assert!(!initial.lists["members"].ids.contains(&key(1_000_000)));
}
