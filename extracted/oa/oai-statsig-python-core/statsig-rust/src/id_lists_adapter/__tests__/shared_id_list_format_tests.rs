use std::collections::HashSet;
use std::fs;
use std::io;
use std::sync::Arc;

use super::shared_id_list_format::{HEADER_LEN, IdListImage, digest, stable_hash, write_list};
use super::{IdList, IdListIds, IdListMetadata, IdListUpdate};

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
    assert!(changed.is_mapped());
    assert_membership(&mapped, &expected);
    let mut expected_changed = expected;
    expected_changed.remove("");
    expected_changed.remove("abc\0defg");
    expected_changed.insert("new\0key".to_owned());
    assert_membership(&mapped_ids(&changed), &expected_changed);
}

#[test]
fn mapped_rounding_boundaries_use_current_unique_cardinality() {
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
    // Each group of 16 slots holds 12 inline keys or 10 fallback keys at target occupancy.
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
    // Exercise both power-of-two and other capacities in each partition.
    for (count, inline_capacity, fallback_capacity) in [(36, 48, 64), (42, 64, 80)] {
        for key_length in [8, 20, 128] {
            let fallback = key_length != 8;
            let capacity = if fallback {
                fallback_capacity
            } else {
                inline_capacity
            };
            let home = capacity - 1;
            // Start collisions at the last slot so probing wraps and crosses three groups.
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
                .take(count + 1)
                .collect::<Vec<_>>();
            assert_eq!(
                colliding.len(),
                count + 1,
                "collision fixture search exhausted"
            );
            let expected = colliding[..count].iter().cloned().collect::<HashSet<_>>();
            let ids = expected.iter().cloned().collect();
            let mut file = tempfile::NamedTempFile::new().unwrap();
            write_list(file.as_file_mut(), &namespace, "members", &ids).unwrap();
            let mapped = IdListIds::from_image(
                IdListImage::open(file.path(), &namespace, "members").unwrap(),
            );
            assert_membership(&mapped, &expected);
            assert!(!mapped.contains(&colliding[count]));
            assert!(!mapped.contains("different-missing-key"));

            let mut broken_chain = fs::read(file.path()).unwrap();
            let count_offset = if fallback { 88 } else { 80 };
            let capacity_offset = if fallback { 112 } else { 104 };
            assert_eq!(image_u64(&broken_chain, capacity_offset), capacity);
            // An empty first slot hides later keys in the probe chain.
            assert_eq!(broken_chain[HEADER_LEN + home], 0);
            broken_chain[HEADER_LEN + home] = 0x80;
            broken_chain[count_offset..count_offset + 8]
                .copy_from_slice(&((count - 1) as u64).to_le_bytes());
            assert_invalid_membership(&broken_chain, &namespace);
        }
    }
}

#[test]
fn hash_algorithm_two_matches_fixed_format_vectors() {
    // Changing these hashes requires a new format or hash version.
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
    // Verified against SDK images written with hash algorithm 2.
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

    // Cover every tail length after full words and stripes.
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
        // Vary one byte per key to catch lanes or tails skipped during lookup.
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
fn mapped_delta_duplicates_noops_and_resets_match_owned_membership() {
    let ids = ["00000000", "00000001", "fallback-0", "éééé"]
        .map(str::to_owned)
        .into_iter()
        .collect();
    let initial = Arc::new(mapped_ids(&ids));
    let mut current = IdList {
        metadata: IdListMetadata {
            name: "members".into(),
            url: "https://example.com/list".into(),
            file_id: Some("file-1".into()),
            size: 100,
            creation_time: 1,
        },
        ids: initial.clone(),
    };
    current.apply_update(IdListUpdate {
        new_metadata: current.metadata.clone(),
        raw_changeset: Some(
            "+00000000\n+00000002\n-fallback-0\n-missing\n+fallback-1\n".to_owned(),
        ),
    });
    assert!(current.ids.is_mapped());
    assert_membership(
        &current.ids,
        &HashSet::from(
            ["00000000", "00000001", "00000002", "fallback-1", "éééé"].map(str::to_owned),
        ),
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
        &HashSet::from(["reset000", "tail"].map(str::to_owned)),
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
        &HashSet::from(["newera00"].map(str::to_owned)),
    );
    assert!(current.ids.is_mapped());
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
    // Version 1 used a sorted array.
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
