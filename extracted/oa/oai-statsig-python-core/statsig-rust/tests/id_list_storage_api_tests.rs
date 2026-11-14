use std::collections::{HashMap, HashSet};

use statsig_rust::evaluation::evaluator_context::IdListResolution;
use statsig_rust::{IdListManifest, IdListMetadata};

// Compile the migration example as a downstream crate. IdList is reached through
// the public resolver even though its defining module is private.
fn materialize_memberships(resolver: &IdListResolution<'_>) -> Vec<HashSet<String>> {
    match resolver {
        IdListResolution::MapLookup(lists) => lists
            .values()
            .map(|list| {
                let _member = list.ids.contains("AbCd1234");
                let _count = list.ids.len();
                list.ids.iter().map(str::to_owned).collect()
            })
            .collect(),
        IdListResolution::Callback(_) => Vec::new(),
    }
}

#[test]
fn inferred_id_list_storage_supports_the_migration_example() {
    let lists = HashMap::new();
    let resolver = IdListResolution::MapLookup(&lists);
    assert!(materialize_memberships(&resolver).is_empty());
}

#[test]
fn public_manifest_type_uses_the_sdk_wire_schema() {
    let row = r#"{"key":"embedded","url":"https://example.test/list","size":12,"creationTime":-1,"ts":"optional"}"#;
    let body = format!(r#"{{"canonical":{row}}}"#);
    let manifest: IdListManifest = serde_json::from_str(&body).unwrap();
    let metadata: &IdListMetadata = &manifest["canonical"].metadata;
    assert_eq!(metadata.name, "embedded");
    assert_eq!(metadata.file_id, None);
    assert_eq!(metadata.creation_time, -1);

    let duplicate_size = body.replace(r#""size":12"#, r#""size":0,"size":12"#);
    assert!(serde_json::from_str::<IdListManifest>(&duplicate_size).is_err());
    let malformed_row = format!(r#"{{"canonical":{row},"malformed":null}}"#);
    assert!(serde_json::from_str::<IdListManifest>(&malformed_row).is_err());
}
