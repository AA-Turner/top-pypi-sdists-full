use std::collections::{HashMap, HashSet};

use statsig_rust::evaluation::evaluator_context::IdListResolution;

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
