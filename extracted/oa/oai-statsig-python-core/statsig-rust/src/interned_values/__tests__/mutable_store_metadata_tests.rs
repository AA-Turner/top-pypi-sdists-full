use super::{MutableStore, WEAK_STORE_SWEEP_INTERVAL, get_returnable_from_local};
use crate::{
    DynamicReturnable,
    evaluation::dynamic_returnable::{DynamicReturnableValue, owned_returnable_stable_hash},
    hashing,
};
use rusty_fork::rusty_fork_test;
use std::{
    borrow::Cow,
    collections::HashMap,
    sync::{Arc, Barrier},
};

#[test]
fn occupied_entry_returns_the_winning_value_and_metadata() {
    let store = MutableStore::<String, u64>::default();
    let first = store.get_or_insert_with_metadata(42, Arc::new("first".into()), 17);
    let loser = Arc::new("second".into());
    let result = store.get_or_insert_with_metadata(42, Arc::clone(&loser), 29);
    let hit = store.get_with_metadata(42).unwrap();

    assert!(Arc::ptr_eq(&result.0, &first.0));
    assert!(Arc::ptr_eq(&hit.0, &first.0));
    assert_eq!(result.1, 17);
    assert_eq!(hit.1, 17);
    assert_eq!(Arc::strong_count(&loser), 1);
}

#[test]
fn concurrent_insertions_keep_value_and_metadata_together() {
    const THREAD_COUNT: usize = 16;
    let store = Arc::new(MutableStore::<u64, u64>::default());
    let start = Arc::new(Barrier::new(THREAD_COUNT));
    let threads = (0..THREAD_COUNT as u64)
        .map(|value| {
            let store = Arc::clone(&store);
            let start = Arc::clone(&start);
            std::thread::spawn(move || {
                start.wait();
                store.get_or_insert_with_metadata(42, Arc::new(value), value * 17 + 99)
            })
        })
        .collect::<Vec<_>>();
    let results = threads
        .into_iter()
        .map(|thread| thread.join().unwrap())
        .collect::<Vec<_>>();

    for (value, metadata) in &results {
        assert!(Arc::ptr_eq(value, &results[0].0));
        assert_eq!(*metadata, **value * 17 + 99);
    }
}

#[test]
fn expired_entry_replaces_both_value_and_metadata() {
    let store = MutableStore::<String, u64>::default();
    let first = store.get_or_insert_with_metadata(42, Arc::new("first".into()), 17);
    let weak = Arc::downgrade(&first.0);
    drop(first);

    assert!(weak.upgrade().is_none());
    assert!(store.get_with_metadata(42).is_none());
    let second = store.get_or_insert_with_metadata(42, Arc::new("second".into()), 29);
    assert_eq!(second.0.as_str(), "second");
    assert_eq!(second.1, 29);
    assert_eq!(store.get_with_metadata(42).unwrap().1, 29);
    assert_eq!(store.live_len(), 1);
}

#[test]
fn metadata_entries_follow_the_existing_sweep_schedule() {
    let store = MutableStore::<u64, u64>::default();
    for hash in 0..WEAK_STORE_SWEEP_INTERVAL as u64 {
        drop(store.get_or_insert_with_metadata(hash, Arc::new(hash), hash + 1));
    }

    assert_eq!(store.live_len(), 0);
    assert_eq!(store.stored_len(), 1);
}

#[test]
fn take_live_discards_metadata_and_weak_references() {
    let store = MutableStore::<String, u64>::default();
    let live = store.get_or_insert_with_metadata(1, Arc::new("live".into()), 17);
    let weak = Arc::downgrade(&live.0);
    drop(store.get_or_insert_with_metadata(2, Arc::new("dead".into()), 29));
    assert_eq!(Arc::weak_count(&live.0), 2);

    let taken = store.take_live();
    assert_eq!(taken.len(), 1);
    assert_eq!(taken[0].0, 1);
    assert!(Arc::ptr_eq(&taken[0].1, &live.0));
    assert_eq!(Arc::weak_count(&live.0), 1);
    assert_eq!(store.stored_len(), 0);
    assert_eq!(store.stored_capacity(), 0);
    assert!(store.get_with_metadata(1).is_none());

    drop(live);
    assert_eq!(Arc::strong_count(&taken[0].1), 1);
    drop(taken);
    assert!(weak.upgrade().is_none());
}

#[test]
fn default_unit_metadata_preserves_replacement_and_drain() {
    let store = MutableStore::<String>::default();
    let original = store.get_or_insert(42, Arc::new("original".into()));
    let replacement = Arc::new("replacement".into());
    store.replace(42, &replacement);
    assert!(Arc::ptr_eq(&store.get(42).unwrap(), &replacement));
    assert_eq!(original.as_str(), "original");

    let taken = store.take_live();
    assert_eq!(taken.len(), 1);
    assert!(Arc::ptr_eq(&taken[0].1, &replacement));
    assert!(store.get(42).is_none());
}

rusty_fork_test! {
    #[test]
    fn local_returnable_hits_preserve_eager_hash_and_json() {
        let raw = serde_json::value::RawValue::from_string(
            r#"{"nested":{"a":1,"b":true},"values":[1,2]}"#.into(),
        ).unwrap();
        let hash = hashing::hash_one(raw.get().as_bytes());
        let first = get_returnable_from_local(hash, Cow::Borrowed(&raw));
        let second = get_returnable_from_local(hash, Cow::Borrowed(&raw));
        let (DynamicReturnableValue::JsonPointer(first_ptr), DynamicReturnableValue::JsonPointer(second_ptr)) =
            (&first.value, &second.value)
        else {
            panic!("local returnables must use pointer values");
        };

        assert!(Arc::ptr_eq(first_ptr, second_ptr));
        assert!(first.has_inline_stable_hash());
        assert!(second.has_inline_stable_hash());
        assert_eq!(first.get_stable_hash(), owned_returnable_stable_hash(first_ptr));
        assert_eq!(first.get_stable_hash(), second.get_stable_hash());
        assert_eq!(first.get_hash(), hash);
        assert_eq!(first, second);
        assert_eq!(
            serde_json::to_value(&second).unwrap(),
            serde_json::json!({"nested": {"a": 1, "b": true}, "values": [1, 2]}),
        );
    }

    #[test]
    fn in_memory_preload_preserves_cached_hashes_in_both_lookup_paths() {
        let raw = serde_json::value::RawValue::from_string(
            r#"{"nested":{"a":1,"b":true},"values":[1,2]}"#.into(),
        ).unwrap();
        let hash = hashing::hash_one(raw.get().as_bytes());
        let value = Arc::new(serde_json::from_str(raw.get()).unwrap());
        // Deliberately distinct metadata detects recomputation, even if output
        // equality alone would still pass. Only this isolated store is seeded.
        let cached_hash = owned_returnable_stable_hash(&value).wrapping_add(1).max(1);
        let held = super::MUTABLE_RETURNABLES
            .get_or_insert_with_metadata(hash, Arc::clone(&value), cached_hash);
        let weak = Arc::downgrade(&value);

        super::InternedStore::preload(
            include_bytes!("../../../tests/data/eval_proj_dcs.json"),
        ).unwrap();
        assert_eq!(super::MUTABLE_RETURNABLES.stored_len(), 0);
        assert_eq!(Arc::weak_count(&value), 1);
        drop(held);
        drop(value);

        let interned = super::InternedStore::get_or_intern_returnable(Cow::Borrowed(&raw));
        let preloaded = super::InternedStore::try_get_preloaded_returnable(raw.get().as_bytes()).unwrap();
        for returnable in [&interned, &preloaded] {
            let DynamicReturnableValue::JsonStatic(value) = &returnable.value else {
                panic!("expected a shared static returnable");
            };
            assert!(std::ptr::eq(*value, weak.as_ptr()));
            assert!(returnable.has_inline_stable_hash());
            assert_eq!(returnable.get_stable_hash(), cached_hash);
            assert_eq!(returnable.get_hash(), hash);
            assert_eq!(serde_json::to_value(returnable).unwrap(),
                serde_json::json!({"nested": {"a": 1, "b": true}, "values": [1, 2]}));
        }
        assert_eq!(interned, preloaded);
    }

    #[test]
    fn new_values_after_preload_keep_local_hash_reuse_and_reclamation() {
        super::InternedStore::preload(
            include_bytes!("../../../tests/data/eval_proj_dcs.json"),
        ).unwrap();
        let raw = serde_json::value::RawValue::from_string(
            r#"{"added_after_preload":[1,{"enabled":true}]}"#.into(),
        ).unwrap();
        assert!(super::InternedStore::try_get_preloaded_returnable(raw.get().as_bytes()).is_none());
        let first = super::InternedStore::get_or_intern_returnable(Cow::Borrowed(&raw));
        let second = super::InternedStore::get_or_intern_returnable(Cow::Borrowed(&raw));
        let (DynamicReturnableValue::JsonPointer(a), DynamicReturnableValue::JsonPointer(b)) =
            (&first.value, &second.value) else { panic!("expected local returnables"); };
        assert!(Arc::ptr_eq(a, b));
        assert_eq!(first.get_stable_hash(), owned_returnable_stable_hash(a));
        assert_eq!(first.get_stable_hash(), second.get_stable_hash());
        let weak = Arc::downgrade(a);
        drop(first);
        drop(second);
        assert!(weak.upgrade().is_none());
    }

    #[test]
    fn invalid_local_returnable_is_not_interned() {
        let raw = serde_json::value::RawValue::from_string("[]".into()).unwrap();
        let hash = hashing::hash_one(raw.get().as_bytes());
        let fallback = get_returnable_from_local(hash, Cow::Borrowed(&raw));
        assert!(super::MUTABLE_RETURNABLES.get_with_metadata(hash).is_none());
        assert_eq!(fallback.get_json(), Some(HashMap::new()));
        assert_eq!(fallback.get_hash(), hash);
        assert!(fallback.has_inline_stable_hash());
        assert_eq!(
            fallback.get_stable_hash(),
            owned_returnable_stable_hash(&HashMap::new()),
        );
    }
}

#[test]
fn zero_cached_hash_preserves_the_existing_fallback() {
    let value = Arc::new(HashMap::new());
    let expected = owned_returnable_stable_hash(&value);
    let returnable =
        DynamicReturnable::from_cached_value(42, DynamicReturnableValue::JsonPointer(value), 0);
    assert!(!returnable.has_inline_stable_hash());
    assert_eq!(returnable.get_stable_hash(), expected);
}
