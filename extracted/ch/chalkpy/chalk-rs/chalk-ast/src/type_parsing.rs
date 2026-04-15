use std::collections::{HashMap, HashSet};

use chalk_utils::to_snake_case;
use lsp_types::{Location, Position, Range, Uri};
use ruff_python_ast::statement_visitor::{self, StatementVisitor};
use ruff_python_ast::{Decorator, Expr, Keyword, Stmt, StmtClassDef, StmtFunctionDef};
use ruff_python_trivia::CommentRanges;
use ruff_source_file::{LineIndex, SourceCode};
use ruff_text_size::{Ranged, TextRange, TextSize};

use crate::ast_types::{
    FeatureClassAST, FeatureFieldAST, FunctionArgAST, ParsedAstFile, ResolverAST,
};
use crate::parser_cache_types::{ImportAliasMap, KwargLocationMap, ParsedFileCache};

const FEATURE_CLASS_DECORATOR_MODULE: &str = "chalk.features";
const RESOLVER_DECORATOR_MODULES: [&str; 2] = ["chalk", "chalk.features"];
const RESOLVER_DECORATOR_SYMBOLS: [&str; 3] = ["online", "offline", "stream"];

pub fn parse_ast_file_with_feature_module(
    file: &ParsedFileCache,
    feature_class_module: &str,
) -> ParsedAstFile {
    let definitions = collect_nested_definitions(&file.stmts);
    let functions = collect_function_asts(file, &definitions.function_defs, feature_class_module);

    ParsedAstFile {
        feature_classes: collect_feature_class_asts(
            file,
            &definitions.class_defs,
            feature_class_module,
        ),
        functions: functions.clone(),
        resolvers: collect_resolver_asts(&functions),
    }
}

fn collect_feature_class_asts(
    file: &ParsedFileCache,
    class_defs: &[&StmtClassDef],
    feature_class_module: &str,
) -> Vec<FeatureClassAST> {
    let imported_feature_names =
        collect_import_names_from_map(&file.imports, &[FEATURE_CLASS_DECORATOR_MODULE], "features");
    if imported_feature_names.is_empty() {
        return Vec::new();
    }

    let line_index = LineIndex::from_source_text(&file.source);
    let source_code = SourceCode::new(&file.source, &line_index);
    let mut asts = Vec::new();

    for class_def in class_defs {
        let class_name = class_def.name.as_str().to_string();
        let Some(class_name_location) = file_location_for_range(
            &file.path,
            identifier_to_range(&class_def.name, &source_code),
        ) else {
            continue;
        };
        let Some(class_definition_location) = line_location_for_offset(
            &file.path,
            class_def.name.range().start().to_usize(),
            &file.source,
            &source_code,
        ) else {
            continue;
        };
        let field_stmts = collect_class_field_statements(&class_def.body);
        let field_comments = collect_feature_class_field_comments(
            &field_stmts,
            class_def.range(),
            &file.source,
            &source_code,
            &file.comment_ranges,
        );
        let annotations = collect_feature_class_fields(
            &field_stmts,
            &file.path,
            &source_code,
            &file.source,
            &field_comments,
        );
        let fields = build_feature_class_field_map(
            &field_stmts,
            &file.path,
            &source_code,
            &file.source,
            &field_comments,
            &annotations,
        );

        let Some(matched_decorator) =
            find_matching_feature_decorator(class_def, &imported_feature_names)
        else {
            continue;
        };
        let Some(decorator_location) = file_location_for_range(
            &file.path,
            expr_to_range(&matched_decorator.expression, &source_code),
        ) else {
            continue;
        };
        let (kwarg_names, kwargs) = match &matched_decorator.expression {
            Expr::Call(call) => keyword_location_maps(
                &call.arguments.keywords,
                &file.source,
                &source_code,
                &file.path,
            ),
            _ => (HashMap::new(), HashMap::new()),
        };
        let namespace = feature_class_namespace(&class_name, matched_decorator);
        let Some(source) = feature_class_source(class_def, &file.source) else {
            continue;
        };

        asts.push(FeatureClassAST {
            module: feature_class_module.to_string(),
            namespace,
            class_name: class_name.clone(),
            source,
            class_name_location: class_name_location.clone(),
            class_definition_location,
            decorator_location,
            kwarg_names,
            kwargs,
            fields,
            annotations,
        });
    }

    asts
}

fn collect_feature_class_fields(
    field_stmts: &[&Stmt],
    file_path: &str,
    source_code: &SourceCode,
    source: &str,
    field_comments: &HashMap<String, FieldCommentMetadata>,
) -> Vec<FeatureFieldAST> {
    let mut annotations = Vec::new();

    for stmt in field_stmts {
        match stmt {
            Stmt::AnnAssign(ann) => {
                let Expr::Name(name) = ann.target.as_ref() else {
                    continue;
                };
                let field_name = name.id.as_str().to_string();
                let comment_metadata = field_comments.get(&field_name).cloned().unwrap_or_default();
                let field_name_location =
                    file_location_for_range(file_path, expr_name_to_range(name, source_code))
                        .expect("field name location should exist");
                let mut field_definition = new_feature_field_ast(
                    field_name.clone(),
                    field_name_location,
                    &comment_metadata,
                );
                field_definition.annotation =
                    file_location_for_range(file_path, expr_to_range(&ann.annotation, source_code));

                let Some(value_expr) = ann.value.as_deref() else {
                    annotations.push(field_definition);
                    continue;
                };
                let Expr::Call(call) = value_expr else {
                    annotations.push(field_definition);
                    continue;
                };
                field_definition.feature_call =
                    file_location_for_range(file_path, expr_to_range(value_expr, source_code));
                let (kwarg_names, kwargs) =
                    keyword_location_maps(&call.arguments.keywords, source, source_code, file_path);
                field_definition.kwarg_names = kwarg_names.clone();
                field_definition.kwargs = kwargs.clone();
                annotations.push(field_definition);
            }
            _ => {}
        }
    }

    annotations
}

fn build_feature_class_field_map(
    field_stmts: &[&Stmt],
    file_path: &str,
    source_code: &SourceCode,
    source: &str,
    field_comments: &HashMap<String, FieldCommentMetadata>,
    annotations: &[FeatureFieldAST],
) -> HashMap<String, FeatureFieldAST> {
    let mut fields = HashMap::new();

    for annotation in annotations {
        fields
            .entry(annotation.field_name.clone())
            .or_insert_with(|| annotation.clone());
    }

    for stmt in field_stmts {
        let Stmt::Assign(assign) = stmt else {
            continue;
        };
        if assign.targets.len() != 1 {
            continue;
        }
        let Expr::Name(name) = &assign.targets[0] else {
            continue;
        };
        let field_name = name.id.as_str().to_string();
        let comment_metadata = field_comments.get(&field_name).cloned().unwrap_or_default();
        let field_name_location =
            file_location_for_range(file_path, expr_name_to_range(name, source_code))
                .expect("field name location should exist");
        let mut field_definition =
            new_feature_field_ast(field_name.clone(), field_name_location, &comment_metadata);
        field_definition.feature_call =
            file_location_for_range(file_path, expr_to_range(assign.value.as_ref(), source_code));
        if let Expr::Call(call) = assign.value.as_ref() {
            let (kwarg_names, kwargs) =
                keyword_location_maps(&call.arguments.keywords, source, source_code, file_path);
            field_definition.kwarg_names = kwarg_names;
            field_definition.kwargs = kwargs;
        }

        let field = fields
            .entry(field_name)
            .or_insert_with(|| field_definition.clone());
        populate_field_comment_metadata(field, comment_metadata);
        field.feature_call = field_definition.feature_call;
        field.kwarg_names = field_definition.kwarg_names;
        field.kwargs = field_definition.kwargs;
    }

    fields
}

fn feature_class_source(class_def: &StmtClassDef, source: &str) -> Option<String> {
    let start = class_def
        .decorator_list
        .first()
        .map(|decorator| decorator.range.start())
        .unwrap_or_else(|| class_def.range().start());
    dedented_source_for_range(start, class_def.range().end(), source)
}

fn dedented_source_for_range(start: TextSize, end: TextSize, source: &str) -> Option<String> {
    let start = line_start_offset(source, start.to_usize())?;
    let end = line_end_offset(source, end.to_usize())?;
    let source = source.get(start..end)?;
    Some(dedent_source(source))
}

fn line_start_offset(source: &str, offset: usize) -> Option<usize> {
    let prefix = source.get(..offset)?;
    Some(prefix.rfind('\n').map_or(0, |index| index + 1))
}

fn line_end_offset(source: &str, offset: usize) -> Option<usize> {
    let suffix = source.get(offset..)?;
    Some(
        suffix
            .find('\n')
            .map_or(source.len(), |index| offset + index + 1),
    )
}

fn dedent_source(source: &str) -> String {
    let margin = source
        .split_inclusive('\n')
        .filter_map(|line| {
            let (content, _) = split_line_ending(line);
            (!content.trim().is_empty()).then_some(
                content
                    .chars()
                    .take_while(|character| matches!(character, ' ' | '\t'))
                    .collect::<String>(),
            )
        })
        .reduce(|margin, indent| common_whitespace_prefix(&margin, &indent))
        .unwrap_or_default();

    let mut dedented = String::with_capacity(source.len());
    for line in source.split_inclusive('\n') {
        let (content, line_ending) = split_line_ending(line);
        if content.trim().is_empty() {
            dedented.push_str(line_ending);
            continue;
        }

        let stripped = content.strip_prefix(&margin).unwrap_or(content);
        dedented.push_str(stripped);
        dedented.push_str(line_ending);
    }

    dedented
}

fn split_line_ending(line: &str) -> (&str, &str) {
    if let Some(content) = line.strip_suffix("\r\n") {
        (content, "\r\n")
    } else if let Some(content) = line.strip_suffix('\n') {
        (content, "\n")
    } else {
        (line, "")
    }
}

fn common_whitespace_prefix(left: &str, right: &str) -> String {
    left.chars()
        .zip(right.chars())
        .take_while(|(left, right)| left == right && matches!(left, ' ' | '\t'))
        .map(|(character, _)| character)
        .collect()
}

fn collect_feature_class_field_comments(
    field_stmts: &[&Stmt],
    class_range: TextRange,
    source: &str,
    source_code: &SourceCode,
    comment_ranges: &CommentRanges,
) -> HashMap<String, FieldCommentMetadata> {
    if field_stmts.is_empty() {
        return HashMap::new();
    }

    let mut comments_by_field = HashMap::new();
    let mut comments = comment_ranges
        .comments_in_range(class_range)
        .iter()
        .copied()
        .filter(|comment| CommentRanges::is_own_line(comment.start(), source))
        .map(|comment| CommentLine {
            line: source_code.line_column(comment.start()).line.get() as usize,
            text: normalize_comment_text(&source[comment]),
        })
        .peekable();
    let mut pending_comment_lines = Vec::new();
    let mut last_comment_line = None;

    for stmt in field_stmts {
        let stmt_start_line = source_code.line_column(stmt.range().start()).line.get() as usize;

        while comments
            .peek()
            .is_some_and(|comment| comment.line < stmt_start_line)
        {
            let comment = comments
                .next()
                .expect("peekable comment iterator should contain a comment");
            if last_comment_line.is_some_and(|line| line + 1 == comment.line) {
                pending_comment_lines.push(comment.text);
            } else {
                pending_comment_lines.clear();
                pending_comment_lines.push(comment.text);
            }
            last_comment_line = Some(comment.line);
        }

        if last_comment_line.is_some_and(|line| line + 1 == stmt_start_line) {
            if let Some(field_name) = feature_field_name(stmt) {
                comments_by_field.insert(
                    field_name,
                    parse_field_comment_metadata(&pending_comment_lines),
                );
            }
        }

        pending_comment_lines.clear();
        last_comment_line = None;
    }

    comments_by_field
}

fn collect_class_field_statements<'a>(body: &'a [Stmt]) -> Vec<&'a Stmt> {
    let mut collector = ClassFieldCollector::default();
    collector.visit_body(body);
    collector.field_stmts
}

#[derive(Clone)]
struct CommentLine {
    line: usize,
    text: String,
}

#[derive(Clone, Default)]
struct FieldCommentMetadata {
    comment: Option<String>,
    description: Option<String>,
    owner: Option<String>,
    tags: Vec<String>,
}

#[derive(Default)]
struct ClassFieldCollector<'a> {
    field_stmts: Vec<&'a Stmt>,
    depth: usize,
}

impl<'a> StatementVisitor<'a> for ClassFieldCollector<'a> {
    fn visit_stmt(&mut self, stmt: &'a Stmt) {
        if self.depth == 0 && feature_field_name(stmt).is_some() {
            self.field_stmts.push(stmt);
        }

        self.depth += 1;
        statement_visitor::walk_stmt(self, stmt);
        self.depth -= 1;
    }
}

fn new_feature_field_ast(
    field_name: String,
    field_name_location: Location,
    metadata: &FieldCommentMetadata,
) -> FeatureFieldAST {
    FeatureFieldAST {
        field_name,
        field_name_location,
        comment: metadata.comment.clone(),
        description: metadata.description.clone(),
        owner: metadata.owner.clone(),
        tags: metadata.tags.clone(),
        annotation: None,
        feature_call: None,
        kwarg_names: HashMap::new(),
        kwargs: HashMap::new(),
    }
}

fn populate_field_comment_metadata(field: &mut FeatureFieldAST, metadata: FieldCommentMetadata) {
    if field.comment.is_none() {
        field.comment = metadata.comment;
    }
    if field.description.is_none() {
        field.description = metadata.description;
    }
    if field.owner.is_none() {
        field.owner = metadata.owner;
    }
    if field.tags.is_empty() {
        field.tags = metadata.tags;
    }
}

fn parse_field_comment_metadata(comment_lines: &[String]) -> FieldCommentMetadata {
    if comment_lines.is_empty() {
        return FieldCommentMetadata::default();
    }

    let comment = comment_lines.join("\n");
    let mut description_lines = Vec::new();
    let mut owner = None;
    let mut tags = Vec::new();

    for line in comment.lines() {
        let stripped_line = line.trim();
        if let Some(value) = stripped_line.strip_prefix(":owner:") {
            owner = Some(value.trim().to_string());
        } else if let Some(value) = stripped_line.strip_prefix(":tags:") {
            tags.extend(parse_tags(value));
        } else {
            description_lines.push(line.to_string());
        }
    }

    let description = (!description_lines.is_empty())
        .then(|| description_lines.join("\n"))
        .filter(|description| !description.trim().is_empty());

    FieldCommentMetadata {
        comment: Some(comment),
        description,
        owner,
        tags,
    }
}

fn feature_field_name(stmt: &Stmt) -> Option<String> {
    match stmt {
        Stmt::AnnAssign(ann) => {
            let Expr::Name(name) = ann.target.as_ref() else {
                return None;
            };
            Some(name.id.as_str().to_string())
        }
        Stmt::Assign(assign) if assign.targets.len() == 1 => {
            let Expr::Name(name) = &assign.targets[0] else {
                return None;
            };
            Some(name.id.as_str().to_string())
        }
        _ => None,
    }
}

fn normalize_comment_text(comment: &str) -> String {
    comment.trim_start_matches('#').trim().to_string()
}

fn parse_tags(tags: &str) -> Vec<String> {
    tags.replace(',', " ")
        .split_whitespace()
        .map(str::to_string)
        .collect()
}

fn collect_function_asts(
    file: &ParsedFileCache,
    function_defs: &[&StmtFunctionDef],
    module_name: &str,
) -> Vec<ResolverAST> {
    let imported_resolver_decorators: HashSet<String> = RESOLVER_DECORATOR_MODULES
        .iter()
        .flat_map(|module| {
            collect_import_names_for_symbols_from_map(
                &file.imports,
                &[*module],
                &RESOLVER_DECORATOR_SYMBOLS,
            )
            .into_iter()
        })
        .collect();

    let line_index = LineIndex::from_source_text(&file.source);
    let source_code = SourceCode::new(&file.source, &line_index);
    let mut asts = Vec::new();

    for function_def in function_defs {
        let resolver_name = function_def.name.as_str().to_string();
        let Some(resolver_name_location) = file_location_for_range(
            &file.path,
            identifier_to_range(&function_def.name, &source_code),
        ) else {
            continue;
        };
        let (args_in_order, args) = function_arg_maps(function_def, &file.path, &source_code);
        let return_annotation = function_def.returns.as_deref().and_then(|expr| {
            file_location_for_range(&file.path, expr_to_range(expr, &source_code))
        });
        let missing_return_annotation = if function_def.returns.is_none() {
            missing_return_annotation_range(function_def, &file.source, &source_code)
                .and_then(|range| file_location_for_range(&file.path, range))
        } else {
            None
        };
        let return_statements: Vec<Location> = return_statement_ranges(function_def, &source_code)
            .into_iter()
            .filter_map(|range| file_location_for_range(&file.path, range))
            .collect();
        let body = function_body_range(function_def, &source_code)
            .and_then(|range| file_location_for_range(&file.path, range));
        let return_arg = first_return_arg_range(function_def, &source_code)
            .and_then(|range| file_location_for_range(&file.path, range));
        let matched_decorator =
            find_matching_resolver_decorator(function_def, &imported_resolver_decorators);
        let decorator_location = matched_decorator.and_then(|decorator| {
            file_location_for_range(
                &file.path,
                expr_to_range(&decorator.expression, &source_code),
            )
        });
        let (kwarg_names, kwargs, kwarg_dict_key_names, kwarg_dict_values) =
            match matched_decorator.map(|decorator| &decorator.expression) {
                Some(Expr::Call(call)) => {
                    let (kwarg_names, kwargs) = keyword_location_maps(
                        &call.arguments.keywords,
                        &file.source,
                        &source_code,
                        &file.path,
                    );
                    let (kwarg_dict_key_names, kwarg_dict_values) = keyword_dict_location_maps(
                        &call.arguments.keywords,
                        &source_code,
                        &file.path,
                    );
                    (kwarg_names, kwargs, kwarg_dict_key_names, kwarg_dict_values)
                }
                _ => (
                    HashMap::new(),
                    HashMap::new(),
                    HashMap::new(),
                    HashMap::new(),
                ),
            };

        asts.push(ResolverAST {
            module: module_name.to_string(),
            resolver_name: resolver_name.clone(),
            resolver_name_location: resolver_name_location.clone(),
            decorator_location,
            kwarg_names,
            kwargs,
            kwarg_dict_key_names,
            kwarg_dict_values,
            args_in_order: args_in_order.clone(),
            args: args.clone(),
            return_annotation: return_annotation.clone(),
            missing_return_annotation: missing_return_annotation.clone(),
            return_statements: return_statements.clone(),
            body: body.clone(),
            return_arg: return_arg.clone(),
        });
    }

    asts
}

fn collect_resolver_asts(functions: &[ResolverAST]) -> Vec<ResolverAST> {
    functions
        .iter()
        .filter(|function_ast| function_ast.decorator_location.is_some())
        .cloned()
        .collect()
}

fn collect_nested_definitions(stmts: &[Stmt]) -> NestedDefinitions<'_> {
    let mut collector = DefinitionCollector::default();
    collector.visit_body(stmts);
    NestedDefinitions {
        class_defs: collector.class_defs,
        function_defs: collector.function_defs,
    }
}

#[derive(Default)]
struct DefinitionCollector<'a> {
    class_defs: Vec<&'a StmtClassDef>,
    function_defs: Vec<&'a StmtFunctionDef>,
}

impl<'a> StatementVisitor<'a> for DefinitionCollector<'a> {
    fn visit_stmt(&mut self, stmt: &'a Stmt) {
        match stmt {
            Stmt::ClassDef(class_def) => self.class_defs.push(class_def),
            Stmt::FunctionDef(function_def) => self.function_defs.push(function_def),
            _ => {}
        }

        statement_visitor::walk_stmt(self, stmt);
    }
}

struct NestedDefinitions<'a> {
    class_defs: Vec<&'a StmtClassDef>,
    function_defs: Vec<&'a StmtFunctionDef>,
}

fn feature_class_namespace(class_name: &str, decorator: &Decorator) -> String {
    decorator_name_kwarg_value(&decorator.expression).unwrap_or_else(|| to_snake_case(class_name))
}

fn decorator_name_kwarg_value(expr: &Expr) -> Option<String> {
    let Expr::Call(call) = expr else {
        return None;
    };
    for keyword in &call.arguments.keywords {
        let Some(arg) = keyword.arg.as_ref() else {
            continue;
        };
        if arg.as_str() != "name" {
            continue;
        }
        if let Some(value) = expr_string_literal_value(&keyword.value) {
            return Some(value);
        }
    }
    None
}

fn expr_string_literal_value(expr: &Expr) -> Option<String> {
    let Expr::StringLiteral(string_literal) = expr else {
        return None;
    };
    let string = string_literal.as_single_part_string()?;
    Some(string.as_str().to_string())
}

fn keyword_location_maps(
    keywords: &[Keyword],
    source: &str,
    source_code: &SourceCode,
    file_path: &str,
) -> (KwargLocationMap, KwargLocationMap) {
    let mut kwarg_names = HashMap::new();
    let mut kwargs = HashMap::new();

    for keyword in keywords {
        let Some(arg) = keyword.arg.as_ref() else {
            continue;
        };
        let Some((name_range, value_range)) =
            keyword_name_and_value_ranges(keyword, source, source_code)
        else {
            continue;
        };
        let key = arg.as_str().to_string();
        if let Some(name_location) = file_location_for_range(file_path, name_range) {
            kwarg_names.insert(key.clone(), name_location);
        }
        if let Some(value_location) = file_location_for_range(file_path, value_range) {
            kwargs.insert(key, value_location);
        }
    }

    (kwarg_names, kwargs)
}

fn keyword_dict_location_maps(
    keywords: &[Keyword],
    source_code: &SourceCode,
    file_path: &str,
) -> (
    HashMap<String, KwargLocationMap>,
    HashMap<String, KwargLocationMap>,
) {
    let mut dict_key_names = HashMap::new();
    let mut dict_values = HashMap::new();

    for keyword in keywords {
        let Some(arg) = keyword.arg.as_ref() else {
            continue;
        };
        let Expr::Dict(dict) = &keyword.value else {
            continue;
        };

        let mut key_names = HashMap::new();
        let mut value_locations = HashMap::new();
        for item in &dict.items {
            let Some(key_expr) = item.key.as_ref() else {
                continue;
            };
            let Some(key_name) = expr_string_literal_value(key_expr) else {
                continue;
            };
            if let Some(key_location) =
                file_location_for_range(file_path, expr_to_range(key_expr, source_code))
            {
                key_names.insert(key_name.clone(), key_location);
            }
            if let Some(value_location) =
                file_location_for_range(file_path, expr_to_range(&item.value, source_code))
            {
                value_locations.insert(key_name, value_location);
            }
        }

        if !key_names.is_empty() {
            dict_key_names.insert(arg.as_str().to_string(), key_names);
        }
        if !value_locations.is_empty() {
            dict_values.insert(arg.as_str().to_string(), value_locations);
        }
    }

    (dict_key_names, dict_values)
}

fn collect_import_names_from_map(
    imports: &ImportAliasMap,
    modules: &[&str],
    symbol: &str,
) -> HashSet<String> {
    collect_import_names_for_symbols_from_map(imports, modules, &[symbol])
}

fn collect_import_names_for_symbols_from_map(
    imports: &ImportAliasMap,
    modules: &[&str],
    symbols: &[&str],
) -> HashSet<String> {
    let mut names = HashSet::new();

    for module in modules {
        let Some(symbol_map) = imports.get(*module) else {
            continue;
        };
        for symbol in symbols {
            let Some(local_names) = symbol_map.get(*symbol) else {
                continue;
            };
            names.extend(local_names.iter().cloned());
        }
    }

    names
}

fn find_matching_feature_decorator<'a>(
    class_def: &'a StmtClassDef,
    imported_feature_names: &HashSet<String>,
) -> Option<&'a Decorator> {
    class_def
        .decorator_list
        .iter()
        .find(|decorator| match &decorator.expression {
            Expr::Name(name) => imported_feature_names.contains(name.id.as_str()),
            Expr::Call(call) => {
                call_func_is_imported_name(call.func.as_ref(), imported_feature_names)
            }
            _ => false,
        })
}

fn find_matching_resolver_decorator<'a>(
    function_def: &'a StmtFunctionDef,
    imported_resolver_decorators: &HashSet<String>,
) -> Option<&'a Decorator> {
    function_def
        .decorator_list
        .iter()
        .find(|decorator| match &decorator.expression {
            Expr::Name(name) => imported_resolver_decorators.contains(name.id.as_str()),
            Expr::Call(call) => {
                call_func_is_imported_name(call.func.as_ref(), imported_resolver_decorators)
            }
            _ => false,
        })
}

fn call_func_is_imported_name(func: &Expr, imported_names: &HashSet<String>) -> bool {
    match func {
        Expr::Name(name) => imported_names.contains(name.id.as_str()),
        _ => false,
    }
}

fn keyword_name_and_value_ranges(
    keyword: &Keyword,
    source: &str,
    source_code: &SourceCode,
) -> Option<(Range, Range)> {
    let kwarg = keyword.arg.as_ref()?.as_str();
    let name_range = keyword_name_range(keyword, kwarg, source, source_code)?;
    let value_range = expr_to_range(&keyword.value, source_code);
    Some((name_range, value_range))
}

fn keyword_name_range(
    keyword: &Keyword,
    kwarg: &str,
    source: &str,
    source_code: &SourceCode,
) -> Option<Range> {
    let keyword_start = keyword.range().start().to_usize();
    let value_start = keyword.value.range().start().to_usize();

    if keyword_start >= source.len() || value_start > source.len() || keyword_start >= value_start {
        return None;
    }

    let prefix = &source[keyword_start..value_start];
    let rel_start = prefix.find(kwarg)?;
    let name_start = keyword_start + rel_start;
    let name_end = name_start + kwarg.len();

    Some(byte_offsets_to_range(name_start, name_end, source_code))
}

fn function_body_range(function_def: &StmtFunctionDef, source_code: &SourceCode) -> Option<Range> {
    let first = function_def.body.first()?;
    let last = function_def.body.last()?;
    let start = first.range().start().to_usize();
    let end = last.range().end().to_usize();
    Some(byte_offsets_to_range(start, end, source_code))
}

fn function_arg_maps(
    function_def: &StmtFunctionDef,
    file_path: &str,
    source_code: &SourceCode,
) -> (Vec<String>, HashMap<String, FunctionArgAST>) {
    let mut args_in_order = Vec::new();
    let mut args = HashMap::new();

    for parameter in function_def.parameters.iter() {
        let parameter = parameter.as_parameter();
        let arg_name = parameter.name.as_str().to_string();
        let arg_location = file_location_for_range(
            file_path,
            expr_or_parameter_range(parameter.range(), source_code),
        )
        .expect("function parameter location should exist");
        let annotation = parameter.annotation().and_then(|annotation| {
            file_location_for_range(file_path, expr_to_range(annotation, source_code))
        });

        args_in_order.push(arg_name.clone());
        args.insert(
            arg_name.clone(),
            FunctionArgAST {
                arg_name,
                arg_location,
                annotation,
            },
        );
    }

    (args_in_order, args)
}

fn return_statement_ranges(function_def: &StmtFunctionDef, source_code: &SourceCode) -> Vec<Range> {
    let mut collector = ReturnCollector::default();
    for stmt in &function_def.body {
        collector.visit_stmt(stmt);
    }
    collector
        .returns
        .into_iter()
        .map(|return_stmt| {
            byte_offsets_to_range(
                return_stmt.range().start().to_usize(),
                return_stmt.range().end().to_usize(),
                source_code,
            )
        })
        .collect()
}

fn first_return_arg_range(
    function_def: &StmtFunctionDef,
    source_code: &SourceCode,
) -> Option<Range> {
    for stmt in &function_def.body {
        let Stmt::Return(return_stmt) = stmt else {
            continue;
        };
        let value = return_stmt.value.as_deref()?;
        return Some(expr_to_range(value, source_code));
    }
    None
}

fn missing_return_annotation_range(
    function_def: &StmtFunctionDef,
    source: &str,
    source_code: &SourceCode,
) -> Option<Range> {
    let search_start = function_def.parameters.range().end().to_usize();
    let search_end = function_def
        .body
        .first()
        .map(|stmt| stmt.range().start().to_usize())
        .unwrap_or_else(|| function_def.range().end().to_usize());
    if search_start >= search_end || search_end > source.len() {
        return None;
    }

    let header_suffix = &source[search_start..search_end];
    let colon_index = header_suffix.find(':')?;
    let start = search_start + colon_index;
    Some(byte_offsets_to_range(start, start + 1, source_code))
}

fn file_location_for_range(file_path: &str, range: Range) -> Option<Location> {
    let path = std::path::Path::new(file_path);
    let absolute = if path.is_absolute() {
        path.to_path_buf()
    } else {
        std::fs::canonicalize(path).ok()?
    };
    let mut uri_path = absolute.to_string_lossy().replace('\\', "/");
    if !uri_path.starts_with('/') {
        uri_path = format!("/{}", uri_path);
    }
    uri_path = uri_path.replace(' ', "%20");
    let uri: Uri = format!("file://{}", uri_path).parse().ok()?;
    Some(Location { uri, range })
}

fn expr_to_range(expr: &Expr, source_code: &SourceCode) -> Range {
    let range = expr.range();
    byte_offsets_to_range(
        range.start().to_usize(),
        range.end().to_usize(),
        source_code,
    )
}

fn expr_or_parameter_range(range: TextRange, source_code: &SourceCode) -> Range {
    byte_offsets_to_range(
        range.start().to_usize(),
        range.end().to_usize(),
        source_code,
    )
}

fn identifier_to_range(
    identifier: &ruff_python_ast::Identifier,
    source_code: &SourceCode,
) -> Range {
    let range = identifier.range();
    byte_offsets_to_range(
        range.start().to_usize(),
        range.end().to_usize(),
        source_code,
    )
}

fn expr_name_to_range(name: &ruff_python_ast::ExprName, source_code: &SourceCode) -> Range {
    let range = name.range();
    byte_offsets_to_range(
        range.start().to_usize(),
        range.end().to_usize(),
        source_code,
    )
}

fn byte_offsets_to_range(start: usize, end: usize, source_code: &SourceCode) -> Range {
    let start = source_code.line_column(TextSize::new(start as u32));
    let end = source_code.line_column(TextSize::new(end as u32));

    Range {
        start: Position {
            line: start.line.get().saturating_sub(1) as u32,
            character: start.column.get().saturating_sub(1) as u32,
        },
        end: Position {
            line: end.line.get().saturating_sub(1) as u32,
            character: end.column.get().saturating_sub(1) as u32,
        },
    }
}

fn line_location_for_offset(
    file_path: &str,
    start: usize,
    source: &str,
    source_code: &SourceCode,
) -> Option<Location> {
    if start >= source.len() {
        return None;
    }
    let line_start = source[..start].rfind('\n').map_or(0, |index| index + 1);
    let line_end = source[start..]
        .find('\n')
        .map_or(source.len(), |index| start + index);
    file_location_for_range(
        file_path,
        byte_offsets_to_range(line_start, line_end, source_code),
    )
}

#[derive(Default)]
struct ReturnCollector<'a> {
    returns: Vec<&'a ruff_python_ast::StmtReturn>,
}

impl<'a> StatementVisitor<'a> for ReturnCollector<'a> {
    fn visit_stmt(&mut self, stmt: &'a Stmt) {
        if let Stmt::Return(return_stmt) = stmt {
            self.returns.push(return_stmt);
        }
        statement_visitor::walk_stmt(self, stmt);
    }
}

#[cfg(test)]
mod tests {
    use ruff_python_parser::parse_module;
    use ruff_python_trivia::CommentRanges;

    use super::parse_ast_file_with_feature_module;
    use crate::{collect_import_alias_map, FeatureClassAST, ParsedAstFile, ParsedFileCache};

    struct ExpectedFieldMetadata<'a> {
        field_name: &'a str,
        comment: Option<&'a str>,
        description: Option<&'a str>,
        owner: Option<&'a str>,
        tags: &'a [&'a str],
        kwarg_count: usize,
    }

    fn parse_fixture(path: &str, source: &str) -> ParsedAstFile {
        let parsed = parse_module(source).expect("source should parse");
        let stmts = parsed.suite().to_vec();
        let imports = collect_import_alias_map(&stmts);
        let comment_ranges = CommentRanges::from(parsed.tokens());
        let file = ParsedFileCache {
            path: path.to_string(),
            source: source.to_string(),
            stmts,
            imports,
            comment_ranges,
        };

        parse_ast_file_with_feature_module(&file, "test_module")
    }

    fn assert_field_metadata(
        feature_class: &FeatureClassAST,
        expected_fields: &[ExpectedFieldMetadata<'_>],
    ) {
        for expected in expected_fields {
            let field = feature_class
                .fields
                .get(expected.field_name)
                .unwrap_or_else(|| panic!("missing field {}", expected.field_name));

            assert_eq!(field.comment.as_deref(), expected.comment);
            assert_eq!(field.description.as_deref(), expected.description);
            assert_eq!(field.owner.as_deref(), expected.owner);
            assert_eq!(field.tags, expected.tags);
            assert_eq!(field.kwargs.len(), expected.kwarg_count);
        }
    }

    #[test]
    fn parses_feature_and_resolver_asts_from_parsed_file() {
        let typed = parse_fixture(
            "/tmp/mixed.py",
            r#"
from chalk.features import features
from chalk import online, feature

@features(name="bank_account")
class BankAccount:
    balance: int = feature(default=0, owner="risk")

@online(mode="continuous")
def compute_account(message: str):
    return message
"#,
        );

        assert_eq!(typed.feature_classes.len(), 1);
        assert_eq!(typed.functions.len(), 1);
        assert_eq!(typed.resolvers.len(), 1);
        assert_eq!(typed.feature_classes[0].class_name, "BankAccount");
        assert_eq!(typed.feature_classes[0].namespace, "bank_account");
        assert_eq!(typed.resolvers[0].resolver_name, "compute_account");
        assert_eq!(typed.feature_classes[0].fields["balance"].kwargs.len(), 2);
        assert_eq!(
            typed.resolvers[0].resolver_name_location.range.start.line,
            9
        );
        assert!(typed.feature_classes[0].kwargs.contains_key("name"));
    }

    #[test]
    fn collects_plain_functions_for_rust_only_function_lookup() {
        let typed = parse_fixture(
            "/tmp/plain_function.py",
            r#"
def parse_message(event: bytes) -> bytes:
    return event
"#,
        );

        assert_eq!(typed.feature_classes.len(), 0);
        assert_eq!(typed.functions.len(), 1);
        assert_eq!(typed.resolvers.len(), 0);

        let function = &typed.functions[0];
        assert_eq!(function.module, "test_module");
        assert_eq!(function.resolver_name, "parse_message");
        assert!(function.decorator_location.is_none());
        assert_eq!(function.args_in_order, vec!["event"]);
        assert!(function.return_annotation.is_some());
        assert_eq!(function.return_statements.len(), 1);
    }

    #[test]
    fn stores_unannotated_assignments_in_feature_field_map() {
        let typed = parse_fixture(
            "/tmp/unannotated.py",
            r#"
from chalk.features import features

@features
class Customer:
    id: str
    join_id = "PushdownRoot.id"
"#,
        );

        let feature_class = &typed.feature_classes[0];
        let field = feature_class
            .fields
            .get("join_id")
            .expect("unannotated assignment should still have a field entry");

        assert!(field.annotation.is_none());
        assert!(field.feature_call.is_some());
        assert!(field.kwargs.is_empty());
        assert_eq!(field.field_name_location.range.start.line, 6);
    }

    #[test]
    fn parses_field_comment_metadata_for_multiple_features() {
        let typed = parse_fixture(
            "/tmp/comments.py",
            r#"
from chalk.features import features
from chalk import feature

@features(name="customer")
class Customer:
    id: int

    # Display name shown in the UI.
    # :tags: pii, profile
    display_name: str

    # Latitude and longitude from the last mobile session.
    # :owner: geo@chalk.ai
    location: str

    # Risk score for fraud workflows.
    # :tags: fraud
    # :tags: underwriting, premium
    risk_score: float = feature(default=0.0)

    # First support note line.
    # Second support note line.
    # :owner: support@chalk.ai
    # :tags: support
    support_note: str

    account_tier: str
"#,
        );

        assert_eq!(typed.feature_classes.len(), 1);
        let feature_class = &typed.feature_classes[0];

        assert_field_metadata(
            feature_class,
            &[
                ExpectedFieldMetadata {
                    field_name: "id",
                    comment: None,
                    description: None,
                    owner: None,
                    tags: &[],
                    kwarg_count: 0,
                },
                ExpectedFieldMetadata {
                    field_name: "display_name",
                    comment: Some("Display name shown in the UI.\n:tags: pii, profile"),
                    description: Some("Display name shown in the UI."),
                    owner: None,
                    tags: &["pii", "profile"],
                    kwarg_count: 0,
                },
                ExpectedFieldMetadata {
                    field_name: "location",
                    comment: Some(
                        "Latitude and longitude from the last mobile session.\n:owner: geo@chalk.ai",
                    ),
                    description: Some("Latitude and longitude from the last mobile session."),
                    owner: Some("geo@chalk.ai"),
                    tags: &[],
                    kwarg_count: 0,
                },
                ExpectedFieldMetadata {
                    field_name: "risk_score",
                    comment: Some(
                        "Risk score for fraud workflows.\n:tags: fraud\n:tags: underwriting, premium",
                    ),
                    description: Some("Risk score for fraud workflows."),
                    owner: None,
                    tags: &["fraud", "underwriting", "premium"],
                    kwarg_count: 1,
                },
                ExpectedFieldMetadata {
                    field_name: "support_note",
                    comment: Some(
                        "First support note line.\nSecond support note line.\n:owner: support@chalk.ai\n:tags: support",
                    ),
                    description: Some("First support note line.\nSecond support note line."),
                    owner: Some("support@chalk.ai"),
                    tags: &["support"],
                    kwarg_count: 0,
                },
                ExpectedFieldMetadata {
                    field_name: "account_tier",
                    comment: None,
                    description: None,
                    owner: None,
                    tags: &[],
                    kwarg_count: 0,
                },
            ],
        );
    }

    #[test]
    fn parses_indented_feature_classes_under_if_blocks() {
        let typed = parse_fixture(
            "/tmp/indented.py",
            r#"
from chalk.features import features
from chalk import feature

if True:
    @features(name="wrapped_customer")
    class Customer:
        # Wrapped customer score.
        # :owner: risk@chalk.ai
        # :tags: nested, premium
        score: int = feature(default=0)
"#,
        );

        assert_eq!(typed.feature_classes.len(), 1);
        let feature_class = &typed.feature_classes[0];

        assert_eq!(feature_class.class_name, "Customer");
        assert_eq!(feature_class.namespace, "wrapped_customer");
        assert_eq!(
            feature_class.source,
            "@features(name=\"wrapped_customer\")\nclass Customer:\n    # Wrapped customer score.\n    # :owner: risk@chalk.ai\n    # :tags: nested, premium\n    score: int = feature(default=0)\n"
        );
        assert_eq!(feature_class.class_name_location.range.start.line, 6);
        assert!(feature_class.kwargs.contains_key("name"));

        assert_field_metadata(
            feature_class,
            &[ExpectedFieldMetadata {
                field_name: "score",
                comment: Some(
                    "Wrapped customer score.\n:owner: risk@chalk.ai\n:tags: nested, premium",
                ),
                description: Some("Wrapped customer score."),
                owner: Some("risk@chalk.ai"),
                tags: &["nested", "premium"],
                kwarg_count: 1,
            }],
        );
    }

    #[test]
    fn stores_dedented_feature_class_source_with_all_decorators() {
        let typed = parse_fixture(
            "/tmp/decorated_source.py",
            r#"
from chalk.features import features
from chalk import feature

def passthrough(cls):
    return cls

if True:
    @passthrough
    @features(name="wrapped_customer")
    class Customer:
        score: int = feature(default=0)  # keep the inline comment
"#,
        );

        let feature_class = &typed.feature_classes[0];
        assert_eq!(
            feature_class.source,
            "@passthrough\n@features(name=\"wrapped_customer\")\nclass Customer:\n    score: int = feature(default=0)  # keep the inline comment\n"
        );
    }

    #[test]
    fn parses_nested_feature_classes_and_resolvers_in_function_and_class_bodies() {
        let typed = parse_fixture(
            "/tmp/nested_bodies.py",
            r#"
from chalk.features import features
from chalk import feature, online

def outer():
    @features(name="nested_user")
    class User:
        # Nested user score.
        score: int = feature(default=0)

class Namespace:
    @online(mode="batch")
    def compute_nested_user(message: str):
        return message
"#,
        );

        assert_eq!(typed.feature_classes.len(), 1);
        assert_eq!(typed.resolvers.len(), 1);

        let feature_class = &typed.feature_classes[0];
        assert_eq!(feature_class.class_name, "User");
        assert_eq!(feature_class.namespace, "nested_user");
        assert_eq!(feature_class.class_name_location.range.start.line, 6);

        assert_field_metadata(
            feature_class,
            &[ExpectedFieldMetadata {
                field_name: "score",
                comment: Some("Nested user score."),
                description: Some("Nested user score."),
                owner: None,
                tags: &[],
                kwarg_count: 1,
            }],
        );

        let resolver = &typed.resolvers[0];
        assert_eq!(resolver.resolver_name, "compute_nested_user");
        assert_eq!(resolver.resolver_name_location.range.start.line, 12);
        assert!(resolver.kwargs.contains_key("mode"));
    }
}
