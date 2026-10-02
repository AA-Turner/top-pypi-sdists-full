//! Port of `software.amazon.kinesis.metrics.MetricsConfig`.

use std::collections::HashSet;
use std::sync::{Arc, Mutex};

use aws_sdk_cloudwatch::Client as CloudWatchClient;
use opentelemetry::metrics::MeterProvider;

use crate::metrics::otel::OtelMetricsFactory;
use crate::metrics::{
    CloudWatchMetricsFactory, MetricsBackend, MetricsFactory, MetricsLevel,
    OPERATION_DIMENSION_NAME, SHARD_ID_DIMENSION_NAME,
};

/// Metrics dimensions always enabled regardless of user config
/// (`{Operation}`).
pub fn metrics_always_enabled_dimensions() -> Vec<String> {
    vec![OPERATION_DIMENSION_NAME.to_string()]
}

/// Metrics dimensions always enabled, plus `ShardId` (`{Operation, ShardId}`).
pub fn metrics_always_enabled_dimensions_with_shard_id() -> Vec<String> {
    vec![
        OPERATION_DIMENSION_NAME.to_string(),
        SHARD_ID_DIMENSION_NAME.to_string(),
    ]
}

/// The "all dimensions" sentinel set (`{"ALL"}`).
pub fn metrics_dimensions_all() -> Vec<String> {
    vec![crate::metrics::METRICS_DIMENSIONS_ALL.to_string()]
}

/// User-facing configuration for KCL metrics; lazily constructs and caches the
/// appropriate [`MetricsFactory`] based on [`metrics_backend`](Self::metrics_backend).
///
/// Port of the Lombok `@Data @Accessors(fluent=true)` class. `cloud_watch_client`
/// and `namespace` are required (Java `final`); the rest have the Java defaults.
/// Fluent setters return `self` for chaining (mirroring the fluent accessors).
///
/// The [`metrics_factory`](Self::metrics_factory) method is hand-written to lazily
/// build and memoize the factory. Because [`CloudWatchMetricsFactory`] spawns a
/// background tokio task, it must be called within a tokio runtime.
pub struct MetricsConfig {
    cloud_watch_client: CloudWatchClient,
    namespace: String,
    metrics_buffer_time_millis: i64,
    metrics_max_queue_size: usize,
    metrics_level: MetricsLevel,
    metrics_enabled_dimensions: Vec<String>,
    publisher_flush_buffer: usize,
    metrics_backend: MetricsBackend,
    /// Optional custom OTel [`MeterProvider`] used when
    /// [`MetricsBackend::Otel`] is selected (Java's nullable `openTelemetry`
    /// field). If `None`, [`opentelemetry::global::meter_provider`] (the noop
    /// default until the application installs one) is used —
    /// matching Java's `GlobalOpenTelemetry.getOrNoop()` fallback.
    meter_provider: Option<Arc<dyn MeterProvider + Send + Sync>>,
    /// User-settable override + lazy cache of the metrics factory. Mirrors
    /// Java's single `metricsFactory` field, which doubles as both the custom
    /// override (when set via [`set_metrics_factory`](Self::set_metrics_factory))
    /// and the memoized lazily-built default.
    metrics_factory: Mutex<Option<Arc<dyn MetricsFactory + Send + Sync>>>,
}

impl MetricsConfig {
    /// Creates a config with the Java defaults: buffer 10000ms, max queue 10000,
    /// level `DETAILED`, dimensions `ALL`, flush buffer 200, backend
    /// `CLOUDWATCH`.
    pub fn new(cloud_watch_client: CloudWatchClient, namespace: impl Into<String>) -> Self {
        Self {
            cloud_watch_client,
            namespace: namespace.into(),
            metrics_buffer_time_millis: 10_000,
            metrics_max_queue_size: 10_000,
            metrics_level: MetricsLevel::Detailed,
            metrics_enabled_dimensions: metrics_dimensions_all(),
            publisher_flush_buffer: 200,
            metrics_backend: MetricsBackend::CloudWatch,
            meter_provider: None,
            metrics_factory: Mutex::new(None),
        }
    }

    // --- fluent getters (no get/set prefix, matching @Accessors(fluent=true)) ---

    pub fn cloud_watch_client(&self) -> &CloudWatchClient {
        &self.cloud_watch_client
    }
    pub fn namespace(&self) -> &str {
        &self.namespace
    }
    pub fn metrics_buffer_time_millis(&self) -> i64 {
        self.metrics_buffer_time_millis
    }
    pub fn metrics_max_queue_size(&self) -> usize {
        self.metrics_max_queue_size
    }
    pub fn metrics_level(&self) -> MetricsLevel {
        self.metrics_level
    }
    pub fn metrics_enabled_dimensions(&self) -> &[String] {
        &self.metrics_enabled_dimensions
    }
    pub fn publisher_flush_buffer(&self) -> usize {
        self.publisher_flush_buffer
    }
    pub fn metrics_backend(&self) -> MetricsBackend {
        self.metrics_backend
    }

    // --- fluent setters (return self for chaining) ---

    pub fn set_metrics_buffer_time_millis(mut self, v: i64) -> Self {
        self.metrics_buffer_time_millis = v;
        self
    }
    pub fn set_metrics_max_queue_size(mut self, v: usize) -> Self {
        self.metrics_max_queue_size = v;
        self
    }
    pub fn set_metrics_level(mut self, v: MetricsLevel) -> Self {
        self.metrics_level = v;
        self
    }
    pub fn set_metrics_enabled_dimensions(mut self, v: Vec<String>) -> Self {
        self.metrics_enabled_dimensions = v;
        self
    }
    pub fn set_publisher_flush_buffer(mut self, v: usize) -> Self {
        self.publisher_flush_buffer = v;
        self
    }
    pub fn set_metrics_backend(mut self, v: MetricsBackend) -> Self {
        self.metrics_backend = v;
        self
    }

    /// The optional custom OTel [`MeterProvider`] (Java's `openTelemetry`).
    pub fn meter_provider(&self) -> Option<&Arc<dyn MeterProvider + Send + Sync>> {
        self.meter_provider.as_ref()
    }

    /// Sets a custom OTel [`MeterProvider`] used when the
    /// [`MetricsBackend::Otel`] backend is selected. Mirrors Java's
    /// `openTelemetry(OpenTelemetry)` setter.
    pub fn set_meter_provider(mut self, v: Arc<dyn MeterProvider + Send + Sync>) -> Self {
        self.meter_provider = Some(v);
        self
    }

    /// Sets a custom [`MetricsFactory`], overriding backend selection. Mirrors
    /// Java's `metricsFactory(MetricsFactory)` setter — when set, this factory
    /// is returned directly by [`metrics_factory`](Self::metrics_factory)
    /// regardless of [`metrics_backend`](Self::metrics_backend).
    pub fn set_metrics_factory(self, v: Arc<dyn MetricsFactory + Send + Sync>) -> Self {
        *self.metrics_factory.lock().unwrap() = Some(v);
        self
    }

    /// Lazily constructs and memoizes the metrics factory for the configured
    /// backend. Port of the hand-written `metricsFactory()` getter.
    ///
    /// If a custom factory was set via
    /// [`set_metrics_factory`](Self::set_metrics_factory), it is returned
    /// directly. Otherwise a [`CloudWatchMetricsFactory`] or an
    /// [`OtelMetricsFactory`] is built (and memoized) per
    /// [`metrics_backend`](Self::metrics_backend). For the OTel backend, the
    /// configured [`MeterProvider`] is used, or
    /// [`opentelemetry::global::meter_provider`] if none was set (Java's
    /// `GlobalOpenTelemetry.getOrNoop()` fallback).
    pub fn metrics_factory(&self) -> Arc<dyn MetricsFactory + Send + Sync> {
        let mut guard = self.metrics_factory.lock().unwrap();
        if let Some(factory) = guard.as_ref() {
            return factory.clone();
        }
        let enabled_dimensions: HashSet<String> =
            self.metrics_enabled_dimensions.iter().cloned().collect();
        let factory: Arc<dyn MetricsFactory + Send + Sync> = match self.metrics_backend {
            MetricsBackend::Otel => {
                let provider = self
                    .meter_provider
                    .clone()
                    .unwrap_or_else(opentelemetry::global::meter_provider);
                Arc::new(OtelMetricsFactory::new(
                    provider,
                    self.metrics_level,
                    enabled_dimensions,
                ))
            }
            MetricsBackend::CloudWatch => Arc::new(CloudWatchMetricsFactory::new(
                self.cloud_watch_client.clone(),
                self.namespace.clone(),
                self.metrics_buffer_time_millis,
                self.metrics_max_queue_size,
                self.metrics_level,
                Some(self.metrics_enabled_dimensions.clone()),
                self.publisher_flush_buffer,
            )),
        };
        *guard = Some(factory.clone());
        factory
    }
}

#[cfg(test)]
mod tests {
    //! Port of `OtelMetricsConfigTest`.
    use super::*;
    use crate::metrics::{CloudWatchMetricsFactory, MetricsScope, OtelMetricsFactory};
    use opentelemetry::metrics::noop::NoopMeterProvider;

    const NAMESPACE: &str = "TestApp";

    fn cloud_watch_client() -> CloudWatchClient {
        CloudWatchClient::from_conf(
            aws_sdk_cloudwatch::Config::builder()
                .behavior_version(aws_sdk_cloudwatch::config::BehaviorVersion::latest())
                .region(aws_sdk_cloudwatch::config::Region::new("us-east-1"))
                .build(),
        )
    }

    fn config() -> MetricsConfig {
        MetricsConfig::new(cloud_watch_client(), NAMESPACE)
    }

    /// A trivial custom factory (stands in for the Java `mock(MetricsFactory.class)`).
    struct CustomFactory;
    impl MetricsFactory for CustomFactory {
        fn create_metrics(&self) -> Box<dyn MetricsScope + Send> {
            Box::new(crate::metrics::NullMetricsScope::new())
        }
        fn as_any(&self) -> &dyn std::any::Any {
            self
        }
    }

    /// Default backend is CLOUDWATCH, creates a `CloudWatchMetricsFactory`.
    #[tokio::test]
    async fn test_default_backend_is_cloud_watch() {
        let config = config();
        let factory = config.metrics_factory();
        assert!(
            factory.as_any().is::<CloudWatchMetricsFactory>(),
            "Default backend should create CloudWatchMetricsFactory"
        );
        // Shut down the spawned publisher task cleanly.
        if let Some(cw) = factory.as_any().downcast_ref::<CloudWatchMetricsFactory>() {
            cw.shutdown().await;
        }
    }

    /// CLOUDWATCH backend explicitly set still creates a `CloudWatchMetricsFactory`.
    #[tokio::test]
    async fn test_cloud_watch_backend_creates_cloud_watch_factory() {
        let config = config().set_metrics_backend(MetricsBackend::CloudWatch);
        let factory = config.metrics_factory();
        assert!(
            factory.as_any().is::<CloudWatchMetricsFactory>(),
            "CLOUDWATCH backend should create CloudWatchMetricsFactory"
        );
        if let Some(cw) = factory.as_any().downcast_ref::<CloudWatchMetricsFactory>() {
            cw.shutdown().await;
        }
    }

    /// OTEL backend creates an `OtelMetricsFactory` without any endpoint/resource
    /// attributes configured.
    #[test]
    fn test_otel_backend_creates_otel_factory_without_endpoint_or_resource_attributes() {
        let config = config().set_metrics_backend(MetricsBackend::Otel);
        let factory = config.metrics_factory();
        assert!(
            factory.as_any().is::<OtelMetricsFactory>(),
            "OTEL backend should create OtelMetricsFactory"
        );
    }

    /// OTEL backend uses the provided `MeterProvider` instance.
    #[test]
    fn test_otel_backend_uses_provided_open_telemetry_instance() {
        let config = config()
            .set_metrics_backend(MetricsBackend::Otel)
            .set_meter_provider(Arc::new(NoopMeterProvider::new()));
        let factory = config.metrics_factory();
        assert!(
            factory.as_any().is::<OtelMetricsFactory>(),
            "OTEL backend with a provided MeterProvider should create OtelMetricsFactory"
        );
    }

    /// OTEL backend falls back to the global `MeterProvider` when none is
    /// provided (verify it does not panic and still builds an OtelMetricsFactory).
    #[test]
    fn test_otel_backend_uses_global_open_telemetry_when_no_instance_provided() {
        let config = config().set_metrics_backend(MetricsBackend::Otel);
        // meter_provider is None — should fall back to global::meter_provider().
        let factory = config.metrics_factory();
        assert!(factory.as_any().is::<OtelMetricsFactory>());
    }

    /// A custom metrics factory overrides backend selection.
    #[test]
    fn test_custom_factory_overrides_backend() {
        let custom: Arc<dyn MetricsFactory + Send + Sync> = Arc::new(CustomFactory);
        let config = config()
            .set_metrics_backend(MetricsBackend::Otel)
            .set_metrics_factory(custom.clone());
        let factory = config.metrics_factory();
        assert!(
            Arc::ptr_eq(&factory, &custom),
            "Custom factory should be used when explicitly set"
        );
    }

    /// A custom metrics factory overrides the default CLOUDWATCH backend too.
    #[test]
    fn test_custom_factory_overrides_default_backend() {
        let custom: Arc<dyn MetricsFactory + Send + Sync> = Arc::new(CustomFactory);
        let config = config().set_metrics_factory(custom.clone());
        let factory = config.metrics_factory();
        assert!(
            Arc::ptr_eq(&factory, &custom),
            "Custom factory should override the default CLOUDWATCH backend"
        );
    }
}
