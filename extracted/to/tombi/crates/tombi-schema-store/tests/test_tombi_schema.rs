use std::path::PathBuf;

use tombi_schema_store::{DocumentSchema, SchemaUrl};

fn project_root_path() -> Result<PathBuf, Box<dyn std::error::Error>> {
    let cargo_manifest_dir = std::path::PathBuf::from(std::env::var("CARGO_MANIFEST_DIR")?);

    if cargo_manifest_dir.ends_with("tombi-schema-store") {
        Ok(cargo_manifest_dir
            .parent()
            .unwrap()
            .parent()
            .unwrap()
            .to_path_buf())
    } else {
        Ok(cargo_manifest_dir)
    }
}

#[test]
fn tombi_schema() -> Result<(), Box<dyn std::error::Error>> {
    use std::{
        fs::File,
        io::{BufReader, Read},
    };

    let document_path = project_root_path()?.join("tombi.schema.json");
    let file = File::open(&document_path)?;
    let mut reader = BufReader::new(file);

    let mut contents = String::new();
    reader.read_to_string(&mut contents)?;

    let value_node = tombi_json::ValueNode::from_str(&contents)?;
    let object = match value_node {
        tombi_json::ValueNode::Object(object) => object,
        _ => {
            return Err(Box::new(tombi_schema_store::Error::SchemaMustBeObject {
                schema_url: SchemaUrl::from_file_path(&document_path).unwrap(),
            }));
        }
    };

    let document_schema =
        DocumentSchema::new(object, SchemaUrl::from_file_path(&document_path).unwrap());

    dbg!(document_schema);
    Ok(())
}
