//! Build-script entry point.  Reads `code-unit.schema.json` once into a
//! shared [`SchemaDoc`] and dispatches to one focused generator per
//! emitted file under `src/generated/`.  All generator-specific logic
//! lives in the sibling modules; this file only orchestrates.

use std::fs;
use std::path::Path;

mod file_path_fields;
mod output;
mod query_reference;
mod schema;
mod schema_constraints;
mod typify;
mod updated_at_paths;

use crate::file_path_fields::generate_file_path_fields;
use crate::output::{check_sibling_generated_files, write_generated};
use crate::query_reference::generate_query_reference;
use crate::schema::SchemaDoc;
use crate::schema_constraints::generate_schema_constraints;
use crate::typify::generate_with_typify;
use crate::updated_at_paths::generate_updated_at_paths;

fn main() {
    println!("cargo:rerun-if-changed=./schemas/code-unit.schema.json");
    println!("cargo:rerun-if-changed=./schemas/query-reference.tmpl");
    println!("cargo:rerun-if-changed=./schemas/query-reference.rs.tmpl");
    println!("cargo:rerun-if-changed=build");

    let schema_path = Path::new("./schemas/code-unit.schema.json");
    let out_dir = Path::new("src/generated");

    fs::create_dir_all(out_dir).expect("Failed to create generated directory");

    if !schema_path.exists() {
        panic!(
            "Schema file not found at {:?}. \
             Ensure schemas/code-unit.schema.json exists before building.",
            schema_path
        );
    }

    let schema_content =
        fs::read_to_string(schema_path).expect("Failed to read code-unit.schema.json");

    // Typify needs its own parse (schemars::schema::RootSchema), so it
    // still receives the raw string.
    let generated_code = generate_with_typify(&schema_content);
    write_generated(out_dir, "types.rs", &generated_code, "types");

    let doc = SchemaDoc::from_str(&schema_content);

    let query_template = fs::read_to_string("./schemas/query-reference.tmpl")
        .expect("Failed to read schemas/query-reference.tmpl");
    let query_rs_template = fs::read_to_string("./schemas/query-reference.rs.tmpl")
        .expect("Failed to read schemas/query-reference.rs.tmpl");

    write_generated(
        out_dir,
        "query_reference.rs",
        &generate_query_reference(&doc, &query_template, &query_rs_template),
        "query reference",
    );

    write_generated(
        out_dir,
        "updated_at_paths.rs",
        &generate_updated_at_paths(&doc),
        "updated_at_paths",
    );

    write_generated(
        out_dir,
        "file_path_fields.rs",
        &generate_file_path_fields(&doc),
        "file_path_fields",
    );

    write_generated(
        out_dir,
        "schema_constraints.rs",
        &generate_schema_constraints(&doc),
        "schema_constraints",
    );

    check_sibling_generated_files();
}
