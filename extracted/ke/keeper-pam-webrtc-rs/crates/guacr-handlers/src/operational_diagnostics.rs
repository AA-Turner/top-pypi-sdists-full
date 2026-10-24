//! Application-owned database diagnostic projection, before any owned capture.
//!
//! Driver payloads are not diagnostic data. Unknown fields (including Debug values)
//! are never formatted; every protected event still produces one diagnostic record.

use std::fmt;

use serde_json::{Map, Value};
use tracing::field::{Field, Visit};
use tracing::{Event, Metadata, Subscriber};
use tracing_subscriber::field::{RecordFields, VisitOutput};
use tracing_subscriber::fmt::format::{DefaultFields, Format, FormatEvent, FormatFields, Writer};
use tracing_subscriber::fmt::FmtContext;
use tracing_subscriber::registry::LookupSpan;

pub const TARGET: &str = "keeper_pam_diagnostics";

pub(crate) fn database_source(target: &str) -> Option<&'static str> {
    let root = target.split([':', '.']).next().unwrap_or(target);
    match root {
        "sqlx" => Some("sqlx"),
        "keeperdb" => Some("keeperdb"),
        "tiberius" => Some("tiberius"),
        "oracle" | "oracle_rs" => Some("oracle"),
        "guacr_database" => Some("guacr_database"),
        _ if root.starts_with("sqlx_") => Some("sqlx"),
        _ if root.starts_with("keeperdb_") || root.starts_with("keeperdb-") => Some("keeperdb"),
        _ => None,
    }
}

fn known_source(value: &str) -> Option<&'static str> {
    match value {
        "sqlx" => Some("sqlx"),
        "keeperdb" => Some("keeperdb"),
        "tiberius" => Some("tiberius"),
        "oracle" => Some("oracle"),
        "guacr_database" => Some("guacr_database"),
        "handler" => Some("handler"),
        _ => None,
    }
}

fn operation(value: &str) -> Option<&'static str> {
    match value {
        "query" => Some("query"),
        "connection" => Some("connection"),
        "authentication" => Some("authentication"),
        "pool" => Some("pool"),
        "cleanup" => Some("cleanup"),
        "lifecycle" => Some("lifecycle"),
        "recording" => Some("recording"),
        "diagnostic" => Some("diagnostic"),
        _ => None,
    }
}

fn outcome(value: &str) -> Option<&'static str> {
    match value {
        "success" => Some("success"),
        "failed" => Some("failed"),
        "started" => Some("started"),
        "finished" => Some("finished"),
        "cancelled" => Some("cancelled"),
        "timed_out" => Some("timed_out"),
        "session_lost" => Some("session_lost"),
        "slow" => Some("slow"),
        "observed" => Some("observed"),
        "requested" => Some("requested"),
        "rejected" => Some("rejected"),
        "confirmation_required" => Some("confirmation_required"),
        _ => None,
    }
}

fn numeric_field(name: &str) -> bool {
    matches!(
        name,
        "rows_returned"
            | "rows_affected"
            | "elapsed_secs"
            | "elapsed_ms"
            | "slow_threshold_ms"
            | "bind_count"
            | "error_code"
            | "errno"
            | "frames"
            | "bytes"
            | "schema_count"
            | "table_count"
            | "metadata_count"
            | "page"
            | "total_rows"
            | "max_connections_per_session"
            | "connection_grace_period_ms"
            | "max_queries"
            | "max_duration_secs"
            | "current_connections"
            | "max_connections"
    )
}

fn code(value: &str) -> bool {
    let bytes = value.as_bytes();
    (!bytes.is_empty() && bytes.len() <= 10 && bytes.iter().all(u8::is_ascii_digit))
        || (bytes.len() == 5
            && bytes
                .iter()
                .all(|c| c.is_ascii_uppercase() || c.is_ascii_digit()))
        || (((bytes.len() == 9 && value.starts_with("ORA-"))
            || (bytes.len() == 8 && value.starts_with("DPI-")))
            && bytes[4..].iter().all(u8::is_ascii_digit))
}

fn envelope_code(value: &str) -> Option<&str> {
    if let Some(rest) = value.strip_prefix("error returned from database: (code: ") {
        let (candidate, suffix) = rest.split_once(')')?;
        return (code(candidate) && (suffix.is_empty() || suffix.starts_with(':')))
            .then_some(candidate);
    }
    let value = value.strip_prefix("Oracle error: ").unwrap_or(value);
    let width = if value.starts_with("ORA-") {
        9
    } else if value.starts_with("DPI-") {
        8
    } else {
        return None;
    };
    let candidate = value.get(..width)?;
    (code(candidate) && (value.len() == width || value[width..].starts_with(':')))
        .then_some(candidate)
}

struct Diagnostic {
    fields: Map<String, Value>,
}

impl Diagnostic {
    fn new(source: &'static str, metadata: Option<&Metadata<'_>>, content_omitted: bool) -> Self {
        let mut fields = Map::new();
        fields.insert("event".into(), Value::from("database_diagnostic"));
        fields.insert("source".into(), Value::from(source));
        fields.insert("operation".into(), Value::from("diagnostic"));
        fields.insert("outcome".into(), Value::from("observed"));
        fields.insert("details_omitted".into(), Value::from(true));
        if content_omitted {
            fields.insert("content_omitted".into(), Value::from(true));
        }
        if let Some(metadata) = metadata {
            if *metadata.level() == tracing::Level::ERROR {
                fields.insert("outcome".into(), Value::from("failed"));
            }
            // The target and field declaration, not the statement/message, identify SQLx queries.
            if source == "sqlx" && metadata.target() == "sqlx::query" {
                fields.insert("operation".into(), Value::from("query"));
                if metadata.fields().field("slow_threshold").is_some() {
                    fields.insert("outcome".into(), Value::from("slow"));
                }
            }
        }
        Self { fields }
    }

    fn insert_number(&mut self, name: &str, value: Value) {
        if numeric_field(name)
            && value.is_number()
            && (!matches!(name, "error_code" | "errno") || value.is_u64() || value.is_i64())
        {
            self.fields.insert(name.into(), value);
        }
    }

    fn insert_str(&mut self, name: &str, value: &str) {
        let validated = match name {
            "operation" => operation(value),
            "outcome" => outcome(value),
            "error_code" if code(value) => Some(value),
            _ => None,
        };
        if let Some(value) = validated {
            self.fields.insert(name.into(), Value::from(value));
        }
    }

    fn json(self) -> String {
        // Only JSON primitives admitted above reach the serializer.
        Value::Object(self.fields).to_string()
    }
}

impl Visit for Diagnostic {
    fn record_u64(&mut self, field: &Field, value: u64) {
        self.insert_number(field.name(), Value::from(value));
    }

    fn record_i64(&mut self, field: &Field, value: i64) {
        self.insert_number(field.name(), Value::from(value));
    }

    fn record_f64(&mut self, field: &Field, value: f64) {
        if let Some(value) = serde_json::Number::from_f64(value) {
            self.insert_number(field.name(), Value::Number(value));
        }
    }

    fn record_bool(&mut self, _: &Field, _: bool) {}

    fn record_str(&mut self, field: &Field, value: &str) {
        if field.name() == "error" && field.callsite().0.metadata().target() != TARGET {
            if let Some(error_code) = envelope_code(value) {
                self.fields
                    .entry("error_code")
                    .or_insert_with(|| Value::from(error_code));
            }
        } else {
            self.insert_str(field.name(), value);
        }
    }

    fn record_debug(&mut self, _: &Field, _: &dyn fmt::Debug) {
        // Deliberately do not format Debug, even for an otherwise allowlisted key.
    }
}

pub fn project_event(event: &Event<'_>) -> Option<String> {
    use tracing_log::NormalizeEvent;
    let normalized = event.normalized_metadata();
    let metadata = normalized.as_ref().unwrap_or_else(|| event.metadata());
    let handler_failure = matches!(
        metadata.target(),
        HANDLER_TARGET
            | "guacr_handlers::error"
            | "guacr_handlers::integration"
            | "guacr_guacd::server"
            | "guacrd"
    ) && matches!(
        *metadata.level(),
        tracing::Level::ERROR | tracing::Level::WARN
    );
    let source = database_source(metadata.target())
        .or_else(|| (metadata.target() == TARGET).then_some("guacr_database"))
        .or_else(|| handler_failure.then_some("handler"))?;
    let mut diagnostic = Diagnostic::new(source, Some(metadata), false);
    if handler_failure {
        diagnostic.insert_str("operation", "lifecycle");
        diagnostic.insert_str("outcome", "failed");
    }
    event.record(&mut diagnostic);
    Some(diagnostic.json())
}

const HANDLER_TARGET: &str = "keeper_pam_webrtc_rs::channel::handler_connections";

/// Legacy arguments cannot expose independently typed fields. Only a literal
/// message may supply one of the fixed classes; never format arbitrary arguments.
pub fn project_record(record: &log::Record<'_>) -> Option<String> {
    let handler_class = (matches!(
        record.target(),
        HANDLER_TARGET
            | "guacr_handlers::error"
            | "guacr_handlers::integration"
            | "guacr_guacd::server"
            | "guacrd"
    ) && record.level() <= log::Level::Warn)
        .then_some(("lifecycle", "failed"));
    let source = database_source(record.target())
        .or_else(|| (record.target() == TARGET).then_some("guacr_database"))
        .or_else(|| handler_class.map(|_| "handler"))?;
    let mut diagnostic = Diagnostic::new(source, None, true);
    if record.level() == log::Level::Error {
        diagnostic.insert_str("outcome", "failed");
    }
    if let Some((operation, outcome)) = handler_class {
        diagnostic.insert_str("operation", operation);
        diagnostic.insert_str("outcome", outcome);
    }
    if let Some(literal) = record.args().as_str() {
        if record.target() == TARGET {
            revalidate_json(&mut diagnostic, literal);
        } else {
            let class = match literal {
                "Database recording failed" => Some(("recording", "failed")),
                "SQL workspace action=DisconnectCleanup outcome=input_required" => {
                    Some(("cleanup", "observed"))
                }
                "DynamoDB: Sent display init instructions"
                | "Elasticsearch: Sent display init instructions" => Some(("lifecycle", "started")),
                "DynamoDB: Initial screen sent successfully"
                | "Elasticsearch: Initial screen sent successfully" => {
                    Some(("lifecycle", "success"))
                }
                "Elasticsearch: JSON input parsing failed; using SQL execution" => {
                    Some(("query", "observed"))
                }
                _ => None,
            };
            if let Some((operation, outcome)) = class {
                diagnostic.insert_str("operation", operation);
                diagnostic.insert_str("outcome", outcome);
            }
        }
    }
    if source == "guacr_database" && record.target().ends_with("::recording") {
        diagnostic.insert_str("operation", "recording");
    }
    Some(diagnostic.json())
}

fn revalidate_json(diagnostic: &mut Diagnostic, text: &str) {
    let Ok(Value::Object(fields)) = serde_json::from_str::<Value>(text) else {
        return;
    };
    if let Some(source) = fields
        .get("source")
        .and_then(Value::as_str)
        .and_then(known_source)
    {
        diagnostic
            .fields
            .insert("source".into(), Value::from(source));
    }
    for (name, value) in fields {
        match value {
            Value::String(value) => diagnostic.insert_str(&name, &value),
            Value::Number(value)
                if value.is_u64()
                    || value.is_i64()
                    || value.as_f64().is_some_and(f64::is_finite) =>
            {
                diagnostic.insert_number(&name, Value::Number(value));
            }
            _ => (),
        }
    }
}

/// Standalone formatting also protects database span fields: the default compact
/// formatter can append parent spans to unrelated events.
pub struct SafeFields;

struct SafeFieldVisitor<'a> {
    default: tracing_subscriber::fmt::format::DefaultVisitor<'a>,
    diagnostic: Option<Diagnostic>,
}

impl SafeFieldVisitor<'_> {
    fn diagnostic(&mut self, field: &Field) -> Option<&mut Diagnostic> {
        // RecordFields has no metadata accessor. The field's static callsite is
        // the same trusted declaration used by Event::metadata and Span::metadata.
        let metadata = field.callsite().0.metadata();
        let source = database_source(metadata.target())
            .or_else(|| (metadata.target() == TARGET).then_some("guacr_database"))
            .or_else(|| {
                (metadata.target() == HANDLER_TARGET && *metadata.level() == tracing::Level::ERROR)
                    .then_some("handler")
            });
        if let Some(source) = source {
            self.diagnostic
                .get_or_insert_with(|| Diagnostic::new(source, Some(metadata), false));
            self.diagnostic.as_mut()
        } else {
            None
        }
    }
}

impl Visit for SafeFieldVisitor<'_> {
    fn record_u64(&mut self, field: &Field, value: u64) {
        if let Some(diagnostic) = self.diagnostic(field) {
            diagnostic.record_u64(field, value);
        } else {
            self.default.record_u64(field, value);
        }
    }
    fn record_i64(&mut self, field: &Field, value: i64) {
        if let Some(diagnostic) = self.diagnostic(field) {
            diagnostic.record_i64(field, value);
        } else {
            self.default.record_i64(field, value);
        }
    }
    fn record_f64(&mut self, field: &Field, value: f64) {
        if let Some(diagnostic) = self.diagnostic(field) {
            diagnostic.record_f64(field, value);
        } else {
            self.default.record_f64(field, value);
        }
    }
    fn record_bool(&mut self, field: &Field, value: bool) {
        if let Some(diagnostic) = self.diagnostic(field) {
            diagnostic.record_bool(field, value);
        } else {
            self.default.record_bool(field, value);
        }
    }
    fn record_str(&mut self, field: &Field, value: &str) {
        if let Some(diagnostic) = self.diagnostic(field) {
            diagnostic.record_str(field, value);
        } else {
            self.default.record_str(field, value);
        }
    }
    fn record_error(&mut self, field: &Field, value: &(dyn std::error::Error + 'static)) {
        if self.diagnostic(field).is_none() {
            self.default.record_error(field, value);
        }
    }
    fn record_bytes(&mut self, field: &Field, value: &[u8]) {
        if self.diagnostic(field).is_none() {
            self.default.record_bytes(field, value);
        }
    }
    fn record_i128(&mut self, field: &Field, value: i128) {
        if self.diagnostic(field).is_none() {
            self.default.record_i128(field, value);
        }
    }
    fn record_u128(&mut self, field: &Field, value: u128) {
        if self.diagnostic(field).is_none() {
            self.default.record_u128(field, value);
        }
    }
    fn record_debug(&mut self, field: &Field, value: &dyn fmt::Debug) {
        if self.diagnostic(field).is_none() {
            self.default.record_debug(field, value);
        }
    }
}

impl<'writer> FormatFields<'writer> for SafeFields {
    fn format_fields<R: RecordFields>(
        &self,
        mut writer: Writer<'writer>,
        fields: R,
    ) -> fmt::Result {
        use tracing_subscriber::field::MakeVisitor;
        let mut visitor = SafeFieldVisitor {
            default: DefaultFields::new().make_visitor(writer.by_ref()),
            diagnostic: None,
        };
        fields.record(&mut visitor);
        let diagnostic = visitor.diagnostic.take();
        visitor.default.finish()?;
        if let Some(diagnostic) = diagnostic {
            write!(writer, "{}", diagnostic.json())?;
        }
        Ok(())
    }
}

pub struct SafeEventFormat(pub Format<tracing_subscriber::fmt::format::Compact>);

impl<S, N> FormatEvent<S, N> for SafeEventFormat
where
    S: Subscriber + for<'a> LookupSpan<'a>,
    N: for<'a> FormatFields<'a> + 'static,
{
    fn format_event(
        &self,
        ctx: &FmtContext<'_, S, N>,
        mut writer: Writer<'_>,
        event: &Event<'_>,
    ) -> fmt::Result {
        if let Some(message) = project_event(event) {
            // Do not append span names or their fields to a protected event.
            writeln!(
                writer,
                "{} {}: {}",
                event.metadata().level(),
                TARGET,
                message
            )
        } else {
            self.0.format_event(ctx, writer, event)
        }
    }
}
