use async_trait::async_trait;
use chrono::Utc;
use std::collections::HashMap;
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::time::Duration;
use tokio::runtime::Handle;
use tokio::sync::{Mutex as AsyncMutex, OnceCell};

use crate::data_store_interface::{RequestPath, get_data_store_key};
use crate::evaluation::country_lookup::CountryLookup;
use crate::hashing::HashUtil;
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::scoped_id_list_membership_service::ScopedIdListMembershipService;
use crate::sdk_event_emitter::SdkEventEmitter;
use crate::snapshot_evaluation_session::SnapshotEvaluationSession;
use crate::spec_store::{SpecStore, SpecStoreData};
use crate::specs_adapter::{ScopedConfigMetadata, ScopedConfigSource, ScopedSourceSpecsAdapter};
use crate::statsig_options::{DEFAULT_INIT_TIMEOUT_MS, SnapshotEvaluationSessionInitOptions};
#[cfg(test)]
use crate::{EvaluationOperation, EvaluationResult};
use crate::{
    EvaluationRequest, IdListsAdapter, ObservabilityClient, SpecsAdapter, SpecsInfo, SpecsSource,
    SpecsUpdate, StatsigErr, StatsigHttpIdListsAdapter, StatsigOptions, StatsigRuntime,
    StatsigUser, networking::ResponseData,
};

const COUNTRY_LOOKUP_TASK: &str = "INIT_COUNTRY_LOOKUP";
const ENGINE_SHUTDOWN_TIMEOUT: Duration = Duration::from_secs(3);
const ID_LIST_INITIALIZATION_TIMEOUT: Duration = Duration::from_millis(DEFAULT_INIT_TIMEOUT_MS);
static NEXT_EVALUATION_CLIENT_ID: AtomicU64 = AtomicU64::new(1);

/// Opaque version and transport-owned token for an authorized data read.
pub type EvaluationDataVersion = ScopedConfigMetadata;

/// Passive data I/O bound to an authorization context owned by its host.
#[async_trait]
pub trait EvaluationDataTransport: Send + Sync {
    /// Returns an optional bounded source category without revealing its identity.
    fn observability_scope_class(&self) -> Option<&'static str> {
        None
    }

    /// Returns the trusted config origin used to resolve remote-value references.
    ///
    /// Hosts that supply configuration from a custom origin must explicitly opt in to trusting
    /// that origin. The SDK still enforces same-origin and content-integrity protections.
    fn trusted_hydration_source_url(&self) -> Option<&str> {
        None
    }

    async fn fetch_metadata(&self) -> Result<EvaluationDataVersion, StatsigErr>;

    /// Fetches metadata using the current cursor owned by the evaluation instance.
    async fn fetch_metadata_with_cursor(
        &self,
        _current: &SpecsInfo,
    ) -> Result<EvaluationDataVersion, StatsigErr> {
        self.fetch_metadata().await
    }

    async fn fetch_payload(
        &self,
        version: &EvaluationDataVersion,
        fallback: bool,
    ) -> Result<ResponseData, StatsigErr>;
}

struct EvaluationDataSource {
    transport: Arc<dyn EvaluationDataTransport>,
}

#[async_trait]
impl ScopedConfigSource for EvaluationDataSource {
    fn observability_scope_class(&self) -> Option<&'static str> {
        self.transport.observability_scope_class()
    }

    fn trusted_hydration_source_url(&self) -> Option<&str> {
        self.transport.trusted_hydration_source_url()
    }

    async fn fetch_metadata(&self) -> Result<ScopedConfigMetadata, StatsigErr> {
        self.transport.fetch_metadata().await
    }

    async fn fetch_metadata_with_cursor(
        &self,
        current: &SpecsInfo,
    ) -> Result<ScopedConfigMetadata, StatsigErr> {
        self.transport.fetch_metadata_with_cursor(current).await
    }

    async fn fetch_payload(
        &self,
        metadata: &ScopedConfigMetadata,
    ) -> Result<ResponseData, StatsigErr> {
        self.transport.fetch_payload(metadata, false).await
    }

    async fn fetch_fallback_payload(
        &self,
        metadata: &ScopedConfigMetadata,
    ) -> Result<Option<ResponseData>, StatsigErr> {
        self.transport.fetch_payload(metadata, true).await.map(Some)
    }
}

fn snapshot_instance_id(identity: &str) -> String {
    format!(
        "scoped:{}",
        crate::hashing::HashUtil::new().sha256(identity)
    )
}

/// An eagerly initialized, tenant-bound ID-list snapshot shared by one evaluation client.
pub struct SharedIdLists {
    tenant_key: Arc<str>,
    owner_instance_id: Arc<str>,
    spec_store: Arc<SpecStore>,
    adapter: Arc<dyn IdListsAdapter>,
    shutting_down: AtomicBool,
}

impl SharedIdLists {
    async fn shutdown(&self) {
        if !self.shutting_down.swap(true, Ordering::AcqRel) {
            let _ = self.adapter.shutdown(ENGINE_SHUTDOWN_TIMEOUT).await;
        }
    }
}

#[derive(Default)]
struct ScopedIdListSources {
    adapter: Option<Arc<dyn IdListsAdapter>>,
    shared: Option<Arc<SharedIdLists>>,
}

/// Owns only the primitives required to synchronize and evaluate one immutable snapshot stream.
pub(crate) struct EvaluationEngine {
    spec_store: Arc<SpecStore>,
    adapter: Option<Arc<ScopedSourceSpecsAdapter>>,
    id_lists_adapter: Option<Arc<dyn IdListsAdapter>>,
    shared_id_lists: Option<Arc<SharedIdLists>>,
    id_lists_initialized: OnceCell<()>,
    runtime: Arc<StatsigRuntime>,
    hashing: HashUtil,
    shutting_down: AtomicBool,
}

impl EvaluationEngine {
    fn new(
        credential: &str,
        identity: &str,
        source: Arc<dyn ScopedConfigSource>,
        runtime: Handle,
        interned_mmap_sdk_key: Option<&str>,
        observability: Option<&Arc<dyn ObservabilityClient>>,
        id_list_sources: ScopedIdListSources,
    ) -> Arc<Self> {
        Self::build(
            credential,
            identity,
            Some(source),
            Some(runtime),
            interned_mmap_sdk_key,
            observability,
            id_list_sources,
        )
    }

    pub(crate) fn from_fixture(
        specs_json: String,
        interned_mmap_sdk_key: Option<&str>,
    ) -> Result<Arc<Self>, StatsigErr> {
        let engine = Self::build(
            "secret-local-evaluation-fixture",
            "local-evaluation-fixture",
            None,
            Handle::try_current().ok(),
            interned_mmap_sdk_key,
            None,
            ScopedIdListSources::default(),
        );
        engine.spec_store.set_source(SpecsSource::Loading);
        if let Err(error) = engine.spec_store.set_values(SpecsUpdate {
            data: ResponseData::from_bytes(specs_json.into_bytes()),
            source: SpecsSource::Bootstrap,
            received_at: Utc::now().timestamp_millis() as u64,
            source_api: None,
            has_updates: None,
        }) {
            engine.spec_store.set_source(SpecsSource::NoValues);
            engine.runtime.shutdown();
            return Err(error);
        }
        engine.start_country_lookup();
        Ok(engine)
    }

    fn build(
        credential: &str,
        identity: &str,
        source: Option<Arc<dyn ScopedConfigSource>>,
        runtime: Option<Handle>,
        interned_mmap_sdk_key: Option<&str>,
        observability: Option<&Arc<dyn ObservabilityClient>>,
        id_list_sources: ScopedIdListSources,
    ) -> Arc<Self> {
        let hashing = HashUtil::new();
        let instance_id = snapshot_instance_id(identity);
        let options = StatsigOptions {
            sdk_instance_id: Some(instance_id.clone()),
            disable_all_logging: Some(true),
            disable_network: Some(true),
            enable_id_lists: Some(
                id_list_sources.adapter.is_some() || id_list_sources.shared.is_some(),
            ),
            fallback_to_statsig_api: Some(false),
            disable_disk_access: Some(true),
            ..StatsigOptions::default()
        };
        let data_store_key =
            get_data_store_key(RequestPath::RulesetsV2, credential, &hashing, &options);
        let engine_runtime = StatsigRuntime::get_runtime();
        if let Some(runtime) = runtime {
            engine_runtime.bind_external_runtime(runtime);
        }
        let session_options = SnapshotEvaluationSessionInitOptions {
            preserve_dcs_session_update_mode: true,
            precompute_gcir_evaluation_plan: true,
            config_only_mode: true,
            interned_mmap_sdk_key: interned_mmap_sdk_key.map(str::to_owned),
        };
        let spec_store = {
            let disabled = Arc::new(OpsStatsForInstance::disabled());
            let _disabled_observability =
                OPS_STATS.enter_instance_scope(instance_id.as_str(), Some(disabled));
            Arc::new(SpecStore::new_with_snapshot_evaluation_session_options(
                credential,
                data_store_key,
                Arc::clone(&engine_runtime),
                Arc::new(SdkEventEmitter::default()),
                Some(&options),
                &session_options,
            ))
        };
        let adapter = source.map(|source| {
            let adapter = Arc::new(ScopedSourceSpecsAdapter::new(source, identity));
            if let Some(observer) = observability {
                adapter.bind_observability_client(Arc::clone(observer));
            }
            adapter
        });
        Arc::new(Self {
            spec_store,
            adapter,
            id_lists_adapter: id_list_sources.adapter,
            shared_id_lists: id_list_sources.shared,
            id_lists_initialized: OnceCell::new(),
            runtime: engine_runtime,
            hashing,
            shutting_down: AtomicBool::new(false),
        })
    }

    async fn initialize(&self) -> Result<(), StatsigErr> {
        let adapter = self.adapter.as_ref().ok_or_else(|| {
            StatsigErr::InvalidOperation("Fixture evaluation engines do not synchronize".into())
        })?;
        self.spec_store.set_source(SpecsSource::Loading);
        adapter.initialize(Arc::clone(&self.spec_store) as _);

        let country_lookup = self.start_country_lookup();

        if let Err(error) = Arc::clone(adapter).start(&self.runtime).await {
            self.spec_store.set_source(SpecsSource::NoValues);
            return Err(error);
        }

        if let Some(task_id) = country_lookup {
            let _ = self
                .runtime
                .await_join_handle(COUNTRY_LOOKUP_TASK, &task_id)
                .await;
        }

        Arc::clone(adapter)
            .schedule_background_sync(&self.runtime)
            .await?;

        Ok(())
    }

    pub(crate) fn id_lists_initialized(&self) -> bool {
        self.adapter.is_none()
            || self.shared_id_lists.is_some()
            || self.id_lists_initialized.get().is_some()
    }

    pub(crate) async fn initialize_id_lists(&self) -> Result<(), StatsigErr> {
        if self.adapter.is_none() {
            return Ok(());
        }
        if self.shutting_down.load(Ordering::Acquire) {
            return Err(StatsigErr::InvalidOperation(
                "Evaluation instance is shutting down".to_string(),
            ));
        }

        let adapter = self.id_lists_adapter.as_ref().ok_or_else(|| {
            StatsigErr::InvalidOperation(
                "An authorized ID-list adapter is required for this evaluation".to_string(),
            )
        })?;

        tokio::time::timeout(
            ID_LIST_INITIALIZATION_TIMEOUT,
            self.id_lists_initialized.get_or_try_init(|| async {
                Arc::clone(adapter)
                    .start(&self.runtime, Arc::clone(&self.spec_store) as _)
                    .await?;
                if self.shutting_down.load(Ordering::Acquire) {
                    return Err(StatsigErr::InvalidOperation(
                        "Evaluation instance is shutting down".to_string(),
                    ));
                }
                Arc::clone(adapter)
                    .schedule_background_sync(&self.runtime)
                    .await?;
                Ok::<(), StatsigErr>(())
            }),
        )
        .await
        .map_err(|_| {
            StatsigErr::DataStoreFailure(
                "ID-list initialization exceeded the SDK initialization timeout".to_string(),
            )
        })??;

        if self.shutting_down.load(Ordering::Acquire) {
            return Err(StatsigErr::InvalidOperation(
                "Evaluation instance is shutting down".to_string(),
            ));
        }
        Ok(())
    }

    fn start_country_lookup(&self) -> Option<tokio::task::Id> {
        if CountryLookup::is_loaded() {
            return None;
        }

        self.runtime
            .spawn(COUNTRY_LOOKUP_TASK, |_| async {
                CountryLookup::load_country_lookup();
            })
            .ok()
    }

    pub(crate) fn snapshot_evaluation_data(&self) -> Arc<SpecStoreData> {
        match &self.shared_id_lists {
            Some(shared) => self
                .spec_store
                .load_data_with_shared_id_lists(&shared.spec_store),
            None => self.spec_store.load_data(),
        }
    }

    pub(crate) fn snapshot_evaluation_session(
        &self,
        data: Arc<SpecStoreData>,
    ) -> SnapshotEvaluationSession<'_> {
        SnapshotEvaluationSession::new_with_statsig(data, &self.hashing, false, None, None)
    }

    #[cfg(test)]
    pub(crate) fn update_fixture_for_test(&self, update: SpecsUpdate) -> Result<(), StatsigErr> {
        self.spec_store.set_values(update)
    }

    #[cfg(any(test, feature = "testing"))]
    pub(crate) fn seed_id_lists_for_test(
        &self,
        memberships: &std::collections::HashMap<String, std::collections::HashSet<String>>,
    ) {
        use crate::id_lists_adapter::{IdListMetadata, IdListUpdate, IdListsUpdateListener};

        let updates = memberships
            .iter()
            .map(|(name, ids)| {
                let raw_changeset = ids
                    .iter()
                    .map(|id| format!("+{id}"))
                    .collect::<Vec<_>>()
                    .join("\n");
                (
                    name.clone(),
                    IdListUpdate {
                        new_metadata: IdListMetadata {
                            name: name.clone(),
                            url: String::new(),
                            file_id: None,
                            size: raw_changeset.len() as u64,
                            creation_time: 0,
                        },
                        raw_changeset: Some(raw_changeset),
                    },
                )
            })
            .collect();
        self.spec_store.did_receive_id_list_updates(updates);
    }

    async fn shutdown(&self) -> Result<(), StatsigErr> {
        if self.shutting_down.swap(true, Ordering::AcqRel) {
            return Ok(());
        }

        let id_list_result = match &self.id_lists_adapter {
            Some(adapter) => adapter.shutdown(ENGINE_SHUTDOWN_TIMEOUT).await,
            None => Ok(()),
        };
        let config_result = match &self.adapter {
            Some(adapter) => {
                adapter
                    .shutdown(ENGINE_SHUTDOWN_TIMEOUT, &self.runtime)
                    .await
            }
            None => Ok(()),
        };
        self.runtime.shutdown();
        id_list_result.and(config_result)
    }
}

/// An initialized evaluation instance securely bound to its authenticated tenant.
pub struct EvaluationInstance {
    engine: Arc<EvaluationEngine>,
    tenant_key: Arc<str>,
}

impl EvaluationInstance {
    /// Shuts down this instance after its host has removed it from circulation.
    pub async fn shutdown(&self) -> Result<(), StatsigErr> {
        self.engine.shutdown().await
    }
}

/// Owns generic instance construction and evaluation against immutable SDK snapshots.
pub struct EvaluationClient {
    runtime: Handle,
    observability: Option<Arc<dyn ObservabilityClient>>,
    id_lists_sdk_instance_id: String,
    _id_lists_ops_stats: Arc<OpsStatsForInstance>,
    id_lists_observability_runtime: Arc<StatsigRuntime>,
    id_list_membership_service: Option<Arc<ScopedIdListMembershipService>>,
    shared_id_lists: AsyncMutex<HashMap<String, Arc<SharedIdLists>>>,
    shutting_down: AtomicBool,
}

impl EvaluationClient {
    pub fn new(
        runtime: Handle,
        observability: Option<Arc<dyn ObservabilityClient>>,
    ) -> Result<Arc<Self>, StatsigErr> {
        Self::new_with_id_list_server(runtime, observability, None)
    }

    /// Optionally resolves request-scoped memberships through a trusted ID-list service.
    pub fn new_with_id_list_server(
        runtime: Handle,
        observability: Option<Arc<dyn ObservabilityClient>>,
        server_url: Option<String>,
    ) -> Result<Arc<Self>, StatsigErr> {
        let id_lists_sdk_instance_id = format!(
            "scoped-id-lists:{}",
            NEXT_EVALUATION_CLIENT_ID.fetch_add(1, Ordering::Relaxed)
        );
        let id_lists_ops_stats = OPS_STATS.get_for_instance(&id_lists_sdk_instance_id);
        let id_lists_observability_runtime = StatsigRuntime::get_runtime();
        id_lists_observability_runtime.bind_external_runtime(runtime.clone());
        let id_list_membership_service = server_url
            .map(|url| {
                ScopedIdListMembershipService::new(
                    url,
                    Arc::clone(&id_lists_observability_runtime),
                    observability
                        .as_ref()
                        .map(|_| Arc::clone(&id_lists_ops_stats)),
                )
            })
            .transpose()?;
        if let Some(observer) = observability.as_ref() {
            let observer = Arc::clone(observer).to_ops_stats_event_observer();
            id_lists_ops_stats.subscribe(
                Arc::clone(&id_lists_observability_runtime),
                Arc::downgrade(&observer),
            );
        }

        Ok(Arc::new(Self {
            runtime,
            observability,
            id_lists_sdk_instance_id,
            _id_lists_ops_stats: id_lists_ops_stats,
            id_lists_observability_runtime,
            id_list_membership_service,
            shared_id_lists: AsyncMutex::new(HashMap::new()),
            shutting_down: AtomicBool::new(false),
        }))
    }

    /// Returns the opaque, shared observability identity for this client's ID-list adapters.
    pub fn id_lists_sdk_instance_id(&self) -> &str {
        &self.id_lists_sdk_instance_id
    }

    /// Downloads a tenant's ID lists once and shares their immutable snapshots across instances.
    pub async fn preload_shared_id_lists(
        &self,
        sdk_key: &str,
        tenant_key: &str,
        options: &StatsigOptions,
    ) -> Result<Arc<SharedIdLists>, StatsigErr> {
        let mut adapter_options = options.clone();
        adapter_options.sdk_instance_id = Some(self.id_lists_sdk_instance_id.clone());
        let adapter = Arc::new(StatsigHttpIdListsAdapter::new(sdk_key, &adapter_options));
        self.preload_shared_id_lists_with_adapter(sdk_key, tenant_key, &adapter_options, adapter)
            .await
    }

    async fn preload_shared_id_lists_with_adapter(
        &self,
        sdk_key: &str,
        tenant_key: &str,
        options: &StatsigOptions,
        adapter: Arc<dyn IdListsAdapter>,
    ) -> Result<Arc<SharedIdLists>, StatsigErr> {
        if sdk_key.is_empty() || tenant_key.is_empty() {
            return Err(StatsigErr::InvalidOperation(
                "A shared ID-list owner requires an authenticated credential and tenant"
                    .to_string(),
            ));
        }

        let credential_identity = HashUtil::new().sha256(sdk_key);
        let mut owners = self.shared_id_lists.lock().await;
        if self.shutting_down.load(Ordering::Acquire) {
            return Err(StatsigErr::InvalidOperation(
                "Evaluation client is shutting down".to_string(),
            ));
        }
        if let Some(owner) = owners.get(&credential_identity) {
            if owner.tenant_key.as_ref() != tenant_key {
                return Err(StatsigErr::InvalidOperation(
                    "A shared ID-list credential cannot be bound to another tenant".to_string(),
                ));
            }
            return Ok(Arc::clone(owner));
        }

        let hashing = HashUtil::new();
        let data_store_key =
            get_data_store_key(RequestPath::RulesetsV2, sdk_key, &hashing, options);
        let session_options = SnapshotEvaluationSessionInitOptions {
            config_only_mode: true,
            ..SnapshotEvaluationSessionInitOptions::default()
        };
        let spec_store = Arc::new(SpecStore::new_with_snapshot_evaluation_session_options(
            sdk_key,
            data_store_key,
            Arc::clone(&self.id_lists_observability_runtime),
            Arc::new(SdkEventEmitter::default()),
            Some(options),
            &session_options,
        ));
        let timeout =
            Duration::from_millis(options.init_timeout_ms.unwrap_or(DEFAULT_INIT_TIMEOUT_MS));
        let initialized = tokio::time::timeout(
            timeout,
            Arc::clone(&adapter).start(
                &self.id_lists_observability_runtime,
                Arc::clone(&spec_store) as _,
            ),
        )
        .await;

        let initialize_error = match initialized {
            Ok(Ok(())) => None,
            Ok(Err(error)) => Some(error),
            Err(_) => Some(StatsigErr::DataStoreFailure(
                "Shared ID-list initialization exceeded the configured timeout".to_string(),
            )),
        };
        if let Some(error) = initialize_error {
            let _ = adapter.shutdown(ENGINE_SHUTDOWN_TIMEOUT).await;
            return Err(error);
        }
        if self.shutting_down.load(Ordering::Acquire) {
            let _ = adapter.shutdown(ENGINE_SHUTDOWN_TIMEOUT).await;
            return Err(StatsigErr::InvalidOperation(
                "Evaluation client is shutting down".to_string(),
            ));
        }
        if let Err(error) = Arc::clone(&adapter)
            .schedule_background_sync(&self.id_lists_observability_runtime)
            .await
        {
            let _ = adapter.shutdown(ENGINE_SHUTDOWN_TIMEOUT).await;
            return Err(error);
        }
        if self.shutting_down.load(Ordering::Acquire) {
            let _ = adapter.shutdown(ENGINE_SHUTDOWN_TIMEOUT).await;
            return Err(StatsigErr::InvalidOperation(
                "Evaluation client is shutting down".to_string(),
            ));
        }

        let owner = Arc::new(SharedIdLists {
            tenant_key: Arc::from(tenant_key),
            owner_instance_id: Arc::from(self.id_lists_sdk_instance_id.as_str()),
            spec_store,
            adapter,
            shutting_down: AtomicBool::new(false),
        });
        owners.insert(credential_identity, Arc::clone(&owner));
        Ok(owner)
    }

    /// Initializes a host-owned, tenant-bound, config-only evaluation instance.
    ///
    /// The host must bind the transport and tenant key to the same authenticated identity.
    pub async fn create_instance(
        &self,
        credential: &str,
        tenant_key: &str,
        opaque_identity: &str,
        transport: Arc<dyn EvaluationDataTransport>,
        interned_mmap_sdk_key: Option<&str>,
        id_lists_adapter: Option<Arc<dyn IdListsAdapter>>,
    ) -> Result<Arc<EvaluationInstance>, StatsigErr> {
        self.create_instance_with_shared_id_lists(
            credential,
            tenant_key,
            opaque_identity,
            transport,
            interned_mmap_sdk_key,
            id_lists_adapter,
            None,
        )
        .await
    }

    /// Initializes a scoped instance with either its own adapter or a tenant-bound shared owner.
    #[allow(clippy::too_many_arguments)]
    pub async fn create_instance_with_shared_id_lists(
        &self,
        credential: &str,
        tenant_key: &str,
        opaque_identity: &str,
        transport: Arc<dyn EvaluationDataTransport>,
        interned_mmap_sdk_key: Option<&str>,
        id_lists_adapter: Option<Arc<dyn IdListsAdapter>>,
        shared_id_lists: Option<Arc<SharedIdLists>>,
    ) -> Result<Arc<EvaluationInstance>, StatsigErr> {
        if self.shutting_down.load(Ordering::Acquire) {
            return Err(StatsigErr::InvalidOperation(
                "Evaluation client is shutting down".to_string(),
            ));
        }
        if let Some(shared) = &shared_id_lists {
            if id_lists_adapter.is_some()
                || shared.tenant_key.as_ref() != tenant_key
                || shared.owner_instance_id.as_ref() != self.id_lists_sdk_instance_id
                || shared.shutting_down.load(Ordering::Acquire)
            {
                return Err(StatsigErr::InvalidOperation(
                    "Shared ID lists must belong exclusively to this client and tenant".to_string(),
                ));
            }
        }

        let engine = EvaluationEngine::new(
            credential,
            opaque_identity,
            Arc::new(EvaluationDataSource { transport }),
            self.runtime.clone(),
            interned_mmap_sdk_key,
            self.observability.as_ref(),
            ScopedIdListSources {
                adapter: id_lists_adapter,
                shared: shared_id_lists,
            },
        );

        if let Err(error) = engine.initialize().await {
            let _ = engine.shutdown().await;
            return Err(error);
        }
        if self.shutting_down.load(Ordering::Acquire) {
            let _ = engine.shutdown().await;
            return Err(StatsigErr::InvalidOperation(
                "Evaluation client is shutting down".to_string(),
            ));
        }

        Ok(Arc::new(EvaluationInstance {
            engine,
            tenant_key: Arc::from(tenant_key),
        }))
    }

    /// Pins an initialized instance and its immutable snapshot for one evaluation request.
    #[cfg(test)]
    pub(crate) fn prepare_evaluation(
        &self,
        instance: Arc<EvaluationInstance>,
        user: StatsigUser,
        target_app_id: Option<String>,
    ) -> Result<EvaluationRequest, StatsigErr> {
        self.prepare_evaluation_with_id_list_access(instance, user, target_app_id, true)
    }

    /// Pins a snapshot with the ID-list access capability granted to its request.
    pub fn prepare_evaluation_with_id_list_access(
        &self,
        instance: Arc<EvaluationInstance>,
        user: StatsigUser,
        target_app_id: Option<String>,
        allow_id_lists: bool,
    ) -> Result<EvaluationRequest, StatsigErr> {
        if self.shutting_down.load(Ordering::Acquire) {
            return Err(StatsigErr::InvalidOperation(
                "Evaluation client is shutting down".to_string(),
            ));
        }

        Ok(EvaluationRequest::new(
            crate::scoped_evaluation_request::ScopedEvaluationRequest::from_engine_with_id_list_access(
                Arc::clone(&instance.engine),
                user,
                target_app_id,
                allow_id_lists,
            ),
            Arc::clone(&instance.tenant_key),
        )
        .with_id_list_membership_service(self.id_list_membership_service.clone()))
    }

    /// Evaluates one request without exposing its snapshot or tenant internals.
    #[cfg(test)]
    pub(crate) async fn evaluate(
        &self,
        instance: Arc<EvaluationInstance>,
        user: StatsigUser,
        target_app_id: Option<String>,
        operation: EvaluationOperation<'_>,
    ) -> Result<EvaluationResult, StatsigErr> {
        self.prepare_evaluation(instance, user, target_app_id)?
            .evaluate(operation)
            .await
    }

    /// Rejects new work after the host has shut down its own evaluation instances.
    pub async fn shutdown(&self) {
        self.shutting_down.store(true, Ordering::Release);
        if let Some(service) = self.id_list_membership_service.as_ref() {
            service.shutdown();
        }
        let owners = {
            let mut owners = self.shared_id_lists.lock().await;
            std::mem::take(&mut *owners)
        };
        for owner in owners.into_values() {
            owner.shutdown().await;
        }
        self.id_lists_observability_runtime.shutdown();
    }
}

#[cfg(test)]
mod tests {
    use super::{
        EvaluationClient, EvaluationDataSource, EvaluationDataTransport, EvaluationDataVersion,
        EvaluationEngine, snapshot_instance_id,
    };
    use crate::{
        EvaluationFixtureClient, EvaluationOperation, EvaluationResult, IdListsAdapter,
        ObservabilityClient, OpsStatsEventObserver, SpecsAdapter, StatsigErr,
        StatsigHttpIdListsAdapter, StatsigOptions, StatsigRuntime, StatsigUser,
        hashing::HashUtil,
        id_lists_adapter::{IdListMetadata, IdListUpdate, IdListsUpdateListener},
        interned_values::{
            InternedStore,
            interned_store::{preload_mmap_v2_multi_for_test, write_mmap_v2_for_test},
        },
        networking::ResponseData,
        observability::ops_stats::OPS_STATS,
        specs_response::spec_types::SpecsResponseFull,
    };
    use async_trait::async_trait;
    use parking_lot::Mutex;
    use rusty_fork::rusty_fork_test;
    use serial_test::serial;
    use std::collections::{HashMap, HashSet};
    use std::sync::Arc;
    use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
    use std::time::Duration;
    use tokio::runtime::Handle;
    use tokio::sync::Notify;

    const TEST_CHECKSUM: &str = "evaluation-instance-test-checksum";

    rusty_fork_test! {
        #[test]
        fn fixture_engine_uses_configured_mmap_sdk_key_without_materializing_specs() {
            const SPECS: &[u8] = include_bytes!("../tests/data/eval_proj_dcs.json");

            assert!(!InternedStore::has_preloaded_mmap_v2());
            let directory = tempfile::tempdir().unwrap();
            let path = directory.path().join("interned-store-v2-snapshot.mmap");
            write_mmap_v2_for_test(SPECS, &path).unwrap();
            preload_mmap_v2_multi_for_test(&[("preload-key", &path)]).unwrap();

            let engine = EvaluationEngine::from_fixture(
                String::from_utf8(SPECS.to_vec()).unwrap(),
                Some("preload-key"),
            )
            .expect("fixture engine should initialize from the configured mmap project");
            let snapshot = engine.snapshot_evaluation_data();

            for specs in [
                &snapshot.snapshot.feature_gates,
                &snapshot.snapshot.dynamic_configs,
                &snapshot.snapshot.layer_configs,
            ] {
                assert!(specs.iter().all(|(_, spec)| spec.is_mmap()));
            }
            assert_eq!(InternedStore::get_mmap_spec_materialization_len(), 0);
        }
    }

    struct TestDataTransport {
        payload: Mutex<Vec<u8>>,
        metadata_fetches: AtomicUsize,
        initialization_thread: Mutex<Option<String>>,
        category: Option<&'static str>,
        trusted_source_url: Option<String>,
    }

    impl TestDataTransport {
        fn new(include_id_list_condition: bool) -> Arc<Self> {
            let mut specs = if include_id_list_condition {
                let mut specs: serde_json::Value =
                    serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                        .expect("evaluation snapshot should deserialize");
                specs["condition_map"]["tenant-id-list"] = serde_json::json!({
                    "type": "unit_id",
                    "targetValue": "tenant_members",
                    "operator": "in_segment_list",
                    "idType": "userID"
                });
                specs["feature_gates"]["test_small_pass_gate"]["rules"][0]["conditions"] =
                    serde_json::json!(["tenant-id-list"]);
                specs["feature_gates"]["test_small_pass_gate"]["rules"][0]["passPercentage"] =
                    serde_json::json!(100);
                specs
            } else {
                serde_json::to_value(SpecsResponseFull::default())
                    .expect("empty snapshot should serialize")
            };
            specs["has_updates"] = serde_json::Value::Bool(true);
            specs["time"] = serde_json::Value::from(1);
            specs["checksum"] = serde_json::Value::String(TEST_CHECKSUM.to_string());

            Arc::new(Self {
                payload: Mutex::new(
                    serde_json::to_vec(&specs).expect("evaluation snapshot should serialize"),
                ),
                metadata_fetches: AtomicUsize::new(0),
                initialization_thread: Mutex::new(None),
                category: Some("tenant"),
                trusted_source_url: None,
            })
        }

        fn replace_snapshot(&self, lcut: u64, checksum: &str, target_app: &str) {
            let mut payload = self.payload.lock();
            let mut specs: serde_json::Value =
                serde_json::from_slice(&payload).expect("evaluation snapshot should deserialize");
            specs["time"] = serde_json::Value::from(lcut);
            specs["checksum"] = serde_json::Value::String(checksum.to_string());
            specs["feature_gates"]["test_small_pass_gate"]["targetAppIDs"] =
                serde_json::json!([target_app]);
            *payload = serde_json::to_vec(&specs).expect("evaluation snapshot should serialize");
        }
    }

    #[async_trait]
    impl EvaluationDataTransport for TestDataTransport {
        fn observability_scope_class(&self) -> Option<&'static str> {
            self.category
        }

        fn trusted_hydration_source_url(&self) -> Option<&str> {
            self.trusted_source_url.as_deref()
        }

        async fn fetch_metadata(&self) -> Result<EvaluationDataVersion, StatsigErr> {
            self.metadata_fetches.fetch_add(1, Ordering::Relaxed);
            *self.initialization_thread.lock() = std::thread::current().name().map(str::to_owned);
            let payload = self.payload.lock();
            let specs: serde_json::Value =
                serde_json::from_slice(&payload).expect("evaluation snapshot should deserialize");
            Ok(EvaluationDataVersion::new(
                specs["time"]
                    .as_u64()
                    .expect("evaluation snapshot should have a valid cursor"),
                specs["checksum"]
                    .as_str()
                    .expect("evaluation snapshot should have a checksum")
                    .to_string(),
                (),
            ))
        }

        async fn fetch_payload(
            &self,
            _version: &EvaluationDataVersion,
            _fallback: bool,
        ) -> Result<ResponseData, StatsigErr> {
            Ok(ResponseData::from_bytes(self.payload.lock().clone()))
        }
    }

    #[derive(Default)]
    struct TestIdListsAdapter {
        memberships: Mutex<HashMap<String, HashSet<String>>>,
        listener: Mutex<Option<Arc<dyn IdListsUpdateListener>>>,
        starts: AtomicUsize,
        background_schedules: AtomicUsize,
        shutdowns: AtomicUsize,
        fail_start: AtomicBool,
        start_entered: Option<Arc<Notify>>,
        start_release: Option<Arc<Notify>>,
    }

    impl TestIdListsAdapter {
        fn containing(list_name: &str, user_id: &str) -> Arc<Self> {
            let lookup = HashUtil::new().sha256(user_id).chars().take(8).collect();
            Arc::new(Self {
                memberships: Mutex::new(HashMap::from([(
                    list_name.to_string(),
                    HashSet::from([lookup]),
                )])),
                ..Self::default()
            })
        }

        fn replace_memberships(&self, memberships: HashMap<String, HashSet<String>>) {
            *self.memberships.lock() = memberships;
            self.publish();
        }

        fn publish(&self) {
            let Some(listener) = self.listener.lock().clone() else {
                return;
            };
            let updates = self
                .memberships
                .lock()
                .iter()
                .map(|(name, ids)| {
                    let raw_changeset = ids
                        .iter()
                        .map(|id| format!("+{id}"))
                        .collect::<Vec<_>>()
                        .join("\n");
                    (
                        name.clone(),
                        IdListUpdate {
                            new_metadata: IdListMetadata {
                                name: name.clone(),
                                url: String::new(),
                                file_id: None,
                                size: raw_changeset.len() as u64,
                                creation_time: 0,
                            },
                            raw_changeset: Some(raw_changeset),
                        },
                    )
                })
                .collect();
            listener.did_receive_id_list_updates(updates);
        }
    }

    #[async_trait]
    impl IdListsAdapter for TestIdListsAdapter {
        async fn start(
            self: Arc<Self>,
            _runtime: &Arc<StatsigRuntime>,
            listener: Arc<dyn IdListsUpdateListener + Send + Sync>,
        ) -> Result<(), StatsigErr> {
            self.starts.fetch_add(1, Ordering::Relaxed);
            if let Some(entered) = self.start_entered.as_ref() {
                entered.notify_one();
            }
            if let Some(release) = self.start_release.as_ref() {
                release.notified().await;
            }
            if self.fail_start.load(Ordering::Relaxed) {
                return Err(StatsigErr::DataStoreFailure(
                    "ID-list manifest could not be initialized".to_string(),
                ));
            }
            *self.listener.lock() = Some(listener);
            self.publish();
            Ok(())
        }

        async fn shutdown(&self, _timeout: Duration) -> Result<(), StatsigErr> {
            self.shutdowns.fetch_add(1, Ordering::Relaxed);
            Ok(())
        }

        async fn schedule_background_sync(
            self: Arc<Self>,
            _runtime: &Arc<StatsigRuntime>,
        ) -> Result<(), StatsigErr> {
            self.background_schedules.fetch_add(1, Ordering::Relaxed);
            Ok(())
        }

        fn get_type_name(&self) -> String {
            "TestIdListsAdapter".to_string()
        }
    }

    #[derive(Clone, Debug, PartialEq)]
    struct RecordedMetric {
        name: String,
        tags: Option<HashMap<String, String>>,
    }

    #[derive(Default)]
    struct TestObservabilityClient {
        metrics: Mutex<Vec<RecordedMetric>>,
    }

    impl ObservabilityClient for TestObservabilityClient {
        fn init(&self) {}

        fn increment(&self, name: String, _value: f64, tags: Option<HashMap<String, String>>) {
            self.metrics.lock().push(RecordedMetric { name, tags });
        }

        fn gauge(&self, _name: String, _value: f64, _tags: Option<HashMap<String, String>>) {}

        fn dist(&self, name: String, _value: f64, tags: Option<HashMap<String, String>>) {
            self.metrics.lock().push(RecordedMetric { name, tags });
        }

        fn error(&self, _tag: String, _error: String) {}

        fn should_enable_high_cardinality_for_this_tag(&self, _tag: String) -> Option<bool> {
            Some(false)
        }

        fn to_ops_stats_event_observer(self: Arc<Self>) -> Arc<dyn OpsStatsEventObserver> {
            self
        }
    }

    #[test]
    fn evaluation_instance_identity_is_stable_and_never_reveals_host_identity() {
        let sensitive_identity = "sensitive-tenant/private-application/private-environment";
        let first = snapshot_instance_id(sensitive_identity);
        let second = snapshot_instance_id(sensitive_identity);
        let another = snapshot_instance_id("another-tenant");

        assert_eq!(first, second);
        assert_ne!(first, another);
        assert!(first.starts_with("scoped:"));
        assert!(!first.contains("sensitive-tenant"));
        assert!(!first.contains("private-application"));
        assert!(!first.contains("private-environment"));
    }

    #[test]
    fn host_owned_transport_explicitly_supplies_trusted_hydration_origin() {
        let default_transport = TestDataTransport::new(false);
        assert!(default_transport.trusted_hydration_source_url().is_none());

        let mut transport = TestDataTransport::new(false);
        Arc::get_mut(&mut transport)
            .expect("new test transport should be exclusively owned")
            .trusted_source_url =
            Some("https://trusted.example/v2/download_config_specs".to_string());
        let source = EvaluationDataSource {
            transport: transport as Arc<dyn EvaluationDataTransport>,
        };

        assert_eq!(
            crate::specs_adapter::ScopedConfigSource::trusted_hydration_source_url(&source),
            Some("https://trusted.example/v2/download_config_specs")
        );
    }

    #[tokio::test]
    #[serial]
    async fn id_list_server_reports_request_outcomes_and_latency_to_host_observers() {
        let mut server = mockito::Server::new_async().await;
        let member_lookup: String = HashUtil::new()
            .sha256("observed-member")
            .chars()
            .take(8)
            .collect();
        let failed_lookup: String = HashUtil::new()
            .sha256("observed-failure")
            .chars()
            .take(8)
            .collect();
        let success = server
            .mock("POST", "/get_id_list_results")
            .match_body(mockito::Matcher::Json(serde_json::json!({
                "companyID": "observed-tenant",
                "mapping": { "tenant_members": member_lookup }
            })))
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(
                serde_json::json!({
                    "result": [format!("tenant_members|{member_lookup}")]
                })
                .to_string(),
            )
            .expect(1)
            .create_async()
            .await;
        let failure = server
            .mock("POST", "/get_id_list_results")
            .match_body(mockito::Matcher::Json(serde_json::json!({
                "companyID": "observed-tenant",
                "mapping": { "tenant_members": failed_lookup }
            })))
            .with_status(503)
            .expect(1)
            .create_async()
            .await;
        let observer = Arc::new(TestObservabilityClient::default());
        let client = EvaluationClient::new_with_id_list_server(
            Handle::current(),
            Some(Arc::clone(&observer) as Arc<dyn ObservabilityClient>),
            Some(server.url()),
        )
        .expect("an observed membership service should initialize");
        let instance = client
            .create_instance(
                "client-observed",
                "observed-tenant",
                "observed-host",
                TestDataTransport::new(true),
                None,
                None,
            )
            .await
            .expect("the observed tenant snapshot should initialize");

        for (user, expected) in [
            ("observed-member", true),
            ("observed-member", true),
            ("observed-failure", false),
        ] {
            let result = client
                .evaluate(
                    Arc::clone(&instance),
                    StatsigUser::with_user_id(user),
                    None,
                    EvaluationOperation::Gate("test_small_pass_gate"),
                )
                .await
                .expect("membership failures should preserve production fallback");
            let EvaluationResult::Gate(gate) = result else {
                panic!("membership-backed gates should evaluate");
            };
            assert_eq!(
                gate.evaluation.map(|evaluation| evaluation.value),
                Some(expected)
            );
        }

        tokio::time::timeout(Duration::from_secs(2), async {
            loop {
                {
                    let metrics = observer.metrics.lock();
                    let observed = |name: &str, result: &str| {
                        metrics.iter().any(|metric| {
                            metric.name == name
                                && metric
                                    .tags
                                    .as_ref()
                                    .and_then(|tags| tags.get("result"))
                                    .map(String::as_str)
                                    == Some(result)
                        })
                    };
                    if observed(
                        "statsig.sdk.id_list_results.request.count",
                        "cache_miss_success",
                    ) && observed("statsig.sdk.id_list_results.request.count", "cache_hit")
                        && observed(
                            "statsig.sdk.id_list_results.request.count",
                            "cache_miss_failure",
                        )
                        && observed("statsig.sdk.id_list_results.fetch.count", "success")
                        && observed("statsig.sdk.id_list_results.fetch.count", "bad_status")
                        && observed("statsig.sdk.id_list_results.fetch.latency_ms", "success")
                        && observed("statsig.sdk.id_list_results.fetch.latency_ms", "bad_status")
                    {
                        for sensitive in [
                            "observed-tenant",
                            "observed-member",
                            "observed-failure",
                            "tenant_members",
                        ] {
                            assert!(metrics.iter().all(|metric| {
                                !metric.name.contains(sensitive)
                                    && metric.tags.as_ref().is_none_or(|tags| {
                                        tags.iter().all(|(name, value)| {
                                            !name.contains(sensitive) && !value.contains(sensitive)
                                        })
                                    })
                            }));
                        }
                        return;
                    }
                }
                tokio::task::yield_now().await;
            }
        })
        .await
        .expect("host observers should receive successful, failed, cached, and latency metrics");

        success.assert_async().await;
        failure.assert_async().await;
        instance.shutdown().await.unwrap();
        client.shutdown().await;
    }

    #[tokio::test]
    #[serial]
    async fn id_list_server_memberships_remain_request_and_tenant_scoped() {
        let mut server = mockito::Server::new_async().await;
        let member_lookup: String = HashUtil::new()
            .sha256("server-member")
            .chars()
            .take(8)
            .collect();
        let shared_lookup: String = HashUtil::new()
            .sha256("shared-member")
            .chars()
            .take(8)
            .collect();
        let authorized = server
            .mock("POST", "/get_id_list_results")
            .match_body(mockito::Matcher::Json(serde_json::json!({
                "companyID": "authorized-tenant",
                "mapping": { "tenant_members": member_lookup }
            })))
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(
                serde_json::json!({
                    "result": [format!("tenant_members|{member_lookup}")]
                })
                .to_string(),
            )
            .expect(1)
            .create_async()
            .await;
        let shared_only = server
            .mock("POST", "/get_id_list_results")
            .match_body(mockito::Matcher::Json(serde_json::json!({
                "companyID": "authorized-tenant",
                "mapping": { "tenant_members": shared_lookup }
            })))
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(r#"{"result":[]}"#)
            .expect(1)
            .create_async()
            .await;
        let foreign = server
            .mock("POST", "/get_id_list_results")
            .match_body(mockito::Matcher::Json(serde_json::json!({
                "companyID": "other-tenant",
                "mapping": { "tenant_members": member_lookup }
            })))
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(r#"{"result":[]}"#)
            .expect(1)
            .create_async()
            .await;

        let client =
            EvaluationClient::new_with_id_list_server(Handle::current(), None, Some(server.url()))
                .expect("a trusted membership server should initialize");
        let shared_adapter = TestIdListsAdapter::containing("tenant_members", "shared-member");
        let shared = client
            .preload_shared_id_lists_with_adapter(
                "secret-shared-owner",
                "authorized-tenant",
                &StatsigOptions::default(),
                Arc::clone(&shared_adapter) as Arc<dyn IdListsAdapter>,
            )
            .await
            .unwrap();
        let instance = client
            .create_instance_with_shared_id_lists(
                "client-authorized",
                "authorized-tenant",
                "authorized-host",
                TestDataTransport::new(true),
                None,
                None,
                Some(Arc::clone(&shared)),
            )
            .await
            .unwrap();

        for (user, expected) in [("server-member", true), ("shared-member", false)] {
            let result = client
                .evaluate(
                    Arc::clone(&instance),
                    StatsigUser::with_user_id(user),
                    None,
                    EvaluationOperation::Gate("test_small_pass_gate"),
                )
                .await
                .unwrap();
            let EvaluationResult::Gate(gate) = result else {
                panic!("a membership-backed gate should evaluate");
            };
            assert_eq!(gate.evaluation.map(|value| value.value), Some(expected));
        }
        let snapshot = instance.engine.snapshot_evaluation_data();
        assert!(
            snapshot.id_lists["tenant_members"]
                .ids
                .contains(&shared_lookup)
        );
        assert!(
            !snapshot.id_lists["tenant_members"]
                .ids
                .contains(&member_lookup)
        );
        assert_eq!(shared_adapter.starts.load(Ordering::Relaxed), 1);

        let failing_adapter = Arc::new(TestIdListsAdapter {
            fail_start: AtomicBool::new(true),
            ..TestIdListsAdapter::default()
        });
        let other_instance = client
            .create_instance(
                "client-other",
                "other-tenant",
                "other-host",
                TestDataTransport::new(true),
                None,
                Some(Arc::clone(&failing_adapter) as Arc<dyn IdListsAdapter>),
            )
            .await
            .unwrap();
        let result = client
            .evaluate(
                Arc::clone(&other_instance),
                StatsigUser::with_user_id("server-member"),
                None,
                EvaluationOperation::Gate("test_small_pass_gate"),
            )
            .await
            .unwrap();
        let EvaluationResult::Gate(gate) = result else {
            panic!("another tenant should receive its own membership result");
        };
        assert_eq!(gate.evaluation.map(|value| value.value), Some(false));
        assert_eq!(failing_adapter.starts.load(Ordering::Relaxed), 0);
        assert!(
            other_instance
                .engine
                .snapshot_evaluation_data()
                .id_lists
                .is_empty()
        );

        authorized.assert_async().await;
        shared_only.assert_async().await;
        foreign.assert_async().await;
        instance.shutdown().await.unwrap();
        other_instance.shutdown().await.unwrap();
        client.shutdown().await;
    }

    #[tokio::test]
    #[serial]
    async fn id_list_server_preserves_custom_units_operators_and_denied_capabilities() {
        let mut server = mockito::Server::new_async().await;
        let member_lookup: String = HashUtil::new()
            .sha256("member-company")
            .chars()
            .take(8)
            .collect();
        let outsider_lookup: String = HashUtil::new()
            .sha256("outsider-company")
            .chars()
            .take(8)
            .collect();
        let member = server
            .mock("POST", "/get_id_list_results")
            .match_body(mockito::Matcher::Json(serde_json::json!({
                "companyID": "authenticated-tenant",
                "mapping": {
                    "tenant_members": member_lookup,
                    "company_id_list": member_lookup
                }
            })))
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(
                serde_json::json!({
                    "result": [format!("tenant_members|{member_lookup}")]
                })
                .to_string(),
            )
            .expect(1)
            .create_async()
            .await;
        let outsider = server
            .mock("POST", "/get_id_list_results")
            .match_body(mockito::Matcher::Json(serde_json::json!({
                "companyID": "authenticated-tenant",
                "mapping": {
                    "tenant_members": outsider_lookup,
                    "company_id_list": outsider_lookup
                }
            })))
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(r#"{"result":[]}"#)
            .expect(1)
            .create_async()
            .await;
        let client =
            EvaluationClient::new_with_id_list_server(Handle::current(), None, Some(server.url()))
                .unwrap();

        for (operator, expected_member, expected_outsider) in [
            ("in_segment_list", true, false),
            ("not_in_segment_list", false, true),
        ] {
            let source = TestDataTransport::new(true);
            {
                let mut payload = source.payload.lock();
                let mut specs: serde_json::Value = serde_json::from_slice(&payload).unwrap();
                specs["condition_map"]["tenant-id-list"]["operator"] = serde_json::json!(operator);
                specs["condition_map"]["tenant-id-list"]["idType"] = serde_json::json!("companyID");
                *payload = serde_json::to_vec(&specs).unwrap();
            }
            let adapter = Arc::new(TestIdListsAdapter {
                fail_start: AtomicBool::new(true),
                ..TestIdListsAdapter::default()
            });
            let instance = client
                .create_instance(
                    "client-custom",
                    "authenticated-tenant",
                    &format!("custom-host-{operator}"),
                    source,
                    None,
                    Some(Arc::clone(&adapter) as Arc<dyn IdListsAdapter>),
                )
                .await
                .unwrap();

            let mut denied_user = StatsigUser::with_user_id("unrelated-primary-user");
            denied_user.set_custom_ids(HashMap::from([("companyID", "member-company")]));
            let denied = client
                .prepare_evaluation_with_id_list_access(
                    Arc::clone(&instance),
                    denied_user,
                    None,
                    false,
                )
                .unwrap()
                .evaluate(EvaluationOperation::Gate("test_small_pass_gate"))
                .await;
            assert!(matches!(denied, Err(StatsigErr::InvalidOperation(_))));

            for (unit, expected) in [
                ("member-company", expected_member),
                ("outsider-company", expected_outsider),
            ] {
                let mut user = StatsigUser::with_user_id("unrelated-primary-user");
                user.set_custom_ids(HashMap::from([("companyID", unit)]));
                let result = client
                    .evaluate(
                        Arc::clone(&instance),
                        user,
                        None,
                        EvaluationOperation::Gate("test_small_pass_gate"),
                    )
                    .await
                    .unwrap();
                let EvaluationResult::Gate(gate) = result else {
                    panic!("a custom-unit membership gate should evaluate");
                };
                assert_eq!(
                    gate.evaluation.map(|value| value.value),
                    Some(expected),
                    "unexpected membership for {operator} and {unit}"
                );
            }
            assert_eq!(adapter.starts.load(Ordering::Relaxed), 0);
            instance.shutdown().await.unwrap();
        }

        member.assert_async().await;
        outsider.assert_async().await;
        client.shutdown().await;
    }

    #[tokio::test]
    #[serial]
    async fn shared_id_lists_preload_the_standard_adapter_once_for_multiple_scopes() {
        let mut server = mockito::Server::new_async().await;
        let lists = [
            ("tenant_members", "shared-member"),
            ("android_members", "android-member"),
            ("ios_members", "ios-member"),
        ];
        let mut manifest = serde_json::Map::new();
        let mut blob_requests = Vec::new();
        for (name, member) in lists {
            let lookup: String = HashUtil::new().sha256(member).chars().take(8).collect();
            let changeset = format!("+{lookup}\n");
            manifest.insert(
                name.to_string(),
                serde_json::json!({
                    "name": name,
                    "url": format!("{}/id_lists/{name}", server.url()),
                    "fileID": format!("{name}-file"),
                    "size": changeset.len(),
                    "creationTime": 1
                }),
            );
            blob_requests.push(
                server
                    .mock("GET", format!("/id_lists/{name}").as_str())
                    .match_header("statsig-api-key", "secret-shared-owner")
                    .with_status(200)
                    .with_body(changeset)
                    .expect(1)
                    .create_async()
                    .await,
            );
        }
        let manifest_request = server
            .mock("POST", "/get_id_lists")
            .match_header("statsig-api-key", "secret-shared-owner")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(serde_json::Value::Object(manifest).to_string())
            .expect(1)
            .create_async()
            .await;
        let client = EvaluationClient::new(Handle::current(), None).unwrap();
        let options = StatsigOptions {
            id_lists_url: Some(format!("{}/get_id_lists", server.url())),
            fallback_to_statsig_api: Some(false),
            disable_disk_access: Some(true),
            ..StatsigOptions::default()
        };
        let shared = client
            .preload_shared_id_lists("secret-shared-owner", "shared-tenant", &options)
            .await
            .expect("the standard adapter should preload every list in its authorized manifest");
        manifest_request.assert_async().await;
        for request in &blob_requests {
            request.assert_async().await;
        }
        let repeated = client
            .preload_shared_id_lists("secret-shared-owner", "shared-tenant", &options)
            .await
            .expect("the same authenticated credential must reuse its preloaded owner");
        assert!(Arc::ptr_eq(&shared, &repeated));

        let mut instances = Vec::new();
        for (app, list_name, member) in [
            ("android", "android_members", "android-member"),
            ("ios", "ios_members", "ios-member"),
        ] {
            let source = TestDataTransport::new(true);
            {
                let mut payload = source.payload.lock();
                let mut specs: serde_json::Value = serde_json::from_slice(&payload).unwrap();
                specs["condition_map"]["tenant-id-list"]["targetValue"] =
                    serde_json::json!(list_name);
                *payload = serde_json::to_vec(&specs).unwrap();
            }
            let instance = client
                .create_instance_with_shared_id_lists(
                    &format!("client-{app}"),
                    "shared-tenant",
                    &format!("shared-{app}"),
                    source,
                    None,
                    None,
                    Some(Arc::clone(&shared)),
                )
                .await
                .expect("each tenant-bound application should attach the shared owner");
            let result = client
                .evaluate(
                    Arc::clone(&instance),
                    StatsigUser::with_user_id(member),
                    None,
                    EvaluationOperation::Gate("test_small_pass_gate"),
                )
                .await
                .expect("the preloaded member should evaluate without another download");
            let EvaluationResult::Gate(gate) = result else {
                panic!("the shared list should evaluate the requested gate");
            };
            assert_eq!(
                gate.evaluation.map(|evaluation| evaluation.value),
                Some(true)
            );
            instances.push(instance);
        }

        let first = instances[0].engine.snapshot_evaluation_data();
        let second = instances[1].engine.snapshot_evaluation_data();
        let owner = shared.spec_store.load_data();
        assert_eq!(owner.id_lists.len(), lists.len());
        assert!(Arc::ptr_eq(&first.id_lists, &second.id_lists));
        assert!(Arc::ptr_eq(&first.id_lists, &owner.id_lists));
        for (name, member) in lists {
            let lookup: String = HashUtil::new().sha256(member).chars().take(8).collect();
            assert!(owner.id_lists[name].ids.contains(&lookup));
            assert!(Arc::ptr_eq(
                &first.id_lists[name].ids,
                &second.id_lists[name].ids
            ));
        }
        manifest_request.assert_async().await;
        for request in &blob_requests {
            request.assert_async().await;
        }

        for instance in instances {
            instance.shutdown().await.unwrap();
        }
        client.shutdown().await;
    }

    #[tokio::test]
    #[serial]
    async fn shared_id_list_refresh_preserves_pinned_snapshots_and_client_ownership() {
        let adapter = TestIdListsAdapter::containing("tenant_members", "original-member");
        let client = EvaluationClient::new(Handle::current(), None).unwrap();
        let shared = client
            .preload_shared_id_lists_with_adapter(
                "secret-shared-refresh",
                "shared-tenant",
                &StatsigOptions::default(),
                Arc::clone(&adapter) as Arc<dyn IdListsAdapter>,
            )
            .await
            .unwrap();
        assert_eq!(adapter.starts.load(Ordering::Relaxed), 1);
        assert_eq!(adapter.background_schedules.load(Ordering::Relaxed), 1);

        let first = client
            .create_instance_with_shared_id_lists(
                "client-first",
                "shared-tenant",
                "first-app",
                TestDataTransport::new(true),
                None,
                None,
                Some(Arc::clone(&shared)),
            )
            .await
            .unwrap();
        let second = client
            .create_instance_with_shared_id_lists(
                "client-second",
                "shared-tenant",
                "second-app",
                TestDataTransport::new(true),
                None,
                None,
                Some(Arc::clone(&shared)),
            )
            .await
            .unwrap();
        let pinned = client
            .prepare_evaluation(
                Arc::clone(&first),
                StatsigUser::with_user_id("refreshed-member"),
                None,
            )
            .unwrap();
        let original_snapshot = first.engine.snapshot_evaluation_data();
        let refreshed_lookup = HashUtil::new()
            .sha256("refreshed-member")
            .chars()
            .take(8)
            .collect();
        adapter.replace_memberships(HashMap::from([(
            "tenant_members".to_string(),
            HashSet::from([refreshed_lookup]),
        )]));

        let old = pinned
            .evaluate(EvaluationOperation::Gate("test_small_pass_gate"))
            .await
            .unwrap();
        let EvaluationResult::Gate(old) = old else {
            panic!("the previously pinned request should evaluate its original snapshot");
        };
        assert_eq!(
            old.evaluation.map(|evaluation| evaluation.value),
            Some(false)
        );

        for instance in [&first, &second] {
            let refreshed = client
                .evaluate(
                    Arc::clone(instance),
                    StatsigUser::with_user_id("refreshed-member"),
                    None,
                    EvaluationOperation::Gate("test_small_pass_gate"),
                )
                .await
                .unwrap();
            let EvaluationResult::Gate(refreshed) = refreshed else {
                panic!("new requests should evaluate the refreshed shared list");
            };
            assert_eq!(
                refreshed.evaluation.map(|evaluation| evaluation.value),
                Some(true)
            );
        }
        let first_refreshed = first.engine.snapshot_evaluation_data();
        let second_refreshed = second.engine.snapshot_evaluation_data();
        assert!(!Arc::ptr_eq(
            &original_snapshot.id_lists,
            &first_refreshed.id_lists
        ));
        assert!(Arc::ptr_eq(
            &first_refreshed.id_lists,
            &second_refreshed.id_lists
        ));

        first.shutdown().await.unwrap();
        assert_eq!(adapter.shutdowns.load(Ordering::Relaxed), 0);
        second.shutdown().await.unwrap();
        assert_eq!(adapter.shutdowns.load(Ordering::Relaxed), 0);
        client.shutdown().await;
        client.shutdown().await;
        assert_eq!(adapter.shutdowns.load(Ordering::Relaxed), 1);
    }

    #[tokio::test]
    #[serial]
    async fn shared_id_lists_fail_closed_across_tenants_clients_and_initialization_errors() {
        let client = EvaluationClient::new(Handle::current(), None).unwrap();
        let failing = Arc::new(TestIdListsAdapter {
            fail_start: AtomicBool::new(true),
            ..TestIdListsAdapter::default()
        });
        let result = client
            .preload_shared_id_lists_with_adapter(
                "secret-shared-boundary",
                "authorized-tenant",
                &StatsigOptions::default(),
                Arc::clone(&failing) as Arc<dyn IdListsAdapter>,
            )
            .await;
        assert!(matches!(result, Err(StatsigErr::DataStoreFailure(_))));
        assert_eq!(failing.background_schedules.load(Ordering::Relaxed), 0);
        assert_eq!(failing.shutdowns.load(Ordering::Relaxed), 1);

        let adapter = TestIdListsAdapter::containing("tenant_members", "authorized-member");
        let shared = client
            .preload_shared_id_lists_with_adapter(
                "secret-shared-boundary",
                "authorized-tenant",
                &StatsigOptions::default(),
                Arc::clone(&adapter) as Arc<dyn IdListsAdapter>,
            )
            .await
            .expect("a failed preload must not prevent a later valid retry");
        let same_credential_other_tenant = client
            .preload_shared_id_lists_with_adapter(
                "secret-shared-boundary",
                "different-tenant",
                &StatsigOptions::default(),
                Arc::clone(&failing) as Arc<dyn IdListsAdapter>,
            )
            .await;
        assert!(matches!(
            same_credential_other_tenant,
            Err(StatsigErr::InvalidOperation(_))
        ));
        assert_eq!(failing.starts.load(Ordering::Relaxed), 1);

        let authorized_instance = client
            .create_instance_with_shared_id_lists(
                "client-authorized",
                "authorized-tenant",
                "authorized-host",
                TestDataTransport::new(true),
                None,
                None,
                Some(Arc::clone(&shared)),
            )
            .await
            .unwrap();
        assert!(
            authorized_instance
                .engine
                .snapshot_evaluation_data()
                .id_lists
                .contains_key("tenant_members")
        );
        let denied = client
            .prepare_evaluation_with_id_list_access(
                Arc::clone(&authorized_instance),
                StatsigUser::with_user_id("authorized-member"),
                None,
                false,
            )
            .unwrap()
            .evaluate(EvaluationOperation::Gate("test_small_pass_gate"))
            .await;
        assert!(matches!(denied, Err(StatsigErr::InvalidOperation(_))));

        for (tenant, direct_adapter) in [
            ("different-tenant", None),
            (
                "authorized-tenant",
                Some(Arc::clone(&adapter) as Arc<dyn IdListsAdapter>),
            ),
        ] {
            let result = client
                .create_instance_with_shared_id_lists(
                    "client-unauthorized",
                    tenant,
                    "unauthorized-host",
                    TestDataTransport::new(true),
                    None,
                    direct_adapter,
                    Some(Arc::clone(&shared)),
                )
                .await;
            assert!(matches!(result, Err(StatsigErr::InvalidOperation(_))));
        }

        let other_client = EvaluationClient::new(Handle::current(), None).unwrap();
        let foreign_owner = other_client
            .create_instance_with_shared_id_lists(
                "client-foreign",
                "authorized-tenant",
                "foreign-host",
                TestDataTransport::new(true),
                None,
                None,
                Some(shared),
            )
            .await;
        assert!(matches!(
            foreign_owner,
            Err(StatsigErr::InvalidOperation(_))
        ));

        authorized_instance.shutdown().await.unwrap();
        other_client.shutdown().await;
        client.shutdown().await;
        assert_eq!(adapter.shutdowns.load(Ordering::Relaxed), 1);
    }

    #[tokio::test]
    #[serial]
    async fn config_only_clients_use_the_standard_id_list_downloader() {
        let mut server = mockito::Server::new_async().await;
        let manifest = include_str!("../tests/data/get_id_lists.json")
            .replace("URL_REPLACE", &format!("{}/id_lists", server.url()));
        let approved_manifest_request = server
            .mock("POST", "/get_id_lists")
            .match_header("statsig-api-key", "secret-approved-tenant")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(manifest)
            .expect(4)
            .create_async()
            .await;
        let denied_manifest_request = server
            .mock("POST", "/get_id_lists")
            .match_header("statsig-api-key", "secret-denied-tenant")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body("{}")
            .expect(4)
            .create_async()
            .await;
        let list_request = server
            .mock("GET", "/id_lists/company_id_list")
            .match_header("statsig-api-key", "secret-approved-tenant")
            .with_status(200)
            .with_body(include_str!("../tests/data/company_id_list"))
            .expect(4)
            .create_async()
            .await;
        let observer = Arc::new(TestObservabilityClient::default());
        let client = EvaluationClient::new(
            Handle::current(),
            Some(Arc::clone(&observer) as Arc<dyn ObservabilityClient>),
        )
        .unwrap();
        let shared_instance_id = client.id_lists_sdk_instance_id().to_string();
        assert!(OPS_STATS.has_instance_for_test(&shared_instance_id));
        assert!(!shared_instance_id.contains("secret"));
        tokio::task::yield_now().await;
        for (operator, id_type, approved_member, approved_nonmember, denied_member) in [
            ("in_segment_list", "userID", true, false, false),
            ("not_in_segment_list", "userID", false, true, true),
            ("in_segment_list", "companyID", true, false, false),
            ("not_in_segment_list", "companyID", false, true, true),
        ] {
            let source = TestDataTransport::new(true);
            {
                let mut payload = source.payload.lock();
                let mut specs: serde_json::Value = serde_json::from_slice(&payload).unwrap();
                specs["condition_map"]["tenant-id-list"]["targetValue"] =
                    serde_json::json!("company_id_list");
                specs["condition_map"]["tenant-id-list"]["operator"] = serde_json::json!(operator);
                specs["condition_map"]["tenant-id-list"]["idType"] = serde_json::json!(id_type);
                *payload = serde_json::to_vec(&specs).unwrap();
            }
            let approved_identity = format!("approved-host-{operator}-{id_type}");
            let approved_options = StatsigOptions {
                sdk_instance_id: Some(client.id_lists_sdk_instance_id().to_string()),
                id_lists_url: Some(format!("{}/get_id_lists", server.url())),
                ..StatsigOptions::default()
            };
            let approved = client
                .create_instance(
                    "client-scoped-approved",
                    "approved-tenant",
                    &approved_identity,
                    Arc::clone(&source) as Arc<dyn EvaluationDataTransport>,
                    None,
                    Some(Arc::new(StatsigHttpIdListsAdapter::new(
                        "secret-approved-tenant",
                        &approved_options,
                    ))),
                )
                .await
                .expect("the existing SDK ID-list downloader should initialize");
            let denied_identity = format!("denied-host-{operator}-{id_type}");
            let denied_options = StatsigOptions {
                sdk_instance_id: Some(client.id_lists_sdk_instance_id().to_string()),
                id_lists_url: Some(format!("{}/get_id_lists", server.url())),
                ..StatsigOptions::default()
            };
            let denied = client
                .create_instance(
                    "client-scoped-denied",
                    "denied-tenant",
                    &denied_identity,
                    source,
                    None,
                    Some(Arc::new(StatsigHttpIdListsAdapter::new(
                        "secret-denied-tenant",
                        &denied_options,
                    ))),
                )
                .await
                .expect("the denied tenant's empty SDK ID-list manifest should initialize");

            for (instance, user_id, expected) in [
                (Arc::clone(&approved), "Marcos", approved_member),
                (Arc::clone(&approved), "not-in-the-list", approved_nonmember),
                (Arc::clone(&denied), "Marcos", denied_member),
            ] {
                let mut user = StatsigUser::with_user_id(if id_type == "userID" {
                    user_id
                } else {
                    "unrelated-primary-user"
                });
                if id_type != "userID" {
                    user.set_custom_ids(HashMap::from([(id_type, user_id)]));
                }
                let EvaluationResult::Gate(result) = client
                    .evaluate(
                        instance,
                        user,
                        None,
                        EvaluationOperation::Gate("test_small_pass_gate"),
                    )
                    .await
                    .expect("standard SDK ID-list membership should evaluate")
                else {
                    panic!("gate operation should return its evaluated result");
                };
                assert_eq!(
                    result.evaluation.map(|evaluation| evaluation.value),
                    Some(expected),
                    "unexpected SDK-owned membership for {operator}, {id_type}, and {user_id}"
                );
            }

            tokio::time::timeout(Duration::from_secs(2), async {
                while !observer
                    .metrics
                    .lock()
                    .iter()
                    .any(|metric| metric.name == "statsig.sdk.id_list_manifest_download_success")
                {
                    tokio::task::yield_now().await;
                }
            })
            .await
            .expect("the existing SDK ID-list adapter should deliver its canonical metrics");

            approved.shutdown().await.unwrap();
            denied.shutdown().await.unwrap();
            assert!(
                OPS_STATS.has_instance_for_test(&shared_instance_id),
                "the client must retain its shared observer across scoped adapter eviction"
            );
        }

        approved_manifest_request.assert_async().await;
        denied_manifest_request.assert_async().await;
        list_request.assert_async().await;
        {
            let metrics = observer.metrics.lock();
            assert!(
                metrics.iter().any(|metric| {
                    metric.name == "statsig.sdk.id_list_manifest_download_success"
                })
            );
            for sensitive in [
                "approved-tenant",
                "denied-tenant",
                "secret-approved-tenant",
                "secret-denied-tenant",
            ] {
                assert!(metrics.iter().all(|metric| {
                    !metric.name.contains(sensitive)
                        && metric.tags.as_ref().is_none_or(|tags| {
                            tags.iter().all(|(name, value)| {
                                !name.contains(sensitive) && !value.contains(sensitive)
                            })
                        })
                }));
            }
        }
        client.shutdown().await;
    }

    #[tokio::test]
    #[serial]
    async fn fixture_seeds_membership_into_the_standard_sdk_id_list_store() {
        let source = TestDataTransport::new(true);
        let specs: SpecsResponseFull = serde_json::from_slice(&source.payload.lock())
            .expect("evaluation fixture should deserialize");
        let fixture_member = "fixture-member";
        let hashed_member = HashUtil::new()
            .sha256(fixture_member)
            .chars()
            .take(8)
            .collect();
        let fixture = EvaluationFixtureClient::from_specs_with_id_lists_for_test(
            specs,
            HashMap::from([("tenant_members".to_string(), HashSet::from([hashed_member]))]),
        );

        for (user_id, expected) in [(fixture_member, true), ("fixture-nonmember", false)] {
            let EvaluationResult::Gate(result) = fixture
                .evaluate(
                    "fixture-tenant",
                    StatsigUser::with_user_id(user_id),
                    None,
                    EvaluationOperation::Gate("test_small_pass_gate"),
                )
                .await
                .expect("seeded fixture membership should evaluate")
            else {
                panic!("fixture gate operation should return its evaluated result");
            };
            assert_eq!(
                result.evaluation.map(|evaluation| evaluation.value),
                Some(expected)
            );
        }
    }

    #[tokio::test]
    #[serial]
    async fn evaluation_instances_keep_tenant_id_lists_and_adapter_lifecycles_separate() {
        let allowed_adapter = TestIdListsAdapter::containing("tenant_members", "same-user");
        let denied_adapter = Arc::new(TestIdListsAdapter::default());
        let observer = Arc::new(TestObservabilityClient::default());
        let client = EvaluationClient::new(
            Handle::current(),
            Some(Arc::clone(&observer) as Arc<dyn ObservabilityClient>),
        )
        .expect("evaluation client should initialize");
        let allowed_source = TestDataTransport::new(true);
        let denied_source = TestDataTransport::new(true);
        let allowed = client
            .create_instance(
                "client-allowed",
                "allowed-tenant",
                "allowed-host-identity",
                Arc::clone(&allowed_source) as Arc<dyn EvaluationDataTransport>,
                None,
                Some(Arc::clone(&allowed_adapter) as Arc<dyn IdListsAdapter>),
            )
            .await
            .expect("allowed tenant instance should initialize");
        let denied = client
            .create_instance(
                "client-denied",
                "denied-tenant",
                "denied-host-identity",
                Arc::clone(&denied_source) as Arc<dyn EvaluationDataTransport>,
                None,
                Some(Arc::clone(&denied_adapter) as Arc<dyn IdListsAdapter>),
            )
            .await
            .expect("denied tenant instance should initialize");

        assert!(!Arc::ptr_eq(
            &allowed.engine.runtime,
            &denied.engine.runtime
        ));
        assert!(!OPS_STATS.has_instance_for_test(&snapshot_instance_id("allowed-host-identity")));
        assert!(!OPS_STATS.has_instance_for_test(&snapshot_instance_id("denied-host-identity")));
        assert_eq!(allowed_adapter.starts.load(Ordering::Relaxed), 0);
        assert_eq!(denied_adapter.starts.load(Ordering::Relaxed), 0);

        for (instance, expected) in [
            (Arc::clone(&allowed), true),
            (Arc::clone(&allowed), true),
            (Arc::clone(&denied), false),
        ] {
            let result = client
                .evaluate(
                    instance,
                    StatsigUser::with_user_id("same-user"),
                    None,
                    EvaluationOperation::Gate("test_small_pass_gate"),
                )
                .await
                .expect("tenant-bound evaluation should succeed");
            let EvaluationResult::Gate(result) = result else {
                panic!("gate operation should return its evaluated result");
            };
            assert_eq!(
                result.evaluation.map(|evaluation| evaluation.value),
                Some(expected)
            );
        }

        assert_eq!(allowed_adapter.starts.load(Ordering::Relaxed), 1);
        assert_eq!(
            allowed_adapter.background_schedules.load(Ordering::Relaxed),
            1
        );
        assert_eq!(denied_adapter.starts.load(Ordering::Relaxed), 1);
        assert_eq!(
            denied_adapter.background_schedules.load(Ordering::Relaxed),
            1
        );
        assert!(
            allowed
                .engine
                .snapshot_evaluation_data()
                .id_lists
                .contains_key("tenant_members")
        );
        assert!(denied.engine.snapshot_evaluation_data().id_lists.is_empty());
        assert_eq!(allowed_source.metadata_fetches.load(Ordering::Relaxed), 1);
        assert_eq!(denied_source.metadata_fetches.load(Ordering::Relaxed), 1);

        {
            let metrics = observer.metrics.lock();
            assert!(metrics.iter().any(|metric| {
                metric.name == "statsig.sdk.evaluation.snapshot.fetch.count"
                    && metric
                        .tags
                        .as_ref()
                        .and_then(|tags| tags.get("scope_class"))
                        .map(String::as_str)
                        == Some("tenant")
            }));
            assert!(metrics.iter().all(|metric| {
                !metric.name.contains("allowed-tenant")
                    && !metric.name.contains("denied-tenant")
                    && metric.tags.as_ref().is_none_or(|tags| {
                        tags.values()
                            .all(|value| value != "allowed-tenant" && value != "denied-tenant")
                    })
            }));
        }

        allowed.shutdown().await.unwrap();
        assert_eq!(allowed_adapter.shutdowns.load(Ordering::Relaxed), 1);
        assert_eq!(denied_adapter.shutdowns.load(Ordering::Relaxed), 0);
        let remaining = client
            .evaluate(
                Arc::clone(&denied),
                StatsigUser::with_user_id("same-user"),
                None,
                EvaluationOperation::Gate("test_small_pass_gate"),
            )
            .await
            .expect("shutting down one engine must not affect another tenant");
        let EvaluationResult::Gate(remaining) = remaining else {
            panic!("remaining tenant should still evaluate its requested gate");
        };
        assert_eq!(
            remaining.evaluation.map(|evaluation| evaluation.value),
            Some(false)
        );
        denied.shutdown().await.unwrap();
        assert_eq!(denied_adapter.shutdowns.load(Ordering::Relaxed), 1);
        client.shutdown().await;
    }

    #[tokio::test]
    #[serial]
    async fn capability_bound_requests_cannot_read_hydrated_id_lists() {
        let client = EvaluationClient::new(Handle::current(), None)
            .expect("evaluation client should initialize");

        for (operator, authorized_membership) in
            [("in_segment_list", true), ("not_in_segment_list", false)]
        {
            let adapter = TestIdListsAdapter::containing("tenant_members", "authorized-user");
            let source = TestDataTransport::new(true);
            {
                let mut payload = source.payload.lock();
                let mut specs: serde_json::Value = serde_json::from_slice(&payload)
                    .expect("evaluation snapshot should deserialize");
                specs["condition_map"]["tenant-id-list"]["operator"] =
                    serde_json::Value::String(operator.to_string());
                let mut unrelated = specs["feature_gates"]["test_small_pass_gate"].clone();
                unrelated["rules"][0]["conditions"] = serde_json::json!([]);
                specs["feature_gates"]["unrelated_gate"] = unrelated;
                *payload =
                    serde_json::to_vec(&specs).expect("evaluation snapshot should serialize");
            }

            let instance = client
                .create_instance(
                    "client-capability",
                    "capability-tenant",
                    &format!("capability-{operator}"),
                    source,
                    None,
                    Some(Arc::clone(&adapter) as Arc<dyn IdListsAdapter>),
                )
                .await
                .expect("configuration should initialize before ID-list authorization");

            let denied = client
                .prepare_evaluation_with_id_list_access(
                    Arc::clone(&instance),
                    StatsigUser::with_user_id("authorized-user"),
                    None,
                    false,
                )
                .expect("restricted requests should retain their configuration snapshot");
            assert!(denied.requires_id_lists(&EvaluationOperation::Gate("test_small_pass_gate")));
            assert!(matches!(
                denied
                    .evaluate(EvaluationOperation::Gate("test_small_pass_gate"))
                    .await,
                Err(StatsigErr::InvalidOperation(_))
            ));
            assert_eq!(adapter.starts.load(Ordering::Relaxed), 0);

            let authorized = client
                .prepare_evaluation(
                    Arc::clone(&instance),
                    StatsigUser::with_user_id("authorized-user"),
                    None,
                )
                .expect("authorized requests should retain their ID-list capability")
                .evaluate(EvaluationOperation::Gate("test_small_pass_gate"))
                .await
                .expect("authorized requests should hydrate the existing SDK ID-list store");
            let EvaluationResult::Gate(authorized) = authorized else {
                panic!("authorized ID-list gate should return its evaluated result");
            };
            assert_eq!(
                authorized.evaluation.map(|evaluation| evaluation.value),
                Some(authorized_membership),
                "unexpected authorized ID-list membership for {operator}"
            );
            assert_eq!(adapter.starts.load(Ordering::Relaxed), 1);
            assert!(
                instance
                    .engine
                    .snapshot_evaluation_data()
                    .id_lists
                    .contains_key("tenant_members")
            );

            let denied = client
                .prepare_evaluation_with_id_list_access(
                    Arc::clone(&instance),
                    StatsigUser::with_user_id("authorized-user"),
                    None,
                    false,
                )
                .expect("restricted requests should not inherit hydrated ID-list access");
            assert!(denied.requires_id_lists(&EvaluationOperation::Gate("test_small_pass_gate")));
            assert!(matches!(
                denied
                    .evaluate(EvaluationOperation::Gate("test_small_pass_gate"))
                    .await,
                Err(StatsigErr::InvalidOperation(_))
            ));

            let unrelated = client
                .prepare_evaluation_with_id_list_access(
                    Arc::clone(&instance),
                    StatsigUser::with_user_id("authorized-user"),
                    None,
                    false,
                )
                .expect("restricted requests should still evaluate unrelated configuration")
                .evaluate(EvaluationOperation::Gate("unrelated_gate"))
                .await
                .expect("unrelated configuration must not require an ID-list capability");
            assert!(matches!(unrelated, EvaluationResult::Gate(_)));
            assert_eq!(adapter.starts.load(Ordering::Relaxed), 1);

            instance.shutdown().await.unwrap();
        }

        client.shutdown().await;
    }

    #[tokio::test]
    #[serial]
    async fn failed_lazy_id_list_initialization_preserves_configuration_and_allows_retry() {
        let adapter = Arc::new(TestIdListsAdapter {
            fail_start: AtomicBool::new(true),
            ..TestIdListsAdapter::default()
        });
        let client = EvaluationClient::new(Handle::current(), None).unwrap();
        let instance = client
            .create_instance(
                "client-failed",
                "failed-tenant",
                "failed-host-identity",
                TestDataTransport::new(true),
                None,
                Some(Arc::clone(&adapter) as Arc<dyn IdListsAdapter>),
            )
            .await
            .expect("ID-list failures must not prevent configuration initialization");

        assert_eq!(adapter.starts.load(Ordering::Relaxed), 0);
        let prepared = client
            .prepare_evaluation(
                Arc::clone(&instance),
                StatsigUser::with_user_id("failed-user"),
                None,
            )
            .expect("snapshot metadata should remain available before list initialization");
        assert_eq!(prepared.metadata().lcut, 1);
        assert_eq!(adapter.starts.load(Ordering::Relaxed), 0);

        let result = prepared
            .evaluate(EvaluationOperation::Gate("test_small_pass_gate"))
            .await;
        assert!(matches!(result, Err(StatsigErr::DataStoreFailure(_))));
        assert_eq!(adapter.starts.load(Ordering::Relaxed), 1);
        assert_eq!(adapter.background_schedules.load(Ordering::Relaxed), 0);
        assert_eq!(adapter.shutdowns.load(Ordering::Relaxed), 0);

        adapter.fail_start.store(false, Ordering::Relaxed);
        let retry = client
            .evaluate(
                Arc::clone(&instance),
                StatsigUser::with_user_id("failed-user"),
                None,
                EvaluationOperation::Gate("test_small_pass_gate"),
            )
            .await
            .expect("a failed lazy list synchronization must be retryable");
        assert!(matches!(retry, EvaluationResult::Gate(_)));
        assert_eq!(adapter.starts.load(Ordering::Relaxed), 2);
        assert_eq!(adapter.background_schedules.load(Ordering::Relaxed), 1);
        assert_eq!(instance.engine.snapshot_evaluation_data().lcut(), 1);

        instance.shutdown().await.unwrap();
        assert_eq!(adapter.shutdowns.load(Ordering::Relaxed), 1);
        client.shutdown().await;
    }

    #[tokio::test]
    #[serial]
    async fn list_free_snapshots_do_not_require_an_id_list_adapter() {
        let client = EvaluationClient::new(Handle::current(), None).unwrap();
        let adapter = Arc::new(TestIdListsAdapter::default());
        let with_adapter = client
            .create_instance(
                "client-list-free",
                "list-free-tenant",
                "list-free-host",
                TestDataTransport::new(false),
                None,
                Some(Arc::clone(&adapter) as Arc<dyn IdListsAdapter>),
            )
            .await
            .unwrap();
        let without_adapter = client
            .create_instance(
                "client-list-free-missing",
                "list-free-tenant",
                "list-free-host-missing",
                TestDataTransport::new(false),
                None,
                None,
            )
            .await
            .unwrap();

        for instance in [&with_adapter, &without_adapter] {
            let result = client
                .evaluate(
                    Arc::clone(instance),
                    StatsigUser::with_user_id("list-free-user"),
                    None,
                    EvaluationOperation::Gate("missing-gate"),
                )
                .await
                .expect("list-free snapshots must not depend on ID-list infrastructure");
            assert!(matches!(result, EvaluationResult::Gate(_)));
        }
        assert_eq!(adapter.starts.load(Ordering::Relaxed), 0);
        assert_eq!(adapter.background_schedules.load(Ordering::Relaxed), 0);

        with_adapter.shutdown().await.unwrap();
        without_adapter.shutdown().await.unwrap();
        client.shutdown().await;
    }

    #[tokio::test]
    #[serial]
    async fn unrelated_entities_in_mixed_snapshots_evaluate_without_id_list_credentials() {
        let source = TestDataTransport::new(true);
        {
            let mut payload = source.payload.lock();
            let mut specs: serde_json::Value = serde_json::from_slice(&payload).unwrap();
            let mut unrelated_gate = specs["feature_gates"]["test_small_pass_gate"].clone();
            unrelated_gate["rules"][0]["conditions"] = serde_json::json!([]);
            specs["feature_gates"]["unrelated_gate"] = unrelated_gate;

            let mut unrelated_config = specs["dynamic_configs"]["test_custom_config"].clone();
            unrelated_config["rules"] = serde_json::json!([]);
            specs["dynamic_configs"]["unrelated_config"] = unrelated_config;

            let mut unrelated_layer = specs["layer_configs"]["layer_with_many_params"].clone();
            unrelated_layer["rules"] = serde_json::json!([]);
            specs["layer_configs"]["unrelated_layer"] = unrelated_layer;

            *payload = serde_json::to_vec(&specs).unwrap();
        }

        let client = EvaluationClient::new(Handle::current(), None).unwrap();
        let instance = client
            .create_instance(
                "client-mixed",
                "mixed-tenant",
                "mixed-host",
                source,
                None,
                None,
            )
            .await
            .expect("mixed snapshots must load without privileged list credentials");

        let unrelated_gate = client
            .evaluate(
                Arc::clone(&instance),
                StatsigUser::with_user_id("mixed-user"),
                None,
                EvaluationOperation::Gate("unrelated_gate"),
            )
            .await
            .expect("unrelated gates must not require ID-list credentials");
        assert!(matches!(unrelated_gate, EvaluationResult::Gate(_)));

        let unrelated_config = client
            .evaluate(
                Arc::clone(&instance),
                StatsigUser::with_user_id("mixed-user"),
                None,
                EvaluationOperation::Config {
                    name: "unrelated_config",
                },
            )
            .await
            .expect("unrelated configs must not require ID-list credentials");
        assert!(matches!(unrelated_config, EvaluationResult::Config(_)));

        let unrelated_layer = client
            .evaluate(
                Arc::clone(&instance),
                StatsigUser::with_user_id("mixed-user"),
                None,
                EvaluationOperation::Layer("unrelated_layer"),
            )
            .await
            .expect("unrelated layers must not require ID-list credentials");
        assert!(matches!(unrelated_layer, EvaluationResult::Layer(_)));

        let list_backed = client
            .evaluate(
                Arc::clone(&instance),
                StatsigUser::with_user_id("mixed-user"),
                None,
                EvaluationOperation::Gate("test_small_pass_gate"),
            )
            .await;
        assert!(matches!(list_backed, Err(StatsigErr::InvalidOperation(_))));

        instance.shutdown().await.unwrap();
        client.shutdown().await;
    }

    #[tokio::test]
    #[serial]
    async fn concurrent_list_evaluations_share_one_lazy_standard_adapter_initialization() {
        let entered = Arc::new(Notify::new());
        let release = Arc::new(Notify::new());
        let mut adapter = TestIdListsAdapter::containing("tenant_members", "concurrent-user");
        {
            let adapter = Arc::get_mut(&mut adapter).unwrap();
            adapter.start_entered = Some(Arc::clone(&entered));
            adapter.start_release = Some(Arc::clone(&release));
        }
        let client = EvaluationClient::new(Handle::current(), None).unwrap();
        let instance = client
            .create_instance(
                "client-concurrent",
                "concurrent-tenant",
                "concurrent-host",
                TestDataTransport::new(true),
                None,
                Some(Arc::clone(&adapter) as Arc<dyn IdListsAdapter>),
            )
            .await
            .unwrap();

        let mut tasks = tokio::task::JoinSet::new();
        for _ in 0..8 {
            let client = Arc::clone(&client);
            let instance = Arc::clone(&instance);
            tasks.spawn(async move {
                client
                    .evaluate(
                        instance,
                        StatsigUser::with_user_id("concurrent-user"),
                        None,
                        EvaluationOperation::Gate("test_small_pass_gate"),
                    )
                    .await
            });
        }

        entered.notified().await;
        for _ in 0..8 {
            tokio::task::yield_now().await;
        }
        assert_eq!(adapter.starts.load(Ordering::Relaxed), 1);
        release.notify_one();

        while let Some(result) = tasks.join_next().await {
            let evaluation = result
                .unwrap()
                .expect("shared list initialization should succeed");
            let EvaluationResult::Gate(gate) = evaluation else {
                panic!("concurrent operation should evaluate its gate");
            };
            assert_eq!(
                gate.evaluation.map(|evaluation| evaluation.value),
                Some(true)
            );
        }
        assert_eq!(adapter.starts.load(Ordering::Relaxed), 1);
        assert_eq!(adapter.background_schedules.load(Ordering::Relaxed), 1);

        instance.shutdown().await.unwrap();
        client.shutdown().await;
    }

    #[tokio::test]
    #[serial]
    async fn stalled_list_initialization_bounds_every_waiter_and_allows_retry() {
        let entered = Arc::new(Notify::new());
        let release = Arc::new(Notify::new());
        let adapter = Arc::new(TestIdListsAdapter {
            start_entered: Some(Arc::clone(&entered)),
            start_release: Some(Arc::clone(&release)),
            ..TestIdListsAdapter::default()
        });
        let client = EvaluationClient::new(Handle::current(), None).unwrap();
        let instance = client
            .create_instance(
                "client-stalled",
                "stalled-tenant",
                "stalled-host",
                TestDataTransport::new(true),
                None,
                Some(Arc::clone(&adapter) as Arc<dyn IdListsAdapter>),
            )
            .await
            .unwrap();

        let started = tokio::time::Instant::now();
        let mut tasks = tokio::task::JoinSet::new();
        for _ in 0..4 {
            let client = Arc::clone(&client);
            let instance = Arc::clone(&instance);
            tasks.spawn(async move {
                client
                    .evaluate(
                        instance,
                        StatsigUser::with_user_id("stalled-user"),
                        None,
                        EvaluationOperation::Gate("test_small_pass_gate"),
                    )
                    .await
            });
        }
        entered.notified().await;

        while let Some(result) = tasks.join_next().await {
            assert!(matches!(
                result.unwrap(),
                Err(StatsigErr::DataStoreFailure(_))
            ));
        }
        assert!(
            started.elapsed() < super::ID_LIST_INITIALIZATION_TIMEOUT + Duration::from_secs(2),
            "queued evaluations must not each add a fresh initialization timeout"
        );

        release.notify_one();
        client
            .evaluate(
                Arc::clone(&instance),
                StatsigUser::with_user_id("stalled-user"),
                None,
                EvaluationOperation::Gate("test_small_pass_gate"),
            )
            .await
            .expect("cancelled list initialization must permit a later retry");
        assert_eq!(adapter.background_schedules.load(Ordering::Relaxed), 1);

        instance.shutdown().await.unwrap();
        client.shutdown().await;
    }

    #[tokio::test]
    #[serial]
    async fn production_engine_evaluates_membership_operators_from_tenant_snapshots() {
        let client = EvaluationClient::new(Handle::current(), None)
            .expect("evaluation client should initialize");

        for (operator, expected_allowed, expected_denied) in [
            ("in_segment_list", true, false),
            ("not_in_segment_list", false, true),
        ] {
            let allowed_adapter =
                TestIdListsAdapter::containing("tenant_members", "operator-matrix-user");
            let denied_adapter = Arc::new(TestIdListsAdapter::default());
            let source = TestDataTransport::new(true);
            {
                let mut payload = source.payload.lock();
                let mut specs: serde_json::Value = serde_json::from_slice(&payload)
                    .expect("evaluation snapshot should deserialize");
                specs["condition_map"]["tenant-id-list"]["operator"] =
                    serde_json::Value::String(operator.to_string());
                *payload =
                    serde_json::to_vec(&specs).expect("evaluation snapshot should serialize");
            }

            let allowed = client
                .create_instance(
                    "client-allowed",
                    "allowed-tenant",
                    &format!("allowed-{operator}"),
                    Arc::clone(&source) as Arc<dyn EvaluationDataTransport>,
                    None,
                    Some(Arc::clone(&allowed_adapter) as Arc<dyn IdListsAdapter>),
                )
                .await
                .expect("allowed tenant instance should initialize");
            let denied = client
                .create_instance(
                    "client-denied",
                    "denied-tenant",
                    &format!("denied-{operator}"),
                    Arc::clone(&source) as Arc<dyn EvaluationDataTransport>,
                    None,
                    Some(Arc::clone(&denied_adapter) as Arc<dyn IdListsAdapter>),
                )
                .await
                .expect("denied tenant instance should initialize");

            let (allowed_result, denied_result) =
                tokio::time::timeout(std::time::Duration::from_secs(2), async {
                    tokio::join!(
                        client.evaluate(
                            Arc::clone(&allowed),
                            StatsigUser::with_user_id("operator-matrix-user"),
                            None,
                            EvaluationOperation::Gate("test_small_pass_gate"),
                        ),
                        client.evaluate(
                            Arc::clone(&denied),
                            StatsigUser::with_user_id("operator-matrix-user"),
                            None,
                            EvaluationOperation::Gate("test_small_pass_gate"),
                        ),
                    )
                })
                .await
                .expect("independent tenant snapshots should evaluate concurrently");

            for (result, expected) in [
                (allowed_result, expected_allowed),
                (denied_result, expected_denied),
            ] {
                let EvaluationResult::Gate(result) =
                    result.expect("ID-list gate should evaluate successfully")
                else {
                    panic!("gate operation should return its evaluated result");
                };
                assert_eq!(
                    result.evaluation.map(|evaluation| evaluation.value),
                    Some(expected),
                    "unexpected ID-list result for {operator}"
                );
            }

            allowed.shutdown().await.unwrap();
            denied.shutdown().await.unwrap();
            assert_eq!(allowed_adapter.starts.load(Ordering::Relaxed), 1);
            assert_eq!(denied_adapter.starts.load(Ordering::Relaxed), 1);
        }
        client.shutdown().await;
    }

    #[tokio::test]
    #[serial]
    async fn lazy_id_list_materialization_keeps_original_pinned_configuration() {
        let adapter = TestIdListsAdapter::containing("tenant_members", "pinned-user");
        let client = EvaluationClient::new(Handle::current(), None).unwrap();
        let source = TestDataTransport::new(true);
        source.replace_snapshot(1, TEST_CHECKSUM, "first-app");
        let instance = client
            .create_instance(
                "client-lazy-pinned",
                "lazy-pinned-tenant",
                "lazy-pinned-host",
                Arc::clone(&source) as Arc<dyn EvaluationDataTransport>,
                None,
                Some(Arc::clone(&adapter) as Arc<dyn IdListsAdapter>),
            )
            .await
            .unwrap();
        let request = client
            .prepare_evaluation(
                Arc::clone(&instance),
                StatsigUser::with_user_id("pinned-user"),
                Some("first-app".to_string()),
            )
            .unwrap();
        assert_eq!(request.metadata().lcut, 1);
        assert_eq!(adapter.starts.load(Ordering::Relaxed), 0);

        source.replace_snapshot(2, "lazy-pinned-refreshed-checksum", "second-app");
        Arc::clone(instance.engine.adapter.as_ref().unwrap())
            .start(&instance.engine.runtime)
            .await
            .unwrap();
        assert_eq!(request.metadata().lcut, 1);

        let EvaluationResult::Gate(evaluation) = request
            .evaluate(EvaluationOperation::Gate("test_small_pass_gate"))
            .await
            .expect("lazy ID lists must hydrate without changing the pinned DCS snapshot")
        else {
            panic!("pinned request should produce a gate result");
        };
        assert_eq!(
            evaluation.evaluation.map(|evaluation| evaluation.value),
            Some(true),
            "rebasing lazy ID lists must not replace the original first-app DCS snapshot"
        );
        assert_eq!(adapter.starts.load(Ordering::Relaxed), 1);

        instance.shutdown().await.unwrap();
        client.shutdown().await;
    }

    #[tokio::test]
    #[serial]
    async fn production_engine_request_pins_snapshot_across_id_list_and_config_refresh() {
        let adapter = TestIdListsAdapter::containing("tenant_members", "pinned-user");
        let client = EvaluationClient::new(Handle::current(), None)
            .expect("evaluation client should initialize");
        let source = TestDataTransport::new(true);
        source.replace_snapshot(1, TEST_CHECKSUM, "first-app");
        let instance = client
            .create_instance(
                "client-pinned",
                "allowed-tenant",
                "pinned-host-identity",
                Arc::clone(&source) as Arc<dyn EvaluationDataTransport>,
                None,
                Some(Arc::clone(&adapter) as Arc<dyn IdListsAdapter>),
            )
            .await
            .expect("tenant-bound evaluation engine should initialize");

        let initial = client
            .evaluate(
                Arc::clone(&instance),
                StatsigUser::with_user_id("pinned-user"),
                Some("first-app".to_string()),
                EvaluationOperation::Gate("test_small_pass_gate"),
            )
            .await
            .expect("the initial list-backed evaluation should lazily hydrate standard ID lists");
        assert!(matches!(initial, EvaluationResult::Gate(_)));

        let request = client
            .prepare_evaluation(
                Arc::clone(&instance),
                StatsigUser::with_user_id("pinned-user"),
                Some("first-app".to_string()),
            )
            .expect("evaluation request should pin the initial snapshot");
        assert_eq!(request.metadata().lcut, 1);
        let metadata_probe = client
            .prepare_evaluation(
                Arc::clone(&instance),
                StatsigUser::with_user_id("pinned-user"),
                Some("first-app".to_string()),
            )
            .expect("metadata probe should pin the same initial snapshot");

        adapter.replace_memberships(HashMap::new());
        let refreshed_lists = client
            .prepare_evaluation(
                Arc::clone(&instance),
                StatsigUser::with_user_id("pinned-user"),
                Some("first-app".to_string()),
            )
            .expect("new requests should pin refreshed SDK ID-list state");
        let EvaluationResult::Gate(refreshed_membership) = refreshed_lists
            .evaluate(EvaluationOperation::Gate("test_small_pass_gate"))
            .await
            .expect("refreshed membership should evaluate")
        else {
            panic!("refreshed membership should return a gate result");
        };
        assert_eq!(
            refreshed_membership
                .evaluation
                .map(|evaluation| evaluation.value),
            Some(false)
        );

        source.replace_snapshot(2, "refreshed-evaluation-instance-checksum", "second-app");
        Arc::clone(
            instance
                .engine
                .adapter
                .as_ref()
                .expect("production evaluation engines should synchronize configuration"),
        )
        .start(&instance.engine.runtime)
        .await
        .expect("newer DCS metadata and payload should publish through the real adapter");
        assert_eq!(metadata_probe.metadata().lcut, 1);

        let refreshed = client
            .prepare_evaluation(
                Arc::clone(&instance),
                StatsigUser::with_user_id("pinned-user"),
                Some("first-app".to_string()),
            )
            .expect("new evaluation should pin the refreshed snapshot");
        assert_eq!(refreshed.metadata().lcut, 2);

        let EvaluationResult::Gate(pinned) = request
            .evaluate(EvaluationOperation::Gate("test_small_pass_gate"))
            .await
            .expect("pinned request should evaluate")
        else {
            panic!("pinned gate should return an evaluated gate result");
        };
        assert_eq!(
            pinned.evaluation.map(|evaluation| evaluation.value),
            Some(true)
        );

        let EvaluationResult::Gate(updated) = refreshed
            .evaluate(EvaluationOperation::Gate("test_small_pass_gate"))
            .await
            .expect("refreshed request should evaluate")
        else {
            panic!("refreshed gate should return an evaluated gate result");
        };
        assert!(updated.evaluation.is_none());
        assert_eq!(source.metadata_fetches.load(Ordering::Relaxed), 2);

        drop(metadata_probe);
        instance.shutdown().await.unwrap();
        client.shutdown().await;
    }

    #[test]
    fn foreground_initialization_keeps_background_work_on_host_runtime() {
        let foreground = tokio::runtime::Builder::new_multi_thread()
            .worker_threads(1)
            .thread_name("evaluation-foreground")
            .enable_all()
            .build()
            .unwrap();
        let background = tokio::runtime::Builder::new_multi_thread()
            .worker_threads(1)
            .thread_name("evaluation-background")
            .enable_all()
            .build()
            .unwrap();

        let background_handle = background.handle().clone();
        foreground
            .block_on(foreground.spawn(async move {
                let transport = TestDataTransport::new(false);
                let client = EvaluationClient::new(background_handle, None).unwrap();
                let instance = client
                    .create_instance(
                        "client-runtime",
                        "runtime-tenant",
                        "runtime-identity",
                        Arc::clone(&transport) as Arc<dyn EvaluationDataTransport>,
                        None,
                        None,
                    )
                    .await
                    .unwrap();

                assert_eq!(
                    transport.initialization_thread.lock().as_deref(),
                    Some("evaluation-foreground")
                );

                let (sender, receiver) = tokio::sync::oneshot::channel();
                instance
                    .engine
                    .runtime
                    .spawn("evaluation-runtime-placement-test", move |_| async move {
                        sender
                            .send(std::thread::current().name().map(str::to_string))
                            .unwrap();
                    })
                    .unwrap();
                assert_eq!(
                    receiver.await.unwrap().as_deref(),
                    Some("evaluation-background")
                );

                instance.shutdown().await.unwrap();
                client.shutdown().await;
            }))
            .unwrap();
    }

    struct BlockingDataTransport {
        started: Arc<Notify>,
        cancelled: Arc<Notify>,
    }

    struct CancelledInitialization(Arc<Notify>);

    impl Drop for CancelledInitialization {
        fn drop(&mut self) {
            self.0.notify_one();
        }
    }

    #[async_trait]
    impl EvaluationDataTransport for BlockingDataTransport {
        async fn fetch_metadata(&self) -> Result<EvaluationDataVersion, StatsigErr> {
            let _cancelled = CancelledInitialization(Arc::clone(&self.cancelled));
            self.started.notify_one();
            std::future::pending().await
        }

        async fn fetch_payload(
            &self,
            _version: &EvaluationDataVersion,
            _fallback: bool,
        ) -> Result<ResponseData, StatsigErr> {
            unreachable!("cancelled initialization must not request a payload")
        }
    }

    #[tokio::test]
    async fn cancelled_initialization_stops_metadata_io_and_allows_retry() {
        let client = EvaluationClient::new(Handle::current(), None).unwrap();
        let blocking = Arc::new(BlockingDataTransport {
            started: Arc::new(Notify::new()),
            cancelled: Arc::new(Notify::new()),
        });
        let blocked_client = Arc::clone(&client);
        let blocked_transport = Arc::clone(&blocking) as Arc<dyn EvaluationDataTransport>;
        let request = tokio::spawn(async move {
            blocked_client
                .create_instance(
                    "client-cancelled",
                    "cancelled-tenant",
                    "cancelled-identity",
                    blocked_transport,
                    None,
                    None,
                )
                .await
        });

        blocking.started.notified().await;
        request.abort();
        assert!(matches!(request.await, Err(error) if error.is_cancelled()));
        blocking.cancelled.notified().await;

        let retry = client
            .create_instance(
                "client-retry",
                "cancelled-tenant",
                "cancelled-identity",
                TestDataTransport::new(false),
                None,
                None,
            )
            .await
            .expect("cancelled initialization must not prevent a later retry");
        retry.shutdown().await.unwrap();
        client.shutdown().await;
    }

    #[tokio::test]
    async fn shutdown_rejects_new_instances_and_prepared_requests() {
        let client = EvaluationClient::new(Handle::current(), None).unwrap();
        let instance = client
            .create_instance(
                "client-existing",
                "shutdown-tenant",
                "shutdown-identity",
                TestDataTransport::new(false),
                None,
                None,
            )
            .await
            .unwrap();

        client.shutdown().await;

        assert!(
            client
                .prepare_evaluation(
                    Arc::clone(&instance),
                    StatsigUser::with_user_id("user"),
                    None,
                )
                .is_err()
        );
        assert!(
            client
                .create_instance(
                    "client-rejected",
                    "shutdown-tenant",
                    "another-identity",
                    TestDataTransport::new(false),
                    None,
                    None,
                )
                .await
                .is_err()
        );
        instance.shutdown().await.unwrap();
    }
}
