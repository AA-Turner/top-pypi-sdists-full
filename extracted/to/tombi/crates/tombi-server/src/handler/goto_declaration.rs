use itertools::Either;
use tower_lsp::lsp_types::request::{GotoDeclarationParams, GotoDeclarationResponse};
use tower_lsp::lsp_types::TextDocumentPositionParams;

use crate::handler::hover::get_hover_range;
use crate::Backend;

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_goto_declaration(
    backend: &Backend,
    params: GotoDeclarationParams,
) -> Result<Option<GotoDeclarationResponse>, tower_lsp::jsonrpc::Error> {
    tracing::info!("handle_goto_declaration");
    tracing::trace!(?params);

    let GotoDeclarationParams {
        text_document_position_params:
            TextDocumentPositionParams {
                text_document,
                position,
            },
        ..
    } = params;

    let Some(root) = backend.get_incomplete_ast(&text_document.uri).await else {
        return Ok(None);
    };

    let source_schema = backend
        .schema_store
        .try_get_source_schema_from_ast(&root, Some(Either::Left(&text_document.uri)))
        .await
        .ok()
        .flatten();

    let (toml_version, _) = backend.source_toml_version(source_schema.as_ref()).await;

    let Some((keys, _)) = get_hover_range(&root, position.into(), toml_version).await else {
        return Ok(None);
    };

    if let Some(location) =
        tombi_cargo_extension::goto_declaration(&text_document, &keys, toml_version).await?
    {
        return Ok(Some(GotoDeclarationResponse::Scalar(location)));
    }

    if let Some(location) =
        tombi_uv_extension::goto_declaration(&text_document, &keys, toml_version).await?
    {
        return Ok(Some(GotoDeclarationResponse::Scalar(location)));
    }

    Ok(None)
}
