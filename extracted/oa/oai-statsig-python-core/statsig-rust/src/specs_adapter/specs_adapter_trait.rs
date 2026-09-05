use crate::StatsigRuntime;
use crate::networking::ResponseData;
use crate::statsig_err::StatsigErr;
use async_trait::async_trait;
use serde::Deserialize;
use serde::Serialize;
use std::fmt::{self, Debug};
use std::sync::Arc;
use std::time::Duration;

use super::remote_config_value_hydrator::RemoteConfigValueHydrator;

#[repr(u8)]
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum SpecsSource {
    Uninitialized = 0,
    NoValues,
    Error,
    Loading,
    Bootstrap,
    Adapter(String),
    Network,
}

const DEFAULT_CONFIG_COMPRESSION_MODE: ConfigCompressionMode = ConfigCompressionMode::Gzip;

#[derive(Clone)]
pub enum ConfigCompressionMode {
    Gzip,
    Dictionary,
}

impl From<&str> for ConfigCompressionMode {
    fn from(s: &str) -> Self {
        match s.to_lowercase().as_str() {
            "gzip" => ConfigCompressionMode::Gzip,
            "dictionary" => ConfigCompressionMode::Dictionary,
            _ => DEFAULT_CONFIG_COMPRESSION_MODE,
        }
    }
}

impl SpecsSource {
    pub fn new_from_string(s: &str) -> Self {
        if s.starts_with("Adapter(") {
            let name = s
                .strip_prefix("Adapter(")
                .and_then(|s| s.strip_suffix(")"))
                .unwrap_or("");
            return SpecsSource::Adapter(name.to_string());
        }

        match s {
            "Uninitialized" => SpecsSource::Uninitialized,
            "NoValues" => SpecsSource::NoValues,
            "Error" => SpecsSource::Error,
            "Loading" => SpecsSource::Loading,
            "Bootstrap" => SpecsSource::Bootstrap,
            "Network" => SpecsSource::Network,
            _ => SpecsSource::Error,
        }
    }
}

impl fmt::Display for SpecsSource {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let s = match self {
            SpecsSource::Adapter(name) => {
                let type_name = format!("Adapter({name})");
                type_name
            }
            SpecsSource::Uninitialized => "Uninitialized".to_string(),
            SpecsSource::NoValues => "NoValues".to_string(),
            SpecsSource::Error => "Error".to_string(),
            SpecsSource::Loading => "Loading".to_string(),
            SpecsSource::Network => "Network".to_string(),
            SpecsSource::Bootstrap => "Bootstrap".to_string(),
        };
        write!(f, "{s}")
    }
}

#[async_trait]
pub trait SpecsAdapter: Send + Sync {
    fn initialize(&self, listener: Arc<dyn SpecsUpdateListener>);

    async fn start(
        self: Arc<Self>,
        statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr>;

    async fn shutdown(
        &self,
        timeout: Duration,
        statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr>;

    async fn schedule_background_sync(
        self: Arc<Self>,
        statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr>;

    fn get_type_name(&self) -> String;
}

pub enum SpecsFormat {
    Json,
    Protobuf,
}

impl From<&SpecsFormat> for &str {
    fn from(val: &SpecsFormat) -> Self {
        match val {
            SpecsFormat::Json => "JSON",
            SpecsFormat::Protobuf => "Protobuf",
        }
    }
}

pub struct SpecsUpdate {
    pub data: ResponseData,
    pub source: SpecsSource,
    pub received_at: u64,
    pub source_api: Option<String>,
    pub has_updates: Option<bool>,
}

/// Internal context used by async adapters that can hydrate remote dynamic
/// config values before publishing an update. The public shape keeps
/// SpecsUpdateListener backwards compatible for custom listener
/// implementations while letting SpecStore fold protobuf hydration into its
/// parser.
#[doc(hidden)]
pub struct SpecsUpdateHydration {
    pub(crate) hydrator: Arc<RemoteConfigValueHydrator>,
    pub(crate) source_url: String,
}

impl SpecsUpdateHydration {
    pub(crate) fn new(hydrator: Arc<RemoteConfigValueHydrator>, source_url: String) -> Self {
        Self {
            hydrator,
            source_url,
        }
    }
}

/// Advances the sync cursor when an adapter proves the semantic payload checksum is unchanged.
#[doc(hidden)]
pub struct SpecsCursorUpdate {
    pub lcut: u64,
    pub checksum: String,
    pub source: SpecsSource,
    pub source_api: Option<String>,
}

#[repr(C)]
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct SpecsInfo {
    pub lcut: Option<u64>,
    pub checksum: Option<String>,
    pub source: SpecsSource,
    pub source_api: Option<String>,
}

impl SpecsInfo {
    #[must_use]
    pub fn empty() -> Self {
        Self {
            lcut: None,
            checksum: None,
            source: SpecsSource::NoValues,
            source_api: None,
        }
    }

    #[must_use]
    pub fn error() -> Self {
        Self {
            lcut: None,
            checksum: None,
            source: SpecsSource::Error,
            source_api: None,
        }
    }
}

#[async_trait]
pub trait SpecsUpdateListener: Send + Sync {
    fn did_receive_specs_update(&self, update: SpecsUpdate) -> Result<(), StatsigErr>;

    /// Async adapters use this entry point when they have enough context to
    /// hydrate remote values. Existing/custom listeners keep their synchronous
    /// behavior through this default implementation.
    async fn did_receive_specs_update_async(
        &self,
        mut update: SpecsUpdate,
        hydration: Option<SpecsUpdateHydration>,
    ) -> Result<(), StatsigErr> {
        if let Some(hydration) = hydration {
            hydration
                .hydrator
                .hydrate_response(&mut update.data, &hydration.source_url)
                .await?;
        }

        self.did_receive_specs_update(update)
    }

    /// Existing listeners may ignore cursor-only updates. The SDK SpecStore uses this to avoid
    /// re-reading an unchanged payload when only the upstream LCUT advances.
    fn did_advance_specs_cursor(&self, _update: SpecsCursorUpdate) -> Result<(), StatsigErr> {
        Ok(())
    }

    fn get_current_specs_info(&self) -> SpecsInfo;
}

impl fmt::Debug for dyn SpecsAdapter {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.get_type_name())
    }
}
