//! Walks the JSON Schema for string properties whose description starts
//! with "Repo-root-relative" and emits them as `FILE_PATH_FIELDS` in
//! `src/generated/file_path_fields.rs`.

use crate::output::render_path_constant;
use crate::schema::{walk_object_tree, SchemaDoc};

pub fn generate_file_path_fields(doc: &SchemaDoc) -> String {
    let mut paths: Vec<Vec<String>> = Vec::new();

    walk_object_tree(doc, &[], &doc.root, &mut |path, node| {
        if doc.node_type(node) == "string" {
            if let Some(desc) = node.get("description").and_then(|d| d.as_str()) {
                if desc.starts_with("Repo-root-relative") {
                    paths.push(path.to_vec());
                }
            }
        }
    });

    paths.sort();
    render_path_constant(
        "FILE_PATH_FIELDS",
        "// Segment paths of all file path properties in code-unit.schema.json",
        &paths,
    )
}
