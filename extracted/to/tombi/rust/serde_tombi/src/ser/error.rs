#[derive(thiserror::Error, Debug)]
#[non_exhaustive]
pub enum Error {
    #[error(transparent)]
    Io(#[from] std::io::Error),

    #[error(transparent)]
    Config(#[from] tombi_config::Error),

    #[error(transparent)]
    SchemaStore(#[from] tombi_schema_store::Error),

    #[error("Document root must be a Table, got {0}")]
    RootMustBeTable(tombi_document::ValueKind),

    #[error("Key must be a String, got {1} for {0}")]
    KeyMustBeString(tombi_schema_store::Accessors, tombi_document::ValueKind),

    #[error("Key is required for {0}")]
    KeyRequired(tombi_schema_store::Accessors),

    #[error("Value is required for {0}")]
    ValueRequired(tombi_schema_store::Accessors),

    #[error("{error} for {accessors}")]
    DateTimeParseFailed {
        accessors: tombi_schema_store::Accessors,
        error: tombi_date_time::parse::Error,
    },

    #[error("TOML must be UTF-8 encoded")]
    TomlMustBeUtf8,

    #[error("{0} required")]
    ArrayValueRequired(tombi_schema_store::Accessors),

    #[error("TOML does not support unit values")]
    SerializeUnit,

    #[error("TOML does not support unit structs")]
    SerializeUnitStruct,

    #[error("{0}")]
    Serde(std::string::String),
}

impl serde::ser::Error for Error {
    fn custom<T: std::fmt::Display>(msg: T) -> Self {
        Error::Serde(msg.to_string())
    }
}
