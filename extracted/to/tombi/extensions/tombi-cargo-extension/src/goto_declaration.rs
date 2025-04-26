use itertools::Itertools;
use tombi_config::TomlVersion;
use tower_lsp::lsp_types::{Location, TextDocumentIdentifier};

use crate::get_workspace_cargo_toml_location;

pub async fn goto_declaration(
    text_document: &TextDocumentIdentifier,
    keys: &[tombi_document_tree::Key],
    toml_version: TomlVersion,
) -> Result<Option<Location>, tower_lsp::jsonrpc::Error> {
    // Check if current file is Cargo.toml
    if !text_document.uri.path().ends_with("Cargo.toml") {
        return Ok(None);
    }
    let Some(cargo_toml_path) = text_document.uri.to_file_path().ok() else {
        return Ok(None);
    };

    let keys = keys.iter().map(|key| key.value()).collect_vec();
    let keys = keys.as_slice();

    if keys.last() != Some(&"workspace") {
        get_workspace_cargo_toml_location(keys, &cargo_toml_path, toml_version, false)
    } else {
        Ok(None)
    }
}
