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
    let store = store(Some(true));
    store.did_receive_id_list_updates(HashMap::from([
        update("kept", Some("+AAAAAAAA\n")),
        update("removed", Some("+obsolete\n")),
    ]));
    let base = store.load_data().id_lists.clone();
    let staged = store.updated_id_lists(
        &base,
        HashMap::from([update("kept", Some("+BBBBBBBB\n"))]),
        IdListPublicationMode::Replace,
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
        .publish_staged_id_lists(
            &base,
            staged,
            HashMap::new(),
            IdListPublicationMode::Replace,
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
    let store = store(Some(true));
    store.did_receive_id_list_updates(HashMap::from([update("members", Some("+AAAAAAAA\n"))]));
    let base = store.load_data().id_lists.clone();
    let staged = store.updated_id_lists(
        &base,
        HashMap::from([update("members", Some("+BBBBBBBB\n"))]),
        IdListPublicationMode::Replace,
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
        store.publish_staged_id_lists(
            &base,
            staged,
            HashMap::new(),
            IdListPublicationMode::Replace
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
fn concurrent_private_callbacks_preserve_independent_appends() {
    let store = store(Some(true));
    store.did_receive_id_list_updates(HashMap::from([update("a", None), update("b", None)]));
    let base = store.load_data().id_lists.clone();
    let owners = Arc::strong_count(&base);
    let commit = store.update_lock.lock();
    std::thread::scope(|scope| {
        let first = scope.spawn(|| {
            store.did_receive_id_list_updates(HashMap::from([
                update("a", Some("+AAAAAAAA\n")),
                update("b", None),
            ]));
        });
        // Stop the first callback between pinning its base and committing. The next
        // callback must still wait to select its base, even if it uses the other hook.
        let deadline = Instant::now() + LOCK_TIMEOUT;
        while Arc::strong_count(&base) == owners {
            assert!(
                Instant::now() < deadline,
                "first callback did not pin the catalog"
            );
            std::thread::yield_now();
        }
        assert!(store.private_id_list_mutation.as_ref().unwrap().is_locked());
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
