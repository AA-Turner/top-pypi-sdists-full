//! Go-to-definition and completion providers, tying the text parsers
//! ([`crate::sql_resolver`], [`crate::expression`]) to the project AST index.

use chalk_ast::{AstProjectIndex, FeatureClassAST, FeatureFieldAST};
use lsp_types::{
    CompletionItem, CompletionItemKind, Documentation, Location, MarkupContent, MarkupKind,
};

use crate::{expression, sql_resolver};

/// Go-to-definition for a `.chalk.sql` resolver file.
///
/// * On the `-- resolves:` target → the feature class definition.
/// * On a `SELECT` output column → the feature it populates.
pub fn sql_definition(
    index: &AstProjectIndex,
    text: &str,
    line: u32,
    col: u32,
) -> Vec<Location> {
    if let Some(reference) = sql_resolver::resolves_ref_at(text, line, col) {
        return index
            .find_feature_class_by_namespace_or_class_name(&reference.identifier)
            .map(|class| vec![class.class_name_location])
            .unwrap_or_default();
    }

    if let Some(column) = sql_resolver::output_column_at(text, line, col) {
        let Some(reference) = sql_resolver::resolves_ref(text) else {
            return Vec::new();
        };
        let Some(class) =
            index.find_feature_class_by_namespace_or_class_name(&reference.identifier)
        else {
            return Vec::new();
        };
        if let Some(field) = class.fields.get(&column.name) {
            return vec![field.field_name_location.clone()];
        }
    }

    Vec::new()
}

/// Go-to-definition for a `_.member` expression in a Python feature file.
pub fn python_definition(
    index: &AstProjectIndex,
    file_path: &str,
    text: &str,
    line: u32,
    col: u32,
) -> Vec<Location> {
    let Some(member) = expression::underscore_member_at(text, line, col) else {
        return Vec::new();
    };
    let Some(base_class) = enclosing_feature_class(index, file_path, line) else {
        return Vec::new();
    };
    let Some(target_class) = resolve_scope_chain(index, base_class, &member.scope_chain) else {
        return Vec::new();
    };
    target_class
        .fields
        .get(&member.member)
        .map(|field| vec![field.field_name_location.clone()])
        .unwrap_or_default()
}

/// Completion for `_.` in a Python feature file: the members of the feature
/// class that `_` currently refers to.
pub fn python_completion(
    index: &AstProjectIndex,
    file_path: &str,
    text: &str,
    line: u32,
    col: u32,
) -> Vec<CompletionItem> {
    let Some(completion) = expression::underscore_completion_at(text, line, col) else {
        return Vec::new();
    };
    let Some(base_class) = enclosing_feature_class(index, file_path, line) else {
        return Vec::new();
    };
    let Some(target_class) = resolve_scope_chain(index, base_class, &completion.scope_chain) else {
        return Vec::new();
    };

    let mut items: Vec<CompletionItem> = target_class
        .fields
        .values()
        .map(field_completion_item)
        .collect();
    items.sort_by(|a, b| a.label.cmp(&b.label));
    items
}

/// The innermost feature class whose source range contains `line`.
fn enclosing_feature_class(
    index: &AstProjectIndex,
    file_path: &str,
    line: u32,
) -> Option<FeatureClassAST> {
    index
        .feature_classes_in_file(file_path)
        .into_iter()
        .filter(|class| {
            class.class_range.range.start.line <= line && line <= class.class_range.range.end.line
        })
        .min_by_key(|class| class.class_range.range.end.line - class.class_range.range.start.line)
}

/// Walk a relationship scope chain (e.g. `["children"]`) from `base`, following
/// each relationship's referenced feature class, and return the class the
/// innermost `_` refers to.
fn resolve_scope_chain(
    index: &AstProjectIndex,
    base: FeatureClassAST,
    chain: &[String],
) -> Option<FeatureClassAST> {
    let mut current = base;
    for relationship in chain {
        let field = current.fields.get(relationship)?;
        let class_name = field.referenced_feature_class.as_deref()?;
        current = index.find_feature_class_by_class_name(class_name)?;
    }
    Some(current)
}

fn field_completion_item(field: &FeatureFieldAST) -> CompletionItem {
    CompletionItem {
        label: field.field_name.clone(),
        kind: Some(CompletionItemKind::FIELD),
        detail: field.description.clone(),
        documentation: field.comment.clone().map(|comment| {
            Documentation::MarkupContent(MarkupContent {
                kind: MarkupKind::Markdown,
                value: comment,
            })
        }),
        ..Default::default()
    }
}
