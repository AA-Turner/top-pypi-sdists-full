use async_trait::async_trait;
use bytes::Bytes;
use guacr_handlers::{
    send_disconnect, EventBasedHandler, EventCallback, HandlerError, HandlerStats, HealthStatus,
    KeepAliveManager, ProtocolHandler, RecordingConfig, VideoOutput,
    DEFAULT_KEEPALIVE_INTERVAL_SECS,
};
use log::{debug, info, warn};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::mpsc;

#[cfg(feature = "threat-detection")]
use guacr_threat_detection::{SessionGuard, ThreatDetector};

use crate::csv_export::{generate_csv_filename, CsvExporter};
use crate::csv_import::CsvImporter;
use crate::query_executor::QueryExecutor;
use crate::recording::{finalize_recording, init_recording, record_query_input, send_and_record};
use crate::security::{check_query_allowed, DatabaseSecuritySettings};

use std::sync::atomic::AtomicI32;

/// Global stream index counter for unique stream IDs
static STREAM_INDEX: AtomicI32 = AtomicI32::new(3000);

/// Oracle Database handler
///
/// Provides interactive SQL*Plus-like terminal access to Oracle databases.
///
/// # Oracle Instant Client Setup
///
/// Requires Oracle Instant Client to be installed and the oracle crate to be
/// available at compile time. See the oracle crate documentation for setup.
pub struct OracleHandler {
    config: OracleConfig,
}

#[derive(Debug, Clone)]
pub struct OracleConfig {
    pub default_port: u16,
    pub service_name: String,
    pub require_encryption: bool,
    pub connection_timeout_secs: u64,
}

impl Default for OracleConfig {
    fn default() -> Self {
        Self {
            default_port: 1521,
            service_name: "ORCL".to_string(),
            require_encryption: true,
            connection_timeout_secs: guacr_handlers::DEFAULT_CONNECTION_TIMEOUT_SECS,
        }
    }
}

impl OracleHandler {
    pub fn new(config: OracleConfig) -> Self {
        Self { config }
    }

    pub fn with_defaults() -> Self {
        Self::new(OracleConfig::default())
    }
}

#[async_trait]
impl ProtocolHandler for OracleHandler {
    fn name(&self) -> &str {
        "oracle"
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
    ) -> guacr_handlers::Result<()> {
        info!("Oracle handler starting");

        // Parse security settings
        let security = DatabaseSecuritySettings::from_params(&params);
        if security.base.read_only {
            info!("Oracle: Read-only mode enabled");
        }

        // Parse recording configuration
        let recording_config = RecordingConfig::from_params(&params);

        // Parse connection parameters
        let hostname = params
            .get("hostname")
            .ok_or_else(|| HandlerError::MissingParameter("hostname".to_string()))?
            .clone();
        let port: u16 = params
            .get("port")
            .and_then(|p| p.parse().ok())
            .unwrap_or(self.config.default_port);
        let username = params
            .get("username")
            .ok_or_else(|| HandlerError::MissingParameter("username".to_string()))?
            .clone();
        let password = params
            .get("password")
            .ok_or_else(|| HandlerError::MissingParameter("password".to_string()))?
            .clone();
        let service = params
            .get("service")
            .cloned()
            .unwrap_or_else(|| self.config.service_name.clone());

        info!(
            "Oracle: Connecting to {}@{}:{}/{}",
            username, hostname, port, service
        );

        let (width, height, cols, rows) = crate::handler_helpers::parse_display_size(&params);

        info!(
            "Oracle: Display size {}x{} px → {}x{} chars",
            width, height, cols, rows
        );

        // Create query executor with SQL*Plus prompt and correct dimensions
        let prompt = if security.base.read_only {
            "SQL [RO]> "
        } else {
            "SQL> "
        };
        let mut executor = QueryExecutor::new_with_size(prompt, "oracle", rows, cols)
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        executor.use_binary = params.get("binary").map(|v| v == "true").unwrap_or(false);

        // Initialize recording if enabled
        let mut recorder = init_recording(&recording_config, &params, "Oracle", cols, rows);

        // Initialize threat detection if enabled.
        // ThreatContext is created first so SessionGuard can borrow from it,
        // avoiding extra Arc/String clones.
        let threat_ctx = crate::threat::ThreatContext {
            hostname: hostname.to_string(),
            username: username.to_string(),
            #[cfg(feature = "threat-detection")]
            detector: Arc::new(
                ThreatDetector::new(crate::threat::threat_config_from_params(&params)).map_err(
                    |e| HandlerError::ProtocolError(format!("Threat detector init: {}", e)),
                )?,
            ),
            #[cfg(feature = "threat-detection")]
            session_id: crate::threat::new_session_id(),
        };
        #[cfg(feature = "threat-detection")]
        let _threat_guard =
            SessionGuard::new(threat_ctx.detector.clone(), threat_ctx.session_id.clone());

        // Send display initialization instructions (ready, name, cursor, size)
        QueryExecutor::send_display_init(&to_client, width, height).await?;
        debug!("Oracle: Sent display init instructions");

        // Try to connect - Oracle connection is blocking and not Send,
        // so we run it in a spawn_blocking context
        let connect_string = format!("//{}:{}/{}", hostname, port, service);
        let username_clone = username.clone();
        let password_clone = password.clone();

        let conn_result = tokio::task::spawn_blocking(move || {
            oracle::Connection::connect(&username_clone, &password_clone, &connect_string)
        })
        .await
        .map_err(|e| HandlerError::ProtocolError(format!("Task join error: {}", e)))?;

        match conn_result {
            Ok(conn) => {
                info!("Oracle: Connected successfully");

                // Run the real mode session
                // Note: oracle::Connection is not Send, so we need to handle it
                // in a way that keeps it on the same thread
                self.run_real_mode_session(
                    conn,
                    &threat_ctx,
                    &security,
                    &recording_config,
                    &mut recorder,
                    &mut executor,
                    &to_client,
                    &mut from_client,
                )
                .await
            }
            Err(e) => {
                let error_msg = format!("Oracle connection failed: {}", e);
                warn!("{}", error_msg);

                crate::handler_helpers::render_connection_error(
                    &mut executor,
                    &to_client,
                    &mut from_client,
                    &error_msg,
                    &[
                        "Check hostname is resolvable",
                        "Verify Oracle server is running",
                        "Check credentials are correct",
                        "Verify network connectivity",
                        "Ensure Oracle Instant Client is installed",
                    ],
                    &mut recorder,
                )
                .await?;
                Err(HandlerError::ConnectionFailed(error_msg))
            }
        }
    }

    async fn health_check(&self) -> guacr_handlers::Result<HealthStatus> {
        Ok(HealthStatus::Healthy)
    }

    async fn stats(&self) -> guacr_handlers::Result<HandlerStats> {
        Ok(HandlerStats::default())
    }
}

/// Result of executing a query against Oracle
struct OracleQueryResult {
    columns: Vec<String>,
    rows: Vec<Vec<String>>,
    #[allow(dead_code)]
    affected_rows: Option<u64>,
    is_error: bool,
    message: String,
}

use guacr_handlers::MultiFormatRecorder;

impl OracleHandler {
    /// Run a real Oracle session
    ///
    /// Note: This uses spawn_blocking for each query since oracle::Connection is not Send
    #[allow(clippy::too_many_arguments)]
    async fn run_real_mode_session(
        &self,
        conn: oracle::Connection,
        threat_ctx: &crate::threat::ThreatContext,
        security: &DatabaseSecuritySettings,
        recording_config: &RecordingConfig,
        recorder: &mut Option<MultiFormatRecorder>,
        executor: &mut QueryExecutor,
        to_client: &mpsc::Sender<Bytes>,
        from_client: &mut mpsc::Receiver<Bytes>,
    ) -> guacr_handlers::Result<()> {
        // Wrap connection in Arc for sharing with spawn_blocking
        // Using parking_lot::Mutex which doesn't poison on panic
        use parking_lot::Mutex;
        let conn = Arc::new(Mutex::new(conn));

        // Send welcome message
        executor
            .write_line("")
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        executor
            .write_line("Connected to Oracle Database")
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        executor
            .write_line("")
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

        // Get database version
        {
            let conn_clone = Arc::clone(&conn);
            let version = tokio::task::spawn_blocking(move || {
                let conn = conn_clone.lock();
                conn.query_row_as::<String>("SELECT banner FROM v$version WHERE ROWNUM = 1", &[])
                    .ok()
            })
            .await
            .ok()
            .flatten();

            if let Some(ver) = version {
                executor
                    .write_line(&ver)
                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            }
        }

        executor
            .write_line("Type 'help' for available commands.")
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        executor
            .write_line("")
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        executor
            .write_prompt()
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

        crate::handler_helpers::send_render(executor, to_client, recorder).await?;

        // Main event loop

        // Debounce timer for batching screen updates (60 FPS)
        let mut debounce = tokio::time::interval(std::time::Duration::from_millis(16));
        debounce.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        // Keepalive to prevent ICE disconnect on idle sessions
        let mut keepalive = KeepAliveManager::new(DEFAULT_KEEPALIVE_INTERVAL_SECS);
        let mut keepalive_interval = tokio::time::interval(std::time::Duration::from_secs(
            DEFAULT_KEEPALIVE_INTERVAL_SECS,
        ));
        keepalive_interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        'outer: loop {
            tokio::select! {
                // Keepalive ping to prevent ICE disconnect on idle sessions
                _ = keepalive_interval.tick() => {
                    if let Some(sync_instr) = keepalive.check() {
                        if send_and_record(to_client, recorder, sync_instr).await.is_err() {
                            debug!("Oracle: Client channel closed during keepalive, stopping");
                            break;
                        }
                    }
                }

                // Debounce tick - render if terminal changed
                _ = debounce.tick() => {
                    // Check if client is still connected before rendering
                    if to_client.is_closed() {
                        debug!("Oracle: Client disconnected, stopping debounce timer");
                        break;
                    }

                    if executor.is_dirty() {
                        if let Ok((_, instructions)) = executor.render_screen().await {
                            for instr in instructions {
                                // Break if send fails (client disconnected)
                                if send_and_record(to_client, recorder, instr).await.is_err() {
                                    debug!("Oracle: Client channel closed during debounce, stopping");
                                    break 'outer;
                                }
                            }
                        }
                    }
                }

                // Process input from client
                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        info!("Oracle: Client disconnected");
                        break 'outer;
                    };
                    match executor.process_input(&msg).await {
                        Ok((needs_render, instructions, pending_query)) => {
                            if let Some(query) = pending_query {
                                info!("Oracle: Query: {}", query);

                        // Check for threats before execution
                        if let Some(threat_desc) = threat_ctx.check_query(&query, "oracle").await {
                            executor
                                .write_error(&format!(
                                    "Session terminated by security policy: {}",
                                    threat_desc
                                ))
                                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                            if let Ok((_, instrs)) = executor.render_screen().await {
                                for instr in instrs {
                                    let _ = send_and_record(to_client, recorder, instr).await;
                                }
                            }
                            return Err(HandlerError::Disconnected(format!(
                                "Threat detected: {}",
                                threat_desc
                            )));
                        }

                        // Record query input
                        record_query_input(recorder, recording_config, &query);

                        // Handle built-in commands
                        match handle_builtin_command(&query, executor, to_client, security).await {
                            Ok(true) => continue,
                            Ok(false) => {}
                            Err(HandlerError::Disconnected(_)) => break 'outer,
                            Err(e) => return Err(e),
                        }

                        // Check for export command
                        if query.to_lowercase().starts_with("\\e ") {
                            let export_query = query[3..].trim().to_string();
                            handle_csv_export_real(
                                &export_query,
                                &conn,
                                executor,
                                to_client,
                                security,
                            )
                            .await?;
                            continue;
                        }

                        // Check for import command
                        if query.to_lowercase().starts_with("\\i ") {
                            let table_name = query[3..].trim().to_string();
                            handle_csv_import_real(
                                &table_name,
                                &conn,
                                executor,
                                to_client,
                                security,
                            )
                            .await?;
                            continue;
                        }

                        // Check read-only mode
                        if let Err(msg) = check_query_allowed(&query, security) {
                            crate::handler_helpers::reject_with_error(executor, to_client, recorder, &msg).await?;
                            continue;
                        }

                        // Execute real query
                        execute_real_query(&query, &conn, executor, to_client).await?;
                        continue;
                    }

                            if needs_render {
                                // Render immediately for special cases (Enter, Escape, etc.)
                                for instr in instructions {
                                    let _ = send_and_record(to_client, recorder, instr).await;
                                }
                            }
                            // For regular keystrokes, debounce timer will handle rendering
                        }
                        Err(e) => {
                            warn!("Oracle: Input processing error: {}", e);
                        }
                    }
                }

                // Client disconnected
                else => {
                    break;
                }
            }
        }

        // Finalize recording
        finalize_recording(recorder.take(), "Oracle");

        send_disconnect(to_client).await;
        info!("Oracle handler ended");
        Ok(())
    }
}

/// Execute a real Oracle query using spawn_blocking
async fn execute_real_query(
    query: &str,
    conn: &Arc<parking_lot::Mutex<oracle::Connection>>,
    executor: &mut QueryExecutor,
    to_client: &mpsc::Sender<Bytes>,
) -> guacr_handlers::Result<()> {
    let query_owned = query.to_string();
    let conn_clone = Arc::clone(conn);

    // Execute query in blocking context
    // Using parking_lot::Mutex which doesn't poison on panic
    let result = tokio::task::spawn_blocking(move || {
        let conn = conn_clone.lock();
        let start_time = std::time::Instant::now();
        let query_upper = query_owned.trim().to_uppercase();

        let is_select = query_upper.starts_with("SELECT")
            || query_upper.starts_with("WITH")
            || query_upper.starts_with("DESCRIBE")
            || query_upper.starts_with("DESC")
            || query_upper.starts_with("SHOW");

        if is_select {
            match conn.query(&query_owned, &[]) {
                Ok(rows) => {
                    let column_info = rows.column_info();
                    let col_count = column_info.len();
                    let col_names: Vec<String> =
                        column_info.iter().map(|c| c.name().to_string()).collect();

                    let mut data_rows: Vec<Vec<String>> = Vec::new();
                    for row_result in rows {
                        match row_result {
                            Ok(row) => {
                                let mut row_data = Vec::new();
                                for i in 0..col_count {
                                    let value: Option<String> = row.get(i).ok();
                                    row_data.push(value.unwrap_or_else(|| "NULL".to_string()));
                                }
                                data_rows.push(row_data);
                            }
                            Err(e) => {
                                warn!("Oracle: Row fetch error: {}", e);
                                break;
                            }
                        }
                    }

                    let elapsed = start_time.elapsed();
                    OracleQueryResult {
                        columns: col_names,
                        rows: data_rows,
                        affected_rows: None,
                        is_error: false,
                        message: format!("{:.3}s", elapsed.as_secs_f64()),
                    }
                }
                Err(e) => OracleQueryResult {
                    columns: vec![],
                    rows: vec![],
                    affected_rows: None,
                    is_error: true,
                    message: format!("ORA-Error: {}", e),
                },
            }
        } else {
            match conn.execute(&query_owned, &[]) {
                Ok(stmt) => {
                    let affected = stmt.row_count().unwrap_or(0);
                    let elapsed = start_time.elapsed();

                    // Auto-commit
                    if let Err(e) = conn.commit() {
                        return OracleQueryResult {
                            columns: vec![],
                            rows: vec![],
                            affected_rows: Some(affected),
                            is_error: true,
                            message: format!("Commit failed: {}", e),
                        };
                    }

                    let msg = if query_upper.starts_with("INSERT")
                        || query_upper.starts_with("UPDATE")
                        || query_upper.starts_with("DELETE")
                    {
                        format!(
                            "{} row(s) affected. ({:.3}s)",
                            affected,
                            elapsed.as_secs_f64()
                        )
                    } else {
                        format!("Statement executed. ({:.3}s)", elapsed.as_secs_f64())
                    };

                    OracleQueryResult {
                        columns: vec![],
                        rows: vec![],
                        affected_rows: Some(affected),
                        is_error: false,
                        message: msg,
                    }
                }
                Err(e) => OracleQueryResult {
                    columns: vec![],
                    rows: vec![],
                    affected_rows: None,
                    is_error: true,
                    message: format!("ORA-Error: {}", e),
                },
            }
        }
    })
    .await
    .map_err(|e| HandlerError::ProtocolError(format!("Task join error: {}", e)))?;

    // Display results
    if result.is_error {
        executor
            .write_error(&result.message)
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
    } else if !result.columns.is_empty() {
        // Display as table
        let query_result = guacr_terminal::QueryResult {
            columns: result.columns,
            rows: result.rows.clone(),
            affected_rows: None,
            execution_time_ms: None,
        };

        executor
            .write_result(&query_result)
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

        executor
            .write_line(&format!(
                "\n{} row(s) selected. ({})",
                result.rows.len(),
                result.message
            ))
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
    } else {
        executor
            .write_success(&result.message)
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
    }

    executor
        .write_prompt()
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

    let (_, instructions) = executor
        .render_screen()
        .await
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
    for instr in instructions {
        to_client
            .send(instr)
            .await
            .map_err(|e| HandlerError::ChannelError(e.to_string()))?;
    }

    Ok(())
}

/// Handle CSV export with real Oracle connection
async fn handle_csv_export_real(
    query: &str,
    conn: &Arc<parking_lot::Mutex<oracle::Connection>>,
    executor: &mut QueryExecutor,
    to_client: &mpsc::Sender<Bytes>,
    security: &DatabaseSecuritySettings,
) -> guacr_handlers::Result<()> {
    use std::sync::atomic::Ordering;

    if security.disable_csv_export {
        executor
            .write_error("CSV export is disabled by your administrator.")
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        executor
            .write_prompt()
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        let (_, instructions) = executor
            .render_screen()
            .await
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        for instr in instructions {
            to_client
                .send(instr)
                .await
                .map_err(|e| HandlerError::ChannelError(e.to_string()))?;
        }
        return Ok(());
    }

    executor
        .write_line("Executing query for export...")
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

    // Execute query in blocking context
    let query_owned = query.to_string();
    let conn_clone = Arc::clone(conn);

    let result = tokio::task::spawn_blocking(move || {
        let conn = conn_clone.lock();
        match conn.query(&query_owned, &[]) {
            Ok(rows) => {
                let column_info = rows.column_info();
                let col_count = column_info.len();
                let col_names: Vec<String> =
                    column_info.iter().map(|c| c.name().to_string()).collect();

                let mut data_rows: Vec<Vec<String>> = Vec::new();
                for row_result in rows {
                    match row_result {
                        Ok(row) => {
                            let mut row_data = Vec::new();
                            for i in 0..col_count {
                                let value: Option<String> = row.get(i).ok();
                                row_data.push(value.unwrap_or_default());
                            }
                            data_rows.push(row_data);
                        }
                        Err(e) => {
                            warn!("Oracle: Row fetch error during export: {}", e);
                            break;
                        }
                    }
                }

                Ok((col_names, data_rows))
            }
            Err(e) => Err(format!("Query failed: {}", e)),
        }
    })
    .await
    .map_err(|e| HandlerError::ProtocolError(format!("Task join error: {}", e)))?;

    match result {
        Ok((columns, rows)) => {
            let query_result = guacr_terminal::QueryResult {
                columns,
                rows: rows.clone(),
                affected_rows: None,
                execution_time_ms: None,
            };

            let filename = generate_csv_filename(query, "oracle");
            let stream_idx = STREAM_INDEX.fetch_add(1, Ordering::SeqCst);
            let mut exporter = CsvExporter::new(stream_idx);

            executor
                .write_line(&format!("Beginning CSV download ({} rows)...", rows.len()))
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

            let (_, instructions) = executor
                .render_screen()
                .await
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            for instr in instructions {
                to_client
                    .send(instr)
                    .await
                    .map_err(|e| HandlerError::ChannelError(e.to_string()))?;
            }

            let file_instr = exporter.start_download(&filename);
            to_client
                .send(file_instr)
                .await
                .map_err(|e| HandlerError::ChannelError(e.to_string()))?;

            match exporter.export_query_result(&query_result, to_client).await {
                Ok(()) => {
                    executor
                        .write_success("Download complete.")
                        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                }
                Err(e) => {
                    executor
                        .write_error(&format!("Export failed: {}", e))
                        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                }
            }
        }
        Err(e) => {
            executor
                .write_error(&e)
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        }
    }

    executor
        .write_prompt()
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
    let (_, instructions) = executor
        .render_screen()
        .await
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
    for instr in instructions {
        to_client
            .send(instr)
            .await
            .map_err(|e| HandlerError::ChannelError(e.to_string()))?;
    }

    Ok(())
}

/// Handle CSV import with real Oracle connection
async fn handle_csv_import_real(
    table_name: &str,
    conn: &Arc<parking_lot::Mutex<oracle::Connection>>,
    executor: &mut QueryExecutor,
    to_client: &mpsc::Sender<Bytes>,
    security: &DatabaseSecuritySettings,
) -> guacr_handlers::Result<()> {
    if security.disable_csv_import {
        executor
            .write_error("CSV import is disabled by your administrator.")
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        executor
            .write_prompt()
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        let (_, instructions) = executor
            .render_screen()
            .await
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        for instr in instructions {
            to_client
                .send(instr)
                .await
                .map_err(|e| HandlerError::ChannelError(e.to_string()))?;
        }
        return Ok(());
    }

    if security.base.read_only {
        executor
            .write_error("Import blocked: read-only mode is enabled.")
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        executor
            .write_prompt()
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        let (_, instructions) = executor
            .render_screen()
            .await
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        for instr in instructions {
            to_client
                .send(instr)
                .await
                .map_err(|e| HandlerError::ChannelError(e.to_string()))?;
        }
        return Ok(());
    }

    if table_name.is_empty() {
        executor
            .write_error("Usage: \\i <table_name>")
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        executor
            .write_prompt()
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        let (_, instructions) = executor
            .render_screen()
            .await
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        for instr in instructions {
            to_client
                .send(instr)
                .await
                .map_err(|e| HandlerError::ChannelError(e.to_string()))?;
        }
        return Ok(());
    }

    executor
        .write_line(&format!("Import into table: {}", table_name))
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
    executor
        .write_line("Demo: Importing sample data...")
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

    // Demo data
    let sample_csv = "ID,NAME,VALUE\n1,Test,100\n2,Demo,200";
    let mut importer = CsvImporter::new(1);

    importer
        .receive_blob(sample_csv.as_bytes())
        .map_err(HandlerError::ProtocolError)?;

    let csv_data = importer
        .finish_receive()
        .map_err(HandlerError::ProtocolError)?;

    executor
        .write_line(&format!(
            "Parsed {} columns, {} rows",
            csv_data.headers.len(),
            csv_data.row_count()
        ))
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

    // Generate Oracle INSERT statements and execute
    let table_name_owned = table_name.to_string();
    let headers = csv_data.headers.clone();
    let rows = csv_data.rows.clone();
    let conn_clone = Arc::clone(conn);

    let (success_count, error_count) = tokio::task::spawn_blocking(move || {
        let conn = conn_clone.lock();
        let columns = headers.join("\", \"");
        let mut success = 0;
        let mut errors = 0;

        for row in &rows {
            if row.len() != headers.len() {
                continue;
            }

            let values: Vec<String> = row
                .iter()
                .map(|v| {
                    if v.eq_ignore_ascii_case("null") || v.is_empty() {
                        "NULL".to_string()
                    } else if v.parse::<f64>().is_ok() {
                        v.to_string()
                    } else {
                        format!("'{}'", v.replace('\'', "''"))
                    }
                })
                .collect();

            let insert = format!(
                "INSERT INTO \"{}\" (\"{}\") VALUES ({})",
                table_name_owned,
                columns,
                values.join(", ")
            );

            match conn.execute(&insert, &[]) {
                Ok(_) => success += 1,
                Err(e) => {
                    errors += 1;
                    warn!("Oracle import error: {}", e);
                }
            }
        }

        if let Err(e) = conn.commit() {
            warn!("Oracle commit error: {}", e);
        }

        (success, errors)
    })
    .await
    .map_err(|e| HandlerError::ProtocolError(format!("Task join error: {}", e)))?;

    executor
        .write_success(&format!(
            "Import complete: {} rows inserted, {} errors",
            success_count, error_count
        ))
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

    executor
        .write_prompt()
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
    let (_, instructions) = executor
        .render_screen()
        .await
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
    for instr in instructions {
        to_client
            .send(instr)
            .await
            .map_err(|e| HandlerError::ChannelError(e.to_string()))?;
    }

    Ok(())
}

/// Handle built-in commands
async fn handle_builtin_command(
    query: &str,
    executor: &mut QueryExecutor,
    to_client: &mpsc::Sender<Bytes>,
    security: &DatabaseSecuritySettings,
) -> guacr_handlers::Result<bool> {
    let query_lower = query.to_lowercase();

    match query_lower.as_str() {
        "help" | "?" => {
            executor
                .write_line("")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("Oracle SQL*Plus Commands:")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("SQL Commands:")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  SELECT ... FROM ...   Execute query")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  DESC table_name       Describe table")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("SQL*Plus Commands:")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  SHOW USER             Show current user")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  QUIT/EXIT             Disconnect")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

            if !security.disable_csv_export {
                executor
                    .write_line("  \\e <query>            Export query as CSV")
                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            }
            if !security.disable_csv_import && !security.base.read_only {
                executor
                    .write_line("  \\i <table>            Import CSV into table")
                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            }

            executor
                .write_line("")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("Example queries:")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  SELECT SYSDATE FROM DUAL;")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  SELECT * FROM ALL_TABLES WHERE ROWNUM <= 10;")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_prompt()
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

            let (_, instructions) = executor
                .render_screen()
                .await
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            for instr in instructions {
                to_client
                    .send(instr)
                    .await
                    .map_err(|e| HandlerError::ChannelError(e.to_string()))?;
            }
            return Ok(true);
        }
        "quit" | "exit" | "bye" | "\\q" => {
            executor
                .write_line("Bye")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            let (_, instructions) = executor
                .render_screen()
                .await
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            for instr in instructions {
                to_client
                    .send(instr)
                    .await
                    .map_err(|e| HandlerError::ChannelError(e.to_string()))?;
            }
            return Err(HandlerError::Disconnected(
                "User requested disconnect".to_string(),
            ));
        }
        _ => {}
    }

    Ok(false)
}

// Event-based handler implementation
#[async_trait]
impl EventBasedHandler for OracleHandler {
    fn name(&self) -> &str {
        "oracle"
    }

    async fn connect_with_events(
        &self,
        params: HashMap<String, String>,
        callback: Arc<dyn EventCallback>,
        from_client: mpsc::Receiver<Bytes>,
        _video_tx: Option<Arc<dyn VideoOutput>>,
    ) -> Result<(), HandlerError> {
        guacr_handlers::connect_with_event_adapter(
            |params, to_client, from_client, _video_tx| {
                self.connect(params, to_client, from_client, _video_tx)
            },
            params,
            callback,
            from_client,
            _video_tx,
            4096,
        )
        .await
    }
}
