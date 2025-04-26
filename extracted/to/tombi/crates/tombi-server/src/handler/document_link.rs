use tower_lsp::lsp_types::{DocumentLink, DocumentLinkParams};

use crate::Backend;

pub async fn handle_document_link(
    backend: &Backend,
    params: DocumentLinkParams,
) -> Result<Option<Vec<DocumentLink>>, tower_lsp::jsonrpc::Error> {
    tracing::info!("handle_document_link");
    tracing::trace!(?params);

    let DocumentLinkParams { text_document, .. } = params;

    let Some(root) = backend.get_incomplete_ast(&text_document.uri).await else {
        return Ok(None);
    };

    let mut document_links = vec![];

    // Document Inline Comment Schema URL
    //
    // ```toml
    // #:schema https://example.com/schema.json
    // key = "value"
    // ```
    if let Some((Ok(schema_url), range)) =
        root.file_schema_url(text_document.uri.to_file_path().ok().as_deref())
    {
        let tooltip = format!("Open schema: {}", schema_url);
        document_links.push(DocumentLink {
            range: range.into(),
            target: Some(schema_url),
            data: None,
            tooltip: Some(tooltip),
        });
    }
    Ok(Some(document_links))
}
