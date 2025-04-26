mod goto_declaration;
mod goto_definition;

use glob;
pub use goto_declaration::goto_declaration;
pub use goto_definition::goto_definition;
use itertools::Itertools;
use tombi_ast::AstNode;
use tombi_config::TomlVersion;
use tombi_document_tree::TryIntoDocumentTree;
use tower_lsp::lsp_types::{Location, Url};

fn load_pyproject_toml(
    pyproject_toml_path: &std::path::Path,
    toml_version: TomlVersion,
) -> Option<tombi_document_tree::DocumentTree> {
    let Some(toml_text) = std::fs::read_to_string(pyproject_toml_path).ok() else {
        return None;
    };

    let Some(root) = tombi_ast::Root::cast(tombi_parser::parse(&toml_text).into_syntax_node())
    else {
        return None;
    };

    root.try_into_document_tree(toml_version).ok()
}

fn find_workspace_pyproject_toml(
    pyproject_toml_path: &std::path::Path,
    toml_version: TomlVersion,
) -> Option<(std::path::PathBuf, tombi_document_tree::DocumentTree)> {
    let Some(mut current_dir) = pyproject_toml_path.parent() else {
        return None;
    };

    while let Some(target_dir) = current_dir.parent() {
        current_dir = target_dir;
        let workspace_pyproject_toml_path = current_dir.join("pyproject.toml");

        if workspace_pyproject_toml_path.exists() {
            let Some(package_pyproject_toml_document_tree) =
                load_pyproject_toml(&workspace_pyproject_toml_path, toml_version)
            else {
                continue;
            };

            // Check if this pyproject.toml has a [tool.uv.workspace] section

            if let Some(_) = tombi_document_tree::dig_keys(
                &package_pyproject_toml_document_tree,
                &["tool", "uv", "workspace"],
            ) {
                return Some((
                    workspace_pyproject_toml_path,
                    package_pyproject_toml_document_tree,
                ));
            }
        }
    }

    None
}

/// Get the location of the workspace pyproject.toml.
///
/// ```toml
/// [project]
/// name = "example"
/// version = "0.1.0"
/// dependencies = ["other-package"]
///
/// [tool.uv.sources]
/// other-package = { workspace = true }
/// ```
fn get_workspace_pyproject_toml_location(
    keys: &[&str],
    pyproject_toml_path: &std::path::Path,
    toml_version: TomlVersion,
    jump_to_package: bool,
) -> Result<Option<Location>, tower_lsp::jsonrpc::Error> {
    assert!(matches!(keys, ["tool", "uv", "sources", _, "workspace"]));

    let Some((workspace_pyproject_toml_path, workspace_pyproject_toml_document_tree)) =
        find_workspace_pyproject_toml(pyproject_toml_path, toml_version)
    else {
        return Ok(None);
    };

    let package_name = keys[3];
    let Some((package_toml_path, member_range)) = find_package_project_toml(
        package_name,
        &workspace_pyproject_toml_document_tree,
        &workspace_pyproject_toml_path,
        toml_version,
    ) else {
        return Ok(None);
    };

    if jump_to_package {
        let Ok(package_pyproject_toml_uri) = Url::from_file_path(&package_toml_path) else {
            return Ok(None);
        };

        Ok(Some(Location::new(
            package_pyproject_toml_uri,
            tombi_text::Range::default().into(),
        )))
    } else {
        let Ok(workspace_pyproject_toml_uri) = Url::from_file_path(&workspace_pyproject_toml_path)
        else {
            return Ok(None);
        };

        Ok(Some(Location::new(
            workspace_pyproject_toml_uri,
            member_range.into(),
        )))
    }
}

fn find_package_project_toml(
    package_name: &str,
    workspace_pyproject_toml_document_tree: &tombi_document_tree::DocumentTree,
    workspace_pyproject_toml_path: &std::path::Path,
    toml_version: TomlVersion,
) -> Option<(std::path::PathBuf, tombi_text::Range)> {
    let Some(workspace_dir_path) = workspace_pyproject_toml_path.parent() else {
        return None;
    };

    let member_patterns = match tombi_document_tree::dig_keys(
        &workspace_pyproject_toml_document_tree,
        &[&"tool", &"uv", &"workspace", &"members"],
    ) {
        Some((_, tombi_document_tree::Value::Array(members))) => members
            .iter()
            .filter_map(|member| match member {
                tombi_document_tree::Value::String(member_pattern) => Some(member_pattern),
                _ => None,
            })
            .collect_vec(),
        _ => vec![],
    };

    let exclude_patterns = match tombi_document_tree::dig_keys(
        &workspace_pyproject_toml_document_tree,
        &[&"tool", &"uv", &"workspace", &"exclude"],
    ) {
        Some((_, tombi_document_tree::Value::Array(exclude))) => exclude
            .iter()
            .filter_map(|member| match member {
                tombi_document_tree::Value::String(member_pattern) => Some(member_pattern),
                _ => None,
            })
            .collect_vec(),
        _ => vec![],
    };

    for (member_item, package_project_toml_path) in
        find_package_project_toml_paths(&member_patterns, &exclude_patterns, workspace_dir_path)
    {
        let Some(package_project_toml_document_tree) =
            load_pyproject_toml(&package_project_toml_path, toml_version)
        else {
            continue;
        };

        if let Some((_, tombi_document_tree::Value::String(name))) =
            tombi_document_tree::dig_keys(&package_project_toml_document_tree, &["project", "name"])
        {
            if name.value() == package_name {
                return Some((package_project_toml_path, member_item.range()));
            }
        }
    }

    None
}

fn find_package_project_toml_paths<'a>(
    member_patterns: &'a [&'a tombi_document_tree::String],
    exclude_patterns: &'a [&'a tombi_document_tree::String],
    workspace_dir_path: &'a std::path::Path,
) -> impl Iterator<Item = (&'a tombi_document_tree::String, std::path::PathBuf)> + 'a {
    let exclude_patterns = exclude_patterns
        .iter()
        .filter_map(|pattern| match glob::Pattern::new(pattern.value()) {
            Ok(exclude_glob) => Some(exclude_glob),
            Err(_) => None,
        })
        .collect_vec();

    member_patterns
        .iter()
        .filter_map(move |&member_pattern| {
            let mut project_toml_paths = vec![];

            let mut member_pattern_path =
                std::path::Path::new(member_pattern.value()).to_path_buf();
            if !member_pattern_path.is_absolute() {
                member_pattern_path = workspace_dir_path.join(member_pattern_path);
            }

            // Find matching paths using glob
            let mut candidate_paths = match glob::glob(&member_pattern_path.to_string_lossy()) {
                Ok(paths) => paths,
                Err(_) => return None,
            };

            // Check if any path matches and is not excluded
            while let Some(Ok(candidate_path)) = candidate_paths.next() {
                // Skip if the path doesn't contain pyproject.toml
                let project_toml_path = if candidate_path.is_dir() {
                    candidate_path.join("pyproject.toml")
                } else {
                    continue;
                };

                if !project_toml_path.exists() || !project_toml_path.is_file() {
                    continue;
                }

                // Check if the path is excluded
                let is_excluded = exclude_patterns.iter().any(|exclude_pattern| {
                    exclude_pattern.matches(&project_toml_path.to_string_lossy())
                });

                if !is_excluded {
                    project_toml_paths.push((member_pattern, project_toml_path));
                }
            }

            if !project_toml_paths.is_empty() {
                Some(project_toml_paths)
            } else {
                None
            }
        })
        .flatten()
}
