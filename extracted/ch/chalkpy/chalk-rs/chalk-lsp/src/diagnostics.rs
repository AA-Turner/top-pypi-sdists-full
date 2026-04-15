use std::collections::{HashMap, HashSet};
use std::path::Path;

use chalk_ast::{AstFileParserCache, FeatureClassAST, ParsedAstFile, ResolverAST};
use lsp_types::{Diagnostic, DiagnosticSeverity, NumberOrString, Position, Range};

const SOURCE: &str = "chalk";

/// Run all lint checks on a single file and return LSP diagnostics.
pub fn lint(project_root: Option<&Path>, file_path: &Path, source: &str) -> Vec<Diagnostic> {
    let mut diags = Vec::new();

    if is_chalk_config(file_path) {
        diags.extend(lint_chalk_config(source));
        return diags;
    }

    if file_path.extension().and_then(|e| e.to_str()) != Some("py") {
        return diags;
    }

    if project_root.is_none() {
        diags.push(Diagnostic {
            range: Range::new(Position::new(0, 0), Position::new(0, 0)),
            severity: Some(DiagnosticSeverity::INFORMATION),
            source: Some(SOURCE.into()),
            message: "No chalk.yml found in any parent directory. \
                      Some lint checks are disabled."
                .into(),
            ..Default::default()
        });
    }

    let root = project_root
        .map(|p| p.to_path_buf())
        .unwrap_or_else(|| file_path.parent().unwrap_or(Path::new(".")).to_path_buf());

    let file_path_str = file_path.to_string_lossy().to_string();

    let parsed = parse_single_file(&root, &file_path_str);

    diags.extend(lint_feature_classes(&parsed.feature_classes));
    diags.extend(lint_resolvers(&parsed.resolvers));

    diags
}

// ---------------------------------------------------------------------------
// chalk.yml validation
// ---------------------------------------------------------------------------

fn is_chalk_config(path: &Path) -> bool {
    path.file_name()
        .and_then(|n| n.to_str())
        .map(|n| chalk_project::PROJECT_CONFIG_FILENAMES.contains(&n))
        .unwrap_or(false)
}

fn lint_chalk_config(source: &str) -> Vec<Diagnostic> {
    let mut diags = Vec::new();

    match serde_yaml::from_str::<chalk_project::ProjectSettings>(source) {
        Ok(settings) => {
            if settings.project.is_empty() {
                diags.push(Diagnostic {
                    range: Range::new(Position::new(0, 0), Position::new(0, 0)),
                    severity: Some(DiagnosticSeverity::WARNING),
                    code: Some(NumberOrString::String("chalk-config-no-project".into())),
                    source: Some(SOURCE.into()),
                    message: "Missing `project` name in chalk config.".into(),
                    ..Default::default()
                });
            }
            if settings.environments.is_empty() {
                diags.push(Diagnostic {
                    range: Range::new(Position::new(0, 0), Position::new(0, 0)),
                    severity: Some(DiagnosticSeverity::WARNING),
                    code: Some(NumberOrString::String("chalk-config-no-environments".into())),
                    source: Some(SOURCE.into()),
                    message: "No environments defined in chalk config.".into(),
                    ..Default::default()
                });
            }
            for (name, env) in &settings.environments {
                if env.runtime.is_none() {
                    diags.push(Diagnostic {
                        range: find_yaml_key_range(source, name),
                        severity: Some(DiagnosticSeverity::WARNING),
                        code: Some(NumberOrString::String("chalk-config-no-runtime".into())),
                        source: Some(SOURCE.into()),
                        message: format!(
                            "Environment `{name}` does not specify a `runtime`."
                        ),
                        ..Default::default()
                    });
                }
            }
        }
        Err(e) => {
            let (line, col) = e
                .location()
                .map(|loc| (loc.line().saturating_sub(1) as u32, loc.column() as u32))
                .unwrap_or((0, 0));
            diags.push(Diagnostic {
                range: Range::new(Position::new(line, col), Position::new(line, col)),
                severity: Some(DiagnosticSeverity::ERROR),
                code: Some(NumberOrString::String("chalk-config-parse-error".into())),
                source: Some(SOURCE.into()),
                message: format!("Invalid chalk config: {e}"),
                ..Default::default()
            });
        }
    }
    diags
}

// ---------------------------------------------------------------------------
// Feature class linting
// ---------------------------------------------------------------------------

fn lint_feature_classes(classes: &[FeatureClassAST]) -> Vec<Diagnostic> {
    let mut diags = Vec::new();

    let mut seen_namespaces: HashMap<&str, &str> = HashMap::new();
    for cls in classes {
        if let Some(prev_class) = seen_namespaces.get(cls.namespace.as_str()) {
            diags.push(at_location(
                &cls.decorator_location,
                DiagnosticSeverity::ERROR,
                "chalk-duplicate-namespace",
                format!(
                    "Namespace `{}` is already used by class `{}`.",
                    cls.namespace, prev_class
                ),
            ));
        } else {
            seen_namespaces.insert(&cls.namespace, &cls.class_name);
        }

        diags.extend(lint_single_feature_class(cls));
    }

    diags
}

fn lint_single_feature_class(cls: &FeatureClassAST) -> Vec<Diagnostic> {
    let mut diags = Vec::new();

    // Duplicate field names (the AST preserves duplicates in `annotations`).
    let mut seen_fields: HashMap<&str, usize> = HashMap::new();
    for field in &cls.annotations {
        let count = seen_fields.entry(&field.field_name).or_insert(0);
        *count += 1;
        if *count == 2 {
            diags.push(at_location(
                &field.field_name_location,
                DiagnosticSeverity::ERROR,
                "chalk-duplicate-field",
                format!(
                    "Duplicate field `{}` in feature class `{}`.",
                    field.field_name, cls.class_name
                ),
            ));
        }
    }

    // Fields without type annotations.
    for field in cls.fields.values() {
        if field.annotation.is_none() {
            diags.push(at_location(
                &field.field_name_location,
                DiagnosticSeverity::ERROR,
                "chalk-field-no-type",
                format!(
                    "Field `{}` in `{}` is missing a type annotation.",
                    field.field_name, cls.class_name
                ),
            ));
        }
    }

    // Empty feature class.
    if cls.fields.is_empty() {
        diags.push(at_location(
            &cls.class_name_location,
            DiagnosticSeverity::WARNING,
            "chalk-empty-feature-class",
            format!("Feature class `{}` has no fields.", cls.class_name),
        ));
    }

    diags
}

// ---------------------------------------------------------------------------
// Resolver linting
// ---------------------------------------------------------------------------

fn lint_resolvers(resolvers: &[ResolverAST]) -> Vec<Diagnostic> {
    let mut diags = Vec::new();

    let mut seen: HashSet<&str> = HashSet::new();
    for r in resolvers {
        if !seen.insert(&r.resolver_name) {
            diags.push(at_location(
                &r.resolver_name_location,
                DiagnosticSeverity::ERROR,
                "chalk-duplicate-resolver",
                format!("Duplicate resolver `{}`.", r.resolver_name),
            ));
        }
        diags.extend(lint_single_resolver(r));
    }

    diags
}

fn lint_single_resolver(r: &ResolverAST) -> Vec<Diagnostic> {
    let mut diags = Vec::new();

    // Missing return type annotation.
    if r.return_annotation.is_none() {
        if let Some(ref loc) = r.missing_return_annotation {
            diags.push(at_location(
                loc,
                DiagnosticSeverity::WARNING,
                "chalk-resolver-no-return-type",
                format!(
                    "Resolver `{}` is missing a return type annotation.",
                    r.resolver_name
                ),
            ));
        }
    }

    // Arguments without type annotations.
    for arg in r.args.values() {
        if arg.annotation.is_none() {
            diags.push(at_location(
                &arg.arg_location,
                DiagnosticSeverity::WARNING,
                "chalk-resolver-arg-no-type",
                format!(
                    "Argument `{}` of resolver `{}` is missing a type annotation.",
                    arg.arg_name, r.resolver_name
                ),
            ));
        }
    }

    diags
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

fn parse_single_file(project_root: &Path, file_path: &str) -> ParsedAstFile {
    let cache = AstFileParserCache::new(project_root.to_path_buf(), vec![file_path.to_string()]);
    match cache.get_parsed_file(file_path) {
        Ok(parsed_file) => {
            let module = cache.module_name_for_path(file_path);
            chalk_ast::parse_ast_file_with_feature_module(&parsed_file, &module)
        }
        Err(_) => ParsedAstFile::default(),
    }
}

fn at_location(
    loc: &lsp_types::Location,
    severity: DiagnosticSeverity,
    code: &str,
    message: String,
) -> Diagnostic {
    Diagnostic {
        range: loc.range,
        severity: Some(severity),
        code: Some(NumberOrString::String(code.into())),
        source: Some(SOURCE.into()),
        message,
        ..Default::default()
    }
}

fn find_yaml_key_range(source: &str, key: &str) -> Range {
    for (i, line) in source.lines().enumerate() {
        let trimmed = line.trim_start();
        if trimmed.starts_with(key) && trimmed[key.len()..].starts_with(':') {
            let col = line.len() - trimmed.len();
            return Range::new(
                Position::new(i as u32, col as u32),
                Position::new(i as u32, (col + key.len()) as u32),
            );
        }
    }
    Range::new(Position::new(0, 0), Position::new(0, 0))
}

#[cfg(test)]
mod tests {
    use std::path::Path;

    use lsp_types::DiagnosticSeverity;
    use tempfile::TempDir;

    use super::lint;

    fn has_code(diags: &[lsp_types::Diagnostic], code: &str) -> bool {
        diags.iter().any(|d| {
            d.code
                .as_ref()
                .map(|c| match c {
                    lsp_types::NumberOrString::String(s) => s == code,
                    _ => false,
                })
                .unwrap_or(false)
        })
    }

    #[test]
    fn lint_chalk_config_missing_project_name() {
        let diags = lint(
            None,
            Path::new("/tmp/chalk.yml"),
            "environments:\n  default:\n    runtime: python312\n",
        );
        assert!(has_code(&diags, "chalk-config-no-project"));
    }

    #[test]
    fn lint_chalk_config_missing_environments() {
        let diags = lint(None, Path::new("/tmp/chalk.yml"), "project: myproject\n");
        assert!(has_code(&diags, "chalk-config-no-environments"));
    }

    #[test]
    fn lint_chalk_config_missing_runtime() {
        let diags = lint(
            None,
            Path::new("/tmp/chalk.yml"),
            "project: myproject\nenvironments:\n  default:\n    requirements: req.txt\n",
        );
        assert!(has_code(&diags, "chalk-config-no-runtime"));
    }

    #[test]
    fn lint_chalk_config_parse_error() {
        let diags = lint(None, Path::new("/tmp/chalk.yml"), "{{invalid yaml");
        assert!(has_code(&diags, "chalk-config-parse-error"));
        assert_eq!(diags[0].severity, Some(DiagnosticSeverity::ERROR));
    }

    #[test]
    fn lint_valid_chalk_config_no_errors() {
        let diags = lint(
            None,
            Path::new("/tmp/chalk.yml"),
            "project: myproject\nenvironments:\n  default:\n    runtime: python312\n",
        );
        assert!(diags.is_empty());
    }

    #[test]
    fn lint_python_file_duplicate_field() {
        let dir = TempDir::new().unwrap();
        let py_path = dir.path().join("features.py");
        let source = r#"
from chalk.features import features

@features
class User:
    score: int
    score: int
"#;
        std::fs::write(&py_path, source).unwrap();

        let diags = lint(
            Some(dir.path()),
            &py_path,
            source,
        );
        assert!(has_code(&diags, "chalk-duplicate-field"));
    }

    #[test]
    fn lint_python_file_empty_feature_class() {
        let dir = TempDir::new().unwrap();
        let py_path = dir.path().join("features.py");
        let source = r#"
from chalk.features import features

@features
class User:
    pass
"#;
        std::fs::write(&py_path, source).unwrap();

        let diags = lint(Some(dir.path()), &py_path, source);
        assert!(has_code(&diags, "chalk-empty-feature-class"));
    }

    #[test]
    fn lint_python_resolver_missing_return_type() {
        let dir = TempDir::new().unwrap();
        let py_path = dir.path().join("resolvers.py");
        let source = r#"
from chalk import online

@online
def get_score(user_id: int):
    return 42
"#;
        std::fs::write(&py_path, source).unwrap();

        let diags = lint(Some(dir.path()), &py_path, source);
        assert!(has_code(&diags, "chalk-resolver-no-return-type"));
    }

    #[test]
    fn lint_python_resolver_missing_arg_type() {
        let dir = TempDir::new().unwrap();
        let py_path = dir.path().join("resolvers.py");
        let source = r#"
from chalk import online

@online
def get_score(user_id) -> int:
    return 42
"#;
        std::fs::write(&py_path, source).unwrap();

        let diags = lint(Some(dir.path()), &py_path, source);
        assert!(has_code(&diags, "chalk-resolver-arg-no-type"));
    }

    #[test]
    fn lint_valid_python_file_no_diagnostics() {
        let dir = TempDir::new().unwrap();
        let py_path = dir.path().join("features.py");
        let source = r#"
from chalk.features import features

@features
class User:
    id: int
    name: str
"#;
        std::fs::write(&py_path, source).unwrap();

        let diags = lint(Some(dir.path()), &py_path, source);
        assert!(diags.is_empty(), "expected no diagnostics, got: {diags:?}");
    }

    #[test]
    fn lint_non_python_file_returns_empty() {
        let diags = lint(None, Path::new("/tmp/readme.md"), "# Hello");
        assert!(diags.is_empty());
    }

    #[test]
    fn lint_python_without_project_root_warns() {
        let dir = TempDir::new().unwrap();
        let py_path = dir.path().join("plain.py");
        let source = "x = 1\n";
        std::fs::write(&py_path, source).unwrap();

        let diags = lint(None, &py_path, source);
        assert!(diags
            .iter()
            .any(|d| d.severity == Some(DiagnosticSeverity::INFORMATION)));
    }
}
