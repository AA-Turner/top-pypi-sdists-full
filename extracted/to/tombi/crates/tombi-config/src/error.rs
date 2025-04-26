use url::Url;

#[derive(thiserror::Error, Debug)]
pub enum Error {
    #[error("unsupported config url: {config_url}")]
    ConfigUrlUnsupported { config_url: Url },

    #[error("failed to parse config url: {config_url}")]
    ConfigUrlParseFailed { config_url: Url },

    #[error("config file not found: {config_path:?}")]
    ConfigFileNotFound { config_path: std::path::PathBuf },

    #[error("failed to read {config_path:?}")]
    ConfigFileReadFailed { config_path: std::path::PathBuf },

    #[error("failed to parse {config_path:?}")]
    ConfigFileParseFailed { config_path: std::path::PathBuf },

    #[error("unsupported config file: {config_path:?}")]
    ConfigFileUnsupported { config_path: std::path::PathBuf },
}
