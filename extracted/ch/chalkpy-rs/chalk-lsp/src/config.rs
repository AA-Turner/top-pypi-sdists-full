use std::path::PathBuf;

use clap::ValueEnum;
use serde::Deserialize;

#[derive(Clone, Debug, Default, Deserialize, PartialEq, Eq)]
#[serde(default)]
pub struct Configuration {
    pub chalk: ChalkSettings,
}

impl Configuration {
    pub fn from_json(config: &str) -> serde_json::Result<Self> {
        Self::from_lsp_value(&serde_json::from_str(config)?)
    }

    pub fn from_lsp_value(value: &serde_json::Value) -> serde_json::Result<Self> {
        serde_json::from_value(value.get("settings").unwrap_or(value).clone())
    }
}

#[derive(Clone, Debug, Deserialize, PartialEq, Eq)]
#[serde(default, rename_all = "camelCase")]
pub struct ChalkSettings {
    pub linters: Vec<Linter>,
    pub remote_diagnostics: RemoteDiagnosticsSettings,
}

impl Default for ChalkSettings {
    fn default() -> Self {
        Self {
            linters: vec![Linter::Local, Linter::Accel],
            remote_diagnostics: RemoteDiagnosticsSettings::default(),
        }
    }
}

#[derive(Clone, Copy, Debug, Deserialize, PartialEq, Eq, ValueEnum)]
#[serde(rename_all = "lowercase")]
pub enum Linter {
    Local,
    Remote,
    Accel,
}

#[derive(Clone, Debug, Default, Deserialize, PartialEq, Eq)]
#[serde(default, rename_all = "camelCase")]
pub struct RemoteDiagnosticsSettings {
    pub api_host: Option<String>,
    pub chalkpy_path_override: Option<PathBuf>,
}
