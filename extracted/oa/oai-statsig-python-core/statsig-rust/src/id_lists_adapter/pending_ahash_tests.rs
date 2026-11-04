use std::collections::{HashMap, HashSet};
use std::sync::Arc;

use super::{CompactionPolicy, DeltaChanges, IdListIds, Storage};
use crate::id_lists_adapter::shared_id_list_delta::{MappedDelta, write_delta};
use crate::id_lists_adapter::shared_id_list_format::{IdListImage, digest, write_list};

fn seeded_pending(base: &Arc<IdListIds>, seed: u64) -> IdListIds {
    let mut ids = (**base).clone();
    ids.make_pending();
    let Storage::Pending(pending) = &mut ids.storage else {
        panic!("mapped fixture")
    };
    let state = ahash::RandomState::with_seeds(seed, seed + 1, seed + 2, seed + 3);
    pending.changes = DeltaChanges {
        inline: HashMap::with_hasher(state.clone()),
        other: HashMap::with_hasher(state),
    };
    ids
}

fn mapped_base() -> (Arc<IdListIds>, String, HashSet<String>) {
    let expected: HashSet<_> = (0..4096)
        .map(|i| format!("{i:08x}"))
        .chain(
            [
                "",
                "éééé",
                "🍋🍋",
                "a\0b",
                "long-字符串",
                "longer-existing-value",
            ]
            .map(str::to_owned),
        )
        .collect();
    let owned: IdListIds = expected.iter().cloned().collect();
    let mut file = tempfile::NamedTempFile::new().unwrap();
    let hash = write_list(
        file.as_file_mut(),
        &digest(b"pending-ahash"),
        "members",
        &owned,
    )
    .unwrap();
    let mapped = IdListImage::open(file.path(), &digest(b"pending-ahash"), "members").unwrap();
    (
        Arc::new(IdListIds::from_image(mapped)),
        format!("list-{hash}.ids"),
        expected,
    )
}

#[test]
fn ahash_pending_normalization_matches_owned_reference_for_exact_key_partitions() {
    let (base, _, mut expected) = mapped_base();
    let mut pending = seeded_pending(&base, 7);
    let values = [
        "00000000",
        "00000001",
        "new00000",
        "new00001",
        "",
        "éééé",
        "🍋🍋",
        "a\0b",
        "new\0value",
        "新しい値",
        "long-字符串",
    ];
    let mut random = 0x7193_abefu32;
    for _ in 0..1024 {
        random ^= random << 13;
        random ^= random >> 17;
        random ^= random << 5;
        let key = values[random as usize % values.len()];
        let present = random & 32 != 0;
        let changed = if present {
            expected.insert(key.to_owned())
        } else {
            expected.remove(key)
        };
        assert_eq!(pending.set(key, present, CompactionPolicy::Batch), changed);
        assert_eq!(pending.len(), expected.len());
        assert_eq!(pending.contains(key), present);
        let Storage::Pending(delta) = &pending.storage else {
            panic!("small change set stays pending")
        };
        assert_eq!(
            delta.changes.len(),
            base.iter().filter(|key| !expected.contains(*key)).count()
                + expected.iter().filter(|key| !base.contains(key)).count()
        );
    }
    assert_eq!(
        pending.iter().map(str::to_owned).collect::<HashSet<_>>(),
        expected
    );
    // Reversals remove pending overrides instead of accumulating a second layer.
    for key in values {
        pending.set(key, base.contains(key), CompactionPolicy::Batch);
    }
    let Storage::Pending(delta) = &pending.storage else {
        panic!("normalized pending")
    };
    assert_eq!(delta.changes.len(), 0);
    assert_eq!(pending, *base);
}

#[test]
fn ahash_pending_probe_collisions_keep_distinct_exact_keys_and_replacements() {
    let state = ahash::RandomState::with_seeds(11, 22, 33, 44);
    let mut inline = Vec::new();
    let mut other = Vec::new();
    // Same low bucket bits and high control-tag bits under the actual aHash
    // builder. This makes ordinary probe collisions; it is not a full-hash
    // collision claim or a replacement membership filter.
    for i in 0..1_000_000u32 {
        if inline.len() < 24 {
            let key: [u8; 8] = format!("{i:08x}").as_bytes().try_into().unwrap();
            let hash = state.hash_one(key);
            if hash & 63 == 0 && hash >> 57 == 0 {
                inline.push(key);
            }
        }
        if other.len() < 24 {
            let key = format!("fallback-{i:08x}-é");
            let hash = state.hash_one(key.as_str());
            if hash & 63 == 0 && hash >> 57 == 0 {
                other.push(key);
            }
        }
        if inline.len() == 24 && other.len() == 24 {
            break;
        }
    }
    assert_eq!((inline.len(), other.len()), (24, 24));
    let mut changes = DeltaChanges {
        inline: HashMap::with_capacity_and_hasher(32, state.clone()),
        other: HashMap::with_capacity_and_hasher(32, state),
    };
    let keys: Vec<_> = inline
        .iter()
        .map(|key| std::str::from_utf8(key).unwrap().to_owned())
        .chain(other)
        .collect();
    let mut reference = HashMap::new();
    for (i, key) in keys.iter().enumerate() {
        changes.set(key, i % 2 == 0);
        reference.insert(key.clone(), i % 2 == 0);
    }
    for (i, key) in keys.iter().enumerate() {
        assert_eq!(changes.get(key), reference.get(key).copied());
        if i % 3 == 0 {
            changes.remove(key);
            reference.remove(key);
        } else {
            changes.set(key, true);
            reference.insert(key.clone(), true);
        }
    }
    assert_eq!(
        changes
            .iter()
            .map(|(key, value)| (key.to_owned(), value))
            .collect::<HashMap<_, _>>(),
        reference
    );
    for key in &keys {
        assert_eq!(changes.get(key), reference.get(key).copied());
    }
    assert_eq!(changes.get("absent-not-an-alias"), None);
}

#[test]
fn ahash_seed_and_insertion_order_do_not_change_delta_or_full_base_serialization() {
    let (base, base_file, mut expected) = mapped_base();
    let operations = [
        ("00000002", false),
        ("éééé", false),
        ("a\0b", false),
        ("new00002", true),
        ("new\0value", true),
        ("新しい値", true),
    ];
    let mut a = seeded_pending(&base, 101);
    let mut b = seeded_pending(&base, 202);
    for &(key, present) in &operations {
        a.set(key, present, CompactionPolicy::Batch);
        if present {
            expected.insert(key.to_owned());
        } else {
            expected.remove(key);
        }
    }
    for &(key, present) in operations.iter().rev() {
        b.set(key, present, CompactionPolicy::Batch);
    }
    assert_eq!(a, b);
    let namespace = digest(b"pending-ahash");
    let mut delta_images = Vec::new();
    for ids in [&a, &b] {
        let Storage::Pending(pending) = &ids.storage else {
            panic!("pending fixture")
        };
        let mut file = tempfile::NamedTempFile::new().unwrap();
        let hash = write_delta(
            file.as_file_mut(),
            &namespace,
            "members",
            &base_file,
            pending,
        )
        .unwrap();
        let mapped = MappedDelta::open(file.path(), &namespace, "members", &base_file).unwrap();
        mapped.validate_membership().unwrap();
        let overlay = IdListIds::from_overlay(Arc::clone(&base), mapped);
        assert_eq!(
            overlay.iter().map(str::to_owned).collect::<HashSet<_>>(),
            expected
        );
        delta_images.push((hash, std::fs::read(file.path()).unwrap()));
    }
    assert_eq!(delta_images[0], delta_images[1]);
    let eager: IdListIds = expected.into_iter().collect();
    let mut images = Vec::new();
    for ids in [&a, &b, &eager] {
        let mut file = tempfile::NamedTempFile::new().unwrap();
        let hash = write_list(file.as_file_mut(), &namespace, "members", ids).unwrap();
        images.push((hash, std::fs::read(file.path()).unwrap()));
    }
    assert_eq!(images[0], images[1]);
    assert_eq!(images[0], images[2]);
}

#[test]
fn delta_encoder_borrows_fallback_keys_and_preserves_reversals() {
    let (base, _, _) = mapped_base();
    let mut ids = (*base).clone();
    for key in ["added-fallback", "12345678", "長い値"] {
        assert!(ids.set(key, true, CompactionPolicy::Batch));
    }
    assert!(ids.set("added-fallback", false, CompactionPolicy::Batch));
    let pending = ids.pending().unwrap();
    let (inline, other) = pending.changes.image_keys();
    assert_eq!(inline, vec![*b"12345678"]);
    assert_eq!(other, vec!["長い値"]);
    let (stored, _) = pending.changes.other.get_key_value("長い値").unwrap();
    assert_eq!(other[0].as_ptr(), stored.as_ptr());
}
