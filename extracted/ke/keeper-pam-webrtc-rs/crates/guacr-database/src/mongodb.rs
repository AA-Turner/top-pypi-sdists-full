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
use crate::handler_helpers::{
    reject_with_error, render_connection_error, render_connection_success, send_render,
};
use crate::query_executor::QueryExecutor;
use crate::recording::{
    finalize_recording, init_recording, record_error_output, record_query_input, send_and_record,
};
use crate::security::DatabaseSecuritySettings;

use std::sync::atomic::AtomicI32;

/// Global stream index counter for unique stream IDs
static STREAM_INDEX: AtomicI32 = AtomicI32::new(5000);

/// MongoDB handler
///
/// Provides interactive MongoDB shell access for NoSQL operations.
pub struct MongoDbHandler {
    config: MongoDbConfig,
}

#[derive(Debug, Clone)]
pub struct MongoDbConfig {
    pub default_port: u16,
    pub require_tls: bool,
    pub connection_timeout_secs: u64,
}

impl Default for MongoDbConfig {
    fn default() -> Self {
        Self {
            default_port: 27017,
            require_tls: false, // TLS configurable
            connection_timeout_secs: guacr_handlers::DEFAULT_CONNECTION_TIMEOUT_SECS,
        }
    }
}

impl MongoDbHandler {
    pub fn new(config: MongoDbConfig) -> Self {
        Self { config }
    }

    pub fn with_defaults() -> Self {
        Self::new(MongoDbConfig::default())
    }
}

#[async_trait]
impl ProtocolHandler for MongoDbHandler {
    fn name(&self) -> &str {
        "mongodb"
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
        info!("[conn={}] MongoDB handler starting", conn_id);

        // Parse security settings
        let security = DatabaseSecuritySettings::from_params(&params);
        if security.base.read_only {
            info!("[conn={}] MongoDB: Read-only mode enabled", conn_id);
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
            .unwrap_or("admin");
        let auth_source = params
            .get("authSource")
            .map(|s| s.as_str())
            .unwrap_or("admin");

        info!(
            "[conn={}] MongoDB: Connecting to {}@{}:{}/{}",
            conn_id, username, hostname, port, database
        );

        let (width, height, cols, rows) = crate::handler_helpers::parse_display_size(&params);

        info!(
            "[conn={}] MongoDB: Display size {}x{} px → {}x{} chars",
            conn_id, width, height, cols, rows
        );

        // Create query executor with MongoDB prompt and correct dimensions
        let prompt = if security.base.read_only {
            "[RO]> "
        } else {
            "> "
        };
        let mut executor = QueryExecutor::new_with_size(prompt, "mongodb", rows, cols)
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

        // Initialize recording if enabled
        let mut recorder = init_recording(&recording_config, &params, "MongoDB", cols, rows);

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
        debug!("[conn={}] MongoDB: Sent display init instructions", conn_id);

        // NOTE: Don't render initial screen yet - wait until after connection
        // This matches SSH behavior and prevents rendering at wrong dimensions

        // Build MongoDB connection URI with proper URL encoding for special characters
        // This is critical for passwords containing: | & ? @ : / # %
        let encoded_username = urlencoding::encode(username);
        let encoded_password = urlencoding::encode(password);
        let encoded_database = urlencoding::encode(database);
        let encoded_auth_source = urlencoding::encode(auth_source);
        let tls_param = if self.config.require_tls {
            "&tls=true"
        } else {
            ""
        };
        let connection_uri = format!(
            "mongodb://{}:{}@{}:{}/{}?authSource={}{}",
            encoded_username,
            encoded_password,
            hostname,
            port,
            encoded_database,
            encoded_auth_source,
            tls_param
        );

        debug!(
            "[conn={}] MongoDB: Connection URI: {}",
            conn_id,
            connection_uri.replace(&encoded_password.to_string(), "***")
        );

        // Connect to MongoDB
        use mongodb::{options::ClientOptions, Client};

        let client_options = match ClientOptions::parse(&connection_uri).await {
            Ok(mut opts) => {
                opts.connect_timeout = Some(std::time::Duration::from_secs(
                    self.config.connection_timeout_secs,
                ));
                opts.app_name = Some("guacr-mongodb".to_string());
                opts
            }
            Err(e) => {
                let error_msg = format!("Failed to parse MongoDB URI: {}", e);
                warn!("[conn={}] MongoDB: {}", conn_id, error_msg);

                render_connection_error(
                    &mut executor,
                    &to_client,
                    &mut from_client,
                    &error_msg,
                    &[
                        "Check hostname and port",
                        "Verify MongoDB server is running",
                        "Check credentials and authSource",
                        "Verify network connectivity",
                    ],
                    &mut recorder,
                )
                .await?;
                return Err(HandlerError::ConnectionFailed(error_msg));
            }
        };

        let client = match Client::with_options(client_options) {
            Ok(client) => client,
            Err(e) => {
                let error_msg = format!("Failed to create MongoDB client: {}", e);
                warn!("[conn={}] MongoDB: {}", conn_id, error_msg);

                render_connection_error(
                    &mut executor,
                    &to_client,
                    &mut from_client,
                    &error_msg,
                    &[
                        "Check hostname and port",
                        "Verify MongoDB server is running",
                        "Check credentials and authSource",
                        "Verify network connectivity",
                    ],
                    &mut recorder,
                )
                .await?;
                return Err(HandlerError::ConnectionFailed(error_msg));
            }
        };

        // Test connection by pinging the database
        let db = client.database(database);
        match db.run_command(mongodb::bson::doc! { "ping": 1 }).await {
            Ok(_) => {
                info!("[conn={}] MongoDB: Connected successfully", conn_id);

                let info = [
                    format!("Connected to MongoDB at {}:{}", hostname, port),
                    format!("Database: {}", database),
                ];
                let info_refs: Vec<&str> = info.iter().map(|s| s.as_str()).collect();
                debug!(
                    "[conn={}] MongoDB: Rendering initial screen with prompt",
                    conn_id
                );
                render_connection_success(
                    &mut executor,
                    &to_client,
                    &info_refs,
                    &security,
                    &mut recorder,
                )
                .await?;
                debug!(
                    "[conn={}] MongoDB: Initial screen sent successfully",
                    conn_id
                );
            }
            Err(e) => {
                let error_msg = format!("MongoDB connection test failed: {}", e);
                warn!("[conn={}] MongoDB: {}", conn_id, error_msg);

                render_connection_error(
                    &mut executor,
                    &to_client,
                    &mut from_client,
                    &error_msg,
                    &[
                        "Check hostname and port",
                        "Verify MongoDB server is running",
                        "Check credentials and authSource",
                        "Verify network connectivity",
                    ],
                    &mut recorder,
                )
                .await?;
                return Err(HandlerError::ConnectionFailed(error_msg));
            }
        }

        // Track current database
        let mut current_db = database.to_string();

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
                            debug!("[conn={}] MongoDB: Client channel closed during keepalive, stopping", conn_id);
                            break;
                        }
                    }
                }

                // Debounce tick - render if terminal or input changed
                _ = debounce.tick() => {
                    // Check if client is still connected before rendering
                    if to_client.is_closed() {
                        debug!("[conn={}] MongoDB: Client disconnected, stopping debounce timer", conn_id);
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
                                debug!("[conn={}] MongoDB: Client channel closed during debounce, stopping", conn_id);
                                break 'outer;
                            }
                        }
                    }
                }

                // Process input from client
                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        info!("[conn={}] MongoDB: Client disconnected", conn_id);
                        break 'outer;
                    };
                    match executor.process_input(&msg).await {
                        Ok((needs_render, instructions, pending_query)) => {
                    if let Some(command) = pending_query {
                        debug!("[conn={}] MongoDB: Executing command: {}", conn_id, command);

                        // Check for threats before execution
                        #[cfg(feature = "threat-detection")]
                        crate::handler_helpers::maybe_terminate_on_threat(
                            &threat_detector, &threat_session_id, &command,
                            username, hostname, "mongodb",
                            &mut executor, &to_client, &mut recorder,
                        )
                        .await?;

                        // Record query input
                        record_query_input(&mut recorder, &recording_config, &command);

                        // Handle built-in commands
                        if let Some(new_db) = handle_builtin_command(
                            &command,
                            &mut executor,
                            &to_client,
                            &client,
                            &current_db,
                            &security,
                        )
                        .await?
                        {
                            current_db = new_db;
                            continue;
                        }

                        // Check for export command: \e <collection>
                        if command.to_lowercase().starts_with("\\e ") {
                            let collection = command[3..].trim();
                            handle_csv_export(
                                collection,
                                &client,
                                &current_db,
                                &mut executor,
                                &to_client,
                                &security,
                                &conn_id,
                            )
                            .await?;
                            continue;
                        }

                        // Check for import command: \i <collection>
                        if command.to_lowercase().starts_with("\\i ") {
                            let collection = command[3..].trim();
                            handle_csv_import(
                                collection,
                                &mut executor,
                                &to_client,
                                &security,
                            )
                            .await?;
                            continue;
                        }

                        // Check read-only mode for modifying commands
                        if security.base.read_only && is_mongodb_modifying_command(&command) {
                            reject_with_error(&mut executor, &to_client, &mut recorder, "Command blocked: read-only mode is enabled.").await?;
                            continue;
                        }

                        // Execute MongoDB command
                        let db = client.database(&current_db);
                        match execute_mongodb_command(&db, &command).await {
                            Ok(result) => {
                                for line in result.lines() {
                                    executor

                                        .write_line(line)
                                        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                                }
                            }
                            Err(e) => {
                                // Record error output
                                record_error_output(&mut recorder, &e);

                                executor

                                    .write_error(&e)
                                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                            }
                        }

                        executor
                            .write_prompt()
                            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

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
                            warn!("[conn={}] MongoDB: Input processing error: {}", conn_id, e);
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
        finalize_recording(recorder, "MongoDB");

        send_disconnect(&to_client).await;
        info!("[conn={}] MongoDB handler ended", conn_id);
        Ok(())
    }

    async fn health_check(&self) -> guacr_handlers::Result<HealthStatus> {
        Ok(HealthStatus::Healthy)
    }

    async fn stats(&self) -> guacr_handlers::Result<HandlerStats> {
        Ok(HandlerStats::default())
    }
}

/// Execute MongoDB command and return result as string
async fn execute_mongodb_command(db: &mongodb::Database, command: &str) -> Result<String, String> {
    use mongodb::bson::doc;

    // Parse simple commands
    let parts: Vec<&str> = command.split_whitespace().collect();
    if parts.is_empty() {
        return Ok("".to_string());
    }

    let cmd = parts[0].to_lowercase();

    match cmd.as_str() {
        "show" if parts.len() > 1 => match parts[1].to_lowercase().as_str() {
            "collections" | "tables" => {
                let collections = db
                    .list_collection_names()
                    .await
                    .map_err(|e| format!("Failed to list collections: {}", e))?;

                if collections.is_empty() {
                    Ok("No collections found".to_string())
                } else {
                    Ok(collections.join("\n"))
                }
            }
            "dbs" | "databases" => {
                let client = db.client();
                let dbs = client
                    .list_database_names()
                    .await
                    .map_err(|e| format!("Failed to list databases: {}", e))?;
                Ok(dbs.join("\n"))
            }
            _ => Err(format!("Unknown show command: {}", parts[1])),
        },
        "db" => Ok(format!("Current database: {}", db.name())),
        "stats" => {
            let result = db
                .run_command(doc! { "dbStats": 1 })
                .await
                .map_err(|e| format!("Failed to get stats: {}", e))?;
            Ok(format_bson_document(&result, 0))
        }
        _ => {
            // Try to parse as JSON and run as command
            if command.starts_with('{') {
                match serde_json::from_str::<serde_json::Value>(command) {
                    Ok(json) => {
                        let bson_doc = mongodb::bson::to_document(&json)
                            .map_err(|e| format!("Failed to convert to BSON: {}", e))?;
                        let result = db
                            .run_command(bson_doc)
                            .await
                            .map_err(|e| format!("Command error: {}", e))?;
                        Ok(format_bson_document(&result, 0))
                    }
                    Err(e) => Err(format!("Invalid JSON: {}", e)),
                }
            } else {
                Err(format!(
                    "Unknown command: {}. Try 'help' for available commands.",
                    cmd
                ))
            }
        }
    }
}

/// Format BSON document for display
fn format_bson_document(doc: &mongodb::bson::Document, indent: usize) -> String {
    let indent_str = "  ".repeat(indent);
    let mut lines = Vec::new();
    lines.push(format!("{}{{", indent_str));

    for (key, value) in doc.iter() {
        let formatted_value = format_bson_value(value, indent + 1);
        lines.push(format!("{}  \"{}\": {}", indent_str, key, formatted_value));
    }

    lines.push(format!("{}}}", indent_str));
    lines.join("\n")
}

/// Format BSON value for display
fn format_bson_value(value: &mongodb::bson::Bson, indent: usize) -> String {
    use mongodb::bson::Bson;

    match value {
        Bson::Null => "null".to_string(),
        Bson::Boolean(b) => b.to_string(),
        Bson::Int32(i) => i.to_string(),
        Bson::Int64(i) => i.to_string(),
        Bson::Double(d) => format!("{:.6}", d),
        Bson::String(s) => format!("\"{}\"", s),
        Bson::Array(arr) => {
            if arr.is_empty() {
                "[]".to_string()
            } else {
                let items: Vec<String> = arr.iter().map(|v| format_bson_value(v, indent)).collect();
                format!("[{}]", items.join(", "))
            }
        }
        Bson::Document(doc) => format_bson_document(doc, indent),
        Bson::ObjectId(id) => format!("ObjectId(\"{}\")", id),
        Bson::DateTime(dt) => format!("ISODate(\"{}\")", dt),
        Bson::Binary(bin) => format!("Binary({} bytes)", bin.bytes.len()),
        Bson::Timestamp(ts) => format!("Timestamp({}, {})", ts.time, ts.increment),
        Bson::RegularExpression(regex) => format!("/{}/{}", regex.pattern, regex.options),
        Bson::Decimal128(d) => d.to_string(),
        _ => format!("{:?}", value),
    }
}

/// Check if a MongoDB command modifies data
pub(crate) fn is_mongodb_modifying_command(command: &str) -> bool {
    let cmd = command
        .split_whitespace()
        .next()
        .unwrap_or("")
        .to_lowercase();

    // Check for JSON commands with modifying operations
    if command.starts_with('{') {
        let command_lower = command.to_lowercase();
        return command_lower.contains("\"insert\"")
            || command_lower.contains("\"update\"")
            || command_lower.contains("\"delete\"")
            || command_lower.contains("\"drop\"")
            || command_lower.contains("\"create\"")
            || command_lower.contains("\"renamecollection\"");
    }

    matches!(
        cmd.as_str(),
        "insert" | "update" | "delete" | "drop" | "create" | "rename"
    )
}

/// Handle built-in commands. Returns Some(new_db) if database changed.
async fn handle_builtin_command(
    command: &str,
    executor: &mut QueryExecutor,
    to_client: &mpsc::Sender<Bytes>,
    _client: &mongodb::Client,
    current_db: &str,
    security: &DatabaseSecuritySettings,
) -> guacr_handlers::Result<Option<String>> {
    let command_lower = command.to_lowercase();
    let parts: Vec<&str> = command.split_whitespace().collect();

    // Check for "use <database>" command
    if parts.len() >= 2 && parts[0].to_lowercase() == "use" {
        let new_db = parts[1].to_string();
        executor
            .write_line(&format!("switched to db {}", new_db))
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
        return Ok(Some(new_db));
    }

    match command_lower.as_str() {
        "help" => {
            executor
                .write_line("")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("MongoDB Shell - Available commands:")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("Database commands:")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  show dbs             List databases")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  use <database>       Switch database")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  db                   Show current database")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  show collections     List collections")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  stats                Database statistics")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            if !security.disable_csv_export {
                executor
                    .write_line("  \\e <collection>      Export collection as CSV")
                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            }
            if !security.disable_csv_import && !security.base.read_only {
                executor
                    .write_line("  \\i <collection>      Import CSV into collection")
                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            }
            executor
                .write_line("")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("You can also run raw MongoDB commands as JSON:")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("  {\"find\": \"collection\", \"limit\": 10}")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("")
                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
            executor
                .write_line("Type 'quit' to disconnect")
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
            return Ok(Some(current_db.to_string())); // Keep current db
        }
        "quit" | "exit" | "\\q" | "bye" => {
            return Err(crate::handler_helpers::handle_quit(executor, to_client, &mut None).await);
        }
        _ => {}
    }

    Ok(None)
}

/// Handle CSV export for MongoDB collection
async fn handle_csv_export(
    collection_name: &str,
    client: &mongodb::Client,
    current_db: &str,
    executor: &mut QueryExecutor,
    to_client: &mpsc::Sender<Bytes>,
    security: &DatabaseSecuritySettings,
    conn_id: &str,
) -> guacr_handlers::Result<()> {
    use mongodb::bson::doc;
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

    if collection_name.is_empty() {
        executor
            .write_error("Usage: \\e <collection_name>")
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
        .write_line(&format!("Exporting collection '{}'...", collection_name))
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

    // Get documents from collection
    let db = client.database(current_db);
    let collection = db.collection::<mongodb::bson::Document>(collection_name);

    use futures_util::StreamExt;
    let mut cursor = collection
        .find(doc! {})
        .await
        .map_err(|e| HandlerError::ProtocolError(format!("Find error: {}", e)))?;

    // Collect all documents and determine columns
    let mut documents = Vec::new();
    let mut all_keys = std::collections::HashSet::new();

    while let Some(result) = cursor.next().await {
        match result {
            Ok(doc) => {
                for key in doc.keys() {
                    all_keys.insert(key.clone());
                }
                documents.push(doc);
            }
            Err(e) => {
                warn!("[conn={}] MongoDB: Error reading document: {}", conn_id, e);
            }
        }
    }

    if documents.is_empty() {
        executor
            .write_line("Collection is empty or not found.")
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

    // Build columns list (sorted for consistency)
    let mut columns: Vec<String> = all_keys.into_iter().collect();
    columns.sort();

    // Build rows
    let mut rows = Vec::new();
    for doc in &documents {
        let mut row = Vec::new();
        for col in &columns {
            let value = doc
                .get(col)
                .map(|v| format_bson_value(v, 0))
                .unwrap_or_default();
            row.push(value);
        }
        rows.push(row);
    }

    let result = guacr_terminal::QueryResult {
        columns,
        rows,
        affected_rows: None,
        execution_time_ms: None,
    };

    // Generate filename and create exporter
    let filename = generate_csv_filename(&format!("collection {}", collection_name), "mongodb");
    let stream_idx = STREAM_INDEX.fetch_add(1, Ordering::SeqCst);
    let mut exporter = CsvExporter::new(stream_idx);

    executor
        .write_line(&format!(
            "Beginning CSV download ({} documents). Press Ctrl+C to cancel.",
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

/// Handle CSV import for a collection
async fn handle_csv_import(
    collection_name: &str,
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

    if collection_name.is_empty() {
        executor
            .write_error("Usage: \\i <collection_name>")
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
        .write_error("CSV import is not yet implemented for MongoDB.")
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
    executor
        .write_line("To import data, use the MongoDB shell or mongoimport tool.")
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
impl EventBasedHandler for MongoDbHandler {
    fn name(&self) -> &str {
        "mongodb"
    }

    async fn connect_with_events(
        &self,
        params: HashMap<String, String>,
        callback: Arc<dyn EventCallback>,
        from_client: mpsc::Receiver<Bytes>,
        _video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: guacr_handlers::SessionHooks,
    ) -> Result<(), HandlerError> {
        guacr_handlers::connect_with_event_adapter(
            |params, to_client, from_client, _video_tx, _hooks| {
                self.connect(params, to_client, from_client, _video_tx, _hooks)
            },
            params,
            callback,
            from_client,
            _video_tx,
            _hooks,
            4096,
        )
        .await
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::query_executor::QueryExecutor;
    use crate::security::DatabaseSecuritySettings;
    use std::collections::HashMap;
    use tokio::sync::mpsc;

    /// CSV import must return "not yet implemented" rather than inserting
    /// hardcoded sample data.  No MongoDB connection is required.
    #[tokio::test]
    async fn test_csv_import_returns_not_implemented() {
        let (to_client, mut rx) = mpsc::channel(64);
        let mut executor = QueryExecutor::new("> ", "mongodb").unwrap();
        let security = DatabaseSecuritySettings::from_params(&HashMap::new());

        handle_csv_import("test_collection", &mut executor, &to_client, &security)
            .await
            .unwrap();

        drop(to_client);
        let mut rendered = String::new();
        while let Some(bytes) = rx.recv().await {
            rendered.push_str(&String::from_utf8_lossy(&bytes));
        }

        assert!(
            rendered.contains("not yet implemented"),
            "import must return 'not yet implemented'; got rendered output of {} bytes",
            rendered.len()
        );
    }
}
