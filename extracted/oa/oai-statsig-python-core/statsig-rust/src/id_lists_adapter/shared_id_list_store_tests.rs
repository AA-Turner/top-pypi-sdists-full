use std::collections::{HashMap, HashSet};
use std::fs;
use std::io;
use std::sync::{Arc, Barrier};

use super::shared_id_list_format::{
    HEADER_LEN, HashTableSizing, IdListImage, digest, stable_hash, write_list,
    write_list_with_sizing,
};
use super::{
    IdList, IdListIds, IdListMetadata, IdListPropagationUpdate, IdListUpdate, SharedIdListStore,
};

fn list(name: &str, ids: &[&str], cursor: u64) -> IdList {
    IdList {
        metadata: IdListMetadata {
            name: name.to_owned(),
            url: "https://example.com/list".to_owned(),
            file_id: Some("file-1".to_owned()),
            size: cursor,
            creation_time: 1,
        },
        ids: Arc::new(ids.iter().map(|value| (*value).to_owned()).collect()),
    }
}

fn store(root: &tempfile::TempDir) -> SharedIdListStore {
    SharedIdListStore::new(root.path(), "secret-fixture", "source-fixture", false).unwrap()
}

fn files(store: &SharedIdListStore) -> HashSet<String> {
    fs::read_dir(store.directory())
        .unwrap()
        .map(|entry| entry.unwrap().file_name().to_string_lossy().into_owned())
        .filter(|name| name.ends_with(".ids"))
        .collect()
}

fn manifest(store: &SharedIdListStore) -> serde_json::Value {
    serde_json::from_slice(&fs::read(store.directory().join("manifest.json")).unwrap()).unwrap()
}

#[test]
fn publisher_and_readers_release_owned_inputs_without_retaining_build_seeds() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let values = ["abcdefgh", "", "nul\0", "éééé"];
    let expected = values
        .map(str::to_owned)
        .into_iter()
        .collect::<HashSet<_>>();
    let lists = HashMap::from([
        (
            "alpha".to_owned(),
            list("alpha", &["11111111", "22222222", "alpha", "🦀🦀"], 9),
        ),
        ("zeta".to_owned(), list("zeta", &values, 9)),
        ("tiny".to_owned(), list("tiny", &["tiny"], 9)),
        ("empty".to_owned(), list("empty", &[], 0)),
    ]);
    let owned_inputs = lists
        .values()
        .map(|list| Arc::downgrade(&list.ids))
        .collect::<Vec<_>>();
    let catalog = writer
        .publish(&lease, &lists, &HashMap::new(), 100)
        .unwrap();
    for (name, published) in &catalog.lists {
        assert!(published.ids.is_mapped());
        assert_eq!(*published.ids, *lists[name].ids);
        assert!(IdListIds::owned_build_seed(&published.ids).is_none());
    }
    drop(lists);
    assert!(owned_inputs.iter().all(|input| input.upgrade().is_none()));
    let follower = store(&root).load().unwrap().unwrap();
    for published in follower.lists.values() {
        assert!(published.ids.is_mapped());
        assert!(IdListIds::owned_build_seed(&published.ids).is_none());
    }
    let mut live_copy = catalog.lists["zeta"].clone();
    assert!(Arc::make_mut(&mut live_copy.ids).remove(""));
    assert!(Arc::make_mut(&mut live_copy.ids).insert_str("live-addition"));
    let mut changed = expected.clone();
    changed.remove("");
    changed.insert("live-addition".to_owned());
    assert_membership(&live_copy.ids, &changed);
    assert_membership(&catalog.lists["zeta"].ids, &expected);
    assert_eq!(live_copy.ids.delta_len_for_test(), 2);
    assert!(live_copy.ids.owned_capacities_for_test().is_none());
    assert!(!live_copy.ids.is_mapped());
    assert!(live_copy.ids.mapped_bytes() > 0);
    drop(lease);
    // Ordinary mutations remain a private pending delta over the old mapping;
    // lease lifetime neither owns an input set nor changes those semantics.
    let mut after_lease = catalog.lists["zeta"].clone();
    Arc::make_mut(&mut after_lease.ids).remove("");
    Arc::make_mut(&mut after_lease.ids).insert_str("live-addition");
    assert_membership(&after_lease.ids, &changed);
    assert_membership(&catalog.lists["zeta"].ids, &expected);
    assert_membership(&follower.lists["zeta"].ids, &expected);
}

#[test]
fn replacement_and_removal_release_private_sources_but_preserve_pinned_generations() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let initial = HashMap::from([(
        "members".to_owned(),
        list("members", &["version1", "fallback", "éééé"], 9),
    )]);
    let first_source = Arc::downgrade(&initial["members"].ids);
    let first = writer
        .publish(&lease, &initial, &HashMap::new(), 100)
        .unwrap();
    drop(initial);
    assert!(first_source.upgrade().is_none());
    let mut changed = first.lists["members"].clone();
    Arc::make_mut(&mut changed.ids).remove("version1");
    Arc::make_mut(&mut changed.ids).insert_str("version2");
    let changed_source = Arc::downgrade(&changed.ids);
    let next = HashMap::from([("members".to_owned(), changed)]);
    let second = writer.publish(&lease, &next, &HashMap::new(), 200).unwrap();
    drop(next);
    assert!(changed_source.upgrade().is_none());
    assert!(IdListIds::owned_build_seed(&second.lists["members"].ids).is_none());
    assert!(first.lists["members"].ids.contains("version1"));
    assert!(!first.lists["members"].ids.contains("version2"));
    assert!(second.lists["members"].ids.contains("version2"));
    let mut stale_copy = first.lists["members"].clone();
    Arc::make_mut(&mut stale_copy.ids).insert_str("stale-addition");
    assert!(stale_copy.ids.contains("version1"));
    assert!(!stale_copy.ids.contains("version2"));
    assert!(!first.lists["members"].ids.contains("stale-addition"));
    writer
        .publish(&lease, &HashMap::new(), &HashMap::new(), 300)
        .unwrap();
    assert!(files(&writer).is_empty());
    assert!(store(&root).load().unwrap().unwrap().lists.is_empty());
    assert!(first.lists["members"].ids.contains("version1"));
    assert!(second.lists["members"].ids.contains("version2"));
}

#[test]
fn replacement_publisher_resumes_committed_cursor_and_sparse_delta_without_a_seed() {
    let root = tempfile::tempdir().unwrap();
    let first_writer = store(&root);
    let first_lease = first_writer.try_acquire_lease().unwrap().unwrap();
    let initial = HashMap::from([(
        "members".to_owned(),
        list("members", &["old00000", "fallback-value", "éééé"], 100),
    )]);
    let old_source = Arc::downgrade(&initial["members"].ids);
    let pinned = first_writer
        .publish(&first_lease, &initial, &HashMap::new(), 100)
        .unwrap();
    let base_file = manifest(&first_writer)["lists"]["members"]["data_file"].clone();
    drop(initial);
    assert!(old_source.upgrade().is_none());
    let replacement = store(&root);
    let baseline = replacement.load().unwrap().unwrap();
    assert!(replacement.try_acquire_lease().unwrap().is_none());
    drop(first_lease);
    let replacement_lease = replacement.try_acquire_lease().unwrap().unwrap();
    let heartbeat = replacement
        .publish(&replacement_lease, &baseline.lists, &HashMap::new(), 200)
        .unwrap();
    assert_eq!(heartbeat.lists["members"].metadata.size, 100);
    let body = "-old00000\n+new00000\n";
    let mut changed = heartbeat.lists["members"].clone();
    changed.apply_update(IdListUpdate {
        new_metadata: changed.metadata.clone(),
        raw_changeset: Some(body.to_owned()),
    });
    assert_eq!(changed.ids.delta_len_for_test(), 2);
    assert!(changed.ids.owned_capacities_for_test().is_none());
    let changed_source = Arc::downgrade(&changed.ids);
    let next = HashMap::from([("members".to_owned(), changed)]);
    let committed = replacement
        .publish(&replacement_lease, &next, &HashMap::new(), 300)
        .unwrap();
    drop(next);
    assert!(changed_source.upgrade().is_none());
    assert!(IdListIds::owned_build_seed(&committed.lists["members"].ids).is_none());
    assert_eq!(
        committed.lists["members"].metadata.size,
        100 + body.len() as u64
    );
    assert_eq!(
        manifest(&replacement)["lists"]["members"]["data_file"],
        base_file
    );
    assert_membership(
        &committed.lists["members"].ids,
        &["new00000", "fallback-value", "éééé"]
            .map(str::to_owned)
            .into_iter()
            .collect(),
    );
    assert!(pinned.lists["members"].ids.contains("old00000"));
    assert!(!pinned.lists["members"].ids.contains("new00000"));
    assert!(baseline.lists["members"].ids.contains("old00000"));
    drop(replacement_lease);
    assert!(committed.lists["members"].ids.contains("new00000"));
}

#[test]
fn removal_only_compaction_shrinks_current_mapping_without_retaining_owned_capacity() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let original = (0..2048)
        .map(|index| format!("{index:08x}"))
        .chain((0..512).map(|index| format!("fallback-{index:04x}")))
        .collect::<HashSet<_>>();
    let mut members = list("members", &[], 100);
    members.ids = Arc::new(original.iter().cloned().collect());
    let original_source = Arc::downgrade(&members.ids);
    let mut owned_control = (*members.ids).clone();
    let initial = HashMap::from([("members".to_owned(), members)]);
    let pinned = writer
        .publish(&lease, &initial, &HashMap::new(), 100)
        .unwrap();
    drop(initial);
    assert!(original_source.upgrade().is_none());
    let original_mapping_bytes = pinned.lists["members"].ids.mapped_bytes();
    let removals = (17..2048)
        .map(|index| format!("{index:08x}"))
        .chain((9..512).map(|index| format!("fallback-{index:04x}")))
        .collect::<Vec<_>>();
    let mut expected = original.clone();
    let mut body = String::new();
    for value in &removals {
        assert!(owned_control.remove(value));
        assert!(expected.remove(value));
        body.push('-');
        body.push_str(value);
        body.push('\n');
    }
    let mut changed = pinned.lists["members"].clone();
    changed.apply_update(IdListUpdate {
        new_metadata: changed.metadata.clone(),
        raw_changeset: Some(body),
    });
    assert_membership(&changed.ids, &expected);
    assert_eq!(*changed.ids, owned_control);
    assert!(
        changed.ids.owned_capacities_for_test().is_some(),
        "the delta threshold materializes once during this large removal batch"
    );
    let changed_source = Arc::downgrade(&changed.ids);
    let next = HashMap::from([("members".to_owned(), changed)]);
    let committed = writer.publish(&lease, &next, &HashMap::new(), 200).unwrap();
    drop(next);
    assert!(changed_source.upgrade().is_none());
    assert!(IdListIds::owned_build_seed(&committed.lists["members"].ids).is_none());
    let entry = manifest(&writer)["lists"]["members"].clone();
    assert!(entry.get("delta_file").is_none());
    let image = fs::read(
        writer
            .directory()
            .join(entry["data_file"].as_str().unwrap()),
    )
    .unwrap();
    assert_eq!((image_u64(&image, 80), image_u64(&image, 88)), (17, 9));
    assert_eq!((image_u64(&image, 104), image_u64(&image, 112)), (32, 16));
    assert!(committed.lists["members"].ids.mapped_bytes() < original_mapping_bytes);
    assert_membership(&pinned.lists["members"].ids, &original);
    assert_membership(&committed.lists["members"].ids, &expected);
    assert_eq!(files(&writer).len(), 1);
}

#[test]
fn failed_publication_preserves_committed_view_and_cursor_without_retaining_private_sources() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let initial = HashMap::from([("members".to_owned(), list("members", &["version1"], 9))]);
    let committed_source = Arc::downgrade(&initial["members"].ids);
    let pinned = writer
        .publish(&lease, &initial, &HashMap::new(), 100)
        .unwrap();
    drop(initial);
    assert!(committed_source.upgrade().is_none());
    let previous_manifest = fs::read(writer.directory().join("manifest.json")).unwrap();
    let next_list = list("members", &["version2", "candidate-extra"], 18);
    let candidate_source = Arc::downgrade(&next_list.ids);
    let namespace = digest(&serde_json::to_vec(&("secret-fixture", "source-fixture")).unwrap());
    let mut temporary = tempfile::tempfile().unwrap();
    let hash = write_list(&mut temporary, &namespace, "members", &next_list.ids).unwrap();
    let orphan = writer.directory().join(format!("list-{hash}.ids"));
    fs::write(&orphan, b"incomplete").unwrap();
    let next = HashMap::from([("members".to_owned(), next_list)]);
    assert!(writer.publish(&lease, &next, &HashMap::new(), 200).is_err());
    drop(next);
    assert!(candidate_source.upgrade().is_none());
    assert_eq!(
        fs::read(writer.directory().join("manifest.json")).unwrap(),
        previous_manifest
    );
    let still_committed = store(&root).load().unwrap().unwrap();
    assert_eq!(still_committed.status.successful_refresh_ms, 100);
    assert_eq!(still_committed.lists["members"].metadata.size, 9);
    assert!(still_committed.lists["members"].ids.contains("version1"));
    assert!(!pinned.lists["members"].ids.contains("version2"));
    fs::remove_file(orphan).unwrap();
    let retry = HashMap::from([(
        "members".to_owned(),
        list("members", &["version2", "candidate-extra"], 18),
    )]);
    let committed = writer
        .publish(&lease, &retry, &HashMap::new(), 200)
        .unwrap();
    assert_eq!(committed.lists["members"].metadata.size, 18);
    assert!(committed.lists["members"].ids.contains("version2"));
    drop(lease);
    assert!(pinned.lists["members"].ids.contains("version1"));
}

fn mapped_ids(ids: &IdListIds) -> IdListIds {
    let namespace = digest(b"round-trip-fixture");
    let mut file = tempfile::NamedTempFile::new().unwrap();
    write_list(file.as_file_mut(), &namespace, "members", ids).unwrap();
    let mapped = IdListImage::open(file.path(), &namespace, "members").unwrap();
    mapped.validate_membership().unwrap();
    IdListIds::from_image(mapped)
}

fn assert_membership(ids: &IdListIds, expected: &HashSet<String>) {
    assert_eq!(ids.len(), expected.len());
    assert_eq!(
        ids.iter().collect::<HashSet<_>>(),
        expected.iter().map(String::as_str).collect::<HashSet<_>>()
    );
    assert_eq!(ids.iter().count(), expected.len());
    for value in expected {
        assert!(ids.contains(value), "missing {value:?}");
    }
}

fn image_u64(bytes: &[u8], offset: usize) -> usize {
    u64::from_le_bytes(bytes[offset..offset + 8].try_into().unwrap()) as usize
}

fn assert_invalid_image(bytes: &[u8], namespace: &[u8; 32]) {
    let file = tempfile::NamedTempFile::new().unwrap();
    fs::write(file.path(), bytes).unwrap();
    assert_eq!(
        IdListImage::open(file.path(), namespace, "members")
            .err()
            .unwrap()
            .kind(),
        io::ErrorKind::InvalidData
    );
}

fn assert_invalid_membership(bytes: &[u8], namespace: &[u8; 32]) {
    let file = tempfile::NamedTempFile::new().unwrap();
    fs::write(file.path(), bytes).unwrap();
    let mapped = IdListImage::open(file.path(), namespace, "members").unwrap();
    assert_eq!(
        mapped.validate_membership().unwrap_err().kind(),
        io::ErrorKind::InvalidData
    );
}

fn duplicate_inline_key(image: &mut [u8]) {
    let capacity = image_u64(image, 104);
    let slots = HEADER_LEN + capacity + 16;
    let occupied = (0..capacity)
        .filter(|slot| image[HEADER_LEN + slot] != 0x80)
        .take(2)
        .collect::<Vec<_>>();
    assert_eq!(occupied.len(), 2);
    let key: [u8; 8] = image[slots + occupied[0] * 8..slots + (occupied[0] + 1) * 8]
        .try_into()
        .unwrap();
    image[slots + occupied[1] * 8..slots + (occupied[1] + 1) * 8].copy_from_slice(&key);
    let control = image[HEADER_LEN + occupied[0]];
    image[HEADER_LEN + occupied[1]] = control;
    if occupied[1] < 16 {
        image[HEADER_LEN + capacity + occupied[1]] = control;
    }
}

#[test]
fn mapped_keys_preserve_exact_bytes_including_nul_and_multibyte_boundaries() {
    let values = [
        "".to_owned(),
        "\0".to_owned(),
        "\0\0\0\0\0\0\0\0".to_owned(),
        "abc\0defg".to_owned(),
        "abc\0defgh".to_owned(),
        "abcdefgh".to_owned(),
        "ABCDEFGH".to_owned(),
        "éééé".to_owned(),
        "🦀🦀".to_owned(),
        "éééa".to_owned(),
        "éééabc".to_owned(),
        "e\u{301}e\u{301}e\u{301}".to_owned(),
        "\n\t \r".to_owned(),
        "界".repeat(21_847),
    ];
    let expected = values.iter().cloned().collect::<HashSet<_>>();
    let owned = values
        .iter()
        .cycle()
        .take(values.len() * 5)
        .cloned()
        .collect();
    let mapped = mapped_ids(&owned);
    assert_membership(&mapped, &expected);
    for absent in ["abc", "abc\0def", "abcdefgh\0", "ééé", "ééééé", "🦀"] {
        assert!(!mapped.contains(absent), "unexpected {absent:?}");
    }
    let mut changed = mapped.clone();
    assert!(changed.remove(""));
    assert!(changed.remove("abc\0defg"));
    assert!(changed.insert_str("new\0key"));
    assert!(!changed.insert_str("new\0key"));
    assert!(!changed.is_mapped());
    assert_membership(&mapped, &expected);
    let mut expected_changed = expected;
    expected_changed.remove("");
    expected_changed.remove("abc\0defg");
    expected_changed.insert("new\0key".to_owned());
    assert_membership(&mapped_ids(&changed), &expected_changed);
}

#[test]
fn mapped_rounding_boundaries_use_current_unique_cardinality() {
    // Cover both power-of-two boundaries and 7/8-full table boundaries. The
    // writer chooses capacity; expected membership is independent of its layout.
    for count in [
        0, 1, 2, 13, 14, 15, 16, 17, 27, 28, 29, 31, 32, 33, 55, 56, 57, 63, 64, 65, 111, 112, 113,
        127, 128, 129, 255, 256, 257, 511, 512, 513, 1023, 1024, 1025, 4095, 4096, 4097,
    ] {
        for fallback in [false, true] {
            let values = (0..count)
                .map(|index| {
                    if fallback {
                        format!("member-{index:08x}-é")
                    } else {
                        format!("{index:08x}")
                    }
                })
                .collect::<Vec<_>>();
            let expected = values.iter().cloned().collect::<HashSet<_>>();
            let unique = values.iter().cloned().collect::<IdListIds>();
            let mut repeated = values
                .iter()
                .cycle()
                .take(count * 3)
                .cloned()
                .collect::<IdListIds>();
            // Removed values must not leave oversized on-disk capacity behind.
            for index in 0..65 {
                repeated.insert(format!("removed-{index}"));
            }
            for index in 0..65 {
                assert!(repeated.remove(&format!("removed-{index}")));
            }
            let mapped = mapped_ids(&repeated);
            let unique_mapped = mapped_ids(&unique);
            assert_membership(&mapped, &expected);
            assert_eq!(mapped.mapped_bytes(), unique_mapped.mapped_bytes());
            assert!(!mapped.contains("ffffffff"));
            assert!(!mapped.contains("member-ffffffff-é"));
        }
    }
}

#[test]
fn default_writer_sizes_unique_inline_and_fallback_partitions_independently() {
    let namespace = digest(b"default-sizing-fixture");
    // The default writer targets 3/4 occupancy for inline keys and 5/8 for
    // fallback keys, rounding each nonempty partition to groups of 16 slots.
    for (inline_count, other_count, inline_capacity, other_capacity) in [
        (24, 17, 32, 32),
        (12, 9, 16, 16),
        (24, 21, 32, 48),
        (0, 17, 0, 32),
        (24, 0, 32, 0),
        (0, 0, 0, 0),
    ] {
        let values = (0..inline_count)
            .map(|index| format!("{index:08x}"))
            .chain((0..other_count).map(|index| format!("fallback-{index}")))
            .collect::<Vec<_>>();
        let expected = values.iter().cloned().collect::<HashSet<_>>();
        let ids = values
            .iter()
            .cycle()
            .take(values.len() * 3)
            .cloned()
            .collect();
        let mut file = tempfile::NamedTempFile::new().unwrap();
        write_list(file.as_file_mut(), &namespace, "members", &ids).unwrap();
        let image = fs::read(file.path()).unwrap();
        assert_eq!(image_u64(&image, 80), inline_count);
        assert_eq!(image_u64(&image, 88), other_count);
        assert_eq!(image_u64(&image, 104), inline_capacity);
        assert_eq!(image_u64(&image, 112), other_capacity);
        let mapped =
            IdListIds::from_image(IdListImage::open(file.path(), &namespace, "members").unwrap());
        assert_membership(&mapped, &expected);
    }
}

#[test]
fn real_hash_collisions_probe_across_groups_and_wraparound() {
    let namespace = digest(b"collision-fixture");
    for power_of_two in [false, true] {
        let sizing = HashTableSizing {
            numerator: 7,
            denominator: 8,
            power_of_two,
        };
        for key_length in [8, 20, 128] {
            let fallback = key_length != 8;
            let capacity = sizing.capacity(40).unwrap();
            let home = capacity - 1;
            // Find real keys with identical initial slots AND fingerprints.
            // Forty entries force three probe groups, starting at the final
            // slot so the first group also crosses the mirrored control suffix.
            let colliding = (0u32..2_000_000)
                .map(|index| {
                    if key_length == 128 {
                        format!("{index:08x}{}", "a".repeat(120))
                    } else if fallback {
                        format!("fallback-{index:08x}-é")
                    } else {
                        format!("{index:08x}")
                    }
                })
                .filter(|value| {
                    let hash = stable_hash(value.as_bytes());
                    if fallback {
                        ((hash as u128 * capacity as u128) >> 64) == home as u128
                            && hash & 0x7f == 0
                    } else {
                        hash % capacity as u64 == home as u64 && hash >> 57 == 0
                    }
                })
                .take(41)
                .collect::<Vec<_>>();
            assert_eq!(colliding.len(), 41, "collision fixture search exhausted");
            let expected = colliding[..40].iter().cloned().collect::<HashSet<_>>();
            let ids = expected.iter().cloned().collect();
            let mut file = tempfile::NamedTempFile::new().unwrap();
            write_list_with_sizing(file.as_file_mut(), &namespace, "members", &ids, sizing)
                .unwrap();
            let mapped = IdListIds::from_image(
                IdListImage::open(file.path(), &namespace, "members").unwrap(),
            );
            assert_membership(&mapped, &expected);
            assert!(!mapped.contains(&colliding[40]));
            assert!(!mapped.contains("different-missing-key"));

            let mut broken_chain = fs::read(file.path()).unwrap();
            let count_offset = if fallback { 88 } else { 80 };
            let capacity_offset = if fallback { 112 } else { 104 };
            assert_eq!(image_u64(&broken_chain, capacity_offset), capacity);
            // Each fixture has only one nonempty partition. Removing an
            // early probe entry while leaving later groups populated must be
            // rejected before publication, rather than silently losing members.
            assert_eq!(broken_chain[HEADER_LEN + home], 0);
            broken_chain[HEADER_LEN + home] = 0x80;
            broken_chain[count_offset..count_offset + 8].copy_from_slice(&39u64.to_le_bytes());
            assert_invalid_membership(&broken_chain, &namespace);
        }
    }
}

#[test]
fn hash_algorithm_two_matches_fixed_format_vectors() {
    // Independent known answers pin algorithm two across architectures and
    // future SDK versions; changing these requires a format/hash version bump.
    for (value, expected) in [
        ("", 0x4821_8226_ff3c_d4bfu64),
        ("abcdefgh", 0xc201_8f56_afc8_c8d3),
        ("\0\0\0\0\0\0\0\0", 0xe220_a839_7b1d_cdaf),
        ("éééé", 0xae33_ca82_4b6f_7598),
        ("a\0b", 0xc45f_aefe_6ccb_31aa),
        ("arbitrary-long-字符串", 0x01a8_e9fe_6451_2c7c),
    ] {
        assert_eq!(stable_hash(value.as_bytes()), expected, "{value:?}");
    }
    for (length, expected) in [
        (31, 0x3c3a_6770_4646_196du64),
        (32, 0x2fcc_c5bc_4364_cae4),
        (33, 0x6109_0c45_9b16_c0ed),
        (63, 0x19fb_eaf0_89e3_c5b9),
        (64, 0xef40_a46f_2e98_0262),
        (65, 0xfd7e_5ca0_5754_2dfe),
        (128, 0x339e_44d8_470e_9237),
        (1024, 0x4959_f9ac_4105_8c20),
    ] {
        assert_eq!(stable_hash("a".repeat(length).as_bytes()), expected);
    }
    for (length, expected) in [
        (32, 0xaa5f_4a57_b710_6cfeu64),
        (64, 0x7850_0f45_4f67_8ef1),
        (128, 0x1f21_2484_8938_2e05),
        (1024, 0xb9f4_677d_3829_5420),
    ] {
        assert_eq!(
            stable_hash("0123456789abcdef".repeat(length / 16).as_bytes()),
            expected
        );
    }
    for (length, expected) in [
        (32, 0xf59e_5500_fcd9_5251u64),
        (64, 0xcbb4_6143_7844_ccb6),
        (1024, 0x28e5_b7fb_451d_ea82),
    ] {
        assert_eq!(stable_hash(&vec![0; length]), expected);
    }
    // Known answers also verified against the measured SDK's ALG2 images.
    for (value, expected) in [
        (
            format!("{}xiCDSkSsk", "λ".repeat(12)),
            0x9b57_3196_b75b_4efa,
        ),
        (
            format!("{}xi2YW7m9Y", "λ".repeat(27)),
            0x4c7c_6e4a_f18f_d369,
        ),
        (
            format!("{}x7tlvUo1E", "λ".repeat(27)),
            0x91fd_5ad5_b88d_a134,
        ),
        (
            format!("{}iCDSkSsk", "λ".repeat(508)),
            0x505c_4da0_efc3_273b,
        ),
    ] {
        assert_eq!(stable_hash(value.as_bytes()), expected);
    }
}

#[test]
fn hash_matches_independent_padded_word_reference() {
    // A simple padded-word reference verifies optimized loads and lane handling.
    // Short-key outputs are unchanged; keys >= 32 use the selected parallel
    // residual algorithm, whose outputs the fixed vectors independently pin.
    fn reference_hash(bytes: &[u8]) -> u64 {
        fn mix(mut value: u64) -> u64 {
            value = (value ^ (value >> 30)).wrapping_mul(0xbf58_476d_1ce4_e5b9);
            value = (value ^ (value >> 27)).wrapping_mul(0x94d0_49bb_1331_11eb);
            value ^ (value >> 31)
        }
        fn word(bytes: &[u8]) -> u64 {
            u64::from_le_bytes(bytes.try_into().unwrap())
        }
        const SEED: u64 = 0x9e37_79b9_7f4a_7c15;
        if bytes.len() == 8 {
            return mix(word(bytes) ^ SEED);
        }
        let mut hash = bytes.len() as u64 ^ SEED;
        if bytes.len() < 32 {
            hash = mix(hash);
            let mut chunks = bytes.chunks_exact(8);
            for chunk in &mut chunks {
                hash = mix(hash ^ word(chunk));
            }
            let mut tail = [0; 8];
            tail[..chunks.remainder().len()].copy_from_slice(chunks.remainder());
            return mix(hash ^ u64::from_le_bytes(tail));
        }
        let mut lanes = [
            hash,
            hash ^ 0xbf58_476d_1ce4_e5b9,
            hash ^ 0x94d0_49bb_1331_11eb,
            hash ^ 0xd6e8_feb8_6659_fd93,
        ];
        let mut chunks = bytes.chunks_exact(8);
        for (index, chunk) in chunks.by_ref().enumerate() {
            lanes[index % 4] = mix(lanes[index % 4] ^ word(chunk));
        }
        let tail_hash = if chunks.remainder().is_empty() {
            0
        } else {
            let mut padded = [0; 8];
            padded[..chunks.remainder().len()].copy_from_slice(chunks.remainder());
            mix(hash ^ u64::from_le_bytes(padded) ^ 0xd6e8_feb8_6659_fd93)
        };
        mix(hash
            ^ lanes[0]
            ^ lanes[1].rotate_left(13)
            ^ lanes[2].rotate_left(29)
            ^ lanes[3].rotate_left(47)
            ^ tail_hash.rotate_left(37))
    }

    // Exercise every one-to-seven-byte tail, including inputs too short to
    // load a word and tails following complete words or four-lane stripes.
    for length in (0..=160).chain(1024..=1031).chain(4096..=4103) {
        let patterns = [
            vec![0; length],
            vec![b'a'; length],
            (0..length)
                .map(|index| ((index * 37 + length * 11) % 128) as u8)
                .collect(),
        ];
        for (pattern, bytes) in patterns.iter().enumerate() {
            assert_eq!(
                stable_hash(bytes),
                reference_hash(bytes),
                "length={length}, pattern={pattern}"
            );
        }
    }
}

#[test]
fn patterned_long_keys_preserve_full_membership_iteration_and_copy_on_write() {
    let mut expected = HashSet::new();
    let mut absent = Vec::new();
    for length in [
        31, 32, 33, 63, 64, 65, 95, 96, 97, 127, 128, 129, 255, 256, 257, 1024, 1025,
    ] {
        let pattern = (0..length)
            .map(|index| b'a' + (index % 23) as u8)
            .collect::<Vec<_>>();
        expected.insert(String::from_utf8(pattern.clone()).unwrap());
        // Exercise every lane and byte tails with long common prefixes and
        // suffixes. These distinct keys must survive even if hashes collide.
        for index in [0, 7, 8, 15, 16, 23, 24, 31, length / 2, length - 1] {
            if index >= length {
                continue;
            }
            let mut changed = pattern.clone();
            changed[index] = b'Z';
            expected.insert(String::from_utf8(changed).unwrap());
        }
        let mut missing = pattern;
        missing[length / 2] = b'Y';
        absent.push(String::from_utf8(missing).unwrap());
        expected.insert("\0".repeat(length));
        expected.insert("é🙂\0".repeat(length / 7));
        expected.insert("0123456789abcdef".repeat(length / 16));
    }
    let source = expected
        .iter()
        .cycle()
        .take(expected.len() * 3)
        .cloned()
        .collect();
    let mapped = mapped_ids(&source);
    assert_membership(&mapped, &expected);
    for value in absent {
        assert!(!mapped.contains(&value));
    }
    let mut changed = mapped.clone();
    let mut expected_changed = expected.clone();
    for value in expected.iter().step_by(3) {
        assert!(changed.remove(value));
        expected_changed.remove(value);
    }
    assert_membership(&mapped, &expected);
    assert_membership(&mapped_ids(&changed), &expected_changed);
}

#[test]
fn version_one_sorted_image_is_rejected_by_hash_reader() {
    let namespace = digest(b"old-version-fixture");
    let mut image = Vec::new();
    image.extend_from_slice(b"STGIDLS\0");
    image.extend_from_slice(&1u32.to_le_bytes());
    image.extend_from_slice(&0u32.to_le_bytes());
    image.extend_from_slice(&namespace);
    image.extend_from_slice(&digest(b"members"));
    for value in [3u64, 0, 0] {
        image.extend_from_slice(&value.to_le_bytes());
    }
    for value in [b"aaaaaaaa", b"bbbbbbbb", b"cccccccc"] {
        image.extend_from_slice(value);
    }
    image.extend_from_slice(&0u64.to_le_bytes());
    assert_invalid_image(&image, &namespace);
}

#[test]
fn canonical_image_does_not_depend_on_owned_set_insertion_order() {
    let namespace = digest(b"canonical-fixture");
    let values = (0..257)
        .flat_map(|index| [format!("{index:08x}"), format!("fallback-{index}-é")])
        .chain([String::new(), "\0".to_owned()])
        .collect::<Vec<_>>();
    let mut first = tempfile::NamedTempFile::new().unwrap();
    let mut second = tempfile::NamedTempFile::new().unwrap();
    let first_digest = write_list(
        first.as_file_mut(),
        &namespace,
        "members",
        &values.iter().cloned().collect(),
    )
    .unwrap();
    let second_digest = write_list(
        second.as_file_mut(),
        &namespace,
        "members",
        &values
            .iter()
            .rev()
            .cycle()
            .take(values.len() * 3)
            .cloned()
            .collect(),
    )
    .unwrap();
    assert_eq!(first_digest, second_digest);
    assert_eq!(
        fs::read(first.path()).unwrap(),
        fs::read(second.path()).unwrap()
    );
}

#[test]
fn mapped_membership_is_exact_and_copy_on_write_preserves_snapshots() {
    let root = tempfile::tempdir().unwrap();
    let store = store(&root);
    let lease = store.try_acquire_lease().unwrap().unwrap();
    let values = [
        "AbCd1234",
        "abcd1234",
        "",
        "short",
        "longer-than-eight",
        "éééé",
        "🦀🦀",
        "é",
    ];
    let lists = HashMap::from([("members".to_owned(), list("members", &values, 123))]);
    let catalog = store.publish(&lease, &lists, &HashMap::new(), 500).unwrap();
    let old = &catalog.lists["members"];
    assert!(old.ids.is_mapped());
    assert!(old.ids.mapped_bytes() > HEADER_LEN);
    assert_eq!(*old.ids, *lists["members"].ids);
    assert_eq!(
        old.ids.iter().collect::<HashSet<_>>(),
        values.into_iter().collect::<HashSet<_>>()
    );
    for value in values {
        assert!(old.ids.contains(value));
    }
    assert!(!old.ids.contains("ABCD1234"));
    assert!(!old.ids.contains("missing"));

    let mut updated = old.clone();
    updated.apply_update(IdListUpdate {
        new_metadata: old.metadata.clone(),
        raw_changeset: Some("-AbCd1234\n-longer-than-eight\n+NewKey00\n+new-fallback\n".to_owned()),
    });
    assert!(!updated.ids.is_mapped());
    assert!(old.ids.is_mapped());
    assert!(old.ids.contains("AbCd1234"));
    assert!(old.ids.contains("longer-than-eight"));
    assert!(!old.ids.contains("NewKey00"));
    assert!(!updated.ids.contains("AbCd1234"));
    assert!(!updated.ids.contains("longer-than-eight"));
    assert!(updated.ids.contains("NewKey00"));
    assert!(updated.ids.contains("new-fallback"));
}

#[test]
fn mapped_delta_duplicates_noops_and_resets_match_owned_membership() {
    let mut current = list(
        "members",
        &["00000000", "00000001", "fallback-0", "éééé"],
        100,
    );
    current.ids = Arc::new(mapped_ids(&current.ids));
    let initial = Arc::clone(&current.ids);
    current.apply_update(IdListUpdate {
        new_metadata: current.metadata.clone(),
        raw_changeset: Some(
            "+00000000\n+00000002\n-fallback-0\n-missing\n+fallback-1\n".to_owned(),
        ),
    });
    assert!(!current.ids.is_mapped());
    assert_membership(
        &current.ids,
        &["00000000", "00000001", "00000002", "fallback-1", "éééé"]
            .map(str::to_owned)
            .into_iter()
            .collect(),
    );
    assert!(initial.contains("fallback-0"));
    assert!(!initial.contains("00000002"));
    current.ids = Arc::new(mapped_ids(&current.ids));
    let before_reset = Arc::clone(&current.ids);
    let mut replacement = current.metadata.clone();
    replacement.file_id = Some("file-2".to_owned());
    current.apply_update(IdListUpdate {
        new_metadata: replacement,
        raw_changeset: Some("+reset000\n+reset000\n+tail\n".to_owned()),
    });
    assert_membership(
        &current.ids,
        &["reset000", "tail"]
            .map(str::to_owned)
            .into_iter()
            .collect(),
    );
    assert!(!before_reset.contains("reset000"));
    current.ids = Arc::new(mapped_ids(&current.ids));
    let mut newer_epoch = current.metadata.clone();
    newer_epoch.creation_time += 1;
    current.apply_update(IdListUpdate {
        new_metadata: newer_epoch,
        raw_changeset: Some("+newera00\n".to_owned()),
    });
    current.ids = Arc::new(mapped_ids(&current.ids));
    let mut stale_epoch = current.metadata.clone();
    stale_epoch.creation_time -= 1;
    current.apply_update(IdListUpdate {
        new_metadata: stale_epoch,
        raw_changeset: Some("+stale000\n".to_owned()),
    });
    assert_membership(
        &current.ids,
        &["newera00"].map(str::to_owned).into_iter().collect(),
    );
    assert!(current.ids.is_mapped());
}

#[test]
fn empty_list_and_empty_catalog_round_trip() {
    let root = tempfile::tempdir().unwrap();
    let store = store(&root);
    assert!(store.load().unwrap().is_none());
    let lease = store.try_acquire_lease().unwrap().unwrap();
    let lists = HashMap::from([("empty".to_owned(), list("empty", &[], 0))]);
    let catalog = store.publish(&lease, &lists, &HashMap::new(), 10).unwrap();
    assert!(catalog.lists["empty"].ids.is_empty());
    assert!(!catalog.lists["empty"].ids.contains(""));
    assert_eq!(catalog.lists["empty"].ids.iter().count(), 0);
    store
        .publish(&lease, &HashMap::new(), &HashMap::new(), 20)
        .unwrap();
    assert!(store.load().unwrap().unwrap().lists.is_empty());
    assert!(files(&store).is_empty());
}

#[test]
fn heartbeat_and_cursor_updates_reuse_files_and_preserve_delivery_metadata() {
    let root = tempfile::tempdir().unwrap();
    let store = store(&root);
    let lease = store.try_acquire_lease().unwrap().unwrap();
    let mut lists = HashMap::from([("members".to_owned(), list("members", &["AbCd1234"], 90))]);
    let proof = HashMap::from([(
        "members".to_owned(),
        IdListPropagationUpdate {
            creation_time: lists["members"].metadata.creation_time,
            file_id: Some("file-1".to_owned()),
            url: "https://example.com/list".to_owned(),
            ts: Some(77),
            size: 90,
            applied_range: Some(0..90),
        },
    )]);
    let first = store.publish(&lease, &lists, &proof, 100).unwrap();
    let first_files = files(&store);
    let second = store.publish(&lease, &lists, &proof, 200).unwrap();
    assert_eq!(files(&store), first_files);
    assert_ne!(first.generation, second.generation);
    assert!(Arc::ptr_eq(
        &first.lists["members"].ids,
        &second.lists["members"].ids
    ));
    lists.get_mut("members").unwrap().metadata.size = 103;
    let cursor_update = store.publish(&lease, &lists, &proof, 300).unwrap();
    assert_ne!(cursor_update.content_digest, second.content_digest);
    let other_reader = self::store(&root);
    let loaded = other_reader.load().unwrap().unwrap();
    assert_eq!(loaded.status.successful_refresh_ms, 300);
    assert_eq!(loaded.lists["members"].metadata.size, 103);
    assert_eq!(loaded.propagation["members"].applied_range, Some(0..90));
    assert_eq!(loaded.propagation["members"].ts, Some(77));
    assert_eq!(files(&store), first_files);
}

#[test]
fn three_generations_survive_unlink_and_weak_cache_does_not_retain_them() {
    let root = tempfile::tempdir().unwrap();
    let store = store(&root);
    let lease = store.try_acquire_lease().unwrap().unwrap();
    let mut lists = HashMap::from([
        ("changing".to_owned(), list("changing", &["version1"], 9)),
        ("stable".to_owned(), list("stable", &["same-key"], 9)),
    ]);
    let first = store.publish(&lease, &lists, &HashMap::new(), 100).unwrap();
    let first_manifest = manifest(&store);
    let first_weak = Arc::downgrade(&first.lists["changing"].ids);
    lists.insert("changing".to_owned(), list("changing", &["version2"], 18));
    let second = store.publish(&lease, &lists, &HashMap::new(), 200).unwrap();
    let second_weak = Arc::downgrade(&second.lists["changing"].ids);
    lists.insert("changing".to_owned(), list("changing", &["version3"], 27));
    let third = store.publish(&lease, &lists, &HashMap::new(), 300).unwrap();
    assert!(first.lists["changing"].ids.contains("version1"));
    assert!(second.lists["changing"].ids.contains("version2"));
    assert!(third.lists["changing"].ids.contains("version3"));
    assert!(Arc::ptr_eq(
        &first.lists["stable"].ids,
        &third.lists["stable"].ids
    ));
    assert_eq!(files(&store).len(), 2);
    let old_file = first_manifest["lists"]["changing"]["data_file"]
        .as_str()
        .unwrap();
    assert!(!store.directory().join(old_file).exists());
    drop(first);
    assert!(first_weak.upgrade().is_none());
    drop(second);
    assert!(second_weak.upgrade().is_none());
}

#[test]
fn skewed_catalog_grows_and_shrinks_without_rewriting_tiny_lists() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let reader = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let mut lists = HashMap::new();
    for index in 0..96 {
        let name = format!("tiny-{index}");
        let values = (0..index % 4)
            .map(|value| format!("{value:08x}"))
            .collect::<Vec<_>>();
        let mut tiny = list(&name, &[], 10);
        tiny.ids = Arc::new(values.into_iter().collect());
        lists.insert(name, tiny);
    }
    let mut pinned = Vec::new();
    let mut expected_generations = Vec::new();
    for (generation, count) in [31, 65_537, 2, 0, 1_025].into_iter().enumerate() {
        let expected = (0..count)
            .map(|index| format!("{generation:02x}{index:06x}"))
            .collect::<HashSet<_>>();
        let mut large = list("large", &[], generation as u64);
        large.ids = Arc::new(expected.iter().cloned().collect());
        lists.insert("large".to_owned(), large);
        let published = writer
            .publish(&lease, &lists, &HashMap::new(), generation as u64)
            .unwrap();
        let loaded = reader.load().unwrap().unwrap();
        assert_eq!(loaded.lists.len(), 97);
        assert_membership(&loaded.lists["large"].ids, &expected);
        for index in 0..96 {
            let name = format!("tiny-{index}");
            assert_eq!(*loaded.lists[&name].ids, *lists[&name].ids);
            assert!(loaded.lists[&name].ids.is_mapped());
            if let Some(previous) = pinned.last() {
                let previous: &super::SharedIdListCatalog = previous;
                let old = &previous.lists[&name].ids;
                let new = &published.lists[&name].ids;
                if old.is_empty() {
                    assert!(Arc::ptr_eq(old, new));
                } else {
                    // First attaching a weak seed may copy the small wrapper,
                    // but unchanged lists must still share the same mmap bytes.
                    for value in old.iter() {
                        let current = new.iter().find(|current| *current == value).unwrap();
                        assert!(std::ptr::eq(value.as_ptr(), current.as_ptr()));
                    }
                }
            }
        }
        pinned.push(published);
        expected_generations.push(expected);
        for (catalog, expected) in pinned.iter().zip(&expected_generations) {
            assert_membership(&catalog.lists["large"].ids, expected);
        }
        assert_eq!(files(&writer).len(), 97);
    }
    assert!(
        pinned[1].lists["large"].ids.mapped_bytes() > pinned[0].lists["large"].ids.mapped_bytes()
    );
    assert!(
        pinned[2].lists["large"].ids.mapped_bytes() < pinned[1].lists["large"].ids.mapped_bytes()
    );
}

#[test]
fn concurrent_readers_keep_several_generations_pinned_during_replacement() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let counts = [15, 113, 3, 4_097, 0, 257];
    let published = Arc::new(Barrier::new(5));
    let readers_loaded = Arc::new(Barrier::new(5));
    std::thread::scope(|scope| {
        for _ in 0..4 {
            let reader = store(&root);
            let published = Arc::clone(&published);
            let readers_loaded = Arc::clone(&readers_loaded);
            scope.spawn(move || {
                let mut pinned: Vec<io::Result<Option<super::SharedIdListCatalog>>> = Vec::new();
                let mut old_views_remain_valid = true;
                for _ in counts {
                    // Old mappings remain readable while the writer publishes
                    // the next generation and unlinks their directory entries.
                    for (old_generation, old) in pinned.iter().enumerate() {
                        if let Ok(Some(old)) = old {
                            let ids = &old.lists["members"].ids;
                            old_views_remain_valid &= ids.len() == counts[old_generation]
                                && ids.iter().count() == counts[old_generation];
                            if !ids.is_empty() {
                                old_views_remain_valid &=
                                    ids.contains(&format!("{old_generation:02x}000000"));
                            }
                        }
                    }
                    published.wait();
                    pinned.push(reader.load());
                    readers_loaded.wait();
                }
                // Assert after all barriers so a failed assertion cannot strand
                // the publisher or another reader waiting at the next barrier.
                assert!(old_views_remain_valid);
                for (generation, catalog) in pinned.into_iter().enumerate() {
                    let catalog = catalog.unwrap().unwrap();
                    assert_eq!(catalog.status.successful_refresh_ms, generation as u64);
                    assert_eq!(catalog.lists["members"].metadata.size, generation as u64);
                    let ids = &catalog.lists["members"].ids;
                    assert_eq!(ids.len(), counts[generation]);
                    assert!(ids.is_mapped());
                    for index in 0..counts[generation] {
                        assert!(ids.contains(&format!("{generation:02x}{index:06x}")));
                    }
                    assert!(!ids.contains("ffffffff"));
                }
            });
        }
        for (generation, count) in counts.into_iter().enumerate() {
            let mut members = list("members", &[], generation as u64);
            members.ids = Arc::new(
                (0..count)
                    .map(|index| format!("{generation:02x}{index:06x}"))
                    .collect(),
            );
            writer
                .publish(
                    &lease,
                    &HashMap::from([("members".to_owned(), members)]),
                    &HashMap::new(),
                    generation as u64,
                )
                .unwrap();
            published.wait();
            readers_loaded.wait();
        }
    });
    assert_eq!(files(&writer).len(), 1);
}

#[test]
fn reader_retries_manifest_that_lost_its_old_files_during_commit() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let reader = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let old = HashMap::from([("members".to_owned(), list("members", &["version1"], 9))]);
    writer.publish(&lease, &old, &HashMap::new(), 100).unwrap();
    let mut changed = false;
    let loaded = reader
        .load_after_manifest_for_test(|| {
            if !changed {
                changed = true;
                let next =
                    HashMap::from([("members".to_owned(), list("members", &["version2"], 18))]);
                writer.publish(&lease, &next, &HashMap::new(), 200).unwrap();
            }
        })
        .unwrap()
        .unwrap();
    assert_eq!(loaded.status.successful_refresh_ms, 200);
    assert!(loaded.lists["members"].ids.contains("version2"));
}

#[test]
fn new_relative_root_and_absolute_root_share_the_same_lease_and_manifest() {
    let parent = tempfile::tempdir_in(".").unwrap();
    let relative = std::path::Path::new(parent.path().file_name().unwrap()).join("new-cache");
    let absolute = std::env::current_dir().unwrap().join(&relative);
    let writer = SharedIdListStore::new(&relative, "key", "source", false).unwrap();
    let reader = SharedIdListStore::new(&absolute, "key", "source", false).unwrap();
    assert_eq!(writer.directory(), reader.directory());
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    assert!(reader.try_acquire_lease().unwrap().is_none());
    reader
        .publish(&lease, &HashMap::new(), &HashMap::new(), 42)
        .unwrap();
    assert_eq!(
        writer.load().unwrap().unwrap().status.successful_refresh_ms,
        42
    );
}

#[test]
fn lease_is_exclusive_released_on_drop_and_namespaced_by_key_and_source() {
    let root = tempfile::tempdir().unwrap();
    let first = store(&root);
    let second = store(&root);
    let lease = first.try_acquire_lease().unwrap().unwrap();
    assert!(second.try_acquire_lease().unwrap().is_none());
    first.cleanup(&lease).unwrap();
    assert!(second.try_acquire_lease().unwrap().is_none());
    assert!(first.directory().join("leader.lock").exists());
    let other_key =
        SharedIdListStore::new(root.path(), "another-key", "source-fixture", false).unwrap();
    let other_source =
        SharedIdListStore::new(root.path(), "secret-fixture", "other-source", false).unwrap();
    assert_ne!(first.directory(), other_key.directory());
    assert_ne!(first.directory(), other_source.directory());
    assert!(other_key.try_acquire_lease().unwrap().is_some());
    assert!(other_source.try_acquire_lease().unwrap().is_some());
    drop(lease);
    assert!(second.try_acquire_lease().unwrap().is_some());
}

#[test]
fn failed_precommit_keeps_manifest_cursors_and_heartbeat_unchanged() {
    let root = tempfile::tempdir().unwrap();
    let store = store(&root);
    let lease = store.try_acquire_lease().unwrap().unwrap();
    let lists = HashMap::from([("members".to_owned(), list("members", &["version1"], 9))]);
    store.publish(&lease, &lists, &HashMap::new(), 100).unwrap();
    let previous = fs::read(store.directory().join("manifest.json")).unwrap();
    let next = list("members", &["version2"], 18);
    let namespace = digest(&serde_json::to_vec(&("secret-fixture", "source-fixture")).unwrap());
    let mut temporary = tempfile::tempfile().unwrap();
    let hash = write_list(&mut temporary, &namespace, "members", &next.ids).unwrap();
    let mut alternate = tempfile::NamedTempFile::new().unwrap();
    write_list(
        alternate.as_file_mut(),
        &namespace,
        "members",
        &IdListIds::from(["version3".to_owned()]),
    )
    .unwrap();
    let next = HashMap::from([("members".to_owned(), next)]);
    // A truncated orphan and a complete orphan with the wrong content digest
    // must both fail before replacing the committed manifest.
    for orphan in [b"incomplete".to_vec(), fs::read(alternate.path()).unwrap()] {
        fs::write(store.directory().join(format!("list-{hash}.ids")), orphan).unwrap();
        assert!(store.publish(&lease, &next, &HashMap::new(), 200).is_err());
        assert_eq!(
            fs::read(store.directory().join("manifest.json")).unwrap(),
            previous
        );
        let loaded = self::store(&root).load().unwrap().unwrap();
        assert_eq!(loaded.status.successful_refresh_ms, 100);
        assert_eq!(loaded.lists["members"].metadata.size, 9);
        assert!(loaded.lists["members"].ids.contains("version1"));
    }
    fs::write(
        store.directory().join("tmp-id-list-interrupted"),
        b"partial",
    )
    .unwrap();
    store.cleanup(&lease).unwrap();
    assert_eq!(files(&store).len(), 1);
    assert!(!store.directory().join("tmp-id-list-interrupted").exists());
}

#[test]
fn publisher_constructs_valid_canonical_images_from_owned_and_mapped_inputs() {
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let namespace = digest(&serde_json::to_vec(&("secret-fixture", "source-fixture")).unwrap());
    let check_committed_image = |store: &SharedIdListStore, expected: &HashSet<String>| {
        let data_file = manifest(store)["lists"]["members"]["data_file"]
            .as_str()
            .unwrap()
            .to_owned();
        let mapped =
            IdListImage::open(&store.directory().join(&data_file), &namespace, "members").unwrap();
        // Full semantic validation stays in construction tests. The runtime
        // reader verifies structure and the digest of this canonical image.
        mapped.validate_membership().unwrap();
        // This prototype has a base image plus an optional cumulative delta.
        if let Some(file) = manifest(store)["lists"]["members"]["delta_file"].as_str() {
            super::shared_id_list_delta::MappedDelta::open(
                &store.directory().join(file),
                &namespace,
                "members",
                &data_file,
            )
            .unwrap()
            .validate_membership()
            .unwrap();
        }
        assert_membership(
            &store.load().unwrap().unwrap().lists["members"].ids,
            expected,
        );
    };
    let expected = (0..45)
        .map(|index| format!("{index:08x}"))
        .chain([
            "".to_owned(),
            "\0".to_owned(),
            "éééé".to_owned(),
            "fallback".repeat(17),
        ])
        .collect::<HashSet<_>>();
    let mut ids = expected
        .iter()
        .cycle()
        .take(expected.len() * 3)
        .cloned()
        .collect::<IdListIds>();
    assert!(ids.insert_str("removed-before-build"));
    assert!(ids.remove("removed-before-build"));
    let mut members = list("members", &[], 100);
    members.ids = Arc::new(ids);
    let owned = HashMap::from([("members".to_owned(), members)]);
    let first = writer
        .publish(&lease, &owned, &HashMap::new(), 100)
        .unwrap();
    check_committed_image(&writer, &expected);
    let first_files = files(&writer);
    drop(owned);

    // A fresh publisher has no pointer cache, so it rebuilds from a real
    // committed mapped source and encounters the identical existing image.
    let follower = store(&root).load().unwrap().unwrap();
    assert!(follower.lists["members"].ids.is_mapped());
    let fresh_writer = store(&root);
    let second = fresh_writer
        .publish(&lease, &follower.lists, &HashMap::new(), 200)
        .unwrap();
    assert_eq!(files(&writer), first_files);
    check_committed_image(&fresh_writer, &expected);

    let mut changed = second.lists["members"].clone();
    assert!(Arc::make_mut(&mut changed.ids).remove("00000000"));
    assert!(Arc::make_mut(&mut changed.ids).insert_str("next\0key"));
    let mut next_expected = expected.clone();
    next_expected.remove("00000000");
    next_expected.insert("next\0key".to_owned());
    fresh_writer
        .publish(
            &lease,
            &HashMap::from([("members".to_owned(), changed)]),
            &HashMap::new(),
            300,
        )
        .unwrap();
    check_committed_image(&fresh_writer, &next_expected);
    assert_membership(&first.lists["members"].ids, &expected);
    assert_membership(&second.lists["members"].ids, &expected);
}

#[test]
fn committed_reader_keeps_header_validation_and_exact_retained_views() {
    let namespace = digest(b"namespace");
    let expected = [
        "",
        "abcdefgh",
        "éééé",
        "🦀",
        "with\0nul",
        "long".repeat(256).as_str(),
    ]
    .map(str::to_owned)
    .into_iter()
    .collect::<HashSet<_>>();
    let ids = expected.iter().cloned().collect::<IdListIds>();
    let mut image = tempfile::NamedTempFile::new().unwrap();
    write_list(image.as_file_mut(), &namespace, "members", &ids).unwrap();
    let bytes = fs::read(image.path()).unwrap();
    let pinned = IdListImage::open(image.path(), &namespace, "members").unwrap();
    // Dropping the directory entry must not invalidate the committed snapshot.
    drop(image);
    assert_membership(&IdListIds::from_image(pinned), &expected);
    for invalid in [bytes[..20].to_vec(), bytes[..bytes.len() - 1].to_vec()] {
        let file = tempfile::NamedTempFile::new().unwrap();
        fs::write(file.path(), invalid).unwrap();
        assert!(IdListImage::open(file.path(), &namespace, "members").is_err());
    }
    for offset in [0, 8, 12, 16, 48, 120, 124] {
        let file = tempfile::NamedTempFile::new().unwrap();
        let mut invalid = bytes.clone();
        invalid[offset] ^= 1;
        fs::write(file.path(), invalid).unwrap();
        assert!(IdListImage::open(file.path(), &namespace, "members").is_err());
    }
}

#[test]
fn cold_reader_and_publisher_reject_body_digest_mismatch_and_old_maps_survive() {
    let root = tempfile::tempdir().unwrap();
    let store = store(&root);
    let lease = store.try_acquire_lease().unwrap().unwrap();
    let lists = HashMap::from([("members".to_owned(), list("members", &["version1"], 9))]);
    let pinned = store.publish(&lease, &lists, &HashMap::new(), 100).unwrap();
    let data_file = manifest(&store)["lists"]["members"]["data_file"]
        .as_str()
        .unwrap()
        .to_owned();
    let namespace = digest(&serde_json::to_vec(&("secret-fixture", "source-fixture")).unwrap());
    let mut alternate = tempfile::NamedTempFile::new_in(store.directory()).unwrap();
    write_list(
        alternate.as_file_mut(),
        &namespace,
        "members",
        &IdListIds::from(["version2".to_owned()]),
    )
    .unwrap();
    IdListImage::open(alternate.path(), &namespace, "members")
        .unwrap()
        .validate_membership()
        .unwrap();
    // Replace the directory entry rather than mutating a mapped inode. The
    // contents are valid, but do not match the committed filename's digest.
    alternate
        .persist(store.directory().join(data_file))
        .unwrap();
    let error = self::store(&root).load().err().unwrap();
    assert_eq!(error.kind(), io::ErrorKind::InvalidData);
    assert!(error.to_string().contains("content digest mismatch"));
    // A fresh publisher cannot commit this orphan under the expected digest.
    let checking_publisher = self::store(&root);
    let error = checking_publisher
        .publish(&lease, &lists, &HashMap::new(), 200)
        .err()
        .unwrap();
    assert_eq!(error.kind(), io::ErrorKind::InvalidData);
    assert!(error.to_string().contains("content digest mismatch"));
    assert!(pinned.lists["members"].ids.contains("version1"));
    assert!(!pinned.lists["members"].ids.contains("version2"));
}

#[test]
fn malformed_manifest_and_wrong_namespace_are_rejected() {
    let root = tempfile::tempdir().unwrap();
    let store = store(&root);
    let lease = store.try_acquire_lease().unwrap().unwrap();
    let lists = HashMap::from([("members".to_owned(), list("members", &["version1"], 9))]);
    store.publish(&lease, &lists, &HashMap::new(), 100).unwrap();
    let original = manifest(&store);
    for (field, value) in [
        ("format_version", serde_json::json!(99)),
        ("namespace", serde_json::json!("wrong")),
    ] {
        let mut changed = original.clone();
        changed[field] = value;
        fs::write(
            store.directory().join("manifest.json"),
            serde_json::to_vec(&changed).unwrap(),
        )
        .unwrap();
        assert!(self::store(&root).load().is_err());
    }
    fs::write(store.directory().join("manifest.json"), b"{").unwrap();
    assert!(self::store(&root).load().is_err());
}

#[test]
fn binary_format_rejects_bad_bounds_controls_utf8_and_identity() {
    let namespace = digest(b"namespace");
    let ids = IdListIds::from([
        "aaaaaaaa".to_owned(),
        "bbbbbbbb".to_owned(),
        "short".to_owned(),
    ]);
    let mut original = tempfile::NamedTempFile::new().unwrap();
    write_list(original.as_file_mut(), &namespace, "members", &ids).unwrap();
    let bytes = fs::read(original.path()).unwrap();
    assert!(IdListImage::open(original.path(), &namespace, "members").is_ok());
    assert!(IdListImage::open(original.path(), &digest(b"other"), "members").is_err());
    assert!(IdListImage::open(original.path(), &namespace, "other").is_err());
    let inline_capacity = image_u64(&bytes, 104);
    let other_capacity = image_u64(&bytes, 112);
    let inline_slots = HEADER_LEN + inline_capacity + 16;
    let other_controls = inline_slots + inline_capacity * 8;
    let other_slots = other_controls + other_capacity + 16;
    let blob_start = other_slots + other_capacity * 16;
    let occupied = (0..inline_capacity)
        .filter(|slot| bytes[HEADER_LEN + slot] != 0x80)
        .collect::<Vec<_>>();
    let other_slot = (0..other_capacity)
        .find(|slot| bytes[other_controls + slot] != 0x80)
        .unwrap();
    let change_control = |image: &mut [u8], slot: usize, value: u8| {
        image[HEADER_LEN + slot] = value;
        if slot < 16 {
            image[HEADER_LEN + inline_capacity + slot] = value;
        }
    };
    let mut cases = vec![bytes[..20].to_vec()];
    // Version one was an unreleased sorted-array prototype. A version-two
    // reader must reject it instead of interpreting its bytes as hash slots.
    for (offset, value) in [(8, 1u32), (8, 99), (12, 1), (120, 99), (124, 1)] {
        let mut image = bytes.clone();
        image[offset..offset + 4].copy_from_slice(&value.to_le_bytes());
        cases.push(image);
    }
    for (offset, value) in [
        (80, u64::MAX),
        (80, 1),
        (80, 16),
        (104, 0),
        (104, 15),
        (104, u64::MAX),
        (112, 0),
        (96, u64::MAX),
    ] {
        let mut image = bytes.clone();
        image[offset..offset + 8].copy_from_slice(&value.to_le_bytes());
        cases.push(image);
    }
    let mut membership_cases = Vec::new();
    let mut duplicate = bytes.clone();
    duplicate_inline_key(&mut duplicate);
    membership_cases.push(duplicate);
    let mut bad_control = bytes.clone();
    change_control(&mut bad_control, occupied[0], 0x81);
    cases.push(bad_control);
    let mut bad_fingerprint = bytes.clone();
    change_control(
        &mut bad_fingerprint,
        occupied[0],
        bytes[HEADER_LEN + occupied[0]] ^ 1,
    );
    membership_cases.push(bad_fingerprint);
    let mut bad_mirror = bytes.clone();
    bad_mirror[HEADER_LEN + inline_capacity] ^= 1;
    cases.push(bad_mirror);
    let mut bad_utf8 = bytes.clone();
    bad_utf8[inline_slots + occupied[0] * 8] = 0xff;
    cases.push(bad_utf8);
    let mut bad_blob_utf8 = bytes.clone();
    bad_blob_utf8[blob_start] = 0xff;
    cases.push(bad_blob_utf8);
    for (offset, value) in [
        (other_slots + other_slot * 16, u64::MAX),
        (other_slots + other_slot * 16, 1),
        (other_slots + other_slot * 16 + 8, u64::MAX),
        (other_slots + other_slot * 16 + 8, 8),
    ] {
        let mut image = bytes.clone();
        image[offset..offset + 8].copy_from_slice(&value.to_le_bytes());
        cases.push(image);
    }
    let mut truncated = bytes.clone();
    truncated.pop();
    cases.push(truncated);
    let mut trailing_bytes = bytes.clone();
    trailing_bytes.push(0);
    cases.push(trailing_bytes);
    for bytes in cases {
        assert_invalid_image(&bytes, &namespace);
    }
    for bytes in membership_cases {
        assert_invalid_membership(&bytes, &namespace);
    }
}

#[test]
fn idle_poll_skips_parsing_and_replacement_reloads_the_opened_manifest() {
    use super::shared_id_list_store::ManifestRead;
    let root = tempfile::tempdir().unwrap();
    let writer = store(&root);
    let reader = store(&root);
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let lists = HashMap::from([("members".to_string(), list("members", &["version1"], 9))]);
    writer.publish(&lease, &lists, &HashMap::new(), 10).unwrap();
    let ManifestRead::Changed(installed, first) = reader.load_if_changed(None, || {}).unwrap()
    else {
        panic!("initial manifest missing");
    };
    for _ in 0..3 {
        assert!(matches!(
            reader
                .load_if_changed(Some(&installed), || panic!("idle manifest parsed"))
                .unwrap(),
            ManifestRead::Unchanged
        ));
    }
    writer.publish(&lease, &lists, &HashMap::new(), 20).unwrap();
    let ManifestRead::Changed(next, second) =
        reader.load_if_changed(Some(&installed), || {}).unwrap()
    else {
        panic!("committed heartbeat skipped");
    };
    assert_ne!(installed, next);
    assert_ne!(first.generation, second.generation);
    assert_eq!(second.status.successful_refresh_ms, 20);
}

#[test]
fn rollout_and_rollback_keep_independent_catalogs() {
    let root = tempfile::tempdir().unwrap();
    let open_store = |elias_fano| {
        SharedIdListStore::new(root.path(), "secret-fixture", "source-fixture", elias_fano).unwrap()
    };
    let legacy = open_store(false);
    let store = open_store(true);
    assert_eq!(
        legacy.directory(),
        root.path()
            .join("05f13bbbbd8c2ea33f3686573cac3e79e2cf2eaee56924d555176434e2130d89")
    );
    assert_eq!(
        store.directory(),
        root.path()
            .join("elias-fano-v1/e426e60f5bc19705aeccfd94a2734b7117ab4c76fc39f6938570957e8f8d6402")
    );

    // Both formats can publish under the same root while the other lease is held.
    let legacy_lease = legacy.try_acquire_lease().unwrap().unwrap();
    let lease = store.try_acquire_lease().unwrap().unwrap();
    for (writer, lease, marker, version) in [
        (&legacy, &legacy_lease, "legacy00", 2),
        (&store, &lease, "compact0", 3),
    ] {
        assert!(writer.load().unwrap().is_none());
        let lists = HashMap::from([("members".into(), list("members", &[marker, "retained"], 20))]);
        writer.publish(lease, &lists, &HashMap::new(), 42).unwrap();
        let base_file = manifest(writer)["lists"]["members"]["data_file"].clone();
        let image = fs::read(writer.directory().join(base_file.as_str().unwrap())).unwrap();
        assert_eq!(
            u32::from_le_bytes(image[8..12].try_into().unwrap()),
            version
        );
    }

    let legacy_manifest = legacy.directory().join("manifest.json");
    let original_manifest = fs::read(&legacy_manifest).unwrap();
    let pinned = open_store(true).load().unwrap().unwrap();
    let original = &pinned.lists["members"];
    let base_file = manifest(&store)["lists"]["members"]["data_file"].clone();
    let mut changed = original.clone();
    changed.apply_update_for_publish(IdListUpdate {
        new_metadata: changed.metadata.clone(),
        raw_changeset: Some("-compact0\n+compact1\n".into()),
    });
    let next = HashMap::from([("members".into(), changed)]);
    store.publish(&lease, &next, &HashMap::new(), 43).unwrap();
    let updated = manifest(&store);
    let entry = &updated["lists"]["members"];
    assert_eq!(entry["data_file"], base_file);
    assert!(entry["delta_file"].is_string());

    let follower = open_store(true).load().unwrap().unwrap();
    let ids = &follower.lists["members"].ids;
    assert!(!ids.contains("compact0"));
    assert!(ids.contains("compact1"));
    assert!(ids.contains("retained"));
    assert!(original.ids.contains("compact0"));
    assert!(!original.ids.contains("compact1"));

    let mut rotated = follower.lists["members"].clone();
    let mut metadata = rotated.metadata.clone();
    metadata.file_id = Some("file-2".into());
    rotated.apply_update_for_publish(IdListUpdate {
        new_metadata: metadata,
        raw_changeset: Some("+AAAAAAAA\n".into()),
    });
    let next = HashMap::from([("members".into(), rotated)]);
    store.publish(&lease, &next, &HashMap::new(), 44).unwrap();
    let updated = manifest(&store);
    let entry = &updated["lists"]["members"];
    // Original #853 v3 image for the single rank zero in this namespace.
    assert_eq!(
        entry["data_file"],
        "list-5fa363dea1917ec6f7d456a3e1bcbe1dd02cd838c0dba7b15cece8253a808408.ids"
    );
    assert!(entry["delta_file"].is_null());
    store.cleanup(&lease).unwrap();
    assert!(ids.contains("compact1") && !ids.contains("AAAAAAAA"));
    assert!(original.ids.contains("compact0") && !original.ids.contains("AAAAAAAA"));

    let reopened = open_store(true).load().unwrap().unwrap();
    let rotated = &reopened.lists["members"];
    assert_eq!(rotated.metadata.file_id.as_deref(), Some("file-2"));
    assert_eq!(rotated.metadata.size, 10);
    assert_eq!(rotated.ids.len(), 1);
    assert!(rotated.ids.contains("AAAAAAAA"));

    drop(legacy_lease);
    let rolled_back = open_store(false);
    let _lease = rolled_back.try_acquire_lease().unwrap().unwrap();
    let old = rolled_back.load().unwrap().unwrap();
    assert!(old.lists["members"].ids.contains("legacy00"));
    assert!(!old.lists["members"].ids.contains("compact0"));
    assert!(!old.lists["members"].ids.contains("compact1"));
    assert_eq!(fs::read(legacy_manifest).unwrap(), original_manifest);
}
