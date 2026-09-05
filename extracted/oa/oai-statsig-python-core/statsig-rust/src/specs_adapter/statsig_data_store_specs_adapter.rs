use super::config_spec_background_sync_metrics::log_config_sync_overall_latency;
use super::remote_config_value_hydrator::RemoteConfigValueHydrator;
use super::response_format::get_specs_response_format;
use super::statsig_http_specs_adapter::DEFAULT_SYNC_INTERVAL_MS;
use super::{SpecsSource, SpecsUpdate, SpecsUpdateHydration};
use crate::data_store_interface::{
    DataStoreBytesResponse, DataStoreCacheKeys, DataStoreGetBytesRequest, DataStoreResponse,
    DataStoreTrait, ENABLE_DCS_ZSTD_DATASTORE_FLAG, RequestPath,
};
use crate::networking::{DEFAULT_CDN_SPECS_URL, NetworkClient, ResponseData, config_specs_url};
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::specs_response::proto_compression::ProtoCompression;
use crate::specs_response::proto_stream_reader::BUFFER_SIZE;
use crate::specs_response::statsig_config_specs as pb;
use crate::statsig_metadata::StatsigMetadata;
use crate::{
    SpecsAdapter, SpecsUpdateListener, log_d, log_e, log_w, read_lock_or_else, unwrap_or_else,
    write_lock_or_else,
};
use crate::{StatsigErr, StatsigOptions, StatsigRuntime};
use async_trait::async_trait;
use chrono::Utc;
use parking_lot::RwLock;
use prost::Message;
use std::collections::HashMap;
use std::{io::Read, sync::Arc, time::Duration};
use tokio::sync::Notify;
use tokio::time::{self, sleep};

const TAG: &str = "StatsigDataStoreSpecsAdapter";

pub struct StatsigDataStoreSpecsAdapter {
    data_store: Arc<dyn DataStoreTrait>,
    cache_keys: DataStoreCacheKeys,
    sync_interval: Duration,
    ops_stats: Arc<OpsStatsForInstance>,
    remote_config_value_hydrator: Arc<RemoteConfigValueHydrator>,
    hydration_source_url: String,
    allow_dcs_zstd: bool,
    listener: RwLock<Option<Arc<dyn SpecsUpdateListener>>>,
    shutdown_notify: Arc<Notify>,
}

struct CachedSpecs {
    result: Option<Vec<u8>>,
    proto_compression: Option<ProtoCompression>,
    time: Option<u64>,
    checksum: Option<String>,
    has_updates: Option<bool>,
}

#[derive(Clone, PartialEq, prost::Message)]
struct CachedSnapshotCursor {
    #[prost(uint64, tag = "2")]
    lcut: u64,
    #[prost(string, tag = "5")]
    checksum: String,
}

#[derive(Clone, PartialEq, prost::Message)]
struct CachedSnapshotEnvelope {
    #[prost(int32, tag = "1")]
    kind: i32,
    #[prost(bytes = "bytes", optional, tag = "4")]
    data: Option<bytes::Bytes>,
}

impl StatsigDataStoreSpecsAdapter {
    pub fn new(
        sdk_key: &str,
        data_store_key: &str,
        data_store: Arc<dyn DataStoreTrait>,
        options: Option<&StatsigOptions>,
        hydration_specs_url_override: Option<&str>,
    ) -> Self {
        let default_options = StatsigOptions::default();
        let options_ref = options.unwrap_or(&default_options);

        let sdk_instance_id = options_ref.get_sdk_instance_id(sdk_key);
        let ops_stats = OPS_STATS.get_for_instance(sdk_instance_id);
        let hydration_specs_url = options_ref
            .remote_config_value_source_url
            .as_deref()
            .or(hydration_specs_url_override)
            .or(options_ref.specs_url.as_deref())
            .unwrap_or(DEFAULT_CDN_SPECS_URL);
        let network = Arc::new(NetworkClient::new(
            sdk_key,
            Some(StatsigMetadata::get_constant_request_headers(
                sdk_key,
                options_ref.service_name.as_deref(),
            )),
            Some(options_ref),
        ));
        let allow_dcs_zstd = options_ref
            .experimental_flags
            .as_ref()
            .is_some_and(|flags| flags.contains(ENABLE_DCS_ZSTD_DATASTORE_FLAG));
        StatsigDataStoreSpecsAdapter {
            data_store,
            cache_keys: DataStoreCacheKeys::from_selected_key(data_store_key),
            sync_interval: Duration::from_millis(u64::from(
                options_ref
                    .specs_sync_interval_ms
                    .unwrap_or(DEFAULT_SYNC_INTERVAL_MS),
            )),
            remote_config_value_hydrator: Arc::new(RemoteConfigValueHydrator::new_with_ops_stats(
                network,
                ops_stats.clone(),
            )),
            hydration_source_url: config_specs_url(hydration_specs_url),
            allow_dcs_zstd,
            ops_stats,
            listener: RwLock::new(None),
            shutdown_notify: Arc::new(Notify::new()),
        }
    }
}

#[async_trait]
impl SpecsAdapter for StatsigDataStoreSpecsAdapter {
    async fn start(
        self: Arc<Self>,
        _statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        let sync_start_ms = Utc::now().timestamp_millis() as u64;
        self.data_store.initialize().await?;

        let update = self.load_cached_specs(None, None).await?;
        if update.result.is_none() && update.has_updates != Some(false) {
            return Err(StatsigErr::DataStoreFailure("Empty result".to_string()));
        }

        let listener = {
            let read_lock = read_lock_or_else!(self.listener, {
                return Err(StatsigErr::UnstartedAdapter(
                    "Failed to acquire read lock on listener".to_string(),
                ));
            });

            match read_lock.as_ref() {
                Some(listener) => listener.clone(),
                None => return Err(StatsigErr::UnstartedAdapter("Listener not set".to_string())),
            }
        };

        let (result, response_format) = self.send_specs_update_to_listener(&listener, update).await;
        self.log_data_store_sync_result(sync_start_ms, &response_format, &result);
        result
    }

    fn initialize(&self, listener: Arc<dyn SpecsUpdateListener>) {
        let mut write_lock = write_lock_or_else!(self.listener, {
            log_e!(TAG, "Failed to acquire write lock on listener");
            return;
        });

        *write_lock = Some(listener);
    }

    async fn schedule_background_sync(
        self: Arc<Self>,
        statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        // Support polling updates function should be pretty cheap. But we have to make it async
        let should_schedule = self
            .data_store
            .support_polling_updates_for(RequestPath::RulesetsV2)
            .await;

        if !should_schedule {
            return Err(StatsigErr::SpecsAdapterSkipPoll(self.get_type_name()));
        }

        let weak_self = Arc::downgrade(&self);

        statsig_runtime.spawn(
            "data_store_specs_adapter",
            move |rt_shutdown_notify| async move {
                let strong_self = if let Some(strong_self) = weak_self.upgrade() {
                    strong_self
                } else {
                    log_w!(TAG, "Failed to upgrade weak instance");
                    return;
                };

                strong_self
                    .execute_background_sync(&rt_shutdown_notify)
                    .await;
            },
        )?;

        Ok(())
    }

    async fn shutdown(
        &self,
        timeout: Duration,
        _statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        self.shutdown_notify.notify_one();
        time::timeout(timeout, async { self.data_store.shutdown().await })
            .await
            .map_err(|e| StatsigErr::DataStoreFailure(format!("Failed to shutdown: {e}")))?
    }

    fn get_type_name(&self) -> String {
        stringify!(StatsigDataStoreSpecAdapter).to_string()
    }
}

impl StatsigDataStoreSpecsAdapter {
    async fn load_cached_specs(
        &self,
        since_time: Option<u64>,
        checksum: Option<String>,
    ) -> Result<CachedSpecs, StatsigErr> {
        let compressed_update = if self.allow_dcs_zstd {
            self.load_compressed_cache(since_time, checksum.clone())
                .await?
        } else {
            self.load_statsig_br_cache(since_time, checksum.clone())
                .await?
        };

        if let Some(update) = compressed_update {
            return Ok(update);
        }

        self.load_plain_text_cache(since_time, checksum).await
    }

    async fn load_statsig_br_cache(
        &self,
        since_time: Option<u64>,
        checksum: Option<String>,
    ) -> Result<Option<CachedSpecs>, StatsigErr> {
        match self
            .load_cached_specs_bytes(
                &self.cache_keys.statsig_br,
                Some(ProtoCompression::Brotli),
                since_time,
                checksum,
            )
            .await
        {
            Ok(update) => Ok(update),
            Err(e @ StatsigErr::BytesNotImplemented) => {
                self.load_cached_specs_string(Some(e)).await.map(Some)
            }
            Err(e) => {
                log_w!(
                    TAG,
                    "Failed to read statsig-br specs bytes from data store. Trying plain text cache: {}",
                    e
                );
                Ok(None)
            }
        }
    }

    async fn load_compressed_cache(
        &self,
        since_time: Option<u64>,
        checksum: Option<String>,
    ) -> Result<Option<CachedSpecs>, StatsigErr> {
        let current_checksum = checksum.clone();
        // Datastores must return a missing codec sibling promptly before this
        // explicitly activated migration path can safely probe both keys.
        let (zstd_result, brotli_result) = tokio::join!(
            self.load_cached_specs_bytes(
                &self.cache_keys.statsig_zstd,
                Some(ProtoCompression::Zstd),
                since_time,
                checksum.clone(),
            ),
            self.load_cached_specs_bytes(
                &self.cache_keys.statsig_br,
                Some(ProtoCompression::Brotli),
                since_time,
                checksum,
            ),
        );

        let mut candidates = Vec::with_capacity(2);
        let mut errors = Vec::new();
        let mut bytes_not_implemented_count = 0;

        for (compression, result) in [
            (ProtoCompression::Zstd, zstd_result),
            (ProtoCompression::Brotli, brotli_result),
        ] {
            match result {
                Ok(Some(update)) => candidates.push(update),
                Ok(None) => {}
                Err(StatsigErr::BytesNotImplemented) => {
                    bytes_not_implemented_count += 1;
                }
                Err(e) => errors.push(format!("{}: {e}", compression.content_encoding())),
            }
        }

        if let Some(update) =
            select_newest_compressed_cache(candidates, since_time, current_checksum.as_deref())
        {
            return Ok(Some(update));
        }

        if bytes_not_implemented_count == 2 {
            return self
                .load_cached_specs_string(Some(StatsigErr::BytesNotImplemented))
                .await
                .map(Some);
        }

        if !errors.is_empty() {
            log_w!(
                TAG,
                "Failed to read compressed protobuf specs from data store. Trying plain text cache: {}",
                errors.join(", ")
            );
        }

        Ok(None)
    }

    async fn load_plain_text_cache(
        &self,
        since_time: Option<u64>,
        checksum: Option<String>,
    ) -> Result<CachedSpecs, StatsigErr> {
        match self
            .load_cached_specs_bytes(&self.cache_keys.plain_text, None, since_time, checksum)
            .await
        {
            Ok(Some(update)) => Ok(update),
            Ok(None) => Ok(CachedSpecs {
                result: None,
                proto_compression: None,
                time: None,
                checksum: None,
                has_updates: None,
            }),
            Err(e @ StatsigErr::BytesNotImplemented) => {
                self.load_cached_specs_string(Some(e)).await
            }
            Err(e) => Err(e),
        }
    }

    async fn load_cached_specs_bytes(
        &self,
        key: &str,
        proto_compression: Option<ProtoCompression>,
        since_time: Option<u64>,
        checksum: Option<String>,
    ) -> Result<Option<CachedSpecs>, StatsigErr> {
        let response = self
            .data_store
            .get_bytes(
                key,
                DataStoreGetBytesRequest {
                    since_time,
                    checksum,
                },
            )
            .await?;
        Ok(cached_specs_from_bytes_response(
            response,
            proto_compression,
        ))
    }

    async fn load_cached_specs_string(
        &self,
        bytes_error: Option<StatsigErr>,
    ) -> Result<CachedSpecs, StatsigErr> {
        if let Some(e) = bytes_error {
            match e {
                StatsigErr::BytesNotImplemented => {}
                _ => {
                    log_w!(
                        TAG,
                        "Failed to read specs from data store as bytes. Falling back to string read: {}",
                        e
                    );
                }
            }
        }

        let response = self.data_store.get(&self.cache_keys.plain_text).await?;
        Ok(cached_specs_from_string_response(response))
    }

    fn specs_response_data_from_cache(
        data: Vec<u8>,
        proto_compression: Option<ProtoCompression>,
    ) -> ResponseData {
        if let Some(proto_compression) = proto_compression {
            return Self::binary_specs_response_data_from_bytes(data, proto_compression);
        }

        ResponseData::from_bytes(data)
    }

    fn binary_specs_response_data_from_bytes(
        bytes: Vec<u8>,
        proto_compression: ProtoCompression,
    ) -> ResponseData {
        ResponseData::from_bytes_with_headers(
            bytes,
            Some(HashMap::from([
                (
                    "content-type".to_string(),
                    "application/octet-stream".to_string(),
                ),
                (
                    "content-encoding".to_string(),
                    proto_compression.content_encoding().to_string(),
                ),
            ])),
        )
    }

    async fn send_specs_update_to_listener(
        &self,
        listener: &Arc<dyn SpecsUpdateListener>,
        cached_specs: CachedSpecs,
    ) -> (Result<(), StatsigErr>, String) {
        let _ = (&cached_specs.time, &cached_specs.checksum);

        let has_result = cached_specs.result.is_some();
        let data = Self::specs_response_data_from_cache(
            cached_specs.result.unwrap_or_default(),
            cached_specs.proto_compression,
        );
        let response_format = get_specs_response_format(&data);

        let hydration = has_result.then(|| {
            SpecsUpdateHydration::new(
                self.remote_config_value_hydrator.clone(),
                self.hydration_source_url.clone(),
            )
        });
        let result = listener
            .did_receive_specs_update_async(
                SpecsUpdate {
                    data,
                    source: SpecsSource::Adapter("DataStore".to_string()),
                    received_at: Utc::now().timestamp_millis() as u64,
                    source_api: Some("datastore".to_string()),
                    has_updates: cached_specs.has_updates,
                },
                hydration,
            )
            .await;

        (result, response_format.as_str().to_string())
    }

    fn log_data_store_sync_result(
        &self,
        sync_start_ms: u64,
        response_format: &str,
        result: &Result<(), StatsigErr>,
    ) {
        log_config_sync_overall_latency(
            &self.ops_stats,
            sync_start_ms,
            "datastore",
            response_format,
            false,
            result.is_ok(),
            result
                .as_ref()
                .err()
                .map_or_else(String::new, |e| e.to_string()),
            false,
            "datastore",
        );
    }

    async fn execute_background_sync(&self, rt_shutdown_notify: &Arc<Notify>) {
        loop {
            tokio::select! {
                () = sleep(self.sync_interval) => self.execute_background_sync_impl().await,
                () = rt_shutdown_notify.notified() => {
                    log_d!(TAG, "Runtime shutdown. Shutting down specs background sync");
                    break;
                }
                () = self.shutdown_notify.notified() => {
                    log_d!(TAG, "Shutting down specs background sync");
                    break;
                }
            }
        }
    }

    async fn execute_background_sync_impl(&self) {
        let sync_start_ms = Utc::now().timestamp_millis() as u64;
        let listener = {
            let read_lock = read_lock_or_else!(self.listener, {
                log_w!(TAG, "Unable to acquire read lock on listener");
                return;
            });

            unwrap_or_else!(read_lock.as_ref(), {
                log_w!(TAG, "Listener not set");
                return;
            })
            .clone()
        };

        let update = match self.load_cached_specs_from_listener(&listener).await {
            Ok(update) => update,
            Err(e) => {
                log_w!(TAG, "Failed to read for data store: {e}");
                return;
            }
        };

        let (result, response_format) = self.send_specs_update_to_listener(&listener, update).await;
        self.log_data_store_sync_result(sync_start_ms, &response_format, &result);

        if let Err(e) = result {
            log_w!(TAG, "Failed to send specs update to listener: {e}");
        }
    }

    async fn load_cached_specs_from_listener(
        &self,
        listener: &Arc<dyn SpecsUpdateListener>,
    ) -> Result<CachedSpecs, StatsigErr> {
        let spec_info = listener.get_current_specs_info();
        self.load_cached_specs(spec_info.lcut, spec_info.checksum)
            .await
    }
}

fn cached_specs_from_bytes_response(
    response: DataStoreBytesResponse,
    proto_compression: Option<ProtoCompression>,
) -> Option<CachedSpecs> {
    if response.result.is_none() && response.has_updates != Some(false) {
        return None;
    }

    Some(CachedSpecs {
        result: response.result,
        proto_compression,
        time: response.time,
        checksum: response.checksum,
        has_updates: response.has_updates,
    })
}

fn cached_specs_from_string_response(response: DataStoreResponse) -> CachedSpecs {
    CachedSpecs {
        result: response.result.map(String::into_bytes),
        proto_compression: None,
        time: response.time,
        checksum: response.checksum,
        has_updates: response.has_updates,
    }
}

fn select_newest_compressed_cache(
    candidates: Vec<CachedSpecs>,
    current_lcut: Option<u64>,
    current_checksum: Option<&str>,
) -> Option<CachedSpecs> {
    let current_checksum = current_checksum.filter(|checksum| !checksum.is_empty());
    let (mut updates, no_updates): (Vec<_>, Vec<_>) = candidates
        .into_iter()
        .partition(|candidate| candidate.has_updates != Some(false));
    let no_update = no_updates.into_iter().max_by_key(|candidate| {
        (
            candidate.time.unwrap_or_default(),
            matches!(candidate.proto_compression, Some(ProtoCompression::Zstd)),
        )
    });

    if updates.is_empty() {
        return current_lcut.and(no_update);
    }

    if updates.len() == 1 {
        let update = updates.pop()?;
        if let (Some(no_update), Some(current_lcut)) = (no_update, current_lcut) {
            let Some(cursor) = cached_snapshot_cursor(&update) else {
                return Some(no_update);
            };
            let current_peer = no_update
                .checksum
                .as_deref()
                .is_none_or(|checksum| current_checksum == Some(checksum));
            let update_is_newer = update
                .time
                .zip(no_update.time)
                .is_some_and(|(update_time, current_time)| update_time > current_time);
            // Without both write times a different checksum cannot be ordered
            // against the current snapshot. Preserve the current response to
            // avoid alternating between stale codec siblings on each poll.
            if (current_peer && current_checksum == Some(cursor.checksum.as_str()))
                || cursor.lcut < current_lcut
                || (cursor.lcut == current_lcut && current_peer && !update_is_newer)
            {
                return Some(no_update);
            }
        }

        return Some(update);
    }

    let compare_times = updates.iter().all(|candidate| candidate.time.is_some());
    updates.into_iter().max_by_key(|candidate| {
        let cursor = cached_snapshot_cursor(candidate);
        (
            cursor.is_some(),
            cursor.as_ref().map_or(0, |cursor| cursor.lcut),
            if compare_times { candidate.time } else { None },
            cursor.as_ref().is_some_and(|cursor| {
                current_checksum.is_some_and(|checksum| {
                    if current_lcut == Some(cursor.lcut) {
                        checksum == cursor.checksum
                    } else {
                        checksum != cursor.checksum
                    }
                })
            }),
            matches!(candidate.proto_compression, Some(ProtoCompression::Zstd)),
        )
    })
}

fn cached_snapshot_cursor(candidate: &CachedSpecs) -> Option<CachedSnapshotCursor> {
    let bytes = candidate.result.as_deref()?;
    match candidate.proto_compression? {
        ProtoCompression::Brotli => {
            decode_cached_snapshot_cursor(brotli::Decompressor::new(bytes, BUFFER_SIZE))
        }
        ProtoCompression::Zstd => {
            decode_cached_snapshot_cursor(zstd::stream::read::Decoder::new(bytes).ok()?)
        }
    }
}

fn decode_cached_snapshot_cursor(mut reader: impl Read) -> Option<CachedSnapshotCursor> {
    let mut delimiter = [0_u8; 10];
    let mut delimiter_len = 0;
    loop {
        reader
            .read_exact(&mut delimiter[delimiter_len..delimiter_len + 1])
            .ok()?;
        delimiter_len += 1;
        if delimiter[delimiter_len - 1] & 0x80 == 0 {
            break;
        }
        if delimiter_len == delimiter.len() {
            return None;
        }
    }

    let envelope_len = prost::decode_length_delimiter(&delimiter[..delimiter_len]).ok()?;
    let mut encoded_envelope = Vec::new();
    reader
        .take(u64::try_from(envelope_len).ok()?)
        .read_to_end(&mut encoded_envelope)
        .ok()?;
    if encoded_envelope.len() != envelope_len {
        return None;
    }

    let envelope = CachedSnapshotEnvelope::decode(bytes::Bytes::from(encoded_envelope)).ok()?;
    if pb::SpecsEnvelopeKind::try_from(envelope.kind).ok()? != pb::SpecsEnvelopeKind::TopLevel {
        return None;
    }

    let cursor = CachedSnapshotCursor::decode(envelope.data?).ok()?;
    (cursor.lcut > 0).then_some(cursor)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    fn compressed_cache(time: u64, compression: ProtoCompression) -> CachedSpecs {
        compressed_cache_with_cursor(time, &format!("checksum-{time}"), compression)
    }

    fn compressed_cache_with_cursor(
        lcut: u64,
        checksum: &str,
        compression: ProtoCompression,
    ) -> CachedSpecs {
        compressed_cache_with_rest(lcut, checksum, compression, Vec::new())
    }

    fn compressed_cache_with_rest(
        lcut: u64,
        checksum: &str,
        compression: ProtoCompression,
        rest: Vec<u8>,
    ) -> CachedSpecs {
        let top_level = pb::SpecsTopLevel {
            time: lcut,
            checksum: checksum.to_string(),
            rest,
            ..Default::default()
        };
        let envelope = pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::TopLevel as i32,
            data: Some(top_level.encode_to_vec()),
            ..Default::default()
        }
        .encode_length_delimited_to_vec();
        let bytes = match compression {
            ProtoCompression::Brotli => {
                let mut writer = brotli::CompressorWriter::new(Vec::new(), BUFFER_SIZE, 5, 22);
                writer.write_all(&envelope).unwrap();
                writer.into_inner()
            }
            ProtoCompression::Zstd => zstd::stream::encode_all(envelope.as_slice(), 3).unwrap(),
        };

        CachedSpecs {
            result: Some(bytes),
            proto_compression: Some(compression),
            time: Some(lcut),
            checksum: Some(checksum.to_string()),
            has_updates: None,
        }
    }

    #[test]
    fn newest_compressed_cache_wins_across_encodings() {
        let selected = select_newest_compressed_cache(
            vec![
                compressed_cache(1, ProtoCompression::Zstd),
                compressed_cache(2, ProtoCompression::Brotli),
            ],
            None,
            None,
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
    }

    #[test]
    fn zstd_wins_when_compressed_cache_times_match() {
        let selected = select_newest_compressed_cache(
            vec![
                compressed_cache(2, ProtoCompression::Brotli),
                compressed_cache(2, ProtoCompression::Zstd),
            ],
            None,
            None,
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Zstd));
    }

    #[test]
    fn update_wins_over_zstd_no_update_when_cache_times_match() {
        let mut zstd_no_update = compressed_cache(2, ProtoCompression::Zstd);
        zstd_no_update.has_updates = Some(false);

        let selected = select_newest_compressed_cache(
            vec![
                compressed_cache(2, ProtoCompression::Brotli),
                zstd_no_update,
            ],
            Some(1),
            Some("checksum-1"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
    }

    #[test]
    fn update_wins_over_zstd_no_update_when_cache_times_are_missing() {
        let mut brotli_update = compressed_cache(1, ProtoCompression::Brotli);
        brotli_update.time = None;
        let mut zstd_no_update = compressed_cache(1, ProtoCompression::Zstd);
        zstd_no_update.time = None;
        zstd_no_update.has_updates = Some(false);

        let selected =
            select_newest_compressed_cache(vec![brotli_update, zstd_no_update], Some(0), None)
                .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
    }

    #[test]
    fn snapshot_lcut_wins_over_datastore_write_time() {
        let mut newer_zstd = compressed_cache(200, ProtoCompression::Zstd);
        newer_zstd.time = Some(1000);
        let mut older_brotli = compressed_cache(100, ProtoCompression::Brotli);
        older_brotli.time = Some(2000);

        let selected =
            select_newest_compressed_cache(vec![newer_zstd, older_brotli], None, None).unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Zstd));
    }

    #[test]
    fn snapshot_lcut_wins_when_datastore_times_are_missing() {
        let mut older_zstd = compressed_cache(100, ProtoCompression::Zstd);
        older_zstd.time = None;
        let mut newer_brotli = compressed_cache(200, ProtoCompression::Brotli);
        newer_brotli.time = None;

        let selected =
            select_newest_compressed_cache(vec![older_zstd, newer_brotli], None, None).unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
    }

    #[test]
    fn changed_checksum_wins_when_snapshot_lcuts_match() {
        let current_zstd = compressed_cache_with_cursor(100, "current", ProtoCompression::Zstd);
        let mut changed_brotli =
            compressed_cache_with_cursor(100, "updated", ProtoCompression::Brotli);
        changed_brotli.time = Some(101);

        let selected = select_newest_compressed_cache(
            vec![current_zstd, changed_brotli],
            Some(100),
            Some("current"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
    }

    #[test]
    fn newer_checksum_wins_over_zstd_preference_on_initialization() {
        let mut older_zstd = compressed_cache_with_cursor(100, "old", ProtoCompression::Zstd);
        older_zstd.time = Some(1000);
        let mut newer_brotli = compressed_cache_with_cursor(100, "new", ProtoCompression::Brotli);
        newer_brotli.time = Some(2000);

        let selected =
            select_newest_compressed_cache(vec![older_zstd, newer_brotli], None, None).unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
    }

    #[test]
    fn newer_checksum_wins_when_both_differ_from_current_checksum() {
        let mut older_zstd = compressed_cache_with_cursor(100, "old", ProtoCompression::Zstd);
        older_zstd.time = Some(1000);
        let mut newer_brotli = compressed_cache_with_cursor(100, "new", ProtoCompression::Brotli);
        newer_brotli.time = Some(2000);

        let selected = select_newest_compressed_cache(
            vec![older_zstd, newer_brotli],
            Some(100),
            Some("current"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
    }

    #[test]
    fn current_snapshot_wins_over_older_same_lcut_checksum() {
        let mut stale_zstd = compressed_cache_with_cursor(100, "old", ProtoCompression::Zstd);
        stale_zstd.time = Some(1000);
        let mut current_brotli =
            compressed_cache_with_cursor(100, "current", ProtoCompression::Brotli);
        current_brotli.time = Some(2000);

        let selected = select_newest_compressed_cache(
            vec![stale_zstd, current_brotli],
            Some(100),
            Some("current"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
    }

    #[test]
    fn current_snapshot_wins_when_same_lcut_write_times_match() {
        let current_brotli = compressed_cache_with_cursor(100, "current", ProtoCompression::Brotli);
        let different_zstd = compressed_cache_with_cursor(100, "different", ProtoCompression::Zstd);

        let selected = select_newest_compressed_cache(
            vec![different_zstd, current_brotli],
            Some(100),
            Some("current"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
    }

    #[test]
    fn current_snapshot_wins_when_same_lcut_write_times_are_missing() {
        let mut current_brotli =
            compressed_cache_with_cursor(100, "current", ProtoCompression::Brotli);
        current_brotli.time = None;
        let mut different_zstd =
            compressed_cache_with_cursor(100, "different", ProtoCompression::Zstd);
        different_zstd.time = None;

        let selected = select_newest_compressed_cache(
            vec![different_zstd, current_brotli],
            Some(100),
            Some("current"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
    }

    #[test]
    fn higher_lcut_prefers_new_checksum_when_write_times_are_missing() {
        let mut duplicate_zstd =
            compressed_cache_with_cursor(200, "current", ProtoCompression::Zstd);
        duplicate_zstd.time = None;
        let mut changed_brotli =
            compressed_cache_with_cursor(200, "updated", ProtoCompression::Brotli);
        changed_brotli.time = None;

        let selected = select_newest_compressed_cache(
            vec![duplicate_zstd, changed_brotli],
            Some(100),
            Some("current"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
    }

    #[test]
    fn newer_no_update_wins_over_stale_same_lcut_checksum() {
        let mut stale_zstd = compressed_cache_with_cursor(100, "old", ProtoCompression::Zstd);
        stale_zstd.time = Some(1000);
        let mut current_brotli =
            compressed_cache_with_cursor(100, "current", ProtoCompression::Brotli);
        current_brotli.time = Some(2000);
        current_brotli.has_updates = Some(false);

        let selected = select_newest_compressed_cache(
            vec![stale_zstd, current_brotli],
            Some(100),
            Some("current"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
        assert_eq!(selected.has_updates, Some(false));
    }

    #[test]
    fn newer_same_lcut_checksum_wins_over_older_no_update() {
        let mut newer_zstd = compressed_cache_with_cursor(100, "new", ProtoCompression::Zstd);
        newer_zstd.time = Some(2000);
        let mut current_brotli =
            compressed_cache_with_cursor(100, "current", ProtoCompression::Brotli);
        current_brotli.time = Some(1000);
        current_brotli.has_updates = Some(false);

        let selected = select_newest_compressed_cache(
            vec![newer_zstd, current_brotli],
            Some(100),
            Some("current"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Zstd));
    }

    #[test]
    fn no_update_wins_when_same_lcut_write_times_are_missing() {
        let mut different_zstd =
            compressed_cache_with_cursor(100, "different", ProtoCompression::Zstd);
        different_zstd.time = None;
        let mut current_brotli =
            compressed_cache_with_cursor(100, "current", ProtoCompression::Brotli);
        current_brotli.time = None;
        current_brotli.checksum = None;
        current_brotli.has_updates = Some(false);

        let selected = select_newest_compressed_cache(
            vec![different_zstd, current_brotli],
            Some(100),
            Some("current"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
        assert_eq!(selected.has_updates, Some(false));
    }

    #[test]
    fn current_snapshot_wins_when_only_one_same_lcut_write_time_is_missing() {
        for (update_time, no_update_time) in [(None, Some(200)), (Some(200), None)] {
            let mut different_zstd =
                compressed_cache_with_cursor(100, "different", ProtoCompression::Zstd);
            different_zstd.time = update_time;
            let mut current_brotli =
                compressed_cache_with_cursor(100, "current", ProtoCompression::Brotli);
            current_brotli.time = no_update_time;
            current_brotli.has_updates = Some(false);

            let selected = select_newest_compressed_cache(
                vec![different_zstd, current_brotli],
                Some(100),
                Some("current"),
            )
            .unwrap();

            assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
            assert_eq!(selected.has_updates, Some(false));
        }
    }

    #[test]
    fn same_lcut_codec_siblings_do_not_oscillate_without_write_times() {
        for (current_compression, sibling_compression) in [
            (ProtoCompression::Brotli, ProtoCompression::Zstd),
            (ProtoCompression::Zstd, ProtoCompression::Brotli),
        ] {
            let mut current = compressed_cache_with_cursor(100, "current", current_compression);
            current.time = None;
            current.has_updates = Some(false);

            let mut sibling = compressed_cache_with_cursor(100, "different", sibling_compression);
            sibling.time = None;

            let selected =
                select_newest_compressed_cache(vec![sibling, current], Some(100), Some("current"))
                    .unwrap();

            assert_eq!(selected.proto_compression, Some(current_compression));
            assert_eq!(selected.has_updates, Some(false));
        }
    }

    #[test]
    fn mismatched_no_update_does_not_suppress_same_lcut_update() {
        let mut changed_zstd = compressed_cache_with_cursor(100, "updated", ProtoCompression::Zstd);
        changed_zstd.time = None;
        let mut unrelated_brotli =
            compressed_cache_with_cursor(100, "unrelated", ProtoCompression::Brotli);
        unrelated_brotli.time = None;
        unrelated_brotli.has_updates = Some(false);

        let selected = select_newest_compressed_cache(
            vec![changed_zstd, unrelated_brotli],
            Some(100),
            Some("current"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Zstd));
    }

    #[test]
    fn no_update_wins_over_higher_lcut_duplicate_checksum() {
        let duplicate_zstd = compressed_cache_with_cursor(200, "current", ProtoCompression::Zstd);
        let mut current_brotli =
            compressed_cache_with_cursor(100, "current", ProtoCompression::Brotli);
        current_brotli.has_updates = Some(false);

        let selected = select_newest_compressed_cache(
            vec![duplicate_zstd, current_brotli],
            Some(100),
            Some("current"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
        assert_eq!(selected.has_updates, Some(false));
    }

    #[test]
    fn no_update_wins_over_stale_brotli_snapshot() {
        let mut current_zstd = compressed_cache(200, ProtoCompression::Zstd);
        current_zstd.has_updates = Some(false);
        current_zstd.result = Some(br#"{"has_updates":false}"#.to_vec());
        let stale_brotli = compressed_cache(100, ProtoCompression::Brotli);

        let selected = select_newest_compressed_cache(
            vec![current_zstd, stale_brotli],
            Some(200),
            Some("checksum-200"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Zstd));
        assert_eq!(selected.has_updates, Some(false));
    }

    #[test]
    fn no_update_cannot_initialize_an_empty_store() {
        let mut no_update = compressed_cache(100, ProtoCompression::Zstd);
        no_update.has_updates = Some(false);

        assert!(select_newest_compressed_cache(vec![no_update], None, None).is_none());
    }

    #[test]
    fn valid_snapshot_wins_over_corrupt_sibling() {
        let mut corrupt_zstd = compressed_cache(200, ProtoCompression::Zstd);
        corrupt_zstd.result = Some(vec![1, 2, 3]);
        let valid_brotli = compressed_cache(100, ProtoCompression::Brotli);

        let selected =
            select_newest_compressed_cache(vec![corrupt_zstd, valid_brotli], None, None).unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Brotli));
    }

    #[test]
    fn no_update_wins_over_corrupt_snapshot() {
        let mut corrupt_brotli = compressed_cache(200, ProtoCompression::Brotli);
        corrupt_brotli.result = Some(vec![1, 2, 3]);
        let mut current_zstd = compressed_cache(100, ProtoCompression::Zstd);
        current_zstd.has_updates = Some(false);

        let selected = select_newest_compressed_cache(
            vec![corrupt_brotli, current_zstd],
            Some(100),
            Some("checksum-100"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Zstd));
        assert_eq!(selected.has_updates, Some(false));
    }

    #[test]
    fn large_top_level_snapshots_are_not_rejected() {
        let large_top_level = vec![0; 8 * 1024 * 1024 + 1];
        let newer_zstd =
            compressed_cache_with_rest(200, "new", ProtoCompression::Zstd, large_top_level.clone());
        let mut current_brotli =
            compressed_cache_with_cursor(100, "current", ProtoCompression::Brotli);
        current_brotli.has_updates = Some(false);

        let selected = select_newest_compressed_cache(
            vec![newer_zstd, current_brotli],
            Some(100),
            Some("current"),
        )
        .unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Zstd));

        let newer_zstd =
            compressed_cache_with_rest(200, "new", ProtoCompression::Zstd, large_top_level);
        let older_brotli = compressed_cache(100, ProtoCompression::Brotli);
        let selected =
            select_newest_compressed_cache(vec![newer_zstd, older_brotli], None, None).unwrap();

        assert_eq!(selected.proto_compression, Some(ProtoCompression::Zstd));
    }

    #[test]
    fn truncated_snapshot_cursor_is_rejected() {
        let mut envelope = Vec::new();
        prost::encode_length_delimiter(1024, &mut envelope).unwrap();
        envelope.extend_from_slice(&[1, 2, 3]);

        assert!(decode_cached_snapshot_cursor(envelope.as_slice()).is_none());
    }
}
