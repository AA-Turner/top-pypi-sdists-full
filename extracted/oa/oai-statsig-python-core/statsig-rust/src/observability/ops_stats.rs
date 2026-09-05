use super::{
    DiagnosticsEvent,
    observability_client_adapter::{MetricType, ObservabilityEvent},
    sdk_errors_observer::ErrorBoundaryEvent,
};
use crate::user::StatsigUserLoggable;
use crate::{ObservabilityClient, StatsigRuntime, log_e, log_w};
use crate::{
    observability::console_capture_observer::ConsoleCaptureEvent,
    sdk_diagnostics::{
        diagnostics::ContextType,
        marker::{KeyType, Marker},
    },
};
use async_trait::async_trait;
use lazy_static::lazy_static;
use parking_lot::RwLock;
use std::{
    cell::{Cell, RefCell},
    collections::HashMap,
    future::Future,
    marker::PhantomData,
    rc::Rc,
    sync::{Arc, Weak},
};
use tokio::sync::Notify;
use tokio::sync::broadcast::{self, Sender};

const TAG: &str = stringify!(OpsStats);

/* Ideally we don't need to pass OpsStats around, but right now I could find a good way to do it to support multiple instances*/
lazy_static! {
    pub static ref OPS_STATS: OpsStats = OpsStats::new();
}

thread_local! {
    // Constructors synchronously pull OpsStats through several SDK-owned children. Keep their
    // mode scoped to that construction thread instead of threading a flag through every child
    // constructor. A scope must not cross an await/thread boundary.
    static INSTANCE_SCOPES: RefCell<Vec<OpsStatsInstanceScope>> = const { RefCell::new(Vec::new()) };
    static NEXT_INSTANCE_SCOPE_TOKEN: Cell<u64> = const { Cell::new(0) };
}

tokio::task_local! {
    static SCOPED_HYDRATION_OBSERVABILITY: Arc<dyn ObservabilityClient>;
}

pub(crate) async fn with_scoped_hydration_observability<F: Future>(
    observer: Option<Arc<dyn ObservabilityClient>>,
    operation: F,
) -> F::Output {
    match observer {
        Some(observer) => {
            SCOPED_HYDRATION_OBSERVABILITY
                .scope(observer, operation)
                .await
        }
        None => operation.await,
    }
}

#[derive(Clone)]
enum OpsStatsInstanceMode {
    Enabled,
    Disabled(Arc<OpsStatsForInstance>),
}

struct OpsStatsInstanceScope {
    registry_id: usize,
    sdk_key: String,
    mode: OpsStatsInstanceMode,
    token: u64,
}

#[must_use]
pub(crate) struct OpsStatsInstanceScopeGuard<'registry> {
    token: u64,
    _registry: PhantomData<&'registry OpsStats>,
    // The scope lives in thread-local storage, so dropping it on another thread would leak the
    // originating thread's mode. Keep the guard !Send and !Sync.
    _not_send_or_sync: PhantomData<Rc<()>>,
}

impl Drop for OpsStatsInstanceScopeGuard<'_> {
    fn drop(&mut self) {
        let _ = INSTANCE_SCOPES.try_with(|scopes| {
            let mut scopes = scopes.borrow_mut();
            if scopes.last().is_some_and(|scope| scope.token == self.token) {
                scopes.pop();
                return;
            }

            // Normal construction drops guards LIFO. Removing by token also makes cleanup safe
            // if a caller manually drops nested guards out of order during unwinding.
            if let Some(index) = scopes.iter().rposition(|scope| scope.token == self.token) {
                scopes.remove(index);
            }
        });
    }
}

pub struct OpsStats {
    instances_map: RwLock<HashMap<String, Weak<OpsStatsForInstance>>>,
}

impl Default for OpsStats {
    fn default() -> Self {
        Self::new()
    }
}

impl OpsStats {
    pub fn new() -> Self {
        OpsStats {
            instances_map: HashMap::new().into(),
        }
    }

    pub fn get_for_instance(&self, sdk_key: &str) -> Arc<OpsStatsForInstance> {
        if let Some(OpsStatsInstanceMode::Disabled(instance)) = self.scoped_instance_mode(sdk_key) {
            return instance;
        }

        match self
            .instances_map
            .try_read_for(std::time::Duration::from_secs(5))
        {
            Some(read_guard) => {
                if let Some(instance) = read_guard.get(sdk_key) {
                    if let Some(instance) = instance.upgrade() {
                        return instance.clone();
                    }
                }
            }
            None => {
                log_e!(
                    TAG,
                    "Failed to get read guard: Failed to lock instances_map"
                );
            }
        }

        let instance = Arc::new(OpsStatsForInstance::new());
        match self
            .instances_map
            .try_write_for(std::time::Duration::from_secs(5))
        {
            Some(mut write_guard) => {
                write_guard.insert(sdk_key.into(), Arc::downgrade(&instance));
            }
            None => {
                log_e!(
                    TAG,
                    "Failed to get write guard: Failed to lock instances_map"
                );
            }
        }

        instance
    }

    /// Routes SDK-owned child construction through the selected namespace for this thread.
    ///
    /// The last matching scope wins so a reentrant ordinary constructor can mask an outer
    /// config-only constructor with the same instance ID.
    pub(crate) fn enter_instance_scope(
        &self,
        sdk_key: &str,
        disabled: Option<Arc<OpsStatsForInstance>>,
    ) -> OpsStatsInstanceScopeGuard<'_> {
        let token = NEXT_INSTANCE_SCOPE_TOKEN.with(|next_token| {
            let token = next_token.get();
            next_token.set(token.wrapping_add(1));
            token
        });
        let mode = disabled.map_or(
            OpsStatsInstanceMode::Enabled,
            OpsStatsInstanceMode::Disabled,
        );
        INSTANCE_SCOPES.with(|scopes| {
            scopes.borrow_mut().push(OpsStatsInstanceScope {
                registry_id: self as *const Self as usize,
                sdk_key: sdk_key.to_string(),
                mode,
                token,
            });
        });

        OpsStatsInstanceScopeGuard {
            token,
            _registry: PhantomData,
            _not_send_or_sync: PhantomData,
        }
    }

    fn scoped_instance_mode(&self, sdk_key: &str) -> Option<OpsStatsInstanceMode> {
        let registry_id = self as *const Self as usize;
        INSTANCE_SCOPES.with(|scopes| {
            scopes
                .borrow()
                .iter()
                .rev()
                .find(|scope| scope.registry_id == registry_id && scope.sdk_key == sdk_key)
                .map(|scope| scope.mode.clone())
        })
    }

    #[cfg(test)]
    pub(crate) fn has_instance_for_test(&self, sdk_key: &str) -> bool {
        self.instances_map
            .read()
            .get(sdk_key)
            .and_then(Weak::upgrade)
            .is_some()
    }
}

#[derive(Clone)]
pub enum OpsStatsEvent {
    Observability(ObservabilityEvent),
    SDKError(ErrorBoundaryEvent),
    Diagnostics(DiagnosticsEvent),
    ConsoleCapture(ConsoleCaptureEvent),
}

pub struct OpsStatsForInstance {
    sender: Option<Sender<OpsStatsEvent>>,
    shutdown_notify: Arc<Notify>,
}

// The class used to handle all observability events including diagnostics, error, event logging, and external metric sharing
impl Default for OpsStatsForInstance {
    fn default() -> Self {
        Self::new()
    }
}

impl OpsStatsForInstance {
    pub fn new() -> Self {
        let (tx, _) = broadcast::channel(1000);
        OpsStatsForInstance {
            sender: Some(tx),
            shutdown_notify: Arc::new(Notify::new()),
        }
    }

    pub(crate) fn disabled() -> Self {
        Self {
            sender: None,
            shutdown_notify: Arc::new(Notify::new()),
        }
    }

    #[cfg(test)]
    pub(crate) fn subscribe_for_test(&self) -> broadcast::Receiver<OpsStatsEvent> {
        self.sender
            .as_ref()
            .expect("test observer requires enabled ops stats")
            .subscribe()
    }

    #[cfg(test)]
    pub(crate) fn is_disabled_for_test(&self) -> bool {
        self.sender.is_none()
    }

    pub fn log(&self, event: OpsStatsEvent) {
        let Some(sender) = self.sender.as_ref() else {
            Self::forward_scoped_hydration_event(event);
            return;
        };
        match sender.send(event) {
            Ok(_) => {}
            Err(e) => {
                log_w!(
                    "OpsStats Message Queue",
                    "Dropping ops stats event {}",
                    e.to_string()
                );
            }
        }
    }

    fn forward_scoped_hydration_event(event: OpsStatsEvent) {
        let OpsStatsEvent::Observability(event) = event else {
            return;
        };
        if !matches!(
            event.metric_name.as_str(),
            "remote_config_hydration.count"
                | "remote_config_hydration.latency"
                | "remote_config_hydration.bytes"
        ) {
            return;
        }

        let _ = SCOPED_HYDRATION_OBSERVABILITY.try_with(|observer| {
            let mut tags = event.tags.unwrap_or_default();
            let metadata = crate::statsig_metadata::StatsigMetadata::get_metadata();
            tags.insert("sdk_type".to_string(), metadata.sdk_type);
            tags.insert("sdk_version".to_string(), metadata.sdk_version);
            let name = format!("statsig.sdk.{}", event.metric_name);
            let tags = Some(tags);
            match event.metric_type {
                MetricType::Increment => observer.increment(name, event.value, tags),
                MetricType::Gauge => observer.gauge(name, event.value, tags),
                MetricType::Dist => observer.dist(name, event.value, tags),
            }
        });
    }

    pub fn log_error(&self, error: ErrorBoundaryEvent) {
        self.log(OpsStatsEvent::SDKError(error));
    }

    pub fn log_checksum_validation_result(&self, is_success: bool) {
        self.log(ObservabilityEvent::new_event(
            MetricType::Increment,
            "deltas_checksum_validation.count".to_string(),
            1.0,
            Some(HashMap::from([(
                "result".to_string(),
                if is_success { "success" } else { "failure" }.to_string(),
            )])),
        ));
    }

    pub fn add_marker(&self, marker: Marker, context: Option<ContextType>) {
        self.log(OpsStatsEvent::Diagnostics(DiagnosticsEvent {
            marker: Some(marker),
            context,
            key: None,
            should_enqueue: false,
        }));
    }

    pub fn set_diagnostics_context(&self, context: ContextType) {
        self.log(OpsStatsEvent::Diagnostics(DiagnosticsEvent {
            marker: None,
            context: Some(context),
            key: None,
            should_enqueue: false,
        }));
    }

    pub fn enqueue_diagnostics_event(&self, key: Option<KeyType>, context: Option<ContextType>) {
        self.log(OpsStatsEvent::Diagnostics(DiagnosticsEvent {
            marker: None,
            context,
            key,
            should_enqueue: true,
        }));
    }

    pub fn enqueue_console_capture_event(
        &self,
        level: String,
        payload: Vec<String>,
        timestamp: u64,
        user: StatsigUserLoggable,
        stack_trace: Option<String>,
    ) {
        self.log(OpsStatsEvent::ConsoleCapture(ConsoleCaptureEvent {
            level,
            payload,
            timestamp,
            user,
            stack_trace,
        }));
    }

    pub fn subscribe(
        &self,
        runtime: Arc<StatsigRuntime>,
        observer: Weak<dyn OpsStatsEventObserver>,
    ) {
        let Some(sender) = self.sender.as_ref() else {
            return;
        };
        let mut rx = sender.subscribe();
        let shutdown_notify = self.shutdown_notify.clone();
        let _ = runtime.spawn("opts_stats_listen_for", |rt_shutdown_notify| async move {
            loop {
                tokio::select! {
                    event = rx.recv() => {
                        let observer = match observer.upgrade() {
                            Some(observer) => observer,
                            None => break,
                        };

                        if let Ok(event) = event {
                            observer.handle_event(event).await;
                        }
                    }
                    () = rt_shutdown_notify.notified() => {
                        break;
                    }
                    () = shutdown_notify.notified() => {
                        break;
                    }
                }
            }
        });
    }
}

impl Drop for OpsStatsForInstance {
    fn drop(&mut self) {
        self.shutdown_notify.notify_waiters();
    }
}

#[async_trait]
pub trait OpsStatsEventObserver: Send + Sync + 'static {
    async fn handle_event(&self, event: OpsStatsEvent);
}

#[cfg(test)]
mod tests {
    use super::{
        OpsStats, OpsStatsEventObserver, OpsStatsForInstance, with_scoped_hydration_observability,
    };
    use crate::ObservabilityClient;
    use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
    use parking_lot::Mutex;
    use std::collections::HashMap;
    use std::panic::{AssertUnwindSafe, catch_unwind};
    use std::sync::Arc;

    type RecordedHydrationMetric = (String, Option<HashMap<String, String>>);

    #[derive(Default)]
    struct RecordingHydrationObserver {
        events: Mutex<Vec<RecordedHydrationMetric>>,
    }

    impl ObservabilityClient for RecordingHydrationObserver {
        fn init(&self) {}

        fn increment(&self, name: String, _value: f64, tags: Option<HashMap<String, String>>) {
            self.events.lock().push((name, tags));
        }

        fn gauge(&self, _name: String, _value: f64, _tags: Option<HashMap<String, String>>) {}

        fn dist(&self, _name: String, _value: f64, _tags: Option<HashMap<String, String>>) {}

        fn error(&self, _tag: String, _error: String) {}

        fn should_enable_high_cardinality_for_this_tag(&self, _tag: String) -> Option<bool> {
            Some(false)
        }

        fn to_ops_stats_event_observer(self: Arc<Self>) -> Arc<dyn OpsStatsEventObserver> {
            self
        }
    }

    fn hydration_count(outcome: &str) -> super::OpsStatsEvent {
        ObservabilityEvent::new_event(
            MetricType::Increment,
            "remote_config_hydration.count".to_string(),
            1.0,
            Some(HashMap::from([(
                "outcome".to_string(),
                outcome.to_string(),
            )])),
        )
    }

    #[tokio::test]
    async fn disabled_hydration_metrics_stay_task_local_and_ignore_unrelated_events() {
        let disabled = Arc::new(OpsStatsForInstance::disabled());
        let first = Arc::new(RecordingHydrationObserver::default());
        let second = Arc::new(RecordingHydrationObserver::default());

        tokio::join!(
            with_scoped_hydration_observability(
                Some(Arc::clone(&first) as Arc<dyn ObservabilityClient>),
                async {
                    tokio::task::yield_now().await;
                    disabled.log(hydration_count("first"));
                    disabled.log(ObservabilityEvent::new_event(
                        MetricType::Increment,
                        "unrelated.private.metric".to_string(),
                        1.0,
                        None,
                    ));
                },
            ),
            with_scoped_hydration_observability(
                Some(Arc::clone(&second) as Arc<dyn ObservabilityClient>),
                async {
                    tokio::task::yield_now().await;
                    disabled.log(hydration_count("second"));
                },
            ),
        );
        disabled.log(hydration_count("outside"));

        for (observer, expected_outcome) in [(first, "first"), (second, "second")] {
            let events = observer.events.lock();
            assert_eq!(events.len(), 1);
            assert_eq!(events[0].0, "statsig.sdk.remote_config_hydration.count");
            let tags = events[0]
                .1
                .as_ref()
                .expect("forwarded hydration metrics should include SDK tags");
            assert_eq!(
                tags.get("outcome").map(String::as_str),
                Some(expected_outcome)
            );
            assert!(tags.contains_key("sdk_type"));
            assert!(tags.contains_key("sdk_version"));
        }
    }

    #[test]
    fn disabled_scope_routes_child_lookups_without_replacing_enabled_instances() {
        let registry = OpsStats::new();
        let enabled = registry.get_for_instance("shared-instance");
        let disabled = Arc::new(OpsStatsForInstance::disabled());

        {
            let _scope =
                registry.enter_instance_scope("shared-instance", Some(Arc::clone(&disabled)));
            let scoped = registry.get_for_instance("shared-instance");

            assert!(scoped.is_disabled_for_test());
            assert!(!Arc::ptr_eq(&enabled, &scoped));
            assert!(Arc::ptr_eq(&disabled, &scoped));
        }

        assert!(Arc::ptr_eq(
            &registry.get_for_instance("shared-instance"),
            &enabled
        ));
    }

    #[test]
    fn last_matching_scope_masks_and_restores_outer_mode() {
        let registry = OpsStats::new();
        let enabled = registry.get_for_instance("shared-instance");
        let disabled = Arc::new(OpsStatsForInstance::disabled());
        let outer = registry.enter_instance_scope("shared-instance", Some(Arc::clone(&disabled)));
        assert!(disabled.is_disabled_for_test());

        {
            let _inner = registry.enter_instance_scope("shared-instance", None);
            assert!(Arc::ptr_eq(
                &registry.get_for_instance("shared-instance"),
                &enabled
            ));
        }

        assert!(Arc::ptr_eq(
            &registry.get_for_instance("shared-instance"),
            &disabled
        ));
        drop(outer);
        assert!(Arc::ptr_eq(
            &registry.get_for_instance("shared-instance"),
            &enabled
        ));
    }

    #[test]
    fn scoped_mode_is_thread_local() {
        let registry = Arc::new(OpsStats::new());
        let disabled = Arc::new(OpsStatsForInstance::disabled());
        let _scope = registry.enter_instance_scope("shared-instance", Some(Arc::clone(&disabled)));
        assert!(disabled.is_disabled_for_test());
        assert!(Arc::ptr_eq(
            &registry.get_for_instance("shared-instance"),
            &disabled
        ));

        let thread_registry = Arc::clone(&registry);
        let enabled =
            std::thread::spawn(move || thread_registry.get_for_instance("shared-instance"))
                .join()
                .unwrap();

        assert!(!enabled.is_disabled_for_test());
        assert!(!Arc::ptr_eq(&enabled, &disabled));
    }

    #[test]
    fn scoped_mode_is_removed_during_panic_unwind() {
        let registry = OpsStats::new();
        let result = catch_unwind(AssertUnwindSafe(|| {
            let _scope = registry.enter_instance_scope(
                "shared-instance",
                Some(Arc::new(OpsStatsForInstance::disabled())),
            );
            assert!(
                registry
                    .get_for_instance("shared-instance")
                    .is_disabled_for_test()
            );
            panic!("test panic");
        }));

        assert!(result.is_err());
        assert!(
            !registry
                .get_for_instance("shared-instance")
                .is_disabled_for_test()
        );
    }

    #[test]
    fn scopes_are_isolated_by_registry_identity() {
        let first_registry = OpsStats::new();
        let second_registry = OpsStats::new();
        let _scope = first_registry.enter_instance_scope(
            "shared-instance",
            Some(Arc::new(OpsStatsForInstance::disabled())),
        );

        assert!(
            first_registry
                .get_for_instance("shared-instance")
                .is_disabled_for_test()
        );
        assert!(
            !second_registry
                .get_for_instance("shared-instance")
                .is_disabled_for_test()
        );
    }

    #[test]
    fn out_of_order_guard_drop_preserves_inner_scope() {
        let registry = OpsStats::new();
        let outer = registry.enter_instance_scope(
            "shared-instance",
            Some(Arc::new(OpsStatsForInstance::disabled())),
        );
        let inner = registry.enter_instance_scope("shared-instance", None);

        drop(outer);
        assert!(
            !registry
                .get_for_instance("shared-instance")
                .is_disabled_for_test()
        );

        drop(inner);
        assert!(
            !registry
                .get_for_instance("shared-instance")
                .is_disabled_for_test()
        );
    }
}
