use std::collections::HashSet;
use std::sync::Arc;

use super::{IdList, IdListIds, IdListMetadata, IdListUpdate};

fn metadata(file: &str, creation_time: i64) -> IdListMetadata {
    IdListMetadata {
        name: "members".to_owned(),
        url: "https://example.com/members".to_owned(),
        file_id: Some(file.to_owned()),
        size: 999,
        creation_time,
    }
}

#[test]
fn membership_and_iteration_preserve_exact_strings() {
    let values = [
        "AbCd1234",
        "abcd1234",
        "abcdefg",
        "abcdefghi",
        "",
        "éééé",
        "🦀🦀",
        "a b c d ",
    ];
    let expected: HashSet<&str> = values.into_iter().collect();
    let mut ids = IdListIds::new();
    assert!(ids.is_empty());
    for value in values {
        assert!(ids.insert_str(value));
        assert!(!ids.insert(value.to_owned()));
        assert!(ids.contains(value));
    }
    assert_eq!(ids.len(), expected.len());
    assert_eq!(ids.iter().collect::<HashSet<_>>(), expected);
    assert!(!ids.contains("ABCD1234"));
    assert!(!ids.contains("abcdefgh"));

    let from_owned: IdListIds = values.map(str::to_owned).into_iter().collect();
    assert_eq!(from_owned, ids);
    assert_eq!(IdListIds::from(values.map(str::to_owned)), ids);

    for value in values {
        assert!(ids.remove(value));
        assert!(!ids.remove(value));
        assert!(!ids.contains(value));
    }
    assert!(ids.is_empty());
    assert_eq!(ids.iter().count(), 0);
}

#[test]
fn updates_preserve_parser_membership_and_byte_cursor() {
    let mut list = IdList::new(metadata("v1", 1));
    assert_eq!(list.metadata.size, 0);
    let first = "+AbCd1234\r\n+short\n+longer-than-eight\n+éééé\n+🦀🦀\n+ trailing \n\n+\n-\nignored\n +ignored\n";
    list.apply_update(IdListUpdate {
        new_metadata: metadata("v1", 1),
        raw_changeset: Some(first.to_owned()),
    });
    assert_eq!(
        list.ids.iter().collect::<HashSet<_>>(),
        HashSet::from([
            "AbCd1234",
            "short",
            "longer-than-eight",
            "éééé",
            "🦀🦀",
            " trailing "
        ])
    );
    assert_eq!(list.metadata.size, first.len() as u64);

    let delta = "-AbCd1234\n-short\n-éééé\n-missing\n+longer-than-eight\n+abcd1234\n";
    list.apply_update(IdListUpdate {
        new_metadata: metadata("v1", 1),
        raw_changeset: Some(delta.to_owned()),
    });
    assert_eq!(
        list.ids.iter().collect::<HashSet<_>>(),
        HashSet::from(["longer-than-eight", "🦀🦀", " trailing ", "abcd1234"])
    );
    assert_eq!(list.metadata.size, (first.len() + delta.len()) as u64);
}

#[test]
fn updates_ignore_multibyte_operators_and_preserve_byte_cursor() {
    let mut list = IdList::new(metadata("v1", 1));
    let initial = "+Remove01\n";
    list.apply_update(IdListUpdate {
        new_metadata: metadata("v1", 1),
        raw_changeset: Some(initial.to_owned()),
    });

    let delta = "\n \t\r\n+\n-\néignored\n+AbCd1234\n中ignored\n+éééé\n🦀ignored\n-Remove01\n";
    list.apply_update(IdListUpdate {
        new_metadata: metadata("v1", 1),
        raw_changeset: Some(delta.to_owned()),
    });

    assert_eq!(
        list.ids.iter().collect::<HashSet<_>>(),
        HashSet::from(["AbCd1234", "éééé"])
    );
    assert_eq!(list.metadata.size, (initial.len() + delta.len()) as u64);
}

#[test]
fn updates_keep_unchanged_snapshots_shared_and_changed_snapshots_isolated() {
    let mut original = IdList::new(metadata("v1", 1));
    original.apply_update(IdListUpdate {
        new_metadata: metadata("v1", 1),
        raw_changeset: Some("+AbCd1234\n+fallback\n+longer-than-eight\n".to_owned()),
    });
    let mut updated = original.clone();
    updated.apply_update(IdListUpdate {
        new_metadata: metadata("v1", 1),
        raw_changeset: None,
    });
    assert!(Arc::ptr_eq(&original.ids, &updated.ids));

    updated.apply_update(IdListUpdate {
        new_metadata: metadata("v1", 1),
        raw_changeset: Some("-AbCd1234\n-longer-than-eight\n+abcd1234\n+new-fallback\n".to_owned()),
    });
    assert!(!Arc::ptr_eq(&original.ids, &updated.ids));
    assert_eq!(
        original.ids.iter().collect::<HashSet<_>>(),
        HashSet::from(["AbCd1234", "fallback", "longer-than-eight"])
    );
    assert_eq!(
        updated.ids.iter().collect::<HashSet<_>>(),
        HashSet::from(["abcd1234", "fallback", "new-fallback"])
    );
}

#[test]
fn newer_file_resets_membership_and_size_without_changing_old_snapshot() {
    let mut list = IdList::new(metadata("v1", 1));
    list.apply_update(IdListUpdate {
        new_metadata: metadata("v1", 1),
        raw_changeset: Some("+AbCd1234\n+longer-than-eight\n".to_owned()),
    });
    let previous = list.clone();
    let replacement = "+NewKey00\n+new-fallback\n";
    list.apply_update(IdListUpdate {
        new_metadata: metadata("v2", 2),
        raw_changeset: Some(replacement.to_owned()),
    });
    assert_eq!(list.metadata.file_id.as_deref(), Some("v2"));
    assert_eq!(list.metadata.creation_time, 2);
    assert_eq!(list.metadata.size, replacement.len() as u64);
    assert_eq!(
        list.ids.iter().collect::<HashSet<_>>(),
        HashSet::from(["NewKey00", "new-fallback"])
    );
    assert!(previous.ids.contains("AbCd1234"));
    assert!(previous.ids.contains("longer-than-eight"));
    assert!(!previous.ids.contains("NewKey00"));

    list.apply_update(IdListUpdate {
        new_metadata: metadata("v3", 3),
        raw_changeset: Some(String::new()),
    });
    assert_eq!(list.metadata.size, 0);
    assert!(list.ids.is_empty());
}

#[test]
fn serialized_id_list_still_contains_only_metadata() {
    let mut list = IdList::new(metadata("v1", 1));
    list.apply_update(IdListUpdate {
        new_metadata: metadata("v1", 1),
        raw_changeset: Some("+AbCd1234\n+longer-than-eight\n".to_owned()),
    });
    assert_eq!(
        serde_json::to_value(&list).unwrap(),
        serde_json::json!({"metadata": serde_json::to_value(&list.metadata).unwrap()})
    );
}
