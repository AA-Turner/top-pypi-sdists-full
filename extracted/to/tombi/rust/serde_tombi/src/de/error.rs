#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error(transparent)]
    Io(#[from] std::io::Error),

    #[error(transparent)]
    Config(#[from] tombi_config::Error),

    #[error(transparent)]
    SchemaStore(#[from] tombi_schema_store::Error),

    #[error("cannot get schema url from document comment: {error} at {url_range}")]
    DocumentCommentSchemaUrl {
        error: tombi_schema_store::Error,
        url_range: tombi_text::Range,
    },

    #[error(transparent)]
    DocumentDeserialize(#[from] tombi_document::de::Error),

    #[error("{}", .0.iter().map(|e| e.to_string()).collect::<Vec<_>>().join(", "))]
    Parser(Vec<tombi_parser::Error>),

    #[error("{}", .0.iter().map(|e| e.to_string()).collect::<Vec<_>>().join(", "))]
    DocumentTree(Vec<tombi_document_tree::Error>),
}
