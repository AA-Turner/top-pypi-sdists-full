use tombi_config::SchemaOptions;
use tombi_schema_store::json::CatalogUrl;
use tower_lsp::lsp_types::{InitializedParams, MessageType};

use crate::backend::Backend;

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_initialized(backend: &Backend, params: InitializedParams) {
    tracing::info!("handle_initialized");
    tracing::trace!(?params);

    load_schemas(backend).await;
}

async fn load_schemas(backend: &Backend) {
    let config = backend.config().await;
    let schema_options = match &config.schema {
        Some(schema) => schema,
        None => &SchemaOptions::default(),
    };

    if schema_options.enabled.unwrap_or_default().value() {
        backend
            .schema_store
            .load_schemas(
                match &config.schemas {
                    Some(schemas) => schemas,
                    None => &[],
                },
                backend.config_dirpath.as_deref(),
            )
            .await;

        for catalog_path in schema_options.catalog_paths().unwrap_or_default().iter() {
            if let Ok(catalog_url) =
                catalog_path.try_to_catalog_url(backend.config_dirpath.as_deref())
            {
                if let Err(err) = backend
                    .schema_store
                    .load_schemas_from_catalog_url(&CatalogUrl::new(catalog_url))
                    .await
                {
                    let Ok(_) = backend
                        .client
                        .show_message_request(MessageType::ERROR, err.to_string(), None)
                        .await
                    else {
                        continue;
                    };
                }
            } else {
                let Ok(_) = backend
                    .client
                    .show_message_request(
                        MessageType::ERROR,
                        format!("invalid catalog url: {:?}", &catalog_path),
                        None,
                    )
                    .await
                else {
                    continue;
                };
            }
        }
    }
}
