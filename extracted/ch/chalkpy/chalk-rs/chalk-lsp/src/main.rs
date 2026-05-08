use std::error::Error;

use crossbeam_channel::Sender;
use log::info;
use lsp_server::{Connection, Message, Notification, Response};
use lsp_types::notification::{
    DidChangeTextDocument, DidCloseTextDocument, DidOpenTextDocument, DidSaveTextDocument,
    Notification as _,
};
use lsp_types::{
    InitializeParams, ServerCapabilities, TextDocumentSyncCapability, TextDocumentSyncKind, Uri,
};

use chalk_lsp::project::ProjectState;

fn main() -> Result<(), Box<dyn Error + Sync + Send>> {
    env_logger::init();

    let args: Vec<String> = std::env::args().collect();
    let (connection, io_threads) = if let Some(pos) = args.iter().position(|a| a == "--port") {
        let port: u16 = args
            .get(pos + 1)
            .ok_or("--port requires a value")?
            .parse()?;
        let addr = format!("127.0.0.1:{port}");
        eprintln!("chalk-lsp listening on {addr}");
        Connection::listen(&addr)?
    } else {
        eprintln!("chalk-lsp starting on stdio");
        Connection::stdio()
    };

    let server_capabilities = serde_json::to_value(ServerCapabilities {
        text_document_sync: Some(TextDocumentSyncCapability::Kind(TextDocumentSyncKind::FULL)),
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

fn main_loop(
    connection: Connection,
    init_params: InitializeParams,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    let mut state = ProjectState::new(&init_params);

    for msg in &connection.receiver {
        match msg {
            Message::Request(req) => {
                if connection.handle_shutdown(&req)? {
                    return Ok(());
                }
                let resp = Response::new_err(
                    req.id,
                    lsp_server::ErrorCode::MethodNotFound as i32,
                    format!("unhandled request: {}", req.method),
                );
                connection.sender.send(Message::Response(resp))?;
            }
            Message::Notification(notif) => {
                handle_notification(&connection.sender, &mut state, notif)?;
            }
            Message::Response(_) => {}
        }
    }
    Ok(())
}

fn handle_notification(
    sender: &Sender<Message>,
    state: &mut ProjectState,
    notif: Notification,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    match notif.method.as_str() {
        DidOpenTextDocument::METHOD => {
            let params: lsp_types::DidOpenTextDocumentParams =
                serde_json::from_value(notif.params)?;
            state.on_open(params.text_document.uri.clone(), params.text_document.text);
            publish_diagnostics(sender, state, &params.text_document.uri)?;
        }
        DidChangeTextDocument::METHOD => {
            let params: lsp_types::DidChangeTextDocumentParams =
                serde_json::from_value(notif.params)?;
            if let Some(change) = params.content_changes.into_iter().last() {
                state.on_change(params.text_document.uri.clone(), change.text);
            }
            publish_diagnostics(sender, state, &params.text_document.uri)?;
        }
        DidSaveTextDocument::METHOD => {
            let params: lsp_types::DidSaveTextDocumentParams =
                serde_json::from_value(notif.params)?;
            publish_diagnostics(sender, state, &params.text_document.uri)?;
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

fn publish_diagnostics(
    sender: &Sender<Message>,
    state: &ProjectState,
    uri: &Uri,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    let diags = state.diagnostics(uri);
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
