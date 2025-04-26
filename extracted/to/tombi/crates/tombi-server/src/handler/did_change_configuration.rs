use tower_lsp::lsp_types::DidChangeConfigurationParams;

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_did_change_configuration(params: DidChangeConfigurationParams) {
    tracing::info!("handle_did_change_configuration");
    tracing::trace!(?params);
}
