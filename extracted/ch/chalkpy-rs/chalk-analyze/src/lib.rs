use std::collections::{HashMap, HashSet};
use std::fmt::Write as _;
use std::path::{Path, PathBuf};
use std::sync::Mutex;

mod bounded_system;

use anyhow::{Context, Result};
use bounded_system::BoundedSystem;
use log::{debug, trace, warn};
use ruff_db::diagnostic::{Diagnostic, DiagnosticId};
use ruff_db::files::File;
use ruff_db::parsed::parsed_module;
use ruff_db::source::{line_index, source_text};
use ruff_db::system::{OsSystem, SystemPath, SystemPathBuf};
use ruff_python_ast::visitor::{self, Visitor};
use ruff_python_ast::{self as ast, ArgOrKeyword};
use ruff_text_size::{Ranged, TextRange};
use ty_module_resolver::file_to_module;
use ty_project::{Db as _, ProgressReporter, ProjectDatabase, ProjectMetadata};
use ty_python_core::definition::Definition;
use ty_python_core::scope::{FileScopeId, ScopeKind};
use ty_python_core::semantic_index;
use ty_python_semantic::types::ide_support::{definitions_for_name, ImportAliasResolution};
use ty_python_semantic::types::{KnownClass, Type, UnionType};
use ty_python_semantic::{HasType, SemanticModel};

#[derive(Clone, Debug)]
pub struct AnalyzeOptions {
    pub project: PathBuf,
    pub paths: Vec<PathBuf>,
}

#[derive(Clone, Debug)]
pub enum AnalysisFact {
    Callsite(CallsiteFact),
    Definition(DefinitionFact),
}

#[derive(Clone, Debug)]
pub struct Position {
    pub line: u32,
    pub character: u32,
}

#[derive(Clone, Debug)]
pub struct Range {
    pub start: Position,
    pub end: Position,
}

#[derive(Clone, Debug)]
pub struct CallsiteFact {
    pub path: PathBuf,
    pub range: Range,
    pub enclosing_function: Option<String>,
    pub qualified_name: Option<String>,
    pub call_kind: CallKind,
    pub call_name: String,
    pub arguments: Vec<ArgumentFact>,
    pub is_user_local: bool,
    pub in_resolver_closure: bool,
}

#[derive(Clone, Copy, Debug, Hash, PartialEq, Eq)]
pub enum CallKind {
    Method,
    Builtin,
    Attribute,
}

#[derive(Clone, Debug)]
pub struct ArgumentFact {
    pub name: Option<String>,
    pub ty: String,
}

#[derive(Clone, Debug)]
pub struct DefinitionFact {
    pub path: PathBuf,
    pub module: Option<String>,
    pub definition_kind: DefinitionKind,
    pub name: String,
    pub qualified_name: String,
    pub decorators: Vec<String>,
    pub is_resolver_root: bool,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum DefinitionKind {
    Function,
    Class,
}

struct AnalyzeReporter {
    project_root: SystemPathBuf,
    facts: Mutex<Vec<AnalysisFact>>,
    errors: Mutex<Vec<String>>,
}

impl AnalyzeReporter {
    fn new(project_root: SystemPathBuf) -> Self {
        Self {
            project_root,
            facts: Mutex::new(Vec::new()),
            errors: Mutex::new(Vec::new()),
        }
    }

    fn into_facts(self) -> Result<Vec<AnalysisFact>> {
        let errors = self.errors.into_inner().expect("fact error lock poisoned");
        if !errors.is_empty() {
            anyhow::bail!("{}", errors.join("\n"));
        }

        let mut facts = self
            .facts
            .into_inner()
            .expect("analysis facts lock poisoned");
        debug!("chalk-analyze: finalizing {} raw facts", facts.len());
        finalize_facts(&mut facts);
        let definitions = facts
            .iter()
            .filter(|fact| matches!(fact, AnalysisFact::Definition(_)))
            .count();
        let callsites = facts.len().saturating_sub(definitions);
        debug!(
            "chalk-analyze: finalized facts definitions={} callsites={}",
            definitions, callsites
        );
        facts.sort_by_key(fact_sort_key);
        Ok(facts)
    }

    fn is_first_party_file(&self, db: &ProjectDatabase, file: File) -> bool {
        file.path(db)
            .as_system_path()
            .is_some_and(|path| path.starts_with(self.project_root.as_path()))
    }
}

impl ProgressReporter for AnalyzeReporter {
    fn set_files(&mut self, _files: usize) {}

    fn report_checked_file(&self, db: &ProjectDatabase, file: File, diagnostics: &[Diagnostic]) {
        let path = file_path(db, file);
        let blocking_diagnostics = diagnostics
            .iter()
            .filter(|diagnostic| diagnostic_blocks_analysis(diagnostic))
            .map(|diagnostic| format_ty_diagnostic(Some(path.as_path()), diagnostic))
            .collect::<Vec<_>>();
        if !blocking_diagnostics.is_empty() {
            debug!(
                "chalk-analyze: ty reported blocking diagnostics file={} count={}",
                path.display(),
                blocking_diagnostics.len()
            );
            for diagnostic in blocking_diagnostics {
                warn!("chalk-analyze: skipping file after ty diagnostic: {diagnostic}");
            }
            return;
        }

        if !self.is_first_party_file(db, file) {
            return;
        }

        debug!(
            "chalk-analyze: extracting facts from checked file {}",
            path.display()
        );
        match file_facts(db, file) {
            Err(err) => {
                self.errors
                    .lock()
                    .expect("fact error lock poisoned")
                    .push(format!("{}: {err:#}", path.display()));
            }
            Ok(mut facts) => {
                let definitions = facts
                    .iter()
                    .filter(|fact| matches!(fact, AnalysisFact::Definition(_)))
                    .count();
                let callsites = facts.len().saturating_sub(definitions);
                debug!(
                    "chalk-analyze: extracted facts file={} definitions={} callsites={}",
                    path.display(),
                    definitions,
                    callsites
                );
                self.facts
                    .lock()
                    .expect("analysis facts lock poisoned")
                    .append(&mut facts);
            }
        }
    }

    fn report_diagnostics(&mut self, _db: &ProjectDatabase, diagnostics: Vec<Diagnostic>) {
        self.errors
            .lock()
            .expect("fact error lock poisoned")
            .extend(
                diagnostics
                    .iter()
                    .filter(|diagnostic| diagnostic_blocks_analysis(diagnostic))
                    .map(|diagnostic| format_ty_diagnostic(None, diagnostic)),
            );
    }
}

fn diagnostic_blocks_analysis(diagnostic: &Diagnostic) -> bool {
    diagnostic.id() == DiagnosticId::Panic || diagnostic.severity().is_fatal()
}

fn format_ty_diagnostic(path: Option<&Path>, diagnostic: &Diagnostic) -> String {
    let mut message = String::new();
    if let Some(path) = path {
        let _ = write!(&mut message, "{}: ", path.display());
    }
    let _ = write!(
        &mut message,
        "ty {} diagnostic [{}]: {}",
        format!("{:?}", diagnostic.severity()).to_lowercase(),
        diagnostic.id(),
        diagnostic.concise_message()
    );
    for sub in diagnostic.sub_diagnostics() {
        let sub_message = sub.concise_message().to_string();
        if sub_message.is_empty() {
            continue;
        }
        let _ = write!(&mut message, "\n  {}: {}", sub.severity(), sub_message);
    }
    message
}

pub fn analyze(options: AnalyzeOptions) -> Result<Vec<AnalysisFact>> {
    let cwd = system_path_from_std(std::env::current_dir().context("failed to read cwd")?)?;
    let project_path = SystemPath::absolute(
        system_path_from_std(options.project)?.as_path(),
        cwd.as_path(),
    );
    debug!(
        "chalk-analyze: starting analysis cwd={} project={} requested_paths={:?}",
        cwd, project_path, options.paths
    );

    let system = BoundedSystem::new(OsSystem::new(cwd.as_path()));
    debug!(
        "chalk-analyze: discovering ty project from {}",
        project_path
    );
    let mut metadata = ProjectMetadata::discover(project_path.as_path(), &system)
        .context("failed to discover ty project")?;
    debug!("chalk-analyze: applying ty configuration files");
    metadata
        .apply_configuration_files(&system)
        .context("failed to apply ty configuration files")?;

    debug!("chalk-analyze: initializing ty database");
    let mut db =
        ProjectDatabase::fallible(metadata, system).context("failed to initialize ty database")?;
    let project = db.project();
    let project_root = project.root(&db).to_path_buf();
    let included_paths = if options.paths.is_empty() {
        vec![project_root.clone()]
    } else {
        options
            .paths
            .into_iter()
            .map(|path| {
                let path = system_path_from_std(path)?;
                Ok(SystemPath::absolute(path.as_path(), cwd.as_path()))
            })
            .collect::<Result<Vec<_>>>()?
    };
    debug!(
        "chalk-analyze: ty project root={} included_paths={:?}",
        project_root, included_paths
    );
    project.set_included_paths(&mut db, included_paths);

    let mut reporter = AnalyzeReporter::new(project_root);
    debug!("chalk-analyze: starting ty check_with_reporter");
    db.check_with_reporter(&mut reporter);
    debug!("chalk-analyze: finished ty check_with_reporter");
    reporter.into_facts()
}

fn system_path_from_std(path: PathBuf) -> Result<SystemPathBuf> {
    SystemPathBuf::from_path_buf(path)
        .map_err(|path| anyhow::anyhow!("path is not valid UTF-8: {}", path.to_string_lossy()))
}

fn file_facts(db: &ProjectDatabase, file: File) -> Result<Vec<AnalysisFact>> {
    let path = file_path(db, file);
    let parsed = parsed_module(db, file).load(db);
    let model = SemanticModel::new(db, file);
    let mut visitor = FactVisitor {
        db,
        file,
        model: &model,
        path,
        facts: Vec::new(),
        result: Ok(()),
        function_stack: Vec::new(),
        callsites_seen: 0,
        top_level_calls_skipped: 0,
    };
    visitor::walk_body(&mut visitor, parsed.suite());
    if visitor.top_level_calls_skipped > 0 {
        debug!(
            "chalk-analyze: skipped top-level callsites file={} count={}",
            visitor.path.display(),
            visitor.top_level_calls_skipped
        );
    }
    visitor.result?;
    Ok(visitor.facts)
}

struct FactVisitor<'a, 'db> {
    db: &'db ProjectDatabase,
    file: File,
    model: &'a SemanticModel<'db>,
    path: PathBuf,
    facts: Vec<AnalysisFact>,
    result: Result<()>,
    function_stack: Vec<String>,
    callsites_seen: usize,
    top_level_calls_skipped: usize,
}

impl<'a, 'db> FactVisitor<'a, 'db> {
    fn emit_callsite(&mut self, call: &ast::ExprCall) {
        if self.result.is_err() {
            return;
        }
        if self.function_stack.is_empty() {
            self.top_level_calls_skipped += 1;
            return;
        }
        self.callsites_seen += 1;
        let display =
            dotted_expr_name(call.func.as_ref()).unwrap_or_else(|| "<unknown>".to_string());
        if self.callsites_seen == 1 || self.callsites_seen % 100 == 0 {
            let range = self.range(call.range());
            debug!(
                "chalk-analyze: callsite progress file={} callsite_index={} line={} character={} function={}",
                self.path.display(),
                self.callsites_seen,
                range.start.line,
                range.start.character,
                display
            );
        }
        trace!(
            "chalk-analyze: callsite file={} callsite_index={} function={}",
            self.path.display(),
            self.callsites_seen,
            display
        );
        match self.callsite_fact(call) {
            Ok(Some(fact)) => self.facts.push(AnalysisFact::Callsite(fact)),
            Ok(None) => {}
            Err(err) => self.result = Err(err),
        }
    }

    fn emit_definition(
        &mut self,
        definition_kind: DefinitionKind,
        name: String,
        qualified_name: String,
        decorators: &[ast::Decorator],
    ) {
        if self.result.is_err() {
            return;
        }
        let decorator_names = decorators
            .iter()
            .filter_map(|decorator| dotted_expr_name(&decorator.expression))
            .collect::<Vec<_>>();
        let is_resolver_root = definition_kind == DefinitionKind::Function
            && decorator_names
                .iter()
                .any(|decorator| is_resolver_decorator(decorator));

        self.facts.push(AnalysisFact::Definition(DefinitionFact {
            path: file_path(self.db, self.file),
            module: self.module_name(),
            definition_kind,
            name,
            qualified_name,
            decorators: decorator_names,
            is_resolver_root,
        }));
    }

    fn callsite_fact(&self, call: &ast::ExprCall) -> Result<Option<CallsiteFact>> {
        let callee_name = match call.func.as_ref() {
            ast::Expr::Name(name) => name.id.to_string(),
            ast::Expr::Attribute(attribute) => attribute.attr.to_string(),
            _ => return Ok(None),
        };
        let receiver_type = receiver_expr(call).and_then(|receiver| self.type_string(receiver));
        let qualified_name = self
            .expression_definition(call.func.as_ref())
            .and_then(|definition| qualified_definition_name(self.db, definition))
            .or_else(|| {
                let ast::Expr::Attribute(attribute) = call.func.as_ref() else {
                    return None;
                };
                let receiver_name = attribute
                    .value
                    .inferred_type(self.model)
                    .and_then(|ty| normalize_type(self.db, ty).definition(self.db))
                    .and_then(|definition| definition.definition().copied())
                    .and_then(|definition| qualified_definition_name(self.db, definition))
                    .or_else(|| {
                        let raw_receiver = receiver_type.as_deref()?.trim();
                        if raw_receiver.is_empty() || raw_receiver == "Unknown" {
                            return None;
                        }
                        Some(
                            raw_receiver
                                .strip_prefix("<module '")
                                .or_else(|| raw_receiver.strip_prefix("<class '"))
                                .and_then(|raw| raw.strip_suffix("'>"))
                                .unwrap_or(raw_receiver)
                                .to_string(),
                        )
                    })?;
                Some(format!("{receiver_name}::{}", attribute.attr))
            });
        let source_arguments = call
            .arguments
            .iter_source_order()
            .filter_map(|argument| self.argument_fact(argument))
            .collect::<Vec<_>>();
        let (call_kind, call_name, arguments) = call_kind_name_and_args(
            &callee_name,
            qualified_name.as_deref(),
            source_arguments,
            receiver_type,
        );

        Ok(Some(CallsiteFact {
            path: file_path(self.db, self.file),
            range: self.range(call.range()),
            enclosing_function: self.function_stack.last().cloned(),
            qualified_name,
            call_kind,
            call_name,
            arguments,
            is_user_local: false,
            in_resolver_closure: false,
        }))
    }

    fn argument_fact(&self, argument: ArgOrKeyword) -> Option<ArgumentFact> {
        let (name, value) = match argument {
            ArgOrKeyword::Arg(arg) => match arg {
                ast::Expr::Starred(starred) => (None, starred.value.as_ref()),
                _ => (None, arg),
            },
            ArgOrKeyword::Keyword(keyword) => {
                keyword.arg.as_ref()?;
                (
                    keyword.arg.as_ref().map(ToString::to_string),
                    &keyword.value,
                )
            }
        };

        Some(ArgumentFact {
            name,
            ty: self
                .type_string(value)
                .unwrap_or_else(|| "Unknown".to_string()),
        })
    }

    fn expression_definition(&self, expression: &ast::Expr) -> Option<Definition<'db>> {
        match expression {
            ast::Expr::Name(name) => {
                if is_python_builtin_name(name.id.as_str()) {
                    return None;
                }
                definitions_for_name(
                    self.model,
                    name.id.as_str(),
                    name.into(),
                    ImportAliasResolution::ResolveAliases,
                )
                .into_iter()
                .find_map(|definition| definition.definition())
            }
            _ => None,
        }
    }

    fn module_name(&self) -> Option<String> {
        file_to_module(self.db, self.file).map(|module| module.name(self.db).to_string())
    }

    fn range(&self, range: TextRange) -> Range {
        range_record(self.db, self.file, range)
    }

    fn type_string(&self, node: &impl HasType) -> Option<String> {
        node.inferred_type(self.model)
            .map(|ty| normalize_type(self.db, ty).display(self.db).to_string())
    }
}

fn normalize_type<'db>(db: &'db ProjectDatabase, ty: Type<'db>) -> Type<'db> {
    match ty {
        Type::Union(union) => UnionType::from_elements(
            db,
            union
                .elements(db)
                .iter()
                .copied()
                .map(|ty| normalize_type(db, ty)),
        ),
        // Normalize out ty's truthiness/non-null refinements
        Type::Intersection(intersection)
            if {
                let mut positive = intersection.iter_positive(db);
                let mut negative = intersection.iter_negative(db);
                matches!(
                    (
                        positive.next(),
                        positive.next(),
                        negative.next(),
                        negative.next(),
                    ),
                    (Some(_), None, Some(negative), None)
                        if negative == Type::AlwaysFalsy || negative.is_none(db)
                )
            } =>
        {
            normalize_type(db, intersection.iter_positive(db).next().unwrap_or(ty))
        }
        Type::LiteralValue(_) => {
            let literal_definition = ty.definition(db);
            [
                KnownClass::Bool,
                KnownClass::Int,
                KnownClass::Str,
                KnownClass::Bytes,
            ]
            .into_iter()
            .map(|class| class.to_instance(db))
            .find(|builtin_instance| {
                builtin_instance
                    .definition(db)
                    .is_some_and(|builtin_definition| {
                        literal_definition.as_ref() == Some(&builtin_definition)
                    })
                    && ty.is_assignable_to(db, *builtin_instance)
            })
            .unwrap_or(ty)
        }
        _ => ty,
    }
}

impl<'ast, 'a, 'db> Visitor<'ast> for FactVisitor<'a, 'db> {
    fn visit_stmt(&mut self, stmt: &'ast ast::Stmt) {
        match stmt {
            ast::Stmt::FunctionDef(function) => {
                let qualified_name = qualified_ast_function_name(self.db, self.file, function);
                self.emit_definition(
                    DefinitionKind::Function,
                    function.name.to_string(),
                    qualified_name.clone(),
                    &function.decorator_list,
                );
                if let Some(type_params) = &function.type_params {
                    self.visit_type_params(type_params);
                }
                self.visit_parameters(&function.parameters);
                if let Some(returns) = &function.returns {
                    self.visit_annotation(returns);
                }
                self.function_stack.push(qualified_name);
                self.visit_body(&function.body);
                self.function_stack.pop();
            }
            ast::Stmt::ClassDef(class) => {
                let qualified_name = qualified_ast_class_name(self.db, self.file, class);
                self.emit_definition(
                    DefinitionKind::Class,
                    class.name.to_string(),
                    qualified_name,
                    &class.decorator_list,
                );
                if let Some(type_params) = &class.type_params {
                    self.visit_type_params(type_params);
                }
                if let Some(arguments) = &class.arguments {
                    self.visit_arguments(arguments);
                }
                self.visit_body(&class.body);
            }
            _ => visitor::walk_stmt(self, stmt),
        }
    }

    fn visit_annotation(&mut self, _expr: &'ast ast::Expr) {}

    fn visit_expr(&mut self, expr: &'ast ast::Expr) {
        if let ast::Expr::Call(call) = expr {
            self.emit_callsite(call);
        }
        visitor::walk_expr(self, expr);
    }
}

fn finalize_facts(facts: &mut [AnalysisFact]) {
    let mut function_names = HashSet::new();
    let mut first_party_call_targets = HashSet::new();
    let mut resolver_roots = HashSet::new();
    let mut contexts: HashMap<String, SourceContext> = HashMap::new();

    for fact in facts.iter() {
        let AnalysisFact::Definition(definition) = fact else {
            continue;
        };
        let path = definition.path.to_string_lossy().to_string();
        let context = contexts.entry(path).or_default();
        context.local_names.insert(definition.name.clone());
        if let Some(module) = &definition.module {
            context.local_modules.insert(module.clone());
        }
        first_party_call_targets.insert(definition.qualified_name.clone());
        if definition.definition_kind == DefinitionKind::Function {
            function_names.insert(definition.qualified_name.clone());
            if definition.is_resolver_root {
                resolver_roots.insert(definition.qualified_name.clone());
            }
        }
    }

    let closure = resolver_closure(facts, &function_names, resolver_roots);
    let mut first_party_callees = 0usize;
    let mut user_local_calls = 0usize;
    let mut resolver_closure_calls = 0usize;
    for fact in facts.iter_mut() {
        let AnalysisFact::Callsite(call) = fact else {
            continue;
        };

        let path = call.path.to_string_lossy().to_string();
        let fallback_context = SourceContext::default();
        let context = contexts.get(&path).unwrap_or(&fallback_context);
        let is_first_party_callee = call
            .qualified_name
            .as_ref()
            .is_some_and(|callee| first_party_call_targets.contains(callee));
        call.is_user_local = is_user_local_call(call, context) || is_first_party_callee;
        call.in_resolver_closure = call
            .enclosing_function
            .as_ref()
            .is_some_and(|caller| closure.contains(caller));
        first_party_callees += usize::from(is_first_party_callee);
        user_local_calls += usize::from(call.is_user_local);
        resolver_closure_calls += usize::from(call.in_resolver_closure);
    }
    debug!(
        "chalk-analyze: resolver summary functions={} \
         resolver_closure_functions={} first_party_callsite_targets={} \
         user_local_calls={} calls_in_resolver_closure={}",
        function_names.len(),
        closure.len(),
        first_party_callees,
        user_local_calls,
        resolver_closure_calls
    );
}

fn resolver_closure(
    facts: &[AnalysisFact],
    function_names: &HashSet<String>,
    mut reachable: HashSet<String>,
) -> HashSet<String> {
    let mut graph: HashMap<String, HashSet<String>> = HashMap::new();
    for fact in facts {
        let AnalysisFact::Callsite(call) = fact else {
            continue;
        };
        let Some(caller) = &call.enclosing_function else {
            continue;
        };
        let Some(callee) = call
            .qualified_name
            .as_ref()
            .filter(|callee| function_names.contains(*callee))
            .cloned()
        else {
            continue;
        };
        graph.entry(caller.clone()).or_default().insert(callee);
    }

    let mut stack = reachable.iter().cloned().collect::<Vec<_>>();
    while let Some(function) = stack.pop() {
        let Some(callees) = graph.get(&function) else {
            continue;
        };
        for callee in callees {
            if reachable.insert(callee.clone()) {
                stack.push(callee.clone());
            }
        }
    }

    reachable
}

fn is_user_local_call(call: &CallsiteFact, context: &SourceContext) -> bool {
    let Some(function_name) = call.qualified_name.as_deref() else {
        return false;
    };
    let bare_name = last_call_path_segment(function_name);
    context.local_names.contains(bare_name)
        || bare_name.starts_with('_')
        || context.local_modules.iter().any(|module| {
            function_name.strip_prefix(module).is_some_and(|suffix| {
                suffix.is_empty() || suffix.starts_with('.') || suffix.starts_with("::")
            })
        })
}

#[derive(Clone, Debug, Default)]
struct SourceContext {
    local_names: HashSet<String>,
    local_modules: HashSet<String>,
}

fn fact_sort_key(fact: &AnalysisFact) -> (String, u32, u32, u8, String) {
    match fact {
        AnalysisFact::Callsite(call) => (
            call.path.to_string_lossy().to_string(),
            call.range.start.line,
            call.range.start.character,
            1,
            call.qualified_name.clone().unwrap_or_default(),
        ),
        AnalysisFact::Definition(definition) => (
            definition.path.to_string_lossy().to_string(),
            0,
            0,
            0,
            definition.qualified_name.clone(),
        ),
    }
}

fn qualified_definition_name<'db>(
    db: &'db ProjectDatabase,
    definition: Definition<'db>,
) -> Option<String> {
    let name = definition.name(db)?;
    let mut components =
        qualified_scope_components(db, definition.file(db), definition.file_scope(db));
    components.push(name);
    Some(components.join("::"))
}

fn receiver_expr(call: &ast::ExprCall) -> Option<&ast::Expr> {
    match call.func.as_ref() {
        ast::Expr::Attribute(attribute) => Some(attribute.value.as_ref()),
        _ => None,
    }
}

fn call_kind_name_and_args(
    callee_name: &str,
    qualified_name: Option<&str>,
    source_args: Vec<ArgumentFact>,
    receiver_type: Option<String>,
) -> (CallKind, String, Vec<ArgumentFact>) {
    let has_explicit_receiver = receiver_type.is_some();
    let call_path = qualified_name.unwrap_or(callee_name);
    let call_path_parts = call_path.split("::").collect::<Vec<_>>();
    let function_name = last_call_path_segment(call_path).to_string();

    let (call_kind, call_name, synthetic_module) = if has_explicit_receiver {
        (CallKind::Method, function_name, None)
    } else if call_path_parts.len() == 2 && call_path_parts[0] == "builtins" {
        (CallKind::Builtin, call_path_parts[1].to_string(), None)
    } else if call_path_parts.len() > 1 {
        let module_name = call_path_parts[..call_path_parts.len() - 1].join(".");
        (
            CallKind::Method,
            call_path_parts[call_path_parts.len() - 1].to_string(),
            Some(module_name),
        )
    } else {
        (CallKind::Builtin, callee_name.to_string(), None)
    };

    let mut args = Vec::new();
    if let Some(receiver_type) = receiver_type {
        args.push(ArgumentFact {
            name: None,
            ty: receiver_type,
        });
    } else if let Some(module_name) = &synthetic_module {
        args.push(ArgumentFact {
            name: None,
            ty: format!("<module '{module_name}'>"),
        });
    }

    let explicit_class_module =
        (has_explicit_receiver && call_path_parts.len() > 1 && call_path_parts[0] != "builtins")
            .then(|| call_path_parts[..call_path_parts.len() - 1].join("."));
    args.extend(source_args.into_iter().enumerate().map(|(index, mut arg)| {
        if index == 0 && arg.ty.trim().starts_with("<class '") {
            if let Some(module_name) = &explicit_class_module {
                arg.ty = format!("<module '{module_name}'>");
            }
        }
        arg
    }));

    (call_kind, call_name, args)
}

fn file_path(db: &ProjectDatabase, file: File) -> PathBuf {
    file.path(db)
        .as_system_path()
        .map(|path| path.as_std_path().to_path_buf())
        .unwrap_or_else(|| PathBuf::from(file.path(db).to_string()))
}

fn range_record(db: &ProjectDatabase, file: File, range: TextRange) -> Range {
    let source = source_text(db, file);
    let line_index = line_index(db, file);
    let start = line_index.line_column(range.start(), source.as_str());
    let end = line_index.line_column(range.end(), source.as_str());
    Range {
        start: Position {
            line: start.line.to_zero_indexed() as u32,
            character: start.column.to_zero_indexed() as u32,
        },
        end: Position {
            line: end.line.to_zero_indexed() as u32,
            character: end.column.to_zero_indexed() as u32,
        },
    }
}

fn dotted_expr_name(expression: &ast::Expr) -> Option<String> {
    match expression {
        ast::Expr::Call(call) => dotted_expr_name(call.func.as_ref()),
        ast::Expr::Name(name) => Some(name.id.to_string()),
        ast::Expr::Attribute(attribute) => {
            let prefix = dotted_expr_name(attribute.value.as_ref())?;
            Some(format!("{prefix}.{}", attribute.attr))
        }
        ast::Expr::Subscript(subscript) => dotted_expr_name(subscript.value.as_ref()),
        _ => None,
    }
}

fn is_python_builtin_name(name: &str) -> bool {
    matches!(
        name,
        "abs"
            | "aiter"
            | "all"
            | "anext"
            | "any"
            | "ascii"
            | "bin"
            | "bool"
            | "breakpoint"
            | "bytearray"
            | "bytes"
            | "callable"
            | "chr"
            | "classmethod"
            | "compile"
            | "complex"
            | "delattr"
            | "dict"
            | "dir"
            | "divmod"
            | "enumerate"
            | "eval"
            | "exec"
            | "filter"
            | "float"
            | "format"
            | "frozenset"
            | "getattr"
            | "globals"
            | "hasattr"
            | "hash"
            | "help"
            | "hex"
            | "id"
            | "input"
            | "int"
            | "isinstance"
            | "issubclass"
            | "iter"
            | "len"
            | "list"
            | "locals"
            | "map"
            | "max"
            | "memoryview"
            | "min"
            | "next"
            | "object"
            | "oct"
            | "open"
            | "ord"
            | "pow"
            | "print"
            | "property"
            | "range"
            | "repr"
            | "reversed"
            | "round"
            | "set"
            | "setattr"
            | "slice"
            | "sorted"
            | "staticmethod"
            | "str"
            | "sum"
            | "super"
            | "tuple"
            | "type"
            | "vars"
            | "zip"
            | "__import__"
    )
}

fn qualified_ast_function_name(
    db: &ProjectDatabase,
    file: File,
    function: &ast::StmtFunctionDef,
) -> String {
    let index = semantic_index(db, file);
    let mut components = index
        .try_definition(function)
        .map(|definition| qualified_scope_components(db, file, definition.file_scope(db)))
        .unwrap_or_else(|| module_component(db, file).into_iter().collect());
    components.push(function.name.to_string());
    components.join("::")
}

fn qualified_ast_class_name(db: &ProjectDatabase, file: File, class: &ast::StmtClassDef) -> String {
    let index = semantic_index(db, file);
    let mut components = index
        .try_definition(class)
        .map(|definition| qualified_scope_components(db, file, definition.file_scope(db)))
        .unwrap_or_else(|| module_component(db, file).into_iter().collect());
    components.push(class.name.to_string());
    components.join("::")
}

fn qualified_scope_components(
    db: &ProjectDatabase,
    file: File,
    file_scope: FileScopeId,
) -> Vec<String> {
    let parsed = parsed_module(db, file).load(db);
    let index = semantic_index(db, file);
    let mut components = Vec::new();
    if let Some(module) = module_component(db, file) {
        components.push(module);
    }
    let mut scopes = index
        .ancestor_scopes(file_scope)
        .filter_map(|(scope_id, scope)| match scope.kind() {
            ScopeKind::Class | ScopeKind::Function => {
                Some(scope_id.to_scope_id(db, file).name(db, &parsed).to_string())
            }
            _ => None,
        })
        .collect::<Vec<_>>();
    scopes.reverse();
    components.extend(scopes);
    components
}

fn module_component(db: &ProjectDatabase, file: File) -> Option<String> {
    file_to_module(db, file).map(|module| module.name(db).to_string())
}

fn is_resolver_decorator(decorator: &str) -> bool {
    matches!(
        decorator,
        "chalk.features.resolver::online"
            | "chalk.features.resolver.online"
            | "chalk.features.resolver::offline"
            | "chalk.features.resolver.offline"
            | "chalk.features.resolver::resolver"
            | "chalk.features.resolver.resolver"
            | "chalk.features::online"
            | "chalk.features.online"
            | "chalk.features::offline"
            | "chalk.features.offline"
            | "chalk.features::resolver"
            | "chalk.features.resolver"
            | "chalk::online"
            | "chalk.online"
            | "chalk::offline"
            | "chalk.offline"
            | "chalk::resolver"
            | "chalk.resolver"
            | "chalk::batch"
            | "chalk.batch"
            | "chalk::realtime"
            | "chalk.realtime"
    ) || matches!(
        last_call_path_segment(decorator),
        "online" | "offline" | "resolver" | "batch" | "realtime"
    )
}

fn last_call_path_segment(raw: &str) -> &str {
    raw.rsplit("::")
        .next()
        .unwrap_or(raw)
        .rsplit('.')
        .next()
        .unwrap_or(raw)
        .trim()
}
