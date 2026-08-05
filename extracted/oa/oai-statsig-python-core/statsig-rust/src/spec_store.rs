use arc_swap::ArcSwap;
use chrono::Utc;
use parking_lot::{Mutex, MutexGuard};
use std::collections::HashMap;
use std::sync::{Arc, OnceLock};
use std::time::Instant;

use crate::data_store_interface::{DataStoreCacheKeys, DataStoreTrait, RequestPath};
use crate::evaluation::evaluator::SpecType;
use crate::gcir::evaluation_plan::GcirEvaluationPlan;
use crate::global_configs::GlobalConfigs;
use crate::hashing::HashUtil;
use crate::id_lists_adapter::{IdList, IdListsUpdateListener};
use crate::interned_string::InternedString;
use crate::interned_values::interned_store::{InternedStore, MmapProjectId};
use crate::macros::LOCK_TIMEOUT;
use crate::networking::ResponseData;
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::observability::sdk_errors_observer::ErrorBoundaryEvent;
use crate::sdk_event_emitter::{SdkEvent, SdkEventEmitter};
use crate::specs_response::proto_specs::{ProtobufUpdate, deserialize_protobuf_for_store};
use crate::specs_response::spec_types::{SpecsResponseFull, SpecsResponseNoUpdates};
use crate::specs_response::specs_hash_map::{SpecDecodeStats, track_spec_decodes};
use crate::utils::{get_loggable_sdk_key, try_release_unused_heap_memory};
use crate::{
    SpecsFormat, SpecsInfo, SpecsSource, SpecsUpdate, SpecsUpdateListener, StatsigErr,
    StatsigOptions, StatsigRuntime, log_d, log_e, log_error_to_statsig_and_console, log_w,
};

#[derive(Clone)]
pub struct SpecStoreData {
    pub source: SpecsSource,
    pub source_api: Option<String>,
    pub time_received_at: Option<u64>,
    pub snapshot: Arc<SpecsResponseFull>,
    pub id_lists: Arc<HashMap<String, IdList>>,
    pub gcir_evaluation_plan: Arc<OnceLock<GcirEvaluationPlan>>,
    sync_cursor: ConfigSyncCursor,
    // Reused as the starting point for delta telemetry so unchanged maps can use native cloning.
    spec_decode_stats: SpecDecodeStats,
}

#[derive(Clone, Default)]
struct ConfigSyncCursor {
    lcut: u64,
    checksum: Option<String>,
}

impl SpecStoreData {
    pub(crate) fn gcir_evaluation_plan(&self, hashing: &HashUtil) -> &GcirEvaluationPlan {
        self.gcir_evaluation_plan
            .get_or_init(|| GcirEvaluationPlan::new(self.snapshot.as_ref(), hashing))
    }

    pub(crate) fn lcut(&self) -> u64 {
        self.sync_cursor.lcut
    }

    fn checksum(&self) -> Option<&str> {
        self.sync_cursor.checksum.as_deref()
    }
}

fn cursor_is_stale_or_duplicate(data: &SpecStoreData, lcut: u64, checksum: &str) -> bool {
    lcut < data.lcut() || (lcut == data.lcut() && data.checksum() == Some(checksum))
}

fn proto_response_lcut(data: &ResponseData) -> Option<u64> {
    data.get_header_ref("x-since-time")?.parse().ok()
}

fn proto_response_matches_cursor(data: &ResponseData, current: &SpecStoreData) -> bool {
    let Some(lcut) = proto_response_lcut(data) else {
        return false;
    };
    let Some(checksum) = data.get_header_ref("x-checksum") else {
        return false;
    };

    lcut == current.lcut() && current.checksum() == Some(checksum)
}

const TAG: &str = stringify!(SpecStore);
const RESPONSE_TYPE_TAG: &str = "response_type";
const DELTAS_USED_HEADER: &str = "x-deltas-used";

#[derive(Clone, Copy)]
enum ConfigResponseType {
    Delta,
    Full,
    NoUpdate,
}

impl ConfigResponseType {
    fn from_applied_response_data(data: &ResponseData) -> Self {
        if data.get_header_ref(DELTAS_USED_HEADER).is_some() {
            Self::Delta
        } else {
            Self::Full
        }
    }

    fn as_str(self) -> &'static str {
        match self {
            Self::Delta => "delta",
            Self::Full => "full",
            Self::NoUpdate => "no_update",
        }
    }
}

const CONFIG_PROTO_UPDATE_COUNT_METRIC: &str = "config_proto_update.count";
const CONFIG_PROTO_UPDATE_LATENCY_METRIC: &str = "config_proto_update.latency";
const CONFIG_PROTO_UPDATE_OUTCOME_TAG: &str = "outcome";
const CONFIG_PROTO_UPDATE_CURSOR_ONLY: &str = "cursor_only";
const CONFIG_PROTO_UPDATE_DUPLICATE: &str = "duplicate";
const CONFIG_PROTO_UPDATE_MATERIALIZED: &str = "materialized";
const INTERNED_MMAP_SPEC_DECODE_COUNT_METRIC: &str = "interned_mmap.spec_decode.count";

pub struct SpecStore {
    data: ArcSwap<SpecStoreData>,
    update_lock: Mutex<()>,

    data_store_keys: DataStoreCacheKeys,
    data_store: Option<Arc<dyn DataStoreTrait>>,
    statsig_runtime: Arc<StatsigRuntime>,
    ops_stats: Arc<OpsStatsForInstance>,
    global_configs: Arc<GlobalConfigs>,
    event_emitter: Arc<SdkEventEmitter>,
    loggable_sdk_key: String,
    mmap_project_id: MmapProjectId,
}

impl SpecStore {
    #[must_use]
    pub fn new(
        sdk_key: &str,
        data_store_key: String,
        statsig_runtime: Arc<StatsigRuntime>,
        event_emitter: Arc<SdkEventEmitter>,
        options: Option<&StatsigOptions>,
    ) -> SpecStore {
        let mut data_store = None;
        if let Some(options) = options {
            data_store = options.data_store.clone();
        }

        let sdk_instance_id = options
            .map(|opts| opts.get_sdk_instance_id(sdk_key))
            .unwrap_or(sdk_key);

        SpecStore {
            data_store_keys: DataStoreCacheKeys::from_selected_key(&data_store_key),
            data: ArcSwap::from_pointee(SpecStoreData {
                snapshot: Arc::new(SpecsResponseFull::default()),
                time_received_at: None,
                source: SpecsSource::Uninitialized,
                source_api: None,
                id_lists: Arc::new(HashMap::new()),
                gcir_evaluation_plan: Arc::new(OnceLock::new()),
                sync_cursor: ConfigSyncCursor::default(),
                spec_decode_stats: SpecDecodeStats::default(),
            }),
            update_lock: Mutex::new(()),
            event_emitter,
            data_store,
            statsig_runtime,
            ops_stats: OPS_STATS.get_for_instance(sdk_instance_id),
            global_configs: GlobalConfigs::get_instance(sdk_instance_id),
            loggable_sdk_key: get_loggable_sdk_key(sdk_key),
            mmap_project_id: MmapProjectId::for_sdk_key(sdk_key),
        }
    }

    pub fn set_source(&self, source: SpecsSource) {
        {
            let Some(_update_guard) = self.try_lock_for_update("set_source") else {
                return;
            };

            let mut next_data = self.load_data().as_ref().clone();
            next_data.source = source.clone();
            self.publish_data(next_data);
        }

        log_d!(TAG, "Source Changed ({:?})", source);
    }

    pub fn get_current_values(&self) -> Option<SpecsResponseFull> {
        let data = self.load_data();
        let json = serde_json::to_string(data.snapshot.as_ref()).ok()?;
        let mut values = serde_json::from_str::<SpecsResponseFull>(&json).ok()?;
        values.time = data.lcut();
        values.checksum = data.sync_cursor.checksum.clone();
        Some(values)
    }

    #[cfg(feature = "testing")]
    pub fn get_spec_storage_counts_for_testing(&self) -> (usize, usize) {
        let data = self.load_data();
        (data.spec_decode_stats.total, data.spec_decode_stats.mmap)
    }

    pub fn get_fields_used_for_entity(
        &self,
        entity_name: &str,
        entity_type: SpecType,
    ) -> Vec<String> {
        let data = self.load_data();
        let entities = match entity_type {
            SpecType::Gate => &data.snapshot.feature_gates,
            SpecType::DynamicConfig | SpecType::Experiment => &data.snapshot.dynamic_configs,
            SpecType::Layer => &data.snapshot.layer_configs,
            SpecType::ParameterStore => return vec![],
        };

        let entity_name = InternedString::from_str_ref(entity_name);
        let entity = entities.get(&entity_name);

        entity
            .map(|entity| entity.view().fields_used())
            .unwrap_or_default()
    }

    pub fn unperformant_keys_entity_filter(
        &self,
        top_level_key: &str,
        entity_type: &str,
    ) -> Vec<String> {
        let data = self.load_data();
        if top_level_key == "param_stores" {
            match &data.snapshot.param_stores {
                Some(param_stores) => {
                    return param_stores
                        .keys()
                        .map(|k| k.unperformant_to_string())
                        .collect();
                }
                None => return vec![],
            }
        }

        let values = match top_level_key {
            "feature_gates" => &data.snapshot.feature_gates,
            "dynamic_configs" => &data.snapshot.dynamic_configs,
            "layer_configs" => &data.snapshot.layer_configs,
            _ => {
                log_e!(TAG, "Invalid top level key: {}", top_level_key);
                return vec![];
            }
        };

        if entity_type == "*" {
            return values.keys().map(|k| k.unperformant_to_string()).collect();
        }

        values
            .iter()
            .filter(|(_, v)| v.view().entity().as_str() == entity_type)
            .map(|(k, _)| k.unperformant_to_string())
            .collect()
    }

    pub fn set_values(&self, mut specs_update: SpecsUpdate) -> Result<(), StatsigErr> {
        let update_started_at = Instant::now();
        // Updating the spec store is a three step process:
        // 1. Prep (serialized writer path). Deserialize and compare to the current snapshot.
        // 2. Apply (serialized writer path). Publish a new immutable snapshot.
        // 3. Notify (no writer lock). Emit SDK events and update the data store.
        let locked_result = {
            let Some(_update_guard) = self.try_lock_for_update("set_values") else {
                return Err(StatsigErr::LockFailure(
                    "Failed to acquire spec store update lock for set_values".to_string(),
                ));
            };

            let prep_result = self.specs_update_prep(&mut specs_update)?;

            match prep_result {
                PrepResult::HasUpdates {
                    values,
                    response_format,
                    is_delta,
                    spec_decode_stats,
                } => {
                    let apply_result =
                        self.specs_update_apply(values, &specs_update, spec_decode_stats)?;
                    Ok(LockedSetValuesResult::Applied(
                        response_format,
                        apply_result,
                        ConfigResponseType::from_applied_response_data(&specs_update.data),
                        is_delta,
                    ))
                }
                PrepResult::CursorOnly { lcut, checksum } => {
                    self.specs_cursor_update_apply(lcut, checksum, &specs_update);
                    Ok(LockedSetValuesResult::NoSemanticUpdate(
                        specs_update.source.clone(),
                        specs_update.source_api.clone(),
                        ConfigResponseType::Delta,
                    ))
                }
                PrepResult::CurrentValuesNewer => Ok(LockedSetValuesResult::CurrentValuesNewer),
                PrepResult::Duplicate => Ok(LockedSetValuesResult::Duplicate),
                PrepResult::NoUpdates => Ok(LockedSetValuesResult::NoSemanticUpdate(
                    specs_update.source.clone(),
                    specs_update.source_api.clone(),
                    ConfigResponseType::NoUpdate,
                )),
            }
        }
        .map_err(|e: StatsigErr| {
            log_error_to_statsig_and_console!(self.ops_stats, TAG, e);
            e
        })?;

        let (response_format, apply_result, response_type, is_delta) = match locked_result {
            LockedSetValuesResult::Applied(
                response_format,
                apply_result,
                response_type,
                is_delta,
            ) => {
                if is_delta {
                    self.ops_stats_log_proto_update(CONFIG_PROTO_UPDATE_MATERIALIZED);
                }
                (response_format, apply_result, response_type, is_delta)
            }
            LockedSetValuesResult::NoSemanticUpdate(source, source_api, response_type) => {
                if matches!(response_type, ConfigResponseType::Delta) {
                    self.ops_stats_log_proto_update(CONFIG_PROTO_UPDATE_CURSOR_ONLY);
                    self.ops_stats_log_proto_update_latency(
                        CONFIG_PROTO_UPDATE_CURSOR_ONLY,
                        update_started_at.elapsed().as_secs_f64() * 1000.0,
                    );
                }
                self.ops_stats_log_no_update(source, source_api, response_type);
                return Ok(());
            }
            LockedSetValuesResult::CurrentValuesNewer => return Ok(()),
            LockedSetValuesResult::Duplicate => {
                self.ops_stats_log_proto_update(CONFIG_PROTO_UPDATE_DUPLICATE);
                return Ok(());
            }
        };

        self.ops_stats_log_interned_mmap_spec_decode(apply_result.spec_decode_stats);

        try_release_unused_heap_memory();

        // --- Notify ---

        let notify_result = self
            .specs_update_notify(response_format, response_type, specs_update, apply_result)
            .map_err(|e| {
                log_error_to_statsig_and_console!(self.ops_stats, TAG, e);
                e
            });

        if is_delta {
            self.ops_stats_log_proto_update_latency(
                CONFIG_PROTO_UPDATE_MATERIALIZED,
                update_started_at.elapsed().as_secs_f64() * 1000.0,
            );
        }

        notify_result
    }
}

// -------------------------------------------------------------------------------------------- [ Private ]

enum PrepResult {
    HasUpdates {
        values: Box<SpecsResponseFull>,
        response_format: SpecsFormat,
        is_delta: bool,
        spec_decode_stats: SpecDecodeStats,
    },
    CursorOnly {
        lcut: u64,
        checksum: String,
    },
    Duplicate,
    NoUpdates,
    CurrentValuesNewer,
}

enum LockedSetValuesResult {
    Applied(SpecsFormat, ApplyResult, ConfigResponseType, bool),
    NoSemanticUpdate(SpecsSource, Option<String>, ConfigResponseType),
    Duplicate,
    CurrentValuesNewer,
}

enum DeserializedSpecs {
    Materialized {
        values: Box<SpecsResponseFull>,
        is_delta: bool,
    },
    CursorOnly {
        lcut: u64,
        checksum: String,
    },
}

struct ApplyResult {
    prev_source: SpecsSource,
    prev_lcut: u64,
    prev_checksum: Option<String>,
    time_received_at: u64,
    notification: SpecUpdateNotification,
    spec_decode_stats: SpecDecodeStats,
}

struct SpecUpdateNotification {
    source: SpecsSource,
    source_api: Option<String>,
    values: Arc<SpecsResponseFull>,
    lcut: u64,
    checksum: Option<String>,
}

impl SpecStore {
    pub(crate) fn load_data(&self) -> Arc<SpecStoreData> {
        self.data.load_full()
    }

    fn publish_data(&self, data: SpecStoreData) {
        self.data.store(Arc::new(data));
    }

    fn try_lock_for_update(&self, operation: &str) -> Option<MutexGuard<'_, ()>> {
        match self.update_lock.try_lock_for(LOCK_TIMEOUT) {
            Some(guard) => Some(guard),
            None => {
                log_e!(
                    TAG,
                    "Failed to acquire spec store update lock for {}",
                    operation
                );
                None
            }
        }
    }

    fn specs_update_prep(&self, specs_update: &mut SpecsUpdate) -> Result<PrepResult, StatsigErr> {
        if specs_update.has_updates == Some(false) {
            return Ok(PrepResult::NoUpdates);
        }

        let response_format = self.get_spec_response_format(specs_update);
        let read_data = self.load_data();
        if matches!(response_format, SpecsFormat::Protobuf)
            && proto_response_lcut(&specs_update.data).is_some_and(|lcut| lcut < read_data.lcut())
        {
            return Ok(PrepResult::CurrentValuesNewer);
        }
        if matches!(response_format, SpecsFormat::Protobuf)
            && proto_response_matches_cursor(&specs_update.data, &read_data)
        {
            return Ok(PrepResult::Duplicate);
        }
        // First, try a full or delta specs response deserialization
        let first_deserialize_result =
            self.deserialize_specs_data(&read_data, &response_format, &mut specs_update.data);

        let first_deserialize_error = match first_deserialize_result {
            Ok((
                DeserializedSpecs::Materialized {
                    values: next_values,
                    is_delta,
                },
                spec_decode_stats,
            )) => {
                if self.are_current_values_newer(&read_data, &next_values) {
                    return Ok(PrepResult::CurrentValuesNewer);
                }

                if next_values.has_updates {
                    return Ok(PrepResult::HasUpdates {
                        values: next_values,
                        response_format,
                        is_delta,
                        spec_decode_stats,
                    });
                }

                None
            }
            Ok((DeserializedSpecs::CursorOnly { lcut, checksum }, _)) => {
                if cursor_is_stale_or_duplicate(&read_data, lcut, &checksum) {
                    return Ok(PrepResult::CurrentValuesNewer);
                }

                return Ok(PrepResult::CursorOnly { lcut, checksum });
            }
            Err(e) => Some(e),
        };

        // Second, try a No Updates deserialization
        let second_deserialize_result = specs_update
            .data
            .deserialize_into::<SpecsResponseNoUpdates>();

        let second_deserialize_error = match second_deserialize_result {
            Ok(result) => {
                if !result.has_updates {
                    return Ok(PrepResult::NoUpdates);
                }

                None
            }
            Err(e) => Some(e),
        };

        let error = first_deserialize_error
            .or(second_deserialize_error)
            .unwrap_or_else(|| {
                StatsigErr::JsonParseError("SpecsResponse".to_string(), "Unknown error".to_string())
            });

        Err(error)
    }

    fn specs_update_apply(
        &self,
        next_values: Box<SpecsResponseFull>,
        specs_update: &SpecsUpdate,
        spec_decode_stats: SpecDecodeStats,
    ) -> Result<ApplyResult, StatsigErr> {
        // DANGER: try_update_global_configs contains its own locks
        self.try_update_global_configs(&next_values);

        let data = self.load_data();
        let prev_source = data.source.clone();
        let prev_lcut = data.lcut();
        let prev_checksum = data.checksum().map(str::to_string);
        let time_received_at = Utc::now().timestamp_millis() as u64;
        let values: Arc<SpecsResponseFull> = Arc::from(next_values);
        let sync_cursor = ConfigSyncCursor {
            lcut: values.time,
            checksum: values.checksum.clone(),
        };
        let notification = SpecUpdateNotification {
            source: specs_update.source.clone(),
            source_api: specs_update.source_api.clone(),
            lcut: values.time,
            checksum: values
                .checksum
                .as_ref()
                .map(|value| value.as_str().to_string()),
            values: values.clone(),
        };

        self.publish_data(SpecStoreData {
            source: specs_update.source.clone(),
            source_api: specs_update.source_api.clone(),
            time_received_at: Some(time_received_at),
            snapshot: values,
            id_lists: data.id_lists.clone(),
            gcir_evaluation_plan: Arc::new(OnceLock::new()),
            sync_cursor,
            spec_decode_stats,
        });

        Ok(ApplyResult {
            prev_source,
            prev_lcut,
            prev_checksum,
            time_received_at,
            notification,
            spec_decode_stats,
        })
    }

    fn specs_cursor_update_apply(&self, lcut: u64, checksum: String, specs_update: &SpecsUpdate) {
        let data = self.load_data();
        let mut next_data = data.as_ref().clone();
        next_data.source = specs_update.source.clone();
        next_data.source_api = specs_update.source_api.clone();
        next_data.time_received_at = Some(Utc::now().timestamp_millis() as u64);
        next_data.sync_cursor = ConfigSyncCursor {
            lcut,
            checksum: Some(checksum),
        };
        self.publish_data(next_data);
    }

    fn specs_update_notify(
        &self,
        response_format: SpecsFormat,
        response_type: ConfigResponseType,
        specs_update: SpecsUpdate,
        apply_result: ApplyResult,
    ) -> Result<(), StatsigErr> {
        let SpecsUpdate { data, .. } = specs_update;
        let ApplyResult {
            prev_source,
            prev_lcut,
            prev_checksum,
            time_received_at,
            notification,
            spec_decode_stats: _,
        } = apply_result;
        let SpecUpdateNotification {
            source,
            source_api,
            values,
            lcut,
            checksum,
        } = notification;

        self.emit_specs_updated_sdk_event(&source, &source_api, values.as_ref());
        if let Some(sdk_configs) = &values.sdk_configs {
            self.emit_internal_sdk_configs_updated_sdk_event(sdk_configs);
        }

        // Data store writes now support both legacy JSON payloads and statsig-br protobuf bytes.
        self.try_update_data_store(
            &source,
            data,
            time_received_at,
            checksum.clone(),
            matches!(response_format, SpecsFormat::Protobuf),
        );

        self.ops_stats_log_config_propagation_diff(
            lcut,
            prev_lcut,
            checksum.as_deref(),
            prev_checksum.as_deref(),
            &source,
            &prev_source,
            source_api,
            response_format,
            response_type,
        );

        Ok(())
    }

    fn deserialize_specs_data(
        &self,
        current_data: &SpecStoreData,
        response_format: &SpecsFormat,
        response_data: &mut ResponseData,
    ) -> Result<(DeserializedSpecs, SpecDecodeStats), StatsigErr> {
        let (result, spec_decode_stats) = track_spec_decodes(|| {
            InternedStore::with_mmap_project(self.mmap_project_id, || {
                let mut next_values = Box::new(SpecsResponseFull::default());

                match response_format {
                    SpecsFormat::Protobuf => {
                        let update = deserialize_protobuf_for_store(
                            &self.ops_stats,
                            current_data.snapshot.as_ref(),
                            current_data.spec_decode_stats,
                            next_values.as_mut(),
                            response_data,
                        )?;
                        match update {
                            ProtobufUpdate::Materialized { is_delta } => {
                                Ok(DeserializedSpecs::Materialized {
                                    values: next_values,
                                    is_delta,
                                })
                            }
                            ProtobufUpdate::CursorOnly { lcut, checksum } => {
                                Ok(DeserializedSpecs::CursorOnly { lcut, checksum })
                            }
                        }
                    }
                    SpecsFormat::Json => {
                        response_data.deserialize_in_place(next_values.as_mut())?;
                        Ok(DeserializedSpecs::Materialized {
                            values: next_values,
                            is_delta: false,
                        })
                    }
                }
            })
        });

        Ok((result?, spec_decode_stats))
    }

    fn emit_specs_updated_sdk_event(
        &self,
        source: &SpecsSource,
        source_api: &Option<String>,
        values: &SpecsResponseFull,
    ) {
        self.event_emitter.emit(SdkEvent::SpecsUpdated {
            source,
            source_api,
            values,
        });
    }

    fn emit_internal_sdk_configs_updated_sdk_event(
        &self,
        sdk_configs: &HashMap<String, crate::DynamicValue>,
    ) {
        self.event_emitter
            .emit(SdkEvent::InternalSdkConfigsUpdated { sdk_configs });
    }

    fn get_spec_response_format(&self, update: &SpecsUpdate) -> SpecsFormat {
        let content_type = update.data.get_header_ref("content-type");
        if content_type.map(|s| s.as_str().contains("application/octet-stream")) != Some(true) {
            return SpecsFormat::Json;
        }

        let content_encoding = update.data.get_header_ref("content-encoding");
        if content_encoding.map(|s| s.as_str().contains("statsig-br")) != Some(true) {
            return SpecsFormat::Json;
        }

        SpecsFormat::Protobuf
    }

    fn try_update_global_configs(&self, dcs: &SpecsResponseFull) {
        if let Some(diagnostics) = &dcs.diagnostics {
            self.global_configs
                .set_diagnostics_sampling_rates(diagnostics.clone());
        }

        if let Some(sdk_configs) = &dcs.sdk_configs {
            self.global_configs.set_sdk_configs(sdk_configs.clone());
        }

        if let Some(sdk_flags) = &dcs.sdk_flags {
            self.global_configs.set_sdk_flags(sdk_flags.clone());
        }
    }

    fn try_update_data_store(
        &self,
        source: &SpecsSource,
        mut data: ResponseData,
        now: u64,
        checksum: Option<String>,
        is_protobuf: bool,
    ) {
        if source != &SpecsSource::Network {
            return;
        }

        if data.get_header_ref("x-deltas-used").is_some() {
            log_d!(
                TAG,
                "Skipping data store write for delta response identified by x-deltas-used header"
            );
            return;
        }

        let data_store = match &self.data_store {
            Some(data_store) => data_store.clone(),
            None => return,
        };

        let data_store_key = if is_protobuf {
            self.data_store_keys.statsig_br.clone()
        } else {
            self.data_store_keys.plain_text.clone()
        };

        let spawn_result = self.statsig_runtime.spawn(
            "spec_store_update_data_store",
            move |_shutdown_notif| async move {
                let data_bytes = match data.read_to_bytes() {
                    Ok(bytes) => bytes,
                    Err(e) => {
                        log_e!(TAG, "Failed to read data as bytes: {}", e);
                        return;
                    }
                };

                write_specs_to_data_store(
                    data_store,
                    data_store_key,
                    data_bytes,
                    checksum,
                    now,
                    is_protobuf,
                )
                .await;
            },
        );

        if let Err(e) = spawn_result {
            log_e!(
                TAG,
                "Failed to spawn spec store update data store task: {e}"
            );
        }
    }

    fn are_current_values_newer(
        &self,
        data: &SpecStoreData,
        next_values: &SpecsResponseFull,
    ) -> bool {
        let curr_checksum = data.checksum().unwrap_or_default();
        let new_checksum = next_values.checksum.as_deref().unwrap_or_default();

        let cached_time_is_newer = data.lcut() > 0 && data.lcut() > next_values.time;
        let checksums_match = !curr_checksum.is_empty() && curr_checksum == new_checksum;

        if cached_time_is_newer || checksums_match {
            log_d!(
                TAG,
                "Received values for [time: {}, checksum: {}], but currently has values for [time: {}, checksum: {}]. Ignoring values.",
                next_values.time,
                new_checksum,
                data.lcut(),
                curr_checksum,
            );
            return true;
        }

        false
    }
}

async fn write_specs_to_data_store(
    data_store: Arc<dyn DataStoreTrait>,
    data_store_key: String,
    data_bytes: Vec<u8>,
    checksum: Option<String>,
    now: u64,
    is_protobuf: bool,
) {
    match data_store
        .set_bytes(&data_store_key, &data_bytes, Some(now), checksum)
        .await
    {
        Ok(()) => return,
        Err(e @ StatsigErr::BytesNotImplemented) if is_protobuf => {
            if data_store
                .support_polling_updates_for(RequestPath::RulesetsV2)
                .await
            {
                log_w!(
                    TAG,
                    "Failed to write protobuf specs to data store as bytes. Protobuf specs cannot fall back to string writes: {}",
                    e
                );
            }
            return;
        }
        Err(e @ StatsigErr::BytesNotImplemented) => {
            log_w!(
                TAG,
                "Data store bytes write is not implemented. Falling back to string write: {}",
                e
            );
        }
        Err(e) => {
            log_w!(TAG, "Failed to write specs to data store as bytes: {}", e);
            return;
        }
    }

    let data_string = match String::from_utf8(data_bytes) {
        Ok(s) => s,
        Err(e) => {
            log_w!(
                TAG,
                "Skipping data store string write because payload is not valid UTF-8: {}",
                e
            );
            return;
        }
    };

    if let Err(e) = data_store
        .set(&data_store_key, &data_string, Some(now))
        .await
    {
        log_w!(TAG, "Failed to write specs to data store as string: {}", e);
    }
}

// -------------------------------------------------------------------------------------------- [ OpsStats Helpers ]

impl SpecStore {
    fn ops_stats_log_interned_mmap_spec_decode(&self, stats: SpecDecodeStats) {
        if stats.total == 0 {
            return;
        }

        let (source, reason) = if stats.mmap == stats.total {
            ("mmap", "preloaded")
        } else if stats.mmap > 0 {
            ("mixed", "partial_match")
        } else if InternedStore::has_preloaded_mmap_v2() {
            ("owned", "no_match")
        } else {
            ("owned", "spec_preload_unavailable")
        };

        self.ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Increment,
            INTERNED_MMAP_SPEC_DECODE_COUNT_METRIC.to_string(),
            1.0,
            Some(HashMap::from([
                ("source".to_string(), source.to_string()),
                ("reason".to_string(), reason.to_string()),
                ("sdk_key".to_string(), self.loggable_sdk_key.clone()),
            ])),
        ));
    }

    fn ops_stats_log_no_update(
        &self,
        source: SpecsSource,
        source_api: Option<String>,
        response_type: ConfigResponseType,
    ) {
        log_d!(TAG, "No Updates");
        self.ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Increment,
            "config_no_update".to_string(),
            1.0,
            Some(HashMap::from([
                ("source".to_string(), source.to_string()),
                ("source_api".to_string(), source_api.unwrap_or_default()),
                (
                    RESPONSE_TYPE_TAG.to_string(),
                    response_type.as_str().to_string(),
                ),
            ])),
        ));
    }

    fn ops_stats_log_proto_update(&self, outcome: &str) {
        self.ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Increment,
            CONFIG_PROTO_UPDATE_COUNT_METRIC.to_string(),
            1.0,
            Some(HashMap::from([(
                CONFIG_PROTO_UPDATE_OUTCOME_TAG.to_string(),
                outcome.to_string(),
            )])),
        ));
    }

    fn ops_stats_log_proto_update_latency(&self, outcome: &str, duration_ms: f64) {
        self.ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Dist,
            CONFIG_PROTO_UPDATE_LATENCY_METRIC.to_string(),
            duration_ms,
            Some(HashMap::from([(
                CONFIG_PROTO_UPDATE_OUTCOME_TAG.to_string(),
                outcome.to_string(),
            )])),
        ));
    }

    #[allow(clippy::too_many_arguments)]
    fn ops_stats_log_config_propagation_diff(
        &self,
        lcut: u64,
        prev_lcut: u64,
        checksum: Option<&str>,
        prev_checksum: Option<&str>,
        source: &SpecsSource,
        prev_source: &SpecsSource,
        source_api: Option<String>,
        response_format: SpecsFormat,
        response_type: ConfigResponseType,
    ) {
        log_d!(TAG, "Updated ({:?})", source);

        if *prev_source == SpecsSource::Uninitialized || *prev_source == SpecsSource::Loading {
            return;
        }

        let cursor_changed = lcut > prev_lcut || (lcut == prev_lcut && checksum != prev_checksum);
        if !cursor_changed {
            return;
        }

        let delay = (Utc::now().timestamp_millis() as u64).saturating_sub(lcut);

        self.ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Dist,
            "config_propagation_diff".to_string(),
            delay as f64,
            Some(HashMap::from([
                ("source".to_string(), source.to_string()),
                ("lcut".to_string(), lcut.to_string()),
                ("prev_lcut".to_string(), prev_lcut.to_string()),
                ("source_api".to_string(), source_api.unwrap_or_default()),
                ("sdk_key".to_string(), self.loggable_sdk_key.clone()),
                (
                    "response_format".to_string(),
                    Into::<&str>::into(&response_format).to_string(),
                ),
                (
                    RESPONSE_TYPE_TAG.to_string(),
                    response_type.as_str().to_string(),
                ),
            ])),
        ));
    }
}

// -------------------------------------------------------------------------------------------- [Impl SpecsUpdateListener]

impl SpecsUpdateListener for SpecStore {
    fn did_receive_specs_update(&self, update: SpecsUpdate) -> Result<(), StatsigErr> {
        self.set_values(update)
    }

    fn get_current_specs_info(&self) -> SpecsInfo {
        let data = self.load_data();
        SpecsInfo {
            lcut: Some(data.lcut()),
            checksum: data.sync_cursor.checksum.clone(),
            source: data.source.clone(),
            source_api: data.source_api.clone(),
        }
    }
}

// -------------------------------------------------------------------------------------------- [Impl IdListsUpdateListener]

impl IdListsUpdateListener for SpecStore {
    fn get_current_id_list_metadata(
        &self,
    ) -> HashMap<String, crate::id_lists_adapter::IdListMetadata> {
        let data = self.load_data();
        data.id_lists
            .iter()
            .map(|(key, list)| (key.clone(), list.metadata.clone()))
            .collect()
    }

    fn did_receive_id_list_updates(
        &self,
        updates: HashMap<String, crate::id_lists_adapter::IdListUpdate>,
    ) {
        let Some(_update_guard) = self.try_lock_for_update("did_receive_id_list_updates") else {
            return;
        };

        let data = self.load_data();
        let mut id_lists = data.id_lists.as_ref().clone();

        // delete any id_lists that are not in the updates
        id_lists.retain(|name, _| updates.contains_key(name));

        for (list_name, update) in updates {
            if let Some(entry) = id_lists.get_mut(&list_name) {
                // update existing
                entry.apply_update(update);
            } else {
                // add new
                let mut list = IdList::new(update.new_metadata.clone());
                list.apply_update(update);
                id_lists.insert(list_name, list);
            }
        }

        let mut next_data = data.as_ref().clone();
        next_data.id_lists = Arc::new(id_lists);
        self.publish_data(next_data);
    }
}

#[cfg(test)]
mod tests {
    use super::{
        ConfigResponseType, ConfigSyncCursor, DELTAS_USED_HEADER, SpecDecodeStats, SpecStoreData,
    };
    use crate::SpecsSource;
    use crate::hashing::HashUtil;
    use crate::networking::ResponseData;
    use crate::specs_response::spec_types::SpecsResponseFull;
    use std::collections::HashMap;
    use std::sync::{Arc, OnceLock};

    #[test]
    fn applied_response_type_uses_delta_header() {
        let delta_data = ResponseData::from_bytes_with_headers(
            Vec::new(),
            Some(HashMap::from([(
                DELTAS_USED_HEADER.to_string(),
                "true".to_string(),
            )])),
        );
        let full_data = ResponseData::from_bytes(Vec::new());

        assert_eq!(
            ConfigResponseType::from_applied_response_data(&delta_data).as_str(),
            "delta"
        );
        assert_eq!(
            ConfigResponseType::from_applied_response_data(&full_data).as_str(),
            "full"
        );
    }

    #[test]
    fn spec_store_data_reuses_gcir_evaluation_plan_cache_across_clones() {
        let data = SpecStoreData {
            source: SpecsSource::Network,
            source_api: Some("/v2/download_config_specs".to_string()),
            time_received_at: Some(1),
            snapshot: Arc::new(SpecsResponseFull::default()),
            id_lists: Arc::new(HashMap::new()),
            gcir_evaluation_plan: Arc::new(OnceLock::new()),
            sync_cursor: ConfigSyncCursor::default(),
            spec_decode_stats: SpecDecodeStats::default(),
        };
        let hashing = HashUtil::new();

        let first = data.gcir_evaluation_plan(&hashing);
        let cloned = data.clone();
        let second = cloned.gcir_evaluation_plan(&hashing);

        assert!(std::ptr::eq(first, second));
    }
}
