use crate::hashing::djb2;
use crate::networking::{DEFAULT_CDN_SPECS_URL, ResponseData, config_specs_url};
use crate::specs_adapter::statsig_http_specs_adapter::SpecsSyncTrigger;
use crate::specs_adapter::{SpecsAdapter, SpecsSource, SpecsUpdate, SpecsUpdateListener};
use crate::specs_response::{
    spec_types::SpecsResponseFull, specs_hash_map::raw_spec_has_unhydrated_remote_config_metadata,
};
use crate::statsig_err::StatsigErr;
use crate::{StatsigOptions, StatsigRuntime, log_e, log_w};
use async_trait::async_trait;
use chrono::Utc;
use parking_lot::RwLock;
use serde_json::value::RawValue;
use std::{collections::HashMap, sync::Arc, time::Duration};

use super::{SpecsInfo, StatsigHttpSpecsAdapter};

const TAG: &str = stringify!(StatsigLocalFileSpecsAdapter);
type RawJsonObject = HashMap<String, Box<RawValue>>;

pub struct StatsigLocalFileSpecsAdapter {
    file_path: String,
    listener: RwLock<Option<Arc<dyn SpecsUpdateListener>>>,
    http_adapter: StatsigHttpSpecsAdapter,
    hydration_source_url: String,
}

impl StatsigLocalFileSpecsAdapter {
    #[must_use]
    pub fn new(
        sdk_key: &str,
        output_directory: &str,
        specs_url: Option<String>,
        fallback_to_statsig_api: bool,
        disable_network: bool,
    ) -> Self {
        let hashed_key = djb2(sdk_key);
        let file_path = format!("{output_directory}/{hashed_key}_specs.json");
        let hydration_source_url =
            config_specs_url(specs_url.as_deref().unwrap_or(DEFAULT_CDN_SPECS_URL));

        let options = StatsigOptions {
            specs_url,
            disable_network: Some(disable_network),
            fallback_to_statsig_api: Some(fallback_to_statsig_api),
            ..Default::default()
        };

        Self {
            file_path,
            listener: RwLock::new(None),
            http_adapter: StatsigHttpSpecsAdapter::new(sdk_key, Some(&options), None),
            hydration_source_url,
        }
    }

    pub async fn fetch_and_write_to_file(&self) -> Result<(), StatsigErr> {
        let specs_info = match self.read_hydrated_specs_from_file().await {
            Ok(Some(specs)) => SpecsInfo {
                lcut: Some(specs.time),
                checksum: specs.checksum,
                source: SpecsSource::Adapter("FileBased".to_owned()),
                source_api: None,
            },
            Ok(None) => SpecsInfo::empty(),
            Err(error) => {
                log_w!(TAG, "Failed to hydrate existing specs file: {}", error);
                SpecsInfo::empty()
            }
        };

        let mut response = self
            .http_adapter
            .fetch_hydrated_specs_from_network(specs_info, SpecsSyncTrigger::Manual)
            .await?;
        let data = response
            .data
            .read_to_string()
            .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;

        if let Some(response) = self.parse_specs_data_to_full_response(&data) {
            if response.has_updates {
                self.write_specs_to_file_bytes(data.as_bytes());
            }
        }

        Ok(())
    }

    /// Replays a local file after hydrating and rewriting any legacy remote
    /// config placeholders it contains.
    pub async fn resync_from_file_with_hydration(&self) -> Result<(), StatsigErr> {
        let data = self
            .read_hydrated_response_data_from_file()
            .await?
            .ok_or_else(|| StatsigErr::FileError("Specs file does not exist".to_string()))?;
        self.send_response_data_to_listener(data)
    }

    pub fn resync_from_file(&self) -> Result<(), StatsigErr> {
        let bytes = match std::fs::read(&self.file_path) {
            Ok(data) => data,
            Err(e) => {
                return Err(StatsigErr::FileError(e.to_string()));
            }
        };
        if may_have_remote_config_metadata(&bytes) {
            return Err(StatsigErr::InvalidOperation(
                "Legacy remote config metadata requires resync_from_file_with_hydration"
                    .to_string(),
            ));
        }

        self.send_response_data_to_listener(ResponseData::from_bytes(bytes))
    }

    async fn read_hydrated_specs_from_file(&self) -> Result<Option<SpecsResponseFull>, StatsigErr> {
        let Some(mut data) = self.read_hydrated_response_data_from_file().await? else {
            return Ok(None);
        };

        Ok(match data.deserialize_into::<SpecsResponseFull>() {
            Ok(response) => Some(response),
            Err(e) => {
                log_w!(TAG, "Failed to parse specs data: {}", e);
                None
            }
        })
    }

    async fn read_hydrated_response_data_from_file(
        &self,
    ) -> Result<Option<ResponseData>, StatsigErr> {
        if !std::path::Path::new(&self.file_path).exists() {
            return Ok(None);
        }

        let original =
            std::fs::read(&self.file_path).map_err(|e| StatsigErr::FileError(e.to_string()))?;
        if !may_have_remote_config_metadata(&original) {
            return Ok(Some(ResponseData::from_bytes(original)));
        }

        let mut data = ResponseData::from_bytes(original.clone());
        self.http_adapter
            .hydrate_response_data(&mut data, &self.hydration_source_url)
            .await?;
        let hydrated = data.read_to_bytes()?;
        if hydrated != original {
            self.write_specs_to_file_bytes(&hydrated);
        }

        Ok(Some(ResponseData::from_bytes(hydrated)))
    }

    fn send_response_data_to_listener(&self, data: ResponseData) -> Result<(), StatsigErr> {
        match &self
            .listener
            .try_read_for(std::time::Duration::from_secs(5))
        {
            Some(lock) => match lock.as_ref() {
                Some(listener) => listener.did_receive_specs_update(SpecsUpdate {
                    data,
                    source: SpecsSource::Adapter("FileBased".to_owned()),
                    received_at: Utc::now().timestamp_millis() as u64,
                    source_api: None,
                    has_updates: None,
                }),
                None => Err(StatsigErr::UnstartedAdapter("Listener not set".to_string())),
            },
            None => Err(StatsigErr::LockFailure(
                "Failed to acquire read lock on listener".to_string(),
            )),
        }
    }

    fn parse_specs_data_to_full_response(&self, data: &str) -> Option<SpecsResponseFull> {
        match serde_json::from_slice::<SpecsResponseFull>(data.as_bytes()) {
            Ok(response) => Some(response),
            Err(e) => {
                log_w!(TAG, "Failed to parse specs data: {}", e);
                None
            }
        }
    }

    fn write_specs_to_file_bytes(&self, data: &[u8]) {
        match std::fs::write(&self.file_path, data) {
            Ok(()) => (),
            Err(e) => log_w!(TAG, "Failed to write specs to file: {}", e),
        }
    }
}

fn may_have_remote_config_metadata(bytes: &[u8]) -> bool {
    const METADATA_KEY: &str = "remoteConfigMetadata";

    // The same key is legal inside an ordinary user-provided JSON value. Only
    // producer-owned dynamic-config and rule fields require async hydration.
    if !bytes
        .windows(METADATA_KEY.len())
        .any(|window| window == METADATA_KEY.as_bytes())
        && !bytes.windows(2).any(|window| window == b"\\u")
    {
        return false;
    }

    // Keep response/config values raw for the same reason as the JSON
    // decoder guard: arbitrary user number lexemes must not hide metadata.
    let Ok(payload) = serde_json::from_slice::<RawJsonObject>(bytes) else {
        return false;
    };
    let Some(configs) = payload.get("dynamic_configs") else {
        return false;
    };
    let Ok(configs) = serde_json::from_str::<RawJsonObject>(configs.get()) else {
        return false;
    };
    configs
        .values()
        .any(|config| raw_spec_has_unhydrated_remote_config_metadata(config.get()))
}

#[async_trait]
impl SpecsAdapter for StatsigLocalFileSpecsAdapter {
    async fn start(
        self: Arc<Self>,
        _statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        self.resync_from_file_with_hydration().await
    }

    fn initialize(&self, listener: Arc<dyn SpecsUpdateListener>) {
        match self
            .listener
            .try_write_for(std::time::Duration::from_secs(5))
        {
            Some(mut lock) => *lock = Some(listener),
            None => {
                log_e!(TAG, "Failed to acquire write lock on listener");
            }
        }
    }

    async fn shutdown(
        &self,
        _timeout: Duration,
        _statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        Ok(())
    }

    async fn schedule_background_sync(
        self: Arc<Self>,
        _statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        Ok(())
    }

    fn get_type_name(&self) -> String {
        stringify!(StatsigLocalFileSpecsAdapter).to_string()
    }
}
