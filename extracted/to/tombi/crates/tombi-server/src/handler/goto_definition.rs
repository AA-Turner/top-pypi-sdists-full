use itertools::Either;
use tower_lsp::lsp_types::{
    GotoDefinitionParams, GotoDefinitionResponse, TextDocumentPositionParams,
};

use crate::handler::hover::get_hover_range;
use crate::Backend;

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_goto_definition(
    backend: &Backend,
    params: GotoDefinitionParams,
) -> Result<Option<GotoDefinitionResponse>, tower_lsp::jsonrpc::Error> {
    tracing::info!("handle_goto_definition");
    tracing::trace!(?params);

    let GotoDefinitionParams {
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
        tombi_cargo_extension::goto_definition(&text_document, &keys, toml_version).await?
    {
        return Ok(Some(GotoDefinitionResponse::Scalar(location)));
    }

    if let Some(location) =
        tombi_uv_extension::goto_definition(&text_document, &keys, toml_version).await?
    {
        return Ok(Some(GotoDefinitionResponse::Scalar(location)));
    }

    Ok(None)
}
