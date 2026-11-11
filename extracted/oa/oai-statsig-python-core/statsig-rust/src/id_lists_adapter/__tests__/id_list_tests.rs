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
        UpdateMode::Private(IdListEncoding::Hash),
        UpdateMode::Private(IdListEncoding::EliasFano),
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

#[test]
fn resident_membership_uses_sdk_storage_for_uniform_and_dense_lists() {
    use crate::portable_id_list_ef::packed;

    let key = |rank| String::from_utf8(packed::encode(rank).to_vec()).unwrap();
    for (stride, expect_ef) in [(1 << 36, true), (1, false)] {
        let body: String = (0..1200)
            .map(|i| format!("+{}\n", key(i * stride)))
            .collect();
        let mut resident = IdListMembership::default();
        let mut local = IdList::new(metadata());
        let name = local.metadata.name.clone();
        let last = key(1199 * stride);
        let replacement = key((1 << 48) - 1);
        for changes in [&body, &format!("-{last}\r\n\n+{replacement}")] {
            resident.apply(&name, changes.as_bytes()).unwrap();
            local.apply_update_with_encoding(
                IdListEncoding::EliasFano,
                IdListUpdate {
                    raw_changeset: Some(changes.to_owned()),
                    new_metadata: local.metadata.clone(),
                },
            );
            assert_eq!(local.ids.has_compact_base(), expect_ef);
            assert_eq!(resident.ids.has_compact_base(), expect_ef);
            assert_eq!(*resident.ids, *local.ids);
        }
        assert!(!resident.contains(&last));
        assert!(resident.contains(&replacement));
    }
}

#[test]
fn resident_membership_rejects_invalid_changes_atomically_and_preserves_clones() {
    use crate::hashing::{HashUtil, IdListFingerprintWidth::Bits48};

    let key = HashUtil::new().id_list_key("alice", Bits48);
    assert_eq!(key, "K9gGyX8O");
    let mut list = IdListMembership::default();
    list.apply("employees", format!("+{key}").into_bytes())
        .unwrap();
    let original = list.clone();

    for invalid in [
        b"?AAAAAAAA".as_slice(),
        b"+short",
        b"+AAAAAAAAA",
        b"+GTejfAo5NJE",            // 64-bit fingerprint
        b"+GTejfAo5NJF+jVDrddBJGA", // 128-bit fingerprint
        b"+!!!!!!!!",
        b"+\xff",
    ] {
        let mut changes = format!("-{key}\n").into_bytes();
        changes.extend_from_slice(invalid);
        for input in [
            Cow::Borrowed(changes.as_slice()),
            Cow::Owned(changes.clone()),
        ] {
            assert_eq!(
                list.apply("employees", input).unwrap_err().kind(),
                io::ErrorKind::InvalidData
            );
            assert!(Arc::ptr_eq(&list.ids, &original.ids));
            assert!(list.contains(&key));
        }
    }

    list.apply("employees", format!("-{key}").as_bytes())
        .unwrap();
    assert!(!list.contains(&key));
    assert!(original.contains(&key));
}

#[test]
fn ordinary_file_updates_share_membership_until_an_append_or_replacement_is_valid() {
    let first = IdListFileVersion {
        file_id: Some("F"),
        creation_time: 1,
        size: 10,
    };
    let first_body = b"+AAAAAAAB\n";
    let full = first.update_from(None).unwrap();
    let original = full.apply_to_membership("ids", None, first_body).unwrap();
    assert!(original.contains("AAAAAAAB"));
    assert!(first.update_from(Some(first)).is_none());

    let larger = IdListFileVersion { size: 20, ..first };
    let append = larger.update_from(Some(first)).unwrap();
    // Ignore both the previously installed prefix and bytes beyond the manifest.
    let body = b"ignored123+AAAAAAAC\n+AAAAAAAD\n";
    let updated = append
        .apply_to_membership("ids", Some(&original), body)
        .unwrap();
    assert!(updated.contains("AAAAAAAB"));
    assert!(updated.contains("AAAAAAAC"));
    assert!(!updated.contains("AAAAAAAD"));
    assert!(!original.contains("AAAAAAAC"));
    assert!(first.update_from(Some(larger)).is_none());

    assert!(append.apply_to_membership("ids", None, body).is_err());
    assert!(
        append
            .apply_to_membership("ids", Some(&original), first_body)
            .is_err()
    );
    for replacement in [
        IdListFileVersion {
            file_id: Some("G"),
            size: 0,
            ..larger
        },
        IdListFileVersion {
            creation_time: 2,
            size: 0,
            ..larger
        },
    ] {
        let empty = replacement
            .update_from(Some(larger))
            .unwrap()
            .apply_to_membership("ids", Some(&updated), &[])
            .unwrap();
        assert!(!empty.contains("AAAAAAAB"));
        assert!(!empty.contains("AAAAAAAC"));
    }

    let stale = IdListFileVersion {
        creation_time: 0,
        file_id: Some("older"),
        ..larger
    };
    assert!(stale.update_from(Some(first)).is_none());
}
