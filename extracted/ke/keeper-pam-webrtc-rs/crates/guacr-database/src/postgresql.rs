use async_trait::async_trait;
use bytes::Bytes;
use guacr_handlers::{
    send_disconnect, EventBasedHandler, EventCallback, HandlerError, HandlerStats, HealthStatus,
    KeepAliveManager, ProtocolHandler, RecordingConfig, VideoOutput,
    DEFAULT_KEEPALIVE_INTERVAL_SECS,
};
use guacr_terminal::QueryResult;
use log::{debug, info, warn};
use sqlx::postgres::{PgPoolOptions, PgRow};
use sqlx::{Column, Row, TypeInfo};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::mpsc;

#[cfg(feature = "threat-detection")]
use guacr_threat_detection::{SessionGuard, ThreatDetector};

use crate::csv_export::{generate_csv_filename, CsvExporter};
use crate::csv_import::CsvImporter;
use crate::handler_helpers::{
    reject_with_error, render_connection_error, render_connection_success, send_render,
};
use crate::query_executor::{execute_with_timing, QueryExecutor};
use crate::recording::{
    finalize_recording, init_recording, record_error_output, record_query_input,
    record_query_output, send_and_record,
};
use crate::security::{
    check_csv_export_allowed, check_csv_import_allowed, check_query_allowed, is_postgres_copy_in,
    is_postgres_copy_out, DatabaseSecuritySettings,
};

use std::sync::atomic::AtomicI32;
use std::time::Duration;

/// Global stream index counter for unique stream IDs
static STREAM_INDEX: AtomicI32 = AtomicI32::new(1000);

/// PostgreSQL protocol handler
///
/// Provides interactive SQL terminal access to PostgreSQL databases.
pub struct PostgreSqlHandler {
    config: PostgreSqlConfig,
}

#[derive(Debug, Clone)]
pub struct PostgreSqlConfig {
    pub default_port: u16,
    pub connection_timeout_secs: u64,
    pub query_timeout_secs: u64,
    pub max_connections: u32,
}

impl Default for PostgreSqlConfig {
    fn default() -> Self {
        Self {
            default_port: 5432,
            connection_timeout_secs: guacr_handlers::DEFAULT_CONNECTION_TIMEOUT_SECS,
            query_timeout_secs: 300,
            max_connections: 5,
        }
    }
}

impl PostgreSqlHandler {
    pub fn new(config: PostgreSqlConfig) -> Self {
        Self { config }
    }

    pub fn with_defaults() -> Self {
        Self::new(PostgreSqlConfig::default())
    }
}

#[async_trait]
impl ProtocolHandler for PostgreSqlHandler {
    fn name(&self) -> &str {
        "postgres"
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
        info!("PostgreSQL handler starting");

        // Initialize rustls crypto provider (required for rustls 0.23+)
        let _ = rustls::crypto::ring::default_provider().install_default();

        // Parse security settings
        let security = DatabaseSecuritySettings::from_params(&params);
        if security.base.read_only {
            info!("PostgreSQL: Read-only mode enabled");
        }

        // Parse recording configuration
        let recording_config = RecordingConfig::from_params(&params);

        // Parse connection parameters
        let hostname = params
            .get("hostname")
            .ok_or_else(|| HandlerError::MissingParameter("hostname".to_string()))?;
        let port: u16 = params
            .get("port")
            .and_then(|p| p.parse().ok())
            .unwrap_or(self.config.default_port);
        let username = params
            .get("username")
            .ok_or_else(|| HandlerError::MissingParameter("username".to_string()))?;
        let password = params
            .get("password")
            .ok_or_else(|| HandlerError::MissingParameter("password".to_string()))?;
        let database = params
            .get("database")
            .map(|s| s.as_str())
            .unwrap_or("postgres");

        info!(
            "PostgreSQL: Connecting to {}@{}:{}/{}",
            username, hostname, port, database
        );

        let (width, height, cols, rows) = crate::handler_helpers::parse_display_size(&params);

        info!(
            "PostgreSQL: Display size {}x{} px → {}x{} chars",
            width, height, cols, rows
        );

        // Create query executor with PostgreSQL prompt and correct dimensions
        let prompt = if security.base.read_only {
            "postgres [RO]=# "
        } else {
            "postgres=# "
        };
        let mut executor = QueryExecutor::new_with_size(prompt, "postgresql", rows, cols)
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        executor.use_binary = params.get("binary").map(|v| v == "true").unwrap_or(false);

        // Initialize recording if enabled
        let mut recorder = init_recording(&recording_config, &params, "PostgreSQL", cols, rows);

        // Initialize threat detection if enabled
        #[cfg(feature = "threat-detection")]
        let threat_detector = Arc::new(
            ThreatDetector::new(crate::threat::threat_config_from_params(&params))
                .map_err(|e| HandlerError::ProtocolError(format!("Threat detector init: {}", e)))?,
        );
        #[cfg(feature = "threat-detection")]
        let threat_session_id = crate::threat::new_session_id();
        #[cfg(feature = "threat-detection")]
        let _threat_guard = SessionGuard::new(threat_detector.clone(), threat_session_id.clone());

        // Send display initialization instructions (ready, name, cursor, size)
        QueryExecutor::send_display_init(&to_client, width, height).await?;
        debug!("PostgreSQL: Sent display init instructions");

        // NOTE: Don't render initial screen yet - wait until after connection
        // This matches SSH behavior and prevents rendering at wrong dimensions

        // Build PostgreSQL connection URL with proper URL encoding for special characters
        // This is critical for passwords containing: | & ? @ : / # %
        let encoded_username = urlencoding::encode(username);
        let encoded_password = urlencoding::encode(password);
        let encoded_database = urlencoding::encode(database);
        let connection_url = format!(
            "postgres://{}:{}@{}:{}/{}",
            encoded_username, encoded_password, hostname, port, encoded_database
        );

        debug!(
            "PostgreSQL: Connection URL: {}",
            connection_url.replace(&encoded_password.to_string(), "***")
        );

        // Connect to PostgreSQL using sqlx
        let pool = match PgPoolOptions::new()
            .max_connections(self.config.max_connections)
            .acquire_timeout(std::time::Duration::from_secs(
                self.config.connection_timeout_secs,
            ))
            .connect(&connection_url)
            .await
        {
            Ok(pool) => {
                info!("PostgreSQL: Connected successfully");

                let info = [
                    format!("Connected to PostgreSQL at {}:{}", hostname, port),
                    format!("Database: {}", database),
                ];
                let info_refs: Vec<&str> = info.iter().map(|s| s.as_str()).collect();
                debug!("PostgreSQL: Rendering initial screen with prompt");
                render_connection_success(
                    &mut executor,
                    &to_client,
                    &info_refs,
                    &security,
                    &mut recorder,
                )
                .await?;
                debug!("PostgreSQL: Initial screen sent successfully");

                pool
            }
            Err(e) => {
                let error_msg = format!("Connection failed: {}", e);
                warn!("PostgreSQL: {}", error_msg);

                render_connection_error(
                    &mut executor,
                    &to_client,
                    &mut from_client,
                    &error_msg,
                    &[
                        "Check hostname is resolvable",
                        "Verify PostgreSQL server is running",
                        "Check pg_hba.conf allows connections",
                        "Verify credentials are correct",
                    ],
                    &mut recorder,
                )
                .await?;
                return Err(HandlerError::ConnectionFailed(error_msg));
            }
        };

        // Event loop
        // NOTE: Screen was already rendered above after connection success

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
                        if send_and_record(&to_client, &mut recorder, sync_instr).await.is_err() {
                            debug!("PostgreSQL: Client channel closed during keepalive, stopping");
                            break;
                        }
                    }
                }

                // Debounce tick - render if terminal or input changed
                _ = debounce.tick() => {
                    // Check if client is still connected before rendering
                    if to_client.is_closed() {
                        debug!("PostgreSQL: Client disconnected, stopping debounce timer");
                        break;
                    }

                    if executor.is_dirty() {
                        let (_, instructions) = executor
                            .render_screen()
                            .await
                            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                        for instr in instructions {
                            // Break if send fails (client disconnected)
                            if send_and_record(&to_client, &mut recorder, instr).await.is_err() {
                                debug!("PostgreSQL: Client channel closed during debounce, stopping");
                                break 'outer;
                            }
                        }
                    }
                }

                // Process input from client
                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        info!("PostgreSQL: Client disconnected");
                        break 'outer;
                    };
                    match executor.process_input(&msg).await {
                        Ok((needs_render, instructions, pending_query)) => {
                    if let Some(query) = pending_query {
                        info!("PostgreSQL: Executing query: {}", query);

                        // Check for threats before execution
                        #[cfg(feature = "threat-detection")]
                        crate::handler_helpers::maybe_terminate_on_threat(
                            &threat_detector, &threat_session_id, &query,
                            username, hostname, "postgres",
                            &mut executor, &to_client, &mut recorder,
                        )
                        .await?;

                        // Record query input
                        record_query_input(&mut recorder, &recording_config, &query);

                        // Handle built-in commands
                        match handle_builtin_command(&query, &mut executor, &to_client, &security)
                            .await
                        {
                            Ok(true) => continue,
                            Ok(false) => {}
                            Err(HandlerError::Disconnected(_)) => break 'outer,
                            Err(e) => return Err(e),
                        }

                        // Check for export command: \e <query>
                        if query.to_lowercase().starts_with("\\e ") {
                            let export_query = query[3..].trim();
                            handle_csv_export(
                                export_query,
                                &pool,
                                &mut executor,
                                &to_client,
                                &security,
                            )
                            .await?;
                            continue;
                        }

                        // Check for import command: \i <table>
                        if query.to_lowercase().starts_with("\\i ") {
                            let table_name = query[3..].trim();
                            handle_csv_import(
                                table_name,
                                &pool,
                                &mut executor,
                                &to_client,
                                &security,
                            )
                            .await?;
                            continue;
                        }

                        // Security checks
                        // Check for COPY TO (export)
                        if is_postgres_copy_out(&query) {
                            if let Err(msg) = check_csv_export_allowed(&security) {
                                reject_with_error(&mut executor, &to_client, &mut recorder, &msg).await?;
                                continue;
                            }
                        }

                        // Check for COPY FROM (import)
                        if is_postgres_copy_in(&query) {
                            if let Err(msg) = check_csv_import_allowed(&security) {
                                reject_with_error(&mut executor, &to_client, &mut recorder, &msg).await?;
                                continue;
                            }
                        }

                        // Check read-only mode
                        if let Err(msg) = check_query_allowed(&query, &security) {
                            reject_with_error(&mut executor, &to_client, &mut recorder, &msg).await?;
                            continue;
                        }

                        // Execute query with timeout
                        let timeout_secs = self.config.query_timeout_secs;
                        match tokio::time::timeout(
                            Duration::from_secs(timeout_secs),
                            execute_with_timing(|| execute_postgres_query(&pool, &query)),
                        ).await {
                            Err(_elapsed) => {
                                let msg = format!("Query timed out after {}s", timeout_secs);
                                record_error_output(&mut recorder, &msg);
                                executor
                                    .write_error(&msg)
                                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                            }
                            Ok(Ok(exec_result)) => {
                                let result = exec_result.into_query_result();

                                // Record query output
                                record_query_output(&mut recorder, &result);

                                executor
                                    .write_result(&result)
                                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                            }
                            Ok(Err(e)) => {
                                // Record error output
                                record_error_output(&mut recorder, &e);

                                executor
                                    .write_error(&e)
                                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                            }
                        }

                        send_render(&mut executor, &to_client, &mut recorder).await?;
                        continue;
                    }

                    if needs_render {
                        // Render immediately for special cases (Enter, Escape, etc.)
                        for instr in instructions {
                            let _ = send_and_record(&to_client, &mut recorder, instr).await;
                        }
                    }
                    // For regular keystrokes, debounce timer will handle rendering
                        }
                        Err(e) => {
                            warn!("PostgreSQL: Input processing error: {}", e);
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
        finalize_recording(recorder, "PostgreSQL");

        send_disconnect(&to_client).await;
        info!("PostgreSQL handler ended");
        Ok(())
    }

    async fn health_check(&self) -> guacr_handlers::Result<HealthStatus> {
        Ok(HealthStatus::Healthy)
    }

    async fn stats(&self) -> guacr_handlers::Result<HandlerStats> {
        Ok(HandlerStats::default())
    }
}

/// Execute PostgreSQL query and return results
async fn execute_postgres_query(pool: &sqlx::PgPool, query: &str) -> Result<QueryResult, String> {
    // Use sqlx::query for raw SQL execution
    let rows: Vec<PgRow> = sqlx::query(query)
        .fetch_all(pool)
        .await
        .map_err(|e| format!("Query error: {}", e))?;

    if rows.is_empty() {
        return Ok(QueryResult {
            columns: vec![],
            rows: vec![],
            affected_rows: Some(0),
            execution_time_ms: None,
        });
    }

    // Get column names from first row
    let columns: Vec<String> = rows[0]
        .columns()
        .iter()
        .map(|col| col.name().to_string())
        .collect();

    let mut query_result = QueryResult::new(columns.clone());

    for row in &rows {
        let mut row_data = Vec::new();
        for (idx, col) in row.columns().iter().enumerate() {
            let value = pg_value_to_string(row, idx, col.type_info());
            row_data.push(value);
        }
        query_result.add_row(row_data);
    }

    Ok(query_result)
}

/// Convert PostgreSQL value to string
fn pg_value_to_string(row: &PgRow, idx: usize, type_info: &sqlx::postgres::PgTypeInfo) -> String {
    let type_name = type_info.name();

    // Try to get value based on type
    match type_name {
        "INT2" | "INT4" | "INT8" => row
            .try_get::<i64, _>(idx)
            .map(|v| v.to_string())
            .unwrap_or_else(|_| "NULL".to_string()),
        "FLOAT4" | "FLOAT8" | "NUMERIC" => row
            .try_get::<f64, _>(idx)
            .map(|v| format!("{:.6}", v))
            .unwrap_or_else(|_| "NULL".to_string()),
        "BOOL" => row
            .try_get::<bool, _>(idx)
            .map(|v| if v { "true" } else { "false" }.to_string())
            .unwrap_or_else(|_| "NULL".to_string()),
        "TEXT" | "VARCHAR" | "CHAR" | "NAME" => row
            .try_get::<String, _>(idx)
            .unwrap_or_else(|_| "NULL".to_string()),
        "TIMESTAMP" | "TIMESTAMPTZ" => row
            .try_get::<chrono::NaiveDateTime, _>(idx)
            .map(|v| v.format("%Y-%m-%d %H:%M:%S").to_string())
            .or_else(|_| {
                row.try_get::<chrono::DateTime<chrono::Utc>, _>(idx)
                    .map(|v| v.format("%Y-%m-%d %H:%M:%S %Z").to_string())
            })
            .unwrap_or_else(|_| "NULL".to_string()),
        "DATE" => row
            .try_get::<chrono::NaiveDate, _>(idx)
            .map(|v| v.format("%Y-%m-%d").to_string())
            .unwrap_or_else(|_| "NULL".to_string()),
        "TIME" => row
            .try_get::<chrono::NaiveTime, _>(idx)
            .map(|v| v.format("%H:%M:%S").to_string())
            .unwrap_or_else(|_| "NULL".to_string()),
        "UUID" => row
            .try_get::<uuid::Uuid, _>(idx)
            .map(|v| v.to_string())
            .unwrap_or_else(|_| "NULL".to_string()),
        "JSON" | "JSONB" => row
            .try_get::<serde_json::Value, _>(idx)
            .map(|v| v.to_string())
            .unwrap_or_else(|_| "NULL".to_string()),
        _ => {
            // Fallback: try as string
            row.try_get::<String, _>(idx)
                .unwrap_or_else(|_| format!("<{}>", type_name))
        }
    }
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
        "help" | "\\h" | "\\?" => {
            executor
                .write_line("")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("Available commands:")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  help, \\h     Show this help")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  quit, \\q     Disconnect")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  \\l           List databases")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  \\dt          List tables")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  \\d table     Describe table")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

            // Show export/import commands if not disabled
            if !security.disable_csv_export {
                executor
                    .write_line("  \\e <query>   Export query results as CSV")
                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            }
            if !security.disable_csv_import && !security.base.read_only {
                executor
                    .write_line("  \\i <table>   Import CSV data into table")
                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            }

            // Show security status in help
            if security.base.read_only {
                executor
                    .write_line("")
                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                executor
                    .write_line("Note: READ-ONLY mode is enabled.")
                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                executor
                    .write_line("      INSERT/UPDATE/DELETE/DROP are disabled.")
                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            }

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
        "quit" | "exit" | "\\q" | "bye" => {
            return Err(crate::handler_helpers::handle_quit(executor, to_client, &mut None).await);
        }
        _ => {}
    }

    Ok(false)
}

/// Handle CSV export for a query
async fn handle_csv_export(
    query: &str,
    pool: &sqlx::PgPool,
    executor: &mut QueryExecutor,
    to_client: &mpsc::Sender<Bytes>,
    security: &DatabaseSecuritySettings,
) -> guacr_handlers::Result<()> {
    use std::sync::atomic::Ordering;

    // Check if export is allowed
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

    // Execute the query
    match execute_postgres_query(pool, query).await {
        Ok(result) => {
            if result.rows.is_empty() {
                executor
                    .write_line("Query returned no results to export.")
                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            } else {
                // Generate filename and create exporter
                let filename = generate_csv_filename(query, "postgres");
                let stream_idx = STREAM_INDEX.fetch_add(1, Ordering::SeqCst);
                let mut exporter = CsvExporter::new(stream_idx);

                executor
                    .write_line(&format!(
                        "Beginning CSV download ({} rows). Press Ctrl+C to cancel.",
                        result.rows.len()
                    ))
                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

                // Send file instruction to start download
                let file_instr = exporter.start_download(&filename);
                to_client
                    .send(file_instr)
                    .await
                    .map_err(|e| HandlerError::ChannelError(e.to_string()))?;

                // Export the data
                match exporter.export_query_result(&result, to_client).await {
                    Ok(()) => {
                        executor
                            .write_line("Download complete.")
                            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                    }
                    Err(e) => {
                        executor
                            .write_error(&format!("Export failed: {}", e))
                            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                    }
                }
            }
        }
        Err(e) => {
            executor
                .write_error(&format!("Query failed: {}", e))
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

/// Handle CSV import for a table
async fn handle_csv_import(
    table_name: &str,
    pool: &sqlx::PgPool,
    executor: &mut QueryExecutor,
    to_client: &mpsc::Sender<Bytes>,
    security: &DatabaseSecuritySettings,
) -> guacr_handlers::Result<()> {
    // Check if import is allowed
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

    // Check read-only mode
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
    let sample_csv = "id,name,value\n1,Test,100\n2,Demo,200";
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

    // Generate and execute INSERT statements
    let inserts = importer
        .generate_postgres_inserts(table_name)
        .map_err(HandlerError::ProtocolError)?;

    let mut success_count = 0;
    let mut error_count = 0;

    for insert in &inserts {
        match sqlx::query(insert).execute(pool).await {
            Ok(_) => success_count += 1,
            Err(e) => {
                error_count += 1;
                warn!("Import error: {}", e);
            }
        }
    }

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

// Event-based handler implementation
#[async_trait]
impl EventBasedHandler for PostgreSqlHandler {
    fn name(&self) -> &str {
        "postgres"
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
