use super::*;
use crate::SpecStore;
use crate::id_lists_adapter::IdList;
use crate::sdk_event_emitter::SdkEventEmitter;
use mockito::Server;
use std::collections::HashSet;

fn metadata() -> IdListMetadata {
    IdListMetadata {
        name: "employees".into(),
        url: "https://example.com/employees".into(),
        file_id: Some("file-1".into()),
        size: 0,
        creation_time: 1,
    }
}

#[test]
fn same_file_and_creation_time_appends_changes() {
    let mut list = IdList::new(metadata());
    list.apply_update(IdListUpdate {
        raw_changeset: Some("+alice\n+bob\n".to_string()),
        new_metadata: metadata(),
    });
    list.apply_update(IdListUpdate {
        raw_changeset: Some("-alice\n+carol\n".to_string()),
        new_metadata: metadata(),
    });

    assert_eq!(
        *list.ids,
        HashSet::from(["bob".to_string(), "carol".to_string()])
    );
    assert_eq!(
        list.metadata.size,
        "+alice\n+bob\n-alice\n+carol\n".len() as u64
    );
}

#[test]
fn new_file_at_same_or_newer_creation_time_replaces_members_and_cursor() {
    for creation_time in [1, 2] {
        let mut list = IdList::new(metadata());
        list.apply_update(IdListUpdate {
            raw_changeset: Some("+alice\n".to_string()),
            new_metadata: metadata(),
        });
        let mut replacement = metadata();
        replacement.file_id = Some("file-2".to_string());
        replacement.creation_time = creation_time;
        list.apply_update(IdListUpdate {
            raw_changeset: Some("+bob\n".to_string()),
            new_metadata: replacement,
        });

        assert_eq!(*list.ids, HashSet::from(["bob".to_string()]));
        assert_eq!(list.metadata.size, "+bob\n".len() as u64);
        assert_eq!(list.metadata.file_id.as_deref(), Some("file-2"));
        assert_eq!(list.metadata.creation_time, creation_time);
    }
}

#[test]
fn missing_body_preserves_members_cursor_and_generation() {
    for file_id in ["file-1", "file-2"] {
        let mut list = IdList::new(metadata());
        list.apply_update(IdListUpdate {
            raw_changeset: Some("+alice\n".into()),
            new_metadata: metadata(),
        });
        let previous = list.clone();
        let mut next = metadata();
        next.file_id = Some(file_id.into());
        next.creation_time = 2;
        list.apply_update(IdListUpdate {
            raw_changeset: None,
            new_metadata: next,
        });
        assert_eq!(*list.ids, *previous.ids);
        assert!(Arc::ptr_eq(&list.ids, &previous.ids));
        assert_eq!(list.metadata.creation_time, previous.metadata.creation_time);
        assert_eq!(list.metadata.file_id, previous.metadata.file_id);
        assert_eq!(list.metadata.size, previous.metadata.size);
    }
}

#[test]
fn same_file_full_replay_can_replace_members_with_an_empty_set() {
    let mut list = IdList::new(metadata());
    list.apply_update(IdListUpdate {
        raw_changeset: Some("+alice\n".into()),
        new_metadata: metadata(),
    });
    let previous = list.clone();
    let mut next = metadata();
    next.creation_time = 2;
    list.apply_update(IdListUpdate {
        raw_changeset: Some(String::new()),
        new_metadata: next,
    });
    assert!(list.ids.is_empty());
    assert_eq!(list.metadata.creation_time, 2);
    assert_eq!(list.metadata.size, 0);
    assert!(previous.ids.contains("alice"));
}

#[tokio::test]
async fn test_same_file_full_replay_updates_cursor_and_only_downloads_once() {
    let mut server = Server::new_async().await;
    let list_name = "employees";
    let initial_body = "+alice\n+bob\n";
    let full_body = "+alice\n+bob\n-alice\n+carol\n";
    let appended_body = "+dan\n";
    let mut metadata = IdListMetadata {
        name: list_name.to_string(),
        url: format!("{}/employees", server.url()),
        file_id: Some("file-a".to_string()),
        size: initial_body.len() as u64,
        creation_time: 1,
    };
    let listener = Arc::new(SpecStore::new(
        "secret-cursor-test",
        "cursor-test".into(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    ));
    // Seed the overcounted cursor left by repeated full replays in an older SDK.
    listener.did_receive_id_list_updates(HashMap::from([(
        list_name.to_string(),
        IdListUpdate {
            raw_changeset: Some(initial_body.repeat(3)),
            new_metadata: metadata.clone(),
        },
    )]));
    let original = listener.load_data();
    assert_eq!(
        original.id_lists[list_name].metadata.size,
        3 * initial_body.len() as u64
    );
    let adapter = StatsigHttpIdListsAdapter::new(
        "secret-key",
        &StatsigOptions {
            id_lists_url: Some(format!("{}/get_id_lists", server.url())),
            ..StatsigOptions::default()
        },
    );
    adapter.set_listener(listener.clone());

    metadata.creation_time = 2;
    metadata.size = full_body.len() as u64;
    let manifest = server
        .mock("POST", "/get_id_lists")
        .with_status(200)
        .with_body(serde_json::to_string(&HashMap::from([(list_name, &metadata)])).unwrap())
        .expect(2)
        .create_async()
        .await;
    let full_download = server
        .mock("GET", "/employees")
        .match_header("range", "bytes=0-")
        .with_status(206)
        .with_body(full_body)
        .expect(1)
        .create_async()
        .await;

    adapter.sync_id_lists().await.unwrap();
    adapter.sync_id_lists().await.unwrap();

    manifest.assert_async().await;
    full_download.assert_async().await;
    let current = listener.get_current_id_list_metadata();
    assert_eq!(current[list_name].creation_time, 2);
    assert_eq!(current[list_name].size, full_body.len() as u64);
    assert!(
        !listener.load_data().id_lists[list_name]
            .ids
            .contains("alice")
    );
    assert!(listener.load_data().id_lists[list_name].ids.contains("bob"));
    assert!(
        listener.load_data().id_lists[list_name]
            .ids
            .contains("carol")
    );

    assert!(original.id_lists[list_name].ids.contains("alice"));
    assert!(!original.id_lists[list_name].ids.contains("carol"));
    let replayed = listener.load_data();

    // With unchanged creationTime, subsequent growth must read just the tail.
    manifest.remove_async().await;
    metadata.size += appended_body.len() as u64;
    let manifest = server
        .mock("POST", "/get_id_lists")
        .with_status(200)
        .with_body(serde_json::to_string(&HashMap::from([(list_name, &metadata)])).unwrap())
        .expect(1)
        .create_async()
        .await;
    let tail_download = server
        .mock("GET", "/employees")
        .match_header("range", format!("bytes={}-", full_body.len()).as_str())
        .with_status(206)
        .with_body(appended_body)
        .expect(1)
        .create_async()
        .await;

    adapter.sync_id_lists().await.unwrap();

    manifest.assert_async().await;
    tail_download.assert_async().await;
    full_download.assert_async().await;
    assert_eq!(
        listener.get_current_id_list_metadata()[list_name].size,
        metadata.size
    );
    assert!(listener.load_data().id_lists[list_name].ids.contains("dan"));
    assert!(listener.load_data().id_lists[list_name].ids.contains("bob"));
    assert!(
        !listener.load_data().id_lists[list_name]
            .ids
            .contains("alice")
    );
    assert!(!replayed.id_lists[list_name].ids.contains("dan"));
}
