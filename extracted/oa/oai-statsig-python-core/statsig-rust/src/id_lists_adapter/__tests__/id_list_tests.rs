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
