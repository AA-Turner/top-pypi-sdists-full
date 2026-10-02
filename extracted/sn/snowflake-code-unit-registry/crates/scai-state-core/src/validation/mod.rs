//! Registry validation — JSON syntax, schema conformance, structural
//! integrity, and optional checksum verification.
//!
//! Each file is automatically migrated to [`CURRENT_SCHEMA_VERSION`](crate::migration::CURRENT_SCHEMA_VERSION)
//! before schema validation runs. If migration fails (e.g. future or
//! malformed `schemaVersion`), a [`SchemaMigrationError`](ValidationIssueKind::SchemaMigrationError)
//! issue is recorded with the originating error code.
//!
//! The JSON Schema is embedded at compile time and the compiled validator
//! is cached in an [`OnceLock`] so repeated calls avoid recompilation.
//!
//! # Validation mechanism policy
//!
//! Structural rules beyond plain JSON Schema land in one of two places.
//! New rules **default to the schema** — only fall back to imperative
//! code when a schema annotation cannot express the rule.
//!
//! ## Prefer schema annotations (default)
//!
//! These cover everything that reasons about field **presence** gated on
//! sibling/ancestor field **values**:
//!
//! - `x-allowed-when` (`apply_allowed_when_constraints`) — leaf may
//!   appear only when every gate resolves to one of its allowed values.
//! - `x-required-when` (`apply_required_when_constraints`) — leaf must
//!   appear once every gate resolves to one of its allowed values.
//! - `x-allowed-fields` (`apply_allowed_field_constraints`) — restricts
//!   which sub-keys an object may carry at a `$ref` use site.
//!
//! Annotations live next to the field they constrain in
//! `code-unit.schema.json`, are extracted at build time into
//! [`crate::generated::schema_constraints`], and are interpreted by the
//! `apply_*_constraints` helpers below.  Adding a new rule of an
//! existing shape is a one-line schema edit.
//!
//! Gate paths in `x-allowed-when` / `x-required-when` resolve
//! **lexically** from the gated field's parent upward — the closest
//! enclosing scope that defines the gate's first segment wins.  Absent
//! gates are vacuously satisfied so upstream presence checks (typically
//! on `kind`) own the diagnostic for the discriminator being missing.
//!
//! One kind stands outside this: `kind: "custom"` documents are exempt
//! from every `x-allowed-when` gate and may carry any field in the schema
//! (see [`is_field_gate_exempt`]).  The gates describe how the conversion
//! engine partitions fields across the kinds it owns; a custom unit names
//! its own type via `customKind` and is orchestrated elsewhere.  So when
//! you add a gate, you do not need to remember to list `"custom"` in it —
//! and you cannot accidentally lock custom units out by forgetting.
//!
//! ## Imperative is justified only when…
//!
//! …the rule cannot be expressed by the annotation vocabulary above.
//! Two structural classes can call for imperative code:
//!
//! 1. **Content-aware checks** — the field is allowed; only its
//!    *contents* matter, which the presence-vs-value vocabulary above
//!    cannot express. None exist today; e.g., were a future rule to
//!    require that an otherwise-allowed array be empty, it would land
//!    here (emptiness is not presence).
//! 2. **Or-of-shapes invariants** — a rule like "at least one of N
//!    sides must be complete" requires evaluating multiple field
//!    presences as a single predicate, not per-leaf gating.
//!    Examples: `apply_database_object_identity`,
//!    `apply_script_identity`.
//!
//! New imperative helpers should name the structural class they
//! enforce (`apply_*_identity`, `apply_*_emptiness`, …) rather than the
//! kind they fire on, and should funnel through `validate_kind_rules`
//! so every per-kind rule shares one entry point and one issue-kind
//! (`ValidationIssueKind::PerKindStructure`).
//!
//! When in doubt: if a rule asks "is field X present?" gated on the
//! values of other fields, it belongs in the schema.  Anything else
//! earns its imperative spot with a doc comment explaining which class
//! above applies.

/// Structural validation of a script's declared `scriptMetadata.IO[]` against
/// the file references a test case supplies.
pub mod script_io;

use std::collections::HashSet;
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::OnceLock;

use serde::{Deserialize, Serialize};
use serde_json::Value;

use crate::checksum::{validate_checksum_report, ChecksumMode, ChecksumValidationStatus};
use crate::dependency_view::{self, Origin};
use crate::error::*;
use crate::generated::types::CodeUnit;
use crate::registry::paths::{filename_of, filename_stem};

const SCHEMA_JSON: &str = include_str!("../../schemas/code-unit.schema.json");

fn schema_validator() -> &'static jsonschema::Validator {
    static VALIDATOR: OnceLock<jsonschema::Validator> = OnceLock::new();
    VALIDATOR.get_or_init(|| {
        let schema: Value =
            serde_json::from_str(SCHEMA_JSON).expect("embedded schema is valid JSON");
        jsonschema::validator_for(&schema).expect("embedded schema compiles")
    })
}

// ── Types ────────────────────────────────────────────────────────────────

/// Category of a validation issue.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ValidationIssueKind {
    IoError,
    InvalidJson,
    SchemaViolation,
    DeserializationError,
    MissingId,
    IdFilenameMismatch,
    DuplicateId,
    UnresolvedDependency,
    ChecksumMismatch,
    NonCanonicalPath,
    SchemaMigrationError,
    /// Violation of a per-kind structural rule (required/forbidden/conditional
    /// fields by `kind`). Distinct from [`SchemaViolation`](Self::SchemaViolation)
    /// so consumers can distinguish JSON-Schema-level from kind-aware checks.
    PerKindStructure,
}

/// A single validation issue tied to a specific file.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ValidationIssue {
    pub file: String,
    pub kind: ValidationIssueKind,
    pub message: String,
    /// Stable error code from the core `Error` enum, when the issue
    /// originates from a core operation (e.g. migration). `None` for
    /// issues that are purely validation-layer concerns (e.g. duplicate ID).
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error_code: Option<i32>,
}

impl ValidationIssue {
    fn new(file: &str, kind: ValidationIssueKind, message: impl Into<String>) -> Self {
        Self {
            file: file.to_string(),
            kind,
            message: message.into(),
            error_code: None,
        }
    }

    fn with_error_code(mut self, code: i32) -> Self {
        self.error_code = Some(code);
        self
    }
}

/// Result of a registry validation run.
///
/// `is_valid` is `true` only when `issues` is empty.
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ValidationReport {
    pub is_valid: bool,
    pub files_checked: usize,
    pub issues: Vec<ValidationIssue>,
}

impl ValidationReport {
    fn from_issues(files_checked: usize, issues: Vec<ValidationIssue>) -> Self {
        Self {
            is_valid: issues.is_empty(),
            files_checked,
            issues,
        }
    }
}

// ── Helpers ──────────────────────────────────────────────────────────────

/// On `Ok`, returns `Some(value)`. On `Err`, records a validation issue and
/// returns `None` so the caller can short-circuit with `?`.
fn try_or_issue<T, E: std::fmt::Display>(
    result: std::result::Result<T, E>,
    issues: &mut Vec<ValidationIssue>,
    file: &str,
    kind: ValidationIssueKind,
    context: &str,
) -> Option<T> {
    match result {
        Ok(v) => Some(v),
        Err(e) => {
            issues.push(ValidationIssue::new(file, kind, format!("{context}: {e}")));
            None
        }
    }
}

/// Like [`try_or_issue`], but for core `Error` results — extracts the stable
/// error code and attaches it to the validation issue.
fn try_or_issue_with_code<T>(
    result: Result<T>,
    issues: &mut Vec<ValidationIssue>,
    file: &str,
    kind: ValidationIssueKind,
    context: &str,
) -> Option<T> {
    match result {
        Ok(v) => Some(v),
        Err(e) => {
            let code = e.error_code_i32();
            issues.push(
                ValidationIssue::new(file, kind, format!("{context}: {e}")).with_error_code(code),
            );
            None
        }
    }
}

/// Collect all `.json` file paths and their filenames from a directory.
fn list_json_files(dir: &Path) -> Result<Vec<(PathBuf, String)>> {
    Ok(crate::registry::paths::json_file_paths(dir)?
        .into_iter()
        .map(|p| {
            let name = filename_of(&p);
            (p, name)
        })
        .collect())
}

// ── Per-file validation ──────────────────────────────────────────────────

/// Validate a single JSON file against the schema and structural rules.
///
/// Issues are accumulated into `issues` as they are found. Returns
/// `Some(CodeUnit)` when parsing succeeds (even if issues were recorded),
/// or `None` when the file is too broken to parse.
fn validate_file(
    path: &Path,
    filename: &str,
    checksum_mode: &ChecksumMode,
    root: &Path,
    issues: &mut Vec<ValidationIssue>,
) -> Option<CodeUnit> {
    let contents = try_or_issue(
        fs::read_to_string(path),
        issues,
        filename,
        ValidationIssueKind::IoError,
        "Failed to read file",
    )?;

    let value: Value = try_or_issue(
        serde_json::from_str(&contents),
        issues,
        filename,
        ValidationIssueKind::InvalidJson,
        "Invalid JSON",
    )?;

    let value: Value = try_or_issue_with_code(
        crate::migration::migrate(value),
        issues,
        filename,
        ValidationIssueKind::SchemaMigrationError,
        "Schema migration failed",
    )?;

    // Schema validation — collects multiple errors, doesn't short-circuit.
    let validator = schema_validator();
    for error in validator.iter_errors(&value) {
        issues.push(ValidationIssue::new(
            filename,
            ValidationIssueKind::SchemaViolation,
            format!("{error} (at {})", error.instance_path()),
        ));
    }

    validate_kind_rules(&value, filename, issues);

    // Non-canonical path detection — runs before from_value consumes the Value.
    check_non_canonical_paths(&value, filename, issues);

    // Deserialization — collects multiple errors, doesn't short-circuit.
    let code_unit: CodeUnit = try_or_issue(
        serde_json::from_value(value),
        issues,
        filename,
        ValidationIssueKind::DeserializationError,
        "Failed to deserialize",
    )?;

    // ID / filename consistency
    if let (Ok(stem), Some(ref id)) = (filename_stem(path), &code_unit.id) {
        if id != stem {
            issues.push(ValidationIssue::new(
                filename,
                ValidationIssueKind::IdFilenameMismatch,
                format!("ID '{id}' does not match filename stem '{stem}'"),
            ));
        }
    }

    // Checksum validation (skipped when mode is none)
    if !checksum_mode.is_none() {
        let report = validate_checksum_report(&code_unit, checksum_mode, root);
        for entry in &report.entries {
            let msg = match entry.status {
                ChecksumValidationStatus::Mismatch => format!(
                    "Checksum mismatch on field '{}': stored={}, computed={}",
                    entry.field,
                    entry.stored_checksum.as_deref().unwrap_or("none"),
                    entry.computed_checksum.as_deref().unwrap_or("none"),
                ),
                ChecksumValidationStatus::MissingFile => format!(
                    "File not found for field '{}': path is set but file does not exist on disk",
                    entry.field,
                ),
                ChecksumValidationStatus::IoError => format!(
                    "I/O error reading file for field '{}': unable to compute checksum",
                    entry.field,
                ),
                _ => continue,
            };
            issues.push(ValidationIssue::new(
                filename,
                ValidationIssueKind::ChecksumMismatch,
                msg,
            ));
        }
    }

    Some(code_unit)
}

fn check_non_canonical_paths(value: &Value, filename: &str, issues: &mut Vec<ValidationIssue>) {
    use crate::generated::file_path_fields::FILE_PATH_FIELDS;
    use crate::registry::paths::navigate_path;

    for segments in FILE_PATH_FIELDS {
        let Some(s) = navigate_path(value, segments).and_then(|v| v.as_str()) else {
            continue;
        };
        if s.contains('\\') {
            issues.push(ValidationIssue::new(
                filename,
                ValidationIssueKind::NonCanonicalPath,
                format!(
                    "Field '{}' contains backslash separators: '{s}'. \
                     Paths will be normalized to forward slashes on next write.",
                    segments.join("."),
                ),
            ));
        }
    }
}

// ── Cross-unit checks ────────────────────────────────────────────────────

/// Check that all dependency references point to existing units. Please note that the
/// existing units might not have a corresponding source code file, but the CodeUnit file
/// is still expected to exist (this is the case of missing dependencies).
fn check_referential_integrity(
    units: &[(String, String, CodeUnit)],
    known_ids: &HashSet<String>,
    issues: &mut Vec<ValidationIssue>,
) {
    for (_, filename, unit) in units {
        for (origin, dep) in dependency_view::depends_on_with_origin(unit) {
            let Some(dep_id) = dep.id.as_deref() else {
                continue;
            };
            if known_ids.contains(dep_id) {
                continue;
            }
            let message = match origin {
                Origin::Root => {
                    format!("Depends on '{dep_id}' which does not exist in the registry")
                }
                Origin::Part(part_id) => format!(
                    "Part '{part_id}' depends on '{dep_id}' which does not exist in the registry"
                ),
            };
            issues.push(ValidationIssue::new(
                filename,
                ValidationIssueKind::UnresolvedDependency,
                message,
            ));
        }
    }
}

// ── Per-kind validation ──────────────────────────────────────────────────

/// Per-kind structural pipeline: schema-driven `apply_*_constraints` first,
/// then the small set of imperative survivors keyed off `kind`.  Runs on
/// the raw [`Value`] before typed deserialization so a single pass can
/// surface every violation, even when typed deserialization would itself
/// fail.  All issues land with [`ValidationIssueKind::PerKindStructure`].
///
/// See the module-level "Validation mechanism policy" for the rules
/// governing where a new structural check belongs.
fn validate_kind_rules(value: &Value, filename: &str, issues: &mut Vec<ValidationIssue>) {
    if !is_field_gate_exempt(value) {
        apply_allowed_when_constraints(value, filename, issues);
    }
    apply_required_when_constraints(value, filename, issues);
    apply_allowed_field_constraints(value, filename, issues);

    let Some(kind) = value.get("kind").and_then(|v| v.as_str()) else {
        return;
    };
    match kind {
        "databaseObject" => apply_database_object_identity(value, filename, issues),
        "script" => apply_script_identity(value, filename, issues),
        "custom" => apply_custom_identity(value, filename, issues),
        _ => {}
    }
}

/// `kind` whose documents opt out of `x-allowed-when` field gating.
const FIELD_GATE_EXEMPT_KIND: &str = "custom";

/// True when this document's `kind` is exempt from every `x-allowed-when`
/// gate, letting it carry any field in the schema.
///
/// The gates partition fields across the *built-in* kinds, whose shapes the
/// conversion engine owns.  A `custom` unit is defined by its own
/// `customKind` and is orchestrated by a project-local state machine, so the
/// engine's partitioning does not describe it and would only get in its way.
/// Exempting the kind here — rather than appending `"custom"` to each
/// allow-list — is what keeps the escape hatch open: a gate added later
/// cannot silently start excluding custom units.
///
/// Scoped to `x-allowed-when` on purpose.  `x-required-when` still applies
/// (nothing it can express today fires on `custom`, and a future rule that
/// did should be a deliberate decision), as does `x-allowed-fields`, which
/// constrains sub-keys of a field rather than whether the field may appear.
/// Gates on non-custom documents are untouched, so `customKind` on a
/// `databaseObject` is still rejected.
fn is_field_gate_exempt(value: &Value) -> bool {
    value.get("kind").and_then(|v| v.as_str()) == Some(FIELD_GATE_EXEMPT_KIND)
}

fn push_issue(issues: &mut Vec<ValidationIssue>, filename: &str, msg: impl Into<String>) {
    issues.push(ValidationIssue::new(
        filename,
        ValidationIssueKind::PerKindStructure,
        msg,
    ));
}

// ── Schema-driven helpers ────────────────────────────────────────────────

/// Apply every `x-allowed-when` constraint emitted in
/// [`schema_constraints::ALLOWED_WHEN_CONSTRAINTS`](crate::generated::schema_constraints::ALLOWED_WHEN_CONSTRAINTS).
///
/// For each constraint:
/// 1. Walk the schema parent pointer into the document, fanning out across
///    array `/items` segments — every concrete `(parent_segments, parent_value)`
///    occurrence is independently checked.
/// 2. If the gated leaf is "present" on the parent (see [`is_field_present`])
///    and any gate's resolved value is *not* in the allow-list, record an
///    issue.  Gates resolve **lexically** from the parent upward via
///    [`resolve_gate_lexical`], so a gate named `format` finds a sibling
///    `target.format` before falling back to a root-level `format`, and a
///    gate named `kind` from `codeStatus.stabilization` walks up to find
///    `root.kind`.
///
/// Absent gate values are treated as vacuously satisfied so that upstream
/// JSON Schema checks (which catch missing/invalid `kind`) own those
/// diagnostics.
fn apply_allowed_when_constraints(
    value: &Value,
    filename: &str,
    issues: &mut Vec<ValidationIssue>,
) {
    use crate::generated::schema_constraints::ALLOWED_WHEN_CONSTRAINTS;

    for constraint in ALLOWED_WHEN_CONSTRAINTS {
        for parent in walk_pointer_in_document(value, constraint.parent_pointer) {
            let Some(leaf) = parent.value.get(constraint.leaf_name) else {
                continue;
            };
            if !is_field_present(leaf) {
                continue;
            }
            for (gate_path, allowed) in constraint.when {
                let Some(actual) = resolve_gate_lexical(value, &parent.segments, gate_path)
                    .and_then(|v| v.as_str())
                else {
                    continue;
                };
                if !allowed.contains(&actual) {
                    push_issue(
                        issues,
                        filename,
                        format!(
                            "{leaf_label} is not allowed when {gate_path} is '{actual}' (allowed values: {})",
                            allowed.join(", "),
                            leaf_label = leaf_label(&parent.segments, constraint.leaf_name),
                        ),
                    );
                }
            }
        }
    }
}

/// Apply every `x-required-when` constraint emitted in
/// [`schema_constraints::REQUIRED_WHEN_CONSTRAINTS`](crate::generated::schema_constraints::REQUIRED_WHEN_CONSTRAINTS).
///
/// Mirror of [`apply_allowed_when_constraints`] with opposite semantic:
/// the leaf is **required to be present** when every gate resolves to one
/// of its allowed values.  When the leaf is already present, no issue is
/// raised regardless of the gates (over-presence is the domain of
/// `x-allowed-when`).  Absent gates are vacuously satisfied so that
/// upstream presence checks (typically on `kind`) own the diagnostic for
/// the root discriminator being missing.
fn apply_required_when_constraints(
    value: &Value,
    filename: &str,
    issues: &mut Vec<ValidationIssue>,
) {
    use crate::generated::schema_constraints::REQUIRED_WHEN_CONSTRAINTS;

    for constraint in REQUIRED_WHEN_CONSTRAINTS {
        for parent in walk_pointer_in_document(value, constraint.parent_pointer) {
            if parent
                .value
                .get(constraint.leaf_name)
                .is_some_and(is_field_present)
            {
                continue;
            }
            // Leaf absent (or null/empty-array): check whether all gates
            // are satisfied.  Any unresolved or out-of-allow-list gate
            // makes the requirement vacuous.
            let mut all_gates_match = true;
            let mut conditions: Vec<String> = Vec::with_capacity(constraint.when.len());
            for (gate_path, allowed) in constraint.when {
                let actual = resolve_gate_lexical(value, &parent.segments, gate_path)
                    .and_then(|v| v.as_str());
                match actual {
                    Some(a) if allowed.contains(&a) => {
                        conditions.push(format!("{gate_path} is '{a}'"));
                    }
                    _ => {
                        all_gates_match = false;
                        break;
                    }
                }
            }
            if all_gates_match {
                push_issue(
                    issues,
                    filename,
                    format!(
                        "{} is required when {}",
                        leaf_label(&parent.segments, constraint.leaf_name),
                        conditions.join(" and "),
                    ),
                );
            }
        }
    }
}

/// Apply every `x-allowed-fields` constraint emitted in
/// [`schema_constraints::ALLOWED_FIELD_CONSTRAINTS`](crate::generated::schema_constraints::ALLOWED_FIELD_CONSTRAINTS).
///
/// Each constraint's JSON Pointer is interpreted against the *document*
/// (not the schema): `/properties/<name>` segments navigate into object
/// fields, and `/items` segments fan out across array elements.  Any
/// sub-key of the targeted object that is not in the allow-list yields an
/// issue, fail-closing new sub-fields until the schema explicitly opts
/// them in.
fn apply_allowed_field_constraints(
    value: &Value,
    filename: &str,
    issues: &mut Vec<ValidationIssue>,
) {
    use crate::generated::schema_constraints::ALLOWED_FIELD_CONSTRAINTS;

    for constraint in ALLOWED_FIELD_CONSTRAINTS {
        for occ in walk_pointer_in_document(value, constraint.pointer) {
            let Some(obj) = occ.value.as_object() else {
                continue;
            };
            let label = render_segments(&occ.segments);
            for key in obj.keys() {
                if !constraint.allowed_fields.contains(&key.as_str()) {
                    push_issue(
                        issues,
                        filename,
                        format!(
                            "{label}.{key} is not allowed (allowed fields: {})",
                            constraint.allowed_fields.join(", "),
                        ),
                    );
                }
            }
        }
    }
}

/// One concrete address in the document, produced by
/// [`walk_pointer_in_document`].
struct DocOccurrence<'a> {
    /// Segments from the document root to this occurrence — a mix of
    /// object keys and array indices.
    segments: Vec<Seg>,
    /// The matched node.
    value: &'a Value,
}

/// One address segment.  Object lookups use `Key`; array fan-out emits
/// `Index`.  Kept separate so [`navigate_segments`] can dispatch correctly
/// without re-parsing rendered labels.
#[derive(Debug, Clone)]
enum Seg {
    Key(String),
    Index(usize),
}

/// "Presence" semantics shared by `x-allowed-when` and `x-required-when`.
/// A field counts as absent — and therefore vacuously satisfies any
/// allow-when constraint and triggers any required-when one — when it is
/// JSON `null` or an empty array.  Empty objects count as present so that
/// users who explicitly opt into a subtree (e.g. `codeStatus.stabilization: {}`)
/// still trigger the gating rule.
fn is_field_present(value: &Value) -> bool {
    match value {
        Value::Null => false,
        Value::Array(a) => !a.is_empty(),
        _ => true,
    }
}

/// Render a segment list as a human-readable dotted path, e.g.
/// `parts[0].target.modelName`.
fn render_segments(segments: &[Seg]) -> String {
    let mut out = String::new();
    for seg in segments {
        match seg {
            Seg::Key(k) => {
                if !out.is_empty() {
                    out.push('.');
                }
                out.push_str(k);
            }
            Seg::Index(i) => {
                out.push_str(&format!("[{i}]"));
            }
        }
    }
    out
}

/// Compose a leaf label from its parent's segments and the leaf name.
fn leaf_label(parent_segments: &[Seg], leaf_name: &str) -> String {
    if parent_segments.is_empty() {
        leaf_name.to_string()
    } else {
        format!("{}.{leaf_name}", render_segments(parent_segments))
    }
}

/// Navigate a segment list from `root`, returning `None` on any miss.
fn navigate_segments<'a>(root: &'a Value, segments: &[Seg]) -> Option<&'a Value> {
    let mut current = root;
    for seg in segments {
        current = match seg {
            Seg::Key(k) => current.get(k.as_str())?,
            Seg::Index(i) => current.get(*i)?,
        };
    }
    Some(current)
}

/// Resolve a gate's dotted path **lexically** starting from
/// `parent_segments` and walking up the document tree until the gate's
/// first segment is found, or the root is exhausted.
///
/// "Lexical" means the closest enclosing scope wins: a gate path `format`
/// referenced from `parts[i].target.modelName` resolves to
/// `parts[i].target.format` (parent), not to a root-level `format`.  This
/// matches the way nested-scope variables resolve in most languages and
/// keeps gate authors from having to spell out absolute paths.
///
/// Returns `None` when no enclosing scope contains the gate path — callers
/// treat this as vacuously satisfied so upstream presence checks own the
/// diagnostic.
fn resolve_gate_lexical<'a>(
    root: &'a Value,
    parent_segments: &[Seg],
    gate_path: &str,
) -> Option<&'a Value> {
    // Walk shallower scopes (parent first, then grandparent, …, then root)
    // and try to resolve `gate_path` beneath each.  Closest match wins,
    // matching nested-scope variable resolution in most languages.
    for depth in (0..=parent_segments.len()).rev() {
        let Some(scope) = navigate_segments(root, &parent_segments[..depth]) else {
            continue;
        };
        if let Some(v) = navigate_dotted(scope, gate_path) {
            return Some(v);
        }
    }
    None
}

/// Walk a dotted property path from `start`, e.g. `"target.format"` →
/// `start.get("target")?.get("format")`.  Object lookups only — no array
/// indexing (gate paths in `x-allowed-when` / `x-required-when` are
/// always property chains).
fn navigate_dotted<'a>(start: &'a Value, dotted: &str) -> Option<&'a Value> {
    let mut cur = start;
    for seg in dotted.split('.') {
        cur = cur.get(seg)?;
    }
    Some(cur)
}

/// Walk a schema-shaped JSON Pointer into the *document*, yielding every
/// concrete occurrence with structured segments.  `/properties/<name>`
/// pushes a `Seg::Key`; `/items` fans out across array elements, pushing
/// a `Seg::Index` for each.
///
/// Other pointer tokens are unsupported and silently skip the constraint;
/// adding new schema shapes (e.g. `oneOf`) means extending this walker.
fn walk_pointer_in_document<'a>(value: &'a Value, pointer: &str) -> Vec<DocOccurrence<'a>> {
    // A `'static` Null sentinel that we hand out when descending into a
    // property that is absent on a parent occurrence.  Synthesizing a
    // null-valued occurrence (rather than dropping the path) lets
    // presence-required rules (`x-required-when`) fire when the parent
    // itself is missing — the leaf is then trivially absent too.  Other
    // consumers (`x-allowed-when`, `x-allowed-fields`) treat null
    // parents as "no leaf, no fields", preserving prior behavior.
    static NULL: Value = Value::Null;

    // Tokenize the pointer once: skip the leading empty element, drop
    // any other empty tokens.  An empty pointer ("") yields no tokens
    // and resolves to the document root.
    let mut tokens = pointer.split('/').skip(1).filter(|s| !s.is_empty());
    let mut frontier: Vec<DocOccurrence<'a>> = vec![DocOccurrence {
        segments: Vec::new(),
        value,
    }];
    while let Some(tok) = tokens.next() {
        frontier = match tok {
            "properties" => {
                let Some(name) = tokens.next() else {
                    return Vec::new();
                };
                frontier
                    .into_iter()
                    .map(|occ| {
                        let child = occ.value.get(name).unwrap_or(&NULL);
                        let mut segs = occ.segments;
                        segs.push(Seg::Key(name.to_string()));
                        DocOccurrence {
                            segments: segs,
                            value: child,
                        }
                    })
                    .collect()
            }
            "items" => frontier
                .into_iter()
                .filter_map(|occ| occ.value.as_array().map(|arr| (occ.segments, arr)))
                .flat_map(|(parent_segs, arr)| {
                    arr.iter().enumerate().map(move |(idx, child)| {
                        let mut segs = parent_segs.clone();
                        segs.push(Seg::Index(idx));
                        DocOccurrence {
                            segments: segs,
                            value: child,
                        }
                    })
                })
                .collect(),
            _ => return Vec::new(),
        };
    }
    frontier
}

// ── Imperative cross-element helpers ─────────────────────────────────────

/// `databaseObject` identity rules: at least one of `source` or `target`
/// must carry a complete identity (`objectType` + `name`), and when a side
/// is present at all both fields are required on it.
fn apply_database_object_identity(
    value: &Value,
    filename: &str,
    issues: &mut Vec<ValidationIssue>,
) {
    let source = value.get("source");
    let target = value.get("target");

    let side_complete = |side: Option<&Value>| {
        side.is_some_and(|s| s.get("objectType").is_some() && s.get("name").is_some())
    };

    if !side_complete(source) && !side_complete(target) {
        push_issue(
            issues,
            filename,
            "databaseObject must have at least one complete side (source or target) with objectType and name",
        );
    }

    for (label, side) in [("source", source), ("target", target)] {
        let Some(side) = side else { continue };
        for required in ["objectType", "name"] {
            if side.get(required).is_none() {
                push_issue(
                    issues,
                    filename,
                    format!("databaseObject with present {label} must set {label}.{required}"),
                );
            }
        }
    }
}

/// `script` identity rule (spec D24): at least one side must carry a
/// complete identity — source requires `platform`, `format`, and
/// `files.source.path`; target requires only `format` and
/// `files.converted.path` (platform is always "snowflake").
///
/// Cross-field requirement that `target.format` be present once
/// `codeStatus.conversion.status == "completed"` is enforced
/// schema-side via `x-required-when` on `target.format` (see
/// [`apply_required_when_constraints`]).
fn apply_script_identity(value: &Value, filename: &str, issues: &mut Vec<ValidationIssue>) {
    let files = value.get("files");
    let source_side_complete =
        source_side_complete_with_path(value.get("source"), files.and_then(|f| f.get("source")));
    let target_side_complete =
        target_side_complete_with_path(value.get("target"), files.and_then(|f| f.get("converted")));

    if !source_side_complete && !target_side_complete {
        push_issue(
            issues,
            filename,
            "script must have at least one complete side: \
             a source with platform/format/files.source.path, \
             or a target with format/files.converted.path",
        );
    }
}

/// Source side is complete when platform, format, and path are all present and non-empty.
fn source_side_complete_with_path(side: Option<&Value>, file_entry: Option<&Value>) -> bool {
    let Some(side) = side else { return false };
    let platform = side.get("platform").and_then(|v| v.as_str()).unwrap_or("");
    let format = side.get("format").and_then(|v| v.as_str()).unwrap_or("");
    let path = file_entry
        .and_then(|f| f.get("path"))
        .and_then(|v| v.as_str())
        .unwrap_or("");
    !platform.is_empty() && !format.is_empty() && !path.is_empty()
}

/// Target side is complete when format and path are present and non-empty.
/// Platform is always "snowflake" so it is not required in the document.
fn target_side_complete_with_path(side: Option<&Value>, file_entry: Option<&Value>) -> bool {
    let Some(side) = side else { return false };
    let format = side.get("format").and_then(|v| v.as_str()).unwrap_or("");
    let path = file_entry
        .and_then(|f| f.get("path"))
        .and_then(|v| v.as_str())
        .unwrap_or("");
    !format.is_empty() && !path.is_empty()
}

/// `custom` identity rule: at least one side must carry a `customKind` and
/// either a `name` or a path under `files.{source|converted}.path`.  The
/// engine never generates these, so we don't enforce a specific shape beyond
/// "we can say what the unit is and find it."
fn apply_custom_identity(value: &Value, filename: &str, issues: &mut Vec<ValidationIssue>) {
    let files = value.get("files");
    let source_complete =
        custom_side_complete(value.get("source"), files.and_then(|f| f.get("source")));
    let target_complete =
        custom_side_complete(value.get("target"), files.and_then(|f| f.get("converted")));

    if !source_complete && !target_complete {
        push_issue(
            issues,
            filename,
            "custom must have at least one complete side: \
             customKind + (name or files.{source|converted}.path)",
        );
    }
}

/// True when `customKind` is present and the side carries either a `name`
/// or a non-empty path on the matching `files` entry.
fn custom_side_complete(side: Option<&Value>, file_entry: Option<&Value>) -> bool {
    let Some(side) = side else { return false };
    let custom_kind = side
        .get("customKind")
        .and_then(|v| v.as_str())
        .unwrap_or("");
    if custom_kind.is_empty() {
        return false;
    }
    let has_name = side
        .get("name")
        .and_then(|v| v.as_str())
        .is_some_and(|s| !s.is_empty());
    let has_path = file_entry
        .and_then(|f| f.get("path"))
        .and_then(|v| v.as_str())
        .is_some_and(|s| !s.is_empty());
    has_name || has_path
}

// ── Entry points ─────────────────────────────────────────────────────────

/// Validate all code units in the registry.
pub(crate) fn validate_registry(
    registry_dir: &Path,
    checksum_mode: &ChecksumMode,
    root: &Path,
) -> Result<ValidationReport> {
    if !registry_dir.exists() {
        return Ok(ValidationReport::from_issues(0, vec![]));
    }

    let json_files = list_json_files(registry_dir)?;
    let mut issues = Vec::new();
    let mut seen_ids: HashSet<String> = HashSet::new();
    let mut parsed_units: Vec<(String, String, CodeUnit)> = Vec::new();

    for (path, filename) in &json_files {
        if let Some(unit) = validate_file(path, filename, checksum_mode, root, &mut issues) {
            let id = match &unit.id {
                Some(id) => id.clone(),
                None => {
                    issues.push(ValidationIssue::new(
                        filename,
                        ValidationIssueKind::MissingId,
                        "Code unit has no 'id' field",
                    ));
                    filename_stem(path).unwrap_or_default().to_string()
                }
            };
            if !seen_ids.insert(id.clone()) {
                issues.push(ValidationIssue::new(
                    filename,
                    ValidationIssueKind::DuplicateId,
                    format!("Duplicate ID '{id}'"),
                ));
            }
            parsed_units.push((id, filename.clone(), unit));
        }
    }

    check_referential_integrity(&parsed_units, &seen_ids, &mut issues);

    Ok(ValidationReport::from_issues(json_files.len(), issues))
}

/// Validate a single code unit file.
pub(crate) fn validate_single(
    path: &Path,
    checksum_mode: &ChecksumMode,
    root: &Path,
) -> Result<ValidationReport> {
    if !path.exists() {
        let id = filename_stem(path).unwrap_or_default();
        return CodeUnitNotFoundSnafu { id }.fail();
    }

    let filename = filename_of(path);
    let mut issues = Vec::new();

    validate_file(path, &filename, checksum_mode, root, &mut issues);

    Ok(ValidationReport::from_issues(1, issues))
}

// ── Tests ────────────────────────────────────────────────────────────────

#[cfg(test)]
mod kind_rules_tests {
    //! Behavioral tests for `validate_kind_rules`.  Both schema-driven
    //! constraints (`x-allowed-when`, `x-allowed-fields`) and the
    //! imperative cross-element helpers funnel through the same entry
    //! point, so every test here exercises the full per-kind pipeline.

    use super::*;
    use serde_json::{json, Value};
    use test_case::test_case;

    fn run(value: Value) -> Vec<String> {
        let mut issues = Vec::new();
        validate_kind_rules(&value, "fixture.json", &mut issues);
        issues
            .into_iter()
            .filter(|i| i.kind == ValidationIssueKind::PerKindStructure)
            .map(|i| i.message)
            .collect()
    }

    fn run_fixture(json_text: &str) -> Vec<String> {
        let value: Value = serde_json::from_str(json_text).expect("fixture is valid JSON");
        run(value)
    }

    fn assert_contains(messages: &[String], needles: &[&str]) {
        assert!(
            messages
                .iter()
                .any(|m| needles.iter().all(|n| m.contains(n))),
            "no message contains all of {:?}; got: {:?}",
            needles,
            messages,
        );
    }

    fn assert_clean(messages: &[String]) {
        assert!(
            messages.is_empty(),
            "expected no PerKindStructure issues, got: {:?}",
            messages,
        );
    }

    // ── Baselines: canonical examples must pass cleanly ─────────────────

    #[test_case(include_str!("../../examples/code-unit.example.json") ; "databaseObject example")]
    #[test_case(include_str!("../../examples/etl-code-unit.example.json") ; "etl example")]
    #[test_case(include_str!("../../examples/script-code-unit.example.json") ; "script example")]
    #[test_case(include_str!("../../examples/custom-code-unit.example.json") ; "custom example")]
    #[test_case(include_str!("../../tests/fixtures/kind-rules/parameterized_reference_clean.json") ; "parameterizedReference clean")]
    fn canonical_example_passes(fixture: &str) {
        assert_clean(&run_fixture(fixture));
    }

    // ── Schema-driven: x-allowed-when on root-level fields ──────────────

    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/etl_signature.json"),
        &["signature", "databaseObject"]
        ; "etl rejects signature"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/etl_root_cloud_status.json"),
        &["cloudStatus", "databaseObject"]
        ; "etl rejects root cloudStatus"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/sql_with_parts.json"),
        &["parts", "etl"]
        ; "databaseObject rejects parts"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/sql_with_stabilization.json"),
        &["codeStatus.stabilization", "etl"]
        ; "databaseObject rejects stabilization"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/etl_root_source_format.json"),
        &["source.format", "databaseObject", "script"]
        ; "etl rejects root source.format"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/parameterized_reference_with_files.json"),
        &["files"]
        ; "parameterizedReference rejects files"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/parameterized_reference_with_script_bindings.json"),
        &["scriptBindings"]
        ; "parameterizedReference rejects scriptBindings"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/parameterized_reference_with_script_metadata.json"),
        &["scriptMetadata"]
        ; "parameterizedReference rejects scriptMetadata"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/parameterized_reference_with_signature.json"),
        &["signature"]
        ; "parameterizedReference rejects signature"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/parameterized_reference_with_cloud_status.json"),
        &["cloudStatus"]
        ; "parameterizedReference rejects cloudStatus"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/parameterized_reference_with_planning.json"),
        &["planning"]
        ; "parameterizedReference rejects planning"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/parameterized_reference_with_issues.json"),
        &["issues"]
        ; "parameterizedReference rejects issues"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/parameterized_reference_with_code_status.json"),
        &["codeStatus"]
        ; "parameterizedReference rejects codeStatus"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/parameterized_reference_with_parts.json"),
        &["parts"]
        ; "parameterizedReference rejects parts"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/parameterized_reference_with_source_format.json"),
        &["source.format"]
        ; "parameterizedReference rejects source.format"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/parameterized_reference_with_target_format.json"),
        &["target.format"]
        ; "parameterizedReference rejects target.format"
    )]
    fn allowed_when_violation(fixture: &str, needles: &[&str]) {
        assert_contains(&run_fixture(fixture), needles);
    }

    // ── Schema-driven: x-allowed-when on nested arrays ──────────────────

    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/etl_part_model_name_on_non_dbt.json"),
        &["parts[0]", "target.modelName", "dbt"]
        ; "part target.modelName requires dbt format (sibling gate)"
    )]
    fn allowed_when_nested_violation(fixture: &str, needles: &[&str]) {
        assert_contains(&run_fixture(fixture), needles);
    }

    // ── Schema-driven: x-allowed-fields on parts[].cloudStatus ──────────

    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/etl_part_cloud_status_data_migration.json"),
        &["parts[0].cloudStatus.dataMigration"]
        ; "rejects part dataMigration"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/etl_part_cloud_status_data_validation.json"),
        &["parts[0].cloudStatus.dataValidation"]
        ; "rejects part dataValidation"
    )]
    fn allowed_fields_violation(fixture: &str, needles: &[&str]) {
        assert_contains(&run_fixture(fixture), needles);
    }

    // ── ETL root dependencies / issues are permitted ────────────────────

    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/etl_root_dependencies.json")
        ; "etl allows root dependsOn"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/etl_root_issues.json")
        ; "etl allows root issues"
    )]
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/etl_root_required_by.json")
        ; "etl tolerates root requiredBy written by refresh"
    )]
    fn etl_root_arrays_allowed(fixture: &str) {
        assert_clean(&run_fixture(fixture));
    }

    // ── Imperative: databaseObject identity ─────────────────────────────

    fn db_unit(source: Option<Value>, target: Option<Value>) -> Value {
        let mut unit = json!({ "kind": "databaseObject" });
        if let Some(s) = source {
            unit["source"] = s;
        }
        if let Some(t) = target {
            unit["target"] = t;
        }
        unit
    }

    fn ok_db_side() -> Value {
        json!({ "objectType": "table", "database": "DB", "schema": "dbo", "name": "Customers" })
    }

    #[test_case(Some(ok_db_side()), Some(ok_db_side()), &[] ; "both sides complete")]
    #[test_case(Some(ok_db_side()), None,                &[] ; "source-only is valid")]
    #[test_case(None,                Some(ok_db_side()), &[] ; "target-only is valid")]
    #[test_case(None, None, &["at least one"] ; "neither side present")]
    #[test_case(
        Some(json!({ "name": "Customers" })),
        Some(ok_db_side()),
        &["source.objectType"]
        ; "source missing objectType"
    )]
    #[test_case(
        Some(json!({ "objectType": "table" })),
        Some(ok_db_side()),
        &["source.name"]
        ; "source missing name"
    )]
    #[test_case(
        Some(ok_db_side()),
        Some(json!({ "name": "CUSTOMERS" })),
        &["target.objectType"]
        ; "target missing objectType"
    )]
    #[test_case(
        Some(ok_db_side()),
        Some(json!({ "objectType": "table" })),
        &["target.name"]
        ; "target missing name"
    )]
    fn db_object_identity(source: Option<Value>, target: Option<Value>, needles: &[&str]) {
        let messages = run(db_unit(source, target));
        if needles.is_empty() {
            assert_clean(&messages);
        } else {
            for needle in needles {
                assert!(
                    messages.iter().any(|m| m.contains(needle)),
                    "expected substring {:?} in messages: {:?}",
                    needle,
                    messages,
                );
            }
        }
    }

    // ── Script: identity (imperative D24) + completion gate (required-when) ──

    fn script_unit(value: Value) -> Value {
        let mut base = json!({ "kind": "script" });
        if let Value::Object(map) = value {
            for (k, v) in map {
                base[k] = v;
            }
        }
        base
    }

    #[test]
    fn script_with_complete_source_passes() {
        let unit = script_unit(json!({
            "source": { "platform": "teradata", "format": "bteq" },
            "files": { "source": { "path": "src/load.bteq" } },
        }));
        assert_clean(&run(unit));
    }

    #[test]
    fn script_with_complete_target_only_passes() {
        // Generated script — only the target side is populated.
        let unit = script_unit(json!({
            "target": { "format": "snowflakeScripting" },
            "files": { "converted": { "path": "out/load.sql" } },
        }));
        assert_clean(&run(unit));
    }

    #[test]
    fn script_with_neither_side_complete_is_rejected() {
        let unit = script_unit(json!({
            "source": { "platform": "teradata" },
            "files": { "source": { "path": "src/load.bteq" } },
        }));
        assert_contains(&run(unit), &["at least one complete side"]);
    }

    #[test]
    fn script_completed_conversion_requires_target_format() {
        let unit = script_unit(json!({
            "source": { "platform": "teradata", "format": "bteq" },
            "files": { "source": { "path": "src/load.bteq" } },
            "codeStatus": { "conversion": { "status": "completed" } },
        }));
        assert_contains(&run(unit), &["target.format", "completed"]);
    }

    #[test]
    fn script_with_completed_conversion_and_target_format_passes() {
        let unit = script_unit(json!({
            "source": { "platform": "teradata", "format": "bteq" },
            "target": { "format": "snowflakeScripting" },
            "files": {
                "source": { "path": "src/load.bteq" },
                "converted": { "path": "out/load.sql" },
            },
            "codeStatus": { "conversion": { "status": "completed" } },
        }));
        assert_clean(&run(unit));
    }

    // ── Custom: identity rule + exemption from field gates ──────────────

    fn custom_unit(value: Value) -> Value {
        let mut base = json!({ "kind": "custom" });
        if let Value::Object(map) = value {
            for (k, v) in map {
                base[k] = v;
            }
        }
        base
    }

    #[test]
    fn custom_with_source_kind_and_name_passes() {
        let unit = custom_unit(json!({
            "source": { "customKind": "powerBiReport", "name": "SalesDashboard" },
        }));
        assert_clean(&run(unit));
    }

    #[test]
    fn custom_with_source_kind_and_path_passes() {
        let unit = custom_unit(json!({
            "source": { "customKind": "ssasCube" },
            "files": { "source": { "path": "source/cubes/Sales.bim" } },
        }));
        assert_clean(&run(unit));
    }

    #[test]
    fn custom_with_target_only_passes() {
        let unit = custom_unit(json!({
            "target": { "customKind": "dbtModel", "name": "stg_orders" },
        }));
        assert_clean(&run(unit));
    }

    #[test]
    fn custom_without_custom_kind_is_rejected() {
        let unit = custom_unit(json!({
            "source": { "name": "orders_sync" },
        }));
        assert_contains(&run(unit), &["customKind"]);
    }

    #[test]
    fn custom_with_kind_but_no_name_or_path_is_rejected() {
        let unit = custom_unit(json!({
            "source": { "customKind": "fivetran" },
        }));
        assert_contains(&run(unit), &["customKind", "name"]);
    }

    #[test]
    fn custom_dependson_at_root_is_allowed() {
        let unit = custom_unit(json!({
            "source": { "customKind": "fivetran", "name": "orders_sync" },
            "dependencies": { "dependsOn": [{ "id": "abc-123" }] },
        }));
        assert_clean(&run(unit));
    }

    /// Every field that `x-allowed-when` gates to some other kind must still
    /// be accepted on a `custom` unit — that exemption is the whole point of
    /// the kind.  Add a case here whenever a new gate lands in the schema.
    #[test_case(json!({ "files": { "source": { "path": "reports/Sales.pbix" } } }) ; "files")]
    #[test_case(json!({ "codeStatus": { "conversion": { "status": "completed" } } }) ; "codeStatus")]
    #[test_case(json!({ "codeStatus": { "stabilization": { "status": "completed" } } }) ; "codeStatus.stabilization")]
    #[test_case(json!({ "cloudStatus": { "deployment": { "status": "completed" } } }) ; "cloudStatus")]
    #[test_case(json!({ "planning": { "wave": 1 } }) ; "planning")]
    #[test_case(json!({ "issues": [{ "code": "X", "severity": "warning" }] }) ; "issues")]
    #[test_case(json!({ "parts": [{ "id": "p1" }] }) ; "parts")]
    #[test_case(json!({ "signature": { "columns": [{ "name": "id", "type": "INT" }] } }) ; "signature")]
    #[test_case(json!({ "scriptMetadata": { "io": {} } }) ; "scriptMetadata")]
    #[test_case(json!({ "scriptBindings": { "bindings": [] } }) ; "scriptBindings")]
    #[test_case(json!({ "source": { "customKind": "powerBiReport", "name": "S", "format": "xml" } }) ; "source.format")]
    #[test_case(json!({ "target": { "customKind": "dbtModel", "name": "s", "format": "dbt" } }) ; "target.format")]
    fn custom_is_exempt_from_field_gates(extra: Value) {
        let mut unit = custom_unit(json!({
            "source": { "customKind": "powerBiReport", "name": "SalesDashboard" },
        }));
        if let Value::Object(map) = extra {
            for (k, v) in map {
                unit[k] = v;
            }
        }
        assert_clean(&run(unit));
    }

    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/db_object_with_custom_kind.json"),
        &["customKind", "custom"]
        ; "databaseObject rejects customKind"
    )]
    fn custom_kind_only_allowed_on_custom(fixture: &str, needles: &[&str]) {
        assert_contains(&run_fixture(fixture), needles);
    }

    /// Counterpart to the gate exemption at fixture level: `signature` is
    /// gated to `databaseObject`, and a `custom` unit carrying one is fine.
    #[test_case(
        include_str!("../../tests/fixtures/kind-rules/custom_with_signature.json")
        ; "custom keeps databaseObject-only fields"
    )]
    fn custom_accepts_gated_fields_from_other_kinds(fixture: &str) {
        assert_clean(&run_fixture(fixture));
    }
}
