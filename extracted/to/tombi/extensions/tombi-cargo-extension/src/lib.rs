mod goto_declaration;
mod goto_definition;

pub use goto_declaration::goto_declaration;
pub use goto_definition::goto_definition;
use itertools::Itertools;
use tombi_ast::AstNode;
use tombi_config::TomlVersion;
use tombi_document_tree::{TryIntoDocumentTree, ValueImpl};
use tower_lsp::lsp_types::{Location, Url};

fn load_cargo_toml(
    cargo_toml_path: &std::path::Path,
    toml_version: TomlVersion,
) -> Option<tombi_document_tree::DocumentTree> {
    let Some(toml_text) = std::fs::read_to_string(cargo_toml_path).ok() else {
        return None;
    };

    let Some(root) = tombi_ast::Root::cast(tombi_parser::parse(&toml_text).into_syntax_node())
    else {
        return None;
    };

    root.try_into_document_tree(toml_version).ok()
}

fn find_workspace_cargo_toml(
    cargo_toml_path: &std::path::Path,
    toml_version: TomlVersion,
) -> Option<(std::path::PathBuf, tombi_document_tree::DocumentTree)> {
    let Some(mut current_dir) = cargo_toml_path.parent() else {
        return None;
    };

    while let Some(target_dir) = current_dir.parent() {
        current_dir = target_dir;
        let workspace_cargo_toml_path = current_dir.join("Cargo.toml");

        if workspace_cargo_toml_path.exists() {
            let Some(document_tree) = load_cargo_toml(&workspace_cargo_toml_path, toml_version)
            else {
                continue;
            };

            if document_tree.contains_key("workspace") {
                return Some((workspace_cargo_toml_path, document_tree));
            };
        }
    }

    None
}

fn get_subcrate_cargo_toml(
    workspace_cargo_toml_path: &std::path::Path,
    subcrate_path: &std::path::Path,
    toml_version: TomlVersion,
) -> Option<(std::path::PathBuf, tombi_document_tree::DocumentTree)> {
    let mut subcrate_path = subcrate_path.to_path_buf();
    if !subcrate_path.is_absolute() {
        if let Some(workspace_dir) = workspace_cargo_toml_path.parent() {
            subcrate_path = workspace_dir.join(subcrate_path);
        }
    }

    let subcrate_cargo_toml_path = subcrate_path.join("Cargo.toml");
    if !subcrate_cargo_toml_path.exists() {
        return None;
    }

    let Some(document_tree) = load_cargo_toml(&subcrate_cargo_toml_path, toml_version) else {
        return None;
    };

    Some((subcrate_cargo_toml_path, document_tree))
}

/// Get the location of the workspace Cargo.toml.
///
/// ```toml
/// [project]
/// name = "my_project"
/// version = { workspace = true }
///
/// [dependencies]
/// tombi-ast = { workspace = true }
/// ```
fn get_workspace_cargo_toml_location(
    keys: &[&str],
    cargo_toml_path: &std::path::Path,
    toml_version: TomlVersion,
    jump_to_subcrate: bool,
) -> Result<Option<Location>, tower_lsp::jsonrpc::Error> {
    assert!(matches!(keys.last(), Some(&"workspace")));

    let Some((workspace_cargo_toml_path, workspace_cargo_toml_document_tree)) =
        find_workspace_cargo_toml(cargo_toml_path, toml_version)
    else {
        return Ok(None);
    };

    let keys = {
        let mut sanitized_keys = vec![sanitize_dependency_key(keys[0])];
        sanitized_keys.extend(keys[1..].iter());
        sanitized_keys
    };

    let Some((key, value)) = tombi_document_tree::dig_keys(
        &workspace_cargo_toml_document_tree,
        &std::iter::once("workspace")
            .chain(keys[..keys.len() - 1].iter().copied())
            .collect_vec(),
    ) else {
        return Ok(None);
    };

    if jump_to_subcrate
        && matches!(
            keys.first(),
            Some(&"dependencies" | &"dev-dependencies" | &"build-dependencies")
        )
    {
        if let tombi_document_tree::Value::Table(table) = value {
            if let Some(tombi_document_tree::Value::String(subcrate_path)) = table.get("path") {
                if let Some((subcrate_cargo_toml_path, _)) = get_subcrate_cargo_toml(
                    &workspace_cargo_toml_path,
                    std::path::Path::new(subcrate_path.value()),
                    toml_version,
                ) {
                    return Ok(Some(Location::new(
                        Url::from_file_path(subcrate_cargo_toml_path).unwrap(),
                        tombi_text::Range::default().into(),
                    )));
                }
            }
        }
    }

    let Ok(workspace_cargo_toml_uri) = Url::from_file_path(&workspace_cargo_toml_path) else {
        return Ok(None);
    };

    Ok(Some(Location::new(
        workspace_cargo_toml_uri,
        key.range().into(),
    )))
}

/// Get the location of the crate path in the workspace.
///
/// ```toml
/// [workspace.dependencies]
/// tombi-ast = { path = "crates/tombi-ast" }
/// ```
fn get_dependencies_crate_path_location(
    keys: &[&str],
    cargo_toml_path: &std::path::Path,
    toml_version: TomlVersion,
) -> Result<Option<Location>, tower_lsp::jsonrpc::Error> {
    assert!(matches!(
        keys,
        ["workspace", "dependencies", _, "path"]
            | [
                "dependencies" | "dev-dependencies" | "build-dependencies",
                _,
                "path"
            ]
    ));

    let Some(document_tree) = load_cargo_toml(cargo_toml_path, toml_version) else {
        return Ok(None);
    };

    let Some((_, value)) = tombi_document_tree::dig_keys(&document_tree, keys) else {
        return Ok(None);
    };

    if value.value_type() == tombi_document_tree::ValueType::String {
        let subcrate_path = match value {
            tombi_document_tree::Value::String(path) => path,
            _ => unreachable!(),
        };

        if let Some((subcrate_cargo_toml_path, _)) = get_subcrate_cargo_toml(
            &cargo_toml_path,
            std::path::Path::new(subcrate_path.value()),
            toml_version,
        ) {
            return Ok(Some(Location::new(
                Url::from_file_path(subcrate_cargo_toml_path).unwrap(),
                tombi_text::Range::default().into(),
            )));
        }
    }

    Ok(None)
}

/// Sanitize the dependency key to be "dependencies" if it is "dev-dependencies" or "build-dependencies".
///
/// This is because the dependency key is always "dependencies" in the workspace Cargo.toml.
#[inline]
fn sanitize_dependency_key(key: &str) -> &str {
    if matches!(key, "dev-dependencies" | "build-dependencies") {
        "dependencies"
    } else {
        key
    }
}
