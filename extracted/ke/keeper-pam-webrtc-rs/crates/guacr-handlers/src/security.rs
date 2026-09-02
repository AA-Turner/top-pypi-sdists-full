// Shared security settings for all protocol handlers
//
// Implements security features that must be consistent across SSH, Telnet, RDP, VNC,
// Database, SFTP, and RBI handlers. Based on KCM's kcm-libguac-client-db security model.
//
// Reference: ~/Documents/kcm/core/packages/kcm-libguac-client-db/extra/libguac-client-db/src/db/settings.c

use std::collections::HashMap;

/// Unified security settings for all protocol handlers
///
/// These settings control access restrictions and must be enforced by every handler.
/// Parsed from connection parameters sent by the Guacamole client.
#[derive(Debug, Clone)]
pub struct HandlerSecuritySettings {
    // ========================================================================
    // Read-Only Mode
    // ========================================================================
    /// Prevent any user input that could modify the remote system
    ///
    /// Behavior by protocol:
    /// - SSH/Telnet: Block all keyboard input except Ctrl+C
    /// - RDP/VNC: Block keyboard and mouse clicks (allow mouse move for viewing)
    /// - Database: Block INSERT/UPDATE/DELETE/DROP/ALTER/TRUNCATE/CREATE queries
    /// - SFTP: Block upload/delete/rename/mkdir operations
    /// - RBI: Block all input
    pub read_only: bool,

    // ========================================================================
    // Clipboard Controls
    // ========================================================================
    /// Disable copying data FROM the remote session TO the client
    /// Prevents data exfiltration
    pub disable_copy: bool,

    /// Disable pasting data FROM the client TO the remote session
    /// Prevents injection of malicious content
    pub disable_paste: bool,

    /// Maximum clipboard buffer size in bytes
    /// Default: 1MB (1048576), Max: 50MB, Min: 256KB
    /// Based on KCM's GUAC_COMMON_CLIPBOARD_MIN/MAX_LENGTH
    pub clipboard_buffer_size: usize,

    // ========================================================================
    // Connection Timeouts & Limits
    // ========================================================================
    /// Connection timeout in seconds (0 = no timeout)
    /// How long to wait for initial connection
    pub connection_timeout_secs: u64,

    /// Idle timeout in seconds (0 = no timeout)
    /// Disconnect if no user activity for this duration
    pub idle_timeout_secs: u64,

    /// Maximum session duration in seconds (0 = no limit)
    /// Force disconnect after this duration regardless of activity
    pub max_session_duration_secs: u64,

    // ========================================================================
    // Credential Supply Gate
    // ========================================================================
    /// Allow the gateway to inject credentials (username/password from vault) at runtime.
    ///
    /// When false (the secure default), the handler must not accept username/password
    /// credentials supplied by the gateway. When true, the gateway is explicitly
    /// permitted to inject vault credentials into the session.
    ///
    /// Parameter name: `allow-supply-user`
    /// Values: "true" / "1" to enable; anything else (including absent) → false.
    pub allow_supply_user: bool,

    // ========================================================================
    // Wake-on-LAN (WoL)
    // ========================================================================
    /// Send WoL magic packet before connecting
    pub wol_send_packet: bool,

    /// MAC address of target system (required if wol_send_packet is true)
    pub wol_mac_addr: Option<String>,

    /// Broadcast address for WoL packet
    /// Default: "255.255.255.255"
    pub wol_broadcast_addr: String,

    /// UDP port for WoL packet
    /// Default: 9
    pub wol_udp_port: u16,

    /// Seconds to wait after WoL before attempting connection
    /// Default: 0
    pub wol_wait_time: u32,
}

// Clipboard buffer size limits (from KCM patches)
pub const CLIPBOARD_MIN_SIZE: usize = 256 * 1024; // 256KB
pub const CLIPBOARD_MAX_SIZE: usize = 50 * 1024 * 1024; // 50MB
pub const CLIPBOARD_DEFAULT_SIZE: usize = 1024 * 1024; // 1MB

impl Default for HandlerSecuritySettings {
    fn default() -> Self {
        Self {
            read_only: false,
            disable_copy: false,
            disable_paste: false,
            clipboard_buffer_size: CLIPBOARD_DEFAULT_SIZE,
            connection_timeout_secs: crate::DEFAULT_CONNECTION_TIMEOUT_SECS,
            idle_timeout_secs: 0,
            max_session_duration_secs: 0,
            allow_supply_user: false,
            wol_send_packet: false,
            wol_mac_addr: None,
            wol_broadcast_addr: "255.255.255.255".to_string(),
            wol_udp_port: 9,
            wol_wait_time: 0,
        }
    }
}

impl HandlerSecuritySettings {
    /// Parse security settings from connection parameters
    ///
    /// Parameter names match Guacamole/KCM conventions:
    /// - read-only: "true" or "1" to enable
    /// - disable-copy: "true" or "1" to enable
    /// - disable-paste: "true" or "1" to enable
    /// - clipboard-buffer-size: bytes (clamped to 256KB-50MB)
    /// - connection-timeout: seconds
    /// - idle-timeout: seconds
    /// - max-session-duration: seconds
    /// - allow-supply-user: "true" or "1" to permit vault credential injection
    /// - wol-send-packet: "true" or "1" to enable
    /// - wol-mac-addr: MAC address (required if WoL enabled)
    /// - wol-broadcast-addr: broadcast IP (default: 255.255.255.255)
    /// - wol-udp-port: UDP port (default: 9)
    /// - wol-wait-time: seconds to wait after WoL
    pub fn from_params(params: &HashMap<String, String>) -> Self {
        let clipboard_buffer_size = params
            .get("clipboard-buffer-size")
            .and_then(|v| v.parse().ok())
            .unwrap_or(CLIPBOARD_DEFAULT_SIZE)
            .clamp(CLIPBOARD_MIN_SIZE, CLIPBOARD_MAX_SIZE);

        Self {
            read_only: parse_bool(params.get("read-only")),
            disable_copy: parse_bool(params.get("disable-copy")),
            disable_paste: parse_bool(params.get("disable-paste")),
            clipboard_buffer_size,
            connection_timeout_secs: params
                .get("timeout") // guacd name
                .or_else(|| params.get("connection-timeout")) // legacy name
                .and_then(|v| v.parse().ok())
                .unwrap_or(crate::DEFAULT_CONNECTION_TIMEOUT_SECS),
            idle_timeout_secs: params
                .get("idle-timeout")
                .and_then(|v| v.parse().ok())
                .unwrap_or(0),
            max_session_duration_secs: params
                .get("max-session-duration")
                .and_then(|v| v.parse().ok())
                .unwrap_or(0),
            allow_supply_user: parse_bool(params.get("allow-supply-user")),
            wol_send_packet: parse_bool(params.get("wol-send-packet")),
            wol_mac_addr: params.get("wol-mac-addr").cloned(),
            wol_broadcast_addr: params
                .get("wol-broadcast-addr")
                .cloned()
                .unwrap_or_else(|| "255.255.255.255".to_string()),
            wol_udp_port: params
                .get("wol-udp-port")
                .and_then(|v| v.parse().ok())
                .unwrap_or(9),
            wol_wait_time: params
                .get("wol-wait-time")
                .and_then(|v| v.parse().ok())
                .unwrap_or(0),
        }
    }

    /// Check if clipboard copy is allowed
    pub fn is_copy_allowed(&self) -> bool {
        !self.disable_copy
    }

    /// Check if clipboard paste is allowed
    pub fn is_paste_allowed(&self) -> bool {
        !self.disable_paste && !self.read_only
    }

    /// Check if keyboard input is allowed
    ///
    /// In read-only mode, most keyboard input is blocked.
    /// Some protocols allow Ctrl+C for interrupt.
    pub fn is_keyboard_allowed(&self) -> bool {
        !self.read_only
    }

    /// Check if mouse click is allowed
    ///
    /// In read-only mode for graphical protocols:
    /// - Mouse movement is allowed (for viewing)
    /// - Mouse clicks are blocked (to prevent modifications)
    pub fn is_mouse_click_allowed(&self) -> bool {
        !self.read_only
    }

    /// Check if file upload is allowed (SFTP, file transfer)
    pub fn is_upload_allowed(&self) -> bool {
        !self.read_only
    }

    /// Check if file modification is allowed (SFTP delete, rename, mkdir)
    pub fn is_file_modification_allowed(&self) -> bool {
        !self.read_only
    }

    /// Check if runtime credential supply is permitted for this connection.
    ///
    /// Returns true only when `allow-supply-user` was explicitly set to true in the
    /// connection parameters. Defaults to false — the gateway must not inject
    /// credentials unless the record explicitly authorizes it.
    pub fn is_credential_supply_allowed(&self) -> bool {
        self.allow_supply_user
    }
}

/// Protocol-specific read-only behavior
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ReadOnlyBehavior {
    /// Block all keyboard input except Ctrl+C (SSH, Telnet)
    TerminalReadOnly,

    /// Block keyboard and mouse clicks, allow mouse move (RDP, VNC)
    GraphicalReadOnly,

    /// Block modifying queries (Database)
    DatabaseReadOnly,

    /// Block upload/delete/rename/mkdir (SFTP)
    SftpReadOnly,

    /// Block all input (RBI)
    BrowserReadOnly,
}

impl ReadOnlyBehavior {
    /// Get the appropriate read-only behavior for a protocol
    pub fn for_protocol(protocol: &str) -> Self {
        match protocol.to_lowercase().as_str() {
            "ssh" | "telnet" => Self::TerminalReadOnly,
            "rdp" | "vnc" => Self::GraphicalReadOnly,
            "mysql" | "postgresql" | "postgres" | "sqlserver" | "mssql" | "oracle" | "mongodb"
            | "redis" => Self::DatabaseReadOnly,
            "sftp" => Self::SftpReadOnly,
            "rbi" | "http" | "browser" => Self::BrowserReadOnly,
            _ => Self::TerminalReadOnly, // Default to terminal behavior
        }
    }
}

/// Check if a keyboard event should be allowed in read-only mode
///
/// For terminal protocols (SSH/Telnet), we allow:
/// - Ctrl+C (keysym 0x63 with Ctrl modifier, or raw 0x03)
///
/// This allows users to interrupt long-running commands even in read-only mode.
pub fn is_keyboard_event_allowed_readonly(keysym: u32, ctrl_pressed: bool) -> bool {
    // Allow Ctrl+C (interrupt)
    if ctrl_pressed && (keysym == 0x63 || keysym == 0x43) {
        return true;
    }

    // Allow raw Ctrl+C character
    if keysym == 0x03 {
        return true;
    }

    false
}

/// Check if a mouse event should be allowed in read-only mode
///
/// For graphical protocols (RDP/VNC), we allow:
/// - Mouse movement (button_mask == 0)
/// - Scroll wheel for viewing (button_mask & 0x18)
///
/// We block:
/// - Left/middle/right clicks (button_mask & 0x07)
pub fn is_mouse_event_allowed_readonly(button_mask: u32) -> bool {
    // Block left, middle, right clicks
    if (button_mask & 0x07) != 0 {
        return false;
    }

    // Allow movement and scroll
    true
}

fn parse_bool(value: Option<&String>) -> bool {
    value.map(|v| v == "true" || v == "1").unwrap_or(false)
}

// ============================================================================
// Protocol-Specific Security Extensions
// ============================================================================

/// Database-specific security settings
///
/// Extends HandlerSecuritySettings with database-specific controls.
/// Used by MySQL, PostgreSQL, SQL Server, Oracle, MongoDB, Redis handlers.
#[derive(Debug, Clone, Default)]
pub struct DatabaseSecuritySettings {
    /// Base security settings
    pub base: HandlerSecuritySettings,

    /// Disable CSV export (downloading query results)
    pub disable_csv_export: bool,

    /// Disable CSV import (uploading data files)
    pub disable_csv_import: bool,
}

impl DatabaseSecuritySettings {
    /// Parse from connection parameters
    pub fn from_params(params: &HashMap<String, String>) -> Self {
        Self {
            base: HandlerSecuritySettings::from_params(params),
            disable_csv_export: parse_bool(params.get("disable-csv-export")),
            disable_csv_import: parse_bool(params.get("disable-csv-import")),
        }
    }

    /// Check if CSV export is allowed
    pub fn is_csv_export_allowed(&self) -> bool {
        !self.disable_csv_export
    }

    /// Check if CSV import is allowed
    pub fn is_csv_import_allowed(&self) -> bool {
        !self.disable_csv_import && !self.base.read_only
    }
}

// ---------------------------------------------------------------------------
// DangerousStatementDetector — comment-stripping, allowlist-posture classifier
// ---------------------------------------------------------------------------
//
// Ported from keeperdb-ops/src/query/safety.rs.
//
// Security posture: allowlist. A statement is safe only if it is provably
// read-only. Anything else is flagged, regardless of whether the classifier
// recognises the specific write keyword. This closes first-token evasions like
//   DROP/**/TABLE users        (comment-split)
//   BEGIN DELETE FROM t; END;  (PL/SQL block body hidden from first-token check)
//   WITH d AS (DELETE …) SELECT * FROM d  (CTE wrapping a write)

/// Detects dangerous SQL statements for read-only mode enforcement.
pub struct DangerousStatementDetector;

impl DangerousStatementDetector {
    /// Returns true only if the statement is provably read-only.
    pub fn is_read_only(sql: &str) -> bool {
        is_read_only_normalized(&sql_normalize(sql))
    }
}

fn sql_normalize(sql: &str) -> String {
    let stripped = sql_strip_comments(sql);
    let mut out = String::with_capacity(stripped.len());
    let mut prev_was_space = true;
    for ch in stripped.chars() {
        let is_boundary = ch.is_whitespace() || ch == '(' || ch == ')' || ch == ',';
        if is_boundary {
            if !prev_was_space {
                out.push(' ');
                prev_was_space = true;
            }
        } else {
            out.push(ch.to_ascii_uppercase());
            prev_was_space = false;
        }
    }
    while out.ends_with(' ') {
        out.pop();
    }
    out
}

fn sql_strip_comments(sql: &str) -> String {
    let bytes = sql.as_bytes();
    let mut out = String::with_capacity(sql.len());
    let mut i = 0;
    while i < bytes.len() {
        if i + 1 < bytes.len() && bytes[i] == b'/' && bytes[i + 1] == b'*' {
            i += 2;
            while i + 1 < bytes.len() && !(bytes[i] == b'*' && bytes[i + 1] == b'/') {
                i += 1;
            }
            if i + 1 < bytes.len() {
                i += 2;
            } else {
                i = bytes.len();
            }
            out.push(' ');
            continue;
        }
        if i + 1 < bytes.len() && bytes[i] == b'-' && bytes[i + 1] == b'-' {
            while i < bytes.len() && bytes[i] != b'\n' {
                i += 1;
            }
            out.push(' ');
            continue;
        }
        if bytes[i] == b'#' {
            while i < bytes.len() && bytes[i] != b'\n' {
                i += 1;
            }
            out.push(' ');
            continue;
        }
        out.push(bytes[i] as char);
        i += 1;
    }
    out
}

fn is_read_only_normalized(n: &str) -> bool {
    // Multi-statement SQL: a semicolon anywhere except the trailing position
    // means more than one statement was submitted. Even if the first statement
    // is a SELECT, the subsequent statements may be writes (DROP, DELETE, …).
    // Reject all multi-statement input — a single legitimate query never needs
    // to send a second statement in the same string.
    //
    // After normalization, trailing whitespace has been stripped, so:
    //   "SELECT * FROM t;"   -> n ends with ';', no content after -> still single-statement
    //   "SELECT * FROM t; DROP TABLE t" -> ';' is followed by ' ' and more content -> multi
    let semicolon_pos = n.bytes().position(|b| b == b';');
    if let Some(pos) = semicolon_pos {
        // Allow a lone trailing semicolon (pos == last byte).
        if pos < n.len() - 1 {
            return false;
        }
    }

    // PL/SQL anonymous blocks are never read-only.
    if n.starts_with("BEGIN ")
        || n.starts_with("DECLARE ")
        || n.starts_with("DO ")
        || n == "BEGIN"
        || n == "DECLARE"
        || n == "DO"
    {
        return false;
    }
    let ro_leaders = [
        "SELECT ",
        "SHOW ",
        "EXPLAIN ",
        "DESCRIBE ",
        "DESC ",
        "PRAGMA ",
        "VALUES ",
        "TABLE ",
        "USE ",
    ];
    for kw in ro_leaders {
        if n.starts_with(kw) {
            return true;
        }
    }
    let single_tok = [
        "SELECT", "SHOW", "EXPLAIN", "DESCRIBE", "DESC", "PRAGMA", "VALUES", "TABLE", "USE",
    ];
    for kw in single_tok {
        if n == kw || n.starts_with(&format!("{kw};")) {
            return true;
        }
    }
    if n.starts_with("WITH ") {
        return is_cte_read_only(n);
    }
    false
}

fn is_cte_read_only(upper: &str) -> bool {
    !upper.contains(" INSERT ")
        && !upper.contains(" UPDATE ")
        && !upper.contains(" DELETE ")
        && !upper.contains(" DROP ")
        && !upper.contains(" ALTER ")
        && !upper.contains(" TRUNCATE ")
        && !upper.contains(" MERGE ")
        && !upper.contains(" REPLACE ")
        && !upper.contains(" CREATE ")
        && !upper.contains(" RENAME ")
        && !upper.contains(" GRANT ")
        && !upper.contains(" REVOKE ")
        && !upper.contains(" CALL ")
        && !upper.contains(" EXEC ")
        && !upper.contains(" EXECUTE ")
}

// ---------------------------------------------------------------------------
// Public SQL classifier (uses DangerousStatementDetector internally)
// ---------------------------------------------------------------------------

/// SQL query classifier for read-only mode enforcement.
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum QueryType {
    /// SELECT, SHOW, DESCRIBE, EXPLAIN and similar — allowed in read-only mode.
    ReadOnly,
    /// Everything not provably read-only — blocked in read-only mode.
    Modifying,
    /// Kept for API compatibility; treated the same as Modifying.
    Unknown,
}

/// Classify a SQL query for security enforcement.
///
/// Uses comment-stripping and allowlist posture: a query is ReadOnly only if
/// it is provably safe (SELECT/SHOW/EXPLAIN/DESCRIBE/…). PL/SQL blocks
/// (BEGIN…END), CTEs wrapping writes, and comment-split evasions are all
/// classified as Modifying.
pub fn classify_sql_query(query: &str) -> QueryType {
    if query.trim().is_empty() {
        return QueryType::Unknown;
    }
    // Psql meta-commands (\d, \dt, \l …) are read-only by convention.
    let first = query
        .trim()
        .split(|c: char| c.is_whitespace() || c == '(')
        .next()
        .unwrap_or("");
    if matches!(
        first,
        "\\d" | "\\dt" | "\\l" | "\\c" | "\\?" | "\\h" | "\\D" | "\\DT" | "\\L" | "\\C" | "\\H"
    ) {
        return QueryType::ReadOnly;
    }
    if DangerousStatementDetector::is_read_only(query) {
        QueryType::ReadOnly
    } else {
        QueryType::Modifying
    }
}

/// Check if runtime credential supply is allowed by the connection's security settings.
///
/// Returns `Ok(())` when `allow-supply-user` was set to true on the connection.
/// Returns `Err` with a descriptive message otherwise, suitable for sending to the client.
///
/// Call this before using `username`/`password` credentials injected by the gateway
/// to ensure the vault record explicitly authorized credential supply for this session.
pub fn check_credential_supply_allowed(settings: &HandlerSecuritySettings) -> Result<(), String> {
    if settings.allow_supply_user {
        Ok(())
    } else {
        Err(
            "Runtime credential supply not permitted for this connection. \
             Set allow-supply-user=true on the connection record to enable it."
                .to_string(),
        )
    }
}

/// Check if a SQL query is allowed based on security settings
pub fn check_sql_query_allowed(
    query: &str,
    settings: &DatabaseSecuritySettings,
) -> Result<(), String> {
    if !settings.base.read_only {
        return Ok(());
    }
    if DangerousStatementDetector::is_read_only(query) {
        Ok(())
    } else {
        Err("Query blocked: read-only mode is enabled. Only SELECT, SHOW, DESCRIBE, EXPLAIN and similar read-only statements are permitted.".to_string())
    }
}

/// Detect MySQL export queries (INTO OUTFILE)
pub fn is_mysql_export_query(query: &str) -> bool {
    let query_upper = query.to_uppercase();
    query_upper.contains("INTO OUTFILE") || query_upper.contains("INTO LOCAL OUTFILE")
}

/// Detect MySQL import queries (LOAD DATA)
pub fn is_mysql_import_query(query: &str) -> bool {
    let query_upper = query.to_uppercase();
    query_upper.contains("LOAD DATA") || query_upper.contains("LOAD LOCAL DATA")
}

/// Detect PostgreSQL COPY export
pub fn is_postgres_copy_out(query: &str) -> bool {
    let query_upper = query.to_uppercase();
    query_upper.starts_with("COPY") && query_upper.contains("TO STDOUT")
}

/// Detect PostgreSQL COPY import
pub fn is_postgres_copy_in(query: &str) -> bool {
    let query_upper = query.to_uppercase();
    query_upper.starts_with("COPY") && query_upper.contains("FROM STDIN")
}

/// SFTP-specific security settings
///
/// Extends HandlerSecuritySettings with SFTP-specific controls.
#[derive(Debug, Clone, Default)]
pub struct SftpSecuritySettings {
    /// Base security settings
    pub base: HandlerSecuritySettings,

    /// Root directory to restrict file access (chroot-like)
    pub root_directory: Option<String>,

    /// Disable file download
    pub disable_download: bool,

    /// Disable file upload
    pub disable_upload: bool,

    /// Maximum file size for upload (bytes, 0 = no limit)
    pub max_upload_size: u64,
}

impl SftpSecuritySettings {
    /// Parse from connection parameters
    ///
    /// Both the `sftp-` prefixed names the gateway sends and the unprefixed names
    /// the `sftp` protocol advertises in `guacr-guacd/src/args.rs` are accepted:
    /// `server.rs` keys the params map by the advertised names, so a client that
    /// fills those slots during the guacd handshake would otherwise be ignored.
    /// The prefixed spelling wins when both are present.
    pub fn from_params(params: &HashMap<String, String>) -> Self {
        Self {
            base: HandlerSecuritySettings::from_params(params),
            root_directory: params
                .get("sftp-root-directory")
                .or_else(|| params.get("root-directory"))
                .cloned(),
            disable_download: parse_bool(
                params
                    .get("sftp-disable-download")
                    .or_else(|| params.get("disable-download")),
            ) || parse_bool(params.get("disable-copy")), // disable-copy affects download
            disable_upload: parse_bool(
                params
                    .get("sftp-disable-upload")
                    .or_else(|| params.get("disable-upload")),
            ) || parse_bool(params.get("read-only")), // read-only blocks upload
            max_upload_size: params
                .get("sftp-max-upload-size")
                .and_then(|v| v.parse().ok())
                .unwrap_or(0),
        }
    }

    /// Check if download is allowed
    pub fn is_download_allowed(&self) -> bool {
        !self.disable_download
    }

    /// Check if upload is allowed
    pub fn is_upload_allowed(&self) -> bool {
        !self.disable_upload && !self.base.read_only
    }

    /// Check if a file operation is allowed
    pub fn is_file_operation_allowed(&self, operation: SftpOperation) -> bool {
        match operation {
            SftpOperation::Read | SftpOperation::List | SftpOperation::Stat => true,
            SftpOperation::Download => self.is_download_allowed(),
            SftpOperation::Upload => self.is_upload_allowed(),
            SftpOperation::Delete
            | SftpOperation::Rename
            | SftpOperation::Mkdir
            | SftpOperation::Rmdir => !self.base.read_only,
        }
    }
}

/// SFTP file operations
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum SftpOperation {
    Read,
    List,
    Stat,
    Download,
    Upload,
    Delete,
    Rename,
    Mkdir,
    Rmdir,
}

/// RBI (Remote Browser Isolation) specific security settings
///
/// Extends HandlerSecuritySettings with browser-specific controls.
#[derive(Debug, Clone, Default)]
pub struct RbiSecuritySettings {
    /// Base security settings
    pub base: HandlerSecuritySettings,

    /// Disable file downloads from browser
    pub disable_download: bool,

    /// Disable file uploads to browser
    pub disable_upload: bool,

    /// Disable printing
    pub disable_print: bool,

    /// URL allowlist (if set, only these URLs are accessible)
    pub url_allowlist: Vec<String>,

    /// URL blocklist (these URLs are blocked)
    pub url_blocklist: Vec<String>,
}

impl RbiSecuritySettings {
    /// Parse from connection parameters
    ///
    /// Both the `rbi-` prefixed names the gateway sends and the unprefixed names the
    /// `http`/`https`/`rbi` protocols advertise in `guacr-guacd/src/args.rs` are
    /// accepted: `server.rs` keys the params map by the advertised names, so a client
    /// that fills those slots during the guacd handshake would otherwise be ignored.
    /// The prefixed spelling wins when both are present.
    pub fn from_params(params: &HashMap<String, String>) -> Self {
        let url_allowlist = params
            .get("rbi-url-allowlist")
            .or_else(|| params.get("url-allowlist"))
            .map(|v| v.split(',').map(|s| s.trim().to_string()).collect())
            .unwrap_or_default();

        let url_blocklist = params
            .get("rbi-url-blocklist")
            .or_else(|| params.get("url-blocklist"))
            .map(|v| v.split(',').map(|s| s.trim().to_string()).collect())
            .unwrap_or_default();

        Self {
            base: HandlerSecuritySettings::from_params(params),
            disable_download: parse_bool(
                params
                    .get("rbi-disable-download")
                    .or_else(|| params.get("disable-download")),
            ),
            disable_upload: parse_bool(
                params
                    .get("rbi-disable-upload")
                    .or_else(|| params.get("disable-upload")),
            ) || parse_bool(params.get("read-only")),
            disable_print: parse_bool(
                params
                    .get("rbi-disable-print")
                    .or_else(|| params.get("disable-print")),
            ),
            url_allowlist,
            url_blocklist,
        }
    }

    /// Check if a URL is allowed.
    ///
    /// Uses host-based matching (same semantics as `is_url_allowed_for_patterns` in
    /// browser_client) to prevent path-confusion bypasses where a substring check would
    /// accept `evil.com?ref=allowed.com` given pattern `allowed.com`.
    pub fn is_url_allowed(&self, url: &str) -> bool {
        // If allowlist is set, URL host must match one of the patterns
        if !self.url_allowlist.is_empty() {
            return rbi_host_matches_any(url, &self.url_allowlist);
        }

        // If blocklist is set, URL host must not match any pattern
        if !self.url_blocklist.is_empty() {
            return !rbi_host_matches_any(url, &self.url_blocklist);
        }

        true
    }

    /// Check if download is allowed
    pub fn is_download_allowed(&self) -> bool {
        !self.disable_download
    }

    /// Check if upload is allowed
    pub fn is_upload_allowed(&self) -> bool {
        !self.disable_upload && !self.base.read_only
    }

    /// Check if printing is allowed
    pub fn is_print_allowed(&self) -> bool {
        !self.disable_print
    }
}

/// Check whether a URL's host matches any of the given patterns.
///
/// Patterns without `*` must match the URL host exactly or as a suffix (subdomain).
/// Patterns with `*.` prefix match any subdomain of the given domain.
///
/// This uses the same semantics as `is_url_allowed_for_patterns` in browser_client.
fn rbi_host_matches_any(url: &str, patterns: &[String]) -> bool {
    let host = rbi_extract_host(url);
    for pattern in patterns {
        if let Some(domain) = pattern.strip_prefix("*.") {
            if host == domain || host.ends_with(&format!(".{}", domain)) {
                return true;
            }
        } else {
            let pat = pattern
                .trim_start_matches("https://")
                .trim_start_matches("http://");
            let pat = pat.split('/').next().unwrap_or(pat);
            if host == pat || host.ends_with(&format!(".{}", pat)) {
                return true;
            }
        }
    }
    false
}

/// Extract the host (without port) from a URL string.
fn rbi_extract_host(url: &str) -> &str {
    let after_scheme = if let Some(rest) = url.strip_prefix("https://") {
        rest
    } else if let Some(rest) = url.strip_prefix("http://") {
        rest
    } else {
        url
    };
    let host_with_port = after_scheme
        .split(['/', '?', '#'])
        .next()
        .unwrap_or(after_scheme);
    if host_with_port.starts_with('[') {
        host_with_port
    } else {
        host_with_port.split(':').next().unwrap_or(host_with_port)
    }
}
