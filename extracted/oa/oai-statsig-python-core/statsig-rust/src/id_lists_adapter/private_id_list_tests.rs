use super::*;
use crate::id_lists_adapter::{
    IdList, IdListMetadata, IdListUpdate, IdListsUpdateListener, SharedIdListStore,
};
use crate::sdk_event_emitter::SdkEventEmitter;
use crate::{SpecStore, Statsig, StatsigOptions, StatsigRuntime};

fn metadata() -> IdListMetadata {
    IdListMetadata {
        name: "members".into(),
        url: String::new(),
        file_id: Some("generation-1".into()),
        size: 0,
        creation_time: 1,
    }
}

fn append(list: &mut IdList, body: &str) {
    list.apply_update_with_elias_fano(IdListUpdate {
        new_metadata: list.metadata.clone(),
        raw_changeset: Some(body.to_owned()),
    });
}

fn image(ids: &IdListIds) -> &Arc<IdListImage> {
    match &ids.storage {
        Storage::Image(image) => image,
        Storage::Pending(p) => image(&p.base),
        _ => panic!("expected an immutable base"),
    }
}

impl IdListIds {
    pub(crate) fn assert_private_format(&self, elias_fano: bool) {
        assert_eq!(self.has_compact_base(), elias_fano);
        assert_eq!(self.owned_capacities_for_test().is_some(), !elias_fano);
        assert_eq!(self.mapped_bytes(), 0);
    }
}

#[test]
fn equality_of_compact_lists_does_not_cache_borrowed_keys() {
    let mut list = IdList::new(metadata());
    append(&mut list, "+AAAAAAAA\n+BBBBBBBB\n");
    append(&mut list, "-BBBBBBBB\n+long-key!\n");
    assert!(image(&list.ids).is_compact());
    let mut expected = IdListIds::from(["AAAAAAAA".into(), "long-key!".into()]);
    assert_eq!(*list.ids, expected);
    expected.remove("AAAAAAAA");
    expected.insert_str("BBBBBBBB");
    assert_ne!(*list.ids, expected);
    assert!(!image(&list.ids).has_cached_iter_keys());
}

#[test]
fn private_sparse_batches_reverse_compact_and_preserve_pins() {
    let mut list = IdList::new(metadata());
    // 0..256 stay within the EF density bound. Variable-length additions
    // exercise the other partition and push the cumulative delta to its limit.
    let mut expected: HashSet<_> = (0..256).map(|i| format!("{i:08}")).collect();
    expected.extend(["long string".to_owned(), "!!!!bad!".to_owned()]);
    let body: String = expected.iter().map(|key| format!("+{key}\n")).collect();
    append(&mut list, &body);
    let initial = list.clone();
    assert!(image(&list.ids).is_compact());
    assert_eq!(list.ids.mapped_bytes(), 0);

    append(&mut list, "-00000000\n+é\n+é\n-absent\n");
    assert_eq!(list.ids.delta_len_for_test(), 2);
    let sparse = list.clone();
    append(&mut list, "+00000000\n-é\n");
    assert!(list.ids.pending().is_none());
    assert!(Arc::ptr_eq(image(&initial.ids), image(&list.ids)));

    let limit = batch_compaction_limits(expected.len()).0;
    let additions: String = (0..limit).map(|i| format!("+long {i}\n")).collect();
    append(&mut list, &additions);
    let at_limit = list.clone();
    assert_eq!(list.ids.delta_len_for_test(), limit);
    assert!(Arc::ptr_eq(image(&initial.ids), image(&list.ids)));
    append(&mut list, "-!!!!bad!\n");
    assert!(list.ids.pending().is_none());
    assert!(image(&list.ids).is_compact());
    assert!(!Arc::ptr_eq(image(&initial.ids), image(&list.ids)));
    expected.extend((0..limit).map(|i| format!("long {i}")));
    expected.remove("!!!!bad!");
    assert_eq!(list.ids.len(), expected.len());
    assert!(expected.iter().all(|key| list.ids.contains(key)));
    assert_eq!(
        list.ids.iter().map(str::to_owned).collect::<HashSet<_>>(),
        expected
    );
    assert!(initial.ids.contains("00000000") && !initial.ids.contains("é"));
    assert!(!sparse.ids.contains("00000000") && sparse.ids.contains("é"));
    assert!(at_limit.ids.contains("!!!!bad!") && at_limit.ids.contains("long 0"));
    assert!(!image(&initial.ids).has_cached_iter_keys());
}

#[test]
fn private_file_recreation_drops_the_overlay_and_resets_the_cursor() {
    let mut list = IdList::new(metadata());
    let initial = "+AAAAAAAA\n".repeat(1000);
    let delta = "+addition\n".repeat(1000);
    append(&mut list, &initial);
    append(&mut list, &delta);
    let pinned = list.clone();
    assert_eq!(pinned.metadata.size, (initial.len() + delta.len()) as u64);
    let mut next = metadata();
    next.file_id = Some("replacement".into());
    let adds = "+BBBBBBBB\n".repeat(1000);
    for (creation_time, body) in [(0, Some(adds.as_str())), (1, None)] {
        list.apply_update_with_elias_fano(IdListUpdate {
            new_metadata: IdListMetadata {
                creation_time,
                ..next.clone()
            },
            raw_changeset: body.map(str::to_owned),
        });
        assert!(Arc::ptr_eq(&list.ids, &pinned.ids));
        assert_eq!(list.metadata.size, pinned.metadata.size);
        assert_eq!(list.metadata.file_id, pinned.metadata.file_id);
    }
    let recreated = IdListMetadata {
        creation_time: 2,
        ..metadata()
    };
    for (next, body) in [
        (&next, adds.as_str()),
        (&recreated, adds.as_str()),
        (&next, ""),
    ] {
        let mut replacement = list.clone();
        replacement.apply_update_with_elias_fano(IdListUpdate {
            new_metadata: next.clone(),
            raw_changeset: Some(body.into()),
        });
        assert_eq!(replacement.metadata.file_id, next.file_id);
        assert_eq!(replacement.metadata.creation_time, next.creation_time);
        assert_eq!(replacement.metadata.size, body.len() as u64);
        assert_eq!(replacement.ids.len(), usize::from(!body.is_empty()));
        assert_eq!(replacement.ids.contains("BBBBBBBB"), !body.is_empty());
        assert!(!replacement.ids.contains("AAAAAAAA") && !replacement.ids.contains("addition"));
        assert!(replacement.ids.pending().is_none());
    }
    assert!(pinned.ids.contains("AAAAAAAA") && pinned.ids.contains("addition"));
}

#[test]
fn duplicate_private_appends_keep_the_overlay_and_advance_the_cursor() {
    let mut list = IdList::new(metadata());
    append(&mut list, "+AAAAAAAA\n+BBBBBBBB\n");
    append(&mut list, "-AAAAAAAA\n+addition\n");
    assert_eq!(list.ids.delta_len_for_test(), 2);
    let pinned = list.clone();
    for body in ["+addition\n", "-AAAAAAAA\n", "?ignored\n+  \n"] {
        let cursor = list.metadata.size;
        append(&mut list, body);
        assert!(Arc::ptr_eq(&pinned.ids, &list.ids));
        assert_eq!(list.metadata.size, cursor + body.len() as u64);
    }
    append(&mut list, "+addition\n-addition\n+addition\n+AAAAAAAA\n");
    assert!(list.ids.contains("addition") && list.ids.contains("AAAAAAAA"));
    assert!(!pinned.ids.contains("AAAAAAAA"));
}

#[test]
fn ineligible_private_image_survives_duplicate_and_unchanged_updates() {
    let mut list = IdList::new(metadata());
    append(&mut list, "+noncanonical\n+!!!!bad!\n");
    let first = list.clone();
    assert!(!image(&first.ids).is_compact());
    for body in ["", "+noncanonical\n", "-absent\n", "+sparse\n"] {
        append(&mut list, body);
        assert!(Arc::ptr_eq(image(&first.ids), image(&list.ids)));
    }
    assert_eq!(list.ids.delta_len_for_test(), 1);
}

fn update(body: &str) -> IdListUpdate {
    IdListUpdate {
        new_metadata: metadata(),
        raw_changeset: Some(body.into()),
    }
}

#[tokio::test]
async fn coexisting_sdk_instances_use_their_own_private_id_list_format() {
    let instances = [None, Some(true), Some(false)].map(|flag| {
        let options = StatsigOptions::builder()
            .enable_id_list_elias_fano(flag)
            .build();
        (
            flag,
            Statsig::new("private-policy", Some(Arc::new(options))),
        )
    });

    for (flag, sdk) in &instances {
        let store = sdk.get_context().spec_store;
        let enabled = flag.unwrap_or(false);
        assert_eq!(store.requires_blocking_id_list_publication(), enabled);
        store.did_receive_id_list_updates(HashMap::from([(
            "members".into(),
            update("+AAAAAAAA\n"),
        )]));
        let snapshot = store.load_data();
        let ids = &snapshot.id_lists["members"].ids;
        assert!(ids.contains("AAAAAAAA"));
        ids.assert_private_format(enabled);
    }
}

#[tokio::test]
async fn shared_publication_falls_back_to_the_instances_private_format() {
    for shared_elias_fano in [false, true] {
        check_shared_fallback(shared_elias_fano);
    }
}

fn check_shared_fallback(shared_elias_fano: bool) {
    let store = SpecStore::new(
        "private-policy",
        String::new(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&StatsigOptions {
            enable_id_list_elias_fano: Some(true),
            ..Default::default()
        }),
    );
    let mut staged = IdList::new(metadata());
    staged.apply_update_for_publish(update("+AAAAAAAA\n"));
    assert!(staged.ids.owned_capacities_for_test().is_some());
    let dir = tempfile::tempdir().unwrap();
    let writer =
        SharedIdListStore::new(dir.path(), "private-policy", "source", shared_elias_fano).unwrap();
    let lease = writer.try_acquire_lease().unwrap().unwrap();
    let catalog = writer
        .publish(
            &lease,
            &HashMap::from([("members".into(), staged)]),
            &HashMap::new(),
            1,
        )
        .unwrap();
    let shared = catalog.lists["members"].clone();
    assert!(shared.ids.is_mapped());
    assert_eq!(shared.ids.has_compact_base(), shared_elias_fano);
    store
        .did_receive_id_list_snapshot(catalog.lists, catalog.propagation)
        .unwrap();
    assert!(store.load_data().id_lists["members"].ids.is_mapped());

    // Private HTTP fallback resumes at the installed shared cursor.
    store.did_receive_id_list_updates(HashMap::from([("members".into(), update("+BBBBBBBB\n"))]));
    let snapshot = store.load_data();
    let private = &snapshot.id_lists["members"];
    assert_eq!(private.metadata.size, shared.metadata.size + 10);
    assert!(private.ids.has_compact_base() && private.ids.mapped_bytes() == 0);
    assert!(private.ids.contains("AAAAAAAA") && private.ids.contains("BBBBBBBB"));
    assert!(!shared.ids.contains("BBBBBBBB"));
}
