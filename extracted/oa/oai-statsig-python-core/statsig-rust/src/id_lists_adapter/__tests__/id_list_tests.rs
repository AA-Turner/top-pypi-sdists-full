use super::*;

fn metadata() -> IdListMetadata {
    IdListMetadata {
        name: "employees".to_string(),
        url: "https://example.com/employees".to_string(),
        file_id: Some("file-1".to_string()),
        size: 0,
        creation_time: 1,
    }
}

#[test]
fn cloned_list_copies_ids_only_when_updated() {
    let mut original = IdList::new(metadata());
    original.apply_update(IdListUpdate {
        raw_changeset: Some("+alice".to_string()),
        new_metadata: metadata(),
    });

    let mut updated = original.clone();
    assert!(Arc::ptr_eq(&original.ids, &updated.ids));

    updated.apply_update(IdListUpdate {
        raw_changeset: Some("+bob".to_string()),
        new_metadata: metadata(),
    });

    assert!(!Arc::ptr_eq(&original.ids, &updated.ids));
    assert!(original.ids.contains("alice"));
    assert!(!original.ids.contains("bob"));
    assert!(updated.ids.contains("alice"));
    assert!(updated.ids.contains("bob"));
}

#[test]
fn update_modes_preserve_id_whitespace_and_consume_ignored_lines() {
    let body = "+  member  \r\n+member\n-member\n+\t\n-\u{2003}\n +ignored\nλignored\n+é \n";
    for mode in [
        UpdateMode::PrivateHash,
        UpdateMode::PrivateEliasFano,
        UpdateMode::SharedPublisher,
    ] {
        let mut list = IdList::new(metadata());
        list.apply_update_inner(
            IdListUpdate {
                raw_changeset: Some(body.into()),
                new_metadata: metadata(),
            },
            mode,
        );
        assert_eq!(list.metadata.size, body.len() as u64);
        assert_eq!(list.ids.len(), 2);
        assert!(list.ids.contains("  member  "));
        assert!(list.ids.contains("é "));
    }
}
