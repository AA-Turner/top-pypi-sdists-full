use arc_swap::ArcSwap;
use async_trait::async_trait;
use chrono::Utc;
use parking_lot::{Mutex, MutexGuard};
use std::collections::{BTreeMap, HashMap, HashSet};
use std::sync::{Arc, OnceLock};
use std::time::Instant;

use serde_json::Value;

use crate::data_store_interface::{DataStoreCacheKeys, DataStoreTrait, RequestPath};
use crate::evaluation::dynamic_string::DynamicString;
use crate::evaluation::evaluator::SpecType;
use crate::gcir::evaluation_plan::GcirEvaluationPlan;
use crate::global_configs::GlobalConfigs;
use crate::hashing::{self, HashUtil};
use crate::id_lists_adapter::{IdList, IdListsUpdateListener};
use crate::interned_string::InternedString;
use crate::interned_values::interned_store::{InternedStore, MmapProjectId};
use crate::macros::LOCK_TIMEOUT;
use crate::networking::ResponseData;
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::observability::sdk_errors_observer::ErrorBoundaryEvent;
use crate::sdk_event_emitter::{SdkEvent, SdkEventEmitter};
use crate::specs_adapter::remote_config_value_hydrator::RemoteConfigValueHydrator;
use crate::specs_response::parse_options::{SpecsResponseParseOptions, with_parse_options};
use crate::specs_response::proto_compression::{ProtoCompression, is_compressed_protobuf_response};
use crate::specs_response::proto_specs::{
    ProtobufHydrationContext, ProtobufUpdate, deserialize_protobuf_for_store_with_hydration,
    deserialize_protobuf_for_store_with_options,
};
use crate::specs_response::spec_types::{
    ConditionOperator, SpecsResponseFull, SpecsResponseNoUpdates,
};
use crate::specs_response::specs_hash_map::{SpecDecodeStats, track_spec_decodes};
use crate::statsig_options::SnapshotEvaluationSessionInitOptions;
use crate::utils::{get_loggable_sdk_key, try_release_unused_heap_memory};
use crate::{
    SpecsCursorUpdate, SpecsFormat, SpecsInfo, SpecsSource, SpecsUpdate, SpecsUpdateHydration,
    SpecsUpdateListener, StatsigErr, StatsigOptions, StatsigRuntime, log_d, log_e,
    log_error_to_statsig_and_console, log_w,
};

#[derive(Default)]
pub(crate) struct LiveOverlayTargetAppIndex {
    pub(crate) has_live_entities: bool,
    pub(crate) target_app_ids: HashSet<String>,
}

pub(crate) struct IdListLookupCondition {
    pub(crate) name: String,
    pub(crate) id_type: DynamicString,
}

#[derive(Clone)]
pub struct SpecStoreData {
    pub source: SpecsSource,
    pub source_api: Option<String>,
    pub time_received_at: Option<u64>,
    pub snapshot: Arc<SpecsResponseFull>,
    pub id_lists: Arc<HashMap<String, IdList>>,
    pub(crate) has_id_list_conditions: bool,
    pub(crate) id_list_lookup_conditions: Arc<OnceLock<Vec<IdListLookupCondition>>>,
    pub(crate) auto_capture_settings_value: Option<Arc<Value>>,
    pub(crate) auto_capture_settings_hash: u64,
    pub(crate) live_overlay_target_app_index: Arc<OnceLock<LiveOverlayTargetAppIndex>>,
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
    pub(crate) fn id_list_lookup_conditions(&self) -> &[IdListLookupCondition] {
        self.id_list_lookup_conditions
            .get_or_init(|| {
                self.snapshot
                    .condition_map
                    .values()
                    .filter_map(|condition| {
                        if !matches!(
                            condition.compiled_operator,
                            ConditionOperator::InSegmentList | ConditionOperator::NotInSegmentList
                        ) {
                            return None;
                        }

                        let name = condition
                            .target_value
                            .as_ref()?
                            .as_value_ref()
                            .string_value()?;
                        Some(IdListLookupCondition {
                            name: name.to_string(),
                            id_type: condition.id_type.clone(),
                        })
                    })
                    .collect()
            })
            .as_slice()
    }

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

fn same_parse_base(expected: &SpecStoreData, current: &SpecStoreData) -> bool {
    Arc::ptr_eq(&expected.snapshot, &current.snapshot)
        && expected.sync_cursor.lcut == current.sync_cursor.lcut
        && expected.sync_cursor.checksum == current.sync_cursor.checksum
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
    global_configs: Option<Arc<GlobalConfigs>>,
    event_emitter: Arc<SdkEventEmitter>,
    loggable_sdk_key: String,
    mmap_project_id: MmapProjectId,
    preserve_session_update_mode: bool,
    precompute_gcir_evaluation_plan: bool,
    prepare_snapshot_evaluation_data: bool,
    internal_observability_enabled: bool,
    release_unused_heap_memory_after_update: bool,
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
        Self::new_with_snapshot_evaluation_session_options(
            sdk_key,
            data_store_key,
            statsig_runtime,
            event_emitter,
            options,
            &SnapshotEvaluationSessionInitOptions::default(),
        )
    }

    pub(crate) fn new_with_snapshot_evaluation_session_options(
        sdk_key: &str,
        data_store_key: String,
        statsig_runtime: Arc<StatsigRuntime>,
        event_emitter: Arc<SdkEventEmitter>,
        options: Option<&StatsigOptions>,
        session_options: &SnapshotEvaluationSessionInitOptions,
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
                has_id_list_conditions: false,
                id_list_lookup_conditions: Arc::new(OnceLock::new()),
                auto_capture_settings_value: None,
                auto_capture_settings_hash: 0,
                live_overlay_target_app_index: Arc::new(OnceLock::new()),
                gcir_evaluation_plan: Arc::new(OnceLock::new()),
                sync_cursor: ConfigSyncCursor::default(),
                spec_decode_stats: SpecDecodeStats::default(),
            }),
            update_lock: Mutex::new(()),
            event_emitter,
            data_store,
            statsig_runtime,
            ops_stats: OPS_STATS.get_for_instance(sdk_instance_id),
            global_configs: (!session_options.config_only_mode)
                .then(|| GlobalConfigs::get_instance(sdk_instance_id)),
            loggable_sdk_key: get_loggable_sdk_key(sdk_key),
            mmap_project_id: MmapProjectId::for_sdk_key(
                session_options
                    .interned_mmap_sdk_key
                    .as_deref()
                    .unwrap_or(sdk_key),
            ),
            preserve_session_update_mode: session_options.preserve_dcs_session_update_mode
                || options
                    .and_then(|options| options.preserve_dcs_session_update_mode)
                    .unwrap_or(false),
            precompute_gcir_evaluation_plan: session_options.precompute_gcir_evaluation_plan,
            prepare_snapshot_evaluation_data: session_options.config_only_mode,
            internal_observability_enabled: !session_options.config_only_mode,
            release_unused_heap_memory_after_update: !session_options.config_only_mode,
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
            self.apply_prep_result(prep_result, &specs_update)
        }
        .map_err(|e: StatsigErr| {
            log_error_to_statsig_and_console!(self.ops_stats, TAG, e);
            e
        })?;

        self.finish_set_values(locked_result, specs_update, update_started_at)
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
    async fn set_values_with_protobuf_hydration(
        &self,
        mut specs_update: SpecsUpdate,
        hydrator: &RemoteConfigValueHydrator,
        source_url: &str,
    ) -> Result<(), StatsigErr> {
        let update_started_at = Instant::now();

        if specs_update.has_updates == Some(false) {
            return self.set_values(specs_update);
        }

        // Capture the immutable parse base before touching the compressed
        // response. Parsing and remote downloads happen without the writer
        // lock; publish is allowed only if this base is still current.
        let parse_base = self.load_data();
        if proto_response_lcut(&specs_update.data).is_some_and(|lcut| lcut < parse_base.lcut()) {
            return self.finish_set_values(
                LockedSetValuesResult::CurrentValuesNewer,
                specs_update,
                update_started_at,
            );
        }
        if proto_response_matches_cursor(&specs_update.data, &parse_base) {
            return self.finish_set_values(
                LockedSetValuesResult::Duplicate,
                specs_update,
                update_started_at,
            );
        }

        let mut next_values = Box::new(SpecsResponseFull::default());
        let capture_hydrated_data_store_bytes = self.data_store.is_some()
            && specs_update.source == SpecsSource::Network
            && specs_update.data.get_header_ref("x-deltas-used").is_none();
        let (protobuf_update, spec_decode_stats, hydrated_data_store_bytes) =
            match deserialize_protobuf_for_store_with_hydration(
                &self.ops_stats,
                parse_base.snapshot.as_ref(),
                parse_base.spec_decode_stats,
                next_values.as_mut(),
                &mut specs_update.data,
                ProtobufHydrationContext {
                    hydrator,
                    source_url,
                    mmap_project_id: self.mmap_project_id,
                    capture_hydrated_data_store_bytes,
                    preserve_session_update_mode: self.preserve_session_update_mode,
                },
            )
            .await
            {
                Ok(result) => result,
                Err(first_error) => {
                    // Preserve the legacy fallback for responses whose headers
                    // identify protobuf but whose body is the JSON no-update
                    // shape.
                    if specs_update
                        .data
                        .deserialize_into::<SpecsResponseNoUpdates>()
                        .is_ok_and(|result| !result.has_updates)
                    {
                        return self.finish_set_values(
                            LockedSetValuesResult::NoSemanticUpdate(
                                specs_update.source.clone(),
                                specs_update.source_api.clone(),
                                ConfigResponseType::NoUpdate,
                            ),
                            specs_update,
                            update_started_at,
                        );
                    }

                    log_error_to_statsig_and_console!(self.ops_stats, TAG, first_error);
                    return Err(first_error);
                }
            };

        if let Some(bytes) = hydrated_data_store_bytes {
            specs_update.data.set_data_store_protobuf_bytes(bytes);
        }

        let prep_result = match protobuf_update {
            ProtobufUpdate::Materialized { is_delta } => {
                if self.are_current_values_newer(&parse_base, &next_values) {
                    PrepResult::CurrentValuesNewer
                } else if next_values.has_updates {
                    PrepResult::HasUpdates {
                        values: next_values,
                        response_format: SpecsFormat::Protobuf,
                        is_delta,
                        spec_decode_stats,
                    }
                } else {
                    PrepResult::NoUpdates
                }
            }
            ProtobufUpdate::CursorOnly { lcut, checksum } => {
                if cursor_is_stale_or_duplicate(&parse_base, lcut, &checksum) {
                    PrepResult::CurrentValuesNewer
                } else {
                    PrepResult::CursorOnly { lcut, checksum }
                }
            }
        };

        let locked_result = {
            let Some(_update_guard) =
                self.try_lock_for_update("set_values_with_protobuf_hydration")
            else {
                return Err(StatsigErr::LockFailure(
                    "Failed to acquire spec store update lock for hydrated protobuf set_values"
                        .to_string(),
                ));
            };

            let current_data = self.load_data();
            if !same_parse_base(&parse_base, &current_data) {
                return Err(StatsigErr::LockFailure(
                    "Spec store base changed while hydrated protobuf update was parsing"
                        .to_string(),
                ));
            }

            self.apply_prep_result(prep_result, &specs_update)
        }
        .map_err(|error: StatsigErr| {
            log_error_to_statsig_and_console!(self.ops_stats, TAG, error);
            error
        })?;

        self.finish_set_values(locked_result, specs_update, update_started_at)
    }

    fn apply_prep_result(
        &self,
        prep_result: PrepResult,
        specs_update: &SpecsUpdate,
    ) -> Result<LockedSetValuesResult, StatsigErr> {
        match prep_result {
            PrepResult::HasUpdates {
                values,
                response_format,
                is_delta,
                spec_decode_stats,
            } => {
                Self::validate_scoped_expected_metadata(
                    specs_update,
                    values.checksum.as_deref(),
                    values.time,
                )?;
                let apply_result =
                    self.specs_update_apply(values, specs_update, is_delta, spec_decode_stats)?;
                Ok(LockedSetValuesResult::Applied(
                    response_format,
                    apply_result,
                    ConfigResponseType::from_applied_response_data(&specs_update.data),
                    is_delta,
                ))
            }
            PrepResult::CursorOnly { lcut, checksum } => {
                Self::validate_scoped_expected_metadata(
                    specs_update,
                    Some(checksum.as_str()),
                    lcut,
                )?;
                self.specs_cursor_update_apply(
                    lcut,
                    checksum,
                    specs_update.source.clone(),
                    specs_update.source_api.clone(),
                );
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

    fn validate_scoped_expected_metadata(
        specs_update: &SpecsUpdate,
        actual_checksum: Option<&str>,
        actual_lcut: u64,
    ) -> Result<(), StatsigErr> {
        let is_scoped_update = matches!(
            &specs_update.source,
            SpecsSource::Adapter(name) if name == "ScopedConfigSource"
        ) && specs_update.source_api.as_deref()
            == Some("ScopedConfigSource");

        if is_scoped_update
            && specs_update
                .data
                .scoped_expected_checksum()
                .is_some_and(|expected| actual_checksum != Some(expected))
        {
            return Err(StatsigErr::ChecksumFailure(
                "Scoped configuration payload checksum does not match its metadata".to_string(),
            ));
        }

        if is_scoped_update
            && specs_update
                .data
                .scoped_expected_lcut()
                .is_some_and(|expected| actual_lcut > expected)
        {
            return Err(StatsigErr::ChecksumFailure(
                "Scoped configuration payload LCUT is newer than its metadata".to_string(),
            ));
        }

        Ok(())
    }

    fn finish_set_values(
        &self,
        locked_result: LockedSetValuesResult,
        specs_update: SpecsUpdate,
        update_started_at: Instant,
    ) -> Result<(), StatsigErr> {
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

        if self.release_unused_heap_memory_after_update {
            try_release_unused_heap_memory();
        }

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

    pub(crate) fn load_data(&self) -> Arc<SpecStoreData> {
        self.data.load_full()
    }

    pub(crate) fn load_data_with_shared_id_lists(&self, source: &SpecStore) -> Arc<SpecStoreData> {
        let current = self.load_data();
        let shared = source.data.load();
        if Arc::ptr_eq(&current.id_lists, &shared.id_lists) {
            return current;
        }
        drop(shared);

        let Some(_update_guard) = self.update_lock.try_lock() else {
            let shared = source.data.load();
            if Arc::ptr_eq(&current.id_lists, &shared.id_lists) {
                return current;
            }
            let mut snapshot = current.as_ref().clone();
            snapshot.id_lists = Arc::clone(&shared.id_lists);
            return Arc::new(snapshot);
        };

        let current = self.load_data();
        let shared = source.data.load();
        if Arc::ptr_eq(&current.id_lists, &shared.id_lists) {
            return current;
        }

        let mut snapshot = current.as_ref().clone();
        snapshot.id_lists = Arc::clone(&shared.id_lists);
        let snapshot = Arc::new(snapshot);
        self.data.store(Arc::clone(&snapshot));
        snapshot
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
        is_delta: bool,
        spec_decode_stats: SpecDecodeStats,
    ) -> Result<ApplyResult, StatsigErr> {
        // DANGER: try_update_global_configs contains its own locks
        self.try_update_global_configs(&next_values, is_delta);

        let data = self.load_data();
        let prev_source = data.source.clone();
        let prev_lcut = data.lcut();
        let prev_checksum = data.checksum().map(str::to_string);
        let time_received_at = Utc::now().timestamp_millis() as u64;
        let values: Arc<SpecsResponseFull> = Arc::from(next_values);
        let has_id_list_conditions = self.prepare_snapshot_evaluation_data
            && values.condition_map.values().any(|condition| {
                matches!(
                    condition
                        .operator
                        .as_ref()
                        .map(|operator| operator.as_str()),
                    Some("in_segment_list" | "not_in_segment_list")
                )
            });
        let (auto_capture_settings_value, auto_capture_settings_hash) =
            if self.prepare_snapshot_evaluation_data {
                build_auto_capture_settings_projection(values.as_ref())
            } else {
                (None, 0)
            };
        let live_overlay_target_app_index = Arc::new(OnceLock::new());
        if self.prepare_snapshot_evaluation_data {
            live_overlay_target_app_index
                .get_or_init(|| build_live_overlay_target_app_index(values.as_ref()));
        }
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

        let gcir_evaluation_plan = Arc::new(OnceLock::new());
        if self.precompute_gcir_evaluation_plan {
            gcir_evaluation_plan
                .get_or_init(|| GcirEvaluationPlan::new(values.as_ref(), &HashUtil::new()));
        }

        self.publish_data(SpecStoreData {
            source: specs_update.source.clone(),
            source_api: specs_update.source_api.clone(),
            time_received_at: Some(time_received_at),
            snapshot: values,
            id_lists: data.id_lists.clone(),
            has_id_list_conditions,
            id_list_lookup_conditions: Arc::new(OnceLock::new()),
            auto_capture_settings_value,
            auto_capture_settings_hash,
            live_overlay_target_app_index,
            gcir_evaluation_plan,
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

    fn specs_cursor_update_apply(
        &self,
        lcut: u64,
        checksum: String,
        source: SpecsSource,
        source_api: Option<String>,
    ) {
        let data = self.load_data();
        let mut next_data = data.as_ref().clone();
        next_data.source = source;
        next_data.source_api = source_api;
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

        // Data store writes preserve the actual full-response compression in
        // codec-specific keys. Delta responses are never persisted.
        let proto_compression = ProtoCompression::from_response(&data);
        self.try_update_data_store(
            &source,
            data,
            time_received_at,
            checksum.clone(),
            proto_compression,
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
                        let update = deserialize_protobuf_for_store_with_options(
                            &self.ops_stats,
                            current_data.snapshot.as_ref(),
                            current_data.spec_decode_stats,
                            next_values.as_mut(),
                            response_data,
                            self.preserve_session_update_mode,
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
                        let parse_options = if self.preserve_session_update_mode {
                            SpecsResponseParseOptions::preserving_session_update_mode()
                        } else {
                            SpecsResponseParseOptions::default()
                        };
                        with_parse_options(parse_options, || {
                            response_data.deserialize_in_place(next_values.as_mut())
                        })?;
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
        if is_compressed_protobuf_response(&update.data) {
            SpecsFormat::Protobuf
        } else {
            SpecsFormat::Json
        }
    }

    fn try_update_global_configs(&self, dcs: &SpecsResponseFull, is_delta: bool) {
        let Some(global_configs) = self.global_configs.as_ref() else {
            return;
        };

        if let Some(diagnostics) = &dcs.diagnostics {
            global_configs.set_diagnostics_sampling_rates(diagnostics.clone());
        }

        if let Some(sdk_configs) = &dcs.sdk_configs {
            global_configs.set_sdk_configs(sdk_configs.clone());
        } else if !is_delta {
            // SDK configs are not normally deleted, but omission from a full
            // snapshot must still revoke any previously enabled rollout boost.
            global_configs.set_sdk_configs(HashMap::new());
        }

        if let Some(sdk_flags) = &dcs.sdk_flags {
            global_configs.set_sdk_flags(sdk_flags.clone());
        }
    }

    fn try_update_data_store(
        &self,
        source: &SpecsSource,
        mut data: ResponseData,
        now: u64,
        checksum: Option<String>,
        proto_compression: Option<ProtoCompression>,
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

        let data_store_key = match proto_compression {
            Some(ProtoCompression::Brotli) => self.data_store_keys.statsig_br.clone(),
            Some(ProtoCompression::Zstd) => self.data_store_keys.statsig_zstd.clone(),
            None => self.data_store_keys.plain_text.clone(),
        };
        let is_protobuf = proto_compression.is_some();

        let spawn_result = self.statsig_runtime.spawn(
            "spec_store_update_data_store",
            move |_shutdown_notif| async move {
                let data_bytes = if is_protobuf {
                    match data.take_data_store_protobuf_bytes() {
                        Some(bytes) => bytes,
                        None => match data.read_to_bytes() {
                            Ok(bytes) => bytes,
                            Err(e) => {
                                log_e!(TAG, "Failed to read data as bytes: {}", e);
                                return;
                            }
                        },
                    }
                } else {
                    match data.read_to_bytes() {
                        Ok(bytes) => bytes,
                        Err(e) => {
                            log_e!(TAG, "Failed to read data as bytes: {}", e);
                            return;
                        }
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

pub(crate) fn build_live_overlay_target_app_index(
    snapshot: &SpecsResponseFull,
) -> LiveOverlayTargetAppIndex {
    let mut index = LiveOverlayTargetAppIndex::default();

    for specs in [
        &snapshot.feature_gates,
        &snapshot.dynamic_configs,
        &snapshot.layer_configs,
    ] {
        for (_, spec) in specs.iter() {
            if spec.session_update_mode() != Some("live") {
                continue;
            }

            index.has_live_entities = true;
            if let Some(target_app_ids) = spec.view().target_app_ids() {
                index.target_app_ids.extend(
                    target_app_ids
                        .into_iter()
                        .map(|target_app_id| target_app_id.as_str().to_string()),
                );
            }
        }
    }

    index
}

fn build_auto_capture_settings_projection(
    snapshot: &SpecsResponseFull,
) -> (Option<Arc<Value>>, u64) {
    let Some(settings) = snapshot.auto_capture_settings.as_ref() else {
        return (None, 0);
    };

    let value = serde_json::to_value(settings).ok().map(Arc::new);
    let disabled_events: BTreeMap<&str, &bool> = settings
        .disabled_events
        .iter()
        .map(|(event, disabled)| (event.as_str(), disabled))
        .collect();
    let serialized = serde_json::to_string(&disabled_events).unwrap_or_default();

    (value, hashing::hash_one(serialized.as_bytes()))
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
        if !self.internal_observability_enabled || stats.total == 0 {
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
        if !self.internal_observability_enabled {
            return;
        }

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
        if !self.internal_observability_enabled {
            return;
        }

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
        if !self.internal_observability_enabled {
            return;
        }

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
        if !self.internal_observability_enabled {
            return;
        }

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

#[async_trait]
impl SpecsUpdateListener for SpecStore {
    fn did_receive_specs_update(&self, update: SpecsUpdate) -> Result<(), StatsigErr> {
        self.set_values(update)
    }

    async fn did_receive_specs_update_async(
        &self,
        mut update: SpecsUpdate,
        hydration: Option<SpecsUpdateHydration>,
    ) -> Result<(), StatsigErr> {
        let Some(hydration) = hydration else {
            return self.set_values(update);
        };

        if matches!(
            self.get_spec_response_format(&update),
            SpecsFormat::Protobuf
        ) {
            return self
                .set_values_with_protobuf_hydration(
                    update,
                    hydration.hydrator.as_ref(),
                    &hydration.source_url,
                )
                .await;
        }

        hydration
            .hydrator
            .hydrate_response(&mut update.data, &hydration.source_url)
            .await?;
        self.set_values(update)
    }

    fn did_advance_specs_cursor(&self, update: SpecsCursorUpdate) -> Result<(), StatsigErr> {
        let Some(_update_guard) = self.try_lock_for_update("did_advance_specs_cursor") else {
            return Err(StatsigErr::LockFailure(
                "Failed to acquire spec store update lock for cursor update".to_string(),
            ));
        };

        let data = self.load_data();
        if data.checksum() != Some(update.checksum.as_str()) || update.lcut <= data.lcut() {
            return Ok(());
        }

        self.specs_cursor_update_apply(
            update.lcut,
            update.checksum,
            update.source,
            update.source_api,
        );
        Ok(())
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
        ConfigResponseType, ConfigSyncCursor, DELTAS_USED_HEADER, SpecDecodeStats, SpecStore,
        SpecStoreData, build_live_overlay_target_app_index,
    };
    use crate::hashing::HashUtil;
    use crate::networking::ResponseData;
    use crate::sdk_event_emitter::SdkEventEmitter;
    use crate::snapshot_evaluation_session::SnapshotEvaluationSession;
    use crate::specs_response::spec_types::SpecsResponseFull;
    use crate::statsig_options::SnapshotEvaluationSessionInitOptions;
    use crate::statsig_runtime::StatsigRuntime;
    use crate::{SpecsSource, SpecsUpdate, StatsigErr};
    use std::collections::HashMap;
    use std::sync::{Arc, OnceLock};
    use std::time::{Duration, Instant};

    #[test]
    fn shared_id_list_snapshots_never_wait_for_config_updates() {
        let runtime = StatsigRuntime::get_runtime();
        let emitter = Arc::new(SdkEventEmitter::default());
        let owner = SpecStore::new(
            "secret-shared-owner",
            "shared-owner".to_string(),
            Arc::clone(&runtime),
            Arc::clone(&emitter),
            None,
        );
        let scoped = SpecStore::new(
            "client-shared-scope",
            "shared-scope".to_string(),
            runtime,
            emitter,
            None,
        );

        let update_guard = scoped.update_lock.lock();
        let started = Instant::now();
        let contended = scoped.load_data_with_shared_id_lists(&owner);
        assert!(started.elapsed() < Duration::from_secs(1));
        assert!(Arc::ptr_eq(
            &contended.id_lists,
            &owner.load_data().id_lists
        ));
        assert!(!Arc::ptr_eq(
            &contended.id_lists,
            &scoped.load_data().id_lists
        ));
        drop(update_guard);

        let published = scoped.load_data_with_shared_id_lists(&owner);
        assert!(Arc::ptr_eq(
            &published.id_lists,
            &owner.load_data().id_lists
        ));
        assert!(Arc::ptr_eq(&published, &scoped.load_data()));
        assert!(Arc::ptr_eq(
            &published,
            &scoped.load_data_with_shared_id_lists(&owner)
        ));
    }

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
    fn config_only_snapshots_skip_process_wide_heap_trimming() {
        let runtime = StatsigRuntime::get_runtime();
        let event_emitter = Arc::new(SdkEventEmitter::default());
        let standard = SpecStore::new(
            "standard-snapshot-trim",
            "standard".to_string(),
            runtime.clone(),
            event_emitter.clone(),
            None,
        );
        let config_only = SpecStore::new_with_snapshot_evaluation_session_options(
            "config-only-snapshot-trim",
            "config-only".to_string(),
            runtime,
            event_emitter,
            None,
            &SnapshotEvaluationSessionInitOptions {
                config_only_mode: true,
                ..SnapshotEvaluationSessionInitOptions::default()
            },
        );

        assert!(standard.release_unused_heap_memory_after_update);
        assert!(!config_only.release_unused_heap_memory_after_update);
        assert!(standard.internal_observability_enabled);
        assert!(!config_only.internal_observability_enabled);
    }

    #[test]
    fn scoped_checksum_mismatch_never_publishes_or_advances_the_snapshot() {
        let store = SpecStore::new_with_snapshot_evaluation_session_options(
            "scoped-checksum-guard",
            "scoped-checksum-guard".to_string(),
            StatsigRuntime::get_runtime(),
            Arc::new(SdkEventEmitter::default()),
            None,
            &SnapshotEvaluationSessionInitOptions {
                config_only_mode: true,
                ..SnapshotEvaluationSessionInitOptions::default()
            },
        );
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json")).unwrap();
        specs["time"] = serde_json::json!(100);
        specs["checksum"] = serde_json::json!("initial-checksum");
        store
            .set_values(SpecsUpdate {
                data: ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap()),
                source: SpecsSource::Network,
                received_at: 1,
                source_api: None,
                has_updates: None,
            })
            .unwrap();
        let original = store.load_data();

        specs["time"] = serde_json::json!(200);
        specs["checksum"] = serde_json::json!("incorrect-payload-checksum");
        let mut data = ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap());
        data.set_scoped_expected_checksum("expected-metadata-checksum");
        let result = store.set_values(SpecsUpdate {
            data,
            source: SpecsSource::Adapter("ScopedConfigSource".to_string()),
            received_at: 2,
            source_api: Some("ScopedConfigSource".to_string()),
            has_updates: None,
        });

        assert!(matches!(result, Err(StatsigErr::ChecksumFailure(_))));
        let unchanged = store.load_data();
        assert!(Arc::ptr_eq(&original, &unchanged));
        assert_eq!(unchanged.lcut(), 100);
        assert_eq!(unchanged.checksum(), Some("initial-checksum"));

        let mut future_lcut_data = ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap());
        future_lcut_data.set_scoped_expected_checksum("incorrect-payload-checksum");
        future_lcut_data.set_scoped_expected_lcut(150);
        let result = store.set_values(SpecsUpdate {
            data: future_lcut_data,
            source: SpecsSource::Adapter("ScopedConfigSource".to_string()),
            received_at: 3,
            source_api: Some("ScopedConfigSource".to_string()),
            has_updates: None,
        });

        assert!(matches!(result, Err(StatsigErr::ChecksumFailure(_))));
        let unchanged = store.load_data();
        assert!(Arc::ptr_eq(&original, &unchanged));
        assert_eq!(unchanged.lcut(), 100);
        assert_eq!(unchanged.checksum(), Some("initial-checksum"));

        let mut network_data = ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap());
        network_data.set_scoped_expected_checksum("irrelevant-scoped-header");
        network_data.set_scoped_expected_lcut(50);
        store
            .set_values(SpecsUpdate {
                data: network_data,
                source: SpecsSource::Network,
                received_at: 4,
                source_api: None,
                has_updates: None,
            })
            .expect("scoped metadata must never constrain ordinary network updates");
        assert_eq!(
            store.load_data().checksum(),
            Some("incorrect-payload-checksum")
        );

        specs["time"] = serde_json::json!(250);
        specs["checksum"] = serde_json::json!("older-than-metadata-checksum");
        let mut older_lcut_data = ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap());
        older_lcut_data.set_scoped_expected_checksum("older-than-metadata-checksum");
        older_lcut_data.set_scoped_expected_lcut(300);
        store
            .set_values(SpecsUpdate {
                data: older_lcut_data,
                source: SpecsSource::Adapter("ScopedConfigSource".to_string()),
                received_at: 5,
                source_api: Some("ScopedConfigSource".to_string()),
                has_updates: None,
            })
            .expect("older payloads must remain eligible for metadata cursor catch-up");
        assert_eq!(store.load_data().lcut(), 250);
    }

    #[test]
    fn config_only_snapshots_preserve_sdk_configs_without_projecting_global_state() {
        let runtime = StatsigRuntime::get_runtime();
        let event_emitter = Arc::new(SdkEventEmitter::default());
        let standard = SpecStore::new(
            "standard-global-projection",
            "standard-global-projection".to_string(),
            runtime.clone(),
            event_emitter.clone(),
            None,
        );
        let config_only = SpecStore::new_with_snapshot_evaluation_session_options(
            "config-only-global-projection",
            "config-only-global-projection".to_string(),
            runtime,
            event_emitter,
            None,
            &SnapshotEvaluationSessionInitOptions {
                config_only_mode: true,
                ..SnapshotEvaluationSessionInitOptions::default()
            },
        );
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json")).unwrap();
        specs["sdk_configs"] = serde_json::json!({ "snapshot_config": "preserved" });
        specs["sdk_flags"] = serde_json::json!({ "snapshot_flag": true });
        specs["diagnostics"] = serde_json::json!({ "initialize": 7.0 });
        let payload = serde_json::to_vec(&specs).unwrap();

        for store in [&standard, &config_only] {
            store
                .set_values(SpecsUpdate {
                    data: ResponseData::from_bytes(payload.clone()),
                    source: SpecsSource::Network,
                    received_at: 1,
                    source_api: None,
                    has_updates: None,
                })
                .unwrap();
        }

        let standard_globals = standard.global_configs.as_ref().unwrap();
        assert!(standard_globals.get_sdk_flag_value("snapshot_flag"));
        standard_globals.use_sdk_config_value("snapshot_config", |value| {
            assert_eq!(
                value.map(|value| &value.json_value),
                Some(&serde_json::json!("preserved"))
            );
        });
        assert!(config_only.global_configs.is_none());
        assert_eq!(
            config_only
                .load_data()
                .snapshot
                .sdk_configs
                .as_ref()
                .and_then(|configs| configs.get("snapshot_config"))
                .map(|value| &value.json_value),
            Some(&serde_json::json!("preserved"))
        );
        assert_eq!(
            config_only
                .load_data()
                .snapshot
                .sdk_flags
                .as_ref()
                .and_then(|flags| flags.get("snapshot_flag")),
            Some(&true)
        );
    }

    #[test]
    fn only_config_only_snapshots_prepare_evaluation_metadata() {
        let runtime = StatsigRuntime::get_runtime();
        let event_emitter = Arc::new(SdkEventEmitter::default());
        let standard = SpecStore::new(
            "standard-snapshot-preparation",
            "standard-snapshot-preparation".to_string(),
            runtime.clone(),
            event_emitter.clone(),
            None,
        );
        let config_only = SpecStore::new_with_snapshot_evaluation_session_options(
            "config-only-snapshot-preparation",
            "config-only-snapshot-preparation".to_string(),
            runtime,
            event_emitter,
            None,
            &SnapshotEvaluationSessionInitOptions {
                config_only_mode: true,
                preserve_dcs_session_update_mode: true,
                ..SnapshotEvaluationSessionInitOptions::default()
            },
        );
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json")).unwrap();
        specs["auto_capture_settings"] = serde_json::json!({
            "disabled_events": { "click": true }
        });
        specs["condition_map"]["snapshot-id-list"] = serde_json::json!({
            "type": "unit_id",
            "targetValue": "beta_users",
            "operator": "in_segment_list",
            "idType": "userID"
        });
        specs["feature_gates"]["test_small_pass_gate"]["sessionUpdateMode"] =
            serde_json::json!("live");
        specs["feature_gates"]["test_small_pass_gate"]["targetAppIDs"] =
            serde_json::json!(["prepared-app"]);
        let payload = serde_json::to_vec(&specs).unwrap();

        for store in [&standard, &config_only] {
            store
                .set_values(SpecsUpdate {
                    data: ResponseData::from_bytes(payload.clone()),
                    source: SpecsSource::Network,
                    received_at: 1,
                    source_api: None,
                    has_updates: None,
                })
                .unwrap();
        }

        let standard_data = standard.load_data();
        assert!(!standard_data.has_id_list_conditions);
        assert!(standard_data.auto_capture_settings_value.is_none());
        assert_eq!(standard_data.auto_capture_settings_hash, 0);
        assert!(standard_data.live_overlay_target_app_index.get().is_none());

        let config_only_data = config_only.load_data();
        assert!(config_only_data.has_id_list_conditions);
        assert!(
            config_only_data
                .id_list_lookup_conditions()
                .iter()
                .any(|condition| condition.name == "beta_users")
        );
        assert!(config_only_data.auto_capture_settings_value.is_some());
        assert_ne!(config_only_data.auto_capture_settings_hash, 0);
        let index = config_only_data
            .live_overlay_target_app_index
            .get()
            .expect("config-only snapshots should prepare live target app metadata");
        assert!(index.has_live_entities);
        assert!(index.target_app_ids.contains("prepared-app"));
    }

    #[test]
    fn spec_store_data_reuses_gcir_evaluation_plan_cache_across_clones() {
        let data = SpecStoreData {
            source: SpecsSource::Network,
            source_api: Some("/v2/download_config_specs".to_string()),
            time_received_at: Some(1),
            snapshot: Arc::new(SpecsResponseFull::default()),
            id_lists: Arc::new(HashMap::new()),
            has_id_list_conditions: false,
            id_list_lookup_conditions: Arc::new(OnceLock::new()),
            auto_capture_settings_value: None,
            auto_capture_settings_hash: 0,
            live_overlay_target_app_index: Arc::new(Default::default()),
            gcir_evaluation_plan: Arc::new(OnceLock::new()),
            sync_cursor: ConfigSyncCursor::default(),
            spec_decode_stats: SpecDecodeStats::default(),
        };
        let hashing = HashUtil::new();

        let first = data.gcir_evaluation_plan(&hashing);
        let cloned = data.clone();
        let second = cloned.gcir_evaluation_plan(&hashing);

        assert!(std::ptr::eq(first, second));
        assert!(Arc::ptr_eq(
            &data.live_overlay_target_app_index,
            &cloned.live_overlay_target_app_index
        ));
        assert!(Arc::ptr_eq(
            &data.id_list_lookup_conditions,
            &cloned.id_list_lookup_conditions
        ));
    }

    #[test]
    fn semantic_snapshot_updates_replace_live_target_app_index_but_cursor_updates_reuse_it() {
        let store = SpecStore::new_with_snapshot_evaluation_session_options(
            "live-overlay-snapshot-index",
            "live-overlay-snapshot-index".to_string(),
            StatsigRuntime::get_runtime(),
            Arc::new(SdkEventEmitter::default()),
            None,
            &SnapshotEvaluationSessionInitOptions {
                config_only_mode: true,
                preserve_dcs_session_update_mode: true,
                ..SnapshotEvaluationSessionInitOptions::default()
            },
        );
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json")).unwrap();
        specs["feature_gates"]["test_small_pass_gate"]["sessionUpdateMode"] =
            serde_json::json!("live");
        specs["feature_gates"]["test_small_pass_gate"]["targetAppIDs"] =
            serde_json::json!(["first-app"]);

        store
            .set_values(SpecsUpdate {
                data: ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap()),
                source: SpecsSource::Network,
                received_at: 1,
                source_api: None,
                has_updates: None,
            })
            .unwrap();
        let first = store.load_data();
        assert!(
            first
                .live_overlay_target_app_index
                .get()
                .unwrap()
                .target_app_ids
                .contains("first-app")
        );

        store.specs_cursor_update_apply(
            first.lcut() + 1,
            "cursor-only-checksum".to_string(),
            SpecsSource::Network,
            None,
        );
        let cursor_only = store.load_data();
        assert!(Arc::ptr_eq(&first.snapshot, &cursor_only.snapshot,));
        assert!(Arc::ptr_eq(
            &first.live_overlay_target_app_index,
            &cursor_only.live_overlay_target_app_index,
        ));
        assert!(Arc::ptr_eq(
            &first.id_list_lookup_conditions,
            &cursor_only.id_list_lookup_conditions,
        ));

        specs["time"] = serde_json::json!(cursor_only.lcut() + 1);
        specs["checksum"] = serde_json::json!("semantic-update-checksum");
        specs["feature_gates"]["test_small_pass_gate"]["targetAppIDs"] =
            serde_json::json!(["second-app"]);
        store
            .set_values(SpecsUpdate {
                data: ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap()),
                source: SpecsSource::Network,
                received_at: 2,
                source_api: None,
                has_updates: None,
            })
            .unwrap();
        let refreshed = store.load_data();
        assert!(!Arc::ptr_eq(
            &cursor_only.live_overlay_target_app_index,
            &refreshed.live_overlay_target_app_index,
        ));
        assert!(!Arc::ptr_eq(
            &cursor_only.id_list_lookup_conditions,
            &refreshed.id_list_lookup_conditions,
        ));
        let refreshed_index = refreshed.live_overlay_target_app_index.get().unwrap();
        assert!(refreshed_index.target_app_ids.contains("second-app"));
        assert!(!refreshed_index.target_app_ids.contains("first-app"));
    }

    #[test]
    fn standard_snapshot_sessions_build_live_target_app_index_lazily() {
        let store = SpecStore::new_with_snapshot_evaluation_session_options(
            "standard-live-overlay-index",
            "standard-live-overlay-index".to_string(),
            StatsigRuntime::get_runtime(),
            Arc::new(SdkEventEmitter::default()),
            None,
            &SnapshotEvaluationSessionInitOptions {
                preserve_dcs_session_update_mode: true,
                ..SnapshotEvaluationSessionInitOptions::default()
            },
        );
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json")).unwrap();
        specs["feature_gates"]["test_small_pass_gate"]["sessionUpdateMode"] =
            serde_json::json!("live");
        specs["feature_gates"]["test_small_pass_gate"]["targetAppIDs"] =
            serde_json::json!(["standard-app"]);
        store
            .set_values(SpecsUpdate {
                data: ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap()),
                source: SpecsSource::Network,
                received_at: 1,
                source_api: None,
                has_updates: None,
            })
            .unwrap();
        let data = store.load_data();
        assert!(data.live_overlay_target_app_index.get().is_none());

        let hashing = HashUtil::new();
        let session = SnapshotEvaluationSession::new(Arc::clone(&data), &hashing, false);
        assert!(session.has_live_overlay_entities_for_target_app(Some("standard-app")));
        assert!(!session.has_live_overlay_entities_for_target_app(Some("other-app")));
        assert!(session.has_live_overlay_entities_for_target_app(None));
        assert!(data.live_overlay_target_app_index.get().is_some());
    }

    #[test]
    fn live_target_app_index_ignores_unscoped_and_non_live_entities() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json")).unwrap();
        specs["feature_gates"]["test_small_pass_gate"]["sessionUpdateMode"] =
            serde_json::json!("live");
        specs["feature_gates"]["test_small_pass_gate"]
            .as_object_mut()
            .unwrap()
            .remove("targetAppIDs");
        specs["dynamic_configs"]["test_custom_config"]["targetAppIDs"] =
            serde_json::json!(["non-live-app"]);
        let specs: SpecsResponseFull = serde_json::from_value(specs).unwrap();
        let index = build_live_overlay_target_app_index(&specs);

        assert!(index.has_live_entities);
        assert!(index.target_app_ids.is_empty());
    }
}
