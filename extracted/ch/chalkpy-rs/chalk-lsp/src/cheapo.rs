use std::{
    collections::{HashMap, HashSet},
    error::Error,
    path::{Path, PathBuf},
    sync::OnceLock,
};

use chalk_analyze::{analyze, AnalysisFact, AnalyzeOptions, CallKind, CallsiteFact};
use chalk_lsp::project::{path_to_file_uri, ExternalFileDiagnostics, PathScope};
use log::debug;
use lsp_types::{Diagnostic, DiagnosticSeverity, NumberOrString, Position, Range};

mod cheapo_supported_funcs {
    include!(concat!(env!("OUT_DIR"), "/cheapo_supported_funcs.rs"));
}

static SUPPORTED_FUNCS: OnceLock<SupportedFuncs> = OnceLock::new();

fn supported_funcs() -> &'static SupportedFuncs {
    let supported = SUPPORTED_FUNCS.get_or_init(cheapo_supported_funcs::supported_funcs);
    debug!(
        "accel: loaded supported function table calls={}",
        supported.impls.len()
    );
    supported
}

pub fn diagnostics_for_project(
    project_root: &Path,
    requested_paths: &[PathBuf],
) -> Result<Vec<ExternalFileDiagnostics>, Box<dyn Error + Sync + Send>> {
    debug!(
        "accel: starting diagnostics project_root={} requested_paths={:?}",
        project_root.display(),
        requested_paths
    );
    let diagnostics = findings_to_file_diagnostics(collect_findings_for_project(
        project_root,
        requested_paths,
        supported_funcs(),
    )?)?;
    let diagnostic_count = diagnostics
        .iter()
        .map(|file| file.diagnostics.len())
        .sum::<usize>();
    debug!(
        "accel: finished diagnostics files={} diagnostics={}",
        diagnostics.len(),
        diagnostic_count
    );
    Ok(diagnostics)
}

fn collect_findings_for_project(
    project_root: &Path,
    requested_paths: &[PathBuf],
    supported: &SupportedFuncs,
) -> Result<Vec<CheapoFinding>, Box<dyn Error + Sync + Send>> {
    debug!("accel: invoking chalk-analyze");
    let facts = analyze(AnalyzeOptions {
        project: project_root.to_path_buf(),
        paths: vec![project_root.to_path_buf()],
    })?;
    let fact_count = facts.len();
    let callsite_count = facts
        .iter()
        .filter(|fact| matches!(fact, AnalysisFact::Callsite(_)))
        .count();
    debug!(
        "accel: chalk-analyze returned facts={} callsites={} definitions={}",
        fact_count,
        callsite_count,
        fact_count.saturating_sub(callsite_count)
    );
    let requested_scopes = PathScope::from_paths(project_root, requested_paths);
    debug!(
        "accel: requested scope filter size={}",
        requested_scopes.len()
    );

    let mut findings = Vec::new();
    let mut emitted = HashSet::new();
    let mut skipped_not_callsite = 0usize;
    let mut skipped_outside_resolver_closure = 0usize;
    let mut skipped_outside_scope = 0usize;
    let mut skipped_supported = 0usize;
    let mut skipped_duplicate = 0usize;
    for fact in facts {
        let AnalysisFact::Callsite(call) = fact else {
            skipped_not_callsite += 1;
            continue;
        };
        if !call.in_resolver_closure {
            skipped_outside_resolver_closure += 1;
            continue;
        }
        if !requested_scopes.is_empty()
            && !requested_scopes
                .iter()
                .any(|scope| scope.contains(project_root, &call.path))
        {
            skipped_outside_scope += 1;
            continue;
        }
        let path = call.path.to_string_lossy().to_string();
        let supported_signatures = unsupported_call_supported_signatures(&call, supported);
        if supported_signatures.is_none() {
            skipped_supported += 1;
            continue;
        }
        let display_name = call
            .qualified_name
            .as_deref()
            .unwrap_or(call.call_name.as_str());
        let display_arg_start = usize::from(call.call_kind == CallKind::Method);
        let signature_args = call.arguments.get(display_arg_start..).unwrap_or(&[]);
        let call_signature = format!(
            "{}({})",
            display_name,
            signature_args
                .iter()
                .map(|arg| match &arg.name {
                    Some(name) => format!("{name}={}", arg.ty),
                    None => arg.ty.clone(),
                })
                .collect::<Vec<_>>()
                .join(", ")
        );
        let finding = CheapoFinding {
            path,
            line: call.range.start.line,
            column: call.range.start.character,
            end_line: call.range.end.line,
            end_column: call.range.end.character,
            call_signature,
            supported_signatures: supported_signatures.unwrap_or_default(),
        };
        if emitted.insert(finding.output_line()) {
            findings.push(finding);
        } else {
            skipped_duplicate += 1;
        }
    }
    debug!(
        "accel: findings summary emitted={} skipped_not_callsite={} \
         skipped_outside_resolver_closure={} skipped_outside_scope={} \
         skipped_supported={} skipped_duplicate={}",
        findings.len(),
        skipped_not_callsite,
        skipped_outside_resolver_closure,
        skipped_outside_scope,
        skipped_supported,
        skipped_duplicate
    );

    Ok(findings)
}

#[derive(Clone, Debug)]
struct CheapoFinding {
    path: String,
    line: u32,
    column: u32,
    end_line: u32,
    end_column: u32,
    call_signature: String,
    supported_signatures: Vec<String>,
}

impl CheapoFinding {
    fn output_line(&self) -> String {
        format!(
            "{}:{}:{} {}",
            self.path, self.line, self.column, self.call_signature,
        )
    }

    fn message(&self) -> String {
        let mut message = format!("{} is not acceleratable", self.call_signature);
        if !self.supported_signatures.is_empty() {
            message.push_str("\nSupported signatures:");
            for signature in &self.supported_signatures {
                message.push_str("\n  ");
                message.push_str(signature);
            }
        }
        message
    }

    fn diagnostic(&self) -> Diagnostic {
        let start = Position {
            line: self.line,
            character: self.column,
        };
        let end = Position {
            line: self.end_line,
            character: self.end_column,
        };
        Diagnostic {
            range: Range { start, end },
            severity: Some(DiagnosticSeverity::WARNING),
            code: Some(NumberOrString::String("unsupported-function".to_string())),
            source: Some("accel".to_string()),
            message: self.message(),
            ..Default::default()
        }
    }
}

fn findings_to_file_diagnostics(
    findings: Vec<CheapoFinding>,
) -> Result<Vec<ExternalFileDiagnostics>, Box<dyn Error + Sync + Send>> {
    let mut by_uri_key: HashMap<String, ExternalFileDiagnostics> = HashMap::new();
    for finding in findings {
        let Some(uri) = path_to_file_uri(Path::new(&finding.path)) else {
            continue;
        };
        let uri_key = uri.as_str().to_string();
        let diagnostic = finding.diagnostic();
        by_uri_key
            .entry(uri_key.clone())
            .or_insert_with(|| ExternalFileDiagnostics {
                uri,
                uri_key,
                diagnostics: Vec::new(),
            })
            .diagnostics
            .push(diagnostic);
    }

    let mut files = by_uri_key.into_values().collect::<Vec<_>>();
    files.sort_by(|left, right| left.uri_key.cmp(&right.uri_key));
    Ok(files)
}

#[derive(Clone, Debug, Hash, PartialEq, Eq)]
struct SupportedCall {
    kind: CallKind,
    name: String,
}

#[derive(Clone, Debug)]
struct SupportedFuncs {
    impls: HashMap<SupportedCall, Vec<SupportedSignature>>,
}

impl SupportedFuncs {
    fn signatures(&self, call: &SupportedCall) -> Option<&[SupportedSignature]> {
        self.impls.get(call).map(Vec::as_slice)
    }
}

#[derive(Clone, Debug)]
struct SupportedSignature {
    args: Vec<SupportedArg>,
}

#[derive(Clone, Debug)]
struct SupportedArg {
    ty: SupportedTy,
    argument_name: Option<String>,
    has_default: bool,
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum SupportedTy {
    Any {
        nullable: bool,
    },
    Bool {
        nullable: bool,
    },
    Bytes {
        nullable: bool,
    },
    Class {
        nullable: bool,
        module: String,
        name: String,
    },
    Counter {
        nullable: bool,
        items: Box<SupportedTy>,
    },
    Date {
        nullable: bool,
    },
    DateTime {
        nullable: bool,
    },
    Dict {
        nullable: bool,
        key_type: Box<SupportedTy>,
        value_type: Box<SupportedTy>,
    },
    Float {
        nullable: bool,
    },
    FrozenSet {
        nullable: bool,
        items: Box<SupportedTy>,
    },
    Generator {
        nullable: bool,
        items: Box<SupportedTy>,
    },
    HashlibHash {
        nullable: bool,
    },
    Int {
        nullable: bool,
    },
    Iterable {
        nullable: bool,
        items: Box<SupportedTy>,
    },
    Json {
        nullable: bool,
    },
    List {
        nullable: bool,
        items: Box<SupportedTy>,
    },
    Module {
        nullable: bool,
        name: String,
    },
    None {
        nullable: bool,
    },
    ReMatch {
        nullable: bool,
    },
    RePattern {
        nullable: bool,
    },
    RequestsHttpResponse {
        nullable: bool,
    },
    Set {
        nullable: bool,
        items: Box<SupportedTy>,
    },
    SequenceMatcher {
        nullable: bool,
    },
    Str {
        nullable: bool,
    },
    SubClassOf {
        ty_name: String,
        match_nullable: bool,
    },
    Time {
        nullable: bool,
    },
    Timedelta {
        nullable: bool,
    },
    TimeZone {
        nullable: bool,
    },
    Tuple {
        nullable: bool,
        items: Vec<SupportedTy>,
        is_variable: bool,
    },
    Other {
        nullable: bool,
        name: String,
    },
}

impl SupportedTy {
    fn display(&self) -> String {
        let (display, nullable) = match self {
            Self::Any { nullable } => ("Any".to_string(), *nullable),
            Self::Bool { nullable } => ("bool".to_string(), *nullable),
            Self::Bytes { nullable } => ("bytes".to_string(), *nullable),
            Self::Class {
                nullable,
                module,
                name,
            } => (format!("class[{module}.{name}]"), *nullable),
            Self::Counter { nullable, items } => {
                (format!("Counter[{}]", items.display()), *nullable)
            }
            Self::Date { nullable } => ("date".to_string(), *nullable),
            Self::DateTime { nullable } => ("datetime".to_string(), *nullable),
            Self::Dict {
                nullable,
                key_type,
                value_type,
                ..
            } => (
                format!("dict[{}, {}]", key_type.display(), value_type.display()),
                *nullable,
            ),
            Self::Float { nullable } => ("float".to_string(), *nullable),
            Self::FrozenSet { nullable, items } => {
                (format!("frozenset[{}]", items.display()), *nullable)
            }
            Self::Generator { nullable, items } => {
                (format!("Generator[{}]", items.display()), *nullable)
            }
            Self::HashlibHash { nullable } => ("hashlib.Hash".to_string(), *nullable),
            Self::Int { nullable } => ("int".to_string(), *nullable),
            Self::Iterable { nullable, items } => {
                (format!("Iterable[{}]", items.display()), *nullable)
            }
            Self::Json { nullable } => ("json".to_string(), *nullable),
            Self::List { nullable, items } => (format!("list[{}]", items.display()), *nullable),
            Self::Module { nullable, name } => (format!("module[{name}]"), *nullable),
            Self::None { nullable } => ("None".to_string(), *nullable),
            Self::ReMatch { nullable } => ("Match".to_string(), *nullable),
            Self::RePattern { nullable } => ("Pattern".to_string(), *nullable),
            Self::RequestsHttpResponse { nullable } => {
                ("RequestsHttpResponse".to_string(), *nullable)
            }
            Self::Set { nullable, items } => (format!("set[{}]", items.display()), *nullable),
            Self::SequenceMatcher { nullable } => ("SequenceMatcher".to_string(), *nullable),
            Self::Str { nullable } => ("str".to_string(), *nullable),
            Self::SubClassOf {
                ty_name,
                match_nullable,
            } => (format!("subclass[{ty_name}]"), *match_nullable),
            Self::Time { nullable } => ("time".to_string(), *nullable),
            Self::Timedelta { nullable } => ("timedelta".to_string(), *nullable),
            Self::TimeZone { nullable } => ("timezone".to_string(), *nullable),
            Self::Tuple {
                nullable,
                items,
                is_variable,
                ..
            } => {
                if *is_variable {
                    let item = items
                        .first()
                        .map(SupportedTy::display)
                        .unwrap_or_else(|| "Any".to_string());
                    (format!("tuple[{item}, ...]"), *nullable)
                } else {
                    (
                        format!(
                            "tuple[{}]",
                            items
                                .iter()
                                .map(SupportedTy::display)
                                .collect::<Vec<_>>()
                                .join(", ")
                        ),
                        *nullable,
                    )
                }
            }
            Self::Other { nullable, name } => (name.clone(), *nullable),
        };

        if nullable {
            format!("option<{display}>")
        } else {
            display
        }
    }
}

#[derive(Clone, Debug)]
struct ObservedArg {
    argument_name: Option<String>,
    ty: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum ObservedTy {
    Bool,
    Bytes,
    Class(String),
    Counter(Box<ObservedTy>),
    Date,
    DateTime,
    Dict(Box<ObservedTy>, Box<ObservedTy>),
    Enum,
    Float,
    FrozenSet(Box<ObservedTy>),
    Function,
    Generator(Box<ObservedTy>),
    HashlibHash,
    Int,
    Iterable(Box<ObservedTy>),
    List(Box<ObservedTy>),
    LogicalStruct,
    Module(String),
    None,
    ReMatch,
    RePattern,
    RequestsHttpResponse,
    Set(Box<ObservedTy>),
    SequenceMatcher,
    Str,
    Time,
    Timedelta,
    TimeZone,
    Tuple(Vec<ObservedTy>, bool),
    Unknown,
    Other(String),
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum MatchResult {
    Match,
    NoMatch,
    Inconclusive,
}

impl MatchResult {
    fn combine(self, other: Self) -> Self {
        match (self, other) {
            (Self::NoMatch, _) | (_, Self::NoMatch) => Self::NoMatch,
            (Self::Inconclusive, _) | (_, Self::Inconclusive) => Self::Inconclusive,
            (Self::Match, Self::Match) => Self::Match,
        }
    }
}

fn unsupported_call_supported_signatures(
    call: &CallsiteFact,
    supported: &SupportedFuncs,
) -> Option<Vec<String>> {
    let supported_call = SupportedCall {
        kind: call.call_kind,
        name: call.call_name.clone(),
    };

    let args = call
        .arguments
        .iter()
        .map(|argument| ObservedArg {
            argument_name: argument.name.clone(),
            ty: argument.ty.clone(),
        })
        .collect::<Vec<_>>();

    if is_implicitly_acceleratable(call, &args) {
        return None;
    }

    if call.is_user_local {
        return None;
    }

    if call.call_kind == CallKind::Builtin && args.len() == 1 && args[0].argument_name.is_none() {
        let dunder_method = match call.call_name.as_str() {
            "bool" => Some("__bool__"),
            "len" => Some("__len__"),
            _ => None,
        };

        if let Some(dunder_method) = dunder_method {
            let dunder_call = SupportedCall {
                kind: CallKind::Method,
                name: dunder_method.to_string(),
            };

            let Some(signatures) = supported.signatures(&dunder_call) else {
                return Some(Vec::new());
            };
            let receiver_signatures =
                receiver_compatible_signatures(&dunder_call, &args, signatures);
            if receiver_signatures.is_empty() {
                return Some(supported_signature_displays(call, signatures));
            }

            return match signature_match(&args, &receiver_signatures) {
                MatchResult::Match | MatchResult::Inconclusive => None,
                MatchResult::NoMatch => {
                    Some(supported_signature_displays(call, &receiver_signatures))
                }
            };
        }
    }

    let Some(signatures) = supported.signatures(&supported_call) else {
        return should_report_call_mismatch(&supported_call, &args).then(Vec::new);
    };
    let signatures = receiver_compatible_signatures(&supported_call, &args, signatures);
    if signatures.is_empty() {
        return should_report_call_mismatch(&supported_call, &args).then(Vec::new);
    }

    match signature_match(&args, &signatures) {
        MatchResult::Match | MatchResult::Inconclusive => None,
        MatchResult::NoMatch => should_report_call_mismatch(&supported_call, &args)
            .then(|| supported_signature_displays(call, &signatures)),
    }
}

fn is_implicitly_acceleratable(call: &CallsiteFact, args: &[ObservedArg]) -> bool {
    if call.qualified_name.as_deref().is_some_and(|name| {
        matches!(
            name.split("::")
                .next()
                .and_then(|module| module.split('.').next()),
            Some("chalk" | "chalkdf")
        )
    }) {
        return true;
    }

    args.first().is_some_and(|arg| {
        let raw = arg.ty.trim();
        raw == "<module 'chalk'>"
            || raw.starts_with("<module 'chalk.")
            || raw == "<class 'chalk'>"
            || raw.starts_with("<class 'chalk.")
            || raw == "<module 'chalkdf'>"
            || raw.starts_with("<module 'chalkdf.")
            || raw == "<class 'chalkdf'>"
            || raw.starts_with("<class 'chalkdf.")
    })
}

fn should_report_call_mismatch(call: &SupportedCall, args: &[ObservedArg]) -> bool {
    if call.kind != CallKind::Method {
        return false;
    }
    args.first().is_some_and(|arg| {
        let raw = arg.ty.trim();
        raw.starts_with("<module '") || raw.starts_with("<class '")
    })
}

fn receiver_compatible_signatures(
    call: &SupportedCall,
    args: &[ObservedArg],
    signatures: &[SupportedSignature],
) -> Vec<SupportedSignature> {
    if call.kind != CallKind::Method && call.kind != CallKind::Attribute {
        return signatures.to_vec();
    }
    let Some(receiver) = args.first() else {
        return signatures.to_vec();
    };
    let receiver_options = observed_ty_options(&receiver.ty);
    signatures
        .iter()
        .filter(|signature| {
            let Some(expected_receiver) = signature.args.first() else {
                return true;
            };
            receiver_options.iter().any(|actual_receiver| {
                does_ty_match(actual_receiver, &expected_receiver.ty) != MatchResult::NoMatch
            })
        })
        .cloned()
        .collect()
}

fn signature_match(args: &[ObservedArg], signatures: &[SupportedSignature]) -> MatchResult {
    let arg_options = observed_arg_options(args);
    if arg_options.is_empty() {
        return MatchResult::NoMatch;
    }

    let mut final_result = MatchResult::Match;
    for args in arg_options {
        let mut combination_result = MatchResult::NoMatch;
        for signature in signatures {
            combination_result = best_match(combination_result, match_signature(&args, signature));
            if combination_result == MatchResult::Match {
                break;
            }
        }
        final_result = final_result.combine(combination_result);
        if final_result == MatchResult::NoMatch {
            return MatchResult::NoMatch;
        }
    }

    final_result
}

fn supported_signature_displays(
    call: &CallsiteFact,
    signatures: &[SupportedSignature],
) -> Vec<String> {
    let display_name = call
        .qualified_name
        .as_deref()
        .unwrap_or(call.call_name.as_str());
    let skip_args = usize::from(call.call_kind == CallKind::Method);
    let mut displays = Vec::new();
    let mut seen = HashSet::new();
    for signature in signatures {
        let args = signature.args.get(skip_args..).unwrap_or(&[]);
        let display = supported_signature_display(display_name, args);
        if seen.insert(display.clone()) {
            displays.push(display);
        }
    }
    if displays.len() > 20 {
        let remaining = displays.len() - 20;
        displays.truncate(20);
        displays.push(format!("... and {remaining} more"));
    }
    displays
}

fn supported_signature_display(display_name: &str, args: &[SupportedArg]) -> String {
    format!(
        "{}({})",
        display_name,
        args.iter()
            .map(|arg| {
                let mut display = arg.ty.display();
                if let Some(name) = &arg.argument_name {
                    display = format!("{name}: {display}");
                }
                if arg.has_default {
                    display.push_str(" = ...");
                }
                display
            })
            .collect::<Vec<_>>()
            .join(", ")
    )
}

fn best_match(left: MatchResult, right: MatchResult) -> MatchResult {
    match (left, right) {
        (MatchResult::Match, _) | (_, MatchResult::Match) => MatchResult::Match,
        (MatchResult::Inconclusive, _) | (_, MatchResult::Inconclusive) => {
            MatchResult::Inconclusive
        }
        (MatchResult::NoMatch, MatchResult::NoMatch) => MatchResult::NoMatch,
    }
}

fn observed_arg_options(args: &[ObservedArg]) -> Vec<Vec<ResolvedObservedArg>> {
    let mut combinations: Vec<Vec<ResolvedObservedArg>> = vec![Vec::new()];
    for arg in args {
        let mut next_combinations = Vec::new();
        let options = observed_ty_options(&arg.ty);
        for combination in &combinations {
            for option in &options {
                let mut next = combination.clone();
                next.push(ResolvedObservedArg {
                    argument_name: arg.argument_name.clone(),
                    ty: option.clone(),
                });
                next_combinations.push(next);
                if next_combinations.len() > 128 {
                    return combinations;
                }
            }
        }
        combinations = next_combinations;
    }
    combinations
}

#[derive(Clone, Debug)]
struct ResolvedObservedArg {
    argument_name: Option<String>,
    ty: ObservedTy,
}

fn match_signature(args: &[ResolvedObservedArg], signature: &SupportedSignature) -> MatchResult {
    let mut positional_arguments = Vec::new();
    let mut keyword_arguments: HashMap<&str, &ResolvedObservedArg> = HashMap::new();

    for arg in args {
        if let Some(name) = &arg.argument_name {
            keyword_arguments.insert(name, arg);
        } else if keyword_arguments.is_empty() {
            positional_arguments.push(arg);
        } else {
            return MatchResult::NoMatch;
        }
    }

    let mut positional_index = 0usize;
    let mut result = MatchResult::Match;

    for signature_arg in &signature.args {
        let actual_arg = if positional_index < positional_arguments.len() {
            let actual_arg = positional_arguments[positional_index];
            positional_index += 1;
            Some(actual_arg)
        } else if let Some(name) = &signature_arg.argument_name {
            keyword_arguments.remove(name.as_str())
        } else {
            None
        };

        let Some(actual_arg) = actual_arg else {
            if signature_arg.has_default {
                continue;
            }
            return MatchResult::NoMatch;
        };

        result = result.combine(does_ty_match(&actual_arg.ty, &signature_arg.ty));
        if result == MatchResult::NoMatch {
            return MatchResult::NoMatch;
        }
    }

    if positional_index < positional_arguments.len() || !keyword_arguments.is_empty() {
        return MatchResult::NoMatch;
    }

    result
}

fn does_ty_match(actual: &ObservedTy, expected: &SupportedTy) -> MatchResult {
    if matches!(actual, ObservedTy::Unknown) {
        return MatchResult::Inconclusive;
    }

    if matches!(expected, SupportedTy::Any { .. }) {
        return MatchResult::Match;
    }

    match expected {
        SupportedTy::Bool { .. } => primitive_match(actual, ObservedTy::Bool),
        SupportedTy::Bytes { .. } => primitive_match(actual, ObservedTy::Bytes),
        SupportedTy::Class { module, name, .. } => match actual {
            ObservedTy::Class(actual_name) => {
                (actual_name == &format!("{module}.{name}")).into_match()
            }
            _ => MatchResult::NoMatch,
        },
        SupportedTy::Counter { items, .. } => match actual {
            ObservedTy::Counter(actual_items) => does_ty_match(actual_items, items),
            _ => MatchResult::NoMatch,
        },
        SupportedTy::Date { .. } => primitive_match(actual, ObservedTy::Date),
        SupportedTy::DateTime { .. } => primitive_match(actual, ObservedTy::DateTime),
        SupportedTy::Dict {
            key_type,
            value_type,
            ..
        } => match actual {
            ObservedTy::Dict(actual_key, actual_value) => {
                does_ty_match(actual_key, key_type).combine(does_ty_match(actual_value, value_type))
            }
            _ => MatchResult::NoMatch,
        },
        SupportedTy::Float { .. } => primitive_match(actual, ObservedTy::Float),
        SupportedTy::FrozenSet { items, .. } => match actual {
            ObservedTy::FrozenSet(actual_items) => does_ty_match(actual_items, items),
            _ => MatchResult::NoMatch,
        },
        SupportedTy::Generator { items, .. } => match actual {
            ObservedTy::Generator(actual_items) => does_ty_match(actual_items, items),
            _ => MatchResult::NoMatch,
        },
        SupportedTy::HashlibHash { .. } => primitive_match(actual, ObservedTy::HashlibHash),
        SupportedTy::Int { .. } => primitive_match(actual, ObservedTy::Int),
        SupportedTy::Iterable { items, .. } => match actual {
            ObservedTy::Generator(actual_items)
            | ObservedTy::Iterable(actual_items)
            | ObservedTy::List(actual_items)
            | ObservedTy::Set(actual_items) => does_ty_match(actual_items, items),
            _ => MatchResult::NoMatch,
        },
        SupportedTy::Json { .. } => match actual {
            ObservedTy::Dict(_, _) | ObservedTy::List(_) => MatchResult::Inconclusive,
            ObservedTy::Other(name) if name == "json" => MatchResult::Match,
            _ => MatchResult::NoMatch,
        },
        SupportedTy::List { items, .. } => match actual {
            ObservedTy::List(actual_items) => does_ty_match(actual_items, items),
            _ => MatchResult::NoMatch,
        },
        SupportedTy::Module { name, .. } => match actual {
            ObservedTy::Module(actual_name) | ObservedTy::Class(actual_name) => {
                (actual_name == name).into_match()
            }
            _ => MatchResult::NoMatch,
        },
        SupportedTy::None { .. } => primitive_match(actual, ObservedTy::None),
        SupportedTy::ReMatch { .. } => primitive_match(actual, ObservedTy::ReMatch),
        SupportedTy::RePattern { .. } => primitive_match(actual, ObservedTy::RePattern),
        SupportedTy::RequestsHttpResponse { .. } => {
            primitive_match(actual, ObservedTy::RequestsHttpResponse)
        }
        SupportedTy::Set { items, .. } => match actual {
            ObservedTy::Set(actual_items) => does_ty_match(actual_items, items),
            _ => MatchResult::NoMatch,
        },
        SupportedTy::SequenceMatcher { .. } => primitive_match(actual, ObservedTy::SequenceMatcher),
        SupportedTy::Str { .. } => primitive_match(actual, ObservedTy::Str),
        SupportedTy::SubClassOf {
            ty_name,
            match_nullable: _,
        } => subclass_match(actual, ty_name),
        SupportedTy::Time { .. } => primitive_match(actual, ObservedTy::Time),
        SupportedTy::Timedelta { .. } => primitive_match(actual, ObservedTy::Timedelta),
        SupportedTy::TimeZone { .. } => primitive_match(actual, ObservedTy::TimeZone),
        SupportedTy::Tuple {
            items, is_variable, ..
        } => match actual {
            ObservedTy::Tuple(actual_items, actual_variable) => {
                if *is_variable {
                    let Some(expected_item) = items.first() else {
                        return MatchResult::Inconclusive;
                    };
                    let mut result = MatchResult::Match;
                    for actual_item in actual_items {
                        result = result.combine(does_ty_match(actual_item, expected_item));
                    }
                    return result;
                }
                if actual_variable != is_variable || actual_items.len() != items.len() {
                    return MatchResult::NoMatch;
                }
                actual_items.iter().zip(items).fold(
                    MatchResult::Match,
                    |result, (actual_item, expected_item)| {
                        result.combine(does_ty_match(actual_item, expected_item))
                    },
                )
            }
            _ => MatchResult::NoMatch,
        },
        SupportedTy::Any { .. } => MatchResult::Match,
        SupportedTy::Other { name, .. } => match actual {
            ObservedTy::Other(actual_name) => (actual_name == name).into_match(),
            _ => MatchResult::Inconclusive,
        },
    }
}

fn primitive_match(actual: &ObservedTy, expected: ObservedTy) -> MatchResult {
    if actual == &ObservedTy::Int && expected == ObservedTy::Float {
        return MatchResult::Match;
    }
    (actual == &expected).into_match()
}

fn subclass_match(actual: &ObservedTy, ty_name: &str) -> MatchResult {
    match (ty_name, actual) {
        ("TyEnum", ObservedTy::Enum) => MatchResult::Match,
        ("TyJson", ObservedTy::Dict(_, _) | ObservedTy::List(_)) => MatchResult::Inconclusive,
        ("TyLogicalStruct", ObservedTy::LogicalStruct) => MatchResult::Match,
        ("TyTuple", ObservedTy::Tuple(_, _)) => MatchResult::Match,
        ("TyProto", ObservedTy::Other(_)) | ("TyProtoEnum", ObservedTy::Other(_)) => {
            MatchResult::Inconclusive
        }
        _ => MatchResult::NoMatch,
    }
}

trait IntoMatch {
    fn into_match(self) -> MatchResult;
}

impl IntoMatch for bool {
    fn into_match(self) -> MatchResult {
        if self {
            MatchResult::Match
        } else {
            MatchResult::NoMatch
        }
    }
}

fn observed_ty_options(raw: &str) -> Vec<ObservedTy> {
    split_top_level(raw.trim(), '|')
        .into_iter()
        .map(parse_observed_ty)
        .collect()
}

fn parse_observed_ty(raw: &str) -> ObservedTy {
    let raw = strip_outer_parens(raw.trim());
    let intersection = split_top_level(raw, '&');
    if intersection.len() > 1 {
        let concrete = intersection
            .into_iter()
            .map(str::trim)
            .filter(|part| {
                !part.starts_with('~')
                    && *part != "Any"
                    && *part != "Unknown"
                    && *part != "Divergent"
                    && !part.starts_with("Top[")
            })
            .collect::<Vec<_>>();
        if concrete.is_empty() {
            return ObservedTy::Unknown;
        }
        return parse_observed_ty(concrete[0]);
    }

    if raw == "Any" || raw == "Unknown" || raw == "Divergent" {
        return ObservedTy::Unknown;
    }
    if raw == "None" {
        return ObservedTy::None;
    }
    if raw == "bool" {
        return ObservedTy::Bool;
    }
    if raw == "bytes" {
        return ObservedTy::Bytes;
    }
    if raw == "date" {
        return ObservedTy::Date;
    }
    if raw == "datetime" {
        return ObservedTy::DateTime;
    }
    if raw == "float" {
        return ObservedTy::Float;
    }
    if raw == "hashlib.Hash" {
        return ObservedTy::HashlibHash;
    }
    if raw == "int" {
        return ObservedTy::Int;
    }
    if raw == "RequestsHttpResponse" {
        return ObservedTy::RequestsHttpResponse;
    }
    if raw == "SequenceMatcher" {
        return ObservedTy::SequenceMatcher;
    }
    if raw == "str" || raw == "LiteralString" {
        return ObservedTy::Str;
    }
    if raw == "time" {
        return ObservedTy::Time;
    }
    if raw == "timedelta" {
        return ObservedTy::Timedelta;
    }
    if raw == "timezone" {
        return ObservedTy::TimeZone;
    }
    if raw.starts_with("Literal[") {
        return parse_literal_ty(raw);
    }
    if let Some(module) = raw
        .strip_prefix("<module '")
        .and_then(|raw| raw.strip_suffix("'>"))
    {
        return ObservedTy::Module(module.to_string());
    }
    if let Some(class_name) = raw
        .strip_prefix("<class '")
        .and_then(|raw| raw.strip_suffix("'>"))
    {
        return ObservedTy::Class(normalize_class_name(class_name));
    }
    if let Some(inner) = strip_generic(raw, "list") {
        return ObservedTy::List(Box::new(parse_observed_ty(inner)));
    }
    if let Some(inner) = strip_generic(raw, "set") {
        return ObservedTy::Set(Box::new(parse_observed_ty(inner)));
    }
    if let Some(inner) = strip_generic(raw, "frozenset") {
        return ObservedTy::FrozenSet(Box::new(parse_observed_ty(inner)));
    }
    if let Some(inner) = strip_generic(raw, "FrozenSet") {
        return ObservedTy::FrozenSet(Box::new(parse_observed_ty(inner)));
    }
    if let Some(inner) = strip_generic(raw, "Counter") {
        return ObservedTy::Counter(Box::new(parse_observed_ty(inner)));
    }
    if strip_generic(raw, "Enum").is_some() {
        return ObservedTy::Enum;
    }
    if strip_generic(raw, "LogicalStruct").is_some() {
        return ObservedTy::LogicalStruct;
    }
    if raw == "Match"
        || strip_generic(raw, "Match").is_some()
        || strip_generic(raw, "re.Match").is_some()
        || strip_generic(raw, "typing.Match").is_some()
    {
        return ObservedTy::ReMatch;
    }
    if raw == "Pattern"
        || strip_generic(raw, "Pattern").is_some()
        || strip_generic(raw, "re.Pattern").is_some()
        || strip_generic(raw, "typing.Pattern").is_some()
    {
        return ObservedTy::RePattern;
    }
    if let Some(inner) = strip_generic(raw, "GeneratorType") {
        let item = split_top_level(inner, ',')
            .into_iter()
            .next()
            .map(parse_observed_ty)
            .unwrap_or(ObservedTy::Unknown);
        return ObservedTy::Generator(Box::new(item));
    }
    if let Some(inner) = strip_generic(raw, "Iterable") {
        return ObservedTy::Iterable(Box::new(parse_observed_ty(inner)));
    }
    if let Some(inner) = strip_generic(raw, "dict") {
        let parts = split_top_level(inner, ',');
        if parts.len() == 2 {
            return ObservedTy::Dict(
                Box::new(parse_observed_ty(parts[0])),
                Box::new(parse_observed_ty(parts[1])),
            );
        }
    }
    if let Some(inner) = strip_generic(raw, "tuple") {
        let parts = split_top_level(inner, ',');
        if parts.len() == 2 && parts[1].trim() == "..." {
            return ObservedTy::Tuple(vec![parse_observed_ty(parts[0])], true);
        }
        return ObservedTy::Tuple(parts.into_iter().map(parse_observed_ty).collect(), false);
    }
    if raw.starts_with("() -> ") {
        return ObservedTy::Function;
    }

    ObservedTy::Other(raw.to_string())
}

fn parse_literal_ty(raw: &str) -> ObservedTy {
    let Some(inner) = strip_generic(raw, "Literal") else {
        return ObservedTy::Unknown;
    };
    let mut result = None;
    for literal in split_top_level(inner, ',') {
        let literal_ty = literal_kind(literal.trim());
        result = match (result, literal_ty) {
            (None, Some(ty)) => Some(ty),
            (Some(existing), Some(ty)) if existing == ty => Some(existing),
            _ => return ObservedTy::Unknown,
        };
    }
    result.unwrap_or(ObservedTy::Unknown)
}

fn literal_kind(raw: &str) -> Option<ObservedTy> {
    if raw == "True" || raw == "False" {
        Some(ObservedTy::Bool)
    } else if raw.starts_with('"') || raw.starts_with('\'') {
        Some(ObservedTy::Str)
    } else if raw.parse::<i64>().is_ok() {
        Some(ObservedTy::Int)
    } else if raw.parse::<f64>().is_ok() {
        Some(ObservedTy::Float)
    } else {
        None
    }
}

fn normalize_class_name(class_name: &str) -> String {
    match class_name {
        "bool" | "bytes" | "dict" | "float" | "int" | "list" | "set" | "str" | "tuple" => {
            format!("builtins.{class_name}")
        }
        "date" => "datetime.date".to_string(),
        "datetime" => "datetime.datetime".to_string(),
        "time" => "datetime.time".to_string(),
        "timedelta" => "datetime.timedelta".to_string(),
        "timezone" => "datetime.timezone".to_string(),
        _ => class_name.to_string(),
    }
}

fn strip_generic<'a>(raw: &'a str, name: &str) -> Option<&'a str> {
    let prefix = format!("{name}[");
    raw.strip_prefix(&prefix)
        .and_then(|raw| raw.strip_suffix(']'))
}

fn split_top_level(raw: &str, delimiter: char) -> Vec<&str> {
    let mut result = Vec::new();
    let mut start = 0usize;
    let mut state = SyntaxState::default();
    for (index, ch) in raw.char_indices() {
        if state.is_top_level() && ch == delimiter {
            result.push(raw[start..index].trim());
            start = index + ch.len_utf8();
        }
        state.advance(ch);
    }
    result.push(raw[start..].trim());
    result
}

fn strip_outer_parens(raw: &str) -> &str {
    let mut raw = raw.trim();
    loop {
        let Some(stripped) = strip_wrapping(raw, '(', ')') else {
            return raw;
        };
        raw = stripped.trim();
    }
}

fn strip_wrapping(raw: &str, open_ch: char, close_ch: char) -> Option<&str> {
    let raw = raw.trim();
    if !raw.starts_with(open_ch) || !raw.ends_with(close_ch) {
        return None;
    }
    let close = raw.len() - close_ch.len_utf8();
    if find_matching_close(raw, 0)? == close {
        Some(&raw[open_ch.len_utf8()..close])
    } else {
        None
    }
}

fn find_matching_close(raw: &str, open: usize) -> Option<usize> {
    let mut state = SyntaxState::default();
    let mut depth = 0usize;

    for (index, ch) in raw.char_indices().filter(|(index, _)| *index >= open) {
        if state.quote.is_none() {
            if ch == '(' {
                depth += 1;
            } else if ch == ')' {
                depth = depth.checked_sub(1)?;
                if depth == 0 {
                    return Some(index);
                }
            }
        }
        state.advance(ch);
    }

    None
}

#[derive(Default)]
struct SyntaxState {
    parens: i32,
    brackets: i32,
    braces: i32,
    quote: Option<char>,
    escaped: bool,
}

impl SyntaxState {
    fn is_top_level(&self) -> bool {
        self.parens == 0 && self.brackets == 0 && self.braces == 0 && self.quote.is_none()
    }

    fn advance(&mut self, ch: char) {
        if let Some(quote) = self.quote {
            if self.escaped {
                self.escaped = false;
            } else if ch == '\\' {
                self.escaped = true;
            } else if ch == quote {
                self.quote = None;
            }
            return;
        }

        match ch {
            '\'' | '"' => self.quote = Some(ch),
            '(' => self.parens += 1,
            ')' => self.parens -= 1,
            '[' => self.brackets += 1,
            ']' => self.brackets -= 1,
            '{' => self.braces += 1,
            '}' => self.braces -= 1,
            _ => {}
        }
    }
}

#[cfg(test)]
mod tests {
    use std::{collections::HashMap, path::PathBuf};

    use super::*;

    #[test]
    fn cheapo_fixture_test() {
        let root =
            PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/resources/cheapo_minimal");
        let findings = collect_findings_for_project(&root, &[], supported_funcs()).unwrap();
        let by_signature: HashMap<&str, &CheapoFinding> = findings
            .iter()
            .map(|finding| (finding.call_signature.as_str(), finding))
            .collect();

        // Supported calls are accepted.
        assert!(!by_signature.contains_key("math::sqrt(float)"));
        assert!(!by_signature.contains_key("math::sqrt(int)"));
        assert!(!by_signature.contains_key("json::loads(str)"));
        assert!(!by_signature.contains_key("re::search(str, str)"));
        assert!(!findings
            .iter()
            .any(|finding| finding.call_signature.starts_with("bool(Match[")));
        assert!(!findings
            .iter()
            .any(|finding| finding.call_signature.starts_with("search(Pattern[")));
        assert!(!findings
            .iter()
            .any(|finding| finding.call_signature.starts_with("len(list[")));
        assert!(!findings
            .iter()
            .any(|finding| finding.call_signature.starts_with("hexdigest(hashlib.Hash")));
        assert!(!findings
            .iter()
            .any(|finding| finding.call_signature.starts_with("digest(hashlib.Hash")));
        assert!(!findings
            .iter()
            .any(|finding| finding.call_signature.starts_with("ratio(SequenceMatcher")));
        assert!(!findings
            .iter()
            .any(|finding| finding.call_signature.starts_with("__eq__(Enum[")));
        assert!(!findings
            .iter()
            .any(|finding| finding.call_signature.starts_with("bool(LogicalStruct[")));

        // Unsupported calls report no suggested signatures.
        assert!(by_signature["math::gcd(int, int)"]
            .supported_signatures
            .is_empty());
        assert!(by_signature["json::load(int)"]
            .supported_signatures
            .is_empty());
        assert!(by_signature["re::finditer(str, str)"]
            .supported_signatures
            .is_empty());

        // Builtin len checks the receiver's __len__ support.
        let len_counter = findings
            .iter()
            .find(|finding| finding.call_signature.starts_with("len(Counter["))
            .expect("expected len(Counter[...]) to be reported");
        assert!(!len_counter.supported_signatures.is_empty());

        // Wrong argument types report suggested signatures.
        assert!(!by_signature["math::sqrt(str)"]
            .supported_signatures
            .is_empty());
        assert!(!by_signature["json::loads(int)"]
            .supported_signatures
            .is_empty());
        assert!(!by_signature["re::search(int, str)"]
            .supported_signatures
            .is_empty());
    }
}
