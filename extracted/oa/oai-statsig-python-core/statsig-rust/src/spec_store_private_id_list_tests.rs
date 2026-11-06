use super::*;
use crate::id_lists_adapter::IdListMetadata;

fn store(enable_id_list_elias_fano: Option<bool>) -> SpecStore {
    SpecStore::new(
        "private-list-publication",
        String::new(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&StatsigOptions {
            enable_id_list_elias_fano,
            ..Default::default()
        }),
    )
}

fn update(name: &str, body: Option<&str>) -> (String, IdListUpdate) {
    (
        name.into(),
        IdListUpdate {
            new_metadata: IdListMetadata {
                name: name.into(),
                url: name.into(),
                file_id: Some("file".into()),
                creation_time: 1,
                size: 0,
            },
            raw_changeset: body.map(str::to_owned),
        },
    )
}

#[tokio::test]
async fn staged_append_and_deletion_survive_config_and_unchanged_list_publications() {
    for format in [None, Some(true)] {
        check_staged_append_and_deletion(store(format));
    }
}

fn check_staged_append_and_deletion(store: SpecStore) {
    store.did_receive_id_list_updates(HashMap::from([
        update("kept", Some("+AAAAAAAA\n")),
        update("removed", Some("+obsolete\n")),
    ]));
    let base = store.load_data().id_lists.clone();
    let staged = store.updated_id_lists(
        &base,
        HashMap::from([update("kept", Some("+BBBBBBBB\n"))]),
        IdListPublicationMode::Replace,
        1,
    );

    store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(
                include_bytes!("../tests/data/dcs_with_checksum.json").to_vec(),
            ),
            source: SpecsSource::Bootstrap,
            received_at: 10,
            source_api: None,
            has_updates: None,
        })
        .unwrap();
    let config = store.load_data();
    store.did_receive_id_list_updates(HashMap::from([
        update("kept", None),
        update("removed", Some("")),
    ]));
    assert!(Arc::ptr_eq(&base, &store.load_data().id_lists));

    store
        .commit_id_lists(
            Some(&base),
            staged,
            HashMap::new(),
            "Network",
            IdListPublicationMode::Replace,
            LOCK_TIMEOUT,
        )
        .unwrap();
    let data = store.load_data();
    assert!(Arc::ptr_eq(&config.snapshot, &data.snapshot));
    assert_eq!(data.source, SpecsSource::Bootstrap);
    assert_eq!(data.lcut(), 1000);
    assert_eq!(data.id_lists.len(), 1);
    assert!(data.id_lists["kept"].ids.contains("BBBBBBBB"));
    assert_eq!(store.get_current_id_list_metadata()["kept"].size, 20);
    assert!(!base["kept"].ids.contains("BBBBBBBB"));
    assert!(base["removed"].ids.contains("obsolete"));
}

#[test]
fn staged_append_cannot_replace_an_installed_snapshot_with_the_same_cursor() {
    for format in [None, Some(true)] {
        check_superseded_append(store(format));
    }
}

fn check_superseded_append(store: SpecStore) {
    store.did_receive_id_list_updates(HashMap::from([update("members", Some("+AAAAAAAA\n"))]));
    let base = store.load_data().id_lists.clone();
    let staged = store.updated_id_lists(
        &base,
        HashMap::from([update("members", Some("+BBBBBBBB\n"))]),
        IdListPublicationMode::Replace,
        1,
    );
    let discarded = Arc::downgrade(&staged);

    let (name, replacement) = update("members", Some("+CCCCCCCC\n"));
    let mut list = IdList::new(replacement.new_metadata.clone());
    list.apply_update(replacement);
    let observation = IdListPropagationUpdate {
        file_id: list.metadata.file_id.clone(),
        creation_time: list.metadata.creation_time,
        url: list.metadata.url.clone(),
        ts: Some(1),
        size: list.metadata.size,
        applied_range: Some(0..list.metadata.size),
    };
    store
        .did_receive_id_list_snapshot(
            HashMap::from([(name.clone(), list)]),
            HashMap::from([(name, observation)]),
        )
        .unwrap();
    let winner = store.load_data();
    assert_eq!(store.config_updates.wait(Duration::ZERO), Some(true));

    // An empty observation map would clear the winner's propagation state if applied.
    assert!(matches!(
        store.commit_id_lists(
            Some(&base),
            staged,
            HashMap::new(),
            "Network",
            IdListPublicationMode::Replace,
            LOCK_TIMEOUT,
        ),
        Err(StatsigErr::InvalidOperation(_))
    ));
    assert!(Arc::ptr_eq(&winner, &store.load_data()));
    assert_eq!(store.get_current_id_list_metadata()["members"].size, 10);
    assert!(winner.id_lists["members"].ids.contains("CCCCCCCC"));
    assert!(store.id_list_propagation.lock().contains_key("members"));
    assert_eq!(store.config_updates.wait(Duration::ZERO), Some(false));
    assert!(discarded.upgrade().is_none());
    assert!(base["members"].ids.contains("AAAAAAAA"));
}

#[test]
fn size_gauges_follow_accepted_list_updates() {
    use crate::observability::ops_stats::{OpsStatsEvent, OpsStatsEventObserver};

    // Read the published OpsStats events synchronously to check their ordering.
    struct Observer;
    impl ObservabilityClient for Observer {
        fn init(&self) {}
        fn increment(&self, _: String, _: f64, _: Option<HashMap<String, String>>) {}
        fn gauge(&self, _: String, _: f64, _: Option<HashMap<String, String>>) {}
        fn dist(&self, _: String, _: f64, _: Option<HashMap<String, String>>) {}
        fn error(&self, _: String, _: String) {}
        fn should_enable_high_cardinality_for_this_tag(&self, _: String) -> Option<bool> {
            None
        }
        fn to_ops_stats_event_observer(self: Arc<Self>) -> Arc<dyn OpsStatsEventObserver> {
            self
        }
    }
    let observer: Arc<dyn ObservabilityClient> = Arc::new(Observer);
    let store = SpecStore::new(
        "list-size-publication",
        String::new(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&StatsigOptions {
            enable_id_list_access_metrics: Some(true),
            observability_client: Some(Arc::downgrade(&observer)),
            ..Default::default()
        }),
    );
    let mut events = store.ops_stats.subscribe_for_test();
    let mut sizes = || {
        let mut samples = Vec::new();
        while let Ok(event) = events.try_recv() {
            if let OpsStatsEvent::Observability(event) = event {
                if event.metric_name == "id_list_size" {
                    assert!(matches!(event.metric_type, MetricType::Gauge));
                    samples.push((event.tags.unwrap()["id_list_name"].clone(), event.value));
                }
            }
        }
        samples.sort_unstable_by(|a, b| a.0.cmp(&b.0));
        samples
    };

    store.did_receive_id_list_updates(HashMap::from([update("disabled", Some("+AAAAAAAA\n"))]));
    assert!(sizes().is_empty());
    store
        .global_configs
        .as_ref()
        .unwrap()
        .set_sdk_configs(HashMap::from([("id_list_access_metrics".into(), 1.into())]));
    store.did_receive_id_list_updates(HashMap::from([
        update("members", Some("+AAAAAAAA\n+BBBBBBBB\n")),
        update("empty", None),
    ]));
    assert_eq!(sizes(), [("empty".into(), 0.0), ("members".into(), 2.0)]);
    let base = store.load_data().id_lists.clone();
    // A shared manifest can rotate a URL or remove a list without changing membership.
    let mut members = base["members"].clone();
    members.metadata.url.push_str("?new-signature");
    store
        .did_receive_id_list_snapshot(
            HashMap::from([("members".into(), members.clone())]),
            HashMap::new(),
        )
        .unwrap();
    assert!(sizes().is_empty());

    // Even with the same file metadata, a newly installed body has a new size.
    Arc::make_mut(&mut members.ids).remove("BBBBBBBB");
    store
        .did_receive_id_list_snapshot(HashMap::from([("members".into(), members)]), HashMap::new())
        .unwrap();
    assert_eq!(sizes(), [("members".into(), 1.0)]);
    let stale = store.updated_id_lists(
        &base,
        HashMap::from([update("members", Some("+CCCCCCCC\n"))]),
        IdListPublicationMode::Replace,
        1,
    );
    assert!(matches!(
        store.commit_id_lists(
            Some(&base),
            stale,
            HashMap::new(),
            "Network",
            IdListPublicationMode::Replace,
            LOCK_TIMEOUT
        ),
        Err(StatsigErr::InvalidOperation(_))
    ));
    assert!(sizes().is_empty());
}

#[test]
fn concurrent_private_callbacks_preserve_independent_appends() {
    for format in [None, Some(true)] {
        check_concurrent_appends(store(format));
    }
}

fn check_concurrent_appends(store: SpecStore) {
    store.did_receive_id_list_updates(HashMap::from([update("a", None), update("b", None)]));
    let commit = store.update_lock.lock();
    std::thread::scope(|scope| {
        let first = scope.spawn(|| {
            store.did_receive_id_list_updates(HashMap::from([
                update("a", Some("+AAAAAAAA\n")),
                update("b", None),
            ]));
        });
        // Hold the first callback at commit. A second writer must still wait
        // before selecting the list snapshot to append to.
        let deadline = Instant::now() + LOCK_TIMEOUT;
        while !store.id_list_propagation.is_locked() {
            assert!(
                Instant::now() < deadline,
                "first callback did not reach publication"
            );
            std::thread::yield_now();
        }
        assert!(store.id_list_mutation.is_locked());
        let second = scope.spawn(|| {
            store.try_receive_id_list_updates_with_propagation(
                HashMap::from([update("a", None), update("b", Some("+BBBBBBBB\n"))]),
                HashMap::new(),
            )
        });
        drop(commit);
        first.join().unwrap();
        second.join().unwrap().unwrap();
    });
    let data = store.load_data();
    assert!(data.id_lists["a"].ids.contains("AAAAAAAA"));
    assert!(data.id_lists["b"].ids.contains("BBBBBBBB"));
    assert_eq!(data.id_lists["a"].metadata.size, 10);
    assert_eq!(data.id_lists["b"].metadata.size, 10);
}

#[tokio::test]
async fn id_list_lock_timeout_preserves_default_readiness_and_compact_retry() {
    std::thread::scope(|scope| {
        for flag in [None, Some(false), Some(true)] {
            let store = store(flag);
            scope.spawn(move || {
                let append = || HashMap::from([update("members", Some("+BBBBBBBB\n"))]);
                store.did_receive_id_list_updates(HashMap::from([update(
                    "members",
                    Some("+AAAAAAAA\n"),
                )]));
                let lock = store.update_lock.lock();
                let result =
                    store.try_receive_id_list_updates_with_propagation(append(), HashMap::new());
                if flag == Some(true) {
                    assert!(matches!(result, Err(StatsigErr::LockFailure(_))));
                } else {
                    result.unwrap();
                }
                assert_eq!(store.get_current_id_list_metadata()["members"].size, 10);
                drop(lock);
                store
                    .try_receive_id_list_updates_with_propagation(append(), HashMap::new())
                    .unwrap();
                assert_eq!(store.get_current_id_list_metadata()["members"].size, 20);
            });
        }
    });
}

#[test]
fn contended_hash_and_shared_writers_finish_without_publishing() {
    let hash = store(None);
    let shared = store(None);
    shared.did_receive_id_list_updates(HashMap::from([update("members", Some("+AAAAAAAA\n"))]));
    let (done, result) = std::sync::mpsc::channel();
    std::thread::scope(|scope| {
        let _mutation = hash.id_list_mutation.lock();
        let _propagation = shared.id_list_propagation.lock();
        scope.spawn(|| {
            hash.try_receive_id_list_updates_with_propagation(
                HashMap::from([update("members", Some("+AAAAAAAA\n"))]),
                HashMap::new(),
            )
            .unwrap();
            done.send(()).unwrap();
        });
        scope.spawn(|| {
            assert!(matches!(
                shared.did_receive_id_list_snapshot(HashMap::new(), HashMap::new()),
                Err(StatsigErr::LockFailure(_))
            ));
            done.send(()).unwrap();
        });
        // Release the guards even if a regression would otherwise hang the test.
        for _ in 0..2 {
            result
                .recv_timeout(LOCK_TIMEOUT * 2)
                .expect("writer did not respect the lock timeout");
        }
    });
    assert!(hash.get_current_id_list_metadata().is_empty());
    let data = shared.load_data();
    assert!(data.id_lists["members"].ids.contains("AAAAAAAA"));
}
