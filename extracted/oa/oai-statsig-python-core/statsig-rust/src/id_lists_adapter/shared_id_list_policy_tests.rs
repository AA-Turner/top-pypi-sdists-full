//! Isolated publisher compaction-policy qualification, without timing claims.
use super::id_list_ids::{BATCH_DELTA_DIVISOR, batch_compaction_limits};
use super::{IdList, IdListIds, IdListMetadata, IdListUpdate, SharedIdListStore};
use std::collections::{HashMap, HashSet};
use std::fs;
use std::sync::Arc;

fn key(index: usize) -> String {
    format!("{index:08x}")
}
fn input(n: usize) -> HashMap<String, IdList> {
    HashMap::from([(
        "members".into(),
        IdList {
            metadata: IdListMetadata {
                name: "members".into(),
                url: "http://fixture/members".into(),
                file_id: Some("initial".into()),
                size: 0,
                creation_time: 1,
            },
            ids: Arc::new((0..n).map(key).collect()),
        },
    )])
}
fn store(root: &tempfile::TempDir) -> SharedIdListStore {
    SharedIdListStore::new(root.path(), "policy-fixture", "source", false).unwrap()
}
fn entry(store: &SharedIdListStore) -> serde_json::Value {
    let manifest: serde_json::Value =
        serde_json::from_slice(&fs::read(store.directory().join("manifest.json")).unwrap())
            .unwrap();
    manifest["lists"]["members"].clone()
}
fn update(list: &mut IdList, body: String) {
    list.apply_update_for_publish(IdListUpdate {
        new_metadata: list.metadata.clone(),
        raw_changeset: Some(body),
    });
}
fn additions(start: usize, n: usize) -> String {
    (start..start + n)
        .map(|i| format!("+{}\n", key(i)))
        .collect()
}
fn assert_exact(ids: &IdListIds, expected: &HashSet<String>) {
    assert_eq!(ids.len(), expected.len());
    assert_eq!(
        ids.iter().map(str::to_owned).collect::<HashSet<_>>(),
        *expected
    );
    assert!(expected.iter().all(|key| ids.contains(key)));
}

#[test]
fn exact_boundary_publishes_delta_then_base_and_recomputes_limit_after_growth() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let n = 32768;
    let limit = batch_compaction_limits(n).0;
    let initial = writer
        .publish(&lease, &input(n), &HashMap::new(), 1)
        .unwrap();
    let old_file = entry(&writer)["data_file"].clone();
    let mut staged = initial.lists["members"].clone();
    update(&mut staged, additions(1_000_000, limit));
    assert!(!staged.ids.pending().unwrap().requires_full_base);
    let edge = writer
        .publish(
            &lease,
            &HashMap::from([("members".into(), staged)]),
            &HashMap::new(),
            2,
        )
        .unwrap();
    assert_eq!(edge.lists["members"].ids.delta_len_for_test(), limit);
    assert_eq!(entry(&writer)["data_file"], old_file);
    let cold = store(&root).load().unwrap().unwrap();
    let mut staged = cold.lists["members"].clone();
    update(&mut staged, additions(1_000_000 + limit, 1));
    if let Some(pending) = staged.ids.pending() {
        assert!(pending.requires_full_base);
        assert!(staged.ids.owned_capacities_for_test().is_none());
    } else {
        // The original small-base limit equals its original scratch guard;
        // preserve that eager fallback, while larger bases keep streaming.
        assert_eq!(batch_compaction_limits(n).0, batch_compaction_limits(n).1);
        assert!(staged.ids.owned_capacities_for_test().is_some());
    }
    let grown = writer
        .publish(
            &lease,
            &HashMap::from([("members".into(), staged)]),
            &HashMap::new(),
            3,
        )
        .unwrap();
    assert!(entry(&writer).get("delta_file").is_none());
    assert_ne!(entry(&writer)["data_file"], old_file);
    assert_eq!(grown.lists["members"].ids.len(), n + limit + 1);
    let next_limit = batch_compaction_limits(n + limit + 1).0;
    assert!(next_limit > limit + 1);
    let mut staged = grown.lists["members"].clone();
    update(&mut staged, additions(2_000_000, next_limit));
    assert_eq!(staged.ids.pending().unwrap().changes.len(), next_limit);
    assert!(!staged.ids.pending().unwrap().requires_full_base);
    let next = writer
        .publish(
            &lease,
            &HashMap::from([("members".into(), staged)]),
            &HashMap::new(),
            4,
        )
        .unwrap();
    assert_eq!(next.lists["members"].ids.delta_len_for_test(), next_limit);
    assert_eq!(
        next.lists["members"].metadata.size,
        ((limit + 1 + next_limit) * 10) as u64
    );
    assert_eq!(initial.lists["members"].ids.len(), n);
    assert!(!initial.lists["members"].ids.contains(&key(1_000_000)));
}

#[test]
fn eight_nonrestoring_steps_really_compact_at_expected_boundaries_and_keep_pins() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let n = 1_100_800; // Large enough for the monotonic extension to exceed the old cap.
    let width = n / 100;
    let mut expected = (0..n).map(key).collect::<HashSet<_>>();
    let initial = writer
        .publish(&lease, &input(n), &HashMap::new(), 1)
        .unwrap();
    let initial_ids = Arc::clone(&initial.lists["members"].ids);
    let mut current = initial;
    let mut middle = None;
    let mut middle_expected = None;
    let mut compactions = Vec::new();
    for step in 1..=8 {
        let prior = entry(&writer)["data_file"].clone();
        let old = if step == 4 {
            store(&root).load().unwrap().unwrap().lists
        } else {
            current.lists.clone()
        };
        let mut staged = old["members"].clone();
        let mut body = additions(10_000_000 + step * width, width);
        for i in 8 + (step - 1) * width..8 + step * width {
            body.push_str(&format!("-{}\n", key(i)));
            assert!(expected.remove(&key(i)));
        }
        for i in 10_000_000 + step * width..10_000_000 + (step + 1) * width {
            assert!(expected.insert(key(i)));
        }
        update(&mut staged, body);
        assert!(
            staged.ids.owned_capacities_for_test().is_none(),
            "step{step} must have publisher scratch headroom"
        );
        current = writer
            .publish(
                &lease,
                &HashMap::from([("members".into(), staged)]),
                &HashMap::new(),
                (step + 1) as u64,
            )
            .unwrap();
        if entry(&writer)["data_file"] != prior {
            compactions.push(step);
            assert!(entry(&writer).get("delta_file").is_none());
        }
        assert_exact(&current.lists["members"].ids, &expected);
        let reopened = store(&root).load().unwrap().unwrap();
        assert_exact(&reopened.lists["members"].ids, &expected);
        assert_eq!(
            current.lists["members"].metadata.size,
            (step * width * 20) as u64
        );
        for i in 0..8 {
            assert!(current.lists["members"].ids.contains(&key(i)));
        }
        assert!(!current.lists["members"].ids.contains("ffffffff"));
        if step == 4 {
            middle = Some(Arc::clone(&current.lists["members"].ids));
            middle_expected = Some(expected.clone());
        }
    }
    assert_eq!(
        compactions,
        if BATCH_DELTA_DIVISOR == 16 {
            vec![4, 8]
        } else {
            vec![7]
        }
    );
    assert_exact(&initial_ids, &(0..n).map(key).collect());
    assert_exact(middle.as_ref().unwrap(), middle_expected.as_ref().unwrap());
    println!(
        "policy_compaction_proof divisor={BATCH_DELTA_DIVISOR} base={n} width={width} steps={compactions:?}"
    );
}

#[test]
fn ordinary_private_path_keeps_the_65536_cap_independently_of_publisher_policy() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let initial = writer
        .publish(&lease, &input(600_000), &HashMap::new(), 1)
        .unwrap();
    let mut private = initial.lists["members"].clone();
    let mut publisher = private.clone();
    assert_eq!(batch_compaction_limits(600_000).0, 65_536);
    let body = additions(1_000_000, 65_537);
    private.apply_update(IdListUpdate {
        new_metadata: private.metadata.clone(),
        raw_changeset: Some(body.clone()),
    });
    update(&mut publisher, body);
    assert!(private.ids.owned_capacities_for_test().is_some());
    assert!(publisher.ids.owned_capacities_for_test().is_none());
    assert_eq!(
        publisher.ids.pending().unwrap().requires_full_base,
        BATCH_DELTA_DIVISOR == 16
    );
    assert_eq!(*private.ids, *publisher.ids);
}

#[test]
fn tiny_floor_dense_growth_falls_back_and_initial_pin_stays_exact() {
    for n in [0, 1, 512] {
        let root = tempfile::tempdir().unwrap();
        let writer = store(&root);
        let lease = writer.try_acquire_lease().unwrap().unwrap();
        let first = writer
            .publish(&lease, &input(n), &HashMap::new(), 1)
            .unwrap();
        let mut next = first.lists["members"].clone();
        update(&mut next, additions(1_000_000, 1025));
        assert!(next.ids.owned_capacities_for_test().is_some());
        let committed = writer
            .publish(
                &lease,
                &HashMap::from([("members".into(), next)]),
                &HashMap::new(),
                2,
            )
            .unwrap();
        assert_eq!(committed.lists["members"].ids.len(), n + 1025);
        assert!(entry(&writer).get("delta_file").is_none());
        assert_eq!(first.lists["members"].ids.len(), n);
        assert!(!first.lists["members"].ids.contains(&key(1_000_000)));
    }
}

#[test]
fn mixed_long_keys_have_exact_images_and_expose_count_policy_byte_cost() {
    let n = 20480;
    let d = batch_compaction_limits(n).0;
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let initial = writer
        .publish(&lease, &input(n), &HashMap::new(), 1)
        .unwrap();
    let mut next = initial.lists["members"].clone();
    let mut expected = (0..n).map(key).collect::<HashSet<_>>();
    let mut body = String::new();
    let (mut ni, mut no, mut blob) = (0usize, 0usize, 0usize);
    for i in 0..d {
        let value = if i.is_multiple_of(3) {
            ni += 1;
            key(1_000_000 + i)
        } else {
            no += 1;
            let prefix = format!("🦀{i:08x}");
            let length = if i.is_multiple_of(2) { 128 } else { 4096 };
            let value = format!("{prefix}{}", "x".repeat(length - prefix.len()));
            blob += value.len();
            value
        };
        body.push_str(&format!("+{value}\n"));
        expected.insert(value);
    }
    update(&mut next, body);
    assert!(!next.ids.pending().unwrap().requires_full_base);
    let committed = writer
        .publish(
            &lease,
            &HashMap::from([("members".into(), next)]),
            &HashMap::new(),
            2,
        )
        .unwrap();
    let delta_file = entry(&writer)["delta_file"].as_str().unwrap().to_owned();
    let actual = fs::metadata(writer.directory().join(delta_file))
        .unwrap()
        .len() as usize;
    let ci = (4 * ni).div_ceil(3).div_ceil(16) * 16;
    let co = (8 * no).div_ceil(5).div_ceil(16) * 16;
    let predicted = 72
        + 128
        + 9 * ci
        + 17 * co
        + 16 * usize::from(ci > 0)
        + 16 * usize::from(co > 0)
        + blob
        + (ci + co).div_ceil(8);
    assert_eq!(actual, predicted);
    assert_exact(&committed.lists["members"].ids, &expected);
    assert_exact(
        &store(&root).load().unwrap().unwrap().lists["members"].ids,
        &expected,
    );
    assert!(actual > initial.lists["members"].ids.mapped_bytes());
    println!(
        "policy_long_keys divisor={BATCH_DELTA_DIVISOR} base_members={n} delta_members={d} inline={ni} other={no} blob_bytes={blob} actual_delta_bytes={actual} base_bytes={}",
        initial.lists["members"].ids.mapped_bytes()
    );
}
