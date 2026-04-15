#[cfg(feature = "server")]
use std::collections::HashMap;
#[cfg(feature = "server")]
use std::error::Error;

#[cfg(feature = "server")]
use crossbeam_channel::Sender;
#[cfg(feature = "server")]
use log::info;
#[cfg(feature = "server")]
use lsp_server::{Connection, Message, Notification, RequestId, Response};
#[cfg(feature = "server")]
use lsp_types::notification::{
    DidChangeTextDocument, DidCloseTextDocument, DidOpenTextDocument, DidSaveTextDocument,
    Notification as _,
};
#[cfg(feature = "server")]
use lsp_types::request::{Completion, HoverRequest, Request, SignatureHelpRequest};
#[cfg(feature = "server")]
use lsp_types::{
    CompletionOptions, InitializeParams, ServerCapabilities, SignatureHelpOptions,
    TextDocumentSyncCapability, TextDocumentSyncKind, Uri,
};

#[cfg(feature = "server")]
fn main() -> Result<(), Box<dyn Error + Sync + Send>> {
    env_logger::init();

    let args: Vec<String> = std::env::args().collect();
    let (connection, io_threads) = if let Some(pos) = args.iter().position(|a| a == "--port") {
        let port: u16 = args
            .get(pos + 1)
            .ok_or("--port requires a value")?
            .parse()?;
        let addr = format!("127.0.0.1:{port}");
        eprintln!("chalk-sql-lsp listening on {addr}");
        Connection::listen(&addr)?
    } else {
        eprintln!("chalk-sql-lsp starting on stdio");
        Connection::stdio()
    };

    let server_capabilities = serde_json::to_value(ServerCapabilities {
        text_document_sync: Some(TextDocumentSyncCapability::Kind(TextDocumentSyncKind::FULL)),
        completion_provider: Some(CompletionOptions {
            trigger_characters: Some(vec!["(".to_string(), ",".to_string(), " ".to_string()]),
            ..Default::default()
        }),
        hover_provider: Some(lsp_types::HoverProviderCapability::Simple(true)),
        signature_help_provider: Some(SignatureHelpOptions {
            trigger_characters: Some(vec!["(".to_string(), ",".to_string()]),
            retrigger_characters: None,
            work_done_progress_options: Default::default(),
        }),
        ..Default::default()
    })?;

    let init_params = match connection.initialize(server_capabilities) {
        Ok(params) => params,
        Err(e) => {
            info!("initialization failed: {e}");
            return Ok(());
        }
    };
    let init_params: InitializeParams = serde_json::from_value(init_params)?;

    info!("initialized with params: {init_params:?}");
    main_loop(connection, init_params)?;
    io_threads.join()?;
    Ok(())
}

#[cfg(not(feature = "server"))]
fn main() {
    eprintln!("chalk-sql-lsp server requires the 'server' feature. Build with: cargo build --features server");
    std::process::exit(1);
}

#[cfg(feature = "server")]
struct DocumentStore {
    docs: HashMap<Uri, String>,
}

#[cfg(feature = "server")]
impl DocumentStore {
    fn new() -> Self {
        Self {
            docs: HashMap::new(),
        }
    }

    fn on_open(&mut self, uri: Uri, text: String) {
        self.docs.insert(uri, text);
    }

    fn on_change(&mut self, uri: Uri, text: String) {
        self.docs.insert(uri, text);
    }

    fn on_close(&mut self, uri: &Uri) {
        self.docs.remove(uri);
    }

    fn get(&self, uri: &Uri) -> Option<&str> {
        self.docs.get(uri).map(|s| s.as_str())
    }
}

#[cfg(feature = "server")]
fn main_loop(
    connection: Connection,
    _init_params: InitializeParams,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    let mut store = DocumentStore::new();

    for msg in &connection.receiver {
        match msg {
            Message::Request(req) => {
                if connection.handle_shutdown(&req)? {
                    return Ok(());
                }
                handle_request(&connection.sender, &store, req.id, &req.method, req.params)?;
            }
            Message::Notification(notif) => {
                handle_notification(&connection.sender, &mut store, notif)?;
            }
            Message::Response(_) => {}
        }
    }
    Ok(())
}

#[cfg(feature = "server")]
fn handle_request(
    sender: &Sender<Message>,
    store: &DocumentStore,
    id: RequestId,
    method: &str,
    params: serde_json::Value,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    match method {
        Completion::METHOD => {
            let params: lsp_types::CompletionParams = serde_json::from_value(params)?;
            let uri = &params.text_document_position.text_document.uri;
            let pos = params.text_document_position.position;
            let result = if let Some(text) = store.get(uri) {
                let items = chalk_sql_lsp::completions::completions(text, pos.line, pos.character);
                serde_json::to_value(items)?
            } else {
                serde_json::Value::Null
            };
            sender.send(Message::Response(Response::new_ok(id, result)))?;
        }
        HoverRequest::METHOD => {
            let params: lsp_types::HoverParams = serde_json::from_value(params)?;
            let uri = &params.text_document_position_params.text_document.uri;
            let pos = params.text_document_position_params.position;
            let result = if let Some(text) = store.get(uri) {
                match chalk_sql_lsp::hover::hover(text, pos.line, pos.character) {
                    Some(h) => serde_json::to_value(h)?,
                    None => serde_json::Value::Null,
                }
            } else {
                serde_json::Value::Null
            };
            sender.send(Message::Response(Response::new_ok(id, result)))?;
        }
        SignatureHelpRequest::METHOD => {
            let params: lsp_types::SignatureHelpParams = serde_json::from_value(params)?;
            let uri = &params.text_document_position_params.text_document.uri;
            let pos = params.text_document_position_params.position;
            let result = if let Some(text) = store.get(uri) {
                match chalk_sql_lsp::signature_help::signature_help(
                    text,
                    pos.line,
                    pos.character,
                ) {
                    Some(sh) => serde_json::to_value(sh)?,
                    None => serde_json::Value::Null,
                }
            } else {
                serde_json::Value::Null
            };
            sender.send(Message::Response(Response::new_ok(id, result)))?;
        }
        _ => {
            let resp = Response::new_err(
                id,
                lsp_server::ErrorCode::MethodNotFound as i32,
                format!("unhandled request: {method}"),
            );
            sender.send(Message::Response(resp))?;
        }
    }
    Ok(())
}

#[cfg(feature = "server")]
fn handle_notification(
    sender: &Sender<Message>,
    store: &mut DocumentStore,
    notif: Notification,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    match notif.method.as_str() {
        DidOpenTextDocument::METHOD => {
            let params: lsp_types::DidOpenTextDocumentParams =
                serde_json::from_value(notif.params)?;
            store.on_open(
                params.text_document.uri.clone(),
                params.text_document.text,
            );
            publish_diagnostics(sender, store, &params.text_document.uri)?;
        }
        DidChangeTextDocument::METHOD => {
            let params: lsp_types::DidChangeTextDocumentParams =
                serde_json::from_value(notif.params)?;
            if let Some(change) = params.content_changes.into_iter().last() {
                store.on_change(params.text_document.uri.clone(), change.text);
            }
            publish_diagnostics(sender, store, &params.text_document.uri)?;
        }
        DidSaveTextDocument::METHOD => {
            let params: lsp_types::DidSaveTextDocumentParams =
                serde_json::from_value(notif.params)?;
            publish_diagnostics(sender, store, &params.text_document.uri)?;
        }
        DidCloseTextDocument::METHOD => {
            let params: lsp_types::DidCloseTextDocumentParams =
                serde_json::from_value(notif.params)?;
            store.on_close(&params.text_document.uri);
        }
        _ => {}
    }
    Ok(())
}

#[cfg(feature = "server")]
fn publish_diagnostics(
    sender: &Sender<Message>,
    store: &DocumentStore,
    uri: &Uri,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    let diags = match store.get(uri) {
        Some(text) => chalk_sql_lsp::diagnostics::diagnostics(text),
        None => vec![],
    };
    let params = lsp_types::PublishDiagnosticsParams {
        uri: uri.clone(),
        diagnostics: diags,
        version: None,
    };
    let notif = Notification::new(
        lsp_types::notification::PublishDiagnostics::METHOD.to_string(),
        params,
    );
    sender.send(Message::Notification(notif))?;
    Ok(())
}
