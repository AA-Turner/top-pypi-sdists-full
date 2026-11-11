use super::*;
use std::collections::HashSet;
use tempfile::NamedTempFile;

fn spelling(rank: u64) -> String {
    use base64::{Engine, engine::general_purpose::STANDARD};
    STANDARD.encode(&rank.to_be_bytes()[2..])
}

#[test]
fn ef_canonical_count_limit() {
    let last_supported = 1_431_655_765;
    assert!(elias_fano::Ef::supports_count(last_supported));
    assert!(!elias_fano::Ef::supports_count(last_supported + 1));
}

#[test]
fn ef_sparse_canonical_partition_avoids_full_rank_reservation() {
    let mut keys: Vec<_> = (0..1024u64).map(u64::to_le_bytes).collect();
    keys.push(*b"AAAAAAAA");
    let (_, ranks) = elias_fano::Ef::prepare(&mut keys).unwrap().unwrap();
    assert_eq!(ranks, [0u64.to_ne_bytes()]);
    assert!(ranks.capacity() < 1024);
}

#[test]
fn ef_base_handles_skew_bounds_arbitrary_strings_and_borrowed_iteration() {
    let mut orig: HashSet<String> = (0..160)
        .chain((0..4000).map(|i| (i * 0x9e37_79b9_7f4bu64) & ((1 << 48) - 1)))
        .chain([(1 << 48) - 1, (1 << 48) - 2])
        .map(spelling)
        .collect();
    for key in [
        "",
        "!!!!bad!",
        "éééé",
        "abcd\0efg",
        "bad-padding==",
        "åλλ",
        "x",
    ] {
        orig.insert(key.to_owned());
    }
    let ids = orig.iter().cloned().collect();
    let mut f = NamedTempFile::new().unwrap();
    let digest = write_list_with_format(f.as_file_mut(), &[7; 32], "mixed", &ids, true).unwrap();
    // Golden digest from the v3 encoder at 0877139e on this mixed-key fixture.
    assert_eq!(
        digest,
        "a4de7ec4d8e0e967cf6658a50b0fdd9c1d7f1769d1facd5d6a2223d75bce5d74"
    );
    let m = IdListImage::open(f.path(), &[7; 32], "mixed").unwrap();
    let heap = IdListImage::build_heap(&[7; 32], "mixed", &ids).unwrap();
    assert!(!heap.is_mapped() && m.is_mapped());
    assert_eq!(&*heap.map, &*m.map);
    assert!(heap.is_compact() && heap.map.len() < 8 * orig.len());
    assert!(heap.iter_keys.get().is_none() && heap.content_digest.get().is_none());
    assert!(m.ef.is_some());
    assert_eq!(m.len(), orig.len());
    assert!(m.iter_keys.get().is_none());
    assert!(m.contains("AAAAAAAA"));
    assert!(m.all_image_keys(
        |key| orig.contains(std::str::from_utf8(&key).unwrap()),
        |key| orig.contains(key),
    ));
    assert!(m.iter_keys.get().is_none());
    let mut cursor = 0;
    assert_eq!(
        std::iter::from_fn(|| m.next(&mut cursor))
            .map(str::to_owned)
            .collect::<HashSet<_>>(),
        orig
    );
    assert!(m.iter_keys.get().is_some());
    for key in orig
        .iter()
        .map(String::as_str)
        .chain(["!!!!!!!!", "AAAAAA==", "éééa", "absent"])
    {
        assert_eq!(heap.contains(key), orig.contains(key));
        assert_eq!(m.contains(key), orig.contains(key));
        assert_eq!(
            m.contains_hashed(key, stable_hash(key.as_bytes())),
            orig.contains(key)
        );
    }
    for x in 0..10000 {
        let key = spelling((x * 0x9e37_79b9_7f4bu64) & ((1 << 48) - 1));
        assert_eq!(m.contains(&key), orig.contains(&key));
    }
    let mut bytes = std::fs::read(f.path()).unwrap();
    // Corrupt restart[0], which must address bit 0.
    bytes[HEADER_LEN + 8] = 1;
    let f2 = NamedTempFile::new().unwrap();
    std::fs::write(f2.path(), bytes).unwrap();
    assert!(IdListImage::open(f2.path(), &[7; 32], "mixed").is_err());
}

#[test]
fn delta_requires_an_in_bounds_v2_hash_table() {
    use crate::id_lists_adapter::shared_id_list_delta::MappedDelta;
    let ns = [11; 32];
    let name = "mixed";
    let base = "list-test.ids";
    let open = |table: &[u8], declared_len: u64| {
        let mut delta = vec![0; 72];
        delta[..8].copy_from_slice(b"STGDELT\0");
        delta[8..12].copy_from_slice(&1u32.to_le_bytes());
        delta[16..24].copy_from_slice(&declared_len.to_le_bytes());
        delta[24..32].copy_from_slice(&1u64.to_le_bytes());
        delta[40..72].copy_from_slice(&digest(base.as_bytes()));
        delta.extend_from_slice(table);
        let f = NamedTempFile::new().unwrap();
        std::fs::write(f.path(), delta).unwrap();
        MappedDelta::open(f.path(), &ns, name, base).map(drop)
    };

    let mut plain = NamedTempFile::new().unwrap();
    write_list(plain.as_file_mut(), &ns, name, &IdListIds::new()).unwrap();
    let table = std::fs::read(plain.path()).unwrap();
    let len = table.len() as u64;
    open(&table, len).unwrap();
    for declared in [len - 1, len + 1, u64::MAX] {
        let err = open(&table, declared).expect_err("invalid table extent");
        assert_eq!(err.kind(), io::ErrorKind::InvalidData, "length {declared}");
    }

    // An EF-only table also has zero hash slots, but no operation bits for its key.
    let ids = IdListIds::from(["AAAAAAAA".to_owned()]);
    let mut compact = NamedTempFile::new().unwrap();
    write_list_with_format(compact.as_file_mut(), &ns, name, &ids, true).unwrap();
    let table = std::fs::read(compact.path()).unwrap();
    let err = open(&table, table.len() as u64).expect_err("EF inside delta");
    assert_eq!(err.kind(), io::ErrorKind::InvalidData);
}

#[test]
fn ef_rejects_canonical_member_in_residual_raw_eight_partition() {
    let ns = [12; 32];
    let name = "mixed";
    let ids = IdListIds::from(["AAAAAAAA".to_owned(), "!!!!bad!".to_owned()]);
    let mut f = NamedTempFile::new().unwrap();
    write_list_with_format(f.as_file_mut(), &ns, name, &ids, true).unwrap();
    let mut bytes = std::fs::read(f.path()).unwrap();
    let offsets: Vec<_> = bytes
        .windows(8)
        .enumerate()
        .filter_map(|(i, w)| (w == b"!!!!bad!").then_some(i))
        .collect();
    assert_eq!(offsets.len(), 1);
    bytes[offsets[0]..offsets[0] + 8].copy_from_slice(b"ZZZZZZZZ");
    let f = NamedTempFile::new().unwrap();
    std::fs::write(f.path(), bytes).unwrap();
    let err = IdListImage::open(f.path(), &ns, name)
        .err()
        .expect("mispartitioned key");
    assert_eq!(err.kind(), std::io::ErrorKind::InvalidData);
    // A plain v2 hash image still accepts canonical and arbitrary raw-eight strings.
    let mut plain = NamedTempFile::new().unwrap();
    write_image_keys(plain.as_file_mut(), &ns, name, ids.collect_image_keys()).unwrap();
    let view = IdListImage::open(plain.path(), &ns, name).unwrap();
    assert!(view.contains("AAAAAAAA") && view.contains("!!!!bad!"));
}

#[test]
fn compact_rejects_duplicate_low_bits_bad_count_and_truncated_members() {
    let ids = IdListIds::from([spelling(0), spelling(1)]);
    let mut image = NamedTempFile::new().unwrap();
    write_list_with_format(image.as_file_mut(), &[0; 32], "list", &ids, true).unwrap();
    let bytes = std::fs::read(image.path()).unwrap();
    let rejects = |bytes: &[u8]| {
        let f = NamedTempFile::new().unwrap();
        std::fs::write(f.path(), bytes).unwrap();
        assert!(IdListImage::open(f.path(), &[0; 32], "list").is_err());
    };
    rejects(&bytes[..bytes.len() - 1]);
    let mut bad = bytes.clone();
    bad[HEADER_LEN..HEADER_LEN + 8].copy_from_slice(&u64::MAX.to_le_bytes());
    rejects(&bad);
    // Two members have 47 low bits each and share a high bucket. Clearing
    // member one's first low bit duplicates the first member.
    let mut bad = bytes;
    bad[HEADER_LEN + 8 + 4 + 47 / 8] &= !(1 << (47 % 8));
    rejects(&bad);
}

#[test]
fn compact_without_canonical_keys_uses_legacy_bytes() {
    let ids = IdListIds::from(["!!!!bad!".to_owned(), "é".to_owned()]);
    let mut compact = NamedTempFile::new().unwrap();
    let mut legacy = NamedTempFile::new().unwrap();
    let write = |file: &mut File, compact| {
        write_list_with_format(file, &[1; 32], "mixed", &ids, compact).unwrap()
    };
    assert_eq!(
        write(compact.as_file_mut(), true),
        write(legacy.as_file_mut(), false)
    );
    assert_eq!(
        std::fs::read(compact.path()).unwrap(),
        std::fs::read(legacy.path()).unwrap()
    );
}

#[test]
fn clustered_million_members_fall_back_without_losing_spellings() {
    let count = 1_000_000;
    let mut ids: IdListIds = (0..count).map(spelling).collect();
    ids.insert_str("éééé");
    ids.insert_str("a longer fallback");
    let mut file = NamedTempFile::new().unwrap();
    write_list_with_format(file.as_file_mut(), &[9; 32], "dense", &ids, true).unwrap();
    let view = IdListImage::open(file.path(), &[9; 32], "dense").unwrap();
    assert!(!view.is_compact());
    assert_eq!(view.len(), ids.len());
    assert!(ids.iter().all(|key| view.contains(key)));
    assert!(!view.contains(&spelling(count)));
}

#[test]
fn accepts_512_unary_bits_rejects_513_in_first_and_last_blocks() {
    // For 481 keys the layout uses 512 buckets, 39 low bits each.
    let count = 481usize;
    let buckets = 512usize;
    let low_bits = 39usize;
    for target in [0, 511] {
        let mut ranks: Vec<u64> = (0..count as u64)
            .map(|i| ((target as u64) << low_bits) + i)
            .collect();
        // Leave 480 members plus 32 separators in the target block.
        let adjacent = if target == 0 { count - 1 } else { 0 };
        let neighbor_bucket = if target == 0 { 32 } else { 479 };
        ranks[adjacent] = (neighbor_bucket << low_bits) + adjacent as u64;
        let ids: IdListIds = ranks.into_iter().map(spelling).collect();
        let mut file = NamedTempFile::new().unwrap();
        write_list_with_format(file.as_file_mut(), &[3; 32], "limit", &ids, true).unwrap();
        let view = IdListImage::open(file.path(), &[3; 32], "limit").unwrap();
        assert!(view.is_compact());
        assert!(ids.iter().all(|key| view.contains(key)));
        let mut crowded = ids.clone();
        assert!(crowded.remove(&spelling((neighbor_bucket << low_bits) + adjacent as u64)));
        assert!(crowded.insert(spelling(((target as u64) << low_bits) + adjacent as u64)));
        let mut fallback = NamedTempFile::new().unwrap();
        write_list_with_format(fallback.as_file_mut(), &[3; 32], "limit", &crowded, true).unwrap();
        let fallback = IdListImage::open(fallback.path(), &[3; 32], "limit").unwrap();
        assert!(!fallback.is_compact());
        assert!(crowded.iter().all(|key| fallback.contains(key)));
        let mut bytes = std::fs::read(file.path()).unwrap();
        // Move the one neighbor into the target bucket. Low values (0..481)
        // and exact ordering remain intact; recompute the unary bits and
        // restart positions, producing an otherwise valid compact image.
        let dir = HEADER_LEN + 8;
        let highs = dir + 4 * buckets.div_ceil(32) + (count * low_bits).div_ceil(8) + 8;
        bytes[highs..highs + (count + buckets).div_ceil(8)].fill(0);
        for i in target..target + count {
            bytes[highs + i / 8] |= 1 << (i % 8);
        }
        for k in (0..buckets).step_by(32) {
            let bit = if k <= target { k } else { k + count };
            let offset = dir + (k / 32) * 4;
            bytes[offset..offset + 4].copy_from_slice(&(bit as u32).to_le_bytes());
        }
        let corrupt = NamedTempFile::new().unwrap();
        std::fs::write(corrupt.path(), bytes).unwrap();
        let err = IdListImage::open(corrupt.path(), &[3; 32], "limit")
            .err()
            .unwrap();
        assert!(err.to_string().contains("density"));
    }
}

#[test]
fn compact_single_partial_restart_block_accepts_last_bucket() {
    let ids: IdListIds = (0..7).map(|i| spelling((1u64 << 48) - 1 - i)).collect();
    let mut file = NamedTempFile::new().unwrap();
    write_list_with_format(file.as_file_mut(), &[3; 32], "partial", &ids, true).unwrap();
    let view = IdListImage::open(file.path(), &[3; 32], "partial").unwrap();
    assert!(view.is_compact());
    assert!(ids.iter().all(|key| view.contains(key)));
}

#[test]
fn direct_adds_match_the_existing_heap_image_including_density_fallback() {
    for (distinct, stride, compact) in [
        (1024, 0x9e37_79b9_7f4bu64, true),
        (1024, 1, false),
        (1, 1, true),
    ] {
        let keys = (0..1024)
            .rev()
            .map(|i| spelling((i % distinct * stride) & ((1 << 48) - 1)))
            .collect::<Vec<_>>();
        let body: String = keys
            .iter()
            .chain(&keys)
            .map(|key| format!("+{key}\n"))
            .collect();
        let ids: IdListIds = keys.into_iter().collect();
        let expected = IdListImage::build_heap(&[7; 32], "direct", &ids).unwrap();
        let actual = IdListImage::try_heap_from_adds(&[7; 32], "direct", body.into()).unwrap();

        assert_eq!(actual.is_compact(), compact);
        assert_eq!(&*actual.map, &*expected.map);
        assert_eq!(actual.len(), distinct as usize);
        assert!(ids.iter().all(|key| actual.contains(key)));
    }
}

#[test]
fn direct_adds_preserve_ineligible_changesets_for_ordered_replay() {
    let prefix = "+AAAAAAAA\n".repeat(1000);
    for suffix in [
        "-AAAAAAAA\n",
        "?BBBBBBBB\n",
        "+!!!!bad!\n",
        "+éééé\n",
        "+BBBBBBBB\r\n",
        "+BBBBBBBB",
    ] {
        let body = format!("{prefix}{suffix}");
        assert!(matches!(
            IdListImage::try_heap_from_adds(&[7; 32], "direct", Cow::Borrowed(&body)),
            Err(Cow::Borrowed(original)) if original == body
        ));
    }
}
