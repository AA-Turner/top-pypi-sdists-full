use super::*;
use crate::id_lists_adapter::{IdListEncoding, IdListUpdate};
use tempfile::TempDir;

fn options(dir: &TempDir) -> StatsigOptions {
    StatsigOptions {
        experimental_flags: Some(["shared_initial_id_list_base".into()].into()),
        shared_id_lists_dir: Some(dir.path().display().to_string()),
        enable_id_list_elias_fano: Some(true),
        ..Default::default()
    }
}
fn cache(dir: &TempDir) -> SharedInitialBaseCache {
    SharedInitialBaseCache::from_options("key", &options(dir)).unwrap()
}
fn apply(list: &mut IdList, body: &str) {
    let update = IdListUpdate {
        new_metadata: list.metadata.clone(),
        raw_changeset: Some(body.into()),
    };
    list.apply_update_with_encoding(IdListEncoding::EliasFano, update);
}
fn list() -> IdList {
    let mut list = IdList::new(IdListMetadata {
        name: "users".into(),
        url: "https://example.org/file?signed".into(),
        file_id: Some("version1".into()),
        creation_time: 10,
        size: 0,
    });
    apply(&mut list, "+AAAAAAAA\n+CCCCCCCC\n");
    list
}

#[test]
fn initial_base_control_requires_exact_opt_in_for_both_encodings() {
    let dir = TempDir::new().unwrap();
    let mut opts = options(&dir);
    for ef in [None, Some(false), Some(true)] {
        opts.enable_id_list_elias_fano = ef;
        assert!(SharedInitialBaseCache::from_options("key", &opts).is_some());
    }
    for flags in [
        None,
        Some(Default::default()),
        Some(
            [
                "SHARED_INITIAL_ID_LIST_BASE".into(),
                "shared_initial_id_list_base=true".into(),
            ]
            .into(),
        ),
    ] {
        opts.experimental_flags = flags;
        assert!(SharedInitialBaseCache::from_options("key", &opts).is_none());
    }
    assert!(std::fs::read_dir(dir.path()).unwrap().next().is_none());
}

#[test]
fn initial_base_is_immutable_through_sparse_edits_and_private_compaction() {
    let dir = TempDir::new().unwrap();
    for ef in [false, true] {
        let opts = StatsigOptions {
            enable_id_list_elias_fano: Some(ef),
            ..options(&dir)
        };
        let cache = SharedInitialBaseCache::from_options("key", &opts).unwrap();
        let apply = |list: &mut IdList, body: &str| {
            list.apply_update_with_encoding(
                cache.encoding,
                IdListUpdate {
                    new_metadata: list.metadata.clone(),
                    raw_changeset: Some(body.into()),
                },
            )
        };
        let first = cache.offer(list());
        let mut target = first.metadata.clone();
        target.size += 20;
        target.url = "updated".into();
        let mut worker = cache.lookup(&target).unwrap();
        assert_eq!(worker.metadata.url, target.url);
        assert_eq!(worker.metadata.size, 20);
        assert_eq!(worker.ids.has_compact_base(), ef);
        let file = first.ids.base_file().unwrap();
        apply(&mut worker, "-AAAAAAAA\n+BBBBBBBB\n");
        assert!(worker.ids.is_mapped());
        assert_eq!(worker.ids.base_file().unwrap(), file);
        assert!(!worker.ids.contains("AAAAAAAA"));
        assert!(worker.ids.contains("BBBBBBBB"));
        let mut edits = String::new();
        for i in 0..1025 {
            use std::fmt::Write;
            writeln!(edits, "+{i:08}").unwrap();
        }
        apply(&mut worker, &edits);
        assert!(!worker.ids.is_mapped());
        assert_eq!(worker.ids.mapped_bytes(), 0);
        assert!(worker.ids.contains("00001024"));
        assert!(worker.ids.contains("BBBBBBBB"));
        assert!(!worker.ids.contains("AAAAAAAA"));
        let latest = cache.lookup(&worker.metadata).unwrap();
        assert_eq!(latest.metadata.size, 20);
        assert_eq!(latest.ids.base_file().unwrap(), file);
        assert_eq!(latest.ids, first.ids);
    }
}

#[test]
fn initial_base_preserves_candidates_on_contention_and_rejects_stale_offers() {
    let dir = TempDir::new().unwrap();
    let cache = cache(&dir);
    let initial = list();
    let store = cache.store(&initial.metadata.name).unwrap();
    let lease = store.try_acquire_lease().unwrap().unwrap();
    let loser = cache.offer(initial.clone());
    assert!(Arc::ptr_eq(&loser.ids, &initial.ids));
    drop(lease);
    let mapped = cache.offer(initial.clone());
    assert!(mapped.ids.is_mapped());
    let mut ahead = initial.clone();
    apply(&mut ahead, "+BBBBBBBB\n");
    assert_eq!(cache.offer(ahead.clone()).metadata.size, 30);
    assert_eq!(cache.lookup(&ahead.metadata).unwrap().metadata.size, 20);
    let mut next = ahead;
    next.metadata.creation_time += 1;
    next.metadata.file_id = Some("version2".into());
    assert!(cache.lookup(&next.metadata).is_none());
    let replacement = cache.offer(next.clone());
    assert!(replacement.ids.is_mapped());
    assert_ne!(replacement.ids.base_file(), mapped.ids.base_file());
    assert!(Arc::ptr_eq(&initial.ids, &cache.offer(initial.clone()).ids));
    assert!(cache.lookup(&initial.metadata).is_none());
    assert!(
        cache
            .lookup(&next.metadata)
            .unwrap()
            .ids
            .contains("BBBBBBBB")
    );
    assert!(mapped.ids.contains("AAAAAAAA"));
    assert!(!mapped.ids.contains("BBBBBBBB"));
}

#[test]
fn initial_base_binds_encoding_credential_source_name_generation_and_cursor() {
    let dir = TempDir::new().unwrap();
    let cache = cache(&dir);
    let candidate = list();
    let mut target = candidate.metadata.clone();
    cache.offer(candidate.clone());
    let make =
        |key, opts: &StatsigOptions| SharedInitialBaseCache::from_options(key, opts).unwrap();
    let mut opts = options(&dir);
    opts.enable_id_list_elias_fano = None;
    let hash = make("key", &opts);
    assert!(hash.lookup(&target).is_none());
    assert!(!hash.offer(candidate.clone()).ids.has_compact_base());
    assert!(cache.lookup(&target).unwrap().ids.has_compact_base());
    opts.enable_id_list_elias_fano = Some(true);
    assert!(make("other", &opts).lookup(&target).is_none());
    opts.id_lists_url = Some("https://other.example/manifest".into());
    assert!(make("key", &opts).lookup(&target).is_none());
    target.name = "other".into();
    assert!(cache.lookup(&target).is_none());
    target.name.clone_from(&candidate.metadata.name);
    target.file_id = Some("updated".into());
    assert!(cache.lookup(&target).is_none());
    target.file_id.clone_from(&candidate.metadata.file_id);
    target.size -= 1;
    assert!(cache.lookup(&target).is_none());
    let store = cache.store(&target.name).unwrap();
    let manifest = store.directory().join("manifest.json");
    let mut body: serde_json::Value =
        serde_json::from_slice(&std::fs::read(&manifest).unwrap()).unwrap();
    assert_eq!(body["lists"]["users"]["metadata"]["url"], "");
    body["lists"]["users"]["metadata"]["size"] = 10.into();
    std::fs::write(manifest, serde_json::to_vec(&body).unwrap()).unwrap();
    assert!(cache.lookup(&target).is_none());
    let repaired = cache.offer(candidate);
    assert!(repaired.ids.is_mapped());
    assert_eq!(cache.lookup(&repaired.metadata).unwrap().metadata.size, 20);
}

#[test]
fn initial_base_counts_lookup_outcomes_and_storage_errors_separately() {
    use crate::observability::ops_stats::OpsStatsEvent;

    let dir = TempDir::new().unwrap();
    let mut cache = cache(&dir);
    cache.ops_stats = Arc::new(OpsStatsForInstance::new());
    let mut events = cache.ops_stats.subscribe_for_test();
    let candidate = list();
    let target = &candidate.metadata;
    assert!(cache.lookup(target).is_none());
    cache.offer(candidate.clone());
    assert!(cache.lookup(target).is_some());
    let mut newer = target.clone();
    newer.creation_time += 1;
    assert!(cache.lookup(&newer).is_none());

    let path = cache
        .store(&target.name)
        .unwrap()
        .directory()
        .join("manifest.json");
    std::fs::write(&path, "corrupt").unwrap();
    assert!(cache.lookup(target).is_none());
    cache.directory = path;
    assert!(!cache.offer(candidate).ids.is_mapped());

    for (name, tag, value) in [
        ("shared_id_lists.cache.lookup", "result", "miss"),
        ("shared_id_lists.cache.lookup", "result", "hit"),
        ("shared_id_lists.cache.lookup", "result", "miss"),
        ("shared_id_lists.failure", "reason", "read"),
        ("shared_id_lists.failure", "reason", "publish"),
    ] {
        let OpsStatsEvent::Observability(event) = events.try_recv().unwrap() else {
            panic!("expected cache metric");
        };
        assert_eq!(event.metric_name, name);
        assert!(matches!(event.metric_type, MetricType::Increment));
        assert_eq!(event.value, 1.0);
        assert_eq!(event.tags, Some([(tag.into(), value.into())].into()));
    }
    assert!(events.try_recv().is_err());
}

#[test]
fn initial_base_unusable_directory_retains_private_result() {
    let dir = TempDir::new().unwrap();
    std::fs::write(dir.path().join(CACHE_DIR), "block directory").unwrap();
    let cache = cache(&dir);
    let candidate = list();
    assert!(cache.lookup(&candidate.metadata).is_none());
    let installed = cache.offer(candidate.clone());
    assert!(Arc::ptr_eq(&installed.ids, &candidate.ids));
}

#[test]
fn initial_base_filters_superseded_metadata_before_opening_image() {
    let dir = TempDir::new().unwrap();
    let cache = cache(&dir);
    let first = cache.offer(list());
    let store = cache.store(&first.metadata.name).unwrap();
    let image = store.directory().join(first.ids.base_file().unwrap());
    drop(first);
    std::fs::remove_file(&image).unwrap();
    assert!(
        store
            .load_initial_base("users", |meta| meta.creation_time > 10)
            .unwrap()
            .is_none()
    );
    assert!(store.load_initial_base("users", |_| true).is_err());
}
