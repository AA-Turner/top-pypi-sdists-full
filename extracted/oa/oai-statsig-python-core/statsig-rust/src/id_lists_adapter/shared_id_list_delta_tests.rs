use super::{IdList, IdListIds, IdListMetadata, IdListUpdate, SharedIdListStore};
use std::collections::{HashMap, HashSet};
use std::fs;
use std::sync::Arc;

fn metadata(name: &str) -> IdListMetadata {
    IdListMetadata {
        name: name.into(),
        url: "http://fixture/list".into(),
        file_id: Some("f1".into()),
        size: 0,
        creation_time: 1,
    }
}
fn list(name: &str, n: usize) -> IdList {
    IdList {
        metadata: metadata(name),
        ids: Arc::new((0..n).map(|i| format!("{i:08x}")).collect()),
    }
}
fn store(root: &tempfile::TempDir) -> SharedIdListStore {
    SharedIdListStore::new(root.path(), "fixture", "source", false).unwrap()
}
fn manifest(store: &SharedIdListStore) -> serde_json::Value {
    serde_json::from_slice(&fs::read(store.directory().join("manifest.json")).unwrap()).unwrap()
}
fn assert_set(ids: &IdListIds, expected: &HashSet<String>) {
    assert_eq!(ids.len(), expected.len());
    assert_eq!(
        ids.iter().map(str::to_owned).collect::<HashSet<_>>(),
        *expected
    );
    for key in expected {
        assert!(ids.contains(key), "missing {key:?}");
    }
    let counts = expected.iter().fold(
        (0, 0),
        |(a, b), k| if k.len() == 8 { (a + 1, b) } else { (a, b + 1) },
    );
    assert_eq!(ids.partition_counts(), counts);
}

#[test]
fn sparse_delta_is_shared_exact_and_preserves_base_and_cursor() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let input = HashMap::from([("members".into(), list("members", 20_000))]);
    let seed = Arc::downgrade(&input["members"].ids);
    let first = writer.publish(&lease, &input, &HashMap::new(), 1).unwrap();
    let before = manifest(&writer);
    drop(input);
    assert!(
        seed.upgrade().is_none(),
        "publisher must not retain the full owned seed"
    );
    let mut next = first.lists.clone();
    let body = "-00000005\n+new-key-with-utf8-🦀\n+éééé\n+00000005\n-00000006\n";
    next.get_mut("members").unwrap().apply_update(IdListUpdate {
        new_metadata: metadata("members"),
        raw_changeset: Some(body.into()),
    });
    assert_eq!(next["members"].ids.delta_len_for_test(), 3);
    assert!(next["members"].ids.owned_capacities_for_test().is_none());
    let second = writer.publish(&lease, &next, &HashMap::new(), 2).unwrap();
    let after = manifest(&writer);
    assert_eq!(
        before["lists"]["members"]["data_file"],
        after["lists"]["members"]["data_file"]
    );
    let delta = after["lists"]["members"]["delta_file"].as_str().unwrap();
    assert!(fs::metadata(writer.directory().join(delta)).unwrap().len() < 4096);
    let follower = store(&root).load().unwrap().unwrap();
    let ids = &follower.lists["members"].ids;
    assert!(ids.is_mapped());
    assert_eq!(ids.delta_len_for_test(), 3);
    assert_eq!(ids.len(), 20_001);
    assert_eq!(follower.lists["members"].metadata.size, body.len() as u64);
    assert!(ids.contains("00000005"));
    assert!(!ids.contains("00000006"));
    assert!(ids.contains("éééé"));
    assert!(ids.contains("new-key-with-utf8-🦀"));
    assert!(!ids.contains("new-key-with-utf8-🦁"));
    assert!(first.lists["members"].ids.contains("00000006"));
    assert!(!first.lists["members"].ids.contains("éééé"));
    assert_eq!(**ids, *second.lists["members"].ids);
}

#[test]
fn delta_reversals_normalize_without_chains_and_old_maps_survive_unlink() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let initial = HashMap::from([("members".into(), list("members", 10000))]);
    let base = writer
        .publish(&lease, &initial, &HashMap::new(), 1)
        .unwrap();
    let mut lists = base.lists.clone();
    let ids = Arc::make_mut(&mut lists.get_mut("members").unwrap().ids);
    ids.insert_str("addition");
    ids.remove("00000001");
    let old = writer.publish(&lease, &lists, &HashMap::new(), 2).unwrap();
    let old_delta = manifest(&writer)["lists"]["members"]["delta_file"]
        .as_str()
        .unwrap()
        .to_owned();
    let mut lists = old.lists.clone();
    let ids = Arc::make_mut(&mut lists.get_mut("members").unwrap().ids);
    ids.remove("addition");
    ids.insert_str("00000001");
    ids.insert_str("");
    ids.insert_str("nul\0key");
    let next = writer.publish(&lease, &lists, &HashMap::new(), 3).unwrap();
    assert!(!writer.directory().join(old_delta).exists());
    assert!(old.lists["members"].ids.contains("addition"));
    assert!(!old.lists["members"].ids.contains("00000001"));
    assert_eq!(next.lists["members"].ids.delta_len_for_test(), 2);
    assert!(next.lists["members"].ids.contains(""));
    assert!(next.lists["members"].ids.contains("nul\0key"));
    let mut lists = next.lists.clone();
    let ids = Arc::make_mut(&mut lists.get_mut("members").unwrap().ids);
    ids.remove("");
    ids.remove("nul\0key");
    let canceled = writer.publish(&lease, &lists, &HashMap::new(), 4).unwrap();
    assert!(
        manifest(&writer)["lists"]["members"]
            .get("delta_file")
            .is_none()
    );
    assert_eq!(*canceled.lists["members"].ids, *base.lists["members"].ids);
}

#[test]
fn threshold_compacts_once_and_shrink_to_empty_releases_current_base() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let first = writer
        .publish(
            &lease,
            &HashMap::from([("members".into(), list("members", 20000))]),
            &HashMap::new(),
            1,
        )
        .unwrap();
    let base_file = manifest(&writer)["lists"]["members"]["data_file"]
        .as_str()
        .unwrap()
        .to_owned();
    let mut lists = first.lists.clone();
    let ids = Arc::make_mut(&mut lists.get_mut("members").unwrap().ids);
    for i in 0..2500 {
        assert!(ids.remove(&format!("{i:08x}")));
    }
    assert_eq!(ids.delta_len_for_test(), 2500);
    assert!(ids.owned_capacities_for_test().is_none());
    ids.remove("000009c4");
    assert!(ids.owned_capacities_for_test().is_some());
    for i in 2501..18000 {
        ids.remove(&format!("{i:08x}"));
    }
    let shrunk = writer.publish(&lease, &lists, &HashMap::new(), 2).unwrap();
    assert_eq!(shrunk.lists["members"].ids.len(), 2000);
    assert_eq!(shrunk.lists["members"].ids.delta_len_for_test(), 0);
    assert!(!writer.directory().join(base_file).exists());
    assert!(first.lists["members"].ids.contains("00000000"));
    let mut lists = shrunk.lists.clone();
    let ids = Arc::make_mut(&mut lists.get_mut("members").unwrap().ids);
    for i in 18000..20000 {
        ids.remove(&format!("{i:08x}"));
    }
    let empty = writer.publish(&lease, &lists, &HashMap::new(), 3).unwrap();
    assert!(empty.lists["members"].ids.is_empty());
    assert_eq!(empty.lists["members"].ids.mapped_bytes(), 128);
    assert_eq!(
        fs::read_dir(writer.directory())
            .unwrap()
            .filter(|e| e
                .as_ref()
                .unwrap()
                .file_name()
                .to_string_lossy()
                .ends_with(".ids"))
            .count(),
        1
    );
}

#[test]
fn cold_new_publisher_updates_delta_without_full_owned_materialization() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let base = writer
        .publish(
            &lease,
            &HashMap::from([("members".into(), list("members", 20000))]),
            &HashMap::new(),
            1,
        )
        .unwrap();
    let mut lists = base.lists.clone();
    Arc::make_mut(&mut lists.get_mut("members").unwrap().ids).insert_str("first-addition");
    let pinned = writer.publish(&lease, &lists, &HashMap::new(), 2).unwrap();
    drop(lease);
    drop(writer);
    drop(lists);
    drop(base);
    let successor = store(&root);
    let lease = successor.try_acquire_lease().unwrap().unwrap();
    let loaded = successor.load().unwrap().unwrap();
    let old_file = manifest(&successor)["lists"]["members"]["data_file"].clone();
    let mut lists = loaded.lists;
    let ids = Arc::make_mut(&mut lists.get_mut("members").unwrap().ids);
    ids.remove("00000000");
    ids.insert_str("second-addition");
    assert_eq!(ids.delta_len_for_test(), 3);
    assert!(ids.owned_capacities_for_test().is_none());
    let updated = successor
        .publish(&lease, &lists, &HashMap::new(), 3)
        .unwrap();
    assert_eq!(
        old_file,
        manifest(&successor)["lists"]["members"]["data_file"]
    );
    assert!(!updated.lists["members"].ids.contains("00000000"));
    assert!(pinned.lists["members"].ids.contains("00000000"));
}

#[test]
fn randomized_cumulative_updates_match_reference_and_pin_generations() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let keys = (0..1400)
        .map(|i| {
            if i % 3 == 0 {
                format!("long-🦀-key-{i}")
            } else {
                format!("{i:08x}")
            }
        })
        .collect::<Vec<_>>();
    let mut expected = keys[..900].iter().cloned().collect::<HashSet<_>>();
    let mut current = writer
        .publish(
            &lease,
            &HashMap::from([(
                "members".into(),
                IdList {
                    metadata: metadata("members"),
                    ids: Arc::new(expected.iter().cloned().collect()),
                },
            )]),
            &HashMap::new(),
            1,
        )
        .unwrap();
    let mut state = 99u64;
    let mut pinned = Vec::new();
    for generation in 2..100 {
        let mut lists = current.lists.clone();
        let ids = Arc::make_mut(&mut lists.get_mut("members").unwrap().ids);
        for _ in 0..31 {
            state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
            let key = &keys[(state >> 16) as usize % keys.len()];
            let add = state & 4 != 0;
            assert_eq!(
                if add {
                    ids.insert_str(key)
                } else {
                    ids.remove(key)
                },
                if add {
                    expected.insert(key.clone())
                } else {
                    expected.remove(key)
                }
            );
        }
        current = writer
            .publish(&lease, &lists, &HashMap::new(), generation)
            .unwrap();
        assert_set(&current.lists["members"].ids, &expected);
        let follower = store(&root).load().unwrap().unwrap();
        assert_set(&follower.lists["members"].ids, &expected);
        if generation % 23 == 0 {
            pinned.push((Arc::clone(&current.lists["members"].ids), expected.clone()));
        }
        for (old, set) in &pinned {
            assert_set(old, set);
        }
    }
}

#[test]
fn catalog_reload_retries_unlinked_delta_and_preserves_whole_generation() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let initial = HashMap::from([("a".into(), list("a", 3000)), ("b".into(), list("b", 3000))]);
    let mut current = writer
        .publish(&lease, &initial, &HashMap::new(), 1)
        .unwrap();
    let mut lists = current.lists.clone();
    for list in lists.values_mut() {
        Arc::make_mut(&mut list.ids).insert_str("old-value");
    }
    current = writer.publish(&lease, &lists, &HashMap::new(), 2).unwrap();
    let reader = store(&root);
    let mut ran = false;
    let loaded = reader
        .load_after_manifest_for_test(|| {
            if !ran {
                ran = true;
                let mut lists = current.lists.clone();
                for list in lists.values_mut() {
                    let ids = Arc::make_mut(&mut list.ids);
                    ids.remove("old-value");
                    ids.insert_str("new-value");
                }
                current = writer.publish(&lease, &lists, &HashMap::new(), 3).unwrap();
            }
        })
        .unwrap()
        .unwrap();
    assert_eq!(loaded.generation, current.generation);
    for list in loaded.lists.values() {
        assert!(list.ids.contains("new-value"));
        assert!(!list.ids.contains("old-value"));
    }
}

#[test]
fn tiny_list_empty_publication_drops_current_base_and_delta_files() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let initial = writer
        .publish(
            &lease,
            &HashMap::from([("members".into(), list("members", 512))]),
            &HashMap::new(),
            1,
        )
        .unwrap();
    let old_file = manifest(&writer)["lists"]["members"]["data_file"]
        .as_str()
        .unwrap()
        .to_owned();
    let mut lists = initial.lists.clone();
    let ids = Arc::make_mut(&mut lists.get_mut("members").unwrap().ids);
    for i in 0..512 {
        assert!(ids.remove(&format!("{i:08x}")));
    }
    let empty = writer.publish(&lease, &lists, &HashMap::new(), 2).unwrap();
    assert!(empty.lists["members"].ids.is_empty());
    assert_eq!(empty.lists["members"].ids.mapped_bytes(), 128);
    assert!(!writer.directory().join(old_file).exists());
    assert!(
        manifest(&writer)["lists"]["members"]
            .get("delta_file")
            .is_none()
    );
    assert_eq!(initial.lists["members"].ids.len(), 512); // Explicit retained old generation remains charged.
    let data_files = fs::read_dir(writer.directory())
        .unwrap()
        .filter(|e| {
            e.as_ref()
                .unwrap()
                .file_name()
                .to_string_lossy()
                .ends_with(".ids")
        })
        .count();
    assert_eq!(data_files, 1);
}
