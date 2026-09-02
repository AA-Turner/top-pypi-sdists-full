use std::collections::HashMap;
use std::sync::Arc;
use std::time::Duration;

use async_trait::async_trait;
use bytes::Bytes;
use guacr_handlers::{
    check_credential_supply_allowed, connect_with_event_adapter, send_disconnect,
    EventBasedHandler, EventCallback, HandlerError, HandlerStats, HealthStatus, KeepAliveManager,
    ProtocolHandler, RecordingConfig, VideoOutput, DEFAULT_KEEPALIVE_INTERVAL_SECS,
};
use keeperdb_core::types::DatabaseType;
use log::{debug, info, warn};
use tokio::sync::mpsc;

#[cfg(feature = "threat-detection")]
use guacr_threat_detection::{SessionGuard, ThreatDetector};

use crate::handler_helpers::{
    reject_with_error, render_connection_error, render_connection_success, send_render,
};
use crate::keeperdb_driver;
use crate::query_executor::QueryExecutor;
use crate::recording::{
    finalize_recording, init_recording, record_error_output, record_query_input,
    record_query_output, send_and_record,
};
use crate::security::DatabaseSecuritySettings;

/// Generic SQL protocol handler backed by the KeeperDB SDK.
///
/// Handles MySQL, MariaDB, PostgreSQL, SQL Server, and Oracle through a single
/// implementation. The DB-specific wire protocol is handled by the keeperdb driver.
pub struct SqlHandler {
    /// Guacamole protocol name (e.g. "mysql", "postgresql", "sql-server", "oracle")
    protocol_name: &'static str,
    db_type: DatabaseType,
    default_port: u16,
    query_timeout_secs: u64,
}

impl SqlHandler {
    pub fn new(protocol_name: &'static str, db_type: DatabaseType, default_port: u16) -> Self {
        Self {
            protocol_name,
            db_type,
            default_port,
            query_timeout_secs: 300,
        }
    }

    pub fn mysql() -> Self {
        Self::new("mysql", DatabaseType::Mysql, 3306)
    }

    pub fn mariadb() -> Self {
        Self::new("mariadb", DatabaseType::Mysql, 3306)
    }

    pub fn postgresql() -> Self {
        Self::new("postgresql", DatabaseType::Postgres, 5432)
    }

    pub fn sql_server() -> Self {
        Self::new("sql-server", DatabaseType::Mssql, 1433)
    }

    pub fn oracle() -> Self {
        Self::new("oracle", DatabaseType::Oracle, 1521)
    }

    /// Build a handler for a keeperdb database type, keyed by its canonical protocol name.
    /// Registry-driven registration uses this so a new keeperdb driver is supported
    /// automatically with no guacr code change.
    pub fn for_type(db_type: DatabaseType) -> Self {
        Self::new(
            db_type.as_str(),
            db_type,
            db_type.default_port().unwrap_or(0),
        )
    }
}

/// Every SQL handler the compiled-in keeperdb driver registry supports.
///
/// Canonical protocol keys come from `DatabaseType::as_str()`, so adding a driver in
/// keeperdb (its factory + the `all-drivers` feature) makes it register here
/// automatically — no guacr change. Legacy protocol-key aliases the vault client may
/// still send (`mariadb`, `postgresql`, `sql-server`) are included for compatibility.
pub fn sql_handlers() -> Vec<SqlHandler> {
    let registry = keeperdb_drivers::with_builtin_factories();
    let mut handlers: Vec<SqlHandler> = registry
        .supported_types()
        .into_iter()
        .map(SqlHandler::for_type)
        .collect();
    handlers.push(SqlHandler::mariadb());
    handlers.push(SqlHandler::postgresql());
    handlers.push(SqlHandler::sql_server());
    handlers
}

#[async_trait]
impl ProtocolHandler for SqlHandler {
    fn name(&self) -> &str {
        self.protocol_name
    }

    fn as_event_based(&self) -> Option<&dyn EventBasedHandler> {
        Some(self)
    }

    async fn connect(
        &self,
        params: HashMap<String, String>,
        to_client: mpsc::Sender<Bytes>,
        mut from_client: mpsc::Receiver<Bytes>,
        _video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: guacr_handlers::SessionHooks,
    ) -> guacr_handlers::Result<()> {
        let conn_id = params.get("client_id").cloned().unwrap_or_default();
        let db_name = self.db_type.display_name();
        info!("[conn={}] {} handler starting", conn_id, db_name);

        // Use aws-lc-rs to match this crate's declared rustls feature; relying on
        // `ring` only compiles by accident via workspace feature unification and
        // breaks when guacr-database is built in isolation.
        let _ = rustls::crypto::aws_lc_rs::default_provider().install_default();

        let security = DatabaseSecuritySettings::from_params(&params);
        let recording_config = RecordingConfig::from_params(&params);

        // Enforce the credential supply gate before connecting.  Database handlers
        // always receive username + password from the params (either static vault
        // credentials or runtime-injected ones).  The connection record must set
        // allow-supply-user=true to authorise their use.
        check_credential_supply_allowed(&security.base).map_err(HandlerError::SecurityViolation)?;

        let hostname = params
            .get("hostname")
            .ok_or_else(|| HandlerError::MissingParameter("hostname".to_string()))?;
        let port: u16 = params
            .get("port")
            .and_then(|p| p.parse().ok())
            .unwrap_or(self.default_port);

        let (width, height, cols, rows) = crate::handler_helpers::parse_display_size(&params);

        let prompt = if security.base.read_only {
            format!("{} [RO]> ", self.protocol_name)
        } else {
            format!("{}> ", self.protocol_name)
        };
        let mut executor = QueryExecutor::new_with_size(&prompt, self.protocol_name, rows, cols)
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

        let mut recorder = init_recording(&recording_config, &params, db_name, cols, rows);

        #[cfg(feature = "threat-detection")]
        let threat_detector = Arc::new(
            ThreatDetector::new(crate::threat::threat_config_from_params(&params))
                .map_err(|e| HandlerError::ProtocolError(format!("Threat detector init: {}", e)))?,
        );
        #[cfg(feature = "threat-detection")]
        let threat_session_id = crate::threat::new_session_id();
        #[cfg(feature = "threat-detection")]
        let _threat_guard = SessionGuard::new(threat_detector.clone(), threat_session_id.clone());

        QueryExecutor::send_display_init(&to_client, width, height).await?;

        // Send terminal color scheme so the vault can theme xterm to match.
        if let Some(scheme) = params.get("colorScheme").filter(|s| !s.is_empty()) {
            let instr = guacr_protocol::format_instruction("colorscheme", &[scheme.as_str()]);
            let _ = to_client.send(bytes::Bytes::from(instr)).await;
        }

        // Connect via KeeperDB driver
        let mut conn_params = params.clone();
        // Ensure port is in params for ConnectionInfo builder
        conn_params.insert("port".to_string(), port.to_string());

        let driver = match keeperdb_driver::connect(self.db_type, &conn_params).await {
            Ok(d) => {
                info!(
                    "[conn={}] {}: Connected to {}:{}",
                    conn_id, db_name, hostname, port
                );
                let mut info = vec![format!("Connected to {} at {}:{}", db_name, hostname, port)];
                let database = params.get("database").map(|s| s.as_str()).unwrap_or("");
                if !database.is_empty() {
                    info.push(format!("Database: {}", database));
                }
                let info_refs: Vec<&str> = info.iter().map(|s| s.as_str()).collect();
                render_connection_success(
                    &mut executor,
                    &to_client,
                    &info_refs,
                    &security,
                    &mut recorder,
                )
                .await?;
                d
            }
            Err(e) => {
                let error_msg = format!("Connection failed: {}", e);
                warn!("[conn={}] {}: {}", conn_id, db_name, error_msg);
                render_connection_error(
                    &mut executor,
                    &to_client,
                    &mut from_client,
                    &error_msg,
                    &[
                        "Check hostname is resolvable",
                        &format!("Verify {} server is running", db_name),
                        "Check credentials are correct",
                        "Verify network connectivity",
                        "For TLS issues: set tls-verify=false in advanced params",
                    ],
                    &mut recorder,
                )
                .await?;
                return Err(HandlerError::ConnectionFailed(error_msg));
            }
        };

        let mut debounce = tokio::time::interval(Duration::from_millis(16));
        debounce.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        let mut keepalive = KeepAliveManager::new(DEFAULT_KEEPALIVE_INTERVAL_SECS);
        let mut keepalive_interval =
            tokio::time::interval(Duration::from_secs(DEFAULT_KEEPALIVE_INTERVAL_SECS));
        keepalive_interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        'outer: loop {
            tokio::select! {
                _ = keepalive_interval.tick() => {
                    if let Some(sync_instr) = keepalive.check() {
                        if send_and_record(&to_client, &mut recorder, sync_instr).await.is_err() {
                            break;
                        }
                    }
                }

                _ = debounce.tick() => {
                    if to_client.is_closed() { break; }
                    if executor.is_dirty() {
                        if let Ok((_, instructions)) = executor.render_screen().await {
                            for instr in instructions {
                                if send_and_record(&to_client, &mut recorder, instr).await.is_err() {
                                    break 'outer;
                                }
                            }
                        }
                    }
                }

                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        info!("[conn={}] {}: Client disconnected", conn_id, db_name);
                        break 'outer;
                    };

                    match executor.process_input(&msg).await {
                        Ok((needs_render, instructions, pending_query)) => {
                            if let Some(query) = pending_query {
                                debug!("[conn={}] {}: Executing: {}", conn_id, db_name, query);

                                #[cfg(feature = "threat-detection")]
                                crate::handler_helpers::maybe_terminate_on_threat(
                                    &threat_detector, &threat_session_id, &query,
                                    params.get("username").map(|s| s.as_str()).unwrap_or(""),
                                    hostname, self.protocol_name,
                                    &mut executor, &to_client, &mut recorder,
                                ).await?;

                                record_query_input(&mut recorder, &recording_config, &query);

                                let query_lower = query.to_lowercase();

                                // Built-in commands
                                match query_lower.as_str() {
                                    "quit" | "exit" | "\\q" => {
                                        let _ = executor.write_line("Bye");
                                        send_render(&mut executor, &to_client, &mut recorder).await?;
                                        break 'outer;
                                    }
                                    "help" | "\\h" | "\\?" => {
                                        self.write_help(&mut executor)?;
                                        send_render(&mut executor, &to_client, &mut recorder).await?;
                                        continue;
                                    }
                                    "clear" | "\\c" => {
                                        executor.write_status("");
                                        send_render(&mut executor, &to_client, &mut recorder).await?;
                                        continue;
                                    }
                                    _ => {}
                                }

                                // CONFIRM: prefix overrides dangerous-statement guard
                                let (sql, confirmed) = if query.starts_with("CONFIRM:") {
                                    (query.trim_start_matches("CONFIRM:").trim(), true)
                                } else {
                                    (query.as_str(), false)
                                };

                                // Read-only enforcement
                                if let Err(msg) = crate::security::check_query_allowed(sql, &security) {
                                    reject_with_error(&mut executor, &to_client, &mut recorder, &msg).await?;
                                    continue;
                                }

                                let timeout_secs = self.query_timeout_secs;
                                let exec_future = if confirmed {
                                    // Re-execute with max_rows to bypass confirmation gate
                                    driver.execute_with_max_rows(sql, 10_000)
                                } else {
                                    driver.execute(sql)
                                };

                                match tokio::time::timeout(
                                    Duration::from_secs(timeout_secs),
                                    exec_future,
                                ).await {
                                    Err(_) => {
                                        let msg = format!("Query timed out after {}s", timeout_secs);
                                        record_error_output(&mut recorder, &msg);
                                        executor.write_error(&msg)
                                            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                                    }
                                    Ok(Err(keeperdb_core::error::KeeperDbError::ConfirmationRequired { operations, .. })) => {
                                        let ops: Vec<String> = operations.iter().map(|o| format!("{:?}", o)).collect();
                                        let msg = format!(
                                            "Dangerous operation detected: {}. \
                                             Type CONFIRM: <query> to execute.",
                                            ops.join(", ")
                                        );
                                        record_error_output(&mut recorder, &msg);
                                        executor.write_error(&msg)
                                            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                                    }
                                    Ok(Err(e)) => {
                                        let msg = e.to_string();
                                        record_error_output(&mut recorder, &msg);
                                        executor.write_error(&msg)
                                            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                                    }
                                    Ok(Ok(result)) => {
                                        let qr = keeperdb_driver::execution_result_to_query_result(result);
                                        record_query_output(&mut recorder, &qr);
                                        executor.write_result(&qr)
                                            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

                                        // Update the prompt when a USE <db> statement succeeds.
                                        if let Some(db) = extract_use_database_name(sql) {
                                            executor.set_current_database(Some(db));
                                        }
                                    }
                                }

                                send_render(&mut executor, &to_client, &mut recorder).await?;
                                continue;
                            }

                            if needs_render {
                                for instr in instructions {
                                    let _ = send_and_record(&to_client, &mut recorder, instr).await;
                                }
                            }
                        }
                        Err(e) => {
                            warn!("[conn={}] {}: Input error: {}", conn_id, db_name, e);
                        }
                    }
                }

                else => break,
            }
        }

        let _ = driver.disconnect().await;
        finalize_recording(recorder, db_name);
        send_disconnect(&to_client).await;
        info!("[conn={}] {} handler ended", conn_id, db_name);
        Ok(())
    }

    async fn health_check(&self) -> guacr_handlers::Result<HealthStatus> {
        Ok(HealthStatus::Healthy)
    }

    async fn stats(&self) -> guacr_handlers::Result<HandlerStats> {
        Ok(HandlerStats::default())
    }
}

#[async_trait]
impl EventBasedHandler for SqlHandler {
    fn name(&self) -> &str {
        self.protocol_name
    }

    async fn connect_with_events(
        &self,
        params: HashMap<String, String>,
        callback: Arc<dyn EventCallback>,
        from_client: mpsc::Receiver<Bytes>,
        video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: guacr_handlers::SessionHooks,
    ) -> Result<(), HandlerError> {
        connect_with_event_adapter(
            |params, to_client, from_client, video_tx, _hooks| {
                self.connect(params, to_client, from_client, video_tx, _hooks)
            },
            params,
            callback,
            from_client,
            video_tx,
            _hooks,
            4096,
        )
        .await
    }
}

/// Extract the database name from a `USE <db>` statement.
///
/// Returns `Some(db_name)` if the query is a USE statement with a non-empty database name,
/// or `None` if the query is not a USE statement.
///
/// Accepts: `USE mydb`, `use mydb`, `USE mydb;`, `  USE   mydb  `.
pub(crate) fn extract_use_database_name(query: &str) -> Option<String> {
    let trimmed = query.trim();
    let upper = trimmed.to_uppercase();
    if !upper.starts_with("USE ") {
        return None;
    }
    let db = trimmed[4..].trim().trim_end_matches(';').trim();
    if db.is_empty() {
        None
    } else {
        Some(db.to_string())
    }
}

impl SqlHandler {
    fn write_help(&self, executor: &mut QueryExecutor) -> guacr_handlers::Result<()> {
        let lines = [
            "",
            "Available commands:",
            "  help, \\h         Show this help",
            "  quit, exit, \\q   Disconnect",
            "  clear, \\c        Clear screen",
            "  CONFIRM: <sql>   Execute dangerous statement (DROP, TRUNCATE, etc.)",
            "",
            "Keyboard shortcuts:",
            "  Tab              Switch to Grid View (when enabled)",
            "  Ctrl+G           Toggle Terminal / Grid View",
            "  Page Up/Down     Scroll output history",
            "",
        ];
        for line in lines {
            executor
                .write_line(line)
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        }
        Ok(())
    }
}
