use parking_lot::Mutex;
use std::fmt;
use std::sync::Arc;

use serde_json::Value;
use tracing::{Event, Subscriber};
use tracing_subscriber::layer::{Context, SubscriberExt};
use tracing_subscriber::Layer;

use crate::operational_diagnostics::{project_event, project_record, SafeEventFormat, SafeFields};

const SECRET: &str = "SELECT 'private-credential-37' /* private-comment-91 */ FROM secret_table";

struct MustNotFormat;
impl fmt::Debug for MustNotFormat {
    fn fmt(&self, _: &mut fmt::Formatter<'_>) -> fmt::Result {
        panic!("database Debug payload must never be formatted")
    }
}

struct Capture(Arc<Mutex<Vec<String>>>);
impl<S: Subscriber> Layer<S> for Capture {
    fn on_event(&self, event: &Event<'_>, _: Context<'_, S>) {
        self.0.lock().push(project_event(event).unwrap());
    }
}

#[test]
fn typed_query_projection_keeps_timing_without_statement_or_debug() {
    let output = Arc::new(Mutex::new(Vec::new()));
    let subscriber = tracing_subscriber::registry().with(Capture(output.clone()));
    tracing::subscriber::with_default(subscriber, || {
        tracing::event!(target: "sqlx::query", tracing::Level::WARN,
            summary = SECRET, db.statement = SECRET, params = SECRET,
            rows_returned = 3_u64, rows_affected = 2_i64,
            elapsed_secs = 0.125_f64, slow_threshold = ?MustNotFormat,
            unknown = ?MustNotFormat, error = SECRET);
    });
    let output = output.lock();
    assert_eq!(output.len(), 1);
    assert!(!output[0].contains("private"));
    assert!(!output[0].contains("secret_table"));
    let diagnostic: Value = serde_json::from_str(&output[0]).unwrap();
    assert_eq!(diagnostic["source"], "sqlx");
    assert_eq!(diagnostic["operation"], "query");
    assert_eq!(diagnostic["outcome"], "slow");
    assert_eq!(diagnostic["rows_returned"], 3);
    assert_eq!(diagnostic["rows_affected"], 2);
    assert_eq!(diagnostic["elapsed_secs"], 0.125);
    assert!(diagnostic.get("summary").is_none());
    assert!(diagnostic.get("slow_threshold").is_none());
}

#[test]
fn typed_failure_projection_preserves_code_and_rejects_unknown_types() {
    let output = Arc::new(Mutex::new(Vec::new()));
    let subscriber = tracing_subscriber::registry().with(Capture(output.clone()));
    tracing::subscriber::with_default(subscriber, || {
        tracing::error!(target: "guacr_database::diagnostics",
            operation = "query", outcome = "failed", error_code = "42601",
            elapsed_ms = 12_u64, rows_affected = ?MustNotFormat,
            error_class = SECRET, error = SECRET);
        tracing::error!(target: "oracle::connection", operation = SECRET,
            outcome = SECRET, error_code = "ORA-00942", elapsed_secs = f64::NAN,
            bytes = SECRET, errno = ?MustNotFormat);
        tracing::error!(target: "keeperdb_core::diagnostic", error_code = SECRET,
            rows_returned = "999", elapsed_ms = f64::INFINITY);
        tracing::error!(target: "sqlx::connection",
            error = "error returned from database: (code: 18456): SELECT 'private-credential-37'");
        tracing::error!(target: "oracle::connection",
            error = "Oracle error: ORA-00942: SELECT 'private-credential-37'");
        tracing::error!(target: "sqlx::connection",
            error = "SELECT 'error returned from database: (code: 18456)' private-credential-37");
    });
    let output = output.lock();
    assert_eq!(output.len(), 6);
    let first: Value = serde_json::from_str(&output[0]).unwrap();
    assert_eq!(first["operation"], "query");
    assert_eq!(first["outcome"], "failed");
    assert_eq!(first["error_code"], "42601");
    assert_eq!(first["elapsed_ms"], 12);
    assert!(first.get("rows_affected").is_none());
    let second: Value = serde_json::from_str(&output[1]).unwrap();
    assert_eq!(second["operation"], "diagnostic");
    assert_eq!(second["outcome"], "failed");
    assert_eq!(second["error_code"], "ORA-00942");
    assert!(second.get("elapsed_secs").is_none());
    assert!(second.get("bytes").is_none());
    let third: Value = serde_json::from_str(&output[2]).unwrap();
    assert!(third.get("error_code").is_none());
    assert!(third.get("rows_returned").is_none());
    assert!(third.get("elapsed_ms").is_none());
    let sqlx: Value = serde_json::from_str(&output[3]).unwrap();
    assert_eq!(sqlx["error_code"], "18456");
    let oracle: Value = serde_json::from_str(&output[4]).unwrap();
    assert_eq!(oracle["error_code"], "ORA-00942");
    let arbitrary: Value = serde_json::from_str(&output[5]).unwrap();
    assert!(arbitrary.get("error_code").is_none());
    assert!(output.iter().all(|line| !line.contains("private")));
}

#[test]
fn legacy_records_are_projected_without_formatting_payload() {
    let projected = project_record(
        &log::Record::builder()
            .target("tiberius::tds")
            .level(log::Level::Error)
            .args(format_args!("{:?}", MustNotFormat))
            .build(),
    )
    .unwrap();
    let diagnostic: Value = serde_json::from_str(&projected).unwrap();
    assert_eq!(diagnostic["source"], "tiberius");
    assert_eq!(diagnostic["content_omitted"], true);
    assert_eq!(diagnostic["operation"], "diagnostic");
    let projected = project_record(
        &log::Record::builder()
            .target("keeper_pam_webrtc_rs::channel::handler_connections")
            .level(log::Level::Error)
            .args(format_args!("Handler error: {:?}", MustNotFormat))
            .build(),
    )
    .unwrap();
    let diagnostic: Value = serde_json::from_str(&projected).unwrap();
    assert_eq!(diagnostic["source"], "handler");
    assert_eq!(diagnostic["operation"], "lifecycle");
    assert_eq!(diagnostic["outcome"], "failed");
    assert!(project_record(
        &log::Record::builder()
            .target("unrelated")
            .args(format_args!("operational startup"))
            .build()
    )
    .is_none());
}

#[test]
fn claimed_safe_json_is_reconstructed_not_trusted() {
    let projected = project_record(&log::Record::builder()
        .target("keeper_pam_diagnostics")
        .args(format_args!(r#"{{"source":"sqlx","operation":"query","outcome":"failed","details_omitted":false,"error_code":"42601","elapsed_ms":12,"sql":"SELECT 'private-credential-37'","rows_returned":"private"}}"#))
        .build()).unwrap();
    let diagnostic: Value = serde_json::from_str(&projected).unwrap();
    assert_eq!(diagnostic["source"], "sqlx");
    assert_eq!(diagnostic["outcome"], "failed");
    assert_eq!(diagnostic["error_code"], "42601");
    assert_eq!(diagnostic["elapsed_ms"], 12);
    assert_eq!(diagnostic["details_omitted"], true);
    assert!(diagnostic.get("sql").is_none());
    assert!(diagnostic.get("rows_returned").is_none());
    assert!(!projected.contains("private"));
}

#[derive(Clone)]
struct Buffer(Arc<Mutex<Vec<u8>>>);
impl std::io::Write for Buffer {
    fn write(&mut self, bytes: &[u8]) -> std::io::Result<usize> {
        self.0.lock().extend_from_slice(bytes);
        Ok(bytes.len())
    }
    fn flush(&mut self) -> std::io::Result<()> {
        Ok(())
    }
}

#[test]
fn standalone_output_protects_database_events_and_parent_span_fields() {
    let bytes = Arc::new(Mutex::new(Vec::new()));
    let buffer = Buffer(bytes.clone());
    let subscriber = tracing_subscriber::fmt()
        .with_max_level(tracing::Level::TRACE)
        .fmt_fields(SafeFields)
        .event_format(SafeEventFormat(
            tracing_subscriber::fmt::format()
                .compact()
                .with_ansi(false)
                .with_target(true)
                .with_level(true),
        ))
        .with_writer(move || buffer.clone())
        .finish();
    tracing::subscriber::with_default(subscriber, || {
        let span = tracing::info_span!(target: "sqlx::connection", "database_connection",
            db.statement = SECRET, driver_payload = ?MustNotFormat);
        let _entered = span.enter();
        tracing::event!(target: "sqlx::query", tracing::Level::ERROR, db.statement = SECRET,
            rows_returned = 0_u64, elapsed_secs = 0.025_f64, error = ?MustNotFormat);
        tracing_log::format_trace(
            &log::Record::builder()
                .target("sqlx::query")
                .level(log::Level::Debug)
                .args(format_args!("{:?}", MustNotFormat))
                .build(),
        )
        .unwrap();
        tracing::info!(target: "application", "operational startup");
    });
    let output = String::from_utf8(bytes.lock().clone()).unwrap();
    assert!(!output.contains("private"));
    assert!(!output.contains("secret_table"));
    assert!(output.contains("database_diagnostic"));
    assert!(output.contains("elapsed_secs"));
    assert!(output.contains("operational startup"));
}

#[test]
fn native_and_proxy_metadata_survive_without_authentication_payload() {
    let output = Arc::new(Mutex::new(Vec::new()));
    let subscriber = tracing_subscriber::registry().with(Capture(output.clone()));
    tracing::subscriber::with_default(subscriber, || {
        tracing::warn!(target: "keeperdb_proxy", operation = "authentication", outcome = "failed",
            error_code = 18456_u64, current_connections = 3_u64, max_connections = 3_u64,
            max_connections_per_session = 3_u64, connection_grace_period_ms = 1000_u64,
            max_queries = 20_u64, max_duration_secs = 60_u64, credentials = ?MustNotFormat);
        tracing::info!(target: "guacr_database::diagnostics", operation = "cleanup", outcome = "requested",
            schema_count = 2_u64, table_count = 4_u64, metadata_count = 7_u64, page = 2_u64,
            total_rows = 99_u64, sql = SECRET);
        tracing::error!(target: "oracle_rs::connection", error_code = "DPI-1080", sql = ?MustNotFormat);
    });
    let captured = output.lock();
    let proxy: Value = serde_json::from_str(&captured[0]).unwrap();
    assert_eq!(proxy["error_code"], 18456);
    assert_eq!(proxy["max_connections_per_session"], 3);
    assert_eq!(proxy["connection_grace_period_ms"], 1000);
    assert_eq!(proxy["max_queries"], 20);
    assert_eq!(proxy["max_duration_secs"], 60);
    assert_eq!(proxy["current_connections"], 3);
    assert_eq!(proxy["outcome"], "failed");
    let workspace: Value = serde_json::from_str(&captured[1]).unwrap();
    assert_eq!(workspace["outcome"], "requested");
    assert_eq!(workspace["schema_count"], 2);
    assert_eq!(workspace["table_count"], 4);
    assert_eq!(workspace["metadata_count"], 7);
    assert_eq!(workspace["page"], 2);
    assert_eq!(workspace["total_rows"], 99);
    let native: Value = serde_json::from_str(&captured[2]).unwrap();
    assert_eq!(native["source"], "oracle");
    assert_eq!(native["error_code"], "DPI-1080");
    assert_eq!(native["outcome"], "failed");
    assert!(captured
        .iter()
        .all(|line| !line.contains("private") && !line.contains("secret_table")));
}
