// Threat detection helpers for database handlers.
//
// All public items in this module are gated behind #[cfg(feature = "threat-detection")].
// Handlers that call into this module must also gate their call sites.

#[cfg(feature = "threat-detection")]
use guacr_threat_detection::{ThreatDetector, ThreatDetectorConfig, ThreatResult};
#[cfg(feature = "threat-detection")]
use std::collections::HashMap;
#[cfg(feature = "threat-detection")]
use std::sync::Arc;

/// Map a database handler's db_type string to the protocol string the
/// threat detector expects.
#[cfg(feature = "threat-detection")]
fn db_type_to_protocol(db_type: &str) -> &'static str {
    match db_type {
        "mysql" | "mariadb" => "mysql",
        "postgresql" => "postgres",
        "sqlserver" => "sql-server",
        "mongodb" => "mongodb",
        "redis" => "redis",
        "cassandra" => "cassandra",
        "elasticsearch" => "elasticsearch",
        "dynamodb" => "dynamodb",
        "oracle" => "oracle",
        _ => "mysql",
    }
}

/// Build a ThreatDetectorConfig from connection params.
///
/// Recognized connection params:
///   threat_detection_enabled        "true" / "false"  (default: false)
///   threat_detection_baml_endpoint  URL of the BAML service
///   threat_detection_baml_api_key   Bearer token (optional)
///   threat_detection_auto_terminate "true" / "false"  (default: true)
#[cfg(feature = "threat-detection")]
pub fn threat_config_from_params(params: &HashMap<String, String>) -> ThreatDetectorConfig {
    let enabled = params
        .get("threat_detection_enabled")
        .map(|s| s == "true")
        .unwrap_or(false);
    let baml_endpoint = params
        .get("threat_detection_baml_endpoint")
        .cloned()
        .unwrap_or_default();
    let baml_api_key = params.get("threat_detection_baml_api_key").cloned();
    let auto_terminate = params
        .get("threat_detection_auto_terminate")
        .map(|s| s != "false")
        .unwrap_or(true);

    ThreatDetectorConfig {
        enabled,
        baml_endpoint,
        baml_api_key,
        auto_terminate,
        ..Default::default()
    }
}

/// Analyze a query for threats.
///
/// Returns `Some(result)` on success. Returns `None` on error — the detector is
/// fail-open, so a network or API failure does not block query execution.
#[cfg(feature = "threat-detection")]
pub async fn analyze_query(
    detector: &Arc<ThreatDetector>,
    session_id: &str,
    query: &str,
    username: &str,
    hostname: &str,
    db_type: &str,
) -> Option<ThreatResult> {
    let protocol = db_type_to_protocol(db_type);
    match detector
        .analyze_keystroke_sequence(session_id, query, username, hostname, protocol)
        .await
    {
        Ok(result) => Some(result),
        Err(e) => {
            log::warn!("Threat detection error (fail-open): {}", e);
            None
        }
    }
}

/// Generate a unique session ID for a new database connection.
#[cfg(feature = "threat-detection")]
pub fn new_session_id() -> String {
    uuid::Uuid::new_v4().to_string()
}
