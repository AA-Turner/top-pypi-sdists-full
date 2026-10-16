use std::{
    error::Error,
    io::{self, BufReader},
    net::TcpStream,
    path::{Path, PathBuf},
    thread,
};

use crossbeam_channel::{bounded, unbounded, Receiver, Sender};
use log::{debug, info, warn};
use lsp_server::{Connection, Message, Notification, Request, Response};
use lsp_types::notification::{
    DidChangeConfiguration, DidChangeTextDocument, DidCloseTextDocument, DidOpenTextDocument,
    DidSaveTextDocument, Notification as _,
};
use lsp_types::request::{Completion, GotoDefinition, Request as _};
use lsp_types::{
    CompletionItem, CompletionOptions, CompletionResponse, GotoDefinitionResponse,
    InitializeParams, InitializeResult, Location, OneOf, Position, ServerCapabilities, ServerInfo,
    TextDocumentSyncCapability, TextDocumentSyncKind, Uri,
};

mod cheapo;
mod cli;
mod config;

use chalk_lsp::external_diagnostics::{
    spawn_external_diagnostics, ExternalDiagnosticsJob, ExternalDiagnosticsResult,
    DEFAULT_LSP_DIAGNOSTICS_API_HOST,
};
use chalk_lsp::index::build_project_index;
use chalk_lsp::project::{uri_to_file_path, ExternalFileDiagnostics, ProjectState};
use chalk_lsp::providers;

fn main() {
    if let Err(err) = try_main() {
        eprintln!("Error: {err}");
        std::process::exit(1);
    }
}

fn try_main() -> Result<(), Box<dyn Error + Sync + Send>> {
    env_logger::init();
    cli::run(run_lsp_command)
}

fn run_lsp_command(
    args: cli::LspCommandArgs,
    config: Option<config::Configuration>,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    let (connection, io_threads) = if let Some(port) = args.port {
        let addr = format!("127.0.0.1:{port}");
        eprintln!("chalk-lsp listening on {addr}");
        listen_on_tcp(&addr)?
    } else {
        eprintln!("chalk-lsp starting on stdio");
        let (connection, io_threads) = Connection::stdio();
        (connection, ServerIoThreads::Stdio(io_threads))
    };

    let server_capabilities = ServerCapabilities {
        text_document_sync: Some(TextDocumentSyncCapability::Kind(TextDocumentSyncKind::FULL)),
        definition_provider: Some(OneOf::Left(true)),
        completion_provider: Some(CompletionOptions {
            trigger_characters: Some(vec![".".to_string()]),
            ..Default::default()
        }),
        ..Default::default()
    };

    let (initialize_id, init_params) = match connection.initialize_start() {
        Ok(params) => params,
        Err(e) => {
            info!("initialization failed: {e}");
            return Ok(());
        }
    };
    let initialize_result = serde_json::to_value(InitializeResult {
        capabilities: server_capabilities,
        server_info: Some(ServerInfo {
            name: "chalk-lsp".to_string(),
            version: Some(env!("CHALK_LSP_VERSION").to_string()),
        }),
    })?;
    if let Err(e) = connection.initialize_finish(initialize_id, initialize_result) {
        info!("initialization failed: {e}");
        return Ok(());
    }
    let init_params: InitializeParams = serde_json::from_value(init_params)?;

    // info!("initialized with params: {init_params:?}");
    main_loop(connection, init_params, config)?;
    io_threads.join()?;
    Ok(())
}

struct CheapoDiagnosticsResult {
    run_id: u64,
    files: Vec<ExternalFileDiagnostics>,
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct ServerSettings {
    cli: Option<config::Configuration>,
    client: config::Configuration,
}

impl ServerSettings {
    fn new(
        cli: Option<config::Configuration>,
        init_params: &InitializeParams,
    ) -> serde_json::Result<Self> {
        let client = init_params
            .initialization_options
            .as_ref()
            .map(config::Configuration::from_lsp_value)
            .transpose()?
            .unwrap_or_default();
        Ok(Self { cli, client })
    }

    fn effective(&self) -> &config::ChalkSettings {
        &self.cli.as_ref().unwrap_or(&self.client).chalk
    }

    fn linter_enabled(&self, linter: config::Linter) -> bool {
        self.effective().linters.contains(&linter)
    }

    fn effective_api_host(&self) -> &str {
        self.effective()
            .remote_diagnostics
            .api_host
            .as_deref()
            .filter(|api_host| !api_host.trim().is_empty())
            .unwrap_or(DEFAULT_LSP_DIAGNOSTICS_API_HOST)
    }

    fn effective_chalkpy_path_override(&self) -> Option<&Path> {
        self.effective()
            .remote_diagnostics
            .chalkpy_path_override
            .as_deref()
    }
}

enum ServerIoThreads {
    Stdio(lsp_server::IoThreads),
    Socket(SocketIoThreads),
}

impl ServerIoThreads {
    fn join(self) -> io::Result<()> {
        match self {
            Self::Stdio(io_threads) => io_threads.join(),
            Self::Socket(io_threads) => io_threads.join(),
        }
    }
}

struct SocketIoThreads {
    reader: thread::JoinHandle<io::Result<()>>,
    writer: thread::JoinHandle<io::Result<()>>,
    dropper: thread::JoinHandle<()>,
}

impl SocketIoThreads {
    fn join(self) -> io::Result<()> {
        match self.reader.join() {
            Ok(result) => result?,
            Err(err) => std::panic::panic_any(err),
        }
        match self.dropper.join() {
            Ok(()) => {}
            Err(err) => std::panic::panic_any(err),
        }
        match self.writer.join() {
            Ok(result) => result,
            Err(err) => std::panic::panic_any(err),
        }
    }
}

fn listen_on_tcp(addr: &str) -> io::Result<(Connection, ServerIoThreads)> {
    let listener = std::net::TcpListener::bind(addr)?;
    let (stream, _) = listener.accept()?;
    let (receiver, reader) = socket_reader(stream.try_clone()?);
    let (sender, writer, messages_to_drop) = socket_writer(stream);
    let dropper = thread::Builder::new()
        .name("ChalkLspMessageDropper".to_string())
        .spawn(move || messages_to_drop.into_iter().for_each(drop))
        .unwrap();

    Ok((
        Connection { sender, receiver },
        ServerIoThreads::Socket(SocketIoThreads {
            reader,
            writer,
            dropper,
        }),
    ))
}

fn socket_reader(stream: TcpStream) -> (Receiver<Message>, thread::JoinHandle<io::Result<()>>) {
    let (reader_sender, reader_receiver) = bounded::<Message>(0);
    let reader = thread::Builder::new()
        .name("ChalkLspSocketReader".to_string())
        .spawn(move || {
            let mut buf_read = BufReader::new(stream);
            while let Some(msg) = Message::read(&mut buf_read)? {
                debug_lsp_message("incoming", &msg);
                let is_exit = matches!(&msg, Message::Notification(n) if n.method == "exit");
                if let Err(err) = reader_sender.send(msg) {
                    return Err(io::Error::new(io::ErrorKind::BrokenPipe, err.to_string()));
                }
                if is_exit {
                    break;
                }
            }
            Ok(())
        })
        .unwrap();
    (reader_receiver, reader)
}

fn socket_writer(
    mut stream: TcpStream,
) -> (
    Sender<Message>,
    thread::JoinHandle<io::Result<()>>,
    Receiver<Message>,
) {
    let (writer_sender, writer_receiver) = bounded::<Message>(0);
    let (drop_sender, drop_receiver) = bounded::<Message>(0);
    let writer = thread::Builder::new()
        .name("ChalkLspSocketWriter".to_string())
        .spawn(move || {
            writer_receiver.into_iter().try_for_each(|msg| {
                debug_lsp_message("outgoing", &msg);
                let result = msg.write(&mut stream);
                let _ = drop_sender.send(msg);
                result
            })
        })
        .unwrap();
    (writer_sender, writer, drop_receiver)
}

fn debug_lsp_message(direction: &str, msg: &Message) {
    let arrow = match direction {
        "incoming" => "<<",
        "outgoing" => ">>",
        _ => direction,
    };

    let text = match msg {
        Message::Request(req) => format_lsp_debug_line(
            arrow,
            Some(&req.id),
            &req.method,
            &format_lsp_details(&req.method, &req.params),
        ),
        Message::Notification(notif) => format_lsp_debug_line(
            arrow,
            None,
            &notif.method,
            &format_lsp_details(&notif.method, &notif.params),
        ),
        Message::Response(resp) => {
            let details = if let Some(error) = &resp.error {
                let value = serde_json::to_value(error).unwrap_or(serde_json::Value::Null);
                format!("error: {}", format_lsp_value(&value))
            } else if let Some(result) = &resp.result {
                format!("result: {}", format_lsp_value(result))
            } else {
                String::new()
            };
            format_lsp_debug_line(arrow, Some(&resp.id), "response", &details)
        }
    };
    debug!("{}", text);
}

fn format_lsp_debug_line(
    arrow: &str,
    id: Option<&lsp_server::RequestId>,
    method: &str,
    details: &str,
) -> String {
    let id = id.map(|id| format!("[{id}]")).unwrap_or_default();
    if details.is_empty() {
        format!("{arrow}{id} {method}")
    } else {
        format!("{arrow}{id} {method} :: {details}")
    }
}

fn format_lsp_details(method: &str, value: &serde_json::Value) -> String {
    match value {
        serde_json::Value::Object(fields) => fields
            .iter()
            .map(|(key, value)| {
                let field_value = if (method == "initialize" && key == "capabilities")
                    || (method.starts_with("textDocument/") && key == "textDocument")
                {
                    "{...}".to_string()
                } else {
                    format_lsp_value(value)
                };
                format!("{key}: {field_value}")
            })
            .collect::<Vec<_>>()
            .join(", "),
        serde_json::Value::Null => String::new(),
        _ => format_lsp_value(value),
    }
}

fn format_lsp_value(value: &serde_json::Value) -> String {
    serde_json::to_string(value).unwrap_or_else(|_| "<unserializable>".to_string())
}

fn main_loop(
    connection: Connection,
    init_params: InitializeParams,
    config: Option<config::Configuration>,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    let mut settings = ServerSettings::new(config, &init_params)?;
    let mut state = ProjectState::new(&init_params, settings.linter_enabled(config::Linter::Local));
    let lsp_receiver = connection.receiver.clone();
    let (cheapo_sender, cheapo_receiver) = unbounded();
    let (external_sender, external_receiver) = unbounded();

    'main: loop {
        crossbeam_channel::select! {
            recv(lsp_receiver) -> msg => {
                let Ok(msg) = msg else {
                    break 'main;
                };
                if handle_lsp_message(
                    &connection,
                    &mut state,
                    &mut settings,
                    msg,
                    &external_sender,
                    &cheapo_sender,
                )? {
                    break 'main;
                }
            }
            recv(cheapo_receiver) -> result => {
                let Ok(result) = result else {
                    break 'main;
                };
                handle_cheapo_diagnostics_result(&connection.sender, &mut state, result)?;
            }
            recv(external_receiver) -> result => {
                let Ok(result) = result else {
                    break 'main;
                };
                handle_external_diagnostics_result(&connection.sender, &mut state, result)?;
            }
        }
    }
    Ok(())
}

fn handle_lsp_message(
    connection: &Connection,
    state: &mut ProjectState,
    settings: &mut ServerSettings,
    msg: Message,
    external_sender: &Sender<ExternalDiagnosticsResult>,
    cheapo_sender: &Sender<CheapoDiagnosticsResult>,
) -> Result<bool, Box<dyn Error + Sync + Send>> {
    match msg {
        Message::Request(req) => {
            if connection.handle_shutdown(&req)? {
                return Ok(true);
            }
            handle_request(connection, state, req)?;
        }
        Message::Notification(notif) => {
            handle_notification(
                &connection.sender,
                state,
                settings,
                notif,
                external_sender,
                cheapo_sender,
            )?;
        }
        Message::Response(_) => {}
    }
    Ok(false)
}

fn handle_request(
    connection: &Connection,
    state: &ProjectState,
    req: Request,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    match req.method.as_str() {
        GotoDefinition::METHOD => {
            let params: lsp_types::GotoDefinitionParams = serde_json::from_value(req.params)?;
            let uri = &params.text_document_position_params.text_document.uri;
            let pos = params.text_document_position_params.position;
            let locations = compute_definition(state, uri, pos);
            let result = if locations.is_empty() {
                serde_json::Value::Null
            } else {
                serde_json::to_value(GotoDefinitionResponse::Array(locations))?
            };
            connection
                .sender
                .send(Message::Response(Response::new_ok(req.id, result)))?;
        }
        Completion::METHOD => {
            let params: lsp_types::CompletionParams = serde_json::from_value(req.params)?;
            let uri = &params.text_document_position.text_document.uri;
            let pos = params.text_document_position.position;
            let items = compute_completion(state, uri, pos);
            let result = if items.is_empty() {
                serde_json::Value::Null
            } else {
                serde_json::to_value(CompletionResponse::Array(items))?
            };
            connection
                .sender
                .send(Message::Response(Response::new_ok(req.id, result)))?;
        }
        _ => {
            let resp = Response::new_err(
                req.id,
                lsp_server::ErrorCode::MethodNotFound as i32,
                format!("unhandled request: {}", req.method),
            );
            connection.sender.send(Message::Response(resp))?;
        }
    }
    Ok(())
}

fn compute_definition(state: &ProjectState, uri: &Uri, pos: Position) -> Vec<Location> {
    let Some(text) = state.document_text(uri) else {
        return Vec::new();
    };
    let Some(path) = uri_to_file_path(uri) else {
        return Vec::new();
    };
    let Some(project_root) = state.project_root_for(&path) else {
        return Vec::new();
    };
    let Some(index) = build_project_index(&project_root, &state.open_documents_by_path()) else {
        return Vec::new();
    };

    if is_chalk_sql(&path) {
        providers::sql_definition(&index, text, pos.line, pos.character)
    } else if is_python(&path) {
        let path_str = path.to_string_lossy().to_string();
        providers::python_definition(&index, &path_str, text, pos.line, pos.character)
    } else {
        Vec::new()
    }
}

fn compute_completion(state: &ProjectState, uri: &Uri, pos: Position) -> Vec<CompletionItem> {
    let Some(text) = state.document_text(uri) else {
        return Vec::new();
    };
    let Some(path) = uri_to_file_path(uri) else {
        return Vec::new();
    };
    if !is_python(&path) {
        return Vec::new();
    }
    let Some(project_root) = state.project_root_for(&path) else {
        return Vec::new();
    };
    let Some(index) = build_project_index(&project_root, &state.open_documents_by_path()) else {
        return Vec::new();
    };
    let path_str = path.to_string_lossy().to_string();
    providers::python_completion(&index, &path_str, text, pos.line, pos.character)
}

fn is_chalk_sql(path: &Path) -> bool {
    path.file_name()
        .and_then(|name| name.to_str())
        .is_some_and(|name| name.ends_with(".chalk.sql"))
}

fn is_python(path: &Path) -> bool {
    path.extension().and_then(|ext| ext.to_str()) == Some("py")
}

fn handle_notification(
    sender: &Sender<Message>,
    state: &mut ProjectState,
    settings: &mut ServerSettings,
    notif: Notification,
    external_sender: &Sender<ExternalDiagnosticsResult>,
    cheapo_sender: &Sender<CheapoDiagnosticsResult>,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    match notif.method.as_str() {
        DidOpenTextDocument::METHOD => {
            let params: lsp_types::DidOpenTextDocumentParams =
                serde_json::from_value(notif.params)?;
            state.on_open(params.text_document.uri.clone(), params.text_document.text);
            publish_merged_diagnostics(sender, state, &params.text_document.uri)?;
            if settings.linter_enabled(config::Linter::Accel) {
                maybe_spawn_cheapo_diagnostics(state, &params.text_document.uri, cheapo_sender);
            }
            if settings.linter_enabled(config::Linter::Remote) {
                maybe_spawn_external_diagnostics(
                    state,
                    &params.text_document.uri,
                    external_sender,
                    settings,
                );
            }
        }
        DidChangeTextDocument::METHOD => {
            let params: lsp_types::DidChangeTextDocumentParams =
                serde_json::from_value(notif.params)?;
            if let Some(change) = params.content_changes.into_iter().last() {
                state.on_change(params.text_document.uri.clone(), change.text);
            }
            publish_merged_diagnostics(sender, state, &params.text_document.uri)?;
            state.invalidate_cheapo_runs();
            state.invalidate_external_runs();
        }
        DidSaveTextDocument::METHOD => {
            let params: lsp_types::DidSaveTextDocumentParams =
                serde_json::from_value(notif.params)?;
            state.on_save(params.text_document.uri.clone(), params.text);
            publish_merged_diagnostics(sender, state, &params.text_document.uri)?;
            if settings.linter_enabled(config::Linter::Accel) {
                maybe_spawn_cheapo_diagnostics(state, &params.text_document.uri, cheapo_sender);
            }
            if settings.linter_enabled(config::Linter::Remote) {
                maybe_spawn_external_diagnostics(
                    state,
                    &params.text_document.uri,
                    external_sender,
                    settings,
                );
            }
        }
        DidChangeConfiguration::METHOD => {
            let params: lsp_types::DidChangeConfigurationParams =
                serde_json::from_value(notif.params)?;
            if settings.cli.is_none() {
                match config::Configuration::from_lsp_value(&params.settings) {
                    Ok(config) => settings.client = config,
                    Err(err) => warn!("ignoring invalid LSP configuration: {err}"),
                }
            }
            state.invalidate_cheapo_runs();
            state.invalidate_external_runs();
            let mut affected_uris =
                state.set_local_diagnostics_enabled(settings.linter_enabled(config::Linter::Local));
            if !settings.linter_enabled(config::Linter::Accel) {
                affected_uris.extend(state.replace_cheapo_diagnostics(Vec::new()));
            }
            if !settings.linter_enabled(config::Linter::Remote) {
                affected_uris.extend(state.replace_external_diagnostics(Vec::new()));
            }
            affected_uris.sort();
            affected_uris.dedup();
            publish_merged_diagnostics_for_uris(sender, state, affected_uris)?;
        }
        DidCloseTextDocument::METHOD => {
            let params: lsp_types::DidCloseTextDocumentParams =
                serde_json::from_value(notif.params)?;
            state.on_close(&params.text_document.uri);
        }
        _ => {}
    }
    Ok(())
}

fn maybe_spawn_cheapo_diagnostics(
    state: &mut ProjectState,
    uri: &Uri,
    cheapo_sender: &Sender<CheapoDiagnosticsResult>,
) {
    info!(
        "considering accel diagnostics for document: {}",
        uri.as_str()
    );

    let Some(file_path) = uri_to_file_path(uri) else {
        info!(
            "skipping accel diagnostics for {}: URI is not a file URI",
            uri.as_str()
        );
        return;
    };
    if !is_python(&file_path) {
        info!(
            "skipping accel diagnostics for {}: file is not a .py file",
            file_path.display()
        );
        return;
    }
    let Some(project_root) = state.project_root_for(&file_path) else {
        info!(
            "skipping accel diagnostics for {}: no Chalk project config found in parent directories",
            file_path.display()
        );
        return;
    };

    let run_id = state.start_cheapo_run();
    info!(
        "spawning accel diagnostics: run_id={}, trigger_uri={}, trigger_file={}, project_root={}",
        run_id,
        uri.as_str(),
        file_path.display(),
        project_root.display(),
    );
    let sender = cheapo_sender.clone();
    thread::spawn(move || {
        let files = match cheapo::diagnostics_for_project(&project_root, &[]) {
            Ok(files) => files,
            Err(err) => {
                warn!(
                    "failed to run accel diagnostics for {}: {err}",
                    project_root.display()
                );
                Vec::new()
            }
        };
        let _ = sender.send(CheapoDiagnosticsResult { run_id, files });
    });
}

fn maybe_spawn_external_diagnostics(
    state: &mut ProjectState,
    uri: &Uri,
    external_sender: &Sender<ExternalDiagnosticsResult>,
    settings: &ServerSettings,
) {
    info!(
        "considering chalk diagnostics for saved document: {}",
        uri.as_str()
    );

    let Some(file_path) = uri_to_file_path(uri) else {
        info!(
            "skipping chalk diagnostics for {}: URI is not a file URI",
            uri.as_str()
        );
        return;
    };
    if !is_python(&file_path) && !is_chalk_sql(&file_path) {
        info!(
            "skipping chalk diagnostics for {}: saved file is not a .py or .chalk.sql file",
            file_path.display()
        );
        return;
    }
    let Some(project_root) = state.project_root_for(&file_path) else {
        info!(
            "skipping chalk diagnostics for {}: no Chalk project config found in parent directories",
            file_path.display()
        );
        return;
    };

    let mut requested_paths = state.open_file_paths_for_project(&project_root);
    requested_paths.retain(|path| is_python(path) || is_chalk_sql(path));
    if requested_paths.is_empty() {
        requested_paths.push(file_path.clone());
    }

    let trigger_text = state.document_text(uri).unwrap_or_default().to_string();
    let run_id = state.start_external_run();
    info!(
        "spawning chalk diagnostics: run_id={}, trigger_uri={}, trigger_file={}, project_root={}, requested_path_count={}",
        run_id,
        uri.as_str(),
        file_path.display(),
        project_root.display(),
        requested_paths.len(),
    );
    let job = ExternalDiagnosticsJob {
        run_id,
        trigger_uri: uri.clone(),
        trigger_uri_key: uri.as_str().to_string(),
        trigger_file_path: file_path,
        trigger_text,
        trigger_project_root: project_root,
        workspace_roots: state.workspace_roots().to_vec(),
        requested_paths,
        api_host: settings.effective_api_host().to_string(),
        chalkpy_path_override: settings
            .effective_chalkpy_path_override()
            .map(PathBuf::from),
    };
    spawn_external_diagnostics(external_sender.clone(), job);
}

fn handle_cheapo_diagnostics_result(
    sender: &Sender<Message>,
    state: &mut ProjectState,
    result: CheapoDiagnosticsResult,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    if !state.is_current_cheapo_run(result.run_id) {
        return Ok(());
    }

    let affected_uris = state.replace_cheapo_diagnostics(result.files);
    publish_merged_diagnostics_for_uris(sender, state, affected_uris)
}

fn handle_external_diagnostics_result(
    sender: &Sender<Message>,
    state: &mut ProjectState,
    result: ExternalDiagnosticsResult,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    if !state.is_current_external_run(result.run_id) {
        return Ok(());
    }

    let affected_uris = state.replace_external_diagnostics(result.files);
    publish_merged_diagnostics_for_uris(sender, state, affected_uris)
}

fn publish_merged_diagnostics(
    sender: &Sender<Message>,
    state: &ProjectState,
    uri: &Uri,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    publish_diagnostics(sender, uri, state.merged_diagnostics(uri))
}

fn publish_merged_diagnostics_for_uris(
    sender: &Sender<Message>,
    state: &ProjectState,
    uris: Vec<Uri>,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    for uri in uris {
        publish_merged_diagnostics(sender, state, &uri)?;
    }
    Ok(())
}

fn publish_diagnostics(
    sender: &Sender<Message>,
    uri: &Uri,
    diagnostics: Vec<lsp_types::Diagnostic>,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    let params = lsp_types::PublishDiagnosticsParams {
        uri: uri.clone(),
        diagnostics,
        version: None,
    };
    let notif = Notification::new(
        lsp_types::notification::PublishDiagnostics::METHOD.to_string(),
        params,
    );
    sender.send(Message::Notification(notif))?;
    Ok(())
}
