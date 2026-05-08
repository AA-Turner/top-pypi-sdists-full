use std::collections::{HashMap, HashSet};

use ruff_python_ast::{Decorator, Expr, Stmt, StmtClassDef, StmtFunctionDef};
use ruff_python_parser::parse_module;
use ruff_text_size::Ranged;

use crate::type_map::TypeMap;

/// A text edit: replace bytes in [start, end) with `replacement`.
#[derive(Debug)]
struct Edit {
    start: usize,
    end: usize,
    replacement: String,
}

/// Transform a single Python source file, replacing Chalk-specific type
/// annotations with standard Python types using the protograph type map.
///
/// Returns `None` if no changes were needed (not a Chalk file).
pub fn transform_source(source: &str, type_map: &TypeMap) -> Option<String> {
    let parsed = parse_module(source).ok()?;
    let stmts = parsed.into_suite();

    // First pass: collect imports to identify which names are Chalk decorators/types.
    let imports = collect_chalk_imports(&stmts);
    if imports.feature_decorator_names.is_empty() && imports.resolver_decorator_names.is_empty() {
        return None;
    }

    // Second pass: walk the AST and collect edits.
    let mut edits = Vec::new();
    let mut return_typedicts: Vec<String> = Vec::new();
    let mut typeddict_counter = 0u32;

    collect_edits_from_stmts(
        &stmts,
        source,
        type_map,
        &imports,
        &mut edits,
        &mut return_typedicts,
        &mut typeddict_counter,
    );

    if edits.is_empty() && return_typedicts.is_empty() {
        return None;
    }

    // When there are no TypedDicts, integrate header imports with any leading
    // stdlib import block so the result has a single sorted/merged block.
    let leading_stdlib = if return_typedicts.is_empty() {
        find_leading_stdlib_block(&stmts)
    } else {
        None
    };

    if let Some(ref info) = leading_stdlib {
        edits.push(Edit {
            start: info.range.0,
            end: info.range.1,
            replacement: String::new(),
        });
    }

    // Apply edits back-to-front so byte offsets remain valid.
    edits.sort_by(|a, b| b.start.cmp(&a.start));
    let mut result = source.to_string();
    for edit in &edits {
        result.replace_range(edit.start..edit.end, &edit.replacement);
    }

    // If we removed a leading stdlib block, the result may now start with
    // blank lines — strip them so the header lands cleanly at the top.
    if leading_stdlib.is_some() {
        let trimmed_len = result
            .bytes()
            .take_while(|&b| b == b'\n' || b == b' ' || b == b'\t' || b == b'\r')
            .count();
        if trimmed_len > 0 {
            result.replace_range(0..trimmed_len, "");
        }
    }

    // Prepend generated TypedDicts and necessary imports at the top of the file.
    if !return_typedicts.is_empty() || !edits.is_empty() {
        let mut header = String::new();
        if !imports.has_future_annotations {
            header.push_str("from __future__ import annotations\n");
        }
        header.push('\n');

        if let Some(ref info) = leading_stdlib {
            // Merge the new imports with the original stdlib block.
            header.push_str(&build_merged_stdlib_block(&imports, info));
        } else {
            // Add imports needed by the transformed code, skipping any
            // that the file already has to avoid shadowing (e.g., `import datetime`
            // would shadow `from datetime import datetime`).
            if imports.datetime_imported_names.is_empty() && !imports.has_datetime_module_import {
                header.push_str("import datetime\n");
            }
            if imports.decimal_imported_names.is_empty() && !imports.has_decimal_module_import {
                header.push_str("import decimal\n");
            }
            header.push_str("from typing import Any, TypedDict\n");
        }

        if !return_typedicts.is_empty() {
            for td in &return_typedicts {
                header.push('\n');
                header.push('\n');
                header.push_str(td);
            }
            // Two blank lines after the last TypedDict (PEP 8).
            header.push('\n');
        }

        header.push('\n');
        result = header + &result;
    }

    Some(result)
}

type ImportName = (String, Option<String>);

/// A leading run of stdlib imports (`datetime`, `decimal`, `typing`) at the
/// top of the file, plus the byte range that covers them.
struct LeadingStdlib {
    range: (usize, usize),
    /// Plain `import X [as Y]` entries, in the order they appear.
    plain: Vec<ImportName>,
    /// `from X import names` entries, in the order modules first appear.
    /// Each module appears once with all its imported names accumulated.
    from_imports: Vec<(String, Vec<ImportName>)>,
}

/// Scan from the top of the file collecting consecutive stdlib imports.
/// `__future__` imports are skipped (they're handled separately). Stops at
/// the first non-stdlib import or non-import statement.
fn find_leading_stdlib_block(stmts: &[Stmt]) -> Option<LeadingStdlib> {
    const STDLIB_MODULES: &[&str] = &["datetime", "decimal", "typing"];

    let mut start: Option<usize> = None;
    let mut end: Option<usize> = None;
    let mut plain: Vec<ImportName> = Vec::new();
    let mut from_imports: Vec<(String, Vec<ImportName>)> = Vec::new();
    let mut from_index: HashMap<String, usize> = HashMap::new();

    for stmt in stmts {
        match stmt {
            Stmt::ImportFrom(import_from)
                if import_from
                    .module
                    .as_ref()
                    .map(|m| m.as_str() == "__future__")
                    .unwrap_or(false) =>
            {
                continue;
            }
            Stmt::Import(import_stmt) => {
                let is_relevant = import_stmt
                    .names
                    .iter()
                    .any(|alias| STDLIB_MODULES.contains(&alias.name.as_str()));
                if !is_relevant {
                    break;
                }
                let r = stmt.range();
                if start.is_none() {
                    start = Some(r.start().to_usize());
                }
                end = Some(r.end().to_usize());
                for alias in &import_stmt.names {
                    if STDLIB_MODULES.contains(&alias.name.as_str()) {
                        let asname = alias.asname.as_ref().map(|n| n.to_string());
                        plain.push((alias.name.to_string(), asname));
                    }
                }
            }
            Stmt::ImportFrom(import_from) => {
                let module_str = match &import_from.module {
                    Some(m) => m.to_string(),
                    None => break,
                };
                if !STDLIB_MODULES.contains(&module_str.as_str()) {
                    break;
                }
                let r = stmt.range();
                if start.is_none() {
                    start = Some(r.start().to_usize());
                }
                end = Some(r.end().to_usize());
                let names: Vec<ImportName> = import_from
                    .names
                    .iter()
                    .map(|alias| {
                        let asname = alias.asname.as_ref().map(|n| n.to_string());
                        (alias.name.to_string(), asname)
                    })
                    .collect();
                if let Some(&idx) = from_index.get(&module_str) {
                    from_imports[idx].1.extend(names);
                } else {
                    from_index.insert(module_str.clone(), from_imports.len());
                    from_imports.push((module_str, names));
                }
            }
            _ => break,
        }
    }

    let range = start.zip(end)?;
    Some(LeadingStdlib {
        range,
        plain,
        from_imports,
    })
}

/// Build the merged stdlib import block: existing imports plus what the
/// transformation needs (`import datetime`/`import decimal` if missing,
/// `Any` and `TypedDict` merged into `from typing`). Plain imports are
/// listed first, then `from` imports, each group sorted alphabetically.
fn build_merged_stdlib_block(imports: &ChalkImports, info: &LeadingStdlib) -> String {
    let mut plain_set: Vec<String> = info
        .plain
        .iter()
        .map(|(name, asname)| match asname {
            Some(a) => format!("import {name} as {a}"),
            None => format!("import {name}"),
        })
        .collect();

    if imports.datetime_imported_names.is_empty() && !imports.has_datetime_module_import {
        let stmt = "import datetime".to_string();
        if !plain_set.contains(&stmt) {
            plain_set.push(stmt);
        }
    }
    if imports.decimal_imported_names.is_empty() && !imports.has_decimal_module_import {
        let stmt = "import decimal".to_string();
        if !plain_set.contains(&stmt) {
            plain_set.push(stmt);
        }
    }

    plain_set.sort();
    plain_set.dedup();

    let mut from_map: HashMap<String, HashSet<String>> = HashMap::new();
    for (module, names) in &info.from_imports {
        let entry = from_map.entry(module.clone()).or_default();
        for (n, asname) in names {
            let s = match asname {
                Some(a) => format!("{n} as {a}"),
                None => n.clone(),
            };
            entry.insert(s);
        }
    }

    let typing_entry = from_map.entry("typing".to_string()).or_default();
    typing_entry.insert("Any".to_string());
    typing_entry.insert("TypedDict".to_string());

    let mut from_sorted: Vec<(String, Vec<String>)> = from_map
        .into_iter()
        .map(|(module, names)| {
            let mut v: Vec<String> = names.into_iter().collect();
            v.sort();
            (module, v)
        })
        .collect();
    from_sorted.sort_by(|a, b| a.0.cmp(&b.0));

    let mut block = String::new();
    for stmt in &plain_set {
        block.push_str(stmt);
        block.push('\n');
    }
    for (module, names) in &from_sorted {
        block.push_str(&format!("from {module} import {}\n", names.join(", ")));
    }
    block
}

/// Rewrite a qualified type annotation to use unqualified names when
/// the file already has `from <module> import <name>`.
/// E.g., `datetime.datetime` → `datetime` if file has `from datetime import datetime`.
fn localize_type(type_str: &str, imports: &ChalkImports) -> String {
    let mut result = type_str.to_string();
    // Replace `datetime.X` with `X` when X is directly imported.
    for name in &imports.datetime_imported_names {
        let qualified = format!("datetime.{name}");
        if result.contains(&qualified) {
            result = result.replace(&qualified, name);
        }
    }
    // Replace `decimal.X` with `X` when X is directly imported.
    for name in &imports.decimal_imported_names {
        let qualified = format!("decimal.{name}");
        if result.contains(&qualified) {
            result = result.replace(&qualified, name);
        }
    }
    result
}

/// Information about imports in the file.
struct ChalkImports {
    /// Names that refer to the `@features` decorator (e.g., "features").
    feature_decorator_names: HashSet<String>,
    /// Names that refer to resolver decorators (e.g., "online", "offline").
    resolver_decorator_names: HashSet<String>,
    /// Names that refer to the `Features` type (for return annotations).
    features_type_names: HashSet<String>,
    /// Names that refer to `DataFrame`.
    dataframe_names: HashSet<String>,
    /// Names that refer to `FeatureTime`.
    feature_time_names: HashSet<String>,
    /// Names that refer to `Primary`.
    primary_names: HashSet<String>,
    /// Names that refer to `Windowed`.
    windowed_names: HashSet<String>,
    /// Whether the file already has `from __future__ import annotations`.
    has_future_annotations: bool,
    /// Names imported from `datetime` module (e.g., `from datetime import datetime, date`).
    /// If non-empty, we should use unqualified names instead of `datetime.datetime`.
    datetime_imported_names: HashSet<String>,
    /// Names imported from `decimal` module.
    decimal_imported_names: HashSet<String>,
    /// Whether the file has `import datetime` (the module, not `from datetime import ...`).
    has_datetime_module_import: bool,
    /// Whether the file has `import decimal`.
    has_decimal_module_import: bool,
}

fn collect_chalk_imports(stmts: &[Stmt]) -> ChalkImports {
    let mut imports = ChalkImports {
        feature_decorator_names: HashSet::new(),
        resolver_decorator_names: HashSet::new(),
        features_type_names: HashSet::new(),
        dataframe_names: HashSet::new(),
        feature_time_names: HashSet::new(),
        primary_names: HashSet::new(),
        windowed_names: HashSet::new(),
        has_future_annotations: false,
        datetime_imported_names: HashSet::new(),
        decimal_imported_names: HashSet::new(),
        has_datetime_module_import: false,
        has_decimal_module_import: false,
    };

    for stmt in stmts {
        // Check for `import datetime` / `import decimal` (bare module imports).
        // Only count as "in scope" if there's no alias (i.e., `import datetime`,
        // not `import datetime as dt` where `datetime` isn't bound).
        if let Stmt::Import(import_stmt) = stmt {
            for alias in &import_stmt.names {
                let has_alias = alias.asname.is_some();
                match alias.name.as_str() {
                    "datetime" if !has_alias => imports.has_datetime_module_import = true,
                    "decimal" if !has_alias => imports.has_decimal_module_import = true,
                    _ => {}
                }
            }
            continue;
        }

        let Stmt::ImportFrom(import_from) = stmt else {
            continue;
        };
        let Some(ref module) = import_from.module else {
            continue;
        };
        let module_str = module.to_string();

        // Track stdlib imports that our header might conflict with.
        match module_str.as_str() {
            "__future__" => {
                for alias in &import_from.names {
                    if alias.name.as_str() == "annotations" {
                        imports.has_future_annotations = true;
                    }
                }
            }
            "datetime" => {
                // `from datetime import datetime, date, ...`
                for alias in &import_from.names {
                    let local = alias
                        .asname
                        .as_ref()
                        .map(|n| n.to_string())
                        .unwrap_or_else(|| alias.name.to_string());
                    imports.datetime_imported_names.insert(local);
                }
            }
            "decimal" => {
                for alias in &import_from.names {
                    let local = alias
                        .asname
                        .as_ref()
                        .map(|n| n.to_string())
                        .unwrap_or_else(|| alias.name.to_string());
                    imports.decimal_imported_names.insert(local);
                }
            }
            _ => {}
        }

        // Check if this is a chalk import.
        if !module_str.starts_with("chalk") {
            continue;
        }

        for alias in &import_from.names {
            let name = alias.name.as_str();
            let local_name = alias
                .asname
                .as_ref()
                .map(|n| n.to_string())
                .unwrap_or_else(|| name.to_string());

            match name {
                "features" => {
                    imports
                        .feature_decorator_names
                        .insert(local_name.to_string());
                }
                "online" | "offline" | "stream" => {
                    imports
                        .resolver_decorator_names
                        .insert(local_name.to_string());
                }
                "Features" => {
                    imports.features_type_names.insert(local_name.to_string());
                }
                "DataFrame" => {
                    imports.dataframe_names.insert(local_name.to_string());
                }
                "FeatureTime" => {
                    imports.feature_time_names.insert(local_name.to_string());
                }
                "Primary" => {
                    imports.primary_names.insert(local_name.to_string());
                }
                "Windowed" | "windowed" => {
                    if name == "Windowed" {
                        imports.windowed_names.insert(local_name.to_string());
                    }
                }
                _ => {}
            }
        }
    }

    imports
}

fn collect_edits_from_stmts(
    stmts: &[Stmt],
    source: &str,
    type_map: &TypeMap,
    imports: &ChalkImports,
    edits: &mut Vec<Edit>,
    return_typedicts: &mut Vec<String>,
    typeddict_counter: &mut u32,
) {
    for stmt in stmts {
        match stmt {
            Stmt::ClassDef(class_def) => {
                handle_class_def(class_def, source, type_map, imports, edits);
                // Recurse into nested definitions.
                collect_edits_from_stmts(
                    &class_def.body,
                    source,
                    type_map,
                    imports,
                    edits,
                    return_typedicts,
                    typeddict_counter,
                );
            }
            Stmt::FunctionDef(func_def) => {
                handle_function_def(
                    func_def,
                    source,
                    type_map,
                    imports,
                    edits,
                    return_typedicts,
                    typeddict_counter,
                );
                // Recurse into nested definitions.
                collect_edits_from_stmts(
                    &func_def.body,
                    source,
                    type_map,
                    imports,
                    edits,
                    return_typedicts,
                    typeddict_counter,
                );
            }
            Stmt::If(if_stmt) => {
                collect_edits_from_stmts(
                    &if_stmt.body,
                    source,
                    type_map,
                    imports,
                    edits,
                    return_typedicts,
                    typeddict_counter,
                );
                for elif in &if_stmt.elif_else_clauses {
                    collect_edits_from_stmts(
                        &elif.body,
                        source,
                        type_map,
                        imports,
                        edits,
                        return_typedicts,
                        typeddict_counter,
                    );
                }
            }
            _ => {}
        }
    }
}

/// Handle a `@features`-decorated class: remove decorator, add permissive __init__.
fn handle_class_def(
    class_def: &StmtClassDef,
    source: &str,
    type_map: &TypeMap,
    imports: &ChalkImports,
    edits: &mut Vec<Edit>,
) {
    let Some(matching_decorator) =
        find_matching_decorator(&class_def.decorator_list, &imports.feature_decorator_names)
    else {
        return;
    };

    // Comment out the @features decorator (may span multiple lines).
    let dec_range = matching_decorator.range();
    let dec_text = &source[dec_range.start().to_usize()..dec_range.end().to_usize()];
    let commented = dec_text
        .lines()
        .map(|line| format!("# {line}"))
        .collect::<Vec<_>>()
        .join("\n");
    edits.push(Edit {
        start: dec_range.start().to_usize(),
        end: dec_range.end().to_usize(),
        replacement: commented,
    });

    // The class name is what we'll use to look up has-one fields in the type_map.
    let class_name = class_def.name.as_str().to_string();

    // Replace Chalk-specific type annotations in field definitions:
    // - FeatureTime -> datetime.datetime
    // - Primary[x] -> x
    // - Windowed[x] -> dict[str, x]
    // - User.id (foreign key refs) -> resolved type from protograph
    // - "Jar.jar_id" (string-quoted foreign key refs) -> resolved type
    // - has-one / has-many fields: rewrite to the relationship target so feature-path
    //   access (`Foo.bar.baz`) doesn't trip ty's None-narrowing.
    for stmt in &class_def.body {
        if let Stmt::AnnAssign(ann) = stmt {
            let target_name = match &*ann.target {
                Expr::Name(n) => Some(n.id.as_str().to_string()),
                _ => None,
            };
            let replacement = resolve_chalk_field_annotation(&ann.annotation, imports)
                .or_else(|| resolve_feature_ref_annotation(&ann.annotation, source, type_map))
                .or_else(|| resolve_string_annotation(&ann.annotation, source, type_map))
                .or_else(|| {
                    target_name
                        .as_ref()
                        .and_then(|n| resolve_relationship_field(&class_name, n, type_map))
                });
            if let Some(replacement) = replacement {
                let range = ann.annotation.range();
                edits.push(Edit {
                    start: range.start().to_usize(),
                    end: range.end().to_usize(),
                    replacement: localize_type(&replacement, imports),
                });
            }
        }
    }

    // Add a permissive __init__ at the end of the class body so that
    // constructors like User(name="hello") type-check without requiring
    // all fields. Chalk's @features classes accept any subset of fields.
    let body_end = class_def.body.last().map(|s| s.range().end().to_usize());
    if let Some(end) = body_end {
        edits.push(Edit {
            start: end,
            end,
            replacement: "\n\n    def __init__(self, **kwargs: Any) -> None: ...".to_string(),
        });
    }
}

/// Resolve Chalk-specific field annotations like FeatureTime and Primary[x].
fn resolve_chalk_field_annotation(expr: &Expr, imports: &ChalkImports) -> Option<String> {
    match expr {
        // FeatureTime -> datetime.datetime
        Expr::Name(name) if imports.feature_time_names.contains(name.id.as_str()) => {
            Some("datetime.datetime".to_string())
        }
        // Primary[x] -> x, Windowed[x] -> dict[str, x]
        Expr::Subscript(subscript) => {
            if let Expr::Name(name) = &*subscript.value {
                if imports.primary_names.contains(name.id.as_str()) {
                    let inner = &subscript.slice;
                    return Some(format_expr_as_source(inner));
                }
                if imports.windowed_names.contains(name.id.as_str()) {
                    let inner = format_expr_as_source(&subscript.slice);
                    return Some(format!("dict[str, {inner}]"));
                }
            }
            None
        }
        _ => None,
    }
}

/// Format an expression back to source text (simple cases only).
fn format_expr_as_source(expr: &Expr) -> String {
    match expr {
        Expr::Name(name) => name.id.to_string(),
        Expr::Subscript(sub) => {
            let base = format_expr_as_source(&sub.value);
            let slice = format_expr_as_source(&sub.slice);
            format!("{base}[{slice}]")
        }
        Expr::Attribute(attr) => {
            let base = format_expr_as_source(&attr.value);
            format!("{base}.{}", attr.attr)
        }
        // Fallback: just use "Any"
        _ => "Any".to_string(),
    }
}

/// If `(class_name, field_name)` is a has-one or has-many in the type_map,
/// return its non-nullable target type so `Class.has_one.subfield` resolves
/// cleanly under ty (which would otherwise complain that `subfield` is "not
/// defined on None"). Scalar fields are left untouched — callers' nullability
/// annotations on plain scalars are correct and meaningful.
fn resolve_relationship_field(
    class_name: &str,
    field_name: &str,
    type_map: &TypeMap,
) -> Option<String> {
    let info = type_map
        .features
        .get(&(class_name.to_string(), field_name.to_string()))?;
    // has-one's python_type is the foreign class name (e.g. "Customer").
    // has-many's is "DataFrame[Customer]". Both are known classes / generic.
    if info.python_type.starts_with("DataFrame[")
        || type_map.class_fields.contains_key(&info.python_type)
    {
        return Some(info.python_type.clone());
    }
    None
}

/// Resolve string-quoted annotations like `"Jar.jar_id"` or `"OomB.id"`.
/// These are forward references to feature fields used as foreign keys.
fn resolve_string_annotation(expr: &Expr, _source: &str, type_map: &TypeMap) -> Option<String> {
    let Expr::StringLiteral(string_lit) = expr else {
        return None;
    };
    let value = string_lit.value.to_str();

    // Try to parse as "ClassName.field_name" pattern.
    let parts: Vec<&str> = value.split('.').collect();
    if parts.len() == 2 {
        let class_name = parts[0].trim();
        let field_name = parts[1].trim();
        if let Some(info) = type_map
            .features
            .get(&(class_name.to_string(), field_name.to_string()))
        {
            return Some(info.annotation());
        }
    }
    None
}

/// Handle a resolver function: replace param annotations and return type.
fn handle_function_def(
    func_def: &StmtFunctionDef,
    source: &str,
    type_map: &TypeMap,
    imports: &ChalkImports,
    edits: &mut Vec<Edit>,
    return_typedicts: &mut Vec<String>,
    typeddict_counter: &mut u32,
) {
    let is_resolver =
        find_matching_decorator(&func_def.decorator_list, &imports.resolver_decorator_names)
            .is_some();

    if !is_resolver {
        return;
    }

    // Replace the resolver decorator with a plain function (remove it).
    if let Some(dec) =
        find_matching_decorator(&func_def.decorator_list, &imports.resolver_decorator_names)
    {
        let dec_range = dec.range();
        // Replace decorator with comments (may span multiple lines).
        let dec_text = &source[dec_range.start().to_usize()..dec_range.end().to_usize()];
        let commented = dec_text
            .lines()
            .map(|line| format!("# {line}"))
            .collect::<Vec<_>>()
            .join("\n");
        edits.push(Edit {
            start: dec_range.start().to_usize(),
            end: dec_range.end().to_usize(),
            replacement: commented,
        });
    }

    // Transform parameter annotations: User.id -> int
    for param in func_def
        .parameters
        .args
        .iter()
        .chain(func_def.parameters.posonlyargs.iter())
        .chain(func_def.parameters.kwonlyargs.iter())
    {
        let Some(ref annotation) = param.parameter.annotation else {
            continue;
        };
        if let Some(replacement) = resolve_feature_ref_annotation(annotation, source, type_map) {
            let range = annotation.range();
            edits.push(Edit {
                start: range.start().to_usize(),
                end: range.end().to_usize(),
                replacement: localize_type(&replacement, imports),
            });
        }
    }

    // Transform return annotation: Features[User.name, User.score] -> TypedDict
    if let Some(ref returns) = func_def.returns {
        if let Some(replacement) = resolve_return_annotation(
            returns,
            source,
            type_map,
            imports,
            return_typedicts,
            typeddict_counter,
            &func_def.name,
        ) {
            let range = returns.range();
            edits.push(Edit {
                start: range.start().to_usize(),
                end: range.end().to_usize(),
                replacement: localize_type(&replacement, imports),
            });
        }
    }
}

/// Try to resolve a feature reference annotation like `User.id`,
/// `User.credit_report.credit_score` (has-one path), or
/// `User.transactions[Transaction.amount]` (has-many with subscript) to its Python type.
fn resolve_feature_ref_annotation(
    expr: &Expr,
    _source: &str,
    type_map: &TypeMap,
) -> Option<String> {
    // Handle has-many subscript: User.transactions[Transaction.amount]
    // The outer expr is a Subscript whose value is the attribute chain.
    // We resolve the chain and if it yields a DataFrame[X], keep it.
    let attr_expr = if let Expr::Subscript(subscript) = expr {
        &*subscript.value
    } else {
        expr
    };

    // Collect the attribute chain, e.g. User.credit_report.credit_score
    // becomes ["User", "credit_report", "credit_score"].
    let mut chain = Vec::new();
    let mut current = attr_expr;
    loop {
        match current {
            Expr::Attribute(attr) => {
                chain.push(attr.attr.as_str());
                current = &attr.value;
            }
            Expr::Name(name) => {
                chain.push(name.id.as_str());
                break;
            }
            _ => return None,
        }
    }
    // chain is reversed: ["credit_score", "credit_report", "User"]
    chain.reverse();
    // Now: ["User", "credit_report", "credit_score"]

    if chain.len() < 2 {
        return None;
    }

    // Walk the chain: start with class name, follow has-one relationships.
    let mut class_name = chain[0].to_string();
    for &field_name in &chain[1..chain.len() - 1] {
        // Intermediate fields must be has-one or has-many relationships.
        let info = type_map
            .features
            .get(&(class_name.clone(), field_name.to_string()))?;
        // The python_type for a has-one is the foreign class name,
        // for a has-many it's "DataFrame[ForeignClass]".
        class_name = info.python_type.clone();
    }

    // Final field is the leaf.
    let leaf_field = chain[chain.len() - 1];
    let info = type_map
        .features
        .get(&(class_name, leaf_field.to_string()))?;
    Some(info.annotation())
}

/// Resolve a return annotation like `Features[User.name, User.score]`.
fn resolve_return_annotation(
    expr: &Expr,
    source: &str,
    type_map: &TypeMap,
    imports: &ChalkImports,
    return_typedicts: &mut Vec<String>,
    typeddict_counter: &mut u32,
    func_name: &str,
) -> Option<String> {
    // Handle bare feature ref like `User.today` as return type.
    if let Expr::Attribute(attr) = expr {
        let class_name = expr_to_simple_name(&attr.value)?;
        let field_name = attr.attr.as_str();
        let info = type_map
            .features
            .get(&(class_name, field_name.to_string()))?;
        return Some(info.annotation());
    }

    // Handle plain class name like `User`.
    if let Expr::Name(name) = expr {
        if type_map.class_fields.contains_key(name.id.as_str()) {
            return Some(name.id.to_string());
        }
    }

    // Match Features[...] pattern.
    let Expr::Subscript(subscript) = expr else {
        return None;
    };

    let Expr::Name(ref base_name) = *subscript.value else {
        return None;
    };

    // Check if this is Features[...] or DataFrame[...]
    if imports.features_type_names.contains(base_name.id.as_str()) {
        return resolve_features_subscript(
            &subscript.slice,
            source,
            type_map,
            imports,
            return_typedicts,
            typeddict_counter,
            func_name,
        );
    }

    if imports.dataframe_names.contains(base_name.id.as_str()) {
        // DataFrame[...] return type -> strip generic args to bare DataFrame.
        return Some("DataFrame".to_string());
    }

    None
}

/// Resolve the contents of Features[User.name, User.score] into a TypedDict.
fn resolve_features_subscript(
    slice: &Expr,
    _source: &str,
    type_map: &TypeMap,
    imports: &ChalkImports,
    return_typedicts: &mut Vec<String>,
    typeddict_counter: &mut u32,
    func_name: &str,
) -> Option<String> {
    // Collect all feature refs from the subscript.
    let feature_refs = match slice {
        // Single feature: Features[User.name]
        Expr::Attribute(_) => vec![slice],
        // Single class: Features[User]
        Expr::Name(name) => {
            // Return the whole class as the type.
            return Some(name.id.to_string());
        }
        // Multiple features: Features[User.name, User.score]
        Expr::Tuple(tuple) => tuple.elts.iter().collect(),
        _ => return None,
    };

    // Build TypedDict fields.
    let mut fields: Vec<(String, String)> = Vec::new();
    for ref_expr in &feature_refs {
        let Expr::Attribute(attr) = ref_expr else {
            continue;
        };
        let Some(class_name) = expr_to_simple_name(&attr.value) else {
            continue;
        };
        let field_name = attr.attr.as_str();
        let info = type_map.features.get(&(class_name, field_name.to_string()));
        let type_str = info
            .map(|i| localize_type(&i.annotation(), imports))
            .unwrap_or_else(|| "Any".to_string());
        fields.push((field_name.to_string(), type_str));
    }

    if fields.is_empty() {
        return Some("Any".to_string());
    }

    // Generate a TypedDict name based on the function name.
    let td_name = format!("__{func_name}_Return",);
    *typeddict_counter += 1;

    let mut td = format!("class {td_name}(TypedDict):\n");
    for (name, typ) in &fields {
        td.push_str(&format!("    {name}: {typ}\n"));
    }

    return_typedicts.push(td);
    Some(td_name)
}

/// Extract a simple name from an expression (e.g., `User` from an ExprName).
fn expr_to_simple_name(expr: &Expr) -> Option<String> {
    match expr {
        Expr::Name(name) => Some(name.id.to_string()),
        _ => None,
    }
}

/// Find a decorator that matches one of the given names.
fn find_matching_decorator<'a>(
    decorators: &'a [Decorator],
    names: &HashSet<String>,
) -> Option<&'a Decorator> {
    decorators.iter().find(|dec| match &dec.expression {
        Expr::Name(name) => names.contains(name.id.as_str()),
        Expr::Call(call) => {
            if let Expr::Name(name) = call.func.as_ref() {
                names.contains(name.id.as_str())
            } else {
                false
            }
        }
        _ => false,
    })
}

/// Generate stub class definitions for all feature classes in the type map.
/// These are plain classes (not dataclasses) so ty doesn't enforce field ordering.
pub fn generate_feature_stubs(type_map: &TypeMap) -> String {
    let mut out = String::new();
    out.push_str("from __future__ import annotations\n\n");
    out.push_str("import datetime\n");
    out.push_str("import decimal\n");
    out.push_str("from typing import Any, Generic, TypeVar\n\n");
    // DataFrame stub: subscriptable via __class_getitem__.
    out.push_str("T = TypeVar(\"T\")\n\n\n");
    out.push_str("class DataFrame(Generic[T]):\n");
    out.push_str("    \"\"\"Stub for chalk.features.DataFrame.\"\"\"\n\n");
    out.push_str("    def __init__(self, *args: Any, **kwargs: Any) -> None: ...\n\n");
    out.push_str("    @classmethod\n");
    out.push_str("    def read_csv(cls, *args: Any, **kwargs: Any) -> DataFrame[Any]:\n");
    out.push_str("        return DataFrame()  # type: ignore\n\n");
    out.push_str("    @classmethod\n");
    out.push_str("    def read_parquet(cls, *args: Any, **kwargs: Any) -> DataFrame[Any]:\n");
    out.push_str("        return DataFrame()  # type: ignore\n\n\n");

    // Sort class names for deterministic output.
    let mut class_names: Vec<&String> = type_map.class_fields.keys().collect();
    class_names.sort();

    for class_name in class_names {
        let fields = &type_map.class_fields[class_name];
        out.push_str(&format!("class {class_name}:\n"));
        if fields.is_empty() {
            out.push_str("    pass\n");
        } else {
            for (field_name, type_str) in fields {
                out.push_str(&format!("    {field_name}: {type_str}\n"));
            }
        }
        // Add __init__ that accepts any kwargs so constructors type-check.
        out.push_str("    def __init__(self, **kwargs: Any) -> None: ...\n");
        out.push_str("\n\n");
    }

    out
}
