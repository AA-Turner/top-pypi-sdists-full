//! Exact byte comparison against the frozen 62ed7d8f encoder.
//! The reference retains the original iterator and all output operations.
use super::*;
use crate::id_lists_adapter::id_list_ids::CompactionPolicy;
use std::collections::BTreeSet;
use std::io::{Read, Seek};

fn reference_write_list(
    file: &mut File,
    namespace: &[u8; 32],
    name: &str,
    ids: &IdListIds,
    inline_sizing: HashTableSizing,
    fallback_sizing: HashTableSizing,
) -> io::Result<String> {
    let (inline_count, other_count) = ids.partition_counts();
    let mut inline = Vec::<[u8; 8]>::with_capacity(inline_count);
    let mut other = Vec::with_capacity(other_count);
    for value in ids.iter() {
        match <[u8; 8]>::try_from(value.as_bytes()) {
            Ok(key) => inline.push(key),
            Err(_) => other.push(value),
        }
    }
    inline.sort_unstable();
    other.sort_unstable();
    let inline_capacity = inline_sizing.capacity(inline.len())?;
    let other_capacity = fallback_sizing.capacity(other.len())?;
    let mut inline_controls = controls(inline_capacity)?;
    let mut inline_slots = vec![[0u8; 8]; inline_capacity];
    for value in inline {
        let slot = insert_slot(
            &mut inline_controls,
            inline_capacity,
            stable_hash(&value),
            true,
        )?;
        inline_slots[slot] = value;
    }
    let mut other_controls = controls(other_capacity)?;
    let mut other_slots = vec![[0u64; 2]; other_capacity];
    let mut blob_len = 0u64;
    for value in &other {
        let slot = insert_slot(
            &mut other_controls,
            other_capacity,
            stable_hash(value.as_bytes()),
            false,
        )?;
        other_slots[slot] = [blob_len, value.len() as u64];
        blob_len = blob_len
            .checked_add(value.len() as u64)
            .ok_or_else(|| invalid("ID-list image is too large"))?;
    }
    let mut hashed = HashingWriter {
        file,
        digest: Sha256::new(),
    };
    {
        let mut writer = BufWriter::with_capacity(64 * 1024, &mut hashed);
        writer.write_all(MAGIC)?;
        writer.write_all(&VERSION.to_le_bytes())?;
        writer.write_all(&0u32.to_le_bytes())?;
        writer.write_all(namespace)?;
        writer.write_all(&digest(name.as_bytes()))?;
        for number in [
            inline_count as u64,
            other.len() as u64,
            blob_len,
            inline_capacity as u64,
            other_capacity as u64,
        ] {
            writer.write_all(&number.to_le_bytes())?;
        }
        writer.write_all(&HASH_ALGORITHM.to_le_bytes())?;
        writer.write_all(&0u32.to_le_bytes())?;
        writer.write_all(&inline_controls)?;
        for value in inline_slots {
            writer.write_all(&value)?;
        }
        writer.write_all(&other_controls)?;
        for [offset, len] in other_slots {
            writer.write_all(&offset.to_le_bytes())?;
            writer.write_all(&len.to_le_bytes())?;
        }
        for value in other {
            writer.write_all(value.as_bytes())?;
        }
        writer.flush()?;
    }
    Ok(hex(&hashed.digest.finalize()))
}

const NAMESPACE: [u8; 32] = [0x31; 32];
const NAME: &str = "typed-collection-equivalence";

fn raw(index: usize) -> String {
    format!("{index:08x}")
}
fn mixed(count: usize) -> IdListIds {
    (0..count)
        .map(raw)
        .chain((0..count).map(|i| format!("other-{i:08x}-λ")))
        .chain(
            [
                "",
                "\0",
                "a\0b",
                "éééé",
                "λ漢字",
                "\0\0\0\0\0\0\0\0",
                "🙂🙂",
                "🙂λ漢-",
                "same",
            ]
            .into_iter()
            .map(str::to_owned),
        )
        .chain(["same".to_owned(), "x".repeat(1024)])
        .collect()
}
fn encoded(ids: &IdListIds, reference: bool) -> (String, Vec<u8>) {
    let mut file = tempfile::tempfile().unwrap();
    let result = if reference {
        reference_write_list(
            &mut file,
            &NAMESPACE,
            NAME,
            ids,
            INLINE_SIZING,
            FALLBACK_SIZING,
        )
    } else {
        write_list(&mut file, &NAMESPACE, NAME, ids)
    }
    .unwrap();
    file.rewind().unwrap();
    let mut bytes = Vec::new();
    file.read_to_end(&mut bytes).unwrap();
    (result, bytes)
}
fn assert_equal(ids: &IdListIds) {
    let expected: BTreeSet<&str> = ids.iter().collect();
    let (inline, other) = ids.collect_image_keys();
    assert_eq!(inline.len() + other.len(), ids.len());
    assert_eq!((inline.len(), other.len()), ids.partition_counts());
    assert_eq!(
        (inline.capacity(), other.capacity()),
        ids.partition_counts()
    );
    let collected: BTreeSet<&str> = inline
        .iter()
        .map(|v| std::str::from_utf8(v).unwrap())
        .chain(other.iter().copied())
        .collect();
    assert_eq!(collected, expected);
    assert_eq!(encoded(ids, false), encoded(ids, true));
}
fn mapped(ids: &IdListIds) -> IdListIds {
    let mut file = tempfile::NamedTempFile::new().unwrap();
    reference_write_list(
        file.as_file_mut(),
        &NAMESPACE,
        NAME,
        ids,
        INLINE_SIZING,
        FALLBACK_SIZING,
    )
    .unwrap();
    let view = IdListImage::open(file.path(), &NAMESPACE, NAME).unwrap();
    view.validate_membership().unwrap();
    IdListIds::from_image(view)
}

#[test]
fn owned_and_mapped_typed_collection_preserve_boundary_images() {
    for count in [
        0, 1, 2, 7, 8, 9, 11, 12, 13, 15, 16, 17, 23, 24, 25, 31, 32, 33, 47, 48, 49, 63, 64, 65,
        95, 96, 97, 127, 128, 129, 255, 256, 257, 1023, 1024, 1025,
    ] {
        let ids = mixed(count);
        assert_equal(&ids);
        assert_equal(&mapped(&ids));
    }
    let empty = IdListIds::new();
    assert_equal(&empty);
    assert_equal(&mapped(&empty));
}

#[test]
fn pending_removals_and_normalization_preserve_reference_images() {
    let original = mapped(&mixed(4096));
    let retained = original.clone();
    let mut pending = original;
    let mut expected: BTreeSet<String> = retained.iter().map(str::to_owned).collect();
    let changes = [
        (raw(0), false),
        (raw(1), false),
        (raw(1), true),
        (raw(99999), true),
        (raw(99999), true),
        (raw(99999), false),
        (raw(88888), true),
        ("".into(), false),
        ("éééé".into(), false),
        ("éééé".into(), true),
        ("🙂🙂".into(), false),
        ("added\0fallback".into(), true),
        ("other-00000002-λ".into(), false),
    ];
    for (key, present) in changes {
        pending.set(&key, present, CompactionPolicy::Batch);
        if present {
            expected.insert(key);
        } else {
            expected.remove(&key);
        }
        assert!(pending.pending().is_some());
        assert_equal(&pending);
        assert_eq!(
            pending.iter().map(str::to_owned).collect::<BTreeSet<_>>(),
            expected
        );
    }
    assert_equal(&retained);
    assert!(retained.contains(&raw(0)));
    assert!(!retained.contains(&raw(88888)));
}

#[test]
fn pending_full_base_stream_preserves_reference_image_without_owned_materialization() {
    let base: IdListIds = (0..600_000).map(raw).collect();
    let mut pending = mapped(&base);
    for i in 0..35_000 {
        pending.set(&raw(i), false, CompactionPolicy::Batch);
        pending.set(&raw(1_000_000 + i), true, CompactionPolicy::Batch);
    }
    let p = pending.pending().unwrap();
    assert!(p.requires_full_base);
    assert_eq!(p.changes.len(), 70_000);
    assert!(pending.owned_capacities_for_test().is_none());
    assert_equal(&pending);
    assert_eq!(pending.len(), base.len());
}

#[test]
fn overlay_and_next_pending_preserve_reference_images() {
    use crate::id_lists_adapter::shared_id_list_delta::{MappedDelta, write_delta};
    let base = Arc::new(mapped(&mixed(4096)));
    let mut pending = (*base).clone();
    pending.set(&raw(3), false, CompactionPolicy::Batch);
    pending.set(&raw(99999), true, CompactionPolicy::Batch);
    pending.set("éééé", false, CompactionPolicy::Batch);
    pending.set("overlay\0fallback", true, CompactionPolicy::Batch);
    let mut file = tempfile::NamedTempFile::new().unwrap();
    let base_file = "list-collection-reference.ids";
    write_delta(
        file.as_file_mut(),
        &NAMESPACE,
        NAME,
        base_file,
        pending.pending().unwrap(),
    )
    .unwrap();
    let delta = MappedDelta::open(file.path(), &NAMESPACE, NAME, base_file).unwrap();
    let overlay = IdListIds::from_overlay(base, delta);
    assert_equal(&overlay);
    let mut next = overlay.clone();
    next.set(&raw(3), true, CompactionPolicy::Batch);
    next.set(&raw(99999), false, CompactionPolicy::Batch);
    next.set("overlay\0fallback", false, CompactionPolicy::Batch);
    next.set("next", true, CompactionPolicy::Batch);
    assert_equal(&next);
    assert_equal(&overlay);
}

#[test]
fn fallback_only_pending_shrink_to_empty_preserves_reference_image() {
    let owned: IdListIds = (0..200)
        .map(|i| format!("fallback-only-λ-{i:04}-{}", "é".repeat(i % 17)))
        .chain([String::new(), "\0".to_owned(), "🙂-fallback".to_owned()])
        .collect();
    assert_eq!(owned.partition_counts().0, 0);
    assert_equal(&owned);
    let mut pending = mapped(&owned);
    let retained = pending.clone();
    assert_equal(&pending);
    for key in owned.iter() {
        assert!(pending.set(key, false, CompactionPolicy::Batch));
    }
    assert!(pending.pending().unwrap().requires_full_base);
    assert_eq!(pending.partition_counts(), (0, 0));
    assert_equal(&pending);
    assert_equal(&retained);
    assert_eq!(retained.len(), owned.len());
}
