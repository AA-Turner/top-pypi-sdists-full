// Shared connection parameter extraction used across all protocol handlers.
//
// These functions replace ad-hoc parameter parsing that was duplicated across
// SSH, Telnet, VNC, RDP, SFTP, TN3270, and TN5250.

use std::collections::HashMap;

use crate::error::HandlerError;

// ---------------------------------------------------------------------------
// ConnectionParameters
// ---------------------------------------------------------------------------

/// Hostname, port, and optional credentials extracted from Guacamole connection
/// parameters.
///
/// Follows the same `from_params` pattern as `HandlerSecuritySettings`.
/// Individual handlers validate which fields are required after construction.
pub struct ConnectionParameters {
    pub hostname: String,
    pub port: u16,
    pub username: Option<String>,
    pub password: Option<String>,
}

impl ConnectionParameters {
    /// Extract connection parameters from the Guacamole parameter map.
    ///
    /// `default_port` is used when the `"port"` key is absent or unparseable.
    /// `hostname` is always required; its absence returns
    /// `HandlerError::MissingParameter`.
    pub fn from_params(
        params: &HashMap<String, String>,
        default_port: u16,
    ) -> Result<Self, HandlerError> {
        let hostname = params
            .get("hostname")
            .ok_or_else(|| HandlerError::MissingParameter("hostname".to_string()))?
            .clone();

        let port: u16 = params
            .get("port")
            .and_then(|p| p.parse().ok())
            .unwrap_or(default_port);

        let username = params.get("username").cloned();
        let password = params.get("password").cloned();

        Ok(Self {
            hostname,
            port,
            username,
            password,
        })
    }
}

// ---------------------------------------------------------------------------
// parse_image_formats
// ---------------------------------------------------------------------------

/// Parse the Guacamole `"image"` parameter and return which formats the client
/// supports.
///
/// Returns `(supports_webp, supports_jpeg)`. Logs with `log_prefix` so callers
/// can identify the protocol in the log stream (e.g. `"VNC"`, `"RDP"`).
pub fn parse_image_formats(params: &HashMap<String, String>, log_prefix: &str) -> (bool, bool) {
    let supported_formats = params
        .get("image")
        .map(|s| s.split(',').map(|f| f.trim()).collect::<Vec<_>>())
        .unwrap_or_else(|| vec!["image/png"]);

    let supports_webp = supported_formats.iter().any(|f| f.contains("webp"));
    let supports_jpeg = supported_formats.iter().any(|f| f.contains("jpeg"));

    log::info!(
        "{}: Client image support - WebP: {}, JPEG: {}, formats: {:?}",
        log_prefix,
        supports_webp,
        supports_jpeg,
        supported_formats
    );

    (supports_webp, supports_jpeg)
}

// ---------------------------------------------------------------------------
// parse_sftp_config
// ---------------------------------------------------------------------------

/// Parsed SFTP connection fields: `(enable, hostname, username, password,
/// private_key, private_key_passphrase, port)`.
pub type SftpConfig = (
    bool,
    Option<String>,
    Option<String>,
    Option<String>,
    Option<String>,
    Option<String>,
    u16,
);

/// Parse SFTP connection settings from Guacamole connection parameters.
///
/// Returns `(enable_sftp, hostname, username, password, private_key,
/// private_key_passphrase, port)`.
///
/// When `enable_sftp` is `false` all `Option` fields are `None` and `port` is
/// `22`. When `enable_sftp` is `true`, `hostname` and `username` are required
/// and their absence returns `HandlerError::MissingParameter`.
///
/// Accepts both camelCase (`sftphostname`) and snake_case (`sftp_hostname`)
/// parameter names for compatibility with different Guacamole client versions.
pub fn parse_sftp_config(params: &HashMap<String, String>) -> Result<SftpConfig, HandlerError> {
    let enable_sftp = params
        .get("enableSftp")
        .or_else(|| params.get("enable_sftp"))
        .map(|v| v == "true")
        .unwrap_or(false);

    if !enable_sftp {
        return Ok((false, None, None, None, None, None, 22));
    }

    let hostname = params
        .get("sftphostname")
        .or_else(|| params.get("sftp_hostname"))
        .ok_or_else(|| HandlerError::MissingParameter("sftphostname".to_string()))?
        .clone();

    let username = params
        .get("sftpusername")
        .or_else(|| params.get("sftp_username"))
        .ok_or_else(|| HandlerError::MissingParameter("sftpusername".to_string()))?
        .clone();

    let password = params
        .get("sftppassword")
        .or_else(|| params.get("sftp_password"))
        .cloned();

    let private_key = params
        .get("sftpprivatekey")
        .or_else(|| params.get("sftp_private_key"))
        .cloned();

    let passphrase = params
        .get("sftppassphrase")
        .or_else(|| params.get("sftp_private_key_passphrase"))
        .cloned();

    let port: u16 = params
        .get("sftpport")
        .or_else(|| params.get("sftp_port"))
        .and_then(|p| p.parse().ok())
        .unwrap_or(22);

    Ok((
        true,
        Some(hostname),
        Some(username),
        password,
        private_key,
        passphrase,
        port,
    ))
}

// ---------------------------------------------------------------------------
// Threat detection risk levels
// ---------------------------------------------------------------------------

/// Parsed form of one risk level entry from the vault record.
pub struct RiskLevelTags {
    pub deny: Vec<String>,
    pub allow: Vec<String>,
}

/// Parse `threat_detection_risk_levels` from connection params.
///
/// The Python gateway serialises the vault record's `resource_ai_risk_levels`
/// field as a JSON string with this shape:
/// ```json
/// {
///   "critical": { "tags": { "deny": [{"tag": "pattern"}], "allow": [...] }, ... },
///   "high":     { ... }
/// }
/// ```
///
/// Returns `(deny_tags, allow_tags)` where each map is
/// `level -> vec![regex_patterns]`. Returns empty maps when the param is
/// absent or cannot be parsed (non-fatal — threat detection simply runs
/// without tag filtering).
pub fn parse_threat_detection_risk_levels(
    params: &HashMap<String, String>,
) -> (HashMap<String, Vec<String>>, HashMap<String, Vec<String>>) {
    let json_str = match params.get("threat_detection_risk_levels") {
        Some(s) if !s.is_empty() => s,
        _ => return (HashMap::new(), HashMap::new()),
    };

    let parsed: serde_json::Value = match serde_json::from_str(json_str) {
        Ok(v) => v,
        Err(e) => {
            log::warn!("threat_detection_risk_levels: JSON parse error: {}", e);
            return (HashMap::new(), HashMap::new());
        }
    };

    let mut deny_tags: HashMap<String, Vec<String>> = HashMap::new();
    let mut allow_tags: HashMap<String, Vec<String>> = HashMap::new();

    if let serde_json::Value::Object(levels) = parsed {
        for (level, entry) in levels {
            let tags = &entry["tags"];
            let extract = |key: &str| -> Vec<String> {
                tags[key]
                    .as_array()
                    .map(|arr| {
                        arr.iter()
                            .filter_map(|item| item["tag"].as_str().map(String::from))
                            .collect()
                    })
                    .unwrap_or_default()
            };
            let deny = extract("deny");
            let allow = extract("allow");
            if !deny.is_empty() {
                deny_tags.insert(level.clone(), deny);
            }
            if !allow.is_empty() {
                allow_tags.insert(level.clone(), allow);
            }
        }
    }

    (deny_tags, allow_tags)
}
