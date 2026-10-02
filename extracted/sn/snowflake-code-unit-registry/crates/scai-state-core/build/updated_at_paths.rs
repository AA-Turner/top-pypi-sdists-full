//! Walks the JSON Schema for parent paths of every `updatedAt` property
//! and emits them as `UPDATED_AT_PARENT_PATHS` in
//! `src/generated/updated_at_paths.rs`.

use crate::output::render_path_constant;
use crate::schema::{walk_object_tree, SchemaDoc};

pub fn generate_updated_at_paths(doc: &SchemaDoc) -> String {
    let mut parent_paths: Vec<Vec<String>> = Vec::new();

    walk_object_tree(doc, &[], &doc.root, &mut |path, _node| {
        if path.last().map(|s| s.as_str()) == Some("updatedAt") {
            parent_paths.push(path[..path.len() - 1].to_vec());
        }
    });

    parent_paths.sort();
    render_path_constant(
        "UPDATED_AT_PARENT_PATHS",
        "// Parent paths of all `updatedAt` properties in code-unit.schema.json",
        &parent_paths,
    )
}
