#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_shutdown() -> Result<(), tower_lsp::jsonrpc::Error> {
    tracing::info!("handle_shutdown");

    Ok(())
}
